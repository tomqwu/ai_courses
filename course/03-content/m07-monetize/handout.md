# Handout M7 — Monetize: Pricing, Packaging, Positioning

**Mental model in one sentence.** Price the way your costs recur, package the transformation the
buyer can show, and derive every claim from a row you can point at.

## Decision table — pick the model from the cost structure

| Archetype | Cost structure | Model | Who pays / when |
|---|---|---|---|
| Type 1 on-device app | No recurring per-user compute | Free core + one-time Pro (or $0 + reputation funnel, support, Pro) | User, at download |
| Type 2 SaaS | Recurring hosting + data + per-seat services | Per-seat tiers; paid paths flagged off until proven | Org admin, when a member is invited |
| Type 3 expertise | Recurring time, zero marginal distribution | Staged funnel: free site → questionnaire → fixed-fee discovery → capped pilot → validation | Sponsor, per bounded stage |

Rule for all three: a price below your cost floor is not a price, it is a subsidy.

## The five moves worth keeping

1. **Floor first.** Fixed monthly cost ÷ (price − per-sale fees) = break-even sales/month.
   Course reference: ≈$80–130/mo → ~2 sales/month at $399 (`course/04-sales/pricing-and-platforms.md`).
2. **Source every price cell.** URL + retrieval date; unconfirmed cells say "approximately" or
   "reportedly" — the convention in `ListenToMe/docs/competition-analysis.md`, header.
3. **Fraction-of-live price.** Self-paced = 70–85% of live *only* with projects + feedback +
   community; otherwise it "shouldn't be sold at all" (`course/00-research/02-course-market-research.md` §C).
4. **Gate what is not proven.** Registered-but-404 routes (`BILLING_ENABLED=false`, `SMS_ENABLED=false`);
   "core scheduling must not require either paid integration" (`SignUpFlow/AGENTS.md`).
5. **One-liner = adjective-wedge × differentiators × audience.** Every clause maps to a column; run
   the deletion test (`ListenToMe/docs/competition-analysis.md:80`).

## Worksheet template (paste into `docs/pricing.md`)

```markdown
Cost floor: $__/mo — hosting $__, API keys $__, dev time $__ amortized
Comparator band: $__ (low) to $__ (high) — rows: <names>
Value anchor: replaces <hours|headcount|subscription> worth ~$__
Chosen model: <one-time|per-seat|free+Pro|usage> — because <one line>
Tiers: <name> $__ — included: <…>; NOT included: <…> — because <…>
Launch price: $__ — founding $__, deadline <date>, traded for <testimonial|feedback>
Rationale ≥150 words, citing specific table rows: <…>
```

## Pointers to open

- `ListenToMe/docs/competition-analysis.md` — 12-row price table and the one-liner (line 80).
- `ListenToMe/docs/RELEASING.md` — the direct-channel machinery (signed, notarized, stapled).
- `SignUpFlow/README.md` — "Provider-backed Features"; `SignUpFlow/AGENTS.md` — the gating rule.
- `ai_qe/_data/engagement.json` — the staged engagement; `ai_qe/index.md` and `ai_qe/discovery.md` — the funnel.
- `ai_qe/docs/method/phased-pilot.md` — pilot gates; `ai_qe/docs/method/discovery-questionnaire.md` — the qualifying form.
- `course/00-research/02-course-market-research.md` §C–§E — price bands, platforms, page anatomy.
- `course/04-sales/pricing-and-platforms.md` — the worked record: floor, ladder, honest-marketing checklist.
- `course/00-research/03-ai-qe-deep-read.md` §1, §3, §4 — measurement pricing and qualified claims.

## Three gotchas

1. **Memory-only pricing.** A price without a URL and a date is fabricated evidence — the one automatic fail.
2. **Subscription without recurring cost.** If your table's cost column says on-device, a monthly price is a charge your buyer can audit.
3. **Unfalsifiable positioning.** "The best AI tool" cannot be broken by deleting a clause; if no row would notice, the line sells nothing.

## You're done when…

- [ ] ≥5 competitor rows, every price cell with URL + retrieval date, uncertain cells qualified.
- [ ] Worksheet complete and numeric: floor, comparator band, value anchor, model, tiers, launch price.
- [ ] Rationale ≥150 words naming specific competitor rows.
- [ ] One-liner with a clause → column/capability mapping; deletion test passed.
- [ ] Packaging page with an explicit "NOT included — because" line per tier.
- [ ] Three buyer objections from your own table, each answered with a named row or file pointer.
- [ ] Honest-marketing checklist run with each of the five passes quoted.
- [ ] Verdict recorded: "Would a skeptical engineer pay this?" — and which objection almost flipped it.
