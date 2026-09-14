# Starter Evidence Dataset: AI-Assisted Development & Testing Claims

> For Lab M6 (mini-briefing). These claims are extracted from the AI × QE research base (`ai_qe/docs/evidence/`, `ai_qe/research/`) and its source records. Each row is deliberately labeled with its **claim type** (the four levels from `ai_qe/docs/principles.md`: task-level efficiency / released capacity / hard-dollar saving / total-spend impact) and its **epistemic status**. Use these to seed your provenance table and slides, or fetch your own sources the same way.

## The four claim levels (never mix them)

| Level | Definition | Who can confirm it |
|---|---|---|
| Task-level efficiency | Net time reduction for a specific activity, after review/correction effort | Pilot measurement |
| Released capacity | Reduction in human hours across the full workflow, after adoption and eligibility | Pilot + baseline capture |
| Hard-dollar saving | Budgeted cost Finance can actually remove or avoid | Finance, against a named budget line |
| Total-spend impact | Broader engineering/delivery cost — must not be mislabeled as QA saving | Finance + CIO office |

## Evidence rows

| # | Claim | Claim type | Epistemic status | Source record |
|---|---|---|---|---|
| 1 | Developers completed real maintenance tasks **19% slower** with AI assistance (CI +2% to +39%); they *expected* 24% faster and *believed* 20% faster afterward | Task-level (negative) | Measured — independent RCT, 16 experienced maintainers, 246 issues | METR early-2025 study (via `ai_qe/docs/evidence/benchmarks.md`) |
| 2 | METR's Feb-2026 follow-up: −18% and −4% point estimates, **both confidence intervals cross zero**; 57 devs, 800+ tasks | Task-level (inconclusive) | Measured — independent, selection bias limited | METR follow-up (via `ai_qe/docs/evidence/benchmarks.md`) |
| 3 | Codex users completed a coding task **55.8% faster** | Task-level | Measured — but vendor-affiliated, 95 freelancers, one synthetic task | Peng et al. 2023 (via `ai_qe/docs/evidence/benchmarks.md`) |
| 4 | AI assistance associated with **+26.1%** completed tasks (SE 10.3) | Task-level | Measured, large-N field data | Cui et al. (via `ai_qe/docs/evidence/benchmarks.md`) |
| 5 | Developers with Copilot access produced **+8.7% more pull requests** | Output metric (≠ time saved) | Measured — vendor-published quasi-experiment | GitHub/Accenture (via `ai_qe/docs/evidence/benchmarks.md`) |
| 6 | Organizations report average efficiency/productivity gains around **10–15%**, rarely monetized as savings | Task-level | Self-reported consultancy estimates — not audited savings | Bain (via `ai_qe/docs/evidence/benchmarks.md`) |
| 7 | Coding ≈ **16% of developer time**; code generation ≈ 25–35% of idea-to-launch — so a 50% task gain **dilutes to single digits** of total engineering time | Denominator evidence | Survey-based | Atlassian; Bain (via `ai_qe/docs/evidence/reading-the-evidence.md`) |
| 8 | TestGen-LLM: cumulative class-level yield **75% → 57% → 25%** across improvement/coverage/build-failure categories | Task-level (testing) | Measured — industrial deployment study | Meta (via `ai_qe/docs/evidence/testing-studies.md`) |
| 9 | FlakyGuard fixed **47.6% of reproducible flaky tests** (51.8% of fixes accepted) — but only **71.6% were reproducible** | Task-level (testing) | Measured — industrial; denominators matter | Uber (via `ai_qe/docs/evidence/testing-studies.md`) |
| 10 | Automated failure triage reached **90.1% accuracy** on 71 manually-evaluated failures; deployed on 52,635 failing tests | Task-level (testing) | Measured — industrial deployment | Google ICSE 2026 (via `ai_qe/docs/evidence/testing-studies.md`) |
| 11 | The illustrative banking economics model: base case **3.3% capacity released → 0.45% net cash** ($45,000 per $10M QA spend); zero-capture scenario is **negative** (−$120,000) | Released capacity / hard-dollar | **Illustrative model — planning inputs are not observed client results** | `ai_qe/docs/economics/savings-model.md`, `_data/scenarios.json` |
| 12 | Not verified (as of the site's research log): any Gartner productivity figure as a *measured* effect; WQR cost-of-quality share; Snyk accuracy claims | — | Explicitly not-verified list | `ai_qe/docs/research-log.md` |

## Slide-wording rules (from `ai_qe/docs/economics/slide-language.md`, summarized)

1. Never present a self-reported percentage as a measured one.
2. Keep task-level and capacity figures on separate lines with separate labels.
3. Any illustrative scenario is labeled *illustrative* — on the slide itself, not in a footnote alone.
4. "The decision requested is whether to fund Phases 0 and 1, not whether to transform QA."

## How to extend this dataset (the actual lab skill)

1. Add a dated `research-log.md` entry *before* editing any page: Question / Checked / Outcome / Changed / Open.
2. Record retrieval: URL, date, and (for files) a SHA-256 — mirror `ai_qe/research/document-manifest.json`.
3. If a source can't be fetched or verified, add it to the "Not verified" list instead of citing it.