# Lab M7 — Price and position your product

> Lab 7 of 8 · Prerequisites: **Labs M2, M4, and M6 complete** — pick the product you will take to market · Time: ~2 hours · Pass = every checklist item below is objectively verifiable

**Goal.** Turn the product you built in Lab M2, Lab M4, or Lab M6 into a priced, packaged, positioned offer: a sourced pricing table, a decision worksheet, a positioning one-liner, a packaging page, and a self-review that survives a skeptical engineer.

**Where to work.** In your product repo, create `docs/pricing.md` (Steps 1–2, 5) and `docs/positioning.md` (Steps 3–4), or one `docs/monetization.md` with all five steps as sections. Every table cell, price, and claim gets a source pointer — this lab's artifacts feed the Module 8 sales page and capstone demo directly.

## Step 1 — Extend your comparison table into a pricing table

Take the comparison table you built in Lab M3 (or build it now if your product changed) and extend it with pricing columns. Requirements:

- **≥5 competitor rows** — competitors you actually visited, not ones you remember.
- Columns must include: **Price**, **Pricing model** (one-time / per-seat subscription / free + Pro / usage-based), and **What the price buys** (limits, seats, privacy boundaries, support).
- Every price cell carries a **source URL and a retrieval date**. No memory-only pricing.
- Cells you could not confirm from a primary source are qualified "reportedly" or "approximately" — ListenToMe's convention: "where a detail could not be confirmed from a primary source, it is qualified with 'approximately' or 'reportedly'" (`ListenToMe/docs/competition-analysis.md`, header, dated 2026-08). Copy MacWhisper's row style: "Pro ~€59 (~$69) one-time; App Store $6.99/mo–$99.99 lifetime" — model, price, and channel in one cell.

## Step 2 — The pricing decision worksheet

Fill the inline template below. Three inputs make the decision defensible: your **cost floor** (hosting, API keys, amortized dev time — dev at $0 like SignUpFlow's "SQLite (dev) / PostgreSQL (prod)" ladder, production as the first line item, `SignUpFlow/README.md`); your **comparator band** (the min–max of your table's comparable rows); and your **value anchor** (what the product replaces: hours, headcount, or a tool subscription). Then choose model, tiers, launch price — and write a rationale of **≥150 words citing specific table rows**. The worked example to imitate is the course's own record at `course/04-sales/pricing-and-platforms.md`: floor ($80–130/mo → break-even ~2 sales/month), Maven's live-hours bands, and a "why not cheaper / why not more expensive" defended in both directions.

## Step 3 — Positioning one-liner

Write your one-liner in the ListenToMe format — **adjective-wedge × differentiators × audience** — e.g. "the free, open-source, fully on-device meeting copilot for macOS — bring your own model, run it private, and shape it to any conversation" (`ListenToMe/docs/competition-analysis.md:80`). Every clause must be traceable: below the one-liner, list a mapping of clause → table column or repo capability (the M7.3 lesson shows ListenToMe's full mapping). Apply the deletion test: remove any clause and the sentence must become false against a specific row. If no row would notice, the clause is decoration — cut it.

## Step 4 — Packaging page

For each tier, state what is included **and what is deliberately not included, and why**. The honesty pattern is SignUpFlow's: billing and SMS routes are registered under the API but return 404 behind `BILLING_ENABLED=false` / `SMS_ENABLED=false` — "the complete scheduling workflow does not require them" (`SignUpFlow/README.md`, "Provider-backed Features"). An explicit "not included" line per tier is not lost revenue; it is the feature-gating honesty that makes the included list credible. Price artifacts and transformation, not volume — "a stack of Zoom recordings is not a self-paced course" (`course/00-research/02-course-market-research.md` §C).

## Step 5 — Self-review: the skeptical-engineer test

Write the **three toughest objections a buyer would raise from your own table** — the ones your table itself invites (e.g., "MacWhisper is $69 once; why is yours more?", "Otter's free tier does 80% of this"). Answer each with evidence: a table row with its source, or a repo capability with a file pointer. If any answer requires hiding something, revise the price or the page — then re-run the test.

## Worksheet template (paste into `docs/pricing.md`)

```markdown
# Pricing worksheet — <product name>

Cost floor: $____/mo — hosting $____, API keys $____, dev time $____ amortized over ____
Comparator band: $____ (low) to $____ (high) across comparable rows: <list row names>
Value anchor: replaces <hours | headcount | a tool subscription> worth ~$____
Chosen model: <one-time | subscription per seat | free + Pro | usage-based> — because <one line>
Tiers:
  - <name> $____ — included: <…>; NOT included: <…>
  - <name> $____ — included: <…>; NOT included: <…>
Launch price: $____ — founding/early-bird: $____, deadline <date>, the discount is traded for: <testimonial | feedback | …>
Rationale (≥150 words, cite specific table rows): <…>
```

## Acceptance checklist (binary — pass = every box checked)

1. ☐ ≥5 competitor rows; every price cell has a source URL + retrieval date; uncertain cells marked "reportedly/approximately."
2. ☐ Worksheet complete: cost floor, comparator band, value anchor, chosen model, tiers, launch price — each filled, numeric where applicable.
3. ☐ Rationale ≥150 words and cites specific table rows by competitor name.
4. ☐ One-liner's every clause traceable — the clause → column/capability mapping is written out.
5. ☐ Packaging page has an explicit "not included" section per tier, each with a reason.
6. ☐ Three buyer objections from the table, each answered with named evidence (row + source, or file pointer).
7. ☐ The honest-marketing checklist passes: run all five items from `course/04-sales/pricing-and-platforms.md` and quote each pass next to the item (e.g., item 1 "Every number carries a source" → "worksheet floor cites platform prices; table cells cite URLs, retrieved <date>").
8. ☐ Skeptical-engineer verdict recorded in one line: "Would a skeptical engineer pay this?" — yes/no, and which objection almost flipped it.

## Evidence to record

Keep in `docs/` (or paste to the community post): the pricing table with sources; the worksheet + rationale; the one-liner + mapping; the packaging page; the three objections and answers; the checklist run with quotes. Cohort students bring the worksheet to the weekly workshop for review; self-paced students post the launch price + one-liner for one peer reply.

## Stretch (optional, ~30 min)

- **Refund policy + guarantee terms.** Write them plainly — scope, window, what the buyer keeps. Reference shape: "14 days or before Module 3 (cohort), keep materials" (`course/04-sales/pricing-and-platforms.md`). State what counts as abuse and what you would honor anyway.
- **90-second demo script.** One problem, one live path through the product, one artifact produced on screen. This is the demo-day warm-up: Module 8's capstone requires a 5-minute demo, and the 90-second core is the part that must work.

## Discussion prompt

Post your launch price, your one-liner, and the one "not included" line you expect the most pushback on. Reply to one peer: run their one-liner against *their* pricing table — which clause is falsifiable, which is decoration, and which objection from their table they failed to answer?