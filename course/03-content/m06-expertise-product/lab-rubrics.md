# Lab Rubrics — M6 (Build a Mini-Briefing)

> Lab M6 is one of the eight pass/fail lab checkpoints in the **60% module-lab component** of the
> course grade (`01-design/assessment-and-rubrics.md`). Weighting below is *within* Lab M6 and sums to
> **100**. It does not change the course-level 60 / 20 / 20 split.
>
> **Pass rule.** Award a pass when every row is **Proficient or better** and the weighted total is
> **≥ 80**. Any row scored **Missing** fails the lab regardless of the total. Every criterion is
> observable from a submitted artifact; none is scored on taste.

## Level definitions

- **Exemplary** — the artifact would survive a skeptical client's audit without edits.
- **Proficient** — complete and correct; minor wording or formatting issues only.
- **Developing** — present but incomplete; a named acceptance item is absent or unverifiable.
- **Missing** — the artifact, or the required element, does not exist.

## Rubric

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---:|---|---|---|---|---|
| **1. Research log** | 15 | ≥8 dated entries; every outcome names what changed; ≥3 honest not-verified/open items with the search that failed | ≥6 dated Question/Checked/Outcome/Changed entries; ≥2 not-verified/open | Entries present but undated, or "not verified" claimed with no search described | Fewer than 6 entries, or no not-verified item | `research-log.md` |
| **2. Provenance table and level routing** | 25 | Every row has URL, retrieval date, level, epistemic label and "what it supports"; includes one negative or inconclusive record and one explicitly illustrative record; no measured level-3 or level-4 claim | Every row has URL, retrieval date and level; labels correct for all task-level and self-reported rows | Rows present but ≥1 lacks a retrieval date or a level, or a self-reported figure is labelled measured | Two or more rows unlabelled, or the illustrative model row unlabelled | Provenance table (Markdown or CSV) |
| **3. 12-slide outline with on-slide citations** | 25 | Exactly 12 slides; every quantitative slide cites a row by number and prints its epistemic label in the slide text; wording matches the Use list in `docs/economics/slide-language.md` | 12 slides; every quantitative slide cites a row and carries a label | ≥1 quantitative slide has no row citation, or the label lives only in speaker notes | Orphan numbers on two or more slides, or no 12-slide outline | Deck outline + citation map |
| **4. Two audience routes and the decision ask** | 20 | Executive route is exactly 6 slides ending on a quoted, bounded ask; technical route is 10 slides retaining ≥3 skipped evidence slides; both declare `closing` and share `full_order` | Executive route is exactly 6 with a quoted decision ask; technical route retains ≥3 skipped evidence slides | Route lengths off, or the ask is quoted but not decidable ("transform QA") | Rewritten slides used as a route, or no decision ask | Route YAML + quoted ask in the evidence record |
| **5. Edition decision record** | 10 | Distinguishes `version` from `slide_edition` exactly as `ai_qe/_data/release.yml` does; states what v2 deliberately retains **and why**; states that the published edition is not overwritten | Distinguishes site from content edition and states what v2 retains | Edition fields named but conflated, or "retained" listed with no reason | No edition record, or all editions bumped together with no retention statement | Edition decision record |
| **6. Peer review** | 5 | Reviewer named and dated; confirms no uncited quantitative claim; lists one specific row the reviewer challenged | Reviewer named in writing; confirms no uncited quantitative claim | Verbal or unnamed confirmation only | No peer review | Reviewer's written confirmation |

## Auto-fail conditions

1. **Fabricated evidence** — a source URL, retrieval date, statistic or quote that does not resolve or
   that the student did not retrieve. This mirrors the course rule that fabricating a test result or
   evidence line is the only automatic fail.
2. **A self-reported figure headlined as measured** — the Bain-style error, presented on a slide with
   the label "measured".
3. **A task-level number sold as a budget saving** — a level-1 figure presented as a hard-dollar
   outcome with no named budget line and no Finance confirmation.
4. **An uncited quantitative claim that the peer review missed and the student left in** — the
   reconciliation check is the pass gate; one orphan number that survives review still fails.
5. **Routes that rewrite slides** — an "executive route" that paraphrases slide content instead of
   reordering stable IDs.
6. **The published edition overwritten** — an edition record that republishes over an existing
   edition or resets a baseline to clear a stale-review failure.

## Grading notes

- **Reconciliation is checked mechanically.** Walk the 12 slides in one pass and ask of each
  quantitative slide: which row number, and which label? Two minutes per submission catches failure
  mode 4, which is the most common.
- **The negative or inconclusive row is the honesty tell.** A table with ten positive rows and no
  METR-style negative result usually means the student selected evidence to fit a deck.
- **Do not grade prose quality.** A terse, correctly labelled deck outscores a polished one with one
  unlabelled percentage. Point students at `ai_qe/docs/economics/slide-language.md` for wording, not
  at the rubric.
- **Self-paced mode.** Rows 1–5 are self-verified against this table; row 6 becomes a paired review in
  the community, per the self-paced adjustments in `02-instructor/instructor-guide.md`.
