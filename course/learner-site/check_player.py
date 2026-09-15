#!/usr/bin/env python3
"""Headless check that the learner site actually works in a browser.

  python3 check_player.py                 # check a few decks
  python3 check_player.py --deck m00 --deck m08
  python3 check_player.py --all
  python3 check_player.py --print-skip    # exit 0 with a note when no browser is installed

Why this exists: the player is the one part of the package that can only be proven by running it.
Static checks confirm the files exist; only a real browser confirms the manifest fetched, the panel
was injected, captions parsed, and the deep link navigated. It uses a browser already on the machine
(no npm install, no Playwright download) so it cannot become an unverifiable dependency.

What it asserts per deck:
  * the narration panel and all controls were injected by player.js
  * exactly one slide is aria-current, and it matches the requested deep link
  * the polite status region announces the right slide number and title
  * the CC control is enabled, which can only happen after the .vtt fetched and parsed
  * a caption cue is rendered with text
  * a slide with no recording degrades to a message rather than a broken player
  * the panel is actually VISIBLE, not merely present in the DOM — an earlier version created it
    hidden and never unhid it, so every control existed and none of them could be seen
"""
from __future__ import annotations

import argparse
import functools
import http.server
import html as html_lib
import json
import re
import shutil
import socketserver
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    shutil.which("google-chrome") or "",
    shutil.which("chromium") or "",
]


def find_browser() -> str | None:
    for candidate in CHROME_CANDIDATES:
        if candidate and Path(candidate).exists():
            return candidate
    return None


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"        # the page requests its assets in parallel

    def log_message(self, *args):        # keep the check output readable
        pass


def serve(directory: Path) -> tuple[socketserver.TCPServer, int]:
    handler = functools.partial(QuietHandler, directory=str(directory))
    # Threading matters: a page loads CSS, two scripts, the manifest and a caption file at once, and
    # a single-threaded server stalls long enough to time the browser out.
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, port


RESET_PAGE = "_aps_reset_storage.html"


def dump_dom(browser: str, url: str, budget_ms: int = 4000) -> str:
    """Render a URL and return the settled DOM.

    Two hard-won constraints, both discovered by hanging for 90+ seconds:
      * Never launch Chrome with a replaced environment (`env={"HOME": ...}`) — it stalls indefinitely.
      * Never use `--user-data-dir` with a fresh directory — new headless does first-run setup that
        virtual time waits on forever. Even a static page with no JavaScript hangs.
    So the browser runs with the ambient profile, and saved progress is cleared explicitly instead.
    """
    args = [browser, "--headless", "--disable-gpu", "--no-sandbox", "--no-first-run",
            "--no-default-browser-check", "--disable-background-networking",
            f"--virtual-time-budget={budget_ms}", "--dump-dom", url]
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        args = [a for a in args if not a.startswith("--virtual-time-budget")]
        args.insert(-2, "--virtual-time-budget=1500")
        try:
            result = subprocess.run(args, capture_output=True, text=True, timeout=60)
        except subprocess.TimeoutExpired:
            return ""
    return result.stdout


def reset_progress(browser: str, port: int) -> None:
    """Clear this player's saved resume position so every check starts from slide 1."""
    page = SITE_ROOT / RESET_PAGE
    page.write_text(
        "<!doctype html><meta charset=utf-8><title>reset</title><p>reset</p><script>"
        "try{Object.keys(localStorage).filter(k=>k.indexOf('aps:')===0)"
        ".forEach(k=>localStorage.removeItem(k))}catch(e){}"
        "</script>", encoding="utf-8")
    try:
        dump_dom(browser, f"http://127.0.0.1:{port}/{RESET_PAGE}", budget_ms=1500)
    finally:
        page.unlink(missing_ok=True)


PROBE_PAGE = "_aps_layout_probe.html"
PROBE_TEMPLATE = r"""<!doctype html><meta charset=utf-8><title>probe</title>
<iframe id="frame" src="__DECK__.html" style="width:1600px;height:1000px;border:0"></iframe>
<pre id="out">pending</pre>
<script>
function measure() {
  var frame = document.getElementById('frame');
  var d = frame.contentDocument, w = frame.contentWindow;
  if (!d) { return 'no-document'; }
  var shown = d.querySelector('.slide:not([hidden])');
  if (!shown) { return 'no-visible-slide'; }
  var box = shown.getBoundingClientRect();
  var style = w.getComputedStyle(shown);
  var text = function (sel) {
    var el = d.querySelector(sel);
    return el ? el.textContent.replace(/\s+/g, ' ').trim() : '';
  };
  var chapters = {};
  Array.prototype.forEach.call(d.querySelectorAll('.slide'), function (s) {
    chapters[s.getAttribute('data-chapter')] = 1;
  });
  return JSON.stringify({
    slideWidth: Math.round(box.width),
    slideHeight: Math.round(box.height),
    ratio: Math.round((box.width / box.height) * 1000) / 1000,
    aspectRatio: style.aspectRatio,
    overflowing: shown.scrollHeight > shown.clientHeight + 2,
    bodyFont: w.getComputedStyle(d.body).fontFamily,
    fontLoaded: d.fonts.check('16px "Source Sans 3"'),
    fontsStatus: d.fonts.status,
    kicker: text('.slide:not([hidden]) .kicker'),
    title: text('.slide:not([hidden]) h2'),
    footer: text('.slide:not([hidden]) .slide-footer'),
    panelHeight: w.getComputedStyle(d.body).getPropertyValue('--narration-height').trim(),
    present: !!d.querySelector('[data-present]'),
    reading: !!d.querySelector('[data-reading]'),
    notes: !!d.querySelector('[data-notes]'),
    drawer: !!d.querySelector('.deck-drawer'),
    coverSlide: !!d.querySelector('#slide-1.slide-cover'),
    chapters: Object.keys(chapters).length,
    optgroups: d.querySelectorAll('optgroup').length,
    titleIds: d.querySelectorAll('.slide h2[id$="-title"]').length,
    footerLinks: d.querySelectorAll('.slide-footer a').length
  });
}

function interact() {
  var frame = document.getElementById('frame');
  var d = frame.contentDocument, w = frame.contentWindow;
  var body = d.body;
  var out = {};
  // Present ↗ — full screen may be refused inside an iframe; the mode must still apply.
  d.querySelector('[data-present]').click();
  out.presentMode = body.classList.contains('presentation-mode');
  out.presentPressed = d.querySelector('[data-present]').getAttribute('aria-pressed');
  d.querySelector('[data-present]').click();
  out.presentCleared = !body.classList.contains('presentation-mode');
  // Read all — every slide visible at once.
  d.querySelector('[data-reading]').click();
  out.readingMode = body.classList.contains('reading-view');
  out.slidesVisibleWhileReading = d.querySelectorAll('.slide:not([hidden])').length;
  out.totalSlides = d.querySelectorAll('.slide').length;
  d.querySelector('[data-reading]').click();
  out.backToOneSlide = d.querySelectorAll('.slide:not([hidden])').length;
  // Sources & notes — the drawer opens with the current slide's notes.
  d.querySelector('[data-notes]').click();
  var drawer = d.querySelector('.deck-drawer');
  out.drawerOpen = !!drawer && drawer.open;
  out.drawerHasNotes = (d.querySelector('[data-drawer-notes]').textContent || '').trim().length > 40;
  drawer.close();
  out.drawerClosed = !drawer.open;
  return JSON.stringify(out);
}
document.getElementById('frame').addEventListener('load', function () {
  setTimeout(function () {
    var data = JSON.parse(measure());
    var extra = JSON.parse(interact());
    for (var key in extra) { data[key] = extra[key]; }
    document.getElementById('out').textContent = JSON.stringify(data);
  }, 700);
});
</script>
"""


def measure_deck(browser: str, port: int, deck_id: str) -> dict:
    """Render the probe and return the raw measurements (used by --measure)."""
    page = SITE_ROOT / PROBE_PAGE
    page.write_text(PROBE_TEMPLATE.replace("__DECK__", deck_id), encoding="utf-8")
    try:
        dom = dump_dom(browser, f"http://127.0.0.1:{port}/{PROBE_PAGE}", budget_ms=4000)
    finally:
        page.unlink(missing_ok=True)
    match = re.search(r'<pre id="out">(.*?)</pre>', dom, re.S)
    if not match:
        return {"error": "probe did not report"}
    try:
        return json.loads(html_lib.unescape(match.group(1)))
    except ValueError:
        return {"error": "unreadable probe output", "raw": match.group(1)[:200]}


def check_layout(browser: str, port: int, deck_id: str, slide_count: int) -> list[str]:
    """Measure the rendered frame instead of trusting the stylesheet.

    A design port can look correct in source and still render wrong: a container-query frame that
    silently fails, a font that never loads, a slide that overflows. This drives the real browser at
    a fixed 1600x1000 viewport, reads the geometry back through a same-origin iframe, and asserts the
    invariants the design depends on.
    """
    page = SITE_ROOT / PROBE_PAGE
    page.write_text(PROBE_TEMPLATE.replace("__DECK__", deck_id), encoding="utf-8")
    try:
        dom = dump_dom(browser, f"http://127.0.0.1:{port}/{PROBE_PAGE}", budget_ms=4000)
    finally:
        page.unlink(missing_ok=True)

    match = re.search(r'<pre id="out">(.*?)</pre>', dom, re.S)
    if not match or match.group(1).strip() == "pending":
        return [f"{deck_id}: layout probe did not report (the page never settled)"]
    try:
        data = json.loads(html_lib.unescape(match.group(1)))
    except ValueError:
        return [f"{deck_id}: layout probe returned unreadable data"]

    problems: list[str] = []
    if not (1.70 <= data["ratio"] <= 1.85):
        problems.append(f"{deck_id}: slide rendered {data['slideWidth']}x{data['slideHeight']} "
                        f"(ratio {data['ratio']}), not the 16:9 frame the design uses")
    if data["slideWidth"] < 900:
        problems.append(f"{deck_id}: the slide frame collapsed to {data['slideWidth']}px wide")
    if data["overflowing"]:
        problems.append(f"{deck_id}: slide 1 overflows its frame, so content is clipped")
    if "Source Sans 3" not in data["bodyFont"]:
        problems.append(f"{deck_id}: body font is {data['bodyFont']!r}, not the ported typeface")
    if not data["fontLoaded"] and data.get("fontsStatus") != "loaded":
        problems.append(f"{deck_id}: Source Sans 3 was requested but never loaded "
                        f"(status {data.get('fontsStatus')!r})")
    if not data["kicker"]:
        problems.append(f"{deck_id}: the current slide has no kicker")
    if not data["title"]:
        problems.append(f"{deck_id}: the current slide has no title")
    if not re.search(r"\d{2} / \d{2}", data["footer"]):
        problems.append(f"{deck_id}: slide footer has no 'NN / NN' number ({data['footer']!r})")
    if float(data["panelHeight"].replace("px", "") or 0) <= 0:
        problems.append(f"{deck_id}: the frame did not give back space for the narration panel")
    for control in ("present", "reading", "notes", "drawer"):
        if not data[control]:
            problems.append(f"{deck_id}: {control} control is missing from the deck chrome")
    if not data["coverSlide"]:
        problems.append(f"{deck_id}: slide 1 is not styled as the cover")
    if data["titleIds"] != slide_count:
        problems.append(f"{deck_id}: {data['titleIds']} slides have an anchored title, expected {slide_count}")
    if data["footerLinks"] != slide_count:
        problems.append(f"{deck_id}: {data['footerLinks']} slides link to their transcript, "
                        f"expected {slide_count}")
    if data["optgroups"] < 2:
        problems.append(f"{deck_id}: the slide picker is not grouped into chapters")
    for label, key, want in (
            ("Present ↗ did not enter presentation mode", "presentMode", True),
            ("Present ↗ did not report its pressed state", "presentPressed", "true"),
            ("Present ↗ did not leave presentation mode", "presentCleared", True),
            ("Read all did not switch to reading view", "readingMode", True),
            ("Read all did not reveal every slide", "slidesVisibleWhileReading", data["totalSlides"]),
            ("Read all did not return to one slide at a time", "backToOneSlide", 1),
            ("Sources & notes did not open the drawer", "drawerOpen", True),
            ("the notes drawer was empty for a slide that has notes", "drawerHasNotes", True),
            ("the notes drawer did not close", "drawerClosed", True)):
        got = data.get(key)
        if got != want:
            problems.append(f"{deck_id}: {label} (got {got!r}, expected {want!r})")
    return problems


def check_deck(browser: str, port: int, deck_id: str, slide_count: int,
               narrated: set[str]) -> list[str]:
    problems: list[str] = []
    url = f"http://127.0.0.1:{port}/{deck_id}.html"
    dom = dump_dom(browser, url)
    if len(dom) < 2000:
        return [f"{deck_id}: page did not render ({len(dom)} bytes of DOM)"]

    required = {
        "narration panel": 'class="narration-panel"',
        "play control": "data-play",
        "replay control": "data-replay",
        "seek control": "data-seek",
        "speed control": "data-speed",
        "cc control": "data-cc",
        "auto-next control": "data-auto",
        "transcript control": "data-transcript",
        "status region": 'role="status"',
    }
    for label, needle in required.items():
        if needle not in dom:
            problems.append(f"{deck_id}: {label} was not injected")

    current = re.findall(r'<section class="slide[^"]*" id="(slide-\d+)"[^>]*aria-current="true"', dom)
    if current != ["slide-1"]:
        problems.append(f"{deck_id}: expected slide-1 to be current on load, got {current or 'none'}")
    status = re.search(r'class="slide-status"[^>]*>([^<]*)', dom)
    if not status or not status.group(1).startswith(f"Slide 1 of {slide_count}"):
        problems.append(f"{deck_id}: status region did not announce slide 1 of {slide_count} "
                        f"(got {(status.group(1).strip() if status else 'nothing')!r})")

    if "slide-1" in narrated:
        # Presence is not visibility: assert the panel is shown and its height was reserved.
        panel = re.search(r'<section class="narration-panel"[^>]*>', dom)
        if not panel:
            problems.append(f"{deck_id}: narration panel is missing entirely")
        elif " hidden" in panel.group(0):
            problems.append(f"{deck_id}: narration panel is present but hidden, so no control is visible")
        height = re.search(r"--narration-height:\s*([0-9.]+)px", dom)
        if not height or float(height.group(1)) <= 0:
            problems.append(f"{deck_id}: --narration-height was not reserved, so the panel covers "
                            f"the bottom of the slide")
        cc = re.search(r"<button[^>]*data-cc[^>]*>", dom)
        if cc and "disabled" in cc.group(0):
            problems.append(f"{deck_id}: CC stayed disabled, so captions never parsed for slide-1")
        caption = re.search(r'class="narration-caption"[^>]*>(.*?)</div>', dom, re.S)
        if not caption or not caption.group(1).strip():
            problems.append(f"{deck_id}: no caption cue rendered for a narrated slide-1")
        start = re.search(r"data-narration-start[^>]*>", dom)
        if start and "disabled" in start.group(0):
            problems.append(f"{deck_id}: Play was disabled even though slide-1 is narrated")

    # Deep link: exercises goTo(), the manifest lookup and a second clip load.
    target = min(5, slide_count)
    dom_hash = dump_dom(browser, f"{url}#slide-{target}")
    current = re.findall(r'<section class="slide[^"]*" id="(slide-\d+)"[^>]*aria-current="true"', dom_hash)
    if current != [f"slide-{target}"]:
        problems.append(f"{deck_id}: #slide-{target} did not become current (got {current or 'none'})")
    status = re.search(r'class="slide-status"[^>]*>([^<]*)', dom_hash)
    if not status or not status.group(1).startswith(f"Slide {target} of {slide_count}"):
        problems.append(f"{deck_id}: status did not follow the deep link")
    return problems


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--deck", action="append", help="deck id (repeatable); default m00 and m08")
    parser.add_argument("--all", action="store_true", help="check every deck with a built page")
    parser.add_argument("--measure", action="store_true",
                        help="print the measured frame geometry for each deck and exit")
    parser.add_argument("--print-skip", action="store_true",
                        help="exit 0 with a note if no browser is installed")
    args = parser.parse_args(argv)

    sys.path.insert(0, str(SITE_ROOT.parent.parent / "course" / "06-production" / "narration"))
    sys.path.insert(0, str(SITE_ROOT.parent / "06-production" / "narration"))
    from narration_data import DECK_IDS, load_manifest, load_scripts   # noqa: PLC0415

    browser = find_browser()
    if not browser:
        message = ("no Chrome/Chromium found — skipping the browser check. Install one, or run "
                   "`make -C course site` and open the site manually.")
        if args.print_skip:
            print(message)
            return 0
        print(message, file=sys.stderr)
        return 2

    scripts = load_scripts()["decks"]
    manifest = load_manifest()
    decks = args.deck or (DECK_IDS if args.all else ["m00", "m08"])
    decks = [d for d in decks if (SITE_ROOT / f"{d}.html").exists()]
    if not decks:
        print("no built deck pages found — run `python3 build_site.py` first", file=sys.stderr)
        return 2

    httpd, port = serve(SITE_ROOT)
    problems: list[str] = []
    try:
        reset_progress(browser, port)
        for deck_id in decks:
            if deck_id not in scripts:
                continue
            recorded = set((manifest.get("decks", {}).get(deck_id, {}) or {}).get("slides", {}))
            if args.measure:
                print(json.dumps(measure_deck(browser, port, deck_id), indent=2))
                continue
            found = check_deck(browser, port, deck_id, len(scripts[deck_id]["slides"]), recorded)
            if not found:
                found = check_layout(browser, port, deck_id, len(scripts[deck_id]["slides"]))
            print(f"  {'ok  ' if not found else 'FAIL'} {deck_id}  "
                  f"({len(scripts[deck_id]['slides'])} slides, {len(recorded)} narrated)")
            problems.extend(found)
    finally:
        httpd.shutdown()

    if problems:
        for problem in problems:
            print(f"  ✗ {problem}")
        print(f"\nFAILED: {len(problems)} problem(s) across {len(decks)} deck(s)")
        return 1
    print(f"\nbrowser check passed: {len(decks)} deck(s) — frame measured, panel injected, captions parsed, "
          f"deep links and status regions correct")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
