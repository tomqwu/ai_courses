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
  * the player bar carries every control (#75): play, speed, CC, auto-next, present, the timeline
  * exactly one slide is aria-current, and it matches the requested deep link
  * the polite status region announces the right slide number and title
  * the CC control is enabled, which can only happen after the .vtt fetched and parsed
  * a caption cue is rendered with text
  * a slide with no recording degrades to a message rather than a broken player
  * the bar is actually VISIBLE and on screen, with its height reserved in the frame — an earlier
    panel was created hidden and never unhidden, so every control existed and none could be seen
  * the transcript panel lists the slide's narration, and the Sources tab shows its notes
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
    """A Chrome/Chromium binary: an explicit path first, then Playwright's cache, then the usual places.

    `CHROME_PATH` is the escape hatch for any runner; `PLAYWRIGHT_BROWSERS_PATH` is what a Playwright
    install (local or in CI) already sets, so a Linux runner with the Playwright Chromium needs no
    extra configuration. Fixed paths alone made the gate silently skip on every Linux machine.
    """
    import os                                                                     # noqa: PLC0415
    import glob                                                                   # noqa: PLC0415
    explicit = os.environ.get("CHROME_PATH")
    if explicit and Path(explicit).exists():
        return explicit
    pw_root = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    roots = [pw_root] if pw_root else []
    roots += [str(Path.home() / ".cache" / "ms-playwright"), "/opt/pw-browsers"]
    for root in roots:
        for pattern in ("chromium-*/chrome-linux/chrome", "chromium-*/chrome-linux64/chrome",
                        "chromium-*/chrome-mac*/Chromium.app/Contents/MacOS/Chromium",
                        "chromium_headless_shell-*/chrome-linux/headless_shell"):
            hits = sorted(glob.glob(str(Path(root) / pattern)))
            if hits:
                return hits[-1]
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
    }, 700);
  };
  document.body.appendChild(f);
}
next();
</script>
""")

DIAGRAM_PROBE_PAGE = "_aps_diagram_probe.html"
DIAGRAM_PROBE_TEMPLATE = r"""<!doctype html><meta charset=utf-8><title>diagram probe</title>
<pre id="out">pending</pre>
<script>
/*CONTRAST*/
var CASES = __CASES__;
var results = [], i = 0, f = null;
function next() {
  if (i >= CASES.length) { document.getElementById("out").textContent = JSON.stringify(results); return; }
  var c = CASES[i++], deck = c[0], n = c[1], audit = c[2], w = c[3], h = c[4];
  try { localStorage.clear(); } catch (e) {}   // the player resumes from localStorage and that
                                                // beats the deep link — start each case clean
  if (f) document.body.removeChild(f);
  f = document.createElement("iframe");
  f.style.cssText = "width:" + w + "px;height:" + h + "px;border:0";
  f.src = "/" + deck + ".html?g=" + n + "#slide-" + n;
  f.done = false;
  f.onload = function () {
    if (f.done) { return; }   // ignore the about:blank load; measure the real document only
    f.done = true;
    setTimeout(function () {
      try {
        var d = f.contentDocument, out = { deck: deck, slide: n, w: w };
        var slide = d.querySelector(".slide:not([hidden])");
        if (!slide) { out.error = "no visible slide"; results.push(out); next(); return; }
        var sb = slide.getBoundingClientRect();
        out.visibleId = slide.id;
        out.overflowing = slide.scrollHeight > slide.clientHeight + 2;
        // .slide-content scrolls rather than clipping, so a too-tall exhibit never overflows the
        // slide itself: it grows a scrollbar the recording cannot scroll. Measure that instead.
        var content = slide.querySelector(".slide-content");
        out.contentOverflow = content ? Math.max(0, content.scrollHeight - content.clientHeight) : 0;
        // The deck contrast audit sees slide 1 (a cover, no diagram); the slides that carry a
        // diagram or an exhibit get audited here, at their real layout. Every slide is measured.
        if (audit) { out.contrast = apsAuditContrast(f.contentWindow, f.contentDocument); }
        out.diagrams = [];
        Array.prototype.forEach.call(slide.querySelectorAll(".diagram"), function (dg) {
          var r = dg.getBoundingClientRect();
          out.diagrams.push({ kind: (dg.className.match(/fig-[a-z]+/) || [dg.className])[0],
            h: Math.round(r.height), wide: dg.scrollWidth - dg.clientWidth,
            insideFrame: r.bottom <= sb.bottom + 1 && r.right <= sb.right + 1 });
        });
        results.push(out);
      } catch (e) { results.push({ deck: deck, slide: n, error: String(e) }); }
      next();
    }, 500);
  };
  document.body.appendChild(f);
}
next();
</script>
"""

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
    fontLoaded: d.fonts.check('16px "IBM Plex Sans"') && d.fonts.check('600 32px "Bricolage Grotesque"'),
    titleFont: w.getComputedStyle(d.querySelector('.slide:not([hidden]) h2') || d.body).fontFamily,
    fontsStatus: d.fonts.status,
    kicker: text('.slide:not([hidden]) .kicker'),
    title: text('.slide:not([hidden]) h2'),
    railNum: text('.slide:not([hidden]) .slide-number'),
    panelHeight: w.getComputedStyle(d.documentElement).getPropertyValue('--narration-height').trim(),
    panelBottom: Math.round(d.querySelector('.player-bar').getBoundingClientRect().bottom),
    panelTop: Math.round(d.querySelector('.player-bar').getBoundingClientRect().top),
    stageBottom: Math.round(d.querySelector('.slides').getBoundingClientRect().bottom),
    viewportHeight: w.innerHeight,
    present: !!d.querySelector('.player-bar [data-present]'),
    play: !!d.querySelector('.player-bar [data-play]'),
    sourcesTab: !!d.querySelector('[role="tab"][data-tab="sources"]'),
    transcriptRows: d.querySelectorAll('[data-transcript-lines] li').length,
    upNext: (d.querySelector('[data-up-title]') || {}).textContent || '',
    coverSlide: !!d.querySelector('#slide-1.slide-cover'),
    chapters: Object.keys(chapters).length,
    segments: d.querySelectorAll('.player-timeline .tl-seg').length,
    titleIds: d.querySelectorAll('.slide h2[id$="-title"]').length,
    rails: d.querySelectorAll('.slide-rail').length,
    metas: d.querySelectorAll('.slide > .slide-meta').length,
    proofs: d.querySelectorAll('.slide-proof').length,
    proofChips: d.querySelectorAll('.slide-proof .slide-meta .evidence-chip').length,
    // Every slide stays light (#76): the darkest slide background, as a luminance.
    darkest: (function () {
      var min = 1;
      Array.prototype.forEach.call(d.querySelectorAll('.slide'), function (s) {
        var m = w.getComputedStyle(s).backgroundColor.match(/\d+(\.\d+)?/g) || [255, 255, 255];
        var l = (0.2126 * m[0] + 0.7152 * m[1] + 0.0722 * m[2]) / 255;
        if (l < min) min = l;
      });
      return Math.round(min * 100) / 100;
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
        // The body is placed in the space under the meta line (#76), so that is where "above" is
        // measured from; the meta line is chrome, not content.
        var meta = s.querySelector('.slide-meta');
        var topEdge = meta ? meta.getBoundingClientRect().bottom : sb.top;
        // The extent of the content is the union of its children: on a proof slide the claim and
        // the exhibit sit side by side, so the first child's top and the last child's bottom
        // would compare two different columns.
        var boxes = kids.map(function (k) { return k.getBoundingClientRect(); });
        var first = { top: Math.min.apply(null, boxes.map(function (b) { return b.top; })) };
        var last = { bottom: Math.max.apply(null, boxes.map(function (b) { return b.bottom; })) };
        var h2 = s.querySelector('h2'), txt = s.querySelector('.slide-content p, .slide-content li');
        var num = s.querySelector('.slide-number');
        out.push({
          id: s.id,
          above: Math.round(first.top - topEdge),
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
  // Sources on this slide — the tab shows the current slide's speaker notes, and back again.
  d.querySelector('[data-tab="sources"]').click();
  var sources = d.getElementById('panel-sources');
  out.sourcesOpen = !!sources && !sources.hidden;
  out.sourcesHaveNotes = (d.querySelector('[data-drawer-notes]').textContent || '').trim().length > 40;
  d.querySelector('[data-tab="transcript"]').click();
  out.transcriptBack = !d.getElementById('panel-transcript').hidden && sources.hidden;
  // The timeline: its last segment opens that unit's first slide.
  var segs = d.querySelectorAll('.tl-seg');
  var lastSeg = segs[segs.length - 1];
  lastSeg.click();
  out.timelineJump = (d.querySelector('.slide:not([hidden])') || {}).id === 'slide-' + lastSeg.getAttribute('data-first');
  segs[0].click();
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
    pages = ["index.html", "paths.html", "evidence.html", "proof.html"]
    for pattern in ("path-*.html", "module-*.html", "transcript-*.html",
                    "lesson-*.html", "lab-*.html", "quiz-*.html", "handout-*.html", "glossary*.html"):
        pages += sorted(p.name for p in SITE_ROOT.glob(pattern))
    pages = [p for p in pages if (SITE_ROOT / p).exists()]
    if not pages:
        return []
    page = SITE_ROOT / PAGES_PROBE_PAGE
    page.write_text(PAGES_PROBE_TEMPLATE.replace("/*CONTRAST*/", CONTRAST_JS)
                                         .replace("__PAGES__", json.dumps(pages)), encoding="utf-8")
    try:
        # Each page is given a settle window; the budget has to scale with the page count or the
        # probe is cut off mid-run and reports nothing readable.
        budget = 6000 + 1200 * len(pages)
        dom = dump_dom(browser, f"http://127.0.0.1:{port}/{PAGES_PROBE_PAGE}", budget_ms=budget)
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


# Slides whose content scrolls inside the 16:9 frame. A recording cannot scroll, so the gate runs
# with `--strict-fit` and fails them (#70); without it they are listed as warnings, for drafting.
FIT_WARNINGS: list[str] = []


GEOMETRY_SIZES = ((1600, 1000), (1280, 800))


def check_diagram_geometry(browser: str, port: int) -> list[str]:
    """A declared diagram must fit its slide frame, and no slide's content may need scrolling.

    The frames are 16:9 with overflow hidden, so an oversized diagram is silently clipped —
    invisible content, not a style bug. This is measured, not assumed: every slide is opened by
    deep link and its diagram and its content box are measured against the frame in a real
    layout.
    """
    sys.path.insert(0, str(SITE_ROOT))
    import build_site as B                                                      # noqa: PLC0415
    cases = []
    for deck_id in B.DECK_IDS:
        for slide in B.parse_deck(deck_id)["slides"]:
            # Every slide is opened and measured: a bullet slide scrolls inside the frame as
            # silently as an exhibit does (#70). Diagrams and code exhibits carry the substance,
            # so those also get the contrast audit at their real layout.
            audit = bool(slide.get("diagram") or "<pre" in slide.get("html", "")
                         or "data-figure" in slide.get("html", ""))
            # Fit is measured at two desktop sizes: the frame's type scales with it, but borders,
            # the cover's facts and the narration bar do not, so a slide that just fits a large
            # screen clips on a 1280x800 laptop. Contrast does not change with size: audit once.
            for w, h in GEOMETRY_SIZES:
                cases.append([deck_id, slide["number"], audit and w == GEOMETRY_SIZES[0][0], w, h])
    if not cases:
        return []
    page = SITE_ROOT / DIAGRAM_PROBE_PAGE
    page.write_text(DIAGRAM_PROBE_TEMPLATE.replace("/*CONTRAST*/", CONTRAST_JS)
                                         .replace("__CASES__", json.dumps(cases)),
                    encoding="utf-8")
    # The probe opens every case in turn, so its time grows with the course. A fixed budget was
    # enough at 30-odd cases and ran out at 85, leaving the page reporting "pending": scale it.
    budget_ms = max(40000, 1500 * len(cases))
    try:
        dom = dump_dom(browser, f"http://127.0.0.1:{port}/{DIAGRAM_PROBE_PAGE}", budget_ms=budget_ms)
    finally:
        page.unlink(missing_ok=True)
    match = re.search(r'<pre id="out">(.*?)</pre>', dom, re.S)
    if not match:
        return ["diagram geometry: probe did not report"]
    raw = html_lib.unescape(match.group(1)).strip()
    if raw == "pending":
        return [f"diagram geometry: probe still running after {budget_ms} ms of virtual time "
                f"for {len(cases)} slides — raise the per-slide budget"]
    try:
        results = json.loads(raw)
    except ValueError:
        return ["diagram geometry: unreadable probe output"]
    by_case = {(r.get("deck"), r.get("slide"), r.get("w")): r for r in results}
    problems: list[str] = []
    for deck_id, n, _audit, w, h in cases:
        r = by_case.get((deck_id, n, w))
        at = "" if w == GEOMETRY_SIZES[0][0] else f" at {w}x{h}"
        if not r or r.get("error"):
            problems.append(f"{deck_id} slide-{n}{at}: geometry probe failed "
                            f"({(r or {}).get('error', 'missing')})")
            continue
        if r.get("visibleId") != f"slide-{n}":
            problems.append(f"{deck_id} slide-{n}{at}: probe measured {r.get('visibleId')}, "
                            f"not the requested slide")
        for d in r.get("diagrams", []):
            if not d.get("insideFrame") or r.get("overflowing"):
                problems.append(f"{deck_id} slide-{n}{at}: {d.get('kind')} does not fit the slide "
                                f"frame ({d.get('h')}px tall — the frame clips it)")
            if (d.get("wide") or 0) > 1:
                problems.append(f"{deck_id} slide-{n}{at}: {d.get('kind')} is {d['wide']}px wider than "
                                f"its box — a row of parts runs off the side")
        # A code exhibit with no diagram was measured and then never reported: the overflow flag
        # only surfaced inside the diagram loop. A clipped exhibit is the same silent failure.
        if r.get("overflowing") and not r.get("diagrams"):
            problems.append(f"{deck_id} slide-{n}{at}: the slide overflows its frame, so the code "
                            f"exhibit or the text under it is clipped")
        if (r.get("contentOverflow") or 0) > 2:
            FIT_WARNINGS.append(f"{deck_id} slide-{n}{at}: the content needs {r['contentOverflow']}px of "
                                f"scrolling — a recorded slide cannot scroll, so that part is never seen")
        bad = (r.get("contrast") or {}).get("failures") or []
        for b in sorted(bad, key=lambda x: x["ratio"])[:3]:
            problems.append(f"{deck_id} slide-{n}: text below WCAG AA — {b['ratio']}:1 "
                            f"(needs {b['need']}) {b['sel']} colour {b['colour']} on "
                            f"{b['background']} ({b['size']}): {b['text']!r}")
        if len(bad) > 3:
            problems.append(f"{deck_id} slide-{n}: {len(bad) - 3} further contrast failures")
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
    # 63 units for M0-M8, plus 7 for the free M9 (intro, three segments, lab, quiz, summary). Kept
    # as a literal on purpose: a deck edit that moves a unit boundary should fail here, not re-count.
    if total != 70:
        problems.append(f"unit model yields {total} units, expected 70")
    # Independent cross-check: the unit model derives 17 segments for the On-Device path from the
    # decks alone, while `bundle-map.md` states "17 of 27 teaching segments" by hand. If a deck
    # edit changes a boundary, the two stop agreeing — which is the whole point of asserting it.
    units_by_deck = {d: SP.module_units(B.parse_deck(d)) for d in B.DECK_IDS}
    for track in SP.TRACKS:
        measured = track.get("measured") or {}
        if track["status"] != "built":
            continue
        if not measured:
            # No course-wide total is stated in this bundle map, so there is nothing to cross-check
            # against. Assert only that the model produces a sane, non-empty path.
            included_any = SP.track_units(track, units_by_deck)
            if not any(u["kind"] == "segment" for u in included_any):
                problems.append(f"{track['slug']}: no teaching segments in the path")
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
    for name in ["paths.html"] + [t["page"] for t in SP.TRACKS
                                  if t["status"] == "built" and t["page"]]:
        if not (SITE_ROOT / name).exists():
            problems.append(f"{name}: missing")

    # The landing page is the paths GUI: the chooser comes first, offers every built path, and the
    # module cards open the path-aware module pages rather than dropping straight into a deck.
    index_html = (SITE_ROOT / "index.html").read_text(encoding="utf-8")
    if 'class="path-grid"' not in index_html:
        problems.append("index.html: no path chooser on the landing page")
    if index_html.index('class="path-grid"') > index_html.index('class="room-grid"'):
        problems.append("index.html: the module grid comes before the path chooser")
    for track in SP.TRACKS:
        if track["status"] == "built" and track["page"]:
            if f'href="./{track["page"]}"' not in index_html:
                problems.append(f"index.html: the chooser does not link {track['page']}")
    if 'href="./module-m00.html"' not in index_html:
        problems.append("index.html: module cards do not open the module pages")

    # A module can sit in several paths, each including it differently. The module page must name
    # every one of them — a page that named a single owner would misdescribe the other paths.
    for deck_id in B.DECK_IDS:
        page = SITE_ROOT / f"module-{deck_id}.html"
        if not page.exists():
            continue
        expected = len(SP.paths_for_module(deck_id))
        got = page.read_text(encoding="utf-8").count('class="path-line"')
        if got != expected:
            problems.append(f"module-{deck_id}.html lists {got} paths, expected {expected}")
    # The shared core must actually be shared: M0/M1/M7/M8 sit in all three paths.
    for deck_id in ("m00", "m01", "m07", "m08"):
        if len(SP.paths_for_module(deck_id)) != 3:
            problems.append(f"{deck_id}: expected in all 3 built paths, "
                            f"found {len(SP.paths_for_module(deck_id))}")

    # Exhibits (#76): every code block is a panel, a panel that copies a cited file names it with its
    # lines and pinned commit, and every `hl=` mark lands on a highlighted line.
    exhibits = headed = 0
    for deck_id in B.DECK_IDS:
        deck = B.parse_deck(deck_id)
        units = SP.module_units(deck)
        for slide in deck["slides"]:
            h = B.slide_shell(deck, slide, None, ".", "", B.slide_place(deck, slide, units))
            shown = h.split('<div class="slide-notes-source"')[0]
            panels = shown.count('<figure class="exhibit')
            exhibits += panels
            headed += shown.count('class="exhibit-lines"')
            if shown.count("<pre") != panels:
                problems.append(f"{deck_id} {slide['id']}: a code block is not rendered as an exhibit panel")
            marks = re.findall(r"^```\S*\s.*\bhl=([\d,-]+)", slide.get("raw", ""), re.M)
            if marks and "is-hl" not in shown:
                problems.append(f"{deck_id} {slide['id']}: hl={marks[0]} marks no highlighted line")
    if exhibits and not headed:
        problems.append("exhibits: no panel names its file, lines and commit — citations are not resolving")

    # Declared diagrams: a slide that declares one must render it, and the hand-typed disease
    # this replaces must not come back — no box-drawing characters anywhere, and no slide may
    # encode a flow as three or more text arrows outside a diagram component.
    box_chars = set("│▼┌└┐┘├")
    for deck_id in B.DECK_IDS:
        deck = B.parse_deck(deck_id)
        for slide in deck["slides"]:
            h = slide.get("html", "")
            sid = f"{deck_id} {slide['id']}"
            bad = sorted(set(h) & box_chars)
            if bad:
                problems.append(f"{sid}: hand-typed box-drawing {bad} — draw it, declare it, "
                                f"or leave it as prose")
            outside = re.sub(r'<figure class="diagram[^"]*" data-figure>.*?</figure>', "", h, flags=re.S)
            # Per text block, not per slide: one arrow in a bullet is legitimate notation
            # ("command → result"); a chain of four-plus stages in one bullet is a diagram
            # trying to escape as prose. Objectives and recaps that REHEARSE a chain already
            # drawn as a diagram elsewhere in the deck are allowlisted, with the reason.
            rehearsal = {("m01", "slide-24"): "recap restates the flow drawn on m01 slide-12",
                         ("m02", "slide-2"): "objective rehearses the figure drawn on m02 slide-3",
                         ("m04", "slide-2"): "objective rehearses the flow drawn on m01 slide-12"}
            for block in re.split(r"</li>|</p>", outside):
                if block.count("→") >= 3 and (deck_id, slide["id"]) not in rehearsal:
                    problems.append(f"{sid}: {block.count('→')} text arrows in one block "
                                    f"outside a diagram — a flow encoded as prose")
            kind = slide.get("diagram")
            if kind:
                # A declared list is drawn as exactly one figure (#99), whatever else the slide holds.
                if h.count("is-from-list\" data-figure") != 1:
                    problems.append(f"{sid}: _diagram:{kind} declared but not rendered")
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
    if "IBM Plex Sans" not in data["bodyFont"]:
        problems.append(f"{deck_id}: body font is {data['bodyFont']!r}, not IBM Plex Sans (#72)")
    if "Bricolage Grotesque" not in data.get("titleFont", ""):
        problems.append(f"{deck_id}: slide titles use {data.get('titleFont')!r}, not Bricolage Grotesque (#72)")
    if not data["fontLoaded"] and data.get("fontsStatus") != "loaded":
        problems.append(f"{deck_id}: IBM Plex Sans / Bricolage Grotesque were requested but never loaded "
                        f"(status {data.get('fontsStatus')!r})")
    if not data["kicker"]:
        problems.append(f"{deck_id}: the current slide has no kicker")
    if not data["title"]:
        problems.append(f"{deck_id}: the current slide has no title")
    if not re.search(r"\d{2} / \d{2}", data["railNum"]):
        problems.append(f"{deck_id}: the slide's meta line has no 'NN / NN' number ({data['railNum']!r})")
    # The four templates (#76): no rail, a meta line on every slide, an Evidence chip on every proof
    # slide, and no dark slide — the navy proof theme is retired.
    if data["rails"]:
        problems.append(f"{deck_id}: {data['rails']} slides still carry the rail")
    if data["metas"] != slide_count:
        problems.append(f"{deck_id}: {data['metas']} slides carry the meta line, expected {slide_count}")
    if data["proofChips"] != data["proofs"]:
        problems.append(f"{deck_id}: {data['proofChips']} of {data['proofs']} proof slides show the Evidence chip")
    if data["darkest"] < 0.8:
        problems.append(f"{deck_id}: a slide background is dark (luminance {data['darkest']}); slides stay light")
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
    # 2.0x, the owner's decision on #71: the 2.5x floor forced ~70px titles and was the main cause
    # of slides overflowing their frame (#70).
    thin = [c for c in comp if c["body"] and c["title"] / c["body"] < 2.0]
    if thin:
        c = thin[0]
        problems.append(f"{deck_id}/{c['id']}: title/body is {c['title'] / c['body']:.2f}x, "
                        f"below the 2.0x hierarchy floor ({len(thin)} slide(s) affected)")
    small = [c for c in comp if c["frameH"] and c["chrome"] / c["frameH"] < 0.02]
    if small:
        c = small[0]
        problems.append(f"{deck_id}/{c['id']}: the meta line is "
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
        problems.append(f"{deck_id}: the player bar is off-screen "
                        f"({data['panelTop']}..{data['panelBottom']} in a {data['viewportHeight']}px viewport)")
    if abs(data["panelTop"] - data["stageBottom"]) > 1:
        problems.append(f"{deck_id}: the player bar ({data['panelTop']}) is not directly under the stage "
                        f"({data['stageBottom']})")
    for control in ("present", "play", "sourcesTab"):
        if not data[control]:
            problems.append(f"{deck_id}: {control} control is missing from the player")
    if data["transcriptRows"] < 1:
        problems.append(f"{deck_id}: the transcript panel lists nothing for the current slide")
    if not data["upNext"].strip():
        problems.append(f"{deck_id}: the Up next card is empty")
    if not data["coverSlide"]:
        problems.append(f"{deck_id}: slide 1 is not styled as the cover")
    if data["titleIds"] != slide_count:
        problems.append(f"{deck_id}: {data['titleIds']} slides have an anchored title, expected {slide_count}")
    if data["segments"] < 5:
        problems.append(f"{deck_id}: the timeline has {data['segments']} unit segments, expected at least 5")
    for label, key, want in (
            ("Present did not enter presentation mode", "presentMode", True),
            ("Present did not report its pressed state", "presentPressed", "true"),
            ("Present did not leave presentation mode", "presentCleared", True),
            ("the Sources tab did not open", "sourcesOpen", True),
            ("the Sources tab was empty for a slide that has notes", "sourcesHaveNotes", True),
            ("the Transcript tab did not come back", "transcriptBack", True),
            ("a timeline segment did not open its unit's first slide", "timelineJump", True)):
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
        "player bar": 'class="player-bar"',
        "play control": "data-play",
        "speed control": "data-speed",
        "cc control": "data-cc",
        "auto-next control": "data-auto",
        "present control": "data-present",
        "timeline": 'class="player-timeline"',
        "transcript panel": "data-transcript-lines",
        "sources panel": "data-source-list",
        "status region": 'role="status"',
    }
    for label, needle in required.items():
        if needle not in dom:
            problems.append(f"{deck_id}: the player has no {label}")

    current = re.findall(r'<section class="slide[^"]*" id="(slide-\d+)"[^>]*aria-current="true"', dom)
    if current != ["slide-1"]:
        problems.append(f"{deck_id}: expected slide-1 to be current on load, got {current or 'none'}")
    status = re.search(r'class="slide-status"[^>]*>([^<]*)', dom)
    if not status or not status.group(1).startswith(f"Slide 1 of {slide_count}"):
        problems.append(f"{deck_id}: status region did not announce slide 1 of {slide_count} "
                        f"(got {(status.group(1).strip() if status else 'nothing')!r})")

    if "slide-1" in narrated:
        # Presence is not visibility: assert the bar's height was reserved in the frame.
        height = re.search(r"--narration-height:\s*([0-9.]+)px", dom)
        if not height or float(height.group(1)) <= 0:
            problems.append(f"{deck_id}: --narration-height was not reserved, so the bar covers "
                            f"the bottom of the slide")
        cc = re.search(r"<button[^>]*data-cc[^>]*>", dom)
        if cc and "disabled" in cc.group(0):
            problems.append(f"{deck_id}: CC stayed disabled, so captions never parsed for slide-1")
        caption = re.search(r'class="player-caption"[^>]*>(.*?)</p>', dom, re.S)
        if not caption or not caption.group(1).strip():
            problems.append(f"{deck_id}: no caption cue rendered for a narrated slide-1")
        play = re.search(r"<button[^>]*data-play[^>]*>", dom)
        if play and "disabled" in play.group(0):
            problems.append(f"{deck_id}: Play was disabled even though slide-1 is narrated")
        # With captions loaded, the transcript rows are the script's sentences, each seeking.
        if "line-seek" not in dom:
            problems.append(f"{deck_id}: the transcript rows did not become seekable once captions loaded")

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
    parser.add_argument("--strict-fit", action="store_true",
                        help="fail, not warn, when a slide's content needs scrolling")
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
        problems.extend(check_diagram_geometry(browser, port))
        if args.strict_fit:
            problems.extend(FIT_WARNINGS)
        elif FIT_WARNINGS:
            print(f"\n  {len(FIT_WARNINGS)} slide(s) need scrolling inside the frame (warning, #70):")
            for w in FIT_WARNINGS:
                print(f"  ! {w}")
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
