# Video Scripts M3 — Privacy, Testing, Shipping

> Three recording scripts, one per segment. Pacing is ~130 words/min, so each 6-minute segment
> carries a ~780-word budget; the beats tables below hold the spoken narration, compressed to the
> lines that must be read aloud. Record against the deck in `slides.md`; open real files on screen.

## Segment M3.1 — Privacy is a mode, not a slogan

**Target runtime:** 6:00 · **Word budget:** ~780 words · **Deck slides:** M3.1 block (slides 3–11)

**Cold open (≈15 s):** "A localhost URL proves nothing. Pull a `:cloud` model and your local
daemon lists it, serves it, and answers through it — while the compute runs on someone else's
machine. Here is the code that catches it."

| Timestamp | On screen | Narration |
|---|---|---|
| 0:00–0:30 | Deck: "Privacy is a mode, not a slogan" | ListenToMe does not express privacy as an adjective. It exposes a mode switch: local only, cloud, or AI off. Read the cloud label at `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:3-13`: "Ollama Cloud — sends transcript and context." It names the data it ships. That is the standard. |
| 0:30–1:30 | `ModelPrivacy.swift:3-13` | Four cases, four labels written to be true rather than to sell. And the boundary is one-directional: pasting a cloud API key stores the key and changes nothing about routing. Adding a key alone does not switch modes. Opting in to cloud is deliberate, never a side effect. |
| 1:30–2:45 | Terminal: `ollama list` plus `ModelPrivacy.swift:16` | Here is the shortcut to reject. Check the URL is localhost and you are done — except the file carries a comment rejecting exactly that. Pull a `:cloud`-suffixed model and it installs through your daemon, appears in `ollama list`, and answers through localhost. The compute is remote. A local endpoint is not proof of local inference. |
| 2:45–3:45 | `ModelPrivacy.swift:17-24` | The fix: ask the daemon to describe the model it is about to run. `remote_host` and `remote_model` must be absent; `details.format` and `model_info` must be non-empty. One guard, defaulting to false. Missing metadata, malformed JSON, an unexpected field — all reject. |
| 3:45–4:45 | `OllamaProvider.swift:99-119` | Three layers around it. The host must be localhost, 127.0.0.1, or ::1, checked before a byte of prompt is written. Verification re-runs on every request, so switching models mid-session cannot skip it. And redirects are refused. |
| 4:45–5:30 | `OllamaProvider.swift:151-157` | Redirect following is silent by default. Even a verified-local server could answer with a 3xx, and the stack would forward your meeting text. `RejectRedirects` answers nil and the request dies. Never follow redirects with meeting text in local-only mode. |
| 5:30–6:00 | Deck: claim → enforcement table | The discipline to copy: every privacy promise is a row whose second column is code a reviewer can open. If a claim has no second column, you do not have a claim — you have copy. |

**Demo cue.** Terminal open with `ollama list`, then the Swift file scrolled to lines 17–24.
Viewers should notice that the guard is a single conditional and that the failure path is the
default, not an exception handler.

**Action-step close.** Run `ollama list` and classify each model by name against the
`isVerifiedLocal` rule: accepted, rejected, or unclassifiable from the name alone. For the
unclassifiable ones, write what metadata you would need before sending a prompt.

**Recording notes.**
- Enlarge the terminal font; `ollama list` output is the visual proof of the cloud-alias case.
- If over time, cut the recap of default filtering; the metadata guard is the must-keep beat.
- Do not say the check *audits* the daemon. It verifies the daemon's self-description; the README
  states that trust boundary honestly.
- Do not claim any specific model is or is not cloud-backed without showing its `/api/show`.

## Segment M3.2 — Testing: floors, contracts, and what CI can't do

**Target runtime:** 6:00 · **Word budget:** ~780 words · **Deck slides:** M3.2 block (slides 12–18)

**Cold open (≈15 s):** "This release had two hundred fifteen passing tests and ninety-seven
percent coverage, and the review still said: do not ship it. Coverage measures which lines your
tests executed. Nothing else."

| Timestamp | On screen | Narration |
|---|---|---|
| 0:00–0:45 | `ListenToMe/.github/workflows/ci.yml:36-42` | The floor first. CI enforces a ninety-five percent line-coverage floor on the core package as a hard gate. Show the workflow step, then `ListenToMe/scripts/check-coverage.sh`: it runs the suite with coverage enabled, computes total line coverage, prints a per-file report, and exits non-zero below the threshold. |
| 0:45–1:45 | Same script, terminal | What the floor buys: nobody adds untested logic to the core without testing it or consciously arguing the floor down. What it does not buy: correctness of what was never built, a working GUI, audio that captures, or a first-run experience a human can survive. |
| 1:45–2:45 | CI job list | Three jobs run: the macOS app build, the iOS app build, and the core suite with the floor. The two build jobs also run a dependency-lock diff against the workspace's resolved lock. The artifact you test is the artifact you ship, built from locked dependencies, or the build says no. |
| 2:45–3:45 | `ListenToMe/Makefile:39-53` | CI cannot reach an Ollama daemon or audio hardware, so the real-LLM contract test lives outside it behind `make e2e`. It builds the app target, verifies the app-path resolution, and runs a real completion through the actual provider against your local daemon. Why contract? Because it tests the seam a mock can only assume. |
| 3:45–4:30 | `OllamaContractE2ETests.swift:4-22` | The test gates on `XCTSkipUnless(env["LTM_E2E"] == "1")`, so normal runs and CI never touch the network. `make e2e` sets the gate and picks the model. The assertion is minimal but real: stream a fixed prompt and require non-empty content. A test that needs infrastructure still ships — it skips with a reason. |
| 4:30–5:15 | `docs/manual-smoke-test.md:1-7` | The top tier is human: mic capture, system audio, and live speech-to-text need a GUI session and manual permission grants. That document opens by stating what `make e2e` already covers and what cannot be automated. It is a numbered script: grant, speak, play audio, confirm the labels. |
| 5:15–6:00 | `design-and-gap-review.md:1-54` | Then the review that said no. A thirty-four-item inventory, G01 through G34, each with a priority and an evidence class, recommended against promoting 1.3.0 — with 215 passing tests and 97.24% coverage in hand. Tests validate what you built; honest review validates what you shipped. |

**Demo cue.** Split screen: the coverage step in `ci.yml` on the left, a terminal running
`make lab-m2` on the right. Viewers should notice the floor is a separate CI step, not a badge.

**Action-step close.** Run your Lab M2 suite and record an evidence note — command, counts,
date — plus one thing the suite cannot tell you. Then write one gap of your own: ID, priority,
evidence class ("source" vs "validate"), required action.

**Recording notes.**
- Enlarge the coverage summary block; the "Required test coverage of 90% reached" line is the
  proof that the floor ran.
- If over time, cut the dependency-lock diff beat, not the gap review.
- Do not call `make e2e` a privacy test. It runs against whatever model the router selects,
  including `:cloud` aliases; the contract is the provider, not privacy.

## Segment M3.3 — Ship it: release discipline and competitive positioning

**Target runtime:** 6:00 · **Word budget:** ~780 words · **Deck slides:** M3.3 block (slides 19–23)

**Cold open (≈15 s):** "A local build is not the end of the workflow. Done means a user can
download the thing — and you have personally proven the download is the thing."

| Timestamp | On screen | Narration |
|---|---|---|
| 0:00–1:00 | `ListenToMe/AGENTS.md`, "Definition of done" | Six steps, and the sixth is the one most projects skip. Implement and run tests, lint, coverage. Verify in the installed production app. Bump version and notes. Commit, push, verify hosted CI. Publish the signed, notarized DMG targeting the exact source commit. Then download the published asset and verify its checksum and tag metadata. |
| 1:00–2:00 | `ListenToMe/docs/RELEASING.md:120-134` | The mechanics: after publishing, download the hosted asset and compare its SHA-256 against the verified local DMG, and create the release with `--target` pinned to the exact commit so the tag cannot silently point at another commit. `make release` scripts the build, deep-codesign, package, notarize, and staple. |
| 2:00–3:00 | `ListenToMe/docs/RELEASING.md:18-31` | Dev builds are a separate app: `com.tomwu.ListenToMe.dev` versus the release id. macOS TCC keys permission grants by bundle id plus the binary's signing requirement, and a Developer ID signature and an Apple Development signature can never satisfy each other. Share one id and installing either silently invalidates the other's grants: the toggle stays on while capture returns nothing. |
| 3:00–3:45 | `ListenToMe/docs/competition-analysis.md:1-14` | The other half of shipping is proving what your product is against what exists. The analysis is dated, qualifies every unconfirmed detail with "approximately" or "reportedly", and ends each competitor entry with a source URL. It names the tension: nearly every commercial product runs its AI in the cloud even when marketed as local-first. |
| 3:45–4:45 | `competition-analysis.md:70-80` | It does not invent a slogan. It identifies a corner almost no competitor fills — fully on-device, free, open-source — and derives the line from the table: the free, open-source, fully on-device meeting copilot for macOS, bring your own model, stay private, shape it to any conversation. |
| 4:45–5:30 | Deck: clause → column table | Every clause is load-bearing. "Free" is the Price column. "Fully on-device" is the On-device? column. "Meeting copilot" is Focus. "Bring your own model" is Multi-model/BYO. Delete a clause and the claim goes false against the table. That is what makes it specific and falsifiable. |
| 5:30–6:00 | Deck: Lab M3 | That is the module. In the lab you build the same guarantees in Python: harden, prove, position. |

**Demo cue.** Open `RELEASING.md` at the checksum step, then the positioning section of
`competition-analysis.md`. Viewers should notice that the one-liner's words map to named table
columns.

**Action-step close.** Draft a five-row comparison table for your own product idea with per-cell
sources, then write your positioning one-liner and annotate each clause with the column that
proves it. Keep it for Lab M3 Step 4.

**Recording notes.**
- Enlarge the clause-to-column table; it is the segment's payoff.
- If over time, cut the TestFlight mention and keep bundle-id separation — the lying toggle is the
  memorable failure.
- Do not quote competitor prices from memory. If you show a cell, show the source URL beside it.
