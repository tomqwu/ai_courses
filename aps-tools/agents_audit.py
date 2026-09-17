#!/usr/bin/env python3
"""Audit an agent rule file — AGENTS.md, CLAUDE.md, a constitution — for rules a stranger could check.

An agent rule file fails in two directions. It gets too long to be read in full on every task, and
it fills with advice no one can verify: "be careful with tenancy", "use good judgement", "where
possible, prefer composition". A rule that cannot be checked cannot be enforced, so it is decoration.

This reads a rule file and reports, per rule:

  * **checkable** — names a path, a command, a number, or a concrete artifact, in an imperative
    voice ("Every database query MUST filter by org_id");
  * **vague** — hedged or subjective, with the phrase that makes it so;
  * **unenforced** — imperative but naming nothing a reader could open or run.

    python3 agents_audit.py AGENTS.md
    python3 agents_audit.py --max-lines 200 --min-checkable 0.8 AGENTS.md CLAUDE.md
    python3 agents_audit.py --json .specify/memory/constitution.md

Exit status is 1 when a file is over its line budget or below the checkable threshold, so it fits in
CI next to your linters. Standard library only; nothing is written and nothing leaves the machine.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

IMPERATIVE_RE = re.compile(r"\b(MUST NOT|MUST|NEVER|ALWAYS|SHALL|DO NOT|DON'T|REQUIRED|FORBIDDEN|"
                           r"Never|Always|Must|Do not)\b")
# An anchor is something a reader can open, run, or count: a backticked token, a file name, a
# number, or an ALL_CAPS identifier. The imperative keywords are stripped before the search, so
# "You MUST write clean code" does not count its own MUST as the thing to check.
ANCHOR_RE = re.compile(r"`[^`]+`|\b[\w./-]+\.(?:py|md|json|ya?ml|swift|ts|tsx|js|toml|sh|sql)\b|"
                       r"\b\d+\b|\b[A-Z][A-Z0-9_]{2,}\b")
VAGUE = [
    "be careful", "as appropriate", "where possible", "if possible", "try to", "good practice",
    "best practice", "reasonable", "use judgement", "use judgment", "make sense", "as needed",
    "etc.", "and so on", "generally", "usually", "ideally", "consider ", "avoid unnecessary",
    "keep it clean", "high quality", "well-written", "properly", "appropriately", "sensible",
]
RULE_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(.*\S)\s*$")
HEADING_RE = re.compile(r"^\s*#{1,6}\s+")


def rules_in(text: str) -> list[tuple[int, str]]:
    """Every list item, plus any non-list line carrying an imperative. Headings and code are skipped."""
    out: list[tuple[int, str]] = []
    in_fence = False
    for number, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or HEADING_RE.match(line) or not line.strip():
            continue
        match = RULE_RE.match(line)
        if match:
            out.append((number, match.group(1)))
        elif IMPERATIVE_RE.search(line) and not line.lstrip().startswith(">"):
            out.append((number, line.strip()))
    return out


def classify(rule: str) -> tuple[str, str]:
    """(verdict, why) for one rule."""
    lowered = rule.lower()
    for phrase in VAGUE:
        if phrase in lowered:
            return "vague", phrase.strip()
    has_anchor = bool(ANCHOR_RE.search(IMPERATIVE_RE.sub("", rule)))
    has_imperative = bool(IMPERATIVE_RE.search(rule))
    if has_anchor and has_imperative:
        return "checkable", ""
    if has_anchor:
        return "checkable", ""
    if has_imperative:
        return "unenforced", "imperative, but names nothing to open, run or count"
    return "unenforced", "neither an imperative nor anything checkable"


def audit(path: Path, max_lines: int) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    rules = rules_in(text)
    findings = []
    counts = {"checkable": 0, "vague": 0, "unenforced": 0}
    seen: dict[str, int] = {}
    for number, rule in rules:
        verdict, why = classify(rule)
        counts[verdict] += 1
        if verdict != "checkable":
            findings.append({"line": number, "verdict": verdict, "why": why, "rule": rule[:120]})
        key = re.sub(r"[^a-z0-9 ]", "", rule.lower())[:80]
        if key in seen:
            findings.append({"line": number, "verdict": "duplicate",
                             "why": f"repeats the rule on line {seen[key]}", "rule": rule[:120]})
        else:
            seen[key] = number
    total = max(1, len(rules))
    return {
        "file": str(path), "lines": len(lines), "max_lines": max_lines,
        "rules": len(rules), "counts": counts,
        "checkable_share": round(counts["checkable"] / total, 3),
        "over_budget": len(lines) > max_lines,
        "findings": findings,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="+", help="rule files to audit (AGENTS.md, CLAUDE.md, constitution.md…)")
    parser.add_argument("--max-lines", type=int, default=200,
                        help="line budget per file (default: 200 — a file an agent reads on every task)")
    parser.add_argument("--min-checkable", type=float, default=0.0,
                        help="fail below this share of checkable rules, e.g. 0.8")
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    args = parser.parse_args(argv)

    reports = []
    failed = False
    for name in args.files:
        path = Path(name)
        if not path.is_file():
            print(f"agents_audit: no such file: {path}", file=sys.stderr)
            return 2
        report = audit(path, args.max_lines)
        reports.append(report)
        if report["over_budget"] or report["checkable_share"] < args.min_checkable:
            failed = True

    if args.json:
        print(json.dumps(reports, indent=2))
        return 1 if failed else 0

    for report in reports:
        counts = report["counts"]
        budget = "over budget" if report["over_budget"] else "within budget"
        print(f"\n{report['file']}")
        print(f"  {report['lines']} lines ({budget}, limit {report['max_lines']}) · {report['rules']} rules · "
              f"{counts['checkable']} checkable, {counts['vague']} vague, {counts['unenforced']} unenforced "
              f"({report['checkable_share'] * 100:.0f}% checkable)")
        for finding in report["findings"]:
            print(f"  {finding['line']:>4}  {finding['verdict']:<10} {finding['why']}")
            print(f"        {finding['rule']}")
    print()
    if failed:
        print("FAILED: a file is over its line budget or below the checkable threshold")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
