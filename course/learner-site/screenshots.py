#!/usr/bin/env python3
"""Screenshot every page and slide template of the built site, at desktop and phone widths (#81).

    python3 screenshots.py --out /tmp/aps-screens      # after the site is built (make -C .. site)

CI uploads the folder as an artifact of every gate run, so a reviewer sees what a change looks like
without building it. The list names each page kind and each of the four slide templates once; it is
a picture of the design, not a test — check_player.py and check_features.py are the tests.
"""
from __future__ import annotations

import argparse
import functools
import http.server
import sys
import threading
from pathlib import Path

SITE = Path(__file__).resolve().parent

# (name, path, what to do first). Slides are opened by deep link; "palette" opens the search.
SHOTS = [
    ("home", "index.html", None),
    ("home-returning", "index.html", "resume"),
    ("paths", "paths.html", None),
    ("path", "path-on-device-app.html", None),
    ("module", "module-m02.html", None),
    ("slide-cover", "m02.html#slide-1", None),
    ("slide-section-opener", "m02.html#slide-10", None),
    ("slide-proof", "m02.html#slide-9", None),
    ("slide-flow", "m01.html#slide-12", None),
    ("slide-concept", "m04.html#slide-6", None),
    ("read-lesson", "lesson-m02.html", None),
    ("read-handout", "handout-m02.html", None),
    ("read-glossary", "glossary-m02.html", None),
    ("transcript", "transcript-m02.html", None),
    ("lab", "lab-m02.html", None),
    ("check", "quiz-m02.html", None),
    ("glossary", "glossary.html", None),
    ("evidence", "evidence.html", None),
    ("proof", "proof.html", None),
    ("palette", "lab-m02.html", "palette"),
]
SIZES = (("desktop", 1440, 900), ("phone", 390, 844))


class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):   # noqa: D401 - silence the per-request log
        pass


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", required=True, help="folder to write the PNGs into")
    args = parser.parse_args(argv)
    try:
        from playwright.sync_api import sync_playwright   # noqa: PLC0415
    except ImportError:
        print("screenshots: skipped — `pip install playwright`")
        return 0
    if not (SITE / "index.html").exists():
        print("screenshots: no built site here — run `make -C .. site` first")
        return 1
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    handler = functools.partial(_Quiet, directory=str(SITE))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    taken = 0
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            for size, width, height in SIZES:
                phone = size == "phone"
                context = browser.new_context(viewport={"width": width, "height": height},
                                              is_mobile=phone, has_touch=phone)
                page = context.new_page()
                for name, path, before in SHOTS:
                    if before == "resume":
                        page.goto(f"{base}/m02.html#slide-9")
                        page.wait_for_timeout(400)
                    page.goto(f"{base}/{path}")
                    page.wait_for_timeout(500)
                    if before == "palette":
                        page.keyboard.press("Control+k")
                        page.keyboard.type("context budget")
                        page.wait_for_timeout(500)
                    page.screenshot(path=str(out / f"{size}-{name}.png"))
                    taken += 1
                context.close()
            browser.close()
    finally:
        server.shutdown()
    print(f"screenshots: {taken} written to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
