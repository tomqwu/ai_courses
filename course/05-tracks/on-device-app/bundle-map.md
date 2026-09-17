# Bundle Map — On-Device AI Apps (Track 1)

> Exactly what you get, module by module, and exactly what you don't.
> **Scope:** 4 of 9 modules in full (M0–M3), plus a monetization-and-launch slice of M7/M8. **17 of 27 teaching segments · 4 of 8 full labs · 5 of 9 quizzes (40 of 72 questions).**
> "Included" means the artifact as it exists in the parent course — nothing is rewritten, reordered, or watered down. The M7/M8 slice is scoped, not summarized.

## The map

| Module | Segments used | Labs used | Artifacts included | Artifacts excluded / not in this track |
|---|---|---|---|---|
| **M0 — Orientation: Three Products, One Method** | M0.1 Why three types, and why these · M0.2 The method: the Spec-to-Ship Loop · M0.3 Set up and get your first win | **Lab M0** (full): environment setup + first ship-win, including the SignUpFlow solver run (TinyCopilot suite smoke run as stretch) | `lesson.md`, `lab.md`, `quiz.md`, `slides.md`, `solutions.md`, `video-scripts.md`, `handout.md`, `facilitation.md` — all in `course/03-content/m00-orientation/` | `glossary.md`, `lab-rubrics.md`, `accessibility.md` — not yet produced course-wide |
| **M1 — The AI Product Operating System** | M1.1 Govern agents with a constitution and rule files · M1.2 Spec → plan → tasks an agent can execute · M1.3 Evidence discipline: validation as a record, not a feeling | **Lab M1** (full): build your own constitution, `AGENTS.md`, spec templates, and run one spec → plan → TDD mini-loop | `lesson.md`, `lab.md`, `quiz.md`, `slides.md`, `solutions.md`, `video-scripts.md`, `handout.md`, `facilitation.md` — all in `course/03-content/m01-operating-system/` | `glossary.md`, `lab-rubrics.md`, `accessibility.md` — not yet produced course-wide |
| **M2 — The On-Device AI App: Architecture** | M2.1 The capture→transcribe→context→prompt→route pipeline · M2.2 Per-role model routing and prompt builders · M2.3 Proactive intelligence without magic | **Lab M2** (full, steps 1–9): delete and re-implement six modules TDD-style, then pass the gate | `lesson.md`, `lab.md`, `quiz.md` (in `course/03-content/m02-ondevice-app/`) **plus the entire runnable `tinycopilot/` reference repo**: `src/tinycopilot/*.py`, `tests/` (191-test suite incl. `test_contract_real_llm.py`), `Makefile`, `demo.py`, `README.md`, `pyproject.toml` | `slides.md`, `solutions.md`, `video-scripts.md`, `handout.md`, `facilitation.md`, `glossary.md`, `lab-rubrics.md`, `accessibility.md` — not yet produced course-wide |
| **M3 — The On-Device AI App: Privacy, Testing, Shipping** | M3.1 Privacy is a mode, not a slogan · M3.2 Testing: floors, contracts, and what CI can't do · M3.3 Ship it: release discipline and competitive positioning | **Lab M3** (full, steps 1–4): privacy hardening TDD, real-LLM contract test, coverage floor, sourced comparison table + positioning one-liner | `lesson.md`, `lab.md`, `quiz.md`, `slides.md` — all in `course/03-content/m03-privacy-ship/` | `solutions.md`, `video-scripts.md`, `handout.md`, `facilitation.md`, `glossary.md`, `lab-rubrics.md`, `accessibility.md` — not yet produced course-wide |
| **M7 — Monetize: Pricing, Packaging, Positioning** | M7.1 Pricing the three archetypes · M7.2 Packaging and platforms · M7.3 Honest marketing that converts | **Lab M7, steps 1–5** only, run against your Type-1 app from Lab M2/M3: Step 1 re-sources the comparison table from your Lab M3 `docs/competition.md`; Steps 2–5 produce the pricing worksheet, one-liner, packaging page, and skeptical-engineer self-review | `lesson.md` (all three segments), `quiz.md` (Quiz M7), `lab.md` steps 1–5 in `course/03-content/m07-monetize/` | Lab M7 prerequisites (Labs M4/M6) and stretch goals; `slides.md`, `solutions.md`, `video-scripts.md`, `handout.md`, `facilitation.md`, `glossary.md`, `lab-rubrics.md`, `accessibility.md` — not yet produced course-wide |
| **M8 — Launch: Sales Page, Email Arc, Capstone** | M8.1 The sales page · M8.2 The launch arc | **No full Lab M8.** The M8.1/M8.2 deliverables only: an 8-section sales page (length set by your Lab M7 price) and a 5-email launch mini-arc; plus the 5-minute demo in the four-beat structure | `lesson.md` segments M8.1–M8.2 in `course/03-content/m08-launch-capstone/` | **M8.3 Capstone: ship and demo** and the entire scored Lab M8 — the capstone contract, the five-dimension rubric, self/peer/instructor scoring, and demo day (`course/03-content/m08-launch-capstone/lab.md`); **Quiz M8**; all other M8 artifacts (not yet produced course-wide) |

## Not in this track at all

| Excluded | Why | Where it lives if you want it |
|---|---|---|
| **M4 — Spec-Driven SaaS: From Idea to Executable Spec** (M4.1–M4.3, Lab M4, Quiz M4) | Track 2 material | `course/03-content/m04-spec-driven-saas/`, full course $399 |
| **M5 — Spec-Driven SaaS: Multi-Tenant Security & Acceptance** (M5.1–M5.3, Lab M5, Quiz M5) | Track 2 material | `course/03-content/m05-security-tests/`, full course $399 |
| **M6 — The Expertise Product** (M6.1–M6.3, Lab M6, Quiz M6) | Track 3 material | `course/03-content/m06-expertise-product/`, full course $399 |
| **M8.3 Capstone + Lab M8 + Quiz M8** | This track closes with a tagged repo and a recorded demo, not the five-dimension scored capstone | `course/03-content/m08-launch-capstone/`, full course $399 |
| **Cohort-only items** | Live workshops, instructor code review on three labs, capstone review, demo day, cohort channel | Studio Live, $1,490 (`course/04-sales/pricing-and-platforms.md`) |
| **Track-level files written for this bundle** | These are the bundle's own five files, not parent-course artifacts | `README.md`, `syllabus.md`, `sales-page.md`, `pricing.md`, `bundle-map.md` in `course/05-tracks/on-device-app/` |

## What you can run before you decide

The lab is public in this workspace. Verify the gate yourself:

```bash
cd course/03-content/m02-ondevice-app/tinycopilot
make lab-m2    # → 191 passed, coverage 100% (floor 90 enforced)
make lab-m3    # → 49 passed
make e2e       # → 2 passed against a live Ollama daemon
```

Verified status is recorded in `course/03-content/m02-ondevice-app/tinycopilot/README.md`. Two environments are valid: a daemon with a local model (accepted by local-only mode) and a daemon with only `:cloud` aliases (rejected by design) — `course/03-content/m03-privacy-ship/lab.md`.

## Case-study coverage in this track

| Case study | How this track uses it | Proof asset available in the workspace |
|---|---|---|
| **ListenToMe** (Type 1, Swift/macOS) | Full read-through and pointer-level study across M2 and M3; the Python lab mirrors `ListenToMeCore` module for module; a Mac-only stretch track maps each Python module to its Swift counterpart | 96% core coverage (`ListenToMe/README.md`); 95% script-enforced floor (`ListenToMe/scripts/check-coverage.sh`); 14-row competitor table (`ListenToMe/docs/competition-analysis.md`); the "do not promote" review at 97.24% coverage (`ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md`) |
| **SignUpFlow** (Type 2, FastAPI) | M0 orientation (three archetypes, one solver run) and M1, where it is the operating-system case study: constitution, `AGENTS.md`, spec pipeline, evidence discipline | "1,464 passed, 21 skipped" dated evidence (`SignUpFlow/docs/playbooks/validation.md`); 7 test tiers (`SignUpFlow/docs/TESTING.md`); 17 spec folders |
| **AI × QE** (Type 3, content) | M0 orientation only — named as the third archetype, no lab in this track | 116 narrated slides = 21+33+26+36 (`ai_qe/_data/briefing_room.json`); published 14-finding self-audit (`ai_qe/research/reviews/site-audit-2026-09-06.md`) |

## Counts, stated plainly

| | This track | Full course |
|---|---|---|
| Modules | 4 of 9 in full + 2 partial (M7, M8) | 9 of 9 |
| Teaching segments | 17 of 27 | 27 of 27 |
| Full labs | 4 (M0–M3), plus Lab M7 steps 1–5 | 8 |
| Quizzes / questions | 5 quizzes / 40 questions with keys | 9 quizzes / 72 questions |
| Case-study archetypes | 1 (on-device app) | 3 |
| Capstone | A tagged repo + recorded demo (Lab M7/M8.1/M8.2 deliverables) | Scored capstone, five-dimension rubric, demo day |
