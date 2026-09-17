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

## Milestone 4 — [Narrated learner site](https://github.com/tomqwu/ai_courses/milestone/4)

| Workstream | Issue |
|---|---|
| Narration pipeline (scripts, TTS providers, caption engine, contract) | [#17](https://github.com/tomqwu/ai_courses/issues/17) |
| Learner site (static build + player, captions, transcript, keyboard) | [#18](https://github.com/tomqwu/ai_courses/issues/18) |
| Record all 9 decks — 233 slides narrated and validated | [#19](https://github.com/tomqwu/ai_courses/issues/19) |
| Verification and docs (browser check, verify.py, regression tests) | [#20](https://github.com/tomqwu/ai_courses/issues/20) |
| Release voice with ElevenLabs | [#21](https://github.com/tomqwu/ai_courses/issues/21) — open, needs an API key |

## How this milestone set was derived

The expansion is scoped by one rule from the course's own method (M1): **a claim is only as good as the
artifact behind it.** A course that teaches evidence discipline has to carry its own. So each module's DoD
is a checklist a reviewer can run — not a description of intent — and the tracking issues mirror those
checklists one-for-one rather than existing as a separate project plan.

## Status

**Milestones 1–3 are complete** — 16/16 issues closed, each with a comment carrying measured
evidence (artifact list, word counts, deck slide/note counts, and the verification command to
reproduce it) rather than a statement of intent.

**Milestone 4** adds the narrated learner site: 4/5 issues closed, with #21 (the paid release voice)
deliberately left open because it needs an `ELEVENLABS_API_KEY` this repository does not hold. The
preview recording is complete, labelled as a preview in the data and in the UI, and swappable with one
command.

| Milestone | Issues | State |
|---|---|---|
| Course Core — Complete Module Packages | #1–#9 | ✅ closed |
| Track Bundles — 3 standalone products | #10–#12 | ✅ closed |
| Production & Launch Readiness | #13–#16 | ✅ closed |
| Narrated learner site | #17–#21 | ✅ #17–#20 closed · #21 open (needs `ELEVENLABS_API_KEY`) |

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

Final verification for milestone 4 (`make -C course check`):

```
$ make -C course check
python3 06-production/narration/validate_narration.py --scripts-only
Narration scripts verified: 9 decks, 233 slides, 21,536 words (mean 92 words/slide)
python3 06-production/narration/validate_narration.py
Narration verified: 9 decks, 233 scripted slides, 233 recordings with timed captions — complete
python3 learner-site/build_site.py --check
site written to /tmp/aps-site-check   decks: 9 · slides: 233 · scripted: 233 · recorded: 233
python3 learner-site/check_player.py --all --print-skip
  ok  m00 … m08   (233 slides, 233 narrated)
browser check passed: 9 deck(s) — panel injected, captions parsed, deep links and status regions correct
python3 06-production/verify.py
[PASS] Artifacts + length bands      [PASS] Rubrics        [PASS] Track bundles
[PASS] Decks                         [PASS] Sales claims   [PASS] Narration contract
[PASS] Learner site                  [PASS] Repo file pointers (1048 checked)

RESULT: ALL CHECKS PASSED
```

**45 unit tests** run in this gate: 32 caption tests and 13 provider tests. The provider suite exists
because the ElevenLabs release path is the *primary* voice and cannot be exercised here — it needs a
paid key this repository does not hold. It is driven instead through a stubbed transport with a real
encode and a real `ffprobe`, so the request we build, the alignment we parse, the proportional
fallback and the no-retry rule are all verified. The suite was mutation-checked: flipping
`ends[hi]` to `ends[lo]` in the token-timing map, and dropping the token start time, each fail three
tests. Word-exactness alone did not catch either, which is why the timing assertions were added.

Three defects were found by this work and fixed before it shipped, all recorded in
[`narration/DESIGN.md`](narration/DESIGN.md): an abbreviation guard that matched `ms.` inside
`seams.` (which scrambled caption timing on affected slides); a player panel that was created hidden
and never shown, so every narration control existed and none was visible; and a merge step that could
push a cue past the line limits. The panel bug was caught only because the browser check was extended
to assert visibility rather than presence.


## Milestones 5–9 — from course package to owned platform (proposed 2026-09-17)

The September 2026 platform review ([`../00-research/04-platform-review-2026.md`](../00-research/04-platform-review-2026.md))
found the package complete and honest, and not yet a product: no way to take money or know a learner,
no licence, a fact base that drifted within five days of being pinned, three labs that cannot be passed
as written, and a curriculum nine months behind in three places. It proposes five further milestones,
each with a Definition of Done a reviewer can run:

| Milestone | Scope | Done when |
|---|---|---|
| 5 — Make the course true again, and keep it true | Re-pin §0.2 from `check_facts.py`, line-range pointer checks, the three unpassable labs, quiz hygiene | `check_facts.py --strict` and `verify.py` both green; audit §9 items 1–11 closed |
| 6 — The 2026 layer | Evals tier, prompt injection, three-tier privacy (on-device / PCC / cloud), spec-kit 1.0, METR/DORA as the governance rationale, worked pricing | Each new segment has a lab step or quiz item that assesses it |
| 7 — Sell (Stage 0) | `LICENSE`, email capture, lead product published, merchant-of-record checkout with repo access, devcontainer, dated update window | A stranger can pay, clone, and run `make lab-m2` green in Codespaces |
| 8 — Own the platform (Stage 1) | Docs-site + paywall, progress, interactive quizzes, Open Badges 3.0, purchasing-power parity, extracted playbooks | Entitlements come from payment webhooks; progress survives a reload |
| 9 — The founding cohort | Cohort #1 at the researched price, evidence log with stated denominators | Completion, refunds and NPS recorded; pricing re-derived from actuals |

The review's first deliverable is already in the tree: `check_facts.py` reports **5 of 14** pinned facts
drifted against the 2026-09-16 upstream heads (competitor rows 12 → 14, latest ListenToMe release
v1.3.0 → v1.4.4, `AGENTS.md` 177 → 188 lines, constitution 79 → 85, tests 1,464 recorded vs 1,766 on
disk). Nothing in the course was silently edited to match — Milestone 5 is where those edits happen,
with the checker naming each file.
