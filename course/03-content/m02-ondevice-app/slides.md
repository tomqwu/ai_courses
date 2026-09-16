---
marp: true
theme: aps
paginate: true
title: M2 — The On-Device AI App: Architecture
---

<!-- _class: lead -->

# M2 — The On-Device AI App: Architecture

**Promise:** trace one real on-device pipeline, then rebuild its core.
**Duration:** ~75 min lesson + ~3 h lab.

<!-- NOTES: Welcome to Module 2. Today the abstraction ends: we open ListenToMe, a shipped macOS meeting copilot, and read the actual pipeline it runs. Then in the lab you rebuild that core in Python as TinyCopilot until 191 tests pass. By the end of this module you will be able to point at a Swift file for every stage and defend each decision. (45 seconds; move to objectives.) -->

---

## By the end you can…

- Sketch capture → transcribe → context → prompt → route.
- Name the file implementing each stage.
- Justify three protocol seams.
- Route models per role, cancel stale streams.
- Write prompt builders as pure functions.
- Type streaming errors so truncation fails loudly.

<!-- NOTES: These six bullets are the whole contract of this module. Notice what is not here: no mention of prompt engineering tricks or model benchmarks. This module is about architecture — where decisions live and how they are proved. Each objective maps to one lab step and to at least one quiz question. If you can do these six things, Lab M2 is passable today. (60 seconds; then open M2.1.) -->

---

## M2.1 — One pipeline, two layers

<!-- _diagram: stack -->

- mic (.you) · system audio (.others)
- PCM chunks
- capture → transcribe → store → context → prompt → route
- seam: capture · transcribe · prompt
- App/ glue · Core (pure)

<!-- NOTES: Read this left to right once, then say the split out loud: everything in `App/` touches hardware; everything in `Sources/ListenToMeCore` is pure. The three seams are `AudioCapturing`, `Transcribing`, and `LLMProvider`. The reason this matters is testability: the pipeline is fully runnable in a unit test against mocks. Hold the diagram; we now walk each layer. (75 seconds; next slide is capture.) -->

---

## Capture is thin on purpose

- `App/DualChannelCapture.swift` taps mic and system audio.
- Two channels: `.you`, `.others`.
- Mono Float PCM → `AudioChunk`s.
- Speaker attribution for free — no diarization model.
- Least testable code, so it is thinnest.

<!-- NOTES: The header comment on `App/DualChannelCapture.swift:8` says both sources are converted to mono Float PCM and emitted as audio chunks. At line 102 the mic tap tags buffers `.you`; at line 212 the ScreenCaptureKit callback tags them `.others`. That one tag is why the app can label "You" versus "Others" without any diarization. Capture is hardware-bound, so it is kept as small as possible — a rule we will reuse in the lab. (70 seconds; move to the seams.) -->

---

## Three protocol seams

| Seam | Core declares | App provides |
|---|---|---|
| `AudioCapturing` | what audio arrives | AVAudioEngine, ScreenCaptureKit |
| `Transcribing` | partials and finals | SpeechAnalyzer, WhisperKit |
| `LLMProvider` | streamed text | Ollama HTTP client |

```swift
public protocol AudioCapturing: Sendable {
    var statusUpdates: AsyncStream<CaptureStatus> { get }
    var chunks: AsyncStream<AudioChunk> { get }
    func start() async throws
    func stop()
}
public protocol LLMProvider: Sendable {
    var id: String { get }
    func stream(_ request: LLMRequest) -> AsyncThrowingStream<String, Error>
}
```

`ListenToMe/Sources/ListenToMeCore/Capture.swift:4` · `LLMProvider.swift:4`

<!-- NOTES: A seam is a protocol the pure core owns and the platform side implements. Core never names AVFoundation or Ollama; it only names these three protocols. That inversion is what lets the test suite inject mocks. The pay-off: if we add a fourth transcription engine tomorrow, nothing below the `Transcribing` protocol changes — not the store, not the prompts, not the router. (75 seconds; next we look inside the transcription seam.) -->

---

## Three engines, one seam

- **SpeechAnalyzer** — default; one analyzer per source.
- **SpeechRecognizer** — legacy; process-global limit.
- **WhisperKit** — opt-in; batch, finalized segments only.
- Apple Speech picks one language; no code-switching.
- Add an engine; nothing downstream changes.

<!-- NOTES: `Sources/ListenToMeCore/Transcriber.swift` defines `prepare()`, `feed(_:)`, `finish()`. The `prepare()` contract matters: warm up before audio so `feed` never blocks and the meeting's opening seconds are not dropped. `App/SpeechAnalyzerTranscriber.swift:6-39` notes one analyzer per source, unlike `SFSpeechRecognizer`. WhisperKit trades live partials for stronger multilingual quality — `App/MeetingView.swift:84` is why: Apple's on-device Speech selects one primary language. (80 seconds; next the store.) -->

---

## The store and its budget

- `ConversationStore.swift` is the single source of truth.
- Finals log plus one current partial.
- `recentContext(maxChars:)` walks newest-first.
- Always keeps the newest, even over budget.
- Default budget: 4,000 characters.
- Recap and action items get 100,000.

```swift
public func buildContext(from store: ConversationStore, notes: String?,
                         maxChars: Int = 4000, summary: String? = nil,
                         responseLanguage: String? = nil, references: String? = nil,
                         personaGuidance: String? = nil) -> PromptContext
```

`ListenToMe/Sources/ListenToMeCore/ContextEngine.swift:12`

<!-- NOTES: `apply(_:)` appends finals and replaces partials. The window function walks utterances newest-first, keeping each while it fits, and always includes the most recent one even if it alone exceeds the budget — the window is never empty (`ConversationStore.swift:56-67`). The default is 4,000 characters (`ContextEngine.swift:12`), but `MeetingSession.transcriptBudget(for:)` raises recap and action-item prompts to 100,000 because they must cover the whole conversation (`MeetingSession.swift:419-427`). (85 seconds; a quick word on segmentation.) -->

---

## When the engine gives no partials

- Core VAD is 37 lines.
- `rms(of:)` measures frame energy.
- Threshold 0.02, trailing silence 0.8 s.
- Fires exactly once per utterance boundary.
- No ML model — a threshold and a timer.

<!-- NOTES: WhisperKit buffers audio, so something must decide where an utterance ends. `Sources/ListenToMeCore/VAD.swift` computes root-mean-square energy per frame and returns true exactly once, on the frame where trailing silence after speech first exceeds the silence duration. Verified by `Tests/ListenToMeCoreTests/VADTests.swift`. This is the module's recurring move: spend the cheap heuristic where a model would be overkill. (70 seconds; time for the proof slide.) -->

---

<!-- _class: proof -->

## The newest segment always survives

- `ListenToMe/Sources/ListenToMeCore/ConversationStore.swift:56-67`
- Newest-first fit, budget-bounded window.
- Guarantee: never an empty context.
- Default 4,000 chars — `ListenToMe/Sources/ListenToMeCore/ContextEngine.swift:12`.
- Why it pays: 96% core coverage, 95% floor.

```swift
public func recentContext(maxChars: Int) -> [TranscriptSegment] {
    var total = 0
    var collected: [TranscriptSegment] = []
    for segment in utterances.reversed() {
        // Always include the most recent; otherwise stop before exceeding the budget.
        if !collected.isEmpty && total + segment.text.count > maxChars { break }
        total += segment.text.count
        collected.append(segment)
    }
    return collected.reversed()
}
```

<!-- NOTES: This is the first proof slide. Open the file and read the loop aloud rather than trusting these bullets. The point of the proof slide in this course is that every claim has a file pointer you can open, and that the pointer resolves. The 96% coverage badge and the 95% floor in `scripts/check-coverage.sh` are downstream consequences of this kind of layering. (70 seconds; transition to routing.) -->

---

## M2.2 — Three roles, three models

| Role | Job | Wants |
|---|---|---|
| Listener | rolling summary | speed |
| Quick | hotkey, proactive | speed |
| Deep | long reasoning | strength |

- Four panes: Transcript, Listener, Quick, Deep.
- Each pane has its own model dropdown.

<!-- NOTES: Roles are an enum — `listener`, `quick`, `deep` in `Sources/ListenToMeCore/CopilotRole.swift` — not a UI accident. Quick answers on a global hotkey and fires proactively, so latency is the whole game. Deep is on-demand long reasoning. Listener auto-refreshes continuously, so speed beats depth. "Just use the best model everywhere" fails twice: it burns latency where it isn't needed and pins the product to one model's quirks. (75 seconds; next, the defaults.) -->

---

## Local-first role defaults

- `ModelRanking.roleDefaults(from:)` picks automatically.
- Quick gets a fast marker — or lightest.
- Deep gets a strong marker — or heaviest.
- `:cloud` filtered out of auto-selection.
- Cloud only when no local model exists.

<!-- NOTES: The logic lives in `Sources/ListenToMeCore/ModelRanking.swift:76-94`, called from `App/MeetingView.swift:717`. Fast markers include flash, mini, nano, lite, small, fast; strong markers include pro, reason, think, coder, code, ultra, max, large. The local-first filter at lines 72-79 is a privacy default, not a speed one: an unpinned pane must never silently send a transcript to Ollama Cloud. The "good for" hints come from `describe(_:)` at lines 101-141. (80 seconds; now the subtle bug.) -->

---

## Token-prefix, not substring

- Split the model name into tokens.
- A marker matches only at a token start.
- `"gemini-2.5-flash"` contains `"mini"`.
- Token check rejects it; substring accepts it.
- One wrong check misroutes a whole family.

```swift
static func tokens(_ model: String) -> [String] {
    model.lowercased().split(whereSeparator: { "-:./ ".contains($0) }).map(String.init)
}
static func hasMarker(_ model: String, _ marker: String) -> Bool {
    tokens(model).contains { $0.hasPrefix(marker) }
}
```

`ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:7-18`

<!-- NOTES: `ModelRanking.swift:13-18` documents this: token-prefix matching, not raw substring, rejects cross-token false hits like gemini containing mini. A raw `contains("mini")` would rank every Gemini model as fast, and your Quick defaults would be quietly wrong for an entire model family — with no test failing unless you wrote the near-miss test. TinyCopilot's `test_gemini_is_not_demoted_as_mini` is exactly that test. (70 seconds; now cancellation.) -->

---

## Generation tokens kill stale streams

- `MeetingSession` keeps a generation counter per role.
- `setModel(_:_)` cancels in-flight work and bumps it.
- The stream loop guards every write.
- Switch mid-answer: old tokens die on the floor.
- Without it, yesterday's model answers under today's name.

<!-- NOTES: `MeetingSession.swift:119-132` is where `setModel` bumps the counter; lines 513-578 are where the streaming loop checks it before every write. The failure this prevents is subtle and embarrassing: a slow answer from the old model finishes after the switch and displays under the new model's name. Users read that as the new model being wrong. Cancellation is a correctness feature, not an optimization. (75 seconds; next, prompts.) -->

---

## PromptBuilder is pure

- `Prompt.swift` — a public enum, static functions.
- Zero I/O, zero state, zero clock.
- Context in, `LLMRequest` out.
- Same inputs, same string, always.
- Tests assert the built text; no model needed.

<!-- NOTES: Purity is not a style preference here. `Tests/ListenToMeCoreTests/PromptBuilderTests.swift` checks built strings directly, so prompt regressions are caught in milliseconds without a network call or a model. That is the only way to keep nine response actions across three roles honest. When you write TinyCopilot's `prompts.py`, any hidden state or randomness will fail the determinism test in `test_prompts.py`. (70 seconds; three base prompts next.) -->

---

## Three base prompts, three contracts

- **Quick:** no preamble, answer in 1–3 sentences.
- **Listener:** never invent owner, deadline, agreement, completion.
- **Deep:** depth over brevity; no padding.
- Nine response actions layer on top.
- Persona directives append to every role.

<!-- NOTES: Read the actual sentences in `Prompt.swift`: Quick at lines 65-71, Listener at 73-81, Deep at 83-88. The Listener contract exists because its summary feeds back into Quick and Deep prompts — one hallucinated owner would propagate everywhere, so it is blocked at the source. `systemWithDirectives` at lines 159-173 appends persona and language to every pane, so a preset like Interview shapes all three roles identically. (80 seconds; proof slide.) -->

---

<!-- _class: proof -->

## Only completed summaries ground other roles

- `ListenToMe/Sources/ListenToMeCore/Prompt.swift:73-81` — never-invent contract.
- `ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:40-43` — two summary fields.
- `lastCompletedListenerSummary` — injected, safe.
- In-flight `listenerSummary` — display only, never injected.
- A half-answer is worse than no answer.

<!-- NOTES: Open `MeetingSession.swift:40-43` and note there are two properties, not one. The live display value is cleared while a refresh streams; the completed value is separate and is what gets injected at lines 435 and 449. The misconception to kill here is "more context is better, inject whatever is on screen." An in-flight summary is a confident-looking half-answer, and Quick would treat it as fact. (75 seconds; M2.3.) -->

---

## M2.3 — Proactive is restraint

- Question detection is 28 lines.
- Deliberately simple; swappable later.
- Ship the cheap heuristic behind a seam.
- Spend complexity elsewhere.
- Trigger is 5%; discipline is 95%.

<!-- NOTES: "Proactive" sounds like it needs intelligence; it needs restraint. `Sources/ListenToMeCore/QuestionDetector.swift` is 28 lines. The design spec at `docs/superpowers/specs/2026-06-18-listentome-design.md` §4.4 says question detection is a lightweight heuristic, debounced so it fires at most once per N seconds, kept deliberately simple and swappable later. The lesson is to make the trigger a seam and put your effort into the gates around it. (75 seconds; the three rules.) -->

---

## QuestionDetector: three rules

- Ends in `?`.
- *Starts with* an interrogative: what, why, how…
- Contains a word-boundary phrase cue.
- `"can you"`, `"any thoughts"`, `"walk me through"`.
- Near-misses must not fire: "however", "whatsapp".

<!-- NOTES: The word "starts" is load-bearing: the interrogative rule applies only to the first token. Phrase cues are matched on word boundaries, so "many thoughts" never triggers "any thoughts", and "we cannot use your laptop" never triggers "can you". These near-misses are the tests students most often forget to write. In TinyCopilot, `test_question_detector.py` ships them for you — eight explicit near-miss strings. (70 seconds; the gate.) -->

---

## The gate: finalized, others, debounced

- Segment must be **finalized**.
- Must come from `.others`.
- Must pass detection.
- At least 8 seconds since last fire.
- One trigger, one answer, then quiet.

<!-- NOTES: `ContextEngine.shouldFireProactive(for:now:)` at `Sources/ListenToMeCore/ContextEngine.swift:31-40` is all four conditions, with the debounce default of 8 seconds at line 8. The `.others` condition is the one people miss: you do not want the app answering your own rhetorical questions. Without the debounce, two heated minutes of questions flood the pane with overlapping suggestions. (70 seconds; now failures.) -->

---

## Typed streaming errors

- Ollama streams NDJSON over `/api/chat`.
- It can return HTTP 200, then `{"error": ...}`.
- `.server` — in-stream error event.
- `.incomplete` — lines ended without `done: true`.
- `.empty` — completed with no visible text.
- Truncation can never finish as success.

```swift
public enum OllamaStreamError: LocalizedError {
    case server(String)
    case incomplete
    case empty
}
```

`ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:159-168`

<!-- NOTES: `Sources/ListenToMeCore/OllamaProvider.swift:120-139` reads NDJSON lines; the line source is injectable so tests feed canned lines. The loop tracks `completed` and `producedContent` at lines 67-83. Three typed cases live at lines 159-170, each with a user-facing message. This design is a scar, not a guess: the September 2026 review found the old provider let truncated streams finish as success — gap G06, P0 — while the project showed 215 passing core tests and 97.24% coverage. (85 seconds; proof slide.) -->

---

<!-- _class: proof -->

## Flicker is information; silence is a lie

- `ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:67-83`
- Two booleans: completion flag, content flag.
- `ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md` — gap G06.
- Old provider: truncated streams finished as success.
- Tests passed; the failure model was wrong.

<!-- NOTES: Open the review and read gap G06. The suite validated what was built; what was built was wrong. The fix was not more coverage but an honest failure model. The recurring misconception — "swallow stream errors to avoid UI flicker" — is exactly backwards: the user gets a silently incomplete answer instead of a retry affordance. Say the line on the slide out loud: flicker is information, silence is a lie. (75 seconds; budgets.) -->

---

## Budgets come from observation

- Quick evaluation: `think: false`, temperature 0.
- 3,072-token cap — chosen from a real truncation.
- 5-second speech batches; 24-char eligibility.
- 30-second / 16 KiB response caps.
- Summary every 30 s, Deep every 60 s, serially.
- Every number is a cost ceiling, not a feature.

<!-- NOTES: `OllamaProvider.swift:49-51` forces `think: false`, temperature 0, and a 3,072-token cap for quick evaluations. Why 3,072? `docs/SHARED-LIVE-SUMMARY.md` line 66 records that live GLM testing exposed planning text despite `think: false`, exhausting the former 1,600-token budget halfway through valid JSON. The cap is the smallest budget that stopped an observed truncation. The shared live-summary engine is documented in the same file: batches, eligibility, caps, serialized reviews. (85 seconds; the lab.) -->

---

## Lab M2 — Build TinyCopilot's core

- Delete six Python modules; re-implement TDD-style.
- Tests are the spec; the reference is the answer key.
- `make lab-m2` → 191 passed, 100% coverage.
- Floor 90 enforced; `make lab-m3` → 49 passed.
- `make demo` → three role outputs from a real model.

<!-- NOTES: Three hours. Six modules: conversation_store, question_detector, prompts, model_router, ollama_provider, copilot. Run the suite green first, read `copilot.py`, then delete one module at a time. Expect a collection error on deletion — that is the real red run — then read the test file for the per-test spec. Do not proceed to a green run without capturing the red one. Acceptance checklist is in `lab.md`. (75 seconds; quiz next.) -->

---

## Quiz M2 — eight questions

- Pipeline order; the coverage enabler.
- Role defaults on three installed models.
- Generation counters; prompt purity.
- The never-invent contract.
- Streaming error cases; debounce conditions.
- Short answers ask you to apply, not recall.

<!-- NOTES: Six multiple choice, two short answer. The distractors encode the misconceptions we taught against: "the strongest model is best everywhere", "localhost proves local", "queue the old stream's tokens". Answer keys cite the exact file pointer and objective. Do the quiz before the workshop; we review the two most-missed items live. (45 seconds; recap.) -->

---

## Recap

- **M2.1** One pipeline; pure Core, thin glue, three seams.
- **M2.2** Per-role models; token-prefix; generations cancel.
- **M2.3** Cheap heuristic, hard gate, typed errors.
- Every stage has a file pointer you can open.
- Every number is a measured ceiling.

<!-- NOTES: Three sentences for three segments. M2.1: decisions live in pure Core, hardware lives in thin glue. M2.2: routing is per role, matching is token-prefix, cancellation is a generation counter. M2.3: proactive is a 28-line heuristic behind an 8-second debounce, and streaming failures are typed so truncation is never success. If you remember one thing, remember that the architecture is what makes the honesty possible. (55 seconds; discussion.) -->

---

## Discussion prompt

- Stakeholder: "Point the biggest model at it."
- Name the trigger, debounce, budget.
- Cite at least three ListenToMe files.
- ~150 words; post to the community.
- Which failure mode does your design prevent?

<!-- NOTES: This is the week's community post and the completion lever. The strong answer names a concrete trigger (finalized `.others` question), an explicit debounce (8 seconds or a justified alternative), a per-response budget, and one failure mode the stakeholder's design loses — for example, no debounce means overlapping suggestions, or no typed errors means silent truncation. Require three file pointers; that is how we grade it. (50 seconds; end.) -->
