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
from narration_data import (COURSE_DIR, DECK_IDS, EDITION, MANIFEST_PATH, PROVENANCE_PATH,  # noqa: E402
                            SITE_ROOT, load_manifest, load_scripts, read_json, write_json)

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


# ---------------------------------------------------------------- deck parsing

def parse_deck(deck_id: str) -> dict:
    matches = sorted(COURSE_DIR.glob(f"03-content/{deck_id}-*/slides.md"))
    if not matches:
        raise SystemExit(f"{deck_id}: no slides.md found")
    source = matches[0]
    front, slide_texts = split_slides(source.read_text(encoding="utf-8"))
    slides = []
    for index, raw in enumerate(slide_texts, 1):
        notes_match = NOTES_RE.search(raw)
        notes = notes_match.group(1).strip() if notes_match else ""
        classes = [m.group(2) for m in DIRECTIVE_RE.finditer(raw) if m.group(1) == "_class"]
        body = NOTES_RE.sub("", DIRECTIVE_RE.sub("", raw)).strip()
        title_match = re.search(r"^#{1,4}\s+(.*)$", body, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else f"Slide {index}"
        rendered = render_blocks(body.splitlines())
        # Point aria-labelledby at a real element: give the slide's first heading the id.
        rendered = re.sub(r"<(h[1-4])>", f'<\\1 id="slide-{index}-title">', rendered, count=1)
        slides.append({
            "id": f"slide-{index}",
            "number": index,
            "title": title,
            "classes": classes,
            "notes": notes,
            "html": rendered,
        })
    return {
        "id": deck_id,
        "label": front.get("title", deck_id.upper()),
        "source": str(source.relative_to(COURSE_DIR)),
        "slides": slides,
    }


def slide_shell(deck: dict, slide: dict, manifest_entry: dict | None) -> str:
    classes = " ".join(["slide"] + slide["classes"])
    hidden = "" if slide["number"] == 1 else " hidden"
    media = ""
    if manifest_entry:
        media = (f' data-audio="{html.escape(manifest_entry["audio"], quote=True)}"'
                 f' data-captions="{html.escape(manifest_entry["captions"], quote=True)}"'
                 f' data-duration="{manifest_entry.get("duration", "")}"')
    return (f'<section class="{classes}" id="{slide["id"]}" data-number="{slide["number"]}"'
            f'{media}{hidden} aria-roledescription="slide" aria-labelledby="{slide["id"]}-title">'
            f'<div class="slide-content">{slide["html"]}</div>'
            f'<details class="slide-notes"><summary>Speaker notes</summary>'
            f'<div>{inline(slide["notes"]) if slide["notes"] else "No notes for this slide."}</div></details>'
            f'</section>')


def page(deck: dict, manifest: dict, provenance: dict, site_base: str) -> str:
    deck_manifest = (manifest.get("decks", {}).get(deck["id"], {}) or {}).get("slides", {})
    prov_by_audio = {rec.get("audio"): rec for rec in provenance.get("recordings", [])}
    bases = {prov_by_audio.get(entry.get("audio"), {}).get("basis") for entry in deck_manifest.values()}
    preview_count = sum(1 for e in deck_manifest.values()
                        if prov_by_audio.get(e.get("audio"), {}).get("basis") == "sentence-measured-preview")
    mixed = 0 < preview_count < len(deck_manifest)
    is_preview = preview_count > 0
    voice = (list(deck_manifest.values()) or [{}])[0].get("voice", manifest.get("voice", ""))
    total = round(sum(float(e.get("duration", 0) or 0) for e in deck_manifest.values()), 1)
    recorded = len(deck_manifest)

    sections = "\n".join(slide_shell(deck, slide, deck_manifest.get(slide["id"])) for slide in deck["slides"])
    options = "\n".join(
        f'<option value="{s["id"]}">{s["number"]}. {html.escape(s["title"][:70])}</option>'
        for s in deck["slides"])
    if not is_preview:
        badge = ""
    elif mixed:
        badge = (f'<p class="voice-badge" role="note">{preview_count} of {recorded} recordings on this '
                 f'page are preview audio — a free local voice, not the finished release recording. '
                 f'The rest were recorded separately; each slide\'s transcript names its voice.</p>')
    else:
        badge = ('<p class="voice-badge" role="note">Preview narration — a free local voice, not the '
                 'finished release recording.</p>')
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(deck['label'])} — AI Product Studio</title>
<link rel="stylesheet" href="{site_base}/assets/player.css">
</head>
<body data-narration-manifest="{site_base}/narration.json" data-narration-deck="{deck['id']}"
      data-site-base="{site_base}" data-voice="{'preview' if is_preview else 'release'}">
<a class="skip-link" href="#slides">Skip to slides</a>
<header class="deck-header">
  <div class="deck-heading">
    <p class="deck-kicker"><a href="{site_base}/index.html">AI Product Studio</a> · Module {deck['id'][1:]}</p>
    <h1>{html.escape(deck['label'])}</h1>
    <p class="deck-meta">{len(deck['slides'])} slides · {recorded} narrated · {int(total // 60)}m {int(total % 60)}s
      {'· <span class="meta-preview">preview voice</span>' if is_preview else ''}</p>
  </div>
  <div class="deck-tools">
    <button type="button" data-narration-start hidden aria-pressed="false">▶ Play narration</button>
    <a class="tool-link" href="{site_base}/assets/audio/{EDITION}/{deck['id']}/slide-1.vtt" download>Captions</a>
  </div>
</header>
{badge}
<main id="slides" class="slides" tabindex="-1" aria-label="{html.escape(deck['label'])}">
{sections}
</main>
<nav class="deck-navigation" aria-label="Slide navigation">
  <button type="button" data-nav="prev">‹ Previous</button>
  <label class="deck-picker"><span class="sr-only">Choose a slide</span>
    <select data-slide-picker>{options}</select></label>
  <button type="button" data-nav="next">Next ›</button>
  <p class="slide-status" role="status" aria-live="polite" aria-atomic="true"></p>
  <p class="deck-message" role="status"></p>
</nav>
<noscript><style>.slide[hidden]{{display:block}}</style>
<p class="noscript">JavaScript is off, so narration and slide navigation are disabled. Every slide is
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
        cards.append(f"""<li class="deck-card">
  <a href="{site_base}/{deck['id']}.html">
    <span class="card-kicker">Module {deck['id'][1:]}</span>
    <strong>{html.escape(deck['label'])}</strong>
    <span class="card-meta">{len(deck['slides'])} slides · {len(entries)} narrated · {int(total // 60)}m {int(total % 60)}s{' · preview voice' if preview else ''}</span>
  </a>
</li>""")

    all_recorded = sum(len((manifest.get("decks", {}).get(d, {}) or {}).get("slides", {})) for d in DECK_IDS)
    all_slides = sum(len(d["slides"]) for d in decks)
    status = ("Every slide is narrated." if all_recorded >= all_slides else
              f"{all_recorded} of {all_slides} slides narrated so far. "
              "Generate the rest with <code>make narration</code>.")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Product Studio — narrated course</title>
<link rel="stylesheet" href="{site_base}/assets/player.css">
</head>
<body class="index">
<header class="index-header">
  <h1>AI Product Studio</h1>
  <p>Build, ship and sell three kinds of AI product. Nine modules, narrated, with captions and transcripts.</p>
  <p class="index-status">{status} Total listening time: {int(grand_total // 60)} minutes.</p>
</header>
<main>
  <ol class="deck-list">
{chr(10).join(cards)}
  </ol>
  <section class="index-notes">
    <h2>How to use this site</h2>
    <ul>
      <li>Every deck plays slide by slide. Narration never autoplays — press play when you are ready.</li>
      <li>Captions are on by default and can be turned off; the transcript is one click away on every slide.</li>
      <li>Keyboard: <kbd>→</kbd>/<kbd>Space</kbd> next, <kbd>←</kbd> previous, <kbd>Home</kbd>/<kbd>End</kbd> first/last, <kbd>Esc</kbd> close.</li>
      <li>The speaker notes under each slide are the presenter version; the narration is the learner version.</li>
    </ul>
  </section>
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
    decks = [parse_deck(deck_id) for deck_id in DECK_IDS]

    target = Path("/tmp/aps-site-check") if args.check else SITE_ROOT
    target.mkdir(parents=True, exist_ok=True)
    if args.check:
        shutil.rmtree(target, ignore_errors=True)
        target.mkdir(parents=True)
    write_json(target / "narration.json", manifest)

    for deck in decks:
        (target / f"{deck['id']}.html").write_text(
            page(deck, manifest, provenance, args.site_base), encoding="utf-8")
    (target / "index.html").write_text(
        index_page(decks, manifest, provenance, args.site_base), encoding="utf-8")

    total_slides = sum(len(d["slides"]) for d in decks)
    scripted = sum(len(v["slides"]) for v in scripts["decks"].values())
    recorded = sum(len((manifest.get("decks", {}).get(d, {}) or {}).get("slides", {}))
                   for d in scripts["decks"])
    print(f"site written to {target}")
    print(f"  decks: {len(decks)} · slides: {total_slides} · scripted: {scripted} · recorded: {recorded}")
    if recorded < scripted:
        print(f"  note: {scripted - recorded} slides have no recording yet — "
              f"run `python3 ../06-production/narration/generate_narration.py generate --provider say`")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
