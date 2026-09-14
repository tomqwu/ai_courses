# Facilitation Kit — M6 (The Expertise Product)

> One 90-minute live session, Week 6 of the cohort cadence (`02-instructor/instructor-guide.md`).
> Pre-work: M6 lessons watched, Lab M5 submitted. Formula: **I do / We do / You do ≈ 25 / 35 / 30**.
> Everything students produce here seeds Lab M6; nothing here is graded on its own.

## Timing table

| Min | Activity | Mode | Artifacts on screen |
|---|---|---|---|
| 2 | Opening hook — the vendor deck vs. the published negative result | I do | `ai_qe/docs/evidence/benchmarks.md` |
| 5 | Case walk: benchmark records and the seven required fields | I do | `ai_qe/CONTRIBUTING.md`, METR record |
| 9 | Label eight dataset claims with one of the four levels | We do | `evidence-dataset.md`, `ai_qe/docs/principles.md` |
| 8 | Build one research-log entry and one provenance row live | We do | `ai_qe/docs/research-log.md` |
| 8 | Pairs draft one honest "not verified" entry | You do | Student's own topic |
| 3 | Debrief: what did the not-verified line prove? | We do | Pair outputs |
| 5 | Case walk: 116 slides → 4 decks, routes over stable IDs | I do | `ai_qe/_data/briefing_room.json`, `briefing_routes.json` |
| 10 | Route the same 6 slides two ways; sharpen the decision ask | We do | `ai_qe/docs/economics/slide-language.md` |
| 12 | **Breakout:** provenance row + two routes + decision ask | You do | Breakout worksheet |
| 6 | Breakout report-out; one decision ask read aloud per group | We do | Group posts |
| 6 | Case walk: editions, `make check`, narration hash gate | I do | `ai_qe/_data/release.yml`, `ai_qe/Makefile` |
| 8 | Write an edition decision record for a one-slide v2 change | You do | Student's draft |
| 3 | Quiz M6 launch and lab handoff | We do | `quiz.md`, `lab.md` |
| 5 | Close — what carries into Lab M6 | I do | Lab checklist |

## Opening hook (2 min)

"Two decks cross your desk. The first promises thirty to fifty percent productivity gains and quotes a
vendor benchmark you cannot open. The second tells you its only independent randomized controlled
trial found developers were nineteen percent *slower*, and then tells you the McKinsey PDF it wanted
to cite timed out. Which one gets the meeting? The second one, because you can check it. In the next
ninety minutes you will build that second kind of artifact — not the argument, the evidence
structure."

## Close (5 min)

"Three things travel with you. One: a claim without a date, a sample, a method and a unit is not
evidence — it is an advertisement with a link. Two: the four levels are a routing rule, not a ranking;
the executive route ends on a decision because *fund Phases 0 and 1* is decidable and *transform QA* is
not. Three: content under edition discipline is content a client can hold. Lab M6 takes what you built
today — one log entry, one provenance row, two routes — and scales it to twelve slides. Post your
decision ask in the lab thread today, before you write the deck."

## Breakout instructions

- **Groups of 3.** Roles rotate inside the group: **Claim owner** (picks one quantitative claim and
  states its level), **Skeptic** (hunts the missing date, sample, method or unit and writes the
  not-verified line), **Router** (writes both route declarations and the decision ask).
- **Time:** 12 minutes, then 6 for report-out.
- **One deliverable posted to the thread** (paste-ready, three parts):

```text
Claim: "<exact slide wording>" — Level: <1–4 or illustrative>
Provenance row: | # | Claim | URL | Retrieved | Level | Label | Supports |
Decision ask: "<one sentence starting with 'Fund ...'>"
```

- **Exact prompt to read aloud:** "Pick one claim you would actually put on a slide. Name the level it
  belongs to and the level your current materials sell it as. Write the provenance row with a real
  retrieval date. Then write two routes over the same six slides: one that reaches your decision ask
  in six slides, and one that keeps the evidence the executive route drops. Post all three parts.
  If you cannot fill the row, post the not-verified line instead — that counts."

## Discussion prompts

1. **"Does the honest wording weaken the pitch, or sharpen the ask?"**
   *Follow-up probe:* "Read your ask aloud as if you were the CFO. What can you fund tomorrow?"
   *Strong answer:* naming that "fund Phases 0 and 1" is decidable while "transform QA" defers the
   decision, and citing the executive message in `ai_qe/docs/economics/slide-language.md`.
2. **"Which of the four levels can you prove today, and which needs Finance?"**
   *Follow-up probe:* "Who signs the budget line, and what evidence will they accept?"
   *Strong answer:* task-level needs a pilot; capacity needs baseline capture; hard-dollar needs a
   named budget line owned by Finance — the "who can confirm it" column in `ai_qe/docs/principles.md`.
3. **"What made you delete a number?"**
   *Follow-up probe:* "What did you replace it with — a lower claim, or a not-verified entry?"
   *Strong answer:* a specific record (self-reported consultancy figure, vendor-affiliated single-task
   study) and the replacement wording, not a general commitment to honesty.
4. **"Your slide changes but the narration does not. What breaks?"** *(stretch)*
   *Follow-up probe:* "What does the hash gate force you to write down?"
   *Strong answer:* voice-slide desynchronisation, and a deliberate `retained` or `refreshed` decision
   with a reason, per `ai_qe/tools/narration-review.cjs` and `ai_qe/CONTRIBUTING.md`.

## Watch-fors

| Stuck point | Symptom | 30-second intervention |
|---|---|---|
| "My topic has no data" | Empty provenance table | "Use the provided AI-testing dataset in `evidence-dataset.md`, or your work domain. Rule: no row, no claim — write a not-verified line instead." |
| Self-reported sold as measured | Bain's 10–15% labelled *measured* | "Read `ai_qe/docs/evidence/benchmarks.md` at the Bain entry. Change the verb to *report* and the label to *self-reported*." |
| Task number sold as cash | 55.8% next to a dollar figure | "`ai_qe/docs/economics/slide-language.md`, Avoid list: no dollar savings before Finance names the capture mechanism." |
| Route that rewrites | Executive route paraphrases slides | "Routes reorder and omit, never rewrite — `ai_qe/_data/briefing_routes.json`. Keep the slide ID stable and cut the words." |
| A crossing interval treated as a near-miss | "12% but the CI reaches 17%, so go" | "`ai_qe/docs/method/phased-pilot.md`: a CI crossing 10% or 15% is insufficient evidence for that boundary." |

## Post-session checklist

- **Record as evidence:** attendance and group membership; each group's posted three-part deliverable;
  the decision asks read aloud; the list of numbers students deleted during the session; the
  item-analysis flag if more than 30% miss one Quiz M6 question (re-teach that objective in next
  week's We-do).
- **Post to the community:** the three sharpest decision asks, one anonymised before/after replacement
  wording from the discussion, and a pinned note that Lab M6's reconciliation check is the pass
  gate — every quantitative slide maps to a provenance row. Reply within 24 hours to every pair that
  posted a not-verified line; that behaviour is the module's whole point.
