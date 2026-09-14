#!/usr/bin/env python3
"""Lint a Marp deck against course/01-design/content-standards.md §2.1.

Checks per deck:
  * `marp: true` and `theme: aps` in the front matter
  * slide count inside the 18-28 band
  * <= 6 bullets per slide
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
        bullets = [m.group(1) for m in (BULLET_RE.match(l) for l in prose.splitlines()) if m]
        if len(bullets) > MAX_BULLETS:
            problems.append(
                f"slide {i} ({title}): {len(bullets)} bullets (max {MAX_BULLETS})"
            )
        for b in bullets:
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
