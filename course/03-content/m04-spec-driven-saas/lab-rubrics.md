# Lab M4 — Grading Rubric

> Four levels: **Exemplary / Proficient / Developing / Missing**. Weights sum to **100**, stated per row,
> and each row names its evidence. Consistent with `01-design/assessment-and-rubrics.md` (labs 60%; Lab M4
> is a cohort deep-review lab).

## Group 1 — `spec.md` and clarification (steps 1–2) · 25

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Independently testable stories | 10 | ≥3 stories; each Independent Test line names an observable outcome and runs alone | 3 stories with Independent Test lines but one depends on another story | Fewer than 3 stories, or stories without Independent Test lines | One story or none | `spec.md`, `### User Story` sections |
| Numeric, assertable Then-clauses | 8 | Every Then-clause is numeric or an observable state change; a test author needs no decisions | Most Then-clauses assertable; one vague remainder | Several "works correctly" / "is secure" clauses | No Given/When/Then | `spec.md` acceptance scenarios |
| ≥8 FRs, technology-agnostic | 4 | ≥8 "System MUST…" FRs; `grep -iE "redis\|sql\|fastapi\|react"` returns nothing | ≥8 FRs, one incidental technology word | <8 FRs, or several FRs name a framework | FRs absent or mostly implementation | `spec.md`; the grep output |
| Unknowns resolved | 3 | Zero `[NEEDS CLARIFICATION]`; each default recorded in Assumptions | Zero markers; assumptions not recorded | A marker survives, or an unknown is silently dropped | Markers left and planning started anyway | `spec.md`; `grep -rn "NEEDS CLARIFICATION"` |

## Group 2 — Research, plan, contract (steps 3–4) · 30

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Decisions with rejected alternatives | 10 | ≥3 decisions, each with options, pros/cons, rationale, and a named rejected alternative | 3 decisions; one rejection stated but not reasoned | Decisions without alternatives ("we'll use X") | No `research.md`, or a list of preferences | `research.md`; each `## Decision` block |
| Constitution Check | 8 | One verdict line per principle of the student's own constitution, with evidence; violations argued | Verdict per principle, thin evidence; violations table empty | Some principles skipped, or one generic "all pass" line | No Constitution Check | `plan.md`; the student's Lab M1 constitution |
| Artifact-set judgment | 4 | Set complete; any absent artifact (e.g. `data-model.md`) justified in `plan.md` | Set complete, no justification for an unusual absence | A template artifact missing without mention | Multiple artifacts missing | `ls specs/001-*/`; `plan.md` |
| Contract seam | 8 | One contract with shapes, error keys, a key schema, and a test sketch asserting a scenario number | Contract has shapes and error keys; test sketch vague | Contract is prose with no shapes or error keys | No contract | `contracts/<seam>.md` |

## Group 3 — `tasks.md` and the gate (steps 5–6) · 30

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Task format and exact paths | 12 | Template format `[ID] [P?] [US#]`; every task names a path, each verified by `grep … \| xargs ls` | Format correct; most paths verified | Format roughly right; several tasks name no file | Tasks are prose bullets ("update the backend") | `tasks.md`; the verification transcript |
| Tests-first phases and checkpoints | 6 | Setup → Foundational → per-story phases; test tasks before implementation; a checkpoint per story | Phases present; one ordering slip | Phases present but no tests-first ordering | Ungrouped task list | `tasks.md` |
| Checklist gate, three groups | 4 | All three groups present and passed, each pass line dated | Three groups present; one item unmarked | Checklist is a single "passed" line | No checklist | `checklists/requirements.md` |
| Drift checks run on your own file | 8 | Student grepped every cited path **and** recounted stories/FRs/priorities against `spec.md`, recording both outputs | Both checks run; output summarized rather than pasted | One check run; the other asserted | Checklist self-graded with no commands recorded | Evidence log: the grep and recount outputs |

## Group 4 — Stranger test, the pass gate (step 7) · 15

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Stranger implements story 1 | 10 | A peer or fresh agent session implements story 1 with zero questions the folder should have answered; transcript recorded | One or two questions, both genuinely outside the folder's scope | Several questions the folder should have answered | No stranger test attempted | Transcript, or the stranger's session log |
| Residual questions and sharpening | 5 | Each residual question names the artifact that starved it; sharpened line shown before/after | Questions listed; one artifact sharpened | Questions listed, artifacts unchanged | No record | Evidence log; the edited artifact |

## Auto-fail conditions

These fail Lab M4 **regardless of the other rows** (per `01-design/assessment-and-rubrics.md`, fabrication
is the only fail):

1. **Fabricated evidence** — any grep transcript, checklist output, or stranger session not produced by
   the commands or person it claims.
2. **A cited path that does not exist and was left unfixed** — including the real `migrations/versions/`
   drift when the repo uses `alembic/versions/`.
3. **A self-graded checklist with no drift-check output** — "all checks passed" with no grep or recount
   recorded.
4. **No `tasks.md`** — the folder cannot be stranger-tested without it, so the pass gate cannot be met.
5. **Implementation leakage left in `spec.md`** after the gate ran — languages, frameworks, or schema SQL.
6. **Unresolved `[NEEDS CLARIFICATION]` markers** while planning or tasks were produced anyway.

## Scoring

Sum the weights of rows graded Proficient or better. **Pass = 70 or above, no auto-fail, and Group 4 not
Missing** — the stranger test is the module's pass gate. For self-paced students the evidence log is the
submission.
