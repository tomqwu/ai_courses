# Lab M4 — Spec a Real Feature, Stranger-Testable

> **Goal:** produce a complete spec-kit folder for one real feature of *your* product, pass it through the same gate SignUpFlow runs, and prove a stranger could implement story 1 from `tasks.md` alone.
> **Prerequisites:** Lesson M4; a feature idea for your SaaS (suggested for a SignUpFlow-style app: **volunteer time-off / availability windows** or **invitation links**; building something else — spec your own feature). **Time:** 90–120 minutes.

You will work in a new folder `specs/001-your-feature/` inside **your own project** (or a scratch repo if you don't have one yet). SignUpFlow's real folders are your templates — open them as you go, don't copy blindly.

## Steps

1. **Pick the feature and write `spec.md` (WHAT only).** Follow `.specify/templates/spec-template.md` in the SignUpFlow repo: ≥3 user stories, each with an "Independent Test" line (every story is a viable MVP slice) and Given/When/Then scenarios whose Then-clauses are testable — numbers, not vibes ("fail authentication 5 times within 5 minutes → blocked for 15 minutes", `specs/014-security-hardening/spec.md` US1, is the model). Add ≥8 functional requirements and measurable, technology-agnostic success criteria. **Zero implementation details** — no languages, frameworks, or schema SQL; entities described "without implementation".
2. **Resolve every unknown before moving on.** No `[NEEDS CLARIFICATION]` markers may remain (the gate rule in `specs/014-security-hardening/checklists/requirements.md`). Ask a bounded set of questions now (max 3, per 014's own practice), or record defaults in an Assumptions section — that is how 014 settled 90-day log retention and 1-hour token expiry.
3. **Write `research.md` (Phase 0).** ≥3 numbered decisions, each with alternatives **and the rejection reason** — the format of `specs/014-security-hardening/research.md` Decision 1 (chose Redis, rejected in-memory outright). A decision without a rejected alternative is a preference, not a decision.
4. **Write `data-model.md`, `plan.md`, and one `contracts/<seam>.md`.** `plan.md` owns HOW (stack, versions, storage, performance targets) and must contain an explicit **Constitution Check**: one verdict line per principle of your project's constitution (SignUpFlow's is `.specify/memory/constitution.md`; use your Lab M1 constitution for your own repo). Any violation goes in a Complexity Tracking table with an argument — "Fill ONLY if Constitution Check has violations that must be justified" (`.specify/templates/plan-template.md`). The contract pins one real seam: request/response shapes, error keys, and a test sketch (model: `specs/014-security-hardening/contracts/rate-limiting.md`).
5. **Write `tasks.md` (Phase 2).** Checkbox tasks in the template format — `[ID] [P?] [US#] description` — organized Setup → Foundational → one phase per story (tests written first, failing) → Polish, with a checkpoint after each story. **Every task names an exact file path** that exists in your repo ("Include exact file paths in descriptions", `.specify/templates/tasks-template.md`; "T017 [P] [US1] Implement create_wizard_state method in api/services/onboarding_service.py", `specs/000-user-onboarding/tasks.md`, is the model).
6. **Write `checklists/requirements.md` and grade yourself honestly.** Three groups, all pass/fail: Content Quality, Requirement Completeness, Feature Readiness (same structure as 014's). Then run the **drift checks** from M4.3 against your own generated file: grep every path it cites and confirm the file exists; recount every count (stories, FRs, priorities) against `spec.md`; confirm no `[NEEDS CLARIFICATION]` remains. 014's self-graded "Quality Score: 100%" printed "5xP1" next to six P1 features — self-reported scores don't catch drift; your greps do.
7. **The stranger test (the pass gate).** Hand `tasks.md` + the folder to a peer (cohort) or to a fresh agent session with no context beyond the folder, and ask for story 1 only. If they must ask you anything the folder doesn't answer, the spec has a hole: sharpen the artifact that starved them and re-run. Record what they asked.

## Acceptance checklist

- [ ] `spec.md`: ≥3 stories, each independently testable with an "Independent Test" line; Given/When/Then with numeric Then-clauses; ≥8 FRs; success criteria measurable and technology-agnostic; no implementation details
- [ ] No `[NEEDS CLARIFICATION]` anywhere; unknowns are resolved via questions or recorded Assumptions
- [ ] `research.md`: ≥3 numbered decisions, each with a rejected alternative and the reason
- [ ] `plan.md`: Constitution Check with a verdict per principle; violations argued in Complexity Tracking
- [ ] ≥1 contract with shapes, error keys, and a test sketch
- [ ] `tasks.md`: checkbox format with `[US#]` links, tests-first phases, checkpoint per story, exact file paths in every task
- [ ] `checklists/requirements.md`: all three groups pass; drift checks run (paths grepped, counts recounted)
- [ ] Stranger test: story 1 implemented (or attempted) with zero questions the folder should have answered; residual questions recorded and artifacts sharpened

## Evidence to record

In your evidence log: the checklist's three pass lines with today's date; the drift-check commands you ran and their output; and the stranger-test transcript (or the questions the stranger asked). Format follows the course evidence-log template from Lab M1.

## Stretch

- Run `/speckit.checklist`-style self-grading on a *previous* project's spec and find one drift case (a stale path or wrong count) — then fix the artifact, not the symptom.
- Implement story 1 from your own tasks.md in one sitting, tests first, and record the honest Validation section (failures included) in the four-part PR format from M4.3.

## Discussion prompt

Post the stranger-test result: what did your stranger ask that your folder should have answered? Name the artifact that starved them and show the sharpened line before/after.