# Lab M2 Rubric — Build TinyCopilot's Core

> Scores the M2 lab inside the course's 60% lab component (`01-design/assessment-and-rubrics.md`).
> This rubric totals **100 points** for Lab M2. Pass = 70 with no auto-fail and every acceptance
> checklist item in `lab.md` true. Observable criteria only; "evidence required" names what the
> student submits.

## A. Baseline and red-run capture (Steps 1–2)

| Criterion | Exemplary | Proficient | Developing | Missing | Weight | Evidence required |
|---|---|---|---|---|---|---|
| Baseline green observed | Captures counts *and* coverage table before deleting | Captures `191 passed`, 100% | Runs it, no capture | No baseline run | 5 | Terminal capture of `make lab-m2` before edits |
| Red run per module | Six captures, each labelled with module, command, exit code | Six captures, exit code implied | Fewer than six, or unlabelled | No red run, or red run after the fix | 10 | Six ImportError captures in the evidence log |

## B. Module implementations (Steps 3–8)

| Criterion | Exemplary | Proficient | Developing | Missing | Weight | Evidence required |
|---|---|---|---|---|---|---|
| `conversation_store` | 15 green; window guarantee explained in one line | 15 green | 12–14 green | <12 green | 10 | `pytest tests/test_conversation_store.py -q` |
| `question_detector` | 32 green; near-miss cases named | 32 green | 20–31 green | <20 green | 10 | `pytest tests/test_question_detector.py -q` |
| `prompts` | 38 green; notes why determinism matters | 38 green | 25–37 green | <25 green | 10 | `pytest tests/test_prompts.py -q` |
| `model_router` | 40 green; can explain the `gemini`/`mini` case | 40 green | 28–39 green | <28 green | 12 | `pytest tests/test_model_router.py -q` |
| `ollama_provider` | 18 green; all three error types distinguished | 18 green | 12–17 green | <12 green | 12 | `pytest tests/test_ollama_provider.py -q` |
| `copilot` | 17 green; cancellation plus grounding both traced | 17 green | 11–16 green | <11 green | 11 | `pytest tests/test_copilot.py -q` |

## C. Gates and demo (Steps 8–9)

| Criterion | Exemplary | Proficient | Developing | Missing | Weight | Evidence required |
|---|---|---|---|---|---|---|
| Coverage floor 90 | Green run shows `Required test coverage of 90% reached` | Floor passes | Floor reached by weakening tests | Floor fails or disabled | 5 | `make lab-m2` full output with coverage table |
| Privacy tests preserved | `test_privacy.py`'s 31 tests green inside `make lab-m2`, file unmodified, and the log notes they are Lab M3's parked-later reference | 31 green, file unmodified | Passes after editing `test_privacy.py` | Fails or tests deleted | 5 | `make lab-m2` output; `git diff` on `tests/test_privacy.py` |
| Demo run | Three labeled role blocks, model names visible, no failure line | Three role blocks with models | Fewer roles, or model name hidden | No demo run | 5 | `make demo` transcript pasted |

## D. Evidence and community (Step 2 onward)

| Criterion | Exemplary | Proficient | Developing | Missing | Weight | Evidence required |
|---|---|---|---|---|---|---|
| Evidence log | Per-module red→green plus one sentence on what the tests specified | Red→green captured per module | Partial or vague entries | Log absent | 3 | Evidence-log file, course format |
| Discussion post | Demo output plus a grounded "most surprising module" answer | Post with the `lab.md` template | Post missing the file pointer | No post | 2 | Community thread permalink |

## Auto-fail conditions

The lab fails regardless of score if any of these is true:

1. **Fabricated evidence** — output that does not match a real run (e.g. "191 failed" as the red run,
   or counts that contradict the recorded environment).
2. **No red run** — any of the six modules goes from the answer key to green with no deletion capture,
   or the red capture is dated after its green run.
3. **Tests weakened to pass** — edits to any `tests/test_<module>.py` assertion, or to the Makefile's
   `--cov-fail-under`, or to `tests/test_privacy.py`.
4. **Green by copying** — a byte-identical restore of the reference file with no test-first cycle and
   no evidence entry explaining what the tests specified.
5. **Coverage floor bypassed** — deleting or excluding modules from `--cov`, or skipping tests to
   raise the percentage.

## Grading notes

- Distinguish a real pass from a plausible fake by re-running `make lab-m2` yourself
  on the submitted tree; a copied implementation still passes, so the evidence log is what separates
  the two.
- The six module rows are deliberately near-equal: this lab grades the *loop*, not one clever module.
- A student who scores Proficient everywhere with a complete log passes; one Exemplary module does not
  compensate for four Missing ones.
