# Course figures: architecture, flow, screenshots and scenes — design

Date: 2026-09-27 · Owner feedback: "content is too dry — no image, diagram, animation of flow,
architecture or high-level view when a topic is introduced; not professional."

## Problem

Across 258 slides there are 24 "diagrams", every one a styled bullet list (`_diagram: flow|steps|grid|
stack|loop`). There is no drawn figure, no architecture picture, no product screenshot, no motion, and
the lesson pages have no visuals at all. The content standard also requires decks to render with no
external assets.

## Decisions (agreed in brainstorming)

1. **One visual system for slides and reading pages** — a figure is written once and appears on the
   slide and in Read.
2. **Motion:** narration-synced build-ins for flow and architecture figures; a one-time draw-in for the
   others; screenshots and scenes are still. `prefers-reduced-motion` shows figures complete.
3. **Imagery:** real product screenshots from the three case-study repos *and* a small library of
   hand-drawn illustrations ("scenes").
4. **Rollout:** the system first, then all ten modules in one pass.
5. **Figures are part of making a module:** the `course-content` skill and the content standard require
   them, and the gate fails a module without them.

## Figure kinds

A figure is a fenced block in a slide or lesson, ```` ```figure ````, holding YAML-like `key: value`
lines (parsed by a small hand-written reader — no new dependency). Every figure has `kind`, `alt`, and
— when it depicts a case study — `source`.

| Kind | Shows | Parts |
|---|---|---|
| `architecture` | layers of boxes on a grid, seams marked | `layers:` each with `name` and `boxes` (`label`, optional `note`, `seam: true`) |
| `flow` | a pipeline or sequence, optional loop back | `steps:` each with `label`, optional `note`, `seam: true`; `loop: true` |
| `compare` | two or three columns side by side | `columns:` each with `title`, `items`, optional `tone: good|bad|neutral` |
| `screenshot` | a real image in a browser or device frame, numbered callouts | `image` (a file in `course/figures/shots/`), `frame: browser|phone|mac`, `callouts:` (`x`,`y` in %, `text`) |
| `scene` | a hand-drawn illustration | `scene` (a file in `course/figures/scenes/`), `caption` |

Any part of an `architecture` or `flow` figure may carry `at: <words>` — the opening words of the
narration sentence at which it builds in.

Rendering: `course/learner-site/figures.py` turns each block into inline SVG (architecture, flow,
compare) or an `<figure>` with framed `<img>` and positioned callouts (screenshot, scene). Colours come
only from the Studio tokens: cobalt marks a seam / "act here", amber marks evidence, ink the core. Text
in SVG is real `<text>` (searchable, selectable, contrast-audited).

## Where figures appear

Per module:

1. **Hero** — the module overview page and the cover slide carry one high-level figure: the whole
   system or method, with this module's part highlighted.
2. **Segment opener** — each segment's first slide carries an `architecture` or `flow` figure; the same
   figure heads that segment in Read.
3. **Proof with a screenshot** — where a claim is about a product, a real screenshot beside or instead
   of bullets.
4. **Lessons** — larger figures (a full request path) where there is room.

The 24 `_diagram` lists are redrawn as `flow`/`architecture`/`compare` figures with the same words.
Target volume: ~10 heroes, ~30 segment figures, 24 upgraded diagrams, 10–15 screenshots, 6–8 scenes.

A figure replaces bullets; it never adds to a full slide. Every slide still fits its 16:9 frame
(`check_player.py --strict-fit`). Narration words do not change.

## Motion

- The build resolves each `at:` to a sentence index of the slide's approved narration (the same
  sentence split the transcript panel uses) and writes `data-step="n"` on the part.
- The player reveals parts as their sentence is spoken (it already times sentences from captions).
  With no audio (the text-first copy) a stepped figure starts complete and → still moves slides; on the
  slide itself the learner can press **Step** (or `.`) to replay the build. Read shows figures complete.
- Figures without `at:` draw in once when their slide is shown (CSS stroke animation).
- `prefers-reduced-motion` and print: every figure complete, no animation.

## Sourcing and honesty

- `source:` on a figure is a pointer the gate resolves like any other citation, shown as the figure's
  source chip.
- Screenshots are copied at the pinned commit into `course/figures/shots/`, recorded in
  `course/figures/manifest.json` (repo, path, commit, sha256). The gate checks each copy is
  byte-identical to the file at the pinned commit. Callouts are drawn over the image, never into it.
- Scenes are illustrations; their caption says so and they cite nothing.
- Every figure has `alt` describing what it shows; meaning is never carried by colour alone (seams are
  also labelled).

## Checks (the gate)

- `verify.py` **Figures**: every module has a hero and a figure on each segment opener; every figure
  has `alt`; `source:` resolves; screenshot copies match their origin; every `at:` matches a sentence
  of that slide's narration; every `image`/`scene` file exists.
- `check_player.py`: strict fit for all slides with figures; contrast inside SVG; figures fit a
  390px phone.
- `check_features.py`: a stepped figure builds by narration sentence and by the Step control, and is
  complete under reduced motion.
- The screenshots artifact (#81) shows the figures on every PR.

## Delivery

One tracking issue; sub-issues: (1) the figure system — renderer, motion, checks, skill and standard,
with the 24 existing diagrams converted to prove it; (2) screenshots and scenes library; (3) figures
for M0–M3; (4) M4–M6; (5) M7–M9. Each PR keeps the gate green and follows AGENTS.md.

## Out of scope

Video; a figure editor; changing narration words; the release voice (#21).
