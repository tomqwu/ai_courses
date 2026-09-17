# Video Scripts — M1, The AI Product Operating System

> One script per segment. Pacing target is **~130 words per minute** of finished narration; the stated
> budget is the spoken-word ceiling. Record at 1920×1080, font ≥18 pt.

## M1.1 — Govern agents with a constitution and rule files

**Target runtime:** 9 minutes · **Word budget:** ~1,170 words at 130 wpm.

**Cold open (0:00–0:15).** Here is a rule an agent cannot follow: "be careful with multi-tenancy."
Careful is not an action, and it is not a check. This segment gives you the stack that replaces it —
four files, under two hundred lines each, where every rule a stranger can verify.

| Timestamp | On screen | Narration |
|---|---|---|
| 0:15 | Four files side by side | SignUpFlow governs every agent with four files. The baseline, `AGENTS.md`, is 188 lines and is consumed by Codex CLI, Cursor, Aider, Jules, OpenHands, Sourcegraph Amp, and Factory. Claude Code does not read it natively, so `CLAUDE.md` links to it and adds addenda. Copilot needs its own restatement. |
| 1:30 | `SignUpFlow/.specify/memory/constitution.md` | Above them sits the constitution — 85 lines, the single source of truth. Four principles: Native First, Test-Driven Implementation, Simplicity and YAGNI, and Safety and Reliability. Safety is concrete: email and SMS disabled by default, and payments mocked or disabled locally. |
| 3:00 | "Autonomy Configuration" | The constitution also fixes autonomy. "YOLO Mode: DISABLED." "Git Autonomy: ENABLED (Commit changes when done)." An agent may commit finished work, and may never run unchecked destructive commands. `AGENTS.md` adds the decisive line: when unsure whether an action is reversible, stop and ask. |
| 4:00 | House-style contrast in `AGENTS.md` | Now the house style, and this is the sentence to write down: each rule must be verifiable — "Filter every query by org_id," not "Be careful with multi-tenancy." A filter is executable and checkable; careful is a feeling. The same file caps every instruction file at about two hundred lines, because a rule file an agent cannot hold in context is one it will not follow. |
| 5:30 | Hierarchy list in `AGENTS.md` | When rules overlap there is a five-level hierarchy: the user's request, repository rules, path-scoped rules, general strategy guidance, then inferred best practice. One tie-breaker handles conflicts: follow the more specific and safer one. Memorize that sentence. |
| 6:30 | Anti-hallucination section | Then the rules your agents need most. Do not invent file paths, function names, routes, commands, or identifiers — grep the repo before referencing. For schema fields and environment variables, read the canonical source; do not recall from memory. When a request is ambiguous, present two or three differentiated options rather than guessing. |
| 7:30 | `docs/research-log.md`, then `AGENTS.md` | Finally, how rules graduate. A new rule does not go straight into `AGENTS.md`. The observation lands in `docs/research-log.md`, the file that exists so exploratory notes never become silent rules. It is tested on one real change, then promoted. Rules earn their place the way features do. |
| 8:30 | Module 1 objective slide | So: one canonical source, short files, verifiable rules, five-level precedence, grep before you claim, and a graduation pipeline. That is governance. |

**Demo cue.** Terminal and editor, no slides. Run `wc -l` on all four files in the clone, then open
`AGENTS.md` and let the viewer read the house-style contrast. Notice: the constitution is the shortest
file and the most authoritative one.

**Action-step close (8:45).** Draft three rules for your own starter repo — one constitution principle,
one baseline `AGENTS.md` rule, one dated research-log observation from Module 0. Rewrite anything that
fails the test: could a stranger check whether it was followed?

**Recording notes.**
- Enlarge the `wc -l` output; the line counts are the proof.
- If over time, reduce beat 4:00 to one sentence — the contrast table is on the slide.
- Do not say the constitution "enforces" anything automatically; agents read it, it is not compiled.
- Do not claim the four files cover every AI tool; `AGENTS.md` names the list it serves.

## M1.2 — Spec → plan → tasks an agent can execute

**Target runtime:** 10 minutes · **Word budget:** ~1,300 words at 130 wpm.

**Cold open (0:00–0:15).** You do not tell an agent "build the feature." You hand it a folder of
artifacts so complete that a fresh session, with no memory of your conversation, can execute one task
line and be right. This segment is that folder.

| Timestamp | On screen | Narration |
|---|---|---|
| 0:15 | `SignUpFlow/docs/SPEC_KIT_SETUP.md` | SignUpFlow builds features through spec-kit slash commands in a fixed order: constitution, specify, clarify, plan, checklist, tasks, analyze, implement. Each step writes a file, and the files — not the chat — become the interface between your intent and the agent's execution. Seventeen spec folders exist in the repo. This is a working habit, not an admired template. |
| 1:30 | `specs/014-security-hardening/spec.md` | Each artifact has one job. `spec.md` is the WHAT, technology-agnostic: prioritized stories P1, P2, P3, each independently testable, with Given/When/Then acceptance scenarios, edge cases, and success criteria. The test of a spec is whether you could build the smallest story alone and ship something real. |
| 3:00 | `specs/014-security-hardening/research.md`, `plan.md` | `research.md` holds numbered decisions with options evaluated, rationale, and rejected alternatives. `data-model.md` fixes entities before code exists. And `plan.md` is the HOW, behind a gate: "GATE: must pass before Phase 0 research. Re-check after Phase 1 design." That gate is a Constitution Check — each principle gets an explicit verdict. This is where a plan that quietly breaks YAGNI gets caught. |
| 4:45 | `specs/014-security-hardening/checklists/requirements.md` | Then the pre-planning quality gate. The checklist forbids implementation details — no languages, frameworks, APIs — forbids remaining `[NEEDS CLARIFICATION]` markers, and requires testable, unambiguous requirements. Spec 014's own checklist confirms the split: the spec describes capabilities without specifying HOW, with technology choices deferred to planning. |
| 6:00 | `specs/019-sms-notifications/tasks.md` | Finally `tasks.md`, the executable list: checkbox tasks in ID, parallel, story format, with exact file paths and tests written first. Here is a real line: "T027 [US1] Implement POST /api/sms/send endpoint per contracts/sms-api.md in api/routers/sms.py." File to touch, contract to follow, order of work — nothing left to ask. |
| 7:00 | Write the worked example live | Watch a story become executable. Story: as a volunteer, I can block dates so the solver skips me. Scenario: given Sarah has a blocked-date period covering 2026-04-23, when an admin runs the solver for that week, then Sarah receives no assignment and the solution reports zero hard violations. That is measurable. Then the task names the router, the contract, and the test file to write first. |
| 8:15 | `ListenToMe/docs/superpowers/specs/2026-06-18-listentome-design.md` | ListenToMe runs the same discipline in Swift. Its design spec pins protocol-level interfaces — `AudioCapturing`, `Transcribing` — with exact signatures, so implementations stay swappable. It writes down non-goals: no cloud backend, accounts, billing, multi-user, and no covert mode. Its plan is a 2,410-line TDD task list that ends by mapping every spec bullet to tasks. |

**Demo cue.** Open the spec 019 task line and the spec 014 gate, then convert the volunteer story into a
scenario and a task line in a blank editor while the viewer watches. Notice: the scenario has a date and
a measurable outcome; the task has a path.

**Action-step close (9:30).** Pick one feature you actually want to build, any archetype. Write the
story in one sentence with a priority, one Given/When/Then scenario, and one task line citing exact
file paths you will create.

**Recording notes.**
- Keep the artifact table on screen through beats 1:30–6:00 so name maps to job.
- If over time, compress the ListenToMe beat to the non-goals only.
- Do not say spec 014 is incomplete; say plainly it has no `tasks.md`, as the deep-read records.
- Say "seventeen spec folders" only after the segment shows the `ls`.

## M1.3 — Evidence discipline: validation as a record, not a feeling

**Target runtime:** 10 minutes · **Word budget:** ~1,300 words at 130 wpm.

**Cold open (0:00–0:15).** A green badge tells you a suite passed. It does not tell you what command
ran, on what environment, against which revision, or what was never tested. This segment replaces the
badge with a record you can audit.

| Timestamp | On screen | Narration |
|---|---|---|
| 0:15 | Constitution validation policy | SignUpFlow runs no CI checks, and this is a deliberate, tested policy. The constitution says: "No CI checks. Run all code review, static analysis, migrations, tests, security scans and artifact validation locally. Record evidence for the pushed revision; never recreate hosted checks or require CI statuses." A policy-regression test guards the rule. |
| 1:30 | `SignUpFlow/tests/unit/test_local_validation_policy.py` | Read the argument, because it changes how you work. A hosted check is a pass-or-fail snapshot. It says nothing about the commands, the environment, or the limits of what you validated. SignUpFlow replaces it with something stronger: the evidence travels with the revision. Every PR records commands, outcomes, limitations, and the pushed head SHA. |
| 2:45 | `SignUpFlow/docs/playbooks/validation.md` | Here is the full-suite line from Module 0, and here is exactly where it lives — `docs/playbooks/validation.md`, not `TESTING.md`. Across backend, web, contract and browser suites: 1,464 passed, 21 skipped. Note the date, 2026-09-12, and that the file was demoted to historical reference on 2026-09-13. Follow-up validation starts from commit `cccc6f7`, pinning the evidence to a revision. |
| 4:15 | "Failures reproduced and repaired" | Now the hardest discipline: include the failures. A browser click race is recorded, and so is the fix — wait for HTMX settling before clicking its newly rendered Delete control. The document says it outright: "this initial failure is not omitted from the evidence." Deleting that paragraph would have made the record shorter and worthless. |
| 5:30 | The validation results table | Known debt is named as debt: "Full API mypy | Existing debt: 835 errors in 40 files; not a pass." And the record closes with limits: do not count manual operational drills, external delivery, PostgreSQL, DST, venue scheduling, or full tenant isolation as verified. An evidence record that cannot say "not verified" is not evidence. It is marketing. |
| 6:45 | `ListenToMe/AGENTS.md`, then the gap review | Done means verified in the shipped thing. ListenToMe's Definition of Done requires verifying behavior in the installed production app; for audio, actual system-audio transcription labeled OTHERS — "a permission toggle or microphone pickup is not proof." Its own gap review then recommends: do not promote the existing 1.3.0 DMG, despite 215 passing Core tests and 97.24% coverage, because those numbers do not establish capture reliability. Coverage tells you what you tested; only an honest record tells you what you shipped. |
| 8:15 | Blank file: the evidence template | Copy this template for every lab. A dated heading with project and feature. Commands with results. Environment. Revision from `git rev-parse HEAD`. Limitations, with at least one honest line. If a run failed and you fixed and re-ran, record both. The record that admits a failure is worth more than the badge that hides one. |

**Demo cue.** Open `docs/playbooks/validation.md`, read the mypy line aloud, then the limits paragraph,
then type the evidence template into a blank `docs/evidence-log.md` live. Notice: every number is
attached to a command, a date, or a SHA.

**Action-step close (9:30).** Write one evidence entry now for the Module 0 solver run or any command
you ran today: exact command, result line, environment, date, and at least one limitation.

**Recording notes.**
- Enlarge the mypy line and the limits paragraph; they are the emotional core.
- If over time, cut beat 1:30 to the snapshot-versus-record sentence.
- Do not call the no-CI policy reckless, and do not imply CI is always wrong.
- Do not re-date the evidence: 2026-09-12, historical as of 2026-09-13, exactly as the file states.
