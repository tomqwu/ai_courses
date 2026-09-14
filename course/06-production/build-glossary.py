#!/usr/bin/env python3
"""Build course/06-production/glossary-master.md from the nine module glossaries.

Merge rules
  * An entry is a blank-line-separated block whose first line starts `**Term** — ...`
    (bullet-prefixed and multi-line entries are both supported).
  * Terms are deduplicated case-insensitively and punctuation-insensitively.
  * A duplicate keeps the longest definition and records every module that uses the term.
  * "Term A vs Term B" confusion pairs are skipped here; they stay in their module glossary.

Re-run after editing any module glossary:  python3 build-glossary.py
"""
from __future__ import annotations

import collections
import pathlib
import re

COURSE = pathlib.Path(__file__).resolve().parents[1]
MODULES = [
    "m00-orientation", "m01-operating-system", "m02-ondevice-app", "m03-privacy-ship",
    "m04-spec-driven-saas", "m05-security-tests", "m06-expertise-product",
    "m07-monetize", "m08-launch-capstone",
]
LABEL = {m: f"M{int(m[1:3])}" for m in MODULES}

# The nine glossaries were written independently and use three entry shapes:
#   A.  **Term** — definition            (most modules; optional bullet prefix)
#   B.  **Term — definition start.**     (m02: the em dash sits inside the bold run)
#   C.  **Term.** definition             (m07: bold term phrase ending in a period)
PATTERNS = [
    re.compile(r"^\s*(?:[-*]\s*)?\*\*(?P<term>[^*]+?)\*\*\s*[—–-]\s*(?P<rest>.*)$"),
    re.compile(r"^\s*(?:[-*]\s*)?\*\*(?P<term>[^*]+?)\.\*\*\s*(?P<rest>.*)$"),
    re.compile(r"^\s*(?:[-*]\s*)?\*\*(?P<term>[^*]+?)\s*[—–-]\s*(?P<rest>.*?)\*\*\s*$"),
]


STOP_HEADING = re.compile(r"^#{1,6}\s*(curated\s+)?(resources?|further reading|keep reading|where to go next)\b", re.IGNORECASE)


def parse(path: pathlib.Path) -> list[tuple[str, str]]:
    """Return [(term, definition)] for one glossary file.

    Line-based, not block-based: the nine glossaries were written independently and some use tight
    bullet lists with no blank line between entries. A line matching a term pattern starts a new
    entry; following non-matching lines are appended to that entry's definition. Parsing stops at
    the curated-resources heading so links are not mistaken for terms.
    """
    found: list[tuple[str, str]] = []
    term: str | None = None
    body_parts: list[str] = []

    def flush() -> None:
        if term and body_parts:
            body = " ".join(body_parts).strip()
            if body:
                found.append((term, body))

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if STOP_HEADING.match(line):
            break
        if not line or line.startswith(("#", ">")):
            continue
        m = None
        for pat in PATTERNS:
            m = pat.match(line)
            if m:
                break
        if m:
            flush()
            term = m.group("term").strip().rstrip(".,;:")
            if re.search(r"\bvs\.?\b", term, re.IGNORECASE):
                term, body_parts = None, []      # confusion pairs stay module-local
                continue
            rest = m.group("rest").strip()
            body_parts = [rest] if rest else []
        elif term is not None:
            body_parts.append(line.lstrip("-* ").strip())
    flush()
    return found


def main() -> int:
    entries: dict[str, dict] = {}
    per_module: dict[str, int] = {}
    for mod in MODULES:
        path = COURSE / "03-content" / mod / "glossary.md"
        if not path.exists():
            print(f"! missing {path}")
            continue
        items = parse(path)
        per_module[mod] = len(items)
        for term, body in items:
            key = re.sub(r"[^a-z0-9]", "", term.lower())
            if key in entries:
                entries[key]["modules"].add(LABEL[mod])
                if len(body) > len(entries[key]["body"]):
                    entries[key]["body"] = body
                    entries[key]["term"] = term
            else:
                entries[key] = {"term": term, "body": body, "modules": {LABEL[mod]}}

    ordered = sorted(entries.values(), key=lambda e: e["term"].lower())
    shared = [e for e in ordered if len(e["modules"]) > 1]

    out: list[str] = [
        "# Master Glossary",
        "",
        "> Merged from the nine module glossaries by `build-glossary.py` (re-run it after editing any",
        "> module glossary). Duplicate terms keep the most detailed definition and list every module",
        "> that uses them. \"Where it lives\" pointers resolve in the cloned case-study repos.",
        "",
        f"**{len(ordered)} terms** across 9 modules · **{len(shared)} shared** by more than one module.",
        "",
        "| Module | Terms contributed |",
        "|---|---|",
    ]
    for mod in MODULES:
        if mod in per_module:
            out.append(f"| {LABEL[mod]} — {mod.split('-', 1)[1].replace('-', ' ')} | {per_module[mod]} |")
    out += [
        "",
        "## Shared vocabulary",
        "",
        "The terms the course leans on repeatedly — learn these once and they carry across modules.",
        "",
    ]
    for e in shared:
        mods = ", ".join(sorted(e["modules"]))
        out.append(f"- **{e['term']}** *({mods})* — {e['body']}")
    out += ["", "## All terms A–Z", ""]
    letter = None
    for e in ordered:
        first = e["term"][0].upper()
        if first != letter:
            letter = first
            out.append(f"### {letter}")
            out.append("")
        mods = ", ".join(sorted(e["modules"]))
        out.append(f"- **{e['term']}** *({mods})* — {e['body']}")
    out.append("")

    dest = COURSE / "06-production" / "glossary-master.md"
    dest.write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {dest.relative_to(COURSE)}: {len(ordered)} terms ({len(shared)} shared)")
    for mod, n in per_module.items():
        print(f"  {LABEL[mod]:>3}  {n:>2} terms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
