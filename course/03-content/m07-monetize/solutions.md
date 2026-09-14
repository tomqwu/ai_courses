# Solutions — Lab M7: Price and position your product

> This is an **open-ended lab**. The "reference answer" is a worked exemplar you grade *against*,
> not a target: grade the structure and the sourcing, not the student's numbers. Every exemplar
> figure traces to `ListenToMe/docs/competition-analysis.md`, the course research, or this course's
> decision record. The student's own floor and tiers must be their own arithmetic.

## Step 1 — Sourced pricing table

**Reference answer.** ≥5 rows the student actually visited; columns **Tool | Pricing model | Price |
What the price buys | Source URL | Retrieved**. The exemplar is the shape to imitate — model, price,
and channel in one cell, per `ListenToMe/docs/competition-analysis.md` header (dated 2026-08):

| Tool | Model | Price | What it buys | Source | Retrieved |
|---|---|---|---|---|---|
| Granola | per-user/mo | Free; Business ~$14/user/mo; Enterprise ~$35/user/mo | cloud ASR + cloud LLM, templates | `competition-analysis.md` row | 2026-08 |
| Otter.ai | per-user/mo | Free (300 min/mo); Pro ~$8.33–16.99; Business ~$20–30 | proprietary ASR, Claude insights | same | 2026-08 |
| MacWhisper | one-time + store | Pro ~€59 (~$69) one-time; App Store $6.99/mo–$99.99 lifetime | on-device Whisper, BYO keys | same | 2026-08 |
| Natively | free + Pro | Free personal; Pro via lifetime/yearly | on-device STT, local RAG | same | 2026-08 |
| ListenToMe | free & open-source | $0, MIT | full on-device copilot, BYO model | same | 2026-08 |

**Verify.** `grep -c '^| ' docs/pricing.md` → expect ≥7 (header + separator + ≥5 rows);
`grep -c 'http' docs/pricing.md` → at least one URL per price cell; `grep -c 'reportedly\|approximately' docs/pricing.md` → ≥1 if any cell is unconfirmed.

**Common wrong answers.** (1) *Memory-only prices* — "Granola is around $10" with no URL and no date:
fails the checklist, and signals the student summarized instead of retrieving. (2) *Qualifier
dropped* — copying "reportedly Whisper-based" or "~$14" as an unhedged fact: misrepresents the
source's own uncertainty convention. (3) *Missing "what the price buys"* — a price with no limits,
seats, or privacy boundary cannot anchor your own tier. (4) *Rows for tools never opened*.

**Grading note.** Spot-check one URL and one qualifier against the cited source; a table where no
cell carries a date is a rewrite, not a retrieval.

## Step 2 — Worked decision worksheet (Type 1, on-device app)

Filled exemplar for a TinyCopilot-class macOS app that runs inference locally:

```markdown
# Pricing worksheet — <on-device app>
Cost floor: $0/mo marginal compute per user (inference runs on the user's Mac);
  recurring lines are dev time amortized + release/notarization overhead — state both in dollars.
  Reference shape for a completed floor: course 04-sales/pricing-and-platforms.md → ~$80–130/mo
  fixed, break-even ~2 sales/month at the $399 tier.
Comparator band: $0 (ListenToMe, MIT) to ~$69 one-time (MacWhisper Pro); subscriptions above it:
  Granola ~$14–35/user/mo, Otter ~$8.33–30/user/mo.
Value anchor: replaces a ~$14–35/user/mo cloud notetaker = ~$168–420/user/year of avoided subscription.
Chosen model: free + one-time Pro — because per-user costs do not recur (On-device? column = Yes).
Tiers:
  - Free — included: on-device transcription, BYO local model; NOT included: multi-pane, presets.
  - Pro ~$69 one-time — included: everything, 18 presets, exports; NOT included: cloud sync
    (no server to sync to — a subscription would pay for infrastructure we deliberately do not run).
Launch price: $69, no founding discount — the comparator IS the anchor.
Rationale (≥150 words): <student writes; must name rows>
```

**Rationale exemplar (the part students most often fake).** *MacWhisper charges ~€59 (~$69) once
because Whisper runs on-device; Granola and Otter charge ~$8.33–35/user/mo because they pay
Deepgram/AssemblyAI or run proprietary ASR plus cloud LLM per meeting (rows in
`competition-analysis.md`). My marginal cost per user is zero, so a monthly price would be a
recurring charge for non-recurring cost — the exact audit a buyer can run. I therefore enter at the
one-time anchor, $69, inside the band MacWhisper established, and keep the free tier complete rather
than crippled, matching Natively's "Free personal; Pro via lifetime/yearly" posture. I am not
undercutting to $0: ListenToMe is MIT and occupies $0, so my only defensible $0-plus claim is
convenience, which the Pro tier prices.*

**Verify.** `wc -w` on the rationale block → ≥150; `grep -o 'Granola\|Otter\|MacWhisper\|Natively' docs/pricing.md | sort -u | wc -l` → ≥3 named rows.

**Common wrong answers.** (1) Floor written as a feeling ("cheap to run") with no dollars. (2) A
subscription bolted onto a product with no recurring per-user cost. (3) Rationale naming no row.
(4) Tiers that are feature lists with no "NOT included" line.

**Grading note.** Ask one question: "which table row made you choose this model?" A pass answers with
a row and a cost structure; a plausible fake answers with a market vibe.

## Step 3 — Worked positioning one-liner

Exemplar (the Quiz M7 model answer, extended): *"the free, open-source, fully offline release-notes
copilot for small teams — bring your own repo, keep your history private, draft notes in one
command."* Calibration: ListenToMe's live version at `ListenToMe/docs/competition-analysis.md:80`.

| Clause | Column / capability that proves it |
|---|---|
| free | Price — competitors charge per seat |
| open-source | License column — rivals closed |
| fully offline | On-device? — cloud rivals answer No |
| for small teams | Audience — pricing unit is a seat/org |
| bring your own repo | BYO capability — model/provider picker |
| keep your history private | Privacy — local storage, no upload |
| draft notes in one command | Workflow — single CLI entry point |

**Deletion test.** Remove "keeps your history private": a row answering *No (cloud)* no longer
contradicts the sentence — the clause is doing work, keep it.

**Common wrong answers.** "The best AI tool for developers" (unfalsifiable); clauses with no column;
a feature list where the audience is missing.

**Grading note.** Run the deletion test yourself, clause by clause; every clause must break against a
row or it is decoration.

## Step 4 — Packaging page

**Reference answer.** Per tier: included *and* deliberately excluded, each exclusion with a reason —
the honesty pattern of `SignUpFlow/README.md` "Provider-backed Features" (billing/SMS routes return
404 behind `BILLING_ENABLED=false`/`SMS_ENABLED=false`; "the complete scheduling workflow does not
require them") and `SignUpFlow/AGENTS.md`: "core scheduling must not require either paid
integration." Price artifacts and transformation, not volume — "a stack of Zoom recordings is not a
self-paced course" (`course/00-research/02-course-market-research.md` §C).

**Common wrong answers.** Exclusions with no reason ("not included: support" — why?); gating the core
workflow; pricing by video hours.

**Grading note.** An exclusion without a reason is a Missing cell, not a Proficient one.

## Step 5 — Skeptical-engineer review

**Reference answer.** Three objections *the student's own table invites*, each answered with a named
row + source or a repo capability + pointer. Exemplar: "MacWhisper is $69 once — why is yours more?"
→ answered by the cost floor and the value anchor, or the price is cut. "Otter's free tier does 80%
of this" → answered by the on-device/privacy column, or the page is revised.

**Common wrong answers.** Objections nobody would raise (softballs); answers that are adjectives; an
answer that requires hiding a limitation.

**Grading note.** The verdict line must name which objection almost flipped it; "no objection was
close" is a red flag.

## Three failures that fail the lab outright

1. **A memory-only competitor price** — no URL, no retrieval date, no qualifier: fabricated evidence.
2. **A subscription bolted onto a product with no recurring per-user cost** — the model contradicts
   the student's own table's On-device/Cost columns.
3. **An unfalsifiable positioning line** ("the best AI tool") — no clause maps to a column, so the
   deletion test cannot even be run.

## Self-check table

| Criterion | Self-verification |
|---|---|
| ≥5 visited competitors | Each row has a URL you can open now |
| Every price dated | `grep -c '2026' docs/pricing.md` ≥ row count |
| Uncertain cells qualified | `grep 'reportedly\|approximately'` |
| Floor in dollars | The floor line contains a `$` figure |
| Rationale ≥150 words | `wc -w` on the rationale block |
| Clause mapping complete | One mapping line per clause |
| Exclusion per tier | One "NOT included — because" line per tier |
| Three objections answered | Each answer names a row or pointer |
| Checklist run quoted | 5 honest-marketing items, each with a quoted pass |
