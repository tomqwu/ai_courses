#!/usr/bin/env python3
"""Re-derive the numbers your documentation states as fact, and report the ones that drifted.

Pointers prove a *file* still exists. Nothing proves the *numbers* are still true — and numbers are
what readers check you on: line counts, test counts, table rows, version tags. This tool keeps a
small pinned file of the numbers you are willing to state, re-derives each one from the source, and
for every number that moved, lists the documents that still print the old value.

    python3 facts_drift.py --facts facts.json --base . --docs docs/
    python3 facts_drift.py --facts facts.json --strict      # exit 1 on any drift

`facts.json` is data, not code — derivations are declarative and this tool never executes anything
from it, so a facts file from a pull request cannot run commands on your machine:

    {
      "agents_md.lines":   {"pinned": 188, "pinned_date": "2026-09-16",
                            "derive": {"kind": "file_lines", "path": "SignUpFlow/AGENTS.md"},
                            "literals": ["AGENTS.md is 188 lines", "188-line"]},
      "core.swift_files":  {"pinned": 45,
                            "derive": {"kind": "glob_count", "glob": "ListenToMe/Sources/**/*.swift"}},
      "core.swift_lines":  {"pinned": 5194,
                            "derive": {"kind": "glob_lines", "glob": "ListenToMe/Sources/**/*.swift"}},
      "competitors.rows":  {"pinned": 14,
                            "derive": {"kind": "table_rows", "path": "docs/competition.md"}},
      "latest.release":    {"pinned": "v1.4.4",
                            "derive": {"kind": "regex_capture", "path": "CHANGELOG.md",
                                       "pattern": "## (v[0-9.]+)"}},
      "tests.recorded":    {"pinned": 1464,
                            "derive": {"kind": "regex_count", "path": "tests/test_api.py",
                                       "pattern": "^def test_"}},
      "score.line":        {"pinned": 193,
                            "derive": {"kind": "line_of", "path": "api/cli/main.py",
                                       "pattern": "Health score"}}
    }

`literals` is optional: exact strings to grep for when that fact drifts, so re-verification is a
targeted edit instead of a re-read of every document. Standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}
TABLE_ROW_RE = re.compile(r"^\|(?!\s*[-:| ]+\|\s*$).+\|\s*$")


class DerivationError(RuntimeError):
    pass


def _read(base: Path, rel: str) -> str:
    path = base / rel
    if not path.is_file():
        raise DerivationError(f"no such file: {rel}")
    return path.read_text(encoding="utf-8", errors="replace")


def _glob(base: Path, pattern: str) -> list[Path]:
    # Path.glob does not accept an absolute-looking pattern, so the first segment anchors the walk.
    return sorted(p for p in base.glob(pattern) if p.is_file())


def derive(spec: dict, base: Path):
    """Evaluate one declarative derivation. Only these kinds exist; nothing here runs a command."""
    kind = spec.get("kind")
    if kind == "file_lines":
        return len(_read(base, spec["path"]).splitlines())
    if kind == "glob_count":
        return len(_glob(base, spec["glob"]))
    if kind == "glob_lines":
        return sum(len(p.read_text(encoding="utf-8", errors="replace").splitlines())
                   for p in _glob(base, spec["glob"]))
    if kind == "regex_count":
        flags = re.M | (re.I if spec.get("ignorecase") else 0)
        return len(re.findall(spec["pattern"], _read(base, spec["path"]), flags))
    if kind == "regex_capture":
        flags = re.M | (re.I if spec.get("ignorecase") else 0)
        match = re.search(spec["pattern"], _read(base, spec["path"]), flags)
        if not match:
            raise DerivationError(f"pattern never matched in {spec['path']}: {spec['pattern']}")
        value = match.group(spec.get("group", 1))
        return int(value) if spec.get("cast") == "int" else value
    if kind == "line_of":
        flags = re.I if spec.get("ignorecase") else 0
        for number, line in enumerate(_read(base, spec["path"]).splitlines(), 1):
            if re.search(spec["pattern"], line, flags):
                return number
        raise DerivationError(f"pattern never matched in {spec['path']}: {spec['pattern']}")
    if kind == "table_rows":
        text = _read(base, spec["path"])
        if spec.get("after"):
            _, _, text = text.partition(spec["after"])
        rows = [line for line in text.splitlines() if TABLE_ROW_RE.match(line.strip())]
        header = 1 if rows else 0
        return max(0, len(rows) - header)
    raise DerivationError(f"unknown derivation kind: {kind!r}")


def find_literals(literals: list[str], docs: list[Path]) -> list[str]:
    """Where a stale value is still printed, as `path:line`."""
    hits: list[str] = []
    for doc in docs:
        try:
            lines = doc.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for number, line in enumerate(lines, 1):
            if any(literal in line for literal in literals):
                hits.append(f"{doc}:{number}")
    return hits


def doc_files(roots: list[Path]) -> list[Path]:
    out: list[Path] = []
    for root in roots:
        if root.is_file():
            out.append(root)
            continue
        for path in sorted(root.rglob("*.md")):
            if not SKIP_DIRS & set(path.parts):
                out.append(path)
    return out


def check(facts: dict, base: Path, docs: list[Path]) -> list[dict]:
    rows = []
    for key, spec in facts.items():
        if key.startswith("_"):
            continue
        row = {"key": key, "pinned": spec.get("pinned"), "pinned_date": spec.get("pinned_date", ""),
               "derived": None, "status": "ok", "note": spec.get("note", ""), "where": []}
        try:
            row["derived"] = derive(spec["derive"], base) if "derive" in spec else None
        except (DerivationError, KeyError, re.error) as error:
            row["status"] = "error"
            row["note"] = str(error)
            rows.append(row)
            continue
        if row["derived"] is None:
            row["status"] = "pinned"
        elif str(row["derived"]) != str(row["pinned"]):
            row["status"] = "drift"
            if spec.get("literals") and docs:
                row["where"] = find_literals(spec["literals"], docs)
        rows.append(row)
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--facts", default="facts.json", help="the pinned facts file (default: facts.json)")
    parser.add_argument("--base", default=".", help="directory the derivations resolve against (default: .)")
    parser.add_argument("--docs", action="append", default=None,
                        help="folder of Markdown to search for stale literals (repeatable)")
    parser.add_argument("--strict", action="store_true", help="exit 1 when anything drifted")
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    args = parser.parse_args(argv)

    facts_path = Path(args.facts)
    if not facts_path.is_file():
        print(f"facts_drift: no such facts file: {facts_path}", file=sys.stderr)
        return 2
    try:
        facts = json.loads(facts_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        print(f"facts_drift: {facts_path} is not valid JSON: {error}", file=sys.stderr)
        return 2

    docs = doc_files([Path(d) for d in args.docs]) if args.docs else []
    rows = check(facts, Path(args.base).resolve(), docs)
    drifted = [r for r in rows if r["status"] == "drift"]
    errored = [r for r in rows if r["status"] == "error"]

    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        width = max((len(r["key"]) for r in rows), default=10)
        for row in rows:
            derived = "—" if row["derived"] is None else row["derived"]
            print(f"{row['key']:<{width}}  {str(row['pinned']):>12}  {str(derived):>12}  {row['status']}")
            if row["status"] == "error":
                print(f"{'':<{width}}  {row['note']}")
            for where in row["where"]:
                print(f"{'':<{width}}  still stated at {where}")
        print()
        if drifted:
            print(f"{len(drifted)} of {len(rows)} fact(s) drifted since they were pinned")
        elif errored:
            print(f"{len(errored)} derivation(s) could not run; the rest re-derive to their pinned values")
        else:
            print(f"all {len(rows)} pinned facts re-derive to their pinned values")
    if errored:
        return 2
    return 1 if (drifted and args.strict) else 0


if __name__ == "__main__":
    raise SystemExit(main())
