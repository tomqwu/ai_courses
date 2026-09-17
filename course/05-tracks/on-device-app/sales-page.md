# Sales Page — On-Device AI Apps (Track 1)

**Page metadata (platform setup)**
- Title: `On-Device AI Apps — build a private AI app whose privacy is enforced in code`
- Meta description: `A 6-week track in Python + Ollama: build TinyCopilot, a multi-role local-first AI copilot, with fail-closed privacy tests and a pricing/launch package. No Mac required.`
- Price point: **$199** → target length 800–1,200 words (`course/00-research/02-course-market-research.md`, §E)
- Single CTA: **Get instant access →**

---

## Ship a private, on-device AI app — and prove every privacy claim with a test.

Most AI app courses end where the hard part starts: a notebook that calls an API, and a privacy story that is one sentence on a slide.

**On-Device AI Apps** is a 6-week project track where you build **TinyCopilot** — a multi-role copilot that streams real inference from a local model through Ollama, routes three roles to three models, and runs a **local-only mode that fails closed**: it refuses to send a character if it cannot prove the model is local.

Then you write the test that proves it. Your red-team case is the hole that breaks naive privacy checkers — a `localhost` daemon quietly serving a cloud-backed model alias. Your code rejects it; your test says so. That is the promise: **privacy claims enforced in code, proven by tests.**

You study this in shipped code. **ListenToMe** is a free, open-source, on-device meeting copilot for macOS/iOS with a 96% core-coverage badge (`ListenToMe/README.md`) and a 95% coverage floor enforced by script (`ListenToMe/scripts/check-coverage.sh`). Its market was mapped in a 14-row, per-cell-sourced competitor table (`ListenToMe/docs/competition-analysis.md`) — and its engineers once held a release back at 97.24% coverage with the words "do not promote" (`ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md`). You read that review in class.

**No Mac required.** The graded labs are Python + Ollama on macOS, Linux, or Windows; the Swift case study is mapped onto your Python modules.

---

## Who this is for — and who it isn't

**For you if you:**
- Write Python (or Swift) seriously and want a shipped product, not another demo repo
- Believe "local-first" should mean something a reviewer can verify in the code
- Already use an AI coding agent and want the operating system — constitution, `AGENTS.md`, specs, evidence discipline — that lets one engineer ship at team speed
- Want the pricing and launch work done too, not left as homework

**Not for you if you:**
- Haven't written code before
- Want a Swift/iOS-only course (the graded labs are Python)
- Want prompt-engineering trivia or an "AI side hustle" with no building
- Need enterprise AI-governance compliance material

---

## The problem, and the stakes

1. **The privacy is copy, not code.** "Your data stays on your device" is easy to write and hard to enforce. A local URL proves nothing — a local daemon serves cloud-backed aliases like any other model (`ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:15-24`).
2. **The workflow that makes agents useful is missing.** Agents generate code fast and hallucinate faster. Without specs, verifiable rules, and recorded evidence, you get plausible code you cannot trust.
3. **Nobody covers what happens after it works** — pricing, positioning, packaging, launch copy.

Skip all three and you get an abandoned repo with a good README.

---

## What you'll be able to do, week by week

| Week | You finish able to… |
|---|---|
| 1 | Run the case studies locally, get Ollama answering, and run the lab gate yourself |
| 2 | Write a constitution and `AGENTS.md` whose rules a stranger could check; run a spec → plan → TDD loop with a recorded red→green history |
| 3 | Re-implement the copilot's pure core test-first: context budgeting, debounced question detection, three role prompts as pure functions |
| 4 | Route three roles to three models with local-first defaults, stream typed-error-checked responses, and cancel stale streams on a model switch — `make lab-m2` green at **201 passed, 100% coverage** (`course/03-content/m02-ondevice-app/tinycopilot/README.md`) |
| 5 | Engineer a fail-closed local-only mode, reject a cloud alias in a red-team test, run a real-LLM contract test outside CI, enforce a coverage floor, and derive positioning from a sourced competitor table |
| 6 | Price it, package it with explicit "not included" lines, write an 8-section sales page and a 5-email launch arc, tag the public repo, record a 5-minute demo |

---

## Your instructor

**Tom Wu** is a software engineer who builds in public. With AI agents under the discipline this track teaches, he shipped ListenToMe — an on-device meeting copilot with 96% core coverage, notarized releases, and a 14-row competitor analysis in the repo (`ListenToMe/README.md`; `ListenToMe/docs/competition-analysis.md`) — plus SignUpFlow, whose validation record reads "1,464 passed, 21 skipped" with a date (`SignUpFlow/docs/playbooks/validation.md`), and AI × QE, an evidence-cited briefing platform with 116 narrated slides (`ai_qe/_data/briefing_room.json`).

---

## Testimonials

> **Empty on purpose.** No student testimonials exist yet — the founding cohort hasn't finished, and we don't invent social proof (`course/04-sales/landing-page.md`). Verify us instead: run the lab's own gate — `make lab-m2` → 201 passed, 100% coverage (`course/03-content/m02-ondevice-app/tinycopilot/README.md`) — and read the gap review that said "do not promote" at 97.24% coverage (`ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md`).

---

## FAQ

**Do I need a Mac?**
No. Every graded lab is Python + Ollama on macOS, Linux, or Windows. The Swift stretch track maps your modules onto the real `ListenToMeCore` files and needs a Mac.

**Do I need AI/ML experience?**
No. You use models through Ollama and learn routing, prompt architecture, streaming failure handling, and privacy engineering.

**How much time per week?**
About 5 hours: one lesson block, one 2–3 hour lab, a quiz, and an evidence write-up. Weeks 3–5 are heaviest.

**What if my Ollama daemon only has `:cloud` aliases?**
That's a valid — and instructive — environment: local-only mode then rejects every model, which is the red-team scenario happening for real. You document it and prove the contract seam with a mocked stream. Do not weaken the checks to make it pass (`course/03-content/m03-privacy-ship/lab.md`).

**I've taken AI courses that didn't stick. Why is this different?**
Because you finish something: a public repo, a tagged release, fail-closed privacy tests, a sourced pricing table, a sales page — judged by objective checklists, not video completion. Every claim points at a file you can open (`course/01-design/content-standards.md`).

**Is this the whole course?**
No — Track 1 of 3, and a strict subset. The module-by-module accounting is in `bundle-map.md`. Want all three product types plus the scored capstone? Take the full course.

**Refunds?**
Full refund within 14 days. Keep the materials.

---

## Pricing

| | What you get | Price |
|---|---|---|
| **On-Device AI Apps (this track)** | M0–M3 plus the M7/M8 monetization-and-launch slice, 4 labs, 5 quizzes (40 questions with keys), the TinyCopilot repo and test suite, the pricing/sales-page deliverable set, lifetime access | **$199** |
| **AI Product Studio (full course)** — *recommended* | All 9 modules, 27 lessons, 8 labs, 72 quiz questions, all three archetypes, the full M7/M8 labs, and the scored capstone with demo day | **$399** |
| Studio Live (8-week cohort) | Everything in the full course plus weekly workshops, instructor code review on three labs, capstone review, and demo day | $1,490 |

If you want more than one product type, **buy the full course at $399**: $200 more adds two archetypes, four labs, and the capstone. This track is for builders who want one thing done properly — a private on-device AI app they can defend in code.

**[ Get instant access → ]**

*Prices in USD, per person. No fake countdowns, no invented testimonials.*

---

## Authoring notes (not published)

- Length: ~1,185 words of copy — inside the 800–1,200 band for a sub-$200 offer (`course/00-research/02-course-market-research.md`, §E; `course/03-content/m08-launch-capstone/lesson.md`, M8.1).
- One CTA only. The $399 path appears as a larger option inside the pricing table, not as a competing button, so the track is not cannibalized (`course/05-tracks/on-device-app/pricing.md`).
- Every number here carries a pointer; if a repo's evidence line changes, update this page, never the claim (`course/01-design/content-standards.md`, §0.1).
- Testimonials stay an honest placeholder until real student results exist.
