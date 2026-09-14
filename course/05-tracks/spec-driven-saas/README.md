# Spec-Driven AI SaaS — Track Bundle

> A standalone, self-paced bundle from **AI Product Studio (APS-3)**. Four modules plus a monetization/launch slice. You leave with a feature spec folder your stranger can implement from and acceptance evidence your auditor can re-run.

**Price: $199.** The full course — all three product tracks plus the capstone — is **$399** and is the recommended path for most buyers. Read `pricing.md` in this folder before you decide.

---

## The promise

Ship a multi-tenant SaaS where **the specs are complete enough for an autonomous agent to implement them** and **the acceptance evidence is something a buyer can audit**.

Two tests define the whole bundle. Everything in it exists to make you pass them:

1. **The stranger test.** Hand your spec folder to a fresh agent session — no chat history, no memory of why any decision was made — and ask for story 1 only. If it has to ask you anything the folder does not answer, the folder has a hole. The standard comes from SignUpFlow's Ralph loop: an agent told to "complete ALL acceptance criteria" cannot ask questions, so the pipeline is the precondition for autonomy, not ceremony around it (`SignUpFlow/.specify/memory/constitution.md`, Context A; `course/03-content/m04-spec-driven-saas/lesson.md`, M4.2).
2. **The auditor test.** Hand your acceptance evidence to a skeptical engineer. Every claim has a command, a count, a date, an environment, a revision, and an explicit "not verified" list. SignUpFlow records its suite as a dated line — "1,464 passed, 21 skipped" (`SignUpFlow/docs/playbooks/validation.md`) — and that same file was demoted to historical reference the next day rather than being left to age into a false claim. Evidence with a date *and a retirement plan* is the standard you are held to.

---

## The case study: SignUpFlow

You work against one production repository throughout: **SignUpFlow**, a multi-tenant volunteer-scheduling SaaS for churches and sports leagues — FastAPI + SQLAlchemy 2.0 + Pydantic 2, JWT (HS256, 24h) + bcrypt auth, a greedy heuristic solver, and a YAML-in/JSON-out CLI (`SignUpFlow/AGENTS.md`, "Repository purpose"; `SignUpFlow/README.md`).

Four things make it the right teaching repo for this bundle:

| What SignUpFlow does | Where you verify it |
|---|---|
| **17 spec folders** — each a complete specify → research → plan → checklist → contracts → tasks package | `SignUpFlow/specs/` (count them: `ls SignUpFlow/specs \| wc -l`) |
| **7 test tiers**, each run in a separate process by `make test-all` | `SignUpFlow/docs/TESTING.md` |
| **No-CI local validation policy** — all checks run locally and evidence travels with the revision; guarded by a policy-regression test | `SignUpFlow/.specify/memory/constitution.md`, "Current Validation Policy (2026-09-13)"; `SignUpFlow/tests/unit/test_local_validation_policy.py` |
| **Executable authorization matrix** — every mounted route classified, with a test that fails on missing, stale, or miswired routes | `SignUpFlow/api/route_auth_policy.py`; `SignUpFlow/tests/unit/test_api_route_auth_policy.py` |

The deepest artifact you study is `specs/014-security-hardening/`: **8 stories, 44 functional requirements, 7 edge cases, 12 success criteria, and 6 contract files totaling roughly 4,661 lines — and no `tasks.md`** (`SignUpFlow/specs/014-security-hardening/`). The missing file is part of the curriculum: you learn the real task format from `.specify/templates/tasks-template.md` and `specs/000-user-onboarding/tasks.md`, and you learn that a plan's "Next Steps" line is a promise, not a deliverable.

---

## Who this is for — and isn't

**For you if you:**
- Write code professionally (≈2+ years) and have a SaaS, a SaaS idea, or a multi-tenant feature you need to actually ship.
- Already use an AI coding agent — Claude Code, Codex, Cursor, Copilot — and suspect you are getting a fraction of its value.
- Want security and acceptance work that holds up when a customer, a co-founder, or an auditor opens the repo.

**Not for you if you:**
- Have not written code before.
- Want the on-device app track (ListenToMe / TinyCopilot) or the expertise-product track (AI × QE). Those are **not in this bundle**; they are in the full course.
- Want AI-governance compliance training.

## Prerequisites

- Python 3.11+, git, and a command line. `SignUpFlow/.specify/memory/constitution.md` and the repo's own floor set Python 3.11+ (`SignUpFlow/AGENTS.md`, "Code style").
- FastAPI + SQLAlchemy familiarity helps for Lab M5; the lab fixes the app shape (three tables — `organizations`, `people`, `events` — and JWT auth) so you are never guessing what to build (`course/03-content/m05-security-tests/lab.md`).
- No LLM, Mac, or cloud account needed. This bundle never calls a model API. You clone one public repo and work in your own.

---

## What's included

| Module | Title | Segments | Lab | Quiz |
|---|---|---|---|---|
| **M0** | Orientation: Three Products, One Method | M0.1, M0.2, M0.3 | Lab M0 — environment + first ship-win | Quiz M0 |
| **M1** | The AI Product Operating System | M1.1, M1.2, M1.3 | Lab M1 — build your operating system, run one loop | Quiz M1 |
| **M4** | The Spec-Driven SaaS: From Idea to Executable Spec | M4.1, M4.2, M4.3 | Lab M4 — spec a real feature, stranger-testable | Quiz M4 |
| **M5** | The Spec-Driven SaaS: Multi-Tenant Security & Acceptance | M5.1, M5.2, M5.3 | Lab M5 — isolate and accept | Quiz M5 |
| **Launch slice** | From M7 (pricing/packaging/honest marketing) and M8 (sales page, launch arc) | M7.1–M7.3, M8.1–M8.2 | Bundle capstone worksheet | — (no quiz in the slice) |

Source files for every row live in `course/03-content/`: `m00-orientation/`, `m01-operating-system/`, `m04-spec-driven-saas/`, `m05-security-tests/`, with the slice drawn from `m07-monetize/lesson.md` and `m08-launch-capstone/lesson.md`.

You also get the module files themselves — every `lesson.md`, `lab.md`, and `quiz.md` in searchable text, plus the quiz answer keys, so you can grep rather than rewatch.

---

## What's *not* included — the honest scope note

This bundle is a **subset**. It is four modules plus a launch slice out of a nine-module course. Specifically, it excludes:

- **M2 and M3 — the on-device AI app track** (the capture→transcribe→context→prompt→route pipeline, privacy engineering, coverage floors, notarized releases).
- **M6 — the expertise-product track** (provenance, audience routing, editions).
- **M8.3 — the capstone and demo day**, including the 5-dimension capstone rubric, the recorded demo, and the peer-review exchange.
- **All live cohort elements**: weekly 90-minute workshops, instructor code review on labs, demo day.
- **Instructor-facing production artifacts** (`slides.md`, `video-scripts.md`, `solutions.md`, `facilitation.md`, `lab-rubrics.md`) from every module. The bundle ships the student-facing lesson, lab, and quiz files.

If you want the other two tracks and the capstone, buy the full course at $399 up front. It is the better value, and `pricing.md` shows the arithmetic rather than asserting it. `bundle-map.md` lists the exclusion line by line.

---

## The 6-week map

Full detail — weekly outcome, time budget, and assessment — is in `syllabus.md`.

| Week | You work on | You finish with |
|---|---|---|
| 1 | M0 — three products, one method; environment and first win | A cloned repo, a solver run captured, an evidence log started |
| 2 | M1 — the agent operating system | Your own `constitution.md` + `AGENTS.md` + one completed spec → plan → TDD loop with honest evidence |
| 3 | M4 — the artifact pipeline and the stranger test | A complete spec folder for one real feature of your SaaS |
| 4 | M5.1–M5.2 — tenancy and permissions vs qualifications | Real-JWT isolation tests, including a forbidden write that leaves the row unchanged |
| 5 | M5.3 — seven tiers, playbooks, honest manifest | A drift test that has been seen to fail and a manifest validator that rejects a removed scenario |
| 6 | M7/M8 slice — pricing, packaging, sales page, launch arc | A pricing rationale with sourced comparators, a sales page, and a 5-email arc for your SaaS |

**Total time:** roughly 18–22 hours across six weeks. Weeks 3–5 are the heavy ones (4–5 hours each); they contain the labs.

---

## Proof assets you can open

Every number in this bundle carries a file pointer that resolves inside the workspace. The five you will meet most:

| Claim | Pointer |
|---|---|
| "1,464 passed, 21 skipped" — full-suite evidence, dated 2026-09-12, demoted to historical reference 2026-09-13 | `SignUpFlow/docs/playbooks/validation.md` |
| 7 test tiers, separate processes, one `make test-all` | `SignUpFlow/docs/TESTING.md` |
| 17 spec folders | `SignUpFlow/specs/` |
| Spec 014: 8 stories / 44 FRs / 7 edge cases / 12 success criteria / 6 contracts (~4,661 lines); no `tasks.md` | `SignUpFlow/specs/014-security-hardening/` |
| Three verified drift cases: stale `/specs/020-user-onboarding/` path; "5xP1" printed beside six P1 stories; `migrations/versions/` cited while the repo has only `alembic/versions/` | `SignUpFlow/specs/000-user-onboarding/tasks.md`; `SignUpFlow/specs/014-security-hardening/checklists/requirements.md`; `SignUpFlow/AGENTS.md` (Validation checklist) |

The drift cases are not embarrassments to hide; they are the module's best teaching artifact. Generated output hallucinates. A self-graded "Quality Score: 100%" in `specs/014-security-hardening/checklists/requirements.md` did not catch its own wrong count — only reading the checklist against the spec did. You learn to run those greps on your own files.

---

## FAQ

**Do I need a Mac?** No. No model runs in this bundle. Python 3.11+, git, and a terminal.

**How is this different from the full course?** The full course teaches three product archetypes (on-device app, spec-driven SaaS, expertise product) and ends in a capstone with a demo. This bundle teaches only the SaaS track, in more depth per module, and ends in a launch package instead of a demo.

**How long do I have access?** Lifetime access to the materials; there is no drip and no live schedule.

**What do I leave with?** A spec folder that passes the stranger test, isolation and authorization tests with recorded red runs, a manifest validator that fails on a removed scenario, an evidence log, and a sourced pricing rationale plus sales page for your SaaS.

**Is this "vibe coding"?** The opposite. You use agents under constitutions, verifiable rules, and evidence recording — the bundle's whole argument is that agents raise the stakes for discipline rather than lowering them (`course/03-content/m01-operating-system/lesson.md`, M1.1).

**What if it isn't for me?** Full refund within 14 days; keep the materials (`course/04-sales/pricing-and-platforms.md`, "Money-back guarantee").

**Do you have testimonials?** Not yet, and none are invented. The proof is the repository: open `SignUpFlow/specs/` and `SignUpFlow/docs/playbooks/validation.md` and judge the work directly. Testimonial slots are reserved, not fabricated.
