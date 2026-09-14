# Quiz M7 — Monetize: Pricing, Packaging, Positioning

> 8 questions: 6 multiple choice + 2 short answer · ~10 minutes · Answer key with rationale and objective refs below

**Q1 (MC).** MacWhisper sells its Pro tier at ~$69 one-time while Granola charges ~$14–35/user/mo. One-time pricing wins when:

- A) You want to undercut rivals' sticker price and grow fast
- B) The product runs fully on the user's machine, so your per-user cost does not recur monthly
- C) Every competitor in the category is free
- D) You plan to stop maintaining the product after purchase

**Q2 (MC).** SignUpFlow's billing and SMS routes are registered under the API but return 404 behind `BILLING_ENABLED=false` / `SMS_ENABLED=false`. What does this pattern teach?

- A) Gate the core workflow behind billing so upgrades are forced
- B) Features are the tiers — every tier should add a visible feature
- C) Build the paid paths, flag them off, and never let the core workflow depend on them — monetize after the workflow is trustworthy
- D) Hide the gating so buyers discover the limitations only after purchase

**Q3 (MC).** Which ordering of the AI × QE funnel is correct, with the right qualification at each stage?

- A) Questionnaire → free site → uncapped retainer → pilot
- B) Free evidence site (trust) → questionnaire (fit) → fixed-fee discovery (budget and sponsor) → capped pilot with go/no-go gates (whether to scale)
- C) Free evidence site → paid pilot → discounted discovery → subscription
- D) Cold email → free trial → enterprise contract

**Q4 (MC).** "Sell measurement, not outcomes" — the consultant prices the discovery, baseline, and instrumented pilot, never a promised savings number. What makes this pricing-integrity device work?

- A) The pilot's go/no-go criteria are hidden from the client until the final invoice
- B) A benefits-realization register ties every claimed saving to a Finance-owned budget row, so claims are reconciled by the client's own finance function
- C) Only industry analyst figures are quoted, never the practitioner's own data
- D) Outcomes are promised in the kickoff call but kept out of the written scope

**Q5 (MC).** Your live cohort is $1,500 with projects, feedback, and community. Per the fraction-of-live-price rule, the self-paced tier should be:

- A) ~$150 — self-paced is roughly 10% of live price because video is cheap to deliver
- B) Identical to the cohort, since the content is the same
- C) 70–85% of the live price if projects + async feedback + community are retained — and a bare recording library should not be sold at all
- D) $9.99, to match marketplace pricing

**Q6 (MC).** Why is Udemy "never primary" for a premium technical course?

- A) It bans programming courses
- B) 37% marketplace payout, platform-controlled $9.99 pricing, and no student-email export — versus own-platform creators charging $50–200+
- C) Its audience is exclusively hobbyists
- D) Its reach makes refund requests rare, so limitations can stay hidden until after purchase

**Q7 (short answer).** Your product: a local-first CLI that drafts release notes from git history, runs fully offline, MIT-licensed, with a paid hosted tier for teams. Write the positioning one-liner in the ListenToMe format (adjective-wedge × differentiators × audience), add one "what this doesn't do" claim you would publish, and explain in one sentence why that claim increases conversion.

**Q8 (short answer).** A meeting-transcription web app sends audio to a cloud ASR vendor at $0.30/hour and stores transcripts on your servers. Choose a pricing model and the first tier's price, and justify in three sentences using one comparator rule from this module.

## Answer key

| Q | Answer | Rationale | Objective ref |
|---|---|---|---|
| 1 | B | Monthly prices track recurring per-user compute: Granola and Otter run cloud ASR + cloud LLM per meeting; MacWhisper's Whisper runs on-device, so ~$69 once is rational — "price the way your costs recur." A is the "price low to grow fast" misconception (`ListenToMe/docs/competition-analysis.md`). | M7.1 — price per archetype from competitive evidence |
| 2 | C | "Core scheduling must not require either paid integration" (`SignUpFlow/AGENTS.md`); paid paths registered but flag-gated; monetization ships later as configuration. A and B are the classic misconceptions ("gate the core to force upgrades"; "features are the tiers"); D violates the honest-limitation rule. | M7.1 — feature-gating rationale |
| 3 | B | The funnel is visible in `ai_qe/index.md` → `/discovery/`; fixed-fee discovery ("no client price or start date has been agreed," `engagement.json`) and sponsor-signed go/no-go gates qualify budget and scale (`course/00-research/03-ai-qe-deep-read.md` §1, §4). | M7.1 — funnel stages and what each qualifies |
| 4 | B | The register ties claimed savings to Finance-owned budget rows (deep-read §4), so claims are checkable by the buyer — which is exactly why they can't be inflated. A contradicts the go/no-go transparency the method requires. | M7.1 — sell measurement, not outcomes |
| 5 | C | Self-paced = 70–85% of live price only when projects + async feedback + community are retained; "a stack of Zoom recordings is not a self-paced course" (`course/00-research/02-course-market-research.md` §C). | M7.2 — fraction-of-live-price rule |
| 6 | B | Udemy economics from the research §D: 37% payout, $9.99 platform control, no email export; own-platform $50–200+ (§C). Marketplaces are discovery/lead-gen only. | M7.2 — marketplace vs own-platform economics |
| 7 | Model answer: "the free, open-source, fully offline release-notes copilot for small teams — bring your own repo, keep your history private, draft notes in one command." Each clause must map to a table column or capability (free/open-source ← price/license row; fully offline ← privacy column; bring your own repo ← BYO; one command ← workflow). Honest claim, e.g.: "It drafts factual, commit-derived notes — it does not invent roadmap promises your commits don't support." Why it converts: qualified claims are a premium signal — a buyer who reads the limitation stops asking "why believe you" and starts asking "when do we start" (`course/00-research/03-ai-qe-deep-read.md` §3). | M7.3 — one-liner derivation; honest-claim conversion logic |
| 8 | Model answer: per-user (or per-hour) subscription, ~$12–15/user/mo for the first tier. (1) Per-user cloud ASR cost recurs monthly, so a one-time price would be a tax users can audit — subscription matches the cost structure. (2) The first tier sits inside Otter's ~$8.33–16.99/user/mo Pro band and at Granola's ~$14 Business floor — position within the comparator band your table shows, above the cost floor. (3) The comparator rule: the price buys defined limits (hours transcribed, seats, retention) and is sourced, per the pricing-table convention (`ListenToMe/docs/competition-analysis.md`). | M7.1/M7.2 — choose model + first tier with a comparator rule |

**Scoring note (grading standard).** Auto-grade Q1–Q6; Q7–Q8 are graded against the model answers on the three checks each: Q7 (format followed; clauses traceable; limitation converts) and Q8 (model matches costs; price in band; comparator rule cited). 6/8 required to pass, consistent with the module standard.