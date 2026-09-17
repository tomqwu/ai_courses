# Quiz M3 — The On-Device AI App: Privacy, Testing, Shipping

> 8 questions (6 multiple choice, 2 short answer) · Answer key below · References lesson segments M3.1–M3.3

## Questions

**Q1 (MC).** In ListenToMe's local-only mode, `/api/show` returns HTTP 200 but the response is missing `model_info`. What happens?

- a) The request proceeds; a warning is logged
- b) The request is rejected — the user must pick a verified local model or explicitly enable Cloud
- c) The provider silently retries against Ollama Cloud
- d) The provider falls back to the last model that passed verification

**Q2 (MC).** Why is a server URL of `http://localhost:11434` insufficient proof of local inference?

- a) Loopback traffic isn't encrypted, so it could be intercepted
- b) A local daemon can serve cloud-backed aliases — e.g. a pulled `:cloud` model — so a local endpoint can execute remote models
- c) The OS doesn't guarantee that loopback ports stay private
- d) HTTPS is required for Ollama to mark a model as local

**Q3 (MC).** What does a passing `ModelPrivacy.isVerifiedLocal` check actually prove?

- a) The model produces high-quality answers on this machine
- b) No audio has ever been uploaded from this Mac
- c) The local Ollama service reports this model as downloaded local weights (no `remote_host`/`remote_model`) — a guarantee that trusts the daemon's metadata
- d) The model was built by a privacy-compliant vendor

**Q4 (MC).** Why does `OllamaProvider` install a `RejectRedirects` delegate in local-only mode?

- a) Redirects add latency to streaming responses
- b) Even a verified-local server could answer with a 3xx, and the HTTP stack would otherwise forward the meeting text to a new location silently
- c) Ollama's API documents redirects as protocol errors
- d) Redirects would double-bill Ollama Cloud usage

**Q5 (MC).** ListenToMe's 95% coverage floor will reliably catch which of these?

- a) A new core module merged with no tests
- b) A privacy design hole where the indicator keys off API-key presence instead of actual routing
- c) A first-run experience no human can complete
- d) Missing durable checkpoints that can lose a meeting on crash

**Q6 (MC).** Why does the real-LLM contract test (`OllamaContractE2ETests`) live behind `LTM_E2E=1` outside CI?

- a) Contract tests are flaky and should never run automatically
- b) It was too slow, so it was cut from CI to save money
- c) CI can't reach an Ollama daemon or audio hardware — the test needs a real model on a real machine, so it gates off (skips with a stated reason) in normal runs
- d) CI runs it against a built-in mock daemon instead

**Q7 (Short answer).** Your TinyCopilot is at 191 passed, 100% coverage, and a teammate says "tag v1.0 and ship." Before tagging, write the three-line self-review entry the September 2026 gap review models (`ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md`): one finding of the kind tests cannot surface (name a concrete one for your copilot), the release claim you refuse to make until it is closed, and what "closed" looks like.

**Q8 (Short answer).** Given a comparison table with columns *platform, on-device?, privacy, model choice, price, focus*, write a positioning one-liner for a hypothetical product and annotate each clause with the column that proves it.

## Answer key

**A1: b.** The guard is one conditional returning false — missing metadata fails closed. (a) is fail-open, the exact anti-pattern; (c)/(d) are silent cloud migration, which the mode forbids. *Ref: M3.1 — `ModelPrivacy.swift:15-24`.*

**A2: b.** A stock `ollama pull` of a `:cloud` alias presents exactly this: installed locally, listed locally, computed remotely ("a local endpoint is not proof of local inference," gap review G01). (a) confuses encryption with destination; (d) invents an HTTPS requirement. *Ref: M3.1.*

**A3: c.** The check proves what the daemon's self-description says, nothing more — the README states the trust boundary ("trusts the installed local Ollama service and its metadata"). (b) overclaims: marketing copy is not the privacy policy. *Ref: M3.1 — `README.md` "Privacy."*

**A4: b.** Redirect following is silent by default; the delegate answers `nil` so meeting text can never be silently forwarded. *Ref: M3.1 — `OllamaProvider.swift:138-142, 208-214`.*

**A5: a.** Untested core code drags the percentage below the floor. (b) and (d) were real gap-review findings (G01, G02) that coexisted with 97% coverage — "97% coverage means ship it" and "one more test would have caught it" are the misconceptions. *Ref: M3.2 — `design-and-gap-review.md`.*

**A6: c.** Tier assignment: CI covers headless logic; `make e2e` covers the real-model contract on your machine; the manual tier covers audio. Gating keeps the test in the default suite — skipped with a reason, not deleted. *Ref: M3.2 — `Makefile:39-53`.*

**A7.** A strong entry names a design or user-facing gap, not a test count — e.g. the privacy label keys off whether an API key is set rather than where the request goes (G01), or nothing checkpoints the transcript so a crash loses the meeting (G02) — refuses the matching claim ("local-only", "production-ready") until it is closed, and defines closure as a P0 filed, the enforcing code plus a test, and a re-review. Reject entries whose "finding" is a coverage or count target. The lesson: metrics validate what you *built*; the review validates what users *need*, which no coverage number establishes — "do not promote" coexisted with 215 passing tests and 97.24% coverage (`ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md:5`). *Ref: M3.2.*

**A8.** Grading: every clause falsifiable against a specific column ("free" ← price; "on-device" ← the on-device? column; "for macOS" ← platform). Reject vague adjectives ("powerful," "modern") with no column behind them, and unsourced claims. *Ref: M3.3 — `competition-analysis.md:70-80`.*
## Objective → assessment map

Every "By the end of this module you can" line in `course/03-content/m03-privacy-ship/lesson.md`, and what checks it.

| Objective (lesson.md) | Checked by |
|---|---|
| **Engineer** a fail-closed local-only mode: metadata verification, host checks, redirect rejection, and truthful mode labels | Q1 (missing `model_info` fails closed), Q2 (a loopback URL is not proof of local inference), Q3 (what a passing verification actually proves), Q4 (why redirects are refused); Lab M3 Step 1, checklist items 2–5, rubric rows 1–3 |
| **Test** in tiers: a coverage floor in CI, a real-LLM contract test outside CI, and a manual smoke test for what only a human can verify | Q5 (what a floor catches — and the two gap-review findings it did not), Q6 (why the contract test gates off rather than being deleted), Q7 (the self-review no coverage number produces); Lab M3 Steps 2–3, checklist items 6–7, rubric rows 4–5 |
| **Ship** with a Definition of Done that ends at a published, downloaded, checksum-verified artifact — and derive positioning from a sourced competitor table | Positioning half: Q8 (one-liner with every clause traced to a column), Lab M3 Step 4, checklist items 8–9, rubric rows 6–7. Shipping half: Lab M3 Step 5 — tag at the tested commit, the built wheel's SHA-256, `OK` on a copy outside the repo and `FAILED` on a corrupted one, rung recorded as *candidate* — checklist item 10 and rubric row 8. The last rung (published and re-downloaded) is Lab M8's release step and rubric C2/C5 |
