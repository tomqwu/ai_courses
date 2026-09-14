# Track Bundles

Three standalone, sellable single-track courses, each carved out of the full studio course for a buyer
who knows which archetype they need. The full course covers all three and remains the recommended path —
each bundle says so plainly in its `pricing.md` rather than pretending to be the better deal.

| Bundle | Promise | Built from | Price |
|---|---|---|---|
| [**On-Device AI Apps**](on-device-app/) | Ship a local-first AI app whose privacy claims are enforced in code and proven by tests | M0, M1, M2, M3 + a monetization/launch slice | $199 |
| [**Spec-Driven AI SaaS**](spec-driven-saas/) | A spec folder that survives a stranger test, and acceptance evidence that survives a skeptical auditor | M0, M1, M4, M5 + a monetization/launch slice | $199 |
| [**Expertise as a Product**](expertise-product/) | Every published claim carries a date, sample, method, unit and level — and the funnel sells a measurement, not a promise | M0, M1, M6 + a monetization/launch slice | $199 |

Full studio course: **$399** self-paced · **$1,490** cohort — see
[`../04-sales/pricing-and-platforms.md`](../04-sales/pricing-and-platforms.md).

## What every bundle contains

Each bundle folder ships five files, and reuses the parent course's module artifacts rather than
duplicating them:

| File | Purpose |
|---|---|
| `README.md` | Promise, audience, prerequisites, what's included, 6-week map, honest scope note, FAQ |
| `syllabus.md` | 6-week schedule: weekly outcome, segments, lab, quiz, time budget, assessment |
| `sales-page.md` | The 8-section anatomy taught in M8, with proof assets for that archetype only |
| `pricing.md` | Price, rationale, and the explicit non-cannibalization statement |
| `bundle-map.md` | Module → segments → labs → artifacts included/excluded, so the buyer knows exactly what they get |

## Why bundles exist at all

Three reasons, in the order that matters:

1. **Fit.** A backend engineer building a multi-tenant SaaS does not need Swift, ScreenCaptureKit, or
   on-device ASR — they need the spec pipeline and the tenant-isolation evidence gate. Bundling by
   archetype removes weeks of irrelevant work.
2. **A cheap first purchase.** $199 is a much smaller commitment than $399, and the bundle's `pricing.md`
   states that upgrading to the full course costs the difference — so the ladder rewards the cautious buyer
   instead of punishing them.
3. **A different proof.** Each bundle leads with the case study that archetype cares about: ListenToMe for
   on-device, SignUpFlow for SaaS, ai_qe for expertise. Same method, different evidence.

## Honest limitations

- The bundles are **not** independent courses with their own labs written from scratch. They sequence and
  frame the parent course's modules for one archetype, and reuse its lesson/lab/quiz artifacts. Each
  `bundle-map.md` states this explicitly.
- No bundle has student testimonials, because the course has none yet. Each sales page uses the reserved-slot
  pattern rather than a fabricated quote (see [`../04-sales/launch-plan.md`](../04-sales/launch-plan.md)).
- A bundle buyer does not get the other two archetypes. That is the point of the bundle, and the reason the
  full course is positioned as the better value.
