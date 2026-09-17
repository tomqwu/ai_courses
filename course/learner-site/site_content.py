"""The course text on the site: lessons, handouts, glossaries, labs and knowledge checks.

The decks are one slide at a time; this module renders the artifacts *underneath* them — the
lesson text the audit called "genuine method", the printable handout, the glossary, the lab with
its acceptance checklist, and the quiz as an interactive knowledge check — so a learner can read,
search and work without leaving the site.

Everything here is parsed from the module Markdown at build time. There is no runtime dependency
and no Markdown library: the subset the course uses is small (headings, paragraphs, lists including
checklists, tables, fenced code, quotes, rules, inline code/bold/italic/links) and a parser that
knows exactly that subset can also *refuse* what it does not understand — which is how the quiz
parser fails the build on a question with zero or two correct answers instead of shipping it.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

INLINE_CODE = re.compile(r"`([^`]+)`")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
ITALIC = re.compile(r"(?<![*\w])\*([^*\n]+)\*(?![*\w])")
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
POINTER = re.compile(r"^(ListenToMe|SignUpFlow|ai_qe|course)/([^\s:#`]+)(?::(\d+)(?:-(\d+))?)?$")
FENCE = re.compile(r"^```")
CHECK = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+(?:\[( |x|X)\]|(☐|☑))\s*(.*)$")

# The upstream heads the pointers were verified against (see 06-production/facts.json and the
# platform review). A pointer becomes a link to the file at that commit, so the link stays true
# even after upstream moves on.
PINNED = {
    "ListenToMe": "a9bde8e",
    "SignUpFlow": "c550d46",
    "ai_qe": "6388f0a",
    "course": "main",
}
GITHUB = "https://github.com/tomqwu"


def slug(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[^\w\s-]", "", html.unescape(text).lower())
    return re.sub(r"[\s_]+", "-", text).strip("-")[:80] or "section"


def pointer_link(raw: str) -> str | None:
    """`SignUpFlow/AGENTS.md:12-40` → a GitHub link at the pinned commit, or None."""
    m = POINTER.match(raw.strip())
    if not m:
        return None
    repo, path, start, end = m.group(1), m.group(2), m.group(3), m.group(4)
    if repo == "course":
        url = f"{GITHUB}/ai_courses/blob/{PINNED['course']}/course/{path}"
    else:
        url = f"{GITHUB}/{repo}/blob/{PINNED[repo]}/{path}"
    if start:
        url += f"#L{start}" + (f"-L{end}" if end else "")
    return url


def inline(text: str) -> str:
    """Escape, then re-introduce the inline subset; repo pointers in code spans become links."""
    out = html.escape(text, quote=False)

    def code(m: re.Match) -> str:
        body = m.group(1)
        link = pointer_link(html.unescape(body))
        if link:
            return f'<a class="pointer" href="{html.escape(link, quote=True)}" rel="noopener"><code>{body}</code></a>'
        return f"<code>{body}</code>"

    out = INLINE_CODE.sub(code, out)
    out = BOLD.sub(lambda m: f"<strong>{m.group(1)}</strong>", out)
    out = ITALIC.sub(lambda m: f"<em>{m.group(1)}</em>", out)
    out = LINK.sub(lambda m: f'<a href="{html.escape(m.group(2), quote=True)}">{m.group(1)}</a>', out)
    return out


# ---------------------------------------------------------------- document renderer

def _list_block(lines: list[str], i: int, checklist_ids: list[str] | None, prefix: str) -> tuple[str, int]:
    """Render a (possibly nested) list starting at line i; return (html, next_index)."""
    def indent(s: str) -> int:
        return len(s) - len(s.lstrip(" "))

    base = indent(lines[i])
    ordered = bool(re.match(r"^\s*\d+\.\s+", lines[i]))
    tag = "ol" if ordered else "ul"
    items: list[str] = []
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            # a blank line ends the list unless the next non-blank line is a deeper continuation
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and indent(lines[j]) > base and not re.match(r"^\s*(?:[-*+]|\d+\.)\s+", lines[j]):
                i = j
                continue
            break
        if indent(line) < base:
            break
        m = re.match(r"^(\s*)(?:[-*+]|\d+\.)\s+(.*)$", line)
        if m and indent(line) == base:
            body = m.group(2)
            i += 1
            # continuation lines and nested lists
            sub_html = ""
            cont: list[str] = []
            while i < len(lines):
                nxt = lines[i]
                if not nxt.strip():
                    # allow one blank inside an item only if followed by deeper indentation
                    j = i + 1
                    while j < len(lines) and not lines[j].strip():
                        j += 1
                    if j < len(lines) and indent(lines[j]) > base:
                        i = j
                        continue
                    break
                if indent(nxt) <= base:
                    break
                if re.match(r"^\s*(?:[-*+]|\d+\.)\s+", nxt):
                    if cont:
                        body += " " + " ".join(s.strip() for s in cont)
                        cont = []
                    inner, i = _list_block(lines, i, checklist_ids, prefix)
                    sub_html += inner
                    continue
                if FENCE.match(nxt.strip()):
                    if cont:
                        body += " " + " ".join(s.strip() for s in cont)
                        cont = []
                    code, i = _fence(lines, i)
                    sub_html += code
                    continue
                cont.append(nxt)
                i += 1
            if cont:
                body += " " + " ".join(s.strip() for s in cont)
            check = CHECK.match(f"- {body}")
            if check and checklist_ids is not None:
                text = check.group(3)
                cid = f"{prefix}-{len(checklist_ids) + 1}"
                checklist_ids.append(cid)
                items.append(f'<li class="check-item"><label><input type="checkbox" data-check="{cid}">'
                             f'<span>{inline(text)}</span></label>{sub_html}</li>')
            elif check:
                items.append(f'<li class="check-static">☐ {inline(check.group(3))}{sub_html}</li>')
            else:
                items.append(f"<li>{inline(body)}{sub_html}</li>")
        else:
            break
    return f"<{tag}>" + "".join(items) + f"</{tag}>", i


def _fence(lines: list[str], i: int) -> tuple[str, int]:
    lang = lines[i].strip()[3:].strip()
    body, i = [], i + 1
    while i < len(lines) and not FENCE.match(lines[i].strip()):
        body.append(lines[i])
        i += 1
    i += 1
    # trim common indentation (fences inside list items are indented)
    if body:
        pad = min((len(s) - len(s.lstrip(" ")) for s in body if s.strip()), default=0)
        body = [s[pad:] for s in body]
    code = html.escape("\n".join(body))
    cls = f' class="lang-{html.escape(lang)}"' if lang else ""
    return (f'<div class="codeblock"><button type="button" class="copy-code" data-copy '
            f'aria-label="Copy code">Copy</button><pre><code{cls}>{code}</code></pre></div>'), i


def render_document(text: str, checklist_prefix: str | None = None,
                    heading_offset: int = 0) -> tuple[str, list[dict], list[str]]:
    """Render a course Markdown document.

    Returns (html, headings, checklist_ids). Headings carry ids for the table of contents; when
    `checklist_prefix` is given, `- [ ]` and `1. ☐` items become persisted checkboxes.
    """
    lines = text.splitlines()
    out: list[str] = []
    headings: list[dict] = []
    checks: list[str] | None = [] if checklist_prefix else None
    i = 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        if FENCE.match(s):
            code, i = _fence(lines, i)
            out.append(code)
            continue
        if re.match(r"^(-{3,}|\*{3,})$", s):
            out.append("<hr>")
            i += 1
            continue
        if s.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            header = rows[0] if rows else []
            body = [r for r in rows[1:] if not all(set(c) <= set("-: ") for c in r)]
            t = ['<div class="table-wrap"><table>']
            if header:
                t.append("<thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in header) + "</tr></thead>")
            t.append("<tbody>" + "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
                                         for r in body) + "</tbody></table></div>")
            out.append("".join(t))
            continue
        if s.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            inner, _, _ = render_document("\n".join(quote))
            out.append(f"<blockquote>{inner}</blockquote>")
            continue
        if re.match(r"^\s*(?:[-*+]|\d+\.)\s+", line):
            block, i = _list_block(lines, i, checks, checklist_prefix or "c")
            out.append(block)
            continue
        h = re.match(r"^(#{1,6})\s+(.*)$", s)
        if h:
            level = min(6, len(h.group(1)) + heading_offset)
            title = h.group(2).strip()
            hid = slug(title)
            n = 2
            while any(x["id"] == hid for x in headings):
                hid = f"{slug(title)}-{n}"
                n += 1
            headings.append({"level": level, "id": hid, "text": re.sub(r"<[^>]+>", "", inline(title))})
            out.append(f'<h{level} id="{hid}">{inline(title)}</h{level}>')
            i += 1
            continue
        para = []
        while i < len(lines):
            nxt = lines[i].strip()
            if (not nxt or nxt.startswith(("|", ">", "#")) or FENCE.match(nxt)
                    or re.match(r"^\s*(?:[-*+]|\d+\.)\s+", lines[i]) or re.match(r"^(-{3,}|\*{3,})$", nxt)):
                break
            para.append(nxt)
            i += 1
        out.append("<p>" + inline(" ".join(para)) + "</p>")
    return "\n".join(out), headings, checks or []


def toc_html(headings: list[dict], min_level: int = 2, max_level: int = 3) -> str:
    items = [h for h in headings if min_level <= h["level"] <= max_level]
    if len(items) < 2:
        return ""
    lis = "".join(f'<li class="toc-l{h["level"]}"><a href="#{h["id"]}">{h["text"]}</a></li>' for h in items)
    return f'<nav class="toc" aria-label="On this page"><p class="toc-title">On this page</p><ol>{lis}</ol></nav>'


def split_title(text: str) -> tuple[str, str]:
    """Return (H1 title, body without the H1)."""
    m = re.match(r"^#\s+(.*)$", text.lstrip(), re.M)
    if not m:
        return "", text
    body = text.lstrip()[m.end():]
    return m.group(1).strip(), body


# ---------------------------------------------------------------- quiz parser

Q_START = re.compile(r"^(?:\*\*Q(\d+)\b([^*]*)\*\*\s*(.*)|###\s+Q(\d+)\b\s*(.*))$")
OPT = re.compile(r"^\s*(?:[-*]\s*)?\(?([a-dA-D])[).]\s+(.*)$")
KEY_LINES = [
    re.compile(r"^(?:[-*]\s*)?\*\*A(\d+):\s*([a-dA-D])\.?\*\*\s*(.*)$"),           # **A1: b.** …
    re.compile(r"^###\s+Q(\d+)\s*[—–-]+\s*([a-dA-D])\s*[—–-]+\s*(.*)$"),           # ### Q1 — b — …
    re.compile(r"^(?:[-*]\s*)?\*\*Q(\d+)\s*[—–-]+\s*([a-dA-D])\.?\*\*\s*(.*)$"),   # **Q1 — B.** … / - **Q1 — b.** …
    re.compile(r"^(?:[-*]\s*)?\*\*Q(\d+)\.?\s*[—–-]+\s*([a-dA-D])\.?\*\*\s*(.*)$"),
]
KEY_ROW = re.compile(r"^\|\s*(?:Q)?(\d+)\s*\|\s*([a-dA-D]|[—–-]|Model answer|Acceptable answer|—)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|$")
SHORT_KEY = [
    re.compile(r"^(?:[-*]\s*)?\*\*A(\d+)\.\*\*\s*(.*)$"),                           # **A7.** …
    re.compile(r"^(?:[-*]\s*)?\*\*Q(\d+)\s*[—–-]+\s*\*\*\s*(.*)$"),                  # - **Q7 —** …
    re.compile(r"^\*\*Q(\d+)\s*[—–-]+\s*(?:Acceptable|Model)[^*]*\*\*\s*(.*)$"),   # **Q7 — Acceptable answer:** …
    re.compile(r"^###\s+Q(\d+)\s*[—–-]+\s*(?:Model|Acceptable)[^—–-]*[—–-]+\s*(.*)$"),
    re.compile(r"^\*\*Q(\d+)\.?\s*\([^)]*\)\s*[—–-]+\s*(?:Acceptable|Model)[^*]*\*\*\s*(.*)$"),
]
SEGMENT = re.compile(r"\bM(\d+)\.(\d+)\b")


class QuizError(ValueError):
    pass


def parse_quiz(text: str, deck_id: str) -> dict:
    title, body = split_title(text)
    if "## Answer key" not in body:
        raise QuizError(f"{deck_id}: quiz has no '## Answer key' section")
    q_part, k_part = body.split("## Answer key", 1)
    questions: list[dict] = []
    cur: dict | None = None
    for raw in q_part.splitlines():
        m = Q_START.match(raw.strip())
        if m:
            n = int(m.group(1) or m.group(4))
            head = (m.group(2) or m.group(5) or "")
            stem = (m.group(3) or "").strip()
            cur = {"n": n, "head": head.strip(" ()."), "stem": [stem] if stem else [],
                   "options": [], "type": "mc"}
            if re.search(r"short", head, re.I):
                cur["type"] = "short"
            seg = SEGMENT.search(head)
            if seg:
                cur["segment"] = f"M{seg.group(1)}.{seg.group(2)}"
            questions.append(cur)
            continue
        if cur is None:
            continue
        o = OPT.match(raw)
        if o and cur["type"] == "mc" and not (cur["options"] == [] and cur["stem"] == []):
            cur["options"].append({"letter": o.group(1).lower(), "text": o.group(2).strip()})
            continue
        if raw.strip() == "---" or raw.strip().startswith("## "):
            continue
        if raw.strip():
            if cur["options"]:
                # text after the options belongs to the last option (a wrapped line)
                cur["options"][-1]["text"] += " " + raw.strip()
            else:
                cur["stem"].append(raw.rstrip())
        elif cur["stem"] and not cur["options"]:
            cur["stem"].append("")
    for q in questions:
        if q["type"] == "mc" and len(q["options"]) < 2:
            q["type"] = "short"
        q["stem_html"], _, _ = render_document("\n".join(q["stem"]).strip())
        q["stem_text"] = re.sub(r"<[^>]+>", "", q["stem_html"])

    keys: dict[int, dict] = {}
    current_key: int | None = None
    for raw in k_part.splitlines():
        s = raw.strip()
        matched = False
        row = KEY_ROW.match(s)
        if row:
            n = int(row.group(1))
            letter = row.group(2).strip().lower()
            answer = letter if re.fullmatch(r"[a-d]", letter) else None
            keys[n] = {"answer": answer, "rationale": (row.group(3) + " (" + row.group(4) + ")").strip()}
            current_key = None
            continue
        loose = re.match(r"^\|\s*(?:Q)?(\d+)\s*\|\s*(.*?)\s*\|?\s*$", s)
        if loose and not s.startswith("|---") and not re.match(r"^\|\s*Q\s*\|", s):
            n = int(loose.group(1))
            cells = [c.strip() for c in loose.group(2).split("|") if c.strip()]
            first = cells[0] if cells else ""
            answer = first.lower() if re.fullmatch(r"[a-dA-D]", first) else None
            rationale = " — ".join(cells[1:] if answer else cells)
            rationale = re.sub(r"^(?:Model answer|Model|Acceptable answer):\s*", "", rationale)
            keys[n] = {"answer": answer, "rationale": rationale}
            current_key = None
            continue
        for rx in KEY_LINES:
            m = rx.match(s)
            if m:
                n = int(m.group(1))
                keys[n] = {"answer": m.group(2).lower(), "rationale": m.group(3).strip()}
                current_key, matched = n, True
                break
        if matched:
            continue
        for rx in SHORT_KEY:
            m = rx.match(s)
            if m:
                n = int(m.group(1))
                keys[n] = {"answer": None, "rationale": m.group(2).strip()}
                current_key, matched = n, True
                break
        if matched:
            continue
        if current_key is not None and s and not s.startswith("#"):
            keys[current_key]["rationale"] += " " + s

    problems = []
    for q in questions:
        k = keys.get(q["n"])
        if not k:
            problems.append(f"Q{q['n']}: no answer-key entry")
            continue
        seg = SEGMENT.search(k["rationale"]) or (SEGMENT.search(q.get("head", "")) if q.get("head") else None)
        q["objective"] = q.get("segment") or (f"M{seg.group(1)}.{seg.group(2)}" if seg else "")
        q["rationale_html"] = inline(k["rationale"])
        if q["type"] == "mc":
            letters = [o["letter"] for o in q["options"]]
            if k["answer"] is None:
                problems.append(f"Q{q['n']}: multiple-choice question has no keyed letter")
            elif k["answer"] not in letters:
                problems.append(f"Q{q['n']}: keyed answer '{k['answer']}' is not one of {letters}")
            elif len(set(letters)) != len(letters):
                problems.append(f"Q{q['n']}: duplicate option letters {letters}")
            q["answer"] = k["answer"]
            for o in q["options"]:
                o["html"] = inline(o["text"])
        else:
            q["answer"] = None
    if len(questions) != 8:
        problems.append(f"expected 8 questions, parsed {len(questions)}")
    if problems:
        raise QuizError(f"{deck_id}/quiz.md: " + "; ".join(problems))
    return {"deck": deck_id, "title": title, "questions": questions,
            "mc": sum(1 for q in questions if q["type"] == "mc"),
            "short": sum(1 for q in questions if q["type"] == "short")}


# ---------------------------------------------------------------- lab parser

def parse_lab(text: str, deck_id: str) -> dict:
    """Split a lab into its sections and render them; the checklist becomes persisted boxes."""
    title, body = split_title(text)
    # the header quote block (Goal / Prerequisites / Time)
    meta = {}
    head_lines = []
    rest_lines = body.splitlines()
    while rest_lines and (not rest_lines[0].strip() or rest_lines[0].strip().startswith(">")):
        line = rest_lines.pop(0)
        if line.strip().startswith(">"):
            head_lines.append(re.sub(r"^\s*>\s?", "", line))
    head = " ".join(head_lines)
    for key in ("Goal", "Prerequisites", "Time"):
        m = re.search(rf"\*{{0,2}}{key[:-1] if key.endswith('s') else key}s?:?\*{{0,2}}\s*(.+?)(?=\s*(?:\*\*|·|\|)\s*(?:Goal|Prerequisites?|Time|Pass)|$)", head)
        if m:
            meta[key] = re.sub(r"\*+", "", m.group(1)).strip(" .—–-")
    body = "\n".join(rest_lines)

    # sections by ## heading
    sections: list[tuple[str, str]] = []
    cur_title, cur = "", []
    in_fence = False
    for line in body.splitlines():
        if FENCE.match(line.strip()):
            in_fence = not in_fence
        h = None if in_fence else re.match(r"^##\s+(.*)$", line.strip())
        if h:
            if cur_title or cur:
                sections.append((cur_title, "\n".join(cur)))
            cur_title, cur = h.group(1).strip(), []
        else:
            cur.append(line)
    if cur_title or cur:
        sections.append((cur_title, "\n".join(cur)))

    rendered = []
    checklist_ids: list[str] = []
    checklist_count = 0
    evidence_md = ""
    for sec_title, sec_body in sections:
        is_check = bool(re.search(r"checklist", sec_title, re.I))
        is_evidence = sec_title.lower().startswith("evidence")
        prefix = f"{deck_id}-lab" if is_check else None
        html_body, _, ids = render_document(sec_body, checklist_prefix=prefix, heading_offset=1)
        if is_check:
            checklist_ids += ids
            checklist_count += len(ids)
        if is_evidence:
            evidence_md = sec_body.strip()
        kind = "checklist" if is_check else ("evidence" if is_evidence else
                                            ("stretch" if sec_title.lower().startswith("stretch") else
                                             ("discussion" if sec_title.lower().startswith("discussion") else "body")))
        rendered.append({"title": sec_title, "html": html_body, "kind": kind})
    return {"deck": deck_id, "title": title, "meta": meta, "sections": rendered,
            "checklist_ids": checklist_ids, "checklist_count": checklist_count,
            "evidence_md": evidence_md}


# ---------------------------------------------------------------- glossary parser

TERMS = [
    re.compile(r"^(?:[-*]\s*)?\*\*(.+?)\*\*\s*[—–-]+\s*(.*)$"),        # **Term** — definition
    re.compile(r"^(?:[-*]\s*)?\*\*([^—–]+?)\s+[—–]\s+(.+?)\*\*\s*(.*)$"),  # **Term — definition.** more
    re.compile(r"^(?:[-*]\s*)?\*\*([^*]+?)\.\*\*\s+(.*)$"),           # **Term.** definition
]


def parse_glossary(text: str) -> list[dict]:
    """Terms in `**Term** — definition — pointer` form, for the search index and the glossary page."""
    title, body = split_title(text)
    terms = []
    cur = None
    for line in body.splitlines():
        m = next((mm for rx in TERMS if (mm := rx.match(line.strip()))), None)
        if m:
            groups = m.groups()
            definition = " ".join(g.strip() for g in groups[1:] if g).strip()
            cur = {"term": groups[0].strip().strip("`"), "definition": definition}
            terms.append(cur)
        elif cur and line.strip() and not line.strip().startswith("#"):
            cur["definition"] += " " + line.strip()
        else:
            cur = None
    return terms


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")
