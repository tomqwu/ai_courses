# Module 4 — The Spec-Driven SaaS: From Idea to Executable Spec

> Part of AI Product Studio (APS-3) · ~75 minutes · Prerequisites: Modules 1–3

## Overview

Module 1 gave you the operating system — constitution, agent rules, templates, one mini-loop. This module runs that loop at production scale on a real SaaS. SignUpFlow is a multi-tenant volunteer-scheduling product (FastAPI + SQLAlchemy 2.0 + JWT) whose features are technically ordinary — CRUD plus a greedy heuristic solver. What the repo demonstrates is a governance system for building with AI agents: 17 spec folders under `specs/`, each a complete, self-contained instruction set. The archetype lesson holds: **agents don't lower the bar for process — they raise it.** When code appears in minutes, the bottleneck moves to specification, verification, and honesty about what was validated.

The exemplar is `specs/014-security-hardening/` — security work specced down to 8 user stories, 44 functional requirements, and roughly 4,700 lines of contracts. This module walks every artifact in that folder, then teaches you to judge spec quality by a single test — *could a fresh agent session with zero conversation memory implement from these files alone?* — and closes with the honest change record: one PR per story, local review with severity-tagged findings, and verification of generated artifacts against the repo itself.

By the end of this module you can:

- **Walk** a production spec folder artifact by artifact and state what each owns and what consumes it (`specs/014-security-hardening/`).
- **Run** the full workflow — specify → clarify → research → data-model → plan → checklist → contracts → tasks → implement — on a feature of your own (`docs/SPEC_KIT_SETUP.md`, `.specify/templates/`).
- **Judge** spec quality by the stranger test and enforce it with the checklist gate's pass rules (`checklists/requirements.md`).
- **Record** the change honestly: one PR per story in the Summary / Changed files / Validation / Follow-ups format, local review with severity and file/line findings, and drift checks on generated artifacts (`AGENTS.md`, `docs/ai-pr-review.md`).

Lab M4 turns this into your own complete spec folder for a real feature.

## Segment M4.1 — The artifact pipeline in full (~25 min)

### Objective

Walk `specs/014-security-hardening/` end to end. For every artifact, name what it owns, which command generates it, and what downstream artifact consumes it — so you can reproduce the set on your own feature in Lab M4.

### Lesson

**The pipeline and its commands.** SignUpFlow drives features with spec-kit slash commands in Claude Code: `/speckit.constitution` → `/speckit.specify` → `/speckit.clarify` → `/speckit.plan` → `/speckit.checklist` → `/speckit.tasks` → `/speckit.analyze` → `/speckit.implement` (`docs/SPEC_KIT_SETUP.md`; command definitions in `.claude/commands/`, templates in `.specify/templates/`). Each command consumes the previous one's output — that is the whole mechanism:

```
 specify ── clarify ── research ── data-model ── plan ── CHECKLIST GATE ── contracts ── tasks ── implement
   WHAT      ≤3 Qs     Phase 0      Phase 1      HOW       pass/fail        Phase 1    Phase 2   Ralph loop
```

Now walk the folder. Every claim below carries the file you can open.

**spec.md — WHAT, technology-agnostic (432 lines).** It opens with 8 prioritized stories: rate limiting (US1), audit logging (US2), CSRF (US3), session invalidation (US4), 2FA (US5), security headers (US6), input validation (US7), password reset (US8) — six P1, two P2. Each carries a plain-language journey, a "Why this priority" line, an "Independent Test," and Given/When/Then acceptance scenarios. Here is US1's first, verbatim:

> 1. **Given** a user attempts to log in, **When** they fail authentication 5 times within 5 minutes, **Then** further login attempts are blocked for 15 minutes

(`specs/014-security-hardening/spec.md`, US1.) Note the numbers — 5, 5, 15 — they recur downstream like a refrain. Below the stories sit 7 edge cases (from shared-IP false positives to distributed brute-force attacks), then 44 functional requirements FR-001–FR-044 in nine category groups — every one phrased "System MUST…", none naming a technology — then 12 measurable success criteria (SC-001–SC-012: 100% brute-force blocking, audit writes within 1 second), key entities with fields but no implementation, and an Open Questions section recording 4 decisions each dated "TBD (implementation phase)" rather than silently resolved.

**research.md — Phase 0, decisions with receipts (965 lines).** Eight numbered decisions, each with the same anatomy: Decision → Options Evaluated (pros and cons per option) → Rationale → Implementation Details (code sketch, config, cost). Decision 1 chooses Redis for rate limiting over process-local memory — in-memory is "lost on server restart," "not shared across API instances," and "only acceptable for development, not production." Decision 2 chooses TOTP over SMS because "NIST SP 800-63B deprecates SMS for 2FA," SIM-swap attacks are well documented, and SMS carries per-message cost; the rationale ends "SMS rejected due to ongoing cost and security vulnerabilities" (`specs/014-security-hardening/research.md`, Decisions 1–2). The remaining decisions pick a PostgreSQL audit-log table, `itsdangerous` for CSRF tokens, `bleach` for sanitization, Redis for sessions, FastAPI middleware for headers, and `itsdangerous` for reset tokens. The file closes with a technology-stack summary, a compliance mapping (SOC 2, HIPAA, GDPR, NIST), a $15/month cost analysis, and a risk table — self-scored "8/8 decisions made with rationale."

**data-model.md — deliberately absent here.** The plan explains: "Security feature has no traditional `data-model.md` (security infrastructure spans multiple entities). Security schema documented in contracts" (`specs/014-security-hardening/plan.md`). Six other specs do have one (000, 001, 011, 015, 016, 019 — verify with `find specs -name data-model.md`). The lesson: the template defines the full set; each feature decides which artifacts earn their keep.

**plan.md — HOW (334 lines).** The Technical Context section pins what the spec deliberately didn't: Python 3.11; dependencies with versions (`redis-py`, `pyotp` 2.9.0, `bleach` 6.1.0, `itsdangerous`); storage (PostgreSQL 15+ for audit logs, Redis 7.0+ for counters and sessions); performance goals (rate-limit check <5ms, audit write <10ms); constraints (zero breaking changes to the auth flow, append-only audit logs); and scale estimates (~10K active rate limits, ~90K audit records). Then the gate, in the template's own words:

> *GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

(`.specify/templates/plan-template.md`, "Constitution Check"; filled in at `specs/014-security-hardening/plan.md`.) Plan 014 walks seven principles — User-First Testing (E2E mandatory), Security-First, Multi-tenant Isolation, Test Coverage Excellence, Internationalization by Default, Code Quality Standards, Clear Documentation — each with a compliance verdict and evidence, ending "Constitution Violations: NONE" and "Complexity Justification: N/A." The Complexity Tracking table is filled "ONLY if Constitution Check has violations that must be justified." Finally the Project Structure annotates every file `[NEW]` or `[MODIFY]` — `api/services/rate_limiter.py` `[NEW]`, `api/routers/auth.py` `[MODIFY]` "Add rate limiting, 2FA check" — roughly 10 files modified, 40 created.

**contracts/ — the seams (6 files, 4,661 lines).** One contract per domain: rate-limiting, audit-logging, csrf-protection, session-management, 2fa-api, password-reset. `contracts/rate-limiting.md` (681 lines) shows the shape: a config table — `POST /api/auth/login` | 5 min window | 5 attempts | Per IP | 15 min lockout — the same numbers as the acceptance scenario; a service API with class and method signatures; i18n error messages; a Redis key schema; monitoring metrics; test sketches; performance benchmarks; and configuration tuning.

**quickstart.md — timed deployment (643 lines).** "10-Minute Deployment": a prerequisites checklist (Redis 7.0+, PostgreSQL 15+, env vars), timed steps — "Step 1: Install Dependencies (2 minutes)" with exact `poetry add pyotp==2.9.0` commands — a verification checklist, and troubleshooting.

**checklists/requirements.md — the gate (50 lines).** Three sections with every box checked: Content Quality ("No implementation details (languages, frameworks, APIs)"), Requirement Completeness ("No [NEEDS CLARIFICATION] markers remain"; "Requirements are testable and unambiguous"), Feature Readiness. The verdict block reads "✅ ALL CHECKS PASSED … Quality Score: 100% (all checklist items passed)," validated 2025-10-22, generated by `/speckit.checklist`. Hold that "100%" in mind: M4.3 shows one number in this very file that is wrong.

**tasks.md — Phase 2.** Spec 014 never got one; its plan's "Next Steps" still lists "Phase 2: Run `/speckit.tasks`." The format is defined in `.specify/templates/tasks-template.md`: checkboxes `[ID] [P?] [Story]` where `[P]` marks parallelizable tasks and `[US#]` ties each task to its story, with the instruction "Include exact file paths in descriptions," organized as Phase 1 Setup → Phase 2 Foundational ("⚠️ CRITICAL: No user story work can begin until this phase is complete") → one phase per user story with tests written first and failing → Polish, with a checkpoint after each story. In real use, `specs/000-user-onboarding/tasks.md` (467 lines): "T017 [P] [US1] Implement create_wizard_state method in api/services/onboarding_service.py." Every task names a file.

### Action step

Open the repo and recount the claims above: `ls specs/` (17 folders), `ls specs/014-security-hardening/` (note what's absent), then open `spec.md` and count the stories, FRs, edge cases, and success criteria. Post: which artifact you'd be most tempted to skip on your next feature, and what breaks downstream when you do — name the artifact that consumes it.

## Segment M4.2 — Spec quality: what makes an agent-executable spec (~25 min)

### Objective

State the one test that defines spec quality — a fresh agent session with zero conversation memory can implement from the artifacts alone — and apply its consequences: WHAT/HOW separation, story independence, test-ready acceptance scenarios, bounded clarification, exact-path tasks, and contracts as the interface between sessions.

### Lesson

**The stranger test.** SignUpFlow runs implementation as a Ralph loop: a script starts an agent with, in essence, the prompt "implement spec" (`.specify/memory/constitution.md`, Context A). That agent has no chat history, no memory of why any decision was made, and — in Ralph mode — no appetite for questions. Everything it knows, it reads from the spec folder and the repo. So the quality test for every artifact: strip away the conversation — could a stranger implement? Every rule below exists because a stranger can't ask follow-ups.

**WHAT vs HOW.** spec.md owns WHAT — user-visible behavior, technology-agnostic. plan.md owns HOW — languages, versions, storage, performance targets. The gate's first checked rule enforces the split: "No implementation details (languages, frameworks, APIs)" (`specs/014-security-hardening/checklists/requirements.md`). 014's checklist notes put it plainly: "All technology decisions (Redis, specific auth libraries, storage mechanisms) documented in assumptions or deferred to planning phase." Kill the common misconception here: a good spec does **not** include the schema SQL. Schema belongs to `data-model.md`, contracts, and migrations; the spec's "Key Entities" section describes entities "without implementation" (`.specify/templates/spec-template.md`). The separation also lets research overturn a tentative lean without touching requirements: 014's spec records Open Decision 1 as "Use in-memory cache (Redis) … with database backup," dated TBD — and `research.md` Decision 1 then chose Redis as the store itself and rejected in-memory outright. The requirement never changed; the reversal is on record.

**Every story is an MVP slice.** The spec template mandates it: "Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them, you should still have a viable MVP" — independently developed, tested, deployed, and demonstrated (`.specify/templates/spec-template.md`). Each 014 story carries its own "Independent Test" line (US1: simulate failed logins, verify lockout and message). Consequences: partial implementation still ships; PRs can carry one story each (M4.3); and the task file groups tasks by story for exactly this reason.

**Acceptance scenarios must be ready to become tests.** Re-read the quoted scenario from M4.1: "fail authentication 5 times within 5 minutes → blocked for 15 minutes." Those numbers reappear as FR-001, as the contract's config row, and as an assertion in a test sketch. That is the standard: a scenario is done when a test author needs to make zero further decisions. A Then-clause like "Then the system is secure" fails the gate's "Requirements are testable and unambiguous" rule — it can't be coded against.

**Bounded clarification.** A draft may mark unknowns — the template shows `FR-006: System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified]` (`.specify/templates/spec-template.md`) — but the gate requires "No [NEEDS CLARIFICATION] markers remain" before planning. Two resolution paths: `/speckit.clarify`, which runs *before* `/speckit.plan` on a deliberately small budget — 014's own next-steps line says "Run `/speckit.clarify` if clarifications needed (max 3 questions)" (`specs/014-security-hardening/spec.md`, "Next Steps") — or documenting a default in Assumptions, which is how 014 settled 90-day log retention, 1-hour token expiry, and ±30-second TOTP tolerance. Ask early, not often: after clarification the spec must stand alone. (Honest footnote: the command definition currently says "up to 5 highly targeted clarification questions" (`.claude/commands/speckit.clarify.md`) — a drift M4.3 returns to.)

**The gate's pass rules.** `checklists/requirements.md` checks three groups, all pass/fail: Content Quality (no implementation details, user-value focus, readable by non-technical stakeholders), Requirement Completeness (no NEEDS CLARIFICATION remains, testable and unambiguous, measurable *and* technology-agnostic success criteria, scenarios defined, edge cases identified, scope bounded, dependencies and assumptions identified), Feature Readiness (every FR has acceptance criteria, scenarios cover primary flows, no implementation leakage). "Checklists are bureaucracy" is exactly backwards: this gate is the cheapest point in the pipeline to catch a spec that would waste an entire autonomous implementation loop. What the gate is *not*: proof — it is generated by `/speckit.checklist` and grades itself (M4.3).

**Tasks cite exact file paths.** "Include exact file paths in descriptions" (`.specify/templates/tasks-template.md`). Why: a fresh agent session doesn't know your project layout, and `AGENTS.md`'s anti-hallucination rule forbids inventing it: "Do not invent file paths, function names, route paths, commands, URLs, or identifiers. Grep the repo before referencing." A task like "update the backend" forces the agent to guess — which is how hallucinated endpoints happen — or to burn its budget rediscovering structure. A task like "T017 [P] [US1] Implement create_wizard_state method in api/services/onboarding_service.py" makes the agent's first action a grep that *confirms* rather than invents. "Tasks can say 'update backend'" is the misconception to unlearn.

**Contracts exist because sessions don't share memory.** A contract is the interface between the session that designed the feature and the (different) session that implements it: request/response shapes, error keys, key schemas, and test sketches pin the seam so neither side improvises at the boundary. `contracts/rate-limiting.md`'s config table is where the spec's WHAT and the plan's HOW first meet — the same 5/5/15 numbers, now with scopes and key formats attached.

**The Constitution Check, and why.** The gate line is "Must pass before Phase 0 research. Re-check after Phase 1 design" (`.specify/templates/plan-template.md`). Purpose: an agent writing a plan will cheerfully violate project principles — skip E2E testing, add unneeded infrastructure — because it hasn't internalized them. The check forces the plan to walk each principle and show compliance, and forces any violation into the Complexity Tracking table where it must be argued ("Fill ONLY if Constitution Check has violations that must be justified"). In 014: seven principles, seven verdicts, zero violations, justification table empty.

**The Ralph loop closes the argument.** Context A of the constitution: started by `ralph-loop.sh` or a prompt mentioning "implement spec," the agent must "Pick highest priority incomplete spec (from `specs/`), Complete ALL acceptance criteria, Output `<promise>DONE</promise>` when 100% complete" (`.specify/memory/constitution.md`). Read that as a design constraint: an agent that must complete ALL acceptance criteria, and cannot ask questions, is only safe if the spec is complete, unambiguous, testable, and gated. The pipeline is the precondition for autonomy, not ceremony around it.

### Action step

Trace one story through the pipeline. Take US1: acceptance scenario → FR-001–FR-004 → `research.md` Decision 1 → `plan.md`'s `[NEW]`/`[MODIFY]` lines → `contracts/rate-limiting.md`'s config table → where a test would assert the lockout. Post the trace with file pointers and flag any link where the language went vague — that's what you'd fix before running a Ralph loop.

## Segment M4.3 — From tasks to PR: the honest change record (~25 min)

### Objective

Turn a completed story into a PR a reviewer can trust: one PR per story in the fixed body format, local code review with severity-tagged findings — and the discipline of verifying generated artifacts against the repo, using three drift cases found in SignUpFlow's own specs.

### Lesson

**One PR per story.** The task file is built for it: tasks grouped by story, tests first, and a checkpoint after each story — "Stop at any checkpoint to validate story independently" (`.specify/templates/tasks-template.md`). A PR carrying exactly one story is reviewable in one sitting, demoable, and revertable without collateral damage.

**The PR body format.** `AGENTS.md` ("PR and commit format") fixes four sections:

```text
Summary:      one line per change
Changed files: path: reason
Validation:   what you ran (commands and result)
Follow-ups:   known gaps, deferred work, or open questions
```

The rules behind it (`AGENTS.md`, "PR rules"): run `make test-all` for every PR; there is no CI — all validation runs locally, so record commands, outcomes, limitations, and the pushed head SHA in the PR; merge only after local validation and review are recorded and GitHub reports mergeable; and never "fabricate status checks, bypass protections, or treat missing evidence as success." A Validation section that says "tests pass" with no command is not evidence; one that records a failure still is — the honest record outranks the flattering one.

**Local code review.** The repo's review policy is a file: `docs/ai-pr-review.md` ("Ollama is not a code-review provider" — it supersedes a retired hosted review gate). The checklist: record the PR head and base SHAs and inspect the complete diff locally with affected source, tests, and agent instructions; check correctness, security, **organization isolation**, authorization, API contracts, migrations, user workflows, and **negative-path test coverage**; report findings with severity and file/line references, fix blocking issues, and re-review the final diff; run `make test-all` and record actual commands, results, skips, and limitations; record the outcome and SHAs in the PR and invalidate stale evidence after source changes. Two hard lines: "Do not claim independent review when the builder performed the review itself," and — `AGENTS.md` PR rule 4 — "**Missing review is not approval**." Reviewer agents must not merge.

**Generated artifacts drift — verified in this repo.** Everything in a spec folder is generated output — `/speckit.tasks` wrote the tasks file, `/speckit.checklist` graded the checklist — and generation is where hallucination risk concentrates. Three verified cases:

1. **A renumbered spec path.** `specs/000-user-onboarding/tasks.md` opens "Input: Design documents from `/specs/020-user-onboarding/`" — but the folder is `specs/000-user-onboarding`. The feature was renumbered; the generated tasks file kept the stale path.
2. **A wrong count in a self-graded gate.** `specs/014-security-hardening/checklists/requirements.md` reports "8 prioritized user stories: 5xP1, 2xP2, 0xP3" — but the spec has **six** P1 stories (US1, US2, US3, US4, US7, US8). The same checklist's notes then list six P1 features while printing "5xP1." The "Quality Score: 100%" did not catch it; only reading the checklist against the spec did.
3. **A path that doesn't exist.** The same tasks file assigns migrations to `migrations/versions/add_onboarding_tables.py` — the repo has no `migrations/` directory; migrations live in `alembic/versions/` (`AGENTS.md`, Validation checklist).

The repo already has the rules that target this: `AGENTS.md`'s operating loop step 6 — "Search for stale commands, counts, check names, and feature-state claims before declaring done" — and the anti-hallucination rule, "Grep the repo before referencing." Treat generated artifacts like generated code: grep paths before citing them, recount counts against their source, and never let a self-reported score substitute for opening the file. Lab M4 runs these checks on your own generated checklist.

### Action step

Open `specs/000-user-onboarding/tasks.md`. Diff one real task against its acceptance scenario: T022–T024 (wizard endpoints in `api/routers/onboarding.py`) against US1's scenarios in `specs/000-user-onboarding/spec.md` (auto-launch with a 5-step progress indicator; real-time field validation; completion confirmation). Post: (a) whether the task lines alone would let a fresh agent implement story 1 — name anything missing; (b) whether you would have caught the stale `/specs/020-user-onboarding/` path on line 3 unaided, and the exact grep you'd now run on your own task files.

## Recap

- The pipeline is a command chain, each step consuming the last: `/speckit.specify` (WHAT) → `/speckit.clarify` → `research.md` (Phase 0 decisions with rejected alternatives) → `data-model.md` → `plan.md` (HOW + Constitution Check) → `checklists/requirements.md` (gate) → `contracts/` (seams) → `tasks.md` (Phase 2, exact paths) → implement (`docs/SPEC_KIT_SETUP.md`).
- Spec 014 shows the set at scale — 8 stories / 44 FRs / 7 edge cases / 12 success criteria; 8 research decisions; 6 contracts totaling 4,661 lines — and one honest gap: no tasks.md yet.
- Spec quality has one test — the stranger test — and the gate enforces it: no implementation leakage, everything testable, no NEEDS CLARIFICATION left, every story an MVP slice, every task citing an exact path.
- The Ralph loop raises the stakes: an agent that must "Complete ALL acceptance criteria" without asking questions is safe exactly to the degree your artifacts are complete (`.specify/memory/constitution.md`).
- The change record is a format, not a feeling: one PR per story; Summary / Changed files / Validation / Follow-ups; local review with severity + file/line findings; "Missing review is not approval."
- Generated artifacts drift — a renumbered path, a wrong count in a self-graded gate, a nonexistent migrations dir — and the countermeasure is already in `AGENTS.md`: grep before referencing, recount against source.

## Discussion prompt

Post to the community with the template below:

> **M4 — Spec-driven SaaS — [your name]**
> Feature I'd spec first with this pipeline: [feature, one line]
> Artifact I was most tempted to skip: [artifact] — what would have broken downstream: [artifact + consequence]
> Hardest thing to make "stranger-testable": [scenario/FR/task you had to sharpen]
> One drift check I now run on generated files: [grep or recount, one line]

Then read two classmates' posts and comment on one: would *their* sharpest acceptance scenario let you implement without asking a question? That is the stranger test, applied to each other.