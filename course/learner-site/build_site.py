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
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "06-production"))

from deck_lint import split_slides                      # noqa: E402
from captions import words
from narration_data import (COURSE_DIR, DECK_IDS, EDITION, MANIFEST_PATH, PROVENANCE_PATH,  # noqa: E402
                            SITE_ROOT, load_manifest, load_scripts, read_json, write_json)
import site_shell as SH                                  # noqa: E402
import figures as FIG                                    # noqa: E402
import site_locale as SL                                 # noqa: E402

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


def render_diagram(kind: str, items: list[str], ordered: bool) -> str:
    """Render a slide's own list as a figure (#99).

    The words are frozen — they come from the same bullets the author wrote — only the
    arrangement is declared: `flow`/`loop`/`steps` become a flow of cards joined by drawn
    connectors, `stack` layered bands, `grid` side-by-side columns.
    """
    try:
        return FIG.render(FIG.from_list(kind, items), inline=inline)
    except FIG.FigureError as exc:
        raise SystemExit(f"_diagram: {exc}") from exc


def render_figure(body: list[str], sentences: list[str] | None) -> str:
    """A ```figure fence: parsed and drawn; parts with `at:` build in on their narration sentence."""
    try:
        return FIG.render(FIG.parse("\n".join(body)), sentences=sentences, inline=inline)
    except FIG.FigureError as exc:
        raise SystemExit(f"figure: {exc}") from exc


def render_blocks(lines: list[str], diagram: str = "", sentences: list[str] | None = None) -> str:
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
            # The info string travels with the block: it says whether the exhibit is a true copy
            # or a declared kind, and which lines to highlight (#76).
            info = stripped[3:].strip()
            body, i = [], i + 1
            while i < len(lines) and not FENCE_RE.match(lines[i].strip()):
                body.append(lines[i])
                i += 1
            i += 1
            if info.split()[:1] == ["figure"]:
                out.append(render_figure(body, sentences))
                continue
            body = [html.escape(line) for line in body]
            out.append(f'<pre data-info="{html.escape(info, quote=True)}"><code>' + "\n".join(body)
                       + "</code></pre>")
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
            out.append("<blockquote>" + render_blocks(quote, sentences=sentences) + "</blockquote>")
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
        # The approved narration is the source of truth for anything spoken; the deck Markdown is
        # the source of truth for what is displayed.
        script_text = ((scripts or {}).get(deck_id, {}).get("slides", {})
                       .get(f"slide-{index}", {}).get("text", "").strip())
        # A figure's parts build in on the sentence of this narration their `at:` names.
        said = sentences(script_text)
        d_match = DIAGRAM_AT.search(content_body)
        if d_match:
            head = content_body[:d_match.start()].strip()
            tail = content_body[d_match.end():].strip()
            rendered = ((render_blocks(head.splitlines(), sentences=said) + "\n") if head else "") \
                + render_blocks(tail.splitlines(), diagram=d_match.group(1).strip(), sentences=said)
        else:
            rendered = render_blocks(content_body.splitlines(), sentences=said)
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
        slides.append({
            "id": f"slide-{index}",
            "raw": body,
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


# Provenance bases a speech synthesizer produced: the preview voices and the release voice alike.
# An imported `external-recording` may be a person, so it is never called synthetic.
GENERATED_BASES = {"aligned-generation", "proportional-generation", "sentence-measured-preview"}


def synthetic_disclosure(entries: dict, provenance: dict) -> str:
    """The sentence that says the narration is machine-spoken, wherever a listener meets it.

    EU AI Act Article 50 makes this disclosure a compliance item, and it is the honesty the course
    teaches (M6.3). It follows each recording's provenance, not the voice tier, so it stays when
    the release voice replaces the preview one: that voice is synthesized too.
    """
    prov = {r.get("audio"): r for r in provenance.get("recordings", [])}
    synthetic = sum(1 for e in entries.values()
                    if prov.get(e.get("audio"), {}).get("basis") in GENERATED_BASES)
    if synthetic and synthetic == len(entries):
        return "The narration is spoken by a synthesized voice, not a human recording."
    if synthetic:
        return f"{synthetic} of {len(entries)} recordings are spoken by a synthesized voice."
    return ""


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
    disclosure = synthetic_disclosure(entries, provenance)
    total = sum(float(e.get("duration", 0) or 0) for e in entries.values())
    out = [f"# {deck['label']}", "", "## Narration transcript", ""]
    out.append(f"**{len(deck['slides'])} slides · {len(entries)} narrated · "
               f"{int(total // 60)}m {int(total % 60)}s of audio**")
    out.append("")
    if preview and preview == len(entries):
        out.append(f"**Voice:** preview narration — a free local voice, not the finished release "
                   f"recording. {disclosure} The words below are the approved narration and do not "
                   f"change when the release voice is recorded.")
    elif preview:
        out.append(f"**Voice:** mixed — {preview} of {len(entries)} recordings are preview audio, "
                   f"the rest are not. {disclosure} The words below are the approved narration.")
    elif voice:
        out.append(f"**Voice:** {voice}. {disclosure}".rstrip())
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
    disclosure = synthetic_disclosure(entries, provenance)
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
        note = (f'<p class="voice-badge" role="note">Preview narration — a free local voice, not the '
                f'finished release recording. {disclosure} These are the approved words and do not '
                f'change when the release voice is recorded.</p>')
    elif preview:
        note = (f'<p class="voice-badge" role="note">Mixed — {preview} of {len(entries)} recordings '
                f'are preview audio. {disclosure} These are the approved words.</p>')
    elif disclosure:
        note = f'<p class="voice-badge" role="note">{disclosure} These are the approved words.</p>'
    else:
        note = ""
    lede = (f'{len(deck["slides"])} slides · {len(entries)} narrated · {int(total // 60)}m {int(total % 60)}s'
            f' · <a href="{site_base}/{deck["id"]}.html">open the narrated deck →</a>')
    content = (SH.page_head(deck["module_tag"], f'{html.escape(deck["label"])} — transcript', lede, note)
               + "\n" + "\n".join(rows))
    return SH.document(f"{deck['label']} — transcript", f"The narration of {deck['label']}, slide by slide.",
                       content, site_base, "transcript",
                       crumbs=SH.module_crumbs(site_base, deck, "Transcript"),
                       deck_id=deck["id"], current="transcript", mode="watch")


BRAND_MARK = SH.BRAND_MARK


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


PRE_RE = re.compile(r'<pre data-info="([^"]*)"><code>(.*?)</code></pre>', re.S)
KIND_NAMES = {"commands": "Commands", "output": "Output", "template": "Template",
              "illustrative": "Illustrative — not a copy of a file"}
FILE_ICON = ('<svg class="exhibit-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
             '<path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8z"/><path d="M14 3v5h5"/></svg>')


def _hl(spec: str) -> set[int]:
    """`hl=4` or `hl=82-83,85` → the line numbers to highlight."""
    out: set[int] = set()
    for part in spec.split(","):
        a, _, b = part.partition("-")
        if a.strip().isdigit():
            out.update(range(int(a), int(b or a) + 1))
    return out


def _numbered(lines: list[str], source: dict | None) -> list[int | None]:
    """Each exhibit line's number in the cited file, found by matching text inside the cited range.

    Exhibits may elide (…) and rewrap, so a line is numbered only where it is found; elisions and
    rewrapped lines carry no number rather than a wrong one.
    """
    if not source:
        return [None] * len(lines)
    import verify as V                                                         # noqa: PLC0415
    text = source["target"].read_text(encoding="utf-8", errors="replace").splitlines()
    ranges = V.parse_line_ranges(source["spec"]) if source["spec"] else None
    lo, hi = (ranges[0][0], ranges[-1][1]) if ranges else (1, len(text))
    out, at = [], lo
    for line in lines:
        want = html.unescape(line).strip()
        # A line cut short with "…" still names its file line: match what precedes the ellipsis.
        prefix = want[:-1].rstrip() if want.endswith("…") and len(want) > 4 else ""
        found = None
        if want and not V.EXHIBIT_ELIDE_RE.fullmatch(want):
            for n in range(at, hi + 1):
                have = text[n - 1].strip() if n - 1 < len(text) else None
                if have is not None and (have == want or (prefix and have.startswith(prefix))):
                    found = n
                    break
        out.append(found)
        if found:
            at = found + 1
    return out


def exhibits(content: str, cited: list[dict]) -> str:
    """Code blocks as exhibit panels (#76): a header naming the file, its lines and the pinned
    commit, line numbers from the file itself, highlighted lines, long lines wrapped with a hanging
    indent instead of clipped. A declared block (commands, output, template, illustrative) says what
    it is instead of naming a file."""
    exhibit_sources = [c for c in cited if c["kind"] == "Exhibit"]

    def panel(m: re.Match) -> str:
        info = html.unescape(m.group(1)).split()
        declared = next((k for k in KIND_NAMES if k in info), "")
        hl = _hl(next((w[3:] for w in info if w.startswith("hl=")), ""))
        lines = m.group(2).split("\n")
        source = None
        if not declared:
            import verify as V                                                 # noqa: PLC0415
            wanted = [V._exhibit_norm(html.unescape(l)) for l in lines if len(html.unescape(l).strip()) > 3]
            source = next((s for s in exhibit_sources if _holds(s["target"], s["spec"], wanted, V)), None)
        numbers = _numbered(lines, source)
        rows = []
        for i, (line, n) in enumerate(zip(lines, numbers), 1):
            lit = (n in hl) if any(numbers) else (i in hl)
            attrs = f' data-n="{n}"' if n else ""
            rows.append(f'<span class="line{" is-hl" if lit else ""}"{attrs}>{line or " "}</span>')
        if source:
            repo, _, path = source["pointer"].partition("/")
            file = f'{repo} / {path.split(":")[0].rsplit("/", 1)[-1]}'
            span = source["spec"].replace("-", "–") if source["spec"] else "whole file"
            head = (f'{FILE_ICON}<span class="exhibit-file">{html.escape(file)}</span>'
                    f'<span class="exhibit-lines">{html.escape(span)} · {source["commit"]}</span>')
        elif declared:
            head = f'<span class="exhibit-file">{KIND_NAMES[declared]}</span>'
        else:
            head = '<span class="exhibit-file">Excerpt</span>'
        numbered = " is-numbered" if any(numbers) else ""
        return (f'<figure class="exhibit{numbered}"><figcaption class="exhibit-head">{head}</figcaption>'
                f'<pre><code>{"".join(rows)}</code></pre></figure>')

    return PRE_RE.sub(panel, content)


SOURCE_LINE = re.compile(r"<p>((?:\s*<code>[^<]+</code>\s*(?:,|·|and|;)?\s*)+)</p>\s*$")


def source_footer(content: str) -> str:
    """A slide that ends on a line of bare citations gets it as its source line (#76): the Source
    chip and the paths, in the chrome size, instead of a paragraph of code."""
    m = SOURCE_LINE.search(content)
    if not m:
        return content
    return (content[:m.start()] + f'<p class="slide-source"><span class="source-chip">Source</span>'
            f'{m.group(1).strip()}</p>' + content[m.end():])


SENTENCE = re.compile(r"(?<=[.!?])\s+(?=[\"“(A-Z0-9])")
POINTER_TOKEN = re.compile(r"\b(?:ListenToMe|SignUpFlow|ai_qe|course)/[^\s`'\"),;<>]+")
DECLARED = ("commands", "output", "template", "illustrative", "figure")


def sentences(text: str) -> list[str]:
    """The approved narration, one sentence per line — the transcript panel's rows before (or
    without) captions. The words are exactly the script's; only the line breaks are added."""
    return [s.strip() for s in SENTENCE.split(" ".join(text.split())) if s.strip()]


def _holds(target: Path, spec: str, lines: list[str], V) -> bool:
    """Whether a cited file (within its cited range) contains the exhibit's lines."""
    text = target.read_text(encoding="utf-8", errors="replace").splitlines()
    ranges = V.parse_line_ranges(spec) if spec else None
    cited = V._exhibit_norm("\n".join(l for lo, hi in ranges for l in text[lo - 1:hi]) if ranges
                            else "\n".join(text))
    return any(line in cited for line in lines)


def slide_sources(slide: dict) -> list[dict]:
    """Every repository file a slide cites, in order, as a link at the pinned commit (#75).

    Citations are read the way the gate reads them (`verify.EXHIBIT_REF_RE` and
    `verify.resolve_case_path`): a prefixed pointer as written, and a bare path such as
    `specs/014-security-hardening/plan.md` when exactly one tracked file in the clones ends with it.
    So the chips name the files the exhibit check proved the slide against, and nothing it could not
    resolve. The kind says where the citation sits: the slide's exhibit (a fenced block with no
    declared kind, which the gate holds to a true copy), elsewhere on the slide, or only in the notes.
    """
    import site_content as SC                                                  # noqa: PLC0415
    import verify as V                                                         # noqa: PLC0415
    raw = slide.get("raw", "")
    # The exhibit's own lines: fenced blocks with no declared kind are true copies of a cited file.
    exhibit_lines = [V._exhibit_norm(line)
                     for info, body in re.findall(r"^```([^\n]*)\n(.*?)^```", raw, re.M | re.S)
                     if not any(k in info for k in DECLARED)
                     for line in body.splitlines()
                     if len(V._exhibit_norm(line)) > 3 and not V.EXHIBIT_ELIDE_RE.fullmatch(line.strip())]
    out, seen = [], set()
    for where, text in (("slide", raw), ("notes", slide.get("notes", ""))):
        refs = [(m.group(1), m.group(2)) for m in V.EXHIBIT_REF_RE.finditer(text)]
        refs += [(t.rstrip(".:").partition(":")[0], t.rstrip(".:").partition(":")[2] or None)
                 for t in POINTER_TOKEN.findall(text)]
        for path, spec in refs:
            target = V.resolve_case_path(path)
            if target is None or not target.is_file():
                continue
            rel = target.relative_to(V.REPO).as_posix()
            spec = (spec or "").strip().replace("\u2013", "-")
            pointer = f"{rel}:{spec}" if spec else rel
            if pointer in seen:
                continue
            seen.add(pointer)
            first = re.match(r"\d+(?:-\d+)?", spec.replace(" ", ""))
            url = SC.pointer_link(f"{rel}:{first.group(0)}" if first else rel)
            if not url:
                continue
            if where == "notes":
                kind = "In the notes"
            elif exhibit_lines and _holds(target, spec, exhibit_lines, V):
                kind = "Exhibit"
            else:
                kind = "On the slide"
            out.append({"pointer": pointer, "url": url, "kind": kind, "target": target, "spec": spec,
                        "commit": SC.PINNED.get(rel.split("/", 1)[0], "main")})
    return out


PLAY_ICON = ('<svg class="icon icon-play" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
             '<path d="M7 4l13 8-13 8z"/></svg>'
             '<svg class="icon icon-pause" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
             '<rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>')
CHEVRON = ('<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
           '<path d="{d}"/></svg>')

def spoken_times(deck: dict, manifest: dict) -> dict[str, list[float]]:
    """Each slide's narration sentences, with the second each starts at, read from its captions.

    The same word-position timing the player uses: every caption word gets a time by its place in
    its cue, and a sentence starts at its first word. Captions and script match word for word (the
    gate proves it), so the counts line up. Times are taken only from the recording the manifest
    describes — its audio must hash to the manifest's sha256 — so a build never publishes times read
    from some other take that happens to be on disk.
    """
    import hashlib                                                             # noqa: PLC0415
    from captions import parse_vtt                                             # noqa: PLC0415
    entries = (manifest.get("decks", {}).get(deck["id"], {}) or {}).get("slides", {})
    out: dict[str, list[float]] = {}
    for slide in deck["slides"]:
        entry = entries.get(slide["id"]) or {}
        path = SITE_ROOT / entry["captions"].lstrip("/") if entry.get("captions") else None
        audio = SITE_ROOT / entry["audio"].lstrip("/") if entry.get("audio") else None
        if not path or not path.is_file() or not audio or not audio.is_file():
            continue
        if hashlib.sha256(audio.read_bytes()).hexdigest() != entry.get("sha256"):
            continue
        try:
            cues = parse_vtt(path.read_text(encoding="utf-8"))
        except ValueError:
            continue
        at = [c.start + (c.end - c.start) * k / len(c.text.split())
              for c in cues for k in range(len(c.text.split()))]
        starts, w = [], 0
        for sentence in sentences(slide["script_text"]):
            starts.append(round(at[min(w, len(at) - 1)], 1) if at else 0.0)
            w += len(sentence.split())
        out[slide["id"]] = starts
    return out


def voice_label(deck_manifest: dict, provenance: dict, recorded: int, preview: int,
                text_only: bool) -> str:
    """The voice disclosure, as a label in the control bar rather than a banner (#75). The wording
    still comes from each recording's provenance (#57), so it follows the release voice too."""
    disclosure = synthetic_disclosure(deck_manifest, provenance)
    if text_only:
        return ("Text-first copy — the narration is not published here; the transcript below is "
                "the complete approved narration.")
    if recorded == 0:
        return "Not yet recorded — the transcript below is the approved narration."
    if preview and preview < recorded:
        return f"Mixed voices — {preview} of {recorded} recordings are the preview voice. {disclosure}"
    if preview:
        return f"Preview voice — a free local voice, not the release recording. {disclosure}"
    return f"Release voice. {disclosure}".strip()


def learn_section(deck: dict, slide: dict, entry: dict | None, site_base: str, bare: bool = False) -> str:
    """One section of the Learn page (#112): what was a slide, as a part of a page — its heading, its
    figures, exhibits and points at full width, then its narration as text, with a Listen button.

    The id stays `slide-N`, so every deep link into the module (search, the quiz's feedback, the
    module page, "continue where you left off") still lands on it.
    """
    cited = slide_sources(slide)
    content = source_footer(exhibits(slide["html"], cited))
    said = sentences(slide.get("script_text", ""))
    media, listen = "", ""
    if entry:
        media = (f' data-audio="{html.escape(entry["audio"], quote=True)}"'
                 f' data-captions="{html.escape(entry["captions"], quote=True)}"'
                 f' data-duration="{entry.get("duration", "")}"')
        secs = float(entry.get("duration", 0) or 0)
        listen = (f'<button type="button" class="learn-listen" data-listen aria-label="Listen to this section">'
                  f'{PLAY_ICON}<span>{int(secs // 60)}:{int(secs % 60):02d}</span></button>')
    chip = '<span class="evidence-chip">Evidence</span>' if "proof" in slide["classes"] else ""
    # A unit's opening part is headed by the unit itself (the cover by the page): no second title.
    heading = "" if bare else (
        f'<header class="learn-head">' + (f'<p class="learn-kicker">{chip}</p>' if chip else "")
        + f'<h3 id="{slide["id"]}-title">{inline(slide["title"][:1].upper() + slide["title"][1:])}</h3>{listen}</header>')
    if bare and listen:
        heading = f'<header class="learn-head is-bare">{listen}</header>'
    narration = ""
    if said:
        spans = " ".join(f'<span class="said" data-s="{i}">{html.escape(t)}</span>' for i, t in enumerate(said))
        narration = f'<div class="learn-said"><p>{spans}</p></div>'
    notes = html.escape(slide["notes"]) if slide["notes"] else ""
    sources = "".join(
        f'<li><a href="{html.escape(src["url"], quote=True)}" rel="noopener" data-kind="{src["kind"]}">'
        f'<span class="source-kind">{src["kind"]}</span><code class="source-path">{html.escape(src["pointer"])}</code>'
        f'<span class="source-open">Open at {src["commit"]}</span></a></li>'
        for src in cited)
    more = ""
    if sources or notes:
        more = (f'<details class="learn-more"><summary>Sources and speaker notes</summary>'
                + (f'<ul class="source-list">{sources}</ul>' if sources else "")
                + (f'<p class="drawer-notes">{notes}</p>' if notes else "")
                + "</details>")
    label = "" if bare else f' aria-labelledby="{slide["id"]}-title"'
    return (f'<section class="learn-section{" is-proof" if chip else ""}" id="{slide["id"]}"'
            f' data-number="{slide["number"]}"{media}{label}>'
            f'{heading}<div class="learn-body">{content}{slide_cta(deck, slide, site_base)}</div>'
            f'{narration}{more}</section>')


def learn_page(deck: dict, manifest: dict, provenance: dict, site_base: str,
               text_only: bool = False, units: list[dict] | None = None,
               unit_meta: dict[str, str] | None = None) -> str:
    """Learn (#112): the module as one page. No slides: each unit is a part of the page, each former
    slide a section with its narration as text, and a mini-player that reads the page aloud, section
    after section, highlighting the sentence it is on. The text-first copy is the same page, silent."""
    deck_manifest = (manifest.get("decks", {}).get(deck["id"], {}) or {}).get("slides", {})
    prov_by_audio = {rec.get("audio"): rec for rec in provenance.get("recordings", [])}
    preview_count = sum(1 for e in deck_manifest.values()
                        if prov_by_audio.get(e.get("audio"), {}).get("basis") == "sentence-measured-preview")
    recorded = len(deck_manifest)
    label = voice_label(deck_manifest, provenance, recorded, preview_count, text_only)
    if text_only:
        deck_manifest = {}
    units = units or []
    unit_meta = unit_meta or {}
    by_number = {sl["number"]: sl for sl in deck["slides"]}
    segments = [u for u in units if u["kind"] == "segment"]
    parts = []
    for u in units:
        span = [by_number[n] for n in range(u["first"], u["last"] + 1) if n in by_number]
        secs = sum(float((deck_manifest.get(sl["id"]) or {}).get("duration", 0) or 0) for sl in span)
        kicker = (f"Section {segments.index(u) + 1} of {len(segments)}" if u["kind"] == "segment"
                  else f"Unit {units.index(u) + 1} of {len(units)}")
        facts = [f"{len(span)} part{'s' if len(span) != 1 else ''}"]
        if secs:
            facts.append(f"{max(1, round(secs / 60))} min narrated")
        if unit_meta.get(u["id"]):
            facts.append(unit_meta[u["id"]])
        listen = (f'<button type="button" class="learn-listen-unit" data-listen-unit>{PLAY_ICON}'
                  f'<span>Listen to this unit</span></button>' if secs else "")
        uid = f"{deck['id']}:{u['id']}"
        sections = "".join(
            learn_section(deck, sl, deck_manifest.get(sl["id"]), site_base,
                          bare=sl["cover"] or (u["kind"] == "segment" and sl["number"] == u["first"]))
            for sl in span)
        # Read to its end, a teaching unit is recorded as read (#84); the lab and the check are
        # completed on their own pages.
        end = (f'<span class="read-end" data-read-unit="{html.escape(uid, quote=True)}" aria-hidden="true"></span>'
               if u["kind"] not in ("lab", "quiz") else "")
        parts.append(
            f'<section class="learn-unit" id="unit-{html.escape(u["id"].lower().replace(".", "-"))}"'
            f' data-unit="{html.escape(uid, quote=True)}" data-unit-kind="{u["kind"]}"'
            f' data-first="{u["first"]}" data-last="{u["last"]}"'
            f' data-unit-label="{html.escape(SH.unit_name(u), quote=True)}">'
            f'<header class="learn-unit-head"><p class="page-kicker">{html.escape(kicker)}</p>'
            f'<h2>{html.escape(SH.unit_name(u))}</h2>'
            f'<p class="learn-unit-facts">{" · ".join(html.escape(f) for f in facts)}</p>{listen}</header>'
            f'{sections}{end}</section>')
    number = int(deck["id"][1:])
    short = re.sub(r"^M\d+\s*—\s*", "", deck["label"]).strip()
    total = sum(float(e.get("duration", 0) or 0) for e in deck_manifest.values())
    head_facts = [f"{len(units)} units", f"{len(deck['slides'])} parts"]
    if total:
        head_facts.append(f"{round(total / 60)} min narrated")
    head = SH.page_head(f"Module {number} · Learn · " + " · ".join(head_facts), html.escape(short), "",
                        f'<p class="learn-voice">{html.escape(label)}</p>')
    player = "" if not deck_manifest else f"""<div class="learn-player" data-learn-player role="group" aria-label="Narration">
  <button type="button" class="lp-icon" data-lp-prev aria-label="Previous part">{CHEVRON.format(d="M15 18l-6-6 6-6")}</button>
  <button type="button" class="lp-play" data-lp-play aria-label="Play narration">{PLAY_ICON}</button>
  <button type="button" class="lp-icon" data-lp-next aria-label="Next part">{CHEVRON.format(d="M9 6l6 6-6 6")}</button>
  <p class="lp-now"><span class="lp-where" data-lp-where>Press play to listen from the start</span><span class="lp-time" data-lp-time></span></p>
  <label class="sr-only" for="lp-speed">Narration speed</label>
  <select class="lp-speed" id="lp-speed" data-lp-speed>
    <option value="0.75">0.75×</option><option value="1" selected>1×</option>
    <option value="1.25">1.25×</option><option value="1.5">1.5×</option>
  </select>
  <label class="lp-auto"><input type="checkbox" data-lp-auto checked> Continue</label>
  <p class="sr-only" data-lp-status role="status" aria-live="polite"></p>
</div>"""
    next_module = f"m{number + 1:02d}"
    body = f"""{head}
<div class="learn doc-article" data-learn="{deck['id']}">
{"".join(parts)}
<p class="learn-foot"><a href="{site_base}/lesson-{deck['id']}.html">Read the full lesson →</a> ·
  <a href="{site_base}/transcript-{deck['id']}.html">The module's transcript →</a> ·
  <a href="{site_base}/{('module-' + next_module + '.html') if next_module in DECK_IDS else 'index.html'}">Next module →</a></p>
</div>
{player}"""
    unit_data = [{"id": u["id"], "first": u["first"], "last": u["last"], "kind": u["kind"],
                  "name": SH.unit_name(u)} for u in units]
    attrs = (f' data-learn-deck="{deck["id"]}" data-deck-label="{html.escape(deck["label"], quote=True)}"'
             f' data-units="{html.escape(json.dumps(unit_data), quote=True)}"')
    return SH.document(f"{deck['label']} — AI Product Studio", deck["label"], body, site_base,
                       "doc-page learn-page", crumbs=SH.module_crumbs(site_base, deck, "Learn"),
                       deck_id=deck["id"], current="watch", mode="watch",
                       scripts=("narration-media.js", "learn.js"), body_attrs=attrs)


def index_page(decks: list[dict], manifest: dict, provenance: dict, site_base: str,
               text_only: bool = False, path_cards: str = "",
               module_paths: dict[str, int] | None = None,
               units_by_deck: dict[str, list[dict]] | None = None,
               proof_html: str = "", subscribe_action: str = "",
               home_data: dict | None = None) -> str:
    """Home (#79). A returning learner lands on where they were and what is next; a first-time
    visitor gets the pitch and the first-win start. Both are built here; `home.js` shows the one
    that fits from the stored progress, so the page works as a static file."""
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
    import site_paths as SP                                                      # noqa: PLC0415
    cards = []
    grand_total = 0.0
    for deck in decks:
        entries = (manifest.get("decks", {}).get(deck["id"], {}) or {}).get("slides", {})
        grand_total += sum(float(e.get("duration", 0) or 0) for e in entries.values())
        short = re.sub(r"^M\d+\s*—\s*", "", deck["label"]).strip()
        # A plain light card (#84): it must never read as a slide or a video. Title, what the module
        # builds, its size, the learner's recorded progress, and one action — Start, or Resume.
        shared_n = (module_paths or {}).get(deck["id"], 0)
        shared = f" · shared by {shared_n} paths" if shared_n > 1 else ""
        module_href = f"{site_base}/module-{deck['id']}.html"
        units = (units_by_deck or {}).get(deck["id"], [])
        unit_ids = ",".join(f"{deck['id']}:{u['id']}" for u in units)
        promise = SP.cover_facts(deck)["promise"]
        cards.append(f"""<article class="module-card" data-card-module="{deck['id']}">
  <p class="card-kicker">Module {int(deck['id'][1:])}{shared} <span class="voice-chip is-release" data-quiz-badge="{deck['id']}" hidden></span></p>
  <h3><a href="{module_href}">{html.escape(short)}</a></h3>
  <p class="card-promise">{html.escape(promise)}</p>
  <p class="card-meta">{len(deck['slides'])} slides · {len(units)} units · lab · knowledge check</p>
  <p class="card-progress"><span class="card-bar" data-ring-units="{unit_ids}" role="img" aria-label="progress"><span class="card-bar-fill"></span></span>
    <span class="card-count" data-ring-text></span></p>
  <a class="card-action" href="{module_href}" data-card-action>Start</a>
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
        section_note = "Each card shows your recorded progress and one next step."
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
        section_note = "Each card shows your recorded progress and one next step."
        first_howto = ('      <li>Narration never autoplays — press <strong>Play</strong> in the '
                       'player bar under any slide.</li>\n'
                       '      <li>Captions are on by default. The transcript sits under the slide and '
                       'follows the narration, and the\n'
                       f'          <a href="{site_base}/transcripts/ALL.md">complete transcript</a> '
                       'covers all nine modules in one file.</li>')
        footnote = ("Speaker notes are the presenter's version; the narration is the learner's. "
                    "Recordings currently use a free preview voice and say so wherever they appear — the "
                    "released voice is recorded separately and the words do not change.")
    head = SH.page_head(
        "AI Product Studio · edition 2026.09 · nine modules",
        "Ship AI products a skeptical engineer can audit.",
        "Three production repositories — an on-device meeting copilot, a multi-tenant SaaS built with "
        "AI agents under written rules, and an evidence-cited briefing site — taught as one method: "
        "spec it, build it, validate it, prove it. Nine narrated modules, labs whose pass criteria are "
        "objective, and a course that checks its own claims every time it is built.",
        f"""<ul class="site-facts">
{facts}
    </ul>
    <div class="hero-actions">
      <a class="btn-hero" href="{site_base}/lab-m00.html">Start here: your first win in about 30 minutes →</a>
      <a class="btn-hero-quiet" href="{site_base}/proof.html">See what this site proves about itself</a>
    </div>""")
    home_json = html.escape(json.dumps(home_data or {}, separators=(",", ":")), quote=True)
    returning = f"""<div class="home-returning" data-continue data-home="{home_json}" hidden>
  <header class="page-head home-head">
    <h1>Pick up where you left off</h1>
    <p class="page-lede"><span data-home-path>The full studio course</span> · labs graded pass/fail against real
      repositories · <a href="{site_base}/paths.html">Change path</a></p>
  </header>
  <section class="resume-card" aria-labelledby="resume-title">
    <div class="resume-thumb" aria-hidden="true">
      <span class="thumb-kicker" data-thumb-kicker></span>
      <span class="thumb-title" data-thumb-title></span>
      <span class="thumb-line"></span><span class="thumb-line is-short"></span>
    </div>
    <div class="resume-body">
      <p class="resume-where" data-resume-where></p>
      <h2 id="resume-title" data-resume-unit></h2>
      <p class="resume-slide" data-resume-slide></p>
      <p class="card-progress"><span class="card-bar"><span class="card-bar-fill" data-resume-fill></span></span>
        <span class="card-count" data-resume-count></span></p>
      <div class="resume-actions">
        <a class="btn-start" href="{site_base}/index.html" data-resume-link data-continue-link>
          <svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M7 4l13 8-13 8z" fill="currentColor" stroke="none"/></svg>
          <span>Resume</span></a>
        <a class="btn-outline" href="{site_base}/index.html" data-resume-read>Read this segment instead</a>
      </div>
    </div>
  </section>
  <div class="home-row">
    <section class="next-steps" aria-labelledby="next-title">
      <h2 id="next-title" data-next-title>Next</h2>
      <ul class="next-list" data-next-list></ul>
    </section>
    {proof_html}
  </div>
  <div class="progress-tools">
    <span>Your progress lives in this browser.</span>
    <button type="button" data-progress-export title="Download your progress as JSON">Export progress</button>
    <button type="button" data-progress-import title="Load a progress file">Import</button>
    <button type="button" data-progress-reset>Reset</button>
  </div>
</div>"""
    content = f"""{returning}
<div class="home-new" data-home-new>
{head}
{proof_html}
</div>
  <div class="section-heading">
    <h2>Start with what you want to build</h2>
    <span class="section-note">Each path teaches one product type end to end. Not sure what a
      <a href="{site_base}/paths.html">path or a unit</a> is?</span>
  </div>
  <div class="path-grid">
{path_cards}
  </div>
  <div class="section-heading">
    <h2>All modules</h2>
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
      <li><strong>Present</strong> goes full screen for a room; <strong>Read</strong> is the lesson as
          one document; <strong>Sources on this slide</strong> opens every file a slide cites, with the
          presenter notes.</li>
      <li>Keyboard: <kbd>←</kbd> <kbd>→</kbd> slide, <kbd>Space</kbd> play, <kbd>T</kbd> transcript,
          <kbd>F</kbd> present, <kbd>Home</kbd>/<kbd>End</kbd> first/last, <kbd>Esc</kbd> close.</li>
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
  <p class="index-footnote">{footnote} Progress, quiz scores and lab checklists are stored in this browser only — export them from the strip above to move machines.</p>"""
    return SH.document("AI Product Studio — narrated course",
                       "Build, ship and sell three kinds of AI product. Nine narrated modules with "
                       "captions and transcripts.", content, site_base, "index home-page",
                       crumbs=[("Home", None)], current="home", scripts=("home.js",))


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
    # Screenshot copies for figures (#100) ship with the site, in every copy of it: they are the
    # byte-identical files course/figures/manifest.json records, never regenerated here.
    shots = COURSE_DIR / "figures" / "shots"
    if shots.is_dir():
        shutil.copytree(shots, target / "figures" / "shots", dirs_exist_ok=True)
    # What the *player* is told. In a text-first publish this is deliberately empty: the recordings
    # exist, but offering them would mean offering files the published copy does not contain.
    player_manifest = {"decks": {}} if args.no_narration else manifest
    write_json(target / "narration.json", player_manifest)

    import site_paths as SP                                                       # noqa: PLC0415
    import site_content as SC                                                     # noqa: PLC0415
    import site_pages as SPG                                                      # noqa: PLC0415
    units_by_deck = {deck["id"]: SP.module_units(deck) for deck in decks}
    figs_by_deck = {deck["id"]: FIG.deck_figures(deck, units_by_deck[deck["id"]]) for deck in decks}
    # Every page carries the course outline (#73), so the shell learns the modules, their units and
    # the paths once, before the first page is written.
    SH.configure(decks, units_by_deck, SP.TRACKS)
    for deck in decks:
        folder = COURSE_DIR / deck["source"].rsplit("/", 1)[0]
        try:
            questions = len(SC.parse_quiz(SC.read(folder / "quiz.md"), deck["id"])["questions"])
        except SC.QuizError as error:
            raise SystemExit(f"knowledge check: {error}")
        meta = {"lab": f"{SP.lab_time(deck['id'])} hands-on", "quiz": f"{questions} questions"}
        (target / f"{deck['id']}.html").write_text(
            learn_page(deck, manifest, provenance, args.site_base, text_only=args.no_narration,
                       units=units_by_deck[deck["id"]], unit_meta=meta),
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
    labs_for_log: list[dict] = []
    for deck in decks:
        folder = COURSE_DIR / deck["source"].rsplit("/", 1)[0]
        for kind in ("lesson", "handout", "glossary"):
            html_out, record = SPG.document_page(deck, kind, SC.read(folder / f"{kind}.md"),
                                                 args.site_base, BRAND_MARK,
                                                 figs_by_deck[deck["id"]]["segments"])
            (target / f"{kind}-{deck['id']}.html").write_text(html_out, encoding="utf-8")
            record["module"] = SPG.short_label(deck)
            if kind == "glossary":
                record["terms"] = SC.parse_glossary(SC.read(folder / "glossary.md"))
                terms_by_deck[deck["id"]] = record["terms"]
            records.append(record)
        lab = SC.parse_lab(SC.read(folder / "lab.md"), deck["id"])
        rubrics = folder / "lab-rubrics.md"
        auto_fail = SC.parse_auto_fail(SC.read(rubrics)) if rubrics.is_file() else None
        html_out, record = SPG.lab_page(deck, lab, args.site_base, BRAND_MARK, auto_fail)
        (target / f"lab-{deck['id']}.html").write_text(html_out, encoding="utf-8")
        labs_for_log.append({"deck": deck["id"], "title": lab["title"],
                             "checks": lab["checklist_count"]})
        record["module"] = SPG.short_label(deck)
        records.append(record)
        try:
            quiz = SC.parse_quiz(SC.read(folder / "quiz.md"), deck["id"])
        except SC.QuizError as error:
            raise SystemExit(f"knowledge check: {error}")
        html_out, record = SPG.quiz_page(deck, quiz, args.site_base, BRAND_MARK, units_by_deck[deck["id"]])
        (target / f"quiz-{deck['id']}.html").write_text(html_out, encoding="utf-8")
        record["module"] = SPG.short_label(deck)
        records.append(record)
    # EN / 中文 (#116): the terms locale.js names beside their first use, per module.
    (target / "assets").mkdir(parents=True, exist_ok=True)
    (target / "assets" / "terms-zh.js").write_text(SL.script(terms_by_deck, SL.load()), encoding="utf-8")
    decks_by_id_for_glossary = {deck["id"]: deck for deck in decks}
    (target / "glossary.html").write_text(
        SPG.master_glossary_page(terms_by_deck, decks_by_id_for_glossary, args.site_base, BRAND_MARK),
        encoding="utf-8")
    (target / "evidence.html").write_text(SPG.evidence_page(labs_for_log, args.site_base),
                                          encoding="utf-8")
    # When each narration sentence is spoken, from the published captions: a search hit on a spoken
    # sentence opens the player there (#80). A text-first copy publishes no captions, so no times.
    times = {} if args.no_narration else {deck["id"]: spoken_times(deck, manifest) for deck in decks}
    (target / "search.json").write_text(SPG.search_index(records, decks, units_by_deck, times), encoding="utf-8")
    decks_by_id = {deck["id"]: deck for deck in decks}
    built_tracks = [t for t in SP.TRACKS if t["status"] == "built"]
    built_modules = {d for t in built_tracks for d in list(t["core"]) + list(t.get("slice") or {})}
    for deck_id in sorted(built_modules):
        # Every path that includes the module, not a single owner: modules are shared, and a
        # module page that named one path would misdescribe the other two.
        tracks_for = SP.paths_for_module(deck_id, built_tracks)
        (target / f"module-{deck_id}.html").write_text(
            SP.module_page(decks_by_id[deck_id], units_by_deck[deck_id], seconds, args.site_base,
                           BRAND_MARK, tracks_for, args.no_narration,
                           hero=figs_by_deck[deck_id]["hero"]), encoding="utf-8")
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
    # What the home page needs to say where a learner is and what is next (#79): each module's units
    # with their slides, where each starts in the lesson, the lab's time and the check's size.
    anchors = {r["deck"]: r.get("read_anchors", {}) for r in records if r["kind"] == "lesson"}
    questions = {r["deck"]: len(r.get("headings", [])) for r in records if r["kind"] == "quiz"}
    home_data = {"modules": {deck["id"]: {
        "number": int(deck["id"][1:]), "title": SH.short_label(deck), "slides": len(deck["slides"]),
        "lab": SP.lab_time(deck["id"]), "questions": questions.get(deck["id"], 0),
        "units": [{"id": u["id"], "kind": u["kind"], "name": SH.unit_name(u), "label": u["label"],
                   "first": u["first"], "last": u["last"], "href": SH.unit_href(deck["id"], u),
                   "read": anchors.get(deck["id"], {}).get(u["id"], "")}
                  for u in units_by_deck[deck["id"]]]} for deck in decks}}
    (target / "proof.html").write_text(
        SH.document("What this site proves — AI Product Studio",
                    "What the build measured about itself: pointers, facts, lab runs and narration.",
                    SH.page_head("Proof", "How each number is checked",
                                 "The numbers on the home page, and the checks that measured them when "
                                 "this site was built.")
                    + SPR.proof_section(proof, args.site_base),
                    args.site_base, "doc-page proof-page",
                    crumbs=[("Course", f"{args.site_base}/index.html"), ("Proof", None)]),
        encoding="utf-8")
    (target / "index.html").write_text(
        index_page(decks, manifest, provenance, args.site_base, text_only=args.no_narration,
                   subscribe_action=args.subscribe_action,
                   path_cards=path_cards, module_paths=module_paths, units_by_deck=units_by_deck,
                   proof_html=SPR.proof_card(proof, args.site_base), home_data=home_data),
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
              f"run `python3 ../06-production/narration/generate_narration.py generate --provider preview`")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
