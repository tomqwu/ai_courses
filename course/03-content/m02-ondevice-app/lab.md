# Lab M2 — Build TinyCopilot's Core (Python + Ollama)
> Part of AI Product Studio (APS-3) · Pass/fail checkpoint for Module 2 · Companion lesson: `lesson.md`

## Goal

Build the working core of **TinyCopilot** — a multi-role AI copilot in Python that mirrors ListenToMe's architecture: a conversation store with a character-budgeted context window, a question detector with debounce, pure prompt builders for three roles, per-role model routing with local-first defaults, streaming Ollama calls with typed errors, and an orchestrator that wires roles to models with per-role cancellation. Lab M3 will later harden this same core with a fail-closed local-only mode, so do not break its tests.

## Prerequisites

- Module 1 complete (you have a starter repo with `constitution.md`, `AGENTS.md`, `specs/`, and an evidence log).
- Python 3.11+ on your PATH.
- Ollama installed and running, with one model pulled: `ollama pull qwen3:0.6b` (any small chat model works; note its name).
- The `tinycopilot/` reference repo in this module's folder.

## Time

~3 hours. The six modules average 25–30 minutes each when you let the tests drive.

## The starter

The `tinycopilot/` folder is a *reference implementation plus a full test suite*. Treat it with a specific discipline: **the tests are the spec, and the reference implementation is the answer key.** You will delete the six marked modules and re-implement each one TDD-style to green — reading the answer key when stuck is legitimate, copying it without running the tests is not. The Makefile runs everything:

- `make lab-m2` — runs this module's test suite and enforces the coverage floor (90).
- `make demo` — feeds a small canned transcript through all three roles with your real Ollama model.
- `make lab-m3` — the privacy tests Module 3 will build on. They must keep passing: your re-implementation must not change behavior the M3 tests pin down.

## Steps

1. Run `make lab-m2` before touching anything. Confirm the suite is green and the coverage floor passes. You are looking at the finished answer key — take ten minutes to read `src/tinycopilot/copilot.py` and see how the pieces connect before you delete them.
2. Delete the first module's implementation: `git rm src/tinycopilot/conversation_store.py` (all modules live under `src/tinycopilot/`; their tests are `tests/test_<module>.py`). Run `make lab-m2` and **capture the red output** in your evidence log — those failures are your spec.
3. Re-implement `conversation_store.py` from its test file (`test_conversation_store.py`): apply finalized vs partial segments, and `recent_context(max_chars)` keeping the newest segments that fit a character budget — always at least the newest one. Run `make lab-m2` until green.
4. Delete and re-implement `question_detector.py` from `test_question_detector.py`: trailing "?", leading interrogatives, word-boundary phrase cues. Include the debounce test — a burst of questions triggers at most once per window.
5. Delete and re-implement `prompts.py` from `test_prompts.py`: three base role prompts (anti-preamble Quick, never-invent Listener, depth-over-brevity Deep), the persona directive appended to every role, and the per-role user-message builder. These must be pure functions — no I/O.
6. Delete and re-implement `model_router.py` from `test_model_router.py`: token-prefix marker matching (no substring false hits — "gemini" must not match "mini"), role defaults (fast→Quick, strong→Deep, distinct fast→Listener), reuse when fewer models exist, and `:cloud` filtered out of local-first defaults.
7. Delete and re-implement `ollama_provider.py` from `test_ollama_provider.py`: streaming chat against `http://localhost:11434/api/chat` with an injectable transport (tests use a fake), NDJSON line parsing, and typed errors — in-stream `{"error": ...}`, truncated stream (no `done`), and empty stream (no content) must each raise a distinct error type, never return success.
8. Delete and re-implement `copilot.py` from `test_copilot.py`: the orchestrator that routes each role to its model, builds that role's prompt, streams the response, and — via a generation counter per role — cancels a stale stream when the role's model switches mid-flight (a switched model's predecessor must not write output).
9. Run the demo: `make demo`. It feeds a small transcript through all three roles against your pulled model. Capture the output — Listener summary, Quick suggestion, Deep answer.

## Acceptance checklist (all must be true)

- [ ] `make lab-m2` exits 0 after all six modules are re-implemented.
- [ ] Your evidence log shows a red run *before* each green run, for all six modules.
- [ ] `make lab-m3` (the pre-provided Module 3 privacy tests) still exits 0.
- [ ] The coverage floor passes at 90 (part of `make lab-m2`).
- [ ] `make demo` prints three distinct role outputs (Listener, Quick, Deep) from at least one real model.
- [ ] Your evidence log explains each module's test-first cycle in one or two sentences per module.
- [ ] The router tests prove distinct per-role models when ≥3 models exist and reuse when fewer exist.
- [ ] The provider tests prove truncated and empty streams raise typed errors and never finish as success.

## Evidence to record

For each module: the failing `make lab-m2` output after deletion, the passing output after re-implementation, and one sentence on what the tests specified that the prompt didn't. Then record the final full `make lab-m2` run (with coverage line), the `make lab-m3` run, and the complete `make demo` transcript with the model name visible. Use the course evidence format: commands, outcomes, date, environment, limitations.

## Stretch goals

- **Swift track (Mac only):** open the real ListenToMeCore files and map each Python module to its Swift counterpart — `conversation_store.py` → `Sources/ListenToMeCore/ConversationStore.swift`, `question_detector.py` → `QuestionDetector.swift`, `prompts.py` → `Prompt.swift`, `model_router.py` → `ModelRanking.swift` (+ `MeetingSession` routing), `ollama_provider.py` → `OllamaProvider.swift`, `copilot.py` → `MeetingSession.swift`. Write down two design decisions the Swift version makes that your Python version doesn't, and why.
- **Add a fourth role** (e.g., a "Critique" role): its own base prompt, default-model rule, dropdown, and tests. Follow the same red → green cycle.
- **Add a VAD-style segmentation heuristic** to the store: split a flat transcript blob into utterances using an RMS threshold and trailing-silence rule mirroring `Sources/ListenToMeCore/VAD.swift`, with tests proving each boundary fires exactly once.

## Discussion prompt

Post to the community: your `make demo` output, plus the answer to — which of the six modules had the biggest gap between "what I thought it should do" and "what the tests said it must do"? Use the template:

> **TinyCopilot M2 — [your name]**
> Demo output: [paste]
> Most surprising module: [module] — I expected [X]; the tests specified [Y] because [reason grounded in a ListenToMe file pointer].