#!/usr/bin/env python3
"""The Chinese edition's sources, held to the English ones (#121).

    python3 zh_edition.py sentences m05      # the English narration, one sentence per row (JSON)
    python3 zh_edition.py check m05 m06      # parity of those modules' Chinese sources
    python3 zh_edition.py check              # every module
    python3 zh_edition.py stamp m05          # record that m05's Chinese matches its English as it is now

The Chinese edition is the same course in Chinese: the same parts in the same order, the same
exhibits (byte for byte — they are copies of real files), the same pointers, the same steps,
checklist items, questions and answer keys. Only the words a learner reads change. This checks
that, so a translation can never drop a part, alter a code block or re-key a quiz; the rules the
translator follows are in course/01-design/zh-translation-guide.md.

Sources: `course/03-content/mNN-*/zh/{slides,lesson,handout,glossary,lab,quiz,lab-rubrics}.md`
and `course/06-production/narration/scripts-zh/mNN.json` (`sentences`: one Chinese sentence per
English sentence, so the English recording can mark the Chinese sentence it is speaking).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

COURSE = Path(__file__).resolve().parents[1]
CONTENT = COURSE / "03-content"
SCRIPTS = COURSE / "06-production" / "narration" / "scripts"
SCRIPTS_ZH = COURSE / "06-production" / "narration" / "scripts-zh"
for extra in (COURSE / "learner-site", COURSE / "06-production" / "narration",
              COURSE / "06-production" / "slides"):
    sys.path.insert(0, str(extra))

FILES = ("slides", "lesson", "handout", "glossary", "lab", "quiz", "lab-rubrics")
# The English each Chinese source was translated from, by hash: an English edit that is not carried
# into the Chinese fails the check until the Chinese is updated and the module is stamped again.
STAMPS = COURSE / "06-production" / "zh-sources.json"


def _sha(path: Path) -> str:
    import hashlib                                                                 # noqa: PLC0415
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def english_sources(deck_id: str) -> dict[str, Path]:
    folder = module_dir(deck_id)
    out = {f"{folder.name}/{n}.md": folder / f"{n}.md" for n in FILES}
    out[f"scripts/{deck_id}.json"] = SCRIPTS / f"{deck_id}.json"
    return out


def stamp(deck_id: str) -> None:
    data = json.loads(STAMPS.read_text(encoding="utf-8")) if STAMPS.is_file() else {}
    data.update({k: _sha(p) for k, p in english_sources(deck_id).items()})
    STAMPS.write_text(json.dumps(dict(sorted(data.items())), indent=1) + "\n", encoding="utf-8")


def check_stamps(deck_id: str, required: bool = False) -> list[str]:
    """Stale Chinese. A module that was never stamped is a translation in progress: only the gate
    (`required`) holds it to having a stamp at all."""
    data = json.loads(STAMPS.read_text(encoding="utf-8")) if STAMPS.is_file() else {}
    if not any(k in data for k in english_sources(deck_id)):
        return [f"not stamped — `zh_edition.py stamp {deck_id}` once its Chinese is reviewed"] if required else []
    stale = [k for k, p in english_sources(deck_id).items() if data.get(k) != _sha(p)]
    return [f"the English {k} changed since the Chinese was stamped — carry the change into the "
            f"Chinese, then `zh_edition.py stamp {deck_id}`" for k in stale]
FENCE = re.compile(r"^```(.*)$")
POINTER = re.compile(r"\b(?:ListenToMe|SignUpFlow|ai_qe|course)/[^\s`'\"),;<>（）。，]+")
CJK = re.compile(r"[一-鿿]")
LINE_WORDS = re.compile(r"第\s*\d+\s*行|\bline\s+\d+", re.I)


def module_dir(deck_id: str) -> Path:
    return sorted(CONTENT.glob(f"{deck_id}-*"))[0]


def modules() -> list[str]:
    from narration_data import DECK_IDS                                          # noqa: PLC0415
    return list(DECK_IDS)


def en_sentences(deck_id: str) -> dict[str, list[str]]:
    """The English narration as the site splits it: what each Chinese sentence answers to."""
    import build_site as B                                                         # noqa: PLC0415
    script = json.loads((SCRIPTS / f"{deck_id}.json").read_text(encoding="utf-8"))
    return {k: B.sentences(v["text"]) for k, v in script["slides"].items()}


def fences(text: str) -> list[tuple[str, str]]:
    """Every fenced block: (info string, body). Figure fences are returned too, marked."""
    out, cur, info = [], None, ""
    for line in text.splitlines():
        m = FENCE.match(line.strip()) if not line.startswith("    ") else None
        if m and cur is None:
            cur, info = [], m.group(1).strip()
        elif m and cur is not None and not m.group(1).strip():
            out.append((info, "\n".join(cur)))
            cur = None
        elif cur is not None:
            cur.append(line)
    return out


def code_blocks(text: str) -> list[str]:
    return [f"```{info}\n{body}" for info, body in fences(text) if info.split()[:1] != ["figure"]]


def figure_blocks(text: str) -> list[str]:
    return [body for info, body in fences(text) if info.split()[:1] == ["figure"]]


def pointers(text: str) -> list[str]:
    return sorted(set(p.rstrip(".:") for p in POINTER.findall(text)))


def outside_fences(text: str) -> str:
    keep, inside = [], False
    for line in text.splitlines():
        if FENCE.match(line.strip()):
            inside = not inside
            continue
        if not inside:
            keep.append(line)
    return "\n".join(keep)


def _figure_shape(body: str) -> dict:
    import figures as F                                                            # noqa: PLC0415
    fig = F.parse(body)
    return {"kind": fig["kind"], "image": fig["image"], "scene": fig["scene"], "source": fig["source"],
            "items": [(sorted(i["flags"]), [(c.get("id"), sorted(c["flags"])) for c in i["children"]])
                      for i in fig["items"]],
            "edges": [(e["from"], e["to"], sorted(e["flags"])) for e in fig.get("edges", [])],
            "loop": fig["loop"], "callouts": len(fig["callouts"])}


def check_slides(deck_id: str, en: str, zh: str) -> list[str]:
    from deck_lint import split_slides                                             # noqa: PLC0415
    import figures as F                                                            # noqa: PLC0415
    problems = []
    front_en, s_en = split_slides(en)
    front_zh, s_zh = split_slides(zh)
    if len(s_en) != len(s_zh):
        return [f"slides: {len(s_zh)} parts, the English has {len(s_en)}"]
    if not re.match(rf"^M{int(deck_id[1:])}\s*—\s*\S", front_zh.get("title", "")):
        problems.append(f"slides: front-matter title must read `M{int(deck_id[1:])} — <Chinese title>`")
    said = load_zh_sentences(deck_id)
    directive = re.compile(r"<!--\s*(_class|_diagram|_paginate|_header|_footer)\s*:\s*([^>]*?)\s*-->")
    for n, (a, b) in enumerate(zip(s_en, s_zh), 1):
        where = f"slides part {n}"
        if directive.findall(a) != directive.findall(b):
            problems.append(f"{where}: directives differ (keep every `<!-- _class/_diagram … -->` as written)")
        if bool(re.search(r"<!--\s*NOTES:", a)) != bool(re.search(r"<!--\s*NOTES:", b)):
            problems.append(f"{where}: the NOTES comment is missing or extra")
        if code_blocks(a) != code_blocks(b):
            problems.append(f"{where}: a code block differs from the English (copy exhibits byte for byte)")
        if pointers(a) != pointers(b):
            problems.append(f"{where}: pointers differ: {sorted(set(pointers(a)) ^ set(pointers(b)))[:4]}")
        fa, fb = figure_blocks(a), figure_blocks(b)
        if len(fa) != len(fb):
            problems.append(f"{where}: {len(fb)} figures, the English has {len(fa)}")
            continue
        for fig_a, fig_b in zip(fa, fb):
            try:
                if _figure_shape(fig_a) != _figure_shape(fig_b):
                    problems.append(f"{where}: the figure's shape differs (same kind, parts, ids, flags, edges)")
                fig = F.parse(fig_b)
            except F.FigureError as exc:
                problems.append(f"{where}: figure: {exc}")
                continue
            parts = [p for item in fig["items"] for p in (item, *item["children"])] + fig.get("edges", [])
            for p in parts:
                if p["at"] and F.step_index(p["at"], said.get(f"slide-{n}", [])) is None:
                    problems.append(f"{where}: figure `@ {p['at']}` opens no sentence of the Chinese narration")
    return problems


def load_zh_sentences(deck_id: str) -> dict[str, list[str]]:
    path = SCRIPTS_ZH / f"{deck_id}.json"
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {k: v.get("sentences", []) for k, v in data.get("slides", {}).items()}


def check_narration(deck_id: str) -> list[str]:
    path = SCRIPTS_ZH / f"{deck_id}.json"
    if not path.is_file():
        return [f"narration: {path.relative_to(COURSE)} is missing"]
    data = json.loads(path.read_text(encoding="utf-8"))
    problems = []
    if not re.match(rf"^M{int(deck_id[1:])}\s*—\s*\S", data.get("label", "")):
        problems.append("narration: label must read `M<n> — <Chinese title>`")
    en = en_sentences(deck_id)
    zh = data.get("slides", {})
    if sorted(en) != sorted(zh):
        problems.append(f"narration: parts differ: {sorted(set(en) ^ set(zh))[:5]}")
    for key, rows in en.items():
        mine = zh.get(key, {})
        got = mine.get("sentences", [])
        if not mine.get("title") or not CJK.search(mine.get("title", "")):
            problems.append(f"narration {key}: no Chinese title")
        if len(got) != len(rows):
            problems.append(f"narration {key}: {len(got)} sentences, the English has {len(rows)} "
                            "(one Chinese sentence per English sentence)")
        for i, s in enumerate(got):
            if not CJK.search(s):
                problems.append(f"narration {key} sentence {i + 1}: not Chinese")
            if LINE_WORDS.search(s):
                problems.append(f"narration {key} sentence {i + 1}: speaks a line number")
    return problems


def check_document(kind: str, en: str, zh: str) -> list[str]:
    problems = []
    if code_blocks(en) != code_blocks(zh):
        ea, za = code_blocks(en), code_blocks(zh)
        first = next((i for i, (x, y) in enumerate(zip(ea, za)) if x != y), min(len(ea), len(za)))
        problems.append(f"{kind}: code block {first + 1} differs from the English "
                        f"({len(za)} blocks, the English has {len(ea)}); copy code byte for byte")
    if pointers(en) != pointers(zh):
        problems.append(f"{kind}: pointers differ: {sorted(set(pointers(en)) ^ set(pointers(zh)))[:4]}")
    heads = lambda t: [len(m.group(1)) for m in re.finditer(r"^(#{1,4})\s", outside_fences(t), re.M)]
    if heads(en) != heads(zh):
        problems.append(f"{kind}: heading structure differs ({len(heads(zh))} headings, the English has {len(heads(en))})")
    seg = lambda t: re.findall(r"^#{2,3}\s+(?:Segment\s+)?(M\d+\.\d+)\b", t, re.M)
    if seg(en) != seg(zh):
        problems.append(f"{kind}: segment headings must keep their ids (`## M5.1 — …`)")
    if len(CJK.findall(outside_fences(zh))) < 50:
        problems.append(f"{kind}: this does not read as Chinese")
    return problems


def check_module(deck_id: str, required: bool = False) -> list[str]:
    import site_content as SC                                                      # noqa: PLC0415
    folder = module_dir(deck_id)
    zh_dir = folder / "zh"
    problems = []
    for name in FILES:
        if not (zh_dir / f"{name}.md").is_file():
            problems.append(f"{name}.md: missing in {zh_dir.relative_to(COURSE)}/")
    problems += check_narration(deck_id)
    if problems and any("missing" in p for p in problems):
        return problems
    problems += check_stamps(deck_id, required)
    read = lambda d, n: (d / f"{n}.md").read_text(encoding="utf-8")
    problems += check_slides(deck_id, read(folder, "slides"), read(zh_dir, "slides"))
    for kind in ("lesson", "handout", "lab"):
        problems += check_document(kind, read(folder, kind), read(zh_dir, kind))
    # glossary: the same terms, each named in Chinese with its English in brackets
    g_en = SC.parse_glossary(read(folder, "glossary"))
    g_zh = SC.parse_glossary(read(zh_dir, "glossary"))
    if len(g_en) != len(g_zh):
        problems.append(f"glossary: {len(g_zh)} terms, the English has {len(g_en)}")
    for a, b in zip(g_en, g_zh):
        if a["term"].lower() not in b["term"].lower() or not CJK.search(b["term"]):
            problems.append(f"glossary: `{b['term']}` must be the Chinese name with `（{a['term']}）`")
    # lab: the same steps and checklist
    l_en, l_zh = SC.parse_lab(read(folder, "lab"), deck_id), SC.parse_lab(read(zh_dir, "lab"), deck_id)
    if len(l_en["sections"]) != len(l_zh["sections"]):
        problems.append(f"lab: {len(l_zh['sections'])} sections, the English has {len(l_en['sections'])}")
    if l_en["checklist_count"] != l_zh["checklist_count"]:
        problems.append(f"lab: {l_zh['checklist_count']} checklist items, the English has {l_en['checklist_count']}")
    # quiz: the same questions, kinds, options, keys and objectives
    try:
        q_en, q_zh = SC.parse_quiz(read(folder, "quiz"), deck_id), SC.parse_quiz(read(zh_dir, "quiz"), deck_id)
    except SC.QuizError as exc:
        problems.append(f"quiz: {exc}")
    else:
        shape = lambda q: [(x["n"], x["type"], len(x["options"]), x["answer"], x["objective"]) for x in q["questions"]]
        if shape(q_en) != shape(q_zh):
            problems.append("quiz: questions, kinds, options, answer keys or objectives differ from the English")
        for x in q_zh["questions"]:
            if not CJK.search(x["stem_text"]):
                problems.append(f"quiz Q{x['n']}: the stem is not Chinese")
    # the rubric's auto-fail list (the only part of it the site shows)
    a_en = SC.parse_auto_fail(read(folder, "lab-rubrics"))
    a_zh = SC.parse_auto_fail(read(zh_dir, "lab-rubrics"))
    if bool(a_en) != bool(a_zh):
        problems.append("lab-rubrics: the `## 自动不通过` (auto-fail) section is missing")
    elif a_en and a_en["html"].count("<li") != a_zh["html"].count("<li"):
        problems.append("lab-rubrics: the auto-fail list has a different number of items")
    return problems


def main(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[0] == "sentences":
        print(json.dumps(en_sentences(argv[1]), ensure_ascii=False, indent=1))
        return 0
    if argv and argv[0] == "stamp":
        for deck_id in argv[1:] or modules():
            problems = [p for p in check_module(deck_id) if "stamped" not in p]
            if problems:
                print(f"{deck_id}: not stamped — fix these first:")
                for p in problems:
                    print("    " + p)
                return 1
            stamp(deck_id)
            print(f"{deck_id}: stamped")
        return 0
    if argv and argv[0] == "check":
        which = argv[1:] or modules()
        failed = 0
        for deck_id in which:
            problems = check_module(deck_id)
            print(f"[{'PASS' if not problems else f'FAIL ({len(problems)})'}] {deck_id}")
            for p in problems[:40]:
                print("    " + p)
            failed += len(problems)
        return 1 if failed else 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
