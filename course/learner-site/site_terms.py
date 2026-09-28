"""Terms explained where they are used (#term-links).

A learner who has never programmed meets words like Git, repository, API or agent on every page.
Each one's first use in a part — a Learn part, a lesson section, a lab step, a question — becomes a
link to its glossary entry, with a card that shows the plain meaning on hover or tap (terms.js).

Two sources, in both editions:
* the Basics glossary (`03-content/_basics/basics.json`): the everyday words of building software,
  each with a plain meaning and an everyday comparison;
* the page's own module glossary: its course concepts (tenant isolation, spec kit …), with the
  module glossary's definition.

The words themselves are never changed: a term is wrapped in a link, so narration text, search and
the read-aloud voice see the same sentence. Code, links, headings, figures, buttons and labels are
never touched.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent
BASICS = SITE.parent / "03-content" / "_basics" / "basics.json"

# Where a term is never linked: code, other links, headings, controls, figures, the page chrome.
SKIP_TAGS = {"pre", "code", "kbd", "a", "h1", "h2", "h3", "h4", "h5", "h6", "button", "label", "summary",
             "script", "style", "textarea", "svg", "nav", "header", "aside", "select", "option", "dt",
             "figcaption", "title", "noscript"}
SKIP_CLASS = re.compile(r'class="[^"]*\b(fig|fig-[\w-]+|sr-only|mode-tabs|learn-player|source-list|'
                        r'slide-source|exhibit[\w-]*|q-option|ladder-peek|evidence-form|page-kicker)\b')
# A new part starts here: the first use in it is linked again.
SCOPE = re.compile(r'<(?:section class="(?:learn-section|lab-step|qq|lab-section)|h2\b|h3\b)')
VOID = {"br", "img", "input", "meta", "link", "hr", "source", "wbr", "col", "area", "base", "path",
        "rect", "circle", "line", "polyline", "polygon", "use", "stop"}
TAG = re.compile(r"(<[^>]+>)")
TAG_NAME = re.compile(r"^<\s*(/?)\s*([a-zA-Z0-9]+)")


def basics() -> list[dict]:
    return json.loads(BASICS.read_text(encoding="utf-8"))["terms"]


def watch() -> list[str]:
    return json.loads(BASICS.read_text(encoding="utf-8")).get("watch", [])


def _clean(definition: str, limit: int = 220) -> str:
    """A module glossary definition as card text: its first sentence or two, no pointers or markup."""
    text = re.sub(r"\((?:[^()]*?/[^()]*?)\)", "", definition)          # (path/pointer; …)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\*\*?([^*]+)\*\*?", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > limit:
        cut = max(text.rfind(". ", 0, limit), text.rfind("。", 0, limit))
        text = text[:cut + 1] if cut > 60 else text[:limit].rstrip() + "…"
    return text


def entries(lang: str, deck_id: str | None, module_terms: list[dict], site_base: str) -> list[dict]:
    """Everything linkable on one page: {forms, title, plain, everyday, href, except}."""
    out = []
    glossary = f"{site_base}/glossary.html" if lang == "en" else "glossary.html"
    for t in basics():
        loc = t["zh"] if lang == "zh" else t
        forms = list(loc["match"])
        out.append({"forms": forms, "title": loc["term"], "plain": loc["plain"], "everyday": loc["everyday"],
                    "href": f"{glossary}#basics-{t['id']}", "except": t.get("except", [])})
    if deck_id:
        # the master glossary gives every term an anchor (module glossary pages are plain lists)
        page = glossary
        import site_content as SC                                                 # noqa: PLC0415
        for t in module_terms:
            name = t["term"]
            if " vs" in name.lower() or " / " in name or name.endswith(".md") or "`" in name:
                continue
            if lang == "zh":
                zh = re.split(r"[（(]", name)[0].strip()
                forms = [zh] if re.search(r"[一-鿿]", zh) else []
            else:
                forms = [re.sub(r"\s*\([^)]*\)\s*$", "", name).strip()]
            forms = [f for f in forms if len(f) >= 3]
            if forms:
                out.append({"forms": forms, "title": name, "plain": _clean(t["definition"]), "everyday": "",
                            "href": f"{page}#{SC.slug(name)}", "except": []})
    return out


def _pattern(form: str) -> str:
    body = re.escape(form).replace(r"\ ", r"[\s-]+")
    if re.search(r"[一-鿿]", form):
        return body
    return rf"(?<![\w-]){body}(?![\w-])"


class Linker:
    def __init__(self, items: list[dict]):
        self.items = items
        parts, self.owner = [], {}
        forms = sorted({(f, i) for i, it in enumerate(items) for f in it["forms"]}, key=lambda x: -len(x[0]))
        for n, (form, i) in enumerate(forms):
            flags = "" if re.search(r"[A-Z]", form) else "(?i:"
            group = f"t{n}"
            self.owner[group] = i
            pat = _pattern(form)
            parts.append(f"(?P<{group}>{flags}{pat}{')' if flags else ''})")
        self.rx = re.compile("|".join(parts)) if parts else None
        self.excepts = [[e.lower() for e in it["except"]] for it in items]

    def _card(self, i: int, word: str) -> str:
        it = self.items[i]
        attrs = (f' data-term-title="{html.escape(it["title"], quote=True)}"'
                 f' data-term-plain="{html.escape(it["plain"], quote=True)}"'
                 + (f' data-term-everyday="{html.escape(it["everyday"], quote=True)}"' if it["everyday"] else ""))
        return f'<a class="term" href="{html.escape(it["href"], quote=True)}"{attrs}>{word}</a>'

    def text(self, raw: str, seen: set[int]) -> str:
        """Link the first unseen term in a run of text (already HTML-escaped)."""
        if not self.rx:
            return raw
        out, pos = [], 0
        for m in self.rx.finditer(raw):
            i = self.owner[m.lastgroup]
            if i in seen:
                continue
            window = raw[max(0, m.start() - 30):m.end() + 30].lower()
            if any(e in window and _covers(window, e, raw[m.start():m.end()].lower()) for e in self.excepts[i]):
                continue
            seen.add(i)
            out.append(raw[pos:m.start()])
            out.append(self._card(i, m.group(0)))
            pos = m.end()
        out.append(raw[pos:])
        return "".join(out)

    def page(self, page: str) -> str:
        """Every term's first use in each part of `<main>`, linked."""
        start = page.find('<main id="content"')
        end = page.find("</main>", start)
        if start < 0 or end < 0:
            return page
        head, body, tail = page[:start], page[start:end], page[end:]
        out, stack, seen = [], [], set()
        for piece in TAG.split(body):
            if not piece:
                continue
            if piece.startswith("<"):
                if SCOPE.match(piece):
                    seen = set()
                m = TAG_NAME.match(piece)
                if m and not piece.startswith("<!"):
                    name = m.group(2).lower()
                    if m.group(1):                         # closing tag
                        while stack:
                            top = stack.pop()
                            if top[0] == name:
                                break
                    elif name not in VOID and not piece.endswith("/>"):
                        skip = name in SKIP_TAGS or bool(SKIP_CLASS.search(piece))
                        stack.append((name, skip))
                out.append(piece)
            elif any(s for _, s in stack):
                out.append(piece)
            else:
                out.append(self.text(piece, seen))
        return head + "".join(out) + tail


def _covers(window: str, phrase: str, word: str) -> bool:
    """Whether an `except` phrase in the window contains this occurrence of the word."""
    return word in phrase


def link_edition(folder: Path, lang: str, site_base: str, terms_by_deck: dict[str, list[dict]]) -> int:
    """Link terms on every module page and the Basics glossary's neighbours; returns links made."""
    made = 0
    deck_re = re.compile(r'data-deck="([a-z]\d+)"')
    for path in sorted(folder.glob("*.html")):
        if path.name.startswith(("glossary", "index", "paths", "path-", "proof", "evidence")):
            continue
        page = path.read_text(encoding="utf-8")
        m = deck_re.search(page)
        deck_id = m.group(1) if m else None
        linker = Linker(entries(lang, deck_id, terms_by_deck.get(deck_id, []) if deck_id else [], site_base))
        linked = linker.page(page)
        made += linked.count('class="term"') - page.count('class="term"')
        if linked != page:
            path.write_text(linked, encoding="utf-8")
    return made


def basics_section(lang: str) -> str:
    """The Basics glossary, at the top of the master glossary page."""
    rows = []
    for t in basics():
        loc = t["zh"] if lang == "zh" else t
        rows.append(f'<dt id="basics-{t["id"]}">{html.escape(loc["term"])}</dt>'
                    f'<dd>{html.escape(loc["plain"])} <em class="basics-everyday">{html.escape(loc["everyday"])}</em></dd>')
    title = "基础词汇" if lang == "zh" else "The basics"
    note = ("写给从没编程过的人：构建软件时最常见的词，用大白话解释。" if lang == "zh"
            else "For anyone who has never programmed: the everyday words of building software, in plain language.")
    return (f'<section class="glossary-letter glossary-basics" id="basics"><h2>{title}</h2>'
            f'<p class="section-note">{note}</p><dl>{"".join(rows)}</dl></section>')
