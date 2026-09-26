# Solutions — Lab M7: Price and position your product

> This is an **open-ended lab**. The "reference answer" is a worked exemplar you grade *against*,
> not a target: grade the structure and the sourcing, not the student's numbers. Every exemplar
> figure traces to a repo file, the course research, the course's decision record, or a named
> assumption. The student's own floor and tiers must be their own arithmetic.

## Step 1 — Sourced pricing table

**Reference answer.** ≥5 rows the student actually visited; columns **Tool | Pricing model | Price |
What the price buys | Source URL | Retrieved**. The exemplar is the shape to imitate — model, price,
and channel in one cell, per `ListenToMe/docs/competition-analysis.md` header (dated 2026-09):

| Tool | Model | Price | What it buys | Source | Retrieved |
|---|---|---|---|---|---|
| Granola | per-user/mo | Free; Business ~$14/user/mo; Enterprise ~$35/user/mo | cloud ASR + cloud LLM, templates | `competition-analysis.md` row | 2026-09 |
| Otter.ai | per-user/mo | Free (300 min/mo); Pro ~$8.33–16.99; Business ~$20–30 | proprietary ASR, cloud LLM insights | same | 2026-09 |
| MacWhisper | one-time + store | Pro ~€59 (~$69) one-time; App Store $6.99/mo–$99.99 lifetime | on-device Whisper, BYO keys | same | 2026-09 |
| Natively | free + Pro | Free personal; Pro via lifetime/yearly | on-device STT, local RAG | same | 2026-09 |
| ListenToMe | free & open-source | $0, MIT | full on-device copilot, BYO model | same | 2026-09 |

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

Filled exemplar: TinyCopilot as a Mac app, arithmetic as in the M7.2 lesson.

```markdown
# Pricing worksheet — TinyCopilot Pro
Inputs: 20 meetings/user/mo (assumption); per meeting 30 answers × 1,800 tokens + 1 recap ×
  26,000 (windows: ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:582-586; 4 chars/token
  assumed); rate $0.005 per 1,000 tokens (assumption — replace with a dated rate card)
Fixed floor: $361.58/mo = developer membership $8.25 + hosting $20 + build 160 h × $50 ÷ 24
Inference-cost line: 20 × 80,000 ÷ 1,000 × $0.005 = $8.00 per user-month
  who pays: on-device → user's hardware; BYOK → customer's key; private cloud → platform
  quota (Mac/iOS, while eligible); Cloud tier → me, capped at 1.6M tokens
Payment fee: 5% + $0.50 (merchant of record, 05-platform-build-options-2026.md §2)
Contribution: Pro $69 − $3.95 = $65.05; Cloud $12 − $1.10 − $8.00 = $2.90 at the cap
Break-even: $361.58 ÷ $65.05 = 5.6 → 6 Pro sales/month (one covers the $28.25 cash lines)
Comparator band: $0 (ListenToMe, MIT) to ~$69 one-time (MacWhisper Pro); subscriptions above it:
  Granola ~$14–35/user/mo, Otter ~$8.33–30/user/mo.
Value anchor: replaces a ~$14–35/user/mo cloud notetaker = ~$168–420/user/year avoided.
Chosen model: free + one-time Pro with a BYOK discount, plus a capped Cloud add-on — because
  the only recurring per-user cost is the Cloud tier's $8.00 line.
Tiers:
  - Free — included: on-device transcription and answers; NOT included: BYOK, presets.
  - Pro $69 once — included: everything on-device, BYOK, 18 presets, exports; NOT included:
    cloud sync (no server to sync to).
  - Cloud $12/mo — included: 1.6M managed tokens a month; NOT included: overage (falls back
    to on-device, because each extra meeting costs $0.40).
Launch price: $69, no founding discount — the comparator IS the anchor.
Rationale (≥150 words): <student writes; must name rows>
```

For a Type 2 product the exemplar is the lesson's SaaS floor: $60 cash, $0.30 inference per
organisation, $26.42 Starter contribution, 3 Starter organisations for cash, 28 with build time.

**Rationale exemplar (the part students most often fake).** *MacWhisper charges ~€59 (~$69) once
because Whisper runs on-device; Granola and Otter charge ~$8.33–35/user/mo because they pay for
cloud or proprietary ASR plus cloud LLM per meeting (rows in `competition-analysis.md`). My marginal
cost per user is zero on-device and under BYOK, so a monthly price there would be a recurring charge
for non-recurring cost — the exact audit a buyer can run. I therefore enter at the one-time anchor,
$69, inside the band MacWhisper established, and keep the free tier complete rather than crippled,
matching Natively's "Free personal; Pro via lifetime/yearly" posture. Only the Cloud tier's $8.00
line recurs, so only Cloud is monthly: $12, capped, inside Otter's Pro band. I am not undercutting
to $0: ListenToMe is MIT and occupies $0, so my only defensible $0-plus claim is convenience, which
the Pro tier prices.*

**Verify.** Recompute: 30 × 1,800 + 26,000 = 80,000; × 20 = 1.6M; × $0.005 per 1,000 =
$8.00; $361.58 ÷ $65.05 = 5.56. `wc -w` on the rationale block → ≥150; `grep -o 'Granola\|Otter\|MacWhisper\|Natively' docs/pricing.md | sort -u | wc -l` → ≥3 named rows.

**Common wrong answers.** (1) Floor written as a feeling ("cheap to run") with no dollars. (2) A
subscription bolted onto a product with no recurring per-user cost. (3) An inference line with no
inputs, or BYOK called free without saying the customer pays. (4) A cloud tier priced under its own inference line, or with no cap. (5) Rationale naming no
row, or tiers with no "NOT included" line.

**Grading note.** Ask: "which table row and which cost line made you choose this model?" A pass
names both, and its break-even reproduces from its own inputs; a plausible fake answers with a vibe.

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
the honesty pattern of `SignUpFlow/README.md` "Provider-backed Features" (billing and SMS return 404
behind flags) and `SignUpFlow/AGENTS.md`: "core scheduling must not require either paid
integration." Price artifacts and transformation, not volume or video hours
(`course/00-research/02-course-market-research.md` §C).

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

A memory-only competitor price (fabricated evidence); a subscription on a product whose own table
shows no recurring per-user cost; an unfalsifiable one-liner, which leaves the deletion test nothing
to break.

## Self-check table

| Criterion | Self-verification |
|---|---|
| ≥5 visited competitors | Each row has a URL you can open now |
| Every price dated | `grep -c '2026' docs/pricing.md` ≥ row count |
| Uncertain cells qualified | `grep 'reportedly\|approximately'` |
| Floor reproduces | Recompute break-even from your stated inputs; it matches |
| Inference line | Calls × tokens ÷ 1,000 × rate shown, or "$0 — no model calls" |
| Rationale ≥150 words | `wc -w` on the rationale block |
| Clause mapping complete | One mapping line per clause |
| Exclusion per tier | One "NOT included — because" line per tier |
| Three objections answered | Each answer names a row or pointer |
| Checklist run quoted | 5 honest-marketing items, each with a quoted pass |
