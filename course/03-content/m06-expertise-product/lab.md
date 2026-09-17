# Lab M6 — Build a Mini-Briefing
> Part of AI Product Studio (APS-3) · Pass/fail checkpoint for Module 6 · Companion lesson: `lesson.md` · Starter data: `evidence-dataset.md` · Self-check: `selfcheck.py`

## Goal

Turn research into a **trustworthy, sellable artifact**: a 12-slide mini-briefing in which every quantitative claim carries provenance and an epistemic label, one slide set serves two audiences through declared routes, and a hypothetical v2 goes through edition discipline. This is the archetype-3 lab checkpoint in the course rubric: "A 12-slide mini-briefing with provenance table + two audience routes + an edition decision."

## Prerequisites

- Modules 1–5 complete (you have a starter repo with `docs/research-log.md` from Lab M1).
- **A topic you actually know.** Default: the AI-testing evidence base — the six starter claims in `evidence-dataset.md` (METR: 19% *longer* completion, CI +2% to +39%; Peng: 55.8% faster, 95 freelancers, vendor-affiliated; Meta TestGen-LLM: 75%/57%/25% cumulative class-level yields; Uber FlakyGuard: 47.6% of *reproducible* flaky tests fixed; Google ICSE 2026: 90.1% triage accuracy, deployed on 52,635 failing tests; Bain: 10–15% average gains, rarely monetized) with source records in `ai_qe/docs/evidence/`. Alternative: your own domain, but then fetch the sources yourself — URLs, retrieval dates, real quotes.

## Time

~2.5 hours.

## Steps

1. **Write `research-log.md`** (dated, newest first, in the AI × QE format — `ai_qe/docs/research-log.md`): at least **6 entries**, each with Question / Checked / Outcome / Changed, including **at least 2 honest "not verified" or "open" entries** — things you looked for and could not confirm. Log before you draft slides; a claim that never enters the log never enters the deck.
2. **Build the provenance table** — one row per claim, using the template below. Label each row with one of the four levels from `ai_qe/docs/principles.md` (task-level efficiency / released capacity / hard-dollar saving / total-spend impact) and an epistemic label (measured / self-reported / vendor-affiliated / illustrative).
3. **Outline 12 slides.** Every **quantitative** slide cites ≥1 provenance row (by row number) and carries its epistemic label *on the slide*. Borrow the wording rules from `ai_qe/docs/economics/slide-language.md`: a self-reported number is never presented as measured; an illustrative scenario is labeled illustrative on the slide itself.
4. **Declare two routes over the SAME 12 slides** (stable slide IDs, modeled on `ai_qe/_data/briefing_routes.json`): an **executive route of 6 slides ending in a specific decision ask** ("fund Phases 0 and 1", not "transform QA" — `ai_qe/docs/economics/slide-language.md`), and a **technical route of 10 slides that retains the supporting evidence** the executive route skips.
5. **Write an edition decision record** for a hypothetical v2 in which one slide gains a new number: what changes, what is **deliberately retained**, and which editions bump (site vs content) — modeled on the `ai_qe/releases.md` entries ("Audio, subtitle timing, and the v1.24.0 PDF editions remain unchanged") and the separation in `ai_qe/_data/release.yml` (`version` vs `slide_edition`).
6. **Run the reconciliation gate on your own file.** Save the briefing — provenance table, slide outline and prose — as one Markdown file and run `python3 selfcheck.py your-briefing.md` from this folder (stdlib only, Python 3.11). It reads every sentence, table row and list item, and exits **1** listing each one that states a number with no citation *in the same unit*. Exactly three forms count as a citation: a backticked repo pointer with a line anchor (`ai_qe/docs/evidence/benchmarks.md:31`), a URL, or a `[source: …]` tag. Structural numbers ("slide 3", "row 12", "Phase 0", "edition 4") are not claims and are not flagged. **Pass = exit 0.** Run `python3 selfcheck.py --selftest` first: it checks itself against a passing and a failing excerpt (`selfcheck-examples/good.md` and `selfcheck-examples/bad.md`) so you can see what each verdict looks like before you run it on your own work. The script proves only that no number is an orphan. It cannot tell you a cited number is *right* — which is why `ai_qe/CONTRIBUTING.md:139-141` refuses to treat a resolving link as evidence — and it does not follow a `[source: row N]` tag to check that row N is itself sourced. Exit 0 is the floor, not the grade; rows 1–5 of the rubric are still yours to meet.

## Templates

**Provenance table** (one row per claim; reconciliation is checked in acceptance):

| # | Claim (exact slide wording) | Source URL | Retrieved | Claim type (level 1–4) | Epistemic label | What it supports |
|---|---|---|---|---|---|---|
| 1 | "Developers took 19% *longer* with AI assistance (CI +2% to +39%)" | https://metr.org/… | 2026-09-04 | Task-level (negative) | Measured — independent RCT | Task-efficiency risk; not a capacity number |
| 2 | … | … | … | … | … | … |

**Route declaration** (stable slide IDs; closing = the decision-ask slide):

```yaml
executive:
  slides: [1, 4, 7, 9, 11, 12]   # 6 slides
  closing: 12                    # ends on the decision ask
technical:
  slides: [1, 2, 3, 4, 5, 6, 7, 8, 9, 11]  # 10 slides — keeps the evidence
  full_order: [1,2,3,4,5,6,7,8,9,10,11,12]
```

## Acceptance checklist (all must be true)

- [ ] `research-log.md` has ≥6 dated Question/Checked/Outcome/Changed entries, ≥2 marked not-verified/open.
- [ ] **Reconciliation check:** every quantitative claim in the 12 slides maps to a provenance row (no orphan numbers).
- [ ] Every provenance row carries a source URL, a retrieval date, and a claim-type level.
- [ ] The executive route has exactly 6 slides and ends in a specific decision ask — **quote the ask** in your evidence record.
- [ ] The technical route retains ≥3 evidence slides the executive route skips (list the slide IDs).
- [ ] Every quantitative slide carries an epistemic label on the slide itself (self-reported / measured / vendor-affiliated / illustrative).
- [ ] The edition record distinguishes site vs content edition and states what v2 deliberately retains.
- [ ] **No uncited quantitative claim.** Self-paced: `python3 selfcheck.py your-briefing.md` exits 0 — paste the command and its last line. Cohort: one named peer reviewer confirms the same in writing. Either way, **name the path you used**; cohorts run the script too, because it catches what a reader skims past.

## Evidence to record

Commands or actions, outcomes, date, environment, limitations (the course format). Include: the full research log, the provenance table, the 12-slide outline with citations, both route declarations with the decision ask quoted, the edition decision record, and the reconciliation evidence: the verbatim `selfcheck.py` output with its exit status and the path you used (self-check or named peer review), plus the peer's written confirmation if you took the cohort path. If a source failed to fetch, record it in the manifest style of `ai_qe/research/document-manifest.json` (status: unavailable + reason) — an honest failure counts as evidence.

## Stretch goals

- **Write the 30-minute meeting script** (Align 5 / Explore 15 / Agree 10 — `ai_qe/briefings/index.md`) for your briefing: what you align on, which slides carry the explore segment, and the concrete agreement you close with.
- **Draft a 10-question role-routed questionnaire** following `ai_qe/docs/method/discovery-questionnaire.md`'s design rules: one form, role-routed at question 1; single-select on the questions that define success; mutually exclusive, gap-free ranges with an unknown option; and at least one financial-capture question.

## Discussion prompt

Post to the community with the template:

> **Mini-briefing M6 — [your name]**
> Topic: [your topic] · Decision ask: [quote your executive route's closing ask]
> Hardest row to prove: [claim] — the evidence I could NOT find was [not-verified item], so I [worded it down / dropped it / labeled it illustrative].
> One question for the group: [a sourcing or labeling judgment call you were unsure about].