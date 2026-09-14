# Quiz M6 — The Expertise Product: Evidence, Routing, Editions
> Part of AI Product Studio (APS-3) · 8 questions (6 MC + 2 short answer) · Answer key included

**Q1.** Which fields must a benchmark record carry before its number may appear on a slide?

A. The source's name and a working link — a successful HTTP response is evidence the claim is correct.
B. Date, sample, method, unit, self-reported vs measured, sponsor, and what claim the record can support; anything unverifiable is listed as such.
C. The finding and the publisher's summary; if the number is impressive, a self-reported vendor figure can headline.
D. A SHA-256 hash; wording is the author's judgment.

**Q2.** Your executive route currently ends on the "transformation vision" slide. What does the case study's routing rule require, and why?

A. "Focused routes end on a decision discussion; full decks retain the supporting material" — a bounded, fundable ask is decidable; "transform QA" is not.
B. One big deck suits everyone — routes are unnecessary if the deck is well organized.
C. End wherever the strongest number appears, so the meeting closes on impact.
D. Routes exist for PDF export only; the live deck plays in full order.

**Q3.** Which questionnaire design follows `docs/method/discovery-questionnaire.md`?

A. Multi-select on the outcome question, with a "balanced combination" option for nuance.
B. One form, role-routed at the first question; single-select on the questions that define success; gap-free ranges with an "unknown" option.
C. Separate 15-question forms per role, so no route exceeds 10 minutes.
D. Financial questions deferred until after the pilot, since budget ownership is Finance's business.

**Q4.** v1.24.1 fixed subtitle rendering; slides, audio and PDFs did not change. What does correct edition discipline look like?

A. Bump the site `version`, retain `slide_edition` at 1.24.0, record in the changelog that the v1.24.0 PDF editions "remain unchanged" — and never overwrite the published 1.24.0 release.
B. Editions are versioning theater; just deploy, since content is unchanged.
C. Bump every edition field together so they never drift.
D. Republish over the old release so no one downloads stale PDFs.

**Q5.** A pilot's net-effort point estimate is 12% (go ≥15%, stop <10%) with a confidence interval of 9–17%. What does the protocol require?

A. Go — the point estimate sits in the review band, which rounds up.
B. Extend until the interval excludes the boundary.
C. Insufficient evidence for that boundary — a CI crossing 10% or 15% is insufficient "even if its point estimate appears favorable" — so take the one bounded extension or hold, per the frozen rules.
D. Relabel the result as a quality win, since effort came in ambiguous.

**Q6.** AI × QE publishes its own 14-finding site audit and remediation table on the live site. What is the commercial logic?

A. Audits are only for big companies with compliance departments.
B. Self-audits should stay internal; publishing findings gives buyers free ammunition.
C. Publish only clean results — an audit that finds nothing proves credibility.
D. Finding → response → verification tables make the site demonstrably harder on itself than any buyer would be, converting skepticism into trust: "why should I believe you?" becomes "when can we start?"

**Q7.** For each claim, give its level (task-level efficiency / released capacity / hard-dollar saving / total-spend impact — or illustrative) and the slide wording it permits:

1. "Peng et al.: 55.8% faster (95 freelancers, one synthetic task, vendor-affiliated)."
2. "Organizations report 10–15% average gains, rarely monetized (Bain, self-reported)."
3. "Our Banking Client: 3.3% capacity released → 0.45% net cash per $10M."

**Q8.** "Sell measurement, not outcomes." Explain what the phased pilot asks the sponsor to fund, what the benefits-realization register adds, and why this closes deals that outcome promises cannot.

---

## Answer key

**Q1 — B.** The conventions require the full record, and unverifiable items go on an explicit "not verified" list; the link check explicitly does *not* treat a working HTTP response as evidence. *(Objective: M6.1 research conventions — `ai_qe/CONTRIBUTING.md`, "Research conventions"; `ai_qe/docs/research-log.md`.)*

**Q2 — A.** Routes end on a decision discussion; the executive message is "whether to fund the first two phases, not whether to transform QA." A decidable ask advances the sale; a transformation vision defers it. *(Objective: M6.2 route design — `ai_qe/README.md`; `ai_qe/docs/economics/slide-language.md`.)*

**Q3 — B.** One form, role-routed at question 1; the three defining questions (primary outcome, autonomy ceiling, go/no-go threshold) are single-select because the "balanced combination" escape option "produced no signal"; ranges are gap-free with an unknown option; the financial-capture set is included — its absence was the failed form's "largest omission." *(Objective: M6.2 questionnaire rules — `ai_qe/docs/method/discovery-questionnaire.md`.)*

**Q4 — A.** A player-only patch advances the site version while deliberately retaining the slide/PDF editions, recorded in the changelog; "an existing published edition is never overwritten." *(Objective: M6.3 edition discipline — `ai_qe/_data/release.yml`; `ai_qe/releases.md`; `ai_qe/CONTRIBUTING.md`.)*

**Q5 — C.** Criteria are frozen before results; a CI crossing a boundary is insufficient evidence; one extension of at most 4 weeks; relabeling an effort miss as a quality win after the fact is explicitly rejected. *(Objective: M6.3 pilot gates — `ai_qe/docs/method/phased-pilot.md`; `ai_qe/_data/pilot_gates.json`.)*

**Q6 — D.** The published audit (14 findings: 4 high, 9 medium, 1 lower) with a finding → response → verification remediation table is credibility engineering: visible self-skepticism is the one thing a hype deck cannot counterfeit. *(Objective: M6.1 publish your own audit — `ai_qe/research/reviews/site-audit-2026-09-06.md`; `remediation-2026-09-06.md`.)*

**Q7 — Acceptable answer:** (1) Task-level efficiency — measured but vendor-affiliated on one synthetic task; may appear only with sample and affiliation labels, never as a productivity rate or capacity claim. (2) Self-reported task-level perception — must read "organizations *report*" and "rarely monetized"; never presented as measured or as savings. (3) Illustrative model output, not observed client results — labeled illustrative on the slide with "planning inputs are not observed client results"; any hard-dollar line requires Finance-confirmed capture. *(Objective: M6.1 four claim levels and the mixing error — `ai_qe/docs/principles.md`; `ai_qe/docs/economics/slide-language.md`; `ai_qe/README.md`.)*

**Q8 — Acceptable answer:** The ask is whether to fund Phases 0 and 1 (sponsor alignment plus a capped baseline), not whether to transform QA; every phase has a cost ceiling, frozen acceptance criteria, and a go/no-go memo signed by the sponsor. The benefits-realization register ties any claimed saving to a Finance-owned budget row (capture mechanism, budget-line owner, earliest date, accepted evidence), so "a capacity result with no capture row is reported as productivity, not cash saving." This closes because the buyer funds a bounded way to *produce* the number with stop rules — no promised outcome to disbelieve, and a negative or noisy result is survivable by design. *(Objective: M6.3 sell measurement, not outcomes — `ai_qe/docs/method/phased-pilot.md`; `ai_qe/docs/economics/slide-language.md`.)*