# Lab Rubrics — Lab M8 (Capstone)

> Lab M8 is the capstone. This rubric is the lab-scale instrument; it scores the same five dimensions
> as `01-design/assessment-and-rubrics.md` (which maps Lab M8 to the capstone's 20% of the course grade,
> alongside labs M0–M7 at 60% and quizzes at 20%). Five criteria, 20 points each. **Pass = ≥80 total and
> no criterion below Proficient.** Levels: **Exemplary** (100% of the row), **Proficient** (80%),
> **Developing** (50%), **Missing** (0). Score self → peer → instructor (cohort: instructor final at
> demo day).

## Deliverable map (so the score is traceable to an artifact)

| Artifact | Primary criterion |
|---|---|
| Spec folder or scope spec | C1 Spec quality |
| Failing-test-first commit | C2 Build discipline |
| Validation evidence record | C3 Evidence honesty |
| Local-only tests / tenant isolation / reconciled provenance | C4 Discipline |
| Tagged release or deployed URL | C2 and C5 |
| Sales page, 5-email arc, demo | C5 Launch-readiness |

## C1 — Spec quality (20 points)

| Level | Observable standard | Evidence required |
|---|---|---|
| Exemplary | A fresh agent session implemented one story from the artifacts alone, no conversation context; checklist gate passed first review | Session transcript or commit + spec files |
| Proficient | Complete artifacts for the shipped scope; ≥2 stories independently testable; acceptance criteria concrete Given/When/Then; non-goals listed | Spec folder (Type 2) or scope spec (Types 1/3) |
| Developing | Spec exists but stories share a criterion, or acceptance criteria are descriptive rather than testable | Spec file with review comments |
| Missing | No spec, or a topic outline that no test could fail | — |

## C2 — Build discipline (20 points)

| Level | Observable standard | Evidence required |
|---|---|---|
| Exemplary | Coverage floor enforced in the suite; negative-path or red-team tests included; a real-provider contract test gated outside CI | Makefile/CI config + test files + run output |
| Proficient | A failing-test-first commit is visible as its own commit; commits are small and reviewable; core separated from glue via protocols/seams | `git log --stat` excerpt |
| Developing | Tests added after implementation in the same commit; no red run anywhere in history | History excerpt showing no red run |
| Missing | No tests, or tests that assert nothing | — |

## C3 — Evidence honesty (20 points)

| Level | Observable standard | Evidence required |
|---|---|---|
| Exemplary | A gap-style self-review identifies known limitations with priorities; a not-verified list of ≥2 honest items; failures kept beside passes | Self-review file + evidence record |
| Proficient | Commands with counts, a date, environment, and limitations; failures included, not hidden | Capstone evidence record |
| Developing | Counts present but no date or environment; limitations omitted | Evidence record |
| Missing | "All tests pass" with no command, or a result that was not produced | — |

## C4 — Discipline artifact (20 points)

*Type 1/2 = privacy/safety engineering; Type 3 = claim discipline.*

| Level | Observable standard | Evidence required |
|---|---|---|
| Exemplary | Multiple defenses layered with a test for each (metadata verification + redirect rejection + truthful labels), or full four-level claim labeling with reconciled provenance | Test files or provenance table + reconciliation check |
| Proficient | Local-only/fail-closed mode tested, **or** tenant isolation with negative-path tests, **or** a provenance table that reconciles every shipped claim | Archetype test run or provenance table |
| Developing | The mechanism exists but is untested, or three or more claims have no provenance row | Source or table with gaps marked |
| Missing | No discipline artifact for the archetype | — |

## C5 — Launch-readiness (20 points)

| Level | Observable standard | Evidence required |
|---|---|---|
| Exemplary | Page ready to publish; arc personalized with the student's own proof assets; demo delivered (recorded or live) | Page, arc, demo link |
| Proficient | Positioning one-liner; pricing rationale with sourced comparators; 8-section page with one CTA; 5-email arc with one CTA each and a stated deadline; demo in four beats ending on limits | Page draft, arc, demo recording |
| Developing | Page missing sections or carrying an unsourced claim; arc has no deadline statement | Page + arc |
| Missing | No page, no arc, or no demo | — |

## Auto-fail conditions (fail the lab regardless of the row scores)

1. **Fabricated evidence** — a command, count, date, or output that never ran, or a testimonial the student wrote.
2. **A green run with no red run recorded** — no failing-test-first commit and no captured failure in the history.
3. **A demo that never ran** — no recording, no live delivery, or a video of slides only.
4. **Tests weakened to pass** — assertions deleted, skipped, or inverted to reach green; check the diff, not the badge.
5. **An unsourced number on the sales page** — a market statistic, coverage figure, or user count with no file behind it.
6. **The plan was not peer-reviewed before building** — the single gate the lab places before the work.

## Scoring notes for the instructor

- A complete loop at small scope scores higher than a sprawling half-loop: C2 and C3 are where size stops mattering.
- Grade the evidence record as a document, not the product: is every claim traceable to something that ran?
- Type 3 students are graded on claim discipline, not privacy engineering; do not penalize the archetype.
- Peer scores are advisory. Where peer and instructor differ by ≥10 points, name the artifact that decided it in the feedback.
- Students may use agents for everything. The record must state what the agent did and what the student verified.
