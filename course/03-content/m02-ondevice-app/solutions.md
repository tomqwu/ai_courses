# Lab M2 — Solutions & Reference Answers

> Companion to `lab.md`. The tests are the spec; `src/tinycopilot/` is the answer key. Commands run
> from `course/03-content/m02-ondevice-app/tinycopilot/`.

## 0. Baseline and the shape of the red run (Steps 1–2)

`make lab-m2` runs `pytest tests -m "not e2e" --cov=src/tinycopilot --cov-fail-under=90 -q`. Verified:

```
201 passed, 2 deselected in 0.13s
Required test coverage of 90% reached. Total coverage: 100.00%
```

Total **460 statements, 0 missed** across the eight source files.

**Step 2 is the step students misread.** Deleting a module does not produce failing tests; it produces
a *collection error*, because `src/tinycopilot/__init__.py:8-34` re-exports all six modules and
`tests/conftest.py:13` imports `TranscriptSegment`. Deleting `conversation_store.py` gives:

```
tests/conftest.py:13: in <module>
    from tinycopilot.conversation_store import TranscriptSegment
E   ModuleNotFoundError: No module named 'tinycopilot.conversation_store'
```

pytest exits **4** and runs zero tests. The other five deletions give the same shape (from
`__init__.py`, or `copilot.py:16-17` for `ollama_provider` and `prompts`) — all exit 4. Record that as
the red run; the test file holds the per-test spec. After a stub imports, red is assertion-level: a
budget-ignoring `recent_context` yields `13 failed, 2 passed`.

Per-file counts: conversation_store **15**, question_detector **32**, prompts **38**, model_router
**40**, ollama_provider **18**, copilot **17** (160, plus `test_privacy.py`'s **31** = 201).
**Grading note:** a "201 failed" red run is fabricated; the honest one is an ImportError, exit 4.

## 1. `conversation_store.py` (Step 3, 15 tests)

**Reference.** `TranscriptSegment` is a frozen dataclass normalizing `source` to lowercase and
rejecting anything else; `labeled()` returns `"Others: text"`. `ConversationStore` keeps `_finals`
plus one `_partial`; `apply` appends finals and clears a partial with the same `id`.
`recent_context(max_chars=4000)` rejects non-positive budgets, walks finals-plus-partial newest-first
charging `len(line)+1`, breaks when the next line would exceed the budget unless nothing is chosen,
then reverses. `transcript_text()` joins finals only.

**Expectations.** `max_chars=200` over six 60-char lines returns 3 lines starting `Others: line-03`;
a 5000-char segment survives `max_chars=100`; `DEFAULT_CONTEXT_CHARS == 4000`.

**Wrong answers.** (1) Partials appended to `_finals` — `test_partial_is_kept_separate_from_finals`
fails; display state treated as the log. (2) Same-id final does not clear its partial. (3)
Oldest-first fit, or dropping everything when the newest exceeds the budget — the never-empty
guarantee fails.

**Grading:** ask for the over-budget case; a real pass keeps the newest segment and says why.

## 2. `question_detector.py` (Step 4, 32 tests)

**Reference.** `INTERROGATIVES = ("what","why","how","when","where","who","whose","which")`,
`PHRASE_CUES = ("can you","any thoughts","walk me through","what do you think")`,
`DEFAULT_DEBOUNCE_SECONDS = 8.0`. `is_question` is False on empty, True on trailing `?`, True when the
first `[a-z]+` token is in `INTERROGATIVES`, else `\b<cue>\b` over the string. `should_fire` requires
final **and** `others` **and** detection, then blocks while `now - last_fired < debounce_seconds`.

**Expectations.** "however", "whatsapp", "many thoughts", "we cannot use your laptop" are False. A
fire at t=0 blocks t=3, allows exactly t=8.0; a non-question at t=2 does not move the window.

**Wrong answers.** (1) `cue in text` substring matching — "many thoughts" fires; missing `\b`.
(2) Prefix tests like `startswith("how")` — "however" fires. (3) Updating `_last_fired` on every call
— `test_non_questions_do_not_reset_the_window` fails. (4) `<=` instead of `<` — the exactly-8 s test
fails.

**Grading:** run the five near-miss parametrizations; substring implementations fail them all.

## 3. `prompts.py` (Step 5, 38 tests)

**Reference.** `LISTENER_CONTRACT` is one constant embedded verbatim in the Listener prompt.
`SYSTEM_PROMPTS` holds three distinct strings (Quick: "No preamble", "1-3 short sentences"; Listener:
four sections; Deep: "depth over brevity"). `build_system_prompt` appends `"Persona guidance: ..."`
then `"Always respond in <lang>."` to every role, in that order. `build_user_prompt` starts `Task: `,
preferring `action.instruction`, then the question, else `ROLE_TASKS[role]`, and ends with context or
`(no transcript yet)`. `ResponseAction` has ≥6 members with distinct instructions.

**Expectations.** Three distinct base prompts; `persona in prompt` and `prompt.startswith(base)` for
all roles; index order base < persona < language.

**Wrong answers.** (1) Persona appended only to Quick — the all-roles test fails; that is the bug
`systemWithDirectives` prevents. (2) Paraphrasing the contract — `LISTENER_CONTRACT in listener` plus
`count == 1` fails; constant and prompt must not drift. (3) Swapped persona/language order. (4) Any
clock, I/O, or randomness — determinism fails.

**Grading:** diff a student's three system prompts; if any two match, they missed the role split.

## 4. `model_router.py` (Step 6, 40 tests)

**Reference.** `_parse_params` matches `(\d+(?:\.\d+)?)\s*([tTbBmM])` (T×1000, B×1, M×0.001), else
0.0. `_has_cue` matches a whole token from its start. `capability_score` = name params (else
metadata) + 20×boosts (pro/reason/coder/max) − 20×demotes (flash/mini/lite/small). `rank_models` sorts
by `(-score, name)`. `is_local` rejects `:cloud` names and remote fields; `is_chat_model` accepts
empty capabilities or `completion`. `role_defaults` prefers the local subset and returns
`{"listener": fastest, "quick": fastest, "deep": strongest}` — `{}` when empty.

**Expectations.** `capability_score("gemini-2.0:12b") == 12.0` but `"gemma-mini:12b" == -8.0`; boosts
52.0, demotes 12.0; `"qwen3"` 0.0, `"qwen3.6:35b-a3b-coding-mxfp4"` 35.0. **Spec discrepancy:**
`lab.md` Step 6 and its checklist say Listener gets a *distinct* fast model, but the executable spec
returns the same fastest model for Listener **and** Quick even with three or more models. `lab.md`
declares the tests authoritative; implement to them and flag the prose.

**Wrong answers.** (1) `"mini" in name` — `gemini-2.0:12b` scores −8.0; the exact false hit
token-prefix matching exists to reject. (2) Parsing bare numbers — `"qwen3"` becomes 3.0.
(3) Not filtering `:cloud`/remote models. (4) Auto-picking embedding-only models.

**Grading:** ask for the two `gemini` scores; only token-prefix matching yields 12.0 and −8.0.

## 5. `ollama_provider.py` (Step 7, 18 tests)

**Reference.** `ServerError`, `IncompleteStreamError`, `EmptyResponseError` under `LLMError`.
`Transport` is `Callable[[str, dict|None], tuple[int, Iterator[str]]]`. `stream_chat` is a generator
posting `{"model","messages","stream":True}` plus options to `/api/chat`; raises `ServerError` for 3xx
(refusing redirects) and ≥400; skips blank/malformed/non-dict lines; raises `ServerError` on any
`{"error": ...}` event; sets `saw_done` on `done: true`; yields non-empty `message.content`; wraps a
mid-stream exception as `IncompleteStreamError("connection lost ...")`; then raises
`IncompleteStreamError` without `done` and `EmptyResponseError` when the joined deltas are whitespace.

**Expectations.** Deltas pass through; the payload carries `stream: True` and merges
`think`/`temperature`; `done=False` raises `IncompleteStreamError`; whitespace-only raises
`EmptyResponseError`; the default transport uses `follow_redirects=False`.

**Wrong answers.** (1) Returning success when no `done` event arrived — the most important failure,
and gap G06's shape. (2) Ignoring an in-stream `{"error": ...}` after HTTP 200. (3) Counting `" "`
deltas as content. (4) `follow_redirects=True`, letting transcript text be forwarded.

**Grading:** delete the `saw_done` check and ask what the suite does; a real pass names
`IncompleteStreamError` immediately.

## 6. `copilot.py` (Step 8, 17 tests)

**Reference.** `CopilotRole` is `listener`/`quick`/`deep`. `set_model` bumps the role's generation then
replaces its provider. `generate` takes the token **eagerly** (`_generations[role] + 1`), builds the
system prompt with persona/language, prepends the completed Listener summary for non-Listener roles,
and passes `{"think": False, "temperature": 0.0}` for Quick only. `_stream_answer` re-checks
`_generations[role] != token` before each yield and commits the summary only for a current Listener
generation.

**Expectations.** After one delta, `set_model(QUICK, ...)` makes `list(stream) == []` while Listener's
model is untouched; a second `generate` cancels the first; Quick's payload has `think is False` and
`temperature == 0.0`, Listener's has no `think` key; an in-flight summary never reaches a Quick prompt.

**Wrong answers.** (1) Taking the token lazily at first `next()` — a newer `generate` no longer
cancels the older stream. (2) Bumping the generation in `set_model` but never checking it in the loop.
(3) Injecting the live `listenerSummary` instead of the completed one. (4) Committing a summary for a
cancelled Listener.

**Grading:** ask for both halves of cancellation — the bump *and* the guard; one without the other is
a plausible fake.

## 7. Step 9 — `make demo`

Runs `demo.py` against `http://localhost:11434`. On a daemon holding `qwen3:0.6b` plus `:cloud`
aliases, the router chose `LISTENER qwen3:0.6b`, `QUICK qwen3:0.6b`,
`DEEP qwen3.6:35b-a3b-coding-mxfp8`, and `demo.py` printed three labeled blocks: a four-section
Listener summary, a Quick answer, and a Deep answer. The text varies by model; what must match is exit
0, three distinct role headers with model names visible, and no `[generation failed]` line. On a
`:cloud`-only daemon use `make demo --mode cloud`; both environments are valid.

## 8. Self-check table

| Criterion | Self-verification |
|---|---|
| Six modules re-implemented | `make lab-m2` exits 0 |
| Red captured per module | Six ImportError captures (exit 4) in the evidence log |
| Coverage floor 90 | `make lab-m2` prints `Required test coverage of 90% reached` |
| Privacy tests preserved | `tests/test_privacy.py` unmodified; its 31 tests are inside `make lab-m2`'s 201 |
| Router matches the spec | `pytest tests/test_model_router.py -q` → 40 passed |
| Typed stream errors | `pytest tests/test_ollama_provider.py -q` → 18 passed |
| Cancellation proven | `pytest tests/test_copilot.py::TestSetModel -q` green |
| Demo ran on a real model | `make demo` transcript with model names visible |
