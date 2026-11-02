# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

**Primary:** intermediate software engineers (roughly 2+ years) who want to build real AI products, use coding agents professionally rather than casually, and eventually monetize what they build. They are comfortable with Python or Swift, Git and the command line; no prior LLM/API experience is assumed. They arrive self-paced or in an eight-week cohort.

**Secondary:** indie hackers and technical founders choosing a first AI product; senior engineers, tech leads and consultants productizing expertise.

**Emerging audience (approved, not yet shipped):** non-coders who want to ship — founders, designers, domain experts and small-business owners — arriving through the beginner ladder (L0–L5), starting with the free GitHub Pages module.

## Product Purpose

AI Product Studio teaches one delivery method — study, spec, build, validate, release, prove — by walking through three real, shipped open-source AI products and having the learner build a working core of the same three archetypes: an on-device AI app, a spec-driven multi-tenant SaaS, and an evidence-cited expertise product. Success is a learner who leaves with public artifacts, recorded validation evidence, a defensible price and launch package, and a repeatable operating system for the next product.

## Positioning

Most AI courses teach API calls. This one teaches the operating system around them: a constitution, agent rule files, spec-kit, evidence discipline and acceptance gates, demonstrated in three production repositories whose every claim resolves to a file the learner can open. The course holds its own material to that same standard — every number carries a pointer, a pinned commit, a date and, where relevant, a limitation.

## Operating Context

The course is a static learner site generated from Markdown and JSON, delivered text-first in English and Chinese. Learners read, search, listen when recordings are published, work through labs with objective acceptance checklists, export an evidence log, and take knowledge checks with answer keys. Progress is stored in the browser; there is no account, server-backed progress, entitlement or payment system in the current build. Pricing is present in sales copy but the site flag keeps prices off the public pages. The full package is checked by one gate (`course/check.sh`) on every change.

## Capabilities and Constraints

- Ten modules: M0–M9, 258 parts, 8 module labs plus the M8 capstone, ten knowledge checks (80 questions including the free M9 check; 72 in the paid M0–M8 course).
- Lessons, handouts, glossaries, labs, interactive checklists, knowledge checks, transcripts and a command-palette search across every unit.
- Every case-study claim carries a repo pointer that resolves at a pinned commit; facts with drift risk are re-derived by `check_facts.py`.
- Static build, no backend, no accounts; browser-local progress with export/import. Payments, entitlements and server-backed progress are open decisions.
- English and Chinese editions are held to parity; a module's Chinese must be re-stamped when the English changes.
- Content is not to be shrunk to fit a frame; the gate checks clipping at two desktop sizes.
- An approved beginner ladder (L0–L5) is in progress on top of M0–M9; L1 is the pilot.
- The learner experience is being rebuilt around an Expedition trailhead: a route map, session-sized legs, a day trail and field notes derived from recorded study events.

## Brand Commitments

- Name: **AI Product Studio** (course code APS-3); tagline: *Study three real, shipped AI products. Build your own. Sell what you build.*
- Voice: second person, imperative, specific, warm but exact. No hype, no invented outcomes, no fabricated testimonials or benchmarks. Limitations are stated plainly.
- The evidence system — the amber EVIDENCE chip, the file/lines/commit exhibit header, the SOURCE footer, the pointer counts — is a binding part of the identity and must survive the redesign.
- The text-first copy, complete transcripts, searchable reading pages and print views are a binding commitment; the redesign changes the learning layer around them, not their availability.
- The owner's learning-GUI brief (confirmed 2026-10-28): a **Quantic MBA spine with Duolingo momentum** — premium, structured and progress-driven, plus playful, bite-sized motivation and immediate feedback. The full visual world is being replaced; the evidence system and text-first transcripts stay.

## Evidence on Hand

- Three production repositories cloned beside the course at pinned commits: ListenToMe (a9bde8e), SignUpFlow (c550d46), ai_qe (6388f0a).
- ListenToMe: 96% core coverage, 95% CI floor, 14-row competitor table, a held-back 1.3.0 at 97.24% coverage, signed/notarized releases.
- SignUpFlow: 1,464 passed / 21 skipped in a dated validation record, seven test tiers, 17 spec folders, an executable route-authorization matrix.
- AI × QE: 116 narrated slides across four decks, four claim levels, a 14-finding self-audit, edition/provenance records.
- The course's own proof: 2,689 resolving pointers, 154 anchored ranges, 258 scripted parts, a full gate that checks artifacts, exhibits, narration, Chinese parity, figures and the learner site.
- No testimonials, customer logos, outcome studies or cohort results exist yet; future work must not invent them.

## Product Principles

1. **Evidence over assertion.** A claim without a pointer, a command, a date or a stated limit is not finished.
2. **Method over tools.** The three archetypes differ in technology; the delivery loop is the transferable product.
3. **One next action.** The learner should always know the smallest useful thing to do now, and why it matters.
4. **Honest motivation.** Streaks, XP and completion moments may reward real study actions; they may never manufacture social proof or urgency.
5. **The reading copy is the source of truth.** Audio, captions, search and play are views of the approved words, not replacements for them.

## Accessibility & Inclusion

WCAG AA is the target: keyboard-operable controls, visible focus, text contrast, no content clipped at the shipped sizes, reduced-motion alternatives that preserve state, and plain-language explanation of technical terms. The learner site is used on phones as well as desktops; mobile is a first-class learning surface, not a fallback. The beginner ladder adds a non-coder audience and requires plain words at first use.
