# Module 3 — The On-Device AI App: Privacy, Testing, Shipping

> Part of AI Product Studio (APS-3) · ~75 minutes · Prerequisites: Module 2

## Overview

Module 2 left you with a working TinyCopilot core. A core that runs is not a product. A product is private by *engineering*, tested in *tiers*, shipped with a *discipline* that ends at verified artifacts, and positioned with a story precise enough that a skeptical engineer can check every clause of it.

The case study is ListenToMe. Every claim below carries a file pointer into the repo you cloned in Module 0. By the end of this module you can:

- **Engineer** a fail-closed local-only mode: metadata verification, host checks, redirect rejection, and truthful mode labels (`ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift`, `Sources/ListenToMeCore/OllamaProvider.swift`).
- **Test** in tiers: a coverage floor in CI, a real-LLM contract test outside CI, and a manual smoke test for what only a human can verify (`ListenToMe/scripts/check-coverage.sh`, `Makefile`, `docs/manual-smoke-test.md`).
- **Ship** with a Definition of Done that ends at a published, downloaded, checksum-verified artifact — and derive positioning from a sourced 13-competitor table (`ListenToMe/AGENTS.md`, `docs/RELEASING.md`, `docs/competition-analysis.md`).

Lab M3 applies all of it to TinyCopilot: harden, prove, position.

## Segment M3.1 — Privacy is a mode, not a slogan (~25 min)

### Objective

Implement (in Lab M3) and explain (here) a local-only AI mode that fails closed: unverified models are rejected, non-local hosts are rejected, redirects are refused — and the user always sees a truthful label for where their data goes. Explain why a localhost URL alone proves nothing, and map every privacy claim your product makes to the code that enforces it.

### Lesson

**A mode switch, not a marketing sentence.** ListenToMe expresses privacy not in an adjective but in an enum the user picks explicitly in Settings — Local only, Cloud, or AI off (`ListenToMe/README.md`, "Models, presets & languages"). In code, `AIProcessingMode` has four cases with labels written to be true rather than to sell:

```swift
case .off:    return "AI off — transcript only"
case .local:  return "Local Ollama models only"
case .apple:  return "Apple Intelligence — on this device"
case .cloud:  return "Ollama Cloud — sends transcript and context"
```

(`ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:3-13`.) Read that last label: the cloud mode *names the data it ships* — the standard for every mode label. And the boundary is one-directional by design: pasting an Ollama Cloud API key stores the key but changes nothing about routing — "Adding a key alone does not switch modes" (`ListenToMe/README.md`, "AI processing mode"). Opting in to cloud is a deliberate act, never a side effect of configuration.

Two consequences follow. First, **graceful degradation**: "AI off leaves capture, transcription and saving available" (same section) — turning AI off is a real option, not turning the app off. Second, **no silent migration**: a local-only user can never drift onto cloud routing without an explicit switch — a property the gap review made release-blocking ("Never silently migrate a local-only user to cloud", `ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md`, G01).

**Why "localhost" proves nothing.** You might think local-only mode is easy: check that the server URL is `http://localhost:11434` and you're done. ListenToMe's code carries a comment rejecting exactly that shortcut: "Fail closed on missing/remote metadata. A localhost URL or a model name alone is insufficient" (`ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:16`).

Here's the failure it guards against. A local Ollama daemon can serve models whose inference happens elsewhere: pull a cloud alias — a `:cloud`-suffixed model like `deepseek-v4-flash:cloud`, the example in `ListenToMe/docs/manual-smoke-test.md` — and it installs through your local daemon like any other model, appears in `ollama list` like any other model, and answers through your localhost URL. But the compute is remote. The gap review states it plainly: "Local Ollama can execute cloud models; a local endpoint is not proof of local inference" (`design-and-gap-review.md`, G01, citing Ollama's cloud docs). This is not a hypothetical attack; it is a supported, everyday configuration of your app's exact dependency. If your privacy model is "the URL is localhost, therefore private," a stock `ollama pull` breaks your promise.

**What the metadata proves — and what it doesn't.** ListenToMe's answer is to ask the daemon, on every request, to describe the model it is about to run, and to accept only the description of a downloaded local one:

```swift
guard let info = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
      info["remote_host"] == nil, info["remote_model"] == nil,
      let details = info["details"] as? [String: Any],
      let format = details["format"] as? String, !format.isEmpty,
      let modelInfo = info["model_info"] as? [String: Any], !modelInfo.isEmpty else { return false }
return true
```

(`ModelPrivacy.swift:17-24`.) A `POST /api/show` for the selected model must return 200 with **no** `remote_host` and **no** `remote_model`, and **with** a non-empty `details.format` and non-empty `model_info` — the shape of a downloaded model carrying weights locally. Anything else fails. Because the guard is one conditional returning `false`, the failure mode is fail-closed: missing metadata, malformed JSON, an unexpected field — all reject. The prompt is never sent on the strength of an assumption.

Note what this does *not* claim. The README states the trust boundary honestly: local-only mode "trusts the installed local Ollama service and its metadata" (`ListenToMe/README.md`, "Privacy"). You are verifying the daemon's self-description, not auditing the daemon — an honest trust boundary is itself a privacy feature, because it tells the user where the guarantee ends.

**Three defenses around the metadata check.** In local-only mode, `OllamaProvider` layers enforcement before every `/api/chat` request (`ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:99-119`):

1. **Host check.** The base URL's host must be `localhost`, `127.0.0.1`, or `::1` — anything else throws before a byte of prompt is written.
2. **Per-request verification.** It POSTs `/api/show` for the selected model and requires HTTP 200 *plus* `ModelPrivacy.isVerifiedLocal(metadata)` — re-verified on every request, so switching models mid-session or a daemon whose model list changes cannot skip the check.
3. **Redirect rejection.** The request runs on a URLSession with a `RejectRedirects` delegate: on any HTTP redirect, the delegate answers `nil`, killing the request. The comment says why: "Never follow redirects with meeting text in local-only mode" (`OllamaProvider.swift:99-103, 151-157`). Without this, even a verified-local server could answer `/api/chat` with a 3xx to anywhere, and the HTTP stack would helpfully forward your meeting text — silently.

Fail closed also shapes *defaults*: `ModelRanking.roleDefaults` filters `:cloud` models out of automatic selection entirely, and cloud is auto-picked only when no local chat model exists — i.e., when the user set a cloud key and opted in (`ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:72-77`). Underneath it all sits one product principle: "Anything that would send data off-device **by default** is out of scope" (`ListenToMe/CLAUDE.md`).

**Claim → Engineering enforcement.** The discipline to copy: every marketing-sounding privacy promise must be a row in a table whose second column is code a reviewer can open. ListenToMe's mapping:

| Claim you might make | Engineering that actually enforces it |
|---|---|
| "Your transcript never leaves your Mac" | `AIProcessingMode.local` + localhost-only host check + per-request `/api/show` verification (`OllamaProvider.swift:99-119`) |
| "Cloud aliases can't sneak in as local" | `ModelPrivacy.isVerifiedLocal`: `remote_host`/`remote_model` absent, `format`/`model_info` present — fail closed (`ModelPrivacy.swift:15-24`) |
| "Meeting text can't be silently forwarded" | `RejectRedirects` delegate refuses every HTTP redirect in local-only mode (`OllamaProvider.swift:151-157`) |
| "Adding an API key never changes your privacy" | Mode is an explicit user setting; keys are stored but routing is untouched (`README.md`, "AI processing mode") |
| "Local by default" | `ModelRanking.roleDefaults` filters `:cloud` from auto-selection (`ModelRanking.swift:72-77`) |
| "We're honest about where data goes" | Truthful labels, incl. "Ollama Cloud — sends transcript and context"; README states the trust boundary ("trusts the installed local Ollama service and its metadata") |
| "Still useful without AI" | AI off keeps capture, transcription, saving working (`README.md`) |

If a claim has no second column, you don't have a claim — you have copy.

### Action step

Run `ollama list` on your machine (or write the list from memory if you're away from it). Apply the `isVerifiedLocal` rule to each model by name: which would a local-only mode accept, which would it reject, and which can't you classify from the name alone? For the unclassifiable ones, write down what metadata you'd need before sending a prompt. Post your list with one privacy claim for your own product idea and the code that would enforce it.

## Segment M3.2 — Testing: floors, contracts, and what CI can't do (~25 min)

### Objective

Explain what a coverage floor enforces and what it structurally cannot; assign each risk to the tier that can actually test it (CI, real-model e2e, human smoke test); and treat honest review as a release gate that outranks green metrics.

### Lesson

**The floor.** ListenToMe's CI enforces a 95% line-coverage floor on `ListenToMeCore` as a hard gate: `scripts/check-coverage.sh 95` runs in the `core` CI job (`ListenToMe/.github/workflows/ci.yml:36-42`). The script (`ListenToMe/scripts/check-coverage.sh`) runs the suite with `--enable-code-coverage`, computes total line coverage via llvm-cov (excluding `Tests/` and `.build/`), prints a per-file report for visibility, and exits non-zero below the threshold. Know what this buys: no one can add untested logic to the core package without either testing it or consciously arguing the floor down. Know what it doesn't: correctness of what wasn't built, a working GUI, audio that actually captures, or a first-run experience a human can survive. Coverage measures which lines your tests executed — nothing else.

**Three jobs and a lock.** CI runs on `macos-26` runners with three jobs: the macOS app build, the iOS app build, and the `ListenToMeCore` suite plus the coverage floor (`ListenToMe/.github/workflows/ci.yml:14-42`; `ListenToMe/README.md`, "CI"). The two build jobs each run `diff -u Config/Package.resolved ...` against the generated workspace's resolved lock — a *dependency-lock diff* that fails the build if the checked-in lock and the workspace drift apart (`ci.yml:24, 35`). Release discipline appears early: the artifact you test is the artifact you ship, built from locked dependencies, or the build says no.

**The contract test that can't live in CI.** CI cannot reach an Ollama daemon or audio hardware. So the real-LLM contract test lives outside it, behind `make e2e`: it builds the app target, verifies `make run`'s app-path resolution, and runs a real completion through the actual `OllamaProvider` against your local daemon, auto-selecting an installed chat model with `LTM_E2E_MODEL` as the override (`ListenToMe/README.md`, "CI"; `ListenToMe/Makefile:39-53`). The test itself — `OllamaContractE2ETests` — is gated by an environment variable: it calls `XCTSkipUnless(env["LTM_E2E"] == "1", ...)`, so normal `swift test` and CI never touch the network; `make e2e` sets the gate and selects the model (`ListenToMe/Tests/ListenToMeCoreTests/OllamaContractE2ETests.swift:4-22`). Its assertion is deliberately minimal but real: stream a completion for a fixed prompt through the same provider code the app uses, and require non-empty streamed content (with `LTM_E2E_BASEURL`/`LTM_E2E_KEY` to point the same test at Ollama Cloud, `OllamaContractE2ETests.swift:5-22`).

Why "contract"? Because it tests the seam that mocks can only *assume*: that your provider's request format, streaming parse, and error typing work against the real daemon. Every unit test in Module 2 used a mock transport; this one run is the only evidence the mock was honest. The gating pattern matters as much as the test: a test that needs live infrastructure still ships in the default suite — it skips with a stated reason instead of silently passing, silently failing, or hanging CI.

**The tier only a human can run.** Above the contract test sits the manual tier: mic capture, system-audio capture, and live speech-to-text "all of which require a GUI session and manual permission grants" — `ListenToMe/docs/manual-smoke-test.md` opens by stating exactly what `make e2e` already covers (app build, bundle-path resolution, real-LLM contract) and what this document covers that "cannot be automated" (`manual-smoke-test.md:1-7`). It is a numbered, repeatable script — grant these permissions, say a sentence, play audio from another app, confirm the labels. The lesson: a testing strategy is a *tier assignment*. For each risk, name the cheapest tier that can actually observe it: unit (mocked) → contract e2e (real model, your machine) → human smoke (real audio, real permissions). Pretending CI covers the top tier just makes your README lie.

**The review that said no.** On September 10, 2026, a production review of the 1.3.0 candidate produced a 34-item gap inventory — G01 through G34 — each with a priority (P0 blocks the supported release path) and an evidence class: "verified" (synthetic execution or measured/API evidence), "source" (a concrete code path), or "validate" (risk awaiting runtime testing) (`ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md:1-54`). Its recommendation, with 215 passing Core tests and 97.24% coverage in hand: "**do not** promote the existing 1.3.0 DMG as a broadly validated production release." The reasoning is the sentence to memorize:

> "A signed installer, 215 passing Core tests, and 97.24% Core coverage are useful foundations; they do not establish capture reliability, durable saving, accurate speaker attribution, or a usable first-run experience." (`design-and-gap-review.md:5`)

Look at what the review caught that the metrics couldn't: G01 is the privacy hole from Segment M3.1 (the privacy indicator depended on the presence of an API key; local endpoints could execute cloud models) — a *design* gap sitting happily inside 97% coverage, because the tests tested what was built. G02: no periodic durable checkpoint — quit or crash could lose the meeting. G06: in-stream Ollama errors ignored, so truncated streams "can finish as success." None of these is "write one more unit test"; they are mismatches between what was shipped and what a user needs, visible only to a reviewer willing to say no. Later releases closed the P0s — the README's explicit AI routing is G01's fix — which is the second half of the lesson: a review only counts if its findings are tracked to closure. **Tests validate what you built; honest review validates what you shipped.** Metrics are the entry fee, not the verdict.

### Action step

Run your Lab M2 TinyCopilot suite and record an evidence note in the course format: the command, the counts (passed/failed/skipped), the date, and one thing the suite cannot tell you about your copilot. Then write one gap of your own in the review's style — ID, priority, evidence class ("source" vs "validate"), and the required action. Post both.

## Segment M3.3 — Ship it: release discipline and competitive positioning (~25 min)

### Objective

Define "done" as *published and verified* artifacts; explain why dev and release builds need separate identities; and derive a positioning one-liner from a sourced comparison table so every clause of it is falsifiable against a competitor column.

### Lesson

**Definition of Done ends at a verified download.** ListenToMe's `AGENTS.md` makes release the default end of any fix or feature: "A local build, local install, or draft PR is not the end of the workflow" (`ListenToMe/docs/RELEASING.md:11-16`). The six steps (`ListenToMe/AGENTS.md`, "Definition of done"): implement and run tests/lint/coverage; verify in the *installed production app* — for audio changes, actual system-audio transcription labeled OTHERS, because "a permission toggle or microphone pickup is not proof"; bump version and notes; commit, push, verify hosted CI, complete the PR; publish the signed, notarized production DMG "targeting the exact source commit used for the artifact," never replacing an already-published binary; and finally — the step most projects skip — "Download the published asset and verify its checksum and release/tag metadata." `docs/RELEASING.md` states the mechanics: after publishing, "download the hosted asset and compare its SHA-256 against the verified local DMG," and create the release with `--target` pinned to the exact commit "so the tag cannot silently point at another commit" (`RELEASING.md:11-16, 120-134`). The pipeline is scripted: `make release` → `scripts/release.sh` builds the Release configuration under the dependency lock, deep-codesigns with Developer ID, packages the DMG, notarizes via notarytool, and staples (`RELEASING.md:89-118`). The policy has an honesty clause matching Segment M3.2: if a real blocker stops publication, "name the blocker and preserve the candidate/evidence; do not describe the work as released" (`AGENTS.md`). Done means a user can download the thing and you have personally proven the download is the thing.

**Two bundle ids, on purpose.** ListenToMe's dev builds are a separate app from the release: `com.tomwu.ListenToMe.dev` ("ListenToMe (Dev)") vs `com.tomwu.ListenToMe` (`ListenToMe/README.md`, "Dev builds are a separate app"; `docs/RELEASING.md:18-31`). The reason is macOS privacy plumbing: TCC — the subsystem holding your Microphone and Screen Recording grants — "keys permission grants by bundle id **plus** the binary's code-signing requirement" (`RELEASING.md:25`). A Developer ID signature and an Apple Development signature "produce requirements that can never satisfy each other," so if both builds shared one bundle id, installing either "would silently invalidate the other's... grants — the toggle in System Settings stays on while capture returns nothing" (`RELEASING.md:26-29`). Study that failure mode: not an error, not a crash — a toggle that lies. The iOS side automates its distribution the same way: TestFlight uploads run via `make ios-testflight` through an App Store Connect API key, with a recorded agent-run upload (iOS 1.4.0 build 11, September 12, 2026) — and the repo insists upload success stays separate from physical-device acceptance (`ListenToMe/AGENTS.md`, "Standing iOS release instruction").

**Competition analysis as an engineering artifact.** The other half of shipping is knowing and proving what your product *is*, against what actually exists. ListenToMe's `docs/competition-analysis.md` is the standard to copy because it is built like a test suite: a dated header ("Last updated: 2026-08... where a detail could not be confirmed from a primary source, it is qualified with 'approximately' or 'reportedly'"), a 14-row × 9-column comparison table (Platform, On-device?, Privacy, Transcription, AI features, Multi-model/BYO, Price, Focus — Granola, Otter, Fireflies, Fathom, Fellow, tl;dv, Cluely, interview-assist tools, Natively, Superpowered, MacWhisper, ListenToMe), and a per-competitor prose section ending every entry with a source URL (`ListenToMe/docs/competition-analysis.md:1-68`). Uncertainty is labeled in-band: Granola's BYO-key support is "reported but unconfirmed"; Fireflies' Whisper usage is "reportedly... (third-party attribution, not officially confirmed)" (`competition-analysis.md:22, 24`). Nothing is asserted from memory.

The table sorts the market into shapes: **bot-joining note-takers** (Otter, Fireflies, Fathom, Fellow, tl;dv); **bot-free cloud capturers** (Granola, Superpowered) and real-time overlays (Cluely, interview-assist) — which capture locally but run cloud ASR and cloud AI; and the genuinely **on-device** tools (MacWhisper, Natively, ListenToMe) (`competition-analysis.md:9-14`). The structural tension the analysis names is the wedge: "nearly every commercial product processes audio and runs its AI in the cloud, even when it markets itself as 'local-first' — the local part is usually just audio *capture*" (`competition-analysis.md:14`). Two columns — *On-device?* and *Multi-model/BYO* — do most of the separating work.

**Deriving the one-liner from an actual gap.** The analysis's positioning section doesn't invent a slogan; it identifies a corner "almost no commercial competitor genuinely fills: a fully on-device, real-time meeting copilot that is also free and open-source" (`competition-analysis.md:72`). Then the one-liner, each clause load-bearing:

> "The free, open-source, fully on-device meeting copilot for macOS — bring your own model, stay private, shape it to any conversation." (`ListenToMe/README.md:7`; the in-repo analysis variant reads "...bring your own model, run it private..." — `competition-analysis.md:80`)

Trace every clause to a table column, which is what makes it *specific and falsifiable* rather than mood music:

| Clause | Table column it comes from |
|---|---|
| "free" | **Price** — the field runs Free tiers up to Cluely's $19.99–149.99/mo; MacWhisper is ~$69 one-time; nothing in the copilot shape is free-and-open |
| "open-source" | **Price** — ListenToMe's cell reads "Free & open-source" against the $14–149/mo commercial tiers; "the code is open for inspection" has no rival in the shape |
| "fully on-device" | **On-device?** — the column only MacWhisper and Natively also answer Yes to; every capturer row reads "local capture, cloud ASR + AI" |
| "meeting copilot" | **Focus** — the real-time shape (Cluely, interview-assist) vs. post-meeting note-takers (Otter, Granola) |
| "for macOS" | **Platform** — macOS-native against cross-platform rivals (Granola: macOS, Windows, iOS; Otter: web, iOS, Android, desktop) |
| "bring your own model" | **Multi-model/BYO** — most rows offer "no picker" at all; only MacWhisper/Natively compare |
| "shape it to any conversation" | **Focus** — rivals pin a vertical (sales for tl;dv, interviews for Cluely, files for MacWhisper); presets make one app serve many |

That is the deliverable: a one-liner where deleting any clause would make it false against the table. Positioning derived this way is an engineering artifact — dated, sourced, qualified — and it becomes the foundation of Module 7's pricing work.

### Action step

Draft the comparison table for **your** product idea: 5 rows minimum, and every row must be a competitor you have actually used or at least visited the site of. Columns: platform, on-device (or your equivalent privacy axis), privacy, model choice, price, focus. Fill every cell from a URL you visited, or mark it "unverified" — no memory-only pricing. Then write your positioning one-liner and annotate each clause with the column that proves it. Keep this draft; Lab M3 Step 4 hardens it into `docs/competition.md`.

## Recap

- **Privacy is a mode, not a slogan.** An explicit `AIProcessingMode` with truthful labels ("Ollama Cloud — sends transcript and context"); adding a key never switches modes; fail-closed per-request `/api/show` verification (`remote_host`/`remote_model` absent, `format`/`model_info` present); localhost-only host enforcement; `RejectRedirects` so meeting text can't be silently forwarded; local-first defaults filtering `:cloud`; graceful degradation when AI is off; an honest trust boundary ("trusts the installed local Ollama service and its metadata", `ListenToMe/README.md`).
- **A localhost URL proves nothing** — a local daemon serves cloud-backed aliases (`ollama pull` of a `:cloud` model presents exactly this), so verify metadata per request and fail closed.
- **Test in tiers.** A 95% floor enforced by `scripts/check-coverage.sh` in CI; three CI jobs plus the dependency-lock diff; `make e2e` runs the real-LLM contract test through the actual `OllamaProvider` against your local daemon (CI can't reach a daemon or audio hardware); the manual tier covers mic/system-audio.
- **Metrics are the entry fee, not the verdict.** The 34-item gap review (G01–G34) said don't promote 1.3.0 despite 97.24% coverage and 215 passing tests: tests validate what you built, honest review validates what you shipped.
- **Done = published and verified.** Signed + notarized + stapled DMG targeting the exact commit; download the published asset and verify the checksum; dev/release bundle-id separation because macOS TCC keys grants by bundle id *and* signing requirement; TestFlight via App Store Connect API key.
- **Positioning derives from a sourced table.** Twelve competitors, dated, qualified ("approximately", "reportedly"), per-cell sources; a taxonomy (bot-joiners / bot-free cloud capturers / genuinely on-device); a one-liner whose every clause traces to a column.

## Discussion prompt

Post the marketing-sounding privacy claim for your product that you are *least* sure you can enforce — and the code or test that would prove it if you wrote it. Where does your guarantee actually end? ListenToMe's README answers that with one clause ("this trusts the installed local Ollama service and its metadata"). What is your product's equivalent sentence, and would you put it on your sales page? Reply to one peer by trying to name the defense they left out.