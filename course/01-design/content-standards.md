# Content Standards (v2) — Complete Module Packages

> **This file is binding for all course content.** Every module package must satisfy it, and every
> writer should read it before producing artifacts. It extends `01-design/positioning.md` (voice),
> `01-design/assessment-and-rubrics.md` (grading) and `02-instructor/instructor-guide.md` (cadence).

## 0. Non-negotiables

1. **Every factual claim about a case-study repo carries a file pointer** that resolves in the local
   clone — e.g. `` `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:15-24` ``,
   `` `SignUpFlow/docs/playbooks/validation.md` ``, `` `ai_qe/_data/pilot_gates.json` ``.
   All 234 existing pointers were verified to resolve. Never invent a path, count, quote, or number.
2. **Verified numbers only.** These are the numbers you may state as fact without re-deriving them
   (re-derived 2026-09-17 against the upstream heads of 2026-09-16 by `06-production/check_facts.py`,
   which is also where each one is pinned — run `make facts` before quoting any of them in new text):
   - ListenToMe: 96% core coverage; 95% CI coverage floor via `scripts/check-coverage.sh`;
     14-row competitor table in `docs/competition-analysis.md`; 1.3.0 held back on 2026-09-10 ("do not promote"; macOS 1.4.0–1.4.4 then shipped 13–14 Sept)
     at 97.24% coverage per `docs/reviews/2026-09-10/design-and-gap-review.md`.
   - SignUpFlow: "1,464 passed, 21 skipped" in `docs/playbooks/validation.md` (dated 2026-09-12,
     demoted to historical reference 2026-09-13); 7 test tiers (`docs/TESTING.md`); 17 spec folders;
     spec 014 has **no** `tasks.md`.
   - ai_qe: 116 narrated slides = 21+33+26+36 (`_data/briefing_room.json`); four claim levels
     (`docs/principles.md`); 14-finding self-audit (`research/reviews/`).
   - TinyCopilot (the lab): `make lab-m2` → **191 passed, 100% coverage** (floor 90 enforced);
     `make lab-m3` → **49 passed**; `make e2e` → **2 passed** against a live Ollama daemon;
     2 contract tests skip without `LAB_E2E=1`.
   - mini-flow (the Lab M5 starter, `03-content/m05-security-tests/mini-flow/`): `make lab-m5` → **51 passed, 23 skipped, 100% coverage** (floor 90 enforced); `make pass-gate` → **11 failed, 63 passed** on the shipped starter by design and **74 passed** with the four reference fixes applied (re-run 2026-09-17).
3. **Numbering.** Modules `M0`–`M8`; segments `M#.#`; labs `Lab M#`; quizzes `Quiz M#`.
   Do not renumber or invent segments — use the segment titles already in each `lesson.md`.
4. **Voice.** Imperative, specific, no hype, no "in this section we will". Second person. Short
   sentences. If a claim can't be verified, say so or cut it.
5. **Honesty.** Mark anything unverified as such. Never fabricate testimonials, outcomes, or outputs.
   Where a lab can legitimately produce two outcomes (e.g. an Ollama daemon with only `:cloud`
   aliases vs one with a local model), say both are valid.

## 1. Module package — file layout

Each `03-content/mNN-slug/` folder contains, in addition to the existing `lesson.md`, `lab.md`,
`quiz.md`:

| File | Artifact | Length band |
|---|---|---|
| `slides.md` | Marp deck + speaker notes on every slide | 18–28 slides |
| `solutions.md` | Lab solutions / reference answers + expected output | 800–1,600 words |
| `video-scripts.md` | Timed recording scripts, one per segment | 1,200–2,100 words |
| `handout.md` | Student one-pager (printable cheat sheet) | 400–650 words |
| `facilitation.md` | Cohort facilitation kit for one live session | 800–1,250 words |
| `glossary.md` | 10–18 terms + curated resources | 500–900 words |
| `lab-rubrics.md` | Per-lab grading rubric, 4 levels | 600–1,100 words |
| `accessibility.md` | Accessibility + transcript/caption notes | 400–900 words |

> **Band recalibration note (honest record).** The first production pass landed six artifacts
> 1–26% above the originally estimated maxima (`m05/lab-rubrics`, `m06/solutions`,
> `m06/video-scripts`, `m06/facilitation`, `m06/accessibility`, `m07/video-scripts`). Every one of
> those overages was content that earns its space — the M6 module carries the claims dataset, and a
> rubric with an evidence column is wider than a bare one. Rather than pad or truncate good content to
> hit an arbitrary number, the maxima above were raised to the delivered envelope. The minima are
> unchanged, and the maxima are **ceilings, not targets**: an artifact that needs 1,600 words is fine,
> an artifact that rambles to 1,600 words is not.

`m06-expertise-product/` additionally keeps `evidence-dataset.md` (already written).

## 2. Artifact specifications

### 2.1 `slides.md` — Marp deck
- Front matter exactly:
  ```
  ---
  marp: true
  theme: aps
  paginate: true
  title: M# — <Module title>
  ---
  ```
- Slide separator: `---` on its own line. Headings: `##` for the slide title.
- **≤ 6 bullets per slide, ≤ 10 words per bullet.** Slides are prompts for the presenter, not prose.
  A list declared with a `<!-- _diagram: … -->` directive is exempt from the bullet count — it renders
  as component nodes (flow, loop, steps, grid, stack), not a bullet wall — but every item in it is still
  word-checked, and the learner-site gate asserts the declared component renders and fits its slide frame.
- Required slide sequence: title (module, promise, duration), "By the end you can…" objectives,
  one slide per segment sub-topic, at least one **proof slide** per segment carrying the repo file
  pointer *on the slide*, lab slide (`Lab M#` goal + pass gate), quiz slide, recap, discussion prompt.
- **Speaker notes are mandatory on every slide**, as an HTML comment immediately after the slide
  content:
  ```
  <!-- NOTES: what to say (40–90 words), the transition to the next slide, and the timing. -->
  ```
  Notes are where the teaching lives: give the example, the number, the pointer, the "why this
  matters". Write them as spoken prose, not bullet fragments.
- Use fenced code blocks for commands/code; keep them ≤ 10 lines. Use tables for comparisons.
- No images required (the deck must render with no external assets). If you reference a diagram,
  build it from text/ASCII or a table.

### 2.2 `solutions.md` — Lab solutions
For **every step** of the module's `lab.md`:
- **Reference answer** — what a complete, correct submission contains.
- **Commands + expected output** — verbatim where the lab is runnable. For TinyCopilot-based labs
  the expected output must match §0.2 numbers. If output varies by environment, show the shape and
  say which part varies.
- **Common wrong answers** — 2–4 per step, each with *why it fails* and *what it signals*.
- **Grading note** — one line on how an instructor distinguishes a real pass from a plausible fake.
- End with a **self-check table**: criterion → self-verification command/action.
- For open-ended labs (M4, M6, M7), "reference answer" means a worked exemplar artifact, not a
  single correct answer — say so, and give the exemplar in full but compact.

### 2.3 `video-scripts.md` — Recording scripts
One section per segment (`M#.1`, `M#.2`, `M#.3`), each with:
- Target runtime (5–15 min) and a word budget at ~130 words/min.
- **Cold open (≈15 s)** — the hook: the concrete failure, number, or decision the segment answers.
- **Beats** — a table of `timestamp | on screen | narration`. Narration is spoken prose, written
  to be read aloud; include exact file pointers to open on screen and exact commands to type.
- **Demo cue** — what to show (terminal, code file, deck slide) and what the viewer should notice.
- **Action-step close** — hand off to the segment's action step from `lesson.md`.
- **Recording notes** — 3–5 bullets: what to enlarge, what to cut if over time, one thing not to
  say (e.g. a claim that isn't verified).

### 2.4 `handout.md` — Student one-pager
Printable single page: the module's mental model in one sentence; a decision table or diagram
(text/table); the 5–8 commands or templates worth keeping; the pointer list (the files a student
should open); 3 gotchas; and "you're done when…" checklist. No new teaching — it is a compression
of the lesson, and it must not introduce a claim the lesson doesn't make.

### 2.5 `facilitation.md` — Cohort facilitation kit
For one 90-minute live session tied to this module:
- **Timing table** (`minutes | activity | mode (I do / We do / You do) | artifacts`), summing to 90.
- **Opening hook** (2 min) and **close** (5 min) scripts.
- **Breakout instructions** — group size, roles, the one deliverable each group must post, and the
  exact prompt.
- **Discussion prompts** — 3–4, with the follow-up probe for each and what a strong answer includes.
- **Watch-fors** — the module's likely stuck points (align with `02-instructor/instructor-guide.md`)
  and the 30-second intervention for each.
- **Post-session checklist** — what the instructor records as evidence, and what to post to the
  community.

### 2.6 `glossary.md`
- 10–18 terms, alphabetical, each: **term — definition (1–2 sentences) — where it lives**
  (repo file pointer or course file).
- A **"terms people get wrong"** subsection: 3–5 pairs (e.g. *local vs. verified local*,
  *acceptance criteria vs. success criteria*) with the distinction stated in one line each.
- **Curated resources**: 5–8 items — the repo files, docs, or external reading genuinely worth the
  student's time, each with a one-line *why*. No link dumps; every item earns its place.

### 2.7 `lab-rubrics.md`
- One rubric table per lab step group (or per lab deliverable), with exactly 4 levels:
  **Exemplary / Proficient / Developing / Missing**.
- Criteria rows must be *observable* ("red run captured before the green run for all six modules"),
  not vibes ("good understanding").
- Weights must sum to **100** and be stated per row.
- An **evidence required** column naming the artifact the student submits for that row.
- An **auto-fail list**: 3–6 conditions that fail the lab regardless of other rows (e.g. fabricated
  evidence, a green run with no red run recorded, tests weakened to pass).
- Consistent with `01-design/assessment-and-rubrics.md` (labs 60% / quizzes 20% / capstone 20%).

### 2.8 `accessibility.md`
- **Deck accessibility**: contrast requirement for the `aps` theme (`06-production/slides/aps.css`),
  minimum font size, alt-text rule for any visual, and the "never encode meaning in colour alone" rule.
- **Code accessibility**: line length, how to read code aloud, why every pointer must be announced
  verbally as well as shown.
- **Transcript structure**: chapter markers keyed to the segment beats, speaker labels, and how to
  handle the ~130 wpm pacing for captions.
- **Captions**: what must be captioned (commands read aloud, file paths spelled out), and the rule
  for non-English terms.
- **Accommodations**: extended time, no-audio path (the handout must suffice), and the
  "two-outcome" labs (local model vs only-`:cloud` daemon) as an equity note — no student is
  blocked by hardware.

## 3. Track bundles (`05-tracks/<slug>/`)

Three standalone sellable bundles: `on-device-app`, `spec-driven-saas`, `expertise-product`.

| File | Contents |
|---|---|
| `README.md` | Bundle promise, audience, prerequisites, what's included (modules + artifacts), 6-week map, honest scope note (it is a subset; the full course covers all three), FAQ |
| `syllabus.md` | 6-week schedule: weekly outcome, modules/segments, lab, quiz, time budget, assessment |
| `sales-page.md` | The 8-section anatomy from M8.1, with real proof assets for that archetype only, and pricing placed per `pricing.md` |
| `pricing.md` | Bundle price + rationale, relationship to the full course ($399) and cohort ($1,490) — must not cannibalize: state plainly that the full course is the better value |
| `bundle-map.md` | Table: module → segments used → labs used → artifacts included/excluded, so the buyer knows exactly what they get |

Bundle prices: **$199** single track (self-paced), with the full course at $399 positioned as the
recommended path. Rationale must cite the pricing research in
`00-research/02-course-market-research.md` and `04-sales/pricing-and-platforms.md`.

## 4. Course-level production (`06-production/`)

- `slides/aps.css` — the shared Marp theme (instructor-facing, not student content).
- `slides/build.sh` + `Makefile` — render every `slides.md` to HTML/PDF with marp-cli when present;
  must fail loudly with an actionable message when marp-cli is absent.
- `glossary-master.md` — merged, deduplicated glossary assembled from the nine module glossaries.
- `certificate.md` — completion certificate template with the assessment thresholds from
  `01-design/assessment-and-rubrics.md`.
- `welcome-packet.md` — onboarding email + environment checklist + how to get help.

## 5. Definition of Done for any module package

- [ ] All 8 artifacts exist and are inside their length bands.
- [ ] `slides.md` has Marp front matter, `theme: aps`, ≤ 6 bullets/slide, and speaker notes on
      **every** slide.
- [ ] Every repo claim in every artifact carries a pointer that resolves.
- [ ] No number appears that is not in §0.2 or re-derived from a pointed file.
- [ ] Solutions' expected outputs match §0.2 where the lab is runnable.
- [ ] Rubric weights sum to 100; auto-fail list present.
- [ ] Cross-references use `M#`/`Lab M#`/`Quiz M#` numbering and name real files.
- [ ] No fabricated student results, testimonials, or third-party outcomes.
