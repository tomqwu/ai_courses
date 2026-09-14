# Free Lead Product: "The 30-Minute AI Product Teardown"

> The list-builder asset from `launch-plan.md` (email 3 + Gumroad). Purpose: deliver the course's core credibility move — every claim has a file pointer — in 30 minutes, and convert to the waitlist. Formats below: 3-email mini-course + a one-page PDF checklist. Publish on Gumroad at $0 (email capture), YouTube (video version), and repo READMEs where appropriate.

---

## Email 1 — "What 'on-device, private' actually costs to build"

Subject: `What "on-device and private" actually costs to build (30-min teardown, part 1)`

Most AI meeting apps say "local-first." Almost all of them mean: *capture* is local — the audio still streams to cloud ASR, and the AI still runs in someone else's datacenter.

One open-source Mac app — ListenToMe — did the opposite, and the engineering receipts are public. Three moves that make "private" real instead of a slogan:

1. **A mode switch, not a marketing sentence.** Local only / Cloud / AI off — and adding an API key alone never switches modes. The label tells the truth: cloud mode literally says "sends transcript and context." (See `ListenToMe/README.md`, "AI processing mode.")

2. **Local-only that assumes it's being lied to.** A model named `something:local` on `localhost` proves nothing — a local daemon can serve a cloud-backed alias. So before every request, the app checks the model's metadata: if a `remote_host` or `remote_model` shows up, the request fails closed. (This is `ModelPrivacy.isVerifiedLocal` in `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift`.)

3. **Redirects are refused.** In local-only mode, HTTP redirects are rejected outright — so meeting text can never be silently forwarded to a second server. (`OllamaProvider.swift`, the `RejectRedirects` delegate.)

That's what a privacy *guarantee* looks like: three engineering decisions, each testable, each visible in the code you can read.

**Your 10-minute exercise:** install Ollama, then run `ollama list`. If you see names ending in `:cloud` — those are cloud-backed models served through your local daemon. You've just met the exact scenario that fails-closed check exists for. (Pull a real local model to see the difference: `ollama pull qwen3:0.6b`.)

Tomorrow: the SaaS that was built by AI agents *under rule of law* — and why its author turned CI off on purpose.

[Get the full teardown checklist →] *(links to the PDF + waitlist)*

## Email 2 — "The SaaS that turned CI off on purpose"

Subject: `Why one SaaS team turned CI off on purpose (30-min teardown, part 2)`

SignUpFlow is a volunteer-scheduling SaaS — FastAPI, multi-tenant, 24 routers. What's interesting isn't the CRUD; it's the governance that let AI agents write most of it without the project dissolving:

- **A 79-line constitution** sits above every agent instruction file. It states the principles (test-driven, YAGNI, dangerous features disabled by default) and even defines the two modes an agent can be in (autonomous implementation loop vs. interactive chat). (`.specify/memory/constitution.md`)

- **Agent rules that are actually checkable.** Not "be careful with multi-tenancy" but "Every database query MUST filter by org_id. A missing org_id filter is a cross-tenant data leak. Treat it as a P0 bug." Verifiable rules, imperative voice, files under 200 lines. (`SignUpFlow/AGENTS.md`)

- **No CI — and evidence instead.** All validation runs locally and the results go in the PR: commands, counts, dates, head SHA — failures included. The last recorded full run: **1,464 passed / 21 skipped**, with the skips honestly listed. The rule: "GitHub does not independently attest local runs; never fabricate a successful status check." (`docs/TESTING.md`, `docs/playbooks/validation.md`)

The insight: **AI agents don't replace process — they raise the stakes for it.** When code is generated at agent speed, the bottleneck moves to specification, verification, and honesty about what was actually validated.

**Exercise (5 min):** open `SignUpFlow/docs/playbooks/coverage.json` and find one scenario marked `blocked`. That honesty label — automated / partial / manual / blocked, enforced by a test — is rarer in industry than the AI code itself.

Tomorrow: how a solo engineer turns research into a product executives pay for — with a provenance file for every claim.

## Email 3 — "The site that sells by disproving itself"

Subject: `The site that sells by disproving itself (30-min teardown, part 3)`

AI × QE is a presentation site about AI-assisted quality engineering. It has 116 narrated slides, and its conversion trick is unusual: it is *more skeptical than its audience*.

- Every research claim carries a source record with date, sample, method, and sponsor — and a tag for what the claim can *actually* support (task efficiency ≠ released capacity ≠ hard-dollar saving). Mixing those levels is, per the site, "the most common error in AI business cases." (`docs/evidence/index.md`, `docs/principles.md`)

- The homepage says, permanently: "Planning inputs and proposed outcomes are not observed client results." The case study is labelled *illustrative* everywhere, including inside the narration scripts. (`README.md`)

- The site publishes its own audit — 14 findings, 4 of them high-severity — followed by a remediation document that maps every finding to a fix and a verification. (`research/reviews/site-audit-2026-09-06.md`)

The payoff: an executive who reads "the only independent RCT found developers were *slower* with AI" on the vendor's own site stops asking "why should I believe you?" and starts asking "when can we start?"

**The pattern across all three products** — the app, the SaaS, the expertise site — is one loop: study → spec → build → validate → release → *prove*. It's learnable. It's what I teach in AI Product Studio: you study these three repos, build working versions of all three product types with AI agents under the same discipline, and package what you build to sell.

**The next cohort opens soon.** Founding-cohort members get a discount in exchange for a testimonial — the same honest trade you've just seen three times. If building like this sounds like your next eight weeks:

[Join the waitlist →] *(cohort details + early-bird on the landing page)*

---

## The PDF: "The 10-Point Teardown Checklist — how to tell a real AI product from a demo"

One page, print-friendly, the exercises condensed:

1. **Mode switch, not slogan** — can the user *see and control* where data goes? (ListenToMe: 3-way mode + truthful labels)
2. **Fail closed** — what happens when privacy can't be verified? (reject, never best-effort)
3. **Redirect rejection** — can a request silently go somewhere new?
4. **Agent rules are checkable** — imperative, verifiable, ≤200 lines (AGENTS.md)
5. **A constitution above the rules** — principles an agent reads before anything else
6. **Evidence over vibes** — commands, counts, dates, SHAs; failures included
7. **Honest manifests** — automated / partial / manual / blocked, enforced by a test
8. **Provenance per claim** — every number has a source record and a claim-type label
9. **Self-audit published** — findings → remediation → verification, all visible
10. **The loop is complete** — study, spec, build, validate, release, *prove*

Footer: `AI Product Studio — study three real products, build your own, sell what you build. [waitlist link]`