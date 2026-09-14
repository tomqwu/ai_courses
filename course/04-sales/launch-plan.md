# Launch Plan & Email Arc

> Evidence-based launch plan per the 2025–26 research: 7–10 emails over ~4 weeks; warmup (no selling) → conversion arc; 42–55% of enrollments arrive in the final 48 hours; email ROI ~$36:1. Deliverability prerequisites: SPF, DKIM, DMARC configured before the first send; list is opt-in only.

## Timeline (cohort launch)

| Week | Phase | What happens |
|---|---|---|
| −4 to −1 | Warmup | 3 emails (below) + free teardown ships + landing page live in "notify me" mode |
| 0 | Cart opens | Email 4 (cart open); 10–14 day open-cart window |
| +1 | Objection handling | Email 5 (FAQ teardown) |
| +2 | Proof | Email 6 (testimonial/beta results) — only after beta testimonials exist |
| Final 72h | Deadline | Email 7 (final call, deadline real) → cart closes |
| +3 | Post-launch | Non-buyer survey; onboard cohort; collect beta feedback; begin evergreen loop |

## The free lead product (list-builder)

**The 30-Minute AI Product Teardown** — one email course (3 emails) or a single video + PDF walking a real repo (ListenToMe): what "on-device, private, BYO-model" costs in engineering, how a local-only mode fails closed, and the 10-minute exercise (run the SignUpFlow solver / pull a model). Delivers the course's core credibility move in miniature: every claim has a file pointer. Distribution: Gumroad ($0 with email capture), repo READMEs (where license/etiquette allows), relevant communities, conference/meetup talks.

## The emails

> Voice: the student is the hero; the instructor is the guide. One idea per email, one CTA. Subject lines written for the technical skeptic — no emoji, no "🚀".

**Email 1 (week −4) — The origin story.**
Subject: `How one engineer shipped three AI products (the receipts are public)`
Body: the three repos and what each proves (96% coverage; 1,464 dated tests; 116 cited slides). The turn: "AI agents didn't make this easier — they made discipline mandatory." CTA: subscribe to the teardown / reply with which archetype you'd build.

**Email 2 (week −3) — The transformation proof.**
Subject: `What "shipped" looks like: specs, tests, evidence`
Body: walk one artifact end-to-end (a spec folder, a coverage badge, a provenance table) and what it means for a hiring manager or a customer. CTA: download the teardown.

**Email 3 (week −2) — The free tool.**
Subject: `A 10-minute exercise that beats a weekend tutorial`
Body: deliver the teardown's mini-lab (clone SignUpFlow, run the solver, capture the health score; pull qwen3 and get a completion). "If this took you 10 minutes, imagine Module 0." CTA: join the notify list; cohort dates announced next week.

**Email 4 (week 0) — Cart open.**
Subject: `AI Product Studio is open (8 weeks, 3 real products)`
Body: the transformation promise, the three archetypes with what you build in each, cohort mechanics (weekly workshops, code review, demo day), founding price $990 (trade: testimonial + feedback), the guarantee. CTA: enroll.

**Email 5 (week +1) — Objection teardown.**
Subject: `"I'll fall behind" — and 6 other honest answers`
Body: FAQ as answers, not marketing: time (4–6 h/wk), falling behind (lifetime + one free cohort repeat), level (intermediate, no ML needed), Mac (not required), "other courses failed me" (labs pass or fail objectively — you can't drift), refunds (before Module 3), team options. CTA: enroll.

**Email 6 (week +2) — Proof.**
Subject: `What the founding cohort built`
Body: only if real: 2–3 student artifacts with before/after/result format (a TinyCopilot repo, a spec folder, a briefing), beta testimonial quotes, demo-day screenshots. If testimonials aren't ready, this email ships a teaching sample instead (a full lesson: Module 1's best segment free). CTA: enroll.

**Email 7 (final 72h) — Final call.**
Subject: `Closes Friday: the cohort that ships`
Body: short. What you leave with (three builds, evidence, sales assets). Deadline is real (cart closes; founding price ends). The honest close: "If you don't ship in 8 weeks with this structure, ask for your money back before Module 3." CTA: enroll.

**Post-launch (non-buyers):** one survey email (what stopped you — price/time/level), one "materials waitlist" for self-paced switchers.

## Launch-day operations checklist

- [ ] SPF/DKIM/DMARC verified (send test to Gmail + a corporate address)
- [ ] Landing page: mobile-checked, CTA fires the right tier's checkout, testimonials honest-or-absent
- [ ] Checkout tested with a live card + a refund dry-run (both tiers)
- [ ] Calendar holds for 8 workshops + demo day; Zoom/Streamyard links tested
- [ ] Community space seeded: welcome post, M0 discussion prompt, intro thread
- [ ] Email sequences queued with correct merge fields; deadline date correct everywhere
- [ ] Evidence file opened for the launch itself (list size, opens, clicks, conversions by email — the course practices what it teaches)

## Metrics to record (the launch evidence log)

List size → delivery rate → open rate (target ≥38%) → click rate (≥12%) → page conversion (≥12% warm) → enrollments by tier → refund rate (≤5%) → completion stats at week 4 and 8. Compare against the revenue model in `pricing-and-platforms.md`; record deviations honestly and re-derive the next launch's model.

## Evergreen loop (post-cohort)

1. Self-paced tier always-on at $399 (Gumroad/Thinkific).
2. Cohorts 2–3× per year; founding discount only for cohort #1; price steps $990 → $1,490 → ($1,800+ if demand holds).
3. Content engine: one repo-teardown post/video monthly (each is a mini sales letter with receipts).
4. Team pipeline: the cohort's enterprise inquiries feed the Team tier.
5. Udemy-style marketplaces: optional, later, as discovery only — never the core funnel.