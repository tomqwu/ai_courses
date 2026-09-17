# Quiz M8 — Launch: Sales Page, Email Arc, Capstone

> 8 questions: 6 multiple choice (exactly one correct) + 2 short answer. Answer key with rationale and objective refs at the end. Sources: this module's lesson; `00-research/02-course-market-research.md` §E; `04-sales/landing-page.md`; `04-sales/launch-plan.md`; `01-design/assessment-and-rubrics.md`.

**Q1. (M8.2)** Your sending platform's dashboard shows a green "domain authenticated" badge, so you are about to queue the arc. First you run `dig +short TXT _dmarc.yourdomain.com` and it returns nothing at all. What does the empty answer mean, and what do you do?

A. Nothing — `_dmarc` is read only by your sending platform, so its dashboard is the authoritative check
B. No DMARC record is published, so receivers have no policy to apply to mail that fails SPF or DKIM alignment; publish one `v=DMARC1;` record with an explicit policy (`p=none` to start) and an `rua=mailto:` address, re-query until it answers, then send the test messages
C. The query failed because DMARC records are not public; read the value in the registrar's control panel instead
D. It does not matter while SPF resolves — `v=spf1 … -all` covers the same ground, and DMARC is optional

**Q2. (M8.1)** Your product is a $149 self-paced course. What page length does the research guidance indicate?

A. 800–1,200 words — under $200, the page answers fewer questions
B. 2,000–3,000 words — longer pages always convert better
C. 3,000+ words — length signals quality at any price
D. Under 500 words — the video does the selling

**Q3. (M8.1)** Launch day is near and you have zero testimonials. What do you do?

A. Draft two plausible ones yourself — you know what users would say
B. Post the proof you have (repo badges, evidence lines, a demo), reserve slots for real testimonials, and never invent quotes
C. Run with no social proof ever — testimonials cannot be added later
D. Turn what two friends said about the idea in DMs into named testimonials — they did say it

**Q4. (M8.2)** Which describes the launch arc correctly?

A. All 7–10 emails should sell — every send asks for the purchase
B. Warmup sells softly; conversion sells hard; the split is roughly half and half
C. Warmup (origin story → transformation proof → free tool) does not sell; then conversion (cart open → objection teardown → testimonial → final call)
D. Send one strong sales email, repeated daily until the deadline

**Q5. (M8.2)** Why does the arc end in a deadline, and what makes the deadline honest?

A. 42–55% of enrollments arrive in the final 48 hours, so a kept deadline is load-bearing — the cart really closes; a fake countdown trains the list to ignore your next deadline
B. Deadlines are dark patterns; ethical launches keep the cart open indefinitely
C. The stat means you should queue most emails inside the final 48 hours
D. Extend the deadline if sales are slow — kindness converts

**Q6. (M8.2 — short answer)** Your list is 800, expected open rate 35%, click rate 12%, page conversion 10%, price $299. Compute expected revenue, carrying decimals through the chain and rounding only the final dollar figure. Name two honest levers to improve it, and one "improvement" you must refuse.

**Q7. (M8.3)** Why does the capstone contract require ONE archetype and ONE shippable scope?

A. The rubric scores the completeness of the loop and the honesty of the evidence — one archetype fully looped is what the five dimensions can verify; code size is not a dimension
B. The capstone is graded on code size, so a small scope reviews faster
C. All three archetypes must be attempted to pass; one is just what you demo
D. Instructors can only review one archetype per student

**Q8. (M8.3 — short answer)** A capstone submission's evidence record reads, in full: "Tests: all green. Repo: github.com/me/rosterbot. Sales page: done." Rewrite it into the required capstone evidence record — every required block, with placeholders for values you do not have — and state what would turn a record like this from *incomplete* into an *automatic fail*.

## Answer key

| Q | Answer | Rationale | Objective |
|---|---|---|---|
| 1 | B | Deliverability is configured before the first send because Gmail and Yahoo enforce SPF/DKIM/DMARC for bulk senders, and the check is a DNS query on your own domain, not a dashboard badge (`04-sales/launch-plan.md`, operations checklist; Lab M8 "Deliverability gate"). An empty `_dmarc` answer means no published policy. A trusts the dashboard the question just contradicted; C is false — DMARC records are public TXT records, which is how receivers read them; D is the common "SPF is enough" error: SPF alone tells receivers nothing about what to do when alignment fails, and leaves you no `rua=` reports. | M8.2 |
| 2 | A | 800–1,200 words under $200; 2,000–3,000 is the $500+/cold-traffic band — length follows price, not "longer is always better." | M8.1 |
| 3 | B | Never invent social proof; real shipped projects are the social proof for technical buyers; reserve slots and earn testimonials via the beta trade. D is still invented proof — a private reaction to an idea is not a student's result. | M8.1 |
| 4 | C | Warmup earns trust without selling; conversion spends it; asking in every email trains the list to stop opening. | M8.2 |
| 5 | A | Deferred decisions collapse at a real deadline; only a deadline you keep stays load-bearing across launches. | M8.2 |
| 6 | Model: 800 × 0.35 = 280 opens; × 0.12 = 33.6 clicks; × 0.10 = 3.36 enrollments; × $299 = $1,004.64 ≈ **$1,005** (the stem fixes the convention: decimals carried, one final rounding). Honest levers, any two: grow the list with the free tool; improve subject lines/sender reputation; one CTA per email; strengthen the sales page; revisit price per M7. Refuse: purchased lists, fake urgency, invented testimonials. | M8.2 |
| 7 | A | The five dimensions (spec, build, evidence, discipline, launch-readiness) score loop completeness and honesty; no dimension counts lines of code. | M8.3 |
| 8 | Model: `## Capstone evidence — rosterbot — <date>` / Commands run: `<command>` → `<N passed, M failed or skipped>`, one line per command, dated / Artifact links: repo at tag `<vX.Y>`, spec folder `<path>`, evidence log `<path>`, sales page draft `<path>` / Limitations, not verified: `<honest list, failures included>` / plus the statement of what the agent did versus what the student verified. Incomplete is recoverable — re-run and fill the blocks. It becomes an automatic fail only when a line is fabricated: "all green" for a run never made, or a count the command did not print. | M8.3 |
## Objective → assessment map

Every "By the end of this module you can" line in `course/03-content/m08-launch-capstone/lesson.md`, and what checks it.

| Objective (lesson.md) | Checked by |
|---|---|
| **Write** a converting sales page in the 8-section evidence-backed anatomy, sourcing every proof claim from artifacts you already own | Q2 (length set by price), Q3 (no invented social proof); Lab M8 checklist line "Sales page: 8 sections, one CTA, word target set by price, no unsourced claim" |
| **Run** a 7–10 email launch arc, with the revenue model and deliverability hygiene that make it arrive | Q4 (warmup/conversion split), Q5 (the honest deadline), Q6 (five-factor revenue model), Q1 (SPF/DKIM/DMARC before the first send); Lab M8 "Deliverability gate" and its checklist line, plus "5 emails drafted; one CTA each; the deadline real" |
| **Ship** the capstone — one archetype, one shippable scope, the complete loop — scored against the 5-dimension rubric | Q7 (why one archetype), Q8 (the evidence record, and what makes it an automatic fail); the whole Lab M8 acceptance checklist, scored by `lab-rubrics.md` C1–C5 |
