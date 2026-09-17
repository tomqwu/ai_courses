# M2 Facilitation Kit — One 90-Minute Live Session

> Cohort week 2. Pre-work: M2 lessons watched, `make lab-m2` run once green, Lab M1 evidence posted.
> Read with `02-instructor/instructor-guide.md` (workshop formula, stuck points) and `lab.md`.

## Timing table

| Min | Activity | Mode | Artifacts |
|---|---|---|---|
| 2 | Opening hook: the 96% badge problem | I do | `slides.md` slides 1–2 |
| 20 | Repo tour + live-build `recent_context` TDD | I do | `ConversationStore.swift:56-67`, `test_conversation_store.py` |
| 12 | Token-prefix: predict the `gemini`/`mini` score | We do | `test_model_router.py` |
| 8 | Typed stream errors: red, then green | We do | `test_ollama_provider.py` |
| 28 | Breakout: TDD one assigned module to green | You do | Evidence-log entry |
| 12 | Share-out and debrief | We do | Breakout posts |
| 5 | Close and hand-off | I do | `lab.md` checklist |
| 3 | Buffer / parking-lot answers | — | — |

## Opening hook (2 min) — script

"ListenToMe is a real-time meeting copilot. It taps your microphone and the other participants'
system audio, transcribes live on-device, and streams AI help from a local model. It cannot run any
of that in CI. No microphone, no ScreenCaptureKit, no Ollama daemon. And it carries a 96% core
coverage badge with a 95% floor in `scripts/check-coverage.sh`.

So the question for the next ninety minutes is not *what did they build*. It is *where did they put
the decisions* so that 96% is honest? Type one sentence in chat: where do you think the decisions
live? Then we open the repo and check."

## I do (20 min) — repo tour and live build

Open the repo, not the slides. Walk the layout table in `tinycopilot/README.md`; name the Swift
counterpart of each module. Then build `recent_context` live, TDD:

1. Show `tests/test_conversation_store.py::TestRecentContext` and read the three assertions aloud.
2. Run `pytest tests/test_conversation_store.py -q` with the module deleted — it exits non-zero with
   `ModuleNotFoundError` in `conftest.py`.
3. Paste in the smallest wrong version: newest-first fit but no "always at least one" exception.
4. Run it; the over-budget test fails. Fix the guard live.
5. Run `pytest tests/test_conversation_store.py -q` → 15 passed.

Deliberately leave one mistake visible. Students learn recovery, not perfection.

## We do (20 min) — two prediction exercises

**Token-prefix (12 min).** On screen: `capability_score` with `gemini-2.0:12b` and `gemma-mini:12b`.
Ask for predictions in chat before running. Most students say both are fast. Run the test; Gemini
scores 12.0, gemma-mini scores −8.0. Then show `ModelRanking.swift:13-18` and name the rule:
token-prefix, not substring.

**Typed errors (8 min).** Open `test_ollama_provider.py` and ask which test would catch "returns
success on a truncated stream." Run it red by deleting the `saw_done` check, then restore. Land the
line: flicker is information, silence is a lie.

## Breakout (28 min) — You do

**Groups of 2 (driver and navigator; swap at 14 minutes).** Assign each pair exactly one module from:
`question_detector`, `prompts`, `model_router`, `ollama_provider`, `copilot`.
Do not assign `conversation_store` — it was built live.

**Exact prompt to post in the breakout channel:**

> Delete your assigned module (`git rm src/tinycopilot/<module>.py`). Run `make lab-m2` and paste the
> red output — it will be a `ModuleNotFoundError` and pytest will exit 4. Do not fix that by hand.
> Read `tests/test_<module>.py`; that file is the spec. Re-implement until
> `pytest tests/test_<module>.py -q` is green, then run `make lab-m2` and `make lab-m3`.

**One deliverable per group, posted before the share-out:** the red output, the green output with its
test count, and one sentence naming something the test specified that the prompt did not. The
expected green counts: question_detector 32, prompts 38, model_router 40, ollama_provider 18,
copilot 17.

## Discussion prompts (12 min share-out)

1. **"The mock-LLM tests feel pointless — when do we use the real model?"** Probe: "What would a real
   model test actually assert — text, or protocol?" Strong answer: unit tests own protocol and
   decisions; the real daemon is a contract test (`make e2e`, `LAB_E2E=1`); ListenToMe's 96% comes
   from mockable seams, not from a model in CI.
2. **"Why not point the strongest model at all three panes?"** Probe: "What does that cost on the
   Quick pane?" Strong answer: Quick fires on a hotkey and proactively, so latency is the product;
   the per-pane dropdown makes model choice a visible budget, not a hidden default.
3. **"Our daemon only has `:cloud` aliases. Am I blocked?"** Probe: "What does local-first do when no
   local model exists?" Strong answer: no — auto-selection falls back to cloud only with no local
   model; M3 is where that distinction becomes the privacy lab.
4. **"`lab.md` says Listener gets a distinct fast model, but our tests reuse Quick's pick. Which is
   right?"** Probe: "Which artifact does the lab declare authoritative?" Strong answer: the tests are
   the spec (`lab.md` §The starter); the bullet describes the Swift `ModelRanking`, and the Python
   reference returns the same fastest model for Listener and Quick. Flag it; do not chase it.

## Watch-fors

| Stuck point | Symptom | 30-second intervention |
|---|---|---|
| Red run misread | "I got an ImportError, not failures — did I break it?" | "Correct. `__init__.py` re-exports the module, so collection fails. Exit 4 is your red run; the test file is your spec." |
| `gemini` mismatch | Router returns a cloud or wrong model | "Print the token list for the name. Is `mini` a token, or part of `gemini`?" |
| Truncated-stream success | Provider test passes but demo prints half a line | "Did the stream see `done: true`? If not, you must raise, not return." |
| Distinct-listener prose | Pair edits `role_defaults` to match `lab.md`, tests go red | "Tests are the spec. Revert to the reference shape; note the discrepancy in your log." |
| Mock tests feel fake | "When do we use the real model?" | Point at `make e2e` and the M3 lab; unit tests are the 90%. |
| Nothing to run against | `ollama list` shows only `:cloud` | "Valid environment. Pull `qwen3:0.6b`, or run `make demo --mode cloud`." |

## Close (5 min) — script

"Three numbers from today. One: 201 tests, 100% coverage, floor 90 — that is your M2 gate. Two: 49
tests in `make lab-m3`; your re-implementation must not break them. Three: the red run is exit 4, an
ImportError, and it is real evidence — not a fabricated '201 failed.'

Before Thursday: finish all six modules, capture six red runs and six green runs, and run `make demo`
once with the model name visible. Post your demo output in the lab thread with the template in
`lab.md`. Next week we red-team a cloud alias and watch `verify_local_model` fail closed."

## Post-session checklist

- **Record as evidence:** each group's red output, the green test count, the one-sentence spec gap,
  and the breakout question that produced the best answer.
- **Grade:** Lab M1 evidence this week; Lab M2 + Quiz M2 next week (per `instructor-guide.md` §2).
- **Post to the community:** a pinned summary with the four discussion answers, the exit-4
  explanation, and the `gemini`/`mini` prediction surprise; plus a reminder of the `make lab-m3` gate.
