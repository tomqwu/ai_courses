# Module 8 — Launch: Sales Page, Email Arc, Capstone
> Part of AI Product Studio (APS-3) · ~75 minutes · Prerequisites: Modules 1–7

## Overview

Modules 1–7 built the machine: the operating system (M1), the three builds (M2–M6), and the monetization plan (M7). Module 8 closes the loop. The sales page and the launch arc turn a shipped product into a sellable one; the capstone ships v1 of one product through the full Spec-to-Ship Loop with recorded evidence, and a 5-minute demo closes the course.

Two sources stand behind every claim: the market research (`00-research/02-course-market-research.md`, §E) supplies the anatomy, the sequence, and the numbers; the course's own sales assets — `04-sales/landing-page.md` and `04-sales/launch-plan.md` — are the worked examples, including how the course handled having no testimonials yet.

By the end of this module you can:

- **Write** a converting sales page in the 8-section evidence-backed anatomy, sourcing every proof claim from artifacts you already own.
- **Run** a 7–10 email launch arc, with the revenue model and deliverability hygiene that make it arrive.
- **Ship** the capstone — one archetype, one shippable scope, the complete loop — scored against the 5-dimension rubric in `01-design/assessment-and-rubrics.md`.

## Segment M8.1 — The sales page (~25 min)

### Objective

Write the 8-section sales-page anatomy for your own product; source every proof claim from an artifact you already own (a repo, an evidence line, a test badge); set the page's length from its price point, not from intuition.

### Lesson

**The anatomy, and why it works.** The eight sections below come from a template distilled across 32,000+ courses and 1.3M enrollments (Ruzuku, cited in `00-research/02-course-market-research.md` §E); restructured onto it, one creator went from 1% to 8% conversion. The page is a *sequence*, not a pile of sections. The course's own page (`04-sales/landing-page.md`) is the worked example — read it alongside this segment and watch each row map:

| # | Section | Its one job | The course's own page |
|---|---|---|---|
| 1 | **Transformation headline** | Sell the destination, not the contents — one falsifiable sentence | "Ship three real AI products. Learn from code that actually shipped." |
| 2 | **Who it's for — and isn't** | Qualify the right buyer; repel the wrong one (cuts refunds, protects completion) | Two explicit lists: "This is for you if…" / "This isn't for you if…" |
| 3 | **Problem & stakes** | Name the gap and the cost of leaving it | "Three things are always missing": the hard 20%, the agent workflow, the part after "it works" |
| 4 | **Curriculum as outcomes** | One ability per module — never a topic list | The Week/Module table; every row reads "You'll leave able to…" |
| 5 | **Instructor bio (100–150 words)** | Relevance + real projects — proof, not autobiography | Tom Wu: three named repos with checkable numbers (96% core coverage; 1,464 dated tests; 116 evidence-cited slides) |
| 6 | **Testimonials** | Borrowed trust, in before/after/result form | Three reserved slots + an honest note (below) |
| 7 | **FAQ** | Answer the *real* objections plainly | Mac? ML? Hours/week? Falling behind? What do I leave with? Refunds? Team? |
| 8 | **Transparent pricing + one CTA** | No price surprises; one action, repeated | Three visible tiers ($399 / $1,490 / from $2,500) and the same enroll CTA at top, middle, and bottom |

Two rows need a second look. Section 4 is where technical pages fail: the course's curriculum table lists abilities ("Engineer a fail-closed local-only mode"), not topics — per-module outcome lines like "Week 3: run an LLM locally — you'll ship a hardened local-only mode" are the standard. Section 8 is a discipline: every tier and price is visible, and exactly one call to action is repeated verbatim wherever it appears — competing CTAs leak the click. Keep the StoryBrand stance from the research (§E): **the student is the hero; you are the guide** — write "you will ship," not "I will teach."

**Per archetype, the sections change jobs — not order:**

| Archetype | Headline sells | Proof leads with | FAQ must answer | Pricing section |
|---|---|---|---|---|
| Type 1 — on-device app | What it does, privately ("run it locally") | Repo badges, coverage, signed release | Platforms, privacy, one-time vs. subscription | One-time price + tier |
| Type 2 — SaaS | The job it does for a team | Tenant-isolation tests, dated evidence line, live demo | Security, data export, seats, uptime | Per-seat tiers |
| Type 3 — expertise | The decision it enables | Provenance table, self-audit, cited slides | Method, sources, what it is *not* | Fixed-fee discovery / capped pilot |

**The testimonials problem — solved honestly.** The course had no students when its page was written, and it invented none. It made two moves (`04-sales/landing-page.md`): it *reserved* three slots labeled "before/after/result format," and it posted the note — "Until then, this section stays honest: no invented social proof. The three repos above are the pre-beta proof." Copy both. A testimonial drafted by the founder is a fabrication — the one disqualifying move under M1's evidence discipline ("never fabricate a status check" covers marketing identically). For a technical audience the research is explicit: real shipped projects *are* the social proof (§E) — the course's badge strip ("ListenToMe · 96% core coverage · MIT", "SignUpFlow · 1,464 tests passing · dated evidence", "AI × QE · 116 evidence-cited slides") carries section 6's weight until real students exist. When they do (the M8.2 beta trade), collect them as before/after/result: *before*, where the buyer was; *after*, what they can now do; *result*, the observable outcome — a link, a number, a shipped artifact.

**Source your proof from M1–M7.** The page's trust load can rest on assets you already built — the same evidence discipline, turned outward:

| Proof asset (you built it in) | Page section it feeds |
|---|---|
| Public repo with tag or deployed URL (M2–M6 labs) | Hero proof line; proof section |
| Dated evidence line — "N passed / M skipped, \<date\>" (M1, M3) | Proof section; bio |
| Coverage number, test badge (M2, M3) | Badge strip; hero |
| Spec folder a buyer can read (M4) | Proof section — technical buyers open it |
| Provenance table, reconciled claims (M6) | Proof section for a Type 3 product |
| Recorded demo (M8 capstone) | Testimonial substitute, pre-beta |
| Pricing rationale with sourced comparators (M7) | Transparent pricing section |

If a claim has no row in that inventory, you have two honest options: build the proof (run the suite, tag the release, record the demo) or state the gap and reserve the slot. The honest-marketing checklist in `04-sales/pricing-and-platforms.md` is the gate: every number carries a source; qualify illustrative vs. observed; state refund and deadline policies plainly.

**Length follows price.** The research guidance (§E): **800–1,200 words under $200; 2,000–3,000 words for $500+ offers or cold traffic.** Stakes are the reason — the more a reader pays and the less they know you, the more questions the page must answer. The course's page runs ~2,250 words for a $399–$1,490 cold-traffic offer, a length check its authoring notes record (`04-sales/landing-page.md`). "Longer pages always convert better" is false in both directions: 2,500 words for a $49 product pads and dilutes; 800 words for a $1,490 cohort leaves the objection teardown unanswered. Set the word target from the price before drafting.

### Action step

Open `04-sales/landing-page.md` beside a blank document and draft your page's eight sections, in order, for the product you priced in Lab M7. Transformation headline first — one falsifiable sentence. Then who it's for/isn't, the problem with its stakes, one outcome line per module, a 100–150-word bio with real projects, testimonials-or-honest-placeholder, the four objections *your* buyer raises, and transparent pricing with one CTA. Tag every claim with its proof artifact (the inventory table is your checklist). Set the word target from your price. This draft becomes capstone artifact 6.

## Segment M8.2 — The launch arc (~25 min)

### Objective

Structure the 7–10 email arc with warmup strictly separated from conversion; explain why the final-48-hours deadline is load-bearing and what makes it honest; compute expected revenue with the five-factor formula; configure deliverability before the first send.

### Lesson

**Two phases, seven emails, four weeks.** The arc comes from the launch research (§E): 7–10 emails over ~4 weeks (full launches can run 10–15 over 10–14 days — Learning Revolution, §E), but the phase structure never changes:

| # | Email | Phase | Its one job |
|---|---|---|---|
| 1 | Origin story | Warmup | Why you built it; the receipts (repos, evidence) |
| 2 | Transformation proof | Warmup | Walk one artifact end-to-end |
| 3 | Free tool | Warmup | Deliver the method in miniature |
| 4 | Cart open | Conversion | The offer: what, mechanics, price, guarantee |
| 5 | Objection teardown | Conversion | The FAQ as answers, not marketing |
| 6 | Testimonial / proof | Conversion | Before/after/result — only if real |
| 7 | Final call | Conversion | Short; the deadline is real |

The phase rule is what people get wrong: **warmup emails do not sell.** They earn the trust the conversion phase spends — the origin story establishes receipts, the transformation proof walks one artifact end-to-end, the free tool proves the method in ten minutes. "All ten emails should sell" is the taught-against misconception: a list asked in every email learns to stop opening, and the final-48-hours pattern below never arrives.

**The course's arc is the worked example** (`04-sales/launch-plan.md` — adapt it, don't admire it). Note the timeline: warmup weeks −4 to −1 with the page in "notify me" mode; cart opens week 0 for 10–14 days; objection teardown at +1; proof at +2 ("only after beta testimonials exist"); the final call in the last 72 hours; a non-buyer survey after. Note the voice rules: one idea per email, one CTA per email, subject lines written for the technical skeptic ("the receipts are public"… "Closes Friday: the cohort that ships" — no emoji). And note the free lead product — the 30-Minute Teardown — that builds the list before the arc runs.

**The final 48 hours — and why the deadline must be real.** In the research, 42–55% of enrollments arrive in the final 48 hours (§E). Deferred decisions collapse at a deadline; that is why the pattern exists — which makes the deadline load-bearing, and its honesty a revenue asset, not just an ethics rule. A countdown that resets, a "last chance" that recurs weekly, trains your list that your deadlines lie — and your *next* launch's final 48 hours underperform. Keep it real: the cart actually closes; the price actually ends. The course's email 7 says "Deadline is real"; its pricing policy commits to "no fake countdowns" (`04-sales/pricing-and-platforms.md`). For real urgency in a first launch, use the beta trade — a founding discount with a stated end date.

**Revenue math: model it before you run it.** The research formula (§E):

> expected revenue = list × open rate × click rate × page conversion × price

Worked example, from the research file: 1,200 × 38% × 15% × 16% × $797 ≈ **$8,767** — 456 opens, ~68 clicks, ~11 enrollments. Sanity-check against the research band (warm lists convert 2–5% overall): the single-chain model is deliberately conservative, because each conversion email is another pass through the funnel. Then hold the course's own evidence discipline: record actuals after the launch (list size, delivery, opens, clicks, conversions by email) and re-derive the next model — `04-sales/launch-plan.md` opens a launch evidence log for exactly this reason ("the course practices what it teaches").

Five levers, five honest moves: **list** — grow it with the free tool and repo READMEs, never purchased lists (they destroy the sender reputation every other lever depends on); **open rate** — skeptic-grade subject lines, list scrubbing, opt-in only; **click rate** — one CTA matched to the email's one idea; **page conversion** — the M8.1 page, which is why the page precedes the arc; **price** — M7's decision, not launch-week panic. Email earns its keep: ROI runs ~$36 per $1 spent (Litmus, §E).

**Deliverability is upstream of every number.** Configure SPF, DKIM, and DMARC on the sending domain *before the first send* — Gmail and Yahoo enforce this for bulk senders (§E). Keep the list opt-in only; scrub hard bounces; test-send to a Gmail and a corporate address before the sequence queues (the launch-plan checklist). No math survives the spam folder: a spam-folder email has an open rate of zero.

**The beta-discount trade.** Where does email 6's testimonial come from before anyone has bought? From the trade the research endorses (Maven's guidance, §C): run cohort one at a discount *explicitly exchanged* for a testimonial and a feedback session — agreement at checkout. The course's founding tier is $990 against $1,490, the trade stated on the page; those testimonials populate the reserved slots and email 6. A discount with a stated trade is honest pricing; a discount with no reason trains buyers to wait — the Udemy $9.99 spiral (§D) is the cautionary tale.

### Action step

Adapt `04-sales/launch-plan.md` to your product. Write all seven emails — subject line, a three-bullet outline, the one CTA — marking each warmup or conversion. Write your deadline and what happens when it passes (the cart closes; the price changes — for real). Compute your revenue model with your actual list size (twenty people is a real number) and your Lab M7 price; name the lever you will invest in first. Run or draft the deliverability checklist for your sending domain. Post your subject lines and your model to the community.

## Segment M8.3 — Capstone: ship and demo (~25 min)

### Objective

Commit to the capstone contract — ONE archetype, ONE shippable scope, the complete loop; map all five rubric dimensions to concrete artifacts before building anything; and rehearse the 5-minute demo structure.

### Lesson

**The contract.** The capstone is not "build something big." It is: pick ONE archetype, define ONE shippable scope, and execute the full Spec-to-Ship Loop — Study → Spec → Build → Validate → Release → Prove (`00-research/00-synthesis.md`) — with recorded evidence. The rubric scores the loop's completeness and the evidence's honesty, not the build's size; the instructor guide's capstone unblock says it exactly: "ONE archetype, ONE shippable scope, the loop complete. The rubric scores the loop, not the size." A complete loop at deliberately small scope out-scores a sprawling half-loop on every dimension — "graded on code size" is the misconception to drop: no rubric dimension counts lines.

**The loop at capstone scale — using what M1–M7 already built.** The capstone extends your labs; it does not restart them:

| Loop stage | You already built this in | The capstone requires |
|---|---|---|
| **Study** | M0 repo tours · M3 competitor table · M6 research log · M7 pricing + positioning | Reuse the M3/M7 artifacts; cite them in the evidence record |
| **Spec** | M1 mini-loop · M4 spec-kit folder | The M4 folder (Type 2) or an equivalent scope spec (Type 1/3) |
| **Build** | M2 TDD core · M5 hardening | Failing-test-first commits; small reviewable changes; core separated from glue |
| **Validate** | M3 contract test + coverage floor · M5 playbook manifest | Tiered tests run *and recorded*, per archetype |
| **Release** | M3 Definition of Done · tags/deploys | A public repo tag with a version, or a deployed page — link verified |
| **Prove** | M6 provenance · M7 honest claims · M8.1/M8.2 assets | The evidence record + sales page + 5-email arc + the demo |

Lab M8 carries the per-archetype scope table — read it before choosing.

**The rubric you will be scored against** (`01-design/assessment-and-rubrics.md`; the full 3/5 table is restated in Lab M8). Five dimensions, 0–5 each, 3 = meets, weighted equally. What "meets" requires:

| # | Dimension | 3 ("meets") |
|---|---|---|
| 1 | **Spec quality** | Complete spec-kit artifacts for the shipped scope; stories independently testable; acceptance criteria concrete |
| 2 | **Build discipline** | TDD evidence (failing test first); small reviewable commits; core separated from glue via protocols/seams |
| 3 | **Evidence honesty** | Validation record with commands, counts, date, limitations; failures included, not hidden |
| 4 | **Privacy/safety engineering** (Type 1/2) or **claim discipline** (Type 3) | Local-only/fail-closed mode, tenant isolation, or a provenance table — implemented and tested |
| 5 | **Launch-readiness** | Positioning one-liner, pricing rationale with sourced comparators, sales page draft, 5-email arc |

Read dimension 4 twice — it is the archetype-dependent one: privacy/safety engineering for Types 1–2, claim discipline for Type 3. **Pass = ≥80% total with no dimension below 3.**

**The evidence record is the required attachment.** Modeled on SignUpFlow's validation format (M1.3), quoted from the rubrics file — use it verbatim:

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

Three blocks are non-negotiable: **commands with results** — the command and its counts, not "tests pass"; **artifact links** — the repo *at a tag*, the spec folder, the evidence log, the sales page draft; and **limitations / not verified** — the honest list, failures included (M3's standard: the gap review that said "don't ship" is worth more than a badge). One honesty clause applies one last time: use agents for everything — the course teaches that — but the record states what the agent did and what you verified. A fabricated result is the only automatic fail.

**The demo.** Five minutes, recorded or live, four beats: **problem (30s)** — whose problem, why now; **loop walkthrough (2 min)** — spec → build → validate → release, one artifact per stage; **live demo (2 min)** — the thing running; **evidence + limits (30s)** — the headline evidence numbers, ending on the not-verified list. The limits beat is where a technical audience decides you are trustworthy. Demo day (cohort, week 8) or the peer exchange (self-paced) closes the course — and doubles as the testimonial engine: the hour that scores you fills your page's reserved slots.

**The loop, closed.** Every stage of the Spec-to-Ship Loop is now something you have *done*, at lab scale, across all three archetypes: studied (M0 repo tours, M3 competitor table, M6 research log), specified (M1 mini-loop, M4 spec-kit), built (M2's TDD core, M5's hardened tests), validated (M3's contract test, M5's playbooks and manifest), released (M3's Definition of Done, tagged and deployed artifacts), and proved (M6's provenance, M8's evidence records and launch assets). That is the course-level outcome, achieved: operate the loop on a real project of your own. The capstone is the loop's first full turn at product scale; what remains is the next turn — your product, your list, your page, shipped.

### Action step

Before you build anything, post your capstone plan for peer review: (1) the archetype and a one-sentence scope; (2) each loop stage mapped to a concrete artifact — name the file, the tag, or the URL; (3) a first-pass self-score against the five dimensions, naming your weakest and what will strengthen it. Review one peer's plan by naming the stage whose artifact is missing or vague. Revise the plan from the replies, then start Lab M8.

## Recap (course-level: the loop, closed)

- **The sales page is a sequence, not a pile.** Eight sections in a proven order — transformation headline → who it's for/isn't → problem & stakes → outcomes per module → instructor bio (100–150 words, real projects) → testimonials (before/after/result) → real-objection FAQ → transparent pricing with one CTA. Restructuring onto this anatomy took one creator from 1% to 8% conversion (research §E). Length follows price: 800–1,200 words under $200; 2,000–3,000 for $500+/cold traffic.
- **Never invent social proof.** The course's own page reserved three slots and pointed at repo badges — for a technical audience, real shipped projects *are* the social proof. Earn testimonials via the beta trade.
- **The launch arc has two phases.** Warmup (origin → proof → free tool) does not sell; conversion (cart open → objections → testimonial → final call) does. 42–55% of enrollments arrive in the final 48 hours, so the deadline is load-bearing — and only a deadline you keep stays load-bearing.
- **Model revenue, then record actuals.** list × open × click × page conversion × price (1,200 × 38% × 15% × 16% × $797 ≈ $8,767); SPF/DKIM/DMARC before the first send (Gmail/Yahoo enforcement); keep a launch evidence log like any other validation record.
- **The capstone is one archetype, one scope, the whole loop** — spec → TDD build → tiered validation → tagged release → evidence record → sales assets → 5-minute demo — scored on five dimensions where 3 = meets and pass = ≥80% with nothing below 3. The rubric scores the loop, not the size.
- **The course outcome is now yours:** every loop stage executed at lab scale in all three archetypes — Study, Spec, Build, Validate, Release, Prove — with the evidence records, pricing package, launch assets, and demo to show for it.

## Discussion prompt

Post the one claim on your draft sales page you are *least* sure you can source — and beside it, the M1–M7 artifact that would make it honest (a test badge, a dated evidence line, a spec folder, the demo video) — or the honest placeholder sentence if no artifact exists yet. Then reply to one peer by naming a proof asset they already own but overlooked. The course's page answered this exact problem with three reserved slots and a badge strip — borrow whichever move fits.