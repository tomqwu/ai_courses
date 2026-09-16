---
marp: true
theme: aps
paginate: true
title: M3 — The On-Device AI App: Privacy, Testing, Shipping
---

## M3 — Privacy, Testing, Shipping

- From "works" to "trustworthy and shippable"
- ~75 minutes of lesson, ~3 hour lab
- Fail-closed privacy, tiered testing, verified shipping
- Case study: ListenToMe, in Swift
- Lab: harden TinyCopilot, then red-team it

<!-- NOTES: Welcome to Module 3. Module 2 gave you a TinyCopilot core that runs; today we make it trustworthy and sellable. Three moves: engineer a local-only mode that fails closed, test in tiers so each risk sits in the tier that can actually observe it, and ship against a Definition of Done that ends at a verified download. Say plainly that the case study is ListenToMe and every claim has a file pointer you can open. Timing: one minute. Transition: the objectives. -->

---

## By the end you can…

- **Engineer** a fail-closed local-only mode
- **Verify** model metadata on every request
- **Test** in tiers: unit, contract, human
- **Ship** to a checksum-verified artifact
- **Position** from a sourced competitor table

<!-- NOTES: Read the five objectives as promises. Engineering means metadata verification, loopback host allowlists, redirect refusal, and truthful labels. Verification means asking the daemon what it is about to run. Tiers mean admitting what CI structurally cannot test. Shipping means the release ends with you downloading your own artifact and checking its checksum. Positioning means a one-liner whose every clause traces to a column. Timing: one minute. Transition: into Segment M3.1. -->

---

## M3.1 — Privacy is a mode, not a slogan

- Privacy is an enum the user picks
- ListenToMe: Local only, Cloud, AI off
- Labels state where data goes
- Adding a key never switches modes
- Opting in to cloud is deliberate

<!-- NOTES: The core idea: privacy is not an adjective in marketing, it is a mode switch in Settings. ListenToMe exposes AIProcessingMode with four cases. Read the cloud label aloud: "Ollama Cloud — sends transcript and context." That label names the data it ships, which is the standard for every mode label you write. Then the boundary rule: pasting an API key stores the key and changes nothing about routing. Timing: two minutes. Transition: the code that enforces it. -->

---

## Proof: the mode enum and its labels

- `AIProcessingMode`: off / local / apple / cloud
- Cloud label names the data it ships
- "Adding a key alone does not switch modes"
- Pointer: `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:3-13`

```swift
public enum AIProcessingMode: String, CaseIterable, Sendable {
    case off, local, apple, cloud
    public var label: String {
        switch self {
        case .off: return "AI off — transcript only"
        case .local: return "Local Ollama models only"
        case .apple: return "Apple Intelligence — on this device"
        case .cloud: return "Ollama Cloud — sends transcript and context"
        }
    }
}
```

<!-- NOTES: Open ModelPrivacy.swift on screen and read lines three to thirteen. Four cases, four honest labels. The one to memorize is cloud: it does not say "enhanced"; it says it sends the transcript and context. The README section "AI processing mode" carries the key rule: adding a key alone does not switch modes. A user cannot drift onto cloud routing as a side effect of configuration. Timing: three minutes. Transition: why the obvious shortcut fails. -->

---

## A localhost URL proves nothing

- `http://localhost:11434` is not proof
- A local daemon can serve cloud aliases
- Pull a `:cloud` model: listed locally, computed remotely
- Code comment: "a localhost URL is insufficient"
- Pointer: `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:16`

<!-- NOTES: This is the failure the whole segment guards against. The obvious implementation is to check that the URL is localhost and call it done. ModelPrivacy.swift carries a comment rejecting exactly that shortcut. Here is why: pull a `:cloud`-suffixed model and it installs through your local daemon, appears in `ollama list`, and answers through your localhost URL, while the compute happens elsewhere. The gap review states it plainly: a local endpoint is not proof of local inference. Timing: three minutes. Transition: what the metadata does prove. -->

---

## What `/api/show` must show

- Ask the daemon to describe the model
- Reject if `remote_host` or `remote_model` present
- Require non-empty `details.format`
- Require non-empty `model_info`
- Anything else fails closed

<!-- NOTES: The fix is to ask the daemon, on every request, to describe the model it is about to run, and accept only the description of a downloaded local one. Four requirements: no remote_host, no remote_model, a non-empty details.format, and a non-empty model_info. The first two catch a cloud alias; the last two prove the shape of a downloaded model carrying weights locally. Everything is one conditional that returns false. Timing: two minutes. Transition: the guard itself. -->

---

## Proof: `isVerifiedLocal` fails closed

- One guard, defaults to `false`
- Missing metadata, bad JSON, odd field: reject
- Trusts the daemon's self-description only
- Pointer: `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:17-24`

```swift
public static func isVerifiedLocal(_ data: Data) -> Bool {
    guard let info = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
          info["remote_host"] == nil, info["remote_model"] == nil,
          let details = info["details"] as? [String: Any],
          let format = details["format"] as? String, !format.isEmpty,
          let modelInfo = info["model_info"] as? [String: Any],
          !modelInfo.isEmpty else { return false }
    return true
}
```

<!-- NOTES: Show lines seventeen to twenty-four. One guard clause: parse the JSON, require remote_host and remote_model to be absent, require details.format non-empty, require model_info non-empty, else return false. Because the failure path is the default, missing metadata, malformed JSON, and unexpected fields all reject. Say the trust boundary out loud: this verifies the daemon's self-description, not the daemon. The README states it honestly. Timing: three minutes. Transition: the three defenses around this check. -->

---

## Three defenses around the check

<!-- _diagram: grid -->

- **Host check** — loopback only, before any prompt
- **Per-request verification** — re-run `/api/show` every request
- **Redirect rejection** — a 3xx kills the request

- Localhost, 127.0.0.1, and ::1 only
- Pointer: `ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:99-119`

<!-- NOTES: In local-only mode three layers run before every chat request. First, the base URL host must be localhost, 127.0.0.1, or ::1; anything else throws before a byte of prompt is written. Second, the provider posts /api/show and requires HTTP 200 plus a verified-local metadata result; re-verified every request, so switching models mid-session cannot skip the check. Third, redirects. Open OllamaProvider.swift lines ninety-nine to one hundred nineteen. Timing: three minutes. Transition: why redirects matter. -->

---

## Redirects refused

- Request runs with `RejectRedirects`
- Delegate answers `nil` on any redirect
- Otherwise your meeting text is forwarded silently
- Pointer: `ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:151-157`

```swift
private final class RejectRedirects: NSObject, URLSessionTaskDelegate {
    func urlSession(_ session: URLSession, task: URLSessionTask,
                    willPerformHTTPRedirection response: HTTPURLResponse,
                    newRequest request: URLRequest,
                    completionHandler: @escaping @Sendable (URLRequest?) -> Void) {
        completionHandler(nil)
    }
}
```

<!-- NOTES: Redirect following is silent by default in most HTTP stacks. Even a verified-local server could answer /api/chat with a 3xx to anywhere, and the stack would helpfully forward your meeting text. The delegate refuses: on any HTTP redirect it answers nil and the request dies. The comment says why: never follow redirects with meeting text in local-only mode. Without this defense, the metadata check is defeated at the transport layer. Timing: two minutes. Transition: fail-closed defaults. -->

---

## Fail closed by default

- `ModelRanking.roleDefaults` filters `:cloud` models
- Cloud auto-picked only when no local chat model exists
- AI off keeps capture, transcription, saving
- Off-device-by-default is out of scope, by principle
- Pointer: `ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:72-77`

<!-- NOTES: Fail closed shapes defaults too. ModelRanking.roleDefaults filters `:cloud` models out of automatic selection entirely; cloud is auto-picked only when no local chat model exists, which means the user set a key and opted in. Underneath sits the product principle in CLAUDE.md: anything that would send data off-device by default is out of scope. And turning AI off is a real option — capture, transcription, and saving keep working. Timing: two minutes. Transition: the discipline to copy. -->

---

## Claim → engineering enforcement

| Claim | Engineering that enforces it |
|---|---|
| Transcript never leaves your Mac | Local mode + host check + `/api/show` |
| Cloud aliases can't sneak in | `isVerifiedLocal` fail-closed guard |
| Text can't be silently forwarded | `RejectRedirects` refuses every 3xx |
| Adding a key never changes privacy | Mode is an explicit user setting |
| Local by default | `roleDefaults` filters `:cloud` |

<!-- NOTES: This table is the discipline to copy. Every privacy promise your product makes must be a row whose second column is code a reviewer can open. If a claim has no second column, you do not have a claim, you have copy. Have students pick one marketing sentence from their own idea and try to fill the table. Most cannot on the first attempt; that is the lesson. Timing: three minutes. Transition: testing, Segment M3.2. -->

---

## M3.2 — Testing is tier assignment

- Unit: logic, mocked transport, runs in CI
- Contract: real model, your machine, outside CI
- Human smoke: mic, system audio, permissions
- Name the cheapest tier that can observe the risk
- Pretending CI covers the top tier makes your README lie

<!-- NOTES: The reframe for this segment: a testing strategy is a tier assignment. For each risk, name the cheapest tier that can actually observe it. Unit tests with a mocked transport cover logic. A contract test against a real daemon covers the seam a mock only assumes. A human smoke test covers audio and permissions. You cannot promote a risk to a tier that cannot see it. Timing: two minutes. Transition: the floor. -->

---

## The 95% coverage floor

- CI enforces a 95% line-coverage floor
- `scripts/check-coverage.sh 95` in the core job
- Below threshold: non-zero exit, build fails
- Buys: no untested core logic without an argument
- Doesn't buy: correctness, GUI, audio, first run

```bash
THRESHOLD="${1:-95}"
swift test --enable-code-coverage
# … compute total line coverage via llvm-cov into PCT …
awk -v pct="$PCT" -v thr="$THRESHOLD" 'BEGIN { exit !(pct + 0 >= thr + 0) }' || {
  echo "FAIL: coverage ${PCT}% is below the ${THRESHOLD}% floor" >&2
  exit 1
}
```

<!-- NOTES: ListenToMe's CI enforces a ninety-five percent line-coverage floor on ListenToMeCore as a hard gate. The script runs the suite with coverage enabled, computes total line coverage, prints a per-file report, and exits non-zero below the threshold. Say what it buys: nobody adds untested logic to the core without testing it or consciously arguing the floor down. Say what it does not buy: correctness of what was never built, a working GUI, audio capture, or a first-run experience a human can survive. Timing: three minutes. Transition: the script in CI. -->

---

## Proof: the floor bites in CI

- `scripts/check-coverage.sh 95` runs in the core job
- Fails non-zero below the floor
- Three CI jobs plus a dependency-lock diff
- Pointers: `ListenToMe/scripts/check-coverage.sh`; `ListenToMe/.github/workflows/ci.yml:36-42`

```yaml
  core:
    name: ListenToMeCore tests + coverage
    runs-on: macos-26
    steps:
      - uses: actions/checkout@v4
      - name: Run ListenToMeCore test suite with a 95% coverage floor
        run: ./scripts/check-coverage.sh 95
```

<!-- NOTES: Open the CI workflow at lines thirty-six to forty-two and show the coverage step, then open the script itself. The workflow has three jobs: the macOS app build, the iOS app build, and the core suite plus the coverage floor. The two build jobs additionally run a dependency-lock diff, so the artifact you test is built from locked dependencies. Release discipline appears early. Timing: three minutes. Transition: the test CI cannot run. -->

---

## The contract test CI can't run

- CI cannot reach a daemon or audio hardware
- So the real-LLM contract test lives outside it
- `make e2e` builds, resolves the app path, streams for real
- Tests the seam mocks can only assume
- Skips with a stated reason, never silently passes

<!-- NOTES: CI cannot reach an Ollama daemon or audio hardware, so the real-LLM contract test lives outside it behind make e2e. It runs a real completion through the actual provider against your local daemon, auto-selecting an installed chat model. Why "contract"? Because it tests the seam that mocks can only assume: that your request format, streaming parse, and error typing work against the real thing. Every unit test used a mock; this one run is the only evidence the mock was honest. Timing: three minutes. Transition: the gating pattern. -->

---

## Proof: a test that skips, not hides

- `XCTSkipUnless(env["LTM_E2E"] == "1", ...)`
- `make e2e` sets the gate and picks a model
- Assertion: non-empty streamed content for a fixed prompt
- Pointer: `ListenToMe/Tests/ListenToMeCoreTests/OllamaContractE2ETests.swift:4-22`

```swift
final class OllamaContractE2ETests: XCTestCase {
    func testRealOllamaStreamingProducesContent() async throws {
        let env = ProcessInfo.processInfo.environment
        try XCTSkipUnless(
            env["LTM_E2E"] == "1",
            "e2e only: set LTM_E2E=1 and run a local Ollama (use `make e2e`)"
        )
        let model = env["LTM_E2E_MODEL"] ?? "llama3.1"
```

<!-- NOTES: Open OllamaContractE2ETests.swift lines four to twenty-two. The test calls XCTSkipUnless on the environment variable, so normal swift test and CI never touch the network; make e2e sets the gate and selects the model. The assertion is deliberately minimal but real: stream a completion for a fixed prompt through the same provider code the app uses and require non-empty content. The gating pattern matters as much as the test. Timing: three minutes. Transition: the tier only a human can run. -->

---

## The tier only a human can run

- Mic capture, system audio, live speech-to-text
- All need a GUI session and manual permission grants
- `docs/manual-smoke-test.md` is a numbered script
- Grant, speak, play audio, confirm the labels
- Say what it covers; say what it cannot

<!-- NOTES: Above the contract test sits the manual tier. Mic capture, system-audio capture, and live speech-to-text all require a GUI session and manual permission grants, and manual-smoke-test.md opens by stating exactly what make e2e already covers and what this document covers that cannot be automated. It is a numbered, repeatable script. A testing strategy that pretends CI covers this tier just makes your README lie. Timing: two minutes. Transition: the review that said no. -->

---

## The review that said no

- 34-item gap inventory, G01 through G34
- 215 passing tests and 97.24% coverage in hand
- Recommendation: do not promote 1.3.0
- G01: local endpoints could execute cloud models
- Tests validate what you built; review validates what you shipped

<!-- NOTES: On September tenth, 2026, a production review of the 1.3.0 candidate produced a thirty-four-item gap inventory, each item with a priority and an evidence class. With two hundred fifteen passing Core tests and ninety-seven point two four percent coverage in hand, it recommended not promoting the release. G01 is the privacy hole from Segment M3.1, sitting happily inside ninety-seven percent coverage, because the tests tested what was built. Timing: four minutes. Transition: shipping, Segment M3.3. -->

---

## M3.3 — Done ends at a verified download

- A local build is not the end of the workflow
- Bump version, push, verify hosted CI
- Publish the signed, notarized DMG
- Pin the release to the exact source commit
- Download the published asset and verify its checksum

<!-- NOTES: ListenToMe's AGENTS.md makes release the default end of any fix or feature: a local build, a local install, or a draft PR is not the end of the workflow. Six steps: implement and run tests, lint, coverage; verify in the installed production app; bump version and notes; commit, push, verify hosted CI; publish the signed, notarized DMG targeting the exact source commit; and finally download the published asset and verify its checksum and tag metadata. That last step is the one most projects skip. Timing: three minutes. Transition: the mechanics. -->

---

## Proof: download it and check the hash

- After publishing, download the hosted asset
- Compare its SHA-256 against the local DMG
- Create the release with `--target` pinned to the commit
- If blocked: name the blocker, do not call it released
- Pointer: `ListenToMe/docs/RELEASING.md:120-134`

<!-- NOTES: Open RELEASING.md around lines one hundred twenty to one hundred thirty-four. After publishing, download the hosted asset and compare its SHA-256 against the verified local DMG, and create the release with target pinned to the exact commit so the tag cannot silently point at another commit. The policy has an honesty clause: if a real blocker stops publication, name the blocker and preserve the candidate; do not describe the work as released. Timing: three minutes. Transition: dev and release identities. -->

---

## Two bundle ids, on purpose

- Dev app: `com.tomwu.ListenToMe.dev`; release: `com.tomwu.ListenToMe`
- macOS TCC keys grants by bundle id plus signing requirement
- One shared id: installing one silently invalidates the other
- The toggle stays on while capture returns nothing
- Pointer: `ListenToMe/docs/RELEASING.md:18-31`

<!-- NOTES: Dev builds are a separate app from the release: one bundle id for dev, one for release. The reason is macOS privacy plumbing. TCC, the subsystem holding Microphone and Screen Recording grants, keys permission grants by bundle id plus the binary's code-signing requirement. A Developer ID signature and an Apple Development signature produce requirements that can never satisfy each other. Share one bundle id and installing either silently invalidates the other's grants: a toggle that lies. Timing: three minutes. Transition: competition analysis. -->

---

## Competition analysis as an engineering artifact

- Dated header, uncertainty labeled in-band
- 12-row by 9-column table, per-cell sources
- "approximately", "reportedly" where unconfirmed
- Taxonomy: bot-joiners, cloud capturers, on-device
- Pointer: `ListenToMe/docs/competition-analysis.md:1-68`

<!-- NOTES: The other half of shipping is knowing and proving what your product is against what exists. Open competition-analysis.md. It is built like a test suite: a dated header stating that unconfirmed details are qualified with approximately or reportedly, a twelve-row by nine-column table, and a per-competitor section ending every entry with a source URL. The analysis names the structural tension: nearly every commercial product runs its AI in the cloud even when marketed as local-first. Timing: three minutes. Transition: the one-liner. -->

---

## The one-liner and its columns

| Clause | Column that proves it |
|---|---|
| free / open-source | Price |
| fully on-device | On-device? |
| meeting copilot | Focus |
| bring your own model | Multi-model/BYO |
| for macOS | Platform |

<!-- NOTES: The analysis does not invent a slogan; it identifies a corner almost no commercial competitor fills and derives the line from the table. The README one-liner: the free, open-source, fully on-device meeting copilot for macOS, bring your own model, stay private, shape it to any conversation. Every clause traces to a column. Deleting any clause would make it false against the table. That is the deliverable: specific and falsifiable, not mood music. Timing: three minutes. Transition: the lab. -->

---

## Lab M3 — Harden, Prove, Position

- Goal: take TinyCopilot from works to trustworthy
- Red-team test first, then implement
- Contract test outside CI, coverage floor, comparison table
- Pass gate: `make lab-m3` → 49 passed
- Both daemon outcomes are valid

<!-- NOTES: Lab M3 is three hours. Step one: write the red-team test first — a mocked /api/show with remote_host set must be rejected in local mode — then implement PrivacyMode, verify_local_model, host enforcement, and redirect refusal. Step two: the real-LLM contract test gated by LAB_E2E. Step three: the coverage floor, with the failure run recorded. Step four: the comparison table. The pass gate is make lab-m3 green: forty-nine passed. Timing: two minutes. Transition: the quiz. -->

---

## Quiz M3

- 8 questions: 6 multiple choice, 2 short answer
- Fail-closed design and why localhost is not proof
- Redirect rejection and coverage-floor mechanics
- Tier assignment and review over metrics
- Positioning derivation from columns

<!-- NOTES: Quiz M3 has eight questions covering the three segments: fail-closed design, why a localhost URL is not proof, the redirect rationale, what a coverage floor will and will not catch, why the contract test lives outside CI, the gap review lesson, and positioning derivation. One question maps to one segment objective. Do it before the workshop. Timing: one minute. Transition: recap. -->

---

## Recap

- Privacy is a mode; verify metadata every request
- A localhost URL proves nothing; fail closed
- Tier the tests; metrics are the entry fee
- Done means published, downloaded, checksum-verified
- Positioning derives from a sourced table

<!-- NOTES: Five sentences to carry out of the module. Privacy is a mode with truthful labels, and metadata is verified per request. A localhost URL proves nothing because a local daemon can serve cloud aliases. Test in tiers and remember that coverage is the entry fee, not the verdict. Done means a verified download, not a local build. Positioning derives from a sourced, qualified table. Timing: two minutes. Transition: the discussion prompt. -->

---

## Discussion prompt

- Post the privacy claim you can least enforce
- Name the code or test that would prove it
- Where does your guarantee actually end?
- Write your trust-boundary sentence
- Reply to one peer: name the defense they left out

<!-- NOTES: Close by asking students to post the marketing-sounding privacy claim they are least sure they can enforce, plus the code or test that would prove it if they wrote it. Then the harder question: where does your guarantee actually end? ListenToMe answers with one clause — this trusts the installed local Ollama service and its metadata. What is your product's equivalent sentence, and would you put it on your sales page? Timing: two minutes. End of deck. -->
