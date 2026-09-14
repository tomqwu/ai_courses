# M2 — Recording Scripts

> One script per lesson segment. Narration is written to be read aloud at ~130 wpm. Open every file
> pointer on screen; type every command. Recordings live behind lifetime access.

## Segment M2.1 — The capture→transcribe→context→prompt→route pipeline

**Target runtime:** 5:30 (≈715 words). **Pre-work for the viewer:** clone ListenToMe and run
`make lab-m2` in `tinycopilot/` once.

**Cold open (~15 s).** A real-time meeting copilot holds a 96% coverage badge. It cannot run a
microphone, a screen-capture stream, or an LLM in CI. So where can 96% come from? Answer: almost all
of its decisions were put somewhere a test can reach.

| Timestamp | On screen | Narration |
|---|---|---|
| 0:00 | `ListenToMe/README.md` | This is ListenToMe, a free on-device meeting copilot for macOS. Two audio channels, live transcription, three AI panes. |
| 0:15 | Architecture diagram from the design spec | The shipped design is one process: audio and speech run off the main actor, and the UI only observes published state. |
| 0:35 | `ListenToMe/Sources/ListenToMeCore/` file list | Here is the split. `Sources/ListenToMeCore` is a pure SwiftPM package, 33 modules, no microphone and no network. `App/` is platform glue. |
| 1:00 | `App/DualChannelCapture.swift` line 8 | Capture taps the mic and creates a ScreenCaptureKit stream, converting both to mono Float PCM and emitting audio chunks. |
| 1:25 | Lines 102 and 212 | The mic tap tags buffers `.you`; the ScreenCaptureKit callback tags `.others`. One tag gives speaker attribution with no diarization model. |
| 1:45 | `Sources/ListenToMeCore/Transcriber.swift` | The `Transcribing` protocol declares `prepare`, `feed`, and `finish`. `prepare` warms the pipeline before audio arrives, so the first seconds of a meeting are not dropped. |
| 2:10 | `App/SpeechAnalyzerTranscriber.swift` lines 6–39 | Three engines sit behind that one protocol: SpeechAnalyzer by default, the legacy `SFSpeechRecognizer`, and opt-in WhisperKit. |
| 2:35 | `Sources/ListenToMeCore/ConversationStore.swift` lines 56–67 | The store keeps an ordered log of finalized utterances plus the current partial. `recentContext(maxChars:)` walks newest-first and never returns an empty window. |
| 3:00 | `Sources/ListenToMeCore/ContextEngine.swift` line 12 | The default budget is 4,000 characters. Recap and action items get 100,000, because they must cover the whole meeting. |
| 3:25 | `Sources/ListenToMeCore/VAD.swift` | When an engine gives no partials, a 37-line VAD decides utterance boundaries: RMS energy, a 0.02 threshold, 0.8 seconds of trailing silence. |
| 3:50 | `scripts/check-coverage.sh` | That layering is why 96% coverage is even meaningful, with a 95% floor enforced by this script. |
| 4:15 | `tinycopilot/README.md` layout table | TinyCopilot copies the shape exactly: a transcription seam satisfied by a canned transcript, and everything else pure and tested. |

**Demo cue.** Terminal: `cd tinycopilot && make lab-m2`. Show `191 passed, 2 deselected` and
`Total coverage: 100.00%`. Say that coverage floor is 90 here, not 95 — the lab is smaller.

**Action-step close.** Pause the video and do the four action steps in `lesson.md` §M2.1: read
`recentContext`, find the two `.you`/`.others` tags, note the `prepare()` contract, then sketch the
pipeline from memory in your evidence log.

**Recording notes.**
- Enlarge the two line numbers in `DualChannelCapture.swift`; viewers replay this moment.
- If over time, cut the VAD beat to one sentence — it returns in M2.3.
- Do not say "96% means 96% of the app is tested." The badge is *core* coverage.
- Keep the file tree on screen for the whole seam explanation.

## Segment M2.2 — Per-role model routing and prompt builders

**Target runtime:** 5:30 (≈715 words). **Pre-work:** run `ollama list` so you can map your own models.

**Cold open (~15 s).** The obvious design is "point the biggest model at every pane." It is wrong
twice: it taxes latency on panes that do not need strength, and it welds your product to one model's
quirks. Here is what shipped instead.

| Timestamp | On screen | Narration |
|---|---|---|
| 0:00 | `Sources/ListenToMeCore/CopilotRole.swift` | Three roles ship as an enum: listener, quick, deep. Each AI pane gets its own model dropdown with "good for" hints. |
| 0:20 | `README.md` lines 78–92 | Listener refreshes a rolling summary continuously, so speed beats depth. Quick answers the hotkey and fires proactively, so it must be fast. Deep is on-demand reasoning, so it should be strong. |
| 0:45 | `Sources/ListenToMeCore/ModelRanking.swift` lines 76–94 | `roleDefaults` picks automatically. Quick gets a curated fast model or the lightest. Deep gets a curated strong model or the heaviest, taken from the models Quick did not take. |
| 1:10 | Lines 72–79 | The defaults are local-first: `:cloud` models are filtered out of auto-selection, so an unpinned pane never silently ships a transcript to the cloud. |
| 1:35 | `ModelRanking.swift` lines 13–18 | Now the subtle bug. The code splits a model name into tokens and matches markers at token starts, not substrings. |
| 2:00 | Type `"gemini-2.5-flash".contains("mini")` in a REPL | Raw substring matching says true. Gemini contains mini. Every Gemini model would rank as fast, and your Quick default would be quietly wrong for a family. |
| 2:25 | Type the token-prefix check | The token check says false, because gemini does not start with mini. Small code, whole-family correctness. |
| 2:50 | `MeetingSession.swift` lines 119–132 | Routing also needs cancellation. `setModel` cancels the role's in-flight task and bumps a generation counter. |
| 3:15 | `MeetingSession.swift` lines 513–578 | The streaming loop captures its generation and guards every write with it. A stale stream's tokens die on the floor. |
| 3:40 | `Sources/ListenToMeCore/Prompt.swift` lines 65–71 | Prompts are a public enum of static functions, zero I/O. Quick's prompt is anti-preamble: no preamble, no "As an AI", answer in one to three sentences. |
| 4:05 | Lines 73–81 | Listener carries the grounding contract: never invent an owner, deadline, agreement, or completion; mark missing details as unstated. |
| 4:30 | `MeetingSession.swift` lines 40–43 | Only a completed Listener summary grounds Quick and Deep. The live display value is cleared while a refresh streams, so a half-answer is never injected. |
| 4:55 | `PromptBuilderTests.swift` | Because the builders are pure, these tests assert the built string with no model and no network. |

**Demo cue.** In Swift or a Python REPL, run the `gemini`/`mini` comparison. Then show
`tinycopilot/tests/test_model_router.py::TestCapabilityScore::test_gemini_is_not_demoted_as_mini`
and run just that test green.

**Action-step close.** Do `lesson.md` §M2.2's four steps: copy the two prompt sentences and say what
breaks without each, trace the `gemini` check by hand, find the generation bump and the guard, then
run `ollama list` and assign your own models to the three roles with a stated rule.

**Recording notes.**
- Cut the `describe(_:)` hints mention if over time; it is a dropdown nicety.
- Do not claim the Listener default is a *distinct* model — in the Python lab it reuses Quick's pick.
- Read the never-invent sentence aloud; it is the most-quoted line in the module.
- Blur any cloud API keys if `ollama list` shows cloud aliases.

## Segment M2.3 — Proactive intelligence without magic

**Target runtime:** 5:30 (≈715 words). **Pre-work:** none beyond the earlier two segments.

**Cold open (~15 s).** A stakeholder asks why your copilot cannot just know when to help. Here is the
uncomfortable answer: it can, and the part that matters is not the intelligence. It is the restraint.

| Timestamp | On screen | Narration |
|---|---|---|
| 0:00 | `Sources/ListenToMeCore/QuestionDetector.swift` | Question detection is 28 lines. That is the whole "intelligence" budget. |
| 0:20 | The three rules | A finalized utterance is a question if it ends in a question mark, starts with an interrogative, or contains a word-boundary phrase cue. |
| 0:45 | `docs/superpowers/specs/2026-06-18-listentome-design.md` §4.4 | The spec chose this deliberately: a lightweight heuristic, debounced, kept simple, swappable later. Ship cheap, keep the seam. |
| 1:05 | `Sources/ListenToMeCore/ContextEngine.swift` lines 31–40 | The gate is where the discipline lives. Fire only for finalized `.others` segments that pass detection, at most once per debounce window. |
| 1:30 | `ContextEngine.swift` line 8 | The default window is eight seconds. Without it, two heated minutes of questions produce overlapping suggestions. |
| 1:50 | `Sources/ListenToMeCore/OllamaProvider.swift` lines 120–139 | Now failures. The provider posts to `/api/chat` with streaming on and reads NDJSON lines. The line source is injectable, so tests feed canned lines. |
| 2:15 | Lines 67–83 | The loop tracks two booleans: did it see a done event, and did it produce visible content. |
| 2:40 | Lines 159–170 | Failures are typed. `.server` for an in-stream error event. `.incomplete` when the lines end without done. `.empty` when it completes with no content. |
| 3:05 | Same lines | A truncated or empty stream therefore cannot finish as success. The user gets a typed failure, not a half-answer. |
| 3:25 | `docs/reviews/2026-09-10/design-and-gap-review.md` | This is a scar. The review found the old provider let truncated and empty streams finish as success — gap G06, priority zero. |
| 3:50 | Lines 5 and 51 of the review | At that moment the project showed 215 passing core tests and 97.24% coverage. The tests validated what was built; what was built was wrong. |
| 4:10 | `OllamaProvider.swift` lines 49–51 | Budgets come from observation too. Quick evaluations force no thinking, temperature zero, and a 3,072-token cap. |
| 4:30 | `docs/SHARED-LIVE-SUMMARY.md` line 66 | Why 3,072? Live testing found planning text exhausting the old 1,600-token budget halfway through valid JSON. The cap is the smallest number that stopped a real truncation. |
| 4:50 | `AutomaticReviewCoordinator.swift` line 51 | The rest is bounded everywhere: five-second speech batches, timers only for queued work, reviews serialized at 30 and 60 seconds. |

**Demo cue.** Split screen: the red run in `tinycopilot/tests/test_ollama_provider.py` for a
`done=False` stream, then the green. Point out the exception type in the traceback, not the message.

**Action-step close.** Do `lesson.md` §M2.3's four steps: list the detector's three rules, name the
two booleans and the error case for "The best ans" with no done event, find the 3,072-token
explanation, then write your own product's trigger, debounce, and per-response budget — three
numbers, no adjectives.

**Recording notes.**
- If short on time, cut the live-summary scheduler beat; M3 covers it more fully.
- Do not say the detector "understands" questions — it pattern-matches three ways.
- Say the error case names exactly; Q7 depends on the distinction.
- Keep the review document on screen while quoting G06; it is the segment's proof.
