"""Learning paths — the Microsoft Learn hierarchy, applied to this course.

Microsoft Learn organises training as a strict four-level hierarchy:

    Career path -> Learning path -> Module -> Unit

and every module follows one fixed unit grammar:

    Introduction -> content units -> Exercise -> Knowledge check -> Summary

This course already had every level; it just did not surface one. The mapping is:

    Learning path  = a track bundle in course/05-tracks/   (4 of them)
    Module         = m00-m08                               (9)
    Unit           = a lesson segment, plus intro/lab/quiz/summary (63 total)

Durations are *measured* from the narration manifest, not estimated, which is the one place this
deliberately beats the model it copies. Lab times are quoted from the module's own source because a
lab's working time is not narration and must never be inferred from it.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

COURSE_DIR = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------- unit model

NUM = re.compile(r"^[mM](\d+)$")
SEGMENT = re.compile(r"^M\d+\.\d+$")
LAB = re.compile(r"^Lab\s+M\d+")
QUIZ = re.compile(r"^Quiz\s+M\d+")
SUMMARY = re.compile(r"^(Recap|Summary|Discussion)", re.I)

KIND_LABEL = {
    "intro": "Introduction",
    "segment": "Lesson",
    "lab": "Exercise",
    "quiz": "Knowledge check",
    "summary": "Summary",
}


def module_units(deck: dict) -> list[dict]:
    """Partition a deck's slides into units, in order, covering every slide exactly once.

    The boundary rules are read off the course's own structure rather than invented:

    * slides 1-2 are always the cover and the "By the end you can…" objectives, so they are the
      module's Introduction (Microsoft's first unit) in every deck without exception;
    * a slide whose *title* opens ``Lab M#``, ``Quiz M#`` or ``Recap`` starts an Exercise, a
      knowledge check or a Summary — matched on the title, because the deck chrome deliberately
      falls back to the module tag for these and never shows ``Quiz M#`` as a kicker;
    * a slide whose kicker is ``M#.#`` starts that segment;
    * a module that marks fewer segments than it declares (m08 has no ``M8.1`` heading at all)
      still opens segment 1 at the first content slide, which is what the declared count means.

    ``check_player.py`` asserts the result covers all 233 slides exactly once, so a future edit to a
    deck that breaks a boundary fails the gate rather than silently mis-grouping a unit.
    """
    number = int(NUM.match(deck["id"]).group(1))
    units: list[dict] = []
    current: dict | None = None
    seen_segment = False

    for slide in deck["slides"]:
        title, kicker, n = slide["title"], slide["kicker"], slide["number"]
        if n <= 2:
            kind, uid, label = "intro", "intro", "Introduction"
        elif LAB.match(title) or LAB.match(kicker):
            kind, uid = "lab", "lab"
            label = re.sub(r"^Lab\s+M\d+\s*(—\s*)?", "", title).strip() or "Lab"
        elif QUIZ.match(title):
            kind, uid, label = "quiz", "quiz", "Knowledge check"
        elif SUMMARY.match(title) or (current and current["kind"] == "summary"):
            kind, uid, label = "summary", "summary", "Summary"
        elif SEGMENT.match(kicker):
            kind, uid, label = "segment", kicker, title
            seen_segment = True
        elif not seen_segment:
            kind, uid, label = "segment", f"M{number}.1", title
            seen_segment = True
        else:
            kind, uid, label = current["kind"], current["id"], current["label"]

        if current is None or uid != current["id"]:
            current = {"kind": kind, "id": uid, "label": label, "deck": deck["id"],
                       "first": n, "last": n, "slides": 1}
            units.append(current)
        else:
            current["last"] = n
            current["slides"] += 1

    for unit in units:
        unit["title"] = (unit["id"] if unit["kind"] == "segment"
                         else KIND_LABEL[unit["kind"]])
        unit["href"] = f"{deck['id']}.html#slide-{unit['first']}"
    return units


# ---------------------------------------------------------------- source facts

# Lab working time, quoted from each module's own source. A lab is hours of hands-on work whose
# narration is a one-slide introduction, so its narration seconds must never stand in for its
# duration. Where lab.md states a time that wins; otherwise the deck front matter is quoted.
LAB_TIME_FALLBACK = {
    "m01": "~2 hours", "m02": "~3 hours", "m04": "90–120 minutes",
    "m05": "~3 hours", "m06": "~2.5 hours",
}
LAB_TIME_RE = re.compile(r"\*\*Time:\*\*\s*([^·|\n]+?)\s*(?=·|\||$)", re.M)
LAB_TIME_RE2 = re.compile(r"(?:^|[·>])\s*Time:\s*([^·|\n]+?)\s*(?=·|\||$)", re.M)
PREREQ_RE = re.compile(r"Prerequisites?:?\*{0,2}\s*([^·|\n]+?)\s*(?=\s*·|\s*\*\*|\s*\||$)", re.M)
NOT_STATED = "not stated in the module source"


def _lab_file(deck_id: str) -> Path | None:
    matches = sorted(COURSE_DIR.glob(f"03-content/{deck_id}-*/lab.md"))
    return matches[0] if matches else None


def lab_time(deck_id: str) -> str:
    path = _lab_file(deck_id)
    if path:
        text = path.read_text(encoding="utf-8")
        for pattern in (LAB_TIME_RE, LAB_TIME_RE2):
            match = pattern.search(text)
            if match:
                value = match.group(1).strip().strip("*").strip()
                if value:
                    return value
    return LAB_TIME_FALLBACK.get(deck_id, NOT_STATED)


def _clean_prereq(value: str) -> str:
    """Tidy a prerequisite pulled out of a lab header.

    Lab headers are prose, and some wrap mid-sentence, so a capture can end inside an unclosed
    bracket. Rather than print half a parenthetical, cut back to the last balanced point — and say
    so plainly rather than guessing at the missing words.
    """
    value = re.sub(r"^[-*\u2022]\s*", "", value.strip())
    value = re.sub(r"\s+", " ", value).strip().strip("*").strip()
    if value.count("(") > value.count(")"):
        value = value[:value.rindex("(")].strip().rstrip(";,:")
    value = value.rstrip(" .;:")
    if not value or value.lower() in {"none", "n/a", "no prerequisites"}:
        return "None stated"
    return value[:1].upper() + value[1:]


def lab_prereq(deck_id: str) -> str:
    path = _lab_file(deck_id)
    if path:
        match = PREREQ_RE.search(path.read_text(encoding="utf-8"))
        if match:
            return _clean_prereq(match.group(1))
    return NOT_STATED


def cover_facts(deck: dict) -> dict:
    """Promise and lesson length, read from the cover slide's body (not the YAML front matter)."""
    body = deck["slides"][0].get("html", "")
    text = re.sub(r"<[^>]+>", " ", body)
    text = html.unescape(re.sub(r"\s+", " ", text))
    promise = re.search(r"Promise:\s*(.+?)\s*(?:Duration:|$)", text)
    duration = re.search(r"Duration:\s*(.+?)\s*$", text)
    return {"promise": promise.group(1).strip() if promise else "",
            "lesson_length": duration.group(1).strip() if duration else ""}


def objectives(deck: dict) -> list[str]:
    """The objectives list from slide 2 (“By the end you can…”)."""
    return re.findall(r"<li>(.*?)</li>", deck["slides"][1].get("html", ""), re.S)


# ---------------------------------------------------------------- the paths

# `core` modules are taught in full; `slice` modules contribute only the named segments. Both are
# copied from each bundle's own `bundle-map.md` rather than inferred from the module list.
TRACKS = [
    {
        "slug": "aps",
        "title": "The full studio course",
        "kicker": "All three archetypes",
        "promise": "Build, ship and sell all three kinds of AI product — and finish with a scored "
                   "capstone, a launch arc and a defensible price.",
        "core": ["m00", "m01", "m02", "m03", "m04", "m05", "m06", "m07", "m08"],
        "slice": {},
        "price": "$399 self-paced · $1,490 cohort",
        "level": "Beginner to intermediate",
        "role": "Founder · Product engineer",
        "status": "full",
        "page": None,  # the full course is the module index itself
    },
    {
        "slug": "on-device-app",
        "title": "On-Device AI Apps",
        "kicker": "Track 1 · Type 1",
        "promise": "Ship a local-first AI app whose privacy claims are enforced in code and proven "
                   "by tests.",
        "core": ["m00", "m01", "m02", "m03"],
        # Straight from the bundle map. `exclude` names the units the map lists as NOT included,
        # `partial` the ones included only in part. Without this the path page listed all seven M8
        # units — including M8.3, Lab M8 and Quiz M8 — and counted their narration as if taught.
        "slice": {
            "m07": {"note": "All three segments · Lab M7 steps 1–5 · Quiz M7",
                    "exclude": [], "partial": ["lab"]},
            "m08": {"note": "Segments M8.1–M8.2 only",
                    "exclude": ["M8.3", "lab", "quiz"], "partial": []},
        },
        "excluded": [
            ("M4 · M5 — the Spec-Driven SaaS track", "m04", "m05"),
            ("M6 — the Expertise track", "m06", None),
            ("M8.3 capstone, Lab M8 and Quiz M8", "m08", None),
        ],
        "price": "$199",
        "level": "Beginner to intermediate",
        "role": "iOS / macOS engineer · Indie developer",
        "subject": "Local-first AI · Privacy engineering",
        "measured": {"segments": (17, 27), "labs": (4, 8), "quizzes": (5, 9), "questions": (40, 72)},
        "status": "built",
        "page": "path-on-device-app.html",
    },
    {
        "slug": "spec-driven-saas",
        "title": "Spec-Driven AI SaaS",
        "kicker": "Track 2 · Type 2",
        "promise": "A spec folder that survives a stranger test, and acceptance evidence that "
                   "survives a skeptical auditor.",
        "core": ["m00", "m01", "m04", "m05"],
        "slice": {"m07": "Monetization slice", "m08": "Launch slice"},
        "price": "$199",
        "level": "Intermediate",
        "role": "Backend engineer · SaaS builder",
        "subject": "Multi-tenant security · Acceptance evidence",
        "status": "outline",
        "page": "path-spec-driven-saas.html",
    },
    {
        "slug": "expertise-product",
        "title": "Expertise as a Product",
        "kicker": "Track 3 · Type 3",
        "promise": "Every published claim carries a date, sample, method, unit and level — and the "
                   "funnel sells a measurement, not a promise.",
        "core": ["m00", "m01", "m06"],
        "slice": {"m07": "Monetization slice", "m08": "Launch slice"},
        "price": "$199",
        "level": "Intermediate",
        "role": "Consultant · Domain expert",
        "subject": "Evidence products · Content as code",
        "status": "outline",
        "page": "path-expertise-product.html",
    },
]

TRACK_BY_SLUG = {t["slug"]: t for t in TRACKS}


def slice_spec(track: dict, deck_id: str) -> dict:
    spec = (track.get("slice") or {}).get(deck_id) or {}
    return spec if isinstance(spec, dict) else {"note": spec, "exclude": [], "partial": []}


def track_units(track: dict, units_by_deck: dict[str, list[dict]]) -> list[dict]:
    """Every unit a path actually includes, in path order, tagged full or slice.

    Units the bundle map excludes are dropped here rather than rendered: a path's unit count and its
    narration total must describe what the buyer gets, not what the parent module contains.
    """
    out = []
    for deck_id in track["core"]:
        for unit in units_by_deck.get(deck_id, []):
            out.append({**unit, "inclusion": "full"})
    for deck_id in (track.get("slice") or {}):
        spec = slice_spec(track, deck_id)
        for unit in units_by_deck.get(deck_id, []):
            if unit["id"] in spec["exclude"]:
                continue
            out.append({**unit, "inclusion": "slice", "note": spec["note"],
                        "partial": unit["id"] in spec["partial"]})
    return out


def track_minutes(track: dict, units_by_deck: dict[str, list[dict]],
                  seconds: dict[str, float]) -> float:
    """Measured narration seconds for the slide-backed units a path includes."""
    total = 0.0
    for deck_id in list(track["core"]) + list(track.get("slice") or {}):
        for unit in units_by_deck.get(deck_id, []):
            total += seconds.get(f"{deck_id}:{unit['id']}", 0.0)
    return total


def unit_seconds(units_by_deck: dict[str, list[dict]], manifest: dict) -> dict[str, float]:
    """Measured narration seconds per unit, summed from the manifest's per-slide durations."""
    out: dict[str, float] = {}
    for deck_id, units in units_by_deck.items():
        entries = (manifest.get("decks", {}).get(deck_id, {}) or {}).get("slides", {})
        for unit in units:
            out[f"{deck_id}:{unit['id']}"] = sum(
                float((entries.get(f"slide-{i}") or {}).get("duration", 0) or 0)
                for i in range(unit["first"], unit["last"] + 1))
    return out


def fmt_minutes(seconds_value: float) -> str:
    minutes = seconds_value / 60.0
    if minutes < 1:
        return f"{seconds_value:.0f} sec"
    return f"{minutes:.1f} min".replace(".0 min", " min")


# ---------------------------------------------------------------- pages

def _crumbs(site_base: str, trail: list[tuple[str, str | None]]) -> str:
    parts = []
    for label, href in trail:
        parts.append(f'<a href="{href}">{html.escape(label)}</a>' if href
                     else f'<span aria-current="page">{html.escape(label)}</span>')
    return f'<nav class="crumbs" aria-label="Breadcrumb">{"<span>/</span>".join(parts)}</nav>'


def _at_a_glance(items: list[tuple[str, str]]) -> str:
    """Microsoft Learn's metadata block: every value is a filter in their catalogue, a fact here."""
    cells = "".join(
        f'<div class="aga-item"><dt>{html.escape(key)}</dt><dd>{html.escape(value)}</dd></div>'
        for key, value in items if value)
    return f'<dl class="at-a-glance">{cells}</dl>'


def _doc_page(title: str, description: str, body: str, site_base: str, body_class: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="preload" href="{site_base}/assets/fonts/source-sans-3.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{site_base}/assets/player.css">
</head>
<body class="index {body_class}">
{body}
</body>
</html>
"""


def paths_page(tracks: list[dict], units_by_deck: dict[str, list[dict]],
               seconds: dict[str, float], site_base: str, brand: str) -> str:
    cards = []
    for track in tracks:
        units = track_units(track, units_by_deck)
        minutes = track_minutes(track, units_by_deck, seconds)
        live = track["page"] and track["status"] == "built"
        status = ('<span class="voice-chip is-release">path page live</span>' if live
                  else '<span class="voice-chip is-text">first slice — page not built yet</span>')
        href = (f"{site_base}/{track['page']}" if live else f"{site_base}/index.html")
        target = "Open this path" if live else "Browse the modules"
        modules = len(track["core"]) + len(track.get("slice") or {})
        cards.append(f"""<article class="path-card">
  <a class="path-cover" href="{href}">
    <span class="path-kicker">{html.escape(track['kicker'])}</span>
    <h3>{html.escape(track['title'])}</h3>
    <span class="path-meta">{modules} modules · {len(units)} units · {fmt_minutes(minutes)} of narration</span>
  </a>
  <div class="path-body">
    <p class="path-promise">{html.escape(track['promise'])}</p>
    {_at_a_glance([("Level", track["level"]), ("Role", track["role"]), ("Price", track["price"])])}
    <p class="path-status">{status}</p>
    <a class="btn-primary" href="{href}">{target} →</a>
  </div>
</article>""")

    total_units = sum(len(u) for u in units_by_deck.values())
    body = f"""<header class="site-header">
  <div class="wrap">
    <a class="site-brand" href="{site_base}/index.html">{brand}AI Product Studio<span class="brand-destination">Course</span></a>
    {_crumbs(site_base, [("Course home", f"{site_base}/index.html"), ("Learning paths", None)])}
    <p class="eyebrow">Learning paths</p>
    <h1>Four ways into the same method.</h1>
    <p class="site-lede">Every path is a sequence of modules drawn from one course, in the order the
      work has to be done. The full studio course teaches all three archetypes; the three track paths
      each teach one, using the same lessons, labs and quizzes — nothing is rewritten or watered down,
      and each path says exactly what it leaves out.</p>
    <ul class="site-facts">
      <li>{len(tracks)} paths</li>
      <li>9 modules · {total_units} units</li>
      <li>Measured durations</li>
    </ul>
  </div>
</header>
<main class="site-main">
  <div class="section-heading">
    <h2>Choose a path</h2>
    <span class="section-note">A unit is one lesson segment, a lab, or a knowledge check — the level
      at which you actually sit down and learn something.</span>
  </div>
  <div class="path-grid">
{chr(10).join(cards)}
  </div>
  <section class="how-to">
    <h2>What a unit is</h2>
    <p>Every module in this course is built the same way, and the path pages show it:</p>
    <ol class="unit-grammar">
      <li><strong>Introduction</strong> — the cover and the module's objectives</li>
      <li><strong>Lesson</strong> — three teaching segments, 27 across the course</li>
      <li><strong>Exercise</strong> — one hands-on lab per module</li>
      <li><strong>Knowledge check</strong> — eight questions per module, 72 across the course</li>
      <li><strong>Summary</strong> — the recap and the discussion prompt</li>
    </ol>
    <p class="index-footnote">Every duration on these pages is measured from the recorded narration,
      not estimated. Lab times are quoted from each module's own source, because a lab is hours of
      hands-on work and its narration is a single slide.</p>
  </section>
</main>"""
    return _doc_page("Learning paths — AI Product Studio",
                     "Four learning paths through one AI product course: the full studio course and "
                     "three single-archetype tracks.", body, site_base, "paths")


def path_page(track: dict, decks_by_id: dict[str, dict], units_by_deck: dict[str, list[dict]],
              seconds: dict[str, float], site_base: str, brand: str,
              built_modules: set[str] | None = None) -> str:
    built_modules = built_modules or set()
    units = track_units(track, units_by_deck)
    minutes = track_minutes(track, units_by_deck, seconds)
    live = track["page"] and track["status"] == "built"
    cards = []
    for deck_id in track["core"]:
        deck = decks_by_id[deck_id]
        facts = cover_facts(deck)
        deck_units = units_by_deck[deck_id]
        deck_minutes = sum(seconds.get(f"{deck_id}:{u['id']}", 0) for u in deck_units)
        cards.append(_module_row(deck, deck_units, deck_minutes, site_base, built_modules, "full", ""))
    for deck_id in (track.get("slice") or {}):
        spec = slice_spec(track, deck_id)
        deck = decks_by_id[deck_id]
        deck_units = units_by_deck[deck_id]
        kept = [u for u in deck_units if u["id"] not in spec["exclude"]]
        deck_minutes = sum(seconds.get(f"{deck_id}:{u['id']}", 0) for u in kept)
        cards.append(_module_row(deck, deck_units, deck_minutes, site_base, built_modules,
                                 "slice", spec))

    measured = track.get("measured") or {}
    counts = ""
    if measured:
        rows = "".join(
            f"<tr><th scope=\"row\">{label}</th><td>{got} of {total}</td></tr>"
            for label, (got, total) in (
                ("Teaching segments", measured["segments"]),
                ("Full labs", measured["labs"]),
                ("Quizzes", measured["quizzes"]),
                ("Quiz questions", measured["questions"]),
            ))
        counts = f"""<section class="path-section">
    <h2>What this path includes</h2>
    <p class="section-note">Counted from the bundle map, not estimated.</p>
    <table class="counts-table">
      <caption>This path compared with the full studio course</caption>
      <thead><tr><th scope="col">Item</th><th scope="col">In this path</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </section>"""

    excluded = ""
    if track.get("excluded"):
        items = "".join(f"<li>{html.escape(label)}</li>" for label, _a, _b in track["excluded"])
        excluded = f"""<section class="path-section">
    <h2>Not in this path</h2>
    <p class="section-note">Stated plainly rather than discovered at checkout.</p>
    <ul class="excluded-list">{items}</ul>
  </section>"""

    body = f"""<header class="site-header">
  <div class="wrap">
    <a class="site-brand" href="{site_base}/index.html">{brand}AI Product Studio<span class="brand-destination">Course</span></a>
    {_crumbs(site_base, [("Course home", f"{site_base}/index.html"),
                         ("Learning paths", f"{site_base}/paths.html"),
                         (track["title"], None)])}
    <p class="eyebrow">Learning path · {len(track['core']) + len(track.get('slice') or {})} modules · {len(units)} units</p>
    <h1>{html.escape(track['title'])}</h1>
    <p class="site-lede">{html.escape(track['promise'])}</p>
    {_at_a_glance([("Level", track["level"]), ("Role", track["role"]),
                   ("Subject", track.get("subject", "AI product engineering")),
                   ("Duration", f"{fmt_minutes(minutes)} of narration + lab time"),
                   ("Price", track["price"])])}
  </div>
</header>
<main class="site-main">
  <section class="path-section">
    <h2>Prerequisites</h2>
    <p>{html.escape(track.get('prereq') or 'None. Module 0 assumes no prior setup beyond a machine that can run Python.')}</p>
  </section>
  <div class="section-heading">
    <h2>Modules in this path</h2>
    <span class="section-note">In order. A slice module contributes only the named segments — the rest
      belongs to another path.</span>
  </div>
  <div class="module-list">
{chr(10).join(cards)}
  </div>
{counts}
{excluded}
  <section class="path-section">
    <h2>The honest scope note</h2>
    <p>This path is not a separate course. It sequences and frames the parent course's modules for one
      archetype and reuses its lesson, lab and quiz artifacts — nothing is rewritten, reordered or
      watered down, and the slice of M7/M8 is scoped rather than summarised.</p>
    <p class="index-footnote">Durations are measured from the recorded narration. Lab times are quoted
      from each module's source. Nothing on this page is an estimate presented as a measurement.</p>
  </section>
</main>"""
    return _doc_page(f"{track['title']} — learning path — AI Product Studio",
                     track["promise"], body, site_base, "path-page")


def _module_row(deck: dict, units: list[dict], minutes: float, site_base: str,
                built_modules: set[str], inclusion: str, spec: dict | str) -> str:
    """One module row on a path page.

    A slice module lists *all* its units, including the ones this path leaves out, and marks them.
    Showing the exclusion is the point: "M8 — Launch" appearing in a path that does not teach the
    capstone would otherwise read as though it did.
    """
    spec = spec if isinstance(spec, dict) else {}
    exclude = set(spec.get("exclude") or ())
    partial = set(spec.get("partial") or ())
    facts = cover_facts(deck)
    short = re.sub(r"^M\d+\s*—\s*", "", deck["label"]).strip()
    number = int(NUM.match(deck["id"]).group(1))
    chip = ('<span class="inclusion-chip is-full">full module</span>' if inclusion == "full"
            else '<span class="inclusion-chip is-slice">slice</span>')

    rows = []
    for unit in units:
        label = f'<a href="{site_base}/{unit["href"]}">{html.escape(unit["title"])}</a>'
        kind = f'<span class="unit-kind">{html.escape(KIND_LABEL[unit["kind"]])}</span>'
        if unit["id"] in exclude:
            rows.append(f'<li class="is-excluded">{label}{kind}'
                        f'<span class="unit-mark">not in this path</span></li>')
        elif unit["id"] in partial:
            rows.append(f'<li>{label}{kind}'
                        f'<span class="unit-mark is-partial">part only</span></li>')
        else:
            rows.append(f'<li>{label}{kind}</li>')

    included = len(units) - len(exclude)
    count = (f"{included} of {len(units)} units" if exclude else f"{len(units)} units")
    note = f'<p class="slice-note">{html.escape(spec["note"])}</p>' if spec.get("note") else ""
    href = (f"{site_base}/module-{deck['id']}.html" if deck["id"] in built_modules
            else f"{site_base}/{deck['id']}.html")
    return f"""<article class="module-row">
  <div class="module-head">
    <p class="module-number">Module {number} {chip}</p>
    <h3><a href="{href}">{html.escape(short)}</a></h3>
    <p class="module-promise">{html.escape(facts['promise'])}</p>
    <p class="module-meta">{count} · {fmt_minutes(minutes)} of narration</p>
    {note}
  </div>
  <ol class="module-units">{"".join(rows)}</ol>
</article>"""


def module_page(deck: dict, units: list[dict], seconds: dict[str, float], site_base: str,
                brand: str, track: dict | None, text_only: bool) -> str:
    """Microsoft Learn's module page: objectives, prerequisites, then the ordered unit list."""
    number = int(NUM.match(deck["id"]).group(1))
    short = re.sub(r"^M\d+\s*—\s*", "", deck["label"]).strip()
    facts = cover_facts(deck)
    objectives_html = "".join(f"<li>{item}</li>" for item in objectives(deck))
    total = sum(seconds.get(f"{deck['id']}:{u['id']}", 0) for u in units)

    rows = []
    for index, unit in enumerate(units, 1):
        seconds_value = seconds.get(f"{deck['id']}:{unit['id']}", 0)
        if unit["kind"] == "lab":
            time_text = f'{fmt_minutes(seconds_value)} slide · {lab_time(deck["id"])} hands-on'
        else:
            time_text = fmt_minutes(seconds_value)
        rows.append(f"""<li class="unit" data-unit="{deck['id']}:{html.escape(unit['id'])}">
  <label class="unit-check">
    <input type="checkbox" data-progress="{deck['id']}:{html.escape(unit['id'])}">
    <span class="unit-kind">{html.escape(KIND_LABEL[unit['kind']])}</span>
    <span class="unit-index">{index}</span>
    <span class="unit-title">{html.escape(unit['title'])}</span>
    <span class="unit-time">{html.escape(time_text)}</span>
  </label>
  <a class="unit-open" href="{site_base}/{unit['href']}">Open →</a>
</li>""")

    path_link = (f'<a href="{site_base}/{track["page"]}">{html.escape(track["title"])}</a>'
                 if track and track.get("page") and track["status"] == "built"
                 else f'<a href="{site_base}/paths.html">Learning paths</a>')
    first = units[0]["href"] if units else f"{deck['id']}.html"

    body = f"""<header class="site-header">
  <div class="wrap">
    <a class="site-brand" href="{site_base}/index.html">{brand}AI Product Studio<span class="brand-destination">Course</span></a>
    {_crumbs(site_base, [("Course home", f"{site_base}/index.html"),
                         ("Learning paths", f"{site_base}/paths.html"), (short, None)])}
    <p class="eyebrow">Module · {len(units)} units · {fmt_minutes(total)} of narration</p>
    <h1>{html.escape(short)}</h1>
    <p class="site-lede">{html.escape(facts['promise'])}</p>
    {_at_a_glance([("Path", track["title"] if track else "Full studio course"),
                   ("Level", track["level"] if track else "Beginner to intermediate"),
                   ("Lesson", facts["lesson_length"]),
                   ("Lab", lab_time(deck["id"]))])}
  </div>
</header>
<main class="site-main">
  <section class="path-section">
    <h2>Learning objectives</h2>
    <ul class="objectives">{objectives_html}</ul>
  </section>
  <section class="path-section">
    <h2>Prerequisites</h2>
    <p>{html.escape(lab_prereq(deck['id']))}</p>
  </section>
  <div class="section-heading">
    <h2>Units in this module</h2>
    <span class="section-note">Work them in order. Each unit opens the deck at its first slide.</span>
  </div>
  <div class="progress-wrap">
    <p class="progress-line"><strong id="progress-count">0 of {len(units)}</strong> complete
      <span class="progress-bar" role="progressbar" aria-labelledby="progress-count"
            aria-valuemin="0" aria-valuemax="{len(units)}" aria-valuenow="0"><span id="progress-fill"></span></span></p>
    <p class="progress-note">Progress is stored in this browser only — there are no accounts on this
      site, so nothing is uploaded and nothing follows you to another device.</p>
  </div>
  <ol class="unit-list">
{chr(10).join(rows)}
  </ol>
  <section class="path-section">
    <a class="btn-primary" href="{site_base}/{first}">Start this module →</a>
    <a class="btn-quiet" href="{site_base}/transcript-{deck['id']}.html">Read the transcript</a>
    <p class="index-footnote">Part of {path_link}. {'This is the text-first copy: narration and captions are not published here, so units are read and presented rather than played.' if text_only else 'Units carry narration, captions and a transcript.'}</p>
  </section>
</main>
<script>
(function () {{
  var KEY = 'aps.progress.v1';
  var boxes = Array.prototype.slice.call(document.querySelectorAll('[data-progress]'));
  var done = {{}};
  try {{ done = JSON.parse(localStorage.getItem(KEY) || '{{}}') || {{}}; }} catch (e) {{ done = {{}}; }}
  function save() {{ try {{ localStorage.setItem(KEY, JSON.stringify(done)); }} catch (e) {{}} }}
  function render() {{
    var n = 0;
    boxes.forEach(function (b) {{
      var on = !!done[b.getAttribute('data-progress')];
      b.checked = on;
      b.closest('.unit').classList.toggle('is-done', on);
      if (on) n++;
    }});
    var count = document.getElementById('progress-count');
    var bar = document.querySelector('.progress-bar');
    var fill = document.getElementById('progress-fill');
    if (count) count.textContent = n + ' of ' + boxes.length;
    if (bar) bar.setAttribute('aria-valuenow', String(n));
    if (fill) fill.style.width = (boxes.length ? (n / boxes.length * 100) : 0) + '%';
  }}
  boxes.forEach(function (b) {{
    b.addEventListener('change', function () {{
      var k = b.getAttribute('data-progress');
      if (b.checked) {{ done[k] = 1; }} else {{ delete done[k]; }}
      save(); render();
    }});
  }});
  render();
}})();
</script>"""
    return _doc_page(f"{short} — module — AI Product Studio", facts["promise"],
                     body, site_base, "module-page")
