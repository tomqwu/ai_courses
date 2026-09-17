# Quiz M2 — The On-Device AI App: Architecture
> Part of AI Product Studio (APS-3) · 8 questions (6 MC + 2 short answer) · Answer key included

**Q1.** A participant asks a question that triggers a proactive Quick response. Which order did the data flow through ListenToMe?

A. Capture → Store → Transcribe → Route → Prompt
B. Capture → Transcribe → Store → Context/Prompt → Route
C. Transcribe → Capture → Route → Store → Prompt
D. Capture → Route → Transcribe → Prompt → Store

**Q2.** ListenToMeCore holds a 96% coverage badge on a real-time audio product. What makes that possible?

A. CI provides microphone and system-audio hardware for the test jobs.
B. All decision logic lives in a pure SwiftPM package behind `AudioCapturing`/`Transcribing`/`LLMProvider` seams, so tests run against mocks with no hardware or network.
C. Coverage is measured only on `App/` glue, which is small.
D. The 95% floor script excludes any module that lacks tests.

**Q3.** In ListenToMe's Swift core, a local Ollama server has three models: `qwen3:0.6b`, `deepseek-v4-pro`, `gemini-2.5-flash`. What does `ModelRanking.roleDefaults` assign? (Answer for the Swift implementation. TinyCopilot's Python `role_defaults` deliberately simplifies this and gives Listener and Quick the same fastest model — for the lab, its tests are authoritative.)

A. All three roles get `deepseek-v4-pro` — the strongest model is best everywhere.
B. Quick = `gemini-2.5-flash` (fast marker), Deep = `deepseek-v4-pro` (strong marker), Listener = `qwen3:0.6b` (the lightest model left once Quick and Deep are taken).
C. Listener = `deepseek-v4-pro` because it writes the longest output.
D. No defaults exist; the user must pick all three panes manually.

**Q4.** `MeetingSession` keeps a per-role `responseGenerations` counter. What is it for?

A. Billing — counting tokens generated per role.
B. Invalidating the in-flight stream when the role's model changes, so a stale answer can't display under the new model's name.
C. Restarting the Ollama daemon after a model switch.
D. Queuing the old stream's tokens until the new model finishes, then merging them.

**Q5.** You are tracing capture → transcribe → context → prompt in the cloned repo. Which option names the file that *implements* each stage?

A. Capture: `Sources/ListenToMeCore/Capture.swift` · transcription: `Sources/ListenToMeCore/Transcriber.swift` · transcript log + context window: `Sources/ListenToMeCore/ConversationStore.swift` · prompt strings: `Sources/ListenToMeCore/ContextEngine.swift`
B. Capture: `App/DualChannelCapture.swift` · transcription: `App/SpeechAnalyzerTranscriber.swift` (and the two alternates) behind the `Transcribing` seam · transcript log + context window: `Sources/ListenToMeCore/ConversationStore.swift` · prompt strings: `Sources/ListenToMeCore/Prompt.swift`
C. All four in `App/MeetingView.swift` — capture, transcription, the store and the prompts stay in the view that displays them, so the pipeline reads top to bottom in one file.
D. Capture: `App/DualChannelCapture.swift` · transcription: `Sources/ListenToMeCore/VAD.swift` · transcript log: `Sources/ListenToMeCore/MeetingSession.swift` · prompt strings: `Sources/ListenToMeCore/ModelRouter.swift`

**Q6.** Why does the Listener system prompt say "Never invent an owner, deadline, agreement, or completion. Mark missing details as unstated"?

A. To keep the rolling summary under the 3,072-token budget.
B. Local Ollama models cannot copy names out of transcripts reliably, so naming anyone is unsafe.
C. The Listener summary is injected into Quick/Deep prompts, so an invented commitment would propagate into every downstream answer; the paired rule is that only *completed* summaries are injected.
D. Meeting-transcription law requires marking unstated details.

**Q7.** A tester reports: "The Quick pane showed a 40-token answer as finished, but the model had stopped mid-sentence — the NDJSON stream ended with no `done: true` line." Using the typed-error design in `OllamaProvider.streamEvents`, name the `OllamaStreamError` case this is, state what the provider must do instead of returning the partial text as a completed answer, and write the one unit test (TinyCopilot or Swift) that would have caught it.

**Q8.** Two bug reports on your proactive Quick trigger: (1) during a rapid-fire Q&A it fired three times in ten seconds; (2) it once answered a question *you* asked, not a participant. Using the guard in `ContextEngine.shouldFireProactive`, name the condition each report violates, name the one condition neither report mentions, and write the two unit-test cases that pin the fix.

---

## Answer key

**Q1 — B.** Chunks flow capture → `Transcribing` seam → `ConversationStore` → prompt assembly → per-role provider; nothing skips or reorders the store. *(Objective: M2.1 pipeline — `docs/superpowers/specs/2026-06-18-listentome-design.md` §3, §5.)*

**Q2 — B.** Every decision lives in the pure core behind the three protocol seams, so the suite runs against mocks — no hardware, no network. *(Objective: M2.1 protocol seams — `Sources/ListenToMeCore/Transcriber.swift`, `README.md` badge.)*

**Q3 — B.** Swift picks per role from the ranked pool: the first fast-marker match → Quick, the strongest strong-marker match excluding Quick's pick → Deep, then Listener = a second fast pick or, failing that, the lightest model remaining — here `qwen3:0.6b`. TinyCopilot's `role_defaults` maps `listener` and `quick` to the same fastest model on purpose (`tinycopilot/src/tinycopilot/model_router.py:176`), so do not carry this answer into the lab. *(Objective: M2.2 role routing — `ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:49-53` for the markers, `ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:91-111` for the picks.)*

**Q4 — B.** `setModel` bumps the generation; the stream loop guards every write with it, so stale tokens can't land after a switch. *(Objective: M2.2 stale-stream cancellation — `Sources/ListenToMeCore/MeetingSession.swift` lines 119–132, 513–578.)*

**Q5 — B.** Core declares the seams; App supplies the implementations. `Capture.swift` is the `AudioCapturing` protocol and says so — "Real impl lives in the app target" (`ListenToMe/Sources/ListenToMeCore/Capture.swift:3-9`) — which the mic + ScreenCaptureKit tap in `ListenToMe/App/DualChannelCapture.swift:8-10` provides; `Transcriber.swift:4` declares `Transcribing` and the three engines sit in `App/` behind it. The log and the never-empty context window are `ConversationStore.recentContext` (`ListenToMe/Sources/ListenToMeCore/ConversationStore.swift:76-87`); the prompt strings are built by the pure `PromptBuilder` (`ListenToMe/Sources/ListenToMeCore/Prompt.swift:87`). A mistakes the two protocol files for implementations and puts prompts in `ContextEngine.swift`, which only "assembles prompt context and decides when to fire a proactive suggestion" (`ListenToMe/Sources/ListenToMeCore/ContextEngine.swift:3`). C is the un-layered shape this segment argues against — a view that owns the pipeline cannot be unit-tested, and the 96% core badge depends on it not doing that. D swaps in three files that do other jobs: `VAD.swift` finds utterance boundaries by energy and silence, `MeetingSession.swift` owns per-role routing and cancellation, and `ModelRouter.swift` "holds the registered providers and routes streaming requests to the active one" (`ListenToMe/Sources/ListenToMeCore/ModelRouter.swift:4-6`). *(Objective: M2.1 name the file that implements each stage — `ListenToMe/Sources/ListenToMeCore/Capture.swift:3-9`; `ListenToMe/Sources/ListenToMeCore/Transcriber.swift:4`; `ListenToMe/App/DualChannelCapture.swift:8-10`; `ListenToMe/Sources/ListenToMeCore/ConversationStore.swift:76-87`; `ListenToMe/Sources/ListenToMeCore/Prompt.swift:87`.)*

**Q6 — C.** The Listener summary grounds every downstream pane, so an invented commitment would propagate; only `lastCompletedListenerSummary` is injected. *(Objective: M2.2 never-invent contract — `Prompt.swift` lines 73–81.)*

**Q7 — Acceptable answer:** `.incomplete` — the line source ended without a `done: true` event (thrown at `ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:101`; the enum is at `ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:216-224`). The provider must *throw* it, so the stream finishes with an error the pane shows ("The response ended before completion. Partial text is kept; retry the request.") and never as success — swallowing it turns truncation into apparent completion, gap G06's exact finding. Test: a fake transport yields content lines and then closes without `done: true`; assert the provider raises `IncompleteStreamError` (`tinycopilot/src/tinycopilot/ollama_provider.py:31`) or `OllamaStreamError.incomplete`, rather than returning the partial string. *(Objective: M2.3 typed streaming errors.)*

**Q8 — Acceptable answer:** (1) violates the 8-second debounce — at most one fire per window (`now - lastFire >= debounce`); (2) violates `segment.source == .others` — your own questions never fire. The condition neither report mentions is `segment.isFinal` (the detector must also classify the text as a question). Tests: two final `.others` questions 3 s apart → the second call returns `false`; a final question from `.you` → `false`. *(Objective: M2.3 bounded proactive triggers — `ListenToMe/Sources/ListenToMeCore/ContextEngine.swift:41-50`; TinyCopilot's `QuestionDetector.should_fire` in `tinycopilot/src/tinycopilot/question_detector.py` applies the same four checks.)*
## Objective → assessment map

Every "By the end of this module you can" line in `course/03-content/m02-ondevice-app/lesson.md`, and what checks it.

| Objective (lesson.md) | Checked by |
|---|---|
| Explain and sketch the capture → transcribe → context → prompt → route pipeline, and name the file that implements each stage | Q1 (stage order), Q5 (the file per stage, seam vs implementation); Lab M2 rebuilds the same stages in `tinycopilot/src/tinycopilot/` |
| Justify the three protocol seams, and implement a conversation store with a character-budgeted context window that always keeps at least the newest segment | Q2 (why the seams make a 96% badge possible); Lab M2 `conversation_store.py` and its tests inside `make lab-m2` (201 passed) |
| Route different models to different roles with local-first defaults, token-prefix matching, and stale-stream cancellation on model switch | Q3 (role defaults), Q4 (the per-role generation counter); Lab M2 `model_router.py` |
| Write prompt builders as pure functions — including a "never invent" grounding contract and an anti-preamble style | Q6 (why the Listener contract is load-bearing downstream); Lab M2 `prompts.py`, asserted string-for-string |
| Add proactive behavior with a deliberately simple question detector behind a debounce | Q8 (which guard condition each bug violates, and the two tests that pin the fix); Lab M2 `question_detector.py` |
| Type streaming errors so a truncated or empty response can never finish as success | Q7 (name the case, what the provider must do, and the test that catches it); Lab M2 `ollama_provider.py`, Lab M3 Step 1 |
