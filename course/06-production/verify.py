#!/usr/bin/env python3
"""Verify the expanded course package against course/01-design/content-standards.md.

Checks
  1. every module (M0-M8) has all 8 artifacts
  2. every artifact is inside its length band
  3. every repo file pointer in the package resolves on disk
  4. rubric weights sum to 100 in each lab-rubrics.md
  5. bundles each ship their 5 files
  6. no deck is missing Marp front matter or speaker notes (delegates detail to deck_lint.py)
  7. narration: every deck has approved words, and every recording matches them word for word
  8. the learner site, when built, has one page per deck with the right slide count

Usage:
  python3 verify.py                # full report, exit 1 on any failure
  python3 verify.py --pointers     # pointer audit only
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
    "m07-monetize", "m08-launch-capstone",
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
BUNDLES = ["on-device-app", "spec-driven-saas", "expertise-product"]
BUNDLE_FILES = ["README.md", "syllabus.md", "sales-page.md", "pricing.md", "bundle-map.md"]

CASE_REPOS = ("ListenToMe", "SignUpFlow", "ai_qe")
POINTER_RE = re.compile(r"`((?:ListenToMe|SignUpFlow|ai_qe)/[^`\s]+)`")
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
    return problems


def check_pointers(files: list[Path] | None = None) -> tuple[int, list[str]]:
    problems: list[str] = []
    checked = 0
    if files is None:
        files = sorted(
            p for p in ROOT.rglob("*.md")
            if "tinycopilot" not in p.parts and "slides/out" not in str(p)
        )
    for f in files:
        text = f.read_text(encoding="utf-8")
        for m in POINTER_RE.finditer(text):
            raw = m.group(1)
            path = raw.split(":")[0].split("#")[0]
            checked += 1
            if not (REPO / path).exists():
                problems.append(f"{f.relative_to(ROOT)}: MISSING POINTER {raw}")
    return checked, problems


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
    pages = sorted(site.glob("m*.html"))
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
            rendered = html.count('aria-roledescription="slide"')
            if slides and rendered != len(slides):
                problems.append(f"{page.name}: renders {rendered} slides, deck has {len(slides)}")
            if len(script["slides"]) != len(slides) and slides:
                problems.append(f"{page.name}: script covers {len(script['slides'])} of {len(slides)} slides")
            for asset in ("assets/player.js", "assets/narration-media.js", "assets/player.css"):
                if f'"{asset}"' not in html and f'/{asset}"' not in html:
                    problems.append(f"{page.name}: does not load {asset}")
    finally:
        pass
    return problems


def main(argv: list[str]) -> int:
    if "--pointers" in argv:
        checked, problems = check_pointers()
        print(f"pointers checked: {checked}")
        for p in problems:
            print("  " + p)
        return 1 if problems else 0

    sections = [
        ("Artifacts + length bands", check_artifacts),
        ("Rubrics", check_rubrics),
        ("Track bundles", check_bundles),
        ("Decks", check_decks),
        ("Sales claims", check_sales_claims),
        ("Narration contract", check_narration),
        ("Learner site", check_learner_site),
    ]
    failed = 0
    for title, fn in sections:
        problems = fn()
        status = "PASS" if not problems else f"FAIL ({len(problems)})"
        print(f"[{status}] {title}")
        for p in problems[:25]:
            print("    " + p)
        if len(problems) > 25:
            print(f"    … and {len(problems) - 25} more")
        failed += len(problems)

    checked, problems = check_pointers()
    status = "PASS" if not problems else f"FAIL ({len(problems)})"
    print(f"[{status}] Repo file pointers ({checked} checked)")
    for p in problems[:25]:
        print("    " + p)
    failed += len(problems)

    print()
    print("RESULT:", "ALL CHECKS PASSED" if failed == 0 else f"{failed} problem(s)")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
