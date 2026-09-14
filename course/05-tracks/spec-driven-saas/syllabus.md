# Syllabus — Spec-Driven AI SaaS (6 Weeks)

> Self-paced track bundle from AI Product Studio (APS-3). Four modules (M0, M1, M4, M5) plus a monetization/launch slice from M7/M8. All source files: `course/03-content/`. Assessment model follows `course/01-design/content-standards.md` §2.7 — labs 60% / quizzes 20% / capstone 20%.

**Bundle outcome.** By the end of week 6 you have shipped the *governance and evidence* half of a multi-tenant SaaS: a spec folder a stranger can implement from, tenant-isolation and authorization tests whose red runs you recorded, a playbook manifest whose validator you have watched fail, and a sourced pricing rationale plus sales page for your product.

**Case study.** SignUpFlow — FastAPI + SQLAlchemy 2.0, multi-tenant, 17 spec folders, 7 test tiers, no-CI local validation policy (`SignUpFlow/AGENTS.md`, "Repository purpose"; `SignUpFlow/docs/TESTING.md`; `.specify/memory/constitution.md`, "Current Validation Policy (2026-09-13)").

**Weekly load:** one module per week for weeks 1–5; week 6 is the launch slice and the bundle capstone. Budget 3–5 hours per week; weeks 3–5 carry the labs.

---

## Week 1 — Orientation and first win

| Field | Detail |
|---|---|
| **Weekly outcome** | You have run real production software and a real scheduler end to end, you can name the six stages of the Spec-to-Ship Loop with one openable artifact per stage, and you have started the evidence log every later week depends on. |
| **Modules / segments** | M0 in full: M0.1 Why three types, and why these · M0.2 The method — the Spec-to-Ship Loop · M0.3 Set up and get your first win |
| **Read** | `course/03-content/m00-orientation/lesson.md` |
| **Lab** | Lab M0 — Environment Setup & First Ship-Win (`course/03-content/m00-orientation/lab.md`) |
| **Quiz** | Quiz M0 — 8 questions on archetypes, proof assets, loop stages (`course/03-content/m00-orientation/quiz.md`) |
| **Time budget** | ≈1.5 h: 30 min lesson + 20–40 min lab (mostly downloads) + 15 min quiz |
| **Assessment** | **Lab M0 (pass/fail):** three repos cloned; `python3 --version` shows 3.11+; `ollama list` shows ≥1 model; solver ran and the health-score line is captured; first-win post up. **Quiz M0:** 8/8 auto-graded, key in the quiz file. |

The first win matters more than it looks: the research dataset behind this course loses 40–50% of students at the "Module 2 Chasm," days 3–7, when the first hard concept lands (`course/00-research/02-course-market-research.md` §B). Week 1 exists to get you past that chasm with a running solver before it arrives.

---

## Week 2 — The AI product operating system

| Field | Detail |
|---|---|
| **Weekly outcome** | You own a starter repo with a constitution, an `AGENTS.md` of verifiable rules, spec templates, and a research log — and you have completed one full spec → plan → TDD loop with a recorded red run and a recorded green run. |
| **Modules / segments** | M1 in full: M1.1 Govern agents with a constitution and rule files · M1.2 Spec → plan → tasks an agent can execute · M1.3 Evidence discipline — validation as a record, not a feeling |
| **Read** | `course/03-content/m01-operating-system/lesson.md` |
| **Lab** | Lab M1 — Build Your Operating System, Then Run One Loop (`course/03-content/m01-operating-system/lab.md`) |
| **Quiz** | Quiz M1 — 8 questions on rule verifiability, hierarchy precedence, spec artifact purposes, evidence format (`course/03-content/m01-operating-system/quiz.md`) |
| **Time budget** | ≈3.25 h: 60 min lesson + ≈2 h lab + 15 min quiz |
| **Assessment** | **Lab M1 (pass/fail):** `constitution.md` ≤80 lines with ≥3 principles and an autonomy config; `AGENTS.md` ≤200 lines with every rule imperative and verifiable; two stories with Given/When/Then; a Constitution Check gate explicitly passed; ≥5 tasks each citing an exact file path, tests first; the failing (red) pytest output recorded before implementation and a green run after; one evidence entry with commands, counts, date, environment, limitations, and head SHA. **Quiz M1:** 8 questions. |

Models to copy while you work: SignUpFlow's 79-line constitution and 177-line `AGENTS.md` (`SignUpFlow/.specify/memory/constitution.md`; `SignUpFlow/AGENTS.md`), and the house-style contrast that makes rules checkable — "Filter every query by `org_id`." not "Be careful with multi-tenancy." (`SignUpFlow/AGENTS.md`, "House style").

---

## Week 3 — From idea to executable spec

| Field | Detail |
|---|---|
| **Weekly outcome** | You have produced a complete spec-kit folder for one real feature of your own SaaS, run the drift checks on your own generated files, and watched a fresh agent session (or a peer) attempt story 1 from `tasks.md` alone. |
| **Modules / segments** | M4 in full: M4.1 The artifact pipeline in full · M4.2 Spec quality — what makes an agent-executable spec · M4.3 From tasks to PR — the honest change record |
| **Read** | `course/03-content/m04-spec-driven-saas/lesson.md` |
| **Lab** | Lab M4 — Spec a Real Feature, Stranger-Testable (`course/03-content/m04-spec-driven-saas/lab.md`) |
| **Quiz** | Quiz M4 — 8 questions on artifact responsibilities, checklist gate rules, task format, research decision format (`course/03-content/m04-spec-driven-saas/quiz.md`) |
| **Time budget** | ≈4 h: 75 min lesson + 90–120 min lab + 15 min quiz, plus reading the case-study folder |
| **Assessment** | **Lab M4 (pass/fail):** ≥3 independently testable stories with numeric Given/When/Then; ≥8 FRs; no `[NEEDS CLARIFICATION]` remaining; ≥3 research decisions each with a rejected alternative; a Constitution Check verdict per principle; ≥1 contract with shapes, error keys, and a test sketch; tasks in `[ID] [P?] [US#]` form citing exact file paths, tests first; checklists passed *and* drift checks run (every cited path grepped, every count recounted). **Pass gate:** the stranger test — story 1 implemented or attempted with zero questions the folder should have answered. **Quiz M4:** 8 questions. |

The exemplar folder is `SignUpFlow/specs/014-security-hardening/`: 8 stories, 44 FRs, 7 edge cases, 12 success criteria, 6 contracts totaling roughly 4,661 lines, and **no `tasks.md`**. Your drift checks target exactly the three failures this repo exhibits: the stale `/specs/020-user-onboarding/` path in `specs/000-user-onboarding/tasks.md`, the "5xP1" line printed beside six P1 stories in `specs/014-security-hardening/checklists/requirements.md`, and the `migrations/versions/` path cited where the repo has only `alembic/versions/`.

---

## Week 4 — Tenancy and the permission/qualification split

| Field | Detail |
|---|---|
| **Weekly outcome** | Your app denies cross-tenant reads and writes with real-JWT tests, proves a denied write leaves the database unchanged, and proves a scheduling qualification confers no admin authority. |
| **Modules / segments** | M5.1 Multi-tenancy as a P0 cultural rule · M5.2 RBAC done right — permissions ≠ qualifications |
| **Read** | `course/03-content/m05-security-tests/lesson.md` (segments M5.1–M5.2) |
| **Lab** | Lab M5 steps 1–2 (`course/03-content/m05-security-tests/lab.md`) |
| **Quiz** | — (Quiz M5 is taken in week 5, after the module is complete) |
| **Time budget** | ≈2.5 h: 50 min lesson + ≈1.5 h lab (steps 1–2 are ~45 min each for a small app) |
| **Assessment** | **Lab M5 partial checkpoint (feeds the Lab M5 grade):** same-tenant member reads own rows OK; foreign-tenant member gets 403 when naming a foreign org and 404 for a guessed id inside their own tenant; the forbidden-write test snapshots the target row, asserts the denial status, re-reads, and asserts the row is identical; a person with roles `["volunteer", "usher"]` receives 403 from the invite endpoint. |

The rule you are implementing is a P0 culture rule, not a wiki page: "Every database query MUST filter by `org_id`." … "A missing `org_id` filter is a cross-tenant data leak. Treat it as a P0 bug." (`SignUpFlow/AGENTS.md`, "Multi-tenancy and auth (project-critical)"). The mechanisms are in `SignUpFlow/api/dependencies.py` (`verify_org_member`, the three-way `Person` filter in `get_current_user`, `get_person_in_actor_org`) and the permission split is enforced in `SignUpFlow/api/roles.py`.

---

## Week 5 — Acceptance: tiers, playbooks, and an honest manifest

| Field | Detail |
|---|---|
| **Weekly outcome** | You have an executable authorization matrix that fails on a deliberately miswired route, and a playbook fixture whose manifest validator refuses to run when a required scenario is removed. Both red runs are recorded. |
| **Modules / segments** | M5.3 Acceptance — seven tiers, playbooks, and an honest manifest |
| **Read** | `course/03-content/m05-security-tests/lesson.md` (segment M5.3) |
| **Lab** | Lab M5 steps 3–4 + full acceptance checklist (`course/03-content/m05-security-tests/lab.md`) |
| **Quiz** | Quiz M5 — 8 questions on the P0 rule, permission/qualification separation, status-code semantics, playbook oracle properties, manifest honesty (`course/03-content/m05-security-tests/quiz.md`) |
| **Time budget** | ≈3 h: 25 min segment + ≈2 h lab (steps 3–4 are ~45 min each) + 15 min quiz |
| **Assessment** | **Lab M5 complete (pass/fail):** route policy table classifies every mounted route; the drift test caught the induced miswire and both red and green runs are recorded; the playbook fixture and manifest validate green; removing a required scenario id fails the validator and both runs are recorded; manifest statuses are honest — no `automated` row without a test id, `manual`/`blocked` rows carry the manual tier. Evidence in the M1 format with both induced failures pasted. **Quiz M5:** 8 questions. |

The tier vocabulary and the manifest honesty rules come from the repo: seven tiers each proving a different property (`SignUpFlow/docs/TESTING.md`), the four statuses `automated` / `partial` / `manual` / `blocked` with their tier coupling (`SignUpFlow/tests/playbooks/coverage.py`), and validation that runs before collection so a removed scenario kills the run (`SignUpFlow/tests/playbooks/plugin.py`). The dated full-suite line you are imitating is "1,464 passed, 21 skipped" (`SignUpFlow/docs/playbooks/validation.md`).

---

## Week 6 — Price it, package it, write the page

| Field | Detail |
|---|---|
| **Weekly outcome** | Your SaaS has a pricing model with a stated reason, a positioning one-liner every clause of which is falsifiable against a sourced comparator table, a sales page in the 8-section anatomy, and a 5-email launch arc. |
| **Modules / segments** | Monetization slice: M7.1 Pricing the three archetypes (Type 2 rows — per-seat tiers, gated paths, invitation growth) · M7.2 Packaging and platforms · M7.3 Honest marketing that converts · M8.1 The sales page · M8.2 The launch arc |
| **Read** | `course/03-content/m07-monetize/lesson.md`; `course/03-content/m08-launch-capstone/lesson.md` (segments M8.1–M8.2 only) |
| **Worked examples** | `course/04-sales/pricing-and-platforms.md` (the decision record); `course/04-sales/landing-page.md` (the 8-section page, including how it handled having no testimonials) |
| **Lab** | Bundle capstone worksheet — see `syllabus` assessment below; no Lab M7 and no Lab M8 (both excluded, see `bundle-map.md`) |
| **Quiz** | — (Quiz M7 and Quiz M8 are not in this bundle) |
| **Time budget** | ≈4 h: 110 min across the M7/M8 segments + ≈2 h capstone worksheet |
| **Assessment** | **Bundle capstone (20%):** four artifacts — (1) a pricing rationale with a 5-competitor table where every price carries a source; (2) a positioning one-liner in the adjective-wedge × differentiators × audience form; (3) a sales page in the 8-section anatomy, length set from the price (`course/00-research/02-course-market-research.md` §E: 800–1,200 words under $200); (4) a 7-email arc with warmup strictly separated from conversion and a real deadline. Honest placeholders are required where no testimonial exists. |

The pricing lesson applied to your own product is SignUpFlow's feature-gating pattern: billing and SMS routes stay in the codebase but return 404 by default behind `BILLING_ENABLED=false` / `SMS_ENABLED=false`, and "core scheduling must not require either paid integration" (`SignUpFlow/README.md`, "Provider-backed Features"; `SignUpFlow/AGENTS.md`). Monetize after the workflow is trustworthy; gate what is not proven; never gate the core.

---

## Assessment summary

| Component | Weight | What is graded | Where the criteria live |
|---|---|---|---|
| **Labs** | 60% | Lab M0, Lab M1, Lab M4, Lab M5 — each pass/fail against its own acceptance checklist, with the M5 red-run demonstrations required | `course/03-content/m0*/lab.md`, `m05-security-tests/lab.md` |
| **Quizzes** | 20% | Quiz M0, M1, M4, M5 — 8 auto-graded questions each, 32 total, keys included | `course/03-content/m0*/quiz.md` |
| **Capstone** | 20% | The week-6 launch package (pricing rationale, positioning one-liner, sales page, email arc) | This syllabus, week 6 |

This is the full course's 60/20/20 model (`course/01-design/content-standards.md` §2.7) with one bundle-specific substitution: the full course's capstone is a shipped product with a recorded demo (Lab M8); this bundle's capstone is the launch package for your SaaS, and there is no demo requirement because M8.3 is out of scope.

**Evidence rule for every lab.** Record commands, counts, date, environment, revision (head SHA), and limitations — including at least one thing you did not verify. The format is fixed in `course/03-content/m01-operating-system/lesson.md` (M1.3) and modeled on `SignUpFlow/docs/playbooks/validation.md`, which records its own failures (a browser click race; a mypy line reading "835 errors in 40 files; not a pass") and states what its runs do not prove.
