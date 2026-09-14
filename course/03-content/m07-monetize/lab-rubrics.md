# Lab Rubrics — Lab M7: Price and position your product

> Lab M7 is an open-ended, artifact-producing lab, so it is graded against observable evidence rather
> than a single correct answer. It counts as one of the eight module labs in the 60% lab component of
> `course/01-design/assessment-and-rubrics.md` (labs 60% / quizzes 20% / capstone 20%). Cohort students
> are reviewed by the instructor in the week-7 workshop; self-paced students are peer-reviewed against
> these tables. **Pass = ≥80 total, no criterion scored Missing, and no auto-fail condition present.**
> Weights sum to 100 across the three tables.

## Table A — Pricing evidence and decision (Lab M7 Steps 1–2) · 45 points

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Sourced competitor table | 20 | ≥5 rows actually visited; every price cell has URL + retrieval date; unconfirmed cells qualified "approximately/reportedly" | ≥5 rows; all cells dated; one or two qualifiers absent | 5 rows but some cells undated or unsourced | <5 rows, or prices from memory | `docs/pricing.md` table |
| Cost floor arithmetic | 10 | Floor in dollars, each line named (hosting, API keys, amortized dev), break-even sales/month computed | Floor numeric; break-even implied not computed | Floor listed but not numeric | No floor, or a qualitative "it's cheap" | Floor block in worksheet |
| Comparator band and value anchor | 5 | Band stated as min–max with row names; anchor names what is replaced and its worth | Both present; band rows unnamed | One of the two present | Neither present | Worksheet lines |
| Model matches cost structure | 5 | Chosen model explicitly derived from the cost column (recurring → subscription; none → one-time) with the row named | Model stated with a one-line reason | Model stated with a generic reason | Subscription with no recurring per-user cost identified | Worksheet "Chosen model" line |
| Rationale | 5 | ≥150 words, names ≥3 specific competitor rows, defends the price in both directions | ≥150 words, names ≥2 rows | Present but <150 words or names no row | Absent or copied | Rationale block |

## Table B — Positioning and packaging (Steps 3–4) · 35 points

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| One-liner form | 8 | Adjective-wedge × differentiators × audience; every clause specific to this product | Full form; one clause generic | Feature list, or audience absent | "The best AI tool"-class line | `docs/positioning.md` one-liner |
| Clause → column mapping | 7 | One mapping line per clause, each naming a table column or repo capability | Mapping present but one clause unmapped | Mapping only for some clauses | No mapping | Mapping table/list |
| Deletion test applied | 5 | Each clause tested; at least one decoration clause identified and cut, with the row that would notice | Deletion test described; result stated | Test mentioned, no result | Not attempted | Deletion-test note |
| Packaging page | 10 | Every tier has "NOT included — because" lines, each with a reason; paid-but-unproven paths flagged, never the core | "NOT included" per tier with brief reasons | Included lists only, no exclusions | Tiers gate the core workflow | Packaging page |
| Price the transformation | 5 | Tiers price artifacts and outcomes a buyer can show, not hours or volume | Mostly artifact-based; one volume-priced row | Priced by hours/volume | A bare-recording-library tier sold alone | Tier table |

## Table C — Skeptical-engineer review and honesty (Step 5 + checklist) · 20 points

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Buyer objections | 8 | Three objections the table itself invites; each answered with a named row + source or a file pointer; one answer caused a price or page revision | Three objections, each answered with evidence | Fewer than three, or answers are adjectives | Objections are softballs or unanswered | Objections section |
| Honest-marketing checklist | 7 | All five items run, each with a quoted pass tying it to an artifact | Five items run with passes | Some items run | Checklist absent | Checklist run with quotes |
| Verdict recorded | 5 | One-line verdict plus the objection that almost flipped it, and why it didn't | Verdict line present | Verdict only | No verdict | Final line of `docs/pricing.md` |

## Auto-fail list

These fail Lab M7 regardless of the score above.

1. **A price with no source URL or retrieval date** — fabricated evidence, the only automatic fail per
   `course/01-design/assessment-and-rubrics.md`.
2. **A fabricated objection answer or copied rationale** presented as the student's own arithmetic.
3. **Gating the core workflow to force upgrades** — a tier that stops the product working until paid,
   contrary to `SignUpFlow/AGENTS.md`: "core scheduling must not require either paid integration."
4. **A positioning one-liner with zero traceable clauses** — no clause maps to a column, so the
   deletion test cannot be run.
5. **No "NOT included" line for any tier** — the packaging page claims completeness no tier can support.
6. **A price stated below the student's own stated cost floor** without acknowledging the subsidy.

## Scoring notes

- Grade the **evidence**, not the price point. Two students pricing the same product at different
  numbers can both be Exemplary if each defends the number with the table and the floor.
- A subscription is defensible without recurring compute only if the student names a recurring
  *service* line (hosting, sync, support).
- The floor line is the most commonly faked row: ask for the arithmetic, not the figure.
- Partial credit below the stated band follows the Developing column; a row is Missing only when the
  artifact contains nothing observable.
