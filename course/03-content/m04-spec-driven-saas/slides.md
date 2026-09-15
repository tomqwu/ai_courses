---
marp: true
theme: aps
paginate: true
title: M4 — The Spec-Driven SaaS: From Idea to Executable Spec
---

# M4 — The Spec-Driven SaaS

**Promise:** produce a spec folder a stranger can implement from.
**Duration:** ~75 min lesson + 90–120 min Lab M4.
**Case study:** SignUpFlow · `specs/014-security-hardening/`

<!-- NOTES: Welcome to Module 4. In M1 you got the operating system; today we run it at production scale on a real multi-tenant SaaS. The promise is narrow and testable: by the end you can produce a spec folder complete enough that a fresh agent session — no chat history, no memory of your reasoning — can implement story 1 without asking you a single question. SignUpFlow drives features with spec-kit slash commands, and its 17 spec folders are the evidence. Timing: M4.1 about 25 minutes walking one folder, M4.2 about 25 on quality, M4.3 about 25 on shipping honestly. Transition: first, the shape of the whole pipeline. -->

---

## By the end you can…

- **Walk** a production spec folder, artifact by artifact
- **Run** specify → clarify → plan → checklist → tasks
- **Judge** specs by the stranger test
- **Enforce** the checklist gate's pass rules
- **Record** the change with severity-tagged review
- **Catch** drift in generated artifacts

<!-- NOTES: Read these as six verbs, not topics — each one is something you will do in the lab, not something you will have heard about. Walk, run, judge, enforce, record, catch. The last two are the ones that separate a demo from a deliverable: anyone can generate a beautiful spec folder; the discipline is in reviewing it locally with findings that name severity and file, and in greeting generated files with suspicion rather than trust. If you only remember two slides from today, remember the stranger test and the drift checks. Transition: let's start with the whole pipeline in one picture. -->

---

## M4.1 — The command chain

```
specify ── clarify ── research ── data-model ── plan ── CHECKLIST ── contracts ── tasks
  WHAT      ≤3 Qs      Phase 0      Phase 1      HOW      pass/fail     seams     Phase 2
```

Each command consumes the previous one's output.
`docs/SPEC_KIT_SETUP.md`; commands in `.claude/commands/`.

<!-- NOTES: This is the entire mechanism, and its whole virtue is that it is boring. Each slash command reads what the last one wrote; nothing is carried in anyone's head. `/speckit.specify` writes WHAT; `/speckit.clarify` burns a small question budget; Phase 0 research records decisions; data-model and plan add HOW and the Constitution Check; the checklist gates; contracts pin the seams; tasks turn it into work. The command definitions live in `.claude/commands/` and the templates in `.specify/templates/` — both openable in the clone. Notice there is exactly one gate, and it is cheap. Transition: now walk the folder itself, starting with WHAT. -->

---

## Proof: `spec.md` owns WHAT

- 8 stories; **six P1**, two P2
- 44 FRs, all "System MUST…"
- 7 edge cases · 12 success criteria
- Given/When/Then with real numbers
- Zero technology named — no Redis, no SQL

`specs/014-security-hardening/spec.md`

<!-- NOTES: Open the file on screen. US1, verbatim: "Given a user attempts to log in, When they fail authentication 5 times within 5 minutes, Then further login attempts are blocked for 15 minutes." Those three numbers — 5, 5, 15 — will reappear in an FR, in a contract config row, and in a test assertion. That recurrence is the point. Below the stories: 44 functional requirements in nine category groups, every one phrased "System MUST", none naming a technology. And the eight stories are six P1 and two P2 — count them, because M4.3 shows a generated file that miscounted them. Transition: WHAT settles behavior; research settles technology. -->

---

## Proof: `research.md` — decisions with receipts

- 8 numbered decisions, same anatomy each

<!-- _diagram: flow -->

- Decision
- Options
- Rationale
- Implementation

- Decision 1: Redis, rejecting in-memory outright
- Decision 2: TOTP over SMS

`specs/014-security-hardening/research.md`

<!-- NOTES: 965 lines, eight decisions. The anatomy never varies: the decision, the options evaluated with pros and cons, the rationale, then implementation details. Decision 1 chooses Redis and says in-memory counters are lost on restart and not shared across API instances. Decision 2 rejects SMS because NIST SP 800-63B deprecates it and SIM-swap is well documented. Here is the rule to steal: a decision without a rejected alternative is a preference, not a decision. Read the file as a record of roads not taken. Transition: next, the artifact 014 deliberately does not have. -->

---

## Proof: `plan.md` — HOW, plus one absence

- **Constitution Check** gate: seven principles, seven verdicts
- "Constitution Violations: NONE"
- Complexity Tracking table, filled only if violations
- Every file annotated `[NEW]` or `[MODIFY]`
- No `data-model.md` here — security spans entities

`specs/014-security-hardening/plan.md`, `.specify/templates/plan-template.md`

<!-- NOTES: The gate line is in the template's own words: "Must pass before Phase 0 research. Re-check after Phase 1 design." Plan 014 walks seven principles — User-First Testing with E2E mandatory, Security-First, Multi-tenant Isolation, Coverage Excellence, i18n by Default, Code Quality, Clear Documentation — gives each a verdict and evidence, and ends with zero violations and an empty Complexity Tracking table. Note the honest absence: 014 has no data-model.md because security infrastructure spans many entities, and the plan says so. Six other specs do have one — the template defines the full set; each feature decides what earns its keep. Transition: the HOW meets the WHAT in contracts. -->

---

## Proof: `contracts/` — six seams

- rate-limiting 681 · 2fa-api 823 · audit-logging 900
- csrf 708 · session 748 · password-reset 801
- **4,661 lines** total
- Config table repeats the spec's numbers
- Key schema, error keys, test sketch, benchmarks

`specs/014-security-hardening/contracts/rate-limiting.md`

<!-- NOTES: Six contracts, 4,661 lines together. The rate-limiting config table's first row reads `POST /api/auth/login`, 5 min window, 5 attempts, per IP, 15 min lockout — the same 5/5/15 as US1's acceptance scenario, now with a scope and a key format attached. That is what a contract is for: it is where WHAT and HOW first meet, and where neither side gets to improvise at the boundary. It also carries i18n error messages, monitoring metrics, test sketches, and performance benchmarks. If you write one artifact carefully in the lab, make it the contract. Transition: deployment and the gate. -->

---

## Proof: the gate and the quickstart

- `quickstart.md`: "10-Minute Deployment", timed steps
- Prerequisites, verification checklist, troubleshooting
- `checklists/requirements.md`: three pass/fail groups
- Verdict: "ALL CHECKS PASSED … Quality Score: 100%"
- Validated 2025-10-22, generated by `/speckit.checklist`

`specs/014-security-hardening/quickstart.md`, `checklists/requirements.md`

<!-- NOTES: The quickstart is 643 lines of timed deployment with exact commands like `poetry add pyotp==2.9.0`. The checklist is 50 lines and grades three groups: Content Quality, Requirement Completeness, Feature Readiness. Its first rule is the WHAT/HOW enforcement line — "No implementation details" — and it ends with a 100% quality score. Hold that number. In M4.3 I show you a count in this very file that is wrong, and the 100% did not catch it. A self-graded gate tells you what its author believed; only reading it against the spec tells you what is true. Transition: and then there's the file 014 never got. -->

---

## Proof: `tasks.md` — Phase 2, and the gap

- 014 has **no** `tasks.md`
- Its plan still lists "Phase 2: Run `/speckit.tasks`"
- Format: `.specify/templates/tasks-template.md`
- `[P]` parallel, `[US#]` story, exact file paths
- Real line: T017 creates a method in `api/services/onboarding_service.py`

`specs/000-user-onboarding/tasks.md`, `.specify/templates/tasks-template.md`

<!-- NOTES: This is the honest gap in the exemplar: 014 is specced down to four thousand lines of contracts and never generated a task breakdown — its plan's Next Steps still lists Phase 2. So we read the real format elsewhere. From the template: checkboxes `[ID] [P?] [US#]`, `[P]` marks parallelizable work, `[US#]` ties each task to a story, and the instruction "Include exact file paths in descriptions." Then `specs/000-user-onboarding/tasks.md`, 467 lines, line 66 verbatim: "T017 [P] [US1] Implement create_wizard_state method in api/services/onboarding_service.py." Every task names a file. Transition: that closes M4.1 — now, what makes a spec good? -->

---

## M4.2 — The stranger test

- Implementation runs as a Ralph loop
- Agent gets "implement spec" and no history
- It cannot ask follow-ups
- So: strip the conversation — could a stranger implement?
- Every rule below exists because of this

`.specify/memory/constitution.md`, Context A

<!-- NOTES: The constitution's Context A defines the Ralph loop: started by `ralph-loop.sh` or a prompt mentioning "implement spec", the agent must "Pick highest priority incomplete spec (from `specs/`)", "Complete ALL acceptance criteria", and output `<promise>DONE</promise>` when 100% complete. That agent has no chat history. In Ralph mode it has no appetite for questions. So the quality test for every artifact is: delete the conversation — could a stranger implement? Everything in this segment follows from that one sentence. Transition: first consequence, the split between WHAT and HOW. -->

---

## WHAT vs HOW

- `spec.md`: user-visible behavior, technology-agnostic
- `plan.md`: languages, versions, storage, performance targets
- Gate rule: "No implementation details (languages, frameworks, APIs)"
- Schema SQL belongs to data-model, contracts, migrations
- Spec "Key Entities" describe fields **without implementation**

`.specify/templates/spec-template.md`, `checklists/requirements.md`

<!-- NOTES: Kill the common misconception here: a good spec does not contain the schema. Entities are described without implementation; the SQL lives in data-model and migrations. And the separation buys you something real. 014's spec records Open Decision 1 as using an in-memory cache with a database backup — dated TBD — and then research Decision 1 chose Redis as the store and rejected in-memory outright. The requirement never changed; the reversal is on the record. If HOW had leaked into the spec, that reversal would have been a spec edit. Transition: consequence two, stories as MVP slices. -->

---

## Every story is an MVP slice

- Template: each story "INDEPENDENTLY TESTABLE"
- Implement one story and you still ship value
- Each 014 story carries its own "Independent Test" line
- US1: simulate failed logins, verify lockout, verify message
- Tasks group by story for exactly this reason

`.specify/templates/spec-template.md`, `specs/014-security-hardening/spec.md`

<!-- NOTES: The spec template mandates it: "Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them, you should still have a viable MVP." Independently developed, tested, deployed, demonstrated. Every 014 story carries an Independent Test line; US1's is to simulate failed logins and verify both the lockout and the message shown. Three consequences follow: a partial implementation still ships, a PR can carry exactly one story, and the task file groups work by story with a checkpoint after each. Transition: and the scenarios inside a story have their own bar. -->

---

## Scenarios ready to become tests

- "fail 5 times in 5 minutes → blocked 15 minutes"
- Numbers reappear as FR, contract row, test assertion
- Standard: a test author makes zero decisions
- "Then the system is secure" fails the gate
- So does "handled appropriately" — code against what?

`specs/014-security-hardening/spec.md` US1

<!-- NOTES: Recall US1's first scenario. The numbers 5, 5, and 15 recur downstream like a refrain: they become FR-001, the first row of the rate-limiting contract's config table, and an assertion in a test sketch. A scenario is done when the person writing the test needs to make no further decisions. Contrast the anti-examples: "Then the system is secure" cannot be coded against; "Then authentication failures are handled appropriately" names no observable outcome. Both fail the gate's rule that requirements are testable and unambiguous. Write Then-clauses that a test could assert tomorrow. Transition: what about what you genuinely don't know yet? -->

---

## Bounded clarification

- Drafts may mark `[NEEDS CLARIFICATION: …]`
- The gate requires zero remaining before planning
- Ask early, not often — 014 says "max 3 questions"
- Or record a default in Assumptions
- 014's defaults: 90-day retention, 1-hour tokens, ±30s TOTP

`.specify/templates/spec-template.md`, `specs/014-security-hardening/spec.md`

<!-- NOTES: The template shows the marker in use: FR-006 authenticates users via `[NEEDS CLARIFICATION: auth method not specified]`. But the checklist's Requirement Completeness group requires that no markers remain before planning. Two resolution paths. `/speckit.clarify` runs before `/speckit.plan` on a deliberately small budget — 014's own Next Steps says "Run `/speckit.clarify` if clarifications needed (max 3 questions)". Or you document a default in Assumptions, which is how 014 settled 90-day log retention, 1-hour token expiry, and ±30-second TOTP tolerance. Honest footnote: the clarify command definition currently says up to five questions — a drift we return to. Transition: here are the gate's actual pass rules. -->

---

## The gate's pass rules

| Group | Sample rule |
|---|---|
| Content Quality | No implementation details |
| Requirement Completeness | No NEEDS CLARIFICATION remains |
| Feature Readiness | Scenarios cover primary flows |

All pass/fail. Cheapest place to stop a bad spec.

<!-- NOTES: Three groups, every item binary. Content Quality: no implementation details, user-value focus, readable by non-technical stakeholders. Requirement Completeness: no unresolved markers, testable and unambiguous, success criteria measurable and technology-agnostic, scenarios and edge cases defined, scope bounded, dependencies and assumptions identified. Feature Readiness: every FR has acceptance criteria, scenarios cover primary flows, no implementation leakage. "Checklists are bureaucracy" is exactly backwards: this is the last cheap moment before you spend an entire autonomous implementation loop on a spec with a hole in it. Transition: tasks, and why paths matter so much. -->

---

## Tasks cite exact file paths

- Template: "Include exact file paths in descriptions"
- A fresh session does not know your layout
- `AGENTS.md`: "Do not invent file paths… Grep the repo"
- "Update the backend" forces a guess or a waste
- A path makes the first action a grep that **confirms**

`.specify/templates/tasks-template.md`, `AGENTS.md`

<!-- NOTES: Why is a path mandatory? Because a fresh agent session has no idea how your project is arranged, and the repo's own anti-hallucination rule forbids inventing structure: "Do not invent file paths, function names, route paths, commands, URLs, or identifiers. Grep the repo before referencing." A task like "update the backend" forces the agent either to guess — which is how hallucinated endpoints happen — or to burn budget rediscovering layout. A task naming the file makes its first action a grep that confirms rather than invents. "Tasks can say 'update backend'" is the misconception to unlearn today. Transition: contracts, which exist for the same reason. -->

---

## Contracts are the seams between sessions

- Designed in one session, implemented in another
- They share no memory — only files
- Pin request/response shapes and error keys
- Pin key schemas and a test sketch
- Rate-limiting config row repeats US1's 5/5/15

`specs/014-security-hardening/contracts/rate-limiting.md`

<!-- NOTES: A contract is the interface between the session that designed the feature and the different session that implements it. Those two share nothing but the files on disk, so the seam must be written down: request and response shapes, error keys, Redis key schema, and a test sketch. In `contracts/rate-limiting.md`, the config table is where the spec's WHAT and the plan's HOW first meet — the same 5/5/15 numbers, now with per-IP scope and a key format attached. Miss the contract and the implementing agent invents the error keys, and your frontend never matches. Transition: the gate that keeps the plan honest. -->

---

## Constitution Check — and the Ralph loop

- "Must pass before Phase 0 research. Re-check after Phase 1"
- Forces the plan to walk each principle
- Violations must be argued in Complexity Tracking
- 014: seven principles, zero violations, empty table
- An agent completing ALL criteria can't afford ambiguity

`.specify/templates/plan-template.md`, `.specify/memory/constitution.md`

<!-- NOTES: An agent writing a plan will cheerfully violate your principles — skip E2E, add infrastructure nobody asked for — because it has not internalized them. The check forces the plan to walk each principle with a verdict and evidence, and any violation must be argued in the Complexity Tracking table, which the template says to fill ONLY if violations exist. 014: seven principles, seven verdicts, zero violations, empty table. Close the loop with Context A: an agent that must complete ALL acceptance criteria and cannot ask questions is safe exactly to the degree your artifacts are complete. The pipeline is the precondition for autonomy, not ceremony around it. Transition: now the honest change record. -->

---

## M4.3 — One PR per story

- Task file groups by story, tests first
- "Stop at any checkpoint to validate story independently"
- One story is reviewable in one sitting
- Demoable and revertable without collateral damage
- Tests-first phases make the PR self-evidencing

`.specify/templates/tasks-template.md`

<!-- NOTES: The task file is built for one-PR-per-story: tasks grouped by story, tests written first and failing, and a checkpoint after each — the template's line is "Stop at any checkpoint to validate story independently." A PR carrying exactly one story is reviewable in one sitting, demoable to a stakeholder, and revertable without dragging unrelated changes back out. This is not process for its own sake; it is what makes the Validation section short enough to be honest. Transition: and that section has a fixed shape. -->

---

## The PR body format

```text
Summary:       one line per change
Changed files: path: reason
Validation:    what you ran (commands and result)
Follow-ups:    known gaps, deferred work, open questions
```

`AGENTS.md` ("PR and commit format")

<!-- NOTES: Four sections, fixed. Summary names the change; Changed files gives path and reason; Validation records the commands you ran and their results; Follow-ups records known gaps, deferred work, and open questions. The rules behind it: run `make test-all` for every PR, there is no CI — all validation runs locally, so record commands, outcomes, limitations, and the pushed head SHA. Merge only after local validation and review are recorded and GitHub reports mergeable. And never "fabricate status checks, bypass protections, or treat missing evidence as success." A Validation section that records a failure is still evidence; "tests pass" with no command is not. -->

---

## Local code review

- `docs/ai-pr-review.md` supersedes the retired review gate
- Record head and base SHAs; inspect the full diff
- Correctness, security, org isolation, migrations, negative paths
- Findings need **severity** and **file/line**
- "Missing review is not approval" (`AGENTS.md`, rule 4)

`docs/ai-pr-review.md`

<!-- NOTES: The repo's review policy is itself a file, and it explicitly states Ollama is not a code-review provider — the former hosted gate is retired, do not recreate it. The checklist: record the PR head and base SHAs; inspect the complete diff with affected source, tests, and agent instructions; check correctness, security, organization isolation, authorization, API contracts, migrations, user workflows, and negative-path test coverage; report findings with severity and file/line references; fix blocking issues and re-review the final diff. Two hard lines: "Do not claim independent review when the builder performed the review itself," and AGENTS rule 4, "Missing review is not approval." Transition: now the part that surprises people — generated files lie. -->

---

## Drift case 1: the stale path

- `specs/000-user-onboarding/tasks.md` line 3:
- "Input: Design documents from `/specs/020-user-onboarding/`"
- The folder is `specs/000-user-onboarding`
- The feature was renumbered; the generator kept the old path
- Nothing failed. Nothing warned. It just sat there.

`specs/000-user-onboarding/tasks.md`

<!-- NOTES: Open the file and read line three: "Input: Design documents from `/specs/020-user-onboarding/`". The folder is `specs/000-user-onboarding`. The feature was renumbered at some point and the generated task file kept the stale path. Nothing failed, no test caught it, no warning fired — it just sat in a generated artifact waiting for an agent to follow a dead end. Everything in a spec folder is generated output: `/speckit.tasks` wrote that file, `/speckit.checklist` graded the other one. Generation is where hallucination risk concentrates, so generated artifacts deserve the same suspicion as generated code. Transition: two more, both inside the exemplar folder. -->

---

## Drift cases 2–3: count and directory

- Checklist prints "8 stories: 5xP1, 2xP2, 0xP3"
- The spec has **six** P1 stories — US1–4, US7, US8
- Same checklist then lists six P1 features
- Tasks assign migrations to `migrations/versions/…`
- No `migrations/` dir exists — migrations are in `alembic/versions/`

`specs/014-security-hardening/checklists/requirements.md`, `specs/000-user-onboarding/tasks.md`

<!-- NOTES: Case two: `specs/014-security-hardening/checklists/requirements.md` reports "8 prioritized user stories: 5xP1, 2xP2, 0xP3" — but the spec marks six P1 stories: rate limiting, audit logging, CSRF, session invalidation, input validation, password reset. The same checklist's notes then list those six while printing "5xP1". The 100% quality score did not catch it; only reading the checklist against the spec did. Case three: the onboarding tasks file assigns migrations to `migrations/versions/add_onboarding_tables.py`, and there is no `migrations/` directory — migrations live in `alembic/versions/`. Both files were generated, both were wrong. Transition: the repo already has the countermeasures. -->

---

## Countermeasures: grep, recount, open

- `AGENTS.md` step 6: search for stale commands and counts
- Anti-hallucination rule: grep the repo before referencing
- Recount every count against its source
- Never let a self-reported score replace opening the file
- Treat the spec folder as generated output, not gospel

`AGENTS.md` (operating loop step 6; anti-hallucination rule)

<!-- NOTES: The repo already has the rules that target this. Operating loop step 6: "Search for stale commands, counts, check names, and feature-state claims before declaring done." And the anti-hallucination rule: "Grep the repo before referencing." So the countermeasures are mechanical. Grep every path a generated file cites and confirm it exists — that catches case three. Recount every count against the source — that catches case two. And never accept a self-reported score as a substitute for opening the file, which is the habit that catches case one. In Lab M4 you run these on your own checklist. Transition: your turn. -->

---

## Lab M4 — Spec a Real Feature

**Goal:** a complete spec folder for one real feature.
**Pass gate:** a stranger implements story 1 with zero questions.
**Artifacts:** spec · research · data-model · plan · contract · checklist · tasks.
**Drift checks:** grep each path, recount each count.

`lab.md` · suggested feature: availability windows or invitation links

<!-- NOTES: The lab is 90 to 120 minutes and it is the whole module compressed into one deliverable. You will work in `specs/001-your-feature/` inside your own project, or extend SignUpFlow if you have no SaaS of your own — the instructor guide's default is a swap-requests feature. Seven artifacts, the same set we walked. Two things are graded unusually strictly: every task must name an exact file path that exists in your repo, and your checklist must survive your own drift checks — grep each cited path, recount each count. Then a peer or a fresh agent session tries story 1 with no context. Record what they asked. Transition: quiz next. -->

---

## Quiz M4

- 8 questions · 6 multiple choice, 2 short answer
- Artifact responsibilities · gate rules
- Task format · research decision format
- One question is the drift-check question

`quiz.md`

<!-- NOTES: Eight questions, mapping to the three segments. The distractors encode the misconceptions we taught against: that a spec may contain code, that "secure" is a testable Then-clause, that a task may name no file. Question 8 asks you to name the two countermeasure habits from `AGENTS.md` and say which drift case each would have caught — grep catches the nonexistent migrations directory, recounting catches the "5xP1" against six P1 stories. Answer key with objective references is at the end of the file. Transition: recap. -->

---

## Recap

- A command chain: each step consumes the last
- 014: 8 stories, 44 FRs, 12 criteria, 7 edge cases
- 8 research decisions, 6 contracts, 4,661 lines, no tasks.md
- One quality test: the stranger test
- Honest record: one PR per story; severity + file/line
- Generated artifacts drift — grep paths, recount counts

`lesson.md` · `specs/014-security-hardening/`

<!-- NOTES: Six lines to take away. The pipeline is a chain where each command consumes the previous file. The exemplar shows the set at scale: eight stories, 44 FRs, seven edge cases, twelve success criteria, eight research decisions, six contracts totaling 4,661 lines — and one honest gap, no tasks file. Quality has a single test, the stranger test, and the gate enforces its consequences. The change record is a format, not a feeling. And generated artifacts drift, so grep paths and recount counts before you cite anything. Transition: discussion prompt. -->

---

## Discussion prompt

> Feature I'd spec first: [one line]
> Artifact I was most tempted to skip: [artifact] → [what breaks]
> Hardest thing to make stranger-testable: [line]
> One drift check I now run: [grep or recount]

Then comment on one classmate's sharpest scenario.

`lesson.md`, "Discussion prompt"

<!-- NOTES: Post to the community with this template. The third line is the one that matters most — name the specific scenario, requirement, or task you had to sharpen, and say what was vague before. Then read two classmates' posts and comment on one with a single question: would their sharpest acceptance scenario let you implement without asking anything? That is the stranger test, applied to each other. That peer exchange is also how you satisfy the Lab M4 pass gate if you are in the self-paced tier. -->

