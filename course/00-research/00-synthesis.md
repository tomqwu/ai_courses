# Cross-Repo Synthesis: The Method Behind Three Shipped AI Products

> This synthesis distills what the three production repositories — **ListenToMe** (native on-device AI app), **SignUpFlow** (spec-driven AI SaaS), and **ai_qe** (research-backed expertise product) — collectively teach. It is the intellectual core of the course. Detailed per-repo evidence lives in `01-listentome-deep-read.md`, `02-signupflow-deep-read.md`, `03-ai-qe-deep-read.md`.

## The three archetypes

| Archetype | Repo | Product shape | Core tech | Monetization pattern |
|---|---|---|---|---|
| **1. The native on-device AI app** | ListenToMe | macOS/iOS meeting copilot; real-time capture→transcribe→LLM loop | Swift 6, SwiftUI, Apple SpeechAnalyzer/WhisperKit, Ollama | Free & open-source + reputation funnel; commercial rivals charge $8–149/mo |
| **2. The spec-driven AI SaaS** | SignUpFlow | Multi-tenant volunteer scheduling platform (API + web + mobile + CLI) | FastAPI, SQLAlchemy 2.0, JWT, HTMX, Flutter, greedy solver | Classic SaaS subscription (billing deliberately feature-gated until ready) |
| **3. The expertise content product** | ai_qe | Research-backed briefing site with narrated decks, PDFs, and a consulting funnel | Jekyll, data-driven slides, Playwright QA, editioned releases | Consulting engagements; content as lead qualification |

## The unified method: six disciplines in one loop

Across all three repos, the same engineering culture shows up — call it the **Spec-to-Ship Loop**:

```
        ┌────────────────────────────────────────────────────────┐
        │                                                        │
        ▼                                                        │
  1. STUDY  ──  2. SPEC  ──  3. BUILD  ──  4. VALIDATE ──  5. RELEASE ──  6. PROVE
  (research,   (constitution,  (agents +     (tests, coverage    (notarize,      (evidence,
   competition   specs, plans    TDD, small    floors, playbooks,  TestFlight,     provenance,
   analysis,    an agent can    reviewable    real-contract       editions)       honest claims)
   positioning) execute)        edits)        tests)
```

1. **Study before solutioning.** ListenToMe's v1 spec began with a 12-competitor analysis that positioned the product at an empty market corner ("the transparent, on-device BYOK inverse of Cluely"). ai_qe's first principle: "Baseline before solutioning." SignUpFlow's research.md files evaluate options with pros/cons before committing. Positioning is a research artifact, not a slogan.

2. **Spec what agents can execute.** All three repos write machine-consumable intent: ListenToMe's design specs contain protocol-level interfaces and non-goals; SignUpFlow's spec-kit produces spec/research/data-model/plan/tasks/contracts artifacts, each with acceptance criteria a different agent session can verify; ai_qe's `_data/*.json` files make slide counts, routes, and gates reconcile by construction. The spec is the interface between human intent and agent execution.

3. **Govern the agents with layered, verifiable rules.** Constitution → AGENTS.md → CLAUDE.md → path-scoped files, every rule imperative and verifiable ("Filter every query by org_id"), anti-hallucination clauses ("grep the repo before referencing"), rule graduation pipelines (observation → tested on a real change → promoted rule), and explicit autonomy limits (YOLO off, reviewer agents can't merge). The unit of agent control is the *checkable instruction*, not the vibe.

4. **Validate with tiers, floors, and real-contract tests.** ListenToMe: 95% coverage floor in CI plus `make e2e` against a real local LLM. SignUpFlow: seven test tiers, 1,464 passing tests recorded with SHAs, playbook acceptance over six-week operational scenarios with an independent oracle and a machine-readable coverage manifest. ai_qe: five browser QA groups across two engines and three viewports, narration-hash review gates, PDF validators. Testing is designed so that *the system itself* detects drift — including the drift of docs, media, and claims.

5. **Release like it matters.** Signed, notarized, checksum-verified DMGs targeting the exact commit (ListenToMe); immutable, editioned releases where "an existing published edition is never overwritten" (ai_qe); atomic org bootstrap and serialized allocation transactions in the SaaS core (SignUpFlow). Dev/prod identity separation, feature-gating unsafe paths off by default (billing, SMS, cloud), and "AI off keeps capture working" are all the same principle: **fail safe, ship reversibly**.

6. **Prove everything — especially the limits.** This is the rarest discipline and the course's ethical spine. Evidence discipline: record commands, counts, dates, SHAs; never fabricate a status check; include the failures in the validation record. Claim discipline: label every number's epistemic status (task efficiency ≠ capacity ≠ cash saving); "planning inputs are not observed client results"; publish your own gap review (ListenToMe's 34-item gap inventory that said "do not promote 1.3.0") and your own site audit with remediations (ai_qe).

## Ten transferable principles (the course's spine)

1. **Positioning is engineering.** A 12-competitor comparison table with qualified, sourced claims (ListenToMe) is a stronger product decision tool than any brainstorm.
2. **Write specs agents can execute** — interfaces, non-goals, acceptance criteria, test-first tasks with exact file paths.
3. **Constrain agents with verifiable rules, layered by scope**, and keep instruction files under ~200 lines.
4. **Separate the testable core from platform glue** with protocols/seams (ListenToMeCore vs App/; pure data models vs Jekyll rendering).
5. **Route models by role, not by default** — per-pane/per-role model selection with local-first ranking and "good for" hints.
6. **Make privacy a mode, not a slogan** — fail-closed verification of model metadata, redirect rejection, truthful labels ("sends transcript and context").
7. **Test in tiers, accept with playbooks, enforce coverage floors, contract-test the real LLM outside CI.**
8. **Record evidence, not vibes** — commands, counts, SHAs, failures included; never fabricate a check.
9. **Treat content like code** — editions, review gates, provenance, QA suites, immutable releases.
10. **Monetize honesty** — qualified claims, published limits, and self-audits are *the* differentiator for premium products (and the reason all three repos are credible enough to teach from).

## Why these three, together

A single engineer, using AI agents under the discipline above, shipped:
- a **real-time, privacy-first, on-device AI app** with 96% core coverage and a signed public release,
- a **production-shaped multi-tenant SaaS** with 1,464 passing tests across seven tiers and 17 spec-kit feature folders,
- an **expertise product** of 116 narrated, evidence-cited slides with PDF editions and a consulting funnel.

That is exactly the portfolio the course asks students to begin: three product types, one operating system for shipping them, and the proof that the method works in public.