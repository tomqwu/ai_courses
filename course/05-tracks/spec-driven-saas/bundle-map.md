# Bundle Map — Spec-Driven AI SaaS

> Exactly what you get, module by module, and exactly what you do not. Every source file below exists in the workspace under `course/03-content/`; every case-study pointer resolves under `SignUpFlow/`.

## How to read this map

- **Segments used** — the lesson segments included, using the course's own numbering (`M#.#`; `course/01-design/content-standards.md` §0.3). Segment titles are the ones in each `lesson.md`, unchanged.
- **Lab used** — the lab included, with its pass gate.
- **Artifacts included** — what ships in the bundle for that module.
- **Artifacts excluded** — what exists in the parent module package or the full course but is **not** in this bundle.

**Coverage:** 4 modules in full + 1 cross-module slice out of 9 modules; 17 of 27 lesson segments; 4 labs; 4 of 9 quizzes (32 of 72 questions). Full-course denominators per `course/01-design/positioning.md` (9 modules, 27 segments) and `course/01-design/curriculum.md` (8 questions per module, 72 total).

---

## Included modules

| Module | Segments used | Lab used (pass gate) | Artifacts included | Artifacts excluded |
|---|---|---|---|---|
| **M0 — Orientation: Three Products, One Method** | M0.1 Why three types, and why these · M0.2 The method: the Spec-to-Ship Loop · M0.3 Set up and get your first win | **Lab M0 — Environment Setup & First Ship-Win.** Pass = 3 repos cloned; Python 3.11+; `ollama list` shows ≥1 model; solver ran with health score captured; first-win post | `m00-orientation/lesson.md`, `lab.md`, `quiz.md` (8 questions + key) | `m00-orientation/slides.md` (instructor deck); M2–M3, M6 content previewed in M0.1 but not taught. **Scope note:** Lab M0 step 5 runs M2's TinyCopilot reference suite (`course/03-content/m02-ondevice-app/tinycopilot`); treat it as an optional environment smoke test in this bundle, since M2 itself is not taught |
| **M1 — The AI Product Operating System** | M1.1 Govern agents with a constitution and rule files · M1.2 Spec → plan → tasks an agent can execute · M1.3 Evidence discipline: validation as a record, not a feeling | **Lab M1 — Build Your Operating System, Then Run One Loop.** Pass = `constitution.md` ≤80 lines, `AGENTS.md` ≤200 lines with verifiable rules, 2 stories with Given/When/Then, Constitution Check gate, ≥5 path-citing tasks, red run recorded before green, evidence entry with head SHA | `m01-operating-system/lesson.md`, `lab.md`, `quiz.md` (8 questions + key); the constitution / `AGENTS.md` / spec / plan / tasks templates embedded in `lab.md` | `m01-operating-system/slides.md`, `solutions.md` (instructor artifacts) |
| **M4 — The Spec-Driven SaaS: From Idea to Executable Spec** | M4.1 The artifact pipeline in full · M4.2 Spec quality: what makes an agent-executable spec · M4.3 From tasks to PR: the honest change record | **Lab M4 — Spec a Real Feature, Stranger-Testable.** Pass = complete spec folder (≥3 stories, ≥8 FRs, ≥3 research decisions with rejections, Constitution Check, ≥1 contract, tasks with exact paths); drift checks run; **stranger test** passed — story 1 implemented or attempted with zero questions the folder should have answered | `m04-spec-driven-saas/lesson.md`, `lab.md`, `quiz.md` (8 questions + key) | `m04-spec-driven-saas/slides.md` and other production artifacts; the full course's M2–M3 lab work that precedes it |
| **M5 — The Spec-Driven SaaS: Multi-Tenant Security & Acceptance** | M5.1 Multi-tenancy as a P0 cultural rule · M5.2 RBAC done right: permissions ≠ qualifications · M5.3 Acceptance: seven tiers, playbooks, and an honest manifest | **Lab M5 — Isolate and Accept.** Pass = isolation tests green incl. foreign-org 403 / guessed-id 404; forbidden write proven to leave the row unchanged; qualification-no-admin test green; route policy classifies every route; **drift test caught a deliberate miswire (red + green recorded)**; manifest validator rejects a removed scenario (red + green recorded) | `m05-security-tests/lesson.md`, `lab.md`, `quiz.md` (8 questions + key); the `food-bank.json` fixture shape embedded in `lab.md` | `m05-security-tests/slides.md`; the two-tenant browser stretch (BO-12 pattern) and CH-drill ports are labeled stretch goals, not graded |
| **Launch slice — from M7 and M8** | M7.1 Pricing the three archetypes (Type 2 rows: per-seat tiers, feature-gating, invitation growth) · M7.2 Packaging and platforms · M7.3 Honest marketing that converts · M8.1 The sales page · M8.2 The launch arc | **No lab.** The week-6 capstone worksheet replaces Lab M7 and Lab M8: a 5-competitor price table where every price is sourced; a positioning one-liner; a sales page in the 8-section anatomy at the price-appropriate length; a 7-email arc with warmup separated from conversion and a real deadline | `m07-monetize/lesson.md` (M7.1–M7.3), `m08-launch-capstone/lesson.md` (M8.1–M8.2); worked examples `course/04-sales/landing-page.md` and `course/04-sales/pricing-and-platforms.md`; the length rule from `course/00-research/02-course-market-research.md` §E | M8.3 Capstone: ship and demo (the full 5-dimension capstone rubric, the evidence-record attachment, the 5-minute demo, demo day); Quiz M7 and Quiz M8; Lab M7 and Lab M8 |

---

## Excluded modules and elements

| Excluded | What it contains | Where it lives |
|---|---|---|
| **M2 — The On-Device AI App: Architecture** | Capture→transcribe→context→prompt→route pipeline; per-role model routing; pure prompt builders; TinyCopilot core build | `course/03-content/m02-ondevice-app/` |
| **M3 — The On-Device AI App: Privacy, Testing, Shipping** | Fail-closed local-only mode; `isVerifiedLocal` metadata check; real-LLM contract test; 95% coverage floor; notarized releases; competitive positioning | `course/03-content/m03-privacy-ship/` |
| **M6 — The Expertise Product: Evidence, Routing, Editions** | Claim provenance; one research base across audiences; editions and immutable releases; consulting-style funnel | `course/03-content/m06-expertise-product/` |
| **M8.3 — Capstone and demo day** | One archetype, one scope, the complete Spec-to-Ship Loop; 5-dimension rubric; evidence-record attachment; 5-minute demo | `course/03-content/m08-launch-capstone/lesson.md`, segment M8.3 |
| **Labs M2, M3, M6, M7, M8** | The four excluded tracks' labs plus the full-course capstone lab | `course/03-content/*/lab.md` |
| **Quizzes M2, M3, M6, M7, M8** | 40 of the course's 72 quiz questions | `course/03-content/*/quiz.md` |
| **Live cohort elements** | Weekly 90-minute "I do / We do / You do" workshops; instructor code review on 3 labs; capstone review; cohort channel | `course/04-sales/pricing-and-platforms.md`, "Packaging details" |
| **Instructor-facing production artifacts** | `slides.md`, `video-scripts.md`, `solutions.md`, `facilitation.md`, `lab-rubrics.md`, `handout.md`, `glossary.md`, `accessibility.md` | `course/01-design/content-standards.md` §1 |
| **The case-study repos themselves** | ListenToMe, SignUpFlow, AI × QE are public clones, not shipped files | `github.com/tomqwu/SignUpFlow`, `.../ListenToMe`, `.../ai_qe` |

---

## Case-study folders you will open (public repo, not bundle content)

| Folder / file | Why the bundle sends you there |
|---|---|
| `SignUpFlow/specs/014-security-hardening/` | The exemplar spec folder: 8 stories, 44 FRs, 7 edge cases, 12 success criteria, 6 contracts (~4,661 lines), and **no `tasks.md`** |
| `SignUpFlow/specs/000-user-onboarding/tasks.md` | The real task format — and drift case 1 (stale `/specs/020-user-onboarding/` path) and drift case 3 (`migrations/versions/` cited; repo has only `alembic/versions/`) |
| `SignUpFlow/specs/014-security-hardening/checklists/requirements.md` | Drift case 2: "5xP1" printed beside six P1 stories, in a self-graded file that reads "Quality Score: 100%" |
| `SignUpFlow/api/dependencies.py` | `verify_org_member`, the three-way `Person` filter in `get_current_user`, `get_person_in_actor_org` |
| `SignUpFlow/api/roles.py`, `api/route_auth_policy.py` | Permission-vs-qualification normalization; the executable authorization matrix |
| `SignUpFlow/tests/unit/test_api_route_auth_policy.py` | The drift test that fails on missing, stale, or miswired routes |
| `SignUpFlow/docs/TESTING.md`, `docs/playbooks/validation.md` | 7 test tiers; "1,464 passed, 21 skipped" (2026-09-12; demoted to historical reference 2026-09-13) |
| `SignUpFlow/docs/playbooks/coverage.json`, `docs/playbooks/church.md`, `tests/playbooks/plugin.py`, `tests/playbooks/coverage.py` | Playbook acceptance, disruption drills (CH-04), four statuses and their tier coupling, validation before collection |

---

## What the buyer receives, in one line

Four module packages' student files (lesson + lab + quiz, searchable text, keys included), one launch slice drawn from two more modules, the lab-embedded templates for a constitution, `AGENTS.md`, a spec folder, a playbook fixture and manifest, and a capstone worksheet — plus lifetime access. Nothing that runs a model; nothing that requires a Mac; no live session; no demo day; no certificate from the full course's capstone path.
