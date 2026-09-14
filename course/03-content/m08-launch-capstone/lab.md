# Lab M8 — Capstone: Ship v1 Through the Full Loop

> Part of AI Product Studio (APS-3) · Prerequisites: Modules 1–7 (earlier labs are the capstone's raw material — reuse and extend them; do not restart) · Time: 6–10 hours over 1–2 weeks (cohort: week 8, ending at demo day)

**Goal.** Ship v1 of one product through the full Spec-to-Ship Loop with a recorded evidence record, plus launch assets — an 8-section sales page and a 5-email mini-arc — and deliver a 5-minute demo. Pass = rubric ≥80% with no dimension below "meets," evidence record included, and a public artifact link that works.

## The capstone contract

**ONE archetype. ONE shippable scope. The complete loop.** The rubric scores the loop and the evidence, not the code size — a complete loop at small scope out-scores a sprawling half-loop on every dimension. Pick your row:

| Archetype | v1 scope (shipped) | Discipline artifact (rubric D4) | Release evidence |
|---|---|---|---|
| **Type 1 — on-device app** | Your TinyCopilot (M2/M3 labs) extended with ONE real feature | Privacy hardening: local-only mode with fail-closed tests, including the cloud-alias red-team case | Public repo, version tag pushed (e.g. `v0.1.0`) |
| **Type 2 — spec-driven SaaS** | The M4 feature implemented per its own spec and tasks | Tenant-isolation negative-path tests + playbook acceptance with a validating manifest | Deployed URL **or** public repo tag |
| **Type 3 — expertise product** | The M6 briefing expanded to 20 slides | Reconciled provenance — every slide claim has a provenance row — plus the questionnaire draft | Live page on any static host |

"Shipped" means the public link works from a clean browser: a pushed tag on a public repo, or a deployed URL.

## Steps

1. **Post your plan before building** (the M8.3 action step): archetype, one-sentence scope, each loop stage mapped to a named artifact (file, tag, or URL). Get one peer reply; revise.
2. **Spec.** Type 2: reuse the M4 folder, updated to what you will actually ship. Types 1/3: write an equivalent scope spec — ≥2 independently testable stories with Given/When/Then acceptance criteria and explicit non-goals. Run the M4 requirements-checklist gate on it.
3. **Build (TDD).** Failing test first, visible as its own commit; small reviewable commits; testable core separated from glue (protocols/seams for Types 1–2; data vs. rendering for Type 3).
4. **Validate.** Run every tier you can: the unit suite; the archetype discipline tests (local-only fail-closed / tenant negative-path / provenance reconciliation); a real-provider contract test gated outside CI where applicable (the M3 pattern, `LAB_E2E=1`). Record commands and counts as you go.
5. **Release.** Tag the public repo and push the tag, or deploy the page. Open the link in a clean browser session and confirm it is the exact artifact you tested.
6. **Sales assets.** Write the 8-section sales page (M8.1 anatomy; length set by your M7 price) and the 5-email mini-arc (below).
7. **Demo.** Record (or rehearse for demo day) the 5-minute demo: problem 30s → loop walkthrough 2 min → live demo 2 min → evidence + limits 30s.
8. **Assemble and score.** Fill in the evidence record (template below), self-score with the rubric, exchange peer scores, submit — cohort: instructor final at demo day; self-paced: your community pair scores with the evidence posted.

## Required artifacts checklist (mapped to rubric dimensions)

| # | Artifact | Dimension |
|---|---|---|
| 1 | Spec artifacts — the M4 folder (Type 2) or an equivalent scope spec (Types 1/3) | D1 Spec quality |
| 2 | TDD evidence — a failing-test-first commit visible in history | D2 Build discipline |
| 3 | Validation evidence record in the SignUpFlow format (below) | D3 Evidence honesty |
| 4 | Released artifact — git tag with a version, or deployed URL; the link works | D2/D5 — the loop, closed |
| 5 | Discipline artifact per archetype — local-only tests / tenant isolation + manifest / reconciled provenance | D4 |
| 6 | Sales page draft — all 8 sections, one CTA, no unsourced claim | D5 Launch-readiness |
| 7 | 5-email launch mini-arc — cart open, objection teardown, testimonial/proof, final call, post-launch survey | D5 |
| 8 | Demo — 5 minutes, recorded or live, in the four-beat structure | D5 |

The **5-email mini-arc** is the capstone-scale cut of the course's 7 (`04-sales/launch-plan.md`), with warmup omitted or reused from your M8.2 draft: **(1) cart open** — the offer, price, guarantee; **(2) objection teardown** — your four real objections answered plainly; **(3) testimonial/proof** — before/after/result only if real, else a walkthrough of your own repo evidence; **(4) final call** — short, with a real deadline; **(5) post-launch survey** — what stopped you: price, time, or level.

## Rubric scoring instructions

Score each dimension 0–5 (3 = meets; equal weights). **Pass = total ≥80% AND no dimension below 3.** The full rubric, restated from `01-design/assessment-and-rubrics.md`:

| # | Dimension | 3 ("meets") looks like | 5 ("exceptional") looks like |
|---|---|---|---|
| 1 | **Spec quality** | Complete spec-kit artifacts for the shipped scope; stories independently testable; acceptance criteria concrete | A fresh agent session implemented a story without conversation context; checklist gate passed on first review |
| 2 | **Build discipline** | TDD evidence (failing test first); small reviewable commits; core separated from glue via protocols/seams | Coverage floor enforced; red-team/negative-path tests included; a real-provider contract test outside CI |
| 3 | **Evidence honesty** | Validation record with commands, counts, date, limitations; failures included, not hidden | Gap-style self-review identifying known limitations with priorities; "not verified" list present |
| 4 | **Privacy/safety engineering** (Type 1/2) **or claim discipline** (Type 3) | Local-only/fail-closed mode OR tenant isolation OR provenance table implemented and tested | Multiple defenses layered with tests for each; or full four-level claim labeling with reconciled provenance |
| 5 | **Launch-readiness** | Positioning one-liner, pricing rationale with sourced comparators, sales page draft, 5-email arc | Sales page ready to publish; arc personalized with your own proof assets; demo delivered (recorded or live) |

Sequence: **self-score → peer-score → instructor final** (cohort, at demo day). Self-paced: self-score, then exchange with your community pair against this table; post both scores with the evidence record. Honesty rule: use agents freely — the course teaches that — but the record states what the agent did and what you verified. A fabricated result or evidence line is the only automatic fail.

## Evidence to record

The capstone evidence record is the required attachment (modeled on SignUpFlow's validation format):

```markdown
## Capstone evidence — <project> — <date>
Commands run (with results):
- <command> → <pass/fail counts>
- ...
Artifact links:
- Repo: <url> (tag <version>)
- Spec folder: <path>
- Evidence log: <path>
- Sales page draft: <path>
Limitations / not verified:
- <honest list>
```

Keep also: the plan post and its peer reply, the demo recording link, both scoresheets, and — if you ran the stretch — the launch actuals.

## Acceptance checklist (pass = every box)

- [ ] Plan posted and peer-reviewed **before** building
- [ ] Spec artifacts exist; stories independently testable; checklist gate run
- [ ] A failing-test-first commit is visible in history
- [ ] All suites green — or every failure honestly recorded
- [ ] Tag pushed or page deployed; link verified from a clean browser
- [ ] Discipline artifact present and passing (Type 3: provenance reconciles)
- [ ] Sales page: 8 sections, one CTA, word target set by price, no unsourced claim
- [ ] 5 emails drafted; one CTA each; the deadline real
- [ ] Demo recorded (≤5:30) or delivered live, ending on the limits
- [ ] Evidence record complete + self-score ≥80% (nothing below 3) + peer score exchanged

## Stretch goals

- **Publish for real.** Put the sales page on any host (Gumroad, a static site) and link it from your repo README.
- **Run the arc.** Send the 5-email mini-arc to a real opt-in list — 20 people is enough — and record actuals (delivery, opens, clicks, conversions, revenue) in a launch evidence log; compare against your M8.2 model and note deviations honestly.
- **Add the real-provider contract test** (Types 1–2), gated outside CI per the M3 pattern.

## Discussion prompt (the demo-day post)

Post your demo using this template — cohort: before demo day; self-paced: when your pair has scored you:

- **Archetype + one-sentence scope** — what v1 does, for whom
- **The loop map** — spec → build → validate → release → prove, one artifact per stage (file, tag, or URL)
- **The demo link** (5 minutes)
- **The top item from your not-verified list** — what you would fix first, and why you didn't
- **One ask** — the specific feedback you want from viewers

Then score one peer against the rubric: the dimensions you would mark 3 or above, and the one you would push higher — naming the artifact that would get it there. This post is the course's testimonial engine; it is what fills the reserved slots on your sales page.