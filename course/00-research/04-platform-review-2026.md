# Platform Review: From a Course Package to an AI Learning Platform You Own (September 2026)

> A whole-repository review of AI Product Studio against 2026 industry practice for creating and
> selling technical courses, plus a plan for turning it into a platform of your own AI
> learning, application and best-practice content. Written 2026-09-17 against commit `5e82458`, with the
> three case-study repos cloned at their 2026-09-16 heads. It is built the way the course says work
> should be built: everything measurable was measured, every external claim carries a source, and the
> things that could not be verified say so.
>
> Companion research, all new: [`05-platform-build-options-2026.md`](05-platform-build-options-2026.md)
> (build vs buy), [`06-competitive-landscape-2026.md`](06-competitive-landscape-2026.md) (market),
> [`07-course-design-practice-2026.md`](07-course-design-practice-2026.md) (learning science),
> [`08-domain-currency-2026.md`](08-domain-currency-2026.md) (is the curriculum current), and
> [`09-content-audit-2026.md`](09-content-audit-2026.md) (module-by-module audit with pointers).

## 1. Verdict

**The package is unusually complete and unusually honest, and it is not yet a product.** It has
nine modules with eleven artifacts each, a self-verifying gate, a narrated learner site, three bundles,
a sales page and a launch plan — and it has no way to take money, no way to know who a learner is, no
licence, no testimonials, and a fact base that started drifting within five days of being written.
The course's strongest asset is its method (evidence discipline, agent governance, fail-closed privacy),
and the market research says that method is the only part of the offer with *no* direct competitor.
The plan below therefore does three things in order: make the course true again and keep it true by
machine; turn the method into the headline and the platform; and only then sell.

Ten moves, in priority order:

1. **Keep the facts true by machine.** `06-production/check_facts.py` (new in this review) re-derives the whitelist numbers from the clones; five of fourteen have already drifted. Wire it into the pre-cohort checklist and make line-range pointers checkable (§4.1).
2. **Fix the three labs that cannot be passed as written** — Lab M3 ships pre-solved, Lab M5 has no starter, and Labs M1/M2 template a red run that the tooling cannot produce (§4.2).
3. **Lead with evidence discipline.** "Every claim carries a file pointer" is the one differentiator nobody else teaches; make it the tagline, ship the pointer-lint and facts-drift tools as the free lead product, and re-frame the three products as the proof (§5).
4. **Add the 2026 layer the buyer screens for**: evals as an eighth test tier, prompt injection as a red-team row, the Apple Foundation Models / Private Cloud Compute three-tier privacy policy, spec-kit 1.0 command names, `AGENTS.md`-imported-by-`CLAUDE.md` (§4.5).
5. **Own the platform in stages, not at once**: sell repo/site access through a merchant-of-record today, build the docs-site + paywall in three months, add team seats and an all-access playbook subscription in twelve (§6).
6. **Re-tier the ladder against the observed market**: keep $199 tracks and $399 self-paced, launch cohort #1 at $790–990, hold $1,490 until there are twenty named testimonials, and consider a $2,000–2,500 mid tier with a course assistant (§5.3).
7. **Publish a dated update window and a changelog** on every sales surface; buyers now screen for "last updated" (§4.4).
8. **Decide the licence and the legal minimums before the first sale**: `LICENSE`, EU withdrawal waiver and button, VAT at customer location or a merchant of record (§4.4).
9. **Make the learner site a product surface**: progress, quiz interactivity, a Codespaces devcontainer for labs, email capture on the free copy (§4.3).
10. **Run the founding cohort as the evidence engine** it was designed to be, and measure completion with a stated denominator rather than quoting the industry's unverified 90% (§7).

## 2. What was reviewed, and how

| Surface | Method | Result |
|---|---|---|
| Design, sales, instructor and production docs | Read in full | §3, §4.4 |
| All nine modules (lesson, lab, quiz in full; the other eight artifacts skimmed) | Instructional-design audit against the binding standard, with pointers | [`09-content-audit-2026.md`](09-content-audit-2026.md) |
| The TinyCopilot lab code | `pytest` with coverage on Python 3.11 | **191 passed, 2 skipped, 100% coverage** — the README's "verified status" reproduces |
| The verification gate | `verify.py`, the 45 unit tests, `build_site.py --check`, `check_player.py --all` | Artifacts, rubrics, bundles, decks, sales claims, learner site and **all 1,052 pointers pass**; narration and browser steps fail only because the audio is generated, not committed |
| The pinned "verified numbers" | Re-derived from the three clones at their 2026-09-16 heads with the new `check_facts.py` | **5 of 14 drifted** (§4.1) |
| The learner site | Built and rendered headless at 1440px and 390px | Renders cleanly; findings in §4.3 |
| Industry practice, market, platforms, domain currency | Four cited web-research reports | `05`–`08` |

Not verified here: the published GitHub Pages copy (unreachable from the review environment), the
ElevenLabs release path (no key), and anything on a Mac (`say`, Xcode, notarization).

## 3. What is strong, and verified

- **The evidence discipline is real, not a slogan.** Every repo claim carries a pointer, `verify.py` resolves all 1,052 of them, the README records five errors the gate caught in shipped content and two proposed "fixes" it rejected, and the narration contract holds captions, transcripts and scripts word-for-word equal. No competitor in the market table publishes anything like this about its own course.
- **The lab reference implementation is solid.** TinyCopilot mirrors ListenToMe's architecture module for module, its tests are the spec, and the numbers the course prints reproduce exactly.
- **The design is backward-designed and cohort-ready.** Objectives use measurable verbs, every lab ends in a pass/fail artifact, every module has a 90-minute facilitation kit that sums to 90, rubrics have four levels with weights summing to 100 and auto-fail lists, and the certificate is bound to a commit SHA.
- **The learner site is a genuine design system**, ported from ai_qe with the changes written down, with a contrast audit that walks every text node and a partition of 233 slides into 63 units that the gate asserts covers every slide exactly once.
- **The sales material is honest.** Testimonial slots are reserved and say so; pricing is a decision record with "why not cheaper / why not more expensive"; the bundles tell buyers the full course is the better value.
- **The market position is defensible.** The competitive scan found no course teaching evidence/provenance discipline, none teaching fail-closed local-AI privacy, and essentially nothing on on-device Swift AI. Spec-driven governance is now taught elsewhere, but only as one-hour introductions ([`06`](06-competitive-landscape-2026.md) §3).

## 4. Findings

### 4.1 The fact base drifts faster than the course can be edited — and nothing measured it

`01-design/content-standards.md` §0.2 whitelists the numbers the course may state as fact. Five days
after they were pinned, five of them are wrong upstream:

| Fact | Pinned (2026-09-12) | Upstream (2026-09-16) | Course files still stating the old value |
|---|---|---|---|
| ListenToMe competitor table rows | 12 | 14 (Hyprnote and Meetily added) | 21 |
| ListenToMe latest macOS release | 1.3.0 "held back" | v1.4.4 (four releases on 13–14 Sept) | 11 |
| SignUpFlow `AGENTS.md` | 177 lines | 188 | 9 |
| SignUpFlow constitution | 79 lines | 85 | 14 |
| SignUpFlow tests | 1,464 recorded run | 1,766 test functions on disk | 37 |

The "1.3.0 held back at 97.24%" story is still true *as a dated record* — the gap review says what it
says — but the course tells it as the current state of the product, and the product has shipped four
releases since. The content audit found four more numbers outside the whitelist that never verified
("33 modules" is 45 files; `CLAUDE.md` is 154 lines, not 143; "10 current PDF editions"; "~460 lines"
is statements, not lines), and one line-range pointer that points at the wrong code
(`OllamaProvider.swift:99-119`), which the gate cannot see because it strips line ranges before
checking.

**Why it matters for a platform:** hand-copied facts in 200 files do not scale to a catalogue that
updates monthly. The fix is structural: one facts manifest, derived by script, with the course text
referencing facts by name where it can and the drift checker naming the files that need an edit where it
cannot. This review ships the first half (`06-production/check_facts.py` + `facts.json`); the second
half (line-range checks in `verify.py`, and templated facts in the decks) is Milestone 5.

### 4.2 Three labs cannot be passed as written

From the audit, ranked by how many learners it stops:

- **Lab M3 is pre-solved.** `privacy.py`, `test_privacy.py`, the contract test and the coverage floor all ship in the tree the learner is holding; the rubric demands a red run before the green and the solutions say the function "does not exist" before the fix. Lab M2 even requires `make lab-m3` to stay green.
- **Lab M5 has no starter.** The curriculum promised a `mini-flow` FastAPI starter; the lab says "this course ships no starter" and asks for a FastAPI + SQLAlchemy + JWT app to be built before any graded step, in a three-hour budget. This is the real "Module 2 chasm" — and it is at Module 5.
- **Labs M1 and M2 template a red run the tooling cannot produce** ("→ 2 failed" where reality is a collection error), which is the exact fabrication their own rubrics auto-fail.
- Lab M6's *named* peer reviewer and Lab M4's stranger test block self-paced buyers; the M0 "30-minute first win" is 45–90 minutes on a fresh machine and is given four different durations.

The full list with pointers is [`09-content-audit-2026.md`](09-content-audit-2026.md) §9.

### 4.3 The learner site is a reader, not a platform

Rendered and inspected (desktop and phone): the site is clean, accessible, keyboard-navigable and
honest about its preview voice. As a *product surface* it lacks everything a paying learner touches:

- no identity, so no progress, no "resume where you left off", no completion evidence;
- quizzes exist only as Markdown with answer keys — the knowledge checks the unit grammar promises are not interactive;
- labs are instructions to run elsewhere; there is no devcontainer or Codespaces entry point (GitHub Classroom, the obvious autograder, was retired on 2026-08-28);
- the free published copy has no email capture and no call to action, so it builds no list;
- 79% of slides are bullet lists and the median slide is 36 words (the site's own README measures this); the content is thin on screen even where the lesson text underneath is rich;
- the gate is macOS-dependent for the free voice (`say`) and finds Chromium only at fixed paths, so a Linux contributor or CI runner cannot run it green.

### 4.4 Selling: the prices are at the floor of the market and the legal minimums are missing

- **No `LICENSE`.** The README says so; nothing can be sold or even legally cloned for the labs until this is decided.
- **Prices vs the observed 2026 bands** ([`06`](06-competitive-landscape-2026.md) §2, [`07`](07-course-design-practice-2026.md) §3): $199 tracks sit well against CodeFast $169 and Small Bets $199; $399 self-paced equals a full year of boot.dev or DeepLearning.AI Pro, so it needs a dated update window to compete; comparable AI-engineering cohorts run $750–950 (mid) to $2,200–5,000 (top), so $1,490 without an audience or alumni is exposed in both directions.
- **No dated update window, no changelog on the sales page.** 2026 buyers screen for "last updated"; creators now sell "updates through <date>" rather than "lifetime".
- **EU legal minimums** for digital courses are absent from the launch checklist: the 14-day withdrawal waiver at checkout, the withdrawal button required since 2026-06-19, VAT at the customer's location for recorded *and* live tiers (or a merchant of record), and WCAG AA — which the site already meets.
- **The free lead product is still a plan.** Three emails and a PDF are written; nothing is published, and the free site does not collect an address.

### 4.5 The curriculum is nine months behind in three places

From [`08-domain-currency-2026.md`](08-domain-currency-2026.md):

- **On-device:** Apple's Foundation Models framework is now provider-agnostic (WWDC26), Private Cloud Compute is a free tier for small apps, and Ollama runs on MLX. The course's "local vs cloud" binary should become a three-tier policy (on-device / PCC / third-party cloud) with the consent screens App Store rule 5.1.2(i) now requires.
- **Spec-driven SaaS:** GitHub spec-kit reached 1.0 with new command names and a `converge` step; `AGENTS.md` is a Linux Foundation standard that Claude Code reads only via an import; OWASP published the GenAI Top 10 *2026*; METR's 2025/2026 studies are the independent evidence for why governance matters, and the course carries them in M6 without using them in M1.
- **Expertise product:** Google AI Overviews cut organic clicks 40–58% in independent studies, NotebookLM turned narrated decks into a commodity, and EU AI Act Article 50 makes synthetic-narration disclosure a compliance item. The durable differentiator is the evidence chain, not the narration.

And across all three, the audit found no evals, no prompt injection, no cost/latency model, no
observability, no retrieval, no tool/MCP design and no SaaS deployment — the seven topics a 2026 buyer of
an "AI product" course expects to see in the syllabus.

## 5. Positioning: lead with the method

### 5.1 What the market says

The competitive table has twenty-eight entries. Free vendor academies (Anthropic, OpenAI, Google,
DeepLearning.AI) now cover *tools*; Maven cohorts at $2,500–5,000 cover *evals*; indie products at
$169–499 cover *shipping a SaaS*. Nobody covers evidence discipline, nobody covers fail-closed local AI,
and nobody applies spec-driven governance to a real multi-tenant product. Free content compresses the
middle of the market, not the top — the $5,000 evals course treats the free version as its funnel.

### 5.2 The re-frame

Today's headline is "Build, ship and sell three kinds of AI product". The three-products framing invites
the critique reviewers gave the 1,600-alumni Vibe bootcamp — breadth over depth, no single guaranteed
outcome — and it is not the part with no competition.

Recommended: **"Ship AI products a skeptical engineer can audit"** — the method is the product; the
three repos are the proof that it works three times; the tracks are how a learner picks the archetype
they will actually sell. Concretely:

- the free lead product becomes the *tools*: the pointer lint, the facts-drift checker, a constitution/`AGENTS.md` audit script — artifacts that demonstrate the method on the learner's own repo in ten minutes;
- the sales page's proof section leads with the gate output and the drift table above, not the coverage badge;
- each track guarantees one shipped artifact (a notarized build, a live tenant URL, a published briefing), which answers "what do I leave with" better than a certificate.

### 5.3 The ladder, re-tiered

| Tier | Now | Recommended | Why |
|---|---|---|---|
| Free lead | 3-email teardown (unpublished) | The tools + the teardown, with email capture on the free site | Demonstrates the method; builds the list the launch plan assumes |
| Playbooks | — | $29–79 each, or an all-access annual | The audit names five modules that stand alone (§6.3); ui.dev sells the same shape at $495/yr |
| Track | $199 | $199, with a dated update window | Matches CodeFast/Small Bets; the Swift track is the uncontested wedge |
| Studio self-paced | $399 | $399 + "updates through Sept 2027" + changelog | Competes with year-long subscriptions only if freshness is visible |
| Cohort | $1,490 (founding $990) | Cohort #1 at $790–990; $1,490 after twenty named testimonials; consider a $2,000–2,500 tier with office hours and a course assistant | Observed mid band is $750–950; top band requires proof this course does not yet have |
| Team | $2,500–4,000 | Per-seat with a governance workshop | Credible against AI Makerspace's $3,200/seat group rate |

## 6. The platform: own it in three stages

Full matrix and sources in [`05-platform-build-options-2026.md`](05-platform-build-options-2026.md).
The pattern every developer-educator with public numbers uses — Comeau, Dodds, Pocock, Bos, Wathan —
is an own site, Stripe or a merchant of record, per-lesson progress, exercises that run on the learner's
machine, region-locked purchasing-power parity and team licences. None uses a hosted LMS.

**Stage 0 — sell now (1–2 weeks, ~$0–30/month).** Keep `build_site.py` and GitHub Pages as the free
copy, with an email form. Put the paid site and lab starters in a private repository and sell access
through Polar (5% + 50¢, merchant of record, auto-invites buyers to the repo). Add a
`.devcontainer/devcontainer.json` so labs open in Codespaces on the learner's free hours with Ollama.
Issue the SHA-bounded certificate as a page. Decide the licence.

**Stage 1 — the docs-site + paywall (three months).** Astro or Next.js rendering the existing Markdown;
Supabase or Clerk for identity; Polar or Paddle webhooks writing entitlements; per-lesson progress and
interactive quizzes in Postgres; Bunny or Mux signed playback if video is recorded; Open Badges 3.0 on
lab-gate pass. Borrow ideas from course-builder and epicshop, both open source. Fallback if the build
slips: Podia at $84/month with 0% fees.

**Stage 2 — the catalogue (twelve months).** Team seats with assignment, an all-access playbook
subscription, cohorts run on your own site with Discord and Zoom rather than Maven's 10–40%, quarterly
"current tooling" editions. Stripe Managed Payments once it is generally available if you want one
processor.

### 6.3 The content model that makes a catalogue possible

- **Facts manifest, not prose numbers.** `facts.json` is the single source; the drift checker names the files to edit; the decks template the values where the build can.
- **Editions, dependency-versioned.** `v2026.09` tags; a `CHANGELOG.md` surfaced on every sales page; a monthly changelog post. ai_qe already does this — copy its `release.yml` shape.
- **Primitives in the core, tools in appendices.** Spec, governance, evals, evidence, privacy boundary, pricing are the spine; Claude Code, Cursor, spec-kit, Ollama versions live in dated appendices refreshed quarterly.
- **Playbooks extracted from the modules the audit rated portable:** agent governance files + evidence log (M1.1/M1.3), fail-closed local-only mode (M3.1), competition table → falsifiable one-liner (M3.3), agent-executable spec checklist + drift checks (M4.2–4.3), multi-tenant negative-path test kit (M5.1–5.2), evidence-cited briefing (M6). Each is 40–60% repo-specific today; each becomes a sellable unit once the case-study material is an illustration rather than load-bearing.
- **Labs that AI cannot do for the learner.** The 2026 learning-science results (Anthropic's RCT: 17% lower concept scores when AI does the work; Bastani: guardrailed tutors avoid the harm) argue for a "first attempt before AI" rule in every lab and a deterministic autograder with an LLM only for narrative feedback.

## 7. Roadmap

Written as milestones in the repository's own style: each has a Definition of Done a reviewer can run.

### Milestone 5 — Make the course true again, and keep it true

- [ ] `check_facts.py --strict` passes: §0.2 re-pinned to the 2026-09-16 values, the "1.3.0" story rewritten as a dated record, the five drifted facts corrected in the files the checker names.
- [ ] `verify.py` checks `path:start-end` ranges (bounds, and a keyword within the range); `OllamaProvider.swift:99-119` and the Lab M3 inheritance fixed.
- [ ] The four numbers outside the whitelist corrected or cut ("33 modules", `CLAUDE.md` 143, "10 PDF editions", "~460 lines").
- [ ] Author machine paths removed from the four M4 artifacts and the three deep-reads.
- [ ] Lab M3 gains a step 0 that removes the shipped solution (or an `m3-start` branch); Lab M2's `make lab-m3` gate adjusted.
- [ ] Lab M5 ships the promised `mini-flow` starter with tests, or is re-budgeted honestly.
- [ ] Labs M1/M2 red-run templates match what the tooling produces.
- [ ] Quiz hygiene: M4 Q5, M2 Q3, M8 Q6, the invented "6/8", `Quiz 0/1/4` titles, 64 vs 72; the six recall short answers rewritten as application.
- [ ] M0: one duration, TinyCopilot moved to stretch, pass gate reconciled.
- [ ] Self-paced unblockers for Lab M4 (scripted stranger prompt) and Lab M6 (self-check alternative).
- [ ] `check_facts.py` added to the pre-cohort checklist in the instructor guide (done in this review) and to the gate once the clones are part of setup.

### Milestone 6 — The 2026 layer

- [ ] Evals as an eighth test tier in M3.2/M5.3 with a promptfoo lab; a red-team suite mapped to OWASP GenAI 2026.
- [ ] Prompt injection: a row in M3.1's claim → enforcement table and a transcript-injection test in Lab M3.
- [ ] Three-tier privacy policy (on-device / Private Cloud Compute / third-party cloud) with the 5.1.2(i) and DPLA §3.3.11(A) consent requirements, in M3.1 and M7.1.
- [ ] Spec-kit 1.0 command names and `converge`; `AGENTS.md` imported by `CLAUDE.md`; a hooks / rules / skills decision table in M1.1.
- [ ] METR 2025/2026 and DORA 2025 as the stated reason for governance in M1.
- [ ] M7: a worked cost floor and tier table for a Type 1 and a Type 2 product; per-seat / usage / outcome / hybrid / BYOK taxonomy.
- [ ] M6/M8: publishing for AI engines, Article 50 disclosure, a machine-readable edition manifest.
- [ ] Model matrix refreshed (Gemma 4 E-series, Qwen3.5-small, Phi-4-mini); Windows ML / ML Kit comparison.

### Milestone 7 — Sell (Stage 0)

- [ ] `LICENSE` decided and committed.
- [ ] Free site: email capture; the lead product published (tools + teardown).
- [ ] Private paid repository; Polar (or Paddle) product with repo-access benefit; the EU withdrawal waiver and button; VAT via the merchant of record.
- [ ] `.devcontainer/devcontainer.json` with Python 3.11, pytest, httpx and an Ollama service; `make lab-m2` green in Codespaces.
- [ ] Sales page: "What's included", "updates through <date>", a changelog, the drift table as proof; prices per §5.3.
- [ ] Gate portable: a Linux TTS fallback for the preview voice (or a committed silent manifest path), Chromium discovered from `PLAYWRIGHT_BROWSERS_PATH`.

### Milestone 8 — Own the platform (Stage 1)

- [ ] Docs-site + paywall: identity, entitlements from payment webhooks, per-lesson progress, interactive quizzes, transcripts from the narration text.
- [ ] Open Badges 3.0 issued on lab-gate pass, bound to the commit SHA the certificate already records.
- [ ] Purchasing-power parity by country table.
- [ ] Playbooks extracted from M1, M3, M4, M5, M6 as standalone products.

### Milestone 9 — The founding cohort as the evidence engine

- [ ] Cohort #1 at $790–990 with the testimonial trade; Discord for the cohort.
- [ ] Completion, refund and NPS recorded with stated denominators; the launch evidence log the plan already specifies, filled in.
- [ ] Pricing re-derived from actuals; $1,490 only after twenty named testimonials with artifact links.

## 8. What this review changed in the repository

- **New:** `06-production/check_facts.py` and `facts.json` — the facts-drift checker, advisory by default, `--strict` for the pre-cohort checklist; `make -C course facts` runs it.
- **New:** this review and the five research documents (`04`–`09`) in `00-research/`.
- **Edited:** the repository README (a "Review it" entry and an honest-status note on drift), the course README (package map), `06-production/MILESTONES.md` (Milestone 5 onward), and the instructor guide's upkeep checklist.
- **Not changed:** any module content, the gate's pass criteria, or the sales prices. Those are Milestone 5–7 work and each is a decision this document argues for rather than makes.

Everything above that was measured can be re-measured: `python3 course/06-production/check_facts.py`,
`python3 course/06-production/verify.py`, and `pytest` in the TinyCopilot folder. Everything cited can be
opened. Where a source was a vendor or a secondary blog, the research files say so — the same four
claim levels the course teaches, applied to the review of the course.
