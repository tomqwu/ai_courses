# M4 Glossary — Spec-Driven SaaS

> Every "where it lives" pointer resolves in the workspace root, where `course/`, `SignUpFlow/`,
> `ListenToMe/` and `ai_qe/` are siblings. SignUpFlow paths are relative to `SignUpFlow/`.

- **Acceptance scenario** — A Given/When/Then statement inside a user story whose Then-clause is an
  observable, numeric outcome. — `SignUpFlow/specs/014-security-hardening/spec.md` (US1).
- **Complexity Tracking** — The plan table that must be filled *only* when the Constitution Check records
  a violation that needs arguing. — `SignUpFlow/.specify/templates/plan-template.md`.
- **Constitution Check** — The plan's per-principle compliance pass; the gate must pass before Phase 0
  research and be re-checked after Phase 1 design. — `SignUpFlow/.specify/templates/plan-template.md`.
- **Contract** — A written interface between the session that designed a feature and the session that
  implements it: request/response shapes, error keys, key schemas, test sketch. —
  `SignUpFlow/specs/014-security-hardening/contracts/rate-limiting.md`.
- **`data-model.md`** — Entities with key fields and no implementation; present when a feature has
  traditional entities, absent when infrastructure spans many (as in 014). —
  `SignUpFlow/specs/000-user-onboarding/data-model.md`.
- **Drift** — A generated artifact disagreeing with the source it was generated from; three verified cases
  exist in SignUpFlow. — `SignUpFlow/specs/000-user-onboarding/tasks.md` (line 3).
- **Functional requirement (FR)** — A numbered "System MUST…" statement, technology-agnostic; 014 has 44. —
  `SignUpFlow/specs/014-security-hardening/spec.md`.
- **Independent Test** — The per-story line proving a story is a viable MVP slice on its own. —
  `SignUpFlow/.specify/templates/spec-template.md`.
- **`[NEEDS CLARIFICATION]`** — The template's marker for an unresolved decision; the gate requires zero
  remaining before planning. — `SignUpFlow/.specify/templates/spec-template.md`.
- **Phase 0 / Phase 1** — Research (decisions with receipts) and design (data-model, contracts,
  quickstart) phases of a feature. — `SignUpFlow/specs/014-security-hardening/plan.md`.
- **`plan.md`** — Owns HOW: languages, versions, storage, performance targets, project structure with
  `[NEW]`/`[MODIFY]` annotations. — `SignUpFlow/specs/014-security-hardening/plan.md`.
- **Ralph loop** — The constitution's Context A: an agent picks the highest-priority incomplete spec,
  completes *all* acceptance criteria, and reports `<promise>DONE</promise>`. —
  `SignUpFlow/.specify/memory/constitution.md`.
- **`research.md`** — Phase 0 decisions: options evaluated, rationale, and the rejected alternatives. —
  `SignUpFlow/specs/014-security-hardening/research.md`.
- **Spec folder** — A self-contained instruction set for one feature (`spec.md`, `research.md`,
  `plan.md`, `contracts/`, `tasks.md`, …); SignUpFlow has 17 under `specs/`. —
  `SignUpFlow/specs/`.
- **Spec-kit** — The slash-command workflow (`/speckit.specify` → `/speckit.clarify` → `/speckit.plan` →
  `/speckit.checklist` → `/speckit.tasks` → `/speckit.implement`). — `SignUpFlow/docs/SPEC_KIT_SETUP.md`.
- **Stranger test** — The one quality test: a fresh agent session with zero conversation memory could
  implement from the artifacts alone. — `course/03-content/m04-spec-driven-saas/lesson.md` (M4.2).
- **Success criteria (SC)** — Measurable, technology-agnostic outcomes; 014 has 12. —
  `SignUpFlow/specs/014-security-hardening/spec.md`.
- **`tasks.md`** — Phase 2 output: checkbox tasks `[ID] [P?] [US#]`, tests first, exact file paths,
  checkpoints per story. — `SignUpFlow/specs/000-user-onboarding/tasks.md`.

## Terms people get wrong

- **Acceptance criteria vs. success criteria** — Acceptance criteria describe one scenario's observable
  outcome (blocked 15 minutes); success criteria are the feature-level measurable targets (100% of
  brute-force attempts blocked). Both live in `spec.md`, and mixing them makes both ungradable.
- **WHAT vs. HOW** — WHAT is user-visible behavior and belongs in `spec.md`; HOW is stack, versions, and
  storage and belongs in `plan.md`. The gate's first rule fails a spec that names a technology.
- **Generated vs. verified** — Generated means a slash command wrote it (`/speckit.tasks`,
  `/speckit.checklist`); verified means you grepped its paths and recounted its counts. A "Quality Score:
  100%" is generated, not verified.
- **`[P]` vs. `[US#]`** — `[P]` marks a task parallelizable with its neighbours (different files, no
  dependency); `[US#]` ties the task to the user story it serves. They are orthogonal, not synonyms.
- **Review vs. approval** — A recorded local review with severity and file/line findings is review;
  approval requires that review plus successful local validation for the pushed head/base. "Missing review
  is not approval" (`SignUpFlow/AGENTS.md`, PR rule 4).

## Curated resources

- `SignUpFlow/specs/014-security-hardening/` — the exemplar set: 8 stories, 44 FRs, 8 decisions, 6
  contracts, no `tasks.md`.
- `SignUpFlow/specs/014-security-hardening/checklists/requirements.md` — the gate, and the "5xP1" count
  that a 100% score failed to catch; read it beside `spec.md`.
- `SignUpFlow/specs/000-user-onboarding/tasks.md` — the real task format; T017 as the model line; line 3
  and the migrations tasks as the drift examples.
- `SignUpFlow/.specify/templates/spec-template.md`, `plan-template.md`, `tasks-template.md` — the three templates that define the
  artifact set and each rule quoted in this module.
- `SignUpFlow/.specify/memory/constitution.md` — Context A (the Ralph loop) and the principles the
  Constitution Check walks.
- `SignUpFlow/docs/ai-pr-review.md` — the local review checklist, the severity/file-line rule, and the two
  hard lines on self-review and approval.
- `course/03-content/m04-spec-driven-saas/lab.md` — Lab M4's seven steps and the acceptance checklist you
  are graded against.
