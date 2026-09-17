# Video Scripts — M4

> Three segments, each **5 minutes** at ~130 words/min (≈650 words). Total file ≈ 15 min.
> Narration is written to be read aloud. Every file pointer shown on screen is also announced verbally.
> Pointers marked **[SIG]** resolve in the `SignUpFlow/` clone (a sibling of `course/` in the workspace root).

## M4.1 — The artifact pipeline in full

**Runtime:** 5:00 · **Word budget:** 650

**Cold open (0:00–0:15).**
SignUpFlow has seventeen spec folders. One of them is four thousand six hundred and sixty-one lines of
contracts, eight research decisions, forty-four requirements — and no task list at all. Here is why that
is not a mistake.

| Time | On screen | Narration |
|---|---|---|
| 0:15 | Terminal: `ls specs/014-security-hardening/` | Open the folder. Six items: `checklists`, `contracts`, `plan.md`, `quickstart.md`, `research.md`, `spec.md`. No `tasks.md`. That absence is real, and it is instructive. |
| 0:45 | `docs/SPEC_KIT_SETUP.md` **[SIG]** | The commands chain: specify, clarify, plan, checklist, tasks, implement. Each consumes the last one's output. Nothing rides in anyone's head. |
| 1:20 | `specs/014-security-hardening/spec.md`, US1 **[SIG]** | Read US1 aloud: fail authentication five times within five minutes, blocked for fifteen. Six P1 stories, forty-four FRs, twelve success criteria — and not one technology named. |
| 2:00 | `research.md`, Decision 1 **[SIG]** | Eight decisions, identical anatomy: decision, options, rationale, implementation. Decision one picks Redis and says in-memory is lost on restart and not shared across instances. |
| 2:35 | `plan.md` Constitution Check **[SIG]** | The gate line: must pass before Phase 0 research, re-check after Phase 1. Seven principles, seven verdicts, zero violations. |
| 3:05 | `contracts/rate-limiting.md`, config table **[SIG]** | Six contracts, 4,661 lines. First row: login, five minutes, five attempts, per IP, fifteen-minute lockout — the same numbers as US1, now with a scope. |
| 3:40 | `checklists/requirements.md` **[SIG]** | The gate: three pass/fail groups and a 100% score. Hold that number; segment three shows a count in this file that is wrong. |
| 4:10 | `specs/000-user-onboarding/tasks.md`, T017 **[SIG]** | The missing artifact's real format, from the template and from line 66: T017, parallel, story one, a method in `api/services/onboarding_service.py`. |
| 4:40 | `plan.md`, Next Steps **[SIG]** | And the gap is documented: 014's plan still says "Phase 2: Run `/speckit.tasks`." Nothing hides it. |

**Demo cue.** Keep one terminal and one editor pane. Open each file for real; do not show screenshots.
Point at the six-number refrain 5/5/15 as it recurs. **Viewer should notice:** each artifact ends where
the next begins, and the missing tasks file is stated rather than papered over.

**Action-step close.** Open the repo, run `ls specs/` — seventeen folders — then count 014's stories,
FRs, edge cases, and success criteria yourself. Post which artifact you would skip and what breaks.

**Recording notes.**
- Enlarge the US1 text and the contract config table; they are the two proof shots.
- If over time, cut the quickstart mention — it has no beat of its own.
- Do not state the exact contract line total from memory; read it off `wc -l`.
- Do not call 014 incomplete without also showing the plan's Next Steps line.

## M4.2 — Spec quality: the stranger test

**Runtime:** 5:00 · **Word budget:** 650

**Cold open (0:00–0:15).**
Imagine handing your spec folder to a competent engineer, then leaving the building for a week. No Slack,
no questions. If they cannot finish, the folder failed — not they.

| Time | On screen | Narration |
|---|---|---|
| 0:15 | `.specify/memory/constitution.md`, Context A **[SIG]** | This is not a thought experiment. The constitution defines the Ralph loop: started by `ralph-loop.sh` or a prompt saying implement spec, the agent picks the highest-priority incomplete spec, completes all acceptance criteria, and reports. It has no history and cannot ask. |
| 0:50 | Two columns: WHAT vs HOW | So spec.md owns WHAT — user-visible behavior — and plan.md owns HOW. The gate's first rule is literally "No implementation details." Schema lives in data-model and migrations. |
| 1:30 | `spec-template.md`, entities line **[SIG]** | Entities are described "without implementation." That separation also lets research overturn a lean without touching a requirement: 014's spec leans in-memory, research picks Redis, and the requirement never moves. |
| 2:05 | `spec-template.md`, independently testable **[SIG]** | Each story must be independently testable — implement one and you still have a viable MVP. Every 014 story carries its own Independent Test line. |
| 2:40 | `spec.md` US1 scenario **[SIG]** | Numbers, not vibes. Five, five, fifteen becomes an FR, a contract row, and a test assertion. "Then the system is secure" is not a scenario; it is a wish. |
| 3:10 | `spec-template.md`, NEEDS CLARIFICATION **[SIG]** | Drafts may mark unknowns, but the gate requires none remaining. Ask early: 014's own next steps cap clarification at three questions. Or record a default in Assumptions. |
| 3:40 | `checklists/requirements.md`, three groups **[SIG]** | Three pass/fail groups: content quality, completeness, readiness. This is the cheapest place to stop a spec that would waste a whole autonomous loop. |
| 4:10 | `tasks-template.md` and T017 **[SIG]** | Tasks cite exact paths because `AGENTS.md` forbids inventing them: do not invent paths, function names, or identifiers — grep before referencing. A path turns the agent's first action into a confirming grep. |
| 4:40 | `contracts/rate-limiting.md` **[SIG]** | Contracts exist because sessions do not share memory. Pin shapes, error keys, and a test sketch at the seam. |

**Demo cue.** Split screen: WHAT column and HOW column, moving one line at a time. **Viewer should
notice:** every rule traces back to the stranger — none is process decoration.

**Action-step close.** Trace US1 end to end: scenario, FR-001–FR-004, research Decision 1, the plan's
`[NEW]` and `[MODIFY]` lines, the contract config table. Post the trace and flag where language went vague.

**Recording notes.**
- Spell the pointer `specs/014-security-hardening/spec.md` aloud while showing it.
- If over time, cut the entities beat; the WHAT/HOW rule carries it.
- Do not say the clarify command caps at three — the spec's Next Steps says three, the command file says
  up to five. Say both, as the lesson does.

## M4.3 — From tasks to PR: the honest change record

**Runtime:** 5:00 · **Word budget:** 650

**Cold open (0:00–0:15).**
Three of SignUpFlow's own generated files are wrong. A stale path, a wrong count, and a directory that
does not exist. All three passed review, because nobody read them against their source.

| Time | On screen | Narration |
|---|---|---|
| 0:15 | `tasks-template.md`, checkpoint line **[SIG]** | One PR per story. The template groups tasks by story and puts a checkpoint after each: stop at any checkpoint to validate the story independently. |
| 0:45 | `AGENTS.md`, PR and commit format **[SIG]** | Four sections: Summary, Changed files with a reason per path, Validation with commands and results, Follow-ups. Fixed shape, no free-form prose. |
| 1:20 | `AGENTS.md`, PR rules **[SIG]** | Run `make test-all` for every PR; there is no CI, so record commands, outcomes, limitations, and the pushed head SHA. Merge only after local validation and review are recorded. Never fabricate status checks or treat missing evidence as success. |
| 1:55 | `docs/ai-pr-review.md` **[SIG]** | The review policy is a file: Ollama is not a code-review provider. Record head and base SHAs, inspect the full diff, check security, organization isolation, migrations, negative paths; report findings with severity and file and line. |
| 2:30 | `docs/ai-pr-review.md`, line 21 **[SIG]** | Two hard lines. Do not claim independent review when the builder performed the review itself. And AGENTS rule four: missing review is not approval. |
| 3:00 | `specs/000-user-onboarding/tasks.md`, line 3 **[SIG]** | Drift one. Line three says design documents come from `specs/020-user-onboarding`. The folder is `specs/000-user-onboarding`. The feature was renumbered; the generated file kept the dead path. |
| 3:40 | `specs/014-security-hardening/checklists/requirements.md` **[SIG]** | Drift two. It prints "five times P1" — while the spec marks six P1 stories, and the same checklist's notes list all six. The 100% score missed it. |
| 4:15 | `tasks.md` migrations tasks **[SIG]** | Drift three. The tasks file writes migrations into `migrations/versions/`. No such directory. Migrations live in `alembic/versions/`. |
| 4:40 | `AGENTS.md`, step 6 **[SIG]** | Countermeasures already in the repo: search for stale commands, counts, and feature-state claims before declaring done; grep the repo before referencing. Grep every path, recount every count. |

**Demo cue.** Grep live: `grep -n "migrations/versions" specs/000-user-onboarding/tasks.md`, then
`ls migrations` and `ls alembic/versions`. **Viewer should notice:** the failures are boring and
mechanical, and so are the fixes.

**Action-step close.** Open the onboarding tasks file and diff T022–T024 against US1's scenarios in its
spec. Post whether those lines alone let a fresh agent implement story 1, and the exact grep you would now
run on your own task files.

**Recording notes.**
- Do not paraphrase the quotes; read them off the file.
- Enlarge the drift lines — they are the segment's whole payload.
- If over time, cut the PR-format beat's narration and leave the block on screen.
