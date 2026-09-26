#!/usr/bin/env python3
"""Lab M6 self-check: every quantitative claim must sit in a sentence that cites its source.

Usage:
    python3 selfcheck.py FILE.md [FILE2.md ...]   exit 0 = pass, exit 1 = uncited claims listed
    python3 selfcheck.py --selftest               run on selfcheck-examples/good.md and bad.md

What counts as a quantitative claim (checked per sentence, outside headings and code fences):
  - a percentage:            19%   55.8 %   +2% to +39%
  - a currency amount:       $450k   EUR 10M   £2,000
  - an ISO date or a year:   2026-09-04   2025
  - a number with a unit or a count word:  16 maintainers, 246 issues, 60 seconds, 3.3x
  - a bare number of two or more digits, or any decimal:  246   47.6
Structural numbers are NOT claims: slide/row/step/phase/level/version/edition/priority labels
("slide 3", "row 12", "Phase 0", "level 1-4", "v1.24.0", "P1", "FR-001", "12-slide"), ordinals
at the start of a list item, and anything inside inline backticks or a Markdown link target.

What counts as a citation (anywhere in the same sentence, or the same table row / list item):
  1. a backticked repo pointer with a line anchor:  `ai_qe/docs/evidence/benchmarks.md:31`
                                                   `SignUpFlow/docs/TESTING.md:12-40`
  2. a URL:                                          https://metr.org/blog/...
  3. a source tag:                                   [source: METR 2025, row 1]   [source: row 4]

A unit is a table row, a list item, or one sentence of a paragraph; a paragraph's sentences all
report the paragraph's first line number.

Why this shape: the AI x QE research conventions require every record to carry date, sample,
method, unit, self-reported vs measured, sponsor and the claim it supports, and anything
unverifiable to be listed as unverifiable (`ai_qe/CONTRIBUTING.md:93-94`). This script cannot
check any of that. It checks the one thing a script can: that a number never appears without a
pointer to the record behind it. The same repo is explicit about the limit -- a link that
resolves is not evidence that the claim is correct (`ai_qe/CONTRIBUTING.md:139-141`). Nor does
it follow a `[source: row N]` tag to check that row N is itself sourced -- bad.md line 23 cites a
row that the same file flags on line 14. A green run means no orphan numbers, not a true
briefing.

The check is deliberately strict: it over-flags rather than under-flags, and it has no ignore
list. If it flags a number that is not a claim, rephrase the sentence or cite it anyway.
stdlib only; Python 3.11.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

POINTER_RE = re.compile(r"`[A-Za-z0-9_.-]+/[^`\s]+:\d+(?:-\d+)?`")
URL_RE = re.compile(r"https?://[^\s)>\]]+")
SOURCE_TAG_RE = re.compile(r"\[source:\s*[^\]]+\]", re.IGNORECASE)

INLINE_CODE_RE = re.compile(r"`[^`]*`")
LINK_TARGET_RE = re.compile(r"\]\([^)]*\)")          # ](http://...) — target only, label stays
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s")
FENCE_RE = re.compile(r"^\s{0,3}(```|~~~)")
LIST_ORDINAL_RE = re.compile(r"^\s*\d+[.)]\s+")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{2,}")

STRUCTURAL_BEFORE = (
    r"(?:slides?|rows?|steps?|phases?|levels?|tiers?|versions?|editions?|priorit(?:y|ies)|"
    r"chapters?|sections?|figures?|tables?|items?|entr(?:y|ies)|questions?|q|us|fr|sc|p|t|v|#|§)"
)
STRUCTURAL_AFTER = r"(?:-slide|-row|-step|-phase|-level|-question|-item|-entry)"
STRUCTURAL_RE = re.compile(
    rf"(?:\b{STRUCTURAL_BEFORE}\s?-?\d+(?:[-–]\d+)?[a-z]?\b)|(?:\b\d+{STRUCTURAL_AFTER}s?\b)|"
    r"(?:\b[A-Z]{1,3}-\d+\b)|(?:\bv?\d+\.\d+\.\d+\b)",
    re.IGNORECASE,
)

PERCENT_RE = re.compile(r"(?<![\d.])[+\-−]?\d+(?:[.,]\d+)?\s?%")
CURRENCY_RE = re.compile(r"(?:[$€£]|\b(?:usd|eur|gbp|cad)\s?)\d[\d,.]*\s?[kmb]?(?:illion)?\b", re.IGNORECASE)
DATE_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b|\b(?:19|20)\d{2}\b")
NUMBER_RE = re.compile(
    r"(?<![\d.])[+\-−]?\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b|(?<![\d.])[+\-−]?\b\d+\.\d+\b|"
    r"(?<![\d.])[+\-−]?\b\d{2,}\b|\b\d\s?(?:x|×)\b"
)
UNIT_COUNT_RE = re.compile(
    r"\b\d+(?:\.\d+)?\s?(?:%|x|×|k|m|bn|ms|s|min|mins|minutes?|hours?|days?|weeks?|months?|years?|"
    r"seconds?|people|persons?|users?|developers?|maintainers?|freelancers?|engineers?|tests?|"
    r"issues?|tasks?|failures?|classes?|files?|slides?|rows?|entries|studies|participants|"
    r"organi[sz]ations?|companies|teams?|pull requests?|prs?|commits?|lines?)\b",
    re.IGNORECASE,
)


@dataclass
class Finding:
    path: str
    line: int
    sentence: str
    claims: list[str]

    def __str__(self) -> str:
        excerpt = self.sentence if len(self.sentence) <= 110 else self.sentence[:107] + "..."
        return f"{self.path}:{self.line}: {excerpt}\n    uncited: {', '.join(self.claims)}"


def is_cited(sentence: str) -> bool:
    return bool(POINTER_RE.search(sentence) or URL_RE.search(sentence) or SOURCE_TAG_RE.search(sentence))


def claims_in(sentence: str) -> list[str]:
    """Return the quantitative tokens in a sentence that are claims, not structure."""
    text = INLINE_CODE_RE.sub(" ", sentence)
    text = LINK_TARGET_RE.sub("]", text)
    text = URL_RE.sub(" ", text)
    text = SOURCE_TAG_RE.sub(" ", text)
    text = LIST_ORDINAL_RE.sub("", text)
    text = STRUCTURAL_RE.sub(" ", text)
    found: list[tuple[int, int, str]] = []
    for rx in (PERCENT_RE, CURRENCY_RE, UNIT_COUNT_RE, DATE_RE, NUMBER_RE):
        for m in rx.finditer(text):
            tok = m.group(0).strip()
            if tok:
                start = m.start() + m.group(0).index(tok)
                found.append((start, start + len(tok), tok))
    # De-duplicate by span: the regexes overlap on purpose (2026-09-04 is a date and two
    # numbers; 3.3x is a decimal and a multiple). Longest match at the earliest start wins,
    # and anything overlapping it is dropped, so one claim is reported once.
    kept: list[tuple[int, int, str]] = []
    for start, end, tok in sorted(found, key=lambda f: (f[0], -(f[1] - f[0]))):
        if any(start < k_end and k_start < end for k_start, k_end, _ in kept):
            continue
        kept.append((start, end, tok))
    return [tok for _, _, tok in kept]


def units(path: Path) -> list[tuple[int, str]]:
    """Split a Markdown file into checkable units: (line number, text).

    A table row or a list item is one unit. Consecutive prose lines form a paragraph that is split
    into sentences; each sentence reports the paragraph's first line. Headings, code fences, and
    table separator rows are skipped.
    """
    out: list[tuple[int, str]] = []
    para: list[str] = []
    para_line = 0
    in_fence = False

    def flush() -> None:
        nonlocal para, para_line
        if para:
            text = " ".join(s.strip() for s in para)
            for sent in re.split(r"(?<=[.!?])\s+(?=[A-Z\[\"“(*_])", text):
                if sent.strip():
                    out.append((para_line, sent.strip()))
        para, para_line = [], 0

    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.rstrip()
        if FENCE_RE.match(line):
            flush()
            in_fence = not in_fence
            continue
        if in_fence or not line.strip():
            flush()
            continue
        if HEADING_RE.match(line) or TABLE_SEP_RE.match(line):
            flush()
            continue
        stripped = line.strip()
        if stripped.startswith("|") or re.match(r"^\s*(?:[-*+]|\d+[.)])\s+", line):
            flush()
            out.append((n, stripped))
            continue
        if not para:
            para_line = n
        para.append(line)
    flush()
    return out


def check(path: Path, label: str | None = None) -> list[Finding]:
    """Findings for one file. `label` is what the report prints instead of the path on disk."""
    findings: list[Finding] = []
    for line, sentence in units(path):
        if is_cited(sentence):
            continue
        claims = claims_in(sentence)
        if claims:
            findings.append(Finding(label or str(path), line, sentence, claims))
    return findings


def run(paths: list[Path]) -> int:
    total = 0
    for p in paths:
        if not p.is_file():
            print(f"{p}: not a file")
            return 2
        findings = check(p)
        total += len(findings)
        for f in findings:
            print(f)
    if total:
        print(f"\nFAIL: {total} uncited quantitative claim(s) in {len(paths)} file(s)")
        return 1
    print(f"PASS: 0 uncited quantitative claims in {len(paths)} file(s)")
    return 0


EXAMPLES = Path(__file__).resolve().parent / "selfcheck-examples"
# bad.md is written to fail on exactly these lines, one per failure mode:
#   13  a repo pointer with no line anchor is not a pointer
#   14  "internal notes" is not a source
#   22  a slide line with a number and no [source: …] tag
#   27  a percentage range asserted in prose
#   30  a currency amount asserted in prose
#   32  a multiple asserted in prose
EXPECTED_BAD_LINES = (13, 14, 22, 27, 30, 32)


def selftest() -> int:
    """Run the checker over the two bundled examples and assert both outcomes."""
    good, bad = EXAMPLES / "good.md", EXAMPLES / "bad.md"
    missing = [f for f in (good, bad) if not f.is_file()]
    if missing:
        for f in missing:
            print(f"SELFTEST: bundled example missing: {f}")
        return 2

    ok = True
    good_findings = check(good, f"{EXAMPLES.name}/{good.name}")
    print(f"[{'PASS' if not good_findings else 'FAIL'}] {good.name}: "
          f"{len(good_findings)} uncited claim(s), expected 0")
    for f in good_findings:
        print("    " + str(f).replace("\n", "\n    "))
    ok &= not good_findings

    bad_findings = check(bad, f"{EXAMPLES.name}/{bad.name}")
    lines = tuple(f.line for f in bad_findings)
    hit = lines == EXPECTED_BAD_LINES
    print(f"[{'PASS' if hit else 'FAIL'}] {bad.name}: flagged lines {list(lines)}, "
          f"expected {list(EXPECTED_BAD_LINES)}")
    for f in bad_findings:
        print(f"    line {f.line}: {', '.join(f.claims)}")
    ok &= hit

    print(f"Full report: selfcheck.py {EXAMPLES.name}/{bad.name}")
    print("\nSELFTEST:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0 if argv else 2
    if argv[0] == "--selftest":
        return selftest()
    return run([Path(a) for a in argv])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
