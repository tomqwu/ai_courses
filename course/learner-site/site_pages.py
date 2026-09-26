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


def module_tabs(deck_id: str, site_base: str, active: str) -> str:
    """The per-module navigation: overview · deck · lesson · lab · knowledge check · handout · glossary."""
    items = [
        ("overview", "Overview", f"module-{deck_id}.html"),
        ("deck", "Slides", f"{deck_id}.html"),
        ("lesson", "Lesson", f"lesson-{deck_id}.html"),
        ("lab", "Lab", f"lab-{deck_id}.html"),
        ("quiz", "Knowledge check", f"quiz-{deck_id}.html"),
        ("handout", "Handout", f"handout-{deck_id}.html"),
        ("glossary", "Glossary", f"glossary-{deck_id}.html"),
        ("transcript", "Transcript", f"transcript-{deck_id}.html"),
    ]
    lis = ""
    for key, label, href in items:
        current = ' aria-current="page"' if key == active else ""
        lis += f'<li><a href="{site_base}/{href}"{current}>{label}</a></li>'
    return f'<nav class="module-tabs" aria-label="More in this module"><ul>{lis}</ul></nav>'




def short_label(deck: dict) -> str:
    return re.sub(r"^M\d+\s*—\s*", "", deck["label"]).strip()


# ---------------------------------------------------------------- reading pages

def document_page(deck: dict, kind: str, text: str, site_base: str, brand: str) -> tuple[str, dict]:
    """Lesson, handout or glossary as a reading page. Returns (html, index_record)."""
    short = short_label(deck)
    number = int(deck["id"][1:])
    title, body = SC.split_title(text)
    rendered, headings, _ = SC.render_document(body)
    toc = SC.toc_html(headings, 2, 3 if kind == "lesson" else 2)
    ledes = {
        "lesson": "The master text for the three segments — what the narration teaches, in full, with every repo pointer linked at the commit it was verified against.",
        "handout": "The one-page cheat sheet: the mental model, the commands worth keeping, the files to open, the gotchas, and the done-when checklist.",
        "glossary": "Every term the module leans on, with where it lives — a file you can open, not a definition you have to trust.",
    }
    head = SH.page_head(f"Module {number} · {KIND_TITLES[kind]}",
                        html.escape(title or f"{KIND_TITLES[kind]} — {short}"), ledes[kind],
                        module_tabs(deck["id"], site_base, kind))
    aside = f'<aside class="doc-aside">{toc}</aside>' if toc else ""
    body_html = f"""{head}
<div class="doc-main{' has-toc' if toc else ''}">
  {aside}
  <article class="doc-article">
{rendered}
    <footer class="doc-footer">
      <p class="index-footnote">Source: <code>course/03-content/{html.escape(deck['source'].split('/')[1])}/{kind}.md</code>. Repo pointers link to the upstream file at the commit the course was verified against.</p>
    </footer>
  </article>
</div>"""
    record = {"kind": kind, "deck": deck["id"], "title": title or f"{KIND_TITLES[kind]} — {short}",
              "href": f"{kind}-{deck['id']}.html",
              "headings": [{"text": h["text"], "id": h["id"]} for h in headings if h["level"] <= 3],
              "text": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", rendered))[:20000]}
    return SH.document(f"{title or KIND_TITLES[kind]} — AI Product Studio", ledes[kind], body_html,
                       site_base, f"doc-page {kind}-page",
                       crumbs=SH.module_crumbs(site_base, deck, KIND_TITLES[kind]),
                       deck_id=deck["id"], mode="read"), record


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
    letters = "".join(f'<a href="#g-{k}">{k}</a>' for k in sorted(by_letter))
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
                        "Every term the course leans on.",
                        "Merged from the module glossaries. Where a term is defined in more than one "
                        "module the fuller definition is kept and every module is linked.",
                        f'<nav class="letter-nav" aria-label="Jump to letter">{letters}</nav>')
    body = f"""{head}
<div class="doc-main">
  <article class="doc-article glossary-all">
{"".join(sections)}
  </article>
</div>"""
    return SH.document("Glossary — AI Product Studio",
                       "Every term the course leans on, merged from the module glossaries.",
                       body, site_base, "doc-page glossary-page",
                       crumbs=[("Course", f"{site_base}/index.html"), ("Glossary", None)],
                       current="glossary")


# ---------------------------------------------------------------- lab page

def lab_page(deck: dict, lab: dict, site_base: str, brand: str,
             auto_fail: dict | None = None) -> tuple[str, dict]:
    short = short_label(deck)
    number = int(deck["id"][1:])
    meta = lab["meta"]
    facts = [("Time", meta.get("Time", "")), ("Prerequisites", meta.get("Prerequisites", "")),
             ("Checklist", f"{lab['checklist_count']} items")]
    aga = "".join(f'<div class="aga-item"><dt>{html.escape(k)}</dt><dd>{SC.inline(v)}</dd></div>'
                  for k, v in facts if v)
    goal = SC.inline(meta["Goal"]) if meta.get("Goal") else \
        ("The hands-on checkpoint for this module. Every item on the acceptance checklist is binary, "
         "and the evidence entry you export is the format the rubrics grade.")
    sections = []
    for sec in lab["sections"]:
        if sec["kind"] == "checklist":
            sections.append(f"""<section class="lab-section lab-checklist" id="{SC.slug(sec['title'])}">
  <h2>{SC.inline(sec['title'])}</h2>
  <p class="check-progress"><strong data-check-count>0 of {lab['checklist_count']} checked</strong>
    <span class="progress-bar" aria-hidden="true"><span data-check-fill></span></span></p>
  {sec['html']}
  <p class="lab-done" data-lab-done hidden><strong>Every item is checked.</strong> This lab now shows as complete on your module and path progress. Record the evidence entry below — the checklist is your claim; the entry is your proof.</p>
</section>""")
            if auto_fail and not any('id="auto-fail"' in x for x in sections):
                sections.append(f"""<section class="lab-section lab-autofail" id="auto-fail" aria-labelledby="auto-fail-title">
  <h2 id="auto-fail-title">{SC.inline(auto_fail['title'])}</h2>
  <p class="section-note">From this lab's rubric (<code>lab-rubrics.md</code>). Any one of these fails the lab whatever the checklist shows, so read them before you submit.</p>
  {auto_fail['html']}
</section>""")
        elif sec["kind"] == "evidence":
            sections.append(f"""<section class="lab-section lab-evidence" id="{SC.slug(sec['title'])}">
  <h2>{SC.inline(sec['title'])}</h2>
  {sec['html']}
  <form class="evidence-form" data-evidence-form onsubmit="return false">
    <h3>Write the evidence entry</h3>
    <p class="section-note">The Module 1 format: commands with results, environment, revision, limitations. Saved in this browser as you type; copy or download it into your evidence log.</p>
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
    </div>
  </form>
</section>""")
        else:
            cls = {"stretch": "lab-stretch", "discussion": "lab-discussion"}.get(sec["kind"], "")
            heading = f"<h2>{SC.inline(sec['title'])}</h2>" if sec["title"] else ""
            sections.append(f'<section class="lab-section {cls}" id="{SC.slug(sec["title"] or "lab")}">{heading}{sec["html"]}</section>')
    head = SH.page_head(f"Module {number} · Lab · pass/fail", SC.inline(lab["title"]), goal,
                        f'<dl class="at-a-glance">{aga}</dl>{module_tabs(deck["id"], site_base, "lab")}')
    body = f"""{head}
<div class="doc-main">
  <article class="doc-article lab-article" data-lab="{deck['id']}" data-lab-checks="{lab['checklist_count']}" data-lab-title="{html.escape(lab['title'], quote=True)}">
{"".join(sections)}
    <footer class="doc-footer">
      <p class="index-footnote">Checklist ticks and the evidence draft are stored in this browser only. Export your progress from the course home if you change machines. Source: <code>course/03-content/{html.escape(deck['source'].split('/')[1])}/lab.md</code>.</p>
    </footer>
  </article>
</div>"""
    record = {"kind": "lab", "deck": deck["id"], "title": lab["title"], "href": f"lab-{deck['id']}.html",
              "headings": [{"text": s["title"], "id": SC.slug(s["title"] or "lab")} for s in lab["sections"] if s["title"]],
              "text": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", "".join(s["html"] for s in lab["sections"])))[:20000]}
    return SH.document(f"{lab['title']} — AI Product Studio", meta.get("Goal", "The module lab."), body,
                       site_base, "doc-page lab-page", crumbs=SH.module_crumbs(site_base, deck, "Lab"),
                       deck_id=deck["id"], current="lab", mode="lab", scripts=("lab.js",)), record


# ---------------------------------------------------------------- knowledge check

def quiz_page(deck: dict, quiz: dict, site_base: str, brand: str) -> tuple[str, dict]:
    short = short_label(deck)
    number = int(deck["id"][1:])
    blocks = []
    for q in quiz["questions"]:
        n = q["n"]
        obj = f'<span class="q-objective">Objective {html.escape(q["objective"])}</span>' if q.get("objective") else ""
        if q["type"] == "mc":
            opts = "".join(
                f'<button type="button" class="q-option" role="radio" aria-checked="false" data-letter="{o["letter"]}">'
                f'<span class="q-letter">{o["letter"].upper()}</span><span class="q-text">{o["html"]}</span></button>'
                for o in q["options"])
            blocks.append(f"""<section class="qq is-mc" data-n="{n}" data-answer="{q['answer']}" aria-labelledby="q{n}-stem">
  <p class="q-number">Question {n} <span class="q-kind">multiple choice</span> {obj}</p>
  <div class="q-stem" id="q{n}-stem">{q['stem_html']}</div>
  <div class="q-options" role="radiogroup" aria-labelledby="q{n}-stem">{opts}</div>
  <div class="q-actions"><button type="button" class="btn-primary" data-check disabled>Check answer</button>
    <span class="q-feedback" data-feedback role="status" aria-live="polite"></span></div>
  <div class="q-explain" hidden><p class="q-explain-title">Why</p><p>{q['rationale_html']}</p></div>
</section>""")
        else:
            blocks.append(f"""<section class="qq is-short" data-n="{n}" aria-labelledby="q{n}-stem">
  <p class="q-number">Question {n} <span class="q-kind">short answer</span> {obj}</p>
  <div class="q-stem" id="q{n}-stem">{q['stem_html']}</div>
  <label class="q-write">Your answer<textarea rows="5" placeholder="Write it first — the model answer unlocks after 20 characters."></textarea></label>
  <div class="q-actions"><button type="button" class="btn-primary" data-reveal disabled>Reveal the model answer</button>
    <span class="q-feedback" data-feedback role="status" aria-live="polite"></span></div>
  <div class="q-explain" hidden><p class="q-explain-title">Model answer</p><p>{q['rationale_html']}</p></div>
</section>""")
    head = SH.page_head(
        f"Module {number} · Knowledge check · {quiz['mc']} multiple choice + {quiz['short']} short answer",
        SC.inline(quiz["title"]),
        "Each question maps to one lesson objective, and the distractors are the misconceptions the "
        "lesson argues against. Multiple choice is checked instantly; short answers reveal the model "
        "answer only after you have written yours. Best score is kept; 75% is the certificate threshold.",
        module_tabs(deck["id"], site_base, "quiz"))
    body = f"""{head}
<div class="doc-main">
  <article class="doc-article quiz-article" data-quiz="{deck['id']}">
    <p class="quiz-score" data-quiz-score role="status" aria-live="polite"></p>
{"".join(blocks)}
    <section class="quiz-summary" data-quiz-summary hidden>
      <h2>Result</h2>
      <p data-summary-text></p>
      <div class="evidence-actions"><button type="button" data-quiz-again>Try again</button>
        <a class="btn-primary" href="{site_base}/module-{deck['id']}.html">Back to the module →</a></div>
    </section>
    <footer class="doc-footer">
      <p class="index-footnote">Scores are stored in this browser only. Source: <code>course/03-content/{html.escape(deck['source'].split('/')[1])}/quiz.md</code> — the answer key with rationale and objective references is the same file.</p>
    </footer>
  </article>
</div>"""
    record = {"kind": "quiz", "deck": deck["id"], "title": quiz["title"], "href": f"quiz-{deck['id']}.html",
              "headings": [{"text": f"Question {q['n']}", "id": f"q{q['n']}-stem"} for q in quiz["questions"]],
              "text": " ".join(q["stem_text"] for q in quiz["questions"])[:20000]}
    return SH.document(f"{quiz['title']} — AI Product Studio", "The module knowledge check, interactive.",
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
        "Your evidence log", "Every lab's evidence entry, in one place.",
        "Each entry is the one you wrote on the lab page: commands with results, environment, revision "
        "and limitations, in the Module 1 format the rubrics grade. They are stored in this browser "
        "only, so copy or download the whole log to keep it with your project.")
    body = f"""{head}
<div class="evidence-log" data-evidence-log>
  <div class="evidence-actions">
    <button type="button" class="btn-primary" data-log-copy>Copy the whole log</button>
    <button type="button" data-log-download>Download evidence-log.md</button>
    <span class="evidence-log-count" data-log-count role="status" aria-live="polite"></span>
  </div>
  <ol class="evidence-rows">{rows}</ol>
  <noscript><p>The log is read from this browser's saved progress, which needs JavaScript. Each lab page still shows its own entry.</p></noscript>
</div>"""
    return SH.document("Your evidence log — AI Product Studio",
                       "Every lab's evidence entry, as you wrote it, in one place.", body, site_base,
                       "doc-page evidence-page",
                       crumbs=[("Course", f"{site_base}/index.html"), ("Your evidence log", None)],
                       current="evidence", scripts=("evidence.js",))


def search_index(records: list[dict], decks: list[dict], units_by_deck: dict) -> str:
    """One JSON index for the client-side search: units, slides, documents, glossary terms."""
    out = []
    for deck in decks:
        short = short_label(deck)
        for slide in deck["slides"]:
            out.append({"k": "slide", "d": deck["id"], "t": f"{slide['kicker']} — {slide['title']}",
                        "h": f"{deck['id']}.html#{slide['id']}", "m": short,
                        "x": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", slide["html"]) + " " + slide["script_text"])[:600]})
        for unit in units_by_deck.get(deck["id"], []):
            out.append({"k": "unit", "d": deck["id"], "t": unit["title"] if unit["kind"] == "segment" else unit["label"],
                        "h": unit["href"], "m": short, "x": f"{unit['kind']} unit, slides {unit['first']}–{unit['last']}"})
    for r in records:
        out.append({"k": r["kind"], "d": r["deck"], "t": r["title"], "h": r["href"], "m": r.get("module", ""),
                    "x": r["text"][:1500]})
        for h in r.get("headings", []):
            out.append({"k": r["kind"] + "-heading", "d": r["deck"], "t": h["text"], "h": f"{r['href']}#{h['id']}",
                        "m": r["title"], "x": ""})
        for t in r.get("terms", []):
            out.append({"k": "term", "d": r["deck"], "t": t["term"], "h": f"{r['href']}#{SC.slug(t['term'])}",
                        "m": r["title"], "x": t["definition"][:400]})
    return json.dumps(out, ensure_ascii=False, separators=(",", ":"))
