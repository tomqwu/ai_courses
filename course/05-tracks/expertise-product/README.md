# Expertise as a Product — Track Bundle

> **AI Product Studio · Track 3 of 3 · 6 weeks · self-paced · $199**
> Turn what you know into a defensible content product that sells a measurement, not a promise.

## The promise

By the end of six weeks you will have built a **sellable expertise product**: a 12-slide evidence-cited mini-briefing with a provenance table, two audience routes over the same slides, an edition decision record, a priced offer, and a sales page whose every claim carries a date, a source, and a claim level.

The distinguishing rule of this bundle is the one the case study runs on: **every claim you publish carries a date, a sample, a method, a unit, and a level — and your funnel sells a measurement, not an outcome.** You will label each number as task-level efficiency, released capacity, hard-dollar saving, or total-spend impact, and you will not let one appear as another (`ai_qe/docs/principles.md`).

That is not a style preference. It is the conversion mechanism. A buyer who reads your "what this doesn't prove" list stops asking *why should I believe you* and starts asking *when can we start*.

## Who this is for

- Senior engineers, tech leads, architects, and consultants who already know something worth selling.
- Practitioners who want to productize expertise — briefings, workshops, assessments, advisory — without inventing outcomes they cannot evidence.
- Anyone who has watched a competent expert lose a deal to a louder deck and wants the opposite strategy: out-audit the hype.

**Prerequisites:** comfort with git and a text editor; Python 3.11+ and Ollama for the setup week (`course/03-content/m00-orientation/lab.md`), both free and cross-platform. No ML background. You bring a topic you actually know; that topic is the raw material.

**Not for:** beginners looking for their first programming course; anyone who wants "AI side hustle" content with no artifact; teams seeking an enterprise AI-governance compliance curriculum.

## The case study: ai_qe

The worked example throughout is **AI × QE** (`github.com/tomqwu/ai_qe`), a research-backed briefing site on AI-assisted quality engineering with a consulting funnel behind it. You will open its actual files, not summaries:

- **116 narrated slides across 4 decks** — 21 + 33 + 26 + 36 (`ai_qe/_data/briefing_room.json`).
- **Four claim levels** with the rule "mixing them is the most common error in AI business cases" (`ai_qe/docs/principles.md`).
- **A published 14-finding self-audit** — four high priority, nine medium, one lower — with a remediation table mapping finding → response → verification (`ai_qe/research/reviews/site-audit-2026-09-06.md`, `ai_qe/research/reviews/remediation-2026-09-06.md`).
- **SHA-256 provenance manifests** — including one retrieval honestly logged as `"status": "unavailable"` (`ai_qe/research/document-manifest.json`).
- **Audience routing over stable slide IDs**, with focused routes ending on a decision discussion (`ai_qe/_data/briefing_routes.json`, `ai_qe/CONTRIBUTING.md`).
- **Editioned immutable releases** — site vs slide vs questionnaire vs research editions (`ai_qe/_data/release.yml`, `ai_qe/releases.md`).
- **A questionnaire → discovery → capped phased pilot funnel**, with sponsor-signed go/no-go gates, 10%/15% effort bands, and ≥30 comparable tasks per arm (`ai_qe/docs/method/phased-pilot.md`, `ai_qe/_data/pilot_gates.json`).

**Honest scope of that case study.** The ai_qe funnel stages are *planned and recorded* stages, not delivered client results. The site says so itself: "Planning inputs and proposed outcomes are not observed client results" (`ai_qe/README.md`), and its engagement record states plainly that "No client price or start date has been agreed" (`ai_qe/_data/engagement.json`). This bundle teaches the method *and* the disclosure — you will write the same kind of qualifier for your own product.

## What's included

| Component | Source | You get |
|---|---|---|
| Orientation & setup | M0 (all 3 segments) | Lab M0, Quiz M0 |
| The AI product operating system | M1 (all 3 segments) | Lab M1, Quiz M1 |
| The expertise product | M6 (all 3 segments) | Lab M6 + evidence dataset, Quiz M6 |
| Monetization slice | M7.1–M7.3 | Lab M7 pricing worksheet (adapted for Type 3), Quiz M7 |
| Launch slice | M8.1–M8.2 + Type 3 capstone variant | Lab M8 Type 3 scope, Quiz M8 |

You also get the module lesson text (searchable), the lab acceptance checklists, the starter evidence dataset (`course/03-content/m06-expertise-product/evidence-dataset.md`), and the evidence-record template from M1.3.

## Six-week map

| Week | Focus | Build |
|---|---|---|
| 1 | Orientation: three products, one method | Environment ready; first ship-win; Quiz M0 |
| 2 | Your operating system: rules, specs, evidence discipline | Starter repo + one spec→plan→TDD loop; Quiz M1 |
| 3 | Credibility is the product: provenance and claim levels | Research log + provenance table; 12-slide outline |
| 4 | One research base, many audiences; content as code | Two routes, decision ask, edition record; Lab M6 passes |
| 5 | Price, package, position — and write the page | Sourced pricing worksheet + 8-section sales page |
| 6 | Launch arc and capstone | Public mini-briefing + launch mini-arc; capstone evidence record |

Full detail, time budgets, and assessment weights are in `syllabus.md`.

## Honest scope note

This is a **subset**. The full course, *AI Product Studio*, covers all three archetypes — the on-device AI app, the spec-driven SaaS, and the expertise product — across 9 modules and 8 labs. This bundle uses only the modules one expertise product needs: M0 and M1 for the method, M6 for the archetype, and a slice of M7/M8 for monetization and launch.

If you want to build and sell all three product types, buy the full course. It is the better value and the recommended path: **$399** for 9 modules, 8 labs, 72 quiz questions, and the capstone rubric (`course/04-sales/pricing-and-platforms.md`). See `pricing.md` for the full comparison.

Nothing here is a demo. Every lab ends in an artifact you can show a buyer, and every factual claim about the case-study repo carries a file pointer you can open under this workspace.

## FAQ

**Do I need a Mac?**
No. The setup week uses Python 3.11+ and Ollama, which run on macOS, Linux, and Windows (`course/03-content/m00-orientation/lab.md`). This track does not use the Swift material.

**Do I need an audience or an email list to start?**
No. The bundle builds the product first. The launch slice teaches the arc; you can run it against twenty opt-in people, which is a real number (`course/03-content/m08-launch-capstone/lab.md`).

**What if I don't have a topic?**
Use the provided AI-testing evidence dataset — six starter claims with sources and epistemic labels (`course/03-content/m06-expertise-product/evidence-dataset.md`). It is a complete, real dataset; you will build the same artifacts you would build for your own domain.

**Will you teach me to promise savings?**
No. The opposite. You will learn to price the *measurement* — the discovery, the baseline, the instrumented pilot — and leave outcomes to a benefits-realization register tied to a Finance-owned budget row (`ai_qe/docs/method/phased-pilot.md`).

**Are there testimonials?**
Not yet, and none are invented. The case-study repos are the pre-beta proof: 116 evidence-cited slides, a published self-audit, and provenance files you can open. Reserved testimonial slots fill from real buyers, in before/after/result form.

**How much time per week?**
4–7 hours. Weeks 3–6 are heavier because you are producing artifacts, not watching lessons.

**Refunds?**
Fourteen days, no questions. Keep the materials.

---

*Part of AI Product Studio (APS-3). Every factual claim in this bundle resolves to a file under this workspace. If you cannot open a file and verify a claim, the claim is wrong — say so.*
