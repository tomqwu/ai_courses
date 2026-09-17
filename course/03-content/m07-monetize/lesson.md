# Module 7 — Monetize: Pricing, Packaging, Positioning

> Part of AI Product Studio (APS-3) · ~60 minutes · Prerequisites: Modules 1–6

## Overview

Modules 1–6 built the working cores of three products. Module 7 prices them. Pricing here is not a gut call — it is an engineering decision derived from evidence: a sourced competitor table, a computed cost floor, and claims your buyer can audit. Every number traces to one of three places: a repo file you can open, the course's market research (`course/00-research/02-course-market-research.md`), or this course's own decision record (`course/04-sales/pricing-and-platforms.md`) — the method you are learning priced the course you are taking.

By the end of this module you can **price** a product per archetype from competitive evidence, **package** it and choose platforms by channel economics, and **market** it with honest, qualified claims (M7.1–M7.3). Lab M7 applies all of it to *your* product (from Lab M2, M4, or M6): a sourced pricing table, a decision worksheet, a positioning one-liner, a packaging page, and a self-review that survives a skeptical engineer.

## Segment M7.1 — Pricing the three archetypes (~20 min)

### Objective

Choose a pricing model for each archetype from evidence, not instinct: one-time vs subscription for an app, per-seat tiers with paid paths gated until proven for a SaaS, and a staged funnel that sells measurement for expertise. State what each choice implies about who pays, and at which stage.

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

The pattern is structural, not stylistic. Every tool that charges monthly runs per-user compute in the cloud: Granola streams every meeting through third-party cloud ASR (it names Deepgram and AssemblyAI) and OpenAI/Anthropic summarization; Otter runs its own proprietary ASR plus Claude-backed insights on its servers (per-competitor sections, `competition-analysis.md`). MacWhisper runs Whisper fully on-device — near-zero marginal cost per user — and charges once. The decision rule in one line: **if your per-user costs recur monthly, price monthly; if they do not, a subscription is a tax your users can audit you against.**

**Where "free & open-source" positions.** ListenToMe prices at $0 — MIT-licensed, "code open for inspection" — against a category running $8–149/mo (`competition-analysis.md`). Free is a price with a business model attached, and the syllabus names the paying surfaces: the reputation funnel, support, and a Pro tier (`course/01-design/curriculum.md`, M7.1). The reputation funnel is working on you right now — the repo, README, coverage badge, and 13-competitor analysis are the marketing. The Pro tier is not hypothetical: Natively, the open-source peer, prices "Free personal; Pro via lifetime/yearly" (`competition-analysis.md` row). Open-source does not mean no revenue; it means the paid tier sits *above* a complete free core, never as a repair of a crippled one.

**The wedge competitors cannot match without rebuilding.** The table names the category's two structural tensions: privacy vs convenience — "nearly every commercial product processes audio and runs its AI in the cloud, even when it markets itself as 'local-first' — the local part is usually just audio *capture*" — and opinionated vs open, where most products lock you to one undisclosed transcription engine and one summarization LLM (`competition-analysis.md:14`). ListenToMe's privacy + BYO-model position is defensible not because it is secret but because copying it destroys the incumbent business model: their monthly price *pays for* cloud ASR and cloud LLM compute; genuinely on-device transcription with a bring-your-own local model removes the cost base the subscription is priced on. Granola cannot ship "fully on-device, BYO model" without rebuilding its pipeline *and* its revenue line at once. A durable pricing differentiator is expensive to copy in **business-model terms**, not merely in code terms.

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

(All rows: `course/00-research/03-ai-qe-deep-read.md` §1, §4.) The questionnaire has a cautionary tale: the failed predecessor form was 29 questions with 186 checkbox options and 20–30 minutes to complete — a form that cannot be completed qualifies no one (deep-read §4).

**Sell measurement, not outcomes.** The consultant never promises a savings number: the executive workshop presents questionnaire results as "questions rather than conclusions; no savings number yet" (deep-read §4). The pricing-integrity device is the benefits-realization register: it "ties every claimed saving to a Finance-owned budget row" (deep-read §4) — claims are reconciled by the client's *own* finance function, so an inflated number is not just dishonest, it is checkable. Price what you deliver — the discovery, the baseline, the instrumented pilot — and let outcomes belong to the register.

### Action step

Write one sentence per archetype naming the pricing model for **your** product, who pays, and at which stage they pay — e.g., "one-time $X at download, because my per-user cost is zero," or "per seat, billed when an admin invites the fourth member." Post it to the community. Lab M7 makes you defend it with a table.

## Segment M7.2 — Packaging and platforms (~20 min)

### Objective

Package the offer so the price buys a transformation and a set of artifacts, not video hours; choose platforms from channel economics rather than habit; and compute a cost floor before setting any price.

### Lesson

**Cohort and self-paced are different products.** The same content is two value propositions: the research's rule of thumb is "$97–297 self-paced, or $500–2,000+ as a live 4-week cohort" (`course/00-research/02-course-market-research.md` §C, citing ShopSpace). What the cohort buyer pays for is live instruction, feedback, and peers — Maven's benchmarks price exactly that: 6–8 live hours + 1+ project → $800–1,200; 8–12 hours + multiple projects/capstone → $1,200–1,800; 12–20 hours + multiple projects + capstone → $1,800–2,450 (§C).

**The fraction-of-live-price rule.** Self-paced is priced as a fraction of the live tier: 70–85% *if it keeps projects + async feedback + community* — and if it keeps none of that, the research's verdict is that a bare library "shouldn't be sold at all" (§C). The anti-pattern the rule exists to prevent, verbatim: **"a stack of Zoom recordings is not a self-paced course"** (§C). Price the artifacts and the transformation — the review, the feedback, the objective lab checklists — not the video hours. The rule generalizes to every archetype: a stack of features is not an app tier; a stack of notes is not a briefing. Ask what the buyer can *show* for the money.

**Marketplace vs own platform.** Udemy: 37% payout on marketplace sales (32¢ per dollar in 2025), platform-controlled $9.99 pricing, and no student-email export — "use only as lead-gen/validation, never primary" (§D). Own-platform creators charge $50–200+ against Udemy's effective $10–15 (§C, §D). The course's own platform table — Maven for the cohort, Thinkific/Teachable for self-paced, Gumroad for the lead product, Circle for community, "Never Udemy (primary)" — is the worked decision (`course/04-sales/pricing-and-platforms.md`).

**App store vs direct for Type 1.** MacWhisper is the natural experiment in channel economics: the same product sells at ~€59/$69 one-time on Gumroad and $6.99/mo–$99.99 lifetime on the App Store (`competition-analysis.md` row). The store brings reach and subscription expectations, takes a cut, and owns the customer; direct gives you the margin and the email address. Direct is not a compromise — you already have the machinery from Module 3: signed, notarized, stapled releases published as DMGs targeting the exact commit (`ListenToMe/docs/RELEASING.md`). Choose per product: store for reach, direct for margin and the customer relationship.

**Infra floors for Type 2.** Compute the floor before the price. SignUpFlow's own cost ladder is explicit — "Database: SQLite (dev) / PostgreSQL (prod)" (`SignUpFlow/README.md`, Architecture) — dev at $0, production the first recurring line item — and its paid paths are feature-flagged (M7.1). Do the arithmetic the way the course did: platforms + community + email ≈ $80–130/month, so break-even at the $399 self-paced tier is ~2 sales/month (`course/04-sales/pricing-and-platforms.md`, "Cost floor"). A price below your floor is not a price; it is a subsidy.

**The worked example is this course.** Read `course/04-sales/pricing-and-platforms.md` as the method applied to a real product — this one. The ladder: $0 lead product → **$399** Studio self-paced → **$1,490** Studio Live cohort (founding **$990**) → **$2,500–4,000** team tier. Every rung is defended in both directions with cited evidence. Not cheaper, because marketplace courses priced ≥$950 earn 50–100% more per landing-page visit, and $500–1,500 programs complete at 53–68% vs 18–25% at $97–197 — and completion is this product. Not more expensive yet, because there are no public testimonials: "raising price before social proof exists inverts the trust order" (all: `pricing-and-platforms.md`). And the founding discount is explicitly a *trade*: $990 (34% off) "is explicitly traded for a testimonial + 30-minute feedback interview (agreement at checkout)" — with a launch policy that bans flash-sale pricing that devalues the cohort. Copy the record format, not just the numbers: floor, comparators, bands, launch policy, and a "why not cheaper / why not more expensive" that resists in both directions.

### Action step

Compute your product's monthly cost floor — hosting, API keys, amortized dev time — and write your two-sentence "why not cheaper," citing one benchmark from `course/00-research/02-course-market-research.md`. Post both to the community; you will paste them into the Lab M7 worksheet.

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

- **Price the way your costs recur.** Recurring per-user cloud compute → subscription (Granola ~$14–35/user/mo, Otter ~$8.33–30); on-device → one-time (MacWhisper ~$69); free & open-source positions on the reputation funnel, support, and a Pro tier (Natively: "Free personal; Pro via lifetime/yearly") (`ListenToMe/docs/competition-analysis.md`).
- **Wedges must be expensive to copy in business-model terms** — ListenToMe's privacy + BYO position forces a rival to rebuild its pipeline *and* the subscription economics priced on it.
- **Gate what is not proven; never gate the core.** Billing/SMS routes registered but 404-gated behind `BILLING_ENABLED=false`/`SMS_ENABLED=false`; "core scheduling must not require either paid integration" (`SignUpFlow/AGENTS.md`). Monetize after the workflow is trustworthy.
- **Type 3 sells measurement.** Free evidence site (trust) → questionnaire (fit) → fixed-fee discovery (budget/sponsor) → capped pilot with go/no-go gates (scale) → validation — with a benefits-realization register tying every claimed saving to a Finance-owned budget row.
- **Package the transformation, not the recording.** Cohort vs self-paced are different products ($97–297 vs $500–2,000+); self-paced at 70–85% of live price only with projects + feedback + community retained — "a stack of Zoom recordings is not a self-paced course" (`course/00-research/02-course-market-research.md` §C).
- **Choose platforms by economics.** Udemy: 37% payout, $9.99 platform pricing, no email export — discovery only; own-platform $50–200+; store vs direct is reach vs margin (MacWhisper ~$69 Gumroad vs $6.99/mo–$99.99 lifetime App Store).
- **Honesty converts.** Being more skeptical than your audience is a premium signal: a "what this doesn't prove" section turns "why should I believe you?" into "when can we start?" (`course/00-research/03-ai-qe-deep-read.md` §3).
- **Derive the one-liner from the table.** Adjective-wedge × differentiators × audience; every clause falsifiable against a column.

## Discussion prompt

Post the one claim on your draft sales page you are *least* comfortable defending to a skeptical engineer — then write the "what this doesn't prove" version of it and the source you would attach. Would you publish the qualified version? Reply to one peer: name which of their one-liner clauses their own comparison table would falsify, and which clause survives the deletion test.