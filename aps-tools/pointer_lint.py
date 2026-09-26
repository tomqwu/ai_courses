#!/usr/bin/env python3
"""Check that every file pointer in your documentation still resolves.

A pointer is a backticked path in Markdown, optionally with line numbers:

    `SignUpFlow/AGENTS.md`            the file must exist
    `api/routers/events.py:88`        line 88 must exist in it
    `src/Prompt.swift:73-81, 99`      every range must lie inside the file

Documentation rots in a specific way: the prose stays plausible while the code moves underneath it.
A reader who follows a pointer into a file that no longer has those lines stops trusting every other
claim on the page. This makes that failure loud and cheap to fix.

    python3 pointer_lint.py docs/                     # lint one folder
    python3 pointer_lint.py --base .. --roots ListenToMe,SignUpFlow course/
    python3 pointer_lint.py --json .                  # machine-readable

Exit status is 1 when any pointer does not resolve, so it drops into a pre-commit hook or CI.
Standard library only; nothing is written and nothing is sent anywhere.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# A pointer is a backticked token holding a slash, optionally followed by one or more line ranges:
# `path/to/file.py`, `path/to/file.py:88`, `path/to/file.py:73-81, 99`. The trailing group lets a
# second, space-separated range stay inside the same pointer.
POINTER_RE = re.compile(r"`([^`\s]+/[^`\s]+?(?::\d+(?:[-–]\d+)?(?:,\s*\d+(?:[-–]\d+)?)*)?)`")
RANGE_RE = re.compile(r"^(\d+)(?:[-–](\d+))?$")
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".mypy_cache"}
# A backticked token with a slash in it is not always a path. These are the shapes that reliably
# are not one, and reporting them as broken pointers is how a linter loses its reader:
#   /v1/things, /solutions/{id}/export   an API route, not a file on disk
#   America/Toronto, owner/repo          a timezone, a repository slug
# A token counts as a pointer when its last segment has an extension, when it ends in a slash (a
# directory written as one), or when it carries a line reference — never when it is templated.
TEMPLATE_RE = re.compile(r"[{}<>*?]")


def parse_ranges(suffix: str) -> list[tuple[int, int]]:
    """`88` → [(88, 88)]; `73-81, 99` → [(73, 81), (99, 99)]. Anything else → []."""
    out: list[tuple[int, int]] = []
    for part in suffix.split(","):
        match = RANGE_RE.match(part.strip())
        if not match:
            return []
        start = int(match.group(1))
        end = int(match.group(2) or match.group(1))
        out.append((start, end))
    return out


def looks_like_path(token: str, suffix: str = "") -> bool:
    """Is this backticked token a file path, rather than a route, a slug or a timezone?"""
    if not token or token.startswith(("/", "http://", "https://", "mailto:", "~")):
        return False
    if TEMPLATE_RE.search(token):
        return False
    if suffix and parse_ranges(suffix):
        return True                       # an explicit line reference means a file
    if token.endswith("/"):
        return True                       # a directory, written as one
    return "." in token.rsplit("/", 1)[-1]


def markdown_files(targets: list[Path]) -> list[Path]:
    found: list[Path] = []
    for target in targets:
        if target.is_file():
            found.append(target)
            continue
        for path in sorted(target.rglob("*.md")):
            if not SKIP_DIRS & set(path.parts):
                found.append(path)
    return found


def lint(targets: list[Path], base: Path, roots: set[str] | None = None) -> dict:
    """Resolve every pointer in every Markdown file under `targets`, relative to `base`."""
    problems: list[dict] = []
    checked = ranges_checked = 0
    line_counts: dict[Path, int] = {}

    def count_lines(path: Path) -> int:
        if path not in line_counts:
            try:
                with path.open("rb") as handle:
                    line_counts[path] = sum(1 for _ in handle)
            except OSError:
                line_counts[path] = 0
        return line_counts[path]

    files = markdown_files(targets)
    for doc in files:
        try:
            text = doc.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for match in POINTER_RE.finditer(line):
                raw = match.group(1)
                path_part, _, suffix = raw.partition(":")
                path_part = path_part.split("#")[0]
                definite = looks_like_path(path_part, suffix)
                target = (base / path_part).resolve()
                if not definite:
                    # Ambiguous: `owner/repo`, `America/Toronto` and `some/dir` are the same shape.
                    # If it resolves, it was a pointer and it is fine; if it does not, there is no
                    # way to tell a broken pointer from a slug, so it is not reported as either.
                    if not target.exists():
                        continue
                if roots is not None and path_part.split("/")[0] not in roots:
                    continue
                if path_part.startswith(("http", "https", "mailto")):
                    continue
                checked += 1
                record = {"doc": str(doc), "line": lineno, "pointer": raw}
                if not target.exists():
                    problems.append({**record, "problem": "no such file"})
                    continue
                spans = parse_ranges(suffix) if suffix else []
                if not spans:
                    continue
                if target.is_dir():
                    problems.append({**record, "problem": "line range on a directory"})
                    continue
                total = count_lines(target)
                for start, end in spans:
                    ranges_checked += 1
                    if start < 1 or end < start or end > total:
                        problems.append({**record, "problem": f"lines {start}-{end} outside 1-{total}"})
    return {"files": len(files), "pointers": checked, "ranges": ranges_checked, "problems": problems}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("targets", nargs="*", default=["."], help="Markdown files or folders (default: .)")
    parser.add_argument("--base", default=None,
                        help="directory pointers resolve against (default: the first target, or its parent "
                             "when --roots names sibling repositories)")
    parser.add_argument("--roots", default=None,
                        help="comma-separated first path segments to lint, e.g. sibling repo names; "
                             "pointers outside them are ignored")
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    args = parser.parse_args(argv)

    targets = [Path(t) for t in (args.targets or ["."])]
    for target in targets:
        if not target.exists():
            print(f"pointer_lint: no such path: {target}", file=sys.stderr)
            return 2
    roots = {r.strip() for r in args.roots.split(",")} if args.roots else None
    if args.base:
        base = Path(args.base)
    else:
        first = targets[0] if targets[0].is_dir() else targets[0].parent
        base = first.parent if roots else first
    report = lint(targets, base.resolve(), roots)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for problem in report["problems"]:
            print(f"{problem['doc']}:{problem['line']}: {problem['pointer']} — {problem['problem']}")
        summary = (f"{report['pointers']} pointer(s) in {report['files']} file(s), "
                   f"{report['ranges']} line range(s) checked against {base}")
        print(summary if not report["problems"] else f"{summary} — {len(report['problems'])} did not resolve")
    return 1 if report["problems"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
