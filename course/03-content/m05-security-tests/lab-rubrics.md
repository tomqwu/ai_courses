# Lab M5 — Grading Rubric: Isolate and Accept

> Lab M5 is a pass/fail checkpoint in the lab component (labs 60% / quizzes 20% / capstone 20%,
> `01-design/assessment-and-rubrics.md`). Pass = Proficient or better on every row, no auto-fail
> condition.

**Four levels.** *Exemplary* = complete, self-verified, shows judgment. *Proficient* = complete and
correct as shipped. *Developing* = attempted, incomplete, or unverified. *Missing* = absent or
fabricated.

## Group A — Tenant isolation, proven by negative paths (lab step 1, 30 points)

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Tenant predicate lives in the query | 10 | Shows the predicate in every query; explains why Python-side filtering still leaks | Every `db.query(` for a tenant table carries `org_id` | Some queries filtered; one filter happens in Python | No predicate, or filtering only in the serializer | Grep output for `db.query(` plus the diff |
| Seven negative cases pass | 12 | All seven, each asserting an exact status and detail | 200 own rows, 403 foreign org, 404 guessed id, 404 foreign PATCH, 401 invalid, 403 missing, 401 mismatched claim | Three or four cases; happy path covered | Only the happy path | Raw pytest output for `test_isolation.py` |
| Forbidden write leaves the row unchanged | 8 | Before/after snapshot, plus why a denied write can still mutate | Snapshot compared before and after the denied PATCH; assertion present | Status asserted, row not re-read | No unchanged-row assertion | The test body showing the before/after comparison |

## Group B — Qualifications confer no authority (lab step 2, 15 points)

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Exactly one permission role enforced | 6 | `"ADMIN"` and a two-role array both raise, with both messages quoted | Normalizer rejects ambiguous case-folding and a second role | Normalizer accepts anything, or silently lowercases | No normalization | `api/roles.py` equivalent + the two error messages |
| Qualification cannot invite | 6 | Real JWT with `["volunteer","usher"]` gets 403 and the student explains why not 404 | The invite call returns `403` | Returns `404`, or the route was never wired | Invite succeeds | Raw pytest output for `test_roles.py` |
| Vocabulary separation stated | 3 | One sentence each on permissions vs. qualifications, with a pointer | Distinguishes them in the evidence log | Describes qualifications as "extra roles" | Conflates them | Evidence-log paragraph |

## Group C — Executable route policy and drift (lab step 3, 25 points)

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Policy classifies every mounted route | 9 | Set equality against live `app.routes`; names a route that would break it | Every mounted route appears in the policy dict | Most routes listed by hand | Static hand-written list, or routes missing | `route_policy.py` + collection output |
| Wiring assertion detects miswiring | 8 | Dependency-tree walk covers admin, member, and public, with the three-way logic explained | Dependency tree checked against the policy class | Only set equality tested | No wiring check | The test source |
| Induced red captured, then green | 8 | Red output pasted for the miswire, failing assertion named, then green | Both runs recorded and dated | Green only, or a described-but-not-pasted failure | No induced failure | Two pasted pytest summaries with timestamps |

## Group D — Playbook fixture, manifest, and validator (lab step 4, 20 points)

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Fixture matches the repo shape | 6 | Mirrors `tests/playbooks/examples/food-bank.json` and adds one drill with an expected rejection | Valid fixture with roles, events, critical role, drill | Fixture present but incomplete | No fixture | The JSON file |
| Manifest statuses are honest | 7 | One row is not `automated`, with a reason; coupling rules enforced | Four allowed statuses only; tiers justify each status | Everything marked `automated` | Statuses outside the four, or no manifest | The manifest file |
| Removal fails validation | 7 | Validator fails **before collection**, error pasted, then restored and green | Removing a required id produces a failing run, recorded | Failure observed but not pasted | No removal demonstration | Both runs |

## Group E — Evidence and community post (10 points)

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Evidence log entry | 6 | Commands, counts, date, environment, head SHA, both induced failures, one limitation | All six fields present | Counts or date missing | No log entry, or summarized without outputs | Evidence-log excerpt |
| Community post | 4 | Red run pasted, what it proved, one non-`automated` status with reason | All three template lines present | Two of three | No post | Permalink or screenshot |

**Weights: 30 + 15 + 25 + 20 + 10 = 100.**

## Auto-fail conditions (fail Lab M5 regardless of other rows)

1. **Fabricated evidence** — an invented pytest summary, a hand-edited count, or output no command
   produced (`01-design/assessment-and-rubrics.md`).
2. **Tenant filtering in Python after the fetch** — the foreign rows were already read; the control
   was never in the query.
3. **A green drift or validator run with no induced failure recorded** — the guard was never seen
   working, so it is unproven.
4. **Tests weakened to pass** — a deleted negative-path assertion, a `404` assertion relaxed to
   `4xx`, or a manifest row deleted instead of marked `blocked`.
5. **Mocked auth in the isolation tier** — tenancy evidence must come from real-JWT requests.
6. **Independent review claimed for your own work** — see `SignUpFlow/docs/ai-pr-review.md`, Local
   Review Checklist item 3.
