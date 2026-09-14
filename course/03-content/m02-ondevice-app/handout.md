# M2 Handout — The On-Device AI App: Architecture

**The mental model in one sentence:** put every decision in a pure core behind a protocol seam, leave
only hardware glue in the platform layer, then prove the decisions with tests that need no
microphone, no screen capture, and no model.

## The pipeline, and where each stage lives

```
mic (.you) · system audio (.others)
      │ PCM chunks
      ▼
capture ─▶ transcribe ─▶ store/context ─▶ prompt ─▶ route ─▶ streamed deltas
 App/       Transcribing   ConversationStore  PromptBuilder  MeetingSession
            seam           (Core, pure)       (Core, pure)   (Core, pure)
```

| Stage | ListenToMe file | TinyCopilot module |
|---|---|---|
| Capture (glue) | `App/DualChannelCapture.swift` | (canned transcript) |
| Transcription seam | `Sources/ListenToMeCore/Transcriber.swift` | `conversation_store.py` feed |
| Store + window | `Sources/ListenToMeCore/ConversationStore.swift` | `conversation_store.py` |
| Proactive gate | `Sources/ListenToMeCore/QuestionDetector.swift` | `question_detector.py` |
| Prompts (pure) | `Sources/ListenToMeCore/Prompt.swift` | `prompts.py` |
| Ranking / routing | `Sources/ListenToMeCore/ModelRanking.swift` | `model_router.py` |
| Streaming errors | `Sources/ListenToMeCore/OllamaProvider.swift` | `ollama_provider.py` |
| Orchestration | `Sources/ListenToMeCore/MeetingSession.swift` | `copilot.py` |

## Decision table worth memorizing

| Decision | Rule | If you get it wrong |
|---|---|---|
| Context window | newest-first fit; always ≥1 segment | empty or ancient context |
| Question cue | token-prefix / word-boundary, never substring | `gemini` misread as `mini` |
| Model default | local-first; `:cloud` only if no local | transcript silently leaves the Mac |
| Model switch | bump generation; guard every write | stale answer under new model's name |
| Listener grounding | only *completed* summaries | half-answer treated as fact |
| Stream end | require `done` **and** visible text | truncation finishes as success |

## Commands to keep

```bash
cd course/03-content/m02-ondevice-app/tinycopilot
make lab-m2     # unit suite + coverage floor 90  → 191 passed, 100%
make lab-m3     # M3 privacy suite must stay green → 49 passed
make e2e        # real-LLM contract test (needs LAB_E2E=1)
make demo       # scripted meeting, three role outputs
pytest tests/test_model_router.py -q   # 40 passed
pytest tests/ -m "not e2e" --collect-only -q | tail -1
```

## Files to open

- `ListenToMe/Sources/ListenToMeCore/ConversationStore.swift:56-67` — the never-empty window.
- `ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:13-18, 76-94` — token-prefix, local-first.
- `ListenToMe/Sources/ListenToMeCore/Prompt.swift:65-88` — three base prompts.
- `ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:67-83, 159-170` — typed errors.
- `ListenToMe/Sources/ListenToMeCore/ContextEngine.swift:31-40` — the proactive gate.
- `ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md` — gap G06, the scar.
- `tinycopilot/tests/test_ollama_provider.py` — the failing-stream spec.

## Three gotchas

1. **Deleting a module gives an ImportError, not failed tests.** `__init__.py` re-exports everything,
   so `make lab-m2` exits 4 with an empty test run. That is the red run; the per-test spec is the test
   file.
2. **`gemini` contains `mini`.** Any substring marker check misroutes a whole model family. Match at
   token starts.
3. **The lab's prose says Listener gets a distinct fast model; the tests do not.** Implement to the
   tests — Listener and Quick both receive the fastest model.

## You're done when…

- [ ] `make lab-m2` exits 0 with 191 passed and the 90 coverage floor reached.
- [ ] Six red runs (ImportError, exit 4) are in your evidence log, each before its green run.
- [ ] `make lab-m3` still prints 49 passed.
- [ ] `make demo` prints Listener, Quick, and Deep outputs with model names visible.
- [ ] Your log explains each module's red→green cycle in one or two sentences.
- [ ] Router tests prove local-first defaults; provider tests prove typed errors on truncated streams.
