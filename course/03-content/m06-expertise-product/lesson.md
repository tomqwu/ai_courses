# Module 6 — The Expertise Product: Evidence, Routing, Editions
> Part of AI Product Studio (APS-3) · ~75 minutes · Prerequisites: Modules 1–5

## Overview

Modules 2–3 shipped an on-device app; Modules 4–5 specced and hardened a SaaS. This module opens the third archetype: the **expertise product** — packaged expertise with an explicit sales funnel. Your case study is AI × QE, a research-backed presentation site about modernizing quality engineering and adding AI assistance around reliable testing in regulated financial services (`ai_qe/README.md`). On the surface it is a content site: four narrated decks, a fintech case study, research pages, downloadable PDFs. Underneath it is trust, engineered like software — and that is the archetype lesson: one expert's research base, methodology and presentation craft can become a versioned, tested, evidence-cited product that demonstrates competence, pre-answers objections, qualifies leads and pre-sells a consulting engagement, provided you treat credibility itself as the product.

AI × QE's topic is QA in banking; its discipline transfers to any field:

- **Evidence discipline** — every claim carries a citation, a date, a sample and an epistemic label; failures and unknowns are published, not hidden (M6.1).
- **Audience routing** — 116 slides re-cut into 4 decks plus guided routes, so one research base serves an executive in six slides and a technical lead in thirty, without forking the content (M6.2).
- **Content as code** — editions, tests, review gates, immutable releases; public content changes require a new edition before deployment (M6.3).

The enabler is the README's signature qualifier — "Planning inputs and proposed outcomes are not observed client results" (`ai_qe/README.md`, quoted in full in M6.1). Honesty is not a disclaimer bolted on afterwards; it is the differentiator that makes the product sellable.

In the lab you build a mini-briefing — 12 evidence-cited slides with a provenance table and two audience routes — from the provided AI-testing dataset or your own domain.

> **Pointer convention.** AI × QE pointers are relative to the `ai_qe/` repo root. Open every file the action steps name — the pointers are this course's provenance.

**By the end of this module you can:**

- Label every quantitative claim with one of the four "saving" levels plus an epistemic status, and avoid the mixing error.
- Keep a dated research log and provenance manifest a skeptic can audit, and re-cut one slide set into routes that end on decisions.
- Run content under edition discipline — separate site vs content versions, immutable releases, review gates.
- Design a pilot offer with go/no-go gates that sells measurement, not outcomes.

## Segment M6.1 — Credibility is the product (~25 min)

### Objective

Apply AI × QE's research conventions to claims in your own field: write benchmark records with full metadata, keep a dated research log with explicit "not verified" entries, maintain provenance manifests, label every number with one of the four "saving" levels, and explain why publishing your own audit converts skeptics.

### Lesson

**The citation is the evidence.** The research conventions (`ai_qe/CONTRIBUTING.md`, "Research conventions") open with a rule that sounds obvious and is almost never followed: "Research sources … are cited by name because the citation is the evidence; no vendor is endorsed." They continue: "Every benchmark record includes date, sample, method, unit, self-reported vs measured, sponsor, and what claim it can support. Anything unverifiable is listed as such." No client, partner or engagement names — "the bank", "the sponsor", "the advisory team".

Open `ai_qe/docs/evidence/benchmarks.md` and read one record end to end. The METR entry shows the shape: **Finding** — "AI-allowed issues took 19% longer (CI +2% to +39%); developers expected 24% faster and afterwards believed 20% faster." **Supports** — "Task efficiency (negative)." **Caveats** — elite developers on repositories they know well; expand for the rest: 16 maintainers, 246 issues, randomized; time per issue; "Measured (screen recording); independent non-profit." Two entries down, Peng: "55.8% faster (71.2 vs 160.9 minutes; CI 21% to 89%)"; 95 freelancers, one synthetic task; measured; "vendor-affiliated (Microsoft Research, GitHub, MIT)". Two real, measured results — one negative and independent, one positive and vendor-affiliated — and the record structure forces you to see the difference instead of averaging them into "AI makes developers 20–55% faster."

**Log research before you publish it.** `ai_qe/docs/research-log.md` is the intake queue for every claim: "Newest first. Each entry records the question, what was checked, the outcome, and what changed on the site. Add an entry before editing a topic page." Entries are dated and structured as **Question / Checked / Outcome / Changed**. The "Initial evidence base" entry's outcome states that "the only independent RCT is negative" — and, the part most sites would delete, an explicit **Not verified** list: World Quality Report cost-of-quality share, "any Gartner AI-testing productivity figure", Snyk DeepCode AI Fix accuracy, and more — plus standing "Open questions for future entries." `CONTRIBUTING.md` states the pipeline: "New research goes in `docs/research-log.md` first (dated entry), then into the topic page." Research you cannot verify goes on the list, not on the slide.

**Provenance files make claims checkable.** Three files exist only to record where content came from:

- `ai_qe/research/document-manifest.json` — 11 retrievals, each with URL, retrieval date, status and SHA-256 hash. It honestly logs a *failure*: the McKinsey PDF (id M02) has `"status": "unavailable"`, reason "The read operation timed out." A failed retrieval recorded in the manifest is worth more trust than a spotless manifest, because it proves the manifest is real.
- `ai_qe/research/visual-provenance.md` — the exact ImageGen prompts for the two hero illustrations, with the note that they are "conceptual editorial illustrations, not photographs of deployed systems." Even the pictures have provenance.
- `ai_qe/maintainers/narration.md` + `assets/data/narration-provenance.json` — voice/model provenance for the 116 narration scripts (57,182 spoken characters); unknown tier details are left null, not guessed.

**Label the level of every number.** `ai_qe/docs/principles.md` ends with the claim taxonomy the whole site runs on — quote it exactly:

| Level | Definition | Who can confirm it |
|---|---|---|
| Task-level efficiency | Net time reduction for a specific activity, after review, correction and control effort | Pilot measurement |
| QA capacity released | Reduction in human QA hours across the full workflow, after adoption and eligibility | Pilot measurement plus baseline time capture |
| Hard-dollar saving | Budgeted cost that Finance can actually remove or avoid | Finance, against a named budget line |
| Total software-spend impact | A broader measure of engineering or delivery cost that must not be mislabelled as QA saving | Finance and the CIO office |

"Every number on this site is labelled with one of these four levels. Mixing them is the most common error in AI business cases." A 55.8% task-level speedup is not 55.8% capacity released, let alone a hard-dollar saving: coding is roughly 16% of developer time and code generation 25–35% of idea-to-launch, so a 50% task gain "dilutes to single digits of total engineering time" (`ai_qe/docs/evidence/reading-the-evidence.md`). Note the third column — each level names *who can confirm it*: task-level claims need a pilot; hard-dollar claims need Finance against a named budget line. Not you.

**The signature qualifier.** Every deck carries it: "Planning inputs and proposed outcomes are not observed client results" (`ai_qe/README.md`). The fintech case is labeled illustrative everywhere, including inside the narration scripts. The product sells a *method* for producing real numbers, and says so in the one sentence a skimming executive will actually read.

**Publish your own audit.** `ai_qe/research/reviews/site-audit-2026-09-06.md` is a self-audit the site publishes about itself: **14 findings — four high priority, nine medium, one lower** — each with severity, evidence paths and acceptance criteria. Finding R01 is the site's own two conflicting "base case" economics. The companion `remediation-2026-09-06.md` maps every finding → implemented response → verification, as a table. A later review record even lists deliberate non-changes — "Do not hide weak economics, convert capacity to cash, or relabel unknown results as observed" (`research/reviews/review-56-resolution-2026-09-10.md`). Findings, responses and refusals all stay published.

**Why being *more* skeptical than your audience converts.** Put yourself in the buyer's chair. You have sat through vendor decks promising 30–50% productivity gains. Then a site whose entire surface is a pitch prints, in its own research log, that the only independent RCT is negative, that consultancy gains are rarely monetized, and that its own McKinsey source download timed out. The questions invert: you stop asking "why should I believe you?" and start asking "when can we start?" Skepticism is the pitch — it is the one thing a hype deck cannot counterfeit.

### Action step

Open the cloned `ai_qe` repo and verify with your own eyes, recording findings in your evidence log:

1. Open `docs/evidence/benchmarks.md`; confirm the METR and Peng records each carry date, sample, method, unit, measured-vs-self-reported, sponsor, and a "Supports" limit.
2. Open `research/document-manifest.json`; find the honestly-logged failed McKinsey retrieval (id M02, "The read operation timed out").
3. Open `docs/research-log.md`; read the "Not verified" list and the "Open questions" section.
4. Draft one dated entry (Question / Checked / Outcome / Changed) about a claim in your own field — including at least one thing you could *not* verify. That not-verified line is what makes the other three believable.

## Segment M6.2 — One research base, many audiences (~25 min)

### Objective

Re-cut one body of research into audience-specific decks and guided routes over stable slide IDs; script the meeting the deck serves; and design a questionnaire that qualifies leads by role — applying the design rules and failed-form post-mortem from `ai_qe/docs/method/discovery-questionnaire.md`.

### Lesson

**One research base, four decks.** `_data/briefing_room.json` defines the presentation room — 116 slides re-cut along two axes, audience (executive/technical) × scenario (banking/industry):

| Deck | Slides | Duration |
|---|---|---|
| Banking scenario · Executive | 21 | 25–30 min |
| Banking scenario · Technical | 33 | 35–45 min |
| Industry perspective · Executive | 26 | 30–40 min |
| Industry perspective · Technical | 36 | 45–60 min |

Nothing is forked: the executive gets the strategic cut, the technical lead gets contracts, sequencing and evidence schemas — both trace back to the same source records.

**Guided routes over stable slide IDs.** `_data/briefing_routes.json` defines curated sequences *over the same stable slide IDs* — the banking executive route plays 14 of the 21 slides (`1, 3, 19, 20, 6, 21, 18, 17, 13, 14, 15, 16, 10, 12`) and declares `"closing": 12`, the brainstorm-questions slide; `full_order` retains everything. The README states the rule: "Focused routes end on a decision discussion; full decks retain the supporting material." Stable IDs are the invariant — routes reorder and omit, they never rewrite, so a route link still resolves. Routes are shareable by URL: `?route=client` on a deck (`README.md`), plus `?for=evp` / `?for=technical` audience views, linked from the homepage (`ai_qe/index.md:27,29`) and documented as shareable views in `ai_qe/CONTRIBUTING.md:23`, with the briefing index filtering cards by that parameter (`ai_qe/assets/js/sales-navigation.js:31`).

**Script the meeting, not just the deck.** `briefings/index.md` embeds "A suggested 30-minute conversation": **01 / Align · 5 minutes** — which part of QA creates the most delay or repeated work? **02 / Explore · 15 minutes** — follow one workflow and show the platform services behind it. **03 / Agree · 10 minutes** — choose the process, owner and evidence needed for a first pilot, landing on the discovery guide. The deck is not the product; the conversation the deck enables is.

**Sell the decision, not the transformation.** `ai_qe/docs/economics/slide-language.md` prescribes exact slide wording; its executive message ends: "The decision today is whether to fund the first two phases, not whether to transform QA." Compare the file's two lists. **Use:** "Working hypothesis, to be tested on the bank's own data"; "Capacity released is not a saving until Finance confirms how it is captured." **Avoid:** "Industry benchmarks show 30-50% productivity gains"; "ROI of X% before a pilot has measured anything"; any squad-level headcount arithmetic. A bounded, fundable ask (Phases 0 and 1) is decidable; "transform QA" is not — and an undecidable ask stalls the deal it was meant to close.

**The questionnaire is lead qualification.** `ai_qe/docs/method/discovery-questionnaire.md` is not a survey; it is the funnel's filter. Its design rules are explicit: "One form, role-routed at the first question; respondents complete the sections they own and leave unknowns blank." Routing: executive sponsor, Finance and procurement answer Sections 1, 5B and 6; engineering, delivery, QE and platform leaders answer Sections 2, 3, 4, 5A and 6. Three structural rules do the heavy lifting:

- **Single-select on the questions that define success** — "Priority questions (what success means, the autonomy ceiling, the go/no-go threshold) are single-select." In v4: Q2 (the ONE outcome that justifies continuing), Q22 (highest acceptable AI-action level), Q31 (minimum net-effort reduction for phase two) — because the failed form's "balanced combination" escape option "produced no signal."
- **Taxonomy aligned to the model** — "The activity taxonomy in the effort question matches the activity categories in the savings formula so that answers feed the model directly."
- **Ranges that don't lie** — mutually exclusive and gap-free ("1-5 / 6-20 / 21-50 / more than 50", never "10-25 / 25-50"), with an unknown option "so that a guess is not recorded as data."

**Read the post-mortem; it is the best part.** The same file dissects the failed original: a "well-built 29-question form with 186 checkbox options across 19 multi-select questions, five dropdowns, two free-text tables and three open questions" that "takes a knowledgeable respondent 20-30 minutes, not 15" — and "No single respondent can answer all six sections: an executive cannot answer flaky-test or CI/CD questions, a QE director cannot answer contractor-renewal or Finance-recognition questions." The largest omission: "the financial-capture question set: budget ownership, variable share of spend, renewal windows, what happens to released capacity, and what Finance will recognize as a saving. Without those, the same 4% capacity result can be booked as a hard saving, as cost avoidance, or as nothing." The v4 form is 36 questions, role-routed, with a timing check: sponsor route about 11–13 minutes, engineering route about 15–25 minutes. One artifact, whole lesson: fewer escape hatches, role routing, and the financial questions that make a pilot fundable.

### Action step

1. Open `_data/briefing_room.json` and `_data/briefing_routes.json`; trace the banking executive route (14 slides, closing 12) against `full_order` (21 slides) and confirm the route omits only, never rewrites.
2. Open `briefings/index.md` and read the 30-minute script; open `ai_qe/discovery.md` and confirm where the Agree segment lands.
3. Take a 10–12 slide body of content you know and write two route declarations over stable IDs: a 5–6 slide executive route ending in a specific, fundable decision ask, and a technical route retaining the supporting evidence. Both routes over the *same* slides — that constraint is the exercise.

## Segment M6.3 — Content as code (~25 min)

### Objective

Run content under software release discipline: separate site and content editions, publish changelogs that record what was deliberately retained, gate media with hashes, keep releases immutable — and design a phased pilot with go/no-go gates that sells measurement instead of outcomes.

### Lesson

**Editions are the release discipline.** `_data/release.yml` keeps five separate fields: `version: "1.24.1"` (site and player), `slide_edition: "1.24.0"`, `fintech_edition: "1.24.0"`, `questionnaire_edition: "4"`, `research_edition: "1.7.0"`. The README states the rule: "Public content changes require a new edition before deployment." `CONTRIBUTING.md` is harder: content changes without a new edition "are rejected on main before deployment." Why two numbers? v1.24.1 was a player-only patch — `releases.md` records that "Audio, subtitle timing, and the v1.24.0 PDF editions remain unchanged." A subtitle fix advanced the site version while *deliberately retaining* the slide and PDF editions, so a client holding the v1.24.0 PDFs knows exactly what they have. The pattern to copy: `releases.md` entries state what changed **and what was deliberately retained**. Immutability is enforced, not aspirational: "An existing published edition is never overwritten" (`CONTRIBUTING.md`); "Superseded editions remain in immutable GitHub releases" (`releases.md`). `tools/prepare_release.py` assembles the ten current PDFs, MP4, captions, CSV/JSON source registers and checksums; `tools/publish_release.py` verifies GitHub's SHA-256 digests and "publishes only after all assets are complete."

**Content changes require tests to pass.** `make check` (`ai_qe/Makefile`) is `models → build → site → browser`: npm model tests, Python unit tests, narration validation with `--require-complete`, contract validation, Jekyll build and finalize, then browser QA. The browser suite is five CI-identical groups — playback, flows, site, models, architecture (`tools/qa-groups.json`) — run in **both Chromium and WebKit** at **1280×720, 1920×1080 and 375×812** (`CONTRIBUTING.md`, "Release validation"). A slide that overflows a projector viewport fails the build like a unit test. The link check refuses wishful thinking: "the link check does not treat a successful HTTP response as evidence that a claim is correct."

**Hash-gate the media.** 116 slides carry recorded narration, so a silent slide edit would desynchronize the voice from the slide. `tools/narration-review.cjs` hashes each rendered slide together with its script, recording and caption-flow definitions; a changed destination "requires a deliberate `retained` or `refreshed` decision with a specific reason," recorded in `assets/data/narration-review.json` (`CONTRIBUTING.md`). And the line to tattoo on your content pipeline: "**Never reset the baseline to silence a stale-review failure.**" A baseline reset converts a drift alarm into a rubber stamp — the gate exists precisely to catch the drift you would have erased.

**The pilot is the product: sell measurement, not outcomes.** `ai_qe/docs/method/phased-pilot.md` is the engagement the whole funnel points at: five phases (0–4), each with objective, duration, deliverables and a cost guardrail; effort is stated in person-day ranges "deliberately not converted to dollars. Each phase ends with a written go/no-go memo signed by the sponsor." Measurement freezes the goal before any result exists: "Record the primary outcome and frozen acceptance criteria before observing pilot results. Do not choose a different success metric after seeing a favorable result." Exact boundaries live in data, not prose — `_data/pilot_gates.json`: 15% net-effort go threshold, 10% review band, 3-week baseline, 8-week pilot, 2 observed releases, **≥30 comparable tasks per arm**, one extension of ≤4 weeks. And the rule that separates this from every pilot you have suffered: "A confidence interval crossing 10% or 15% is insufficient evidence for that boundary, even if its point estimate appears favorable." A noisy result is *no result*. Finally, the **benefits-realization register** ties any claimed saving to a Finance-owned budget row — one row per capture mechanism, the budget-line owner, the earliest date it could change, the evidence Finance will accept — because "A capacity result with no capture row is reported as productivity, not cash saving." That is what "sell measurement, not outcomes" means: the offer is a bounded, funded way to *produce* the number, never the number itself.

### Action step

Pick one quantitative claim from your own field — something you actually say to clients or colleagues. Write it at **all four levels** from `ai_qe/docs/principles.md`:

1. **Task-level efficiency** — net time reduction for one activity, after review/correction effort.
2. **Released capacity** — human hours freed across the full workflow, after adoption and eligibility.
3. **Hard-dollar saving** — budgeted cost Finance can remove or avoid, against a named budget line.
4. **Total-spend impact** — the broader engineering-cost measure that "must not be mislabelled."

For each level, mark **supported** or **not supported**, and name the evidence you would need (and who could confirm it — pilot, baseline capture, Finance). Then check which level your current materials actually claim. If they claim a level you marked not supported, you have found the most common error in AI business cases — in your own materials — before your buyer did. Carry this exercise into Lab M6.

## Recap

- **The citation is the evidence.** Every benchmark record carries date, sample, method, unit, self-reported-vs-measured, sponsor and what claim it supports; anything unverifiable is listed as such (`ai_qe/CONTRIBUTING.md`).
- **Log before you publish.** Dated Question/Checked/Outcome/Changed entries, plus explicit "Not verified" and open-questions lists (`ai_qe/docs/research-log.md`); provenance files hash every retrieval, including the failed McKinsey download (`research/document-manifest.json`).
- **Four levels, never mixed.** Task-level efficiency / released capacity / hard-dollar saving / total-spend impact — "Mixing them is the most common error in AI business cases" (`ai_qe/docs/principles.md`); "Planning inputs are not observed client results" (`README.md`).
- **Publish your own audit.** 14 findings → a remediation table mapping finding → response → verification (`research/reviews/`). More skepticism than your audience converts: "why should I believe you?" becomes "when can we start?"
- **Route one research base.** 116 slides → 4 decks (`_data/briefing_room.json`); guided routes over stable slide IDs ending on a decision discussion (`_data/briefing_routes.json`); "whether to fund the first two phases, not whether to transform QA" (`docs/economics/slide-language.md`).
- **Qualify with the questionnaire.** One form, role-routed at question 1; single-select on the three questions that define success; taxonomy aligned to the savings formula; the financial-capture set the failed 29-question/186-option form lacked (`docs/method/discovery-questionnaire.md`).
- **Treat content as code.** "Public content changes require a new edition before deployment"; "An existing published edition is never overwritten"; changelogs record what was deliberately retained; `make check` runs five QA groups across Chromium and WebKit at three viewports; "Never reset the baseline to silence a stale-review failure."
- **Sell measurement, not outcomes.** Sponsor-signed go/no-go gates; frozen criteria before results; ≥30 tasks per arm; CIs crossing a boundary = insufficient evidence; savings tied to Finance-owned budget rows (`docs/method/phased-pilot.md`, `_data/pilot_gates.json`).

## Discussion prompt

Find one quantitative claim from your field's public discourse that mixes the four levels — a task-level number presented as a budget saving, or a self-reported figure presented as measured. Post the claim as written, name the level it actually belongs to, name the level it is being sold as, and write the honest replacement wording in one sentence (borrow `slide-language.md`'s Use list for tone). Then answer: does the honest wording weaken the pitch, or sharpen the ask? Ground your post in at least one AI × QE file pointer showing the convention you applied.