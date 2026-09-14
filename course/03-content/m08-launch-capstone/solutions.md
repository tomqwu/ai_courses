# Solutions — M8 Capstone (Instructor Grading Exemplar)

> M8 is a capstone, not a lab with one correct answer. This file is the grading exemplar: what a strong
> submission contains artifact by artifact, the five-dimension rubric applied to two contrasting
> submissions, and the auto-fail conditions. Score against `01-design/assessment-and-rubrics.md` and the
> restated table in `03-content/m08-launch-capstone/lab.md`. The student's evidence record is the
> primary graded artifact; the demo is the oral defense.

## 1. A strong submission, artifact by artifact

Exemplar shape: **Type 1 — on-device app**, one feature added to TinyCopilot, all six loop stages
(`00-research/00-synthesis.md`). Counts in *italics* are the verified lab figures in
`01-design/content-standards.md` §0.2 — the command is unchanged, so the number is checkable. Every
number a student adds must carry its own observed run.

| # | Artifact | What a complete submission contains | Reference point |
|---|---|---|---|
| 0 | Plan post | Archetype, one-sentence scope, each stage mapped to a named file/tag/URL, first-pass self-score naming the weakest dimension | `03-content/m08-launch-capstone/lab.md` step 1 |
| 1 | Spec | ≥2 independently testable stories, Given/When/Then criteria, explicit non-goals, checklist gate run | Spec 014 shows the shape: `SignUpFlow/specs/014-security-hardening/spec.md` |
| 2 | TDD evidence | The failing-test-first commit visible as its own commit in `git log`, not squashed into the fix | `03-content/m08-launch-capstone/lab.md` step 3 |
| 3 | Validation record | Commands, counts, date, environment, limitations; the red run kept beside the green | `make lab-m2` → *191 passed, 100% coverage (floor 90)*; `make lab-m3` → *49 passed* |
| 4 | Release | Pushed version tag or deployed URL, opened in a clean browser and confirmed identical to the tested artifact | `03-content/m08-launch-capstone/lab.md` step 5 |
| 5 | Discipline artifact | Local-only mode fail-closed **plus** the cloud-alias red-team case as a test | `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift` |
| 6 | Sales page | Eight sections in the M8.1 order, one CTA, word target set by the M7 price, every claim tagged | `04-sales/landing-page.md` (~1,900 words of copy, measured by `06-production/verify.py`) |
| 7 | 5-email arc | Cart open, objections, proof, final call, survey; one CTA each; deadline real | `04-sales/launch-plan.md` |
| 8 | Demo | ≤5:30, four beats, ends on the not-verified list | `03-content/m08-launch-capstone/lab.md` step 7 |

Type 2 substitutes tenant-isolation negative-path tests plus a validating playbook manifest
(`SignUpFlow/docs/TESTING.md`); Type 3 substitutes a reconciled provenance table where every slide
claim has a row (`ai_qe/docs/principles.md`).

**A strong evidence record (excerpt shape, Type 1):**

```markdown
## Capstone evidence — TinyCopilot local-only v1 — 2026-xx-xx
Commands run (with results):
- make lab-m2 → 191 passed, coverage 100% (floor 90), 2026-xx-xx
- make lab-m3 → 49 passed
- make e2e → 2 passed (live Ollama daemon); 2 contract tests skipped
  without LAB_E2E=1
Artifact links:
- Repo: <public url> (tag v0.1.0)
- Spec folder: <path>
Limitations / not verified:
- Cloud-alias red-team covers aliases observed on this daemon only; no
  other provider families tested. UI not exercised end-to-end.
```

## 2. The rubric applied to two contrasting submissions

Scores are 0–5 per dimension, equal weights; pass = ≥80% total and nothing below 3.

**Submission A — pass (88%: 5/5/4/4/4).** Type 1, small scope, loop complete.

| # | Score | Why |
|---|---|---|
| 1 | 5 | A fresh agent session implemented one story from the spec folder with no conversation context |
| 2 | 5 | Red-then-green visible in history; coverage floor enforced; red-team test included |
| 3 | 4 | Commands, counts, date, environment, limitations all present; no gap-style prioritized self-review |
| 4 | 4 | Local-only mode fail-closed and tested; one defense layered, not several |
| 5 | 4 | Positioning line, sourced pricing rationale, eight-section page, five-email arc, demo delivered |

**Submission B — fail (52%: 3/2/2/3/3).** Sprawling scope, half the loop.

| # | Score | Why |
|---|---|---|
| 1 | 3 | Spec exists but stories share one acceptance criterion; one story is not independently testable |
| 2 | 2 | Tests were written after the code; history shows a single "implement + tests" commit — no red run |
| 3 | 2 | Evidence line reads "all tests pass"; no counts, no date, no limitations block |
| 4 | 3 | Provenance table present and reconciles, but three claims have no row |
| 5 | 3 | Positioning and rationale present; page is five sections; arc never reaches a deadline statement |

Both students used agents; both records say so. A fails on **build discipline and evidence honesty**,
which are the two dimensions a fabricated or post-hoc record cannot fake. B's failure is not the
product's quality — it is that the loop is not evidenced end to end.

## 3. Auto-fail conditions

Fail regardless of the other rows:

1. **Fabricated evidence** — a command, count, date, or output that did not run, or a testimonial the student wrote.
2. **A green run with no red run recorded** — no failing-test-first commit and no captured failure anywhere in the history.
3. **A demo that never ran** — no recording, no live delivery, or a video showing slides only.
4. **Tests weakened to pass** — assertions deleted or skipped to reach green; check the diff, not the badge.
5. **An unsourced number on the sales page** — a market statistic, coverage figure, or user count with no file behind it.
6. **The agent did the record** — the evidence record does not state what the student personally verified.

## 4. Common wrong answers, by artifact

- **Spec:** a topic outline ("feature X") instead of testable stories; implementation detail leaking into the spec file (code belongs in plan/contracts). Signals the M4 checklist gate was skipped.
- **Build:** one commit containing implementation and tests, described as TDD. Signals the student knows the vocabulary but not the sequence.
- **Validation:** "191 passed" with no date, environment, or skipped count. Signals copy-paste from the lab rather than the student's own run — which is why the count alone is never accepted.
- **Sales page:** a topic list for section 4; two different CTAs; a drafted testimonial. Signals the student read the anatomy but not the honesty rules.
- **Arc:** all five emails sell. Signals the warmup/conversion split was not internalized.

## 5. Self-check table (send to students with the rubric)

| Criterion | Self-verification |
|---|---|
| Failing test first | `git log --stat` shows a commit that adds only a failing test |
| Red and green both recorded | Both outputs are in the evidence log, with dates |
| Link works clean | Open the tag or URL in a private window |
| No unsourced claim | Every number on the page maps to a file pointer |
| Deadline real | State what changes when it passes, and hold it |
| Discipline artifact runs | The archetype test suite passes on its own |
| Limits listed | The not-verified list has ≥2 honest items |
