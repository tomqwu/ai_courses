---
marp: true
theme: aps
paginate: true
title: M6 — The Expertise Product: Evidence, Routing, Editions
---

<!-- _class: lead -->

## M6 — The Expertise Product: Evidence, Routing, Editions

- **Promise:** turn expertise into a defensible, sellable content product
- **Duration:** ~75 minutes, plus a ~2.5-hour lab
- **Prerequisites:** Modules 1–5
- **Case study:** AI × QE — `ai_qe/README.md`

<!-- NOTES: Welcome to Module 6, the third archetype. Modules 2 and 3 shipped an on-device app; Modules 4 and 5 specced and hardened a SaaS. This module packages expertise itself. Your case study is AI × QE, a research-backed presentation site about modernizing quality engineering in regulated financial services. Its topic is banking QA; its discipline transfers to any field. The promise is narrow and testable: you will learn to publish claims a skeptic can audit. Timing: 1 minute. Transition: next, the four capabilities you leave with. -->

---

## By the end you can…

- Label every number with one of four saving levels
- Keep a dated research log a skeptic can audit
- Hash every retrieval in a provenance manifest
- Re-cut one slide set into two routes
- Run content under edition discipline
- Design a pilot that sells measurement

<!-- NOTES: These six outcomes are the quiz blueprint and the lab checklist, so treat them as this module's contract. Notice the verbs: label, keep, hash, re-cut, run, design. Every one produces an artifact someone else can check. That is the same standard the case-study repos hold themselves to: if it cannot be observed, it does not count. The lab turns all six into one deliverable — a twelve-slide mini-briefing with a provenance table and two audience routes. Timing: 2 minutes. Transition: segment one, where credibility itself becomes the product. -->

---

## M6.1 — Credibility is the product

- One expert's research base becomes a product
- The citation is the evidence, not decoration
- Failures and unknowns are published, not hidden
- The signature qualifier does real commercial work
- Publish your own audit and convert skeptics

<!-- NOTES: Segment M6.1 has one argument: in this archetype, trust is the product, and trust is engineered like software. AI × QE looks like a content site — four narrated decks, a fintech case study, research pages, downloadable PDFs. Underneath, every number carries a citation, a date, a sample, a method and an epistemic label, and the site publishes the things it could not verify. We will take that apart file by file over the next twenty-five minutes. Timing: 3 minutes. Transition: start with the rule that sounds obvious and is almost never followed. -->

---

## The citation is the evidence

- Benchmark record: date, sample, method, unit
- Plus: self-reported vs measured, sponsor, supported claim
- "The citation is the evidence; no vendor is endorsed"
- Anything unverifiable is listed as unverifiable
- No client or partner names — "the bank", "the sponsor"

<!-- NOTES: Open `ai_qe/CONTRIBUTING.md` at the section titled Research conventions and read the rule aloud. It says research sources are cited by name because the citation is the evidence, and that no vendor is endorsed. Then it lists the required fields: date, sample, method, unit, self-reported versus measured, sponsor, and what claim the record can support. That last field is the one people skip. A number without a stated limit is not evidence; it is an advertisement. Timing: 5 minutes. Transition: look at two real records that make the difference visible. -->

---

<!-- _class: proof -->

## Benchmark records, side by side

- `ai_qe/CONTRIBUTING.md` — "Research conventions"
- `ai_qe/docs/evidence/benchmarks.md` — METR and Peng records
- METR: 19% longer (CI +2% to +39%), 246 issues
- Peng: 55.8% faster, 95 freelancers, one synthetic task
- Both measured — one independent, one vendor-affiliated

<!-- NOTES: Read one record end to end. The METR entry says AI-allowed issues took nineteen percent longer, with a confidence interval of plus two to plus thirty-nine percent; developers expected twenty-four percent faster and afterwards believed twenty percent faster. Supports: task efficiency, negative. Caveats: sixteen experienced maintainers on repositories they know well, two hundred forty-six real issues, measured by screen recording, independent non-profit. Two entries down, Peng: fifty-five point eight percent faster, ninety-five freelancers, one synthetic task, vendor-affiliated. Both are real. The record structure refuses to average them. Timing: 5 minutes. Transition: research gets logged before it reaches a slide. -->

---

## Log before you publish

- Newest first: Question / Checked / Outcome / Changed
- Add an entry before editing a topic page
- Publish a "Not verified" list, openly
- The only independent RCT is negative — say so
- Research you cannot verify goes on the list

<!-- NOTES: `ai_qe/docs/research-log.md` is the intake queue. Its own instruction is that new research goes in first as a dated entry, then into the topic page. Entries are structured Question, Checked, Outcome, Changed. In the initial evidence base entry, the outcome states that the only independent randomized controlled trial is negative — and the part most sites would delete, an explicit Not verified list: World Quality Report cost-of-quality share, any Gartner AI-testing productivity figure, Snyk accuracy claims. That list is what makes the other four entries believable. Timing: 5 minutes. Transition: three files exist only to record where content came from. -->

---

<!-- _class: proof -->

## Provenance manifests

- `ai_qe/research/document-manifest.json` — 11 retrievals, hashed
- M02 McKinsey PDF: `"status": "unavailable"`
- Reason recorded: "The read operation timed out"
- A logged failure proves the manifest is real
- `ai_qe/research/visual-provenance.md` — even images have provenance

<!-- NOTES: Open the manifest and find entry M02. Eleven retrievals are listed, each with a URL, a retrieval date, a status and a SHA-256 hash for the downloaded file. M02 is the McKinsey PDF, and its status is unavailable, with the reason recorded verbatim: the read operation timed out. A spotless manifest is suspicious. A manifest that logs its own failure is checkable, because you can re-run the retrieval. Then open visual-provenance dot md: the two hero illustrations are conceptual editorial illustrations, not photographs of deployed systems, and the prompts are recorded. Timing: 4 minutes. Transition: now label the level of every number. -->

---

## Four levels of "saving"

| Level | Definition | Who can confirm it |
|---|---|---|
| Task-level efficiency | Net time reduction for one activity, after review and correction | Pilot measurement |
| QA capacity released | Human hours freed across the workflow, after adoption | Pilot plus baseline capture |
| Hard-dollar saving | Budgeted cost Finance can actually remove or avoid | Finance, named budget line |
| Total software-spend impact | Broader engineering cost — never mislabelled as QA saving | Finance and the CIO office |

<!-- NOTES: This table is quoted from `ai_qe/docs/principles.md`, and the whole site runs on it. Every number on the site is labelled with one of these four levels, and the file says plainly that mixing them is the most common error in AI business cases. Read the third column carefully, because it is the part people ignore: each level names who can confirm it. Task-level claims need a pilot. Capacity claims need baseline time capture. Hard-dollar claims need Finance, against a named budget line. Not you. Not a vendor deck. Timing: 5 minutes. Transition: watch the mixing error happen. -->

---

## The mixing error

- 55.8% task-level speedup is not 55.8% capacity
- Coding ≈ 16% of developer time
- Code generation ≈ 25–35% of idea-to-launch
- A 50% task gain dilutes to single digits
- Pointer: `ai_qe/docs/evidence/reading-the-evidence.md`

<!-- NOTES: Take Peng's measured fifty-five point eight percent and try to sell it as a budget number. Coding is roughly sixteen percent of developer time, and code generation is twenty-five to thirty-five percent of idea-to-launch, according to the survey sources recorded in the reading-the-evidence page. So a fifty percent task gain dilutes to single digits of total engineering time before any redeployment or headcount decision. The file states that dilution. The same paragraph notes that the nineteen percent, the ten to fifteen percent and the roughly two-times figures are perception or per-task numbers. Timing: 4 minutes. Transition: publish your own audit. -->

---

## Publish your own audit

- `ai_qe/research/reviews/site-audit-2026-09-06.md`
- 14 findings: four high, nine medium, one lower
- R01 is the site's own conflicting base-case economics
- Remediation maps finding → response → verification
- Refusals stay published too
- Skeptics stop asking "should I believe you?"

<!-- NOTES: `ai_qe/research/reviews/site-audit-2026-09-06.md` is a review the site publishes about itself. Fourteen findings: four high priority, nine medium, one lower. Finding R01 is a content inconsistency between two different base-case economics — the site caught its own numbers disagreeing. The companion remediation file is a three-column table: finding, implemented response, verification. A later resolution record even lists deliberate non-changes: do not hide weak economics, convert capacity to cash, or relabel unknown results as observed. Findings, responses and refusals all stay published. Timing: 5 minutes. Transition: segment two, one research base for many audiences. -->

---

## M6.2 — One research base, many audiences

- 116 slides, one research base
- Two axes: audience × scenario
- Four decks, nothing forked
- Routes reorder and omit; they never rewrite
- The deck serves a conversation, not itself
- Qualify leads with one role-routed form

<!-- NOTES: Segment M6.2 is about distribution without duplication. The site has one hundred sixteen narrated slides and serves them as four decks along two axes: executive or technical, banking scenario or industry perspective. An executive gets the strategic cut; a technical lead gets contracts, sequencing and evidence schemas. Both trace back to the same source records. Nothing is forked, so a correction lands once and appears everywhere. Then we will look at how the same body of work qualifies leads through a single questionnaire. Timing: 3 minutes. Transition: here is the actual cut. -->

---

## 116 slides, four decks

| Deck | Slides | Duration |
|---|---|---|
| Banking scenario · Executive | 21 | 25–30 min |
| Banking scenario · Technical | 33 | 35–45 min |
| Industry perspective · Executive | 26 | 30–40 min |
| Industry perspective · Technical | 36 | 45–60 min |

- Pointer: `ai_qe/_data/briefing_room.json`
- The four decks total 116 narrated slides

<!-- NOTES: This is the arithmetic that shows nothing is forked: twenty-one plus thirty-three plus twenty-six plus thirty-six equals one hundred sixteen. Open `_data/briefing_room.json` and you see each deck declared as data — audience, series, cover, URL, PDF prefix, edition, slide count, duration and a full outline keyed by stable slide number. Because the outlines live in data rather than in four hand-maintained documents, the counts stay honest and the routes can be generated. Timing: 4 minutes. Transition: routes are the second layer. -->

---

<!-- _class: proof -->

## Routes over stable slide IDs

`ai_qe/_data/briefing_routes.json`

```yaml
evp:
  slides: [1, 3, 19, 20, 6, 21, 18, 17, 13, 14, 15, 16, 10, 12]
  closing: 12
```

- 14 of 21 slides; `full_order` retains all
- Routes reorder and omit — never rewrite
- Stable IDs keep every link resolving

<!-- NOTES: `_data/briefing_routes.json` declares curated sequences over the same stable slide IDs. The banking executive route plays fourteen of the twenty-one slides and declares closing twelve — the brainstorm-questions slide — as its endpoint. The full order retains everything. Read the README's rule: focused routes end on a decision discussion; full decks retain the supporting material. The invariant is the slide ID. A route reorders and omits; it never rewrites, so a shared route link still resolves to the same slide next quarter. Timing: 4 minutes. Transition: the deck exists to run a meeting. -->

---

## Script the meeting, not the deck

- 01 / Align · 5 min — where work repeats
- 02 / Explore · 15 min — follow one workflow
- 03 / Agree · 10 min — process, owner, evidence
- `ai_qe/briefings/index.md`
- The deck is not the product

<!-- NOTES: `ai_qe/briefings/index.md` embeds a suggested thirty-minute conversation. Align for five minutes: which part of QA creates the most delay or repeated work? Explore for fifteen: follow one workflow and show the platform services behind it. Agree for ten: choose the process, the owner and the evidence needed for a first pilot, landing on the discovery guide. Notice what that structure does. It spends half the meeting on the buyer's problem and closes on a decision, not on a feature list. Timing: 4 minutes. Transition: make the ask decidable. -->

---

## Sell the decision, not the transformation

- Use: "working hypothesis, tested on the bank's data"
- Use: "capacity is not a saving until Finance confirms"
- Avoid: "industry benchmarks show 30-50% gains"
- Avoid: "ROI of X%" before a pilot measures
- Decision: fund Phases 0 and 1, not transform
- Pointer: `ai_qe/docs/economics/slide-language.md`

<!-- NOTES: `ai_qe/docs/economics/slide-language.md` gives exact wording rules. Its Use list includes "working hypothesis, to be tested on the bank's own data" and "capacity released is not a saving until Finance confirms how it is captured." Its Avoid list includes "industry benchmarks show 30 to 50 percent productivity gains," "ROI of X percent before a pilot has measured anything," and any squad-level headcount arithmetic. The executive message ends with the line to remember: the decision today is whether to fund the first two phases, not whether to transform QA. A bounded ask is decidable. Timing: 4 minutes. Transition: the funnel starts with one form. -->

---

## The questionnaire is lead qualification

- One form, role-routed at the first question
- Executive sponsor, Finance, procurement: Sections 1, 5B, 6
- Engineering, delivery, QE, platform: 2, 3, 4, 5A, 6
- Single-select on the questions that define success
- Ranges mutually exclusive and gap-free
- An "unknown" option so a guess is not data

<!-- NOTES: `ai_qe/docs/method/discovery-questionnaire.md` is not a survey; it is the funnel's filter. The design rules are explicit: one form, role-routed at the first question; respondents complete the sections they own and leave unknowns blank. The executive sponsor, Finance and procurement answer Sections 1, 5B and 6. Engineering, delivery, QE and platform leaders answer Sections 2, 3, 4, 5A and 6. Priority questions — what success means, the autonomy ceiling, the go/no-go threshold — are single-select, because a nuanced multi-select produced no signal. Timing: 5 minutes. Transition: read the post-mortem. -->

---

<!-- _class: proof -->

## The failed form, dissected

- `ai_qe/docs/method/discovery-questionnaire.md`
- Failed form: 29 questions, 186 checkbox options
- Took 20-30 minutes, not 15
- No single respondent could answer all six sections
- Largest omission: the financial-capture set
- v4: 36 questions, role-routed, timing-checked

<!-- NOTES: The same file dissects the predecessor. A well-built twenty-nine-question form with one hundred eighty-six checkbox options across nineteen multi-select questions takes a knowledgeable respondent twenty to thirty minutes, not fifteen, because every option must be read before a selection limit applies. And no single respondent can answer all six sections — an executive cannot answer flaky-test questions; a QE director cannot answer Finance-recognition questions. The largest omission was the financial-capture set. Without it, the same four percent capacity result can be booked as a saving, as cost avoidance, or as nothing. Timing: 5 minutes. Transition: segment three, content as code. -->

---

## M6.3 — Content as code

- Public content changes require a new edition
- Site version and content editions are separate
- Published editions are never overwritten
- Changelogs record what is deliberately retained
- Tests gate content like code
- The pilot sells measurement, not outcomes

<!-- NOTES: Segment M6.3 applies software release discipline to content. Two ideas carry it. First, editions: the site version and the content editions move independently, so a player fix does not invalidate a client's PDF. Second, tests: content changes must pass a build, and a slide that overflows a projector viewport fails like a unit test. Then we take the same discipline to the commercial end of the funnel, where the product is a phased pilot that measures rather than promises. Timing: 3 minutes. Transition: look at how editions are separated. -->

---

## Editions: site vs content

`ai_qe/_data/release.yml`

```yaml
version: "1.24.1"          # site + player
slide_edition: "1.24.0"
fintech_edition: "1.24.0"
questionnaire_edition: "4"
research_edition: "1.7.0"
```

- A player-only patch advanced `version` alone
- `slide_edition` stayed at 1.24.0, deliberately
- "Public content changes require a new edition"

<!-- NOTES: `_data/release.yml` keeps five separate fields, and the separation is the point. The version identifies the site and the player. The slide, fintech, questionnaire and research editions move on their own schedules. The README states the rule: public content changes require a new edition before deployment. `CONTRIBUTING.md` is harder — content changes without a new edition are rejected on main before deployment. Why two numbers? Because a client holding a version 1.24.0 PDF needs to know exactly what they have. Timing: 4 minutes. Transition: the changelog proves the retention was deliberate. -->

---

<!-- _class: proof -->

## Changelogs record what is retained

- `ai_qe/releases.md` — v1.24.1 responsive subtitles
- The v1.24.0 PDF editions remain unchanged
- `ai_qe/CONTRIBUTING.md`: editions are "never overwritten"
- `tools/prepare_release.py` assembles and checksums assets
- `tools/publish_release.py` verifies SHA-256 before publishing

<!-- NOTES: Open `ai_qe/releases.md` at the 1.24.1 entry. It says subtitles now use the available player width, then states explicitly that audio, subtitle timing and the version 1.24.0 PDF editions remain unchanged. That sentence is the discipline: a changelog records what changed and what was deliberately retained. Immutability is enforced, not aspirational — `CONTRIBUTING.md` says an existing published edition is never overwritten. The prepare-release tool assembles the PDFs, MP4, captions and source registers with checksums; the publish tool verifies GitHub's SHA-256 digests first. Timing: 4 minutes. Transition: what makes content changes safe? -->

---

## `make check` — content needs tests

- `ai_qe/Makefile`: `check: models build site browser`
- Browser QA: five CI-identical groups
- Both Chromium and WebKit
- Viewports: 1280×720, 1920×1080, 375×812
- An overflowing slide fails like a unit test
- Links are checked; a 200 is not proof

<!-- NOTES: `ai_qe/Makefile` defines check as models, build, site, browser. Models runs the npm tests, the Python unit tests, narration validation with require-complete, and contract validation. Build runs Jekyll and finalize. Browser runs five CI-identical groups declared in `tools/qa-groups.json` — playback, flows, site, models, architecture — in both Chromium and WebKit at three viewports: twelve eighty by seven twenty, nineteen twenty by ten eighty, and three seventy-five by eight twelve. One more line to keep: the link check does not treat a successful HTTP response as evidence a claim is correct. Timing: 4 minutes. Transition: media needs its own gate. -->

---

## Hash-gate the media

- `ai_qe/tools/narration-review.cjs` hashes each slide
- A changed destination needs `retained` or `refreshed`
- Reasons are recorded in `assets/data/narration-review.json`
- "Never reset the baseline to silence a stale-review failure"
- A baseline reset rubber-stamps the drift you erased

<!-- NOTES: One hundred sixteen slides carry recorded narration, so a silent slide edit would desynchronize the voice from the slide. `tools/narration-review.cjs` hashes each rendered slide together with its script, recording and caption-flow definitions. A changed destination requires a deliberate retained or refreshed decision with a specific reason, committed to `assets/data/narration-review.json`. Then the line to tattoo on your pipeline, from `CONTRIBUTING.md`: never reset the baseline to silence a stale-review failure. Resetting converts a drift alarm into a rubber stamp. Timing: 4 minutes. Transition: now the commercial end. -->

---

## The pilot is the product

- Five phases (0–4), each with a cost ceiling
- Effort in person-day ranges, never dollars
- Each phase ends in a sponsor-signed go/no-go memo
- Freeze the outcome before observing results
- A CI crossing 10% or 15% is insufficient evidence
- ≥30 comparable tasks per arm

<!-- NOTES: `ai_qe/docs/method/phased-pilot.md` is the engagement the whole funnel points at: five phases, each with an objective, a duration, deliverables and a cost guardrail. Effort is stated in person-day ranges, deliberately not converted to dollars, and every phase ends with a written go/no-go memo signed by the sponsor. Measurement freezes the goal before any result exists: record the primary outcome and acceptance criteria before observing pilot results, and do not choose a different success metric after seeing a favourable one. Timing: 5 minutes. Transition: the boundaries are data. -->

---

<!-- _class: proof -->

## Gates live in data

`ai_qe/_data/pilot_gates.json`

```json
{ "go_saving": 15, "review_saving": 10, "baseline_weeks": 3,
  "pilot_weeks": 8, "observation_releases": 2,
  "min_tasks_per_arm": 30, "max_extension_weeks": 4 }
```

- Boundaries are data, not prose
- Benefits register: one row per capture mechanism
- No capture row means productivity, not cash
- Pointer: `ai_qe/docs/method/phased-pilot.md`

<!-- NOTES: The exact boundaries live in `_data/pilot_gates.json`, not in a paragraph someone can soften later: a fifteen percent net-effort go threshold, a ten percent review band, a three-week baseline, an eight-week pilot, two observed releases, at least thirty comparable tasks per arm, and one extension of at most four weeks. The rule that separates this from every pilot you have suffered: a confidence interval crossing ten or fifteen percent is insufficient evidence for that boundary, even if its point estimate looks favourable. A noisy result is no result. Timing: 5 minutes. Transition: the lab. -->

---

## Lab M6 — Build a mini-briefing

- Goal: 12 evidence-cited slides, provenance, two routes
- Plus a dated research log and an edition decision
- Pass: every slide claim maps to a provenance row
- Pass: executive route of 6 ends in a decision ask
- Pass: technical route keeps ≥3 skipped evidence slides
- Peer review confirms no uncited quantitative claim

<!-- NOTES: Lab M6 is the archetype-three checkpoint. You produce five artifacts: a research log with at least six dated Question, Checked, Outcome, Changed entries including at least two not-verified items; a provenance table with one row per claim; a twelve-slide outline where every quantitative slide cites a row by number; two routes over the same twelve slides, one executive and one technical; and an edition decision record for a hypothetical version two. Every checklist item is binary. Nothing is graded on taste. Timing: 4 minutes. Transition: the quiz. -->

---

## Quiz M6

- 8 questions: 6 multiple choice, 2 short answer
- Claim levels; provenance requirements
- Route design; edition discipline; pilot gates
- Answer key maps each question to a segment
- Pointer: `course/03-content/m06-expertise-product/quiz.md`

<!-- NOTES: The quiz has eight questions, each mapped to exactly one segment objective — that mapping is printed with the answer key. The multiple-choice distractors are the misconceptions we taught against: a working HTTP response as proof of a claim, a "balanced combination" option on the outcome question, bumping every edition together, extending a pilot until the interval excludes the boundary, and republishing over a released edition. Take it after the lab; the two short answers are the real assessment. Timing: 2 minutes. Transition: recap the module. -->

---

## Recap

- Citation is evidence; log before you publish
- Four levels, never mixed
- Publish your own audit — 14 findings
- 116 slides → four decks; routes end on decisions
- Editions in, tests pass, releases immutable
- Sell measurement, not outcomes

<!-- NOTES: Six lines to carry out of this module. The citation is the evidence, and research gets logged before it reaches a slide. Label every number with one of the four levels and never mix them. Publish your own audit: fourteen findings, a remediation table, and refusals stay published. Route one research base of one hundred sixteen slides into four decks whose guided routes end on a decision. Put content under edition discipline where tests gate the change and published editions are immutable. Finally, sell measurement, not outcomes. Timing: 3 minutes. Transition: one discussion prompt before you go. -->

---

## Discussion prompt

- Find a claim that mixes the four levels
- Name the real level and the sold level
- Write the honest replacement wording in one sentence
- Ground it in one AI × QE pointer
- Post it: does honesty weaken or sharpen the ask?

<!-- NOTES: For the community post, find one quantitative claim from your field's public discourse that mixes the levels — a task-level number presented as a budget saving, or a self-reported figure presented as measured. Post the claim as written, name the level it actually belongs to, name the level it is being sold as, and write the honest replacement wording in one sentence, borrowing the tone of the Use list in slide-language dot md. Then answer the real question: does the honest wording weaken the pitch, or sharpen the ask? Timing: 2 minutes. -->

---
