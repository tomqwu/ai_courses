#!/usr/bin/env python3
"""The site's interactive features, driven in a real browser the way a learner uses them.

    python3 check_features.py               # build the site first (make -C .. site)
    python3 check_features.py --print-skip  # exit 0 with a note when Playwright is not installed

check_player.py proves the pages look right: contrast, layout, geometry, the unit partition. This
proves they work: progress survives a reload and reaches the cards, every knowledge-check question
plays to its keyed answer and never shows a model answer before an attempt, a lab checklist
persists and exports its evidence entry in the Module 1 format, the rubric's auto-fail list is on
every lab page, search opens on "/" and finds a term with its slide, the reading pages link
pointers at a pinned commit, and the landing page leads with linked proof and fits a phone.

The app shell (#73) is held to its done-when: every page renders the outline and the top bar and
none opens on a hero, the outline reflects stored progress after a reload and follows the player,
the keyboard order is skip link → outline (search included) → top bar → content, and below 1024px
the outline is a drawer that opens, closes on Escape and hands focus back.

Each browser context starts with empty storage, so nothing a learner saved is read or changed.
Needs the Python Playwright package (CI installs it for check_player.py); the browser is found the
same way check_player.py finds it.
"""
from __future__ import annotations

import argparse
import functools
import http.server
import json
import re
import sys
import threading
from pathlib import Path

SITE = Path(__file__).resolve().parent
COURSE = SITE.parent
sys.path.insert(0, str(SITE))


class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):   # noqa: D401 - silence the per-request log
        pass


def run(page, browser, base: str) -> list[str]:
    problems: list[str] = []

    def need(cond, what):
        if not cond:
            problems.append(what)

    def units():
        return json.loads(page.evaluate("JSON.stringify(window.APSProgress.get().units)"))

    def events():
        return json.loads(page.evaluate("JSON.stringify(window.APSProgress.events())"))

    # Progress is recorded, never self-ticked (#84): no page offers a checkbox that marks a unit, and
    # a new visitor sees Start above the fold on a module page, on a desktop and on a phone.
    for built in sorted(p for p in SITE.glob("*.html") if not p.name.startswith("_")):
        need('data-progress="' not in built.read_text(encoding="utf-8"),
             f"{built.name}: offers a checkbox that marks a unit done")
    for w, h in ((1440, 900), (390, 844)):
        fresh = browser.new_context(viewport={"width": w, "height": h}).new_page()
        fresh.goto(f"{base}/module-m03.html")
        box = fresh.locator("[data-start-link]").bounding_box()
        need(box and box["y"] + box["height"] <= h and fresh.locator("[data-start-link]").inner_text().strip() == "Start module",
             f"module-m03 at {w}x{h}: Start module is not above the fold for a new visitor")
        fresh.close()
    page.goto(f"{base}/index.html")
    need(page.locator("[data-continue]").is_hidden(), "index: a first visit shows 'continue'")
    # A module's landing point (#74): a first visit is offered the start, at the top of the page.
    page.goto(f"{base}/module-m02.html")
    start = page.locator("[data-start-link]")
    need(start.inner_text().strip() == "Start module" and (start.get_attribute("href") or "").endswith("m02.html#slide-1")
         and start.bounding_box()["y"] < 900,
         "module-m02: a first visit is not offered 'Start module' above the fold")
    # Paging through a deck records where the learner is, and completes nothing.
    page.goto(f"{base}/m02.html")
    page.locator("#slides").focus()
    for _ in range(4):
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(60)
    need(not any(k.startswith("m02:") for k in units()), "deck: paging M2 completed a unit without watching it")
    # Watching: the narration ending on a unit's last slide records the unit as watched. The audio
    # itself is not played here (a module is minutes long); its `ended` event is what the player
    # records, so that is what is fired, on each lesson unit's last slide.
    page.goto(f"{base}/module-m02.html")
    watch = [(a.get_attribute("data-unit"), a.get_attribute("data-last"))
             for a in page.locator(".unit-link[data-unit]").all()
             if a.get_attribute("data-unit").split(":")[1] not in ("lab", "quiz")]
    for unit, last in watch:
        page.goto(f"{base}/m02.html#slide-{last}")
        page.wait_for_timeout(250)
        page.evaluate("document.querySelector('audio[data-narration-audio]').dispatchEvent(new Event('ended'))")
    watched = {e["unit"] for e in events() if e["kind"] == "watched"}
    need(watched == {u for u, _ in watch}, f"deck: watching M2 end to end recorded {sorted(watched)}")
    page.goto(f"{base}/module-m02.html")
    page.reload()
    for unit, _ in watch:
        row = page.locator(f'.unit-link[data-unit="{unit}"]')
        need("is-done" in (row.get_attribute("class") or ""), f"module-m02: {unit} was watched but its row is not done")
        need("is-done" in (page.locator(f'#app-outline [data-unit="{unit}"]').get_attribute("class") or ""),
             f"outline: {unit} was watched but the outline does not show it done")
    page.goto(f"{base}/index.html")
    need(page.locator("[data-continue]").is_visible(), "index: a returning visit shows no 'continue'")
    card = page.locator('[data-card-module="m02"] [data-ring-units]').get_attribute("aria-label") or ""
    need(card.startswith(f"{len(watch)} of"), f"index: the M2 card does not show its watched units ({card!r})")
    rings = page.eval_on_selector_all("[data-ring-units]", "els => els.map(e => e.getAttribute('aria-label'))")
    need(any(r and not r.startswith("0 of") for r in rings), f"index: no progress ring reflects progress ({rings[:3]})")
    need('"kind": "watched"' in page.evaluate("window.APSProgress.exportJSON()"), "progress export lacks the watched events")
    # Reading: a lesson read to the end records its units as read.
    page.goto(f"{base}/lesson-m03.html")
    height = page.evaluate("document.documentElement.scrollHeight")
    for y in range(0, height + 900, 500):
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(40)
    page.wait_for_timeout(300)
    read = {e["unit"] for e in events() if e["kind"] == "read"}
    need({"m03:intro", "m03:M3.1", "m03:M3.2", "m03:M3.3", "m03:summary"} <= read,
         f"lesson-m03: reading to the end recorded {sorted(read)}")

    # The shell (#73): one frame on every page, and no page opens on the old hero band.
    for built in sorted(p for p in SITE.glob("*.html") if not p.name.startswith("_")):
        text = built.read_text(encoding="utf-8")
        need('id="app-outline"' in text and 'class="app-bar"' in text and 'class="skip-link"' in text,
             f"{built.name}: does not render the shell (outline, top bar and skip link)")
        need('class="site-header' not in text, f"{built.name}: still opens on the hero band")
        # Four modes, not nine tabs (#74): a module page offers Watch · Read · Lab · Check and nothing
        # beside them at the top level.
        need('class="module-tabs"' not in text, f"{built.name}: still shows the module tab row")
        if 'class="mode-switch"' in text:
            modes = re.search(r'<nav class="mode-switch"[^>]*>(.*?)</nav>', text, re.S).group(1)
            labels = [re.sub(r"<[^>]+>", "", a).strip() for a in re.findall(r"<a [^>]*>(.*?)</a>", modes, re.S)]
            need(labels == ["Watch", "Read", "Lab", "Check"],
                 f"{built.name}: the mode switch is not exactly Watch · Read · Lab · Check")
    # Every old per-module URL still resolves, as a view of its mode.
    for deck in sorted(p.stem.split("-")[1] for p in SITE.glob("quiz-m*.html")):
        for pattern, mode in (("{d}.html", "Watch"), ("lesson-{d}.html", "Read"), ("handout-{d}.html", "Read"),
                              ("glossary-{d}.html", "Read"), ("transcript-{d}.html", "Watch"),
                              ("lab-{d}.html", "Lab"), ("quiz-{d}.html", "Check"), ("module-{d}.html", None)):
            path = SITE / pattern.format(d=deck)
            if not path.exists():
                problems.append(f"{path.name}: an old URL no longer resolves")
                continue
            current = re.search(r'<nav class="mode-switch".*?<a [^>]*aria-current="page"[^>]*>(.*?)</a>',
                                path.read_text(encoding="utf-8"), re.S)
            shown = re.sub(r"<[^>]+>", "", current.group(1)).strip() if current else None
            need(shown == mode, f"{path.name}: shows mode {shown!r}, expected {mode!r}")
    # The outline reflects what was stored, after a reload: paging M2 above recorded its first unit.
    page.goto(f"{base}/module-m02.html")
    page.reload()
    done = sorted(k for k in units() if k.startswith("m02:"))
    module_cls = page.locator('#app-outline [data-module="m02"] > a').get_attribute("class") or ""
    need("is-progress" in module_cls or "is-done" in module_cls,
         f"outline: M2 does not show as started after a reload ({module_cls!r})")
    if done:
        row = page.locator(f'#app-outline [data-unit="{done[0]}"]')
        need("is-done" in (row.get_attribute("class") or "")
             and (row.locator("[data-status-text]").text_content() or "").strip() == "done",
             f"outline: {done[0]} was recorded done but the outline does not say so in words")
    # …and the module's start point has become the resume point.
    need(page.locator("[data-start-label]").inner_text().startswith("Resume · slide "),
         "module-m02: after paging the deck, the start point does not offer to resume")
    todo = page.locator('#app-outline [data-module="m05"] > a')
    need("is-todo" in (todo.get_attribute("class") or "")
         and (todo.locator("[data-status-text]").text_content() or "").strip() == "not started",
         "outline: an untouched module is not marked 'not started'")
    # It follows the player: a deep link to M2.2 makes that unit "you are here".
    first = page.locator('#app-outline [data-unit="m02:M2.2"]').get_attribute("data-first")
    page.goto(f"{base}/m02.html#slide-{first}")
    page.wait_for_timeout(300)
    need(page.locator('#app-outline [data-unit="m02:M2.2"][aria-current]').count() == 1
         and page.locator('#app-outline [aria-current]').count() == 1,
         "outline: the deck's current unit is not the one marked aria-current")
    # A lab page names itself in the outline and in the mode switch.
    page.goto(f"{base}/lab-m03.html")
    need(page.locator('#app-outline [data-unit="m03:lab"][aria-current="page"]').count() == 1,
         "outline: the lab page does not mark its unit aria-current")
    need(page.locator('.mode-switch a[aria-current="page"]').text_content().strip() == "Lab",
         "top bar: the lab page's mode switch does not show Lab as current")
    # The player works without a mouse (#75): arrows move slides, T opens the transcript, the tabs
    # answer arrow keys, F presents and F leaves; the Up next card names what follows.
    page.goto(f"{base}/m03.html#slide-1")
    page.wait_for_timeout(300)
    page.locator("#slides").focus()
    page.keyboard.press("ArrowRight")
    need(page.evaluate("document.querySelector('.slide[aria-current]').id") == "slide-2",
         "player: ArrowRight did not move to slide 2")
    page.keyboard.press("t")
    need(page.evaluate("document.activeElement.id") == "tab-transcript", "player: T did not focus the transcript tab")
    page.keyboard.press("ArrowRight")
    need(page.evaluate("document.activeElement.id") == "tab-sources"
         and not page.locator("#panel-sources").is_hidden(),
         "player: the panel tabs do not answer the arrow keys")
    page.locator("#slides").focus()
    page.keyboard.press("f")
    presenting = page.evaluate("document.body.classList.contains('presentation-mode')")
    page.keyboard.press("f")
    need(presenting and not page.evaluate("document.body.classList.contains('presentation-mode')"),
         "player: F did not enter and leave presentation mode")
    need(page.locator("[data-up-title]").inner_text().strip() != "", "player: the Up next card is empty")

    # Keyboard order: skip link, then the outline (with search), then the top bar, then the content.
    page.goto(f"{base}/lab-m03.html")
    groups = page.evaluate("""() => {
      const sel = 'a[href], button:not([disabled]), input:not([disabled]), select, textarea, [tabindex]:not([tabindex="-1"])';
      return [...document.querySelectorAll(sel)].filter(e => {
        const s = getComputedStyle(e); return s.visibility !== 'hidden' && s.display !== 'none' && e.getClientRects().length;
      }).map(e => e.classList.contains('skip-link') ? 'skip' : e.closest('#app-outline')
        ? (e.matches('[data-search-open]') ? 'search' : 'outline')
        : e.closest('.app-bar') ? 'bar' : e.closest('#content') ? 'content' : 'other');
    }""")
    last = {g: max(i for i, x in enumerate(groups) if x == g) for g in set(groups)}
    firsts = {g: groups.index(g) for g in set(groups)}
    need(groups[:1] == ["skip"] and "search" in firsts
         and last.get("outline", -1) < firsts.get("bar", -1) < firsts.get("content", -1)
         and last.get("bar", -1) < firsts.get("content", -1),
         f"keyboard order is not skip → outline → top bar → content ({groups[:6]} …)")
    page.keyboard.press("Tab")
    need(page.evaluate("document.activeElement.classList.contains('skip-link')"),
         "the first Tab does not land on the skip link")
    page.keyboard.press("Enter")
    need(page.evaluate("document.activeElement.id") == "content", "the skip link does not move focus to the content")
    # Below 1024px the outline is a drawer: hidden, opened from the top bar, closed by Escape.
    tablet = browser.new_context(viewport={"width": 800, "height": 900}).new_page()
    tablet.goto(f"{base}/lesson-m02.html")
    hidden = lambda: tablet.locator("#app-outline").evaluate("n => getComputedStyle(n).visibility") == "hidden"
    need(hidden(), "outline at 800px: not collapsed to a drawer")
    tablet.click("[data-outline-toggle]")
    tablet.wait_for_timeout(350)
    need(not hidden() and tablet.get_attribute("[data-outline-toggle]", "aria-expanded") == "true"
         and tablet.evaluate("!!document.activeElement.closest('#app-outline')"),
         "outline at 800px: the drawer did not open with focus inside it")
    tablet.keyboard.press("Escape")
    tablet.wait_for_timeout(350)
    need(hidden() and tablet.evaluate("document.activeElement.matches('[data-outline-toggle]')"),
         "outline at 800px: Escape did not close the drawer and return focus to its button")
    tablet.close()

    # Knowledge checks: every question on every page, played to its keyed answer.
    quiz_pages = sorted(SITE.glob("quiz-m*.html"))
    need(quiz_pages, "no quiz pages built")
    played = 0
    # One question at a time (#78): each is answered, then "Next question" opens the next; the last
    # opens the result. Every question is a fieldset with a legend, and its feedback is a status.
    for qp in quiz_pages:
        page.goto(f"{base}/{qp.name}")
        qs = page.locator(".qq")
        for i in range(qs.count()):
            q, label = qs.nth(i), f"{qp.name} question {i + 1}"
            played += 1
            need(q.is_visible() and page.locator(".qq:visible").count() == 1,
                 f"{label}: not shown on its own screen")
            if "is-mc" in (q.get_attribute("class") or ""):
                key = q.get_attribute("data-answer") or ""
                need(q.locator("fieldset legend").count() == 1 and q.locator('[role="status"]').count() == 1,
                     f"{label}: no fieldset/legend, or no status region for the feedback")
                if q.locator(f'.q-option[data-letter="{key}"]').count() != 1:
                    problems.append(f"{label}: keyed answer {key!r} is not exactly one option")
                    continue
                q.locator(f'.q-option[data-letter="{key}"]').click()
                q.locator("[data-check]").click()
                need(q.locator(".q-explain").is_visible()
                     and "Correct answer" in q.locator(f'.q-option[data-letter="{key}"] [data-mark]').inner_text(),
                     f"{label}: no rationale, or the correct answer is not labelled in words")
            else:
                need(q.locator(".q-explain").is_hidden() and q.locator("[data-reveal]").is_disabled(),
                     f"{label}: model answer reachable before an attempt")
                q.locator("textarea").fill("An attempt long enough to count as one.")
                q.locator("[data-reveal]").click()
            q.locator("[data-next]").click()
        summary = page.locator("[data-summary-text]")
        need(summary.count() and "clears the 75%" in summary.inner_text(),
             f"{qp.name}: all keyed answers did not clear the 75% threshold")
    quizzes = json.loads(page.evaluate("JSON.stringify(window.APSProgress.get().quizzes)"))
    need(len(quizzes) == len(quiz_pages), f"quiz scores reached progress for {len(quizzes)} of {len(quiz_pages)} modules")
    # Answers persist: a finished check reopens on its result; "Try again" clears it.
    page.goto(f"{base}/quiz-m03.html")
    need(page.locator("[data-quiz-summary]").is_visible(), "quiz-m03: a finished check did not reopen on its result")
    page.locator("[data-quiz-again]").click()
    page.wait_for_load_state()
    # Keyboard only, wrong answer: the feedback names the key, and links back to the segment.
    q = page.locator(".qq.is-mc").first
    key = q.get_attribute("data-answer") or "a"
    wrong = next(l for l in "abcd" if l != key and q.locator(f'.q-option[data-letter="{l}"]').count())
    q.locator(f'.q-option[data-letter="{wrong}"] input').focus()
    page.keyboard.press("Space")
    q.locator("[data-check]").focus()
    page.keyboard.press("Enter")
    need(f"keyed answer is {key.upper()}" in q.locator("[data-feedback]").inner_text()
         and "Your answer" in q.locator(f'.q-option[data-letter="{wrong}"] [data-mark]').inner_text(),
         "quiz-m03: a keyboard-only wrong answer got no feedback naming the key and the learner's answer")
    need(re.search(r"m03\.html#slide-\d+$", q.locator(".q-rewatch").get_attribute("href") or ""),
         "quiz-m03: the feedback does not link back to the slide that teaches the question")
    page.reload()
    need(page.locator(".qq:visible").get_attribute("data-n") != q.get_attribute("data-n")
         and "is-wrong" in (page.locator(".qq").first.get_attribute("class") or ""),
         "quiz-m03: the answer did not survive a reload, or the check did not resume at the next question")

    # Labs: the checklist persists and completes; the evidence entry exports; auto-fail is shown.
    page.goto(f"{base}/lab-m01.html")
    boxes = page.locator("[data-check]")
    for i in range(boxes.count()):
        boxes.nth(i).check()
    page.reload()
    kept = sum(1 for i in range(boxes.count()) if page.locator("[data-check]").nth(i).is_checked())
    need(kept == boxes.count() > 0 and page.locator("[data-lab-done]").is_visible(),
         f"lab-m01: {kept} of {boxes.count()} checks survived a reload, or the lab did not complete")
    need("m01:lab" not in units(), "lab-m01: the checklist alone completed the lab — the evidence entry is not exported yet")
    page.fill('[data-evidence="project"]', "my-studio")
    page.fill('[data-evidence="commands"]', "python3 -m pytest tests/ -q → 2 passed")
    out = page.input_value("[data-evidence-out]")
    need(out.startswith("## Evidence — my-studio —") and "Commands (with results):\n- python3 -m pytest" in out
         and "Environment:" in out and "Revision:" in out and "Limitations / not verified:" in out,
         f"lab-m01: evidence export is not in the Module 1 format: {out[:120]!r}")
    # The exported, filled-in entry is what completes the lab (#84).
    page.fill('[data-evidence="environment"]', "macOS 15.6, Python 3.11.9")
    page.fill('[data-evidence="revision"]', "abc1234")
    with page.expect_download():
        page.click("[data-evidence-download]")
    need("m01:lab" in units() and page.locator("[data-lab-complete]").is_visible()
         and any(e["unit"] == "m01:lab" and e["kind"] == "completed" for e in events()),
         "lab-m01: exporting the filled-in evidence entry did not complete the lab")
    for lp in sorted(SITE.glob("lab-m*.html")):
        page.goto(f"{base}/{lp.name}")
        section = page.locator("#auto-fail")
        need(section.count() == 1 and section.is_visible() and section.locator("li").count() >= 3,
             f"{lp.name}: the rubric's auto-fail list is not shown exactly once")
        # The lab's header block is its brief, shown whole: every line of it is on the page (it once
        # mined three fields and dropped the rest, the pass gate included).
        src = next(COURSE.glob(f"03-content/{lp.stem[4:]}-*/lab.md")).read_text(encoding="utf-8").splitlines()[1:]
        quoted = []
        for l in src:
            if l.strip().startswith(">"):
                if l.strip("> ").strip():
                    quoted.append(l)
            elif l.strip():
                break
        need(page.locator(".lab-brief p").count() == len(quoted),
             f"{lp.name}: the brief shows {page.locator('.lab-brief p').count()} of the {len(quoted)} header lines")
        # One page (#110): every step shown in full, in order, then the checklist — nothing paged,
        # nothing in a scrolling side panel.
        steps = page.locator(".lab-step")
        shown = sum(1 for i in range(steps.count()) if steps.nth(i).is_visible())
        need(steps.count() >= 3 and page.locator(".lab-steps [data-step-go]").count() == steps.count()
             and shown == steps.count(),
             f"{lp.name}: not one page ({steps.count()} steps, {shown} shown)")
        boxed = page.evaluate("""() => [...document.querySelectorAll('.lab-root *')].filter(e => {
            const s = getComputedStyle(e); return /(auto|scroll)/.test(s.overflowY) && e.scrollHeight > e.clientHeight + 2
              && !e.matches('pre, textarea'); }).length""")
        need(page.locator(".lab-accept [data-check]").count() > 0 and boxed == 0,
             f"{lp.name}: the checklist is missing, or {boxed} part(s) of the lab scroll inside a box")
    # A step's own toggle marks it done, and that survives a reload.
    page.goto(f"{base}/lab-m05.html")
    page.locator(".lab-step").nth(1).locator("[data-step-done]").click()
    page.reload()
    need(page.locator(".lab-step").nth(1).locator("[data-step-done]").get_attribute("aria-pressed") == "true"
         and "is-done" in (page.locator('[data-step-go="1"]').get_attribute("class") or ""),
         "lab-m05: marking a step done did not persist")

    # Search is a command palette (#80): "/" and Ctrl/⌘+K open it from any page; results come back
    # grouped by kind with the matched words marked; ↓ ↵ open a result; every glossary term is found
    # by its name; a slide found by its narration opens the player where the sentence is spoken.
    page.goto(f"{base}/index.html")
    page.keyboard.press("/")
    page.wait_for_timeout(200)
    need(page.locator("dialog.search-dialog").evaluate("d => d.open"), "search: '/' did not open it")
    page.keyboard.type("fail-closed")
    page.wait_for_timeout(600)
    need(page.locator('[data-group="glossary"] .search-hit').count() >= 1
         and page.locator('[data-group="slides"] .search-hit').count() >= 1
         and page.locator(".search-results mark").count() >= 2,
         "search: 'fail-closed' did not return a glossary term and a slide, with the match marked")
    # A multi-word term opens on its own entry, not on the slides that mention its words.
    page.fill("#aps-search-input", "contract test")
    page.wait_for_timeout(400)
    first = page.eval_on_selector_all(".search-hit", "as => as.slice(0, 1).map(a => a.getAttribute('href'))")
    need(first and first[0].endswith("glossary-m03.html#contract-test"),
         f"search: 'contract test' does not open on its glossary entry (first hit {first})")
    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    try:
        page.wait_for_url("**/glossary-m03.html#contract-test", timeout=5000)
    except Exception:                                   # noqa: BLE001 - reported just below
        pass
    need(page.url.endswith("glossary-m03.html#contract-test"), f"search: ↓ ↵ did not open the first hit ({page.url})")
    for where in ("lab-m03.html", "m02.html"):
        page.goto(f"{base}/{where}")
        page.wait_for_timeout(300)
        page.keyboard.press("Control+k")
        page.wait_for_timeout(200)
        need(page.locator("dialog.search-dialog").evaluate("d => d.open"), f"search: Ctrl+K did not open it on {where}")
        page.keyboard.press("Escape")
    missed = page.evaluate("""async () => {
      const idx = await fetch('search.json').then(r => r.json());
      const miss = [];
      for (const t of idx.filter(x => x.k === 'term')) {
        const r = await window.APSSearch.query(t.t);
        const g = r.groups.find(g => g.key === 'glossary');
        if (!g || !g.items.some(h => h.it.h === t.h)) miss.push(t.t);
      }
      return miss;
    }""")
    need(not missed, f"search: {len(missed)} glossary terms are not found by their own name ({missed[:5]})")
    spoken = page.evaluate("""async () => {
      const idx = await fetch('search.json').then(r => r.json());
      const s = idx.find(x => x.k === 'slide' && x.ts && x.s.length > 3);
      if (!s) return null;
      const r = await window.APSSearch.query(s.s[3].split(' ').slice(0, 6).join(' '));
      return { want: s.h, hits: [].concat(...r.groups.map(g => g.items.map(h => h.it.h))) };
    }""")
    if spoken:
        page.keyboard.press("Control+k")
        page.wait_for_timeout(200)
        page.keyboard.type(page.evaluate("""async () => {
          const idx = await fetch('search.json').then(r => r.json());
          return idx.find(x => x.k === 'slide' && x.ts && x.s.length > 3).s[3].split(' ').slice(0, 6).join(' ');
        }"""))
        page.wait_for_timeout(500)
        hrefs = page.eval_on_selector_all(".search-hit[data-kind=slide]", "as => as.map(a => a.getAttribute('href'))")
        timed = next((h for h in hrefs if "?t=" in h and h.endswith(spoken["want"].split("#")[1])), None)
        need(timed, f"search: a slide found by a spoken sentence does not open at its time ({hrefs[:3]})")
        if timed:
            page.keyboard.press("Escape")
            page.goto(f"{base}/{timed.lstrip('./')}")
            page.wait_for_timeout(700)
            need("Starts at" in page.locator("[data-status]").inner_text(),
                 "player: opened from a spoken-sentence hit, it does not say where it starts")

    # Reading pages: a table of contents, and pointers linked at a pinned commit.
    for kind in ("lesson", "handout", "glossary"):
        built = len(list(SITE.glob(f"{kind}-m*.html")))
        need(built == len(quiz_pages), f"{built} {kind} pages for {len(quiz_pages)} modules")
    page.goto(f"{base}/lesson-m03.html")
    pinned = re.findall(r'href="https://github\.com/[^"]+/blob/[0-9a-f]{7,40}/', page.content())
    need(len(pinned) >= 5 and page.locator("nav.toc, .toc, [data-toc]").count(),
         f"lesson-m03: {len(pinned)} pinned pointer links, or no table of contents")

    # Home (#79). A returning learner lands on the resume point in one click; the proof numbers are
    # the build's own; the full proof, with its sources, is one link away.
    page.goto(f"{base}/index.html")
    last = page.evaluate("window.APSProgress.get().last.href")
    resume = page.locator("[data-resume-link]")
    need(page.locator("[data-home]").is_visible() and resume.get_attribute("href").endswith(last),
         f"home: the resume card does not point at the stored position ({last})")
    built = json.loads((SITE / "proof.json").read_text(encoding="utf-8"))
    shown = page.locator("[data-home] .proof-value").all_inner_texts()
    want = [f"{built['pointers']['checked']:,}", f"{built['pointers']['anchors']:,}", f"{built['narration']['recorded']:,}"]
    need(shown == want, f"home: the proof numbers {shown} are not the build's {want}")
    resume.click()
    page.wait_for_selector(".slide[aria-current]")
    need(page.url.endswith(last) and page.evaluate("document.querySelector('.slide[aria-current]').id") == last.split("#")[1],
         "home: Resume did not land on the stored slide")
    page.goto(f"{base}/proof.html")
    need(len(page.eval_on_selector_all(".proof a", "as => as.map(a => a.href)")) >= 3,
         "proof: the proof section links fewer than three sources")
    # A first-time visitor sees the pitch and the first-win start, not a resume card.
    newcomer = browser.new_context(viewport={"width": 1280, "height": 900}).new_page()
    newcomer.goto(f"{base}/index.html")
    need(newcomer.locator("[data-home]").is_hidden()
         and newcomer.locator('[data-home-new] a[href$="lab-m00.html"]').is_visible(),
         "home: a first-time visitor is not offered the first-win start")
    newcomer.close()
    # Figures build on the narration (#99): a stepped figure opens complete, Replay (or ".") takes it
    # back to its first part and builds it one step at a time to complete, and under reduced motion
    # it never hides a part. In Read the same figure heads its segment, complete, with no steps.
    pending = "document.querySelectorAll('.slide[aria-current] .fig [data-step].is-pending').length"
    page.goto(f"{base}/m02.html#slide-3")
    page.wait_for_timeout(300)
    steps = page.evaluate("document.querySelectorAll('.slide[aria-current] .fig [data-step]').length")
    need(steps >= 3, f"m02 slide-3: the stepped figure has {steps} build steps")
    need(page.evaluate(pending) == 0, "m02 slide-3: a stepped figure does not open complete")
    need(page.locator("[data-fig-replay]").is_visible(), "m02 slide-3: no Replay figure control")
    page.locator(".slide[aria-current] h2, .slide[aria-current] h1").first.click()
    page.keyboard.press(".")
    page.wait_for_timeout(200)
    need(page.evaluate(pending) == steps, "m02 slide-3: '.' did not take the figure back to its first part")
    page.wait_for_timeout(1500)
    mid = page.evaluate(pending)
    need(0 < mid < steps, f"m02 slide-3: the replay did not build step by step ({mid} of {steps} pending)")
    page.wait_for_timeout(900 * steps + 600)
    need(page.evaluate(pending) == 0, "m02 slide-3: the replay did not finish complete")
    page.goto(f"{base}/m02.html#slide-4")
    need(page.locator("[data-fig-replay]").is_hidden(), "m02 slide-4: Replay figure shown on a slide with no stepped figure")
    calm = browser.new_context(viewport={"width": 1280, "height": 900}, reduced_motion="reduce").new_page()
    calm.goto(f"{base}/m02.html#slide-3")
    calm.keyboard.press(".")
    calm.wait_for_timeout(300)
    need(calm.evaluate(pending) == 0, "m02 slide-3: reduced motion still hides figure parts")
    calm.close()
    # A numbered procedure is a left-aligned stepper: each step's text starts beside its number,
    # not centred across a full-width row (the M0.3 bug).
    page.goto(f"{base}/m00.html#slide-12")
    page.wait_for_timeout(300)
    gap = page.evaluate("""() => { const n = document.querySelector('.slide[aria-current] .fig-track.is-numbered .fig-node');
        return n ? n.querySelector('.fig-label').getBoundingClientRect().left - n.getBoundingClientRect().left : -1; }""")
    need(0 <= gap < 60, f"m00 slide-12: a numbered step's text starts {gap}px into its row — not left-aligned")
    page.goto(f"{base}/lesson-m02.html")
    need(page.locator(".doc-article [data-figure]").count() >= 1
         and page.locator(".doc-article [data-figure] [data-step]").count() == 0,
         "lesson-m02: the segment figure is missing from Read, or carries build steps")

    # Landing: a phone-width page with no sideways scroll.
    page.goto(f"{base}/index.html")
    phone = browser.new_context(viewport={"width": 390, "height": 844}).new_page()
    phone.goto(f"{base}/index.html")
    overflow = phone.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    need(overflow <= 0, f"index at 390px scrolls sideways by {overflow}px")
    # The phone (#81), 390x844: the player and a lab work with no sideways scroll, the modes are a
    # bottom tab bar, and every visible control is a 44px touch target.
    handset = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True).new_page()
    small_js = """() => [...document.querySelectorAll('button, select, .mode-switch a, .card-action, .lab-steps a')]
      .filter(e => { const r = e.getBoundingClientRect(), s = getComputedStyle(e);
        return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && r.height < 43.5; })
      .map(e => (e.getAttribute('aria-label') || e.textContent || e.tagName).trim().slice(0, 30))"""
    for path in ("m02.html#slide-9", "lab-m02.html", "module-m02.html", "quiz-m02.html", "lesson-m02.html", "index.html"):
        handset.goto(f"{base}/{path}")
        handset.wait_for_timeout(400)
        overflow = handset.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        need(overflow <= 0, f"{path} at 390px scrolls sideways by {overflow}px")
        small = handset.evaluate(small_js)
        need(not small, f"{path} at 390px: controls under 44px tall: {small[:4]}")
        if path != "index.html":
            bar = handset.locator(".app-bar .mode-switch")
            box = bar.bounding_box()
            need(box and abs(box["y"] + box["height"] - 844) <= 1 and bar.locator("a").count() == 4,
                 f"{path} at 390px: the four modes are not a bottom tab bar")
    # No page scrolls sideways on a phone — every built page, not a sample: a single unbroken word in
    # one lesson heading was enough to push a page 175px wide.
    wide = []
    for built in sorted(p for p in SITE.glob("*.html") if not p.name.startswith("_")):
        handset.goto(f"{base}/{built.name}", wait_until="domcontentloaded")
        over = handset.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        if over > 0:
            wide.append(f"{built.name} (+{over}px)")
    need(not wide, f"at 390px these pages scroll sideways: {wide[:6]}")
    handset.goto(f"{base}/m02.html#slide-9")
    handset.wait_for_timeout(400)
    slide = handset.locator(".slide[aria-current]").bounding_box()
    handset.locator("[data-play]").scroll_into_view_if_needed()
    play = handset.locator("[data-play]").bounding_box()
    need(slide and slide["width"] >= 360 and play and play["width"] >= 44 and play["height"] >= 44,
         "player at 390px: the slide is not full width, or Play is not a 44px target")
    handset.close()
    print(f"  played {played} knowledge-check questions, {len(list(SITE.glob('lab-m*.html')))} lab pages")
    return problems


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--print-skip", action="store_true",
                        help="exit 0 with a note when Playwright or a browser is missing")
    args = parser.parse_args(argv)
    try:
        from playwright.sync_api import sync_playwright   # noqa: PLC0415
    except ImportError:
        print("site features: skipped — `pip install playwright` to run them")
        return 0 if args.print_skip else 2
    if not (SITE / "index.html").exists():
        print("site features: no built site here — run `make -C .. site` first")
        return 1
    from check_player import find_browser               # noqa: PLC0415

    handler = functools.partial(_Quiet, directory=str(SITE))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    errors: list[str] = []
    try:
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch()
            except Exception:                                # noqa: BLE001 - fall back to a found binary
                exe = find_browser()
                if not exe:
                    print("site features: skipped — no Chromium found")
                    return 0 if args.print_skip else 2
                browser = p.chromium.launch(executable_path=exe)
            page = browser.new_context(viewport={"width": 1280, "height": 900}).new_page()
            page.on("pageerror", lambda e: errors.append(str(e)))
            problems = run(page, browser, base)
            browser.close()
    finally:
        server.shutdown()
    problems += [f"page error: {e}" for e in errors]
    for p_ in problems:
        print(f"  ✗ {p_}")
    print("site features:", "PASS" if not problems else f"FAIL ({len(problems)})")
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
