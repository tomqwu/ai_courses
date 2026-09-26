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

    # Progress: a first visit offers no "continue"; ticks survive a reload; the deck marks units;
    # the cards and the landing page reflect it; the learner can export it.
    page.goto(f"{base}/index.html")
    need(page.locator("[data-continue]").is_hidden(), "index: a first visit shows 'continue'")
    # A module's landing point (#74): a first visit is offered the start, at the top of the page.
    page.goto(f"{base}/module-m02.html")
    start = page.locator("[data-start-link]")
    need(start.inner_text().strip() == "Start module" and (start.get_attribute("href") or "").endswith("m02.html#slide-1")
         and start.bounding_box()["y"] < 900,
         "module-m02: a first visit is not offered 'Start module' above the fold")
    page.goto(f"{base}/module-m01.html")
    page.check('[data-progress="m01:intro"]')
    page.reload()
    need(page.is_checked('[data-progress="m01:intro"]'), "module page: a ticked unit did not survive a reload")
    page.goto(f"{base}/m02.html")
    for _ in range(40):
        if any(k.startswith("m02:") for k in units()):
            break
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(100)
    need(any(k.startswith("m02:") for k in units()), "deck: paging through M2 marked no unit done")
    page.goto(f"{base}/index.html")
    need(page.locator("[data-continue]").is_visible(), "index: a returning visit shows no 'continue'")
    rings = page.eval_on_selector_all("[data-ring-units]", "els => els.map(e => e.getAttribute('aria-label'))")
    need(any(r and not r.startswith("0 of") for r in rings), f"index: no progress ring reflects progress ({rings[:3]})")
    need('"m01:intro"' in page.evaluate("window.APSProgress.exportJSON()"), "progress export lacks a ticked unit")

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
            need(re.findall(r">([^<]+)</a>", modes) == ["Watch", "Read", "Lab", "Check"],
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
            current = re.search(r'<nav class="mode-switch".*?<a [^>]*aria-current="page"[^>]*>([^<]+)</a>',
                                path.read_text(encoding="utf-8"), re.S)
            need((current.group(1) if current else None) == mode,
                 f"{path.name}: shows mode {current.group(1) if current else None!r}, expected {mode!r}")
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
    need(page.locator('.mode-switch a[aria-current="page"]').inner_text().strip() == "Lab",
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
    page.fill('[data-evidence="project"]', "my-studio")
    page.fill('[data-evidence="commands"]', "python3 -m pytest tests/ -q → 2 passed")
    out = page.input_value("[data-evidence-out]")
    need(out.startswith("## Evidence — my-studio —") and "Commands (with results):\n- python3 -m pytest" in out
         and "Environment:" in out and "Revision:" in out and "Limitations / not verified:" in out,
         f"lab-m01: evidence export is not in the Module 1 format: {out[:120]!r}")
    for lp in sorted(SITE.glob("lab-m*.html")):
        page.goto(f"{base}/{lp.name}")
        section = page.locator("#auto-fail")
        need(section.count() == 1 and section.is_visible() and section.locator("li").count() >= 3,
             f"{lp.name}: the rubric's auto-fail list is not shown exactly once")
        # The workspace (#77): a step list and its steps, one shown at a time, with the checklist and
        # the auto-fail list in the panel beside them.
        steps = page.locator(".lab-step")
        shown = sum(1 for i in range(steps.count()) if steps.nth(i).is_visible())
        need(steps.count() >= 3 and page.locator(".lab-steps [data-step-go]").count() == steps.count() and shown == 1,
             f"{lp.name}: not a workspace ({steps.count()} steps, {shown} shown)")
        need(page.locator(".lab-panel #auto-fail").count() == 1 and page.locator(".lab-panel [data-check]").count() > 0,
             f"{lp.name}: the checklist and auto-fail list are not in the panel beside the steps")
    # A step is marked done and the next one opens; both survive a reload; a deep link opens a step.
    page.goto(f"{base}/lab-m05.html")
    first = page.locator(".lab-step:visible").get_attribute("id")
    page.locator(".lab-step:visible [data-step-next]").click()
    second = page.locator(".lab-step:visible").get_attribute("id")
    page.reload()
    need(second != first and page.locator(".lab-step:visible").get_attribute("id") == second
         and "is-done" in (page.locator('[data-step-go="0"]').get_attribute("class") or ""),
         f"lab-m05: 'Mark done, next step' did not move on and persist ({first} → {second})")
    target = page.locator(".lab-step").nth(3).get_attribute("id")
    page.goto(f"{base}/lab-m05.html#{target}")
    need(page.locator(".lab-step:visible").get_attribute("id") == target, "lab-m05: a deep link to a step did not open it")

    # Search: "/" opens it; a glossary term comes back with its definition and a slide.
    page.goto(f"{base}/index.html")
    page.keyboard.press("/")
    page.wait_for_timeout(200)
    need(page.locator("dialog.search-dialog").evaluate("d => d.open"), "search: '/' did not open it")
    page.keyboard.type("fail-closed")
    page.wait_for_timeout(600)
    kinds = [k.upper() for k in page.eval_on_selector_all(".search-results a", "as => as.map(a => a.innerText)")]
    need(any(k.startswith(("TERM", "GLOSSARY")) for k in kinds) and any(k.startswith("SLIDE") for k in kinds),
         f"search: 'fail-closed' did not return a term and a slide ({kinds[:3]})")
    # A multi-word term opens on its own entry, not on the slides that mention its words.
    page.fill("#aps-search-input", "contract test")
    page.wait_for_timeout(400)
    first = page.eval_on_selector_all(".search-results a", "as => as.slice(0, 1).map(a => a.getAttribute('href'))")
    need(first and first[0].endswith("glossary-m03.html#contract-test"),
         f"search: 'contract test' does not open on its glossary entry (first hit {first})")
    page.keyboard.press("Escape")

    # Reading pages: a table of contents, and pointers linked at a pinned commit.
    for kind in ("lesson", "handout", "glossary"):
        built = len(list(SITE.glob(f"{kind}-m*.html")))
        need(built == len(quiz_pages), f"{built} {kind} pages for {len(quiz_pages)} modules")
    page.goto(f"{base}/lesson-m03.html")
    pinned = re.findall(r'href="https://github\.com/[^"]+/blob/[0-9a-f]{7,40}/', page.content())
    need(len(pinned) >= 5 and page.locator("nav.toc, .toc, [data-toc]").count(),
         f"lesson-m03: {len(pinned)} pinned pointer links, or no table of contents")

    # Landing: linked proof, and a phone-width page with no sideways scroll.
    page.goto(f"{base}/index.html")
    need(len(page.eval_on_selector_all(".proof a", "as => as.map(a => a.href)")) >= 3,
         "index: the proof strip links fewer than three sources")
    phone = browser.new_context(viewport={"width": 390, "height": 844}).new_page()
    phone.goto(f"{base}/index.html")
    overflow = phone.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    need(overflow <= 0, f"index at 390px scrolls sideways by {overflow}px")
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
