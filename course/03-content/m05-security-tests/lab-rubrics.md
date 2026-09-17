# Lab M5 — Grading Rubric: Isolate and Accept

> Lab M5 is a pass/fail checkpoint in the lab component (labs 60% / quizzes 20% / capstone 20%,
> `01-design/assessment-and-rubrics.md`). Pass = Proficient or better on every row, no auto-fail
> condition. The lab runs against the `mini-flow/` starter, so the expected counts are exact
> (`solutions.md`); a student on their own SaaS is graded on the same rows by shape.

**Four levels.** *Exemplary* = complete, self-verified, shows judgment. *Proficient* = complete and
correct as shipped. *Developing* = attempted, incomplete, or unverified. *Missing* = absent or
fabricated.

## Group A — Tenant isolation, proven by negative paths (steps 0–1, 30 points)

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Baseline and leak recorded before any change | 6 | `51 passed, 23 skipped` plus both `LEAK` lines, dated, with the `'stolen'` title quoted | Baseline count and the two `LEAK` lines present | Baseline only, or demo only | Submission starts green | First evidence-log entry |
| Tenant predicate lives in the query | 12 | Both event lookups share one `get_event_in_actor_org`; explains why Python-side filtering still leaks | Every `db.query(Event)` in the events router carries `org_id` | One of the two lookups fixed | No predicate, or `verify_org_member` after the load (403) | The diff of `routers/events.py` |
| Forbidden write leaves the row unchanged | 12 | `make step1` → `6 passed` and `make demo` after shows `'Sunday rota'`, with a sentence on why a denied write can still mutate | `make step1` → `6 passed`; demo after shows zero leaks | Read fixed, PATCH test still red | Test edited to expect 403 or 200 | Raw `make step1` before/after and both demo runs |

## Group B — Qualifications confer no authority (step 2, 15 points)

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Admin iff `admin` in roles | 6 | One-line gate matching `SignUpFlow/api/dependencies.py:15-17`; names the escalation path (self-promotion) it closed | Usher gets 403 on invite, event creation and self-promotion | Invite fixed, self-promotion still 200 | Usher still an admin | Raw `make step2` before/after |
| Ambiguous role refused, not repaired | 6 | `"ADMIN"` raises "ambiguous" and the student explains refuse-vs-repair | `test_uppercase_admin_is_ambiguous_not_repaired` green | Still lowercasing; three of four fixed | Normalizer accepts anything | The `roles.py` diff + the error message |
| Vocabulary separation stated | 3 | One sentence each on permissions vs. qualifications, with `SignUpFlow/AGENTS.md:60` | Distinguishes them in the evidence log | Describes qualifications as "extra roles" | Conflates them | Evidence-log paragraph |

## Group C — Executable route policy and drift (step 3, 25 points)

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Policy classifies every mounted route | 8 | `update_event` classified `admin` with a note on why not `member`; names a route that would break set equality | `make step3` → `4 passed` | Classified as `member` (wiring test red) | Route still unclassified, or test edited | `route_auth_policy.py` diff + `make step3` |
| Induced miswire captured red, then green | 12 | Red output names `create_event` and `get_current_admin_user`; both runs dated; explains why demoting an `admin` route is the stronger demonstration | Both runs pasted, the red naming `create_event` | Green only, or a described-but-not-pasted failure | No induced failure | Two pasted pytest summaries with timestamps |
| Mechanism understood | 5 | Explains live-route comparison vs. two static lists and where the dependency walk lives | States the test compares against `app.routes` | Vague ("the test checks routes") | Claims a static list is equivalent | Evidence-log paragraph |

## Group D — Playbook fixture, manifest, and validator (step 4, 20 points)

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Validator enforces required ids, drills and coupling | 7 | All three checks in the loader, matching `SignUpFlow/tests/playbooks/coverage.py:42-46`; `make step4` → `6 passed` | `make step4` → `6 passed` | Two of three checks; one test red | Checks placed inside a test, or none | The `coverage.py` diff + `make step4` |
| Removal fails **before collection** | 7 | `Error 4` line pasted with zero tests run, then restored green; explains why pre-collection beats one failing test | `ERROR: Invalid playbook coverage manifest … ['MF-03']` pasted, then green | Removal observed as `1 failed` | No removal demonstration | Both runs |
| Manifest statuses are honest | 6 | MF-02/MF-03 `automated` citing the exact test ids; PF-04 `manual` with the no-solver reason | Statuses updated; PF-04 not `automated` | Everything `automated`, or MF rows left `blocked` | Row deleted, or statuses outside the four | The `coverage.json` diff |

## Group E — Evidence and community post (10 points)

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Evidence log entry | 6 | Every command with counts, date, environment, head SHA, all four pre-fix reds, both induced failures, `make pass-gate` → `74 passed`, one limitation | All fields present; pass gate pasted | Counts or date missing | No log entry, or summarized without outputs | Evidence-log excerpt |
| Community post | 4 | Red run pasted, what it proved, one non-`automated` status with reason | All three template lines present | Two of three | No post | Permalink or screenshot |

**Weights: 30 + 15 + 25 + 20 + 10 = 100.**

## Auto-fail conditions (fail Lab M5 regardless of other rows)

1. **Fabricated evidence** — an invented pytest summary, a hand-edited count, or output no command
   produced (`01-design/assessment-and-rubrics.md`).
2. **Tenant filtering in Python after the fetch** — the foreign rows were already read; the control
   was never in the query.
3. **A green drift or validator run with no induced failure recorded** — the guard was never seen
   working, so it is unproven.
4. **Tests weakened to pass** — any diff under `mini-flow/tests/test_lab*.py` beyond un-skipping, a
   `404` relaxed to `4xx`, a deleted assertion, or a manifest row deleted instead of marked `blocked`.
5. **Mocked auth in the isolation tier** — tenancy evidence must come from real-JWT requests
   through the starter's `tests/support.py` helpers or an equivalent.
6. **Independent review claimed for your own work** — see `SignUpFlow/docs/ai-pr-review.md`, Local
   Review Checklist item 3.
