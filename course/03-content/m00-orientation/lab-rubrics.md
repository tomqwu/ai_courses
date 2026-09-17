# Lab M0 — Grading Rubric

> Lab M0 is a pass/fail checkpoint inside the course's lab component (labs 60% / quizzes 20% /
> capstone 20%, `course/01-design/assessment-and-rubrics.md`). The percentages below are Lab M0's internal
> weights (100 points). A student passes the lab at **Proficient or better on every weighted row and no
> auto-fail condition**; those points then count in the lab component. The pass gate is the solver
> summary block plus a non-empty `ollama list`. The TinyCopilot suite is a "Before Module 1" stretch
> item: recorded, not weighted here — it is Lab M2's gate.

**Four levels.** *Exemplary* = complete, self-verified, shows judgment. *Proficient* = complete
and correct as shipped. *Developing* = attempted, incomplete, or unverified. *Missing* = absent or
fabricated.

## Group A — Environment proven (lab steps 1–3, 30 points)

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Three case-study repos present locally | 10 | All three sibling checkouts; student states why local copies matter for pointers | `ls -d ListenToMe SignUpFlow ai_qe` prints all three | One or two cloned; others read on the web | None local | Pasted `ls` output |
| Python interpreter is in the course band | 8 | Shows both `python3 --version` and which interpreter Poetry resolved | `python3 --version` prints 3.11–3.13 | Version outside band reported as "close enough" | Version not reported | Command + output, same line |
| Ollama model present, and labeled local vs `:cloud` | 12 | Distinguishes weights-on-disk from cloud-backed aliases and explains what a `localhost` URL does *not* prove | `ollama list` shows ≥1 model; each entry labeled local or `:cloud` | Model pulled or alias present, but the suffix is not explained | No model or no `ollama list` output | `ollama list` output + one-sentence labeling |

## Group B — First ship-win: the solver (lab step 4, 40 points)

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| `make setup` completes | 10 | Student notes the Python band check (`SignUpFlow/Makefile`, `check-python`) passing | Setup reaches "Setup complete" or the solver runs afterwards | Setup failed and the failure line is described, not quoted | Setup never attempted | Command + final output lines |
| Workspace initialized | 8 | Names all three generated YAML files | `init my-church` output shows `org.yaml`, `people.yaml`, `events.yaml` | Workspace created but output not captured | `init` skipped | `init` output |
| Solver summary captured with health score | 22 | Full block plus the date, the SignUpFlow commit it ran at, and a note on which fields vary by machine | Full block as the run printed it: `Workspace:`, `People: 5`, `Events: 2`, `Mode:`, the `Health score:` line, `Violations:`, `Fairness:`, and `Solution saved to my-church/output/solution.json` (at the 2026-09-16 head: `0.0/100`, `2 hard, 0 soft`, `stdev=0.50`; older revisions printed `100.0/100`) | Only the health-score line, or a paraphrase of the block | No solver output, or a number not produced by a run | Full pasted summary block |

## Group C — Evidence log and first-win post (lab step 5 + "Before Module 1", 30 points)

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Evidence log entry | 15 | Dated entry, verbatim outputs, and one line on what remains unverified | Solver block and `ollama list` pasted with the date | Outputs pasted with no date, or summarized instead of verbatim | No log entry | Evidence-log excerpt with date |
| First-win community post | 15 | All three parts, plus a specific archetype choice and a stated non-goal | Solver block with health score + labeled `ollama list` + one archetype sentence | Post missing one of the three parts, or no post yet | Post contains outputs no command produced | Permalink or screenshot of the post |

## Stretch — TinyCopilot acceptance gate ("Before Module 1", not weighted)

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Suite run reported honestly | — | `201 passed`, coverage `100%`, and student notes the 90% floor is enforced by `--cov-fail-under` (`tinycopilot/Makefile`) | `201 passed` with coverage `100%`, or the exact missing package plus the exact error line | "All tests pass" with no summary, or a named-but-vague missing dependency | Claims green with no summary, or a summary not from a run | Pytest summary line, or the exact error text |

Record the result in the evidence log; grade it in Lab M2, where `make lab-m2` is the gate.

## Auto-fail conditions (fail Lab M0 regardless of other rows)

1. **Fabricated output** — a hand-edited health score, an invented pytest summary, or a pasted block
   that no command produced (`course/01-design/assessment-and-rubrics.md`: fabrication is the only automatic
   fail).
2. **Green claimed without a summary** — asserting "tests pass" (for the TinyCopilot stretch) with no
   pytest summary line anywhere in the evidence.
3. **Health score without a run record** — the score appears but no workspace summary and no
   `Solution saved to …` line, so nothing shows the solver actually wrote a file.
4. **Local claimed for a `:cloud` alias** — labeling a cloud-backed alias as local, or asserting no
   data leaves the machine while only aliases are present.
5. **Real tenant data used** — running `init`/`solve` against a real organization's people or events
   instead of the sample workspace.

A missing community post is *Developing* on its row, not an auto-fail: chase it (it is the completion
lever, `course/02-instructor/instructor-guide.md` §1), but grade the evidence.

## How to distinguish a real pass from a plausible fake

Ask one question: **"Show me the line before and the line after."** Real solver output has a workspace
header above the score and a `Solution saved to …` line below it; real pytest output has a collection
count and a coverage table. A fabricated paste is usually one cherry-picked line — and a `100.0/100`
pasted from an old README is one too: at the current head the sample workspace does not score 100.
Then ask for the command that produced it; a student who ran it can reproduce it live in under a minute.