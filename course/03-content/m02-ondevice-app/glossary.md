# M2 Glossary — The On-Device AI App: Architecture

Pointers are relative to the cloned repo root unless prefixed `ListenToMe/`; course pointers are
relative to the course root.

## Terms

- **`:cloud` alias — a model a *local* daemon serves from a remote backend.** The name ends in
  `:cloud`, or `/api/tags` reports a `remote_host`/`remote_model`. `ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:72-79`;
  `course/03-content/m02-ondevice-app/tinycopilot/src/tinycopilot/model_router.py`.
- **`AudioCapturing` — the capture protocol seam.** Core declares what audio arrives; `App/` supplies
  `AVAudioEngine` and ScreenCaptureKit. `ListenToMe/Sources/ListenToMeCore/Capture.swift:4`.
- **Context window (`recentContext`) — the character-budgeted slice of transcript sent to a prompt.**
  Newest-first fit, default 4,000 characters, never empty.
  `ListenToMe/Sources/ListenToMeCore/ConversationStore.swift:56-67`.
- **`CopilotRole` — the three AI roles as an enum: `listener`, `quick`, `deep`.** Routing, prompts,
  and cancellation are all keyed by it. `ListenToMe/Sources/ListenToMeCore/CopilotRole.swift:5-7`.
- **Debounce — the minimum interval between proactive fires.** ListenToMe's default is 8 seconds.
  `ListenToMe/Sources/ListenToMeCore/ContextEngine.swift:8,31-40`.
- **Generation token — a per-role counter that invalidates an in-flight stream.** Switch a model, bump
  the token, and the old stream's deltas stop being written.
  `ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:119-132,513-578`.
- **`LLMProvider` — the provider protocol seam.** Core streams text through it; `App/` implements it
  with Ollama over HTTP. `ListenToMe/Sources/ListenToMeCore/LLMProvider.swift:4`.
- **Local-first defaults — auto-selection that filters cloud aliases out first.** Cloud is chosen only
  when no local model exists. `ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:76-94`.
- **NDJSON — newline-delimited JSON, Ollama's streaming format.** One JSON object per line carrying a
  delta or `done: true`. `ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:120-139`.
- **Partial vs. final — live in-flight text versus a settled utterance.** Partials never enter the
  finalized log; a final with the same id supersedes its partial.
  `course/03-content/m02-ondevice-app/tinycopilot/src/tinycopilot/conversation_store.py`.
- **Persona directive — preset guidance appended to every role's system prompt.** Same code path for
  manual panes and automatic reviews. `ListenToMe/Sources/ListenToMeCore/Prompt.swift:159-173`.
- **Proactive gate — the four conditions before a proactive answer fires.** Finalized, from `.others`,
  passes question detection, outside the debounce window.
  `ListenToMe/Sources/ListenToMeCore/ContextEngine.swift:31-40`.
- **`PromptBuilder` — the pure prompt-construction layer.** A public enum of static functions: context
  in, request out, no I/O. `ListenToMe/Sources/ListenToMeCore/Prompt.swift`.
- **Protocol seam — a protocol the pure core declares and platform glue implements.** The three are
  `AudioCapturing`, `Transcribing`, `LLMProvider`; they are what let tests run without hardware.
- **Token-prefix matching — capability markers matched at a token start, never as a substring.**
  Prevents `gemini` from being demoted as `mini`. `ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:13-18`.
- **Typed stream errors (`OllamaStreamError`) — the failure model for streaming.** `.server` for an
  in-stream error event, `.incomplete` when `done` never arrives, `.empty` when no visible text
  arrives. `ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:67-83,159-170`.
- **VAD — voice activity detection that finds utterance boundaries.** 37 lines: RMS energy, a 0.02
  threshold, 0.8 seconds of trailing silence. `ListenToMe/Sources/ListenToMeCore/VAD.swift`.
- **Verified local — a fail-closed metadata check, not a hostname check.** `isVerifiedLocal` rejects a
  model unless `remote_host` and `remote_model` are absent.
  `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:17`.

## Terms people get wrong

- **Local vs. verified local.** A `localhost` URL proves nothing — a local daemon can serve
  cloud-backed aliases; only the `/api/show` metadata check (M3) proves locality.
- **Coverage vs. correctness.** The old provider held 97.24% coverage *and* let truncated streams
  finish as success (`ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md`, gap G06). Tests
  validate what was built, not whether it was right.
- **Debounce vs. "wait for quiet."** This debounce does not pause until things calm down; it blocks
  re-firing for 8 seconds *after a fire*, so a burst produces exactly one answer.
- **Partial vs. final.** A partial is display state that will be replaced; treating it as conversation
  history is the bug the store's two-container design prevents.
- **Token-prefix vs. substring.** `"gemini"` contains `"mini"` but does not start a token with it;
  substring matching misroutes an entire model family.

## Curated resources

- `ListenToMe/docs/superpowers/specs/2026-06-18-listentome-design.md` §3–§4.4 — the approved
  architecture and the "deliberately simple, swappable later" rationale for question detection.
- `ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md` — gap G06; the clearest lesson in the
  repo on why an honest failure model beats more coverage.
- `ListenToMe/docs/SHARED-LIVE-SUMMARY.md` — every proactive budget (5 s batches, 24-char eligibility,
  3,072 tokens, 30 s/16 KiB caps) with the observation that set it.
- `ListenToMe/Sources/ListenToMeCore/ConversationStore.swift` — read `recentContext` until the
  never-empty guarantee is obvious; the lab reimplements it.
- `course/03-content/m02-ondevice-app/tinycopilot/tests/test_model_router.py` — the executable spec for
  token-prefix matching and local-first defaults, including the `gemini` negative case.
- `course/03-content/m02-ondevice-app/tinycopilot/tests/test_ollama_provider.py` — the failing-stream
  spec; read it before writing a provider.
- `ListenToMe/Sources/ListenToMeCore/VAD.swift` — 37 lines that show how far a threshold and a timer
  can go before you need a model.
