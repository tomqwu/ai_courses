#!/usr/bin/env python3
"""Unit tests for the figure grammar and renderers (figures.py, #99).

    python3 course/learner-site/test_figures.py
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import figures as F  # noqa: E402

FLOW = """kind: flow
alt: Audio moves from capture to routing through one pipeline.
source: ListenToMe/Sources/ListenToMeCore/Capture.swift:3-9
step: capture (seam) — mic and system audio @ Here is the whole system
step: store — never-empty context @ The store keeps
step: route
"""

ARCH = """kind: architecture
alt: Platform glue sits over a pure core that owns every decision.
layer: App/ glue — platform code implements the seams
  box: capture (seam)
  box: transcribe (seam) @ The seam is
layer: Core (pure) — every decision, tested against mocks
  box: store
  box: prompt (hl)
"""

SENTENCES = ["Here is the whole system in one line.", "The store keeps the newest segment.",
             "The seam is a protocol the core owns."]


class Parse(unittest.TestCase):
    def test_flow_parts(self):
        fig = F.parse(FLOW)
        self.assertEqual(fig["kind"], "flow")
        self.assertEqual([p["label"] for p in fig["items"]], ["capture", "store", "route"])
        first = fig["items"][0]
        self.assertEqual(first["flags"], {"seam"})
        self.assertEqual(first["note"], "mic and system audio")
        self.assertEqual(first["at"], "Here is the whole system")
        self.assertEqual(fig["source"], "ListenToMe/Sources/ListenToMeCore/Capture.swift:3-9")

    def test_architecture_nests_boxes(self):
        fig = F.parse(ARCH)
        self.assertEqual([l["label"] for l in fig["items"]], ["App/ glue", "Core (pure)"])
        self.assertEqual([b["label"] for b in fig["items"][0]["children"]], ["capture", "transcribe"])
        self.assertEqual(fig["items"][1]["children"][1]["flags"], {"hl"})
        self.assertEqual(fig["items"][0]["children"][1]["at"], "The seam is")

    def test_label_keeps_non_flag_parentheses(self):
        part = F.parse("kind: flow\nalt: a figure with a bracket label\nstep: Core (pure)\n")["items"][0]
        self.assertEqual(part["label"], "Core (pure)")
        self.assertEqual(part["flags"], set())

    def test_flags_may_close_the_note(self):
        part = F.parse("kind: flow\nalt: flags written after the note\nstep: API — real JWT (hl)\n")["items"][0]
        self.assertEqual((part["label"], part["note"], part["flags"]), ("API", "real JWT", {"hl"}))

    def test_screenshot_callouts(self):
        fig = F.parse("kind: screenshot\nalt: The dashboard with three callouts marked.\n"
                      "image: dash.png\nframe: browser\ncallout: 12,30 — Gaps first\n")
        self.assertEqual(fig["image"], "dash.png")
        self.assertEqual(fig["callouts"], [{"x": 12.0, "y": 30.0, "text": "Gaps first"}])

    def test_missing_alt_fails(self):
        with self.assertRaises(F.FigureError):
            F.parse("kind: flow\nstep: a\n")

    def test_unknown_kind_fails(self):
        with self.assertRaises(F.FigureError):
            F.parse("kind: pie\nalt: a pie chart of something\n")


class Render(unittest.TestCase):
    def test_flow_nodes_links_and_steps(self):
        html = F.render(F.parse(FLOW), sentences=SENTENCES)
        self.assertIn('data-figure', html)
        self.assertEqual(html.count('class="fig-node'), 3)
        self.assertIn('class="fig-node is-seam"', html)
        self.assertEqual(html.count('class="fig-link"'), 2)
        self.assertIn('data-step="0"', html)
        self.assertIn('data-step="1"', html)
        self.assertIn('class="sr-only">Audio moves', html)
        self.assertIn('fig-source', html)

    def test_architecture_layers(self):
        html = F.render(F.parse(ARCH), sentences=SENTENCES)
        self.assertEqual(html.count('class="fig-layer'), 2)
        self.assertEqual(html.count('class="fig-box'), 4)
        self.assertIn('data-step="2"', html)
        self.assertIn('is-hl', html)

    def test_chain_layer_links_its_boxes(self):
        html = F.render(F.parse("kind: architecture\nalt: a pipeline drawn as a chain row\n"
                                "layer: Pipeline (chain)\n  box: a\n  box: b\n  box: c\n"))
        self.assertEqual(html.count('class="fig-link"'), 2)
        self.assertIn('fig-layer is-chain', html)

    def test_text_is_escaped(self):
        html = F.render(F.parse("kind: flow\nalt: escape check for markup\nstep: <b>x</b>\n"))
        self.assertIn("&lt;b&gt;", html)

    def test_screenshot_frame(self):
        html = F.render(F.parse("kind: screenshot\nalt: The dashboard with one callout.\n"
                                "image: dash.png\nframe: phone\ncallout: 50,50 — Here\n"), base=".")
        self.assertIn('src="./figures/shots/dash.png"', html)
        self.assertIn('fig-frame-phone', html)
        self.assertIn('fig-pin', html)


    def test_crop_shows_the_top_and_rescales_pins(self):
        html = F.render(F.parse("kind: screenshot\nalt: the swap requests screen, top half\n"
                                "image: signupflow-replacement-needed.png\ncrop: 50\ncallout: 10,20 — here\n"))
        self.assertIn('aspect-ratio:2880/900', html)
        self.assertIn('top:40%', html)

    def test_frameless_screenshot_and_bad_frame(self):
        base = "kind: screenshot\nalt: an app window that carries its own chrome\nimage: app.png\n"
        self.assertIn("fig-frame-none", F.render(F.parse(base + "frame: none\n")))
        with self.assertRaises(F.FigureError):
            F.render(F.parse(base + "frame: tablet\n"))

    def test_every_scene_inlines_with_its_alt_and_only_palette_classes(self):
        import re
        for svg in sorted(F.SCENES.glob("*.svg")):
            html = F.render(F.parse(f"kind: scene\nalt: the {svg.stem} illustration\nscene: {svg.name}\n"))
            self.assertIn(f'role="img" aria-label="the {svg.stem} illustration"', html)
            self.assertIn("Illustration", html)
            text = svg.read_text()
            self.assertIn("<title>", text, svg.name)
            self.assertNotRegex(text, r"#[0-9a-fA-F]{3,6}\b|rgb\(|fill=\"(?!none)", svg.name)
            for cls in re.findall(r'class="([^"]+)"', text):
                for c in cls.split():
                    self.assertTrue(c == "scene" or c.startswith("sc-"), f"{svg.name}: {c}")


SYSTEM = """kind: system
alt: A request passes the auth dependency before any query reaches the database.
layer: Clients
  node web: Web — HTMX pages
  node cli: CLI
layer: API
  node api: routes (seam) @ The API and security tier
  node deps: verify_org_member (hl)
layer: Data
  node db: database
edge: web -> api — cookie JWT
edge: cli -> api
edge: api -> deps — every request (hl)
edge: deps -> db — org_id filter @ Unit tests are fast
"""


class System(unittest.TestCase):
    def test_nodes_edges_and_steps(self):
        fig = F.parse(SYSTEM)
        self.assertEqual([c["id"] for c in fig["items"][1]["children"]], ["api", "deps"])
        self.assertEqual(fig["edges"][0], {"from": "web", "to": "api", "label": "cookie JWT", "flags": set(), "at": ""})
        self.assertEqual(fig["edges"][2]["flags"], {"hl"})
        html = F.render(fig, sentences=["Unit tests are fast.", "The API and security tier runs."])
        self.assertIn('data-sys', html)
        self.assertEqual(html.count('data-node='), 5)
        self.assertEqual(html.count('<li class="fig-edge'), 4)
        self.assertIn('data-from="deps" data-to="db"', html)
        self.assertIn('data-node="api" data-step="1"', html)
        self.assertIn('Web → routes', html)

    def test_edge_to_unknown_node_fails(self):
        with self.assertRaises(F.FigureError):
            F.parse(SYSTEM + "edge: api -> cache\n")

    def test_system_without_edges_fails(self):
        with self.assertRaises(F.FigureError):
            F.parse("kind: system\nalt: boxes with nothing joining them\nlayer: A\n  node a: one\n")


class FromList(unittest.TestCase):
    def test_stack_becomes_architecture_with_same_words(self):
        fig = F.from_list("stack", ["mic (.you) · system audio (.others)", "PCM chunks"])
        self.assertEqual(fig["kind"], "architecture")
        self.assertEqual([l["label"] for l in fig["items"]], ["mic (.you) · system audio (.others)", "PCM chunks"])

    def test_flow_and_grid(self):
        self.assertEqual(F.from_list("flow", ["a", "b"])["kind"], "flow")
        self.assertTrue(F.from_list("loop", ["a", "b"])["loop"])
        self.assertEqual(F.from_list("grid", ["x: y"])["kind"], "compare")


class StepIndex(unittest.TestCase):
    def test_match(self):
        self.assertEqual(F.step_index("the STORE keeps", SENTENCES), 1)
        self.assertIsNone(F.step_index("nothing like this", SENTENCES))


if __name__ == "__main__":
    unittest.main(verbosity=1)
