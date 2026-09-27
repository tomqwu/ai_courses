"""Figures (#99): architecture, flow, compare, screenshot and scene, declared in the Markdown.

A slide or a lesson writes a ```figure fence; this module parses it and renders HTML — cards, layered
bands and columns joined by inline SVG connectors, or a framed image with numbered callouts — styled
only with the Studio tokens in player.css. The text is HTML, so it wraps on a phone, uses the slide's
type scale and is contrast-audited like every other line.

The grammar, one `key: value` per line:

    kind: flow | architecture | compare | screenshot | scene
    alt: One sentence describing what the figure shows.          (required)
    source: Repo/path:N-M                                         (when it depicts a case study)
    title: A caption shown under the figure
    step: capture (seam) — mic and system audio @ Here is the whole system      (flow)
    loop: yes                                                                     (flow)
    layer: App/ glue — platform code implements the seams                        (architecture)
      box: capture (seam)
    column: Fail closed (good)                                                    (compare)
      item: an unknown host throws
    image: signupflow-dashboard.png · frame: browser | phone | mac | none               (screenshot)
    callout: 12,30 — The admin sees gaps before members do
    scene: stranger-clone.svg · caption: …                                        (scene)

A part's value is `label [(flags)] [— note] [@ at-words]`. Flags are seam, hl, good, bad, and
chain (a layer whose boxes are a sequence, drawn joined by connectors); the
`at-words` are the opening words of the narration sentence at which the part builds in, and become
`data-step` when the slide's sentences are known.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

KINDS = ("flow", "architecture", "compare", "screenshot", "scene")
FRAMES = ("browser", "phone", "mac", "none")    # none: the image carries its own window chrome
FLAGS = {"seam", "hl", "good", "bad", "chain"}
REPEATED = {"step", "layer", "column"}
CHILDREN = {"box", "item"}
SCENES = Path(__file__).resolve().parents[1] / "figures" / "scenes"

LINK = ('<svg class="fig-link" viewBox="0 0 40 16" aria-hidden="true" focusable="false">'
        '<path class="fig-link-line" d="M2 8h29"/><path class="fig-link-head" d="M27 3l7 5-7 5"/></svg>')
FLAG_WORDS = {"seam": "seam", "hl": "in focus"}
TONE_ICON = {
    "good": ('<svg class="fig-tone" viewBox="0 0 20 20" role="img" aria-label="holds">'
             '<path d="M5 10.5l3.2 3.2L15 6.8"/></svg>'),
    "bad": ('<svg class="fig-tone" viewBox="0 0 20 20" role="img" aria-label="breaks">'
            '<path d="M6 6l8 8M14 6l-8 8"/></svg>'),
}


class FigureError(ValueError):
    """A figure block that cannot be drawn: the build fails rather than ship a broken figure."""


# ---------------------------------------------------------------- parsing

def _part(value: str) -> dict:
    """`label [(flags)] [— note] [@ at-words]` → a part."""
    at = ""
    if " @ " in value:
        value, at = value.rsplit(" @ ", 1)
    note = ""
    if " — " in value:
        value, note = value.split(" — ", 1)
    label, flags = _flags(value.strip())
    note, more = _flags(note.strip())       # flags may also close the note: `API — real JWT (hl)`
    return {"label": label, "note": note, "flags": flags | more, "at": at.strip(), "children": []}


def _flags(text: str) -> tuple[str, set]:
    """Split a trailing `(seam, hl)` off `text` — only when every word in it is a flag."""
    m = re.search(r"\s*\(([a-z ,]+)\)$", text)
    words = set(re.split(r"[ ,]+", m.group(1).strip())) if m else set()
    if m and words <= FLAGS:
        return text[:m.start()].strip(), words
    return text, set()


def parse(text: str) -> dict:
    fig = {"kind": "", "alt": "", "source": "", "title": "", "items": [], "loop": False,
           "image": "", "frame": "browser", "scene": "", "caption": "", "callouts": []}
    for n, raw in enumerate(text.splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indented = raw.startswith("  ")
        key, sep, value = raw.strip().partition(":")
        key, value = key.strip().lower(), value.strip()
        if not sep:
            raise FigureError(f"line {n}: expected `key: value`, got {raw.strip()!r}")
        if indented and key in CHILDREN:
            if not fig["items"]:
                raise FigureError(f"line {n}: `{key}:` has no layer or column above it")
            fig["items"][-1]["children"].append(_part(value))
        elif key in REPEATED:
            fig["items"].append(_part(value))
        elif key == "callout":
            m = re.match(r"^([\d.]+)\s*,\s*([\d.]+)\s*—\s*(.+)$", value)
            if not m:
                raise FigureError(f"line {n}: a callout is `x,y — text` in percent")
            fig["callouts"].append({"x": float(m.group(1)), "y": float(m.group(2)), "text": m.group(3).strip()})
        elif key == "loop":
            fig["loop"] = value.lower() in ("yes", "true", "1")
        elif key in fig:
            fig[key] = value
        else:
            raise FigureError(f"line {n}: unknown key `{key}`")
    if fig["kind"] not in KINDS:
        raise FigureError(f"kind must be one of {', '.join(KINDS)} (got {fig['kind']!r})")
    if not fig["alt"]:
        raise FigureError("a figure needs `alt:` — one sentence saying what it shows")
    if fig["kind"] == "screenshot" and not fig["image"]:
        raise FigureError("a screenshot needs `image:`")
    if fig["kind"] == "scene" and not fig["scene"]:
        raise FigureError("a scene needs `scene:`")
    if fig["kind"] in ("flow", "architecture", "compare") and not fig["items"]:
        raise FigureError(f"a {fig['kind']} figure needs parts")
    return fig


# ---------------------------------------------------------------- _diagram lists

LABEL_CAPTION = re.compile(r"^(.*?)(?::\s+|\s+—\s+)(.*)$", re.S)


def _split(raw: str) -> tuple[str, str]:
    m = LABEL_CAPTION.match(raw.strip())
    return (m.group(1).strip(), m.group(2).strip()) if m else (raw.strip(), "")


def from_list(kind: str, items: list[str]) -> dict:
    """A declared `_diagram` list as a figure, word for word: flow, loop and steps become a flow,
    stack becomes layered bands, grid becomes columns."""
    fig = {"kind": "flow", "alt": "", "source": "", "title": "", "items": [], "loop": kind == "loop",
           "image": "", "frame": "browser", "scene": "", "caption": "", "callouts": [],
           "numbered": kind == "steps", "from_list": True}
    if kind in ("flow", "loop", "steps"):
        for raw in items:
            label, note = _split(raw)
            flags = {"seam"} if re.search(r"\bseam\b", raw, re.I) else set()
            fig["items"].append({"label": label, "note": note, "flags": flags, "at": "", "children": []})
    elif kind == "stack":
        fig["kind"] = "architecture"
        for raw in items:
            chain = [c.strip() for c in raw.split("→")] if " → " in raw else []
            seam = raw.strip().lower().startswith("seam")
            flags = ({"seam"} if seam else set()) | ({"chain"} if chain else set())
            layer = {"label": "" if chain else raw.strip(), "note": "", "flags": flags,
                     "at": "", "children": [{"label": c, "note": "", "flags": set(), "at": "", "children": []}
                                            for c in chain]}
            fig["items"].append(layer)
    elif kind == "grid":
        fig["kind"] = "compare"
        for raw in items:
            label, note = _split(raw)
            fig["items"].append({"label": label, "note": "", "flags": set(), "at": "",
                                 "children": [{"label": note, "note": "", "flags": set(), "at": "", "children": []}]
                                 if note else []})
    else:
        raise FigureError(f"unknown diagram kind: {kind}")
    fig["alt"] = " → ".join(re.sub(r"[`*]", "", p["label"]) for p in fig["items"] if p["label"])[:240] or kind
    return fig


# ---------------------------------------------------------------- build-in steps

def _norm(text: str) -> str:
    return " ".join(re.sub(r"[`*_“”\"'’]", "", text).lower().split())


def step_index(at: str, sentences: list[str]) -> int | None:
    """The index of the narration sentence that opens with `at`, or None."""
    want = _norm(at)
    if not want:
        return None
    for i, sentence in enumerate(sentences):
        if _norm(sentence).startswith(want):
            return i
    return None


# ---------------------------------------------------------------- rendering

def _esc(text: str) -> str:
    return html.escape(text, quote=False)


def _classes(base: str, part: dict) -> str:
    extra = "".join(f" is-{f}" for f in sorted(part["flags"]))
    return f"{base}{extra}"


def _step(part: dict, sentences: list[str] | None) -> str:
    if not sentences or not part["at"]:
        return ""
    i = step_index(part["at"], sentences)
    return f' data-step="{i}"' if i is not None else ""


def _tags(part: dict) -> str:
    return "".join(f'<span class="fig-flag">{FLAG_WORDS[f]}</span>' for f in sorted(part["flags"]) if f in FLAG_WORDS)


def _body(part: dict, inline) -> str:
    note = f'<span class="fig-note">{inline(part["note"])}</span>' if part["note"] else ""
    label = f'<span class="fig-label">{inline(part["label"])}</span>' if part["label"] else ""
    return f"{label}{note}{_tags(part)}"


def _flow(fig: dict, sentences, inline) -> str:
    nodes = []
    for i, part in enumerate(fig["items"]):
        if i:
            nodes.append(LINK)
        number = f'<span class="fig-number">{i + 1}</span>' if fig.get("numbered") else ""
        nodes.append(f'<div class="{_classes("fig-node", part)}"{_step(part, sentences)}>{number}{_body(part, inline)}</div>')
    loop = ('<svg class="fig-loop" viewBox="0 0 100 12" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
            '<path d="M97 1v5H3V1"/></svg>') if fig["loop"] else ""
    layout = " is-numbered" if fig.get("numbered") else ""
    return f'<div class="fig-track{layout}">{"".join(nodes)}</div>{loop}'


def _architecture(fig: dict, sentences, inline) -> str:
    bands = []
    for layer in fig["items"]:
        boxes = []
        for i, box in enumerate(layer["children"]):
            if i and "chain" in layer["flags"]:
                boxes.append(LINK)          # a chain: its boxes are a sequence
            boxes.append(f'<div class="{_classes("fig-box", box)}"{_step(box, sentences)}>{_body(box, inline)}</div>')
        head = (f'<div class="fig-band-head">{_body(layer, inline)}</div>'
                if layer["label"] or layer["note"] else "")
        row = f'<div class="fig-row">{"".join(boxes)}</div>' if boxes else ""
        bands.append(f'<div class="{_classes("fig-layer", layer)}"{_step(layer, sentences)}>{head}{row}</div>')
    return f'<div class="fig-bands">{"".join(bands)}</div>'


def _compare(fig: dict, sentences, inline) -> str:
    cols = []
    for col in fig["items"]:
        tone = next((TONE_ICON[f] for f in ("good", "bad") if f in col["flags"]), "")
        items = "".join(f'<li{_step(item, sentences)}>{inline(item["label"])}'
                        + (f' <span class="fig-note">{inline(item["note"])}</span>' if item["note"] else "")
                        + "</li>" for item in col["children"])
        cols.append(f'<div class="{_classes("fig-column", col)}"{_step(col, sentences)}>'
                    f'<p class="fig-column-head">{tone}<span class="fig-label">{inline(col["label"])}</span></p>'
                    + (f'<ul class="fig-items">{items}</ul>' if items else "")
                    + (f'<p class="fig-note">{inline(col["note"])}</p>' if col["note"] else "")
                    + "</div>")
    return f'<div class="fig-columns" style="--cols:{max(1, len(cols))}">{"".join(cols)}</div>'


def _screenshot(fig: dict, base: str, inline) -> str:
    pins = "".join(f'<span class="fig-pin" style="left:{c["x"]:g}%;top:{c["y"]:g}%" aria-hidden="true">{i}</span>'
                   for i, c in enumerate(fig["callouts"], 1))
    if fig["frame"] not in FRAMES:
        raise FigureError(f"frame must be one of {', '.join(FRAMES)} (got {fig['frame']!r})")
    chrome = '<div class="fig-chrome" aria-hidden="true"><span></span><span></span><span></span></div>' \
        if fig["frame"] in ("browser", "mac") else ""
    notes = ("<ol class=\"fig-callouts\">" + "".join(f"<li>{inline(c['text'])}</li>" for c in fig["callouts"]) + "</ol>"
             if fig["callouts"] else "")
    src = f"{base}/figures/shots/{fig['image']}"
    return (f'<div class="fig-frame fig-frame-{_esc(fig["frame"])}">{chrome}'
            f'<div class="fig-shot"><img src="{html.escape(src, quote=True)}" alt="{html.escape(fig["alt"], quote=True)}"'
            f' loading="lazy">{pins}</div></div>{notes}')


def _scene(fig: dict, inline) -> str:
    path = SCENES / fig["scene"]
    if not path.is_file():
        raise FigureError(f"scene not found: course/figures/scenes/{fig['scene']}")
    svg = path.read_text(encoding="utf-8")
    svg = re.sub(r"^<\?xml[^>]*>\s*", "", svg)
    svg = svg.replace("<svg ", f'<svg role="img" aria-label="{html.escape(fig["alt"], quote=True)}" ', 1)
    caption = f'<figcaption class="fig-title">Illustration · {inline(fig["caption"])}</figcaption>' if fig["caption"] else \
        '<figcaption class="fig-title">Illustration</figcaption>'
    return f'<div class="fig-scene-art">{svg}</div>{caption}'


def render(fig: dict, *, sentences: list[str] | None = None, inline=_esc, base: str = ".") -> str:
    """The figure as HTML. With `sentences`, parts whose `at` opens a sentence get `data-step`."""
    kind = fig["kind"]
    if kind == "flow":
        inner = _flow(fig, sentences, inline)
    elif kind == "architecture":
        inner = _architecture(fig, sentences, inline)
    elif kind == "compare":
        inner = _compare(fig, sentences, inline)
    elif kind == "screenshot":
        inner = _screenshot(fig, base, inline)
    elif kind == "scene":
        inner = _scene(fig, inline)
    else:
        raise FigureError(f"unknown kind {kind!r}")
    alt = "" if kind in ("screenshot", "scene") else f'<figcaption class="sr-only">{_esc(fig["alt"])}</figcaption>'
    title = (f'<figcaption class="fig-title">{inline(fig["title"])}</figcaption>'
             if fig["title"] and kind != "scene" else "")
    source = (f'<p class="fig-source"><span class="source-chip">Source</span><code>{_esc(fig["source"])}</code></p>'
              if fig["source"] else "")
    stepped = " is-stepped" if "data-step=" in inner else ""
    listed = " is-from-list" if fig.get("from_list") else ""
    return (f'<figure class="diagram fig fig-{kind}{stepped}{listed}" data-figure>'
            f'{alt}{inner}{title}{source}</figure>')


# ---------------------------------------------------------------- reuse outside the player

FIGURE_HTML = re.compile(r'<figure class="diagram[^"]*" data-figure>.*?</figure>', re.S)


def first_figure(rendered: str) -> str:
    """The first figure in a rendered slide, complete: the module page and Read have no narration
    to build it on, so its steps are dropped."""
    m = FIGURE_HTML.search(rendered)
    if not m:
        return ""
    return re.sub(r' data-step="\d+"', "", m.group(0)).replace(" is-stepped", "")


def deck_figures(deck: dict, units: list[dict]) -> dict:
    """The module's hero (the cover slide's figure) and each segment opener's figure, by unit id."""
    by_number = {s["number"]: s for s in deck["slides"]}
    hero = first_figure(by_number[1]["html"]) if 1 in by_number else ""
    segments = {}
    for unit in units:
        if unit["kind"] == "segment" and unit["first"] in by_number:
            fig = first_figure(by_number[unit["first"]]["html"])
            if fig:
                segments[unit["id"]] = fig
    return {"hero": hero, "segments": segments}
