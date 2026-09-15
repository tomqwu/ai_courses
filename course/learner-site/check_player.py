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


CONTRAST_JS = r"""
function apsAuditContrast(w, d) {
  function parse(c) {
    var m = String(c).match(/rgba?\(([^)]+)\)/);
    if (m) { var p = m[1].split(',').map(parseFloat); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }; }
    var h = String(c).match(/^#([0-9a-f]{3}|[0-9a-f]{6})$/i);
    if (h) { var x = h[1];
      if (x.length === 3) { x = x[0]+x[0]+x[1]+x[1]+x[2]+x[2]; }
      return { r: parseInt(x.slice(0,2),16), g: parseInt(x.slice(2,4),16), b: parseInt(x.slice(4,6),16), a: 1 }; }
    return null;
  }
  function stops(img) {
    var out = [], m, re = /rgba?\([^)]+\)|#[0-9a-f]{3,8}/gi;
    while ((m = re.exec(img))) { var c = parse(m[0]); if (c) out.push(c); }
    return out;
  }
  // Walk ancestors to the first painted surface, compositing translucent layers. Gradients are
  // resolved to their colour stops and judged by the WORST stop, so a gradient can never hide a
  // failure. Getting this wrong is how navy-on-navy shipped as 1.00:1 on the landing page.
  function effBg(el) {
    var stack = [], n = el;
    while (n && n.nodeType === 1) {
      var cs = w.getComputedStyle(n);
      if (cs.backgroundImage && cs.backgroundImage !== 'none') {
        var st = stops(cs.backgroundImage);
        if (st.length) return { stops: st };
      }
      var c = parse(cs.backgroundColor);
      if (c && c.a > 0) { stack.push(c); if (c.a >= 1) break; }
      n = n.parentElement;
    }
    if (!stack.length) return { stops: [{ r: 255, g: 255, b: 255, a: 1 }] };
    var base = stack[stack.length - 1];
    for (var i = stack.length - 2; i >= 0; i--) {
      var c = stack[i];
      base = { r: c.r*c.a + base.r*(1-c.a), g: c.g*c.a + base.g*(1-c.a),
               b: c.b*c.a + base.b*(1-c.a), a: 1 };
    }
    return { stops: [base] };
  }
  function lum(c) { function f(v) { v /= 255; return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); }
    return 0.2126*f(c.r) + 0.7152*f(c.g) + 0.0722*f(c.b); }
  function ratio(a, b) { var la = lum(a), lb = lum(b), hi = Math.max(la, lb), lo = Math.min(la, lb);
    return (hi + 0.05) / (lo + 0.05); }
  var slides = Array.prototype.slice.call(d.querySelectorAll('.slide'));
  var was = slides.map(function (s) { return s.hidden; });
  slides.forEach(function (s) { s.hidden = false; });
  var bad = [], measured = 0;
  var walker = d.createTreeWalker(d.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    var node = walker.currentNode;
    if (!node.textContent.trim()) continue;
    var el = node.parentElement;
    if (!el) continue;
    var cs = w.getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) === 0) continue;
    if (!el.getClientRects().length) continue;
    var fg = parse(cs.color);
    if (!fg || fg.a === 0) continue;
    var bg = effBg(el);
    var size = parseFloat(cs.fontSize), weight = parseInt(cs.fontWeight, 10) || 400;
    var large = size >= 24 || (size >= 18.66 && weight >= 700);
    var need = large ? 3.0 : 4.5;
    var worst = Infinity, worstBg = null;
    bg.stops.forEach(function (s) { var r = ratio(fg, s); if (r < worst) { worst = r; worstBg = s; } });
    measured++;
    if (worst < need - 0.005) {
      var sel = el.tagName.toLowerCase();
      if (el.className && typeof el.className === 'string') {
        sel += '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.');
      }
      bad.push({ sel: sel, text: node.textContent.trim().slice(0, 44), colour: cs.color,
                 background: 'rgb(' + Math.round(worstBg.r) + ',' + Math.round(worstBg.g) + ',' + Math.round(worstBg.b) + ')',
                 ratio: Math.round(worst * 100) / 100, need: need, size: cs.fontSize });
    }
  }
  slides.forEach(function (s, i) { s.hidden = was[i]; });
  return { measured: measured, failures: bad };
}
"""

PAGES_PROBE_PAGE = "_aps_pages_probe.html"
PAGES_PROBE_TEMPLATE = (r"""<!doctype html><meta charset=utf-8><title>pages probe</title>
<pre id="out">pending</pre>
<script>
/*CONTRAST*/
var pages = __PAGES__;
var results = [], i = 0;
function next() {
  if (i >= pages.length) { document.getElementById("out").textContent = JSON.stringify(results); return; }
  var page = pages[i++];
  var f = document.createElement("iframe");
  f.style.cssText = "width:1600px;height:1000px;border:0";
  f.src = page;
  f.onload = function () {
    setTimeout(function () {
      try { results.push({ page: page, audit: apsAuditContrast(f.contentWindow, f.contentDocument) }); }
      catch (e) { results.push({ page: page, error: String(e) }); }
      document.body.removeChild(f); next();
    }, 900);
  };
  document.body.appendChild(f);
}
next();
</script>
""")

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
    rail: text('.slide:not([hidden]) .slide-rail'),
    railNum: text('.slide:not([hidden]) .slide-number'),
    panelHeight: w.getComputedStyle(d.documentElement).getPropertyValue('--narration-height').trim(),
    panelBottom: Math.round(d.querySelector('.narration-panel').getBoundingClientRect().bottom),
    panelTop: Math.round(d.querySelector('.narration-panel').getBoundingClientRect().top),
    navTop: Math.round(d.querySelector('.deck-navigation').getBoundingClientRect().top),
    viewportHeight: w.innerHeight,
    present: !!d.querySelector('[data-present]'),
    reading: !!d.querySelector('[data-reading]'),
    notes: !!d.querySelector('[data-notes]'),
    drawer: !!d.querySelector('.deck-drawer'),
    coverSlide: !!d.querySelector('#slide-1.slide-cover'),
    chapters: Object.keys(chapters).length,
    optgroups: d.querySelectorAll('optgroup').length,
    titleIds: d.querySelectorAll('.slide h2[id$="-title"]').length,
    railLinks: d.querySelectorAll('.slide-rail a[href*="transcript-"]').length,
    moduleLinks: d.querySelectorAll('.slide-rail a[href*="module-"]').length,
    rails: d.querySelectorAll('.slide-rail').length,
    spine: (function () {
      var r = d.querySelector('.slide-rail');
      if (!r) return '';
      return w.getComputedStyle(r).borderRightWidth;
    })(),
    // ── the design system's own rules, asserted so they cannot drift again ──
    // Measured across EVERY slide, not just the visible one: in deck-ready mode only slide 1 is
    // visible, so measuring that alone would mean the whole check inspected nothing but covers,
    // and any content slide could drift unnoticed.
    system: (function () {
      var slides = Array.prototype.slice.call(d.querySelectorAll('.slide'));
      var was = slides.map(function (s) { return s.hidden; });
      slides.forEach(function (s) { s.hidden = false; });
      var worst = { typeScale: [], textColours: [], spacing: [], slide: '' };
      slides.forEach(function (s) {
        var ts = {}, tc = {}, sp = {};
        [s].concat(Array.prototype.slice.call(s.querySelectorAll('*'))).forEach(function (e) {
          var cs = w.getComputedStyle(e);
          if (cs.display === 'none' || cs.visibility === 'hidden') return;    // unrendered
          var hasText = !!e.textContent.trim();
          if (hasText && !e.children.length) ts[Math.round(parseFloat(cs.fontSize) * 10) / 10] = 1;
          if (hasText) tc[cs.color] = 1;
          ['marginTop', 'marginBottom', 'paddingTop', 'paddingBottom', 'gap'].forEach(function (k) {
            var v = cs[k];
            if (!v || v === '0px' || v === 'normal') return;
            var n = parseFloat(v);
            if (!isFinite(n) || n === 0) return;      // 'auto' resolves to NaN once laid out
            sp[Math.round(n * 10) / 10] = 1;
          });
        });
        var n = Object.keys(ts).length + Object.keys(tc).length + Object.keys(sp).length;
        var best = worst.typeScale.length + worst.textColours.length + worst.spacing.length;
        if (n > best) {
          worst = { typeScale: Object.keys(ts).map(Number),
                    textColours: Object.keys(tc),
                    spacing: Object.keys(sp).map(Number),
                    slide: s.id };
        }
      });
      slides.forEach(function (s, i) { s.hidden = was[i]; });
      return worst;
    })(),
    // ── composition, measured across every slide ──
    contrast: apsAuditContrast(w, d),
    composition: (function () {
      var slides = Array.prototype.slice.call(d.querySelectorAll('.slide'));
      var was = slides.map(function (s) { return s.hidden; });
      slides.forEach(function (s) { s.hidden = false; });
      var out = [];
      slides.forEach(function (s) {
        var body = s.querySelector('.slide-body');
        if (!body) return;
        // Measure the CONTENT extent, not the body box: the body is a stretch-aligned grid item, so
        // its box always fills the cell and any measurement of it would be trivially centred.
        var kids = Array.prototype.slice.call(body.children)
                     .filter(function (e) { return e.getClientRects().length; });
        if (!kids.length) return;
        var sb = s.getBoundingClientRect();
        var first = kids[0].getBoundingClientRect();
        var last = kids[kids.length - 1].getBoundingClientRect();
        var h2 = s.querySelector('h2'), txt = s.querySelector('.slide-content p, .slide-content li');
        var num = s.querySelector('.slide-number');
        out.push({
          id: s.id,
          above: Math.round(first.top - sb.top),
          below: Math.round(sb.bottom - last.bottom),
          contentH: Math.round(last.bottom - first.top),
          frameH: Math.round(sb.height),
          title: h2 ? parseFloat(w.getComputedStyle(h2).fontSize) : 0,
          body: txt ? parseFloat(w.getComputedStyle(txt).fontSize) : 0,
          chrome: num ? parseFloat(w.getComputedStyle(num).fontSize) : 0
        });
      });
      slides.forEach(function (s, i) { s.hidden = was[i]; });
      return out;
    })()
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


def write_probe(deck_id: str) -> str:
    """The deck probe with the shared contrast auditor injected."""
    return (PROBE_TEMPLATE.replace("function measure() {", CONTRAST_JS + "\nfunction measure() {", 1)
                         .replace("__DECK__", deck_id))


def check_pages(browser: str, port: int) -> list[str]:
    """Contrast on the pages that are not decks — the landing page and the transcripts.

    The landing page is where an invisible-heading bug actually shipped: a global
    `h1, h2, h3 { color: navy }` beat the element colour on a navy gradient, so every module
    title rendered at 1.00:1. The deck probe could never have caught it.
    """
    pages = ["index.html", "paths.html"]
    for pattern in ("path-*.html", "module-*.html", "transcript-*.html"):
        pages += sorted(p.name for p in SITE_ROOT.glob(pattern))
    pages = [p for p in pages if (SITE_ROOT / p).exists()]
    if not pages:
        return []
    page = SITE_ROOT / PAGES_PROBE_PAGE
    page.write_text(PAGES_PROBE_TEMPLATE.replace("/*CONTRAST*/", CONTRAST_JS)
                                         .replace("__PAGES__", json.dumps(pages)), encoding="utf-8")
    try:
        dom = dump_dom(browser, f"http://127.0.0.1:{port}/{PAGES_PROBE_PAGE}", budget_ms=20000)
    finally:
        page.unlink(missing_ok=True)
    match = re.search(r'<pre id="out">(.*?)</pre>', dom, re.S)
    if not match:
        return ["pages: contrast probe did not report"]
    try:
        results = json.loads(html_lib.unescape(match.group(1)))
    except ValueError:
        return ["pages: unreadable contrast probe output"]
    problems: list[str] = []
    for r in results:
        if r.get("error"):
            problems.append(f"{r['page']}: contrast probe failed ({r['error']})")
            continue
        for b in (r.get("audit") or {}).get("failures") or []:
            problems.append(f"{r['page']}: text below WCAG AA — {b['ratio']}:1 (needs {b['need']}) "
                            f"{b['sel']} colour {b['colour']} on {b['background']} ({b['size']}): "
                            f"{b['text']!r}")
    return problems


def check_units() -> list[str]:
    """Assert the learning-path unit model still covers every slide exactly once.

    The path pages, the module pages and their completion tracking are all derived from
    `site_paths.module_units`. A deck edit that moves a segment boundary would silently re-group a
    unit — and a unit that swallowed or dropped a slide would never show up in a browser check,
    because the deck itself would still render all 233 slides perfectly.
    """
    sys.path.insert(0, str(SITE_ROOT))
    import build_site as B                                                      # noqa: PLC0415
    import site_paths as SP                                                     # noqa: PLC0415

    problems: list[str] = []
    total = 0
    for deck_id in B.DECK_IDS:
        deck = B.parse_deck(deck_id)
        units = SP.module_units(deck)
        slides = len(deck["slides"])
        total += len(units)
        covered = sum(u["slides"] for u in units)
        if covered != slides:
            problems.append(f"{deck_id}: units cover {covered} of {slides} slides")
        if units and (units[0]["first"] != 1 or units[-1]["last"] != slides):
            problems.append(f"{deck_id}: unit ranges do not span the deck")
        kinds = [u["kind"] for u in units]
        for required in ("intro", "lab", "quiz", "summary"):
            if required not in kinds:
                problems.append(f"{deck_id}: no {required} unit")
        if kinds.count("segment") != 3:
            problems.append(f"{deck_id}: {kinds.count('segment')} segment units, expected 3")
        # A path page must never link a module page that the build did not write.
        if not (SITE_ROOT / f"module-{deck_id}.html").exists() and deck_id in {
                d for tr in SP.TRACKS if tr["status"] == "built"
                for d in list(tr["core"]) + list(tr.get("slice") or {})}:
            problems.append(f"{deck_id}: in a built path but has no module page")
    if total != 63:
        problems.append(f"unit model yields {total} units, expected 63")
    # Independent cross-check: the unit model derives 17 segments for the On-Device path from the
    # decks alone, while `bundle-map.md` states "17 of 27 teaching segments" by hand. If a deck
    # edit changes a boundary, the two stop agreeing — which is the whole point of asserting it.
    units_by_deck = {d: SP.module_units(B.parse_deck(d)) for d in B.DECK_IDS}
    for track in SP.TRACKS:
        measured = track.get("measured") or {}
        if track["status"] != "built" or not measured:
            continue
        included = SP.track_units(track, units_by_deck)
        segments = sum(1 for u in included if u["kind"] == "segment")
        labs = sum(1 for u in included if u["kind"] == "lab" and u["inclusion"] == "full")
        quizzes = sum(1 for u in included if u["kind"] == "quiz")
        partial_labs = sum(1 for u in included if u["kind"] == "lab" and u.get("partial"))
        if partial_labs and measured["labs"][0] + partial_labs > len(included):
            problems.append(f"{track['slug']}: {partial_labs} partial lab(s) with no full lab")
        for label, got, want in (("segments", segments, measured["segments"][0]),
                                 ("labs", labs, measured["labs"][0]),
                                 ("quizzes", quizzes, measured["quizzes"][0])):
            if got != want:
                problems.append(f"{track['slug']}: model gives {got} {label}, "
                                f"bundle-map.md states {want}")
    for name in ("paths.html", "path-on-device-app.html"):
        if not (SITE_ROOT / name).exists():
            problems.append(f"{name}: missing")
    return problems


def measure_deck(browser: str, port: int, deck_id: str) -> dict:
    """Render the probe and return the raw measurements (used by --measure)."""
    page = SITE_ROOT / PROBE_PAGE
    page.write_text(write_probe(deck_id), encoding="utf-8")
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
    page.write_text(write_probe(deck_id), encoding="utf-8")
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
    if not re.search(r"\d{2} / \d{2}", data["railNum"]):
        problems.append(f"{deck_id}: slide rail has no 'NN / NN' number ({data['railNum']!r})")
    if data["rails"] != slide_count:
        problems.append(f"{deck_id}: {data['rails']} slides carry the editorial rail, expected {slide_count}")
    if not data["spine"] or float(data["spine"].replace("px", "") or 0) <= 0:
        problems.append(f"{deck_id}: the rail has no spine rule (border-right is {data['spine']!r})")
    con = data.get("contrast") or {}
    bad = con.get("failures") or []
    for b in sorted(bad, key=lambda x: x["ratio"])[:4]:
        problems.append(f"{deck_id}: text below WCAG AA — {b['ratio']}:1 (needs {b['need']}) "
                        f"{b['sel']} colour {b['colour']} on {b['background']} ({b['size']}): "
                        f"{b['text']!r}")
    if len(bad) > 4:
        problems.append(f"{deck_id}: {len(bad) - 4} further contrast failures")
    sysd = data["system"]
    worst = sysd["slide"]
    if len(sysd["typeScale"]) > 8:
        problems.append(f"{deck_id}: {len(sysd['typeScale'])} distinct type sizes on {worst}, "
                        f"expected <= 8 — the scale has drifted: {sorted(sysd['typeScale'], reverse=True)}")
    if len(sysd["textColours"]) > 8:
        problems.append(f"{deck_id}: {len(sysd['textColours'])} distinct text colours on {worst}, "
                        f"expected <= 8: {sysd['textColours']}")
    if len(sysd["spacing"]) > 14:
        problems.append(f"{deck_id}: {len(sysd['spacing'])} distinct spacing values on {worst}, "
                        f"expected <= 14: {sorted(sysd['spacing'], reverse=True)}")
    comp = data["composition"]
    thin = [c for c in comp if c["body"] and c["title"] / c["body"] < 2.5]
    if thin:
        c = thin[0]
        problems.append(f"{deck_id}/{c['id']}: title/body is {c['title'] / c['body']:.2f}x, "
                        f"below the 2.5x hierarchy floor ({len(thin)} slide(s) affected)")
    small = [c for c in comp if c["frameH"] and c["chrome"] / c["frameH"] < 0.02]
    if small:
        c = small[0]
        problems.append(f"{deck_id}/{c['id']}: rail chrome is "
                        f"{c['chrome'] / c['frameH'] * 100:.2f}% of the frame height, below the 2% "
                        f"floor that survives a projector ({len(small)} slide(s) affected)")
    off = [c for c in comp if abs(c["above"] - c["below"]) > max(24, c["frameH"] * 0.06)]
    if off:
        c = max(off, key=lambda x: abs(x["above"] - x["below"]))
        problems.append(f"{deck_id}: {len(off)}/{len(comp)} slides are not optically centred; "
                        f"worst {c['id']} ({c['above']}px above, {c['below']}px below)")
    if float(data["panelHeight"].replace("px", "") or 0) <= 0:
        problems.append(f"{deck_id}: the frame did not give back space for the narration panel")
    # Presence is not visibility: a panel pushed below the fold is unusable, and the frame maths
    # silently failing to read --narration-height is exactly how that happens.
    if data["panelTop"] < 0 or data["panelBottom"] > data["viewportHeight"] + 1:
        problems.append(f"{deck_id}: the narration panel is off-screen "
                        f"({data['panelTop']}..{data['panelBottom']} in a {data['viewportHeight']}px viewport)")
    if data["panelBottom"] > data["navTop"] + 1:
        problems.append(f"{deck_id}: the narration panel ({data['panelBottom']}) runs under the "
                        f"navigation strip ({data['navTop']})")
    for control in ("present", "reading", "notes", "drawer"):
        if not data[control]:
            problems.append(f"{deck_id}: {control} control is missing from the deck chrome")
    if not data["coverSlide"]:
        problems.append(f"{deck_id}: slide 1 is not styled as the cover")
    if data["titleIds"] != slide_count:
        problems.append(f"{deck_id}: {data['titleIds']} slides have an anchored title, expected {slide_count}")
    if data["moduleLinks"] != slide_count:
        problems.append(f"{deck_id}: {data['moduleLinks']} slides link to their module overview, "
                        f"expected {slide_count}")
    if data["railLinks"] != slide_count:
        problems.append(f"{deck_id}: {data['railLinks']} slides link to their transcript, "
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
        problems.extend(check_units())
        problems.extend(check_pages(browser, port))
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
