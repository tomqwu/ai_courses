# M4 Handout — The Spec-Driven SaaS (one page)

**Mental model:** a spec folder is an instruction set for an agent that has no memory of you — so every
artifact must survive a stranger, and the checklist gate is the last cheap place to catch what won't.

## The pipeline

```
specify ─ clarify ─ research ─ data-model ─ plan ─ CHECKLIST ─ contracts ─ tasks ─ implement
  WHAT     ≤3 Qs      Phase 0     Phase 1     HOW    pass/fail    seams     Phase 2   Ralph loop
```

| Artifact | Owns | Refuses to hold |
|---|---|---|
| `spec.md` | WHAT: stories, Given/When/Then, FRs, success criteria | languages, frameworks, schema SQL |
| `research.md` | Decisions with options, rationale, rejected alternatives | silent preferences |
| `data-model.md` | Entities and fields | — (absent when infrastructure spans entities) |
| `plan.md` | HOW: stack, versions, storage, targets + Constitution Check | user-facing behavior |
| `contracts/` | Seams: shapes, error keys, key schemas, test sketch | vibes at the boundary |
| `checklists/requirements.md` | The gate: Content Quality, Completeness, Readiness | — (generated, so verify it) |
| `tasks.md` | Work by story, tests first, **exact file paths** | "update the backend" |

## Keep these commands and formats

```bash
ls specs/                                   # 17 folders in SignUpFlow
grep -rn "NEEDS CLARIFICATION" specs/       # must return zero
grep -o "FR-[0-9]\{3\}" spec.md | sort -u | wc -l   # recount against the checklist
grep -o "app/[a-z_/]*\.py" tasks.md | sort -u | xargs ls  # every cited path must exist
ls alembic/versions/                        # where migrations actually live
```

PR body (fixed four sections): `Summary:` one line per change · `Changed files:` path: reason ·
`Validation:` commands and results · `Follow-ups:` known gaps and open questions.

Task line: `- [ ] T017 [P] [US1] Implement create_wizard_state method in api/services/onboarding_service.py`

## Files worth opening

- `SignUpFlow/specs/014-security-hardening/spec.md` — 8 stories, 44 FRs, 7 edge cases, 12 criteria.
- `SignUpFlow/specs/014-security-hardening/plan.md` — Constitution Check, seven verdicts, zero violations.
- `SignUpFlow/specs/014-security-hardening/contracts/rate-limiting.md` — the 5/5/15 refrain as a config table.
- `SignUpFlow/specs/014-security-hardening/checklists/requirements.md` — the gate, and the "5xP1" drift.
- `SignUpFlow/specs/000-user-onboarding/tasks.md` — real task format; line 3's stale path; migrations drift.
- `SignUpFlow/.specify/templates/` (`spec-template.md`, `plan-template.md`, `tasks-template.md`) — the set each feature draws from.
- `SignUpFlow/.specify/memory/constitution.md` — Context A, the Ralph loop's own rules.
- `SignUpFlow/docs/ai-pr-review.md` — local review checklist and the two hard lines.

## Three gotchas

1. **Technology leaks into `spec.md`.** The gate's first rule forbids it. Schema belongs to data-model,
   contracts, and migrations — entities are described "without implementation."
2. **"Then the system is secure" is not a scenario.** A scenario is done when a test author makes zero
   decisions; numbers (5/5/15) recur as FR, contract row, and assertion.
3. **Generated artifacts drift.** A stale `/specs/020-user-onboarding/` path, a checklist printing "5xP1"
   over six P1 stories, migrations sent to a nonexistent `migrations/` directory. Grep paths, recount counts.

## You're done when…

- [ ] `spec.md` has ≥3 independently testable stories, numeric Then-clauses, ≥8 FRs, no implementation detail.
- [ ] Zero `[NEEDS CLARIFICATION]` markers remain; unknowns recorded in Assumptions.
- [ ] `research.md` has ≥3 decisions, each with a rejected alternative and a reason.
- [ ] `plan.md` carries a Constitution Check verdict per principle; violations argued.
- [ ] One contract has shapes, error keys, and a test sketch.
- [ ] Every `tasks.md` task names an existing file path; tests-first phases; checkpoint per story.
- [ ] Your checklist passed after you grepped its paths and recounted its counts.
- [ ] A stranger implemented story 1 with no questions the folder should have answered.
