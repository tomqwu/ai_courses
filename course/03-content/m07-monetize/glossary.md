# Glossary — M7: Monetize

Alphabetical. Each term: definition, then where it lives (repo pointer or course file).

**Adjective-wedge.** The leading adjectives of a positioning one-liner that carry the differentiator —
the part a competitor would have to rebuild to match. Lives in the derived one-liner at
`ListenToMe/docs/competition-analysis.md:80`.

**Benefits-realization register.** The pricing-integrity device that ties every claimed saving to a
Finance-owned budget row, so claims are reconciled by the client's own finance function rather than
by the seller. Lives in `course/00-research/03-ai-qe-deep-read.md` §4.

**Capped phased pilot.** The bounded engagement stage: 8–10 weeks, five phases (0–4), go/no-go gates
signed by the sponsor, frozen acceptance criteria before results are observed. Lives in
`ai_qe/_data/engagement.json` and `ai_qe/docs/method/phased-pilot.md`.

**Comparator band.** The min–max price range of the rows in your own table that are genuinely
comparable to your product. Lives in `lab.md` Step 2 (the worksheet template).

**Cost floor.** Your fixed monthly cost — hosting, API keys, amortized dev time — converted to the
sales per month needed to break even. Lives in `course/04-sales/pricing-and-platforms.md`, "Cost floor."

**Deletion test.** Remove one clause from a positioning one-liner; if no row in your table would
notice the sentence became false, the clause is decoration and gets cut. Lives in `lesson.md` M7.3.

**Feature gating.** Registering paid routes in the codebase but returning 404 behind a flag until the
workflow they depend on is trustworthy. Lives in `SignUpFlow/README.md`, "Provider-backed Features,"
and `SignUpFlow/AGENTS.md`.

**Fixed-fee discovery.** A bounded first paid engagement that qualifies budget and sponsor before any
larger commitment. Lives in `ai_qe/_data/engagement.json` (commercial field).

**Fraction-of-live-price rule.** Self-paced prices at 70–85% of the live tier only if projects, async
feedback, and community are retained; otherwise a bare library should not be sold at all. Lives in
`course/00-research/02-course-market-research.md` §C.

**Honest-marketing checklist.** Five rules every sales asset must pass: sourced numbers, qualified
claims, no invented testimonials, plain refund/deadline policies, price the transformation. Lives in
`course/04-sales/pricing-and-platforms.md`.

**One-time pricing.** Charging once because per-user marginal cost does not recur — the on-device
pattern. Exemplified by the MacWhisper row, `ListenToMe/docs/competition-analysis.md`.

**Per-seat pricing.** Pricing a SaaS by seat so the unit of price scales with the organization's
adoption. Lives in `lesson.md` M7.1, grounded in `SignUpFlow/README.md`'s invitation flow.

**Positioning one-liner.** A single sentence in the form adjective-wedge × differentiators × audience,
derived clause by clause from a comparison table. Lives in `lesson.md` M7.3.

**Qualified claim.** A claim that carries both its source and its limitation, so a buyer can audit it.
Lives in `course/00-research/03-ai-qe-deep-read.md` §3 ("planning inputs are not observed client results").

**Reputation funnel.** The marketing surface a free or open-source product runs on: code, README,
coverage badge, published competitor analysis, support, and a Pro tier. Lives in
`course/01-design/curriculum.md`, M7.1.

**Sales-page anatomy.** The eight-section structure: transformation headline, who it's for/isn't,
problem and stakes, per-module outcomes, instructor proof, testimonials, FAQ, transparent pricing with
one CTA. Lives in `course/00-research/02-course-market-research.md` §E.

**Skeptical-engineer test.** Lab M7 Step 5: the three toughest objections your own table invites, each
answered with a named row or a repo pointer. Lives in `lab.md` Step 5.

**Value anchor.** What your product replaces — hours, headcount, or a tool subscription — expressed as
a comparable amount. Lives in `lab.md` Step 2.

## Terms people get wrong

- **Price vs. cost floor.** A price is what you ask; the floor is the break-even arithmetic underneath
  it. A price below the floor is a subsidy, whatever the comparator band says.
- **Feature gating vs. gating the core.** Gating defers a *paid path* that is not proven; gating the
  core makes the essential workflow stop until you pay. `SignUpFlow/AGENTS.md` bans the second.
- **Qualified claim vs. hedged claim.** A qualified claim names its source and its limitation; a hedge
  ("results may vary") names neither and buys no trust.
- **Free tier vs. free-and-open positioning.** A free tier is a limit on a paid product; free-and-open
  is a $0 price with a business model attached. ListenToMe is the second; Natively's row shows both.
- **Comparator band vs. cheapest sticker price.** The band spans comparable rows; the cheapest sticker
  in the category is usually a different product with a different cost structure.

## Curated resources

1. `ListenToMe/docs/competition-analysis.md` — the 12-row table and the clause-by-clause one-liner;
   read it as the format for your own table.
2. `SignUpFlow/README.md` ("Provider-backed Features") + `SignUpFlow/AGENTS.md` — the gating pattern
   and the rule that the core must not depend on paid paths.
3. `ai_qe/_data/engagement.json` + `ai_qe/docs/method/phased-pilot.md` — the staged funnel and its
   sponsor-signed gates; the shape of a bounded expertise offer.
4. `ai_qe/docs/method/discovery-questionnaire.md` — the lead-qualification asset, including the
   post-mortem of a form nobody could finish.
5. `course/00-research/02-course-market-research.md` §C–§E — price bands, platform economics, and the
   eight-section page anatomy.
6. `course/04-sales/pricing-and-platforms.md` — this course's own decision record; copy its format
   (floor, ladder, why-not-cheaper, why-not-more, launch policy).
7. `course/00-research/03-ai-qe-deep-read.md` §1, §3, §4 — why qualified claims convert, and how
   measurement is priced.
8. `ai_qe/docs/economics/slide-language.md` — the wording that may and may not appear on a slide; the
   strictest version of claim discipline in the case studies.
