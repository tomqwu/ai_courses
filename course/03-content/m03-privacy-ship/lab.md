# Lab M3 — Harden, Prove, Position

> Time: ~3 hours · Pass/fail · Prerequisites: Lab M2 complete

## Goal

Take TinyCopilot from "works" to "trustworthy and shippable." You will add a fail-closed local-only mode and red-team it with your own tests, run a real-LLM contract test outside CI, wire a coverage floor into your test target, and produce a sourced comparison table that doubles as your positioning statement. Everything ListenToMe proves in Swift, you prove in Python.

## Prerequisites

- **Lab M2 done:** the `tinycopilot` unit suite is green, including `OllamaProvider` with an injectable transport (the seam this lab depends on).
- **Ollama running** at `http://localhost:11434` with at least one model installed.
- **Note — your daemon decides Step 1's flavor.** Many machines' Ollama daemons have only `:cloud` aliases pulled. The lab uses this: if your daemon has a local model like `qwen3:0.6b`, local-only mode accepts it; if it has only `:cloud` aliases, local-only mode rejects everything. **Both are valid lab outcomes — record which you hit.** The second case is the red-team scenario from Segment M3.1 happening for real; do not "fix" it by weakening your checks. (Step 2's contract test is unaffected: it runs in the provider's default mode, on whatever chat model the router picks.)

## Step 0 — Park the shipped solution (~5 min)

`tinycopilot/` ships with this lab's answer already in it: `src/tinycopilot/privacy.py`, `tests/test_privacy.py`, and `tests/test_contract_real_llm.py` are the reference, and the Makefile's coverage floor is already wired. Start from a tree that does not contain its own answer:

1. From `course/03-content/m02-ondevice-app/tinycopilot/`, run `make m3-start`. It moves those three files into `.m3-solution/` (git-ignored) and rewrites the Makefile's `COV_FLOOR ?= 90` to `0`.
2. Run `make lab-m3` — it is now **red**, and not with failing tests: `src/tinycopilot/__init__.py:28-34` re-exports five names from `privacy`, so `tests/conftest.py` cannot import the package (`ModuleNotFoundError: No module named 'tinycopilot.privacy'`, pytest exit 4). **Record that output** — it is the first red of this lab, the same shape as Lab M2's deletions.
3. `make m3-restore` puts the reference back and resets the floor to 90 (it refuses while your own versions of the three files exist — move them aside first). Use it to compare implementations at the end, not to skip the lab.

## Step 1 — Privacy hardening, TDD-style (~60 min)

Write the red-team test **first**, watch it fail, then implement. Your first move is a `src/tinycopilot/privacy.py` that exports the five names `__init__.py` imports (`PrivacyMode`, `PrivacyViolation`, `assert_host_local`, `guard_request`, `verify_local_model`) so the package imports again; with that stub in place `make lab-m3` reports `file or directory not found: tests/test_privacy.py` until you create the test file, and then an assertion failure until you implement the rule. The red-team case: a "local alias of a cloud model" — a mocked `/api/show` response with `remote_host` set — must be **rejected** in local-only mode.

Then implement:

1. **`PrivacyMode`** — an explicit enum (`off` / `local` / `cloud`) with truthful labels. Copy ListenToMe's standard: the cloud label names the data it ships (cf. `"Ollama Cloud — sends transcript and context"`, `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:3-13`).
2. **`verify_local_model()`** — call the daemon's `/api/show` for the selected model and require `remote_host` and `remote_model` **absent** and `details.format` and `model_info` **present and non-empty**. Return `False` on anything missing, malformed, or unexpected — one conditional, fail closed. Reference: `ModelPrivacy.isVerifiedLocal` (`ModelPrivacy.swift:15-24`).
3. **Local-only host enforcement** — in local-only mode, accept only hosts `localhost`, `127.0.0.1`, or `::1`; throw before a byte of prompt is written. Reference: `ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:145-147`.
4. **Redirect refusal** — in local-only mode, an HTTP redirect (3xx) kills the request instead of following it. Reference: `RejectRedirects`, the delegate whose comment reads "Never follow redirects with meeting text in local-only mode" (`OllamaProvider.swift:138-142, 208-214`).

Write one test per defense, all with mocked transports: the cloud-alias rejection, fail-closed on missing metadata, non-localhost host rejection, redirect refusal.

## Step 2 — Real-LLM contract test (~30 min)

1. Create `tests/test_contract_real_llm.py`, gated by the environment variable `LAB_E2E=1` — skipped with a stated reason otherwise.
2. The test sends a **real** completion through *your* `OllamaProvider` — the same code path the app uses, not a reimplementation — with a fixed prompt, and asserts minimum content: non-empty response **and** contains an expected keyword (e.g., ask it to name a color and assert the color appears). Pick the model the way the app does — `role_defaults(fetch_models(...))` — rather than hard-coding one.
3. This is a **contract** test, not a privacy test: it runs in the provider's default mode against whatever chat model the router selects, `:cloud` aliases included, because its only job is to prove the request shape, streaming parse, and error typing hold against a real daemon (`tinycopilot/README.md`, "Verified status"; the parked reference's docstring says the same). Do not gate it on local-only mode, and do not substitute a mocked stream — a cloud-only daemon runs it just as well.
4. Run `LAB_E2E=1 pytest tests/test_contract_real_llm.py` and record the output; run the suite without the flag and record the skip.

Reference: ListenToMe's `make e2e` (auto-selects an installed chat model, `LTM_E2E_MODEL` override; `ListenToMe/Makefile:39-53`) and `OllamaContractE2ETests`, which skips unless `LTM_E2E=1` and asserts non-empty streamed content (`ListenToMe/Tests/ListenToMeCoreTests/OllamaContractE2ETests.swift:4-41`). ListenToMe's test also runs on any model, local or cloud (`LTM_E2E_BASEURL` may even point at Ollama Cloud).

## Step 3 — Coverage floor (~30 min)

1. `make m3-start` set the Makefile's `COV_FLOOR ?= 90` to `0`; the `lab-m2` target already passes `--cov=src/tinycopilot --cov-fail-under=$(COV_FLOOR)`. Put the floor back — `COV_FLOOR ?= 90` — and confirm `make lab-m2` prints `Required test coverage of 90% reached`. (In your own project this is the step where you add `--cov=<package> --cov-fail-under=90` to the test target yourself.)
2. **Prove the floor bites:** temporarily delete (or skip) one module's tests, run the suite, and record the **failure**. Restore the tests and record the **passing** run.

Reference: ListenToMe's 95% floor (`ListenToMe/scripts/check-coverage.sh`, run in the `core` CI job — `ListenToMe/.github/workflows/ci.yml:36-42`) and the Module 1 evidence rule: include the failures in your record, not just the green run.

## Step 4 — Comparison table (~60 min)

Produce `docs/competition.md` for **your** product idea:

- **≥5 competitors** — only ones you have actually used or visited.
- **≥6 columns** — platform, on-device (or your privacy axis), privacy, model choice, price, focus.
- **Every cell sourced** with the URL you checked, or marked **"unverified."** No memory-only pricing.
- **Qualify uncertain claims** exactly as ListenToMe does — "approximately," "reportedly" (`ListenToMe/docs/competition-analysis.md:3`).
- **Derive a one-line positioning statement** and annotate each clause with the column that proves it, the way the "free / open-source / fully on-device / bring your own model" clauses trace to Price, On-device?, and Multi-model/BYO columns (`competition-analysis.md:70-80`).

## Acceptance checklist (all must pass)

1. ☐ Step 0 recorded: the `make m3-start` output and the red `make lab-m3` run (`ModuleNotFoundError`, exit 4) precede everything else in the evidence log.
2. ☐ Red-team test green: a mocked cloud alias (`remote_host` set) is rejected in local-only mode, proven by test output, with its own red run recorded first.
3. ☐ `verify_local_model()` fails closed on missing metadata (mocked test with `format`/`model_info` absent).
4. ☐ Non-localhost host rejected in local-only mode (test).
5. ☐ Redirects refused in local-only mode (test).
6. ☐ `LAB_E2E` contract test passes against your daemon (any chat model the router picks) with output recorded, and the no-flag run records the skip with its reason.
7. ☐ Coverage floor enforced: `COV_FLOOR` back at 90, both the failure run and the success run recorded.
8. ☐ `competition.md` has ≥5 rows, ≥6 columns, per-cell sources or "unverified" marks.
9. ☐ Positioning one-liner derived and specific: every clause traceable to a table column.

## Evidence to record

Use the Module 1 format (commands, counts, date, environment, limitations, head SHA) plus: the Step 0 red run, which daemon case you hit in Step 1 (local model or only-cloud aliases), the red-team test output, both coverage runs (failure and success), and the `LAB_E2E` run *and* its skip message.

## Stretch goals

- **Swift track:** read `ModelPrivacy.swift` and `OllamaProvider.swift` in `ListenToMeCore` and map each defense — truthful labels, fail-closed metadata verification, host check, `RejectRedirects`, per-request re-verification — to the equivalent line of your Python code, as a table.
- **A `RejectRedirects` equivalent** — the reference tinycopilot repo has one (an httpx transport built with `follow_redirects=False` plus an explicit 3xx refusal, `src/tinycopilot/ollama_provider.py`); build yours first, then compare implementations.

## Discussion prompt

Post your red-team test: the mocked `/api/show` response you chose and the assertion that failed before you implemented the fix. Which defense was hardest to test — the metadata rule, the host check, or redirect refusal? Use the community template: your daemon case + the test + one claim→enforcement row from your `competition.md`.