# Milestones & Tracking

Work on this course is tracked as GitHub milestones and issues in
[`tomqwu/ai_courses`](https://github.com/tomqwu/ai_courses/issues). This file is the in-repo mirror so the
roadmap travels with the content.

## Milestone 1 — [Course Core — Complete Module Packages](https://github.com/tomqwu/ai_courses/milestone/1)

Every module from M0 to M8 gains the full end-to-end package defined in
[`../01-design/content-standards.md`](../01-design/content-standards.md): Marp slides with speaker notes,
lab solutions, timed video scripts, a printable handout, a cohort facilitation kit, a glossary with
curated resources, per-lab rubrics, and accessibility/transcript notes.

| Module | Issue | Artifacts |
|---|---|---|
| M0 — Orientation | [#1](https://github.com/tomqwu/ai_courses/issues/1) | 8 |
| M1 — The Operating System | [#2](https://github.com/tomqwu/ai_courses/issues/2) | 8 |
| M2 — The On-Device AI App: Architecture | [#3](https://github.com/tomqwu/ai_courses/issues/3) | 8 |
| M3 — Privacy, Testing, Shipping | [#4](https://github.com/tomqwu/ai_courses/issues/4) | 8 |
| M4 — The Spec-Driven AI SaaS | [#5](https://github.com/tomqwu/ai_courses/issues/5) | 8 |
| M5 — Multi-Tenant Security & the Acceptance Gate | [#6](https://github.com/tomqwu/ai_courses/issues/6) | 8 |
| M6 — The Expertise Content Product | [#7](https://github.com/tomqwu/ai_courses/issues/7) | 8 |
| M7 — Monetize: Pricing, Packaging, Positioning | [#8](https://github.com/tomqwu/ai_courses/issues/8) | 8 |
| M8 — Launch: Sales Page, Email Arc, Capstone | [#9](https://github.com/tomqwu/ai_courses/issues/9) | 8 |

**Definition of Done:** §5 of the content standard — length bands met, every repo claim carries a pointer
that resolves, no unverified numbers, no fabricated outputs, speaker notes on every slide.

## Milestone 2 — [Track Bundles — 3 standalone products](https://github.com/tomqwu/ai_courses/milestone/2)

Three single-track bundles, each a complete sellable product built from a subset of the course, priced
at **$199** against the full course at **$399** (the full course stays the recommended path — see each
bundle's `pricing.md`).

| Bundle | Issue | Built from |
|---|---|---|
| On-Device AI Apps | [#10](https://github.com/tomqwu/ai_courses/issues/10) | M0, M1, M2, M3 + M7/M8 slice |
| Spec-Driven AI SaaS | [#11](https://github.com/tomqwu/ai_courses/issues/11) | M0, M1, M4, M5 + M7/M8 slice |
| Expertise as a Product | [#12](https://github.com/tomqwu/ai_courses/issues/12) | M0, M1, M6 + M7/M8 slice |

Each bundle ships `README.md`, `syllabus.md`, `sales-page.md`, `pricing.md`, and `bundle-map.md`.

## Milestone 3 — [Production & Launch Readiness](https://github.com/tomqwu/ai_courses/milestone/3)

| Workstream | Issue |
|---|---|
| Slide tooling (Marp theme, build, validation) | [#13](https://github.com/tomqwu/ai_courses/issues/13) |
| Course-level production docs (master glossary, certificate, welcome packet) | [#14](https://github.com/tomqwu/ai_courses/issues/14) |
| Verification pass (decks build, pointers resolve, counts consistent) | [#15](https://github.com/tomqwu/ai_courses/issues/15) |
| Docs update + release | [#16](https://github.com/tomqwu/ai_courses/issues/16) |

## How this milestone set was derived

The expansion is scoped by one rule from the course's own method (M1): **a claim is only as good as the
artifact behind it.** A course that teaches evidence discipline has to carry its own. So each module's DoD
is a checklist a reviewer can run — not a description of intent — and the tracking issues mirror those
checklists one-for-one rather than existing as a separate project plan.

## Status

**All three milestones are complete** — 16/16 issues closed, each with a comment carrying measured
evidence (artifact list, word counts, deck slide/note counts, and the verification command to
reproduce it) rather than a statement of intent.

| Milestone | Issues | State |
|---|---|---|
| Course Core — Complete Module Packages | #1–#9 | ✅ closed |
| Track Bundles — 3 standalone products | #10–#12 | ✅ closed |
| Production & Launch Readiness | #13–#16 | ✅ closed |

Final verification at completion (`bd43c95`):

```
$ python3 course/06-production/verify.py
[PASS] Artifacts + length bands
[PASS] Rubrics
[PASS] Track bundles
[PASS] Decks
[PASS] Sales claims
[PASS] Repo file pointers (1044 checked)

RESULT: ALL CHECKS PASSED
```

The pass caught five real errors in content that had already shipped (recorded in
[`../README.md`](../README.md), "Drift the verification pass caught") and rejected two proposed
corrections that did not survive checking the source. Both outcomes are the point: the tracking is
only worth having if closing an issue means a check ran.
