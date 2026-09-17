# Module 1 — The AI Product Operating System
> Part of AI Product Studio (APS-3) · ~60 minutes · Prerequisites: Module 0

## Overview

Module 0 gave you three shipped products and one loop. This module gives you the machinery that made them shippable by *one engineer working with AI agents*: the **AI product operating system**. It has three parts, and they map exactly to this module's three segments. First, **governance** — how SignUpFlow constrains every agent it works with using a layered stack of instruction files that are short, imperative, and verifiable. Second, **specification** — the spec-kit artifact pipeline that turns an idea into tasks a fresh agent session can execute with no conversation context. Third, **evidence discipline** — the practice of recording validation as dated, SHA-pinned, failure-including evidence instead of a feeling.

Why does this come before any product type? Because AI agents don't replace process; they raise the stakes for it. When code is generated at agent speed, the bottleneck moves to specifying what you want, verifying what you got, and being honest about what was actually validated (`00-research/02-signupflow-deep-read.md`, §1). The archetypes differ; the operating system is the same — and it's the part most builders skip, then pay for.

The case study throughout is SignUpFlow — the spec-driven SaaS from Module 0 — with ListenToMe and AI × QE supplying the variants and the honesty exemplars. In the lab (`m01-operating-system/lab.md`) you build your own starter repo — `constitution.md`, `AGENTS.md`, spec templates, research log — and run one complete spec → plan → TDD mini-loop on a small CLI feature.

**By the end of this module you can:**

- Write layered agent rules (constitution, `AGENTS.md`) in imperative, verifiable form, under the ~200-line cap.
- Apply the 5-level instruction hierarchy ("follow the more specific and safer one") and the anti-hallucination rules agents must follow.
- Describe each spec-kit artifact's job (spec, research, data-model, plan, contracts, quickstart, checklist, tasks) and turn one user story into an acceptance scenario plus a task line.
- Record validation evidence in the prescribed format — commands, counts, date, environment, limitations, head SHA — with failures included.

## Segment M1.1 — Govern agents with a constitution and rule files (~20 min)

### Objective

Explain SignUpFlow's layered instruction stack, write rules in its house style, and apply the hierarchy and anti-hallucination rules that keep agents honest.

### Lesson

**The stack.** Open these four files from your SignUpFlow clone and note their lengths:

- `.specify/memory/constitution.md` — **85 lines**. Project principles, "single source of truth above all agent files" (`SignUpFlow/AGENTS.md`, "File-by-file scope notes"). It defines two operating contexts (a Ralph implementation loop vs. interactive chat), four principles, an autonomy configuration, and the current validation policy.
- `AGENTS.md` — **188 lines**. The universal baseline "consumed by Codex CLI, Cursor, Aider, Jules, OpenHands, Sourcegraph Amp, Factory" (`SignUpFlow/AGENTS.md`).
- `CLAUDE.md` — **154 lines** (as of 2026-09-16). Claude Code doesn't read `AGENTS.md` natively, so `CLAUDE.md` cross-references it via a link at the top and adds Claude-specific addenda (`SignUpFlow/AGENTS.md`).
- `.github/copilot-instructions.md` — a restatement for Copilot, which needs its own file.

Three properties make this stack work. **One canonical source, many delivery files** — the baseline lives in `AGENTS.md` and the other files reference or restate it rather than duplicating prose (`SignUpFlow/docs/ai-agent-coding-strategy.md`, "Single source, multi-host"). **Short files** — house style: "Keep each instruction file under ~200 lines. Split by topic rather than nest" (`SignUpFlow/AGENTS.md`). **Imperative, verifiable rules** — the heart of the house style, stated as a contrast:

> "Each rule must be verifiable. `Filter every query by org_id.` Not `Be careful with multi-tenancy`." (`SignUpFlow/AGENTS.md`, "House style")

A rule an agent can't check is a vibe, not a rule. Use this contrast table when you write your own:

| Bad rule (unverifiable) | Good rule (verifiable) | Why |
|---|---|---|
| "Be careful with multi-tenancy" | "Filter every query by `org_id`" (`SignUpFlow/AGENTS.md`) | "Careful" can't be executed or checked; a filter can |
| "Keep instruction files manageable" | "Keep each instruction file under ~200 lines" (`SignUpFlow/AGENTS.md`) | A number is checkable; "manageable" is a feeling |
| "Value test coverage" | "Write tests first (TDD): write the failing test, implement to make it pass, run `make test-unit`" (`SignUpFlow/AGENTS.md`) | Names the action and the check command |
| "Handle secrets safely" | "Never commit secrets, API keys, JWT signing keys... Read them from environment variables" (`SignUpFlow/AGENTS.md`, "Safety") | "Never commit X" is greppable; "safely" isn't |

**What a constitution holds.** SignUpFlow's 85-line constitution keeps only what must never drift: four principles — *Native First* (prefer plain Poetry + SQLite over Docker for local dev), *Test-Driven Implementation*, *Simplicity & YAGNI* ("Build exactly what's needed, nothing more."), and *Safety & Reliability*: email and SMS "MUST be disabled by default (`EMAIL_ENABLED=false`, `SMS_ENABLED=false`...)" and payments "MUST be mocked or disabled" (`SignUpFlow/.specify/memory/constitution.md`). It also fixes **autonomy**: "YOLO Mode: DISABLED / Git Autonomy: ENABLED (Commit changes when done)" — agents may commit finished work but never run unchecked destructive commands; `AGENTS.md` adds "When unsure whether an action is reversible, stop and ask" (`SignUpFlow/AGENTS.md`, "Safety").

**Precedence.** When rules overlap, `AGENTS.md` gives a 5-level hierarchy and one tie-breaker: "follow the more specific and safer one."

1. The user's request in the current task.
2. Repository-specific rules in `CLAUDE.md` and `AGENTS.md`.
3. Path-scoped rules under `.github/instructions/` (Copilot).
4. General guidance in `docs/ai-agent-coding-strategy.md`.
5. Inferred best practice.

(`SignUpFlow/AGENTS.md`, "Agent instruction hierarchy")

**Anti-hallucination.** The same file's rules are the ones your agents need most:

> "Do not invent file paths, function names, route paths, commands, URLs, or identifiers. Grep the repo before referencing." (`SignUpFlow/AGENTS.md`, "Anti-hallucination")

> "When the request is ambiguous, present 2-3 differentiated options rather than guessing." (`SignUpFlow/AGENTS.md`, "Anti-hallucination")

And for facts like schema fields or env var names: "read them from the canonical source. Do not recall from memory" (`SignUpFlow/AGENTS.md`). These rules turn hallucination — the biggest failure mode of agent-assisted work — into a checkable prohibition.

**How rules graduate.** New rules don't go straight into `AGENTS.md`. They climb a pipeline defined in `docs/ai-agent-coding-strategy.md` ("How rules graduate"): an observation is recorded in `docs/research-log.md` (which exists precisely so "exploratory notes never become silent rules" — `SignUpFlow/docs/research-log.md`); it is tested on at least one real change; only then is it promoted into `AGENTS.md` or a per-agent file; the source row in `docs/source-repos.md` moves `pending → extracted → promoted`; and if it generalizes, it's upstreamed to `tomqwu/GenAI_Common`. Rules earn their place the same way features do: by surviving contact with real work.

### Action step

Open your loop journal and draft **three rules for your own starter repo**, one per layer: one constitution principle (a sentence, with a MUST or a default-off safety stance), one baseline `AGENTS.md` rule (imperative + verifiable), one research-log observation (dated, from something you actually hit in Module 0 — an install hiccup counts). Rewrite any rule that fails the test: *could a stranger check whether it was followed?* In Lab M1 these become your real files.

## Segment M1.2 — Spec → plan → tasks an agent can execute (~20 min)

### Objective

Name each spec-kit artifact and its one-line job, and convert one user story into an acceptance scenario plus a task line an agent could execute without conversation context.

### Lesson

SignUpFlow's features are built through GitHub's spec-kit slash commands — `/speckit.constitution` → `/speckit.specify` → `/speckit.clarify` → `/speckit.plan` → `/speckit.checklist` → `/speckit.tasks` → `/speckit.analyze` → `/speckit.implement` (`SignUpFlow/docs/SPEC_KIT_SETUP.md`) — which produce a folder of artifacts under `specs/`. Seventeen such folders exist (`SignUpFlow/specs/`). Each artifact has one job:

| Artifact | Job (one line) |
|---|---|
| `spec.md` | The **WHAT**, technology-agnostic: prioritized stories (P1/P2/P3, each independently testable — an MVP slice), Given/When/Then acceptance scenarios, edge cases, success criteria |
| `research.md` | The decisions: numbered entries with options evaluated, rationale, and rejected alternatives — "## Decision 1: Rate Limiting Infrastructure" (`SignUpFlow/specs/014-security-hardening/research.md`) |
| `data-model.md` | The entities and relationships, before code exists |
| `plan.md` | The **HOW**: technical context plus a gate — "*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design*" (`SignUpFlow/specs/014-security-hardening/plan.md`, "Constitution Check") |
| `contracts/` | Per-domain interfaces: class definitions, error keys, test sketches, benchmarks — spec 014 has 6 contract files (`00-research/02-signupflow-deep-read.md`, §2) |
| `quickstart.md` | The timed deployment path with a verification checklist |
| `checklists/requirements.md` | The quality gate before planning: "No implementation details (languages, frameworks, APIs)", "No [NEEDS CLARIFICATION] markers remain", "Requirements are testable and unambiguous" (`SignUpFlow/specs/014-security-hardening/checklists/requirements.md`) |
| `tasks.md` | The executable list: checkbox tasks in `[ID] [P?] [Story]` format, exact file paths, tests written first |

Two disciplines matter most. **Spec WHAT, not HOW.** The spec says *what users need*; technology decisions live in `research.md` and `plan.md`. Spec 014's own checklist confirms the split: the spec describes security capabilities "without specifying HOW," with technology choices deferred to planning (`SignUpFlow/specs/014-security-hardening/checklists/requirements.md`). **Cite exact paths.** Task lines name the file to touch, so an agent with no conversation memory can execute — real example: "`T027 [US1] Implement POST /api/sms/send endpoint per contracts/sms-api.md in api/routers/sms.py`" (`SignUpFlow/specs/019-sms-notifications/tasks.md`).

**ListenToMe's variant** is the same discipline in Swift. Its design spec defines protocol-level interfaces — `AudioCapturing`, `Transcribing`, with exact Swift signatures — so implementations stay swappable (`ListenToMe/docs/superpowers/specs/2026-06-18-listentome-design.md`, §4) — and a **YAGNI non-goals** list: "No cloud backend, accounts, billing, or multi-user... No covert/'stealth' mode" (§2). Its implementation plan is a 2,410-line TDD task list ("write the failing test, watch it fail, write the minimal code, watch it pass, commit") that ends with a **self-review mapping every spec bullet to tasks**: "On-device STT behind swappable `Transcribing` protocol → Tasks 10, 13. ✅" (`ListenToMe/docs/superpowers/plans/2026-06-18-listentome-mvp.md`). Non-goals and self-review are what keep an agent-built plan from growing a life of its own.

**A worked example — from story to executable line.** Take one real-shaped story from SignUpFlow's domain (volunteers genuinely can block dates; the feature exists as the availability router — `SignUpFlow/api/routers/availability.py`, "manage person availability and time-off"):

> **US1 (P1):** As a volunteer, I can block dates so the solver skips me.

Turn it into one acceptance scenario:

> **Given** volunteer Sarah has a blocked-date period covering 2026-04-23, **When** an admin runs the solver for that week, **Then** Sarah receives no assignment and the solution reports zero hard violations.

Then one task line, in the repo's real format:

```text
- [ ] T031 [P] [US1] Implement POST /api/v1/availability/time-off in
      api/routers/availability.py per contracts/availability-api.md: volunteer
      submits blocked dates; write the failing test in tests/api/test_availability.py first
```

Notice what just happened: a sentence of intent became a *checkable* scenario (dates, expected outcome, a measurable claim) and a task that names the file, the contract, the test file, and the order (test first). A fresh agent session — or a teammate — could execute that with no further conversation. That is the entire point of the pipeline: **the spec is the interface between human intent and agent execution** (`00-research/00-synthesis.md`).

### Action step

Pick one feature you actually want to build in this course (any archetype). In your loop journal, write: the story in one sentence with a priority, one Given/When/Then acceptance scenario, and one task line citing exact file paths you will create. In Lab M1 this becomes `specs/001-todo-command/` in your starter repo — same shape, smaller feature.

## Segment M1.3 — Evidence discipline: validation as a record, not a feeling (~20 min)

### Objective

Explain SignUpFlow's no-CI local-validation policy, write an evidence record in its exact format, and apply "include the failures" to your own work.

### Lesson

SignUpFlow runs **no CI checks**. This is a deliberate, tested policy, not an omission: "No CI checks. Run all code review, static analysis, migrations, tests, security scans and artifact validation locally. Record evidence for the pushed revision; never recreate hosted checks or require CI statuses" (`SignUpFlow/.specify/memory/constitution.md`, "Current Validation Policy (2026-09-13)"). There is even a policy-regression test guarding it (`SignUpFlow/tests/unit/test_local_validation_policy.py`).

Why would a production SaaS refuse CI? Because a hosted check is not a *record of what you validated* — it's a pass/fail snapshot that says nothing about commands, environment, or limits. SignUpFlow replaces it with something stronger: **the evidence travels with the revision.** Every PR runs `make test-all` locally and records "commands, outcomes, limitations and the pushed head SHA in the PR" (`SignUpFlow/AGENTS.md`, PR rules) — counts included, dated, with the environment named. The full-suite line you met in Module 0 lives in `docs/playbooks/validation.md`: "make test-all: 420 unit tests passed, 21 skipped; 444 API, 16 CLI, and 325 integration tests passed... 1,464 passed, 21 skipped," with follow-up validation "starting from `cccc6f7`" — a head SHA pinning the evidence to an exact revision.

The hard rule: **"Do not fabricate status checks, bypass protections, or treat missing evidence as success"** (`SignUpFlow/AGENTS.md`, PR rules). A green feeling is not a green suite.

**Include the failures.** The same validation record shows what this means in practice. A browser timing race is recorded, not hidden: "An older recurring-event browser test exposed a click race; wait for HTMX settling before clicking its newly rendered Delete control" — and "this initial failure is not omitted from the evidence" (`SignUpFlow/docs/playbooks/validation.md`). Known debt is named as debt: "Full API mypy | Existing debt: 835 errors in 40 files; not a pass" (`SignUpFlow/docs/playbooks/validation.md`). And the record closes with limits: "Do not count manual operational drills, external delivery, PostgreSQL, DST, venue scheduling or full tenant isolation as verified by these runs" (`SignUpFlow/docs/playbooks/validation.md`). An evidence record that can't say "not verified" isn't evidence — it's marketing.

**Definition of Done means verified in the real thing.** ListenToMe's DoD requires the maintainer to "Verify affected behavior in the installed production app. For audio changes, verify actual system-audio transcription labeled OTHERS; **a permission toggle or microphone pickup is not proof**" (`ListenToMe/AGENTS.md`). Its checklist also sweeps every doc the change touches: "**Stale docs are a Definition-of-Done failure**, not a follow-up" (`ListenToMe/CLAUDE.md`). Tests validate what you built; the DoD validates what you shipped.

**The honest-review pattern.** The strongest artifact in all three repos is ListenToMe's gap review of its own release candidate: "**Recommendation: do not promote the existing 1.3.0 DMG as a broadly validated production release.**" — written *despite* "215 passing Core tests, and 97.24% Core coverage," because those numbers "do not establish capture reliability, durable saving, accurate speaker attribution, or a usable first-run experience" (`ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md`). AI × QE practices the same honesty as a habit: its research log requires that "each entry records the question, what was checked, the outcome, and what changed on the site" (`ai_qe/docs/research-log.md`), and it published its own 14-finding site audit (`ai_qe/research/reviews/site-audit-2026-09-06.md`). Coverage tells you what you tested. Only an honest record tells you what you shipped.

**Your evidence-log template.** Copy this verbatim and use it for every lab in this course:

```markdown
## Evidence — <project> — <feature> — <YYYY-MM-DD>
Commands (with results):
- <command> → <N passed, M skipped, K failed>
- ...
Environment: <OS, Python version, machine notes>
Revision: <`git rev-parse HEAD` output>
Limitations / not verified:
- <honest list — include at least one>
```

If a run failed and you fixed and re-ran, record both lines. If you skipped something, write the skip. The record that admits a failure is worth more than the badge that hides one.

### Action step

Open your loop journal and write one evidence entry now, for the SignUpFlow solver run you did in Module 0 (or any command you've run today): the exact command, the result line, your environment, the date, and at least one limitation (e.g., "sample data only; health score on my-church workspace, not a real tenant"). Then check it against the template above — every field filled. This habit is 20% of your grade in every lab that follows.

## Recap

- **Governance:** an 85-line constitution above a 188-line `AGENTS.md` baseline, with `CLAUDE.md` (154) and Copilot restatements — every file imperative, verifiable, under ~200 lines (`SignUpFlow/.specify/memory/constitution.md`, `SignUpFlow/AGENTS.md`).
- **Precedence:** five levels, and when they conflict, "follow the more specific and safer one" (`SignUpFlow/AGENTS.md`).
- **Anti-hallucination:** grep before referencing; read facts from the canonical source; present 2-3 differentiated options when ambiguous (`SignUpFlow/AGENTS.md`).
- **Rules graduate:** research-log observation → tested on a real change → promoted → upstreamed (`SignUpFlow/docs/ai-agent-coding-strategy.md`).
- **Spec pipeline:** spec (WHAT, P1/P2/P3, Given/When/Then) → research (numbered decisions) → data-model → plan (Constitution Check gate) → contracts → quickstart → checklist gate → tasks (`[ID] [P?] [Story]`, exact paths, tests first).
- **Evidence:** commands, counts, date, environment, limitations, head SHA; never fabricate a check; include the failures — the click race and the mypy "not a pass" line are the model (`SignUpFlow/docs/playbooks/validation.md`).
- **Done means done:** verified in the installed app ("a permission toggle is not proof"), docs current, and honest reviews that say "do not promote" when the evidence says so (`ListenToMe/AGENTS.md`, `ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md`).

## Discussion prompt

Post the one rule you rewrote from vague to verifiable (before → after), plus the M0 evidence entry you just wrote. Then read two classmates' rules and answer: **could you personally check whether their rule was followed, without asking them anything?** If not, say which word makes it uncheckable — that comment is the whole skill.