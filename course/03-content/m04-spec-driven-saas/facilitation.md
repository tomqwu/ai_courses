# Facilitation Kit — M4 Live Session (90 minutes)

> Week 4 workshop per `02-instructor/instructor-guide.md`: "spec one feature live from student
> suggestions; run the checklist gate on it." Formula: **I do / We do / You do ≈ 25 / 35 / 30**.
> Pointers marked **[SIG]** resolve in the `SignUpFlow/` clone (a sibling of `course/` in the workspace root).

## Timing table

| Min | Activity | Mode | Artifacts |
|---|---|---|---|
| 0–2 | Opening hook: the 4,661 lines and the missing tasks file | I do | `specs/014-security-hardening/` **[SIG]** |
| 2–7 | Walk the command chain and the folder's six items | I do | `docs/SPEC_KIT_SETUP.md` **[SIG]** |
| 7–15 | Read US1 aloud; follow 5/5/15 into the contract table | I do | `spec.md`, `contracts/rate-limiting.md` **[SIG]** |
| 15–22 | Run the checklist gate on screen — then find the wrong count | I do | `checklists/requirements.md` **[SIG]** |
| 22–25 | Frame the We-do: pick the feature, name the artifacts | I do | whiteboard |
| 25–45 | Spec one feature live from student suggestions | We do | shared screen / doc |
| 45–55 | Draft three Given/When/Then and three FRs together | We do | shared doc |
| 55–60 | Fail the checklist gate deliberately, then fix the spec | We do | checklist draft |
| 60–75 | Breakouts: stranger-test one group's `tasks.md` | You do | breakout rooms |
| 75–85 | Reports: stranger questions + one drift find | You do | community thread |
| 85–90 | Close: the four lines you post tonight | I do | `lesson.md` prompt |

## Opening hook (2 min)

"SignUpFlow has seventeen spec folders. `specs/014-security-hardening/` has eight user stories, 44
functional requirements, seven edge cases, twelve success criteria, eight research decisions, and six
contracts totaling 4,661 lines. It has no `tasks.md` — and its own plan says so, in a Next Steps line that
still reads 'Phase 2: Run `/speckit.tasks`'. Today you produce the same folder for your own feature, and
you do the thing nobody did for those generated files: you check them against their source."

## Close (5 min)

"Three sentences before you go. One: the spec folder is not documentation, it is the instruction set for
an agent that cannot ask you anything. Two: the gate is cheap and self-graded, so you are the gate — grep
its paths, recount its counts. Three: post tonight using the discussion template in `lesson.md`: the
feature you'd spec first, the artifact you were tempted to skip and what breaks downstream, the hardest
thing to make stranger-testable, and one drift check you now run. That post is the lab's completion lever."

## Breakout instructions

- **Groups of four.** Roles: **Spec author** (owns the folder), **Stranger** (implements story 1 from
  `tasks.md` alone, no explanations allowed), **Drift hunter** (greps every cited path, recounts every
  count), **Scribe** (captures questions and the before/after line).
- **Time:** 12 minutes working, 3 minutes writing the post. Groups choose one group member's spec folder
  from Lab M4, or — if none exists yet — build a 10-line `tasks.md` skeleton for a shared feature.
- **Exact prompt:** "Stranger: attempt story 1 using only the files. Every time you need something the
  folder doesn't answer, write the question down and stop — do not ask the author. Drift hunter: run
  `grep -rn "app/" tasks.md | …` style checks and `grep -rn "NEEDS CLARIFICATION"`; report the first path
  that does not exist and the first count that disagrees with `spec.md`."
- **One deliverable to post:** the artifact line **before and after** sharpening, plus the stranger's
  question list — including "zero questions" as a valid, strong result.

## Discussion prompts

1. **"Which artifact would you skip, and what breaks downstream?"**
   Probe: "Name the artifact that consumes the one you skipped." Strong answer names a concrete
   consumption edge — skipping `research.md` leaves the plan with preferences instead of decisions, so
   contracts can't cite why a library was chosen.
2. **"What does 'secure' mean in a Then-clause?"**
   Probe: "Write the assertion." Strong answer replaces the adjective with numbers and an observable state
   change, in the shape of 014's US1 (5 failures / 5 minutes / 15-minute block).
3. **"How would you have caught the stale `/specs/020-user-onboarding/` path?"**
   Probe: "What command, run when?" Strong answer: grep every path a generated file cites during the
   checklist step — not after review — and treats generated artifacts as untrusted output.
4. **"Is a self-graded 100% checklist evidence?"**
   Probe: "What would make it evidence?" Strong answer: no — evidence is the diff between the checklist's
   claims and `spec.md`; 014 printed "5xP1" beside six P1 stories and still scored 100%.

## Watch-fors (aligned with the instructor guide)

| Stall | Symptom | 30-second intervention |
|---|---|---|
| Implementation leakage (guide: "M4: spec wants to include code") | `spec.md` naming Redis, SQLAlchemy, FastAPI | "Read the gate's first rule aloud, then move that line to `plan.md`; the spec keeps WHAT only." |
| No SaaS of their own (guide: writer's block) | Sitting idle, no feature | "Extend SignUpFlow itself — spec a swap-requests feature; the folder is cloned and the templates are right there." |
| Self-graded checklist passed instantly | All boxes checked, no commands run | "Show me one grep output and one recounted number; until then the checklist is a claim, not a check." |
| Untestable Then-clause | "Then it works correctly" | "Write the assertion as if you were the test author — if you'd need a decision, the scenario isn't done." |
| Tasks without a file path | "Update the backend and add tests" | "Grep the repo, name the file, put it in the task; `AGENTS.md` forbids inventing paths." |

## Post-session checklist

- [ ] Record attendance, the live-spec artifact, and every drift find in the cohort log.
- [ ] Post the session recording, the whiteboard spec, and the two drift examples to the community.
- [ ] Pin the top three stuck points from this session with their unblocks.
- [ ] Note for the next workshop: which gate rule students misread most (drives the We-do next week).
- [ ] Remind the cohort that the Lab M4 stranger test may be a classmate — that peer exchange satisfies
      the pass gate in the self-paced tier.
