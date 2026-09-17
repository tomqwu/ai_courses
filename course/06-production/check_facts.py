#!/usr/bin/env python3
"""Re-derive the course's pinned facts from the cloned case-study repos and report drift.

`01-design/content-standards.md` §0.2 whitelists the numbers the course may state as fact
(coverage, test counts, spec-folder counts, line counts, slide counts…). `verify.py` proves every
*file pointer* still resolves, but nothing proved the *numbers* were still true — and the upstream
repos move daily. This script closes that gap:

  1. derive each pinned fact from the clone, the same way a student would (count rows, read a
     badge, count folders, read a release tag);
  2. compare against the pinned value in `facts.json`;
  3. for every fact that drifted, list the course files that still state the old literal, so the
     re-verification is a targeted edit rather than a re-read of 200 files.

    python3 course/06-production/check_facts.py            # report, exit 0
    python3 course/06-production/check_facts.py --strict   # exit 1 on any drift

Advisory by default because a drifted upstream number is not a defect of the course — it is a
re-verification task. `--strict` is for the pre-cohort checklist (instructor-guide §8), where a
stale number *is* a defect.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

COURSE = Path(__file__).resolve().parents[1]
ROOT = COURSE.parent
FACTS = Path(__file__).with_name("facts.json")


def _lines(path: str) -> int | None:
    p = ROOT / path
    return sum(1 for _ in p.open(encoding="utf-8")) if p.exists() else None


def _count_dirs(path: str, pattern: str) -> int | None:
    p = ROOT / path
    if not p.is_dir():
        return None
    return sum(1 for d in p.iterdir() if d.is_dir() and re.match(pattern, d.name))


def _exists(path: str) -> bool | None:
    return (ROOT / path).exists() if (ROOT / path.split("/")[0]).exists() else None


def _grep_first(path: str, pattern: str, group: int = 1) -> str | None:
    p = ROOT / path
    if not p.exists():
        return None
    m = re.search(pattern, p.read_text(encoding="utf-8"), re.M)
    return m.group(group) if m else None


def _table_rows(path: str) -> int | None:
    """Data rows of the first Markdown table (excluding header and separator)."""
    p = ROOT / path
    if not p.exists():
        return None
    rows, in_table = 0, False
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.startswith("|"):
            if re.match(r"^\|\s*-", line):
                in_table = True
                continue
            if in_table:
                rows += 1
        elif in_table and rows:
            break
    return rows


def _def_count(path: str) -> int | None:
    p = ROOT / path
    if not p.is_dir():
        return None
    return sum(len(re.findall(r"^\s*(?:async )?def test_", f.read_text(encoding="utf-8", errors="ignore"), re.M))
               for f in p.rglob("*.py"))


def _latest_tag(repo: str, prefix: str) -> str | None:
    p = ROOT / repo
    if not p.is_dir():
        return None
    try:
        out = subprocess.run(["git", "-C", str(p), "tag", "--list", f"{prefix}*", "--sort=-v:refname"],
                             capture_output=True, text=True, check=True).stdout.split()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return out[0] if out else None


def _json_slide_counts(path: str) -> str | None:
    p = ROOT / path
    if not p.exists():
        return None
    counts: list[int] = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "slides" and isinstance(v, int):
                    counts.append(v)
                elif k == "slides" and isinstance(v, list):
                    counts.append(len(v))
                walk(v)
        elif isinstance(o, list):
            for i in o:
                walk(i)

    walk(json.loads(p.read_text(encoding="utf-8")))
    return f"{sum(counts)} = {'+'.join(map(str, counts))}" if counts else None


def _count_files(path: str, glob: str) -> int | None:
    p = ROOT / path
    return sum(1 for _ in p.rglob(glob)) if p.is_dir() else None


def _lines_glob(path: str, glob: str) -> int | None:
    p = ROOT / path
    if not p.is_dir():
        return None
    return sum(sum(1 for _ in f.open(encoding="utf-8", errors="ignore")) for f in p.rglob(glob))


def _line_of(path: str, pattern: str) -> int | None:
    """1-based line number of the first line matching `pattern`."""
    p = ROOT / path
    if not p.exists():
        return None
    for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if re.search(pattern, line):
            return i
    return None


def _current_pdf_editions() -> int | None:
    """PDFs in ai_qe/assets/pdf at the editions release.yml names: full + guided decks at
    slide_edition / fintech_edition, the questionnaire and the research companion at theirs."""
    rel = ROOT / "ai_qe/_data/release.yml"
    pdf = ROOT / "ai_qe/assets/pdf"
    if not rel.exists() or not pdf.is_dir():
        return None
    ed = dict(re.findall(r'^(\w+):\s*"([^"]+)"', rel.read_text(encoding="utf-8"), re.M))
    try:
        patterns = [
            rf"^ai-qe-(evp|technical)(-guided)?-v{re.escape(ed['slide_edition'])}\.pdf$",
            rf"^ai-qe-fintech-(evp|technical)(-guided)?-v{re.escape(ed['fintech_edition'])}\.pdf$",
            rf"^ai-qe-discovery-questionnaire-v{re.escape(ed['questionnaire_edition'])}\.pdf$",
            rf"^ai-qe-industry-research-v{re.escape(ed['research_edition'])}\.pdf$",
        ]
    except KeyError:
        return None
    return sum(1 for f in pdf.iterdir() if any(re.match(pat, f.name) for pat in patterns))


DERIVATIONS = {
    "listentome.coverage_badge": lambda: _grep_first("ListenToMe/README.md", r"Core_coverage-(\d+)%25"),
    "listentome.coverage_floor": lambda: _grep_first("ListenToMe/scripts/check-coverage.sh", r'THRESHOLD="\$\{1:-(\d+)\}"'),
    "listentome.competitor_rows": lambda: _table_rows("ListenToMe/docs/competition-analysis.md"),
    "listentome.latest_macos_tag": lambda: _latest_tag("ListenToMe", "v"),
    "listentome.gap_review_verdict": lambda: _grep_first(
        "ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md", r"\*\*Recommendation: (.+?)\.\*\*"),
    "signupflow.agents_md_lines": lambda: _lines("SignUpFlow/AGENTS.md"),
    "signupflow.constitution_lines": lambda: _lines("SignUpFlow/.specify/memory/constitution.md"),
    "signupflow.claude_md_lines": lambda: _lines("SignUpFlow/CLAUDE.md"),
    "signupflow.copilot_lines": lambda: _lines("SignUpFlow/.github/copilot-instructions.md"),
    "listentome.competition_updated": lambda: _grep_first("ListenToMe/docs/competition-analysis.md", r"_Last updated: (\d{4}-\d{2})"),
    "signupflow.spec_folders": lambda: _count_dirs("SignUpFlow/specs", r"."),
    "signupflow.spec_014_has_tasks": lambda: _exists("SignUpFlow/specs/014-security-hardening/tasks.md"),
    "signupflow.validation_status": lambda: _grep_first("SignUpFlow/docs/playbooks/validation.md", r"^> (Historical reference)"),
    "signupflow.test_functions": lambda: _def_count("SignUpFlow/tests"),
    "ai_qe.slide_counts": lambda: _json_slide_counts("ai_qe/_data/briefing_room.json"),
    "ai_qe.site_version": lambda: _grep_first("ai_qe/_data/release.yml", r'^version:\s*"([^"]+)"'),
    "ai_qe.self_audit_findings": lambda: _grep_first(
        "ai_qe/research/reviews/site-audit-2026-09-06.md", r"identifies \*\*(\d+) findings"),
    "listentome.core_swift_files": lambda: _count_files("ListenToMe/Sources/ListenToMeCore", "*.swift"),
    "listentome.core_swift_lines": lambda: _lines_glob("ListenToMe/Sources/ListenToMeCore", "*.swift"),
    "ai_qe.current_pdf_editions": _current_pdf_editions,
    "signupflow.health_score_line": lambda: _line_of("SignUpFlow/api/cli/main.py", r'click\.echo\(f"Health score: '),
}


def course_files_stating(literals: list[str]) -> list[str]:
    hits: set[str] = set()
    for path in COURSE.rglob("*.md"):
        rel = str(path.relative_to(COURSE))
        # Transcripts are generated from the decks, and the review documents record the drift on
        # purpose — neither is a place where a stale number needs editing.
        if rel.startswith("learner-site/transcripts") or re.match(r"00-research/0[4-9]-", rel):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if any(lit in text for lit in literals):
            hits.add(str(path.relative_to(COURSE)))
    return sorted(hits)


def main(argv: list[str]) -> int:
    strict = "--strict" in argv
    facts = json.loads(FACTS.read_text(encoding="utf-8"))
    missing_clone = [r for r in ("ListenToMe", "SignUpFlow", "ai_qe") if not (ROOT / r).is_dir()]
    if missing_clone:
        print(f"cannot derive: clone {', '.join(missing_clone)} into {ROOT} first "
              f"(see 03-content/m00-orientation/lab.md)")
        return 2 if strict else 0

    drifted = 0
    print(f"{'fact':38} {'pinned':>22} {'derived now':>22}  status")
    for key, spec in facts.items():
        derived = DERIVATIONS[key]()
        pinned = spec["pinned"]
        if derived is None:
            status = "UNDERIVABLE"
        elif str(derived) == str(pinned):
            status = "ok"
        else:
            status = "DRIFT"
            drifted += 1
        print(f"{key:38} {str(pinned)[:22]:>22} {str(derived)[:22]:>22}  {status}")
        if status == "DRIFT":
            if len(str(pinned)) > 22 or len(str(derived)) > 22:
                print(f"    pinned:  {pinned}\n    derived: {derived}")
            files = course_files_stating(spec.get("literals", []))
            print(f"    pinned on {spec['pinned_date']} — {spec['note']}")
            if files:
                print(f"    still stated in {len(files)} course file(s): " + ", ".join(files[:6])
                      + (" …" if len(files) > 6 else ""))

    print()
    if drifted:
        print(f"{drifted} pinned fact(s) have drifted upstream. Re-verify and update "
              f"01-design/content-standards.md §0.2 plus the files listed above, or record the "
              f"divergence deliberately (the course teaches this in M4.3).")
        return 1 if strict else 0
    print("all pinned facts re-derive to their pinned values")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
