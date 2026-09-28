#!/usr/bin/env python3
"""Verify the expanded course package against course/01-design/content-standards.md.

Checks
  1. every module (M0-M8) has all 8 artifacts
  2. every artifact is inside its length band
  3. every repo file pointer in the package resolves on disk, and every `:N` / `:N-M`
     line range lies inside the file it points at
  4. rubric weights sum to 100 in each lab-rubrics.md
  5. bundles each ship their 5 files
  6. no deck is missing Marp front matter or speaker notes (delegates detail to deck_lint.py)
  7. narration: every deck has approved words, and every recording matches them word for word
  8. the learner site, when built, has one page per deck with the right slide count
  9. every slide exhibit is a copy of a file the slide cites, or declares what else it is
 10. figures: each parses, says what it shows, cites what resolves, builds in on a sentence the
     narration speaks, uses files that exist; screenshot copies match their origin; covered
     modules open with a hero and head every segment with a figure

Usage:
  python3 verify.py                # full report, exit 1 on any failure
  python3 verify.py --pointers     # pointer audit only: paths + line ranges, e.g.
                                   #   "pointers checked: N (M line ranges verified)"
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # course/
REPO = ROOT.parent                                  # workspace (holds the cloned repos)
CONTENT = ROOT / "03-content"
TRACKS = ROOT / "05-tracks"

MODULES = [
    "m00-orientation", "m01-operating-system", "m02-ondevice-app", "m03-privacy-ship",
    "m04-spec-driven-saas", "m05-security-tests", "m06-expertise-product",
    "m07-monetize", "m08-launch-capstone", "m09-github-pages",
]
ARTIFACTS = {
    "slides.md": None,          # slide-count checked by deck_lint.py
    "solutions.md": (800, 1600),
    "video-scripts.md": (1200, 2100),
    "handout.md": (400, 650),
    "facilitation.md": (800, 1250),
    "glossary.md": (500, 900),
    "lab-rubrics.md": (600, 1100),
    "accessibility.md": (400, 900),
}
# Standalone playbooks (#66): each folder is a sellable unit extracted from a module.
PLAYBOOKS = ROOT / "07-playbooks"
PLAYBOOK_BAND = (1500, 3000)
SALES_BAND = (400, 750)
PLAYBOOK_SECTIONS = ["## The method", "## Template", "## Checklist", "## Worked example",
                     "## Self-check", "## Limits", "## Sources"]
BUNDLES = ["on-device-app", "spec-driven-saas", "expertise-product"]
BUNDLE_FILES = ["README.md", "syllabus.md", "sales-page.md", "pricing.md", "bundle-map.md"]

CASE_REPOS = ("ListenToMe", "SignUpFlow", "ai_qe")
# A pointer is `<repo>/<path>` optionally followed by `:<lines>`, where <lines> is one or more
# comma-separated `N` or `N-M` ranges (`:15-24`, `:57,61`, `:99-103, 151-157`). The optional
# trailing group lets a space-separated second range stay inside one pointer.
POINTER_RE = re.compile(
    r"`((?:ListenToMe|SignUpFlow|ai_qe)/[^`\s]+(?:,\s*\d+(?:[-\u2013]\d+)?)*)`"
)
LINE_RANGE_RE = re.compile(r"^(\d+)(?:[-\u2013](\d+))?$")
# Two more forms name case-repo lines without the repo prefix, and the gate used to see neither:
# a bare pointer (`ModelRanking.swift:13-18`, `App/MeetingView.swift:845`) and prose
# (`MeetingSession.swift`, lines 54–87). Each is checked when its path resolves to exactly one
# tracked file in the three clones; an ambiguous name (`README.md`) or a course file is left alone.
_LINES = r"\d+(?:\s*[-\u2013]\s*\d+)?(?:(?:,\s*|\s+and\s+)\d+(?:\s*[-\u2013]\s*\d+)?)*"
BARE_POINTER_RE = re.compile(
    r"`((?!(?:ListenToMe|SignUpFlow|ai_qe)/)[A-Za-z0-9_][A-Za-z0-9_./-]*\.[A-Za-z]{1,6}):(" + _LINES + r")`")
PROSE_POINTER_RE = re.compile(
    r"`((?:(?:ListenToMe|SignUpFlow|ai_qe)/)?[A-Za-z0-9_][A-Za-z0-9_./-]*\.[A-Za-z]{1,6})`,?\s*lines?\s+(" + _LINES + r")")
# A range can stay in bounds and still point at the wrong code after the source moves (#68). An
# anchor names what the range must contain: {"<pointer as written>": "symbol" or ["a", "b"]}.
ANCHORS = ROOT / "06-production" / "pointer-anchors.json"
_CASE_INDEX: dict[str, list[str]] | None = None


def _case_index() -> dict[str, list[str]]:
    """basename -> tracked repo-relative paths ("ListenToMe/App/MeetingView.swift") in the clones."""
    global _CASE_INDEX
    if _CASE_INDEX is None:
        _CASE_INDEX = {}
        for repo in CASE_REPOS:
            if not (REPO / repo / ".git").exists():
                continue
            out = subprocess.run(["git", "-C", str(REPO / repo), "ls-files"],
                                 capture_output=True, text=True).stdout
            for rel in out.split():
                _CASE_INDEX.setdefault(Path(rel).name, []).append(f"{repo}/{rel}")
    return _CASE_INDEX


_COURSE_INDEX: dict[str, list[str]] | None = None


def _course_index() -> dict[str, list[str]]:
    """basename -> tracked course/ paths, for course-internal pointers (`08-domain-currency-2026.md:74`)."""
    global _COURSE_INDEX
    if _COURSE_INDEX is None:
        _COURSE_INDEX = {}
        out = subprocess.run(["git", "-C", str(REPO), "ls-files", "course"], capture_output=True, text=True).stdout
        for rel in out.split():
            _COURSE_INDEX.setdefault(Path(rel).name, []).append(rel)
    return _COURSE_INDEX


def resolve_case_path(path: str) -> Path | None:
    """A prefixed path as-is (a case repo or course/); a bare one when exactly one tracked file,
    first in the clones and then in course/, ends with it. A line range into the course's own
    research moves when that file is edited, which is how M6's citations of the currency review
    drifted by seven lines unseen; these are now range-checked and can be anchored too."""
    if path.split("/")[0] in CASE_REPOS or path.startswith("course/"):
        return REPO / path
    # One match across the clones and course/ together, or nothing: `tests/conftest.py` exists in
    # SignUpFlow and in two course starters, and range-checking whichever came first checks the
    # wrong file.
    hits = [c for index in (_case_index(), _course_index())
            for c in index.get(Path(path).name, []) if c == path or c.endswith("/" + path)]
    return REPO / hits[0] if len(hits) == 1 else None


def _prose_ranges(spec: str) -> list[tuple[int, int]]:
    return parse_line_ranges(re.sub(r"\s+and\s+", ",", spec).replace(" ", "")) or []
WEIGHT_RE = re.compile(r"\b(\d{1,3})\s*%")
# A table row that looks like a rubric weight row: contains a % and a criterion-ish phrase
RUBRIC_ROW_RE = re.compile(r"^\|.+\|\s*(?:\*\*)?(\d{1,3})\s*%\s*(?:\*\*)?\s*\|")


def word_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").split())


def check_artifacts() -> list[str]:
    problems = []
    for mod in MODULES:
        folder = CONTENT / mod
        if not folder.is_dir():
            problems.append(f"{mod}: folder missing")
            continue
        for name, band in ARTIFACTS.items():
            f = folder / name
            if not f.exists():
                problems.append(f"{mod}/{name}: MISSING")
                continue
            if band is None:
                continue
            n = word_count(f)
            lo, hi = band
            if not (lo <= n <= hi):
                problems.append(f"{mod}/{name}: {n} words, band {lo}-{hi}")
    problems += check_playbooks()
    return problems


def check_playbooks() -> list[str]:
    """Each playbook stands alone: the sections in order, inside its band, with no pointer back into
    the course's modules or labs (a buyer never saw them), and a sales page that proposes a price."""
    problems: list[str] = []
    if not PLAYBOOKS.is_dir():
        return problems
    for folder in sorted(p for p in PLAYBOOKS.iterdir() if p.is_dir()):
        book, sales = folder / "playbook.md", folder / "sales.md"
        for f, band in ((book, PLAYBOOK_BAND), (sales, SALES_BAND)):
            if not f.exists():
                problems.append(f"07-playbooks/{folder.name}/{f.name}: MISSING")
                continue
            n = word_count(f)
            if not (band[0] <= n <= band[1]):
                problems.append(f"07-playbooks/{folder.name}/{f.name}: {n} words, band {band[0]}-{band[1]}")
        if book.exists():
            # Templates carry their own headings inside code fences; only the playbook's count.
            text = re.sub(r"```.*?```", "", book.read_text(encoding="utf-8"), flags=re.S)
            at = [text.find("\n" + h) for h in PLAYBOOK_SECTIONS]
            if -1 in at or at != sorted(at):
                problems.append(f"07-playbooks/{folder.name}/playbook.md: sections missing or out of order "
                                f"(need {', '.join(h[3:] for h in PLAYBOOK_SECTIONS)})")
            body = text.rsplit("\n## Sources", 1)[0]
            leak = re.search(r"\b(?:Lab M\d|M\d\.\d|in this module|as we saw)\b", body)
            if leak:
                problems.append(f"07-playbooks/{folder.name}/playbook.md: not standalone ({leak.group(0)!r})")
        if sales.exists() and "the owner sets the final price" not in sales.read_text(encoding="utf-8"):
            problems.append(f"07-playbooks/{folder.name}/sales.md: price not labelled as a proposal")
    return problems


def parse_line_ranges(suffix: str) -> list[tuple[int, int]] | None:
    """`15-24` -> [(15, 24)]; `57,61` -> [(57, 57), (61, 61)]. None when the suffix is not a
    line spec at all (an anchor or a symbol name), so the caller checks the path only."""
    suffix = suffix.split("#")[0].strip().rstrip(",.;")
    if not suffix:
        return None
    ranges: list[tuple[int, int]] = []
    for part in suffix.split(","):
        m = LINE_RANGE_RE.match(part.strip())
        if not m:
            return None
        lo = int(m.group(1))
        hi = int(m.group(2)) if m.group(2) else lo
        ranges.append((lo, hi))
    return ranges


def _label(f: Path) -> str:
    """Report paths relative to course/ when they are inside it, verbatim otherwise."""
    try:
        return str(f.relative_to(ROOT))
    except ValueError:
        return str(f)


def check_pointers(files: list[Path] | None = None) -> tuple[int, int, list[str]]:
    """Every pointer's path must exist; every `:N` / `:N-M` must lie inside the file.

    Returns (pointers checked, line ranges checked, problems). A range is in bounds when
    1 <= N <= M <= line count of the file — a pointer into a directory, or past the end of the
    file, is reported. Line counts are cached per file.
    """
    problems: list[str] = []
    checked = 0
    ranges_checked = 0
    line_counts: dict[Path, int] = {}
    if files is None:
        files = sorted(
            p for p in ROOT.rglob("*.md")
            if "tinycopilot" not in p.parts and "slides/out" not in str(p)
        )
    for f in files:
        text = f.read_text(encoding="utf-8")
        for m in POINTER_RE.finditer(text):
            raw = m.group(1)
            path, _, suffix = raw.partition(":")
            path = path.split("#")[0]
            checked += 1
            target = REPO / path
            if not target.exists():
                problems.append(f"{_label(f)}: MISSING POINTER {raw}")
                continue
            ranges = parse_line_ranges(suffix)
            if not ranges:
                continue
            if target.is_dir():
                problems.append(f"{_label(f)}: LINE RANGE ON A DIRECTORY {raw}")
                continue
            if target not in line_counts:
                line_counts[target] = len(
                    target.read_text(encoding="utf-8", errors="replace").splitlines()
                )
            n = line_counts[target]
            for lo, hi in ranges:
                ranges_checked += 1
                if not (1 <= lo <= hi <= n):
                    problems.append(
                        f"{_label(f)}: OUT OF RANGE {raw} "
                        f"(lines {lo}-{hi}; file has {n} lines)"
                    )
        for m in list(BARE_POINTER_RE.finditer(text)) + list(PROSE_POINTER_RE.finditer(text)):
            path, spec = m.group(1), m.group(2)
            target = resolve_case_path(path)
            if target is None or not target.is_file():
                continue
            rngs = _prose_ranges(spec) if m.re is PROSE_POINTER_RE else (parse_line_ranges(spec) or [])
            if not rngs:
                continue
            checked += 1
            if target not in line_counts:
                line_counts[target] = len(target.read_text(encoding="utf-8", errors="replace").splitlines())
            n = line_counts[target]
            for lo, hi in rngs:
                ranges_checked += 1
                if not (1 <= lo <= hi <= n):
                    problems.append(f"{_label(f)}: OUT OF RANGE {path} lines {spec} "
                                    f"(resolved to {target.relative_to(REPO)}; file has {n} lines)")
    return checked, ranges_checked, problems


WEIGHT_HEADERS = {
    "wt", "w", "weight", "weights", "weightpts", "wtpts",
    "points", "point", "pts", "pt", "weightpoints",
}


def _weight_column(lines: list[str]) -> int | None:
    """Find the table column index whose header names the weight/points column.

    Header wording varies across the nine rubric files (Wt, W, Weight, Points), so match
    on a normalized exact token rather than a substring — 'Evidence required' must not
    be mistaken for a weight column.
    """
    for line in lines:
        if not line.strip().startswith("|"):
            continue
        cells = line.strip().strip("|").split("|")
        for i, c in enumerate(cells):
            norm = re.sub(r"[^a-z]", "", c.lower())
            if norm in WEIGHT_HEADERS:
                return i
    return None


def check_rubrics() -> list[str]:
    problems = []
    for mod in MODULES:
        f = CONTENT / mod / "lab-rubrics.md"
        if not f.exists():
            continue
        lines = f.read_text(encoding="utf-8").splitlines()
        text = "\n".join(lines)
        if "auto-fail" not in text.lower():
            problems.append(f"{mod}/lab-rubrics.md: no auto-fail list")

        col = _weight_column(lines)
        total = 0
        rows = 0
        if col is not None:
            for line in lines:
                if not line.strip().startswith("|"):
                    continue
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if col >= len(cells):
                    continue
                cell = cells[col].replace("*", "")
                m = re.search(r"\d{1,3}", cell)
                if m and not set(cell) <= set("-: "):
                    total += int(m.group(0))
                    rows += 1
        if col is None or rows == 0:
            # No machine-readable weight column: require a stated total instead.
            if not re.search(r"100\s*(points|%|pts)", text, re.IGNORECASE):
                problems.append(
                    f"{mod}/lab-rubrics.md: no weight column and no stated 100-point total"
                )
        elif total % 100 != 0:
            problems.append(
                f"{mod}/lab-rubrics.md: weight column totals {total} over {rows} rows "
                f"(expected a multiple of 100)"
            )
    return problems


def check_bundles() -> list[str]:
    problems = []
    for b in BUNDLES:
        folder = TRACKS / b
        if not folder.is_dir():
            problems.append(f"tracks/{b}: folder missing")
            continue
        for name in BUNDLE_FILES:
            if not (folder / name).exists():
                problems.append(f"tracks/{b}/{name}: MISSING")
    return problems


def check_decks() -> list[str]:
    decks = sorted(CONTENT.glob("*/slides.md"))
    if not decks:
        return ["no decks found"]
    proc = subprocess.run(
        [sys.executable, str(ROOT / "06-production/slides/deck_lint.py"), *map(str, decks)],
        capture_output=True, text=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode == 0:
        return []
    return [f"deck_lint: {line.strip()}" for line in out.splitlines() if line.strip().startswith(("✗", "slide", "course"))][:40]


# A slide exhibit is either a copy of a file the slide cites, or it says what else it is. The
# info string carries the declaration (the site and Marp read only its first word): ```bash
# commands, ```text output, ```markdown template, ```text illustrative. A copy may rewrap lines
# and elide with "…", but every line must occur in a cited file, inside the cited range when the
# file is cited only with ranges. Refitting slides to the frame (#70) trims exhibits, and nothing
# else would notice a trimmed exhibit that no longer matches its source.
EXHIBIT_FENCE_RE = re.compile(r"^```([^\n]*)\n(.*?)^```", re.S | re.M)
EXHIBIT_KINDS = {"commands", "output", "template", "illustrative"}
EXHIBIT_REF_RE = re.compile(r"`((?:ListenToMe|SignUpFlow|ai_qe|course)/[A-Za-z0-9_./-]+"   # `ai_qe/Makefile`
                            r"|[A-Za-z0-9_][A-Za-z0-9_./-]*\.[A-Za-z]{1,6})(?::([0-9 ,\u2013-]+))?`")
EXHIBIT_LABEL_RE = re.compile(r"^\s*<!--\s*(\S+?)\s*-->\s*$")
EXHIBIT_ELIDE_RE = re.compile(r"…|\.\.\.")


def _exhibit_norm(s: str) -> str:
    """Compare text, not typography: blockquote markers, emphasis and wrapping do not count."""
    s = re.sub(r"(?m)^\s*>\s?", "", s)
    return " ".join(re.sub(r"[*`]", "", s).split())


def check_exhibits() -> list[str]:
    problems: list[str] = []
    texts: dict[Path, list[str]] = {}
    for deck in sorted(CONTENT.glob("*/slides.md")):
        slides = re.split(r"\n---\n", deck.read_text(encoding="utf-8"))
        for n, slide in enumerate(slides[1:], start=1):
            shown = re.sub(r"<!-- NOTES:.*?-->", "", slide, flags=re.S)
            refs = [(m.group(1), m.group(2)) for m in EXHIBIT_REF_RE.finditer(slide)]
            refs += [(lab.partition(":")[0], lab.partition(":")[2] or None)
                     for line in shown.splitlines()
                     if (lab := (EXHIBIT_LABEL_RE.match(line) or [None, ""])[1])]
            whole: list[str] = []
            cited: list[str] = []
            for path, spec in refs:
                target = resolve_case_path(path)
                if target is None or not target.is_file():
                    continue
                if target not in texts:
                    texts[target] = target.read_text(encoding="utf-8", errors="replace").splitlines()
                lines = texts[target]
                whole.append(_exhibit_norm("\n".join(lines)))
                rngs = parse_line_ranges(spec) if spec else None
                cited.append(_exhibit_norm("\n".join(l for lo, hi in rngs for l in lines[lo - 1:hi]))
                             if rngs else whole[-1])
            where = f"{deck.parent.name}/slides.md slide {n}"
            for info, body in EXHIBIT_FENCE_RE.findall(shown):
                if EXHIBIT_KINDS & set(info.split()[1:]) or info.split()[:1] == ["figure"]:
                    continue    # a declared kind, or a figure (checked by check_figures)
                if not whole:
                    problems.append(f"{where}: an exhibit cites no file it copies; cite the source "
                                    f"or declare it ({', '.join(sorted(EXHIBIT_KINDS))})")
                    continue
                for line in body.splitlines():
                    if EXHIBIT_LABEL_RE.match(line):
                        continue
                    for piece in EXHIBIT_ELIDE_RE.split(line):
                        piece = _exhibit_norm(piece)
                        if len(piece) <= 3:
                            continue
                        if not any(piece in s for s in whole):
                            problems.append(f"{where}: exhibit line not in the cited file(s): {piece[:90]!r}")
                        elif not any(piece in s for s in cited):
                            problems.append(f"{where}: exhibit line is outside the cited range: {piece[:90]!r}")
    return problems


# Figures (#99). A module listed here is held to the standard's coverage rule: its cover slide
# carries the hero figure and every segment's first slide carries a figure. A module joins the list
# in the change that draws its figures (the course-content skill's "A new module" step).
FIGURE_MODULES: list[str] = ["m00", "m01", "m02", "m03", "m04", "m05", "m06", "m07", "m08", "m09"]
FIGURES = ROOT / "figures"
FIGURE_FENCE_RE = re.compile(r"^```figure[^\n]*\n(.*?)^```", re.S | re.M)


def _figure_sources(value: str) -> list[str]:
    return [v.strip() for v in re.split(r"\s+·\s+|;\s*", value) if v.strip()]


def check_figure_manifest() -> tuple[int, list[str]]:
    """Every screenshot copy is byte-identical to the file at the commit it was copied from."""
    import hashlib                                                             # noqa: PLC0415
    import json                                                                # noqa: PLC0415
    manifest = FIGURES / "manifest.json"
    if not manifest.exists():
        return 0, []
    problems = []
    entries = json.loads(manifest.read_text(encoding="utf-8")).get("shots", [])
    for e in entries:
        copy = FIGURES / "shots" / e["name"]
        if not copy.is_file():
            problems.append(f"figures/shots/{e['name']}: in the manifest but missing")
            continue
        got = hashlib.sha256(copy.read_bytes()).hexdigest()
        if got != e["sha256"]:
            problems.append(f"figures/shots/{e['name']}: differs from the manifest (edited after copying?)")
        origin = subprocess.run(["git", "-C", str(REPO / e["repo"]), "show", f"{e['commit']}:{e['path']}"],
                                capture_output=True)
        if origin.returncode != 0:
            problems.append(f"figures/shots/{e['name']}: {e['repo']}/{e['path']} not found at {e['commit'][:12]}")
        elif hashlib.sha256(origin.stdout).hexdigest() != e["sha256"]:
            problems.append(f"figures/shots/{e['name']}: not the file at {e['repo']}@{e['commit'][:12]}")
    listed = {e["name"] for e in entries}
    for extra in sorted((FIGURES / "shots").glob("*")) if (FIGURES / "shots").is_dir() else []:
        if extra.name not in listed:
            problems.append(f"figures/shots/{extra.name}: not in manifest.json — copy it with figures_shots.py")
    return len(entries), problems


def check_figures() -> list[str]:
    """The figures standard (content-standards.md, Figures), in the Markdown and in the built slides."""
    site = ROOT / "learner-site"
    for extra in (site, ROOT / "06-production" / "narration", ROOT / "06-production" / "slides"):
        if str(extra) not in sys.path:
            sys.path.insert(0, str(extra))
    import figures as F                                                        # noqa: PLC0415
    import build_site as B                                                     # noqa: PLC0415
    import site_paths as SP                                                    # noqa: PLC0415
    from narration_data import load_scripts                                    # noqa: PLC0415
    from deck_lint import split_slides                                         # noqa: PLC0415
    scripts = load_scripts()["decks"]
    problems: list[str] = []
    count = stepped = 0
    systems: dict[str, int] = {}

    def one(where: str, body: str, said: list[str] | None) -> None:
        nonlocal count, stepped
        count += 1
        try:
            fig = F.parse(body)
        except F.FigureError as exc:
            problems.append(f"{where}: {exc}")
            return
        if fig["kind"] == "system":
            mod = where.split("-")[0]
            systems[mod] = systems.get(mod, 0) + 1
        if len(fig["alt"]) < 12:
            problems.append(f"{where}: alt is too short to say what the figure shows")
        for src in _figure_sources(fig["source"]):
            path, _, spec = src.partition(":")
            target = resolve_case_path(path)
            if target is None or not target.is_file():
                problems.append(f"{where}: source {src!r} does not resolve")
                continue
            ranges = parse_line_ranges(spec) if spec else None
            if ranges:
                n = len(target.read_text(encoding="utf-8", errors="replace").splitlines())
                if any(hi > n or lo < 1 or lo > hi for lo, hi in ranges):
                    problems.append(f"{where}: source {src!r} is outside the file ({n} lines)")
        if fig["kind"] == "screenshot" and not (FIGURES / "shots" / fig["image"]).is_file():
            problems.append(f"{where}: image {fig['image']} is not in course/figures/shots/")
        if fig["kind"] == "scene" and not (FIGURES / "scenes" / fig["scene"]).is_file():
            problems.append(f"{where}: scene {fig['scene']} is not in course/figures/scenes/")
        parts = [p for item in fig["items"] for p in (item, *item["children"])] + fig.get("edges", [])
        ats = [p for p in parts if p["at"]]
        if ats:
            stepped += 1
        for p in ats:
            if said is None:
                problems.append(f"{where}: `@ {p['at']}` — only a slide's figure builds on narration")
            elif F.step_index(p["at"], said) is None:
                problems.append(f"{where}: `@ {p['at']}` opens no sentence of this slide's narration")

    for deck_path in sorted(CONTENT.glob("*/slides.md")):
        deck_id = deck_path.parent.name.split("-")[0]
        slides = split_slides(deck_path.read_text(encoding="utf-8"))[1]
        for n, raw in enumerate(slides, 1):
            text = scripts.get(deck_id, {}).get("slides", {}).get(f"slide-{n}", {}).get("text", "")
            for body in FIGURE_FENCE_RE.findall(raw):
                one(f"{deck_path.parent.name}/slides.md slide {n}", body, B.sentences(text))
    for lesson in sorted(CONTENT.glob("*/lesson.md")):
        for body in FIGURE_FENCE_RE.findall(lesson.read_text(encoding="utf-8")):
            one(f"{lesson.parent.name}/lesson.md", body, None)

    for deck_id in FIGURE_MODULES:
        # Every module draws at least one real system — components and the arrows between them (#115).
        if not systems.get(deck_id):
            problems.append(f"{deck_id}: no system diagram (kind: system) in its slides or lesson")
        deck = B.parse_deck(deck_id, scripts)
        units = SP.module_units(deck)
        figs = F.deck_figures(deck, units)
        if not figs["hero"]:
            problems.append(f"{deck_id}: the cover slide has no hero figure")
        for unit in units:
            if unit["kind"] == "segment" and unit["id"] not in figs["segments"]:
                problems.append(f"{deck_id}: segment {unit['id']} opens (slide {unit['first']}) with no figure")

    shots, manifest_problems = check_figure_manifest()
    problems += manifest_problems
    check_figures.summary = (f"{count} figures, {stepped} stepped, {sum(systems.values())} systems, {shots} screenshots, "
                             f"{len(FIGURE_MODULES)} modules covered")
    return problems


def check_sales_claims() -> list[str]:
    """The sales docs state measured word counts. Counts drift the moment a file is edited,
    so verify the claim against the file instead of trusting the note."""
    problems = []
    f = ROOT / "04-sales" / "landing-page.md"
    if not f.exists():
        return [f"{f.name}: missing"]
    text = f.read_text(encoding="utf-8")
    measured = len(text.split())
    m = re.search(r"([\d,]{3,})\s+words total", text)
    if not m:
        problems.append("landing-page.md: no measured 'N words total' claim found")
    else:
        claimed = int(m.group(1).replace(",", ""))
        drift = abs(claimed - measured) / measured
        if drift > 0.10:
            problems.append(
                f"landing-page.md: claims {claimed:,} words total but the file measures "
                f"{measured:,} ({drift:.0%} drift) — re-measure and update the note"
            )
    return problems


def check_narration() -> list[str]:
    """Run the narration contract without re-hashing media; `make check` runs the full version.

    Word equality between captions, transcript and the approved script is the invariant that makes
    a narrated deck trustworthy, so it belongs in the main gate rather than an optional extra.
    """
    validator = ROOT / "06-production" / "narration" / "validate_narration.py"
    if not validator.exists():
        return [f"{validator.name}: missing"]
    proc = subprocess.run([sys.executable, str(validator), "--no-media"],
                          capture_output=True, text=True)
    if proc.returncode == 0:
        return []
    return [f"narration: {line.strip()}" for line in
            ((proc.stdout or "") + (proc.stderr or "")).splitlines()
            if line.strip().startswith("✗")][:40] or ["narration: validation failed"]


def check_learner_site() -> list[str]:
    """Only meaningful once the site is built; an unbuilt site is a note, not a failure."""
    site = ROOT / "learner-site"
    # Deck pages only: `m00.html`..`m08.html`. A bare `m*.html` also matches the learning-path
    # module pages (`module-m02.html`), which are not decks and have no narration script.
    pages = sorted(site.glob("m[0-9][0-9].html"))
    if not pages:
        return []
    problems = []
    if not (site / "narration.json").exists():
        problems.append("learner-site/narration.json missing — rebuild with `make site`")
    sys.path.insert(0, str(site))
    sys.path.insert(0, str(ROOT / "06-production" / "narration"))
    sys.path.insert(0, str(ROOT / "06-production" / "slides"))   # deck_lint lives here
    try:
        from narration_data import load_scripts                       # noqa: PLC0415
        from deck_lint import split_slides                            # noqa: PLC0415
        scripts = load_scripts()["decks"]
        for page in pages:
            deck_id = page.stem
            script = scripts.get(deck_id)
            if not script:
                problems.append(f"{page.name}: no narration script for this deck")
                continue
            slides = split_slides(sorted(CONTENT.glob(f"{deck_id}-*/slides.md"))[0]
                                  .read_text(encoding="utf-8"))[1] if list(
                CONTENT.glob(f"{deck_id}-*/slides.md")) else []
            html = page.read_text(encoding="utf-8")
            rendered = html.count('class="learn-section')
            if slides and rendered != len(slides):
                problems.append(f"{page.name}: renders {rendered} parts, the module has {len(slides)}")
            if len(script["slides"]) != len(slides) and slides:
                problems.append(f"{page.name}: script covers {len(script['slides'])} of {len(slides)} slides")
            for asset in ("assets/learn.js", "assets/narration-media.js", "assets/player.css"):
                if f'"{asset}"' not in html and f'/{asset}"' not in html:
                    problems.append(f"{page.name}: does not load {asset}")
    finally:
        pass
    return problems


def check_terms_zh() -> list[str]:
    """EN / 中文 (#116): every glossary term has a Chinese name and a one-line Chinese definition in
    terms-zh.json, and the file names no term a glossary does not define (a renamed term leaves its
    old entry behind otherwise). A name must be Chinese and must not simply repeat the English."""
    import json                                                        # noqa: PLC0415
    sys.path.insert(0, str(ROOT / "learner-site"))
    import site_content as SC                                           # noqa: PLC0415
    import site_locale as SL                                            # noqa: PLC0415
    terms = SL.load()
    defined = {}
    for module in MODULES:
        for t in SC.parse_glossary((CONTENT / module / "glossary.md").read_text(encoding="utf-8")):
            defined.setdefault(t["term"], module)
    problems = []
    cjk = re.compile(r"[\u4e00-\u9fff]")
    for term, module in sorted(defined.items()):
        entry = terms.get(term)
        if not entry:
            problems.append(f"{module}/glossary.md: \"{term}\" has no entry in terms-zh.json")
            continue
        for key in ("zh", "def"):
            if not cjk.search(entry.get(key, "")):
                problems.append(f"terms-zh.json: \"{term}\" {key} is not Chinese")
        if SL.stem(term).lower() in entry.get("zh", "").lower():
            problems.append(f"terms-zh.json: \"{term}\" zh repeats the English; give only the Chinese")
        if entry.get("scope") not in (None, "module"):
            problems.append(f"terms-zh.json: \"{term}\" scope must be \"module\" or absent")
    for term in sorted(set(terms) - set(defined)):
        problems.append(f"terms-zh.json: \"{term}\" is in no glossary — remove it or restore the term")
    check_terms_zh.summary = f"{len(defined)} terms, {sum(1 for t in defined if terms.get(t, {}).get('inline', True))} named inline"
    return problems


def check_anchors() -> tuple[int, list[str]]:
    """Every anchored pointer is still cited somewhere, and its range still contains its symbol."""
    import json                                                              # noqa: PLC0415
    if not ANCHORS.exists():
        return 0, []
    anchors = json.loads(ANCHORS.read_text(encoding="utf-8"))
    corpus = "\n".join(p.read_text(encoding="utf-8") for p in ROOT.rglob("*.md")
                       if "tinycopilot" not in p.parts and "slides/out" not in str(p))
    problems: list[str] = []
    held = 0
    for pointer, want in anchors.items():
        if pointer.startswith("_"):
            continue
        tokens = [want] if isinstance(want, str) else list(want)
        if f"`{pointer}`" not in corpus:
            problems.append(f"anchor for `{pointer}`: no longer cited anywhere; update or remove the entry")
            continue
        path, _, spec = pointer.partition(":")
        target = resolve_case_path(path)
        rngs = parse_line_ranges(spec) if spec else None
        if target is None or not target.is_file() or not rngs:
            problems.append(f"anchor for `{pointer}`: path does not resolve to one case-repo file")
            continue
        lines = target.read_text(encoding="utf-8", errors="replace").splitlines()
        # Whitespace-insensitive, so a phrase the source wraps across two lines still matches.
        body = " ".join(w for lo, hi in rngs for w in " ".join(lines[lo - 1:hi]).split())
        missing = [t for t in tokens if " ".join(t.split()) not in body]
        if missing:
            where = {t: [i + 1 for i, l in enumerate(lines) if t in l][:3] for t in missing}
            problems.append(f"ANCHOR MISSED `{pointer}`: {missing} not in those lines (found at {where})")
        else:
            held += 1
    return held, problems


def main(argv: list[str]) -> int:
    if "--pointers" in argv:
        checked, ranges, problems = check_pointers()
        print(f"pointers checked: {checked} ({ranges} line ranges verified)")
        for p in problems:
            print("  " + p)
        return 1 if problems else 0

    sections = [
        ("Artifacts + length bands", check_artifacts),
        ("Rubrics", check_rubrics),
        ("Track bundles", check_bundles),
        ("Decks", check_decks),
        ("Slide exhibits", check_exhibits),
        ("Figures", check_figures),
        ("Sales claims", check_sales_claims),
        ("Narration contract", check_narration),
        ("Learner site", check_learner_site),
        ("EN / 中文 terms", check_terms_zh),
    ]
    failed = 0
    for title, fn in sections:
        problems = fn()
        status = "PASS" if not problems else f"FAIL ({len(problems)})"
        summary = getattr(fn, "summary", "")
        print(f"[{status}] {title}" + (f" ({summary})" if summary else ""))
        for p in problems[:25]:
            print("    " + p)
        if len(problems) > 25:
            print(f"    … and {len(problems) - 25} more")
        failed += len(problems)

    checked, ranges, problems = check_pointers()
    held, anchor_problems = check_anchors()
    problems += anchor_problems
    status = "PASS" if not problems else f"FAIL ({len(problems)})"
    print(f"[{status}] Repo file pointers ({checked} checked, {ranges} line ranges verified, "
          f"{held} anchors held)")
    for p in problems[:25]:
        print("    " + p)
    failed += len(problems)

    print()
    print("RESULT:", "ALL CHECKS PASSED" if failed == 0 else f"{failed} problem(s)")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
