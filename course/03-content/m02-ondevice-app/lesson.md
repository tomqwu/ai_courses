# Module 2 — The On-Device AI App: Architecture
> Part of AI Product Studio (APS-3) · ~75 minutes · Prerequisites: Module 1

## Overview

```figure
kind: scene
alt: A video meeting on a laptop, with a copilot pane beside the call offering a suggestion.
scene: meeting.svg
caption: what ListenToMe is for — a copilot beside the call, not inside it
```

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

**Layer 1 — capture.** `App/DualChannelCapture.swift` taps `AVAudioEngine`'s input node for the mic and creates a ScreenCaptureKit `SCStream` for system audio, "converting both to mono Float PCM and emitting `AudioChunk`s" (its header comment, `ListenToMe/App/DualChannelCapture.swift:8-9`). Every buffer is tagged with a `SpeakerSource` — `.you` for the mic tap (`ListenToMe/App/DualChannelCapture.swift:143`), `.others` for the `SCStream` callback (`ListenToMe/App/DualChannelCapture.swift:324`). That one tag is what gives the app speaker attribution for free: "You" vs "Others" with no diarization model. Capture is the least testable code in the product, so it is also the thinnest.

**Layer 2 — the transcription seam.** Core declares the protocol; App provides the engines. `Sources/ListenToMeCore/Transcriber.swift` defines `Transcribing` — `prepare()`, `feed(_:)`, `finish()` — with a documented contract: `prepare()` warms the pipeline (model download, analyzer start) *before* any audio is fed, so `feed` never blocks and the opening seconds of a meeting aren't dropped, and it must observe cancellation while doing it. Three engines ship behind that one seam, selected in Settings:

- **`SpeechAnalyzerTranscriber`** (default): Apple's macOS 26 SpeechAnalyzer. One analyzer per source, so both channels transcribe concurrently, "unlike SFSpeechRecognizer" which has a single-active-recognition limit (`ListenToMe/App/SpeechAnalyzerTranscriber.swift:6-39`).
- **`SpeechRecognizerTranscriber`** (legacy): the older `SFSpeechRecognizer`, one recognition task per source. It can hit Apple's process-global active-recognition limit, error `kAFAssistantErrorDomain 1100` — documented in the README's known limitations, and the reason `MeetingSession` keeps a stop-drain task so a quick restart can't run two of these at once (`ListenToMe/README.md:374-376`; `ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:164-166`).
- **`WhisperKitTranscriber`** (opt-in): a batch transcriber. It buffers each source's audio, uses Core's `VADSegmenter` to find utterance boundaries, and emits only *finalized* segments — trading live partials for "Whisper's stronger multilingual / code-switching quality" (`ListenToMe/App/WhisperKitTranscriber.swift:6-13`). That trade exists because Apple's on-device Speech "selects one primary language; it does not auto-detect or code-switch" (`ListenToMe/App/MeetingView.swift:106-107`) — Mandarin↔English mixed speech is exactly the case WhisperKit is for.

The seam is the point: everything downstream cannot tell which engine produced a segment — add a fourth engine and nothing below the protocol changes.

**Layer 3 — store and context window.** `Sources/ListenToMeCore/ConversationStore.swift` is the single source of truth: an ordered log of finalized `TranscriptSegment`s plus the current partial per source (`apply(_:)` appends finals, replaces partials). The context window is `recentContext(maxChars:)`: walk utterances newest-first, keep segments while they fit the budget, and always include the most recent one even if it alone exceeds the budget — the window is never empty (`ListenToMe/Sources/ListenToMeCore/ConversationStore.swift:76-87`). The default budget is 4,000 characters (`ContextEngine.buildContext`, `ListenToMe/Sources/ListenToMeCore/ContextEngine.swift:12`), and budgets vary by intent: `MeetingSession.transcriptBudget(for:)` gives recap and action-items prompts 100,000 characters because they must cover the whole conversation, while on-the-spot answers get the recent window (`ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:582-587`).

**Where utterance boundaries come from.** When the engine does not stream partials (WhisperKit), something must decide where an utterance ends. Core's VAD is 37 lines: `rms(of:)` computes root-mean-square energy per frame, and `VADSegmenter` (defaults: speech threshold 0.02, trailing silence 0.8 s) returns `true` "exactly once, on the frame where trailing silence after speech first exceeds `silenceDuration`" (`Sources/ListenToMeCore/VAD.swift`). No ML model — a threshold and a timer, verified by `Tests/ListenToMeCoreTests/VADTests.swift`.

**Why the layering pays.** Everything marked Core above is pure: no microphone, no network, no UI. That is how a real-time audio product holds a 96% core-coverage badge with a 95% floor enforced in CI (`README.md` badge; `scripts/check-coverage.sh`, default threshold 95). Glue can't be unit-tested, so minimize it; logic can, so put the product there. Your TinyCopilot lab copies this shape exactly: a transcription seam satisfied by a canned transcript file, and everything else pure and tested.

**The same archetype off the Mac.** Only the glue above is Apple-specific. The core and its three seams are the architecture; a platform decides two things only: which system services can fill `Transcribing` and `LLMProvider`, and what you must check before you trust them. As of September 2026 each major client platform ships an on-device stack. The table compresses what each one provides, what it constrains, and what stays your code. Every cell is the vendor describing its own product; the source, read date and evidence grade for each is in `course/03-content/m02-ondevice-app/appendix-models-2026-09.md`.

| | Apple | Windows | Android |
|---|---|---|---|
| **Language model the OS provides** | Foundation Models: the on-device Apple Intelligence model, OS 26+. From OS 27 a `LanguageModel` protocol lets any provider plug into the same API | Phi Silica through the Windows AI APIs, on Copilot+ PCs. Foundry Local: 20+ open-source LLM and speech models behind an OpenAI-compatible API, on any Windows hardware | Gemini Nano through the ML Kit GenAI Prompt API, run by the AICore system service |
| **Speech** | SpeechAnalyzer, ListenToMe's default engine | Whisper through Foundry Local, or the older Windows SDK recognizer | ML Kit GenAI speech recognition |
| **Bring your own model** | Core AI (announced at WWDC26) and MLX | Windows ML: ONNX Runtime with NPU, GPU and CPU execution providers that Windows installs and updates. Running LLMs on it directly is labelled Preview | LiteRT-LM, whose Kotlin API is marked Stable |
| **What it constrains** | An Apple Intelligence device, a supported region and the user's opt-in. A small window: ListenToMe caps every Apple prompt at 8,000 characters | Phi Silica needs a Copilot+ PC and an unlock token, and is not offered in China. Foundry Local's WinML build on a virtual machine without GPU passthrough returns a *successful, empty* response, and the runtime "may collect usage data and send it to Microsoft" | Prompt input under 4,000 tokens, a per-app inference quota, and a model that may still be downloading. The Prompt API is a beta (`1.0.0-beta4`) |
| **What you still write** | An availability fallback, a prompt budget, and errors mapped to messages a user can act on | The same, plus a fallback chain. Microsoft's own sample falls from Phi Silica to Foundry Local to Azure; a local-first product stops at Foundry Local, or asks first | The same, plus download states (`DOWNLOADABLE`, `DOWNLOADING`) and quota errors |

Three things the table does not change. **The decisions stay yours.** The context window, the question gate, role routing, the prompts and the typed stream errors are in no platform's API; they live in your core on every OS. **A platform model is a provider, not an architecture.** ListenToMe already fills `LLMProvider` twice. Beside `OllamaProvider` sits `AppleIntelligenceProvider`, which checks availability before it generates (`ListenToMe/SharedPlatform/AppleIntelligenceProvider.swift:17-25`), refuses an over-budget prompt rather than answer from a truncated one (`ListenToMe/SharedPlatform/AppleIntelligenceProvider.swift:80-85`), and turns each Foundation Models error into a message that names a way out (`ListenToMe/SharedPlatform/AppleIntelligenceProvider.swift:42-65`). The app picks one provider or the other in a single closure (`ListenToMe/App/MeetingView.swift:176-180`). **On-device is not the same as good enough.** ListenToMe tried the Apple model as its automatic Quick evaluator: "The native Auto experiment failed the quality gate (3/7 cases …)", so it stays outside both app targets (`ListenToMe/docs/SHARED-LIVE-SUMMARY.md:64-68`). Measure each role on each platform model before you ship it. Foundry Local's empty success is the same warning from the other side: it is exactly the stream M2.3's `.empty` error exists to refuse.

**What this course runs.** The labs are Python against Ollama, which installs on macOS, Windows and Linux. The Swift track in Lab M2 is the only platform code the course ships, and it is Mac-only (`lab.md`, "Swift track"). No Windows or Android code ships here, and nothing in the table was built or measured by this course. If you target Windows or Android, the architecture carries over unchanged: port the core, then write one `LLMProvider` and one transcription adapter behind the same seams, and test them against fakes the way TinyCopilot does.

### Action step

Open the cloned repo and verify each claim with your own eyes; record findings in your evidence log:

1. Open `Sources/ListenToMeCore/ConversationStore.swift` and read `recentContext(maxChars:)`. Confirm in the code that the newest utterance is included even when it exceeds the budget.
2. Open `App/DualChannelCapture.swift` and find the two places buffers are tagged `.you` and `.others` (the mic tap and the `SCStream` output callback).
3. Open `Sources/ListenToMeCore/Transcriber.swift` and note the `prepare()` contract: warm-up before audio, cancellation observed.
4. Sketch the pipeline diagram from memory in your evidence log, naming the file that implements each stage.
5. Open `ListenToMe/SharedPlatform/AppleIntelligenceProvider.swift:17-25` and copy the three `.unavailable` cases. For the platform you would ship on, write the equivalent checks from the table above, and what your UI shows for each.

## Segment M2.2 — Per-role model routing and prompt builders (~25 min)

### Objective

Explain why one AI role ≠ one model, assign the right model to each role using local-first defaults, cancel stale streams on model switch, and write prompt builders as pure functions with a grounding contract.

### Lesson

ListenToMe's UI shows four panes — Transcript, Listener, Quick, Deep — and "Each AI pane's model is set from a model picker in the left status rail" (`ListenToMe/README.md:120-121`), annotated with "good for" hints (`ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:119-159`). The roles are an enum, not a UI accident: `listener`, `quick`, `deep` (`Sources/ListenToMeCore/CopilotRole.swift`). Quick answers on the global hotkey and fires proactively — it must be fast (`ListenToMe/README.md:101-105`). Deep gives on-demand long-reasoning answers — it should be strong (`ListenToMe/README.md:106`). Listener keeps a rolling summary (`ListenToMe/README.md:100`) that "auto-refreshes continuously, so speed beats depth" (`ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:74-78`).

The tempting design — "just use the best model everywhere" — is wrong twice. It burns latency on roles that don't need strength, and it pins the whole product to one model's quirks. Per-role routing turns model choice into a per-pane budget the user can see and change.

**Local-first defaults.** When the app discovers installed models it calls `ModelRanking.roleDefaults(from:local:)` (`ListenToMe/App/MeetingView.swift:845`; logic in `ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:91-111`). Quick gets a curated fast model — matching `fastPatterns` (flash, mini, nano, lite, small, fast) — or else the lightest. Deep gets a curated strong model — matching `strongPatterns` (pro, reason, think, coder, code, ultra, max, large) — or else the heaviest, picked from the models Quick didn't take so one name matching both sets can't collapse both panes onto one model. Listener gets a second fast model distinct from Quick and Deep, because it refreshes continuously. The defaults are **local-first**: when Ollama's own `/api/show` metadata has verified any model as local, only those are considered (a `:cloud` or `-cloud` name is the fallback test when locality is unknown), so an unpinned pane never silently sends a transcript to Ollama Cloud; cloud is auto-picked only when no local model exists (`ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:80-95`). The "good for" hints come from the same file: `describe(_:)` maps about twenty known model families to one-line hints, with keyword-heuristic fallback (`ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:119-159`).

**Which models? The survey lives in a dated appendix.** The rules above outlast any model list; the list does not. Qwen alone published Qwen3.5, 3.6 and 3.8 between February and August 2026, so this lesson carries no model survey. The matrix is `course/03-content/m02-ondevice-app/appendix-models-2026-09.md`: family, sizes, what each is good for, where it runs, and a source with its read date on every row. The date is in the filename. When the survey ages, a new dated file replaces it and this pointer changes; nothing else does. The lab default does not move with the survey. `qwen3:0.6b` stays the model `lab.md` asks you to pull and the one TinyCopilot's demo and privacy tests name, because it runs on any laptop, not because it wins anything. ListenToMe shows the same split in code: routing runs on two short marker lists (`ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:49-54`), while the `describe(_:)` hints are a hand-kept table of 21 model families (`ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:119-143`) that ages like any survey. Rules age slowly; lists age fast. Date the lists.

**Token-prefix matching.** To detect "mini" in a name, `ModelRanking` splits the name into lowercase tokens and checks whether any token *begins with* the marker — "Token-prefix matching (not raw substring) rejects cross-token false hits like `gemini` ⊃ `mini`" (`ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:13-18`). A raw substring check would rank every Gemini model as "fast," because "gemini" contains "mini" — your defaults would be quietly wrong for an entire model family.

**Generation tokens — killing stale streams.** `MeetingSession` keeps `models`, `providers`, and `responseGenerations` dictionaries per role (`ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:123, 144, 169-170`). `setModel(_:_)` calls `cancelResponse(_:)`, which cancels that role's in-flight task and bumps its generation counter (`ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:204-221`). The streaming loop captures its generation and guards every write with `generation == responseGenerations[role]` (`ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:803-880`), so when you switch models mid-answer the old stream's tokens die on the floor — without this, a slow answer from the old model could finish *after* the switch and display under the new model's name.

**Prompt builders are pure functions.** `PromptBuilder` is a `public enum` with static functions and zero I/O (`Sources/ListenToMeCore/Prompt.swift`): context in, `LLMRequest` out. That purity is what makes prompts unit-testable (`Tests/ListenToMeCoreTests/PromptBuilderTests.swift`) — you assert on the built string, no model needed. Three base system prompts ship:

- **Quick** is anti-preamble: "Be concise and conversational. No preamble, no 'As an AI', no restating the question, no meta-commentary. Prefer 1-3 short sentences or a tight bullet list. If a question was asked, answer it directly first." (`ListenToMe/Sources/ListenToMeCore/Prompt.swift:129-135`). In a pane you read at meeting speed, every preamble word is a latency tax.
- **Listener** carries the grounding contract: "Never invent an owner, deadline, agreement, or completion. Mark missing details as unstated." (`ListenToMe/Sources/ListenToMeCore/Prompt.swift:137-145`). The Listener's output feeds back into other panes' prompts, so one hallucinated owner would propagate everywhere; the contract blocks it at the source.
- **Deep** inverts Quick's budget: "Be thorough and precise — depth is valued over brevity here." (`ListenToMe/Sources/ListenToMeCore/Prompt.swift:147-152`).

On top of the base prompts sit **9 response actions** — `answerQuestion`, `recap`, `followUp`, `proactive`, `actionItems`, `clarify`, `counterpoint`, `keyTerms`, `draftReply` — each with separate Quick and Deep instruction variants (`ListenToMe/Sources/ListenToMeCore/Prompt.swift:14-24, 154-201`). And `systemWithDirectives(_:_)` appends the selected preset's persona guidance and a response-language directive to *every* pane's system prompt (`ListenToMe/Sources/ListenToMeCore/Prompt.swift:245-260`) — manual panes and automatic reviews share the path, so a preset like Interview shapes all three roles identically.

**Listener→Quick/Deep grounding.** Quick and Deep prompts are grounded in the Listener's summary — but only the last *completed* one. `MeetingSession` keeps `lastCompletedListenerSummary` separate from `listenerSummary`, the live display value that is cleared while a refresh streams, "so a proactive Quick can't read an empty/partial in-flight summary" (`ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:53, 81-84`). It is read in one place, `clampedContext`, which builds both the Quick and the Deep prompt (`ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:601-605, 640-653`). The common misconception — "more context is better, inject whatever is on screen" — fails exactly here: an in-flight summary is *worse* than no summary, because it is a confident-looking half-answer. Inject only completed work.

### Action step

1. Open `Sources/ListenToMeCore/Prompt.swift`. Find the listener's never-invent contract and the Quick pane's anti-preamble sentence. Copy both into your evidence log and write one sentence each on what breaks if the line is removed.
2. Open `Sources/ListenToMeCore/ModelRanking.swift` and trace `hasMarker("gemini-2.5-flash", "mini")` by hand; then compare with `"gemini-2.5-flash".contains("mini")`. Record both results.
3. Open `ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:204-221` and `ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:803-880`: follow `setModel` into `cancelResponse`, where the generation counter is bumped, and find where the stream loop checks it.
4. Run `ollama list`. In your evidence log, assign each of your installed models to Listener/Quick/Deep and justify each pick with the rules above. If `qwen3:0.6b` is all you have, pick one Quick and one Deep candidate from the appendix instead, and write the appendix's read date beside each pick.

## Segment M2.3 — Proactive intelligence without magic (~25 min)

### Objective

Implement proactive triggering with a deliberately simple heuristic behind a debounce, and treat streaming failures as typed, visible errors — automation under a budget, not on vibes.

### Lesson

"Proactive" sounds like it needs intelligence. It needs restraint. ListenToMe's question detector is 28 lines: `Sources/ListenToMeCore/QuestionDetector.swift` classifies a finalized utterance as a question if it ends in "?", *starts with* an interrogative (what, why, how, when, where, who, which, whose), or contains a phrase cue matched on word boundaries ("can you", "could you", "any thoughts", "walk me through", …). The design spec chose this on purpose: question detection is a "lightweight heuristic … Debounced so it fires at most once per N seconds. Kept deliberately simple; swappable later" (`docs/superpowers/specs/2026-06-18-listentome-design.md`, §4.4). Ship the cheap heuristic *behind a seam*, keep the option to swap in a classifier, and spend your complexity budget elsewhere.

The restraint comes from the gate. `ContextEngine.shouldFireProactive(for:now:)` fires only when the segment is finalized, came from `.others` (someone asking *you* — not you talking to yourself), passes question detection, **and** at least `debounce` seconds (default 8) have passed since the last fire (`ListenToMe/Sources/ListenToMeCore/ContextEngine.swift:8, 41-50`). Without the debounce, two heated minutes of questions would flood the pane with overlapping suggestions. One trigger, one answer, then quiet.

**Streaming with typed errors.** `OllamaProvider` POSTs to `/api/chat` with `stream: true` and reads the response as NDJSON lines — each line a JSON object carrying a message delta or `done: true` (`ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:159-177`; the `lineSource` is injectable so tests feed canned lines: `ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:42-50`). Three details make this production-grade:

1. **In-stream error events.** Ollama can answer HTTP 200 and then send `{"error": "..."}` mid-stream. The provider parses every line and throws `OllamaStreamError.server(error)` when it finds one (`ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:84-86`).
2. **Completion flags.** The stream loop tracks `completed` (saw `done: true`) and `producedContent` (yielded at least one non-whitespace delta). If the lines end without `done`, it throws `.incomplete`; if the stream "completes" with no content, it throws `.empty`, or `.thinkingOnly` when the model sent only reasoning (`ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:79-104`). A truncated or empty stream therefore *cannot finish as success*.
3. **Typed cases.** `OllamaStreamError` has five cases — `.server(String)`, `.unreachable(String)`, `.incomplete`, `.empty`, `.thinkingOnly` — each with a user-facing message; `.incomplete` even tells you the partial text is kept (`ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:216-236`).

This design is a scar, not a guess. The September 2026 design-and-gap review found the *old* provider ignored in-stream Ollama errors and let "truncated/empty streams … finish as success" — gap G06, P0 — at a moment when the project showed 215 passing Core tests and 97.24% coverage (`ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md:5, 51`). The tests validated what was built; what was built was wrong. The fix was not more coverage — it was an honest failure model. The recurring misconception, "swallow stream errors to avoid UI flicker," is exactly backwards: the user gets a silently incomplete answer instead of a retry affordance. Flicker is information; silence is a lie.

**Budgets come from observation.** Automatic Quick evaluations run with `LLMRequest.Purpose.quickEvaluation`, which forces `think: false`, temperature 0, and a 3,072-token output cap (`ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:62-63`). Why 3,072? Live GLM testing "exposed planning text despite `think: false`, exhausting the former 1,600-token budget halfway through valid final JSON" — so Quick now allows 3,072 generated tokens and a 30-second deadline while keeping a 16-KiB response cap (`ListenToMe/docs/SHARED-LIVE-SUMMARY.md:102`). The number is not theory; it is the smallest budget that stopped an observed truncation. When your own caps break in live testing, raise them the same way — from evidence.

**Automation under budget.** The shared live-summary engine — `LiveSummaryScheduler`, `QuickSummaryContext`, `AutomaticReviewCoordinator` in Core, documented in `docs/SHARED-LIVE-SUMMARY.md` — is what "proactive" looks like in production: event-driven and bounded everywhere.

- Speech **batches for five seconds** before evaluation; a non-final hypothesis needs **24 trimmed characters** to be eligible (`ListenToMe/docs/SHARED-LIVE-SUMMARY.md:8-10`; the threshold is `ConversationStore.provisionalMinimumCharacters`, `ListenToMe/Sources/ListenToMeCore/ConversationStore.swift:89-92`, applied in `ListenToMe/Sources/ListenToMeCore/QuickSummaryContext.swift:65-66`).
- **Unchanged input does not poll** — "Timers exist only for queued work or a failed request" (`ListenToMe/Sources/ListenToMeCore/AutomaticReviewCoordinator.swift:59`).
- Responses cap at **30 seconds / 16 KiB** (`ListenToMe/docs/SHARED-LIVE-SUMMARY.md:31`).
- When a Quick evaluation recommends it, full **Summary** and **Deep** reviews run **serially** — Summary at most every 30 s, Deep every 60 s; the first eligible review starts immediately, and unchanged input cannot regenerate a completed review (`ListenToMe/Sources/ListenToMeCore/AutomaticReviewCoordinator.swift:107`; `ListenToMe/docs/SHARED-LIVE-SUMMARY.md:96`).

Every number here is a cost ceiling, not a feature. That is the segment's takeaway: proactive intelligence is 5% trigger — a 28-line heuristic — and 95% discipline: debounces, budgets, caps, typed failures.

### Action step

1. Open `Sources/ListenToMeCore/QuestionDetector.swift` and list its three rules, noting which rule requires the cue at the *start* of the utterance.
2. Open `Sources/ListenToMeCore/OllamaProvider.swift` and find the two booleans that make truncated and empty streams fail. Then write in your evidence log: a stream yields "The best ans" and ends without `done` — which `OllamaStreamError` case fires, and what does the user see?
3. Open `docs/SHARED-LIVE-SUMMARY.md` and find the sentence explaining why the quick-evaluation budget is 3,072 tokens.
4. Audit your own product idea: write its proactive trigger, its debounce window, and its per-response budget — three numbers, no adjectives.

## Recap

- **M2.1** — The pipeline is capture → transcribe → store/context → prompt → route. Platform glue lives in `App/`; every decision lives in pure Core behind `AudioCapturing`, `Transcribing`, `LLMProvider`. Three transcription engines swap behind one seam; `ConversationStore.recentContext` enforces a character budget (default 4,000) that always keeps at least the newest segment; a 37-line VAD segments utterances when the engine can't. The split is platform-neutral: Apple, Windows and Android each ship an on-device stack that can fill the same seams, and each leaves availability checks, budgets and error messages to you.
- **M2.2** — Three roles (Listener/Quick/Deep) get different models: local-first `roleDefaults` (fast→Quick, strong→Deep, distinct fast→Listener), token-prefix matching rejects the "gemini ⊃ mini" false hit, and generation tokens cancel stale streams on model switch. `PromptBuilder` is pure — anti-preamble Quick, never-invent Listener, depth-over-brevity Deep — with 9 response actions and persona directives threaded through every pane. Only *completed* listener summaries ground Quick/Deep. The model survey lives in a dated appendix; `qwen3:0.6b` stays the lab default.
- **M2.3** — Proactive = a 28-line question heuristic behind a seam, gated by an 8-second debounce on finalized `.others` segments. Streaming errors are typed (`.server`/`.incomplete`/`.empty`) so truncation can't pass as success — the fix for gap G06. Budgets (3,072 quick tokens, 5 s batches, 24-char eligibility, 30 s/16 KiB caps, 30 s/60 s review spacing) come from observed failures, not guesses.

## Discussion prompt

Post your answer to the community: a stakeholder proposes your copilot "should just know when to help — point the biggest model at it and let it decide." Using this module's evidence (cite at least three ListenToMe files), write a ~150-word reply naming (a) what the trigger would actually be, (b) what debounce and budget you would put around it, and (c) which failure mode your design prevents that theirs doesn't.