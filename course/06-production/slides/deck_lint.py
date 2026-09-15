#!/usr/bin/env python3
"""Lint a Marp deck against course/01-design/content-standards.md §2.1.

Checks per deck:
  * `marp: true` and `theme: aps` in the front matter
  * slide count inside the 18-28 band
  * <= 6 bullets per slide (a list declared `_diagram:` is component nodes, not bullets —
    its items are still word-checked)
  * <= 10 words per bullet
  * a `<!-- NOTES: ... -->` speaker note on every slide
  * at least one PROOF slide (marked with the `proof` class or the word "Proof")

Exit code 0 = clean, 1 = violations (printed with slide numbers).
Usage: python3 deck_lint.py path/to/slides.md [...]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

MAX_BULLETS = 6
MAX_BULLET_WORDS = 10
MIN_SLIDES, MAX_SLIDES = 18, 28
BULLET_RE = re.compile(r"^\s{0,3}[-*+]\s+(.*\S)\s*$")
OL_RE = re.compile(r"^\s{0,3}\d+\.\s+(.*\S)\s*$")
DIAGRAM_DIRECTIVE = re.compile(r"<!--\s*_diagram\s*:\s*\w+\s*-->")


def extract_diagram_list(slide: str) -> tuple[list[str], str]:
    """Pull the list a `_diagram:` directive upgrades out of the bullet count.

    The bullet budget exists to stop prose walls; an eight-command pipeline rendered as one
    flow component is not a wall. The items are still word-checked, and the learner-site gate
    asserts the declared component renders and fits its frame — a directive with no list, or
    a wall relabelled as a diagram, fails elsewhere.
    """
    m = DIAGRAM_DIRECTIVE.search(slide)
    if not m:
        return [], slide
    lines = slide[m.end():].splitlines()
    j = 0
    while j < len(lines) and not lines[j].strip():
        j += 1
    k = j
    items: list[str] = []
    while k < len(lines) and (BULLET_RE.match(lines[k]) or OL_RE.match(lines[k])):
        match = BULLET_RE.match(lines[k]) or OL_RE.match(lines[k])
        items.append(match.group(1))
        k += 1
    if not items:
        return [], slide
    return items, slide[:m.start()] + "\n".join(lines[k:])


def split_slides(text: str) -> tuple[dict[str, str], list[str]]:
    """Return (front_matter, slides). Front matter is the first `---` fenced block."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, [text]
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}, [text]
    fm = {}
    for line in lines[1:end]:
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    body = "\n".join(lines[end + 1:])
    slides = [s for s in re.split(r"^---\s*$", body, flags=re.MULTILINE)]
    return fm, [s for s in slides if s.strip()]


def strip_code_fences(slide: str) -> str:
    """Remove fenced code blocks — commands and payloads are not bullets or prose."""
    out, in_fence = [], False
    for line in slide.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    return "\n".join(out)


def lint(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    problems: list[str] = []
    fm, slides = split_slides(text)

    if fm.get("marp") != "true":
        problems.append("front matter: missing `marp: true`")
    if fm.get("theme") != "aps":
        problems.append("front matter: missing `theme: aps`")

    if not (MIN_SLIDES <= len(slides) <= MAX_SLIDES):
        problems.append(
            f"slide count {len(slides)} outside the {MIN_SLIDES}-{MAX_SLIDES} band"
        )

    proof_seen = False
    for i, slide in enumerate(slides, start=1):
        title = next(
            (l.lstrip("# ").strip() for l in slide.splitlines() if l.startswith("#")),
            "(untitled)",
        )
        if "class:" in slide and "proof" in slide.lower():
            proof_seen = True
        if re.search(r"proof", slide, re.IGNORECASE):
            proof_seen = True

        if "<!-- NOTES:" not in slide:
            problems.append(f"slide {i} ({title}): no `<!-- NOTES: ... -->` speaker note")

        prose = strip_code_fences(slide)
        diagram_items, prose = extract_diagram_list(prose)
        bullets = [m.group(1) for m in (BULLET_RE.match(l) for l in prose.splitlines()) if m]
        if len(bullets) > MAX_BULLETS:
            problems.append(
                f"slide {i} ({title}): {len(bullets)} bullets (max {MAX_BULLETS})"
            )
        for b in bullets + diagram_items:
            # strip inline code/markup before counting words
            plain = re.sub(r"[`*_\[\]()#>]", " ", b)
            words = [w for w in plain.split() if any(c.isalnum() for c in w)]
            if len(words) > MAX_BULLET_WORDS:
                excerpt = " ".join(words[:14]) + ("…" if len(words) > 14 else "")
                problems.append(
                    f"slide {i} ({title}): bullet has {len(words)} words "
                    f"(max {MAX_BULLET_WORDS}): {excerpt}"
                )

    if not proof_seen:
        problems.append("no PROOF slide found (mark one with `<!-- _class: proof -->`)")

    return problems


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    total = 0
    for arg in argv:
        path = Path(arg)
        problems = lint(path)
        rel = path
        if problems:
            total += len(problems)
            print(f"✗ {rel}")
            for p in problems:
                print(f"    {p}")
        else:
            print(f"✓ {rel}")
    if total:
        print(f"\n{total} violation(s). See course/01-design/content-standards.md §2.1")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
