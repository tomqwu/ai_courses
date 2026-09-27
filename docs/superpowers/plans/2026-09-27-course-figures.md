# Course Figures Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give every module drawn architecture and flow figures, real product screenshots and
illustrations, with narration-synced build-ins — declared in the Markdown, rendered by the build,
held by the gate.

**Architecture:** A ```` ```figure ```` fence in slides or lessons holds a small line grammar that
`course/learner-site/figures.py` parses and renders to HTML (cards, bands, columns, framed images)
joined by inline SVG connectors, styled only with Studio tokens. The deck renderer (`build_site.py`)
and the reading renderer (`site_content.py`) both call it; the existing `_diagram` lists are routed
through the same renderer. Parts with `at:` get `data-step` (a narration sentence index) and
`player.js` reveals them as the sentence is spoken. `verify.py` checks every figure.

**Tech Stack:** Python 3.11 standard library, vanilla JS, CSS, Playwright (existing checks).

## Global Constraints

- Standard library only in Python; no new pip or npm dependency; no external assets at runtime.
- Colours only from the `:root` tokens in `player.css`; add a token rather than a literal.
- Every slide fits its 16:9 frame (`check_player.py --strict-fit`); ≤ 8 type sizes, ≤ 8 text colours,
  ≤ 14 spacing values per slide; WCAG AA contrast.
- Narration words never change; slides are never split or renumbered.
- Code must compile on Python 3.11 (CI) — no backslash inside an f-string expression.
- Every change ends merged to `main` through a PR with the gate green (AGENTS.md).
- Figures with a case-study subject carry `source:`; screenshots are byte-identical copies at the pinned
  commits (ListenToMe `a9bde8e`, SignUpFlow `c550d46`, ai_qe `6388f0a`).

## The figure grammar (used by every task)

```figure
kind: flow | architecture | compare | screenshot | scene
alt: One sentence describing what the figure shows.
source: ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:10-40     (optional)
title: Optional caption shown under the figure
step: capture (seam) — mic and system audio @ Here is the whole system
step: store — never-empty context
loop: yes                                                             (flow only)
layer: App/ glue — platform code implements the seams                 (architecture)
  box: capture (seam)
  box: transcribe (seam) @ The seam is a protocol
column: Fail closed (good)                                            (compare)
  item: an unknown host throws
image: signupflow-dashboard.png                                       (screenshot)
frame: browser | phone | mac
callout: 12,30 — The admin sees gaps before members do
scene: stranger-clones.svg                                            (scene)
```

A value is `label [(flags)] [— note] [@ at-words]`. Flags: `seam`, `hl`, `good`, `bad`.
`at-words` are the first words of the narration sentence at which the part builds in.

## File Structure

| File | Responsibility |
|---|---|
| `course/learner-site/figures.py` (new) | parse the grammar; render five kinds; convert `_diagram` lists; resolve `at:` |
| `course/learner-site/test_figures.py` (new) | unit tests for the parser, renderers and `at:` resolution |
| `course/learner-site/build_site.py` | call figures for ```` ```figure ```` fences and `_diagram` lists on slides; pass sentences for `at:` |
| `course/learner-site/site_content.py` | call figures for ```` ```figure ```` fences in lessons and other reading pages |
| `course/learner-site/site_paths.py`, `site_pages.py` | hero figure on the module page; segment figure at the head of each segment in Read |
| `course/learner-site/assets/player.css` | figure styles, connector motion, build-in states, reduced motion, phone |
| `course/learner-site/assets/player.js` | reveal `data-step` parts by narration sentence; Replay control (`.`) |
| `course/06-production/verify.py` | Figures check; skip `figure` fences in the exhibit check |
| `course/figures/shots/`, `course/figures/manifest.json`, `course/figures/scenes/` (new) | screenshots with provenance; illustrations |
| `course/06-production/figures_shots.py` (new) | copy screenshots at pinned commits and write the manifest |
| `course/check.sh` | run `test_figures.py` |
| `course/01-design/content-standards.md`, `.claude/skills/course-content/SKILL.md`, `course/learner-site/README.md` | the Figures rules |

---

## Part A — the figure system (#99)

### Task 1: Parser and renderers (`figures.py`) with unit tests

**Files:** Create `course/learner-site/figures.py`, `course/learner-site/test_figures.py`; Modify `course/check.sh`.

**Interfaces — Produces:**
- `parse(text: str) -> dict` — `{"kind", "alt", "source", "title", "items": [Part], "loop": bool, "image", "frame", "scene", "callouts": [{"x","y","text"}]}` where `Part = {"label","note","flags": set[str],"at": str,"children": [Part]}`.
- `render(fig: dict, *, sentences: list[str] | None = None, inline=callable) -> str` — HTML string; parts whose `at` matches a sentence get `data-step="<index>"`.
- `from_list(kind: str, items: list[str]) -> dict` — a `_diagram` list as a figure (`flow|loop|steps` → flow, `stack` → architecture, `grid` → compare).
- `step_index(at: str, sentences: list[str]) -> int | None` — first sentence starting with the words (case/space-insensitive).
- `class FigureError(ValueError)`.

- [ ] **Step 1: Write failing tests** in `test_figures.py` (unittest): parse a flow with a seam flag, note and `at`; parse an architecture with two layers and indented boxes; `render` of a flow contains one `.fig-node` per step, `class="fig-node is-seam"` for the seam, an `<svg class="fig-link"` between nodes, and `data-step="1"` when `at` matches the second sentence; `render` raises `FigureError` when `alt` is missing; `from_list("stack", ...)` yields an architecture whose rows keep the words; `step_index` is case-insensitive and returns `None` for no match.
- [ ] **Step 2: Run** `python3 course/learner-site/test_figures.py` — FAIL (module missing).
- [ ] **Step 3: Implement** `figures.py`: a line parser (top-level `key: value`; `step|layer|column|callout` repeat into `items`/`callouts`; lines indented by two spaces with `box:`/`item:` attach to the last item), the value grammar, and one renderer per kind. Output roots are `<figure class="diagram fig fig-<kind>" data-figure>` with a visually hidden `<figcaption class="sr-only">alt</figcaption>`, a visible `<figcaption class="fig-title">` when `title` is set, and a `fig-source` chip when `source` is set. Connectors are inline `<svg class="fig-link" viewBox="0 0 40 16" aria-hidden="true"><path d="M2 8h30"/><path d="M28 3l6 5-6 5"/></svg>`.
- [ ] **Step 4: Run tests** — PASS. **Step 5:** add `step "unit tests — figures" "$PYTHON" learner-site/test_figures.py` to `check.sh`; commit.

### Task 2: Figures on slides and in reading pages; `_diagram` routed through figures; exhibit check skips figures

**Files:** Modify `build_site.py` (`render_blocks`, `render_diagram`, `parse_deck`, `slide_shell`), `site_content.py` (`render_document`), `06-production/verify.py` (`check_exhibits`), `check_player.py` (diagram needle).

**Interfaces — Consumes:** `figures.parse/render/from_list`. **Produces:** slide HTML where a ```` ```figure ```` fence becomes `render(parse(body), sentences=<the slide's narration sentences>)`, and `_diagram` lists become `render(from_list(kind, items))`.

- [ ] Step 1: In `render_blocks`, when the fence info is `figure`, collect the body raw (unescaped) and emit a placeholder `<!--figure:N-->`; `parse_deck` passes the slide's sentences so `slide_shell` replaces placeholders with rendered figures (sentences come from `sentences(script_text)`).
- [ ] Step 2: `render_diagram(kind, items, ordered)` returns `figures.render(figures.from_list(kind, items))` — every `_diagram` slide now draws a figure with the same words.
- [ ] Step 3: `site_content.render_document` renders ```` ```figure ```` fences with `figures.render(figures.parse(body), inline=inline)`.
- [ ] Step 4: `verify.check_exhibits` skips fences whose info is `figure`; `check_player.check_units` asserts each declared `_diagram` renders one `data-figure` root instead of the old class needle.
- [ ] Step 5: Build (`python3 build_site.py`) and run `check_player.py --all --strict-fit`; every slide fits; commit.

### Task 3: Figure styles and motion

**Files:** Modify `assets/player.css`.

- [ ] Nodes are light cards (`--surface`, 2px `--c-ink-strong` border, radius .6em); `.is-seam` uses `--accent-soft` + `--accent`; `.is-hl` a thicker accent border; architecture layers are bands (`--wash` header row with the layer name) holding a row of boxes; compare columns use `good` (`--done` rule) / `bad` (`--proof-ink` rule) with labelled headings (never colour alone); screenshot frames (browser chrome bar with three dots drawn in CSS, phone bezel, mac) with numbered callout pins (`--accent`, white numerals, a matching numbered list under the image); scenes centred with a caption.
- [ ] Connectors: `.fig-link path` stroke `--ink-faint`; when the figure is shown, a one-time draw-in (`stroke-dasharray` + `@keyframes fig-draw`); on flows, `.fig-link.is-live` runs a moving dash (`@keyframes fig-flow`) between the active node and the next.
- [ ] Build-in states: `[data-step].is-pending { opacity:.15 }`, `.is-shown` transitions to 1; `@media (prefers-reduced-motion: reduce)` and `@media print` force all parts shown and disable animations.
- [ ] Phone (≤ 480px): flows wrap to a vertical list with downward connectors; architecture bands stack.
- [ ] Run `check_player.py --all --strict-fit` (type scale, colours, contrast, fit); commit.

### Task 4: Narration-synced build-ins in the player

**Files:** Modify `assets/player.js`; Modify `check_features.py`.

- [ ] On `goTo`, for the current slide's `[data-step]` parts: if the slide has a clip and motion is allowed, mark every part `is-pending`, then on each caption tick reveal parts whose step ≤ the current transcript row index (`rows.findIndex`). With no clip, or reduced motion, all parts are shown. After the narration ends, all parts are shown.
- [ ] A `Replay build` button (`data-fig-replay`, in `.player-meta`, shown only when the slide has stepped parts) and the `.` key re-run the build from the first step at one step per 900 ms without audio.
- [ ] `check_features.py`: on a slide with a stepped figure, parts start pending while narration is ready, `.` reveals them one by one to complete, and with `reduced_motion="reduce"` every part is shown on load.
- [ ] Commit.

### Task 5: Hero on the module page; segment figures in Read

**Files:** Modify `site_paths.module_page`, `site_pages.document_page` (lesson), `build_site.main`.

- [ ] `build_site` collects, per deck, the rendered figure HTML of slide 1 (the hero) and of each segment's first slide (keyed by segment id), rendered without `data-step` (complete).
- [ ] `module_page` shows the hero under the page head, above Learning objectives, when the deck has one.
- [ ] `document_page` for a lesson inserts each segment figure right after that segment's heading (using the `READ_UNIT` heading map).
- [ ] Commit.

### Task 6: The gate — `verify.py` Figures check

**Files:** Modify `course/06-production/verify.py`.

- [ ] `check_figures() -> list[str]` over every `slides.md` and `lesson.md`: each figure parses; has `alt` (≥ 12 characters); `source` resolves with `resolve_case_path` (when present); every `at:` on a slide matches a sentence of that slide's approved narration (`narration_data.load_scripts`); `image` files exist in `course/figures/shots/` and `scene` files in `course/figures/scenes/`; each `course/figures/manifest.json` entry's sha256 equals the file at its pinned commit (`git -C <repo> show <commit>:<path>`), and the copy's sha256 equals it too.
- [ ] Coverage: for modules listed in `FIGURE_MODULES` (empty in Part A; filled by Parts C–E), slide 1 and every segment's first slide carry a figure. Report as `[PASS] Figures (N figures, M stepped, K modules covered)`.
- [ ] Commit.

### Task 7: The rules — standard, skill, README; the sample stepped figure

**Files:** Modify `course/01-design/content-standards.md`, `.claude/skills/course-content/SKILL.md`, `course/learner-site/README.md`, `course/03-content/m02-ondevice-app/slides.md` (slide 3).

- [ ] Content standard: a **Figures** section — the five kinds, the grammar, when each is used, the hero and segment-opener requirement, `alt`, `source`, `at:`, screenshots as provenance-recorded copies, scenes labelled as illustrations, "a figure replaces bullets".
- [ ] Skill: in "A new module", a **Figures** step (hero, a figure per segment opener, screenshots on product claims) and the registration step "add the module to `FIGURE_MODULES` in `verify.py`".
- [ ] M2 slide 3: replace the `_diagram: stack` list with an `architecture` figure of the same words, parts stepped on the narration's sentences; `source:` the pipeline's files.
- [ ] Run the full gate `bash course/check.sh`; commit; PR "Figures 1"; merge on green; close #99 with evidence.

## Part B — screenshots and scenes (#100)

### Task 8: Screenshot copies with provenance; scenes

**Files:** Create `course/06-production/figures_shots.py`, `course/figures/manifest.json`, `course/figures/shots/*`, `course/figures/scenes/*.svg`.

- [ ] `figures_shots.py copy <repo>/<path> [--as <name>]` runs `git -C ../<repo> show <commit>:<path>` (commit from the pinned table in `gate.yml`), writes `course/figures/shots/<name>`, and records `{name, repo, path, commit, sha256}` in `manifest.json`; `figures_shots.py verify` re-checks all entries (used by `verify.py`).
- [ ] Copy: SignUpFlow `docs/screenshots/current/basketball/1440/{dashboard,onboarding,schedule-change-admin,replacement-needed}.png`; ListenToMe `docs/images/screenshot.png`; ai_qe — the diagram SVGs used as evidence of its own figures (`_includes/diagrams/context-route.svg`, `contract-chain.svg`).
- [ ] Scenes (hand-drawn SVG, Studio tokens as `currentColor`/CSS vars, 640×360): `meeting.svg` (a call with a copilot pane), `stranger-clone.svg` (a stranger at a terminal with a repo), `buyer-checkout.svg`, `auditor.svg` (a reviewer with a checklist), `launch-arc.svg` (emails to a page), `cohort.svg` (a small group, a demo). Each with a `<title>` and used by one figure.
- [ ] Gate green; PR "Figures 2"; merge; close #100.

## Parts C–E — module figures (#101 M0–M3, #102 M4–M6, #103 M7–M9)

### Task 9 (one per module, executed per part)

For each module `mNN`, reading its lesson, slides, narration and the case-study sources first:

- [ ] **Hero (slide 1 + module page):** one `architecture` or `flow` figure of the whole system or method, with this module's part flagged `hl`.
- [ ] **Segment openers (3):** one figure each — the segment's system or process — with `at:` build-ins on the sentences that walk it; trim bullets the figure now carries so the slide fits.
- [ ] **Screenshots:** on the module's product-claim proof slides, a `screenshot` figure from `course/figures/shots/` with 2–4 callouts drawn from what the narration says.
- [ ] **Scenes:** where a segment opens on a human situation (a stranger test, a buyer, an auditor, a demo), the matching scene.
- [ ] Add the module to `FIGURE_MODULES`; run `check_player.py --deck mNN --strict-fit` and `verify.py`.

Per part: full gate; PR; merge; close the issue. Part E also closes #98 when all ten modules are in `FIGURE_MODULES`.

---

## Self-review

- Spec coverage: kinds (T1), slides + reading (T2, T5), `_diagram` redrawn (T2), motion (T3, T4), sourcing and screenshots (T6, T8), scenes (T8), checks (T4, T6, strict fit in T2/T3), skill and standard (T7), delivery (Parts A–E). Refinement vs the spec: figures render as HTML with SVG connectors rather than all-SVG, so text wraps on phones, uses the slide type scale and is contrast-audited like other text.
- Names are consistent: `figures.parse`, `figures.render`, `figures.from_list`, `figures.step_index`, `FigureError`, `FIGURE_MODULES`, `data-figure`, `data-step`, `data-fig-replay`.
