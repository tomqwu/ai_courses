# Agent-Executable Specs: The Checklist and the Drift Checks

The session that implements a story is rarely the session that designed it, and an autonomous agent cannot stop to ask you what you meant. This playbook is for the engineer or tech lead who hands features to coding agents. When you finish, you will have a spec folder that passes a pre-planning gate, a scripted "stranger test" proving a fresh agent session can build story 1 from the files alone, and a drift-check script that catches the stale paths, wrong counts and stale status lines that generated spec artifacts collect.

## The method

1. **Run the spec-kit loop, and make two optional gates mandatory.** Spec-kit 1.0's loop is "Constitution once per project; specify → plan → tasks → implement → converge per feature", and you "Repeat **implement → converge** until convergence reports **Converged**" (spec-kit README at v1.0.12, https://github.com/github/spec-kit, read 2026-09-26). Clarify, checklist and analyze are optional there: "Add clarification, checklists, and consistency analysis when you need extra quality gates." This playbook requires two gates the tool leaves optional: bounded clarification (step 3) and the requirements checklist (step 4). Command spellings differ by agent: dash-named skills such as `/speckit-specify` in Claude Code, dotted `/speckit.specify` in spec-kit's reference pages. Type whatever your `specify init` output lists.

2. **Write `spec.md` as WHAT, never HOW.** Prioritize user stories. Each one must be "INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them, you should still have a viable MVP" (`SignUpFlow/.specify/templates/spec-template.md:12-13`). Give each story an Independent Test line and Given/When/Then scenarios whose Then-clause a test author can assert with no further decisions: a number, an error key, an observable state. Phrase requirements "System MUST…" and name no language, framework, store or schema. Describe entities by "key attributes without implementation" (`SignUpFlow/.specify/templates/spec-template.md:100`).

3. **Mark unknowns, then resolve every one before planning.** While drafting, write `[NEEDS CLARIFICATION: …]` inline, as the template does (`SignUpFlow/.specify/templates/spec-template.md:95`). Resolve each marker by one of two routes. Either ask a bounded set of questions (the clarify command allows "up to 5", per `SignUpFlow/.claude/commands/speckit.clarify.md:2`; set a lower cap if you can), or record a default in an Assumptions section. After this step the spec must stand without you.

4. **Pass the requirements checklist before you plan.** Spec-kit's specify step writes `checklists/requirements.md` itself, with the stated purpose "Validate specification completeness and quality before proceeding to planning" (`SignUpFlow/.claude/commands/speckit.specify.md:72-80`; the same step exists in spec-kit 1.0.12's `templates/commands/specify.md`, read 2026-09-26). Three groups, every item pass or fail: Content Quality, Requirement Completeness, Feature Readiness. Three items decide whether an agent can execute the spec: no implementation details, no `[NEEDS CLARIFICATION]` left, requirements testable and unambiguous. The checklist grades itself, so recount it against the spec (step 8) before you trust a single tick.

5. **Let `plan.md` own HOW, behind the constitution gate.** Pin language, versions, storage and performance targets here. Walk every principle of your constitution with a verdict; the template's rule is "GATE: Must pass before Phase 0 research. Re-check after Phase 1 design." (`SignUpFlow/.specify/templates/plan-template.md:32`). Argue any violation in Complexity Tracking, which you "Fill ONLY if Constitution Check has violations that must be justified" (`SignUpFlow/.specify/templates/plan-template.md:97-99`). Tag every file `[NEW]` or `[MODIFY]`. A `[MODIFY]` file must exist today.

6. **Pin the seams in contracts, and write tasks a stranger can follow.** A contract carries request and response shapes, error keys, and a test sketch that repeats the scenario's numbers. Tasks use the format `[ID] [P?] [Story] Description`, and the template adds "Include exact file paths in descriptions" (`SignUpFlow/.specify/templates/tasks-template.md:17-20`). Order them Setup, Foundational, one phase per story with tests written first and failing, then Polish, with a checkpoint after each story.

7. **Run the stranger test.** Commit the folder. Open a fresh agent session on a clean clone, with no memory files and no chat history. Paste the stranger prompt from the template below. The agent implements story 1 alone and logs every question it would have asked and every assumption it made. Label each row spec-owed or environment-owed. **Pass = zero spec-owed rows.** On a fail, sharpen the artifact the row names and re-run in another fresh session.

8. **Run the drift checks after every generation step.** Run `drift-check.sh` (template below) on the folder after specify, after plan, after tasks and after converge. It exits 1 on an unresolved marker or a path whose parent directory does not exist, and prints the counts and status words you must reconcile by eye. Then do the one check no script can: take each numeric Then-clause and find the constant in the code that enforces it.

9. **Implement, converge, and still verify.** Converge reads `spec.md`, `plan.md` and `tasks.md` "as the **sole source of intent**", appends unmet work under `## Phase N: Convergence`, and must not modify the spec, the plan, existing tasks or code. It treats ticked boxes with suspicion: "completion claims are not evidence" (`templates/commands/converge.md` in spec-kit v1.0.12, read 2026-09-26). It is still an agent grading code against artifacts an agent wrote. "Converged" means the code matches the artifacts, not that the artifacts are right. Step 8 is how you check the artifacts.

## Template

**Story block for `spec.md`.**

```markdown
### User Story 1 - <verb + object> (Priority: P1)
<One paragraph: who does what, and why it matters.>
**Why this priority**: <what breaks without it>
**Independent Test**: <one action + one observable result, runnable with no other story built>

**Acceptance Scenarios**:
1. **Given** <state>, **When** <action>, **Then** <assertable outcome with a number or error key>
2. **Given** <state>, **When** <invalid action>, **Then** <rejected with `<error_key>`; nothing is stored>

- **FR-001**: System MUST <behaviour, with the same number as the scenario>.
- **SC-001**: <measurable outcome, technology-agnostic>.

## Assumptions
1. <default chosen instead of asking, with the value>
```

**The gate, `checklists/requirements.md`.** Every box is binary.

```markdown
## Content Quality
- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value; readable by a non-technical stakeholder
## Requirement Completeness
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable and technology-agnostic
- [ ] Edge cases identified; scope bounded; assumptions recorded
## Feature Readiness
- [ ] Every FR has acceptance criteria
- [ ] Counts stated here were recounted against spec.md: stories __, P1 __, FRs __
```

**A task line.** `- [ ] T004 [P] [US1] Test inverted window returns 409 in tests/api/test_availability.py`

**The stranger prompt.** Paste as-is into a fresh session; fill the two placeholders.

```text
You are implementing one user story from a written specification. You have NO access to
the author. Work only from the files under <SPEC FOLDER> in the repository at <REPO ROOT>.
1. Read spec.md, plan.md, data-model.md, research.md, contracts/ and tasks.md first.
2. Implement ONLY the tasks tagged [US1], in order, tests first. Stop at the first
   Checkpoint line after the US1 phase.
3. Do not ask me anything. When the folder does not give you something, log a QUESTION
   and make the most conservative choice. When you decide something the folder leaves
   open, log an ASSUMPTION.
4. Do not invent file paths, function names, routes, commands or identifiers. If a task
   names a path that does not exist, log a QUESTION; do not create a substitute.
5. Do not read git history, issues, or anything outside <REPO ROOT>.
6. Run the tests you wrote. Do not modify a test to make it pass.
When you stop, print this report and nothing after it. Number every item; use "none".

=== STRANGER REPORT ===
Story: <story 1 title>
Tasks attempted: <IDs>
Stopped because: <checkpoint reached | blocked at T0NN: reason>
## Built
<path — what it does>
## Acceptance scenarios
| # | Then-clause (copied) | Checked how | pass / fail / not checkable: why |
## Questions (Q)
Q1. <what you needed> — needed for: <task> — where I looked: <files>
## Assumptions (A)
A1. <what you decided> — instead of: <alternative> — needed for: <task>
## Counts
QUESTIONS: <n>  ASSUMPTIONS: <n>  SCENARIOS CHECKED: <passed>/<total>
=== END REPORT ===
```

Label every Q and A row. **Spec-owed:** the folder should have answered it (behaviour, data shape, error key, limit, ordering, permission, file placement, which test proves a scenario). **Environment-owed:** toolchain, credentials or machine. A "not checkable" scenario counts as spec-owed unless its reason is environmental. You may not relabel a row without naming the artifact whose job it is not.

**`drift-check.sh`.** Save at the repository root; run `bash drift-check.sh specs/NNN-feature`.

```bash
#!/usr/bin/env bash
# drift-check.sh SPEC_DIR -- run from the repository root. Exit 1 on a hard failure.
d="${1:?usage: drift-check.sh specs/NNN-feature}"
fail=0
echo "== 1. unresolved [NEEDS CLARIFICATION] markers (must be 0)"
n=$(grep -rn "NEEDS CLARIFICATION:" "$d" | wc -l | tr -d ' ')
echo "$n"; [ "$n" -eq 0 ] || fail=1
echo "== 2. technology words in spec.md (judge each hit: threat name or design choice?)"
grep -niE "redis|postgres|mysql|sql|fastapi|django|flask|react|kafka|jwt|docker" "$d/spec.md" || echo "none"
echo "== 3. counts to reconcile against checklists/requirements.md"
echo "stories: $(grep -c '^### User Story' "$d/spec.md")"
for p in P1 P2 P3; do echo "$p: $(grep -c "(Priority: $p)" "$d/spec.md")"; done
echo "FRs: $(grep -oE 'FR-[0-9]{3}' "$d/spec.md" | sort -u | wc -l | tr -d ' ')"
echo "== 4. repo paths cited in spec.md, plan.md, tasks.md"
for f in "$d/spec.md" "$d/plan.md" "$d/tasks.md"; do
  [ -f "$f" ] || { echo "absent: $f"; continue; }
  while read -r p; do
    { [ -e "$p" ] || [ -e "$d/$p" ]; } && continue
    if [ -d "$(dirname "$p")" ]; then echo "absent     $p  ($f)"
    else echo "NO-PARENT  $p  ($f)"; fail=1; fi
  done < <(grep -oE '(\.?[A-Za-z0-9_-]+/)+[A-Za-z0-9_.-]+\.[a-z]{2,4}' "$f" | grep -v '^specs/' | sort -u)
done
echo "== 5. stale status words (compare with what exists)"
grep -nE "PENDING|Not Started|IN PROGRESS|TBD" "$d"/*.md || echo "none"
exit $fail
```

Edit the technology list in check 2 to your stack. An `absent` line is fine for a file a task creates and drift for a file the spec says exists or a `[MODIFY]` tag names. Every `NO-PARENT` line is drift.

## Checklist

- [ ] Every story has an Independent Test line and runs without any other story built.
- [ ] Every Then-clause holds a number, an error key or an observable state.
- [ ] No FR or success criterion names a language, framework, store or schema.
- [ ] Zero `[NEEDS CLARIFICATION:` markers; each default is written in Assumptions.
- [ ] The requirements checklist passed before `plan.md` existed, with its counts recounted.
- [ ] `plan.md` has one verdict per constitution principle; violations argued in Complexity Tracking.
- [ ] Every `[MODIFY]` path exists; every `[NEW]` path has an existing parent directory.
- [ ] At least one contract carries shapes, error keys and a test sketch with the scenario's numbers.
- [ ] Every task names an exact file path and a `[US#]`; tests precede code; one checkpoint per story.
- [ ] A fresh-session stranger report for story 1 shows zero spec-owed rows; earlier failing reports kept.
- [ ] `drift-check.sh` exits 0, and every `absent` line is a file some task creates.
- [ ] Each numeric Then-clause of story 1 was found as a constant in the code, or logged as missing.

## Worked example from a real repo

SignUpFlow, a multi-tenant FastAPI scheduling SaaS, at commit c550d46. **It predates spec-kit 1.0.** It added spec-kit on 2025-10-20 (commit 2af939f) and still has the pre-1.0 layout: eight dotted command files in `SignUpFlow/.claude/commands/`, no converge step, and a documented order of specify, clarify, plan, tasks, analyze, implement (`SignUpFlow/docs/SPEC_KIT_SETUP.md:7-15`). Its analyze step compares artifacts with each other, not with the code (`SignUpFlow/.claude/commands/speckit.analyze.md:2`). Read it for the artifact shapes. The template rules quoted in this playbook are unchanged in 1.0.12's templates (checked 2026-09-26). Type the 1.0 names when you run spec-kit yourself.

**The folder.** `SignUpFlow/specs/014-security-hardening/` holds `spec.md`, `research.md`, `plan.md`, `quickstart.md`, six contracts and `checklists/requirements.md`, and no `tasks.md`. The plan still lists it as the next step (`SignUpFlow/specs/014-security-hardening/plan.md:334`). Story 1 is the model scenario: "fail authentication 5 times within 5 minutes, **Then** further login attempts are blocked for 15 minutes" (`SignUpFlow/specs/014-security-hardening/spec.md:30`). The same 5/5/15 reappears in FR-001 (`SignUpFlow/specs/014-security-hardening/spec.md:202`) and in the contract's config row (`SignUpFlow/specs/014-security-hardening/contracts/rate-limiting.md:26-28`). The checklist's purpose line names the gate's position: "before proceeding to planning" (`SignUpFlow/specs/014-security-hardening/checklists/requirements.md:3`). Its note says the defaults (1-hour token expiry, ±30-second TOTP tolerance) are "documented in Assumptions section" (`SignUpFlow/specs/014-security-hardening/checklists/requirements.md:27`). They are not. Both are written as requirements (`SignUpFlow/specs/014-security-hardening/spec.md:232`, `SignUpFlow/specs/014-security-hardening/spec.md:251`), and the Assumptions section holds other defaults (`SignUpFlow/specs/014-security-hardening/spec.md:350-359`). Harmless here, but the note is generated text that nobody checked.

**The drift, found with `drift-check.sh` (run 2026-09-26).**

- *A wrong count in a self-graded gate.* The checklist prints "8 prioritized user stories: 5xP1, 2xP2, 0xP3" and "Quality Score: 100%" (`SignUpFlow/specs/014-security-hardening/checklists/requirements.md:32`, `SignUpFlow/specs/014-security-hardening/checklists/requirements.md:44`). Check 3 prints `P1: 6`, `P2: 2`. The checklist's own note lists six P1 features beside the "5xP1" (`SignUpFlow/specs/014-security-hardening/checklists/requirements.md:36`).
- *Stale status words.* Check 5 finds `research.md`, `quickstart.md` and `contracts/` marked "(PENDING)" in the plan (`SignUpFlow/specs/014-security-hardening/plan.md:216-219`), yet all three exist in the folder.
- *Paths that do not exist.* The plan cites `.specify/templates/commands/plan.md` (`SignUpFlow/specs/014-security-hardening/plan.md:6`); that directory does not exist. The spec names the "existing authentication flow (api/core/security.py)" (`SignUpFlow/specs/014-security-hardening/spec.md:318`), and the plan tags the same path `[MODIFY]` (`SignUpFlow/specs/014-security-hardening/plan.md:260`). No such file appears anywhere in the repo's history; the JWT code lives in `SignUpFlow/api/security.py`. The plan also targets `frontend/js/security.js` (`SignUpFlow/specs/014-security-hardening/plan.md:174`), but the `frontend/` tree was deleted on 2026-05-05 (commit c47340e). The older onboarding spec shows the same decay at scale: check 4 prints 14 `NO-PARENT` lines for `SignUpFlow/specs/000-user-onboarding/`, including `migrations/versions/…` where the repo uses `alembic/versions/` (`SignUpFlow/specs/000-user-onboarding/tasks.md:40`), and its header still reads `/specs/020-user-onboarding/` (`SignUpFlow/specs/000-user-onboarding/tasks.md:3`).
- *A triage hit, not a verdict.* Check 2 flags ten lines in `spec.md`. Six name SQL injection, a threat the feature defends against. Three name the existing JWT system as a constraint. One is a design choice: the rate-limit store, "Use in-memory cache (Redis)", parked as an open decision dated "TBD (implementation phase)" (`SignUpFlow/specs/014-security-hardening/spec.md:380-383`). Judge each hit; do not just count them.

**Spec against code: the step no script does.** The spec folder says "Implementation Status: Not Started" (`SignUpFlow/specs/014-security-hardening/spec.md:428`), yet login limiting exists outside the planned locations. The plan's `[NEW] api/services/rate_limiter.py` (`SignUpFlow/specs/014-security-hardening/plan.md:243`) is absent. The limiter lives in `SignUpFlow/api/utils/rate_limiter.py`, where login allows 5 requests per 300 seconds (`SignUpFlow/api/utils/rate_limiter.py:246-249`), keyed per IP (`SignUpFlow/api/utils/rate_limit_middleware.py:79`). Two requirements have no counterpart. The production limiter is a fixed window with no lockout period (`SignUpFlow/api/utils/rate_limiter.py:108-120`), and a grep of `api/` for `lockout` finds nothing, so "blocked for 15 minutes" is unenforced. The 429 says "Rate limit exceeded. Please try again later." (`SignUpFlow/api/utils/rate_limit_middleware.py:95-98`), where FR-004 asks for the time until reset (`SignUpFlow/specs/014-security-hardening/spec.md:205`). The contract even contradicts itself: its table scopes the login lockout "Per IP" (`SignUpFlow/specs/014-security-hardening/contracts/rate-limiting.md:28`), its trigger section says "account-level, not IP-level" (`SignUpFlow/specs/014-security-hardening/contracts/rate-limiting.md:340`). A stranger given this contract would log that as a spec-owed question. That is the test doing its job.

The repo already states the rules that catch all of this: "Search for stale commands, counts, check names, and feature-state claims before declaring done" (`SignUpFlow/AGENTS.md:27`) and "Grep the repo before referencing" (`SignUpFlow/AGENTS.md:65`).

## Self-check

There is no script beyond the template's. Run two commands and score one table.

1. `bash drift-check.sh specs/NNN-feature; echo "exit=$?"` must print `exit=0`. Explain every `absent` line in writing.
2. The final stranger report for story 1 must show zero spec-owed rows, with every earlier report kept.

Then score yourself. **Pass = 70 or more, with rows A and F both passing.**

| Row | Criterion (pass or fail) | Points |
|---|---|---|
| A | Zero spec-owed rows in a fresh-session stranger report | 20 |
| B | Every Then-clause assertable with no further decision | 15 |
| C | No implementation detail in `spec.md` after judging each check-2 hit | 10 |
| D | Checklist counts match check 3's recount | 10 |
| E | Constitution verdict per principle; violations argued | 10 |
| F | `drift-check.sh` exits 0 | 15 |
| G | Every task names an exact path and a `[US#]`; tests first | 10 |
| H | Story 1's numbers found in code, or logged as missing | 10 |

Fabricated output fails the self-check outright: a report with edited counts, deleted rows, or a checklist ticked with no recount.

## Limits

- This playbook tests whether an agent can execute your spec, not whether the spec describes the right product. A folder can pass every check and still build the wrong feature.
- `drift-check.sh` is a triage tool. It over-flags technology words, cannot tell a file to create from a file claimed to exist, and parses only paths written with a directory. Tree diagrams escape it.
- The stranger test samples one story in one session. Another session may ask different questions. Passing on story 1 does not certify stories 2 to N.
- Converge and the checklist are generators grading generated work. Neither replaces your tests, a code review, or reading the diff.
- Nothing here covers security review, performance or migration safety.

## Sources

- Spec-kit README, and `templates/commands/specify.md`, `clarify.md`, `checklist.md` and `converge.md`, plus the spec, plan and tasks templates, at v1.0.12: https://github.com/github/spec-kit (read 2026-09-26).
- SignUpFlow at commit c550d46: `SignUpFlow/specs/014-security-hardening/spec.md`, `SignUpFlow/specs/014-security-hardening/plan.md`, `SignUpFlow/specs/014-security-hardening/checklists/requirements.md`, `SignUpFlow/specs/014-security-hardening/contracts/rate-limiting.md`, `SignUpFlow/specs/000-user-onboarding/tasks.md`, `SignUpFlow/.specify/templates/`, `SignUpFlow/.claude/commands/`, `SignUpFlow/docs/SPEC_KIT_SETUP.md`, `SignUpFlow/AGENTS.md`, `SignUpFlow/api/utils/rate_limiter.py`, `SignUpFlow/api/utils/rate_limit_middleware.py`.
- The stranger prompt and pass rule are condensed from the course file `course/03-content/m04-spec-driven-saas/stranger-prompt.md`.

This playbook is drawn from Module 4 of the AI Product Studio course.
