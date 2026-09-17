# Master Glossary

> Merged from the nine module glossaries by `build-glossary.py` (re-run it after editing any
> module glossary). Duplicate terms keep the most detailed definition and list every module
> that uses them. "Where it lives" pointers resolve in the cloned case-study repos.

**137 terms** across 9 modules · **13 shared** by more than one module.

| Module | Terms contributed |
|---|---|
| M0 — orientation | 19 |
| M1 — operating system | 15 |
| M2 — ondevice app | 16 |
| M3 — privacy ship | 16 |
| M4 — spec driven saas | 18 |
| M5 — security tests | 18 |
| M6 — expertise product | 16 |
| M7 — monetize | 18 |
| M8 — launch capstone | 18 |

## Shared vocabulary

The terms the course leans on repeatedly — learn these once and they carry across modules.

- **`:cloud` alias** *(M0, M3)* — An Ollama model name ending in `:cloud` that is backed by a hosted service rather than weights on your disk. Its presence means the daemon can reach a cloud model; it says nothing about where your text is processed. — `course/03-content/m02-ondevice-app/tinycopilot/README.md`
- **Benefits-realization register** *(M6, M7)* — The pricing-integrity device that ties every claimed saving to a Finance-owned budget row, so claims are reconciled by the client's own finance function rather than by the seller. Lives in `course/00-research/03-ai-qe-deep-read.md` §4.
- **Coverage floor** *(M0, M3)* — A hard CI gate that fails the build when total line coverage drops below a threshold; it buys enforcement against untested core logic and nothing else — `ListenToMe/scripts/check-coverage.sh`; `ListenToMe/.github/workflows/ci.yml:36-42`.
- **Edition** *(M0, M6)* — A named version of one content surface, tracked separately from the site version. Lives in `ai_qe/_data/release.yml` (`version`, `slide_edition`, `fintech_edition`, `questionnaire_edition`, `research_edition`).
- **Evidence record** *(M1, M5, M8)* — A dated, revision-pinned account of validation: commands with results, environment, head SHA, and an explicit list of what was not verified. (`SignUpFlow/docs/playbooks/validation.md`; template in `03-content/m01-operating-system/lesson.md`, §M1.3)
- **Fail-closed** *(M0, M3, M8)* — A local-only mode that rejects anything it cannot verify as local, rather than falling back to a cloud model. The Type 1 discipline artifact. *Where:* `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift`; `03-content/m08-launch-capstone/lesson.md` M8.3.
- **No-CI local validation** *(M1, M5)* — SignUpFlow's deliberate policy of running all review, analysis, migrations, tests, and artifact validation locally and recording evidence for the pushed revision instead of requiring hosted checks. (`SignUpFlow/.specify/memory/constitution.md`, "Current Validation Policy (2026-09-13)")
- **Proof asset** *(M0, M8)* — An artifact you already own that carries a page claim: a tagged repo, a dated evidence line, a coverage number, a spec folder, a provenance table, a demo. *Where:* `03-content/m08-launch-capstone/lesson.md` M8.1 inventory table.
- **Spec-kit** *(M0, M1, M4)* — GitHub's slash-command feature pipeline — constitution, specify, clarify, plan, checklist, tasks, analyze, implement — that produces a folder of artifacts under `specs/`. (`SignUpFlow/docs/SPEC_KIT_SETUP.md`)
- **Spec-to-Ship Loop** *(M0, M8)* — The six-stage method used in every module: Study → Spec → Build → Validate → Release → Prove, with a real artifact at each stage. — `course/00-research/00-synthesis.md`
- **Tenant isolation** *(M0, M8)* — Enforcing that every query and route is scoped to one organization, verified with negative-path tests using real JWTs. The Type 2 discipline artifact. *Where:* `SignUpFlow/docs/TESTING.md`; `03-content/m08-launch-capstone/lab.md`.
- **Test tier** *(M0, M3, M5)* — One layer of the test pyramid run in its own process. SignUpFlow documents seven tiers; the full local suite once recorded "1,464 passed, 21 skipped". — `SignUpFlow/docs/TESTING.md`; `SignUpFlow/docs/playbooks/validation.md`
- **YAGNI non-goals** *(M0, M1)* — An explicit list of what the product will not do, written into the design spec so scope cannot grow silently. ListenToMe: no cloud backend, accounts, billing, multi-user, and no covert mode. (`ListenToMe/docs/superpowers/specs/2026-06-18-listentome-design.md`, §2)

## All terms A–Z

### `

- **`:cloud` alias** *(M0, M3)* — An Ollama model name ending in `:cloud` that is backed by a hosted service rather than weights on your disk. Its presence means the daemon can reach a cloud model; it says nothing about where your text is processed. — `course/03-content/m02-ondevice-app/tinycopilot/README.md`
- **`[NEEDS CLARIFICATION]`** *(M4)* — The template's marker for an unresolved decision; the gate requires zero remaining before planning. — `SignUpFlow/.specify/templates/spec-template.md`.
- **`AudioCapturing` — the capture protocol seam** *(M2)* — Core declares what audio arrives; `App/` supplies `AVAudioEngine` and ScreenCaptureKit. `ListenToMe/Sources/ListenToMeCore/Capture.swift:4`.
- **`CopilotRole` — the three AI roles as an enum: `listener`, `quick`, `deep`** *(M2)* — Routing, prompts, and cancellation are all keyed by it. `ListenToMe/Sources/ListenToMeCore/CopilotRole.swift:5-7`.
- **`data-model.md`** *(M4)* — Entities with key fields and no implementation; present when a feature has traditional entities, absent when infrastructure spans many (as in 014). — `SignUpFlow/specs/000-user-onboarding/data-model.md`.
- **`LLMProvider` — the provider protocol seam** *(M2)* — Core streams text through it; `App/` implements it with Ollama over HTTP. `ListenToMe/Sources/ListenToMeCore/LLMProvider.swift:4`.
- **`plan.md`** *(M4)* — Owns HOW: languages, versions, storage, performance targets, project structure with `[NEW]`/`[MODIFY]` annotations. — `SignUpFlow/specs/014-security-hardening/plan.md`.
- **`PrivacyMode`** *(M3)* — The explicit three-way mode switch (`off`/`local`/`cloud`) a user picks; adding a cloud key never switches it — `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:3-13`; TinyCopilot mirror: `course/03-content/m02-ondevice-app/tinycopilot/src/tinycopilot/privacy.py:28-37`.
- **`PromptBuilder` — the pure prompt-construction layer** *(M2)* — A public enum of static functions: context in, request out, no I/O. `ListenToMe/Sources/ListenToMeCore/Prompt.swift`.
- **`research.md`** *(M4)* — Phase 0 decisions: options evaluated, rationale, and the rejected alternatives. — `SignUpFlow/specs/014-security-hardening/research.md`.
- **`tasks.md`** *(M4)* — Phase 2 output: checkbox tasks `[ID] [P?] [US#]`, tests first, exact file paths, checkpoints per story. — `SignUpFlow/specs/000-user-onboarding/tasks.md`.
- **`verify_local_model()`** *(M3)* — The fail-closed `/api/show` check: `remote_host` and `remote_model` absent, `details.format` and `model_info` present and non-empty — `course/03-content/m02-ondevice-app/tinycopilot/src/tinycopilot/privacy.py:93-135`.
### A

- **Acceptance criteria** *(M8)* — Concrete, testable conditions a story must satisfy, written Given/When/Then. The capstone's dimension 1 fails when criteria are vague. *Where:* `SignUpFlow/specs/014-security-hardening/spec.md`; `03-content/m08-launch-capstone/lab.md` step 2.
- **Acceptance gate** *(M5)* — The point where the product must be proven operable, not merely functional: playbook scenarios, disruption drills, and a manifest that admits unproven rows. (`SignUpFlow/docs/playbooks/coverage.json`; `docs/playbooks/church.md`)
- **Acceptance scenario** *(M4)* — A Given/When/Then statement inside a user story whose Then-clause is an observable, numeric outcome. — `SignUpFlow/specs/014-security-hardening/spec.md` (US1).
- **Adjective-wedge** *(M7)* — The leading adjectives of a positioning one-liner that carry the differentiator — the part a competitor would have to rebuild to match. Lives in the derived one-liner at `ListenToMe/docs/competition-analysis.md:80`.
- **AGENTS.md** *(M1)* — The cross-agent baseline rules file that tools such as Codex CLI, Cursor, Aider, Jules, OpenHands, Sourcegraph Amp, and Factory read natively. In SignUpFlow it is 188 lines and is restated or cross-referenced by the host-specific files. (`SignUpFlow/AGENTS.md`)
- **Anti-hallucination rules** *(M1)* — Prohibitions that make fabricated facts checkable: do not invent paths, names, commands, or identifiers; grep before referencing; read facts from the canonical source; offer 2–3 options when a request is ambiguous. (`SignUpFlow/AGENTS.md`, "Anti-hallucination")
- **Archetype** *(M0)* — One of the three product shapes this course builds: on-device app, spec-driven SaaS, expertise product. They differ in technical center of gravity, not in method. — `course/03-content/m00-orientation/lesson.md`
- **Authorization matrix (executable)** *(M5)* — A dict classifying every mounted route as public/ member/ admin, paired with a test that compares the dict to the live route table and to each route's dependency tree. (`SignUpFlow/api/route_auth_policy.py:8-171`; test in `tests/unit/test_api_route_auth_policy.py`)
- **Autonomy configuration** *(M1)* — The section of a constitution that fixes what an agent may do alone. SignUpFlow's: `YOLO Mode: DISABLED`, `Git Autonomy: ENABLED (Commit changes when done)`. (`SignUpFlow/.specify/memory/constitution.md`, "Autonomy Configuration")
### B

- **Benchmark record** *(M6)* — The unit of citable evidence: one finding plus date, sample, method, unit, self-reported vs measured, sponsor, and what claim it can support. Anything unverifiable is listed as such. Lives in `ai_qe/CONTRIBUTING.md`, "Research conventions"; examples in `ai_qe/docs/evidence/benchmarks.md`.
- **Benefits-realization register** *(M6, M7)* — The pricing-integrity device that ties every claimed saving to a Finance-owned budget row, so claims are reconciled by the client's own finance function rather than by the seller. Lives in `course/00-research/03-ai-qe-deep-read.md` §4.
- **Beta-discount trade** *(M8)* — A founding-cohort discount explicitly exchanged for a testimonial and a feedback session, agreed at checkout. Honest because the buyer knows what the discount buys. *Where:* `04-sales/pricing-and-platforms.md` (launch-price policy).
- **Bundle id / TCC** *(M3)* — macOS keys Microphone and Screen Recording grants by bundle id *plus* the binary's code-signing requirement, so a dev build and a release build need separate ids — `ListenToMe/docs/RELEASING.md:18-31`.
### C

- **Capped phased pilot** *(M7)* — The bounded engagement stage: 8–10 weeks, five phases (0–4), go/no-go gates signed by the sponsor, frozen acceptance criteria before results are observed. Lives in `ai_qe/_data/engagement.json` and `ai_qe/docs/method/phased-pilot.md`.
- **Cart open** *(M8)* — Email 4 and the moment the offer becomes purchasable; the course opens the cart for 10–14 days. The first email of the conversion phase. *Where:* `04-sales/launch-plan.md`.
- **Case study** *(M0)* — One of the three public repos used as worked examples throughout the course: ListenToMe, SignUpFlow, AI × QE. — `course/01-design/curriculum.md`
- **Claim level** *(M6)* — One of four labels that every number must carry: task-level efficiency, QA capacity released, hard-dollar saving, total software-spend impact. Lives in `ai_qe/docs/principles.md`; reproduced in `evidence-dataset.md`.
- **Comparator band** *(M7)* — The min–max price range of the rows in your own table that are genuinely comparable to your product. Lives in `lab.md` Step 2 (the worksheet template).
- **Complexity Tracking** *(M4)* — The plan table that must be filled *only* when the Constitution Check records a violation that needs arguing. — `SignUpFlow/.specify/templates/plan-template.md`.
- **Constitution** *(M1)* — The shortest and most authoritative governance file: the few principles that must never drift, plus the current validation policy. SignUpFlow's is 85 lines and sits above all agent instruction files. (`SignUpFlow/.specify/memory/constitution.md`)
- **Constitution Check** *(M4)* — The plan's per-principle compliance pass; the gate must pass before Phase 0 research and be re-checked after Phase 1 design. — `SignUpFlow/.specify/templates/plan-template.md`.
- **Constitution Check gate** *(M1)* — The explicit pass/fail checkpoint in `plan.md` that must pass before Phase 0 research and be re-checked after Phase 1 design. (`SignUpFlow/specs/014-security-hardening/plan.md`)
- **Content as code** *(M6)* — Running published content under the same discipline as software: tests, review gates, hashed media, editions and immutable releases. Lives in `ai_qe/Makefile` and `ai_qe/CONTRIBUTING.md`, "Release validation".
- **Context window (`recentContext`) — the character-budgeted slice of transcript sent to a prompt** *(M2)* — Newest-first fit, default 4,000 characters, never empty. `ListenToMe/Sources/ListenToMeCore/ConversationStore.swift:56-67`.
- **Contract** *(M4)* — A written interface between the session that designed a feature and the session that implements it: request/response shapes, error keys, key schemas, test sketch. — `SignUpFlow/specs/014-security-hardening/contracts/rate-limiting.md`.
- **Contract test** *(M3)* — A test that exercises the real seam a mock only assumes — here, NDJSON request shape and stream parsing against a live Ollama daemon — kept outside CI behind an environment gate — `ListenToMe/Tests/ListenToMeCoreTests/OllamaContractE2ETests.swift:4-22`.
- **Conversion phase** *(M8)* — The last four emails (cart open → objection teardown → proof → final call), which spend the trust the warmup phase earned. *Where:* `04-sales/launch-plan.md`; `00-research/02-course-market-research.md` §E.
- **Cost floor** *(M7)* — Your fixed monthly cost — hosting, API keys, amortized dev time — converted to the sales per month needed to break even. Lives in `course/04-sales/pricing-and-platforms.md`, "Cost floor."
- **Coverage floor** *(M0, M3)* — A hard CI gate that fails the build when total line coverage drops below a threshold; it buys enforcement against untested core logic and nothing else — `ListenToMe/scripts/check-coverage.sh`; `ListenToMe/.github/workflows/ci.yml:36-42`.
- **Coverage manifest** *(M5)* — A machine-readable file binding each scenario to actor, precondition, operation, expected result, tiers, evidence paths, and a status; pytest validates it before collection. (`SignUpFlow/docs/playbooks/coverage.json`; `tests/playbooks/plugin.py:37-45`)
- **Coverage status** *(M5)* — One of exactly four values — `automated`, `partial`, `manual`, `blocked` — coupled to tiers so a blocked row cannot masquerade as automated. (`SignUpFlow/tests/playbooks/coverage.py:19,43-46`)
- **Cross-tenant data leak** *(M5)* — One unfiltered query returning another organization's rows to a valid, authenticated user; SignUpFlow classifies it as a P0 bug. (`SignUpFlow/AGENTS.md:57,61`)
### D

- **Deadline honesty** *(M8)* — The rule that a launch deadline must describe a real change — the cart closes, the price ends — because a resetting or recurring deadline teaches the list to wait. *Where:* `04-sales/pricing-and-platforms.md` ("no fake countdowns").
- **Debounce — the minimum interval between proactive fires** *(M2)* — ListenToMe's default is 8 seconds. `ListenToMe/Sources/ListenToMeCore/ContextEngine.swift:8,31-40`.
- **Definition of Done** *(M3)* — Release as the default end of any fix: published, notarized, and verified by downloading the artifact and checking its checksum — `ListenToMe/AGENTS.md`; `ListenToMe/docs/RELEASING.md:11-16`.
- **Definition of Done (DoD)** *(M1)* — The standard for "shipped," not "built": verify the affected behavior in the installed production app, and treat stale docs as a failure rather than a follow-up. (`ListenToMe/AGENTS.md`, `ListenToMe/CLAUDE.md`)
- **Deletion test** *(M7)* — Remove one clause from a positioning one-liner; if no row in your table would notice the sentence became false, the clause is decoration and gets cut. Lives in `lesson.md` M7.3.
- **Deliverability** *(M8)* — Whether email reaches the inbox at all; configured through SPF, DKIM, and DMARC on the sending domain, enforced by Gmail and Yahoo for bulk senders. Upstream of every conversion number. *Where:* `04-sales/launch-plan.md` (header and ops checklist).
- **Dependency-lock diff** *(M3)* — The CI step that fails a build when the checked-in dependency lock and the generated workspace's resolved lock drift apart — `ListenToMe/.github/workflows/ci.yml:24, 35`.
- **Disruption drill** *(M5)* — A scenario that breaks the happy path on purpose and specifies what rejection must look like, such as CH-04's blocked worship leaders and rejected publication. (`SignUpFlow/docs/playbooks/church.md:73`)
- **Drift** *(M4)* — A generated artifact disagreeing with the source it was generated from; three verified cases exist in SignUpFlow. — `SignUpFlow/specs/000-user-onboarding/tasks.md` (line 3).
### E

- **Edition** *(M0, M6)* — A named version of one content surface, tracked separately from the site version. Lives in `ai_qe/_data/release.yml` (`version`, `slide_edition`, `fintech_edition`, `questionnaire_edition`, `research_edition`).
- **Epistemic label** *(M6)* — The status of a number: measured / self-reported / vendor-affiliated / illustrative. Lives on the slide itself, per the wording rules in `ai_qe/docs/economics/slide-language.md`.
- **Evidence log** *(M0)* — The dated, append-only record of commands and outputs a student keeps all course; it becomes the capstone's evidence record. — `course/03-content/m00-orientation/lab.md`
- **Evidence record** *(M1, M5, M8)* — A dated, revision-pinned account of validation: commands with results, environment, head SHA, and an explicit list of what was not verified. (`SignUpFlow/docs/playbooks/validation.md`; template in `03-content/m01-operating-system/lesson.md`, §M1.3)
### F

- **Fail-closed** *(M0, M3, M8)* — A local-only mode that rejects anything it cannot verify as local, rather than falling back to a cloud model. The Type 1 discipline artifact. *Where:* `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift`; `03-content/m08-launch-capstone/lesson.md` M8.3.
- **Feature gating** *(M7)* — Registering paid routes in the codebase but returning 404 behind a flag until the workflow they depend on is trustworthy. Lives in `SignUpFlow/README.md`, "Provider-backed Features," and `SignUpFlow/AGENTS.md`.
- **Financial-capture set** *(M6)* — The questionnaire questions the failed form omitted: budget ownership, variable share of spend, renewal windows, what happens to released capacity, and what Finance will recognise as a saving. Lives in `ai_qe/docs/method/discovery-questionnaire.md`.
- **Fixed-fee discovery** *(M7)* — A bounded first paid engagement that qualifies budget and sponsor before any larger commitment. Lives in `ai_qe/_data/engagement.json` (commercial field).
- **Fraction-of-live-price rule** *(M7)* — Self-paced prices at 70–85% of the live tier only if projects, async feedback, and community are retained; otherwise a bare library should not be sold at all. Lives in `course/00-research/02-course-market-research.md` §C.
- **Functional requirement (FR)** *(M4)* — A numbered "System MUST…" statement, technology-agnostic; 014 has 44. — `SignUpFlow/specs/014-security-hardening/spec.md`.
### G

- **Generation token — a per-role counter that invalidates an in-flight stream** *(M2)* — Switch a model, bump the token, and the old stream's deltas stop being written. `ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:119-132,513-578`.
- **Go/no-go gate** *(M6)* — A sponsor-signed decision boundary with a cost ceiling, a stop rule and frozen criteria. Lives in `ai_qe/docs/method/phased-pilot.md`; the exact numbers live in `ai_qe/_data/pilot_gates.json`.
- **Graceful degradation** *(M3)* — Turning AI off leaves capture, transcription, and saving working; the app degrades, it does not stop — `ListenToMe/README.md`, "AI processing mode".
- **Guided route** *(M6)* — A curated sequence over stable slide IDs, with a declared `closing` slide, that reorders and omits but never rewrites. Lives in `ai_qe/_data/briefing_routes.json`.
### H

- **Health score** *(M0)* — The solver's 0–100 quality metric for a generated roster, printed by `api.cli.main solve`. On the sample workspace it is `100.0/100`. — `SignUpFlow/README.md`
- **Honest-marketing checklist** *(M7)* — Five rules every sales asset must pass: sourced numbers, qualified claims, no invented testimonials, plain refund/deadline policies, price the transformation. Lives in `course/04-sales/pricing-and-platforms.md`.
### I

- **Immutable release** *(M6)* — A published edition that is never overwritten; a new one is cut instead. Lives in `ai_qe/CONTRIBUTING.md` and `ai_qe/releases.md`.
- **Independent oracle** *(M5)* — A check that recomputes correctness from the produced artifact rather than asking the producer: exact role counts, distinct qualified assignees, non-overlap, balanced loads. (`SignUpFlow/docs/playbooks/README.md:37-38`)
- **Independent Test** *(M4)* — The per-story line proving a story is a viable MVP slice on its own. — `SignUpFlow/.specify/templates/spec-template.md`.
- **Instruction hierarchy** *(M1)* — The five-level precedence order for overlapping rules, with one tie-breaker: follow the more specific and safer one. (`SignUpFlow/AGENTS.md`, "Agent instruction hierarchy")
- **Invitation-only growth** *(M5)* — Signup atomically creates an organization and its first admin and never joins an existing one; later accounts arrive through administrator-created, single-use invitations. (`SignUpFlow/AGENTS.md:59`; BO-02 in `docs/playbooks/coverage.json`)
### L

- **Launch evidence log** *(M8)* — The record of actual list size, delivery, opens, clicks, conversions by email, and revenue, kept so the next revenue model is derived from observations. *Where:* `04-sales/launch-plan.md` (metrics to record).
- **Lead product** *(M8)* — The free asset that builds the list before the arc runs; the course uses a 30-minute AI product teardown. *Where:* `04-sales/launch-plan.md` (the free lead product).
- **Local model** *(M0)* — A model whose weights run on your machine. In M0 the example is `qwen3:0.6b`; the point of pulling one is that no API key and no cloud bill are involved. — `course/03-content/m00-orientation/lesson.md`
- **Local-first defaults — auto-selection that filters cloud aliases out first** *(M2)* — Cloud is chosen only when no local model exists. `ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:76-94`.
- **LOCAL_HOSTS / loopback allowlist** *(M3)* — The only hosts local-only mode trusts: `localhost`, `127.0.0.1`, `::1`. Anything else throws before a prompt is written — `ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:106-108`.
- **Loop journal** *(M0)* — The single file, started in M0.2, where a student records one line per loop stage touched by each action step. — `course/03-content/m00-orientation/lesson.md`
### M

- **Manual smoke test** *(M3)* — The tier that covers mic capture, system audio, and live speech-to-text, all of which need a GUI session and manual permission grants — a numbered, repeatable script — `ListenToMe/docs/manual-smoke-test.md:1-7`.
### N

- **NDJSON — newline-delimited JSON, Ollama's streaming format** *(M2)* — One JSON object per line carrying a delta or `done: true`. `ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:120-139`.
- **Negative-path test** *(M5)* — A test that asserts the denial and its status code, not the success case: the seven cases in `03-content/m05-security-tests/solutions.md` step 1. (`SignUpFlow/docs/API_AUTHORIZATION.md:21-24`)
- **No-CI local validation** *(M1, M5)* — SignUpFlow's deliberate policy of running all review, analysis, migrations, tests, and artifact validation locally and recording evidence for the pushed revision instead of requiring hosted checks. (`SignUpFlow/.specify/memory/constitution.md`, "Current Validation Policy (2026-09-13)")
- **Not-verified list** *(M6)* — Explicit published list of claims that could not be confirmed, kept alongside the verified ones. Lives in `ai_qe/docs/research-log.md`.
### O

- **On-device** *(M0)* — Processing that happens on the user's hardware, so audio or text need not leave the machine. ListenToMe is the on-device case study. — `ListenToMe/README.md`
- **One CTA** *(M8)* — Exactly one call to action, repeated verbatim wherever it appears. Two competing buttons give the reader a way to do nothing. *Where:* `04-sales/landing-page.md` (hero, pricing, final call).
- **One-time pricing** *(M7)* — Charging once because per-user marginal cost does not recur — the on-device pattern. Exemplified by the MacWhisper row, `ListenToMe/docs/competition-analysis.md`.
### P

- **P0 bug** *(M5)* — The severity SignUpFlow assigns to a missing `org_id` filter: not a triage negotiation, a query that does not ship. (`SignUpFlow/AGENTS.md:61`)
- **Per-seat pricing** *(M7)* — Pricing a SaaS by seat so the unit of price scales with the organization's adoption. Lives in `lesson.md` M7.1, grounded in `SignUpFlow/README.md`'s invitation flow.
- **Permission role** *(M5)* — What an account may do; exactly one of `admin` or `volunteer`, enforced by a frozenset and by a normalization rule that refuses two roles. (`SignUpFlow/api/roles.py:8,38-53`)
- **Persona directive — preset guidance appended to every role's system prompt** *(M2)* — Same code path for manual panes and automatic reviews. `ListenToMe/Sources/ListenToMeCore/Prompt.swift:159-173`.
- **Phase 0 / Phase 1** *(M4)* — Research (decisions with receipts) and design (data-model, contracts, quickstart) phases of a feature. — `SignUpFlow/specs/014-security-hardening/plan.md`.
- **Positioning one-liner** *(M7)* — A single sentence in the form adjective-wedge × differentiators × audience, derived clause by clause from a comparison table. Lives in `lesson.md` M7.3.
- **Proactive gate — the four conditions before a proactive answer fires** *(M2)* — Finalized, from `.others`, passes question detection, outside the debounce window. `ListenToMe/Sources/ListenToMeCore/ContextEngine.swift:31-40`.
- **Proof asset** *(M0, M8)* — An artifact you already own that carries a page claim: a tagged repo, a dated evidence line, a coverage number, a spec folder, a provenance table, a demo. *Where:* `03-content/m08-launch-capstone/lesson.md` M8.1 inventory table.
- **Protocol seam — a protocol the pure core declares and platform glue implements** *(M2)* — The three are `AudioCapturing`, `Transcribing`, `LLMProvider`; they are what let tests run without hardware.
- **Provenance** *(M0)* — The traced origin of a claim: source, retrieval date, and claim type. Every AI × QE claim carries it, and M6 requires it of student briefings. — `ai_qe/README.md`
- **Provenance manifest** *(M6)* — Record of every retrieval with URL, retrieval date, status and SHA-256 hash — including failures. Lives in `ai_qe/research/document-manifest.json`; images in `ai_qe/research/visual-provenance.md`; voice in `ai_qe/assets/data/narration-provenance.json`.
### Q

- **Qualification** *(M5)* — What a person can do (`usher`, `coach`, `worship_leader`, `sound`); stored in the same `roles` array as permission roles but never interpreted as authority. (`SignUpFlow/api/roles.py:12`; `docs/playbooks/church.md:26`)
- **Qualified claim** *(M7)* — A claim that carries both its source and its limitation, so a buyer can audit it. Lives in `course/00-research/03-ai-qe-deep-read.md` §3 ("planning inputs are not observed client results").
### R

- **Ralph loop** *(M4)* — The constitution's Context A: an agent picks the highest-priority incomplete spec, completes *all* acceptance criteria, and reports `<promise>DONE</promise>`. — `SignUpFlow/.specify/memory/constitution.md`.
- **Redirect refusal (`RejectRedirects`)** *(M3)* — A transport that refuses every 3xx instead of following it, so meeting text can never be silently forwarded — the Swift URLSession delegate is `ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:151-157`; the Python twin builds httpx with `follow_redirects=False` and raises on 3xx in `course/03-content/m02-ondevice-app/tinycopilot/src/tinycopilot/ollama_provider.py:45-78`.
- **Reputation funnel** *(M7)* — The marketing surface a free or open-source product runs on: code, README, coverage badge, published competitor analysis, support, and a Pro tier. Lives in `course/01-design/curriculum.md`, M7.1.
- **Research log** *(M6)* — The dated intake queue where a claim enters before it can reach a page: Question / Checked / Outcome / Changed. Lives in `ai_qe/docs/research-log.md`.
- **Reserved testimonial slot** *(M8)* — A labeled, empty testimonial placeholder with an honesty note, used instead of inventing social proof. The course's page reserves three in before/after/result format. *Where:* `04-sales/landing-page.md` (testimonials).
- **Resource enumeration** *(M5)* — Mapping which resources exist by observing error codes; defeated by loading target rows through the actor's organization so foreign and absent ids both return `404`. (`SignUpFlow/docs/API_AUTHORIZATION.md:23`; `api/dependencies.py:61-66`)
- **Reviewed head SHA** *(M5)* — The revision a local review and its evidence are bound to; changing source invalidates stale evidence and forces a recheck. (`SignUpFlow/docs/ai-pr-review.md`, Local Review Checklist items 1 and 5)
- **Rule graduation** *(M1)* — The pipeline by which an observation becomes a rule: recorded in `docs/research-log.md`, tested on a real change, then promoted into `AGENTS.md` or a per-agent file. (`SignUpFlow/docs/ai-agent-coding-strategy.md`)
### S

- **Sales-page anatomy** *(M7)* — The eight-section structure: transformation headline, who it's for/isn't, problem and stakes, per-module outcomes, instructor proof, testimonials, FAQ, transparent pricing with one CTA. Lives in `course/00-research/02-course-market-research.md` §E.
- **Self-review mapping** *(M1)* — A closing section of an implementation plan that maps every spec bullet to the tasks that satisfy it, so nothing silently drops. (`ListenToMe/docs/superpowers/plans/2026-06-18-listentome-mvp.md`)
- **Signature qualifier** *(M6)* — The one sentence that labels the whole product: "Planning inputs and proposed outcomes are not observed client results." Lives in `ai_qe/README.md`.
- **Skeptical-engineer test** *(M7)* — Lab M7 Step 5: the three toughest objections your own table invites, each answered with a named row or a repo pointer. Lives in `lab.md` Step 5.
- **Spec (the WHAT)** *(M1)* — The technology-agnostic statement of what users need: prioritized, independently testable stories with Given/When/Then acceptance scenarios and success criteria. (`SignUpFlow/specs/014-security-hardening/spec.md`)
- **Spec folder** *(M4)* — A self-contained instruction set for one feature (`spec.md`, `research.md`, `plan.md`, `contracts/`, `tasks.md`, …); SignUpFlow has 17 under `specs/`. — `SignUpFlow/specs/`.
- **Spec-kit** *(M0, M1, M4)* — GitHub's slash-command feature pipeline — constitution, specify, clarify, plan, checklist, tasks, analyze, implement — that produces a folder of artifacts under `specs/`. (`SignUpFlow/docs/SPEC_KIT_SETUP.md`)
- **Spec-to-Ship Loop** *(M0, M8)* — The six-stage method used in every module: Study → Spec → Build → Validate → Release → Prove, with a real artifact at each stage. — `course/00-research/00-synthesis.md`
- **Stable slide ID** *(M6)* — The invariant slide number that routes and shared links resolve against, so a route can reorder without breaking a link. Lives in `ai_qe/_data/briefing_room.json` outlines.
- **StoryBrand stance** *(M8)* — The positioning rule that the student is the hero and the instructor is the guide; write "you will ship," not "I will teach." *Where:* `00-research/02-course-market-research.md` §E.
- **Stranger test** *(M4)* — The one quality test: a fresh agent session with zero conversation memory could implement from the artifacts alone. — `course/03-content/m04-spec-driven-saas/lesson.md` (M4.2).
- **Success criteria (SC)** *(M4)* — Measurable, technology-agnostic outcomes; 014 has 12. — `SignUpFlow/specs/014-security-hardening/spec.md`.
- **Sufficient evidence** *(M6)* — A result whose confidence interval does not cross the relevant decision boundary. A point estimate alone is never sufficient; lives in `ai_qe/docs/method/phased-pilot.md`.
### T

- **Task line** *(M1)* — An executable entry in `tasks.md` in `[ID] [P?] [Story]` format with an exact file path and tests first. Real example: "T027 [US1] Implement POST /api/sms/send endpoint per contracts/sms-api.md in api/routers/sms.py". (`SignUpFlow/specs/019-sms-notifications/tasks.md`)
- **Tenant isolation** *(M0, M8)* — Enforcing that every query and route is scoped to one organization, verified with negative-path tests using real JWTs. The Type 2 discipline artifact. *Where:* `SignUpFlow/docs/TESTING.md`; `03-content/m08-launch-capstone/lab.md`.
- **Tenant-bound credential** *(M5)* — A JWT or session carrying both the person `sub` and the `org_id`, both required, and reloaded against an active membership before the request proceeds. (`SignUpFlow/api/dependencies.py:78-121`; `docs/API_AUTHORIZATION.md:28-33`)
- **Test tier** *(M0, M3, M5)* — One layer of the test pyramid run in its own process. SignUpFlow documents seven tiers; the full local suite once recorded "1,464 passed, 21 skipped". — `SignUpFlow/docs/TESTING.md`; `SignUpFlow/docs/playbooks/validation.md`
- **Token-prefix matching — capability markers matched at a token start, never as a substring** *(M2)* — Prevents `gemini` from being demoted as `mini`. `ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:13-18`.
- **Transformation headline** *(M8)* — A one-sentence, falsifiable statement of the destination, not the contents. The first of the eight sections. *Where:* `00-research/02-course-market-research.md` §E; `04-sales/landing-page.md`.
- **Trust boundary** *(M3)* — The honest edge of a guarantee. Local-only mode trusts the installed local Ollama service and its metadata; it verifies a self-description, not the daemon itself — `ListenToMe/README.md`, "Privacy".
- **Truthful mode label** *(M3)* — A label that names where data goes rather than how good the feature is — e.g. "Ollama Cloud — sends transcript and context" — `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:3-13`.
- **Typed stream errors (`OllamaStreamError`) — the failure model for streaming** *(M2)* — `.server` for an in-stream error event, `.incomplete` when `done` never arrives, `.empty` when no visible text arrives. `ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:67-83,159-170`.
### V

- **VAD — voice activity detection that finds utterance boundaries** *(M2)* — 37 lines: RMS energy, a 0.02 threshold, 0.8 seconds of trailing silence. `ListenToMe/Sources/ListenToMeCore/VAD.swift`.
- **Value anchor** *(M7)* — What your product replaces — hours, headcount, or a tool subscription — expressed as a comparable amount. Lives in `lab.md` Step 2.
- **Verified local** *(M0)* — A local model accepted only after metadata proves it is not remote-backed: `remote_host`/`remote_model` absent, format/model-info present. A `localhost` URL alone is not proof. — `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift`
- **Verified local — a fail-closed metadata check, not a hostname check** *(M2)* — `isVerifiedLocal` rejects a model unless `remote_host` and `remote_model` are absent. `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:17`.
### W

- **Warmup phase** *(M8)* — The first three emails (origin story → transformation proof → free tool), which earn trust and make no sales ask. *Where:* `04-sales/launch-plan.md`.
### Y

- **YAGNI non-goals** *(M0, M1)* — An explicit list of what the product will not do, written into the design spec so scope cannot grow silently. ListenToMe: no cloud backend, accounts, billing, multi-user, and no covert mode. (`ListenToMe/docs/superpowers/specs/2026-06-18-listentome-design.md`, §2)
