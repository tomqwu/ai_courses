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

    # Knowledge checks: every question on every page, played to its keyed answer.
    quiz_pages = sorted(SITE.glob("quiz-m*.html"))
    need(quiz_pages, "no quiz pages built")
    played = 0
    for qp in quiz_pages:
        page.goto(f"{base}/{qp.name}")
        qs = page.locator(".qq")
        for i in range(qs.count()):
            q, label = qs.nth(i), f"{qp.name} question {i + 1}"
            played += 1
            if "is-mc" in (q.get_attribute("class") or ""):
                key = q.get_attribute("data-answer") or ""
                if q.locator(f'.q-option[data-letter="{key}"]').count() != 1:
                    problems.append(f"{label}: keyed answer {key!r} is not exactly one option")
                    continue
                q.locator(f'.q-option[data-letter="{key}"]').click()
                q.locator("[data-check]").click()
                need(q.locator(".q-explain").is_visible(), f"{label}: no rationale after checking")
            else:
                need(q.locator(".q-explain").is_hidden() and q.locator("[data-reveal]").is_disabled(),
                     f"{label}: model answer reachable before an attempt")
                q.locator("textarea").fill("An attempt long enough to count as one.")
                q.locator("[data-reveal]").click()
        summary = page.locator("[data-summary-text]")
        need(summary.count() and "clears the 75%" in summary.inner_text(),
             f"{qp.name}: all keyed answers did not clear the 75% threshold")
    quizzes = json.loads(page.evaluate("JSON.stringify(window.APSProgress.get().quizzes)"))
    need(len(quizzes) == len(quiz_pages), f"quiz scores reached progress for {len(quizzes)} of {len(quiz_pages)} modules")
    # Keyboard only, wrong answer: the feedback names the key.
    page.goto(f"{base}/quiz-m03.html")
    q = page.locator(".qq.is-mc").first
    key = q.get_attribute("data-answer") or "a"
    wrong = next(l for l in "abcd" if l != key and q.locator(f'.q-option[data-letter="{l}"]').count())
    q.locator(f'.q-option[data-letter="{wrong}"]').focus()
    page.keyboard.press("Space")
    q.locator("[data-check]").focus()
    page.keyboard.press("Enter")
    need(f"keyed answer is {key.upper()}" in q.locator("[data-feedback]").inner_text(),
         "quiz-m03: a keyboard-only wrong answer got no feedback naming the key")

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
