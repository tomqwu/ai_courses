# Solutions — Lab M6 (Build a Mini-Briefing)

> Lab M6 is an **open-ended lab**: the reference answer is a worked exemplar, not a single correct
> answer. It uses the claims dataset in `evidence-dataset.md` (records from
> `ai_qe/docs/evidence/benchmarks.md`, `ai_qe/docs/evidence/testing-studies.md` and
> `ai_qe/docs/economics/savings-model.md`). Any topic the student knows is accepted, provided every
> claim carries a source URL, a retrieval date and a claim level.

## Reference exemplar — the 12-slide deck

1. Title: "What the evidence supports, and what it does not."
2. Why this matters: task-level gains are not budget savings.
3. METR: 19% longer (CI +2% to +39%), 16 maintainers, 246 issues.
4. Peng: 55.8% faster, 95 freelancers, one synthetic task.
5. Denominators: coding ≈ 16% of developer time; code generation 25–35%.
6. Bain: organizations report 10–15% gains, rarely monetized.
7. TestGen-LLM yields: 75% → 57% → 25% (class-level, cumulative).
8. FlakyGuard: 47.6% of *reproducible* tests fixed; 71.6% reproducible.
9. The four levels, applied to this deck.
10. Illustrative model: 3.3% capacity → 0.45% net cash per $10M.
11. What we cannot say: the not-verified list.
12. Decision ask.

## Step 1 — `research-log.md`

**Reference answer.** Six or more dated entries, newest first, each in the AI × QE format
(`ai_qe/docs/research-log.md`): Question / Checked / Outcome / Changed. At least two entries state
explicitly that a claim could not be verified. Worked exemplar (abbreviated):

| Date | Question | Outcome | Changed |
|---|---|---|---|
| 2026-09-12 | Does AI speed up maintenance work? | No — 19% longer, independent RCT | Slide 3 labelled measured, negative |
| 2026-09-12 | Is the Feb-2026 follow-up decisive? | No — both CIs cross zero | Recorded as inconclusive, no slide number |
| 2026-09-12 | Is 55.8% a capacity figure? | No — one synthetic task | Labelled task-level, vendor-affiliated |
| 2026-09-12 | Are Bain's 10–15% gains audited? | **Not verified** — self-reported only | Wording uses "report" |
| 2026-09-12 | Can we confirm a hard-dollar saving? | **Not verified** — no budget line | Slide 10 labelled illustrative |
| 2026-09-12 | Is TestGen-LLM a QA capacity number? | No — class-level generation yield | Labelled task-level, industrial |

**Commands.** Run against the student's file; counts vary, not the shape.

```bash
grep -cE '^#{2,3} ' research-log.md      # ≥ 6  — entry count
grep -ciE 'not verified|open question' research-log.md   # ≥ 2
```

**Common wrong answers.** (a) Six entries with no date — signals copying the template headings
without the intake habit. (b) All six outcomes positive — signals marketing, not a log.

**Grading note.** A real log contains an entry that changed the student's mind; a fake one only
records what was already on the slide.

## Step 2 — provenance table and claim routing

**Reference answer.** One row per claim: exact slide wording, source URL, retrieval date, claim type,
epistemic label, what it supports. Correct routing of the dataset:

| # | Claim | Level | Epistemic label |
|---|---|---|---|
| 1 | METR: 19% longer, CI +2% to +39% | 1 — task-level (negative) | Measured, independent RCT |
| 2 | METR follow-up: −18% and −4% | 1 — task-level (inconclusive) | Measured, CI crosses zero |
| 3 | Peng: 55.8% faster | 1 — task-level | Measured, vendor-affiliated |
| 4 | Cui: +26.1% completed tasks | Output metric — not level 1 or 2 | Measured, large-N |
| 5 | GitHub/Accenture: +8.7% pull requests | Output metric — not level 1 | Measured, vendor-published |
| 6 | Bain: 10–15% reported gains | 1 — task-level perception | Self-reported consultancy |
| 7 | Coding ≈ 16% of developer time | Denominator — caps level 4 | Survey-based |
| 8 | TestGen-LLM: 75/57/25 yields | 1 — task-level (testing) | Measured, industrial |
| 9 | FlakyGuard: 47.6% of reproducible | 1 — task-level (testing) | Measured, industrial |
| 10 | Banking model: 3.3% → 0.45% cash | 2 released capacity + 3 hard-dollar | **Illustrative** |

No row in this dataset is a *measured* level-3 or level-4 claim. That is the finding, not a gap.

**Common wrong answers.** (a) Bain routed to level 3 because "10–15%" sounds like money — fails; it
is a self-reported perception figure. (b) The illustrative 3.3% → 0.45% model routed to level 3
without the illustrative label — fails; the label goes on the slide, not the footnote. (c) "Coding is
16% of developer time" entered as a claim level — fails; it is denominator evidence.

**Grading note.** Check the two rows a student cannot fake: a negative or inconclusive record, and an
explicitly illustrative one.

## Step 3 — 12-slide outline and citations

**Reference answer.** Every quantitative slide cites at least one provenance row by number and
carries its epistemic label in the slide text — for example "Peng et al.: 55.8% faster (95
freelancers; one synthetic task; vendor-affiliated)."

**Common wrong answers.** (a) A number on slide 5 with no row — an orphan number that
`selfcheck.py` catches in step 6. (b) "Measured" applied to the Bain figure — the headline failure below.

## Step 4 — two routes over the same 12 slides

```yaml
executive:
  slides: [1, 3, 6, 9, 11, 12]           # 6 slides
  closing: 12                             # the decision ask
technical:
  slides: [1, 3, 4, 5, 7, 8, 10, 9, 11, 12]  # 10 slides
  closing: 12
full_order: [1,2,3,4,5,6,7,8,9,10,11,12]
```

Decision ask, quoted in the record: "Fund Phases 0 and 1 — a three-week baseline and one capped pilot
— not a transformation programme." The technical route retains slides 4, 5, 7, 8 and 10, all skipped
by the executive route — five evidence slides, above the required three.

**Common wrong answers.** (a) A seven-slide "executive" route — fails the exactly-six requirement.
(b) The ask reads "transform QA" — fails the decidable-ask rule from
`ai_qe/docs/economics/slide-language.md`.

## Step 5 — edition decision record

**Reference answer.** A record naming what changes and what is deliberately retained, with the
editions split as `ai_qe/_data/release.yml` splits them. Exemplar: slide 3 gains the Feb-2026
follow-up; `slide_edition` advances 1.0 → 1.1 and `version` with it; the questionnaire edition stays
at 4; audio, subtitle timing and the existing PDF edition remain unchanged. Published editions are
never overwritten (`ai_qe/CONTRIBUTING.md`).

**Common wrong answers.** (a) Bumping every edition together — signals version theatre.
(b) Republishing over the old release — editions are immutable.

## Step 6 — the reconciliation gate

**Reference answer.** The briefing as one Markdown file, `selfcheck.py` run against it, exit
status 0, and the command, its last line and the path used recorded.

**Commands and exact output.** The script checks itself first — verbatim:

```text
$ python3 selfcheck.py --selftest
[PASS] good.md: 0 uncited claim(s), expected 0
[PASS] bad.md: flagged lines [13, 14, 22, 27, 30, 32], expected [13, 14, 22, 27, 30, 32]
    line 13: 55.8%, 71.2, 160.9 minutes, 2026-09-04
    line 14: 47.6%, 2026-09-04
    line 22: 55.8%
    line 27: 10, 15%
    line 30: $450k
    line 32: 3.3x
Full report: selfcheck.py selfcheck-examples/bad.md

SELFTEST: PASS
```

On the briefing itself a clean file prints `PASS: 0 uncited quantitative claims in 1 file(s)`;
anything else exits 1 and names the unit, not just the number.

**Common wrong answers.** (a) A source cell holding `ai_qe/docs/evidence/benchmarks.md` with no
line anchor: that names a file, not a record, and the script flags it — `bad.md` line 13. (b)
Deleting the number instead of citing it: green gate, lost claim.
(c) Rewording until the pattern stops matching; the check over-flags on purpose.

**Grading note.** A real pass pastes the command, the file name and the exit status; a fake pastes
a bare `PASS`, or output naming another file.

## The mixed-level claim, and the honest replacement

Raw: "AI cuts testing time 55.8%, so we can take $450k out of the QA budget."

Honest replacement, in one sentence: "One vendor-affiliated study measured a 55.8% speedup on a
single synthetic task; our own pilot will measure net QA effort on our data, and any capacity it
releases becomes a saving only when Finance names the budget line it is captured against."

The raw claim commits three errors: a task-level number sold as capacity, capacity sold as cash, and a
fictitious dollar figure. The replacement keeps the strongest number and drops the rest.

## Common student failures

1. **A vendor self-reported figure headlined as measured.** "Organizations achieve 10–15% gains"
   labelled *measured*; the fix is the verb, "organizations *report*".
2. **A task-level number sold as a budget saving.** 55.8% presented as a Finance outcome with no
   named budget line.
3. **A citation with a link but no date, sample, method or unit.** A bare URL is not a benchmark
   record (`ai_qe/CONTRIBUTING.md:93-94`). The fix is the full record, or a not-verified entry.
4. **Routes that rewrite rather than reorder.** A reworded "executive route" breaks the stable-ID
   invariant and every shared link with it.

## Self-check table

| Criterion | Self-verification |
|---|---|
| ≥6 dated log entries, ≥2 not-verified | `grep -cE '^#{2,3} ' research-log.md`; read the outcomes |
| No orphan numbers | Walk slides 1–12; each quantitative slide names a row number |
| Every row has URL + date + level | Read the table's last three columns top to bottom |
| Executive route is exactly 6, decision ask quoted | Count the YAML list; paste the ask |
| Technical route keeps ≥3 skipped evidence slides | Diff the two `slides:` lists |
| No uncited quantitative claim | `python3 selfcheck.py briefing.md` → exit 0; cohort path adds the named reviewer's written confirmation |
