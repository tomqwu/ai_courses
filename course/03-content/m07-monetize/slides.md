---
marp: true
theme: aps
paginate: true
title: M7 — Monetize: Pricing, Packaging, Positioning
---

<!-- _class: lead -->

# M7 — Monetize: Pricing, Packaging, Positioning

**AI Product Studio (APS-3)** · ~60 minutes · Prerequisites: Modules 1–6

Price it, package it, position it — from evidence.

<!-- NOTES: Welcome to M7. In M1–M6 you built three working product cores; today you price them. Say the promise plainly: by the end of this module you will have chosen a pricing model per archetype from a sourced table, computed a cost floor, and written a positioning line a skeptical engineer can falsify. Timing for the module: roughly 60 minutes of lesson, about 20 per segment. Transition: we start with the one decision rule that removes the guesswork. -->

---

## By the end you can…

- **Price** each archetype from competitive evidence
- **Compute** a cost floor before setting a price
- **Package** transformation and artifacts, not video hours
- **Choose** platforms by channel economics, deliberately
- **Derive** a falsifiable positioning one-liner
- **Survive** the skeptical-engineer review

<!-- NOTES: Read these as the six graded outcomes, not aspirations. Lab M7 asks for all six artifacts: a sourced pricing table, a decision worksheet, a one-liner with a clause-to-column mapping, a packaging page with explicit exclusions, three answered buyer objections, and the honest-marketing checklist run. Quiz M7 checks the same objectives. Timing: 1 minute here. Transition: the first rule is the load-bearing one — price the way your costs recur. -->

---

## M7.1 — Price the way your costs recur

- Cloud per-user compute recurs monthly
- That cost makes a subscription honest
- On-device compute recurs zero times per user
- Then a subscription is a tax users audit
- The table shows the pattern, not a style
- Evidence first, then the model

<!-- NOTES: This is the segment's thesis. Every monthly-priced tool in the category runs per-user compute in the cloud; every one-time-priced tool runs inference on the user's machine. Say the one-line rule aloud: if your per-user costs recur monthly, price monthly; if they do not, a subscription is a tax your users can audit you against. The next slide opens the file where that pattern is recorded. Timing: 2 minutes. Transition: open the competitor table. -->

---

<!-- _class: proof -->

## The competitor table is your raw material

- `ListenToMe/docs/competition-analysis.md`
- 12 competitor rows, dated 2026-08
- Unconfirmed details marked "approximately" or "reportedly"
- Price column carries model, price, and channel
- Commercial tiers run about $8–149/mo
- Read rows, never headlines

```markdown
# Competition Analysis

_Last updated: 2026-08. All pricing and feature facts are stated as of 2026;
where a detail could not be confirmed from a primary source, it is qualified
with "approximately" or "reportedly."_
```

<!-- NOTES: Put the file on screen. Note the header convention: every price fact is stated as of 2026, and where a detail could not be confirmed from a primary source it is qualified "approximately" or "reportedly." That convention is the honesty mechanism you copy in Lab M7 Step 1 — every price cell gets a source URL and a retrieval date, and unconfirmed cells get the qualifier. Point at the twelve rows; this is not a summary, it is evidence you can audit. Timing: 3 minutes. Transition: now read the Price column against each row's cost structure. -->

---

## Recurring compute sets the model

| Tool | Cost structure | Price |
|---|---|---|
| Granola | Cloud ASR + cloud LLM | Free; ~$14–35/user/mo |
| Otter.ai | Own ASR + Claude insights | Free; ~$8.33–30/user/mo |
| Fireflies.ai | Cloud ASR + cloud AI | Free; ~$10–39/seat/mo |
| MacWhisper | Whisper on-device | Free; ~€59 (~$69) once |

<!-- NOTES: Walk the four rows. Granola and Otter both spend per user per month on cloud transcription and cloud summarization, so their monthly price is a pass-through of a recurring cost. MacWhisper runs Whisper on-device, so its marginal cost per user is near zero and it charges once. The pattern is structural: the pricing model tracks who pays the compute. All four rows are from `ListenToMe/docs/competition-analysis.md`. Timing: 4 minutes. Transition: free is also a price, with a business model attached. -->

---

## Free and open-source is a price

- ListenToMe prices at $0, MIT-licensed
- "Code open for inspection" against $8–149/mo rivals
- Free still has a business model attached
- Paying surfaces: reputation funnel, support, Pro tier
- Peer evidence: Natively "Free personal; Pro via lifetime/yearly"
- Paid tier sits above a complete free core

<!-- NOTES: A $0 price is a decision, not an absence of one. The course syllabus names the paying surfaces for an open-source product: the reputation funnel, support, and a Pro tier — see `course/01-design/curriculum.md`, M7.1. The open-source peer Natively is the existence proof: its row in `ListenToMe/docs/competition-analysis.md` reads "Free personal; Pro via lifetime/yearly." State the rule: the paid tier sits above a complete free core, never as a repair of a deliberately crippled one. Timing: 3 minutes. Transition: why this position is defensible. -->

---

## The wedge rivals cannot copy cheaply

- Category tension one: privacy versus convenience
- "Local-first" usually means local capture only
- Category tension two: opinionated versus open
- Rivals lock one engine, one undisclosed LLM
- Copying privacy + BYO destroys their cost base
- Durable wedges are expensive in business-model terms

<!-- NOTES: Read the tension paragraph near the top of `ListenToMe/docs/competition-analysis.md`: nearly every commercial product processes audio and runs its AI in the cloud, even when it markets itself as local-first; the local part is usually just audio capture. The second tension is opinionated versus open — most products lock you to one undisclosed transcription engine and one summarization LLM. Say why the wedge holds: their monthly price pays for the cloud compute that the wedge removes. Copying it means rebuilding the pipeline and the revenue line at once. Timing: 3 minutes. Transition: Type 2 prices differently. -->

---

<!-- _class: proof -->

## Type 2: gate what is not proven

- `SignUpFlow/README.md`, "Provider-backed Features"
- Billing under `/api/v1`, SMS under `/api/sms`
- Both return 404 behind `BILLING_ENABLED=false`
- `SMS_ENABLED=false` gates the second path
- "The complete scheduling workflow does not require them"
- `SignUpFlow/AGENTS.md`: core must not require paid paths

<!-- NOTES: Open the README section and read the sentence verbatim: billing routes remain in the codebase under `/api/v1`, and SMS routes under `/api/sms`, but both return 404 by default behind those two flags; paid billing and SMS are deferred, and the complete scheduling workflow does not require them. Then open `SignUpFlow/AGENTS.md` line 18: "core scheduling must not require either paid integration." This bars two failure modes: charging for a path that is not trustworthy yet, and gating the core workflow to force upgrades. Timing: 3 minutes. Transition: how a SaaS grows into its billing event. -->

---

## Invitation growth produces the billing event

- Public signup is rejected for existing orgs
- New members join through administrator invitations
- `/auth/signup` creates org plus first admin atomically
- Token-based onboarding, no email required
- The admin who invites is the buyer
- Make the growth loop emit the billing event

<!-- NOTES: The README's onboarding section says existing organizations reject public signup and every later member is added through an administrator-created invitation; `/auth/signup` creates the org and its first admin atomically, and later members join by token. That makes growth and billing the same event: every new member is an invited org member, so per-seat pricing tracks real adoption, and the person who invites is the person who pays. Read the exact passages in `SignUpFlow/README.md`. Timing: 3 minutes. Transition: Type 3 sells measurement. -->

---

<!-- _class: proof -->

## The funnel that sells measurement

| Stage | Qualifies |
|---|---|
| Free evidence site | Trust |
| Questionnaire | Fit and scope |
| Fixed-fee discovery | Budget and sponsor |
| Capped phased pilot | Whether to scale |
| Validation | Renewal, on evidence |

Pointer: `ai_qe/_data/engagement.json`; `ai_qe/index.md`; `ai_qe/discovery.md`

<!-- NOTES: The AI × QE funnel is visible in its own files, not in a pitch deck. `ai_qe/index.md` routes the visitor through four path cards ending at `/discovery/` — "Start with one workflow. Agree what better means." — which ends in a questionnaire download. `ai_qe/_data/engagement.json` records the staged timeline: 2 weeks sponsor alignment, 4–6 weeks baseline and readiness, 8–10 weeks capped pilot, 1–2 quarters limited validation. Its commercial field says: "fixed-fee or capped discovery; separately capped pilot... No client price or start date has been agreed." Timing: 4 minutes. Transition: what a consultancy should actually price. -->

---

## Sell measurement, not outcomes

- The workshop presents "questions rather than conclusions"
- "No savings number yet" — deliberate
- A benefits-realization register ties each saving
- Every claimed saving maps to a Finance-owned budget row
- Claims are checkable by the client's own finance function
- **Action step:** one sentence per archetype, who pays, when

<!-- NOTES: The consultancy never promises a savings number. The executive workshop shows questionnaire results as questions rather than conclusions, with no savings number yet, and the pricing-integrity device is the benefits-realization register: it ties every claimed saving to a Finance-owned budget row, so an inflated number is checkable by the client's own finance function. Price what you deliver — discovery, baseline, instrumented pilot — and let outcomes belong to the register. All from `course/00-research/03-ai-qe-deep-read.md` §4. Then give the action step. Timing: 3 minutes. Transition: segment two, packaging and platforms. -->

---

## Action step — M7.1

- Write one sentence **per archetype**
- Name the model, who pays, when they pay
- Example: "one-time $X at download, per-user cost is zero"
- Example: "per seat, billed when an admin invites"
- Post the three sentences to the community
- Lab M7 makes you defend them with a table

<!-- NOTES: This is the two-minute action step that closes segment one: one sentence per archetype naming the pricing model for your product, who pays, and at which stage they pay. Give both worked shapes aloud — a one-time price justified by a zero marginal cost, and a per-seat price billed at the moment an admin invites another member. Tell them Lab M7 will make them defend the sentence with a sourced table and a cost floor, so the sentence is a claim, not a preference. Timing: 2 minutes. Transition: packaging is where the same content becomes two products. -->

---

## M7.2 — Cohort and self-paced are different products

- Same content, two value propositions
- Rule of thumb: $97–297 self-paced
- Live 4-week cohort: $500–2,000+
- Maven: 8–12 live hours + projects → $1,200–1,800
- Maven: 12–20 live hours + capstone → $1,800–2,450
- The cohort buyer pays for live feedback and peers

<!-- NOTES: Source is `course/00-research/02-course-market-research.md` §C, citing ShopSpace and Maven's published benchmarks. The point to make: these are not the same product at two prices; they are two value propositions. The cohort buyer pays for live instruction, peer interaction, and feedback — which is exactly what Maven's live-hour bands price. Say the bands slowly, because students will use them as a comparator in Lab M7. Timing: 3 minutes. Transition: the rule that connects the two prices. -->

---

<!-- _class: proof -->

## The fraction-of-live-price rule

- Self-paced = 70–85% of live price
- Only if projects + async feedback + community stay
- Strip all three and the research verdict is blunt
- "A stack of Zoom recordings is not a self-paced course"
- Source: `course/00-research/02-course-market-research.md` §C
- Ask what the buyer can show for the money

```markdown
- Self-paced should be priced as a fraction of the live cohort price: 70–85%
  if it keeps projects + async feedback/office hours + community; a bare video
  library shouldn't be sold at all ("a stack of Zoom recordings is not a
  self-paced course").
```

<!-- NOTES: Read the rule exactly: self-paced should be priced as a fraction of the live cohort price, 70–85%, if it keeps projects plus async feedback or office hours plus community; a bare video library shouldn't be sold at all. The research's own phrasing is "a stack of Zoom recordings is not a self-paced course" — quote it. Then generalize it: a stack of features is not an app tier, and a stack of notes is not a briefing. The question that tests any package is: what can the buyer show for the money? Timing: 4 minutes. Transition: where you sell changes what you keep. -->

---

## Marketplace vs own platform

- Udemy: 37% marketplace payout
- 32 cents per dollar marketplace-wide in 2025
- Platform controls pricing, $9.99 flash sales
- No student-email export — no customer relationship
- Own-platform creators charge $50–200+
- Marketplace is discovery and validation, never primary

<!-- NOTES: Source: `course/00-research/02-course-market-research.md` §D, with the own-platform figure in §C. The decision is not about reach alone; it is about margin and the customer list. At 37% payout with platform-controlled $9.99 pricing and no email export, the marketplace keeps the relationship as well as the money. Use it to validate demand and as optional discovery. The course's own platform table is the worked decision — see `course/04-sales/pricing-and-platforms.md`. Timing: 3 minutes. Transition: the same reach-versus-margin split appears for apps. -->

---

## Store vs direct is reach vs margin

- MacWhisper sells on two channels at once
- Gumroad: ~€59 (~$69) one-time
- App Store: $6.99/mo to $99.99 lifetime
- Store brings reach, takes a cut, owns the customer
- Direct gives margin and the email address
- Direct machinery: `ListenToMe/docs/RELEASING.md`

<!-- NOTES: MacWhisper is the natural experiment: one row in `ListenToMe/docs/competition-analysis.md` carries both channels — "Pro ~€59 (~$69) one-time; App Store $6.99/mo–$99.99 lifetime." The store adds subscription expectations and subtracts margin and ownership; direct keeps both. Direct is not a compromise for a small team — the release machinery already exists: signed, notarized, stapled releases targeting an exact commit, documented in `ListenToMe/docs/RELEASING.md`. Choose per product: store for reach, direct for margin. Timing: 3 minutes. Transition: before any price, do the arithmetic. -->

---

<!-- _class: proof -->

## Compute the floor before the price

- Source: `course/04-sales/pricing-and-platforms.md`, "Cost floor"
- Maven per-course fee + Thinkific ~$54/mo
- Circle ~$49/mo or Discord $0 + email ~$29/mo
- Fixed cost: ≈ $80–130/mo plus per-enrollment fees
- Break-even at the $399 tier: ~2 sales/month
- A price below your floor is a subsidy

```markdown
### Cost floor (month-1, lean)

Maven (per-course fee on enrollment) + Thinkific ~$54/mo or Gumroad-only
start + Circle ~$49/mo or Discord $0 + email ~$29/mo ≈ $80–130/mo
+ per-enrollment fees. Break-even at Studio tier: ~2 sales/month covers
fixed costs.
```

<!-- NOTES: This is the course's own arithmetic, recorded in `course/04-sales/pricing-and-platforms.md` under cost floor. Walk the lines: course-platform fee, community ~$49/mo or zero on Discord, email ~$29/mo, giving roughly $80–130/month in fixed cost plus per-enrollment fees; at the $399 self-paced tier that is about two sales a month to break even. The transferable move is the order: floor, then comparator band, then value anchor, then price. SignUpFlow's SQLite-in-dev, PostgreSQL-in-prod ladder is the same discipline for a SaaS. Timing: 4 minutes. Transition: the course is the worked example. -->

---

## The worked example is this course

- $0 lead product → **$399** self-paced
- **$1,490** cohort, founding **$990**
- **$2,500–4,000** team tier, 3–5 seats
- Why not cheaper: ≥$950 courses earn 50–100% more
- Why not more: no public testimonials yet
- Founding discount trades for a testimonial and interview

<!-- NOTES: Read `course/04-sales/pricing-and-platforms.md` as the method applied to a real product — this one. Each rung is defended in both directions. Not cheaper: marketplace courses priced at $950 or more earn 50–100% more per landing-page visit, and $500–1,500 programs complete at 53–68% versus 18–25% at $97–197. Not more expensive yet: no public testimonials exist, and raising price before social proof inverts the trust order. The $990 founding price is explicitly traded for a testimonial and a 30-minute feedback interview. Timing: 4 minutes. Transition: the second action step. -->

---

## Action step — M7.2

- Compute your monthly cost floor
- Hosting + API keys + amortized dev time
- Write your two-sentence "why not cheaper"
- Cite one benchmark from the market research
- Post both to the community
- Paste both into the Lab M7 worksheet

<!-- NOTES: Two artifacts, both short. First, the floor: hosting, API keys, amortized dev time — dev counts as zero only if it truly is, the way SignUpFlow's SQLite-in-dev line is zero. Second, the two-sentence "why not cheaper," citing one benchmark from `course/00-research/02-course-market-research.md`. Tell them these two paste directly into the Lab M7 worksheet, so the post is not busywork. Timing: 2 minutes. Transition: segment three — honest marketing that converts. -->

---

## M7.3 — The hero is the buyer

- StoryBrand: the student is the hero, you are the guide
- Every page section answers the buyer's question
- "Does this get me there, and can I trust you?"
- For technical audiences, shipped projects ARE social proof
- Repos, demos, dated evidence lines, test badges
- Never invent a testimonial

<!-- NOTES: Source: `course/00-research/02-course-market-research.md` §E. The reframe is grammatical: the buyer is the subject of every sentence, and you are the guide who has already walked the path. For a technical audience the proof assets are concrete — the repos, the demos, the dated evidence lines, the test badges you have been recording since Module 1. Say the course's own rule from `course/04-sales/pricing-and-platforms.md`: never invent testimonials; ship beta before claiming social proof. Timing: 3 minutes. Transition: the page skeleton. -->

---

## Sales-page anatomy: eight sections

<!-- _diagram: steps -->

1. Transformation headline — the outcome
2. Who it's for — and who it isn't
3. Problem and stakes
4. Outcomes per module
5. Instructor proof, 100–150 words
6. Testimonials, before/after/result
7. FAQ — real objections
8. Transparent pricing, one CTA

<!-- NOTES: This is the research's template, drawn from 32,000-plus courses; the research also records that a restructure along these lines took one creator from 1% to 8% conversion. Length scales with price: 800–1,200 words under $200; 2,000–3,000 words for $500-plus or cold traffic. Today you draft the skeleton and actually write sections one, two, and five. Module 8 turns the skeleton into the full page. All from `course/00-research/02-course-market-research.md` §E. Timing: 3 minutes. Transition: the counterintuitive part — skepticism sells. -->

---

<!-- _class: proof -->

## Skepticism converts

- AI × QE publishes "the only independent RCT is negative"
- Signature qualifier: "planning inputs are not observed client results"
- The observed effect: the executive's question changes
- "why should I believe you?" becomes "when can we start?"
- Qualified claims with sources are a premium signal
- You audited yourself harder than the buyer would

<!-- NOTES: This is the strongest evidence in the module and it comes from a real product's own files: `course/00-research/03-ai-qe-deep-read.md` §1 and §3. The site publishes a negative independent RCT on its own decks and stamps planning numbers with the qualifier that they are not observed client results. The deep-read records the effect: an executive who reads that stops asking why they should believe you and starts asking when they can start. Mechanism: the cheapest objection — belief — is removed, leaving only start date. Timing: 4 minutes. Transition: how to derive a line that earns that trust. -->

---

<!-- _class: proof -->

## Derive the one-liner from the table

> "ListenToMe is the free, open-source, fully on-device meeting copilot for macOS — bring your own model, run it private, and shape it to any conversation." (`ListenToMe/docs/competition-analysis.md:80`)

| Clause | Column that proves it |
|---|---|
| free | Price — nothing else free-and-open |
| open-source | Privacy/AI — closed rivals |
| fully on-device | On-device? — only MacWhisper, Natively |
| bring your own model | Multi-model/BYO — most read "no picker" |
| run it private | Privacy — local Ollama, no audio leaves |
| shape it to any conversation | Focus — 18 presets vs one vertical |

<!-- NOTES: Emphasize that this sentence was derived, not composed — Module 3.3 built it clause by clause from the comparison table. That is what makes it falsifiable instead of mood music. Apply the deletion test out loud: remove a clause and the sentence must become false against a specific row; if no row would notice, the clause is decoration and gets cut. Then give the action step: the eight-section skeleton with sections one, two, and five actually drafted, plus the one "what this doesn't do" line you would publish. Timing: 4 minutes. Transition: the lab turns this into a package. -->

---

## Action step — M7.3

- Draft the eight-section skeleton
- Write sections 1, 2, 5 for real
- Cite an artifact you actually have
- Add one "what this doesn't do" line
- Post the headline and the limitation
- Module 8 builds the full page

<!-- NOTES: Insist on "for real" for sections one, two, and five: a transformation headline, who it is and is not for, and instructor proof citing an artifact that exists — a repo, a test run, a dated evidence line. The honest-limitation line is the one that earns the rest of the page its credibility, so write it even when it stings. Post the headline and the limitation to the community for peer review. Module 8 turns the skeleton into the full sales page. Timing: 3 minutes. Transition: the lab. -->

---

## Lab M7 — Price and position your product

- Goal: priced, packaged, positioned offer

<!-- _diagram: steps -->

- sourced pricing table, ≥5 rows
- decision worksheet, rationale ≥150 words
- one-liner plus clause mapping
- packaging page with exclusions
- three objections, answered

**Pass gate:** every checklist item objectively verifiable.

<!-- NOTES: Two hours, in your product repo under `docs/pricing.md` and `docs/positioning.md`, or one `docs/monetization.md`. Say the pass gate: every one of the eight acceptance-checklist boxes is objectively verifiable, and the artifacts feed the Module 8 sales page and capstone directly. Warn them about the two most common failures — prices recalled from memory instead of retrieved, and a subscription attached to a product with no recurring per-user cost. Timing: 2 minutes. Transition: the quiz. -->

---

## Quiz M7 — what it checks

- Six multiple choice, two short answer
- Costs recur → model matches
- Gate what is not proven
- Funnel order and what each stage qualifies
- Fraction-of-live-price rule
- One-liner format and honest limitations

**6/8 to pass.** Source: `quiz.md`, answer key included.

<!-- NOTES: The quiz is open-book in spirit: every answer is traceable to a file pointer in the key. Questions one and two cover pricing models and flag-gating; three and four the expertise funnel and measurement pricing; five and six packaging and platform economics; seven and eight ask you to write a one-liner and choose a first-tier price with a comparator rule. Six of eight passes, consistent with the module standard. Timing: 1 minute. Transition: recap. -->

---

## Recap

- Price the way your costs recur
- Wedges must be costly in business-model terms
- Gate the unproven; never gate the core
- Sell measurement, let outcomes belong to the register
- Package the transformation, not the recording
- Derive the one-liner; qualify every number

<!-- NOTES: Compress the module to six lines and point back at the pointers students should already have open: `ListenToMe/docs/competition-analysis.md`, `SignUpFlow/README.md`, `ai_qe/_data/engagement.json`, `course/00-research/02-course-market-research.md`, and `course/04-sales/pricing-and-platforms.md`. If a student remembers one thing, make it the first line and the last: the model tracks the cost structure, and every number carries a source. Timing: 2 minutes. Transition: the discussion prompt. -->

---

## Discussion prompt

- Post the claim you least want to defend
- Write its "what this doesn't prove" version
- Name the source you would attach
- Would you publish the qualified version?
- Reply to one peer's one-liner
- Name the clause their own table would falsify

<!-- NOTES: This closes the module and seeds Lab M7 Step 5. The prompt is deliberately uncomfortable: name the claim on your draft page you are least comfortable defending to a skeptical engineer, then write the qualified version and the source. Ask them to answer whether they would publish it, and why. In peer replies, they must name one clause in a peer's one-liner that the peer's own table would falsify and one that survives the deletion test. Timing: 3 minutes. Transition: close the session and hand out the lab. -->
