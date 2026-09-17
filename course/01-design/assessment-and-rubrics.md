# Assessment Design & Rubrics: AI Product Studio (APS-3)

> Assessment philosophy: **criterion-referenced checkpoints** — every graded element ends in a verifiable artifact, never in "watched the video." This mirrors the source repos' own acceptance style (Given/When/Then, evidence records, honest manifests).

## Grade weights

| Component | Weight | Format |
|---|---|---|
| Module labs (M0–M7) | 60% | Pass/fail checkpoints, 8 labs, self-verified with evidence; instructor-verified in cohort tier |
| Module quizzes | 20% | 8 auto-gradable questions each (72 total across the nine modules M0–M8), answer keys in each quiz file |
| Capstone (M8) | 20% | 5-dimension rubric below, ≥80% to pass, demo required |

Certificate of completion (cohort/self-paced with evidence): all 8 labs passed + quizzes ≥75% average + capstone ≥80%.

## Quiz design rules (used by every quiz file)

1. 8 questions per module: 6 multiple choice (4 options, exactly one correct), 2 short-answer (one-paragraph, graded against a model answer).
2. Each question maps to exactly one lesson segment (M#.#) learning objective; the mapping is printed with the answer key.
3. Multiple-choice distractors encode the *plausible misconceptions* taught against in the lesson (e.g., "localhost is proof of local-only" — false; "adding an API key switches modes" — false).
4. Short answers ask for *applications*, not recall ("Write the Given/When/Then for one acceptance scenario of X").
5. Answer key format: correct option letter, one-sentence rationale, objective reference.

## Lab acceptance-checklist standard (every lab file)

Each lab defines:
- **Goal** — one sentence.
- **Prerequisites** — modules/labs that must be complete.
- **Time estimate** — honest range.
- **Steps** — imperative, numbered, runnable.
- **Acceptance checklist** — 5–10 binary items ("`make lab-m2` exits 0", "Table has ≥5 rows with source URLs").
- **Evidence to record** — what the student keeps (command output, screenshots, files) and the evidence-log entry format.
- **Stretch goals** — optional depth.
- **Discussion prompt** — the community post that closes the lab (the +14-point completion lever).

## Capstone rubric (M8)

Scored 0–5 per dimension (3 = meets; weighted equally; pass = total ≥80% and no dimension below 3):

| # | Dimension | 3 ("meets") looks like | 5 ("exceptional") looks like |
|---|---|---|---|
| 1 | **Spec quality** | Complete spec-kit artifacts for the shipped scope; stories independently testable; acceptance criteria concrete | Artifacts so complete that a fresh agent session implemented a story without conversation context; checklist gate passed on first review |
| 2 | **Build discipline** | TDD evidence (failing test first); small reviewable commits; core separated from glue via protocols/seams | Coverage floor enforced; red-team/negative-path tests included; a real-provider contract test outside CI |
| 3 | **Evidence honesty** | Validation record with commands, counts, date, limitations; failures included, not hidden | Gap-style self-review identifying known limitations with priorities; "not verified" list present |
| 4 | **Privacy/safety engineering** (Type 1/2) or **claim discipline** (Type 3) | Local-only/fail-closed mode OR tenant isolation OR provenance table implemented and tested | Multiple defenses layered (metadata verification + redirect rejection + truthful labels) with tests for each; or full four-level claim labeling with reconciled provenance |
| 5 | **Launch-readiness** | Positioning one-liner, pricing rationale with sourced comparators, sales page draft, 5-email arc | Sales page ready to publish; email arc personalized with student's own proof assets; demo delivered (recorded or live) |

### Capstone evidence record (required attachment)

Modeled on SignUpFlow's validation format:

```markdown
## Capstone evidence — <project> — <date>
Commands run (with results):
- <command> → <pass/fail counts>
- ...
Artifact links:
- Repo: <url> (tag <version>)
- Spec folder: <path>
- Evidence log: <path>
- Sales page draft: <path>
Limitations / not verified:
- <honest list>
```

## Academic honesty (mirrors the repos' ethos)

- Students may use AI agents for any lab/capstone — **the course teaches that** — but the evidence record must state what the agent did and what the student verified ("I implemented X via agent; I reviewed Y; tests were run locally with results below"). Fabricating a test result or an evidence line is the only fail.
- Peer review exchange (self-paced) requires reviewing one other student's M6 briefing or M7 pricing worksheet against the printed checklists; the review template is in the instructor guide.

## Cohort-specific assessment mechanics

- Weekly: quiz due before workshop; lab checkpoint reviewed in the "You do" segment.
- Week 5: mid-course portfolio review (labs M1–M4 evidence posted).
- Week 8: demo day — 5-minute capstone demos, peer rubric scoring (instructor final), testimonial collection (beta-cohort agreement signed at enrollment: feedback in exchange for the discount).