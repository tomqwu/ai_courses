# On-Device AI Apps — Track 1 of AI Product Studio

> **Price:** $199 · self-paced · 6 weeks · ~5 hours/week
> **Prerequisite:** you write code (Python), use git, and are comfortable in a terminal
> **You ship:** a working local-first AI app whose privacy claims are enforced in code and proven by tests.

## The promise

Most "AI app" tutorials end with a notebook that calls an API. This track ends with a product: **TinyCopilot**, a multi-role AI copilot with per-role model routing, streaming local inference through Ollama, and a local-only mode that *fails closed* — it refuses to send your text anywhere it cannot prove is local.

The distinguishing promise is the second half: your privacy claims are not adjectives. Every one of them is a line of code plus a test that proves it. You will write the red-team test for the exact hole that breaks naive privacy checkers — a `localhost` daemon quietly serving a cloud-backed model alias — and watch your code reject it.

You study the real thing. **ListenToMe** is a shipped, free, open-source macOS/iOS meeting copilot: dual-channel capture, on-device transcription, real-time AI through models you choose, signed and notarized public releases (`ListenToMe/README.md`). Its core package holds a **96% coverage badge** against a **95% floor enforced by script** (`ListenToMe/README.md`; `ListenToMe/scripts/check-coverage.sh`), its positioning came from a **14-row sourced competitor table** (`ListenToMe/docs/competition-analysis.md`), and its own engineers once held a release back at **97.24% coverage** with the words "do not promote" (`ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md`). That last file is why this track treats green tests as the entry fee, not the verdict.

The core labs are **Python + Ollama**, so **no Mac is required**. The Swift/macOS case study is read and mapped; the building happens in a Python lab that mirrors `ListenToMeCore` module for module (`course/03-content/m02-ondevice-app/tinycopilot/README.md`).

## Who this is for — and who it isn't

**For you if you:**
- Write Python professionally or seriously and want to ship a real on-device AI product, not an API demo.
- Care about privacy as an engineering property — local inference, BYO model, no silent cloud fallback.
- Use an AI coding agent already and want the operating system (constitution, `AGENTS.md`, specs, evidence discipline) that makes one engineer ship at team speed.
- Want the packaging and pricing work done too, not left as an exercise.

**Not for you if you:**
- Have never written code (take a programming course first).
- Want a Swift/iOS-only course. There is a mapped Swift stretch track, but the graded labs are Python (`course/03-content/m02-ondevice-app/lab.md`).
- Want prompt-engineering trivia, or a course where "done" means a video finished rather than a test suite green.
- Need enterprise AI-governance compliance material — that is a different product.

## Prerequisites

- **Python 3.11+** (TinyCopilot itself also runs on 3.10 — `course/03-content/m02-ondevice-app/tinycopilot/README.md`).
- **Ollama** installed and one model pulled, e.g. `qwen3:0.6b` (`course/03-content/m00-orientation/lab.md`).
- Git and a terminal. `pytest`, `pytest-cov`, and `httpx` as lab dependencies (`course/03-content/m02-ondevice-app/tinycopilot/README.md`).
- No prior LLM/ML experience. No Mac. A daemon with only `:cloud` aliases is a **valid** environment — it makes the privacy lab more instructive, not less (`course/03-content/m03-privacy-ship/lab.md`).

## What's included

| | |
|---|---|
| **Modules** | M0 Orientation, M1 The AI Product Operating System, M2 On-Device AI App: Architecture, M3 On-Device AI App: Privacy/Testing/Shipping, plus a monetization and launch slice from M7 and M8 |
| **Lessons** | All 12 teaching segments for M0–M3, plus M7.1–M7.3 and M8.1–M8.2 — each ends with an action step |
| **Labs** | Lab M0 (environment + first ship-win), Lab M1 (your operating system), Lab M2 (build TinyCopilot's core), Lab M3 (harden, prove, position), and a Week 6 pricing/sales-page deliverable set drawn from Lab M7 |
| **Quizzes** | Quiz M0, M1, M2, M3, and M7 — 40 auto-gradable questions with answer keys |
| **Code** | The full `tinycopilot` reference implementation and its test suite (`course/03-content/m02-ondevice-app/tinycopilot/`) — the tests are the spec; the implementation is the answer key |
| **Artifacts you leave with** | A public TinyCopilot repo with a red→green TDD history, fail-closed privacy tests, a real-LLM contract test, a coverage floor, a sourced competitor/pricing table, a positioning one-liner, and a sales page draft |

Everything above is enumerated module by module — including what is deliberately **not** included — in `bundle-map.md`.

## The 6-week map

| Week | Focus | Lab | You finish the week with |
|---|---|---|---|
| 1 | Orient and get running (M0) | Lab M0 | Three repos cloned, Ollama running, SignUpFlow solver output captured (TinyCopilot suite as stretch) |
| 2 | Your AI product operating system (M1) | Lab M1 | `constitution.md`, `AGENTS.md`, `specs/001-todo-command/`, one red→green TDD loop, a dated evidence entry |
| 3 | The on-device architecture (M2.1–M2.3) | Lab M2, modules 1–3 | `conversation_store`, `question_detector`, `prompts` re-implemented test-first |
| 4 | Routing, streaming, orchestration (M2) | Lab M2, modules 4–6 | `make lab-m2` green: 201 passed, 100% coverage, floor 90 (`course/03-content/m02-ondevice-app/tinycopilot/README.md`) |
| 5 | Privacy, tiered testing, shipping (M3) | Lab M3, steps 1–4 | Fail-closed local-only mode, red-team test, `LAB_E2E` contract test, coverage floor, `docs/competition.md` |
| 6 | Price, package, launch (M7 slice + M8.1/M8.2) | Lab M7 steps 1–5 | Pricing worksheet, positioning one-liner, packaging page, 8-section sales page, 5-email mini-arc, recorded demo |

Time budget, assessment per week, and the quiz schedule are in `syllabus.md`.

## Honest scope note

This is a **subset** of AI Product Studio, and that is deliberate. The full course teaches three product archetypes — this one (on-device app), a spec-driven multi-tenant SaaS (built on SignUpFlow: dated evidence of "1,464 passed, 21 skipped" in `SignUpFlow/docs/playbooks/validation.md`, 7 test tiers per `SignUpFlow/docs/TESTING.md`, 17 spec folders), and an evidence-cited expertise product (built on AI × QE: 116 narrated slides = 21+33+26+36 per `ai_qe/_data/briefing_room.json`).

What this track does **not** include: the M4/M5 spec-kit and multi-tenant security labs, the M6 expertise-product lab, the full M7/M8 labs, and the scored capstone with its rubric and demo day (`course/03-content/m08-launch-capstone/lab.md`). If you want to build and sell **one** product type, this track is complete on its own. If you are choosing a path and can afford it, the full course at $399 is the better value — see `pricing.md` for the arithmetic, stated plainly.

**No testimonials yet — and we won't invent any.** This track, like the parent course, has no student results to show while the founding cohort is still running. Where a sales page would normally carry before/after/result quotes, ours carries the three public case-study repos and says so (`course/04-sales/landing-page.md`).

## FAQ

**Do I need a Mac?**
No. Every graded lab is Python + Ollama on macOS, Linux, or Windows (`course/03-content/m02-ondevice-app/lab.md`). The Swift stretch track maps each Python module onto its `ListenToMeCore` counterpart and requires a Mac (`course/03-content/m02-ondevice-app/tinycopilot/README.md`).

**Do I need to know AI or ML?**
No. You consume models through Ollama. You learn routing, prompt architecture, streaming error handling, and privacy engineering — not training.

**What if my Ollama daemon has only `:cloud` aliases?**
Both outcomes are valid and both are graded. A local model is accepted by local-only mode; a cloud-only daemon rejects everything, which is the red-team scenario happening for real. Record which one you hit; do not weaken the checks to make the lab "pass" (`course/03-content/m03-privacy-ship/lab.md`).

**How much time per week?**
About 5 hours: 60–90 minutes of lesson, 2–3 hours of lab, quiz and evidence write-up. Weeks 3–5 are the heavy ones.

**Is this the whole course?**
No — it is Track 1 of 3. Compare before you buy (`bundle-map.md`), and read `pricing.md`; the honest recommendation is that the $399 full course is better value if you want all three archetypes.

**Refunds?**
Same policy as the parent course: full refund within 14 days, keep the materials (`course/04-sales/landing-page.md`).

**Are the case-study claims verifiable?**
Yes — that is the point. Every factual claim in this track carries a file path you can open in the cloned repos or in `course/`. If a pointer doesn't resolve, the claim is wrong; say so.

## Verify anything

- Case study: `ListenToMe/README.md`, `ListenToMe/docs/competition-analysis.md`, `ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md`
- Run the lab gate yourself: `cd course/03-content/m02-ondevice-app/tinycopilot && make lab-m2` → 201 passed, 100% coverage; `make lab-m3` → 49 passed; `make e2e` → 2 passed (`course/03-content/m02-ondevice-app/tinycopilot/README.md`)
- Standards this bundle is written to: `course/01-design/content-standards.md`
