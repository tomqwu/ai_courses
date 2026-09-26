# Pricing, Packaging & Platform Decisions

> Grounded in the 2025–26 course-market research (`00-research/02-course-market-research.md`). Every number here traces to a cited benchmark. This is the decision record — the "why" behind the prices on the landing page.

## The price ladder

| Tier | Price | What justifies it (per Maven/Ruzuku benchmarks) |
|---|---|---|
| Free lead product — *The 30-Minute AI Product Teardown* | $0 | List-builder; a single repo teardown (ListenToMe recommended: privacy story is the most striking) delivered as a short email course or YouTube video + PDF checklist |
| **Track bundle (self-paced, one archetype)** | **$199** | One of three archetype tracks — On-Device AI Apps, Spec-Driven AI SaaS, or Expertise as a Product — built from 4 modules + a monetization/launch slice, with the same 8-artifact packages. Priced at the same per-module rate as the full course ($199/4.5 modules ≈ $44 vs $399/9 ≈ $44), so the bundle is a fit decision, not a discount. **Deliberately positioned as the smaller buy:** every bundle's `pricing.md` states above the fold that the $399 full course is the better value and offers no upgrade credit. Rationale in `05-tracks/README.md` |
| **Studio (self-paced)** | **$399** | 9 modules, 8 objective-checkpoint labs + capstone, 72 quiz questions, 9 slide decks, community, capstone rubric. Self-paced with projects+community retained should price at a meaningful fraction of the live tier (Maven: 70–85% *with* async feedback; ~27% here reflects no live review). Ruzuku price-vs-completion data: $297–497 band completes at ~38–42% — a floor we want for a hands-on course |
| **Studio Live (cohort)** | **$1,490** (founding: **$990**) | ~16 live hours (8×90-min workshops) + 3 projects + capstone review + demo day → Maven's 12–20-live-hours band = $1,800–2,450; we enter below the band midpoint because the instructor is not yet a recognized name — the founding-cohort discount buys testimonials (Maven's recommended trade) |
| **Team / Enterprise** | **$2,500–4,000** (3–5 seats) | Multi-seat + private code review + private workshop; typical team-tier band from the research |

## Why not cheaper

- Marketplace data: courses priced ≥$950 on professional marketplaces earn 50–100% more per landing-page visit than cheaper ones — price signals quality to professional buyers (Maven).
- Completion economics: $500–1,500 programs complete at 53–68% vs 18–25% at $97–197 (Ruzuku). This course's entire value proposition is *shipping*; completion is the product.
- Creators undercharge by 2–5× (pricing-coach consensus via Ruzuku); the honest anchor here is the alternative: an engineer who ships one sellable product from the capstone recovers the cohort price many times over.

## Why not more expensive (yet)

- No public testimonials yet (beta cohort runs first); raising price before social proof exists inverts the trust order.
- The instructor's proof assets (three repos) are strong but pre-revenue as a course business. Founding cohort at $990 → collect testimonials → hold $1,490 → revisit $1,800+ for cohort #3 if demand supports it (that's the top of Maven's band).

## Launch-price policy

- Founding cohort: $990 (34% off) — the discount is *explicitly traded* for a testimonial + 30-minute feedback interview (agreement at checkout).
- Early-bird for self-paced in launch week: $299 (25% off), 72 hours, deadline stated plainly (42–55% of enrollments arrive in the final 48 hours — the deadline is load-bearing).
- Never run flash-sale pricing that devalues the cohort (Udemy's $9.99 pattern is the cautionary tale: it trains buyers to wait).

## Platform decisions

| Need | Choice | Why (research) | Runner-up |
|---|---|---|---|
| Cohort product | **Maven** | Cohort-native marketplace for professional/technical audiences; $500–3,000 price points; built-in discovery; per-course pricing, no subscription | Thinkific (if self-managing all marketing) |
| Self-paced product | **Thinkific** (or Teachable) | Solid sales pages/payments; design customization; no marketplace margin pressure | Teachable (avoid its 5% Basic-tier fee) |
| Community | **Circle** (or Discord) | Community-first; lesson-level discussion prompts are the +14-point completion lever; free-form build logs | Discord (free, developer-native, less structured) |
| Lead product | **Gumroad** | Near-zero setup, ~10% fee, fine for a $0–29 PDF/email mini-product | Podia (if consolidating later) |
| Email | ConvertKit/MailerLite-class | Needed for the 7–10 email launch arc; SPF/DKIM/DMARC required by Gmail/Yahoo | — |
| **Never** | Udemy (primary) | 37% marketplace payout (32¢/dollar 2025), platform-controlled $9.99 pricing, no email export | Use only as optional discovery/lead-gen later |

### Cost floor (month-1, lean)

Maven (per-course fee on enrollment) + Thinkific ~$54/mo or Gumroad-only start + Circle ~$49/mo or Discord $0 + email ~$29/mo ≈ **$80–130/mo + per-enrollment fees**. Break-even at Studio tier: ~2 sales/month covers fixed costs.

## Packaging details

- **What's in every tier:** the 3 case-study repos (public, students clone them), all lesson text (searchable — developers expect text they can grep), lab starters (TinyCopilot reference implementation), templates (constitution/AGENTS/spec-kit/coverage manifest/evidence log), quizzes with keys.
- **Cohort-only:** live workshops, code review on Labs M1/M2(or M4)/M5, capstone review, demo day, cohort channel.
- **Team-only:** private workshop, team code review, a team capstone review call.
- **The "not a course" rule:** a bare recording library is never sold alone (research: "a stack of Zoom recordings is not a self-paced course"). If self-paced is sold, it ships with community + objective lab checklists.
- **Money-back guarantee:** 14 days or before Module 3 (cohort), keep materials. Generous refunds are a conversion asset for trust-sensitive technical buyers; the capstone-based value makes abuse rare.

## Revenue model (launch, conservative)

Assumptions from research: warm list 800 subscribers (built via the free teardown + repo READMEs + relevant communities), 38% open, 12% click, 12% page conversion at $990 founding cohort → ~4–6 founding students → **$4,000–6,000**; launch-week self-paced early bird adds ~8–12 at $299 → **$2,400–3,600**. Cohort #2 at $1,490 with testimonials + 20% list growth → **$9,000–15,000**. These are plans, not promises — record actuals after each launch and re-derive (the course's own evidence discipline applied to its business).

## The honest-marketing checklist (applies to every asset)

1. Every number on any sales asset carries a source (repo file or cited research).
2. Qualify what's illustrative vs. observed (AI × QE's rule: "planning inputs are not observed client results").
3. Never invent testimonials; ship beta before claiming social proof.
4. State refund and deadline policies plainly; no fake countdowns.
5. Price the transformation and the artifacts (review, feedback, community) — not the video hours.

## Decision record — 2026-09-17 (platform review)

The September 2026 review (`../00-research/04-platform-review-2026.md` §5.3, with the market table in
`../00-research/06-competitive-landscape-2026.md`) placed this ladder against the bands observed that
month: single tracks at $169–199 for indie products, subscription libraries clustering at $199–399 a
year, Maven cohorts averaging ~$500 with a $750–950 mid band and a $2,200–5,000 top band held by
instructors with published research and alumni.

Decisions recorded, not yet acted on where marked:

1. **Founding cohort stays at $990.** It sits at the top of the observed mid band, which is where a
   first cohort with three public repos and no alumni belongs.
2. **$1,490 is held, not raised, and it is gated:** it applies from cohort #2 only once twenty named
   testimonials with artifact links exist. Until then the sales page shows $1,490 as the list price
   and $990 as the founding price, which is the same trade the ladder always stated.
3. **A mid tier is proposed, not launched:** $2,000–2,500 with office hours and a course-specific
   assistant, the shape the $5,000 evals course sells. Revisit after cohort #1's actuals
   (issue #67).
4. **A dated update window replaces "lifetime updates"** on every surface: editions through
   September 2027, with `CHANGELOG.md` linked from the page. Buyers of technical courses screen for
   "last updated"; a window is a promise that can be checked.
5. **The proof section leads with the gate**, not the coverage badge: pointers resolved, facts
   re-derived, lab runs, the narration contract — the numbers the build printed.
6. **EU minimums** are stated on the page (withdrawal right, consent-to-immediate-access) and the
   checkout will be handled by a merchant of record (issue #35), which also settles VAT at the
   customer's location for recorded and live tiers.

These are the review's recommendations recorded as decisions; the price changes in (3) wait for
evidence, as this file's own "why not more expensive (yet)" section requires.
