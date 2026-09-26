# Module 1 — The AI Product Operating System
> Part of AI Product Studio (APS-3) · ~60 minutes · Prerequisites: Module 0

## Overview

Module 0 gave you three shipped products and one loop. This module gives you the machinery that made them shippable by *one engineer working with AI agents*: the **AI product operating system**. It has three parts, and they map exactly to this module's three segments. First, **governance** — how SignUpFlow constrains every agent it works with using a layered stack of instruction files that are short, imperative, and verifiable. Second, **specification** — the spec-kit artifact pipeline that turns an idea into tasks a fresh agent session can execute with no conversation context. Third, **evidence discipline** — the practice of recording validation as dated, SHA-pinned, failure-including evidence instead of a feeling.

Why does this come before any product type? Because AI agents don't replace process; they raise the stakes for it. When code is generated at agent speed, the bottleneck moves to specifying what you want, verifying what you got, and being honest about what was actually validated (`00-research/02-signupflow-deep-read.md`, §1). The archetypes differ; the operating system is the same — and it's the part most builders skip, then pay for.

**Why governance, in numbers — at the level each number supports.** The case for rules, specs and evidence records is not instructor taste. The course's own evidence dataset carries the independent measurement (`course/03-content/m06-expertise-product/evidence-dataset.md`, rows 1–2):

| Row | Finding | Claim level | What it does and does not show |
|---|---|---|---|
| 1 | METR 2025: experienced maintainers **19% slower** with AI on their own repositories (CI +2% to +39%), while *believing* they were 20% faster | Task-level, measured, independent randomized trial, 16 developers, 246 issues | Felt speed and measured speed can point in opposite directions. It does not show AI slows everyone down |
| 2 | METR's Feb-2026 follow-up: −18% and −4%, **both confidence intervals cross zero**; 57 developers, 800+ tasks | Task-level, inconclusive | The effect is not settled either way — which is itself the argument for measuring your own |

DORA's 2025 report adds a correlation from a practitioner survey: AI adoption goes with higher delivery throughput *and* higher delivery instability, with AI amplifying whatever practices a team already has (`course/00-research/08-domain-currency-2026.md`, Domain 2). Read it as direction, not a measured effect. Together they say one thing: when an agent produces code at machine speed, the impression that it went well is the least reliable signal you have. Everything in this module replaces that impression with something a stranger can check.

The case study throughout is SignUpFlow — the spec-driven SaaS from Module 0 — with ListenToMe and AI × QE supplying the variants and the honesty exemplars. In the lab (`m01-operating-system/lab.md`) you build your own starter repo — `constitution.md`, one `AGENTS.md` with a `CLAUDE.md` that imports it, spec templates, a research log, and one hook that checks your evidence log — and run one complete spec → plan → TDD mini-loop on a small CLI feature.

**By the end of this module you can:**

- Write layered agent rules — a constitution, and one `AGENTS.md` that `CLAUDE.md` imports — in imperative, verifiable form, under the ~200-line cap.
- Choose between a rule, a hook, a skill and a subagent for a job, and say what each one cannot do.
- Apply the 5-level instruction hierarchy ("follow the more specific and safer one") and the anti-hallucination rules agents must follow.
- Describe each spec-kit artifact's job (spec, research, data-model, plan, contracts, quickstart, checklist, tasks) and turn one user story into an acceptance scenario plus a task line.
- Record validation evidence in the prescribed format — commands, counts, date, environment, limitations, head SHA — with failures included.

## Segment M1.1 — Govern agents with a constitution and rule files (~20 min)

### Objective

Explain SignUpFlow's layered instruction stack as one `AGENTS.md` imported by `CLAUDE.md`, write rules in its house style, apply the hierarchy and anti-hallucination rules that keep agents honest, and decide when a rule should be a hook, a skill or a subagent instead.

### Lesson

**The stack: one `AGENTS.md`, imported by `CLAUDE.md`.** Open these four files from your SignUpFlow clone and note their lengths:

- `.specify/memory/constitution.md` — **85 lines**. Project principles, "single source of truth above all agent files" (`SignUpFlow/AGENTS.md:181`). It defines two operating contexts (a Ralph implementation loop vs. interactive chat), four principles, an autonomy configuration, and the current validation policy.
- `AGENTS.md` — **188 lines**. The one baseline every agent shares, "Consumed by Codex CLI, Cursor, Aider, Jules, OpenHands, Sourcegraph Amp, Factory, and other tools that read `AGENTS.md`" (`SignUpFlow/AGENTS.md:3`). `AGENTS.md` is an open format, "now stewarded by the Agentic AI Foundation under the Linux Foundation" (the agents.md site's own source, `github.com/agentsmd/agents.md`, read 2026-09-26).
- `CLAUDE.md` — **154 lines** (as of 2026-09-16). Claude-specific addenda, with `AGENTS.md` reached through a markdown link on line 5 (`SignUpFlow/CLAUDE.md:5`).
- `.github/copilot-instructions.md` — a restatement for Copilot, which needs its own file.

**Import, don't link.** Claude Code's memory documentation (code.claude.com/docs/en/memory, read 2026-09-26) spells out what Claude loads. With an `AGENTS.md` and no `CLAUDE.md`, Claude Code v2.1.277 or later reads `AGENTS.md` itself. With both files present, it reads "Your `CLAUDE.md` files only". With a `CLAUDE.md` that imports `AGENTS.md`, it reads both. The import is one line, `@AGENTS.md`, and "Imported files are expanded and loaded into context at launch." A link is not an import: for "a `CLAUDE.md` that tells Claude in words to read `AGENTS.md`", the same page says "Claude sees `AGENTS.md` only if it decides to open the file." That is SignUpFlow's setup. Its `AGENTS.md` still gives the old reason for it — "Claude Code does not read this file natively" (`SignUpFlow/AGENTS.md:5`) — which was true when written and is stale now. For SignUpFlow the import is one line but not a one-line fix: its 188-line `AGENTS.md` imported into its 154-line `CLAUDE.md` would load 342 lines, well past the budget below, so the `CLAUDE.md` would first have to shrink to Claude-only addenda. Start your own repo the current way instead: everything shared lives in `AGENTS.md`, and `CLAUDE.md` holds the import plus only what is specific to Claude Code.

```markdown
@AGENTS.md

## Claude Code addenda
- A Stop hook runs scripts/check-evidence-log.sh. When it blocks, fix the entry it names.
```

Nothing is written twice, and Codex, Cursor and Claude read the same baseline. One cost to know: an import loads in full, so the line budget covers `AGENTS.md` and the addenda together. The same page says "target under 200 lines per CLAUDE.md file," and imported files "still load and enter the context window at launch."

Three properties make this stack work. **One canonical source, many delivery files** — the baseline lives in `AGENTS.md` and the other files import, reference or restate it rather than duplicating prose (`SignUpFlow/docs/ai-agent-coding-strategy.md`, "Single source, multi-host"). **Short files** — house style: "Keep each instruction file under ~200 lines. Split by topic rather than nest" (`SignUpFlow/AGENTS.md`). **Imperative, verifiable rules** — the heart of the house style, stated as a contrast:

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

**Rule, hook, skill or subagent.** A rule is the right tool only for what an agent should *know*. Claude Code treats `CLAUDE.md` "as context, not enforced configuration" (code.claude.com/docs/en/memory), and its best-practices page draws the line: "Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens" (code.claude.com/docs/en/best-practices; both read 2026-09-26). Anthropic's advice for keeping `CLAUDE.md` short follows from that: move procedures into skills, move path-specific rules into `.claude/rules/`, and move anything that must hold every time into a hook. The course's rules for writing a rule still hold — imperative, verifiable, under ~200 lines. This table adds what each mechanism is for, what it cannot do, and when to reach for it:

| Mechanism | What it is for | What it cannot do | Reach for it when |
|---|---|---|---|
| **Rule** — a line in `AGENTS.md` or `CLAUDE.md`, or a file in `.claude/rules/` (a `paths:` list loads it only when Claude reads matching files) | Facts and conventions the agent needs every session: commands, prohibitions, house style | Guarantee anything. It is context the model weighs, and a long file dilutes it | Claude gets a convention or command wrong twice, and the code cannot show it the right one |
| **Hook** — a script bound to an event in `.claude/settings.json`: `Stop` runs when Claude finishes a turn, `PreToolUse` before a tool call | Enforcement. Exit code 2 blocks the tool call, or makes Claude keep working, and Claude reads the script's stderr | Judge meaning. It checks what a script can decide, such as a field being present or a SHA that resolves, never whether the evidence is true. It runs only inside Claude Code, not when you commit from your own terminal | A rule must hold every time and a script can decide it |
| **Skill** — `.claude/skills/<name>/SKILL.md`, loaded when relevant or run as `/<name>`; spec-kit 1.0's `/speckit-plan` is one | A procedure or reference that would bloat `CLAUDE.md`: a release checklist, a style guide | Enforce anything. Claude "interprets the instructions; outcome can vary", and by default its description loads into every session | You paste the same multi-step procedure into chat a third time |
| **Subagent** — `.claude/agents/<name>.md`, or "use a subagent to…" | A worker with its own context window and tool list that returns only a summary: wide research, or a review by a session that did not write the code | See your conversation — it gets only what you pass it, plus `CLAUDE.md`. It enforces nothing, and its summary is still a claim to check | A side task would flood your context, or the work needs a reviewer that did not write it |

(Sources: code.claude.com/docs/en/features-overview and code.claude.com/docs/en/hooks, read 2026-09-26.) SignUpFlow's `.claude/` folder holds only its spec-kit commands (`SignUpFlow/.claude/commands/`) — no hooks, skills, subagents or rules files. It applies the hook principle outside Claude Code instead: its guarded agent runner fails a forbidden Git mutation "even if the agent ignores the command error and prints DONE" (`SignUpFlow/docs/AGENT_RUNNER.md:27-29`), and a policy-regression test guards the no-CI rule (`SignUpFlow/tests/unit/test_local_validation_policy.py`). A rule that must never break gets a check a script runs, not a sentence the model reads. Lab M1 gives your starter one such hook.

### Action step

Open your loop journal and draft **three rules for your own starter repo**, one per layer: one constitution principle (a sentence, with a MUST or a default-off safety stance), one baseline `AGENTS.md` rule (imperative + verifiable), one research-log observation (dated, from something you actually hit in Module 0 — an install hiccup counts). Rewrite any rule that fails the test: *could a stranger check whether it was followed?* Then take the rule you would least trust an agent to follow and name its mechanism from the table — does it stay a rule, or become a hook? In Lab M1 these become your real files.

## Segment M1.2 — Spec → plan → tasks an agent can execute (~20 min)

### Objective

Name each spec-kit artifact and its one-line job, and convert one user story into an acceptance scenario plus a task line an agent could execute without conversation context.

### Lesson

SignUpFlow's features are built with GitHub's spec-kit, whose commands produce a folder of artifacts under `specs/`. The repo installed spec-kit in October 2025 and documents the older dotted command names — `/speckit.specify` → `/speckit.clarify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.analyze` → `/speckit.implement`, with `/speckit.checklist` to check the requirements (`SignUpFlow/docs/SPEC_KIT_SETUP.md:9-18`). Spec-kit 1.0 (released 2026-08-21) installs the same steps into Claude Code as skills: `/speckit-constitution` once per project, then `/speckit-specify` → `/speckit-plan` → `/speckit-tasks` → `/speckit-implement` → `/speckit-converge` per feature, with clarify, checklist and analyze optional (github.com/github/spec-kit README, read 2026-09-26). M4.1 walks the differences. The artifacts did not change. Seventeen such folders exist (`SignUpFlow/specs/`). Each artifact has one job:

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

- **Governance:** an 85-line constitution above one 188-line `AGENTS.md` that every agent reads. `CLAUDE.md` imports it with `@AGENTS.md` and adds only Claude addenda; SignUpFlow's 154-line `CLAUDE.md` still links instead. Every file is imperative, verifiable and under ~200 lines (`SignUpFlow/.specify/memory/constitution.md`, `SignUpFlow/AGENTS.md`, `SignUpFlow/CLAUDE.md:5`).
- **Mechanism:** rules advise, hooks enforce, skills carry procedures, subagents isolate work. A rule that must hold every time becomes a hook (code.claude.com/docs/en/best-practices, read 2026-09-26).
- **Precedence:** five levels, and when they conflict, "follow the more specific and safer one" (`SignUpFlow/AGENTS.md`).
- **Anti-hallucination:** grep before referencing; read facts from the canonical source; present 2-3 differentiated options when ambiguous (`SignUpFlow/AGENTS.md`).
- **Rules graduate:** research-log observation → tested on a real change → promoted → upstreamed (`SignUpFlow/docs/ai-agent-coding-strategy.md`).
- **Spec pipeline:** spec (WHAT, P1/P2/P3, Given/When/Then) → research (numbered decisions) → data-model → plan (Constitution Check gate) → contracts → quickstart → checklist gate → tasks (`[ID] [P?] [Story]`, exact paths, tests first).
- **Evidence:** commands, counts, date, environment, limitations, head SHA; never fabricate a check; include the failures — the click race and the mypy "not a pass" line are the model (`SignUpFlow/docs/playbooks/validation.md`).
- **Done means done:** verified in the installed app ("a permission toggle is not proof"), docs current, and honest reviews that say "do not promote" when the evidence says so (`ListenToMe/AGENTS.md`, `ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md`).

## Discussion prompt

Post the one rule you rewrote from vague to verifiable (before → after), plus the M0 evidence entry you just wrote. Then read two classmates' rules and answer: **could you personally check whether their rule was followed, without asking them anything?** If not, say which word makes it uncheckable — that comment is the whole skill.