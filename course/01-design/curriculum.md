# Curriculum: AI Product Studio (APS-3)

> Master syllabus and authoring brief. Learning objectives use measurable verbs (build, write, run, red-team, price). Every module = 3 lesson segments + 1 lab + 1 quiz. Written lessons are the master scripts for 5–15 minute videos.

## What ships with every module

Each of the nine module folders carries a complete eight-artifact package, bound by
[`content-standards.md`](content-standards.md):

| Artifact | File | Used for |
|---|---|---|
| Lesson | `lesson.md` | The master script for the three segments (record from `video-scripts.md`) |
| Lab | `lab.md` | The pass/fail checkpoint, with an objective acceptance checklist |
| Quiz | `quiz.md` | 8 questions (6 multiple choice + 2 short answer) with an answer key |
| Slides | `slides.md` | Marp deck, ≤6 bullets per slide, speaker notes on every slide |
| Solutions | `solutions.md` | Lab solutions, expected output, common wrong answers, grading notes |
| Video scripts | `video-scripts.md` | Timed per-segment recording scripts (hook → beats → action step) |
| Handout | `handout.md` | Printable one-page cheat sheet students keep |
| Facilitation | `facilitation.md` | 90-minute cohort session kit (timing, breakouts, watch-fors) |
| Glossary | `glossary.md` | 10–18 terms with "where it lives" pointers + curated resources |
| Rubrics | `lab-rubrics.md` | 4-level grading rubric per lab, weights summing to 100, auto-fail list |
| Accessibility | `accessibility.md` | Deck/code accessibility, transcript and caption rules, accommodations |

Verify the whole set with `python3 ../06-production/verify.py`.

## Course-level learning outcomes

By completion, a student can:

1. **Operate** a spec-driven, AI-assisted development loop (constitution → spec → plan → TDD build → tiered validation → evidence-recorded release) on a real project of their own.
2. **Build** a multi-role AI copilot core: model routing per role, context windowing, prompt builders as pure functions, proactive triggers, local LLM streaming (Ollama), with unit tests throughout.
3. **Engineer** privacy guarantees: fail-closed local-only mode, redirect rejection, truthful mode labels, and tests that prove each.
4. **Specify** a SaaS feature with the full spec-kit artifact set and **harden** it with multi-tenant tests (org_id isolation, RBAC, negative paths) plus playbook-based acceptance.
5. **Produce** an evidence-cited expertise artifact (mini-briefing) with provenance, audience routing, and edition discipline.
6. **Package and price** their product using competitive analysis (per archetype) and write a sales page + launch sequence for it.

## Module map

| Module | Title | Archetype/Track | Lab checkpoint (pass/fail artifact) |
|---|---|---|---|
| M0 | Orientation: Three Products, One Method | — | All 3 repos cloned; SignUpFlow solver runs on sample workspace; environment form posted |
| M1 | The AI Product Operating System | Method | Your starter repo with constitution.md, AGENTS.md, spec templates + one spec→plan→TDD mini-loop completed |
| M2 | The On-Device AI App: Architecture | Type 1 | TinyCopilot core passes its unit suite: 3 roles, 3 models, routed prompts, context window, question detection |
| M3 | The On-Device AI App: Privacy, Testing, Shipping | Type 1 | Local-only mode hardening tests + a real-LLM contract test + a 5-competitor comparison table pass review |
| M4 | The Spec-Driven SaaS: From Idea to Executable Spec | Type 2 | A complete spec-kit folder for one real feature passes the requirements checklist gate |
| M5 | The Spec-Driven SaaS: Multi-Tenant Security & Acceptance | Type 2 | Tenant-isolation negative-path tests + a playbook JSON fixture validated by a manifest |
| M6 | The Expertise Product: Evidence, Routing, Editions | Type 3 | A 12-slide mini-briefing with provenance table + two audience routes + an edition decision |
| M7 | Monetize: Pricing, Packaging, Positioning | All | A pricing worksheet + positioning one-liner + packaging page for the student's chosen product |
| M8 | Launch: Sales Page, Email Arc, Capstone | All | Capstone shipped (spec → build → validate → release) + sales page + 5-email launch mini-arc |

---

## M0 — Orientation: Three Products, One Method (~30 min)

**Objectives.** Students can describe the three AI product archetypes, name each case-study repo and its proof asset, run the SignUpFlow solver locally, and post a goal + environment note to the community.

- **M0.1 Why three types, and why these.** The three archetypes (native on-device AI app / spec-driven SaaS / expertise product); what "production-grade" means here (coverage badge, dated evidence line, provenance files). Action step: skim all three READMEs and write a two-sentence "which archetype is mine" note.
- **M0.2 The method you'll learn: the Spec-to-Ship Loop.** Study → Spec → Build → Validate → Release → Prove, previewed with one concrete artifact per stage from the three repos. Action step: save the loop diagram; keep a "loop journal" for the course.
- **M0.3 Set up and first win.** Clone all three repos; `poetry`/`make setup` for SignUpFlow; run `python -m api.cli.main init && solve` on the sample church workspace and capture the health score output; install Ollama + pull one small model (`qwen3:0.6b` or similar) and run one chat completion. Action step: post your solver output + goal to the community (the 2-minute first win that beats the "Module 2 chasm").

**Lab M0.** Environment setup with a verification checklist (git, Python 3.11+, Ollama, one model pulled; optional Xcode for the Swift stretch track). Pass = solver output screenshot/paste + `ollama list` shows ≥1 model.

**Quiz M0.** 8 questions on archetypes, proof assets, the loop stages.

---

## M1 — The AI Product Operating System (~60 min core + 2h lab)

**Objectives.** Students can write layered agent rules (constitution, AGENTS.md) that are imperative and verifiable; can run a spec → plan → TDD loop on a small feature; can record validation evidence honestly.

- **M1.1 Govern agents with a constitution and rule files.** Case study: SignUpFlow's stack — `.specify/memory/constitution.md` (85 lines, single source of truth), `AGENTS.md` (188 lines, universal baseline), `CLAUDE.md` (cross-reference + addenda), Copilot restatement; house style (imperative voice, every rule verifiable, <200 lines, runnable commands); the 5-level instruction hierarchy ("more specific and safer wins"); anti-hallucination rules ("grep the repo before referencing"); rule graduation pipeline (research-log observation → tested on real change → promoted rule → upstreamed).
- **M1.2 Spec → plan → tasks an agent can execute.** Case study: the spec-kit artifact set (spec.md with P1/P2/P3 independently-testable stories and Given/When/Then acceptance; research.md with numbered decisions; data-model.md; plan.md with Constitution Check gate; contracts/; quickstart.md; checklists; tasks.md with `[ID] [P?] [Story]` checkboxes citing exact file paths). ListenToMe's variant: design specs with protocol-level interfaces + YAGNI non-goals; implementation plans as 2,000+ line TDD task lists ending in a self-review mapping spec bullets to tasks.
- **M1.3 Evidence discipline: validation as a record, not a feeling.** SignUpFlow's "no CI — all local, evidence recorded" policy; the validation evidence format (commands, counts, date, environment, limitations, head SHA); "never fabricate a status check"; include the failures (validation.md records a browser timing race; mypy debt listed as "835 errors — not a pass"); ListenToMe's Definition-of-Done (verify in the installed app — "a permission toggle is not proof"; stale docs are a DoD failure); AI × QE's research-log Question/Checked/Outcome/Changed pattern.

**Lab M1. Build your operating system.** Create your own starter repo: `constitution.md` (≤80 lines, your principles + autonomy config), `AGENTS.md` (≤200 lines, verifiable rules, validation checklist), `specs/` with the templates provided in the course materials, `docs/research-log.md`. Then run one full mini-loop on a small feature (e.g., a CLI "todo" command): write spec.md (2 stories, Given/When/Then), plan, tasks, implement with TDD, record evidence in the prescribed format. Pass = all artifacts exist, tests pass, evidence recorded with command outputs.

**Quiz M1.** 8 questions: rule verifiability, hierarchy precedence, spec artifact purposes, evidence format, anti-hallucination rules.

---

## M2 — The On-Device AI App: Architecture (~75 min + 3h lab)

**Objectives.** Students can explain and implement: dual-source capture, transcription seams, a conversation store, context windowing, per-role model routing with streaming, pure prompt builders, and cheap proactive triggers — all testable without hardware.

- **M2.1 The capture→transcribe→context→prompt→route pipeline.** Case study: ListenToMe architecture — `ListenToMeCore` (pure SwiftPM package, 33 modules, 96% coverage) vs `App/` platform glue; the protocol seams (`AudioCapturing`, `Transcribing`, `LLMProvider`); three swappable transcription engines (SpeechAnalyzer default / legacy SpeechRecognizer / opt-in WhisperKit for code-switching); VAD segmentation (rms threshold + trailing silence); ConversationStore's rolling buffer with a character budget (default 4,000).
- **M2.2 Per-role model routing and prompt builders.** The three AI roles (Listener / Quick / Deep) each with its own model dropdown and "good for" hints; ModelRanking's local-first auto-defaults (Quick = fastest, Deep = strongest), token-prefix name matching, generation tokens so a model switch cancels stale streams; PromptBuilder as pure functions with three base system prompts (anti-preamble Quick; Listener "never invent an owner, deadline, agreement, or completion"; Deep = depth over brevity); 9 ResponseActions; preset persona guidance threading through every prompt; Listener→Quick/Deep grounding (only *completed* summaries are injected).
- **M2.3 Proactive intelligence without magic.** QuestionDetector's deliberately simple heuristic (trailing "?", interrogatives, phrase cues) + debounce; why the spec kept it swappable; the shared live-summary engine (5-second batches, eligibility threshold, response caps, serialized Quick/Summary/Deep reviews) as an example of resource-disciplined automation; OllamaProvider streaming details: NDJSON over `/api/chat`, in-stream error events, typed stream errors so truncated responses can't finish as success.

**Lab M2. Build TinyCopilot's core (Python + Ollama).** Provided starter: `tinycopilot/` skeleton with tests. Implement: (1) `ConversationStore` with `recent_context(max_chars)`; (2) `QuestionDetector` with debounce; (3) `PromptBuilder` (three role prompts + persona directive); (4) `OllamaProvider` (streaming chat via httpx or requests against localhost:11434, typed errors, injectable transport for tests); (5) `ModelRouter` with role defaults + local-first ranking from `/api/tags`; (6) `Copilot` orchestrator wiring roles to models with per-role cancellation on switch. All unit-tested with a mock LLM; `make lab-m2` runs the suite. Pass = all tests green, one transcript-driven demo run captured.

**Quiz M2.** 8 questions: pipeline order, role routing, prompt purity, streaming error types, debounce.

---

## M3 — The On-Device AI App: Privacy, Testing, Shipping (~75 min + 3h lab)

**Objectives.** Students can engineer a fail-closed local-only mode, write a real-LLM contract test that runs outside CI, enforce a coverage floor, and produce a sourced competitive analysis that doubles as positioning.

- **M3.1 Privacy is a mode, not a slogan.** Case study: ListenToMe's AIProcessingMode (off / local / cloud) with truthful labels ("Ollama Cloud — sends transcript and context"); adding a key never switches modes; `ModelPrivacy.isVerifiedLocal` fail-closed metadata verification on every request (`remote_host`/`remote_model` absent, format/model_info present — a localhost URL alone is insufficient because a local daemon can serve cloud aliases); localhost-only host enforcement; `RejectRedirects` delegate so meeting text can never be silently forwarded; local-first model auto-defaults; "AI off keeps capture working" as graceful degradation; honest trust boundaries ("trusts the installed local Ollama service and its metadata").
- **M3.2 Testing: floors, contracts, and what CI can't do.** The 95% coverage floor enforced by script in CI; three CI jobs (macOS build, iOS build, core tests) + dependency-lock diff; `make e2e` — a real LLM contract test through the actual provider against your local Ollama (CI can't reach a daemon or audio hardware); the manual smoke-test tier for what only a human can verify; the gap review that said "don't ship 1.3.0" despite 97% coverage — tests validate what you built, honesty validates what you shipped.
- **M3.3 Ship it: release discipline and competitive positioning.** Signed + notarized + stapled releases targeting the exact commit; dev/release bundle-id separation (macOS TCC keys grants by id + signing requirement); TestFlight distribution via API key; Definition-of-Done that ends at *published, verified* artifacts. Then: competition analysis as an engineering artifact — the 13-competitor table with sourced, qualified claims; the category taxonomy (bot-joiners / bot-free cloud capturers / genuinely on-device); positioning one-liner derived from an actual market gap ("the transparent, on-device, BYOK inverse of Cluely").

**Lab M3. Harden, prove, position.** (1) Add `PrivacyMode` + `verify_local_model()` to TinyCopilot: fail closed when metadata is missing, reject non-localhost hosts in local-only mode, refuse redirects; unit tests for each including the "local alias of a cloud model" red-team case. (2) Write `test_contract_real_llm.py` gated by `LAB_E2E=1` (skipped in normal runs): a real Ollama completion with a minimum-content assertion. (3) Add a coverage floor script (`fail_under`) wired into your test runner. (4) Produce a 5-competitor comparison table for *your* product idea with per-cell source URLs and uncertainty qualifiers. Pass = all tests incl. red-team case green; contract test passes locally; table reviewed by a peer (or self-reviewed against the course checklist).

**Quiz M3.** 8 questions: fail-closed design, why localhost isn't proof, redirect rejection rationale, coverage floor mechanics, positioning derivation.

---

## M4 — The Spec-Driven SaaS: From Idea to Executable Spec (~75 min + 3h lab)

**Objectives.** Students can run the complete spec-kit workflow for a real feature: specify → clarify → plan → checklist → tasks, producing artifacts a fresh agent session could execute without conversation context.

- **M4.1 The artifact pipeline in full.** Walk `specs/014-security-hardening/` end-to-end: spec.md (8 stories P1–P3, 44 FRs, Given/When/Then, edge cases, success criteria, open decisions); research.md (8 numbered decisions with options, pros/cons, rationale — Redis for rate limits, TOTP over SMS citing NIST deprecation, etc.); plan.md (technical context + the Constitution Check gate + `[NEW]`/`[MODIFY]` structure annotations + complexity-justification table); contracts/ (6 contract files ≈ 4,700 lines: config tables, class interfaces, error keys, test sketches, benchmarks); quickstart.md; checklists/requirements.md as the gate before planning. Honest gap: 014 has **no tasks.md** (its plan's Next Steps still lists Phase 2) — read the real task format from `.specify/templates/tasks-template.md` and `specs/000-user-onboarding/tasks.md` (`T017 [P] [US1] Implement create_wizard_state method in api/services/onboarding_service.py`: `[P]` marks parallelizable, `[US#]` ties to story, exact paths, tests-first phases).
- **M4.2 Spec quality: what makes an agent-executable spec.** Technology-agnostic WHAT vs implementation HOW; every story independently testable (an MVP slice); acceptance scenarios concrete enough to become tests; `[NEEDS CLARIFICATION]` markers resolved before planning (max 3 clarifying questions — ask early, not often); the checklist gate (no implementation leakage, all requirements testable); how tasks cite files so an agent with no conversation memory can implement; the Ralph-loop pattern (pick highest-priority incomplete spec → complete ALL acceptance criteria → report).
- **M4.3 From tasks to PR: the honest change record.** One PR per story; the PR body format (Summary / Changed files / Validation with commands+outcomes / Follow-ups); local code review checklist (correctness, security, org isolation, migrations, negative-path coverage; severity + file/line findings recorded; "missing review is not approval"); how generated artifacts drift and how to catch it (the renumbered spec path and mismatched priority counts the deep-read found — verify generated files like any other output).

**Lab M4. Spec a real feature.** Choose a real feature for *your* SaaS (suggested: "availability time-off" or "invitation links" in a SignUpFlow-style app — students building other products spec their own). Produce the complete folder: spec.md (≥3 stories with Given/When/Then + ≥8 FRs + success criteria), research.md (≥3 numbered decisions with rejected alternatives), data-model.md, plan.md (with an explicit Constitution Check), one contract file, quickstart.md, checklists/requirements.md, tasks.md (checkbox tasks with exact file paths, tests first). Pass = the folder survives the requirements checklist gate; a peer (or the instructor in the cohort tier) can implement story 1 from tasks.md alone.

**Quiz M4.** 8 questions: artifact responsibilities, checklist gate rules, task format, research decision format.

---

## M5 — The Spec-Driven SaaS: Multi-Tenant Security & Acceptance (~75 min + 3h lab)

**Objectives.** Students can enforce tenant isolation with tests, separate permissions from qualifications, make an authorization matrix executable, and design playbook acceptance with a coverage manifest.

- **M5.1 Multi-tenancy as a P0 cultural rule.** "Every database query MUST filter by org_id — a missing filter is a cross-tenant data leak, a P0 bug" (AGENTS.md); `verify_org_member(person, org_id)` enforcement; never read user state from the request body; atomic org bootstrap (`/auth/signup` creates org + first admin, rejects existing ids); invitation-only growth; tenant-bound credentials (token carries person `sub` + `org_id`; both revalidated); deliberate status semantics (401 invalid bearer / 403 missing or foreign org / 404 guessed id inside your tenant — no existence leak).
- **M5.2 RBAC done right: permissions ≠ qualifications.** Exactly one permission role (`volunteer` or `admin`); scheduling qualifications (usher, coach) live in the same array but are never permissions — "do not grant admin access merely because someone leads a ministry"; normalization via `normalize_roles`; the executable authorization matrix: `route_auth_policy.py` classifies every route, a test compares it to the live route table and fails on drift; the 6-step change protocol from `API_AUTHORIZATION.md`.
- **M5.3 Acceptance: seven tiers, playbooks, and an honest manifest.** The tier pyramid (unit with mocked auth / API+security with real JWT / CLI / integration real DB / web HTMX / contract OpenAPI snapshots / browser Playwright), dated evidence "1,464 passed / 21 skipped (2026-09-12)"; playbook acceptance: six-week church and basketball scenarios as operational drills with actors and disruption criteria (block both worship leaders → publication rejected, prior roster stays live); JSON fixtures parameterized through API and browser tiers at 360px/1440px with an independent oracle (exact role counts, distinct qualified assignees, non-overlap, balanced loads); `coverage.json` — a machine-readable manifest with honest statuses (automated/partial/manual/blocked) validated by pytest *before* collection so a removed scenario fails the run; the solver case study: a 357-line greedy heuristic (health score, fairness stdev, change-minimization weight) whose evolution traces spec → code comment → oracle.

**Lab M5. Isolate and accept.** Working from the provided `mini-flow` FastAPI starter (or their own SaaS): (1) add `org_id` isolation to two resources + `verify_org_member`; write real-JWT tests proving a member cannot read/write another tenant's rows (and that a forbidden write leaves the DB unchanged); (2) add a qualifications field and prove with a test that a qualification does not confer admin rights; (3) write a route policy table + a drift test against the live route table; (4) author one playbook JSON fixture (roles, headcounts, one disruption drill) + a tiny manifest and a validator that fails when a required scenario is removed. Pass = all tests green including negative paths; the drift test catches a deliberately miswired route; manifest validation fails on a removed scenario (students demonstrate each failure mode, then fix).

**Quiz M5.** 8 questions: P0 rule, permission/qualification separation, status-code semantics, playbook oracle properties, manifest honesty.

---

## M6 — The Expertise Product: Evidence, Routing, Editions (~75 min + 2.5h lab)

**Objectives.** Students can turn research into a trustworthy sellable artifact: claims with provenance and epistemic labels, one body of research routed to multiple audiences, content under release discipline, and a consulting-style funnel.

- **M6.1 Credibility is the product.** Case study AI × QE: research conventions ("the citation is the evidence"; every benchmark record carries date, sample, method, unit, self-reported-vs-measured, sponsor, and what claim it supports); the research log (Question/Checked/Outcome/Changed + explicit "Not verified" lists); provenance files (SHA-256 retrieval manifests, image-prompt provenance, voice provenance); the four levels of "saving" (task efficiency / released capacity / hard-dollar / total-spend — "mixing them is the most common error in AI business cases"); the signature qualifier ("planning inputs are not observed client results"); publishing your own audit (14-finding site audit → remediation table with verification).
- **M6.2 One research base, many audiences.** 116 slides re-cut into 4 decks (executive/technical × strategy/implementation); guided routes over stable slide IDs ending on a decision discussion ("sell the decision, not the transformation" — "the decision requested is whether to fund Phases 0 and 1, not whether to transform QA"); shareable route links; the sales-meeting script (Align 5 / Explore 15 / Agree 10); the questionnaire as lead qualification (role-routed, one form, single-select on the three questions that define success; the post-mortem of the failed 29-question/186-option form).
- **M6.3 Content as code.** Editions (site version vs slide edition vs questionnaire edition — "public content changes require a new edition before deployment"; changelogs record what was retained); `make check` = models → build → site → browser with five QA groups across two engines and three viewports; narration-hash review gates ("never reset the baseline to silence a stale-review failure"); immutable releases ("an existing published edition is never overwritten"); the phased pilot model with go/no-go gates, cost ceilings, and benefits-realization registers — how to sell measurement instead of outcomes.

**Lab M6. Build a mini-briefing.** Pick a topic the student actually knows (or use the provided AI-testing-evidence dataset from the repo reports). Produce: (1) a `research-log.md` with ≥6 dated entries (≥2 marked not-verified/open); (2) a provenance table: every claim → source URL, retrieval date, claim-type label; (3) a 12-slide outline where each slide cites ≥1 provenance row; (4) two audience routes over the same slides (executive: 6 slides ending in a decision; technical: 10 slides with the supporting evidence); (5) an edition decision record for a hypothetical v2 change. Pass = table reconciles (every slide claim has a row); routes end appropriately; one peer review confirms no uncited quantitative claim.

**Quiz M6.** 8 questions: claim levels, provenance requirements, route design, edition discipline, pilot gates.

---

## M7 — Monetize: Pricing, Packaging, Positioning (~60 min + 2h lab)

**Objectives.** Students can price a product per archetype using competitive evidence, choose packaging and platforms deliberately, and write honest marketing claims that convert.

- **M7.1 Pricing the three archetypes.** Type 1 (apps): one-time vs subscription tradeoffs from the ListenToMe competitive table (MacWhisper ~$69 one-time vs Granola ~$14–35/user/mo vs Cluely $19.99–149.99/mo) — the "privacy + BYO model + open-source" wedge and what it implies about who pays (reputation funnel, support, Pro tiers); Type 2 (SaaS): per-seat tiers, feature-gating risky paths until proven (billing/SMS 404-gated in SignUpFlow), the invitation-growth pattern; Type 3 (expertise): the AI × QE funnel (free evidence site → questionnaire → fixed-fee discovery → capped pilot with go/no-go gates), pricing measurement not outcomes.
- **M7.2 Packaging and platforms.** Course-research benchmarks (self-paced vs cohort price ladders; platform tradeoffs: Maven/Thinkific/Teachables/Gumroad/Udemy caution); app-store vs direct distribution for Type 1; infra cost floors for Type 2 (SQLite→Postgres, feature flags); productized consulting for Type 3. The universal rule: price the transformation and the artifacts (live review, capstone feedback) — "a stack of recordings is not a course" (and the same is true of a stack of features/notes).
- **M7.3 Honest marketing that converts.** StoryBrand: the student is the hero, the product is the guide; sales-page anatomy from the research (transformation headline → who it's for/isn't → problem → per-module outcomes → instructor proof → testimonials → FAQ → price); qualified claims as conversion assets (AI × QE is *more skeptical than its audience* — and that's why it sells); the pricing worksheet: value anchor, floor (costs), comparator set, tier design, launch discount policy.

**Lab M7. Price and position your product.** For the product from Lab M2/M4/M6 (their choice): (1) a 5-competitor comparison table with sourced prices (extend M3's table to pricing columns); (2) a pricing decision: model, tiers, launch price, one-page rationale citing the table; (3) a positioning one-liner in the ListenToMe format (adjective wedge × differentiation × who); (4) a packaging page (what's in each tier). Pass = every price in the table has a source URL; rationale survives the "would a skeptical engineer pay this?" self-review; one-liner is specific enough to be falsifiable.

**Quiz M7.** 8 questions: archetype pricing patterns, feature-gating rationale, honest-claim rules, tier design.

---

## M8 — Launch: Sales Page, Email Arc, Capstone (~75 min + capstone)

**Objectives.** Students can write a converting sales page, run a small email launch arc, and — the capstone — ship a v1 of one product through the full Spec-to-Ship Loop with recorded evidence.

- **M8.1 The sales page.** Full walkthrough of the 8-section anatomy applied to each archetype; writing per-module outcome lines ("Week 3: run an LLM locally — you'll ship…"); proof assets you already own (repos, evidence lines, test badges); FAQ that answers real objections (time, level, refunds, "other courses failed me"); length guidance by price point (800–1,200 words under $200; 2,000–3,000 words for $500+/cold traffic).
- **M8.2 The launch arc.** The 7–10 email sequence (warmup: origin story, transformation proof, free tool → conversion: cart-open, objection teardown, testimonial, final call); the 42–55%-in-final-48-hours pattern and deadline ethics; revenue math (list × open × click × page-conversion × price) with a worked example; deliverability hygiene (SPF/DKIM/DMARC); where the beta-cohort discount fits (Maven's guidance: trade it for testimonials).
- **M8.3 Capstone: ship and demo.** Pick one archetype. Execute the full loop: spec → plan → TDD build → tiered validation → release (public repo + tag or deployed page) → evidence record → sales page + 5-email mini-arc (M7/M8 assets) → a 5-minute demo (recorded video or live, cohort mode). The capstone rubric (in `assessment-and-rubrics.md`) scores: artifact completeness, evidence honesty, test/quality discipline, positioning clarity, launch-readiness. Demo day (cohort) or peer-review exchange (self-paced) closes the course — this is the testimonial engine.

**Lab M8 = Capstone.** Pass = rubric ≥ 80% with no dimension below "meets"; evidence record included; public artifact link works.

**Quiz M8.** 8 questions: page anatomy, email sequence stages, launch math, capstone rubric dimensions.

---

## Assessment design (summary; details in `assessment-and-rubrics.md`)

- **Labs (60%):** pass/fail checkpoints; each lab's acceptance list is objective ("tests pass", "table reconciles", "route works").
- **Quizzes (20%):** 8 auto-gradable questions per module (72 questions total), answer keys included in each quiz file.
- **Capstone (20%):** rubric-scored, 5 dimensions, demo requirement.

## Course engineering notes (for the author/instructor)

- Lesson files are written as master scripts; for video, each segment (M#.#) is one 5–15 minute recording with its action step stated on screen at the end.
- Discussion prompt per module ships with the lab (community post template included in each lab file).
- Keep all repo file pointers exact — they are the course's provenance. If a repo changes, update pointers rather than paraphrasing from memory (the repos' own rule).
- The Swift stretch track: M2/M3 labs have a companion "same lab in Swift" appendix pointing at the actual ListenToMeCore files (MockLLMProvider, PromptBuilderTests, ModelPrivacy) for students on Mac.