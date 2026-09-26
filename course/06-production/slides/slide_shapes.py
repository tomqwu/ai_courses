#!/usr/bin/env python3
"""Measure what shape each slide's content is in, so "the decks read thin" stops being an opinion.

A slide can carry a bullet list, a table, code, a declared diagram, an image, a quote or a pull
figure. The audit that started this found 79% of slides carried a bullet list and 61% were *exactly*
a heading plus one bullet list — not because the material was thin, but because the display language
was. This measures both shares, per deck and overall, so a content pass can be aimed and then shown
to have landed.

    python3 slide_shapes.py ../../03-content/*/slides.md
    python3 slide_shapes.py --max-bullet-only 0.5 ../../03-content/*/slides.md   # fail above 50%
    python3 slide_shapes.py --json ../../03-content/m03-privacy-ship/slides.md
    python3 slide_shapes.py --list-bullet-only ../../03-content/*/slides.md      # what to work on

Bullet-only means the body is one list and nothing else. A slide whose list is declared `_diagram:`
is a diagram, not a bullet list — the words are the same, the display is not, which is exactly the
distinction being measured. Standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

NOTES_RE = re.compile(r"<!--\s*NOTES:.*?-->", re.S)
DIRECTIVE_RE = re.compile(r"<!--\s*_[a-z]+\s*:.*?-->", re.S)
DIAGRAM_RE = re.compile(r"<!--\s*_diagram\s*:\s*(\w+)\s*-->")
CLASS_RE = re.compile(r"<!--\s*_class\s*:\s*([^-]+?)\s*-->")
BULLET_RE = re.compile(r"^\s{0,3}(?:[-*+]|\d+[.)])\s+\S")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+")
TABLE_RE = re.compile(r"^\s*\|.*\|\s*$")


def split_slides(text: str) -> list[str]:
    """Marp slides are separated by `---` at column 0; the first block is front matter."""
    blocks = re.split(r"(?m)^---\s*$", text)
    return [b for b in blocks[2:] if b.strip()] if text.lstrip().startswith("---") else \
           [b for b in blocks if b.strip()]


def shape_of(slide: str) -> set[str]:
    """Which display elements the slide body uses, ignoring narration and directives."""
    diagram = DIAGRAM_RE.search(slide)
    klass = CLASS_RE.search(slide)
    body = DIRECTIVE_RE.sub("", NOTES_RE.sub("", slide))
    kinds: set[str] = set()
    if diagram:
        kinds.add(f"diagram:{diagram.group(1)}")
    if klass:
        for name in klass.group(1).split():
            if name in {"metrics", "pillars", "takeaway", "quote", "proof", "cover", "section"}:
                kinds.add(f"class:{name}")
    in_fence = False
    saw_list = saw_table = saw_prose = saw_image = saw_quote = False
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            if in_fence:
                kinds.add("code")
            continue
        if in_fence or not stripped or HEADING_RE.match(line):
            continue
        if stripped.startswith("!["):
            saw_image = True
        elif TABLE_RE.match(line):
            saw_table = True
        elif BULLET_RE.match(line):
            saw_list = True
        elif stripped.startswith(">"):
            saw_quote = True
        elif not stripped.startswith("<"):
            saw_prose = True
    # A list the directive upgraded is the diagram's nodes, not a bullet list.
    if saw_list and not diagram:
        kinds.add("list")
    for flag, name in ((saw_table, "table"), (saw_image, "image"), (saw_quote, "quote"),
                       (saw_prose, "prose")):
        if flag:
            kinds.add(name)
    return kinds or {"heading-only"}


def measure(paths: list[Path]) -> dict:
    decks = []
    for path in paths:
        slides = split_slides(path.read_text(encoding="utf-8"))
        rows = []
        for number, slide in enumerate(slides, 1):
            kinds = shape_of(slide)
            title_match = re.search(r"(?m)^#{1,6}\s+(.*\S)\s*$", NOTES_RE.sub("", slide))
            rows.append({
                "slide": number,
                "title": title_match.group(1)[:60] if title_match else "",
                "kinds": sorted(kinds),
                "bullet_only": kinds == {"list"},
                "has_list": "list" in kinds,
            })
        decks.append({"deck": path.parent.name, "path": str(path), "slides": rows})
    total = sum(len(d["slides"]) for d in decks)
    bullet_only = sum(1 for d in decks for s in d["slides"] if s["bullet_only"])
    with_list = sum(1 for d in decks for s in d["slides"] if s["has_list"])
    histogram: dict[str, int] = {}
    for deck in decks:
        for slide in deck["slides"]:
            for kind in slide["kinds"]:
                histogram[kind] = histogram.get(kind, 0) + 1
    return {"decks": decks, "total": total, "bullet_only": bullet_only, "with_list": with_list,
            "bullet_only_share": round(bullet_only / total, 4) if total else 0.0,
            "with_list_share": round(with_list / total, 4) if total else 0.0,
            "histogram": dict(sorted(histogram.items(), key=lambda kv: -kv[1]))}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("decks", nargs="+", help="slides.md files")
    parser.add_argument("--max-bullet-only", type=float, default=None,
                        help="exit 1 when the bullet-only share is above this (e.g. 0.5)")
    parser.add_argument("--list-bullet-only", action="store_true", help="print every bullet-only slide")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    paths = [Path(p) for p in args.decks]
    for path in paths:
        if not path.is_file():
            print(f"slide_shapes: no such deck: {path}", file=sys.stderr)
            return 2
    report = measure(paths)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"{'deck':<26} {'slides':>6} {'bullet-only':>12} {'with a list':>12}")
        for deck in report["decks"]:
            slides = deck["slides"]
            only = sum(1 for s in slides if s["bullet_only"])
            lists = sum(1 for s in slides if s["has_list"])
            print(f"{deck['deck'][:25]:<26} {len(slides):>6} "
                  f"{only:>5} ({only / len(slides) * 100:>3.0f}%) {lists:>5} ({lists / len(slides) * 100:>3.0f}%)")
        print(f"{'ALL':<26} {report['total']:>6} "
              f"{report['bullet_only']:>5} ({report['bullet_only_share'] * 100:>3.0f}%) "
              f"{report['with_list']:>5} ({report['with_list_share'] * 100:>3.0f}%)")
        print("\nshapes: " + " · ".join(f"{k} {v}" for k, v in report["histogram"].items()))
        if args.list_bullet_only:
            print("\nbullet-only slides:")
            for deck in report["decks"]:
                for slide in deck["slides"]:
                    if slide["bullet_only"]:
                        print(f"  {deck['deck']:<24} {slide['slide']:>3}  {slide['title']}")
    if args.max_bullet_only is not None and report["bullet_only_share"] > args.max_bullet_only:
        print(f"\nFAILED: {report['bullet_only_share'] * 100:.0f}% of slides are a heading plus one "
              f"bullet list, above the {args.max_bullet_only * 100:.0f}% ceiling")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
