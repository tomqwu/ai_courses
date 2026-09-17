# Glossary M3 — Privacy, Testing, Shipping

> Terms are alphabetical. "Where it lives" is a file pointer you can open, not a definition you
> have to trust.

**Bundle id / TCC** — macOS keys Microphone and Screen Recording grants by bundle id *plus* the
binary's code-signing requirement, so a dev build and a release build need separate ids —
`ListenToMe/docs/RELEASING.md:18-31`.

**Cloud alias** — A model name ending in `:cloud` (or a remote-backed model under a local-sounding
name) that installs and lists on a local daemon while its inference runs remotely —
`ListenToMe/docs/manual-smoke-test.md`; `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:16`.

**Contract test** — A test that exercises the real seam a mock only assumes — here, NDJSON
request shape and stream parsing against a live Ollama daemon — kept outside CI behind an
environment gate — `ListenToMe/Tests/ListenToMeCoreTests/OllamaContractE2ETests.swift:4-22`.

**Coverage floor** — A hard CI gate that fails the build when total line coverage drops below a
threshold; it buys enforcement against untested core logic and nothing else —
`ListenToMe/scripts/check-coverage.sh`; `ListenToMe/.github/workflows/ci.yml:36-42`.

**Definition of Done** — Release as the default end of any fix: published, notarized, and verified
by downloading the artifact and checking its checksum — `ListenToMe/AGENTS.md`;
`ListenToMe/docs/RELEASING.md:11-16`.

**Dependency-lock diff** — The CI step that fails a build when the checked-in dependency lock and
the generated workspace's resolved lock drift apart — `ListenToMe/.github/workflows/ci.yml:24, 35`.

**Fail closed** — A design where the failure path is the safe path: missing, malformed, or
unexpected metadata rejects the request rather than proceeding —
`ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:17-24`.

**Graceful degradation** — Turning AI off leaves capture, transcription, and saving working; the
app degrades, it does not stop — `ListenToMe/README.md`, "AI processing mode".

**LOCAL_HOSTS / loopback allowlist** — The only hosts local-only mode trusts:
`localhost`, `127.0.0.1`, `::1`. Anything else throws before a prompt is written —
`ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:145-147`.

**Manual smoke test** — The tier that covers mic capture, system audio, and live speech-to-text,
all of which need a GUI session and manual permission grants — a numbered, repeatable script —
`ListenToMe/docs/manual-smoke-test.md:1-7`.

**Metric vs. verdict** — Coverage and test counts are the entry fee; a review that validates what
you *shipped* is the verdict — `ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md:5`.

**`PrivacyMode`** — The explicit three-way mode switch (`off`/`local`/`cloud`) a user picks;
adding a cloud key never switches it — `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:3-13`;
TinyCopilot mirror: `course/03-content/m02-ondevice-app/tinycopilot/src/tinycopilot/privacy.py:28-37`.

**Redirect refusal (`RejectRedirects`)** — A transport that refuses every 3xx instead of following
it, so meeting text can never be silently forwarded — the Swift URLSession delegate is
`ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:138-142, 208-214`; the Python twin builds httpx with
`follow_redirects=False` and raises on 3xx in
`course/03-content/m02-ondevice-app/tinycopilot/src/tinycopilot/ollama_provider.py:45-78`.

**Test tier** — The cheapest layer that can actually observe a risk: unit (mocked) → contract (real
model, your machine) → human smoke (real audio, real permissions) — `ListenToMe/docs/manual-smoke-test.md`.

**Trust boundary** — The honest edge of a guarantee. Local-only mode trusts the installed local
Ollama service and its metadata; it verifies a self-description, not the daemon itself —
`ListenToMe/README.md`, "Privacy".

**Truthful mode label** — A label that names where data goes rather than how good the feature is —
e.g. "Ollama Cloud — sends transcript and context" —
`ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:3-13`.

**`verify_local_model()`** — The fail-closed `/api/show` check: `remote_host` and `remote_model`
absent, `details.format` and `model_info` present and non-empty —
`course/03-content/m02-ondevice-app/tinycopilot/src/tinycopilot/privacy.py:93-135`.

## Terms people get wrong

- **Local vs. verified local** — A localhost URL or a model name is an address; verified local is a
  metadata result that says the weights are downloaded. Only the second is evidence.
- **Coverage vs. correctness** — Coverage says which lines your tests executed. It says nothing
  about whether the design serves the user; G01 sat inside 97.24% coverage.
- **Tested vs. shipped** — A green suite validates what you built. A review validates what users
  need. The 1.3.0 recommendation turned on the second, not the first.
- **Cloud opted-in vs. cloud by default** — Opting in is a mode choice the user makes and sees.
  Cloud by default is out of scope by principle (`ListenToMe/CLAUDE.md`).
- **Skipped vs. deleted** — A test that needs infrastructure should ship and skip with a stated
  reason, never be silently removed or allowed to hang CI.

## Curated resources

- `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift` — the whole privacy argument in twenty-four
  lines: modes, truthful labels, and the fail-closed guard.
- `ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift` — see host enforcement, per-request
  verification, and redirect refusal layered around one chat call.
- `ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md` — the clearest available example of
  honest review outranking green metrics.
- `ListenToMe/docs/RELEASING.md` — the mechanics of a release that ends at a checksum, plus why
  TCC forces two bundle ids.
- `ListenToMe/docs/competition-analysis.md` — a sourced, dated, qualified table; copy its structure
  for Lab M3 Step 4.
- `ListenToMe/docs/manual-smoke-test.md` — how to write the tier CI cannot run.
- `course/03-content/m02-ondevice-app/tinycopilot/README.md` — the Python lab's verified status and
  the one-paragraph privacy model.
- `course/01-design/assessment-and-rubrics.md` — how the lab, quiz, and capstone weights combine.
