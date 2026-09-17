# TinyCopilot — the Module 2/3 lab for AI Product Studio

A compact, fully working Python re-implementation of the core architecture of
[ListenToMe](https://github.com/tomqwu/ListenToMe) — a free, open-source, fully on-device
meeting copilot for macOS/iOS (Swift). TinyCopilot mirrors ListenToMe's
`Sources/ListenToMeCore` design in 460 Python statements (1,079 source lines under
`src/tinycopilot/`) so the same ideas run on macOS, Linux, and Windows with nothing
but Python and Ollama.

**How the course uses this repo:** *the tests are the spec; the reference implementation
is the answer key.* In Lab M2 you run the suite once to see it green, then delete the
marked modules and re-implement each one test-first until the gate passes again.
In Lab M3 you harden it (privacy mode, real-LLM contract test, coverage floor) and
red-team it.

## Layout (each module maps to its Swift counterpart)

| File | Mirrors (in `ListenToMe/Sources/ListenToMeCore/`) | Job |
|---|---|---|
| `src/tinycopilot/conversation_store.py` | `ConversationStore.swift` | ordered finalized-utterance log + partial; `recent_context(max_chars)` char budget, always ≥1 segment |
| `src/tinycopilot/question_detector.py` | `QuestionDetector.swift` | cheap heuristic ("?", interrogatives, phrase cues) + injectable-clock debounce |
| `src/tinycopilot/prompts.py` | `Prompt.swift` | pure prompt builders; three role contracts (anti-preamble Quick; Listener's "Never invent an owner, deadline, agreement, or completion"; Deep = depth) |
| `src/tinycopilot/ollama_provider.py` | `OllamaProvider.swift` | NDJSON streaming over `/api/chat`; typed errors (`ServerError` / `IncompleteStreamError` / `EmptyResponseError`); in-stream error events; no redirect following |
| `src/tinycopilot/model_router.py` | `ModelRanking.swift`, `ModelRouter.swift` | `/api/tags` discovery, local-first role defaults (Listener=fast, Quick=fastest, Deep=strongest), token-prefix capability hints |
| `src/tinycopilot/privacy.py` | `ModelPrivacy.swift` | `PrivacyMode` (OFF/LOCAL/CLOUD); `verify_local_model()` **fail-closed** `/api/show` metadata check (remote_host/remote_model must be absent); localhost-only host rule |
| `src/tinycopilot/copilot.py` | `MeetingSession.swift`, `CopilotRole.swift` | three roles → three models; per-role generation tokens cancel stale streams; only *completed* listener summaries ground Quick/Deep |
| `tests/` | `Tests/ListenToMeCoreTests/` | the executable spec (191 tests; contract tests gated by `LAB_E2E=1`) |
| `demo.py` | — | feeds a scripted meeting through all three roles |

## Setup

```bash
# 1. Python 3.11+ (the course standard, matching SignUpFlow's floor; TinyCopilot itself also runs on 3.10) and pytest + httpx
python3 -m pip install pytest pytest-cov httpx

# 2. Ollama running (https://ollama.com) with at least one model.
#    A genuinely local model makes the privacy lab meaningful:
ollama pull qwen3:0.6b
#    (A daemon with only :cloud aliases is also a valid — and instructive — environment.)

# 3. From this folder:
make lab-m2    # unit suite + coverage floor ≥90  (Module 2 pass gate)
make lab-m3    # privacy + streaming hardening suite (Module 3 pass gate)
make e2e       # real-LLM contract test (needs LAB_E2E=1 and a reachable daemon)
make demo      # scripted meeting through Listener → Quick → Deep
make m3-start  # Lab M3 step 0: park privacy.py + its tests + the contract test; COV_FLOOR -> 0
make m3-restore  # bring the reference Lab M3 solution back; COV_FLOOR -> 90
```

## Verified status (as shipped)

- `make lab-m2` → **191 passed**, coverage **100%** (floor: 90% enforced via `--cov-fail-under`)
- `make lab-m3` → **49 passed**
- `make e2e` → **2 passed** against a live Ollama daemon (cloud aliases and local models both work — the contract test is about the provider, not privacy)
- `make demo` → produces labeled LISTENER / QUICK / DEEP outputs; picks models via `model_router.role_defaults`

## The privacy lab, in one paragraph

Local-only mode is engineered to **fail closed**: before every request, `verify_local_model()`
calls Ollama's `/api/show` and rejects the model unless `remote_host` and `remote_model` are
absent and `details.format` / `model_info` are present. A `localhost` URL proves nothing —
a local daemon can serve cloud-backed aliases (`something:cloud` names, or a remote-backed
model presented under a local-sounding name). The red-team test ships with the repo: a mocked
`/api/show` response carrying a `remote_host` must be rejected in LOCAL mode. This mirrors
ListenToMe's `ModelPrivacy.isVerifiedLocal` and its `RejectRedirects` transport behavior.

## Course pointers

- Lesson: `../../m02-ondevice-app/lesson.md` (architecture) and `../../m03-privacy-ship/lesson.md` (privacy/testing/shipping)
- Labs: `../../m02-ondevice-app/lab.md`, `../../m03-privacy-ship/lab.md`
- Swift stretch track: keep this table beside the real files in `ListenToMe/Sources/ListenToMeCore/` — every Python module above has a Swift counterpart with the same responsibilities.