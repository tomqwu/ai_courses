# Pricing — On-Device AI Apps (Track 1)

> **Price: $199** — self-paced, single track, lifetime access.
> Grounded in `course/00-research/02-course-market-research.md` and the course's decision record `course/04-sales/pricing-and-platforms.md`. Every claim here traces to one of those files or to a repo file pointer.

## The decision in one paragraph

$199 buys 4 of 9 modules plus a monetization-and-launch slice, 4 labs, 5 quizzes, the runnable TinyCopilot lab, and a Week 6 deliverable set — the module-by-module accounting is in `bundle-map.md`. It is deliberately priced at the **top of the entry band and below the course's own self-paced core tier**: high enough to be a real product with real lab gates, low enough to be an entry point into the full course rather than a substitute for it.

## What $199 buys — and what it deliberately doesn't

| Included | Not included (and why) |
|---|---|
| M0, M1, M2, M3 in full; the M7.1–M7.3 and M8.1–M8.2 teaching segments | M4/M5 (spec-driven SaaS) and M6 (expertise product) — those are Tracks 2 and 3 |
| Lab M0, Lab M1, Lab M2, Lab M3, and Lab M7 steps 1–5 scoped to your on-device app | The full Lab M7/Lab M8 course labs, the scored capstone, and demo day (`course/03-content/m08-launch-capstone/lab.md`) |
| Quiz M0–M3 and Quiz M7 — 40 questions with answer keys | Quiz M8, which tests capstone material outside this track |
| The `tinycopilot` reference implementation and its 201-test suite | Live workshops, instructor code review, cohort channel — those are cohort-tier ($1,490) |

## Why $199

1. **The completion-band evidence.** Ruzuku's platform data puts $97–197 programs at 18–25% completion and $297–497 at roughly 38–42% (`course/00-research/02-course-market-research.md`, §B). A track whose whole value is *shipping artifacts* wants the higher band — but this track's labs are objective-checkpoint labs with a community post, and its price has to leave room for the recommended upgrade. $199 is the compromise: entry-priced, but carrying the same checkpoint discipline that lifts completion.
2. **The platform median.** The median one-time course price is $150 (IQR $49–357) across 408 programs (`02-course-market-research.md`, §C). $199 sits just above median and well below the $300–500 self-paced "core" tier the same research identifies — i.e., an entry product, not a flagship.
3. **The self-paced-to-cohort fraction rule.** Maven's guidance is that self-paced should be a fraction of the live tier *if* projects, async feedback, and community are retained; a bare video library shouldn't be sold at all (`02-course-market-research.md`, §C). The parent course prices self-paced at ~27% of the cohort ($399 vs $1,490 — `course/04-sales/pricing-and-platforms.md`). This track at $199 is ~50% of the full self-paced price and ~13% of the cohort: an entry point, with community but no live review.
4. **The value anchor.** One shipped Type-1 app — a public repo, fail-closed privacy tests, a sourced pricing table, a sales page — is the deliverable. The alternative anchor is the engineer's own time: an entry seat recovers $199 with a single sale of almost anything the track teaches you to package.
5. **Why not cheaper.** A $49–99 price would put the track in the 8–12% completion band, and the research's cautionary tale is the opposite direction: flash-sale pricing devalues the cohort ladder (Udemy's $9.99 pattern is the recorded lesson, `course/04-sales/pricing-and-platforms.md`). Do not discount this track below $199, ever — discount the *decision*, not the price.
6. **Why not more (yet).** There are no testimonials for this track yet, and raising price before social proof exists "inverts the trust order" (`course/04-sales/pricing-and-platforms.md`, "Why not more expensive"). Maven's ≥$950 premium-per-visit effect applies to professional cohort products, not to a $199 self-paced single track.

**Honest per-module arithmetic:** the full course is $399 for 9 modules (~$44/module); this track is $199 for roughly 4.5 modules of teaching (~$44/module). The rate is the same — the full course isn't discounted, it's simply bigger. The track's advantage is the lower entry price; the full course's advantage is scope.

## Relationship to the full course ($399) and the cohort ($1,490)

The track must not cannibalize the full course. Here is the rule, stated plainly for the buyer:

- **If you want one product type:** buy this track. It is complete for that purpose — build TinyCopilot, harden it, price it, write its sales page.
- **If you want more than one product type, or you want the scored capstone:** buy the full course at **$399 — it is the recommended path.** For $200 more you add M4/M5 (the spec-driven multi-tenant SaaS built on SignUpFlow: "1,464 passed, 21 skipped" recorded with a date in `SignUpFlow/docs/playbooks/validation.md`; 7 test tiers in `SignUpFlow/docs/TESTING.md`), M6 (the evidence-cited expertise product built on AI × QE's 116 slides, `ai_qe/_data/briefing_room.json`), the complete Lab M7 and Lab M8, the capstone rubric with demo day, and 32 more quiz questions.
- **If you want live instruction, review, and a demo day:** the cohort at **$1,490** is the parent course's live tier, priced below Maven's $1,800–2,450 band for 12–20 live hours + projects + capstone because the instructor is not yet a recognized name (`course/04-sales/pricing-and-platforms.md`).

| Rung | Product | Price | Job in the ladder |
|---|---|---|---|
| 1 | *The 30-Minute AI Product Teardown* | $0 | List-builder, one repo teardown |
| 2 | **On-Device AI Apps (this track)** | **$199** | Entry product; one archetype, fully shipped |
| 3 | **AI Product Studio (full course)** — *recommended* | **$399** | All three archetypes + full labs + capstone |
| 4 | Studio Live (8-week cohort) | $1,490 (founding $990) | Live workshops, code review, demo day |
| 5 | Team (3–5 seats) | $2,500–4,000 | Private workshop and reviews |

This ladder is the tiering pattern the research recommends (self-paced core → live cohort → team; `course/00-research/02-course-market-research.md`, §C, §F), with the $199 track added below the core tier as a narrower on-ramp.

## Cannibalization guardrails (operational rules)

1. **The track is never sold as "the full course, cheaper."** Every sales asset links `bundle-map.md` and states the subset in the same screen as the price.
2. **The full course is always named as the recommended path** wherever the track is sold (`sales-page.md`, pricing table), with the $200 delta and what it adds.
3. **No upgrade pricing games.** No "credit your $199 toward $399" offer in launch, because it makes the full course look like the track plus a penalty. If a bundle credit is ever tested, the full course price stays $399 and the credit is capped at $99 — and only with recorded conversion data.
4. **The track carries no capstone certificate.** Completion evidence for the track is the tagged repo and demo, so the full course's capstone/certificate value stays distinct (`course/01-design/assessment-and-rubrics.md` thresholds are not restated here).
5. **Cost floor.** The parent course's lean month-1 floor is ≈$80–130/mo plus per-enrollment fees, breaking even at ~2 sales/month at $399 (`course/04-sales/pricing-and-platforms.md`). At $199 the track contributes roughly half the revenue per sale, so the track is a volume/entry play, not the business — say that internally, never on the page.

## Launch-price policy for this track

- **Launch price: $199.** No early-bird discount, no countdown. The parent course runs a $299 launch-week early bird on the $399 tier (`course/04-sales/pricing-and-platforms.md`); that stays a full-course decision and must never be priced below $199, or the track's price becomes incoherent.
- Founding-cohort discounts buy testimonials in the cohort tier, not here. When real track testimonials exist, the price is revisited upward — not the other way around.

## Refunds and guarantees

Full refund within 14 days, keep the materials — the parent course's policy (`course/04-sales/landing-page.md`). Generous refunds are a conversion asset for trust-sensitive technical buyers, and the lab-based artifacts make abuse rare (`course/04-sales/pricing-and-platforms.md`).

## Honest-marketing checklist (run before publishing any price change)

Per `course/04-sales/pricing-and-platforms.md`, all five items, quoted with each pass:

1. **Every number carries a source** → this file's numbers cite the research file, the pricing record, or a repo pointer.
2. **Illustrative vs. observed qualified** → completion bands are cited platform data, not this track's results; no track outcomes exist yet.
3. **Never invent testimonials** → `sales-page.md` ships an honest placeholder.
4. **Refund and deadline policies stated plainly** → 14 days, no fake countdowns.
5. **Price the transformation and the artifacts, not video hours** → the ladder above is priced by labs, quizzes, review, and capstone — not by runtime.
