# Module 2 — The On-Device AI App: Architecture
> Part of AI Product Studio (APS-3) · ~75 minutes · Prerequisites: Module 1

## Overview

Module 1 gave you an operating system for AI-assisted building. This module opens the first product archetype: the **native on-device AI app** — a real-time system that captures the world, reasons about it locally, and keeps the user in control of every byte that leaves the machine. Your case study is ListenToMe, a free, open-source meeting copilot for macOS that listens to your microphone and the other participants' system audio, transcribes live on-device, and streams AI help through Ollama with a model you choose (`README.md`). One engineer shipped it with a 96% core-coverage badge — possible only because of the architecture you are about to study.

The central engineering problem of this archetype: the interesting decisions — segmentation, context windowing, question detection, model routing, prompt assembly, stream-error handling — all live downstream of audio hardware and a live LLM daemon, neither of which a CI runner can touch. ListenToMe's answer is a hard split. Every decision lives in `Sources/ListenToMeCore`, a pure SwiftPM package of 45 Swift source files (5,194 lines as of 2026-09-16) that needs no microphone, no screen capture, and no network to run its tests; `App/` holds only platform glue — AVAudioEngine, ScreenCaptureKit, Speech, SwiftUI. The two sides meet at three protocol seams: `AudioCapturing`, `Transcribing`, and `LLMProvider`. The whole pipeline runs in a unit test against mocks; only the thin glue is left for a human to smoke-test.

In this module you trace that pipeline end to end (M2.1), learn how three AI roles get routed to different models with per-role cancellation (M2.2), and see how "proactive intelligence" is actually a cheap heuristic wrapped in budgets, debounces, and typed errors (M2.3). In the lab you build TinyCopilot — the same architecture in Python + Ollama, small enough to finish in one sitting.

**By the end of this module you can:**

- Explain and sketch the capture → transcribe → context → prompt → route pipeline, and name the file that implements each stage.
- Justify the three protocol seams, and implement a conversation store with a character-budgeted context window that always keeps at least the newest segment.
- Route different models to different roles with local-first defaults, token-prefix matching, and stale-stream cancellation on model switch.
- Write prompt builders as pure functions — including a "never invent" grounding contract and an anti-preamble style.
- Add proactive behavior with a deliberately simple question detector behind a debounce.
- Type streaming errors so a truncated or empty response can never finish as success.

> **Pointer convention.** ListenToMe pointers are relative to the cloned repo root. Open every file the action steps name — the pointers are this course's provenance.

## Segment M2.1 — The capture→transcribe→context→prompt→route pipeline (~25 min)

### Objective

Explain ListenToMe's layered architecture: name the layers, name the three protocol seams, and justify the pure-core/app-glue split. Sketch the pipeline from memory and locate each stage in the code.

### Lesson

Start from the shipped product and walk backwards. ListenToMe captures two audio channels live — your microphone (labeled **You**) and the other participants' system audio via ScreenCaptureKit (labeled **Others**) — and gives each AI pane its own model (`README.md`, "Why ListenToMe"). The approved design spec describes a single-process SwiftUI app in which "audio and ASR run off the main actor; UI observes published state" (`docs/superpowers/specs/2026-06-18-listentome-design.md`, §3). Here is the pipeline as shipped — adapted from that spec's architecture diagram (§3), with the spec's single Response/Summary engines replaced by the three roles that actually shipped (`Sources/ListenToMeCore/CopilotRole.swift`):

```
      mic (.you)  ·  system audio (.others)
                     PCM chunks
                        │
      ┌──────────────────▼─────────────────┐
      │ DualChannelCapture (App/ glue)     │   seam: AudioCapturing
      └──────────────────┬─────────────────┘
                        ▼
      ┌────────────────────────────────────┐
      │ Transcriber (protocol seam)        │   seam: Transcribing
      │  SpeechAnalyzer (default)          │
      │  SpeechRecognizer (legacy)         │
      │  WhisperKit (opt-in)               │
      └──────────────────┬─────────────────┘
        partial + finalized segments
                        ▼
      ┌────────────────────────────────────┐
      │ ConversationStore                  │
      │  rolling utterance log;            │
      │  recentContext ≤ 4,000 chars       │
      └──────────────────┬─────────────────┘
                        ▼
  hotkey ─────────────┐
  QuestionDetector ───┴─▶ ContextEngine ─▶ PromptBuilder (pure)
  + 8 s debounce             Listener / Quick / Deep prompts
                      │
                      ▼
      ┌────────────────────────────────────┐
      │ MeetingSession per-role routing    │   seam: LLMProvider
      │  model + provider per role;        │
      │  generation token per role         │
      │  → OllamaProvider /api/chat        │
      └──────────────────┬─────────────────┘
              streamed token deltas
                      ▼
         Listener · Quick · Deep panes
```

**Layer 1 — capture.** `App/DualChannelCapture.swift` taps `AVAudioEngine`'s input node for the mic and creates a ScreenCaptureKit `SCStream` for system audio, "converting both to mono Float PCM and emitting `AudioChunk`s" (its header comment, line 8). Every buffer is tagged with a `SpeakerSource` — `.you` for the mic tap (line 102), `.others` for the `SCStream` callback (line 212). That one tag is what gives the app speaker attribution for free: "You" vs "Others" with no diarization model. Capture is the least testable code in the product, so it is also the thinnest.

**Layer 2 — the transcription seam.** Core declares the protocol; App provides the engines. `Sources/ListenToMeCore/Transcriber.swift` defines `Transcribing` — `prepare()`, `feed(_:)`, `finish()` — with a documented contract: `prepare()` warms the pipeline (model download, analyzer start) *before* any audio is fed, so `feed` never blocks and the opening seconds of a meeting aren't dropped, and it must observe cancellation while doing it. Three engines ship behind that one seam, selected in Settings:

- **`SpeechAnalyzerTranscriber`** (default): Apple's macOS 26 SpeechAnalyzer. One analyzer per source, so both channels transcribe concurrently, "unlike SFSpeechRecognizer" which has a single-active-recognition limit (`App/SpeechAnalyzerTranscriber.swift`, lines 6–39).
- **`SpeechRecognizerTranscriber`** (legacy): the older `SFSpeechRecognizer`, one recognition task per source. It can hit Apple's process-global active-recognition limit, error `kAFAssistantErrorDomain 1100` — documented in the README's known limitations, and the reason `MeetingSession` keeps a stop-drain task so a quick restart can't run two of these at once (`README.md`, line 244; `Sources/ListenToMeCore/MeetingSession.swift`, line 84).
- **`WhisperKitTranscriber`** (opt-in): a batch transcriber. It buffers each source's audio, uses Core's `VADSegmenter` to find utterance boundaries, and emits only *finalized* segments — trading live partials for "Whisper's stronger multilingual / code-switching quality" (`App/WhisperKitTranscriber.swift`, lines 6–13). That trade exists because Apple's on-device Speech "selects one primary language; it does not auto-detect or code-switch" (`App/MeetingView.swift`, line 84) — Mandarin↔English mixed speech is exactly the case WhisperKit is for.

The seam is the point: everything downstream cannot tell which engine produced a segment — add a fourth engine and nothing below the protocol changes.

**Layer 3 — store and context window.** `Sources/ListenToMeCore/ConversationStore.swift` is the single source of truth: an ordered log of finalized `TranscriptSegment`s plus the current partial per source (`apply(_:)` appends finals, replaces partials). The context window is `recentContext(maxChars:)`: walk utterances newest-first, keep segments while they fit the budget, and always include the most recent one even if it alone exceeds the budget — the window is never empty (lines 56–67). The default budget is 4,000 characters (`ContextEngine.buildContext`, `Sources/ListenToMeCore/ContextEngine.swift`, line 12), and budgets vary by intent: `MeetingSession.transcriptBudget(for:)` gives recap and action-items prompts 100,000 characters because they must cover the whole conversation, while on-the-spot answers get the recent window (`MeetingSession.swift`, lines 419–427).

**Where utterance boundaries come from.** When the engine does not stream partials (WhisperKit), something must decide where an utterance ends. Core's VAD is 37 lines: `rms(of:)` computes root-mean-square energy per frame, and `VADSegmenter` (defaults: speech threshold 0.02, trailing silence 0.8 s) returns `true` "exactly once, on the frame where trailing silence after speech first exceeds `silenceDuration`" (`Sources/ListenToMeCore/VAD.swift`). No ML model — a threshold and a timer, verified by `Tests/ListenToMeCoreTests/VADTests.swift`.

**Why the layering pays.** Everything marked Core above is pure: no microphone, no network, no UI. That is how a real-time audio product holds a 96% core-coverage badge with a 95% floor enforced in CI (`README.md` badge; `scripts/check-coverage.sh`, default threshold 95). Glue can't be unit-tested, so minimize it; logic can, so put the product there. Your TinyCopilot lab copies this shape exactly: a transcription seam satisfied by a canned transcript file, and everything else pure and tested.

### Action step

Open the cloned repo and verify each claim with your own eyes; record findings in your evidence log:

1. Open `Sources/ListenToMeCore/ConversationStore.swift` and read `recentContext(maxChars:)`. Confirm in the code that the newest utterance is included even when it exceeds the budget.
2. Open `App/DualChannelCapture.swift` and find the two places buffers are tagged `.you` and `.others` (the mic tap and the `SCStream` output callback).
3. Open `Sources/ListenToMeCore/Transcriber.swift` and note the `prepare()` contract: warm-up before audio, cancellation observed.
4. Sketch the pipeline diagram from memory in your evidence log, naming the file that implements each stage.

## Segment M2.2 — Per-role model routing and prompt builders (~25 min)

### Objective

Explain why one AI role ≠ one model, assign the right model to each role using local-first defaults, cancel stale streams on model switch, and write prompt builders as pure functions with a grounding contract.

### Lesson

ListenToMe's UI shows four panes — Transcript, Listener, Quick, Deep — and "each AI pane has its own model dropdown with 'good for' hints" (`README.md`, lines 89–92). The roles are an enum, not a UI accident: `listener`, `quick`, `deep` (`Sources/ListenToMeCore/CopilotRole.swift`). Quick answers on the global hotkey and fires proactively — it must be fast (`README.md`, lines 79–80). Deep gives on-demand long-reasoning answers — it should be strong (line 81). Listener auto-refreshes a rolling summary continuously — speed beats depth (line 78).

The tempting design — "just use the best model everywhere" — is wrong twice. It burns latency on roles that don't need strength, and it pins the whole product to one model's quirks. Per-role routing turns model choice into a per-pane budget the user can see and change.

**Local-first defaults.** When the app discovers installed models it calls `ModelRanking.roleDefaults(from:)` (`App/MeetingView.swift`, line 717; logic in `Sources/ListenToMeCore/ModelRanking.swift`, lines 76–94). Quick gets a curated fast model — matching `fastPatterns` (flash, mini, nano, lite, small, fast) — or else the lightest. Deep gets a curated strong model — matching `strongPatterns` (pro, reason, think, coder, code, ultra, max, large) — or else the heaviest, picked from the models Quick didn't take so one name matching both sets can't collapse both panes onto one model. Listener gets a second fast model distinct from Quick and Deep, because it refreshes continuously. The defaults are **local-first**: `:cloud` models are filtered out of auto-selection, so an unpinned pane never silently sends a transcript to Ollama Cloud; cloud is auto-picked only when no local model exists (lines 72–79). The "good for" hints come from the same file: `describe(_:)` maps about twenty known model families to one-line hints, with keyword-heuristic fallback (lines 101–141).

**Token-prefix matching.** To detect "mini" in a name, `ModelRanking` splits the name into lowercase tokens and checks whether any token *begins with* the marker — "Token-prefix matching (not raw substring) rejects cross-token false hits like `gemini` ⊃ `mini`" (`ModelRanking.swift`, lines 13–18). A raw substring check would rank every Gemini model as "fast," because "gemini" contains "mini" — your defaults would be quietly wrong for an entire model family.

**Generation tokens — killing stale streams.** `MeetingSession` keeps `models`, `providers`, and `responseGenerations` dictionaries per role (`MeetingSession.swift`, lines 54–87). `setModel(_:_)` cancels that role's in-flight task and bumps its generation counter (lines 119–132). The streaming loop captures its generation and guards every write with `generation == responseGenerations[role]` (lines 513–578), so when you switch models mid-answer the old stream's tokens die on the floor — without this, a slow answer from the old model could finish *after* the switch and display under the new model's name.

**Prompt builders are pure functions.** `PromptBuilder` is a `public enum` with static functions and zero I/O (`Sources/ListenToMeCore/Prompt.swift`): context in, `LLMRequest` out. That purity is what makes prompts unit-testable (`Tests/ListenToMeCoreTests/PromptBuilderTests.swift`) — you assert on the built string, no model needed. Three base system prompts ship:

- **Quick** is anti-preamble: "Be concise and conversational. No preamble, no 'As an AI', no restating the question, no meta-commentary. Prefer 1-3 short sentences or a tight bullet list. If a question was asked, answer it directly first." (lines 65–71). In a pane you read at meeting speed, every preamble word is a latency tax.
- **Listener** carries the grounding contract: "Never invent an owner, deadline, agreement, or completion. Mark missing details as unstated." (lines 73–81). The Listener's output feeds back into other panes' prompts, so one hallucinated owner would propagate everywhere; the contract blocks it at the source.
- **Deep** inverts Quick's budget: "Be thorough and precise — depth is valued over brevity here." (lines 83–88).

On top of the base prompts sit **9 response actions** — `answerQuestion`, `recap`, `followUp`, `proactive`, `actionItems`, `clarify`, `counterpoint`, `keyTerms`, `draftReply` — each with separate Quick and Deep instruction variants (lines 14–24 and 90–137). And `systemWithDirectives(_:_)` appends the selected preset's persona guidance and a response-language directive to *every* pane's system prompt (lines 159–173) — manual panes and automatic reviews share the path, so a preset like Interview shapes all three roles identically.

**Listener→Quick/Deep grounding.** Quick and Deep prompts are grounded in the Listener's summary — but only the last *completed* one. `MeetingSession` keeps `lastCompletedListenerSummary` separate from `listenerSummary`, the live display value that is cleared while a refresh streams, "so a proactive Quick can't read an empty/partial in-flight summary" (`MeetingSession.swift`, lines 40–43; injected at lines 435 and 449). The common misconception — "more context is better, inject whatever is on screen" — fails exactly here: an in-flight summary is *worse* than no summary, because it is a confident-looking half-answer. Inject only completed work.

### Action step

1. Open `Sources/ListenToMeCore/Prompt.swift`. Find the listener's never-invent contract and the Quick pane's anti-preamble sentence. Copy both into your evidence log and write one sentence each on what breaks if the line is removed.
2. Open `Sources/ListenToMeCore/ModelRanking.swift` and trace `hasMarker("gemini-2.5-flash", "mini")` by hand; then compare with `"gemini-2.5-flash".contains("mini")`. Record both results.
3. Open `Sources/ListenToMeCore/MeetingSession.swift` at lines 119–132 and 513–578: find where `setModel` bumps the generation counter and where the stream loop checks it.
4. Run `ollama list`. In your evidence log, assign each of your installed models to Listener/Quick/Deep and justify each pick with the rules above.

## Segment M2.3 — Proactive intelligence without magic (~25 min)

### Objective

Implement proactive triggering with a deliberately simple heuristic behind a debounce, and treat streaming failures as typed, visible errors — automation under a budget, not on vibes.

### Lesson

"Proactive" sounds like it needs intelligence. It needs restraint. ListenToMe's question detector is 28 lines: `Sources/ListenToMeCore/QuestionDetector.swift` classifies a finalized utterance as a question if it ends in "?", *starts with* an interrogative (what, why, how, when, where, who, which, whose), or contains a phrase cue matched on word boundaries ("can you", "could you", "any thoughts", "walk me through", …). The design spec chose this on purpose: question detection is a "lightweight heuristic … Debounced so it fires at most once per N seconds. Kept deliberately simple; swappable later" (`docs/superpowers/specs/2026-06-18-listentome-design.md`, §4.4). Ship the cheap heuristic *behind a seam*, keep the option to swap in a classifier, and spend your complexity budget elsewhere.

The restraint comes from the gate. `ContextEngine.shouldFireProactive(for:now:)` fires only when the segment is finalized, came from `.others` (someone asking *you* — not you talking to yourself), passes question detection, **and** at least `debounce` seconds (default 8) have passed since the last fire (`Sources/ListenToMeCore/ContextEngine.swift`, lines 8 and 31–40). Without the debounce, two heated minutes of questions would flood the pane with overlapping suggestions. One trigger, one answer, then quiet.

**Streaming with typed errors.** `OllamaProvider` POSTs to `/api/chat` with `stream: true` and reads the response as NDJSON lines — each line a JSON object carrying a message delta or `done: true` (`Sources/ListenToMeCore/OllamaProvider.swift`, lines 120–139; the `lineSource` is injectable so tests feed canned lines). Three details make this production-grade:

1. **In-stream error events.** Ollama can answer HTTP 200 and then send `{"error": "..."}` mid-stream. The provider parses every line and throws `OllamaStreamError.server(error)` when it finds one (lines 70–73).
2. **Completion flags.** The stream loop tracks `completed` (saw `done: true`) and `producedContent` (yielded at least one non-whitespace delta). If the lines end without `done`, it throws `.incomplete`; if the stream "completes" with no content, it throws `.empty` (lines 67–83). A truncated or empty stream therefore *cannot finish as success*.
3. **Typed cases.** `OllamaStreamError` is `.server(String)` / `.incomplete` / `.empty`, each with a user-facing message — `.incomplete` even tells you the partial text is kept (lines 159–170).

This design is a scar, not a guess. The September 2026 design-and-gap review found the *old* provider ignored in-stream Ollama errors and let "truncated/empty streams … finish as success" — gap G06, P0 — at a moment when the project showed 215 passing Core tests and 97.24% coverage (`docs/reviews/2026-09-10/design-and-gap-review.md`, lines 5 and 51). The tests validated what was built; what was built was wrong. The fix was not more coverage — it was an honest failure model. The recurring misconception, "swallow stream errors to avoid UI flicker," is exactly backwards: the user gets a silently incomplete answer instead of a retry affordance. Flicker is information; silence is a lie.

**Budgets come from observation.** Automatic Quick evaluations run with `LLMRequest.Purpose.quickEvaluation`, which forces `think: false`, temperature 0, and a 3,072-token output cap (`OllamaProvider.swift`, lines 49–51). Why 3,072? Live GLM testing "exposed planning text despite `think: false`, exhausting the former 1,600-token budget halfway through valid final JSON" — so Quick now allows 3,072 generated tokens and a 30-second deadline while keeping a 16-KiB response cap (`docs/SHARED-LIVE-SUMMARY.md`, line 66). The number is not theory; it is the smallest budget that stopped an observed truncation. When your own caps break in live testing, raise them the same way — from evidence.

**Automation under budget.** The shared live-summary engine — `LiveSummaryScheduler`, `QuickSummaryContext`, `AutomaticReviewCoordinator` in Core, documented in `docs/SHARED-LIVE-SUMMARY.md` — is what "proactive" looks like in production: event-driven and bounded everywhere.

- Speech **batches for five seconds** before evaluation; a non-final hypothesis needs **24 trimmed characters** to be eligible (`docs/SHARED-LIVE-SUMMARY.md`, lines 8–10; `Sources/ListenToMeCore/QuickSummaryContext.swift`, line 65).
- **Unchanged input does not poll** — "timers exist only for queued work or a failed request" (`AutomaticReviewCoordinator.swift`, line 51).
- Responses cap at **30 seconds / 16 KiB** (`docs/SHARED-LIVE-SUMMARY.md`, lines 16–19).
- When a Quick evaluation recommends it, full **Summary** and **Deep** reviews run **serially** — Summary at most every 30 s, Deep every 60 s; the first eligible review starts immediately, and unchanged input cannot regenerate a completed review (`AutomaticReviewCoordinator.swift`, line 83; `docs/SHARED-LIVE-SUMMARY.md`, line 60).

Every number here is a cost ceiling, not a feature. That is the segment's takeaway: proactive intelligence is 5% trigger — a 28-line heuristic — and 95% discipline: debounces, budgets, caps, typed failures.

### Action step

1. Open `Sources/ListenToMeCore/QuestionDetector.swift` and list its three rules, noting which rule requires the cue at the *start* of the utterance.
2. Open `Sources/ListenToMeCore/OllamaProvider.swift` and find the two booleans that make truncated and empty streams fail. Then write in your evidence log: a stream yields "The best ans" and ends without `done` — which `OllamaStreamError` case fires, and what does the user see?
3. Open `docs/SHARED-LIVE-SUMMARY.md` and find the sentence explaining why the quick-evaluation budget is 3,072 tokens.
4. Audit your own product idea: write its proactive trigger, its debounce window, and its per-response budget — three numbers, no adjectives.

## Recap

- **M2.1** — The pipeline is capture → transcribe → store/context → prompt → route. Platform glue lives in `App/`; every decision lives in pure Core behind `AudioCapturing`, `Transcribing`, `LLMProvider`. Three transcription engines swap behind one seam; `ConversationStore.recentContext` enforces a character budget (default 4,000) that always keeps at least the newest segment; a 37-line VAD segments utterances when the engine can't.
- **M2.2** — Three roles (Listener/Quick/Deep) get different models: local-first `roleDefaults` (fast→Quick, strong→Deep, distinct fast→Listener), token-prefix matching rejects the "gemini ⊃ mini" false hit, and generation tokens cancel stale streams on model switch. `PromptBuilder` is pure — anti-preamble Quick, never-invent Listener, depth-over-brevity Deep — with 9 response actions and persona directives threaded through every pane. Only *completed* listener summaries ground Quick/Deep.
- **M2.3** — Proactive = a 28-line question heuristic behind a seam, gated by an 8-second debounce on finalized `.others` segments. Streaming errors are typed (`.server`/`.incomplete`/`.empty`) so truncation can't pass as success — the fix for gap G06. Budgets (3,072 quick tokens, 5 s batches, 24-char eligibility, 30 s/16 KiB caps, 30 s/60 s review spacing) come from observed failures, not guesses.

## Discussion prompt

Post your answer to the community: a stakeholder proposes your copilot "should just know when to help — point the biggest model at it and let it decide." Using this module's evidence (cite at least three ListenToMe files), write a ~150-word reply naming (a) what the trigger would actually be, (b) what debounce and budget you would put around it, and (c) which failure mode your design prevents that theirs doesn't.