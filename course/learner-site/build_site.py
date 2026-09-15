#!/usr/bin/env python3
"""Build the static learner site from the course decks + the narration manifest.

  python3 build_site.py            # write index.html and mNN.html into the site root
  python3 build_site.py --check    # verify the site is buildable and matches the manifest

The site is plain HTML + two small scripts. There is no framework and no build step to install:
the course repo already has no runtime dependency, and adding Ruby or a bundler to *read a course*
would be a step backwards. The generated HTML is a derived artifact and is gitignored; the source
of truth is the deck Markdown plus `narration/manifest.json`.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "06-production" / "slides"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "06-production" / "narration"))

from deck_lint import split_slides                      # noqa: E402
from captions import words
from narration_data import (COURSE_DIR, DECK_IDS, EDITION, MANIFEST_PATH, PROVENANCE_PATH,  # noqa: E402
                            SITE_ROOT, load_manifest, load_scripts, read_json, write_json)

# Our decks already write `M0.1 — Real title` and `Type 1 — Real title`, which is exactly the
# kicker/title split ai_qe uses (`02 / Strategic target state`). Only an em dash splits: an en dash
# inside "Stages 1–3" must stay part of the label.
KICKER_RE = re.compile(
    r"^(M\d+(?:\.\d+)?|Type\s+\d+|Lab\s+M\d+|Segment\s+M\d+(?:\.\d+)?|"
    r"Stages?\s+\d+\s*[–-]\s*\d+|Proof|Part\s+\d+|Step\s+\d+)\s+—\s+(.+)$")
DECK_LABEL_RE = re.compile(r"^(M\d+)\s*—\s*(.+)$")

NOTES_RE = re.compile(r"<!--\s*NOTES:(.*?)-->", re.DOTALL)
DIRECTIVE_RE = re.compile(r"<!--\s*(_class|_footer|_paginate|_header)\s*:\s*([^>]*?)\s*-->")
FENCE_RE = re.compile(r"^```")
INLINE_CODE = re.compile(r"`([^`]+)`")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
ITALIC = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


# ---------------------------------------------------------------- inline + block markdown

def inline(text: str) -> str:
    """Escape, then re-introduce the small inline subset the decks actually use."""
    out = html.escape(text, quote=False)
    out = INLINE_CODE.sub(lambda m: f"<code>{m.group(1)}</code>", out)
    out = BOLD.sub(lambda m: f"<strong>{m.group(1)}</strong>", out)
    out = ITALIC.sub(lambda m: f"<em>{m.group(1)}</em>", out)
    out = LINK.sub(lambda m: f'<a href="{html.escape(m.group(2), quote=True)}">{m.group(1)}</a>', out)
    return out


def render_blocks(lines: list[str]) -> str:
    """Render the block subset: fenced code, tables, quotes, lists, headings, paragraphs."""
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        if FENCE_RE.match(stripped):
            body, i = [], i + 1
            while i < len(lines) and not FENCE_RE.match(lines[i].strip()):
                body.append(html.escape(lines[i]))
                i += 1
            i += 1
            out.append("<pre><code>" + "\n".join(body) + "</code></pre>")
            continue
        if stripped.startswith("|"):
            rows, i = [], i
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            header = rows[0] if rows else []
            body = [r for r in rows[1:] if not all(set(c) <= set("-: ") for c in r)]
            table = ["<table>"]
            if header:
                table.append("<thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in header) + "</tr></thead>")
            table.append("<tbody>")
            for row in body:
                table.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>")
            table.append("</tbody></table>")
            out.append("".join(table))
            continue
        if stripped.startswith("> "):
            quote, i = [], i
            while i < len(lines) and lines[i].strip().startswith("> "):
                quote.append(lines[i].strip()[2:])
                i += 1
            out.append("<blockquote>" + render_blocks(quote) + "</blockquote>")
            continue
        match_ul = re.match(r"^(\s*)[-*+]\s+(.*)$", line)
        match_ol = re.match(r"^(\s*)\d+\.\s+(.*)$", line)
        if match_ul or match_ol:
            ordered = bool(match_ol)
            items, i = [], i
            pattern = r"^\s*\d+\.\s+(.*)$" if ordered else r"^\s*[-*+]\s+(.*)$"
            while i < len(lines):
                m = re.match(pattern, lines[i])
                if not m:
                    break
                items.append(inline(m.group(1)))
                i += 1
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{item}</li>" for item in items) + f"</{tag}>")
            continue
        heading = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if heading:
            level = len(heading.group(1))
            out.append(f"<h{level}>{inline(heading.group(2))}</h{level}>")
            i += 1
            continue
        # paragraph: absorb consecutive plain lines
        para, i = [], i
        while i < len(lines):
            nxt = lines[i].strip()
            if (not nxt or nxt.startswith(("|", ">", "#")) or FENCE_RE.match(nxt)
                    or re.match(r"^\s*[-*+]\s+", lines[i]) or re.match(r"^\s*\d+\.\s+", lines[i])):
                break
            para.append(nxt)
            i += 1
        out.append("<p>" + inline(" ".join(para)) + "</p>")
    return "\n".join(out)


def module_tag(deck_id: str, label: str) -> str:
    """`M0 · Orientation` — the standing kicker for slides that carry no section label of their own."""
    match = DECK_LABEL_RE.match(label.strip())
    tag, rest = (match.group(1), match.group(2)) if match else (deck_id.upper(), label.strip())
    rest = rest.strip()
    if len(rest) > 34 and ":" in rest:
        rest = rest.split(":")[0].strip()
    return f"{tag} · {rest}"


def split_kicker(title: str, fallback: str) -> tuple[str, str]:
    """Return (kicker, title) for a slide heading."""
    match = KICKER_RE.match(title.strip())
    if match:
        kicker = re.sub(r"^Segment\s+", "", match.group(1).strip())
        return kicker, match.group(2).strip()
    return fallback, title.strip()


# ---------------------------------------------------------------- deck parsing

def parse_deck(deck_id: str, scripts: dict | None = None) -> dict:
    matches = sorted(COURSE_DIR.glob(f"03-content/{deck_id}-*/slides.md"))
    if not matches:
        raise SystemExit(f"{deck_id}: no slides.md found")
    source = matches[0]
    front, slide_texts = split_slides(source.read_text(encoding="utf-8"))
    label = front.get("title", deck_id.upper())
    standing = module_tag(deck_id, label)
    slides = []
    chapter = "Opening"
    for index, raw in enumerate(slide_texts, 1):
        notes_match = NOTES_RE.search(raw)
        notes = notes_match.group(1).strip() if notes_match else ""
        classes = [m.group(2) for m in DIRECTIVE_RE.finditer(raw) if m.group(1) == "_class"]
        body = NOTES_RE.sub("", DIRECTIVE_RE.sub("", raw)).strip()
        title_match = re.search(r"^#{1,4}\s+(.*)$", body, re.MULTILINE)
        raw_title = title_match.group(1).strip() if title_match else f"Slide {index}"
        # The heading becomes the slide's own chrome, so keep it out of the rendered body.
        content_body = re.sub(r"^#{1,4}\s+.*$", "", body, count=1, flags=re.MULTILINE).strip()
        rendered = render_blocks(content_body.splitlines())
        cover = index == 1
        if cover:
            # The opening slide is a title slide: the deck's own name, not a section label.
            deck_match = DECK_LABEL_RE.match(raw_title)
            kicker = f"AI Product Studio · Module {int(deck_id[1:])} of {len(DECK_IDS)}"
            title = deck_match.group(2).strip() if deck_match else raw_title
        else:
            kicker, title = split_kicker(raw_title, standing)
            if re.fullmatch(r"M\d+\.\d+", kicker):
                chapter = kicker            # a segment heading opens a new chapter, carried forward
        # The approved narration is the source of truth for anything spoken; the deck Markdown is
        # the source of truth for what is displayed.
        script_text = ((scripts or {}).get(deck_id, {}).get("slides", {})
                       .get(f"slide-{index}", {}).get("text", "").strip())
        slides.append({
            "id": f"slide-{index}",
            "number": index,
            "title": title,
            "full_title": raw_title,
            "kicker": kicker,
            "chapter": chapter,
            "cover": cover,
            "classes": classes,
            "notes": notes,
            "html": rendered,
            "script_text": script_text,
        })
    return {
        "id": deck_id,
        "label": label,
        "module_tag": standing,
        "source": str(source.relative_to(COURSE_DIR)),
        "slides": slides,
    }


def _deck_voice(deck_id: str, manifest: dict, provenance: dict) -> tuple[str, int]:
    """Return (voice label, number of preview recordings) for a deck."""
    entries = (manifest.get("decks", {}).get(deck_id, {}) or {}).get("slides", {})
    prov = {r.get("audio"): r for r in provenance.get("recordings", [])}
    preview = sum(1 for e in entries.values()
                  if prov.get(e.get("audio"), {}).get("basis") == "sentence-measured-preview")
    label = next((e.get("voice") for e in entries.values() if e.get("voice")), "")
    return label, preview


def _slide_heading(deck: dict, slide: dict) -> str:
    """Slide 1 is usually titled after the deck itself; do not say it twice.

    Uses the unsplit heading: the transcript has no kicker column, so "M0.1 — Three archetypes"
    must survive here even though the slide chrome separates the two.
    """
    title = slide.get("full_title", slide["title"]).strip()
    if title.split("—")[-1].strip().casefold() == deck["label"].split("—")[-1].strip().casefold():
        return f"Slide {slide['number']}"
    return f"Slide {slide['number']} — {title}"


def transcript_markdown(deck: dict, manifest: dict, provenance: dict) -> str:
    """A readable transcript of the narration for one deck.

    Convention: a line starting with "> " is spoken narration and nothing else. Headings, timing and
    the voice note are ordinary lines, so `words()` over the blockquotes must equal `words()` over the
    approved script. Do not put metadata in a blockquote here.

    The spoken words are the approved script — the same words the captions must match — so this file
    is a text alternative to the audio, not a summary of it. Narration is emitted as blockquotes so
    the words that are *spoken* are mechanically separable from the metadata around them; that is what
    lets `validate_narration.py` prove the transcript still matches the script word for word.

    Speaker notes are deliberately excluded: they are the presenter's version, not the narration.
    """
    entries = (manifest.get("decks", {}).get(deck["id"], {}) or {}).get("slides", {})
    voice, preview = _deck_voice(deck["id"], manifest, provenance)
    total = sum(float(e.get("duration", 0) or 0) for e in entries.values())
    out = [f"# {deck['label']}", "", "## Narration transcript", ""]
    out.append(f"**{len(deck['slides'])} slides · {len(entries)} narrated · "
               f"{int(total // 60)}m {int(total % 60)}s of audio**")
    out.append("")
    if preview and preview == len(entries):
        out.append("**Voice:** preview narration — a free local voice, not the finished release "
                   "recording. The words below are the approved narration and do not change when the "
                   "release voice is recorded.")
    elif preview:
        out.append(f"**Voice:** mixed — {preview} of {len(entries)} recordings are preview audio; "
                   f"the rest were recorded separately. The words below are the approved narration.")
    elif voice:
        out.append(f"**Voice:** {voice}")
    out.append("")
    out.append("The text below is what is spoken on each slide, in order. It is the same text as the "
               "captions and the approved narration script, checked word for word by "
               "`course/06-production/narration/validate_narration.py`.")
    out.append("")
    out.append("---")
    out.append("")
    for slide in deck["slides"]:
        entry = entries.get(slide["id"])
        out.append(f"### {_slide_heading(deck, slide)}")
        out.append("")
        if entry:
            out.append(f"*{float(entry.get('duration', 0) or 0):.1f}s · "
                       f"{entry.get('caption_method', '')}*")
            out.append("")
        for paragraph in slide["script_text"].split("\n\n"):
            if paragraph.strip():
                out.append("> " + paragraph.strip())
                out.append("")
    return "\n".join(out).rstrip() + "\n"


def transcript_page(deck: dict, manifest: dict, provenance: dict, site_base: str) -> str:
    """The same transcript as a printable page on the site."""
    entries = (manifest.get("decks", {}).get(deck["id"], {}) or {}).get("slides", {})
    voice, preview = _deck_voice(deck["id"], manifest, provenance)
    total = sum(float(e.get("duration", 0) or 0) for e in entries.values())
    rows = []
    for slide in deck["slides"]:
        entry = entries.get(slide["id"])
        meta = (f'{slide["kicker"]} · {float(entry.get("duration", 0) or 0):.1f}s · '
                f'{entry.get("caption_method", "")}' if entry else f'{slide["kicker"]} · not recorded')
        rows.append(
            f'<section class="transcript-slide" id="{slide["id"]}">'
            f'<h2><a href="{site_base}/{deck["id"]}.html#{slide["id"]}">{_slide_heading(deck, slide)}</a></h2>'
            f'<p class="transcript-meta">{html.escape(meta)}</p>'
            f'<blockquote>{inline(slide["script_text"])}</blockquote></section>')

    if preview and preview == len(entries):
        note = ('<p class="voice-badge" role="note">Preview narration — a free local voice, not the '
                'finished release recording. These are the approved words and do not change when the '
                'release voice is recorded.</p>')
    elif preview:
        note = (f'<p class="voice-badge" role="note">Mixed — {preview} of {len(entries)} recordings '
                f'are preview audio. These are the approved words.</p>')
    else:
        note = ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(deck['label'])} — transcript</title>
<link rel="preload" href="{site_base}/assets/fonts/source-sans-3.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{site_base}/assets/player.css">
</head>
<body class="transcript">
<header class="transcript-head">
  <p class="kicker"><a href="{site_base}/index.html">AI Product Studio</a> · {html.escape(deck['module_tag'])}</p>
  <h1>{html.escape(deck['label'])} — transcript</h1>
  <p>{len(deck['slides'])} slides · {len(entries)} narrated · {int(total // 60)}m {int(total % 60)}s
     · <a href="{site_base}/{deck['id']}.html">open the narrated deck →</a></p>
  {note}
</header>
<main>
{chr(10).join(rows)}
</main>
</body>
</html>
"""


BRAND_MARK = ('<svg class="brand-mark" viewBox="0 0 32 32" aria-hidden="true" focusable="false">'
              '<rect width="32" height="32" rx="7" fill="#096d69"/>'
              '<path d="M9 21.6 16 9.4l7 12.2" fill="none" stroke="#85d5c4" stroke-width="2.3" '
              'stroke-linejoin="round" stroke-linecap="round"/>'
              '<path d="M12.3 18.3h7.4" stroke="#fcfcfa" stroke-width="2.3" stroke-linecap="round"/>'
              '</svg>')


def slide_footer(deck: dict, slide: dict, site_base: str) -> str:
    """One footer for every slide: what this is, where to read it, and where you are."""
    total = len(deck["slides"])
    return (f'<footer class="slide-footer">'
            f'<span class="deck-tag">AI Product Studio <span class="footer-divider">/</span> '
            f'{html.escape(deck["module_tag"])}</span>'
            f'<span class="footer-divider" aria-hidden="true">/</span>'
            f'<a href="{site_base}/transcript-{deck["id"]}.html#{slide["id"]}">Slide transcript</a>'
            f'<span class="footer-divider" aria-hidden="true">/</span>'
            f'<span class="slide-number" aria-label="Slide {slide["number"]} of {total}">'
            f'{slide["number"]:02d} / {total:02d}</span></footer>')


def slide_shell(deck: dict, slide: dict, manifest_entry: dict | None,
                site_base: str, cover_note: str = "") -> str:
    classes = ["slide"]
    if slide["cover"]:
        classes.append("slide-cover")
    elif "proof" in slide["classes"]:
        classes.append("slide-proof")          # the decks' evidence slides get a change of rhythm
    hidden = "" if slide["number"] == 1 else " hidden"
    media = ""
    if manifest_entry:
        media = (f' data-audio="{html.escape(manifest_entry["audio"], quote=True)}"'
                 f' data-captions="{html.escape(manifest_entry["captions"], quote=True)}"'
                 f' data-duration="{manifest_entry.get("duration", "")}"')
    content = f'<div class="slide-content">{slide["html"]}</div>'
    body = (f'<div class="cover-grid">{content}<aside class="cover-note">{cover_note}</aside></div>'
            if slide["cover"] else content)
    # Speaker notes travel with the slide so the drawer can read them without a second request.
    notes = html.escape(slide["notes"]) if slide["notes"] else ""
    return (f'<section class="{" ".join(classes)}" id="{slide["id"]}" data-number="{slide["number"]}"'
            f' data-chapter="{html.escape(slide["chapter"], quote=True)}"'
            f'{media}{hidden} aria-roledescription="slide" aria-labelledby="{slide["id"]}-title">'
            f'<p class="kicker">{html.escape(slide["kicker"])}</p>'
            f'<h2 id="{slide["id"]}-title">{inline(slide["title"])}</h2>'
            f'{body}'
            f'{slide_footer(deck, slide, site_base)}'
            f'<div class="slide-notes-source" hidden>{notes}</div>'
            f'</section>')


def page(deck: dict, manifest: dict, provenance: dict, site_base: str) -> str:
    deck_manifest = (manifest.get("decks", {}).get(deck["id"], {}) or {}).get("slides", {})
    prov_by_audio = {rec.get("audio"): rec for rec in provenance.get("recordings", [])}
    preview_count = sum(1 for e in deck_manifest.values()
                        if prov_by_audio.get(e.get("audio"), {}).get("basis") == "sentence-measured-preview")
    mixed = 0 < preview_count < len(deck_manifest)
    is_preview = preview_count > 0
    total = round(sum(float(e.get("duration", 0) or 0) for e in deck_manifest.values()), 1)
    recorded = len(deck_manifest)

    if is_preview and mixed:
        voice_chip = f'<span class="voice-chip is-preview">{preview_count} of {recorded} preview voice</span>'
    elif is_preview:
        voice_chip = '<span class="voice-chip is-preview">preview voice</span>'
    else:
        voice_chip = '<span class="voice-chip is-release">release voice</span>'

    cover_note = (f'<strong>{len(deck["slides"])} slides · {recorded} narrated</strong>'
                  f'<small>{int(total // 60)}m {int(total % 60)}s of narration with captions and transcript.'
                  f'{" Free preview voice — the release recording is pending." if is_preview else ""}'
                  f'</small>')
    sections = "\n".join(
        slide_shell(deck, slide, deck_manifest.get(slide["id"]), site_base, cover_note)
        for slide in deck["slides"])

    # Group the picker by chapter, the way the deck is actually structured.
    groups: list[tuple[str, list[dict]]] = []
    for slide in deck["slides"]:
        if not groups or groups[-1][0] != slide["chapter"]:
            groups.append((slide["chapter"], []))
        groups[-1][1].append(slide)
    options = "\n".join(
        f'<optgroup label="{html.escape(chapter)}">' + "".join(
            f'<option value="{s["id"]}">{s["number"]}. {html.escape(s["title"][:70])}</option>'
            for s in slides) + '</optgroup>'
        for chapter, slides in groups)

    if not is_preview:
        badge = ""
    elif mixed:
        badge = (f'<p class="voice-badge" role="note">{preview_count} of {recorded} recordings on this '
                 f'page are preview audio — a free local voice, not the finished release recording. '
                 f'The rest were recorded separately; each slide\'s transcript names its voice.</p>')
    else:
        badge = ('<p class="voice-badge" role="note">Preview narration — a free local voice, not the '
                 'finished release recording. The transcript is the approved narration and does not '
                 'change when the release voice is recorded.</p>')
    return f"""<!doctype html>
<html lang="en" class="js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(deck['label'])} — AI Product Studio</title>
<link rel="preload" href="{site_base}/assets/fonts/source-sans-3.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{site_base}/assets/player.css">
</head>
<body class="deck-page" data-narration-manifest="{site_base}/narration.json"
      data-narration-deck="{deck['id']}" data-site-base="{site_base}"
      data-voice="{'preview' if is_preview else 'release'}">
<a class="skip-link" href="#slides">Skip to slides</a>
<header class="deck-header">
  <a class="deck-brand" href="{site_base}/index.html">{BRAND_MARK}AI Product Studio<span class="brand-destination">{html.escape(deck['module_tag'])}</span></a>
  <span class="deck-audience">{len(deck['slides'])} slides · {recorded} narrated · {int(total // 60)}m {int(total % 60)}s</span>
  <div class="deck-tools">
    <button type="button" class="tool-primary" data-narration-start hidden aria-pressed="false">▶ Play narration</button>
    <button type="button" data-present aria-pressed="false" title="Full screen presentation">Present ↗</button>
    <button type="button" data-reading aria-pressed="false" title="Show every slide as a document">Read all</button>
    <button type="button" data-notes title="Presenter notes for this slide">Sources &amp; notes</button>
    <a class="tool-link" href="{site_base}/transcript-{deck['id']}.html">Transcript</a>
    {voice_chip}
  </div>
</header>
{badge}
<main id="slides" class="slides" tabindex="-1" aria-label="{html.escape(deck['label'])}">
<h1 class="sr-only">{html.escape(deck['label'])}</h1>
{sections}
</main>
<nav class="deck-navigation" aria-label="Slide navigation">
  <div class="deck-nav-controls">
    <button type="button" data-nav="prev" aria-label="Previous slide">←</button>
    <button type="button" data-nav="next" aria-label="Next slide">→</button>
  </div>
  <p class="slide-status" role="status" aria-live="polite" aria-atomic="true"></p>
  <label class="slide-picker-label">Go to slide
    <select data-slide-picker aria-label="Go to slide">{options}</select></label>
</nav>
<p class="deck-message" role="status"></p>
<dialog class="deck-drawer" aria-labelledby="drawer-title">
  <div class="drawer-heading">
    <h2 id="drawer-title">Speaker notes</h2>
    <button type="button" data-close-drawer aria-label="Close notes">Close ×</button>
  </div>
  <p class="drawer-meta" data-drawer-meta></p>
  <div class="drawer-notes" data-drawer-notes></div>
</dialog>
<noscript><style>.slide[hidden]{{display:block}}</style>
<p class="no-script">JavaScript is off, so narration and slide navigation are disabled. Every slide is
shown below in order and remains readable.</p></noscript>
<script src="{site_base}/assets/narration-media.js" defer></script>
<script src="{site_base}/assets/player.js" defer></script>
</body>
</html>
"""


def index_page(decks: list[dict], manifest: dict, provenance: dict, site_base: str) -> str:
    prov_by_audio = {rec.get("audio"): rec for rec in provenance.get("recordings", [])}
    cards = []
    grand_total = 0.0
    for deck in decks:
        entries = (manifest.get("decks", {}).get(deck["id"], {}) or {}).get("slides", {})
        total = sum(float(e.get("duration", 0) or 0) for e in entries.values())
        grand_total += total
        preview = any(prov_by_audio.get(e.get("audio"), {}).get("basis") == "sentence-measured-preview"
                      for e in entries.values())
        if preview:
            chip = '<span class="voice-chip is-preview">preview voice</span>'
        else:
            chip = '<span class="voice-chip is-release">release voice</span>'
        short = re.sub(r"^M\d+\s*—\s*", "", deck["label"]).strip()
        # A small waveform motif: one bar per chapter, so the cover is not a flat block.
        waves = "".join(
            f'<span style="height:{h}px"></span>' for h in (6, 11, 16, 9, 14, 7, 12))
        outline = "".join(
            f'<li><a href="{site_base}/{deck["id"]}.html#{s["id"]}">'
            f'{s["number"]}. {html.escape(s["title"][:64])}</a></li>'
            for s in deck["slides"][:8])
        cards.append(f"""<article class="room-card">
  <a class="room-cover" href="{site_base}/{deck['id']}.html">
    <span class="room-audience">Module {int(deck['id'][1:])} · {len(deck['slides'])} slides</span>
    <h3>{html.escape(short)}</h3>
    <span class="room-number">{int(total // 60)}m {int(total % 60)}s of narration</span>
    <span class="room-waves" aria-hidden="true">{waves}</span>
  </a>
  <div class="room-body">
    <p class="room-meta">{len(entries)} narrated · captions · transcript {chip}</p>
    <details><summary>See the slides</summary><ul>{outline}</ul></details>
    <div class="room-actions">
      <a class="btn-primary" href="{site_base}/{deck['id']}.html">Present this deck →</a>
      <a href="{site_base}/transcript-{deck['id']}.html">Read the transcript</a>
    </div>
  </div>
</article>""")

    all_recorded = sum(len((manifest.get("decks", {}).get(d, {}) or {}).get("slides", {})) for d in DECK_IDS)
    all_slides = sum(len(d["slides"]) for d in decks)
    status = ("Every slide is narrated." if all_recorded >= all_slides else
              f"{all_recorded} of {all_slides} slides narrated so far.")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Product Studio — narrated course</title>
<meta name="description" content="Build, ship and sell three kinds of AI product. Nine narrated modules with captions and transcripts.">
<link rel="preload" href="{site_base}/assets/fonts/source-sans-3.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{site_base}/assets/player.css">
</head>
<body class="index">
<header class="site-header">
  <div class="wrap">
    <a class="site-brand" href="{site_base}/index.html">{BRAND_MARK}AI Product Studio<span class="brand-destination">Course</span></a>
    <p class="eyebrow">Nine modules · 233 slides</p>
    <h1>Build, ship and sell three kinds of AI product.</h1>
    <p class="site-lede">Every module is narrated slide by slide, with captions, a readable transcript
      and a deck you can present. Built from three production repositories, and verified with the same
      evidence discipline it teaches.</p>
    <ul class="site-facts">
      <li>9 modules · 233 slides</li>
      <li>{int(grand_total // 60)} minutes of narration</li>
      <li>Captions on every slide</li>
      <li>{status}</li>
    </ul>
  </div>
</header>
<main class="site-main">
  <div class="section-heading">
    <h2>Open a module</h2>
    <span class="section-note">Each deck plays one slide at a time. Press play when you are ready.</span>
  </div>
  <div class="room-grid">
{chr(10).join(cards)}
  </div>
  <section class="how-to">
    <h2>How to use this site</h2>
    <ul>
      <li>Narration never autoplays — press <strong>Play narration</strong> on any deck.</li>
      <li>Captions are on by default. The full transcript is behind <strong>Transcript</strong>, and the
          <a href="{site_base}/transcripts/ALL.md">complete transcript</a> covers all nine modules in one file.</li>
      <li><strong>Present ↗</strong> goes full screen for a room; <strong>Read all</strong> turns the deck
          into one scrolling document; <strong>Sources &amp; notes</strong> opens the presenter notes.</li>
      <li>Keyboard: <kbd>→</kbd>/<kbd>Space</kbd> next, <kbd>←</kbd> previous, <kbd>Home</kbd>/<kbd>End</kbd>
          first/last, <kbd>Esc</kbd> close.</li>
      <li>Printing a deck prints one 16:9 slide per page.</li>
    </ul>
  </section>
  <p class="index-footnote">Speaker notes are the presenter's version; the narration is the learner's.
    Recordings currently use a free preview voice and say so wherever they appear — the released voice
    is recorded separately and the words do not change.</p>
</main>
</body>
</html>
"""


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="build into a temp dir and report only")
    parser.add_argument("--site-base", default=".",
                        help="prefix for asset URLs; '.' works from file:// and any subpath")
    args = parser.parse_args(argv)

    manifest = load_manifest()
    provenance = read_json(PROVENANCE_PATH, None) or {"recordings": []}
    scripts = load_scripts()
    decks = [parse_deck(deck_id, scripts["decks"]) for deck_id in DECK_IDS]

    target = Path("/tmp/aps-site-check") if args.check else SITE_ROOT
    target.mkdir(parents=True, exist_ok=True)
    if args.check:
        shutil.rmtree(target, ignore_errors=True)
        target.mkdir(parents=True)
    write_json(target / "narration.json", manifest)

    for deck in decks:
        (target / f"{deck['id']}.html").write_text(
            page(deck, manifest, provenance, args.site_base), encoding="utf-8")
        (target / f"transcript-{deck['id']}.html").write_text(
            transcript_page(deck, manifest, provenance, args.site_base), encoding="utf-8")
    (target / "index.html").write_text(
        index_page(decks, manifest, provenance, args.site_base), encoding="utf-8")

    # The transcripts are committed as Markdown, so a check must prove the committed copies still
    # match what the scripts say rather than quietly regenerating them.
    # Always the committed location: a check must compare against what is in the repository, not
    # against a copy it just wrote.
    transcript_dir = SITE_ROOT / "transcripts"
    if not args.check:
        transcript_dir.mkdir(parents=True, exist_ok=True)
    drift = []
    for deck in decks:
        text = transcript_markdown(deck, manifest, provenance)
        out = transcript_dir / f"{deck['id']}.md"
        if args.check:
            on_disk = out.read_text(encoding="utf-8") if out.is_file() else None
            if on_disk != text:
                drift.append(f"transcripts/{out.name}")
        else:
            out.write_text(text, encoding="utf-8")
        # A transcript that does not say exactly what the script says is a bug, not a formatting
        # difference: assert it here so it can never be committed wrong.
        spoken = words(" ".join(line.lstrip("> ").strip()
                                for line in text.splitlines() if line.startswith("> ")))
        approved = words(" ".join(s["script_text"] for s in deck["slides"]))
        if spoken != approved:
            raise SystemExit(f"{deck['id']}: transcript words do not match the approved script")

    combined = ["# AI Product Studio — complete narration transcript", "",
                "Every word spoken in the course, in order. The words are the approved narration "
                "scripts; they match the captions word for word and do not change when the release "
                "voice is recorded.", ""]
    for deck in decks:
        entries = (manifest.get("decks", {}).get(deck["id"], {}) or {}).get("slides", {})
        total = sum(float(e.get("duration", 0) or 0) for e in entries.values())
        combined.append(f"- [{deck['label']}](#{deck['id']}) — {len(deck['slides'])} slides, "
                        f"{int(total // 60)}m {int(total % 60)}s")
    combined.append("")
    for deck in decks:
        body = transcript_markdown(deck, manifest, provenance)
        body = "\n".join(body.splitlines()[2:])          # drop the repeated H1 and section heading
        combined.append(f'<a id="{deck["id"]}"></a>')
        combined.append("")
        combined.append(f"# {deck['label']}")
        combined.append(body.strip())
        combined.append("")
    all_text = "\n".join(combined).rstrip() + "\n"
    out = transcript_dir / "ALL.md"
    if args.check:
        if not out.is_file() or out.read_text(encoding="utf-8") != all_text:
            drift.append(f"transcripts/{out.name}")
    else:
        out.write_text(all_text, encoding="utf-8")

    if args.check and drift:
        print("transcripts are stale: " + ", ".join(str(d) for d in drift))
        print("run `make -C .. transcripts` to regenerate them")
        return 1

    total_slides = sum(len(d["slides"]) for d in decks)
    scripted = sum(len(v["slides"]) for v in scripts["decks"].values())
    recorded = sum(len((manifest.get("decks", {}).get(d, {}) or {}).get("slides", {}))
                   for d in scripts["decks"])
    transcript_words = sum(len(s["script_text"].split()) for d in decks for s in d["slides"])
    print(f"site written to {target}")
    print(f"  decks: {len(decks)} · slides: {total_slides} · scripted: {scripted} · recorded: {recorded}")
    print(f"  transcripts: {len(decks)} decks · {transcript_words:,} words"
          f"{' (verified against the approved scripts)' if args.check else ''}")
    if recorded < scripted:
        print(f"  note: {scripted - recorded} slides have no recording yet — "
              f"run `python3 ../06-production/narration/generate_narration.py generate --provider say`")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
