# Syllabus — Expertise as a Product (6 weeks)

> **AI Product Studio · Track 3 of 3 · self-paced · $199**
> Modules used: M0, M1, M6 in full; a monetization slice of M7 and a launch slice of M8.
> Every week ends in an artifact. Pass criteria are objective: a table reconciles, a route ends on a decision, a page carries no unsourced number.

## How the six weeks work

Each week has one outcome, one lab checkpoint, and one quiz. Lessons are 5–15 minutes each; every lesson ends with an action step. Budget 4–7 hours per week, front-loaded toward doing.

| Week | Weekly outcome | Modules / segments | Lab | Quiz | Time budget | Assessment |
|---|---|---|---|---|---|---|
| **1** | Environment proven: three case studies cloned, a production solver run, one local model answering. You can name the six loop stages and each repo's proof asset. | M0.1 Why three types · M0.2 The Spec-to-Ship Loop · M0.3 Set up and first win | **Lab M0** — Environment Setup & First Ship-Win (20–40 min) | **Quiz M0** — 8 Q (archetypes, proof assets, loop stages) | 3–5 h (≈30 min lesson, 20–40 min lab, downloads) | Lab M0 acceptance checklist (6 items, pass/fail); Quiz M0 auto-graded. First-win post with solver health-score line + `ollama list`. |
| **2** | Your own operating system exists: a starter repo with `constitution.md`, `AGENTS.md`, spec templates, and a research log — proven by one red→green TDD mini-loop with a recorded evidence entry. | M1.1 Govern agents · M1.2 Spec → plan → tasks · M1.3 Evidence discipline | **Lab M1** — Build Your Operating System, Then Run One Loop (~2 h) | **Quiz M1** — 8 Q (rule verifiability, precedence, artifact jobs, evidence format) | 4–6 h (≈60 min lesson, 2 h lab, 30 min quiz/review) | Lab M1 acceptance checklist (10 items); evidence entry with commands, counts, date, environment, limitations, head SHA; red run recorded *before* the green run. |
| **3** | Research you cannot verify is on a list, not on a slide. You can label any number with one of the four claim levels and name who could confirm it. | M6.1 Credibility is the product | **Lab M6, Steps 1–2** — `research-log.md` (≥6 dated entries, ≥2 not-verified/open) + provenance table seeded with claim level and epistemic label per row | **Quiz M6 · Q1–Q4** (claim levels, provenance requirements) | 4–6 h (≈25 min lesson, 2 h lab work, 30 min quiz) | Research log dated and structured Question / Checked / Outcome / Changed; provenance rows carry source URL, retrieval date, level, and label. |
| **4** | One research base serves two audiences without forking, and your content obeys release discipline. Lab M6 passes. | M6.2 One research base, many audiences · M6.3 Content as code | **Lab M6, Steps 3–5 (complete)** — 12-slide outline with citations on every quantitative slide; executive route (6 slides, specific decision ask) + technical route (10 slides, retains ≥3 evidence slides); edition decision record | **Quiz M6 · Q5–Q8** (route design, edition discipline, pilot gates) | 5–7 h (≈50 min lesson, 2.5 h lab, 30 min quiz + peer review) | **Lab M6 acceptance checklist (8 items)** — reconciliation check every quantitative claim → provenance row; the decision ask quoted in the evidence record; one peer review confirms no uncited quantitative claim. |
| **5** | Your product has a price, a position, and a page. Every number on the page carries a source, and the page's length is set by the price. | M7.1 Pricing the three archetypes (Type 3 funnel in depth) · M7.2 Packaging and platforms · M7.3 Honest marketing that converts · M8.1 The sales page | **Lab M7 (adapted)** — sourced pricing table (≥5 rows), pricing worksheet, positioning one-liner with clause→column mapping, packaging page with explicit "not included" lines | **Quiz M7** — 8 Q (archetype pricing, feature-gating rationale, honest claims, tier design) | 5–7 h (≈80 min lesson, 2 h lab, 30 min quiz) | Lab M7 checklist (8 binary items) incl. the skeptical-engineer verdict line; **8-section sales page draft** with one CTA and no unsourced claim; word target set from price. |
| **6** | The product is launched and provable: a public briefing link that works from a clean browser, a real launch arc, and a capstone evidence record ending on a "not verified" list. | M8.2 The launch arc · M8.3 Type 3 capstone variant | **Lab M8 (Type 3 row)** — expand the M6 briefing to 20 slides, reconcile every claim to a provenance row, draft the questionnaire, deploy to any static host, record the evidence | **Quiz M8** — 8 Q (page anatomy, email sequence, launch math, capstone rubric) | 6–9 h (≈50 min lesson, 6–8 h capstone, 30 min quiz) | **Type 3 capstone** — public link verified from a clean browser; provenance reconciles; 5-email mini-arc; 5-minute demo ending on limits; evidence record complete. Pass = rubric ≥80% with no dimension below 3. |

## Assessment model

Consistent with `course/01-design/assessment-and-rubrics.md` — labs 60% / quizzes 20% / capstone 20%.

| Component | Weight | What is collected | Pass condition |
|---|---|---|---|
| **Lab checkpoints** | 60% | Lab M1 operating-system repo + evidence entry; Lab M6 research log, provenance table, two routes, edition record; Lab M7 pricing table, worksheet, one-liner, packaging page | Each lab's acceptance checklist is fully checked. Lab M0 is the gate, not a weighted component — no checkpoint counts until it passes. |
| **Quizzes** | 20% | Quiz M0, M1, M6, M7, M8 (8 questions each; answer keys included in each quiz file) | 80% correct across the set; short-answer items graded against the model answers in each key. |
| **Type 3 capstone** | 20% | Public mini-briefing (≥20 slides) with reconciled provenance, questionnaire draft, deployed link, 8-section sales page, 5-email mini-arc, 5-minute demo, evidence record | Rubric ≥80% total and no dimension below 3 (meets). Dimensions: spec quality, build discipline, evidence honesty, claim discipline, launch-readiness. A fabricated result or evidence line is an automatic fail. |

## Cross-week rules that apply to every artifact

1. **Every factual claim about a case-study repo carries a file pointer** that resolves under this workspace. If you cannot open it, do not write it.
2. **Every evidence entry includes limitations.** A record that cannot say "not verified" is marketing (`course/03-content/m01-operating-system/lesson.md`, M1.3).
3. **Every published number carries a level** — task-level efficiency, released capacity, hard-dollar saving, or total-spend impact — and never two at once (`ai_qe/docs/principles.md`).
4. **No invented social proof.** Use the honest placeholder pattern until real buyers exist.

## What this bundle deliberately omits

Weeks 2–5 of the full course (the on-device app in M2–M3 and the spec-driven SaaS in M4–M5) are not included here. That omission is why the bundle is $199 and the full course is $399 — see `pricing.md`. If you want all three archetypes, take the full course; it is the recommended path and the better value.
