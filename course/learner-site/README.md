# Learner site

The learner-facing build of the course: nine decks, one slide at a time, with narration, synchronized
captions, a transcript, and navigation that works with a keyboard.

```bash
cd course
make narration-preview   # free local preview voice (or `make narration` with ELEVENLABS_API_KEY)
make site                # generate index.html and mNN.html
make serve               # http://localhost:8043
```

`make site` is enough to read the decks; narration is layered on when recordings exist. A deck with no
recordings is still fully readable, and the player says so instead of failing.

## What is generated

| Path | Source | Committed? |
|---|---|---|
| `mNN.html`, `index.html` | `03-content/mNN-*/slides.md` + `06-production/narration/manifest.json` | No — generated |
| `narration.json` | `06-production/narration/manifest.json` | No — copied at build time |
| `assets/audio/…` | `generate_narration.py` | No — generated (see the narration README) |
| `assets/player.js`, `narration-media.js`, `player.css` | hand-written | **Yes** |
| `assets/fonts/source-sans-3.woff2` | Source Sans 3, SIL OFL 1.1 (licence travels with it) | **Yes** |
| `build_site.py`, `check_player.py` | hand-written | **Yes** |

## Design system

The presentation layer is ported from **ai_qe**, the third case study, because that site is the one
this course holds up as its own standard for publishing claims a skeptic can audit. What was borrowed,
and what was deliberately changed, is written down rather than implied:

| Borrowed | Detail |
|---|---|
| Typeface | Source Sans 3, self-hosted `woff2`, `font-display: swap`, preloaded |
| Palette | navy `#152e40` · teal `#096d69` · mint `#85d5c4` · ink `#405563` · paper `#fcfcfa` on `#eaf0ec` |
| The 16:9 master | `--frame-width: min(100vw - 32px, (100dvh - chrome - narration) * 16/9)`, `.slide { aspect-ratio: 16/9 }` |
| Container-query type | slide type is sized in `cqw`, so it scales with the frame instead of the viewport |
| Kicker + title | `M0.1 — Three archetypes` renders as kicker `M0.1` and title `Three archetypes`, exactly ai_qe's `02 / Strategic target state` |
| Source footer | every slide carries a full-height left spine — kicker, running head, module tag, `NN / NN`, transcript link |
| Modes | presentation (full screen), reading view, notes drawer, one 16:9 slide per printed page |
| Chapter grouping | `data-chapter` per slide; the picker is grouped with `<optgroup>` |

Changed for this course: proof slides (`<!-- _class: proof -->`) get a dark, accented treatment so the
evidence slides change the deck's rhythm; the vocabulary is limited to what these decks contain
(bullets, tables, code, takeaways, pillars, metrics); and the honesty badge for the preview voice keeps
its own light-theme styling because it must be legible wherever it appears.

### The editorial rail

The first port was faithful to ai_qe's *chrome* but not to its *composition*, and an audit of the built
site found why it read flat. Measured across all 233 slides:

| Measured | Before | After |
|---|---|---|
| Content block as a share of the frame's inner height | 45%, top-aligned in the corner | **59%, optically centred** (164px above, 164px below) |
| Distinct type sizes in use | 11, including four inside 18–21px | **one 1.25 scale** |
| Distinct spacing values | 17, all fractional (`41.77`, `23.34`, `6.76`…) | **one 8pt grid in `cqw`** |
| Distinct hex colours in the stylesheet | 48, ≈20 of them outside the token block | **25 named tokens, zero literals outside the block** |
| Title / body size ratio | 2.29× | **2.61×** |
| Slide-chrome text as a share of frame height | 1.47% — dies on a projector | **2.40%** |
| Slides whose content shape is one bullet list | 143 / 233 = 61% (79% bullet-only) | unchanged — a content problem, not a CSS one |

The rail is the structural half of the fix: a spine running the full frame height gives the empty half
of the frame an edge to sit against, and the body block is centred against it. **This composes the
whitespace rather than eliminating it.** The content is still thin — a median 36 words per slide — and
no layout makes 36 words fill a 16:9 frame. Making the deck *look* full would mean inventing content,
which this course does not do.

The scale lives in `.slides` as custom properties (`--t-chrome` … `--t-display`, `--s1` … `--s8`).
Below 700px the mobile block redefines those tokens to `rem` values — one breakpoint, one place, which
is what stops container-query type from rendering 5px chrome on a phone. The index and transcript pages
run on a tighter seven-step document scale (`--d-1` … `--d-7`) because 1.25 steps are too coarse for UI
text; they previously used twenty sizes, nine of them inside 11–15px.

`check_player.py` asserts the system's own rules so they cannot drift back: ≤8 type sizes, ≤8 text
colours and ≤14 spacing values on any slide; title/body ≥2.5×; chrome ≥2% of frame height; every slide
optically centred; a rail with a real spine rule on all 233; and **no text below WCAG AA**. These are
measured across **every** slide — an earlier version measured only the visible one, which in deck-ready
mode is always the cover, so any content slide could have drifted unnoticed. Centring is measured on the
*content extent*, not the body box: the body is a stretch-aligned grid item, so measuring its box would
be trivially centred.

### Colour is resolved per slide kind, not per override

The first version of the rail wired each component colour by hand and then hand-wrote a `.slide-proof`
override for each one. That is a bug factory: every new component is one forgotten override away from
invisible text, and two were already forgotten — inline `code` on the cover rendered at **1.16:1**, and
`blockquote` on a proof slide at **2.31:1**. Neither was caught, because the checker had no contrast
assertion at all.

Components now reference semantic names (`--c-ink`, `--c-rule`, `--c-surface`, `--c-code-bg`,
`--c-accent`, …) and the slide *kind* redefines them once:

```css
.slide-proof, .slide-cover { --c-ink: var(--navy-ink); --c-accent: var(--mint); … }
```

No `.slide-proof <component>` colour override remains. Every colour in the stylesheet is a named token —
including `--white` — and `check_player.py` fails on any hex literal of any length outside the token
block. An earlier claim of "zero literals outside the block" was only true for six-digit hexes; nineteen
`#fff` and a `#0003` had gone uncounted.

### The contrast audit

`apsAuditContrast` walks every text node in the rendered page, composites its real background by walking
ancestors through translucent layers, resolves gradient backgrounds to their stops and judges the text
against the **worst** stop, then applies the WCAG AA threshold (4.5:1, or 3:1 for large text). It runs
over all 233 slides plus the deck chrome, and over the landing page and all ten transcript pages — the
pages the deck probe can never see.

That last part matters: the landing page was shipping an invisible-heading bug. A global
`h1, h2, h3 { color: var(--navy) }` beat the element colour on `.room-cover`'s navy gradient, so **every
module card title rendered at 1.00:1**. It predates the rail (it is in `8cd140f`), and no amount of
reading the CSS caught it — it took a rendered-text audit. The audit is verified to fire: reintroducing
the bug fails the check with all nine titles named.

Still unmeasured by it: text inside `<dialog>` elements that are closed (the drawer and the transcript
modal are `display: none` until opened), and any text over a photographic background.


## Declared diagrams

A content audit of all 233 slides found the display language was the weak layer, not the substance:
79% of slides were bullet lists, 61% were *exactly* "heading + one bullet list", and there were **zero
images or SVGs in the entire course**. Where structure was needed, it was hand-typed: 13 slides encoded
flows as text arrows, and the two slides that needed real drawings — the Spec-to-Ship Loop and the
ListenToMe pipeline — faked them with `│` and `▼` box characters. The method loop had even *lost an
arrow to a line wrap* (`3. BUILD 4. VALIDATE`), which nobody noticed because a wrapped text diagram was
the house style.

The fix is a **`_diagram:` directive** in the slide Markdown, next to `_class:`. It upgrades the next
list at that position into one of five components — `flow`, `loop`, `steps`, `grid`, `stack` — and the
**words are frozen**: the nodes are the author's own bullets, only the arrangement is declared. The
source stays a valid Markdown list, so Marp still renders it, and the narration (the approved source for
anything spoken) stays true because the same words are displayed.

Thirteen slides carry diagrams: the Spec-to-Ship Loop (`loop`), the spec-kit pipeline's eight commands
(`flow`), the ListenToMe two-layer architecture (`stack`), the decision anatomy, three grids (the
archetypes, the three defenses, the three enforcers), and five numbered procedures (`steps`).

What the gate asserts, so this cannot regress:

- **Every declared diagram renders** — `_diagram: flow` in the source must produce exactly one
  `diagram-flow` component in the built slide.
- **No hand-typed diagrams come back** — box-drawing characters anywhere in a slide fail the check, and
  so does a chain of three or more `→` arrows in a single text block outside a diagram component. One
  arrow in a bullet ("command → result") is legitimate notation; a four-stage chain in prose is a
  diagram trying to escape.
- Objectives and recaps that *rehearse* a chain already drawn elsewhere in the deck are allowlisted in
  the check, with the reason recorded next to each entry.
- **Every diagram fits its frame** — `check_diagram_geometry` opens each diagram slide by deep link and
  measures the component against the 16:9 frame, which clips overflow invisibly. This assertion is not
  hypothetical: the first build of `steps` overflowed m07's eight-section slide by 287px, and a subtler
  grid bug (the caption landing on its own implicit grid row) doubled every labelled row.
- **Diagram slides get the contrast audit** — the deck probe audits slide 1 (a cover, no diagram), so
  the geometry probe runs `apsAuditContrast` on every diagram slide at its real layout.

Two content findings from the audit, deliberately **not** auto-fixed because both would desync approved
narration: the m02 objectives slide names five pipeline stages while the architecture slide teaches six
(`store` is missing from the objective), and the player's resume-from-localStorage beats `#slide-N`
deep links, so a returning learner clicking a unit's "Open →" lands at their saved position instead.

The word-freeze was verified mechanically: every converted slide's rendered word multiset was compared
before and after. Six slides changed by documented design — the m00 loop drops its duplicated hand-typed
stage line, the m02 stack names the three seam positions the narration already names
(AudioCapturing/Transcribing/LLMProvider), the two `steps` labs render "Step N" as numerals, and three
label/caption splits consume a separator character. Everything else is byte-identical word-for-word.



## Learning paths

The site was nine decks in a grid: one order, no entry point for anyone who did not want all of it.
Microsoft Learn solves this with a four-level hierarchy — **career path → learning path → module →
unit** — and one fixed unit grammar inside every module:

```
Introduction → content units → Exercise → Knowledge check → Summary
```

This course already had every level of that. It just never surfaced one, and the mapping is exact:

| Microsoft Learn | Here | Count |
|---|---|---|
| Career path | an archetype entry point | 4 paths |
| Learning path | a track bundle in `05-tracks/` | 3 + the full course |
| Module | `m00`–`m08` | 9 |
| Unit | a lesson segment, lab, quiz, intro or recap | **63** |
| Exercise | `Lab M#` | 9 |
| Knowledge check | `Quiz M#` (8 questions each) | 9 · 72 questions |
| Summary | the recap + discussion prompt | 9 |

A unit is a **lesson segment**, not a slide: 63 units over 233 slides averages 3.7 slides a unit, which
sits inside Microsoft's 3–10 minute unit size, while a single slide averages 34 seconds and would be
a meaningless thing to mark complete.

### The unit model is derived, and asserted

`site_paths.module_units()` partitions each deck, and the boundary rules are read off the course's own
structure rather than invented:

- slides 1–2 are the cover and the objectives in **all nine decks**, so they are the Introduction;
- a slide whose *title* opens `Lab M#`, `Quiz M#` or `Recap` starts an Exercise, knowledge check or
  Summary — matched on the title, because the deck chrome deliberately falls back to the module tag
  for these and never shows `Quiz M#` as a kicker;
- a slide whose kicker is `M#.#` starts that segment;
- a module that marks fewer segments than it declares still opens segment 1 at the first content
  slide. `m08` has no `M8.1` heading anywhere in its source — without this rule, five minutes of
  segment-one content would have been filed as the Introduction.

`check_player.py` asserts the result covers all 233 slides **exactly once**, that every module has an
intro, three segments, a lab, a quiz and a summary, and that the total is 63.

It then cross-checks the model against a number written by hand: `bundle-map.md` states the On-Device
path is *"17 of 27 teaching segments · 4 of 8 full labs · 5 of 9 quizzes"*. The model derives 17
segments, 4 full labs and 5 quizzes from the decks alone. Two independent sources agreeing is worth
more than either one being internally consistent.

### A path must not claim what it does not teach

The first version of the path page listed all seven M8 units, including `M8.3`, `Lab M8` and
`Quiz M8` — every one of which the bundle map explicitly excludes — and counted their narration in the
path total. Slice modules now carry an explicit `exclude` list and mark the rows: M8 reads
**"4 of 7 units · 10.3 min"**, with the three excluded units struck through and labelled *not in this
path*, and M7's lab is labelled *part only* because the path includes steps 1–5.

### Durations are measured, not estimated

This is the one place the implementation deliberately beats the model it copies. Microsoft Learn shows
an estimated duration per unit; every duration here is summed from the narration manifest's real
per-slide durations. Lab units show **both**: the narration seconds *and* the lab's hands-on time,
quoted from the module's own source, because a lab is hours of work whose narration is one slide.
`site_paths.lab_time()` reads it from `lab.md` where stated and falls back to the deck front matter
otherwise, and never infers a number from narration.

### Progress is local and says so

The module page has a checkbox per unit and a progress bar, stored in `localStorage` under
`aps.progress.v1`. There are no accounts on this site, so the page states plainly that progress is
stored in one browser and follows you nowhere. Showing a percentage that silently resets on another
device would be a lie told by a progress bar.

### Not adopted

The gamification layer — XP, levels, trophies, streaks. `learn.microsoft.com/en-us/training/achievements/`
returns 404 and the browse page is client-rendered, so the mechanics could not be verified, and
inventing a points economy and calling it "the Azure framework" would be slop. Badges and an
Achievements surface are documented; what they *do* is not.

### Sorted by product type

The three paths are the three **product types** the course is built from, named in the bundle maps as
Type 1/2/3 and each anchored to a real product:

| Path | You build | Product type | Case study |
|---|---|---|---|
| On-Device AI Apps | an **app** | Type 1 · AI with an app | ListenToMe (Swift/macOS) |
| Spec-Driven AI SaaS | a **web service** | Type 2 · AI with the web | SignUpFlow (FastAPI) |
| Expertise as a Product | a **content product** — a learning site, a presentation, a sales pitch | Type 3 · AI with content | ai_qe (116-slide narrated briefing) |

The third is the least obvious and the most literal: `ai_qe` is a narrated, routed, editioned learning
product, and this site is built on the same port. Its bundle map lists the case-study files a Type 3
builder actually opens — the four claim levels, the benchmark records carrying date/sample/method/unit,
the immutable release editions, the phased pilot with sponsor-signed gates, and the executive
presentation script.

### Status

Three of the four paths are built end to end: paths index, a path page for the On-Device, SaaS and
Expertise tracks, and module pages for all nine modules. The full studio course is not a separate page
because it *is* the module index, and its card says so rather than pretending to be one.

### The landing page is the path chooser

The site used to open with nine decks in a grid and a link to the paths. It now opens with the
question the paths exist to answer — *what do you want to build?* — and the four cards are the
primary content, with the module grid below it as the second section. The chooser is generated by
the same `path_cards_html()` as the paths page, from the same `TRACKS` data, so the two surfaces
cannot disagree about what exists.

Module cards now open the **module page** rather than dropping straight into a deck: the module page
is the path-aware surface, it lists which paths include the module, and the deck is one click further
down. A learner who wants the raw deck can still reach it from every path page, every module page and
the slide rail.

### Modules are shared, and the pages say so

M0 and M1 sit in **all three paths in full** — they are the shared core. M7 and M8 are sliced into
all three, each with a *different* exclude list. A module page that named a single owner path would
misdescribe the other two, so every module page renders one row per path that includes it, with that
path's inclusion:

- `module-m00.html` — three rows, each "full module".
- `module-m07.html` — three rows, and three different treatments: **App** keeps Lab M7 steps 1–5 and
  Quiz M7; **Web** excludes the lab *and* the quiz; **Content** keeps the lab for the Type 3 offer
  only. Same module, three honest descriptions.
- `module-m02.html` — one row, because only the App path teaches it.

The gate asserts this: every module page must list exactly `len(paths_for_module(id))` path rows, M0 /
M1 / M7 / M8 must each sit in all three built paths, and the landing page must offer every built path
*before* the module grid.

The three paths differ in ways the model has to respect rather than smooth over:

- **On-Device** keeps Lab M7 (steps 1–5) and Quiz M7 — 5 quizzes.
- **SaaS** excludes Lab M7 *and* Quiz M7, because the week-6 capstone worksheet replaces the lab. Same
  17 segments as On-Device, but **4 quizzes, not 5**.
- **Expertise** is the only path that keeps **M8.3 and Quiz M8** — but the capstone and Lab M8 are the
  *Type 3 row only*, so both are marked partial rather than excluded.

Only the first two state a course-wide total in their bundle map ("17 of 27 teaching segments · 4 of 8
full labs · …"), so only those two are cross-checked by the gate. The Expertise map states none, so its
counts are derived from its own rows and the page labels them **derived** rather than quoting a total
that does not exist.


## Evidence exhibits

The depth audit that followed the diagram pass found the real cause of the "hello 101" feel: the
depth was in the *spoken* layer (86–103 words a slide, real numbers, real files) while the visible
face was a 36-word prompt — and the slides that teach a real Swift codebase showed **zero lines of
code**. A slide that says "newest-first fit, budget-bounded window" and cites
`ConversationStore.swift:56-67` without showing the loop is asking to be trusted.

The fix is the **evidence exhibit**: the cited code, verbatim, on the slide — a code fence under the
claims (fences were always exempt from the bullet budget; the budget is about prose, not proof). The
pilot is module m02, five slides: the three protocol seams, the `buildContext` signature with its
4,000-character default, the eleven-line `recentContext` loop whose guard is the "never empty"
guarantee, the token-prefix matcher, and the three-case `OllamaStreamError` enum. The narration for
those five slides was rewritten to walk the code, regenerated with the free local `say` preview
voice, and the manifest re-verified — the release voice (#21) is still uncut, so this is the window
in which scripts can change. The narration contract pins captions = transcript = script, so all
three regenerate together; the gate's repo-pointer check now verifies the exhibit pointers resolve
(1052 pointers).

Two rules for exhibits, learned from the pilot: the code is **verbatim from the repo** (whitespace
may reflow, tokens may not), and the fence joins the geometry gate — `check_diagram_geometry` opens
every slide carrying a `<pre>` by deep link and measures it against the frame, because a clipped
fence is invisible evidence, not a style bug.

### Exhibit pass, per module

| Module | Status | Exhibits |
|---|---|---|
| m02 — On-device app: architecture | **deepened** (86c9b8c) | 5: protocol seams, `buildContext` signature, `recentContext` loop, token-prefix matcher, `OllamaStreamError` enum |
| m03 — On-device app: privacy, testing, shipping | **deepened** | 6: `AIProcessingMode` enum + labels, `isVerifiedLocal` fail-closed guard, `RejectRedirects` delegate, coverage-floor gate (awk), the CI core job, the `XCTSkipUnless` e2e test |
| m05 — Multi-tenant security | **deepened** | 5: `get_person_in_actor_org` 404 query, the grep-able P0 rule from `AGENTS.md`, `normalize_roles` refusals, the route-policy docstring + class set, the dated-evidence retirement banner |
| m04 — Spec-driven SaaS | **deepened** | 6: `spec.md` FR-001 + story-1 GWT, `research.md` Decision 1, `plan.md` Constitution Check gate + NONE verdict, rate-limit contract table, checklist verdict `Quality Score: 100%`, `tasks.md` T017/T002 format |
| m06 — Expertise product | **deepened** | 4: METR + Peng benchmark records verbatim, the `document-manifest.json` M02 `"unavailable"` entry, the `Makefile` check target, a `narration-review.json` retained verdict with its reason |
| m07 — Monetize | **deepened** | 3: the competition-analysis header convention (dated + approximately/reportedly), the §C research line with the 70–85% rule and the Zoom-records verdict, the cost-floor arithmetic from the sales doc |
| m08 — Launch | **deepened** | 3: the landing page's own headline + isn't-list, the launch plan's deliverability prerequisites + verified checkbox, the founding-cohort trade line ($990 in exchange for a testimonial and feedback) |
| m00 — Orientation | **deepened** | 1: the three proof lines verbatim — the 96% coverage badge, "1,464 passed, 21 skipped", the dated site-audit header (Reviewed edition 1.2.1) |
| m01 — Operating system | **deepened** | 2: the constitution's own head (one sentence of purpose, version 1.1.0), spec 019's T027/T028 task lines with contracts and file paths |

**Pass complete: 9/9 modules deepened, 33 exhibits on the slides, 30 scripts rewritten to walk
their evidence, all preview recordings re-synthesized, manifest 233/233 at every step.**

m03 discipline notes: the awk gate and the CI job are exhibits with one elision each, marked `# …` /
verbatim lines around it. The `isVerifiedLocal` guard and `RejectRedirects` delegate reflowed
whitespace only. All six scripts walked their code and the preview voice re-recorded them
sentence-measured; manifest 233/233 re-verified; gate green.

## Transcripts

Every deck has a transcript, committed as Markdown rather than generated HTML:

```
learner-site/transcripts/m00.md … m08.md   one deck each
learner-site/transcripts/ALL.md            all nine modules in one file, with a table of contents
```

Each file carries the slide number, title, per-slide duration and caption method, then the spoken
words. **Speaker notes are excluded** — they are the presenter's version, not the narration. The words
are the approved narration scripts, so the transcript is a true text alternative to the audio and does
not change when the release voice is recorded. Each deck page has a **Transcript** link in its toolbar.

The convention that makes it checkable: **a line starting with `> ` is spoken narration and nothing
else.** Headings, timing and the voice note are ordinary lines, so `words()` over the blockquotes must
equal `words()` over the approved script. `build_site.py` asserts that at generation time,
`validate_narration.py` asserts it on the committed files, and `build_site.py --check` fails if they
are stale. Do not put metadata in a blockquote.

```
$ python3 06-production/narration/validate_narration.py --no-media
Transcripts verified: 10 documents match the approved scripts (22,239 words)
```

## Page structure

Each deck page is a 48px header, the 16:9 frame, a fixed navigation strip, and a notes dialog.

```
deck page
├── header        brand · module · slide meta · Play narration · Present ↗ · Read all
│                 Sources & notes · Transcript · voice chip
├── main.slides   one <section class="slide"> per slide
│                 ├── .kicker      M0.1, Type 1, Lab M0 (falls back to "M0 · Orientation")
│                 ├── h2#slide-N-title
│                 ├── .slide-content
│                 └── footer        deck tag / slide transcript / 01 / 19
├── nav           ← → · live status · chapter-grouped slide picker
└── dialog        speaker notes for the current slide
```

Slide variants: `slide-cover` (slide 1, always), `slide-proof` (from `_class: proof`).

### Modes

| Mode | Control | Behaviour |
|---|---|---|
| One slide at a time | default | `goTo()` hides every other slide; the narration panel sits below the frame |
| Presentation | **Present ↗** or <kbd>P</kbd> | full screen, dark chrome, trimmed header; <kbd>Esc</kbd> leaves it |
| Reading | **Read all** | every slide as one scrolling document, 1200px measure |
| Notes | **Sources & notes** or <kbd>N</kbd> | dialog with the current slide's presenter notes |
| Print | <kbd>⌘P</kbd> | one 16:9 slide per page (`@page 13.333in 7.5in`) |

A deck without JavaScript still shows every slide in order, and the reading view has a CSS fallback so
it works even if the script never runs.

### Other pages

Every generated deck page is:

```
body[data-narration-manifest][data-narration-deck][data-site-base][data-voice]
  header.deck-header          title, slide/narration counts, Play narration, Captions download
  p.voice-badge               only when the recordings are a preview voice
  main#slides
    section.slide#slide-N     aria-roledescription="slide", aria-labelledby="slide-N-title"
                                data-audio / data-captions / data-duration from the manifest
      .slide-content          the rendered slide
      details.slide-notes     the presenter notes (not read aloud)
  nav.deck-navigation         prev · slide picker · next · status · message
  section.narration-panel     injected by player.js before .deck-navigation
    .narration-caption        the current cue
    .narration-controls       play · replay · seek · time · speed · CC · auto-next
    .narration-meta           status · Retry captions · Transcript
  audio[data-narration-audio]
```

Slides after the first are `hidden` so the page does not flash 233 slides before the script runs. A
`<noscript>` block reverses that for no-JS readers, and `@media print` reveals every slide.

## Player behaviour

* **No autoplay, ever.** Play starts the current slide; auto-next (on by default, opt-out) continues.
* **One clock.** Captions, the seek bar and the time readout all derive from `audio.currentTime`.
* **One audio owner per frame tree.** `narration-media.js` claims focus synchronously before buffering,
  coordinates across tabs via `BroadcastChannel` (with a `localStorage` fallback), and a cancelled play
  request cannot steal focus back.
* **A beat between slides.** Auto-next waits 2000 ms, or 700 ms under `prefers-reduced-motion`, and is
  cancelled by any navigation, seek, dialog or hidden tab.
* **Resume.** The last slide is remembered per deck in `localStorage` and offered back on return.
* **Captions on by default.** CC toggles them; every slide also has the full transcript in a dialog,
  labelled with the voice and the caption method.
* **A slide without a recording still navigates**, with an explanation rather than a dead player.
* **Keyboard:** `→`/`Space`/`PageDown` next, `←`/`PageUp` previous, `Home`/`End` first/last. Shortcuts
  are ignored while typing in a control or while a dialog is open.

## Accessibility

* One `h1` per page; slides are `<section>` landmarks labelled by their own heading.
* A polite status region announces `Slide N of M — title` on every move, and a separate live region
  announces playback and failure states.
* A skip link jumps to the slides. Focus follows the slide heading, not the window.
* Visible focus rings on every control; `aria-pressed` on Play and CC; `aria-valuetext` on the seek bar.
* Caption text is rendered as text, never as markup, and the cue element is `aria-live="off"` so a
  screen reader is not flooded during playback.
* Reduced-motion users get no smooth scrolling and a shorter auto-advance beat.
* Print output contains every slide, without the player chrome.

## Publishing

The site is generated and gitignored, so GitHub Pages cannot serve the repository as-is — it needs a
build. `course/publish_site.py` builds it and pushes the result to a `gh-pages` branch, which keeps the
generated HTML out of `main`:

```bash
python3 course/publish_site.py                 # text-first (default)
python3 course/publish_site.py --with-audio    # include the recordings so narration plays
python3 course/publish_site.py --dry-run       # build and stage, do not push
```

The gate runs first and the publish is refused unless it is green.

**The published copy is text-first by default.** The 233 recordings exist, but they are ~62 MB and
throwaway until the release voice is recorded, so the published copy tells the player there are no
recordings: `narration.json` is written empty, the narration panel and the Play button stay hidden
and no `data-audio` attribute is emitted. That is not cosmetic — it means **nothing 404s** and no
button offers a file the copy does not contain. The decks, the full design, all 233 transcripts and the
print stylesheet work either way.

```
text-first   36 files, 1.1 MB
with audio  269 files, ~63 MB
```

Switch to audio — for example once the release voice is recorded — with one command:

```bash
python3 course/publish_site.py --with-audio
```

## Verifying the site

`check_player.py` does two things: it drives the player's behaviour, and it **measures the rendered
frame** rather than trusting the stylesheet. The second part exists because a design port can look
right in source and still render wrong — and it caught exactly that during this work (the `@font-face`
URL was copied from ai_qe's `/assets/css/` layout while our CSS sits in `/assets/`, so the font 404'd
and silently fell back).

The probe loads the deck in a same-origin iframe at a fixed 1600x1000 viewport, then asserts geometry
and interaction:

```
$ python3 learner-site/check_player.py --deck m06 --measure
{
  "slideWidth": 1228, "slideHeight": 691, "ratio": 1.778, "aspectRatio": "16 / 9",
  "overflowing": false,
  "fontLoaded": true, "fontsStatus": "loaded",
  "kicker": "AI Product Studio · Module 6 of 9",
  "title": "The Expertise Product: Evidence, Routing, Editions",
  "footer": "AI Product Studio / M6 · The Expertise Product / Slide transcript / 01 / 28",
  "panelHeight": "124px", "panelTop": 812, "panelBottom": 936, "navTop": 948, "viewportHeight": 1000,
  "coverSlide": true, "chapters": 4, "optgroups": 4, "titleIds": 28, "footerLinks": 28,
  "presentMode": true, "readingMode": true, "slidesVisibleWhileReading": 28,
  "backToOneSlide": 1, "drawerOpen": true, "drawerHasNotes": true, "drawerClosed": true
}
```

This is not ceremony. It has caught four bugs that all rendered wrong while looking right in source:

| Bug | What the measurement showed |
|---|---|
| `@font-face` URL | copied from ai_qe's `/assets/css/` layout while our CSS sits in `/assets/`, so the font 404'd and silently fell back to a system sans |
| **Read all** | switched the class but left every other slide `hidden` — 1 slide visible when 28 should be |
| Narration panel | pushed to 897..1021 in a 900px viewport: the controls were **off-screen**, because `--frame-width` is declared on `:root` and a `var()` inside a custom property is substituted where that property is declared, so setting `--narration-height` on `<body>` never reached the frame maths |
| Chrome budget | the honesty badge adds ~49px that a hardcoded `112px` constant did not know about, so the panel ran under the navigation strip |

The fourth is why `--chrome-height` is measured by the player rather than assumed.

So every deck is checked for: the frame really is 16:9 and does not overflow, the typeface actually
loaded, the kicker/title/footer exist on the current slide, **the narration panel is inside the
viewport and clear of the navigation strip**, every slide has an anchored title and a transcript link,
the picker is chapter-grouped, and Present / Read all / Sources & notes all change state correctly.


```bash
python3 course/learner-site/check_player.py        # headless Chrome, no npm install
python3 course/learner-site/build_site.py --check  # build into a temp dir
python3 course/06-production/verify.py             # the whole course gate, incl. narration
```

`check_player.py` drives a browser already on the machine (Chrome or Chromium) and asserts that the
panel was injected, exactly one slide is `aria-current`, the status region names the right slide, the
CC control became enabled (which can only happen after the `.vtt` fetched *and* parsed), a cue is
rendered, and a deep link (`#slide-5`) navigates correctly. It exits 2 with a clear message if no
browser is installed, so it can never become an unverifiable dependency.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Page is text-only, player says narration is unavailable | `narration.json` was not built or the manifest is empty — run `make site` after generating narration. |
| "Captions could not load" | The `.vtt` is missing or invalid. Run `python3 course/06-production/narration/validate_narration.py`. |
| A visible "preview narration" badge | The recordings are the free local voice. Record the release voice (`make narration`) to replace it. |
| Audio works from the server but not from `file://` | Browsers block `fetch` for local files. Use `make serve`. |
| Two tabs fight over playback | Should not happen — `narration-media.js` coordinates them. If it does, note the reproduction; that is a bug worth fixing. |
