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

**Q4 (MC).** Your macOS app sells at ~$69 one-time through your own checkout. A store listing would add reach, take a cut of every sale, push subscription expectations, and own the customer record. Choosing "by channel economics" means:

- A) Take the store — reach is the variable that compounds, and the cut is simply the cost of distribution
- B) Stay direct on principle — any platform cut is value destroyed, whatever it buys
- C) Price each channel for what it actually costs you — payout share, who controls the price, who owns the customer (and therefore the email address) — which is why the same product can run one-time direct and subscription-or-lifetime in the store; direct is only an option because you already have the signed, checksum-verified release pipeline from M3
- D) List in both at the identical price and model, so the comparison stays honest and buyers self-select

**Q5 (MC).** Your live cohort is $1,500 with projects, feedback, and community. Per the fraction-of-live-price rule, the self-paced tier should be:

- A) ~$150 — self-paced is roughly 10% of live price because video is cheap to deliver
- B) Identical to the cohort, since the content is the same
- C) 70–85% of the live price if projects + async feedback + community are retained — and a bare recording library should not be sold at all
- D) $9.99, to match marketplace pricing

**Q6 (MC).** Your desktop copilot runs on-device by default. Users who paste their own API key cost you nothing per month, and so do users served by the platform's private-cloud model while your app qualifies for its free tier; a managed cloud option costs you about $8.00 per active user per month at your assumed token rate. Which pricing structure matches these costs?

- A) One flat monthly subscription for every user, so the cloud users' cost is spread across everyone
- B) A one-time Pro covering on-device, bring-your-own-key and eligible private-cloud use, plus an optional capped monthly cloud tier priced above its $8.00 line
- C) Per-seat pricing at the category's ~$14/user/mo, because that is where the comparator band sits
- D) Per-token usage pricing for every user, on-device included, so every bill is proportional

**Q7 (short answer).** Your product: a local-first CLI that drafts release notes from git history, runs fully offline, MIT-licensed, with a paid hosted tier for teams. Write the positioning one-liner in the ListenToMe format (adjective-wedge × differentiators × audience), add one "what this doesn't do" claim you would publish, and explain in one sentence why that claim increases conversion.

**Q8 (short answer).** A meeting-transcription web app sends audio to a cloud ASR vendor at $0.30 per hour of audio and stores transcripts on your servers. Assume a typical user transcribes 20 hours a month and payments cost 5% + $0.50 per charge. Compute the per-user inference-cost line and the lowest monthly price that covers it, then choose a pricing model and the first tier's price, and justify in three sentences using one comparator rule from this module.

## Answer key

| Q | Answer | Rationale | Objective ref |
|---|---|---|---|
| 1 | B | Monthly prices track recurring per-user compute: Granola and Otter run cloud ASR + cloud LLM per meeting; MacWhisper's Whisper runs on-device, so ~$69 once is rational — "price the way your costs recur." A is the "price low to grow fast" misconception (`ListenToMe/docs/competition-analysis.md`). | M7.1 — price per archetype from competitive evidence |
| 2 | C | "Core scheduling must not require either paid integration" (`SignUpFlow/AGENTS.md`); paid paths registered but flag-gated; monetization ships later as configuration. A and B are the classic misconceptions ("gate the core to force upgrades"; "features are the tiers"); D violates the honest-limitation rule. | M7.1 — feature-gating rationale |
| 3 | B | The funnel is visible in `ai_qe/index.md` → `/discovery/`; fixed-fee discovery ("no client price or start date has been agreed," `engagement.json`) and sponsor-signed go/no-go gates qualify budget and scale (`course/00-research/03-ai-qe-deep-read.md` §1, §4). | M7.1 — funnel stages and what each qualifies |
| 4 | C | MacWhisper is the natural experiment: the same app is ~€59/$69 one-time on Gumroad and $6.99/mo–$99.99 lifetime in the App Store (`ListenToMe/docs/competition-analysis.md:34`), so the channel changes the model, not just the sticker. The three variables to price against are payout share, price control and customer ownership — the same three that make a marketplace lead-gen only (M7.2, Udemy). A treats reach as free; B makes a rule out of what should be a per-product calculation; D is what the evidence contradicts — identical pricing in both channels ignores that the store buys reach with your margin and your customer record. Direct is available at all only because M3's release discipline (tag at the tested commit, artifact checksum-verified) already exists (`ListenToMe/docs/RELEASING.md:33-36`). | M7.2 — choose platforms by channel economics |
| 5 | C | Self-paced = 70–85% of live price only when projects + async feedback + community are retained; "a stack of Zoom recordings is not a self-paced course" (`course/00-research/02-course-market-research.md` §C). | M7.2 — fraction-of-live-price rule |
| 6 | B | Price the way each cost recurs, tier by tier: on-device, bring-your-own-key and eligible private-cloud users cost nothing monthly, so a one-time price fits them (the BYOK discount) — though only the first may be sold as "on-device" (M3.1's three tiers); only the managed cloud tier recurs, so only it is monthly, priced above its line and capped (hybrid) — the M7.2 TinyCopilot floor (`course/03-content/m07-monetize/lesson.md`). A taxes on-device users for a cost they do not cause — the audit a buyer can run; C takes the price from the band without the cost structure; D meters compute you do not pay for. | M7.1 — pricing taxonomy: what each model matches and punishes |
| 7 | Model answer: "the free, open-source, fully offline release-notes copilot for small teams — bring your own repo, keep your history private, draft notes in one command." Each clause must map to a table column or capability (free/open-source ← price/license row; fully offline ← privacy column; bring your own repo ← BYO; one command ← workflow). Honest claim, e.g.: "It drafts factual, commit-derived notes — it does not invent roadmap promises your commits don't support." Why it converts: qualified claims are a premium signal — a buyer who reads the limitation stops asking "why believe you" and starts asking "when do we start" (`course/00-research/03-ai-qe-deep-read.md` §3). | M7.3 — one-liner derivation; honest-claim conversion logic |
| 8 | Model answer: inference-cost line 20 h × $0.30 = **$6.00 per user per month**, recurring; covering it after fees needs 0.95 × price − $0.50 ≥ $6.00, so price ≥ **$6.85**. Model: per-user subscription with a 20-hour allowance (hybrid), ~$12–15/user/mo for the first tier, leaving ~$4.90–7.75 per user toward the fixed floor. (1) Per-user cloud ASR cost recurs monthly, so a one-time price would be a subsidy that grows with use — subscription matches the cost structure, and the allowance caps the heavy user (40 hours costs $12.00). (2) The first tier sits inside Otter's ~$8.33–16.99/user/mo Pro band and at Granola's ~$14 Business price — within the comparator band your table shows, above the floor. (3) The comparator rule: the price buys defined limits (hours transcribed, seats, retention) and is sourced, per the pricing-table convention (`ListenToMe/docs/competition-analysis.md`). | M7.1/M7.2 — compute the inference-cost line, then choose model + first tier with a comparator rule |

## Objective → assessment map

Every "By the end of this module you can" clause in `course/03-content/m07-monetize/lesson.md`, and what checks it.

| Objective (lesson.md) | Checked by |
|---|---|
| **Price** a product per archetype from competitive evidence (M7.1) | Q1 (one-time vs subscription from how costs recur), Q2 (paid paths flag-gated, core never depends on them), Q3 (the expertise funnel and what each stage qualifies), Q6 (which of the five recurring-cost models matches each tier's cost), Q8 (choose a model and a first-tier price against a comparator rule); Lab M7 sourced pricing table + decision worksheet |
| **Package** it and choose platforms by channel economics (M7.2) | Q5 (fraction-of-live-price rule), Q4 (store vs direct priced against payout, price control and customer ownership), Q8 (inference-cost line and the price that covers it); Lab M7 packaging page + cost floor with inference-cost line and break-even |
| **Market** it with honest, qualified claims (M7.3) | Q7 (one-liner in the ListenToMe format plus a published "what this doesn't do" claim, and why it converts); Lab M7 positioning one-liner + the self-review that survives a skeptical engineer |

**Scoring note (grading standard).** Auto-grade Q1–Q6; Q7–Q8 are graded against the model answers on the three checks each: Q7 (format followed; clauses traceable; limitation converts) and Q8 (inference-cost line and covering price computed; model matches costs; price in band with a comparator rule cited). There is no per-quiz pass mark: scores feed the course-wide quiz average, which must be ≥75% for the certificate (`01-design/assessment-and-rubrics.md`).