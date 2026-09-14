# Bundle Map — Expertise as a Product

> Exactly what you get. Modules, segments, labs, and artifacts are named by their real identifiers (`M#`, `M#.#`, `Lab M#`, `Quiz M#`) so every row cross-references the full course unambiguously. Source paths are relative to this workspace.

## 1. Module → segments → labs → artifacts

| Module | Segments used | Labs used | Quiz | Module artifacts included | Module artifacts excluded |
|---|---|---|---|---|---|
| **M0 — Orientation: Three Products, One Method** | M0.1 Why three types, and why these · M0.2 The method: the Spec-to-Ship Loop · M0.3 Set up and get your first win | **Lab M0** (environment setup & first ship-win) | Quiz M0 (8 Q) | `lesson.md`, `lab.md`, `quiz.md` | `slides.md`, `solutions.md`, `video-scripts.md`, `handout.md`, `facilitation.md`, `glossary.md`, `lab-rubrics.md`, `accessibility.md` |
| **M1 — The AI Product Operating System** | M1.1 Govern agents with a constitution and rule files · M1.2 Spec → plan → tasks an agent can execute · M1.3 Evidence discipline: validation as a record, not a feeling | **Lab M1** (build your operating system + one full loop) | Quiz M1 (8 Q) | `lesson.md`, `lab.md`, `quiz.md` | `slides.md`, `solutions.md`, `video-scripts.md`, `handout.md`, `facilitation.md`, `glossary.md`, `lab-rubrics.md`, `accessibility.md` |
| **M6 — The Expertise Product: Evidence, Routing, Editions** | M6.1 Credibility is the product · M6.2 One research base, many audiences · M6.3 Content as code | **Lab M6** (mini-briefing: research log, provenance table, 12 slides, two routes, edition record) | Quiz M6 (8 Q) | `lesson.md`, `lab.md`, `quiz.md`, `evidence-dataset.md` | `slides.md`, `solutions.md`, `video-scripts.md`, `handout.md`, `facilitation.md`, `glossary.md`, `lab-rubrics.md`, `accessibility.md` |
| **M7 — Monetize: Pricing, Packaging, Positioning** *(slice)* | M7.1 Pricing the three archetypes — **Type 3 funnel read in full; Type 1/Type 2 rows as reference only** · M7.2 Packaging and platforms · M7.3 Honest marketing that converts | **Lab M7 (adapted)** — Type 3 offer only: sourcing the table, worksheet, one-liner, packaging page | Quiz M7 (8 Q) | `lesson.md`, `lab.md` (adapted per `syllabus.md`, week 5), `quiz.md` | The Lab M7 Type 1/Type 2 product paths; `slides.md`, `solutions.md`, `video-scripts.md`, `handout.md`, `facilitation.md`, `glossary.md`, `lab-rubrics.md`, `accessibility.md` |
| **M8 — Launch: Sales Page, Email Arc, Capstone** *(slice)* | M8.1 The sales page · M8.2 The launch arc · M8.3 Capstone — **Type 3 row only** ("The M6 briefing expanded to 20 slides") | **Lab M8 (Type 3 row)** — 20-slide briefing, reconciled provenance, questionnaire draft, deployed link, 5-email mini-arc, 5-minute demo | Quiz M8 (8 Q) | `lesson.md`, `lab.md` (Type 3 row; other rows excluded), `quiz.md` | The Lab M8 Type 1 and Type 2 rows; Type 1/Type 2 discipline artifacts; `slides.md`, `solutions.md`, `video-scripts.md`, `handout.md`, `facilitation.md`, `glossary.md`, `lab-rubrics.md`, `accessibility.md` |

## 2. Modules and labs deliberately not included

| Excluded | Why |
|---|---|
| **M2 — The On-Device AI App: Architecture** (M2.1–M2.3, Lab M2, Quiz M2) | Archetype 1. Not needed to build an expertise product; belongs to the $399 full course. |
| **M3 — The On-Device AI App: Privacy, Testing, Shipping** (M3.1–M3.3, Lab M3, Quiz M3) | Archetype 1. The coverage/contract-test discipline is cited as reference in M1.3, not taught here. |
| **M4 — The Spec-Driven SaaS: From Idea to Executable Spec** (M4.1–M4.3, Lab M4, Quiz M4) | Archetype 2. M1.2 teaches the spec-kit artifact set at method level; the full SaaS workflow is not in this bundle. |
| **M5 — The Spec-Driven SaaS: Multi-Tenant Security & Acceptance** (M5.1–M5.3, Lab M5, Quiz M5) | Archetype 2. |
| **M8.3 Type 1 / Type 2 capstone rows** | The capstone is scoped to one archetype by contract ("ONE archetype, ONE shippable scope, the complete loop", `course/03-content/m08-launch-capstone/lab.md`). This bundle uses the Type 3 row. |

## 3. Bundle-level artifacts included

| Artifact | File |
|---|---|
| Bundle overview, promise, audience, 6-week map, FAQ | `course/05-tracks/expertise-product/README.md` |
| Six-week schedule with outcomes, labs, quizzes, time budgets, assessment | `course/05-tracks/expertise-product/syllabus.md` |
| 8-section sales page (sub-$200 length band) | `course/05-tracks/expertise-product/sales-page.md` |
| Bundle price + rationale + anti-cannibalization rules | `course/05-tracks/expertise-product/pricing.md` |
| This map | `course/05-tracks/expertise-product/bundle-map.md` |
| Starter evidence dataset (6 real claims, 4 claim levels, slide-wording rules) | `course/03-content/m06-expertise-product/evidence-dataset.md` |
| Evidence-record template (commands, counts, date, environment, limitations, head SHA) | `course/03-content/m01-operating-system/lesson.md`, M1.3 |

## 4. Case-study files you will open (all Type 3 / ai_qe)

| File | What it proves in the bundle |
|---|---|
| `ai_qe/_data/briefing_room.json` | 116 slides = 21 + 33 + 26 + 36 across four decks |
| `ai_qe/_data/briefing_routes.json` | Guided routes over stable slide IDs; focused routes close on a decision |
| `ai_qe/docs/principles.md` | The four claim levels and the "never mix them" rule |
| `ai_qe/docs/evidence/benchmarks.md` | Benchmark records carrying date, sample, method, unit, sponsor, and "Supports" limit |
| `ai_qe/docs/research-log.md` | Dated Question / Checked / Outcome / Changed entries and the "Not verified" list |
| `ai_qe/research/document-manifest.json` | SHA-256 retrieval provenance, including an honestly logged failed retrieval |
| `ai_qe/research/reviews/site-audit-2026-09-06.md` | The published 14-finding self-audit |
| `ai_qe/research/reviews/remediation-2026-09-06.md` | Finding → response → verification table |
| `ai_qe/_data/release.yml` | Site vs slide vs questionnaire vs research editions |
| `ai_qe/releases.md` | Changelogs that record what was deliberately retained; immutable superseded editions |
| `ai_qe/docs/economics/slide-language.md` | Slide wording rules; "fund Phases 0 and 1, not transform QA" |
| `ai_qe/docs/method/discovery-questionnaire.md` | Role-routed questionnaire + post-mortem of the 29-question/186-option predecessor that lacked the financial-capture set |
| `ai_qe/docs/method/phased-pilot.md` | Five phases, sponsor-signed go/no-go gates, frozen acceptance criteria |
| `ai_qe/_data/pilot_gates.json` | 15% go / 10% review bands, 3-week baseline, 8-week pilot, ≥30 tasks per arm, ≤4-week extension |
| `ai_qe/_data/engagement.json` | Engagement stages, including "No client price or start date has been agreed." |
| `ai_qe/CONTRIBUTING.md` | Research conventions, release validation, the narration-hash review gate |
| `ai_qe/Makefile` + `ai_qe/tools/qa-groups.json` | `make check` and the five browser QA groups across two engines and three viewports |
| `ai_qe/docs/method/executive-presentation.md` | The workshop script that presents questionnaire results as questions, not conclusions |

## 5. Honest scope statement

This map is the whole bundle. If a module, segment, lab, or artifact is not listed as included above, you do not get it here. The full course, *AI Product Studio* at $399, contains all nine modules and all eight labs; it is the recommended path and the better value (`pricing.md`). The ai_qe funnel stages taught in M6.1–M6.3 and M7.1 are planned and recorded stages, not delivered client results (`ai_qe/README.md`, `ai_qe/_data/engagement.json`).
