# Lab M0 — Grading Rubric

> Lab M0 is a pass/fail checkpoint inside the course's lab component (labs 60% / quizzes 20% /
> capstone 20%, `course/01-design/assessment-and-rubrics.md`). The percentages below are Lab M0's internal
> weights (100 points). A student passes the lab at **Proficient or better on every row and no
> auto-fail condition**; those points then count in the lab component.

**Four levels.** *Exemplary* = complete, self-verified, shows judgment. *Proficient* = complete
and correct as shipped. *Developing* = attempted, incomplete, or unverified. *Missing* = absent or
fabricated.

## Group A — Environment proven (lab steps 1–3, 25 points)

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Three case-study repos present locally | 8 | All three sibling checkouts; student states why local copies matter for pointers | `ls -d ListenToMe SignUpFlow ai_qe` prints all three | One or two cloned; others read on the web | None local | Pasted `ls` output |
| Python interpreter is in the course band | 7 | Shows both `python3 --version` and which interpreter Poetry resolved | `python3 --version` prints 3.11–3.13 | Version outside band reported as "close enough" | Version not reported | Command + output, same line |
| Ollama model present, and labeled local vs `:cloud` | 10 | Distinguishes weights-on-disk from cloud-backed aliases and explains what a `localhost` URL does *not* prove | `ollama list` shows ≥1 model; each entry labeled local or `:cloud` | Model pulled or alias present, but the suffix is not explained | No model or no `ollama list` output | `ollama list` output + one-sentence labeling |

## Group B — First ship-win: the solver (lab step 4, 30 points)

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| `make setup` completes | 8 | Student notes the Python band check (`SignUpFlow/Makefile`, `check-python`) passing | Setup reaches "Setup complete" or the solver runs afterwards | Setup failed and the failure line is described, not quoted | Setup never attempted | Command + final output lines |
| Workspace initialized | 6 | Names all three generated YAML files | `init my-church` output shows `org.yaml`, `people.yaml`, `events.yaml` | Workspace created but output not captured | `init` skipped | `init` output |
| Solver summary captured with health score | 16 | Full block plus the date and a note on which fields vary by machine | Full block: `People: 5`, `Events: 2`, `Health score: 100.0/100`, `Violations: 0 hard, 0 soft`, `Fairness: stdev=0.43`, `Solution saved to my-church/output/solution.json` | Only the health-score line, or a paraphrase of the block | No solver output, or a number not produced by a run | Full pasted summary block |

## Group C — TinyCopilot acceptance gate (lab step 5, 25 points)

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Suite runs from the correct folder with the right command | 7 | Shows `make lab-m2` and the equivalent `pytest tests -q` | Runs `make lab-m2` or `pytest tests -q` in `tinycopilot/` | Ran from the repo root; `tests` not found; then corrected | No run shown | Command + working directory |
| Gate result reported honestly | 18 | `191 passed`, coverage `100%`, and student notes the 90% floor is enforced by `--cov-fail-under` | `191 passed` with coverage `100%`, or — if a dependency is missing — the exact package named plus the exact error line | "All tests pass" with no summary, or a named-but-vague missing dependency | Claims green with no summary, or a summary not from a run | Pytest summary line, or the exact error text |

## Group D — Evidence log and first-win post (lab step 6 + evidence, 20 points)

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Evidence log entry | 10 | Dated entry, verbatim outputs, and one line on what remains unverified | Solver output, `ollama list`, and pytest summary pasted with the date | Outputs pasted with no date, or summarized instead of verbatim | No log entry | Evidence-log excerpt with date |
| First-win community post | 10 | All three parts, plus a specific archetype choice and a stated non-goal | Solver output with health score + `ollama list` + one archetype sentence | Post missing one of the three parts | No post | Permalink or screenshot of the post |

## Auto-fail conditions (fail Lab M0 regardless of other rows)

1. **Fabricated output** — a hand-edited health score, an invented pytest summary, or a pasted block
   that no command produced (`course/01-design/assessment-and-rubrics.md`: fabrication is the only automatic
   fail).
2. **Green claimed without a red or a summary** — asserting "tests pass" with no pytest summary line
   anywhere in the evidence.
3. **Health score without a run record** — the score appears but no workspace summary and no
   `Solution saved to …` line, so nothing shows the solver actually wrote a file.
4. **Local claimed for a `:cloud` alias** — labeling a cloud-backed alias as local, or asserting no
   data leaves the machine while only aliases are present.
5. **Real tenant data used** — running `init`/`solve` against a real organization's people or events
   instead of the sample workspace.
6. **No community post** — the lab's discussion prompt is the completion lever and one of the six
   acceptance-checklist items (`course/02-instructor/instructor-guide.md` §1).

## How to distinguish a real pass from a plausible fake

Ask one question: **"Show me the line before and the line after."** Real solver output has a workspace
header above the score and a `Solution saved to …` line below it; real pytest output has a collection
count and a coverage table. A fabricated paste is usually one cherry-picked line. Then ask for the
command that produced it; a student who ran it can reproduce it live in under a minute.
