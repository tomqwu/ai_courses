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
DIRECTIVE_RE = re.compile(r"<!--\s*(_class|_footer|_paginate|_header|_diagram)\s*:\s*([^>]*?)\s*-->")
OTHER_DIRECTIVE_RE = re.compile(r"<!--\s*(_class|_footer|_paginate|_header)\s*:\s*[^>]*?-->")
DIAGRAM_AT = re.compile(r"<!--\s*_diagram\s*:\s*([^>]*?)\s*-->")
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


LABEL_CAPTION = re.compile(r"^(.*?)(?::\s+|\s+—\s+)(.*)$", re.DOTALL)


def _label_caption(raw: str) -> tuple[str, str]:
    """`Study: research…` and `**Host check** — loopback…` both split into node label + caption."""
    m = LABEL_CAPTION.match(raw.strip())
    return (m.group(1).strip(), m.group(2).strip()) if m else (raw.strip(), "")


def render_diagram(kind: str, items: list[str], ordered: bool) -> str:
    """Render a slide's own list as a diagram component.

    The words are frozen — they come from the same bullets the author wrote — only the
    arrangement is declared. `flow`/`loop` chain the items; `steps` stacks them numbered;
    `grid` lays parallel items out as cards; `stack` keeps row order and draws the
    connectors the hand-typed ASCII was faking (│ ▼) with CSS.
    """
    if kind in ("flow", "loop"):
        nodes = []
        for raw in items:
            label, caption = _label_caption(raw)
            cap = (f'<span class="d-caption">{inline(caption)}</span>' if caption else "")
            nodes.append(f'<li class="d-node"><span class="d-label">{inline(label)}</span>{cap}</li>')
        extra = " diagram-loop" if kind == "loop" else ""
        return f'<ol class="diagram diagram-flow{extra}">' + "".join(nodes) + "</ol>"
    if kind == "steps":
        rows = []
        for raw in items:
            label, caption = _label_caption(raw)
            # Inline, not under: eight labelled rows stack twice as tall when the caption
            # wraps to its own line, and the slide frame is 16:9 with overflow hidden.
            cap = (f'<span class="d-caption"> — {inline(caption)}</span>' if caption else "")
            # One grid cell for the whole step body: two sibling spans would put the caption
            # on its own implicit grid row, doubling the height of every labelled step.
            rows.append(f'<li><span class="d-step-body">'
                        f'<span class="d-label">{inline(label)}</span>{cap}'
                        f"</span></li>")
        return '<ol class="diagram diagram-steps">' + "".join(rows) + "</ol>"
    if kind == "grid":
        cards = []
        for raw in items:
            label, caption = _label_caption(raw)
            cap = (f'<p class="d-caption">{inline(caption)}</p>' if caption else "")
            cards.append(f'<li class="d-card"><span class="d-label">{inline(label)}</span>{cap}</li>')
        return '<ul class="diagram diagram-grid">' + "".join(cards) + "</ul>"
    if kind == "stack":
        rows = []
        for raw in items:
            if " → " in raw:
                chips = "".join(f'<span class="d-chip">{inline(c.strip())}</span>'
                                for c in raw.split("→"))
                rows.append(f'<li class="d-row d-chain">{chips}</li>')
            elif raw.strip().lower().startswith("seam"):
                rows.append(f'<li class="d-row d-seam">{inline(raw)}</li>')
            else:
                rows.append(f'<li class="d-row">{inline(raw)}</li>')
        return '<ul class="diagram diagram-stack">' + "".join(rows) + "</ul>"
    raise SystemExit(f"unknown diagram kind: {kind}")


def render_blocks(lines: list[str], diagram: str = "") -> str:
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
                items.append(m.group(1))
                i += 1
            if diagram:
                out.append(render_diagram(diagram, items, ordered))
                diagram = ""
            else:
                tag = "ol" if ordered else "ul"
                out.append(f"<{tag}>" + "".join(f"<li>{inline(item)}</li>" for item in items) + f"</{tag}>")
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
        diagram = next((m.group(2).strip() for m in DIRECTIVE_RE.finditer(raw)
                        if m.group(1) == "_diagram"), "")
        # _diagram survives the strip so its position is known: it upgrades the next list at
        # that point in the slide, not the first list on the slide.
        body = NOTES_RE.sub("", OTHER_DIRECTIVE_RE.sub("", raw)).strip()
        title_match = re.search(r"^#{1,4}\s+(.*)$", body, re.MULTILINE)
        raw_title = title_match.group(1).strip() if title_match else f"Slide {index}"
        # The heading becomes the slide's own chrome, so keep it out of the rendered body.
        content_body = re.sub(r"^#{1,4}\s+.*$", "", body, count=1, flags=re.MULTILINE).strip()
        d_match = DIAGRAM_AT.search(content_body)
        if d_match:
            head = content_body[:d_match.start()].strip()
            tail = content_body[d_match.end():].strip()
            rendered = ((render_blocks(head.splitlines()) + "\n") if head else "") \
                + render_blocks(tail.splitlines(), diagram=d_match.group(1).strip())
        else:
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
            "diagram": diagram,
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


def transcript_page(deck: dict, manifest: dict, provenance: dict, site_base: str,
                    text_only: bool = False) -> str:
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

    if text_only:
        note = ('<p class="voice-badge" role="note"><strong>Text-first copy.</strong> The narration '
                'and captions are not published here. These are the approved words and are complete.</p>')
    elif preview and preview == len(entries):
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


def slide_rail(deck: dict, slide: dict, site_base: str) -> str:
    """The spine: what this is, where you are, and where to read it.

    The rail spans the full frame height on purpose. The layout audit found the content area a median
    45% filled with the text sitting in the top-left corner of a large empty frame — leftover
    whitespace. A full-height spine frames that space instead, and the body block is optically
    centred against it.
    """
    total = len(deck["slides"])
    # A running head, as a book would carry one: every page but the title page.
    brand = "" if slide["cover"] else '<p class="rail-brand">AI Product Studio</p>'
    # When a slide has no segment kicker the parser falls back to the module tag; don't print it twice.
    module = ("" if slide["kicker"] == deck["module_tag"]
              else f'<p class="rail-module">{html.escape(deck["module_tag"])}</p>')
    return (f'<div class="slide-rail">'
            f'<div class="rail-head">'
            f'<p class="kicker">{html.escape(slide["kicker"])}</p>'
            f'{brand}'
            f'{module}'
            f'</div>'
            f'<div class="rail-foot">'
            f'<span class="slide-number" aria-label="Slide {slide["number"]} of {total}">'
            f'{slide["number"]:02d} / {total:02d}</span>'
            f'<a class="rail-link" '
            f'href="{site_base}/transcript-{deck["id"]}.html#{slide["id"]}">Slide transcript</a>'
            f'<a class="rail-link" '
            f'href="{site_base}/module-{deck["id"]}.html">Module overview</a>'
            f'</div></div>')


def slide_cta(deck: dict, slide: dict, site_base: str) -> str:
    """The unit's next step, on the slide that opens it: the lab checklist or the knowledge check."""
    title = slide.get("full_title", slide["title"])
    if re.match(r"^Lab\s+M\d+", title) or re.match(r"^Lab\s+M\d+", slide["kicker"]):
        return (f'<p class="slide-cta"><a href="{site_base}/lab-{deck["id"]}.html">'
                f'Open the lab checklist →</a></p>')
    if re.match(r"^Quiz\s+M\d+", title):
        return (f'<p class="slide-cta"><a href="{site_base}/quiz-{deck["id"]}.html">'
                f'Take the knowledge check →</a></p>')
    return ""


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
    # The body is one block, centred in the frame: title, content, and — on the cover — the
    # standing metadata about the deck.
    cover_meta = f'<p class="lede cover-meta">{cover_note}</p>' if slide["cover"] else ""
    # Speaker notes travel with the slide so the drawer can read them without a second request.
    notes = html.escape(slide["notes"]) if slide["notes"] else ""
    return (f'<section class="{" ".join(classes)}" id="{slide["id"]}" data-number="{slide["number"]}"'
            f' data-chapter="{html.escape(slide["chapter"], quote=True)}"'
            f'{media}{hidden} aria-roledescription="slide" aria-labelledby="{slide["id"]}-title">'
            f'{slide_rail(deck, slide, site_base)}'
            f'<div class="slide-body">'
            f'<h2 id="{slide["id"]}-title">{inline(slide["title"])}</h2>'
            f'<div class="slide-content">{slide["html"]}</div>'
            f'{slide_cta(deck, slide, site_base)}'
            f'{cover_meta}'
            f'</div>'
            f'<div class="slide-notes-source" hidden>{notes}</div>'
            f'</section>')


def page(deck: dict, manifest: dict, provenance: dict, site_base: str,
         text_only: bool = False, units: list[dict] | None = None) -> str:
    deck_manifest = (manifest.get("decks", {}).get(deck["id"], {}) or {}).get("slides", {})
    prov_by_audio = {rec.get("audio"): rec for rec in provenance.get("recordings", [])}
    preview_count = sum(1 for e in deck_manifest.values()
                        if prov_by_audio.get(e.get("audio"), {}).get("basis") == "sentence-measured-preview")
    mixed = 0 < preview_count < len(deck_manifest)
    is_preview = preview_count > 0
    total = round(sum(float(e.get("duration", 0) or 0) for e in deck_manifest.values()), 1)
    recorded = len(deck_manifest)
    if text_only:
        # The recordings exist but are not part of the published copy. The player must see no
        # recordings at all, or it would offer a Play button that fetches files which are not there.
        deck_manifest = {}

    if text_only:
        voice_chip = '<span class="voice-chip is-text">text-first</span>'
    elif is_preview and mixed:
        voice_chip = f'<span class="voice-chip is-preview">{preview_count} of {recorded} preview voice</span>'
    elif is_preview:
        voice_chip = '<span class="voice-chip is-preview">preview voice</span>'
    else:
        voice_chip = '<span class="voice-chip is-release">release voice</span>'

    if text_only:
        cover_note = (f'<strong>{len(deck["slides"])} slides</strong>'
                      f'<small>Narration is not published with this copy; every slide carries a '
                      f'complete transcript.</small>')
    else:
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

    if text_only:
        badge = ('<p class="voice-badge" role="note"><strong>Text-first copy.</strong> The narration '
                 'and captions are not published here, so there is no audio to play and Play '
                 'narration is off. Every transcript is the complete approved narration.</p>')
    elif not is_preview:
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
      data-voice="{'preview' if is_preview else 'release'}"
      data-units="{html.escape(json.dumps([{'id': u['id'], 'first': u['first'], 'last': u['last'], 'label': u['title'] if u['kind'] == 'segment' else u['label']} for u in (units or [])]), quote=True)}"
      data-deck-label="{html.escape(deck['label'], quote=True)}">
<a class="skip-link" href="#slides">Skip to slides</a>
<header class="deck-header">
  <a class="deck-brand" href="{site_base}/index.html">{BRAND_MARK}AI Product Studio<span class="brand-destination">{html.escape(deck['module_tag'])}</span></a>
  <span class="deck-audience">{len(deck['slides'])} slides{' · text-first copy' if text_only else f" · {recorded} narrated · {int(total // 60)}m {int(total % 60)}s"}</span>
  <div class="deck-tools">
    <button type="button" class="tool-primary" data-narration-start hidden aria-pressed="false">▶ Play narration</button>
    <button type="button" data-present aria-pressed="false" title="Full screen presentation">Present ↗</button>
    <button type="button" data-reading aria-pressed="false" title="Show every slide as a document">Read all</button>
    <button type="button" data-notes title="Presenter notes for this slide">Sources &amp; notes</button>
    <a class="tool-link" href="{site_base}/lesson-{deck['id']}.html">Lesson</a>
    <a class="tool-link" href="{site_base}/lab-{deck['id']}.html">Lab</a>
    <a class="tool-link" href="{site_base}/quiz-{deck['id']}.html">Knowledge check</a>
    <a class="tool-link" href="{site_base}/transcript-{deck['id']}.html">Transcript</a>
    <button type="button" class="search-button" data-search-open title="Search the course (press /)">Search <kbd>/</kbd></button>
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
<script src="{site_base}/assets/progress.js" defer></script>
<script src="{site_base}/assets/narration-media.js" defer></script>
<script src="{site_base}/assets/player.js" defer></script>
<script src="{site_base}/assets/search.js" defer></script>
</body>
</html>
"""


def index_page(decks: list[dict], manifest: dict, provenance: dict, site_base: str,
               text_only: bool = False, path_cards: str = "",
               module_paths: dict[str, int] | None = None,
               units_by_deck: dict[str, list[dict]] | None = None,
               proof_html: str = "", subscribe_action: str = "") -> str:
    # The sign-up form posts to whatever mailing provider the operator configures at build time.
    # With none configured the form is shown disabled and says so, rather than silently posting
    # into the void and telling a visitor their address was taken.
    configured = bool(subscribe_action)
    capture_html = f"""  <section class="capture" id="stay">
    <div class="capture-inner">
      <h2>The 30-minute teardown, in three emails</h2>
      <p>How three shipped products make their claims checkable: a privacy guarantee that fails
         closed, a SaaS built by agents under written rules, and an expertise site that cites itself.
         One email a day for three days, then the checklist. No other mail.</p>
      <form class="capture-form" method="post" action="{html.escape(subscribe_action)}"{"" if configured else " data-unconfigured"}>
        <label class="sr-only" for="aps-email">Your email address</label>
        <input id="aps-email" type="email" name="email" required autocomplete="email"
               placeholder="you@example.com" spellcheck="false"{"" if configured else " disabled"}>
        <button class="btn-primary" type="submit"{"" if configured else " disabled"}>Send me the teardown</button>
        <label class="capture-consent">
          <input type="checkbox" name="consent" value="yes" required{"" if configured else " disabled"}>
          <span>Yes, email me the three-part teardown and occasional notes about the course. I can
                unsubscribe from any email, and my address is not shared or sold.</span>
        </label>
      </form>
      {"" if configured else '<p class="capture-note">No mailing provider is configured for this build, so the form is disabled. Build the site with <code>--subscribe-action &lt;form url&gt;</code> to turn it on.</p>'}
    </div>
  </section>"""
    prov_by_audio = {rec.get("audio"): rec for rec in provenance.get("recordings", [])}
    cards = []
    grand_total = 0.0
    for deck in decks:
        entries = (manifest.get("decks", {}).get(deck["id"], {}) or {}).get("slides", {})
        total = sum(float(e.get("duration", 0) or 0) for e in entries.values())
        grand_total += total
        preview = any(prov_by_audio.get(e.get("audio"), {}).get("basis") == "sentence-measured-preview"
                      for e in entries.values())
        if text_only:
            chip = '<span class="voice-chip is-text">text-first</span>'
        elif preview:
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
        # Modules are shared between paths — M0 and M1 open all three — so the card says how many
        # paths a module belongs to rather than implying it has one home.
        shared_n = (module_paths or {}).get(deck["id"], 0)
        shared_chip = (f'<span class="voice-chip is-shared">shared · {shared_n} paths</span>'
                       if shared_n > 1 else "")
        module_href = f"{site_base}/module-{deck['id']}.html"
        unit_ids = ",".join(f"{deck['id']}:{u['id']}" for u in (units_by_deck or {}).get(deck["id"], []))
        ring = (f'<span class="ring" data-ring-units="{unit_ids}" role="img" aria-label="progress">'
                f'<span class="ring-core" data-ring-label>0%</span></span>')
        cards.append(f"""<article class="room-card">
  <a class="room-cover" href="{module_href}">
    {ring}
    <span class="room-audience">Module {int(deck['id'][1:])} · {len(deck['slides'])} slides</span>
    <h3>{html.escape(short)}</h3>
    <span class="room-number">{f"{len(deck['slides'])} slides" if text_only else f"{int(total // 60)}m {int(total % 60)}s of narration"}</span>
    <span class="room-waves" aria-hidden="true">{waves}</span>
  </a>
  <div class="room-body">
    <p class="room-meta">{"slides · transcript · print-ready" if text_only else f"{len(entries)} narrated · captions · transcript"} {chip} {shared_chip} <span class="voice-chip is-release" data-quiz-badge="{deck['id']}" hidden></span></p>
    <p class="room-links"><a href="{site_base}/lesson-{deck['id']}.html">Lesson</a> · <a href="{site_base}/lab-{deck['id']}.html">Lab</a> · <a href="{site_base}/quiz-{deck['id']}.html">Knowledge check</a> · <a href="{site_base}/handout-{deck['id']}.html">Handout</a></p>
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
    if text_only:
        lede = ("Every module is a deck you can present, read or print, with a complete transcript for "
                "every slide. Built from three production repositories, and verified with the same "
                "evidence discipline it teaches.")
        facts = ("      <li>9 modules · 233 slides</li>\n"
                 f"      <li>{all_slides} slide transcripts</li>\n"
                 "      <li>Present · read · print</li>\n"
                 "      <li>Design ported from ai_qe</li>")
        section_note = "Each deck plays one slide at a time, or read and print it as a document."
        first_howto = ('      <li><strong>Text-first copy:</strong> narration and captions are not '
                       'published here, so the decks are read, presented and printed rather than '
                       'played.</li>\n'
                       '      <li>Every slide carries its transcript, and the\n'
                       f'          <a href="{site_base}/transcripts/ALL.md">complete transcript</a> '
                       'covers all nine modules in one file.</li>')
        footnote = ("Speaker notes are the presenter's version; the narration script is the learner's. "
                    "The recordings exist but are not part of this published copy — the transcripts are "
                    "the complete approved narration either way.")
    else:
        lede = ("Every module is narrated slide by slide, with captions, a readable transcript and a "
                "deck you can present. Built from three production repositories, and verified with the "
                "same evidence discipline it teaches.")
        facts = ("      <li>9 modules · 233 slides</li>\n"
                 f"      <li>{int(grand_total // 60)} minutes of narration</li>\n"
                 "      <li>Captions on every slide</li>\n"
                 f"      <li>{status}</li>")
        section_note = "Each deck plays one slide at a time. Press play when you are ready."
        first_howto = ('      <li>Narration never autoplays — press <strong>Play narration</strong> on '
                       'any deck.</li>\n'
                       '      <li>Captions are on by default. The full transcript is behind '
                       '<strong>Transcript</strong>, and the\n'
                       f'          <a href="{site_base}/transcripts/ALL.md">complete transcript</a> '
                       'covers all nine modules in one file.</li>')
        footnote = ("Speaker notes are the presenter's version; the narration is the learner's. "
                    "Recordings currently use a free preview voice and say so wherever they appear — the "
                    "released voice is recorded separately and the words do not change.")
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
    <div class="site-brand-row">
      <a class="site-brand" href="{site_base}/index.html">{BRAND_MARK}AI Product Studio<span class="brand-destination">Course</span></a>
      <button type="button" class="search-button" data-search-open title="Search the course (press /)">Search <kbd>/</kbd></button>
    </div>
    <p class="eyebrow">AI Product Studio · edition 2026.09 · nine modules</p>
    <h1>Ship AI products a skeptical engineer can audit.</h1>
    <p class="site-lede">Three production repositories — an on-device meeting copilot, a multi-tenant SaaS
      built with AI agents under written rules, and an evidence-cited briefing site — taught as one method:
      spec it, build it, validate it, prove it. Nine narrated modules, labs whose pass criteria are objective,
      and a course that checks its own claims every time it is built.</p>
    <ul class="site-facts">
{facts}
    </ul>
    <div class="hero-actions">
      <a class="btn-hero" href="{site_base}/lab-m00.html">Start here: your first win in about 30 minutes →</a>
      <a class="btn-hero-quiet" href="#proof">See what this site proves about itself</a>
    </div>
  </div>
</header>
<main class="site-main">
  <div class="continue-strip" data-continue hidden>
    <p><strong>Continue where you left off:</strong> <span data-continue-label></span></p>
    <a class="btn-primary" href="{site_base}/index.html">Continue →</a>
    <div class="progress-tools">
      <button type="button" data-progress-export title="Download your progress as JSON">Export progress</button>
      <button type="button" data-progress-import title="Load a progress file">Import</button>
      <button type="button" data-progress-reset>Reset</button>
    </div>
  </div>
{proof_html}
  <div class="section-heading">
    <h2>Start with what you want to build</h2>
    <span class="section-note">Each path teaches one product type end to end. Not sure what a
      <a href="{site_base}/paths.html">path or a unit</a> is?</span>
  </div>
  <div class="path-grid">
{path_cards}
  </div>
  <div class="section-heading">
    <h2>Or open a single module</h2>
    <span class="section-note">{section_note}</span>
  </div>
  <div class="room-grid">
{chr(10).join(cards)}
  </div>
  <section class="included" id="included">
    <div class="section-heading">
      <h2>What is included</h2>
      <span class="section-note">Stated the way the sales page states it — and the sales page is in the repository, so the two cannot drift.</span>
    </div>
    <div class="included-grid">
      <article class="included-card">
        <h3>Studio · self-paced</h3>
        <p class="included-price">$399</p>
        <ul>
          <li>All 9 modules: 27 narrated lesson segments with captions and transcripts</li>
          <li>8 labs with objective acceptance checklists, plus the capstone</li>
          <li>9 knowledge checks (72 questions) with rationale and objective references</li>
          <li>The TinyCopilot and mini-flow lab starters with their verified test runs</li>
          <li>Lessons, handouts and glossaries as searchable text</li>
          <li>The capstone rubric and the evidence-record template</li>
        </ul>
      </article>
      <article class="included-card is-featured">
        <h3>Studio Live · 8-week cohort</h3>
        <p class="included-price">$1,490 <small>founding cohort $990</small></p>
        <ul>
          <li>Everything in Studio</li>
          <li>Eight 90-minute workshops (I do / we do / you do)</li>
          <li>Instructor code review on three labs</li>
          <li>Capstone review and demo day</li>
          <li>The cohort channel and the founding-cohort testimonial trade</li>
        </ul>
      </article>
      <article class="included-card">
        <h3>One track · self-paced</h3>
        <p class="included-price">$199</p>
        <ul>
          <li>One archetype: on-device app, spec-driven SaaS, or expertise product</li>
          <li>Four modules in full plus the monetise-and-launch slice</li>
          <li>The same labs, decks, checks and artifacts for those modules</li>
          <li>Each path page states what it leaves out, before checkout</li>
        </ul>
      </article>
    </div>
    <p class="index-footnote">Prices are the decision record in <a href="https://github.com/tomqwu/ai_courses/blob/main/course/04-sales/pricing-and-platforms.md">pricing-and-platforms.md</a>, with the reasoning in both directions. Testimonials are not shown because none exist yet; the three repositories are the proof until the founding cohort finishes.</p>
  </section>
  <section class="how-to">
    <h2>How to use this site</h2>
    <ul>
{first_howto}
      <li><strong>Present ↗</strong> goes full screen for a room; <strong>Read all</strong> turns the deck
          into one scrolling document; <strong>Sources &amp; notes</strong> opens the presenter notes.</li>
      <li>Keyboard: <kbd>→</kbd>/<kbd>Space</kbd> next, <kbd>←</kbd> previous, <kbd>Home</kbd>/<kbd>End</kbd>
          first/last, <kbd>Esc</kbd> close.</li>
      <li>Printing a deck prints one 16:9 slide per page.</li>
    </ul>
  </section>
  <section class="tools" id="tools">
    <div class="section-heading">
      <h2>Take the method without buying the course</h2>
      <span class="section-note">The three checkers this site runs on itself, free and self-contained.</span>
    </div>
    <div class="tools-grid">
      <article class="tools-card">
        <h3>Pointer lint</h3>
        <p>Every claim in your documentation carries a path, and every path and line range still
           resolves — or the run fails with the file and line to fix.</p>
        <code>python3 pointer_lint.py docs/</code>
      </article>
      <article class="tools-card">
        <h3>Facts drift</h3>
        <p>Re-derives the numbers you state as fact from the source they came from, and names the
           documents still printing the old value. The pinned file is data, never code.</p>
        <code>python3 facts_drift.py --facts facts.json --strict</code>
      </article>
      <article class="tools-card">
        <h3>Agent rule audit</h3>
        <p>Reads an <code>AGENTS.md</code>, a <code>CLAUDE.md</code> or a constitution and sorts every
           rule into checkable, vague, or imperative-but-unenforced.</p>
        <code>python3 agents_audit.py AGENTS.md</code>
      </article>
    </div>
    <p class="index-footnote">Standard library only, no install, nothing sent anywhere.
      <a href="https://github.com/tomqwu/ai_courses/tree/main/aps-tools">Read them or copy the folder →</a></p>
  </section>
{capture_html}
  <p class="index-footnote">{footnote} Progress, quiz scores and lab checklists are stored in this browser only — export them from the strip above to move machines.</p>
</main>
<script src="{site_base}/assets/progress.js" defer></script>
<script src="{site_base}/assets/search.js" defer></script>
</body>
</html>
"""


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="build into a temp dir and report only")
    parser.add_argument("--subscribe-action", default="",
                        help="form action URL of your mailing provider for the teardown sign-up; "
                             "without it the form is shown disabled and says so")
    parser.add_argument("--site-base", default=".",
                        help="prefix for asset URLs; '.' works from file:// and any subpath")
    parser.add_argument("--out", metavar="DIR",
                        help="build into DIR instead of in place (used when publishing)")
    parser.add_argument("--no-narration", action="store_true",
                        help="publish text-first: the player is told there are no recordings, so "
                             "no Play button offers files that are not in the published copy")
    args = parser.parse_args(argv)

    manifest = load_manifest()
    provenance = read_json(PROVENANCE_PATH, None) or {"recordings": []}
    scripts = load_scripts()
    decks = [parse_deck(deck_id, scripts["decks"]) for deck_id in DECK_IDS]

    if args.check:
        target = Path("/tmp/aps-site-check")
    elif args.out:
        target = Path(args.out).expanduser().resolve()
    else:
        target = SITE_ROOT
    target.mkdir(parents=True, exist_ok=True)
    if args.check:
        shutil.rmtree(target, ignore_errors=True)
        target.mkdir(parents=True)
    # What the *player* is told. In a text-first publish this is deliberately empty: the recordings
    # exist, but offering them would mean offering files the published copy does not contain.
    player_manifest = {"decks": {}} if args.no_narration else manifest
    write_json(target / "narration.json", player_manifest)

    import site_paths as SP                                                       # noqa: PLC0415
    import site_content as SC                                                     # noqa: PLC0415
    import site_pages as SPG                                                      # noqa: PLC0415
    units_by_deck = {deck["id"]: SP.module_units(deck) for deck in decks}
    for deck in decks:
        (target / f"{deck['id']}.html").write_text(
            page(deck, manifest, provenance, args.site_base, text_only=args.no_narration,
                 units=units_by_deck[deck["id"]]),
            encoding="utf-8")
        (target / f"transcript-{deck['id']}.html").write_text(
            transcript_page(deck, manifest, provenance, args.site_base, text_only=args.no_narration),
            encoding="utf-8")
    # ── learning paths ────────────────────────────────────────────────────────────────────────────
    # The Microsoft Learn hierarchy (path -> module -> unit) built on the content that already
    # exists. Paths are built one at a time; `status` on each track decides what gets a real page,
    # so a path that has not been built cannot link to a page that does not exist.
    seconds = SP.unit_seconds(units_by_deck, manifest)

    # ── the course text: lesson, handout, glossary, lab, knowledge check ──────────────────────────
    # Parsed from the module Markdown; the quiz parser refuses a malformed item, so a question with
    # zero or two keyed answers fails the build here rather than shipping.
    records: list[dict] = []
    terms_by_deck: dict[str, list[dict]] = {}
    for deck in decks:
        folder = COURSE_DIR / deck["source"].rsplit("/", 1)[0]
        for kind in ("lesson", "handout", "glossary"):
            html_out, record = SPG.document_page(deck, kind, SC.read(folder / f"{kind}.md"),
                                                 args.site_base, BRAND_MARK)
            (target / f"{kind}-{deck['id']}.html").write_text(html_out, encoding="utf-8")
            record["module"] = SPG.short_label(deck)
            if kind == "glossary":
                record["terms"] = SC.parse_glossary(SC.read(folder / "glossary.md"))
                terms_by_deck[deck["id"]] = record["terms"]
            records.append(record)
        lab = SC.parse_lab(SC.read(folder / "lab.md"), deck["id"])
        html_out, record = SPG.lab_page(deck, lab, args.site_base, BRAND_MARK)
        (target / f"lab-{deck['id']}.html").write_text(html_out, encoding="utf-8")
        record["module"] = SPG.short_label(deck)
        records.append(record)
        try:
            quiz = SC.parse_quiz(SC.read(folder / "quiz.md"), deck["id"])
        except SC.QuizError as error:
            raise SystemExit(f"knowledge check: {error}")
        html_out, record = SPG.quiz_page(deck, quiz, args.site_base, BRAND_MARK)
        (target / f"quiz-{deck['id']}.html").write_text(html_out, encoding="utf-8")
        record["module"] = SPG.short_label(deck)
        records.append(record)
    decks_by_id_for_glossary = {deck["id"]: deck for deck in decks}
    (target / "glossary.html").write_text(
        SPG.master_glossary_page(terms_by_deck, decks_by_id_for_glossary, args.site_base, BRAND_MARK),
        encoding="utf-8")
    (target / "search.json").write_text(SPG.search_index(records, decks, units_by_deck), encoding="utf-8")
    decks_by_id = {deck["id"]: deck for deck in decks}
    built_tracks = [t for t in SP.TRACKS if t["status"] == "built"]
    built_modules = {d for t in built_tracks for d in list(t["core"]) + list(t.get("slice") or {})}
    for deck_id in sorted(built_modules):
        # Every path that includes the module, not a single owner: modules are shared, and a
        # module page that named one path would misdescribe the other two.
        tracks_for = SP.paths_for_module(deck_id, built_tracks)
        (target / f"module-{deck_id}.html").write_text(
            SP.module_page(decks_by_id[deck_id], units_by_deck[deck_id], seconds, args.site_base,
                           BRAND_MARK, tracks_for, args.no_narration), encoding="utf-8")
    (target / "paths.html").write_text(
        SP.paths_page(SP.TRACKS, units_by_deck, seconds, args.site_base, BRAND_MARK),
        encoding="utf-8")
    for track in built_tracks:
        (target / track["page"]).write_text(
            SP.path_page(track, decks_by_id, units_by_deck, seconds, args.site_base, BRAND_MARK,
                         built_modules), encoding="utf-8")

    # The landing page is the paths GUI now: the chooser is rendered from the same TRACKS data as
    # the path pages, so the two cannot disagree about what exists.
    path_cards = SP.path_cards_html(SP.TRACKS, units_by_deck, seconds, args.site_base)
    module_paths = {deck_id: len(SP.paths_for_module(deck_id, built_tracks))
                    for deck_id in DECK_IDS}
    import site_proof as SPR                                                      # noqa: PLC0415
    proof = SPR.gather(decks, manifest)
    (target / "proof.json").write_text(json.dumps(proof, indent=1, default=str), encoding="utf-8")
    (target / "index.html").write_text(
        index_page(decks, manifest, provenance, args.site_base, text_only=args.no_narration,
                   subscribe_action=args.subscribe_action,
                   path_cards=path_cards, module_paths=module_paths, units_by_deck=units_by_deck,
                   proof_html=SPR.proof_section(proof, args.site_base)),
        encoding="utf-8")

    # The transcripts are committed as Markdown, so a check must prove the committed copies still
    # match what the scripts say rather than quietly regenerating them.
    # Always the committed location: a check must compare against what is in the repository, not
    # against a copy it just wrote.
    transcript_dir = SITE_ROOT / "transcripts"
    if args.out:
        # Publishing must not rewrite the repository's committed transcripts: they are the source of
        # truth and the gate has already validated them. Copy them into the published copy instead.
        published = target / "transcripts"
        published.mkdir(parents=True, exist_ok=True)
        for path in sorted(transcript_dir.glob("*.md")):
            shutil.copy2(path, published / path.name)
    elif not args.check:
        transcript_dir.mkdir(parents=True, exist_ok=True)
    drift = []
    for deck in decks:
        text = transcript_markdown(deck, manifest, provenance)
        out = transcript_dir / f"{deck['id']}.md"
        if args.check:
            on_disk = out.read_text(encoding="utf-8") if out.is_file() else None
            if on_disk != text:
                drift.append(f"transcripts/{out.name}")
        elif not args.out:
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
    elif not args.out:
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
    print(f"site written to {target}"
          f"{' (text-first: no recordings published)' if args.no_narration else ''}")
    print(f"  decks: {len(decks)} · slides: {total_slides} · scripted: {scripted} · recorded: {recorded}")
    print(f"  transcripts: {len(decks)} decks · {transcript_words:,} words"
          f"{' (verified against the approved scripts)' if args.check else ''}")
    print(f"  course text: {len(decks)} lessons · labs · knowledge checks ({sum(1 for r in records if r['kind'] == 'quiz') * 8} questions) "
          f"· handouts · glossaries ({sum(len(t) for t in terms_by_deck.values())} terms) · search index {len(json.loads((target / 'search.json').read_text(encoding='utf-8')))} entries")
    if recorded < scripted:
        print(f"  note: {scripted - recorded} slides have no recording yet — "
              f"run `python3 ../06-production/narration/generate_narration.py generate --provider say`")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
