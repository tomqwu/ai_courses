# Sales Page: Evidence-Cited Briefing

> Single-playbook page in the eight-section anatomy of `course/04-sales/landing-page.md`: headline, who it is for, problem, outcomes, proof, testimonials, FAQ, pricing with one call to action.

## 1. Headline

**Turn what you know into a briefing a skeptical buyer can check, number by number.**

A method, templates and two stdlib-only scripts for evidence-cited decks.

## 2. Who it is for, and who it is not for

**For you if you:**
- sell expertise as a briefing, deck, report or workshop, and your buyers are skeptical;
- quote studies and benchmarks and want each number to survive a hard question;
- publish on the web and want engines and readers to cite the version you actually wrote.

**Not for you if you:**
- want slide design or presentation delivery coaching;
- need a pricing model or a consulting offer (this stops at the briefing);
- want a method for running your own studies.

## 3. The problem

Most business-case decks mix levels. A per-task speedup from one study becomes "capacity", capacity becomes "savings", and nobody names the budget line. Self-reported figures sit unlabelled beside measured ones. Then the deck is edited in place, and nobody can say which version a client saw. A buyer who finds one of these stops trusting the rest.

## 4. What you will be able to do

- Keep a dated research log that records what you could not verify.
- Write a benchmark record for every source: date, sample, method, unit, measured or self-reported, sponsor, and what it supports.
- Label every number with one of four saving levels, never mixed, plus an epistemic label on the slide itself.
- Build a provenance table and a slide set with no orphan numbers, checked by a script.
- Cut executive and technical routes over one slide set, each ending on a decision a sponsor can make.
- Release in editions that are never overwritten, with a signed claim manifest that fails when a claim changes.
- Publish so AI engines can cite you correctly: a source in the sentence, a permalink per claim.

## 5. Proof

- **The scripts run and test themselves.** On 2026-09-26, `selfcheck.py --selftest` and `edition_manifest.py --selftest` both printed `SELFTEST: PASS`. A full build, sign, verify and check cycle on a sample briefing gave a good signature, and a one-number edit made `check` exit 1 and name the changed claim. Both are stdlib-only Python 3.11 and live in the course repository at `course/03-content/m06-expertise-product/`.
- **The playbook passes its own gate.** Run on the playbook file itself, `selfcheck.py` reports `PASS: 0 uncited quantitative claims`.
- **A real site built this way.** AI × QE keeps full benchmark records (`ai_qe/docs/evidence/benchmarks.md:31-42`), logs a failed download instead of hiding it (`ai_qe/research/document-manifest.json:2-8`), labels every number with one of four levels (`ai_qe/docs/principles.md:52-61`), and separates its site version from its content editions (`ai_qe/_data/release.yml:1-7`). The playbook also shows one place where that site's research log breaks its own ordering rule (`ai_qe/docs/research-log.md:153-155`).

The playbook comes from the AI Product Studio course by Tom Wu, who built the AI × QE briefing site (`course/04-sales/landing-page.md`).

## 6. Testimonials

None yet. No buyer has used this playbook, and this page will not invent one. Real results will appear here in before, after and result form.

## 7. FAQ

**Is it only for software topics?** No. The example is quality engineering; the method fits any field where you quote numbers.

**Do I need to code?** You need to run two Python commands and `ssh-keygen`. The rest is Markdown.

**Does passing the script mean my briefing is true?** No. It means no number lacks a source. The Limits section says so plainly.

**Are the scripts included?** They live in the AI Product Studio course repository; the playbook names their paths and expected output. Whether they ship with the playbook is the owner's decision.

**Is this the whole course?** No. It is one extracted method from the AI Product Studio course.

## 8. Price

**Proposed: $49** (proposed; the owner sets the final price). The course prices a module at about $44 (`course/04-sales/pricing-and-platforms.md:10`). This playbook carries a whole module's method and two runnable checks, so it sits at that rate.

[**Get the playbook →**]
