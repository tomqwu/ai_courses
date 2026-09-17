---
marp: true
theme: aps
paginate: true
title: M1 — The AI Product Operating System
---

<!-- _class: lead -->
# M1 — The AI Product Operating System

**Promise:** govern agents, specify work, record evidence — in your own repo.

**Duration:** ~60 minutes · 3 segments · Lab M1 ~2 hours

<!-- NOTES: Welcome to Module 1. Module 0 gave you three shipped products and one loop; this module hands you the machinery that made them shippable by one engineer working with AI agents. Governance, specification, evidence discipline — three parts, three segments. By the end you will have written your own constitution and AGENTS.md and run one complete spec-to-TDD loop. That is the deliverable, not the notes. Transition: let's state exactly what you will be able to do. Timing: 1 minute. -->

---

## By the end you can…

- Write layered agent rules: imperative, verifiable, under ~200 lines.
- Apply the 5-level instruction hierarchy and anti-hallucination rules.
- Turn one story into a scenario and task.
- Record validation evidence with commands, counts, date, limits, head SHA.

<!-- NOTES: Four capabilities, and each is checkable. Notice they are verbs: write, apply, turn, record. Not "understand governance." You will be graded by artifacts, and every artifact here is a file in your starter repo. The lab closes the loop: a constitution, an AGENTS.md, a spec folder, and one red-then-green pytest run recorded honestly. Transition: first capability — governance. Timing: 2 minutes. -->

---

## Why governance comes before product type

- Agents do not replace process; they raise its stakes.
- Code appears at agent speed; verification stays human-speed.
- The bottleneck moves to: specify, verify, admit limits.
- Archetypes differ; the operating system is identical.
- Most builders skip it, then pay for it.

<!-- NOTES: This is the module's argument. When code is generated quickly, the scarce resource is no longer typing. It is a clear statement of what you want, a check that you got it, and honesty about what was actually validated. SignUpFlow's deep-read makes this point in section one. The three product archetypes differ in what they build, never in how they govern the build. Transition: here is the stack that does the governing. Timing: 2 minutes. -->

---

## Segment M1.1 — The four-file instruction stack

One canonical source, many delivery files.

<!-- _diagram: stack -->

- `.specify/memory/constitution.md` — above all agent files
- `AGENTS.md` — the universal baseline agents read
- `CLAUDE.md` — cross-references it, then adds Claude addenda
- `.github/copilot-instructions.md` — restates rules for Copilot

<!-- NOTES: Four files, one canonical source. The baseline lives in AGENTS.md and is consumed by Codex CLI, Cursor, Aider, Jules, OpenHands, Sourcegraph Amp, and Factory. Claude Code does not read AGENTS.md natively, so CLAUDE.md links to it at the top and adds Claude-specific addenda. Copilot needs its own restatement file. The constitution is the single source of truth above all of them. Transition: the next slide proves the lengths are real. Timing: 3 minutes. -->

---

<!-- _class: proof -->
## Proof: the stack, with real line counts

| File | Lines | Role |
|---|---|---|
| `.specify/memory/constitution.md` | 85 | Principles, single source of truth |
| `AGENTS.md` | 188 | Universal baseline |
| `CLAUDE.md` | 154 | Cross-reference plus addenda |
| `.github/copilot-instructions.md` | 127 | Copilot restatement |

Pointers: `SignUpFlow/.specify/memory/constitution.md`, `SignUpFlow/AGENTS.md`,
```markdown
# SignUpFlow Constitution

> A roster and scheduling system with email/SMS notifications.

## Version
1.1.0
```

`SignUpFlow/CLAUDE.md`, `SignUpFlow/.github/copilot-instructions.md`

<!-- NOTES: Open these four files in your own clone and count. The constitution is 85 lines, AGENTS.md is 188, CLAUDE.md is 154, and the Copilot file is 127 — all under the ~200-line cap the house style sets. The lesson gives this as a table you can verify with wc -l. Why it matters: a rule file an agent cannot hold in context is a rule file it will not follow. Transition: short is necessary, not sufficient — the rules must also be checkable. Timing: 3 minutes. -->

---

## House style: a rule must be verifiable

- Imperative voice, not suggestion.
- A stranger can check whether it was followed.
- Numbers beat adjectives: "under ~200 lines."
- Commands beat prose: name the exact check.
- A rule an agent cannot check is a vibe.

<!-- NOTES: This is the heart of the house style. The repo states the contrast directly: each rule must be verifiable — "Filter every query by org_id," not "Be careful with multi-tenancy." Careful cannot be executed or checked; a filter can. The same test applies to your own files in Lab M1: could a stranger check whether this rule was followed, without asking you anything? Transition: run that test on four real rules. Timing: 3 minutes. -->

---

## The contrast table

| Bad rule | Good rule |
|---|---|
| "Be careful with multi-tenancy" | "Filter every query by `org_id`" |
| "Keep files manageable" | "Keep each file under ~200 lines" |
| "Value test coverage" | "Write tests first; run `make test-unit`" |
| "Handle secrets safely" | "Never commit secrets; read from env vars" |

Pointer: `SignUpFlow/AGENTS.md`, "House style" and "Safety"

<!-- NOTES: Four rewrites, all from AGENTS.md. Look at what changes each time. "Careful" becomes a filter. "Manageable" becomes a number. "Value coverage" becomes an action plus a check command. "Safely" becomes a greppable prohibition: never commit X. This is the exercise you will do in the lab, and it is also the discussion prompt — post your before and after. Transition: a constitution is a special subset of rules. Timing: 3 minutes. -->

---

## What a constitution holds

Four principles in 85 lines — keep only what must never drift.

| Principle | What it fixes |
|---|---|
| Native First | Poetry + SQLite locally, not Docker |
| Test-Driven Implementation | the smallest failing test first |
| Simplicity & YAGNI | build exactly what's needed, nothing more |
| Safety & Reliability | `EMAIL_ENABLED=false`, `SMS_ENABLED=false` |

- Payments MUST be mocked or disabled locally.
- Autonomy is fixed: YOLO DISABLED, Git autonomy ENABLED.

Pointer: `SignUpFlow/.specify/memory/constitution.md:41-53`

<!-- NOTES: The constitution is not a longer AGENTS.md. It holds the few things that must never drift. SignUpFlow's four principles are Native First — prefer plain Poetry and SQLite over Docker locally — Test-Driven Implementation, Simplicity and YAGNI, and Safety and Reliability. Safety is concrete: email and SMS disabled by default, payments mocked or disabled. Autonomy is also fixed: agents may commit finished work, never run unchecked destructive commands. Transition: when two rules conflict, which wins? Timing: 3 minutes. -->

---

## Precedence: five levels, one tie-breaker

| # | Rule source |
|---|---|
| 1 | The user's request in the current task |
| 2 | Repository rules: `CLAUDE.md` and `AGENTS.md` |
| 3 | Path-scoped rules under `.github/instructions/` |
| 4 | `docs/ai-agent-coding-strategy.md` guidance |
| 5 | Inferred best practice |

Tie-breaker: **follow the more specific and safer one.**

Pointer: `SignUpFlow/AGENTS.md:153-161`

<!-- NOTES: Five levels from AGENTS.md. The user's request wins at the top. Repository rules come next. Path-scoped rules for Copilot come third. General strategy guidance is fourth, and inferred best practice is last. The single tie-breaker when rules overlap is the sentence to memorize: follow the more specific and safer one. That is how a specific path rule can beat a general baseline without anyone maintaining a precedence matrix. Transition: the rules that keep agents honest about facts. Timing: 3 minutes. -->

---

## Anti-hallucination rules

- Do not invent paths, function names, routes, or identifiers.
- Grep the repo before referencing anything.
- Read facts from the canonical source; do not recall.
- Ambiguous request? Present 2-3 differentiated options.
- Encode a hard-stop checklist for research tasks.

<!-- NOTES: Hallucination is the biggest failure mode of agent-assisted work, so it gets rules, not advice. AGENTS.md forbids inventing file paths, function names, route paths, commands, URLs, or identifiers — grep first. For schema fields and env var names, read the canonical source; do not recall from memory. When a request is ambiguous, present two or three differentiated options instead of guessing. Each of these is checkable against a transcript. Transition: rules do not arrive fully formed; they graduate. Timing: 3 minutes. -->

---

## How rules graduate

- Observation recorded in `docs/research-log.md`.
- Tested on at least one real change.
- Only then promoted into `AGENTS.md`.

<!-- _diagram: flow -->

- `pending`
- `extracted`
- `promoted`

- Source row moves `pending → extracted → promoted`.
- If it generalizes, upstream it to `GenAI_Common`.

<!-- NOTES: New rules do not go straight into AGENTS.md. The strategy doc defines the pipeline: an observation lands in docs/research-log.md, which exists so exploratory notes never become silent rules. It gets tested on a real change. Only then is it promoted. The source-repos row moves pending to extracted to promoted, and if it generalizes it is upstreamed to tomqwu/GenAI_Common. Rules earn their place the way features do: by surviving contact with real work. Transition: that is governance; now the artifacts governance protects. Timing: 3 minutes. -->

---

## Segment M1.2 — The spec-kit pipeline

<!-- _diagram: flow -->

- `/speckit.constitution`
- `/speckit.specify`
- `/speckit.clarify`
- `/speckit.plan`
- `/speckit.checklist`
- `/speckit.tasks`
- `/speckit.analyze`
- `/speckit.implement`

- Output: a folder of artifacts under `specs/`.
- 17 spec folders exist in SignUpFlow today.

<!-- NOTES: SignUpFlow builds features through GitHub's spec-kit slash commands, in this order. Each step produces a file, and the files are the interface between your intent and an agent session that has no memory of your conversation. There are seventeen spec folders in the repo, so this is not theory. The pipeline answer to "the agent did the wrong thing" is almost always "the spec did not say". Transition: each artifact has exactly one job. Timing: 3 minutes. -->

---

## Each artifact has one job

| Artifact | Job |
|---|---|
| `spec.md` | The WHAT: P1/P2/P3 stories, Given/When/Then |
| `research.md` | Numbered decisions with rejected alternatives |
| `data-model.md` | Entities and relationships, before code |
| `plan.md` | The HOW, behind a Constitution Check gate |
| `contracts/` | Per-domain interfaces, errors, test sketches |
| `quickstart.md` | Timed deployment path with verification |
| `checklists/` | Quality gate before planning |
| `tasks.md` | Checkbox tasks with exact file paths |

<!-- NOTES: This table is the segment's spine, and you will be quizzed on the pairings. The two most confused pairs: spec.md is the technology-agnostic WHAT, while research.md and plan.md hold decisions and the HOW. And checklists is the quality gate before planning, while quickstart is the deployment path. Spec 014's own checklist confirms the split: the spec describes capabilities without specifying HOW, with technology choices deferred to planning. Transition: the next slide is the proof, including an artifact that is deliberately missing. Timing: 4 minutes. -->

---

<!-- _class: proof -->
## Proof: the artifacts are real files

- Spec folders under `SignUpFlow/specs/` — 17 of them.
- Real task line: `SignUpFlow/specs/019-sms-notifications/tasks.md`
- Real gate: `SignUpFlow/specs/014-security-hardening/plan.md`
- Real checklist: `.../014-security-hardening/checklists/requirements.md`
- Spec 014 has **no** `tasks.md`.

```markdown
- [ ] T027 [US1] Implement POST /api/sms/send endpoint per contracts/sms-api.md
  in api/routers/sms.py
- [ ] T028 [P] [US1] Implement GET /api/sms/messages endpoint (message history)
  per contracts/sms-api.md in api/routers/sms.py
```

<!-- NOTES: Proof, not description. There are seventeen folders under SignUpFlow/specs/. The task line "T027 [US1] Implement POST /api/sms/send endpoint per contracts/sms-api.md in api/routers/sms.py" is a real line from spec 019. The Constitution Check gate sentence is real in spec 014's plan. And note the honesty detail from the deep-read: spec 014 has no tasks.md. A folder that stops at planning is a legitimate state, and the record says so rather than inventing a file. Transition: how a story becomes executable. Timing: 3 minutes. -->

---

## Story → scenario → task

- Story: "As a volunteer, I can block dates."
- Scenario: given a blocked period, then zero hard violations.
- Task line: `[ID] [P?] [Story]` plus exact file paths.

```text
- [ ] T031 [P] [US1] Implement POST /api/v1/availability/time-off in
      api/routers/availability.py per contracts/availability-api.md:
      volunteer submits blocked dates; write the failing test in
      tests/api/test_availability.py first
```

- Test first: the failing test is the task's first deliverable.

Pointer: `SignUpFlow/api/routers/availability.py`

<!-- NOTES: Watch the abstraction drop. A sentence of intent becomes a checkable scenario with dates, a measurable outcome, and a named artifact. Then it becomes a task that names the file to touch, the contract to follow, the test file to write first, and the order of work. A fresh agent session — or a teammate — could execute that with no further conversation. That is the entire point of the pipeline: the spec is the interface between human intent and agent execution. Transition: ListenToMe runs the same discipline in Swift. Timing: 4 minutes. -->

---

## ListenToMe's variant: protocols and non-goals

- Design spec defines protocol-level interfaces with Swift signatures.
- Swappable: `AudioCapturing`, `Transcribing`.
- YAGNI non-goals: no cloud backend, accounts, billing.
- No covert or "stealth" mode.
- 2,410-line TDD plan ends with a spec-to-task self-review.

<!-- NOTES: The same discipline in a different language. ListenToMe's design spec pins protocol-level interfaces so implementations stay swappable, and it writes down non-goals: no cloud backend, accounts, billing, multi-user, and no covert mode. Its implementation plan is a 2,410-line TDD task list that ends with a self-review mapping every spec bullet to tasks — for example, on-device STT behind a swappable Transcribing protocol maps to tasks 10 and 13, checked. Non-goals and self-review are what stop an agent-built plan growing a life of its own. Transition: the last segment is evidence. Timing: 3 minutes. -->

---

## Segment M1.3 — No CI checks, by policy

- Local-only validation is a tested policy, not an omission.
- "Never recreate hosted checks or require CI statuses."
- A policy-regression test guards the rule.
- Evidence travels with the revision instead.

| A hosted check | An evidence record |
|---|---|
| A pass/fail snapshot | Commands, counts, date |
| Silent about the environment | Names the environment |
| Silent about the limits | Lists what was not verified |

Pointer: `SignUpFlow/.specify/memory/constitution.md:34-39`

<!-- NOTES: SignUpFlow runs no CI checks. That is a deliberate, tested policy stated in its constitution's Current Validation Policy, and there is a policy-regression test in tests/unit/test_local_validation_policy.py guarding it. The argument: a hosted check tells you pass or fail and nothing about commands, environment, or limits. Replace it with something stronger — the evidence travels with the revision. Every PR records commands, outcomes, limitations, and the pushed head SHA. Transition: here is that record, verbatim. Timing: 3 minutes. -->

---

<!-- _class: proof -->
## Proof: the evidence line

```text
make test-all: 420 unit tests passed, 21 skipped;
444 API, 16 CLI, and 325 integration tests passed.
Across backend, web, contract and browser suites: 1,464 passed, 21 skipped.
```

- Pointer: `SignUpFlow/docs/playbooks/validation.md`
- Dated 2026-09-12; demoted to historical reference 2026-09-13.
- Follow-up validation starts from `cccc6f7` — a pinned head SHA.

<!-- NOTES: This is the line from Module 0, and here is exactly where it lives: docs/playbooks/validation.md in SignUpFlow, not TESTING.md. Note the second bullet carefully. The file is dated 2026-09-12 and was reclassified as historical reference on 2026-09-13, so it is evidence of a past run, not a live status badge. The follow-up validation starts from commit cccc6f7, pinning the evidence to an exact revision. Counting without a date and a SHA is not evidence. Transition: the record's hardest discipline is what it includes. Timing: 4 minutes. -->

---

## Include the failures

- A browser click race is recorded, not hidden.
- "This initial failure is not omitted from the evidence."
- An evidence record that cannot say "not verified" is marketing.

```text
| Full API mypy | Existing debt: 835 errors in 40 files; not a pass |

Do not count manual operational drills, external delivery, PostgreSQL, DST,
venue scheduling or full tenant isolation as verified by these runs.
```

Pointer: `SignUpFlow/docs/playbooks/validation.md:45, 69-70`

<!-- NOTES: Three moves. First, a real failure is named: an older recurring-event browser test exposed a click race; the fix is recorded, and the initial failure stays in the document. Second, known debt is named as debt: full API mypy has 835 errors in 40 files, and the record says "not a pass" instead of rounding it away. Third, the record ends with limits: do not count manual drills, external delivery, PostgreSQL, DST, venue scheduling, or full tenant isolation as verified. Transition: what "done" means once tests are green. Timing: 3 minutes. -->

---

## Done means verified in the shipped thing

- Tests validate what you built; DoD validates what you shipped.
- Verify in the installed production app.
- Stale docs are a Definition-of-Done failure.
- ListenToMe's own review says: do not promote 1.3.0.

> For audio changes, verify actual system-audio transcription labeled OTHERS;
> a permission toggle or microphone pickup is not proof.

Pointer: `ListenToMe/AGENTS.md:21-23`

<!-- NOTES: ListenToMe's Definition of Done requires the maintainer to verify affected behavior in the installed production app. For audio changes, verify actual system-audio transcription labeled OTHERS — a permission toggle or microphone pickup is not proof. Its checklist also states that stale docs are a Definition-of-Done failure, not a follow-up. And the strongest artifact in all three repos is the gap review recommending against promoting 1.3.0 despite 215 passing Core tests and 97.24% coverage, because those numbers do not establish capture reliability. Transition: copy the template now. Timing: 3 minutes. -->

---

## Your evidence-log template

```markdown
## Evidence — <project> — <feature> — <YYYY-MM-DD>
Commands (with results):
- <command> → <N passed, M skipped, K failed>
Environment: <OS, Python version, machine notes>
Revision: <`git rev-parse HEAD` output>
Limitations / not verified:
- <honest list — include at least one>
```

<!-- NOTES: Copy this verbatim and use it in every lab for the rest of the course. If a run failed and you fixed and re-ran, record both lines. If you skipped something, write the skip. The one field students leave empty is limitations, and it is the field that separates a record from a badge. This habit is twenty percent of every lab grade. Transition: now build your own version of all of it. Timing: 3 minutes. -->

---

## Lab M1 — build your operating system

<!-- _diagram: steps -->

- Write `constitution.md` (≤80 lines) and `AGENTS.md` (≤200 lines).
- Write `specs/001-todo-command/`: spec, plan with gate, tasks.
- Run TDD: failing test first, then implement, `pytest -q` green.
- Record red run, green run, environment, head SHA, limitations.

Pass gate: artifacts exist; `pytest tests/ -q` exits 0.

<!-- NOTES: Two hours. You create a starter repo, write a constitution of at most eighty lines and an AGENTS.md of at most two hundred, then a spec folder for a small todo CLI feature. Then you run the loop for real: write the failing tests, watch them fail, implement, watch them pass, commit. The pass gate is objective: the artifacts exist and pytest exits zero. The evidence entry is not optional — it is the point of the lab. Transition: check your understanding with the quiz. Timing: 3 minutes. -->

---

## Quiz M1

- 8 questions: 6 multiple choice, 2 short answer.
- Covers rule verifiability, precedence, artifact jobs, evidence.
- Short answers are applications, not recall.
- Take it before the workshop; labs are graded on evidence.

<!-- NOTES: Eight questions, six multiple choice and two short answer. Q7 asks you to write a Given/When/Then scenario and a task line; Q8 asks for a full evidence entry that keeps a flaky failure visible. Those are the two skills the module is actually about. Take the quiz before the workshop so we can spend live time on the rules you rewrote, not on definitions. Transition: recap. Timing: 1 minute. -->

---

## Recap

- Governance: 85-line constitution, 188-line baseline, every rule verifiable.
- Precedence: five levels; the more specific and safer rule wins.
- Anti-hallucination: grep first; read canonical sources; offer options.
- Spec pipeline: WHAT → decisions → HOW → tasks.
- Evidence: commands, counts, date, environment, limits, head SHA.
- Include the failures; "not a pass" is valid.

<!-- NOTES: Six lines, one per idea. If you remember nothing else: a rule you cannot check is a vibe; a spec without exact paths is not executable; an evidence record without limitations is marketing. Those three sentences are the module. Everything else is the machinery that delivers them. Transition: one discussion prompt to close. Timing: 2 minutes. -->

---

## Discussion prompt

- Post your before → after rule rewrite.
- Post the evidence entry you wrote from Module 0.
- Review two classmates' rules.
- Ask: could I check this without asking them anything?
- Name the word that makes it uncheckable.

<!-- NOTES: Post the vague rule and the verifiable rewrite, plus the Module 0 evidence entry. Then read two classmates' AGENTS.md rules and answer one question: could you personally check whether their rule was followed without asking them anything? If not, name the exact word that makes it uncheckable. That comment is the whole skill — it is the same test the repo applies to itself. Timing: 2 minutes; close the segment. -->
