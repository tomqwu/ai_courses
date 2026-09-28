"""Page templates for the course text: lesson, handout, glossary, lab and knowledge check.

Every page is rendered in the app shell (`site_shell`, #73): the course outline, the top bar with the
module's four modes, and the page title in the content column — so a learner can move between the
deck, the lesson, the lab and the knowledge check of one module without losing their place.
Progress is read by `progress.js` on every page.
"""
from __future__ import annotations

import html
import json
import re

import site_content as SC
import site_shell as SH

KIND_TITLES = {
    "lesson": "Lesson", "handout": "Handout", "glossary": "Glossary",
    "lab": "Lab", "quiz": "Knowledge check", "deck": "Deck", "transcript": "Transcript",
}


def source_path(deck: dict, kind: str) -> str:
    """The Markdown a page is built from, in its edition: `…/m05-…/lab.md` or `…/m05-…/zh/lab.md`."""
    folder = deck["source"].split("/")[1]
    return html.escape(f"course/03-content/{folder}/{'zh/' if deck.get('lang') == 'zh' else ''}{kind}.md")


def read_views(deck_id: str, site_base: str, active: str) -> str:
    """Read is one mode with three views (#74): the lesson, its one-page handout, and its glossary.

    They keep their own URLs, so every link into them — search hits, the master glossary, lessons,
    certificates — still resolves; what changed is that they are views of Read, not tabs beside it.
    """
    items = (("lesson", "Lesson", f"lesson-{deck_id}.html"),
             ("handout", "Handout", f"handout-{deck_id}.html"),
             ("glossary", "Glossary", f"glossary-{deck_id}.html"))
    current = ' aria-current="page"'
    links = "".join(f'<a href="{site_base}/{href}"{current if key == active else ""}>{label}</a>'
                    for key, label, href in items)
    return f'<nav class="view-tabs" aria-label="Read">{links}</nav>'




def short_label(deck: dict) -> str:
    return re.sub(r"^M\d+\s*—\s*", "", deck["label"]).strip()


# ---------------------------------------------------------------- reading pages

def document_page(deck: dict, kind: str, text: str, site_base: str, brand: str,
                  segment_figures: dict[str, str] | None = None) -> tuple[str, dict]:
    """Lesson, handout or glossary as a reading page. Returns (html, index_record).

    `segment_figures` (unit id → figure HTML) heads each segment of a lesson with the figure that
    opens it on the slides (#99): one picture, taught in both modes.
    """
    short = short_label(deck)
    number = int(deck["id"][1:])
    title, body = SC.split_title(text)
    rendered, headings, _ = SC.render_document(body)
    if kind == "lesson":
        rendered = reading_marks(rendered, deck["id"])
        if segment_figures:
            rendered = segment_heads(rendered, segment_figures)
    toc = SC.toc_html(headings, 2, 3 if kind == "lesson" else 2)
    ledes = {
        "lesson": SH.T("The master text for the three segments — what the narration teaches, in full, with every repo pointer linked at the commit it was verified against.",
                       "三个分段的完整正文：讲解所教的全部内容，每个仓库指针都链接到核对时的那次提交。"),
        "handout": SH.T("The one-page cheat sheet: the mental model, the commands worth keeping, the files to open, the gotchas, and the done-when checklist.",
                        "一页速查：心智模型、值得记住的命令、要打开的文件、易错点，以及完成标准清单。"),
        "glossary": SH.T("Every term the module leans on, with where it lives — a file you can open, not a definition you have to trust.",
                         "本模块用到的每个术语及其出处——一个你可以打开的文件，而不是一个只能相信的定义。"),
    }
    head = SH.page_head(f"Module {number} · {KIND_TITLES[kind]}",
                        html.escape(title or f"{KIND_TITLES[kind]} — {short}"), ledes[kind],
                        read_views(deck["id"], site_base, kind))
    aside = f'<aside class="doc-aside">{toc}</aside>' if toc else ""
    body_html = f"""{head}
<div class="doc-main{' has-toc' if toc else ''}">
  {aside}
  <article class="doc-article {kind}-doc">
{rendered}
    <footer class="doc-footer">
      <p class="index-footnote">{SH.T("Source", "来源")}: <code>{source_path(deck, kind)}</code>. {SH.T("Repo pointers link to the upstream file at the commit the course was verified against.", "仓库指针链接到课程核对时那次提交中的上游文件。")}</p>
    </footer>
  </article>
</div>"""
    # Where each unit's section starts in the lesson — the home page's "Read this segment instead".
    read_anchors = {}
    if kind == "lesson":
        for h in headings:
            if h["level"] != 2:
                continue
            text = html.unescape(re.sub(r"<[^>]+>", "", h["text"])).strip()
            for rx, fixed in READ_UNIT:
                m = rx.match(text)
                if m:
                    read_anchors.setdefault(fixed or m.group(1), h["id"])
                    break
    # Each section's own text, so the palette can match and quote a section, not only its heading.
    section_text = {m.group(1): re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(2))).strip()
                    for m in re.finditer(r'<h[23] id="([^"]+)"[^>]*>.*?</h[23]>(.*?)(?=<h[23] |\Z)', rendered, re.S)}
    record = {"kind": kind, "deck": deck["id"], "title": title or f"{KIND_TITLES[kind]} — {short}",
              "read_anchors": read_anchors,
              "href": f"{kind}-{deck['id']}.html",
              "headings": [{"text": h["text"], "id": h["id"], "x": section_text.get(h["id"], "")[:1500]}
                           for h in headings if h["level"] <= 3],
              "text": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", rendered))[:20000]}
    return SH.document(f"{title or KIND_TITLES[kind]} — AI Product Studio", ledes[kind], body_html,
                       site_base, f"doc-page {kind}-page",
                       crumbs=SH.module_crumbs(site_base, deck, KIND_TITLES[kind]),
                       deck_id=deck["id"], current={"glossary": "module-glossary"}.get(kind, kind),
                       mode="read"), record


READ_UNIT = (
    (re.compile(r"^(?:Overview\b|概览)", re.I), "intro"),
    (re.compile(r"^(?:Segment\s+)?(M\d+\.\d)\b"), None),
    (re.compile(r"^(?:Recap\b|回顾)", re.I), "summary"),
)


def segment_heads(rendered: str, figures_by_unit: dict[str, str]) -> str:
    """Put each segment's figure right under the lesson heading that opens that segment."""
    def place(m: re.Match) -> str:
        text = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
        for rx, fixed in READ_UNIT:
            hit = rx.match(text)
            if hit:
                fig = figures_by_unit.get(fixed or hit.group(1), "")
                return m.group(0) + fig
        return m.group(0)
    return re.sub(r"<h2[^>]*>(.*?)</h2>", place, rendered, flags=re.S)


def reading_marks(rendered: str, deck_id: str) -> str:
    """Mark the end of each section that is a unit, so reading it to the end records the unit (#84).

    The lesson's own headings name the units: Overview is the introduction, "Segment M2.1 — …" is
    that segment, Recap is the summary. A marker sits where the section ends — before the next
    heading at its level — and shell.js records the unit as read when the marker comes into view.
    """
    parts = re.split(r"(?=<h2[ >])", rendered)
    out = []
    for part in parts:
        heading = re.match(r"<h2[^>]*>(.*?)</h2>", part, re.S)
        text = html.unescape(re.sub(r"<[^>]+>", "", heading.group(1))).strip() if heading else ""
        unit = None
        for rx, fixed in READ_UNIT:
            m = rx.match(text)
            if m:
                unit = fixed or m.group(1)
                break
        out.append(part + (f'<span class="read-end" data-read-unit="{deck_id}:{unit}" aria-hidden="true"></span>'
                           if unit else ""))
    return "".join(out)


def master_glossary_page(terms_by_deck: dict[str, list[dict]], decks_by_id: dict, site_base: str,
                         brand: str) -> str:
    merged: dict[str, dict] = {}
    for deck_id, terms in terms_by_deck.items():
        for t in terms:
            key = t["term"].lower()
            if key in merged:
                merged[key]["modules"].append(deck_id)
                if len(t["definition"]) > len(merged[key]["definition"]):
                    merged[key]["definition"] = t["definition"]
            else:
                merged[key] = {"term": t["term"], "definition": t["definition"], "modules": [deck_id]}
    items = sorted(merged.values(), key=lambda t: t["term"].lower())
    by_letter: dict[str, list[dict]] = {}
    for t in items:
        first = re.sub(r"[^a-z]", "", t["term"].lower()[:1]) or "#"
        by_letter.setdefault(first.upper(), []).append(t)
    letters = (f'<a href="#basics">{SH.T("Basics", "基础")}</a>'
               + "".join(f'<a href="#g-{k}">{k}</a>' for k in sorted(by_letter)))
    sections = []
    for k in sorted(by_letter):
        rows = "".join(
            f'<dt id="{SC.slug(t["term"])}">{SC.inline(t["term"])}'
            + "".join(f' <a class="term-module" href="{site_base}/glossary-{m}.html">M{int(m[1:])}</a>' for m in t["modules"])
            + f'</dt><dd>{SC.inline(t["definition"])}</dd>'
            for t in by_letter[k])
        sections.append(f'<section class="glossary-letter" id="g-{k}"><h2>{k}</h2><dl>{rows}</dl></section>')
    shared = sum(1 for t in items if len(t["modules"]) > 1)
    head = SH.page_head(f"Master glossary · {len(items)} terms · {shared} shared across modules",
                        SH.T("Every term the course leans on.", "课程用到的每个术语。"),
                        SH.T("Merged from the module glossaries. Where a term is defined in more than one "
                             "module the fuller definition is kept and every module is linked.",
                             "由各模块术语表合并而成。同一术语在多个模块中都有定义时，保留更完整的定义，并链接到每个模块。"),
                        f'<nav class="letter-nav" aria-label="Jump to letter">{letters}</nav>')
    import site_terms as ST                                                       # noqa: PLC0415
    body = f"""{head}
<div class="doc-main">
  <article class="doc-article glossary-all">
{ST.basics_section(SH.LANG)}
{"".join(sections)}
  </article>
</div>"""
    return SH.document("Glossary — AI Product Studio",
                       SH.T("Every term the course leans on, merged from the module glossaries.", "课程用到的每个术语，由各模块术语表合并而成。"),
                       body, site_base, "doc-page glossary-page",
                       crumbs=[("Course", f"{site_base}/index.html"), ("Glossary", None)],
                       current="glossary")


# ---------------------------------------------------------------- lab page

def lab_page(deck: dict, lab: dict, site_base: str, brand: str,
             auto_fail: dict | None = None) -> tuple[str, dict]:
    short = short_label(deck)
    number = int(deck["id"][1:])
    meta = lab["meta"]
    goal = SC.inline(meta["Goal"][:1].upper() + meta["Goal"][1:]) if meta.get("Goal") else \
        SH.T("The hands-on checkpoint for this module. Every item on the acceptance checklist is binary, "
             "and the evidence entry you export is the format the rubrics grade.",
             "本模块的动手检查点。验收清单的每一项都只有是或否，你导出的证据条目就是评分标准所评的格式。")
    # One page, read top to bottom: every step in full, then the acceptance checklist, the auto-fail
    # list, the evidence entry, stretch goals and discussion — nothing paged or boxed into a panel.
    # A sticky step list beside the steps is the only navigation. `sections` collects the checklist.
    sections = []
    steps: list[dict] = []
    before: list[str] = []
    after: list[str] = []
    for sec in lab["sections"]:
        if sec.get("steps"):
            steps += sec["steps"]
            continue
        if sec.get("place") == "before":
            heading = f"<h3>{SC.inline(sec['title'])}</h3>" if sec["title"] else ""
            before.append(f'<div class="step-context" id="{sec["id"]}">{heading}{sec["html"]}</div>')
            continue
        if sec["kind"] == "checklist":
            sections.append(f"""<section class="lab-section lab-checklist" id="{SC.slug(sec['title'])}">
  <h2>{SC.inline(sec['title'])}</h2>
  <p class="check-progress"><strong data-check-count>0 of {lab['checklist_count']} checked</strong>
    <span class="progress-bar" aria-hidden="true"><span data-check-fill></span></span></p>
  {sec['html']}
  <p class="lab-done" data-lab-done hidden>{SH.T("<strong>Every item is checked.</strong> Now fill in the evidence entry and copy or download it: the checklist is your claim; the exported entry is your proof, and it is what completes the lab.", "<strong>每一项都已勾选。</strong>现在填写证据条目并复制或下载：清单是你的主张，导出的条目是你的证明，导出它才算完成实验。")}</p>
  <p class="lab-done is-complete" data-lab-complete hidden>{SH.T("<strong>Lab complete.</strong> The checklist is done and the evidence entry was exported; this lab now shows as complete on your module and path progress.", "<strong>实验已完成。</strong>清单已完成，证据条目已导出；本实验在你的模块和路线进度中显示为已完成。")}</p>
</section>""")
            if auto_fail and not any('id="auto-fail"' in x for x in sections):
                sections.append(f"""<section class="lab-section lab-autofail" id="auto-fail" aria-labelledby="auto-fail-title">
  <h2 id="auto-fail-title">{SC.inline(auto_fail['title'])}</h2>
  <p class="section-note">{SH.T("From this lab's rubric (<code>lab-rubrics.md</code>). Any one of these fails the lab whatever the checklist shows, so read them before you submit.", "摘自本实验的评分标准（<code>lab-rubrics.md</code>）。无论清单显示什么，只要出现其中任何一项，实验即不通过，所以提交前先读一遍。")}</p>
  {auto_fail['html']}
</section>""")
        elif sec["kind"] == "evidence":
            after.append(f"""<section class="lab-section lab-evidence" id="{SC.slug(sec['title'])}">
  <h2>{SC.inline(sec['title'])}</h2>
  {sec['html']}
  <form class="evidence-form" data-evidence-form onsubmit="return false">
    <h3>{SH.T("Write the evidence entry", "撰写证据条目")}</h3>
    <p class="section-note">{SH.T("The Module 1 format: commands with results, environment, revision, limitations. Saved in this browser as you type; copy or download it into your evidence log.", "模块 1 的格式：命令及结果、环境、版本、局限。输入时即保存在此浏览器中；复制或下载到你的证据日志。")}</p>
    <div class="evidence-grid">
      <label>Project<input type="text" data-evidence="project" placeholder="my-studio"></label>
      <label>Date<input type="date" data-evidence="date"></label>
      <label class="wide">Commands, one per line, with results<textarea data-evidence="commands" rows="4" placeholder="python3 -m pytest tests/ -q → 201 passed, 2 skipped"></textarea></label>
      <label>Environment<input type="text" data-evidence="environment" placeholder="macOS 15.6, Python 3.11.9, Ollama 0.30 (qwen3:0.6b local)"></label>
      <label>Revision (git rev-parse HEAD)<input type="text" data-evidence="revision" placeholder="abc1234"></label>
      <label class="wide">Limitations / not verified, one per line<textarea data-evidence="limitations" rows="3" placeholder="Contract test skipped — daemon has only :cloud aliases"></textarea></label>
    </div>
    <label class="wide">Evidence entry (Markdown)<textarea data-evidence-out rows="10" readonly></textarea></label>
    <div class="evidence-actions">
      <button type="button" class="btn-primary" data-evidence-copy>Copy evidence entry</button>
      <button type="button" data-evidence-download>Download .md</button>
      <span class="evidence-status" data-evidence-status role="status" aria-live="polite"></span>
    </div>
  </form>
</section>""")
        else:
            cls = {"stretch": "lab-stretch", "discussion": "lab-discussion"}.get(sec["kind"], "")
            heading = f"<h2>{SC.inline(sec['title'])}</h2>" if sec["title"] else ""
            after.append(f'<section class="lab-section {cls}" id="{SC.slug(sec["title"] or "lab")}">{heading}{sec["html"]}</section>')
    evidence_id = next((s["id"] for s in lab["sections"] if s["kind"] == "evidence"), "")
    if evidence_id:
        sections.append(f'<a class="btn-dark lab-export" href="#{evidence_id}" data-evidence-jump>'
                        f'{SH.T("Write and export the evidence entry", "撰写并导出证据条目")}</a>')
    if before:
        steps.insert(0, {"title": "Before you start", "time": "", "id": "before-you-start",
                         "html": "".join(before), "intro": True})
    counted = [s for s in steps if not s.get("intro")]
    rows, views = [], []
    number_of = 0
    for i, step in enumerate(steps):
        if not step.get("intro"):
            number_of += 1
        dot = "i" if step.get("intro") else str(number_of)
        time = f'<p class="step-time">{html.escape(step["time"])}</p>' if step["time"] else ""
        where = ("Before you start" if step.get("intro")
                 else f"Step {number_of} of {len(counted)}")
        rows.append(f'<li><a href="#{step["id"]}" data-step-go="{i}"><span class="step-dot" aria-hidden="true">{dot}</span>'
                    f'<span class="step-name">{SC.inline(step["title"])}</span>'
                    f'<span class="sr-only" data-step-state>to do</span></a></li>')
        toggle = "" if step.get("intro") else (
            f'<div class="step-actions"><button type="button" class="step-done" data-step-done aria-pressed="false">'
            f'<span class="step-done-box" aria-hidden="true"></span><span data-step-done-label>Mark step {number_of} done</span>'
            f'</button></div>')
        views.append(f"""<section class="lab-step" id="{step['id']}" data-step="{i}" aria-labelledby="{step['id']}-title">
  <p class="step-count">{where}</p>
  <h2 id="{step['id']}-title">{SC.inline(step['title'])}</h2>
  {time}
  <div class="step-body">{step['html']}</div>
  {toggle}
</section>""")
    # After the steps, the list points at what decides the grade.
    for sec in lab["sections"]:
        if sec["kind"] in ("checklist", "evidence") and sec["title"]:
            mark = "✓" if sec["kind"] == "checklist" else "✎"
            rows.append(f'<li class="lab-steps-after"><a href="#{SC.slug(sec["title"])}"><span class="step-dot" aria-hidden="true">{mark}</span>'
                        f'<span class="step-name">{SC.inline(sec["title"])}</span></a></li>')
    facts_row = f"{len(counted)} steps · {lab['checklist_count']} checks decide the grade"
    # The lab's own header block, whole — goal, notes, prerequisites, time and the pass gate — as the
    # brief under the title. Labs that open without one keep the generic line.
    brief = (f'<div class="lab-brief">{lab["brief_html"]}</div>' if lab.get("brief_html")
             else f'<p class="page-lede">{goal}</p>')
    head = SH.page_head(f"Module {number} · Lab · pass/fail", SC.inline(lab["title"]), "",
                        brief + f'<p class="lab-facts">{facts_row}</p>')
    body = f"""{head}
<div class="lab-root" data-lab="{deck['id']}" data-lab-checks="{lab['checklist_count']}" data-lab-title="{html.escape(lab['title'], quote=True)}">
  <div class="lab-workspace">
    <nav class="lab-steps" aria-label="Steps"><ol>{"".join(rows)}</ol></nav>
    <div class="lab-main doc-article">
      <div class="lab-view">{"".join(views)}</div>
      <div class="lab-accept" aria-label="Acceptance">{"".join(sections)}</div>
      <div class="lab-after">
{"".join(after)}
      <footer class="doc-footer">
        <p class="index-footnote">{SH.T("Checklist ticks, finished steps and the evidence draft are stored in this browser only. Export your progress from the course home if you change machines.", "清单勾选、已完成的步骤和证据草稿只保存在此浏览器中。换电脑时，请从课程首页导出进度。")} {SH.T("Source", "来源")}: <code>{source_path(deck, "lab")}</code>.</p>
      </footer>
    </div>
  </div>
</div>"""
    step_headings = [{"text": s["title"], "id": s["id"], "step": True,
                      "x": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s["html"])).strip()[:1500]} for s in steps]
    other = [{"text": s["title"], "id": SC.slug(s["title"] or "lab")} for s in lab["sections"]
             if s["title"] and not s.get("steps") and s.get("place") != "before"]
    record = {"kind": "lab", "deck": deck["id"], "title": lab["title"], "href": f"lab-{deck['id']}.html",
              "headings": step_headings + other,
              "text": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", "".join(s["html"] for s in lab["sections"])))[:20000]}
    return SH.document(f"{lab['title']} — AI Product Studio", meta.get("Goal", SH.T("The module lab.", "本模块的实验。")), body,
                       site_base, "doc-page lab-page", crumbs=SH.module_crumbs(site_base, deck, "Lab"),
                       deck_id=deck["id"], current="lab", mode="lab", scripts=("lab.js",)), record


# ---------------------------------------------------------------- knowledge check

def quiz_page(deck: dict, quiz: dict, site_base: str, brand: str,
              units: list[dict] | None = None) -> tuple[str, dict]:
    """Check (#78, #112): every question on one page, feedback under each answer that links back to
    the part of the Learn page that teaches it, and the result at the end.

    Every question maps to a lesson objective, and the objective names its segment (M2.1), so the
    Rewatch link is the segment's first slide — derived, never hand-written.
    """
    short = short_label(deck)
    number = int(deck["id"][1:])
    by_segment = {u["id"]: u for u in (units or []) if u["kind"] == "segment"}
    total = len(quiz["questions"])
    blocks = []
    for index, q in enumerate(quiz["questions"], 1):
        n = q["n"]
        unit = by_segment.get(q.get("objective", ""))
        rewatch = (f'<a class="q-rewatch" href="{site_base}/{deck["id"]}.html#slide-{unit["first"]}">'
                   f'Revisit {html.escape(unit["id"])} — {SC.inline(unit["label"])}</a>') if unit else ""
        attrs = (f'data-n="{n}" data-objective="{html.escape(q.get("objective_text", ""), quote=True)}"'
                 f' data-rewatch="{site_base}/{deck["id"]}.html#slide-{unit["first"]}"' if unit else
                 f'data-n="{n}" data-objective="{html.escape(q.get("objective_text", ""), quote=True)}"')
        objective = q.get("objective_text", "")
        nav = ""
        count = (f'<p class="q-count-line" id="q{n}-count"><span>Question {index} of {total}</span>'
                 + (f'<span class="q-objective">Objective: {html.escape(objective)}</span>' if objective else "")
                 + '</p>')
        if q["type"] == "mc":
            opts = "".join(
                f'<label class="q-option" data-letter="{o["letter"]}">'
                f'<input type="radio" name="q{n}" value="{o["letter"]}">'
                f'<span class="q-letter" aria-hidden="true">{o["letter"].upper()}</span>'
                f'<span class="q-text">{o["html"]}</span><span class="q-mark" data-mark></span></label>'
                for o in q["options"])
            blocks.append(f"""<section class="qq is-mc" {attrs} data-answer="{q['answer']}" aria-labelledby="q{n}-count">
  {count}
  <div class="q-stem" id="q{n}-stem">{q['stem_html']}</div>
  <fieldset class="q-field" aria-describedby="q{n}-stem">
    <legend class="sr-only">Question {index} of {total}: choose one answer</legend>
    <div class="q-options">{opts}</div>
  </fieldset>
  <div class="q-actions"><button type="button" class="btn-primary" data-check disabled>Check answer</button></div>
  <p class="q-feedback" data-feedback role="status" aria-live="polite"></p>
  <div class="q-explain" hidden><p class="q-explain-title">Why</p><p>{q['rationale_html']}</p>{rewatch}</div>
  {nav}
</section>""")
        else:
            blocks.append(f"""<section class="qq is-short" {attrs} aria-labelledby="q{n}-count">
  {count}
  <div class="q-stem" id="q{n}-stem">{q['stem_html']}</div>
  <label class="q-write">Your answer<textarea rows="5" placeholder="{SH.T("Write it first — the model answer unlocks after 20 characters.", "先写出你的答案——写满 20 个字符后可查看参考答案。")}"></textarea></label>
  <div class="q-actions"><button type="button" class="btn-primary" data-reveal disabled>Reveal the model answer</button></div>
  <p class="q-feedback" data-feedback role="status" aria-live="polite"></p>
  <div class="q-explain" hidden><p class="q-explain-title">Model answer</p><p>{q['rationale_html']}</p>{rewatch}</div>
  {nav}
</section>""")
    head = SH.page_head(
        f"Module {number} · Knowledge check · {quiz['mc']} multiple choice + {quiz['short']} short answer",
        SC.inline(quiz["title"]),
        SH.T("Each question maps to one lesson objective, and the distractors are the misconceptions the "
             "lesson argues against. Multiple choice is checked instantly; short answers reveal the model "
             "answer only after you have written yours. Best score is kept; 75% is the certificate threshold.",
             "每道题对应一个课程目标，干扰项正是课程所反驳的误解。选择题即时判分；简答题要先写出你的答案，"
             "才会显示参考答案。保留最好成绩；75% 是证书门槛。"))
    body = f"""{head}
<div class="doc-main">
  <article class="doc-article quiz-article" data-quiz="{deck['id']}" data-total="{total}">
    <p class="quiz-score sr-only" data-quiz-score role="status" aria-live="polite"></p>
{"".join(blocks)}
    <section class="quiz-summary" data-quiz-summary aria-labelledby="quiz-result-title">
      <h2 id="quiz-result-title" tabindex="-1">Your result</h2>
      <p data-summary-text>{SH.T("Answer every question above; your result appears here.", "回答上面的每道题，结果会显示在这里。")}</p>
      <div data-revisit hidden><h3>Objectives to revisit</h3><ul class="revisit-list" data-revisit-list></ul></div>
      <div class="evidence-actions"><button type="button" data-quiz-again>Try again</button>
        <a class="btn-primary" href="{site_base}/module-{deck['id']}.html">Back to the module →</a></div>
    </section>
    <footer class="doc-footer">
      <p class="index-footnote">{SH.T("Scores are stored in this browser only.", "成绩只保存在此浏览器中。")} {SH.T("Source", "来源")}: <code>{source_path(deck, "quiz")}</code> {SH.T("— the answer key with rationale and objective references is the same file.", "——带解析和目标对照的答案也在同一个文件中。")}</p>
    </footer>
  </article>
</div>"""
    record = {"kind": "quiz", "deck": deck["id"], "title": quiz["title"], "href": f"quiz-{deck['id']}.html",
              "headings": [{"text": f"Question {q['n']}", "id": f"q{q['n']}-stem"} for q in quiz["questions"]],
              "text": " ".join(q["stem_text"] for q in quiz["questions"])[:20000]}
    return SH.document(f"{quiz['title']} — AI Product Studio", SH.T("The module knowledge check, interactive.", "本模块的互动知识测验。"),
                       body, site_base, "doc-page quiz-page",
                       crumbs=SH.module_crumbs(site_base, deck, "Knowledge check"),
                       deck_id=deck["id"], current="quiz", mode="check", scripts=("quiz.js",)), record


# ---------------------------------------------------------------- evidence log

def evidence_page(labs: list[dict], site_base: str) -> str:
    """"Your evidence log" (#73): every lab's evidence entry, as the learner wrote it, in one place.

    The entries live in this browser's progress store, so the page is a frame that `evidence.js`
    fills: one row per lab with its checklist state and the entry in the Module 1 format, and copy
    and download for the whole log. Nothing is uploaded.
    """
    rows = "".join(
        f'<li class="evidence-row" data-evidence-lab="{lab["deck"]}"'
        f' data-lab-title="{html.escape(lab["title"], quote=True)}" data-lab-checks="{lab["checks"]}">'
        f'<h2><a href="{site_base}/lab-{lab["deck"]}.html">{SC.inline(lab["title"])}</a></h2>'
        f'<p class="evidence-state" data-evidence-state>Module {int(lab["deck"][1:])} · no entry yet</p>'
        f'<pre class="evidence-entry" data-evidence-entry hidden></pre></li>'
        for lab in labs)
    head = SH.page_head(
        "Your evidence log", SH.T("Every lab's evidence entry, in one place.", "所有实验的证据条目，汇总在一处。"),
        SH.T("Each entry is the one you wrote on the lab page: commands with results, environment, revision "
             "and limitations, in the Module 1 format the rubrics grade. They are stored in this browser "
             "only, so copy or download the whole log to keep it with your project.",
             "每一条都是你在实验页上写的：命令及结果、环境、版本和局限，采用评分标准所评的模块 1 格式。"
             "它们只保存在此浏览器中，所以请复制或下载整份日志，和你的项目放在一起。"))
    body = f"""{head}
<div class="evidence-log" data-evidence-log>
  <div class="evidence-actions">
    <button type="button" class="btn-primary" data-log-copy>Copy the whole log</button>
    <button type="button" data-log-download>Download evidence-log.md</button>
    <span class="evidence-log-count" data-log-count role="status" aria-live="polite"></span>
  </div>
  <ol class="evidence-rows">{rows}</ol>
  <noscript><p>{SH.T("The log is read from this browser's saved progress, which needs JavaScript. Each lab page still shows its own entry.", "日志读取自此浏览器保存的进度，需要 JavaScript。每个实验页仍会显示它自己的条目。")}</p></noscript>
</div>"""
    return SH.document("Your evidence log — AI Product Studio",
                       SH.T("Every lab's evidence entry, as you wrote it, in one place.", "所有实验的证据条目，按你写的原样汇总在一处。"), body, site_base,
                       "doc-page evidence-page",
                       crumbs=[("Course", f"{site_base}/index.html"), ("Your evidence log", None)],
                       current="evidence", scripts=("evidence.js",))


def search_index(records: list[dict], decks: list[dict], units_by_deck: dict,
                 times: dict | None = None) -> str:
    """The palette's index (#80): slides with their narration a sentence at a time, lesson and
    handout sections with their text, lab steps with their instructions, and glossary terms.

    Keys: k kind · d module · t title · h link · m where it sits · x text to match and quote · for a
    slide, n its number, s its narration sentences and ts when each is spoken (only when captions
    are published, so a hit can open the player at the moment it is said).
    """
    import build_site as B                                                     # noqa: PLC0415
    out = []
    times = times or {}
    for deck in decks:
        short = short_label(deck)
        for slide in deck["slides"]:
            entry = {"k": "slide", "d": deck["id"], "t": f"{slide['kicker']} — {slide['title']}",
                     "h": f"{deck['id']}.html#{slide['id']}", "m": short, "n": slide["number"],
                     "x": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", slide["html"])).strip()[:400],
                     "s": B.said_of(slide)}
            spoken = times.get(deck["id"], {}).get(slide["id"])
            if spoken and len(spoken) == len(entry["s"]):
                entry["ts"] = spoken
            out.append(entry)
        for unit in units_by_deck.get(deck["id"], []):
            out.append({"k": "unit", "d": deck["id"], "t": unit["title"] if unit["kind"] == "segment" else unit["label"],
                        "h": unit["href"], "m": short, "x": f"{unit['kind']} unit, slides {unit['first']}–{unit['last']}"})
    for r in records:
        out.append({"k": r["kind"], "d": r["deck"], "t": r["title"], "h": r["href"], "m": r.get("module", ""),
                    "x": r["text"][:1500]})
        for h in r.get("headings", []):
            out.append({"k": r["kind"] + "-heading", "d": r["deck"], "t": re.sub(r"<[^>]+>", "", h["text"]),
                        "h": f"{r['href']}#{h['id']}", "m": r["title"], "x": h.get("x", "")})
        for t in r.get("terms", []):
            out.append({"k": "term", "d": r["deck"], "t": t["term"], "h": f"{r['href']}#{SC.slug(t['term'])}",
                        "m": r["title"], "x": t["definition"][:400]})
    return json.dumps(out, ensure_ascii=False, separators=(",", ":"))
