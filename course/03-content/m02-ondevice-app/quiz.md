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

**Q3.** A local Ollama server has three models: `qwen3:0.6b`, `deepseek-v4-pro`, `gemini-2.5-flash`. What does `ModelRanking.roleDefaults` assign?

A. All three roles get `deepseek-v4-pro` — the strongest model is best everywhere.
B. Quick = `gemini-2.5-flash` (fast marker), Deep = `deepseek-v4-pro` (strong marker), Listener = `qwen3:0.6b` (a distinct fast/light pick).
C. Listener = `deepseek-v4-pro` because it writes the longest output.
D. No defaults exist; the user must pick all three panes manually.

**Q4.** `MeetingSession` keeps a per-role `responseGenerations` counter. What is it for?

A. Billing — counting tokens generated per role.
B. Invalidating the in-flight stream when the role's model changes, so a stale answer can't display under the new model's name.
C. Restarting the Ollama daemon after a model switch.
D. Queuing the old stream's tokens until the new model finishes, then merging them.

**Q5.** `PromptBuilder` is a pure enum of static functions with no I/O. Why is that the right shape?

A. Swift enums compile faster than classes.
B. Prompts become exactly assertable unit-test output — `PromptBuilderTests` checks built strings with no LLM, network, or model.
C. It lets each provider rewrite the base system prompts at request time.
D. Purity is required by the Swift 6 compiler.

**Q6.** Why does the Listener system prompt say "Never invent an owner, deadline, agreement, or completion. Mark missing details as unstated"?

A. To keep the rolling summary under the 3,072-token budget.
B. Local Ollama models cannot copy names out of transcripts reliably, so naming anyone is unsafe.
C. The Listener summary is injected into Quick/Deep prompts, so an invented commitment would propagate into every downstream answer; the paired rule is that only *completed* summaries are injected.
D. Meeting-transcription law requires marking unstated details.

**Q7.** Name `OllamaStreamError`'s three cases and the condition that triggers each. Then explain in one sentence why "catch stream errors silently to avoid UI flicker" is rejected by this design.

**Q8.** `QuestionDetector` alone would flag every question-like utterance. What does the 8-second debounce in `ContextEngine.shouldFireProactive` prevent, and what two other conditions must hold before a proactive response fires?

---

## Answer key

**Q1 — B.** Chunks flow capture → `Transcribing` seam → `ConversationStore` → prompt assembly → per-role provider; nothing skips or reorders the store. *(Objective: M2.1 pipeline — `docs/superpowers/specs/2026-06-18-listentome-design.md` §3, §5.)*

**Q2 — B.** Every decision lives in the pure core behind the three protocol seams, so the suite runs against mocks — no hardware, no network. *(Objective: M2.1 protocol seams — `Sources/ListenToMeCore/Transcriber.swift`, `README.md` badge.)*

**Q3 — B.** Defaults match capability markers per role — fast→Quick, strong→Deep (excluding Quick's pick), a distinct fast model→Listener. *(Objective: M2.2 role routing — `Sources/ListenToMeCore/ModelRanking.swift` lines 49–94.)*

**Q4 — B.** `setModel` bumps the generation; the stream loop guards every write with it, so stale tokens can't land after a switch. *(Objective: M2.2 stale-stream cancellation — `Sources/ListenToMeCore/MeetingSession.swift` lines 119–132, 513–578.)*

**Q5 — B.** Purity makes the built prompt a deterministic function of context — assertable string-for-string with no model. *(Objective: M2.2 pure prompt builders — `Sources/ListenToMeCore/Prompt.swift`, `Tests/ListenToMeCoreTests/PromptBuilderTests.swift`.)*

**Q6 — C.** The Listener summary grounds every downstream pane, so an invented commitment would propagate; only `lastCompletedListenerSummary` is injected. *(Objective: M2.2 never-invent contract — `Prompt.swift` lines 73–81.)*

**Q7 — Acceptable answer:** `.server` — an in-stream `{"error": ...}` event; `.incomplete` — the lines ended without `done: true`; `.empty` — completed with no non-whitespace content. Swallowing errors is rejected because it turns truncation into apparent success — gap G06's exact finding. *(Objective: M2.3 typed streaming errors — `Sources/ListenToMeCore/OllamaProvider.swift` lines 67–83, 159–170.)*

**Q8 — Acceptable answer:** Flooding — several questions in quick succession fire at most one proactive response per 8-second window; the segment must also be finalized and from `.others` (and pass detection). *(Objective: M2.3 bounded proactive triggers — `Sources/ListenToMeCore/ContextEngine.swift` lines 31–40.)*