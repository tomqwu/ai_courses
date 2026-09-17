# Lab M4 — Solutions & Worked Exemplar

> **Lab M4 is open-ended**, so "reference answer" here means a **worked exemplar artifact set**, not one
> correct answer. The exemplar feature is **availability windows** (volunteer time-off) for a
> SignUpFlow-style app, built in the student's *own* project. Exemplar paths (`app/…`, `specs/001-…`)
> belong to that exemplar project, not to SignUpFlow. Pointers marked **[SIG]** resolve in
> the `SignUpFlow/` clone (a sibling of `course/` in the workspace root).
> Models to imitate: **[SIG]** `specs/014-security-hardening/spec.md`, `specs/000-user-onboarding/tasks.md`,
> `.specify/templates/{spec,plan,tasks}-template.md`, `specs/014-security-hardening/checklists/requirements.md`.

## Step 1 — `spec.md` (WHAT only)

**Reference answer.** ≥3 stories, each with an "Independent Test" line and Given/When/Then scenarios whose
Then-clauses are numeric; ≥8 FRs phrased "System MUST…"; measurable, technology-agnostic success criteria;
no language, framework, or schema anywhere.

**Worked exemplar** (abridged):

```markdown
# Feature Specification: Availability Windows

### User Story 1 - Submit an availability window (Priority: P1)
As a volunteer I submit a start and end time I am unavailable.
**Why this priority**: without submission nothing downstream exists.
**Independent Test**: POST one window, then read it back; window appears with
state `pending` and a conflict flag is computed.

**Acceptance Scenarios**
1. **Given** a volunteer submits 2026-03-02 09:00–17:00, **When** the window is
   saved, **Then** state is `pending` and a coordinator is notified within 60s.
2. **Given** an end time earlier than the start, **When** submitted, **Then** the
   request is rejected with `invalid_window` and nothing is stored.

### User Story 2 - Approve or deny a window (Priority: P1)
**Independent Test**: approve a pending window; state becomes `approved` and the
volunteer sees it without a page reload on next fetch.

### User Story 3 - Weekly recurring windows (Priority: P2)
**Independent Test**: submit a recurrence with count 4; exactly 4 dated windows
exist and all four share one `recurrence_id`.

**Functional Requirements**
- **FR-001**: System MUST reject a window whose end is not after its start.
- **FR-002**: System MUST store all times in UTC and render in org timezone.
- **FR-003**: System MUST mark a window `conflict` within 2 seconds of save.
- **FR-004**: System MUST notify the org's coordinators within 60 seconds of a save.
- **FR-005**: System MUST move a window `pending → approved | denied` only once.
- **FR-006**: System MUST reject a recurrence whose count exceeds 12.
- **FR-007**: System MUST scope every read and write to the caller's `organization_id`.
- **FR-008**: System MUST let the owner delete their own pending window.
- **FR-009**: System MUST write one audit entry per state change.
- **FR-010**: System MUST retain availability records for 90 days by default.

**Success Criteria**
- **SC-001**: 100% of inverted windows rejected with `invalid_window`.
- **SC-002**: conflict flag present within 2 seconds for 95% of saves.
```

## Step 2 — Resolve unknowns

**Reference answer.** Zero `[NEEDS CLARIFICATION]` markers; each unknown either asked (≤3 questions) or
defaulted in an Assumptions section. **[SIG]** 014 used Assumptions for 90-day retention and 1-hour tokens.

## Step 3 — `research.md` (≥3 decisions, each with a rejected alternative)

**Worked exemplar:**

```markdown
## Decision 1: Window storage
**Options**: (a) PostgreSQL `tstzrange` column; (b) JSONB blob; (c) app-side intervals.
**Decision**: (a). **Rejected (b)**: no overlap query, forces full-table reads.
**Rejected (c)**: timezone bugs land in every endpoint, not one column.
## Decision 2: Overlap detection
**Options**: (a) DB exclusion constraint; (b) service-layer check.
**Decision**: (a) constraint plus service pre-check for a friendly error.
**Rejected (b) alone**: races under concurrent submits leave duplicate overlaps.
## Decision 3: Notification transport
**Options**: (a) transactional outbox row drained by a worker; (b) inline send.
**Decision**: (a). **Rejected (b)**: a mail failure must not roll back the save.
```

## Step 4 — `data-model.md`, `plan.md`, one contract

**Reference answer.** `plan.md` owns HOW and carries a Constitution Check with one verdict line per
principle, violations argued in Complexity Tracking. Contract pins shapes, error keys, test sketch.

```markdown
## Constitution Check  (exemplar plan.md; principle names from the student's Lab M1 constitution)
- **Test-First**: PASS — tasks T004–T006 are failing tests before implementation.
- **Tenant Isolation**: PASS — every query filters `organization_id`; test T009 asserts it.
- **No Silent Failures**: PASS — outbox write is in the same transaction as the save.
**Constitution Violations**: NONE. **Complexity Tracking**: N/A.

## Contract: availability-api.md
POST /api/availability  →  201 {"id","start_utc","end_utc","state","conflict"}
409 errors: {"error":"invalid_window"} | {"error":"outside_org"}
Test sketch: inverted window → 409 invalid_window, no row written.
```

## Step 5 — `tasks.md` (exact paths, tests first)

```markdown
- [ ] T004 [P] [US1] Test inverted window returns 409 in tests/api/test_availability.py
- [ ] T005 [P] [US1] Add AvailabilityWindow model in app/models/availability.py
- [ ] T006 [US1] Implement create_window in app/services/availability_service.py
- [ ] T007 [US1] Expose POST /api/availability in app/api/routes/availability.py
- [ ] T008 [US1] Add overlap exclusion migration in alembic/versions/
### Checkpoint: validate US1 independently before starting US2
```

## Steps 6–7 — checklist and stranger test

**Reference answer.** All three groups pass; the student ran the drift checks and recorded their output;
the scripted stranger (`stranger-prompt.md`, or a peer using its report format) implemented story 1
and the report shows **zero spec-owed Q/A rows** — after a re-run if the first run found a hole.

**Sample stranger report** (first run on the exemplar; the report is abridged, the counts are not):

```text
=== STRANGER REPORT ===
Story: Submit an availability window
Tasks attempted: T004-T008
Stopped because: checkpoint reached

## Built
tests/api/test_availability.py — 3 tests (inverted window, happy path, org scope)
app/models/availability.py — AvailabilityWindow, start_utc/end_utc/state/conflict
app/services/availability_service.py — create_window
app/api/routes/availability.py — POST /api/availability

## Acceptance scenarios
| # | Scenario (Then-clause, copied) | Checked how | Result |
|---|---|---|---|
| 1 | state is `pending` and a coordinator is notified within 60s | test_create_pending covers the state half only | not checkable: no notification seam in US1 tasks |
| 2 | rejected with `invalid_window` and nothing is stored | test_inverted_window | pass |

## Questions (Q)
Q1. Is the window end exclusive (17:00 ends at 16:59:59)? — needed for: T006 — where I looked: spec.md FR-001, data-model.md
Q2. Which package installs the migration tool? — needed for: T008 — where I looked: plan.md, repo root

## Assumptions (A)
A1. Overlap compares only windows of the same volunteer — instead of: whole org — needed for: T008

## Counts
QUESTIONS: 2
ASSUMPTIONS: 1
SCENARIOS CHECKED: 1/2
=== END REPORT ===
```

**Labelling.** Q1 spec-owed (`data-model.md` never defined the interval bound). Q2 environment-owed
(a toolchain question; `plan.md` names the tool, the machine lacks it). A1 spec-owed (the contract
never said whose windows overlap). Scenario 1 "not checkable" is spec-owed: `tasks.md` has no US1
task for the notification outbox. **Three spec-owed rows: fail.** Sharpen `data-model.md` (add "end
exclusive"), the contract (overlap scope), and `tasks.md` (add T009 [US1] outbox write), re-run in a
fresh session, and keep both reports. The second run's `Counts` read `QUESTIONS: 1` (Q2 again,
environment-owed), `ASSUMPTIONS: 0`, `SCENARIOS CHECKED: 2/2` — pass.

**Commands and expected output** (shape; counts vary with your feature):

```text
$ ls specs/001-availability-windows/
checklists  contracts  data-model.md  plan.md  quickstart.md  research.md  spec.md  tasks.md
$ grep -rn "NEEDS CLARIFICATION" specs/001-availability-windows/ | wc -l
0
$ grep -o "FR-[0-9]\{3\}" specs/001-availability-windows/spec.md | sort -u | wc -l
10
$ grep -o "app/[a-z_/]*\.py" specs/001-availability-windows/tasks.md | sort -u | xargs ls
app/models/availability.py  app/services/availability_service.py
app/api/routes/availability.py
```

The `ls` line is the drift check that matters: it fails on a hallucinated path. A submission whose
`grep … | xargs ls` prints "No such file" has not run step 6.

## Common wrong answers (the four that recur)

| Failure | Why it fails | What it signals |
|---|---|---|
| **Technology in `spec.md`** ("Redis-backed, SQLAlchemy range column") | Breaks WHAT/HOW; **[SIG]** gate rule 1 is "No implementation details (languages, frameworks, APIs)" | The student wrote the plan and back-filled a spec |
| **"Then the system is secure"** / "handled appropriately" | Untestable; no assertion exists | Scenarios written for a reader, not a test author |
| **Tasks without paths** ("update the backend") | A fresh session must guess; **[SIG]** `AGENTS.md` forbids inventing paths | Task authored from memory, not from the repo |
| **Self-graded checklist passed without drift checks** | Reproduces the real bug: **[SIG]** 014's checklist prints "5xP1" while the spec has six P1 stories | Trusting generated output over the source |

**Grading note.** A real pass shows a `grep … | xargs ls` transcript for every cited path and a stranger
report whose `Counts` block matches its numbered rows, every row labelled, spec-owed rows fixed and
re-run; a plausible fake reports "all checks passed" with no commands, or a report with a `Counts`
block and no rows.

## Self-check table

| Criterion | Self-verification |
|---|---|
| ≥3 stories, numeric Then-clauses | Count `### User Story` and read each Then-clause |
| ≥8 FRs, no implementation detail | `grep -c "FR-" spec.md`; `grep -iE "redis|sql|fastapi|react" spec.md` → 0 |
| No unresolved unknowns | `grep -rn "NEEDS CLARIFICATION" specs/001-*/` → 0 |
| ≥3 research decisions with rejections | Count `## Decision` and confirm each has "Rejected" |
| Constitution Check per principle | One verdict line per Lab M1 principle; violations argued |
| Contract has shapes + error keys + test sketch | Open the file and point at all three |
| Every task path exists | `grep -o "app/[a-z_/]*\.py" tasks.md \| sort -u \| xargs ls` |
| Counts match source | Recount stories/FRs/priorities in the checklist against `spec.md` |
| Stranger test recorded | Every report verbatim; count spec-owed rows in the final run → 0 |
