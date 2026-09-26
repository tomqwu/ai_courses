# Module 7 — Monetize: Pricing, Packaging, Positioning

> Part of AI Product Studio (APS-3) · ~60 minutes · Prerequisites: Modules 1–6

## Overview

Modules 1–6 built the working cores of three products. Module 7 prices them. Pricing here is not a gut call — it is an engineering decision derived from evidence: a sourced competitor table, a computed cost floor, and claims your buyer can audit. Every number traces to a repo file you can open, the course's research (`course/00-research/`), this course's own decision record (`course/04-sales/pricing-and-platforms.md`), or a named assumption you replace with your own dated figure. Two worked floors show the arithmetic; the course's own record is a third.

By the end of this module you can **price** a product per archetype from competitive evidence, **package** it and choose platforms by channel economics, and **market** it with honest, qualified claims (M7.1–M7.3). Lab M7 applies all of it to *your* product (from Lab M2, M4, or M6): a sourced pricing table, a decision worksheet, a positioning one-liner, a packaging page, and a self-review that survives a skeptical engineer.

## Segment M7.1 — Pricing the three archetypes (~20 min)

### Objective

Choose a pricing model for each archetype from evidence, not instinct: one-time vs subscription for an app, per-seat tiers with paid paths gated until proven for a SaaS, and a staged funnel that sells measurement for expertise. Name what each recurring-cost model — per-seat, usage, per-outcome, hybrid, bring-your-own-key discount — matches and punishes. State what each choice implies about who pays, and at which stage.

### Lesson

**Type 1 — price the way your costs recur.** Open `ListenToMe/docs/competition-analysis.md` and read the Price column; entries carry the file's own uncertainty convention — unconfirmable details are qualified "approximately" or "reportedly" (header, dated 2026-09). The market, condensed:

| Tool | Pricing model | Price (2026, per `competition-analysis.md`) |
|---|---|---|
| Granola | per-user/mo | Free tier; Business ~$14/user/mo; Enterprise ~$35/user/mo |
| Otter.ai | per-user/mo | Free (300 min/mo); Pro ~$8.33–16.99/user/mo; Business ~$20–30/user/mo |
| Fireflies.ai | per-seat/mo | Free; Pro ~$10–18/seat/mo; Business ~$19–29; Enterprise ~$39 |
| Superpowered | per-user/mo | Free (10 notes/mo); Basic $25/mo; Pro $50/mo |
| Cluely | per-user/mo | Free Starter; Pro $19.99/mo; Pro + Undetectability $149.99/mo |
| MacWhisper | one-time (direct) | Free tier; Pro ~€59 (~$69) one-time; App Store $6.99/mo–$99.99 lifetime |
| Natively | free + Pro | Free personal; Pro via lifetime/yearly |
| ListenToMe | free & open-source | $0, MIT |

The pattern is structural, not stylistic. Every tool that charges monthly runs per-user compute in the cloud: Granola streams every meeting through third-party cloud ASR and cloud LLM summarization; Otter runs its own proprietary ASR plus cloud LLM insights on its servers (per-competitor sections, `competition-analysis.md`). MacWhisper runs Whisper fully on-device — near-zero marginal cost per user — and charges once. The decision rule in one line: **if your per-user costs recur monthly, price monthly; if they do not, a subscription is a tax your users can audit you against.**

**Five models for a cost that recurs.** Without a recurring cost, stop at one-time or free + Pro (MacWhisper, Natively). With one, pick from five; choose by what the cost, and the buyer's value, grows with:

| Model | Matches | Punishes | Example |
|---|---|---|---|
| Per-seat | Value and cost that grow with each person using it | Growth in low-value seats (volunteers, viewers); seat-sharing | Granola Business ~$14/user/mo (`ListenToMe/docs/competition-analysis.md`); SignUpFlow's invitation is the billing event |
| Usage | A cost that grows with consumption: tokens, minutes, core-hours | The buyer's budget: bills they cannot predict | Otter's free tier, 300 min/mo (same table); GitHub Codespaces, 120 free core-hours a month then $0.18 each (`course/00-research/05-platform-build-options-2026.md` §4, third-party) |
| Per-outcome | Value the buyer can count: a resolved ticket, a filled shift | The seller, whenever attribution is disputed | Intercom's $0.99 per resolution (`course/00-research/08-domain-currency-2026.md`, cross-cutting; vendor blog, secondary); AI × QE declines it (below) |
| Hybrid | A predictable base plus a variable cost you must cap | Simplicity: two numbers to explain, overage surprises | Circle, $89/mo plus a 0.5–2% transaction fee (05 §1, third-party); the Cloud tier below |
| BYOK discount | An inference cost you can hand to the customer | Buyers without a key, and any "local" claim | MacWhisper: your own API keys, or a paid cloud assistant (table, MacWhisper section); ListenToMe: a cloud option "with your own key" (`ListenToMe/README.md:38-39`) |

BYOK moves the bill, not the data: it "is not local — your prompt still travels to a cloud provider" (08, cross-cutting). Direction, not fact: secondary reports say seat-only pricing fell while hybrid and outcome models rose to ~41–43% of AI SaaS (same section). *Evidence: a pricing vendor's blog, secondary — teach the direction, not the percentage.*

**Where "free & open-source" positions.** ListenToMe prices at $0 — MIT-licensed, "code open for inspection" — against a category running $8–149/mo (`competition-analysis.md`). Free is a price with a business model attached, and the syllabus names the paying surfaces: the reputation funnel, support, and a Pro tier (`course/01-design/curriculum.md`, M7.1). The reputation funnel is working on you right now — the repo, README, coverage badge, and 13-competitor analysis are the marketing. The Pro tier is not hypothetical: Natively, the open-source peer, prices "Free personal; Pro via lifetime/yearly" (`competition-analysis.md` row). Open-source does not mean no revenue; it means the paid tier sits *above* a complete free core, never as a repair of a crippled one.

**The wedge competitors cannot match without rebuilding.** The table names the category's two structural tensions: privacy vs convenience — "nearly every commercial product processes audio and runs its AI in the cloud, even when it markets itself as 'local-first' — the local part is usually just audio *capture*" — and opinionated vs open, where most products lock you to one undisclosed transcription engine and one summarization LLM (`competition-analysis.md:14`). ListenToMe's privacy + BYO-model position is defensible not because it is secret but because copying it destroys the incumbent business model: their monthly price *pays for* cloud ASR and cloud LLM compute; genuinely on-device transcription with a bring-your-own local model removes the cost base the subscription is priced on. A durable pricing differentiator is expensive to copy in **business-model terms**, not merely in code terms.

**Type 2 — per-seat tiers, and gate what is not proven.** SaaS value scales with the organization, so the unit of price is the seat. The pricing lesson is SignUpFlow's feature-gating pattern. Read the README's "Provider-backed Features" paragraph: billing routes remain in the codebase under `/api/v1`, SMS routes under `/api/sms`, "but both return 404 by default behind `BILLING_ENABLED=false` and `SMS_ENABLED=false`. Paid billing and SMS are deferred; the complete scheduling workflow does not require them." (`SignUpFlow/README.md`). `SignUpFlow/AGENTS.md` states the rule outright: "core scheduling must not require either paid integration."

That sentence bars two failure modes. First, charging for a path that is not yet trustworthy — billing wired into a workflow the team cannot yet rely on. Second, gating the core workflow to force upgrades — a scheduling product that stops scheduling until you pay. The monetization order is: make the workflow trustworthy, *then* flip the flag. The paid paths are registered and flag-gated, so monetization later ships as configuration, not surgery.

**Invitation-growth mechanics.** SignUpFlow grows organization by invitation: `/auth/signup` atomically creates the org plus its first admin, and "all later members join through administrator-created invitations" — "token-based volunteer onboarding" (`SignUpFlow/README.md`). Growth and billing are the same event: every new member is an invited org member, so per-seat pricing tracks real adoption, and the person who invites — the admin — is the buyer. When you design your SaaS growth loop, make it produce the billing event.

**Type 3 — the funnel that sells measurement.** AI × QE's funnel is visible in its own files: `ai_qe/index.md` routes the visitor through four path cards (01/VISION, 02/THE STORY, 03/ARCHITECTURE, 04/NEXT STEP), and the terminal page is `ai_qe/discovery.md` — "Start with one workflow. Agree what better means." — ending in a questionnaire download (`course/00-research/03-ai-qe-deep-read.md` §1). The stages, and what each one qualifies:

| Stage | What it is | What it qualifies |
|---|---|---|
| 1. Free evidence site | 116 cited slides, research log, published self-audit | Trust — demonstrates competence and pre-answers objections at zero marginal cost |
| 2. Questionnaire | v4 form: 36 questions, role-routed, single-select on the three questions that define success | Fit and scope — qualifies the lead and feeds the baseline model |
| 3. Fixed-fee discovery | "fixed-fee or capped discovery; separately capped pilot… No client price or start date has been agreed." (`ai_qe/_data/engagement.json`) | Budget and sponsor — a bounded first paid engagement |
| 4. Capped phased pilot | 8–10 weeks, five phases (0–4), go/no-go gates signed by the sponsor; frozen acceptance criteria *before* observing results; ≥30 comparable tasks per arm; 10%/15% effort decision bands; one extension ≤4 weeks | Whether to scale |
| 5. Validation | 1–2 quarters with a benefits-realization register | Renewal, on evidence |

(All rows: `course/00-research/03-ai-qe-deep-read.md` §1, §4.)

**Sell measurement, not outcomes.** The consultant never promises a savings number: the executive workshop presents questionnaire results as "questions rather than conclusions; no savings number yet" (deep-read §4). The pricing-integrity device is the benefits-realization register: it "ties every claimed saving to a Finance-owned budget row" (deep-read §4) — claims are reconciled by the client's *own* finance function, so an inflated number is not just dishonest, it is checkable. Price what you deliver — the discovery, the baseline, the instrumented pilot — and let outcomes belong to the register.

### Action step

Write one sentence per archetype naming the pricing model for **your** product, who pays, and at which stage they pay — e.g., "one-time $X at download, because my per-user cost is zero," or "per seat, billed when an admin invites the fourth member." Post it to the community. Lab M7 makes you defend it with a table.

## Segment M7.2 — Packaging and platforms (~20 min)

### Objective

Package the offer so the price buys a transformation and a set of artifacts, not video hours; choose platforms from channel economics rather than habit; and compute a cost floor — fixed lines plus an inference-cost line — and its break-even before setting any price.

### Lesson

**Cohort and self-paced are different products.** The same content is two value propositions: the research's rule of thumb is "$97–297 self-paced, or $500–2,000+ as a live 4-week cohort" (`course/00-research/02-course-market-research.md` §C, citing ShopSpace). What the cohort buyer pays for is live instruction, feedback, and peers — Maven's benchmarks price exactly that: 6–8 live hours + 1+ project → $800–1,200; 8–12 hours + multiple projects/capstone → $1,200–1,800; 12–20 hours + multiple projects + capstone → $1,800–2,450 (§C).

**The fraction-of-live-price rule.** Self-paced is priced as a fraction of the live tier: 70–85% *if it keeps projects + async feedback + community* — and if it keeps none of that, the research's verdict is that a bare library "shouldn't be sold at all" (§C). The anti-pattern the rule exists to prevent, verbatim: **"a stack of Zoom recordings is not a self-paced course"** (§C). Price the artifacts and the transformation — the review, the feedback, the objective lab checklists — not the video hours. The rule generalizes to every archetype: a stack of features is not an app tier; a stack of notes is not a briefing. Ask what the buyer can *show* for the money.

**Marketplace vs own platform.** Udemy: 37% payout on marketplace sales (32¢ per dollar in 2025), platform-controlled $9.99 pricing, and no student-email export — "use only as lead-gen/validation, never primary" (§D). Own-platform creators charge $50–200+ against Udemy's effective $10–15 (§C, §D). The course's own platform table — Maven for the cohort, Thinkific/Teachable for self-paced, Gumroad for the lead product, Circle for community, "Never Udemy (primary)" — is the worked decision (`course/04-sales/pricing-and-platforms.md`).

**App store vs direct for Type 1.** MacWhisper is the natural experiment in channel economics: the same product sells at ~€59/$69 one-time on Gumroad and $6.99/mo–$99.99 lifetime on the App Store (`competition-analysis.md` row). The store brings reach and subscription expectations, takes a cut, and owns the customer; direct gives you the margin and the email address. Direct is not a compromise — you already have the machinery from Module 3: signed, notarized, stapled releases published as DMGs targeting the exact commit (`ListenToMe/docs/RELEASING.md`). Choose per product: store for reach, direct for margin and the customer relationship.

**Compute the floor before the price.** The **fixed floor** is what you pay each month before anyone buys: hosting, database, email, developer membership, build time amortized. The **inference-cost line** is what one more user costs you each month:

```
inference cost / user-month = calls per month × tokens per call ÷ 1,000 × rate per 1,000 tokens
contribution per sale       = price − payment fee − variable cost
break-even                  = fixed floor ÷ contribution, rounded up
```

Every input is a source you can point at or an assumption you name. No file in this course carries a current model-API rate, so both examples **assume $0.005 per 1,000 tokens, input and output blended** — a placeholder, not any vendor's price. Retrieve your provider's rate card, date it, substitute; the arithmetic holds for any value. The course's own floor is the simplest case, all fixed: platforms + community + email ≈ $80–130/month, so break-even at the $399 self-paced tier is ~2 sales/month (`course/04-sales/pricing-and-platforms.md`, "Cost floor"). A price below your floor is not a price; it is a subsidy.

**Worked floor 1 — TinyCopilot as a product (Type 1).** Sell the Lab M2 copilot as a Mac app with a cloud option. Inputs:

- **A1** 20 meetings per user per month; **A2** 30 Quick answers per meeting — *assumptions*. The ceiling is 450: one per 8-second debounce for an hour (`ListenToMe/Sources/ListenToMeCore/ContextEngine.swift:8`).
- **A3** 1,800 tokens per answer: the 4,000-character window (`ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:582-586`) at an *assumed* 4 characters per token, plus *assumed* 500 of prompt and 300 of answer.
- **A4** One recap per meeting, 26,000 tokens: the 100,000-character recap budget (same lines) ÷ 4, plus 1,000 out — a ceiling.
- **A5** Payment fee 5% + $0.50 per sale through a merchant of record (`course/00-research/05-platform-build-options-2026.md` §2, third-party).
- **A6** Fixed cash $28.25/mo: developer membership $99/yr (`ListenToMe/docs/superpowers/specs/2026-06-18-listentome-design.md:259`) plus hosting at the top of 05 §1's ~$0–20/mo band. **A7** Build time $333.33/mo: 160 hours × $50 ÷ 24 months — *assumption*.

Walk it. Per meeting, 30 × 1,800 + 26,000 = **80,000 tokens**; per user-month, 20 × 80,000 = **1.6 million**. If you pay, the inference-cost line is 1,600 × $0.005 = **$8.00 per user per month**. Who pays depends on where inference runs. **On-device**: you pay $0; the user pays in hardware, ~8–16 GB of RAM for a 7B model at 4-bit (05 §4, third-party), and the platform's on-device model is free per request (`course/00-research/06-competitive-landscape-2026.md` §3). **BYOK**: you pay $0; the customer's provider bills them for the same 1.6 million tokens — print the formula beside the key field. **Platform private cloud**: you pay $0 while you qualify. Apple gives Small Business Program apps under 2M first-time downloads a private-cloud model tier "at no cloud API cost", 32K context, with a per-user daily quota (`course/00-research/08-domain-currency-2026.md`, Domain 1; vendor sessions, not independently confirmed). The 26,000-token recap fits.

The fixed floor is $28.25 + $333.33 = **$361.58/month**. Pro at $69 once — MacWhisper's anchor — nets $69 − $3.45 − $0.50 = **$65.05**: break-even is $361.58 ÷ $65.05 = 5.6 → **6 Pro sales a month**. A managed-cloud tier must clear $8.00 after fees, 0.95 × price − $0.50 ≥ $8.00, so price ≥ **$8.95**. At $12 it contributes $12 − $1.10 − $8.00 = **$2.90**; a 40-meeting user costs $16.00, so the tier carries a cap.

| Tier | Where inference runs | Your cost / user-month | Price | Model |
|---|---|---|---|---|
| Free | On-device | $0 | $0 | Complete free core |
| Pro | On-device; BYOK; platform private cloud where eligible | $0 | $69 once (nets $65.05) | One-time, BYOK discount built in |
| Cloud | Managed, to 1.6M tokens/month; then on-device | ≤ $8.00 | $12/month (nets $10.90) | Hybrid: subscription + allowance |

**What the private tier changes.** On a qualifying Mac or iPhone, cloud-class answers ship inside the one-time Pro. It cannot promise "unlimited" (the platform meters the quota), "on-device" (it is a cloud, however private — label it as its own privacy tier, as M3's modes do) or permanence (qualification ends at 2M downloads). Keep the Cloud tier as the fallback — and the only cloud option on Windows and Linux, where TinyCopilot also runs (`course/03-content/m02-ondevice-app/tinycopilot/README.md`). Its $12 sits inside Otter's ~$8.33–16.99 Pro band (`ListenToMe/docs/competition-analysis.md`): a recurring inference line, priced.

**Worked floor 2 — a SignUpFlow-shaped SaaS (Type 2).** SignUpFlow ships "No hosted service, paid plan, or production deployment" (`SignUpFlow/README.md`, Quick Start) and schedules with a greedy heuristic, not a model. So price the hypothetical: host it for volunteer organisations, with one LLM feature drafting each event's rota announcement and a swap proposal when someone declines. Inputs:

- **B1** 40 members per organisation (3 admins, 37 volunteers); **B2** 12 events a month; **B3** 250 emails a month (12 events × 10 volunteers × 2, plus 10 invitations); **B4** 2 LLM calls per event at 2,500 tokens each (2,000 in, 500 out) — *assumptions*. The rate is the same assumed $0.005.
- **B5** Database $25/mo (Supabase Pro, 05 §1, third-party); $0 in dev on the "SQLite (dev) / PostgreSQL (prod)" ladder (`SignUpFlow/README.md`). **B6** Hosting $20/mo, the top of 05 §1's band — a static-site estimate, so a floor for an API server.
- **B7** Email $15/mo for up to 40,000 — *assumption*, the figure in SignUpFlow's superseded roadmap (`SignUpFlow/docs/LAUNCH_ROADMAP.md`, marked historical); re-price it.
- **B8** Payment fee 5% + $0.50 (05 §2). **B9** Build time $666.67/mo: 320 hours × $50 ÷ 24 months — *assumption*; 320 hours is that roadmap's own estimate.

Walk it. The fixed cash floor is $25 + $20 + $15 = **$60/month**; with build time, **$726.67**. The inference-cost line is 12 × 2 × 2,500 ÷ 1,000 × $0.005 = **$0.30 per organisation per month** — small because calls scale with events, not members. Run the feature once per volunteer per event and it is $1.50: that is the line you cap. Email is a step cost: 40,000 ÷ 250 = **160 organisations**, free and paid, before the plan steps up. Test the prices SignUpFlow's own 2025 plan proposed — $29 for up to 50 volunteers, $99 for up to 200 (`SignUpFlow/docs/saas/STRIPE_INTEGRATION_PLAN.md`, a "Historical planning document") — with AI allowances as caps:

| Tier | Seats | AI calls/month | Price / org / month | Fee | AI at cap | Contribution |
|---|---|---|---|---|---|---|
| Free | ≤ 10 | none; full scheduling | $0 | — | $0 | rides the fixed plans |
| Starter | ≤ 50 | 50 | $29 | $1.95 | $0.63 | **$26.42** |
| Professional | ≤ 200 | 200 | $99 | $5.45 | $2.50 | **$91.05** |

**Break-even:** $60 ÷ $26.42 → **3 Starter organisations** cover the cash floor; $726.67 ÷ $26.42 = 27.5 → **28 Starter** (or 8 Professional) repay the build too. Inference is at most ~2% of Starter's price, so the fixed floor decides break-even. Fellow's ~$7/user/mo Team price (`ListenToMe/docs/competition-analysis.md`) would bill this organisation $280 a month for a tool three admins run: per-seat punishing volunteer growth. Price bands of seats, not heads.

**The third worked example is this course.** Read `course/04-sales/pricing-and-platforms.md` as the method applied to a real product — this one. The ladder: $0 lead product → **$399** Studio self-paced → **$1,490** Studio Live cohort (founding **$990**) → **$2,500–4,000** team tier. Not cheaper, because marketplace courses priced ≥$950 earn 50–100% more per landing-page visit, and $500–1,500 programs complete at 53–68% vs 18–25% at $97–197 — and completion is this product. Not more expensive yet, because there are no public testimonials: "raising price before social proof exists inverts the trust order" (all: `pricing-and-platforms.md`). And the founding discount is explicitly a *trade*: $990 (34% off) "is explicitly traded for a testimonial + 30-minute feedback interview (agreement at checkout)". Copy the record format, not just the numbers: floor, comparators, bands, launch policy, and a "why not cheaper / why not more expensive" that resists in both directions.

### Action step

Compute your product's monthly cost floor — hosting, API keys, amortized dev time — plus its inference-cost line and break-even, and write your two-sentence "why not cheaper," citing one benchmark from `course/00-research/02-course-market-research.md`. Post both to the community; you will paste them into the Lab M7 worksheet.

## Segment M7.3 — Honest marketing that converts (~20 min)

### Objective

Write the 8-section sales-page skeleton; assign the hero's role correctly; explain why being more skeptical than your audience converts; and derive a positioning one-liner whose every clause is falsifiable against your table.

### Lesson

**The hero is the buyer.** StoryBrand positioning, per the research: "the student is the hero, you're the guide" (`course/00-research/02-course-market-research.md` §E). Every section of your page answers the buyer's question — *does this get me there, and can I trust you?* — not yours. For a technical audience, "real shipped projects ARE the social proof" (§E): the repos, demos, dated evidence lines, and test badges you have been recording since Module 1 are your proof assets. Use them. Do not manufacture social proof — the course's own rule: "Never invent testimonials; ship beta before claiming social proof" (`course/04-sales/pricing-and-platforms.md`, honest-marketing checklist).

**Sales-page anatomy.** Eight sections, from the research's template drawn from 32k+ courses — a restructure along these lines took one creator from 1% to 8% conversion (§E):

1. **Transformation headline** — the outcome ("Ship three production AI apps…"), not the curriculum name.
2. **Who it's for — and who it isn't.**
3. **Problem and stakes.**
4. **Outcomes per module** — the curriculum framed as what the buyer can do after.
5. **Instructor proof** — relevance plus real projects, 100–150 words.
6. **Testimonials** — before/after/result form (when they exist; see above).
7. **FAQ** — answering real objections: time, level, refunds, "other courses failed me."
8. **Transparent pricing, one CTA.**

Length by price: 800–1,200 words under $200; 2,000–3,000 words for $500+ or cold traffic (§E). Module 8 builds the full page; today you draft its skeleton with three sections actually written.

**Skepticism converts.** The strongest evidence in this module comes from AI × QE. The site publishes, on its own decks, "the only independent RCT is negative," and stamps every planning number with its signature qualifier — "planning inputs are not observed client results" (`course/00-research/03-ai-qe-deep-read.md` §1, §3). The observed effect, in the deep-read's words: "An executive who reads 'the only independent RCT is negative' on a vendor deck's own site stops asking 'why should I believe you?' and starts asking 'when can we start?'" (§3). The mechanism: **qualified claims with sources are a premium signal.** They tell the buyer that you audit yourself harder than they would — and a buyer who reads your "what this doesn't prove" section has had their cheapest objection (belief) removed, leaving only the real question (start date). This is the course's checklist as a rule, not a vibe: "Every number on any sales asset carries a source"; "Qualify what's illustrative vs. observed" (`course/04-sales/pricing-and-platforms.md`, honest-marketing checklist items 1–2). The alternative — hide limitations until after purchase — fails on contact: technical buyers discover them inside the refund window, and the refund is the good outcome.

**The one-liner, derived not composed.** Module 3.3 derived ListenToMe's positioning clause-by-clause from its comparison table; the formula generalizes to every product: **adjective-wedge × differentiators × audience.** ListenToMe's:

> "ListenToMe is the free, open-source, fully on-device meeting copilot for macOS — bring your own model, run it private, and shape it to any conversation." (`ListenToMe/docs/competition-analysis.md:80`)

Trace each clause to a column, which is what makes it falsifiable instead of mood music:

| Clause | Column it comes from |
|---|---|
| "free" | **Price** — the field runs Free tiers up to $149.99/mo; nothing else in the copilot shape is free-and-open |
| "open-source" | **Privacy / AI features** — rivals are closed, undisclosed pipelines; "code open for inspection" has no counterpart |
| "fully on-device" | **On-device?** — only MacWhisper and Natively also answer Yes |
| "bring your own model" | **Multi-model/BYO** — most rows read "no picker"; only MacWhisper/Natively compare |
| "run it private" | **Privacy** — BYO local Ollama means "no audio need leave the machine" |
| "shape it to any conversation" | **Focus** — rivals pin one vertical (sales for tl;dv, interviews for Cluely, files for MacWhisper); 18 use-case presets serve many |

The test is deletion: remove a clause and the sentence must become false against a specific row. If no row would notice, the clause is decoration — cut it.

### Action step

Write the 8-section skeleton for **your** product's sales page — all eight section headers, one line each — with *real drafts* for section 1 (transformation headline), section 2 (who it's for / isn't), and section 5 (instructor proof, citing an artifact you actually have: a repo, a test run, an evidence line). Add the one "what this doesn't do" line you would publish. Post the headline and the honest-limitation line to the community. Lab M7 hardens this into a packaging page; Module 8 turns the skeleton into the full sales page.

## Recap

- **Price the way your costs recur.** Recurring per-user cloud compute → subscription (Granola, Otter); on-device → one-time (MacWhisper); free & open-source → reputation funnel, support, Pro (Natively).
- **Five models for a recurring cost** — per-seat, usage, per-outcome, hybrid, BYOK discount — each matches one cost shape and punishes another.
- **Floor = fixed lines + an inference-cost line**, each input sourced or named as an assumption; break-even = floor ÷ contribution. TinyCopilot: $8.00 per cloud user-month, 6 Pro sales a month. The SaaS: $0.30 per organisation, 3 Starter organisations for cash, 28 with build time.
- **Wedges must be expensive to copy in business-model terms.**
- **Gate what is not proven; never gate the core** (`SignUpFlow/AGENTS.md`).
- **Type 3 sells measurement**, with a benefits-realization register tying every claimed saving to a Finance-owned budget row.
- **Package the transformation, not the recording**; choose platforms and channels by payout, price control and customer ownership.
- **Honesty converts, and the one-liner is derived from the table** — every clause falsifiable against a column.

## Discussion prompt

Post the one claim on your draft sales page you are *least* comfortable defending to a skeptical engineer — then write the "what this doesn't prove" version of it and the source you would attach. Would you publish the qualified version? Reply to one peer: name which of their one-liner clauses their own comparison table would falsify, and which clause survives the deletion test.