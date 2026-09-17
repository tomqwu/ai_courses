# Mini-briefing v1 — an excerpt that passes the self-check

Every sentence here that states a number carries a citation in the same sentence, table row or list
item. Three forms count: a backticked repo pointer with a line anchor, a URL, or a `[source: …]`
tag. The record fields come from the AI × QE research conventions — date, sample, method, unit,
self-reported vs measured, sponsor, and the claim each record supports
(`ai_qe/CONTRIBUTING.md:93-94`).

## Provenance table

| # | Claim (exact slide wording) | Source | Retrieved | Level | Epistemic label |
|---|---|---|---|---|---|
| 1 | "AI-allowed issues took 19% longer (CI +2% to +39%)" | `ai_qe/docs/evidence/benchmarks.md:31` | 2026-09-04 | Task-level, negative | Measured, independent |
| 2 | "16 experienced maintainers, 246 real issues, randomized" | `ai_qe/docs/evidence/benchmarks.md:40` | 2026-09-04 | Sample and method | Measured |
| 3 | "55.8% faster (71.2 vs 160.9 minutes)" | `ai_qe/docs/evidence/benchmarks.md:97` | 2026-09-04 | Task-level | Measured, vendor-affiliated |
| 4 | "47.6% of reproducible flaky tests received fixes; only 71.6% were reproducible" | `ai_qe/docs/evidence/testing-studies.md:50` | 2026-09-04 | Task-level, testing | Measured, industrial |
| 5 | "Completion time −18% and −4%; both intervals include no effect" | https://metr.org/blog/2026-02-24-uplift-update/ | 2026-09-04 | Task-level, inconclusive | Measured |
| 6 | "Base case releases 3.3% of capacity and 0.45% of net cash" | `ai_qe/docs/economics/savings-model.md:115` | 2026-09-04 | Released capacity | Illustrative |

## Slide outline (excerpt)

- Slide 3 — "Maintenance work took 19% longer with assistance" [source: row 1]
- Slide 4 — "55.8% faster on one synthetic task, vendor-affiliated" [source: row 3]
- Slide 8 — "47.6% of reproducible flaky tests fixed" [source: row 4]
- Slide 10 — illustrative model, labelled illustrative on the slide itself [source: row 6]
- Slide 11 — 3.3% capacity is the base the scenario re-runs from [source: row 6]

## Prose that still cites

The independent trial is the one number worth arguing with: experienced maintainers were 19% slower
on their own repositories, and the confidence interval runs from +2% to +39%
(`ai_qe/docs/evidence/benchmarks.md:31`). The speed-up most decks quote instead was measured on one
synthetic task, at 55.8% (https://arxiv.org/abs/2302.06590). Both are real results and neither is a
budget number.

## Numbers that are structure, not claims

Slide 3 cites row 1 and slide 8 cites row 4; the citation map is the reconciliation check.
The 12-slide outline, the executive route and the technical route are unchanged this edition.
Phase 0 and Phase 1 are the funded phases; the questionnaire stays at edition 4 and the deck at
`v1.24.0`.

1. Read the provenance table.
2. Walk the slides and name the row each number comes from.
3. Fix the orphans.
