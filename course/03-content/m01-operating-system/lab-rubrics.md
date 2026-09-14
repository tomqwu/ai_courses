# Lab Rubrics — M1 (Lab M1: Build Your Operating System)

> Labs are 60% of the course grade (`01-design/assessment-and-rubrics.md`). Lab M1 is pass/fail at the
> module checkpoint, self-verified with evidence in the self-paced tier and instructor-verified in the
> cohort tier. The four deliverable groups below sum to **100**. Every criterion is observable; "good
> understanding" is never a row. Exemplary is what a student could post as a public proof asset.

## Deliverable A — Governance files (30)

| Criterion | W | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Constitution is within cap, with ≥3 principles and an autonomy config | 10 | ≤80 lines; principles are project-specific (not copied); autonomy states YOLO and Git stances plus the "stop and ask" rule | ≤80 lines; ≥3 principles; autonomy present | Over 80 lines or principles are generic restatements | No constitution, or under 3 principles | `constitution.md` + `wc -l` output |
| `AGENTS.md` is within cap and carries a validation checklist | 10 | ≤200 lines; checklist items map to commands; scope notes split by topic rather than nested | ≤200 lines; checklist present | Over 200 lines, or checklist absent | No `AGENTS.md` | `AGENTS.md` + `wc -l` output |
| Every rule is imperative and verifiable | 10 | Three sampled rules each survive "what command proves it?" with no rewriting needed | Most rules survive; one or two need a rewrite | Rules are advisory ("be careful", "keep clean") | Rules are prose paragraphs with no imperative | The rule lines, quoted in the submission |

## Deliverable B — Spec folder (25)

| Criterion | W | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| `spec.md`: 2 independently testable stories, each with Given/When/Then | 10 | Concrete expected values (ids, titles, `done` flags); no technology named anywhere | 2 stories, ≥1 scenario each, technology-free | One story covers everything, or scenarios lack expected outcomes | No spec, or no acceptance scenarios | `specs/001-todo-command/spec.md` |
| `plan.md`: Constitution Check gate explicitly passed | 7 | Gate lists each principle with an explicit verdict, placed before the tasks | Gate present and checked | Gate quoted but not checked | No gate | `plan.md` |
| `tasks.md`: ≥5 tasks with exact paths, tests first | 8 | Every task names a real file; the test task precedes the code task for each story; an agent could start from any line | ≥5 tasks in `[ID] [P?] [Story]` format with paths | Tasks lack paths, or code precedes tests | No `tasks.md`, or fewer than 5 tasks | `tasks.md` |

## Deliverable C — The TDD loop (25)

| Criterion | W | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Red run captured before the green run | 12 | Failing output saved verbatim, dated, ordered before the passing run in the log | Red output present and precedes green | Red run mentioned in prose with no output | No red run | `docs/evidence-log.md` + saved terminal output |
| Green run exits 0 | 8 | `python3 -m pytest tests/ -q` exits 0 with all tests passing | Same command exits 0, count recorded | Tests pass on the student's machine but the command is not the recorded one | Suite does not pass | Command + exit code |
| Implementation matches the spec; tests were not weakened | 5 | Every acceptance scenario in `spec.md` has a corresponding test; no test edited to fit the implementation | Tests match the spec's scenarios | A scenario is untested, or a test assertion was loosened | Tests deleted or skipped to pass | Diff of `tests/test_todo.py` + `todo.py` |

## Deliverable D — Evidence and honesty (20)

| Criterion | W | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Evidence entry has all six fields | 10 | Commands, counts, date, environment, revision, and limitations all present, with the revision matching the actual head SHA | All six fields present | One field missing (usually limitations or environment) | No evidence entry | `docs/evidence-log.md` + `git rev-parse HEAD` |
| Failures and limits are included, not hidden | 6 | Failures appear in order with their fix; at least one limitation is specific ("CLI arg handling tested by hand, not automated") | One honest limitation named | Limitations field contains "none" | A failure visible in the output is absent from the record | Evidence entry vs. raw output |
| Research log and commit body | 4 | ≥1 dated observation from a real experience; commit body follows Summary / Changed files / Validation / Follow-ups | Both present, one imperfect | One present | Neither present | `docs/research-log.md`, `git log -1` |

## Auto-fail conditions

Regardless of other rows, the lab fails if any of these is true:

1. **Fabricated evidence** — a test count, output line, command, or head SHA that the recorded run does not produce.
2. **A green run with no red run recorded** — the TDD loop is the deliverable; the red output is its proof.
3. **Tests weakened to pass** — assertions loosened, tests deleted, skipped, or rewritten after failing to fit the implementation.
4. **No head SHA in the evidence record** — evidence that cannot be pinned to a revision is a claim, not a record.
5. **Placeholder brackets left in submitted files** — `[<your rule>]` still visible in `constitution.md` or `AGENTS.md`.
6. **A failure visible in the raw output but absent from the evidence entry** — selective recording is fabrication by omission.

Consistency note: this rubric grades Lab M1 only. The course-level split remains labs 60% / quizzes 20% /
capstone 20%, and the academic-honesty rule is the one real rule — using an agent is allowed and taught;
stating what the agent did and what you verified is required.
