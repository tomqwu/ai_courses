# AI Product Studio — Course Package

**A complete, market-ready online course: "AI Product Studio: Build, Ship & Sell 3 Types of AI Products"**

Built from a deep study of three production open-source repositories by the same engineer — each a different archetype of AI product:

| Archetype | Case-study repo (cloned here) | Proof assets |
|---|---|---|
| 1. Native on-device AI app | `../ListenToMe/` — macOS/iOS meeting copilot | 96% core coverage · notarized releases · 13-competitor analysis |
| 2. Spec-driven AI SaaS | `../SignUpFlow/` — volunteer-scheduling platform | 1,464 dated tests · 7 tiers · 17 spec folders |
| 3. Expertise content product | `../ai_qe/` — "AI × QE" briefing site | 116 cited slides · provenance · published self-audit |

## What's in this package

```
course/
├── README.md                       ← you are here (package map)
│   (repository front door: ../README.md)
├── Makefile                        ← narration · transcripts · site · serve · test · check
├── check.sh                        ← the gate, runnable without make (macOS make needs the Xcode licence accepted)
├── publish_site.py                 ← builds the site and pushes it to the gh-pages branch
├── 00-research/                    ← the deep research behind the course
│   ├── 00-synthesis.md            ← the unified method (Spec-to-Ship Loop) drawn from all 3 repos
│   ├── 01-listentome-deep-read.md ← architecture, privacy engineering, release discipline (with file pointers)
│   ├── 02-signupflow-deep-read.md ← spec-kit methodology, 7-tier testing, multi-tenant security
│   ├── 02-course-market-research.md ← how to create/sell courses: frameworks, completion stats, pricing, platforms (all cited)
│   ├── 03-ai-qe-deep-read.md      ← evidence discipline, audience routing, editions, consulting funnel
│   ├── 04-platform-review-2026.md ← the September 2026 review: verdict, findings, positioning, platform plan, roadmap
│   ├── 05-platform-build-options-2026.md ← build vs buy: LMSes, merchants of record, reference architectures, labs, video
│   ├── 06-competitive-landscape-2026.md  ← 28 competitors, price bands, gaps, demand signals, threats
│   ├── 07-course-design-practice-2026.md ← what changed in learning science and cohort economics since 02-
│   ├── 08-domain-currency-2026.md ← is each archetype's curriculum current (Apple FM, spec-kit 1.0, AI search)
│   └── 09-content-audit-2026.md   ← module-by-module audit with pointers and the top-15 fixes
├── 01-design/                      ← course design (read first)
│   ├── positioning.md             ← concept, audience, promise, differentiation, pricing ladder, voice standards
│   ├── curriculum.md              ← master syllabus: 9 modules, objectives, labs, quizzes (the authoring brief)
│   ├── content-standards.md       ← BINDING spec for the 8 artifacts; every writer and reviewer follows it
│   └── assessment-and-rubrics.md  ← grading weights, quiz rules, lab standard, capstone rubric
├── 02-instructor/
│   └── instructor-guide.md         ← cohort cadence, workshop scripts (I do/We do/You do), stuck-point table, grading workflow
├── 03-content/                    ← the course itself (9 modules, 8 artifacts each)
│   ├── mNN-*/                     ← lesson.md · lab.md · quiz.md · slides.md (Marp + notes) · solutions.md
│   │                                · video-scripts.md · handout.md · facilitation.md · glossary.md
│   │                                · lab-rubrics.md · accessibility.md
│   ├── m00-orientation/           ← + lab
│   ├── m02-ondevice-app/         ← + tinycopilot/ (runnable, tested lab code)
│   ├── m06-expertise-product/    ← + evidence-dataset.md (student-facing claims data)
│   └── m08-launch-capstone/      ← the capstone lab
├── 04-sales/                       ← the course's own go-to-market
│   ├── landing-page.md           ← complete sales-page copy (~1,900 words, publish-ready)
│   ├── pricing-and-platforms.md  ← price ladder ($399 self-paced / $1,490 cohort / $2.5k team) with decision record
│   ├── launch-plan.md            ← launch timeline, 7-email arc, operations checklist, metrics
│   └── lead-product-teardown.md  ← the free lead product (3-email mini-course + 10-point checklist)
├── 05-tracks/                      ← 3 standalone sellable bundles ($199 each), one archetype apiece
│   ├── README.md                  ← bundle index and the honest case for the full course
│   └── {on-device-app,spec-driven-saas,expertise-product}/
│                                   ← README · syllabus · sales-page · pricing · bundle-map
└── 06-production/                  ← how the package is built and verified (instructor-facing)
    ├── MILESTONES.md              ← public roadmap mirroring the GitHub milestones/issues
    ├── slides/aps.css             ← shared Marp theme (`@theme aps`)
    ├── slides/build.sh · Makefile ← render/validate every deck (HTML/PDF)
    ├── slides/deck_lint.py        ← enforces bullets, per-slide notes, proof slide
    ├── verify.py                  ← artifacts, bands, rubrics, bundles, 900+ pointers
    ├── check_facts.py · facts.json ← re-derives the pinned case-study numbers from the clones; reports drift
    ├── build-glossary.py          ← merges the nine module glossaries
    ├── glossary-master.md         ← 137 merged terms (13 shared across modules)
    ├── certificate.md             ← completion certificate + issuance rules (SHA-bounded)
    ├── welcome-packet.md          ← onboarding emails, environment checklist, help routing
    └── narration/                 ← narrated audio + captions pipeline (scripts → TTS → align → validate)
        ├── DESIGN.md              ← what this borrows from ai_qe, and what it deliberately changes
        ├── README.md              ← operator's guide: generate, validate, swap the voice
        ├── scripts/mNN.json       ← the approved narration words for each deck
        ├── voices: elevenlabs (release) · say (free preview) · pronunciations.json
        ├── generate_narration.py · validate_narration.py · import_narration.py
        ├── captions.py · providers.py · narration_data.py
        └── test_captions.py (32) · test_providers.py (13)

└── learner-site/                   ← the learner-facing build: one slide at a time, narrated
    ├── build_site.py              ← decks + narration manifest → static site (no framework)
    ├── check_player.py            ← headless browser check: measures the rendered 16:9 frame,
    │                                 the loaded font and the Present/Read all/notes modes
    ├── transcripts/               ← committed transcripts: mNN.md × 9 + ALL.md
    └── assets/player.js · narration-media.js · player.css
```

## How to use this package

**To understand the course:** read `01-design/positioning.md`, then `01-design/curriculum.md`.

**To teach it:** start with `02-instructor/instructor-guide.md`. Each module folder carries **eight artifacts**: the lesson (readable as-is, or record each `M#.#` segment from `video-scripts.md`), the lab, the quiz, a Marp slide deck with speaker notes on every slide, lab solutions with expected output, a printable handout, a 90-minute facilitation kit, a glossary, per-lab rubrics, and accessibility/transcript notes. Render the decks with `make -C 06-production/slides html`; validate them with `make -C 06-production/slides check`.

**To learn it, narrated:** `make -C course narration-preview && make -C course serve` builds the learner site and serves it on <http://localhost:8043>. All 233 slides are narrated, captioned and keyboard-navigable; the free preview voice needs no API key, and `make -C course narration` records the release voice when `ELEVENLABS_API_KEY` is set. Every deck also has a transcript, committed under `learner-site/transcripts/` — `ALL.md` covers all nine modules in one file. See `learner-site/README.md`.
**To read it instead:** `course/learner-site/transcripts/ALL.md` — 233 slides, 21,536 words, with per-slide timings.

**To verify the package:** `python3 06-production/verify.py` checks all 72 banded module artifacts against the length bands, sums every rubric's weights, confirms the three bundles ship their five files, lints all nine decks, resolves every repo file pointer (1,048), and runs the narration contract — every caption and every published transcript must match its approved script word for word. It is the same evidence discipline the course teaches, applied to the course.

**To sell one archetype instead of all three:** `05-tracks/` holds three standalone bundles at $199 (on-device app · spec-driven SaaS · expertise) with their own syllabus, sales page, pricing, and bundle map. Each states plainly that the $399 full course is the better value.

**To sell it:** `04-sales/` is publish-ready: landing-page copy, pricing rationale grounded in 2025–26 platform benchmarks, and a full launch plan with the 7-email arc.

**To run the labs yourself:** the Module 2/3 labs use `03-content/m02-ondevice-app/tinycopilot/` — a complete, tested Python reference implementation that mirrors ListenToMe's architecture (see its README). **Verified status as shipped:** `make lab-m2` → 191 passed, 100% coverage (floor 90 enforced); `make lab-m3` → 49 passed; `make e2e` → 2 passed against a live Ollama daemon; `make demo` → three role outputs. Requirements: Python 3.11+ (TinyCopilot itself also runs on 3.10), pytest, httpx, and Ollama (`ollama pull qwen3:0.6b` for a local model).
The Module 5 lab uses `03-content/m05-security-tests/mini-flow/` — a deliberately incomplete FastAPI + SQLAlchemy + JWT multi-tenant starter mirroring SignUpFlow's auth shape (see its README for the intentional gaps). **Verified status as shipped:** `make lab-m5` → 51 passed, 23 skipped, 100% coverage (floor 90 enforced); `make pass-gate` → 11 failed, 63 passed on the starter by design, 74 passed once the four lab fixes are in; `make demo` → two `LEAK` lines. Requirements: Python 3.11+, `make setup` (no compiled dependencies, no database server).


## Course at a glance

- **9 modules · 27 lesson segments · 8 module labs (M0–M7) + the M8 capstone · 72 quiz questions (8 per module)**
- **9 Marp slide decks** (speaker notes on every slide) · **72 module artifacts** · **15 bundle artifacts**
- **3 sellable track bundles** ($199 each) — see `05-tracks/README.md`
- Formats: self-paced ($399) or 8-week cohort ($1,490) — see `04-sales/pricing-and-platforms.md`
- Core labs: Python + Ollama (macOS/Linux/Windows); Swift stretch track maps labs onto the real ListenToMe code
- Every claim in every file carries a source pointer — the course practices the evidence discipline it teaches

## Honesty notes (the standard this package holds itself to)

- All facts about the three case-study repos were read from the cloned repos in this workspace and carry file pointers; verify before publishing (repos evolve).
- Market-research claims cite their sources in `00-research/02-course-market-research.md`; stats like completion rates and price bands are industry research, not guarantees.
- Testimonials do not exist yet: the landing page reserves slots and says so. Run the founding cohort first (see `04-sales/launch-plan.md`).
- The three track bundles are **subsets**, not independent courses: they sequence this course's modules for one archetype and reuse its artifacts. Each `bundle-map.md` says exactly what is in and out, and each `pricing.md` states that the full course is the better value rather than pretending otherwise.
- **Length bands were recalibrated, not met by padding.** Six artifacts in the first production pass ran 1–26% over the original estimates; the maxima in `01-design/content-standards.md` were raised to the delivered envelope and the change is recorded there. Minima were untouched.

### Drift the verification pass caught (and fixed)

The expansion ran `06-production/verify.py` and a deck linter over every artifact, and the module
writers were told to report anything they could not verify. That process found five real errors in
**already-shipped** content — each one exactly the kind of drift M4 teaches students to hunt:

| Drift | Where | Fix |
|---|---|---|
| Field names invented for a release file | `03-content/m00-orientation/lab.md` claimed "five edition fields (site vs slide…)" | Rewritten to the real fields: `version`, `slide_edition`, `fintech_edition`, `questionnaire_edition`, `research_edition` |
| An off-by-two count presented as fact | M5 lesson said the policy's `admin` class had **80** operations | AST count gives 7/6/2/50/**78** = 143; lesson corrected and the total added |
| A pointer attributed to the wrong file | M6 lesson placed the `?for=evp` audience views in `briefings/index.md` | Corrected to `ai_qe/index.md:27,29` + `ai_qe/CONTRIBUTING.md:23` |
| An unmeasured "length check" | Landing page claimed "~2,250 words" in its own authoring note | Measured: 2,251 total / ~1,900 body; corrected in 7 places (and re-measured after the bundle edit) |
| Prose contradicting the executable spec | M2 lab said the router picks a *distinct* Listener model when ≥3 exist | The Python tests share Listener/Quick; the Swift original differs. Lab now states the divergence explicitly and points at `ModelRanking.swift:76-94` |

Two further "corrections" proposed by writers were **rejected after checking the source**: the
coverage statuses really are on `coverage.py:18` (as the lesson said), and "Missing review is not
approval" really is `AGENTS.md` PR rule 4 (as the M4 lesson said). A writer's suggested fix is a
claim like any other — it carries a pointer or it doesn't get applied.