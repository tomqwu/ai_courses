# Sales Page — Spec-Driven AI SaaS

> Published copy for the **Spec-Driven AI SaaS** track bundle ($199). Eight sections in the M8.1 anatomy (`course/03-content/m08-launch-capstone/lesson.md`, segment M8.1). Length is set from the price: 800–1,200 words under $200 (`course/00-research/02-course-market-research.md` §E). Published copy is kept inside the 800–1,200-word band for an under-$200 offer; authoring notes are not part of the page.

---

## 1. Ship the spec folder a stranger can implement — and the evidence an auditor can re-run

**Spec-Driven AI SaaS** is a self-paced track bundle from **AI Product Studio**. You work against one real production repo — SignUpFlow, a multi-tenant volunteer-scheduling SaaS built on FastAPI + SQLAlchemy 2.0 + JWT (`SignUpFlow/AGENTS.md`) — and you leave with the governance and evidence half of *your own* SaaS shipped: a spec folder a fresh agent session can implement from, tenant-isolation tests with recorded failures, and acceptance evidence nobody has to take on faith.

Four modules. One launch slice. Six weeks. No model API key and no Mac required.

**Proof strip:** SignUpFlow · 17 spec folders (`SignUpFlow/specs/`) · 7 test tiers (`SignUpFlow/docs/TESTING.md`) · "1,464 passed, 21 skipped", dated 2026-09-12 (`SignUpFlow/docs/playbooks/validation.md`)

[**Get instant access — $199 →**]

---

## 2. Who this is for — and isn't

**This is for you if you:**
- Write code professionally (≈2+ years, Python) and have a SaaS or a multi-tenant feature you actually need to ship.
- Already use a coding agent — Claude Code, Codex, Cursor, Copilot — and want it implementing instead of guessing.
- Want security and acceptance work that survives a customer, a co-founder, or a skeptical engineer opening the repo.

**This isn't for you if you:**
- Haven't written code before.
- Want the on-device app track or the expertise-product track. Both are in the full course; neither is in this bundle.
- Want prompt-engineering tips or "AI side hustle" content. This bundle is about shipping under audit.

---

## 3. The problem — agents don't lower the bar, they raise it

When code appears in minutes, the bottleneck moves to *specifying* what you want, *verifying* what you got, and *being honest* about what was validated (`course/03-content/m01-operating-system/lesson.md`, overview).

Most SaaS builders hit the same three walls:

1. **The spec that only works in your head.** The agent implements something plausible, you correct it in chat, and the correction lives nowhere. Next session, it guesses again.
2. **The tenant leak you never tested.** Multi-tenancy fails in one missing filter — and a missing filter is not a small bug, it is a cross-tenant data leak (`SignUpFlow/AGENTS.md`: "Treat it as a P0 bug").
3. **The evidence that evaporates.** "Tests pass" with no command, no count, no date, no revision. An auditor asks one question and the claim collapses.

The costs are written down in the case study. SignUpFlow's validation record publishes a browser click race and a mypy line reading "835 errors in 40 files; not a pass" (`SignUpFlow/docs/playbooks/validation.md`). Its spec 014 shipped 8 stories, 44 functional requirements, and 6 contracts (~4,661 lines) — with **no `tasks.md`** (`SignUpFlow/specs/014-security-hardening/`). Real repos have holes. You learn to find yours first.

---

## 4. What you'll be able to do — week by week

| Week | You'll leave able to… |
|---|---|
| **1** | Run the case study end to end and name each stage of the Spec-to-Ship Loop with a file you can open |
| **2** | Write a constitution and an `AGENTS.md` of rules an agent can actually be checked against, then run one spec → plan → TDD loop with a recorded red run and green run |
| **3** | Produce a complete spec folder for one real feature — stories, research decisions with rejected alternatives, a Constitution Check, contracts, and tasks citing exact file paths — and pass it through the stranger test |
| **4** | Deny cross-tenant reads and writes with real-JWT tests, prove a denied write leaves the row unchanged, and prove a scheduling qualification grants no admin rights |
| **5** | Make authorization executable with a route policy and a drift test, then design playbook acceptance with an honest coverage manifest that fails the run when a scenario is removed |
| **6** | Price your SaaS with sourced comparators, gate what isn't proven, and write a sales page and launch arc in the 8-section anatomy |

*Every lesson ends with an action step; every module ends in a lab with an objective pass gate.*

---

## 5. Your instructor

**Tom Wu** is a software engineer who builds in public. He shipped **SignUpFlow**, the multi-tenant SaaS you study here: FastAPI + SQLAlchemy 2.0, JWT auth, a greedy scheduling solver, 17 spec-kit feature folders, and a seven-tier suite whose dated evidence line reads "1,464 passed, 21 skipped" (`SignUpFlow/docs/playbooks/validation.md`). He also shipped **ListenToMe**, an on-device macOS/iOS meeting copilot with 96% core coverage and notarized releases, and **AI × QE**, a briefing platform with 116 evidence-cited slides. He teaches the workflow he runs daily: spec-driven, agent-assisted, evidence-recorded.

---

## 6. Testimonials

> **Beta cohort: these slots are reserved. No invented social proof appears on this page.** Quotes land here in before/after/result form after the first cohort. Until then the proof is the repository: open `SignUpFlow/specs/` and `SignUpFlow/docs/playbooks/validation.md`.

**[Reserved — 3 slots: before / after / result]**

---

## 7. FAQ

**Do I need a Mac?** No. Nothing in this bundle calls a model or touches audio. Python 3.11+, git, a terminal.

**Do I need to know FastAPI?** It helps for weeks 4–5; the lab fixes the app shape — three tables (`organizations`, `people`, `events`) and JWT auth (`course/03-content/m05-security-tests/lab.md`).

**How much time per week?** 3–5 hours. Weeks 3–5 are the heavy ones.

**Is this the full course?** No — it is four modules plus a launch slice out of nine. It excludes the on-device app track (M2–M3), the expertise-product track (M6), and the capstone demo (M8.3). The full course is $399 and is the better value if you want more than the SaaS track; the arithmetic is in `pricing.md`.

**What exactly do I leave with?** A spec folder that passes the stranger test, isolation and authorization tests with recorded red runs, a manifest validator you have watched reject a removed scenario, an evidence log in the repo's format, and a sourced pricing rationale plus sales page for your SaaS.

**Refunds?** Full refund within 14 days; keep the materials (`course/04-sales/pricing-and-platforms.md`, "Money-back guarantee").

---

## 8. Transparent pricing

| Tier | Price | What it is |
|---|---|---|
| **Spec-Driven AI SaaS (this bundle)** | **$199** | 4 modules + launch slice · 4 labs · 4 quizzes (32 questions) · lifetime access |
| **AI Product Studio — full course** | **$399** | All 9 modules, all 3 product tracks, 8 labs, 72 quiz questions, capstone rubric. **The recommended path** |
| **Studio Live — 8-week cohort** | **$1,490** | Everything in the full course plus weekly workshops, instructor code review, and demo day |

The bundle is deliberately a subset, and it is priced at the same per-module rate as the full course — $199 for roughly 4.5 modules against $399 for 9. If you want the on-device app track or the expertise-product track, buy the full course up front. You are not being steered into the smaller product here; you are being shown the door to the better one.

[**Get instant access — $199 →**]

*Prices are per person in USD. No fake countdowns; the price you see is the price. Refund within 14 days, keep the materials.*

---

## Authoring notes (not published)

- Length check: published copy (sections 1–8) is inside the 800–1,200 band for an under-$200 offer (research §E).
- Proof inventory: every claim above maps to a file — `SignUpFlow/specs/`, `SignUpFlow/docs/TESTING.md`, `SignUpFlow/docs/playbooks/validation.md`, `SignUpFlow/specs/014-security-hardening/`, `SignUpFlow/AGENTS.md`, `SignUpFlow/api/route_auth_policy.py`.
- Testimonial handling copies the full course's page (`course/04-sales/landing-page.md`): reserved slots plus an explicit no-invention note.
- One CTA, repeated verbatim at top, middle, and bottom. A/B test candidate: proof-first layout, badges above the headline, for cold technical traffic.
