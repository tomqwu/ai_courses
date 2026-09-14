# Glossary — M8: Launch: Sales Page, Email Arc, Capstone

> Eighteen terms, alphabetical. "Where it lives" is the file to open — every entry resolves in this
> repository. Definitions are the ones this module teaches, not a general marketing dictionary.

**Acceptance criteria** — Concrete, testable conditions a story must satisfy, written Given/When/Then. The capstone's dimension 1 fails when criteria are vague. *Where:* `SignUpFlow/specs/014-security-hardening/spec.md`; `03-content/m08-launch-capstone/lab.md` step 2.

**Beta-discount trade** — A founding-cohort discount explicitly exchanged for a testimonial and a feedback session, agreed at checkout. Honest because the buyer knows what the discount buys. *Where:* `04-sales/pricing-and-platforms.md` (launch-price policy).

**Cart open** — Email 4 and the moment the offer becomes purchasable; the course opens the cart for 10–14 days. The first email of the conversion phase. *Where:* `04-sales/launch-plan.md`.

**Conversion phase** — The last four emails (cart open → objection teardown → proof → final call), which spend the trust the warmup phase earned. *Where:* `04-sales/launch-plan.md`; `00-research/02-course-market-research.md` §E.

**Deadline honesty** — The rule that a launch deadline must describe a real change — the cart closes, the price ends — because a resetting or recurring deadline teaches the list to wait. *Where:* `04-sales/pricing-and-platforms.md` ("no fake countdowns").

**Deliverability** — Whether email reaches the inbox at all; configured through SPF, DKIM, and DMARC on the sending domain, enforced by Gmail and Yahoo for bulk senders. Upstream of every conversion number. *Where:* `04-sales/launch-plan.md` (header and ops checklist).

**Evidence record** — The capstone's required attachment: commands with results, artifact links, and a limitations list. Vagueness ("tests pass") fails dimension 3. *Where:* `01-design/assessment-and-rubrics.md` (capstone evidence record).

**Fail-closed** — A local-only mode that rejects anything it cannot verify as local, rather than falling back to a cloud model. The Type 1 discipline artifact. *Where:* `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift`; `03-content/m08-launch-capstone/lesson.md` M8.3.

**Launch evidence log** — The record of actual list size, delivery, opens, clicks, conversions by email, and revenue, kept so the next revenue model is derived from observations. *Where:* `04-sales/launch-plan.md` (metrics to record).

**Lead product** — The free asset that builds the list before the arc runs; the course uses a 30-minute AI product teardown. *Where:* `04-sales/launch-plan.md` (the free lead product).

**One CTA** — Exactly one call to action, repeated verbatim wherever it appears. Two competing buttons give the reader a way to do nothing. *Where:* `04-sales/landing-page.md` (hero, pricing, final call).

**Proof asset** — An artifact you already own that carries a page claim: a tagged repo, a dated evidence line, a coverage number, a spec folder, a provenance table, a demo. *Where:* `03-content/m08-launch-capstone/lesson.md` M8.1 inventory table.

**Reserved testimonial slot** — A labeled, empty testimonial placeholder with an honesty note, used instead of inventing social proof. The course's page reserves three in before/after/result format. *Where:* `04-sales/landing-page.md` (testimonials).

**Spec-to-Ship Loop** — The course's six stages: Study → Spec → Build → Validate → Release → Prove. The capstone executes all six on one product. *Where:* `00-research/00-synthesis.md`.

**StoryBrand stance** — The positioning rule that the student is the hero and the instructor is the guide; write "you will ship," not "I will teach." *Where:* `00-research/02-course-market-research.md` §E.

**Tenant isolation** — Enforcing that every query and route is scoped to one organization, verified with negative-path tests using real JWTs. The Type 2 discipline artifact. *Where:* `SignUpFlow/docs/TESTING.md`; `03-content/m08-launch-capstone/lab.md`.

**Transformation headline** — A one-sentence, falsifiable statement of the destination, not the contents. The first of the eight sections. *Where:* `00-research/02-course-market-research.md` §E; `04-sales/landing-page.md`.

**Warmup phase** — The first three emails (origin story → transformation proof → free tool), which earn trust and make no sales ask. *Where:* `04-sales/launch-plan.md`.

## Terms people get wrong

- **Warmup vs. conversion** — warmup earns the right to sell; conversion spends it. An email that sells during warmup is a conversion email in the wrong slot.
- **Reserved slot vs. placeholder testimonial** — a reserved slot is empty and labeled as such; a placeholder testimonial is a quote you wrote. The second is fabrication.
- **Lead product vs. the course** — the free teardown is a list-builder that delivers one method in miniature; it is not a discount version of the paid offer.
- **A passing badge vs. recorded evidence** — a badge is a current status; an evidence record is a command, its counts, a date, and its limits. Only the second survives a gap review.
- **Page length vs. page quality** — length follows price and stakes; it is an output of the objections you must answer, never a proxy for thoroughness.

## Curated resources

1. `04-sales/landing-page.md` — the complete worked page; read it as eight sequenced moves, and copy the reserved-slot pattern verbatim.
2. `04-sales/launch-plan.md` — the seven-email arc with subject lines, plus the ops checklist you run before the first send.
3. `04-sales/pricing-and-platforms.md` — the price ladder and the honest-marketing checklist that gates every asset you write.
4. `00-research/02-course-market-research.md` §E — the primary source for the anatomy, the phase split, the final-48-hours figure, and the revenue formula.
5. `01-design/assessment-and-rubrics.md` — the five-dimension capstone rubric and the evidence-record template, restated in the lab.
6. `03-content/m08-launch-capstone/lab.md` — per-archetype scope table, required-artifact checklist, acceptance checklist.
7. `SignUpFlow/docs/playbooks/validation.md` — the format your evidence record imitates: counts, a date, environment, and failures still visible.
8. `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift` — the reference implementation of fail-closed local-only behavior your Type 1 discipline artifact is measured against.
