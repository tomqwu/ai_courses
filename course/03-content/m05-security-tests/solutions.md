# Solutions M5 — Lab M5: Isolate and Accept

> Reference answers for `lab.md`, in order, against the `mini-flow/` starter. Lab M5 is a closed
> lab: the tests ship with the starter, so the counts below are exact, not shapes (re-run
> 2026-09-17, Python 3.11.15, FastAPI 0.141.1). Students working on their own SaaS instead must
> match the *shape*: a named test id, a red run and a green run for every induced failure.

## The worked cross-tenant leak

`make demo` shows it before any test does. Tokyo's admin holds a valid Tokyo token and requests
Grace's event:

```text
GET   /api/events/<grace_event>  -> 200  LEAK  (contract says 404)
PATCH /api/events/<grace_event>  -> 200  LEAK  (contract says 404)
Grace's event title in the database is now: 'stolen'
```

The leak is a query with no tenant predicate (`src/miniflow/routers/events.py`, `get_event` and
`update_event`):

```python
event = db.query(Event).filter(Event.id == event_id).first()      # WRONG: primary key only
```

The fix moves the tenant into the `WHERE` clause, the shape of `SignUpFlow/api/dependencies.py:61-66`,
so a foreign row and an absent row both miss:

```python
def get_event_in_actor_org(event_id: str, actor: Person, db: Session) -> Event:
    event = (db.query(Event)
               .filter(Event.id == event_id, Event.org_id == actor.org_id)
               .first())
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
```

The test that proves it is `test_foreign_admin_patch_is_denied_and_row_unchanged`: snapshot from a
fresh session, denied write, `assert status == 404`, then `assert event_snapshot(id) == before`.
The first assert proves the *contract*; the second proves the *control*. A denied request that
mutates the row anyway is a security bug wearing a test-green costume.

## Step 0 — Baseline

```bash
make lab-m5
# 51 passed, 23 skipped        coverage 100%  (floor 90)
make pass-gate
# 11 failed, 63 passed         (2 + 4 + 1 + 4 — one named defect per step)
```

**Grading note.** The baseline line dated *before* any diff is the first thing to look for. No
baseline, no proof the student saw the starter red.

## Step 1 — Isolate the events router

**Reference answer.** Both event lookups go through `get_event_in_actor_org` above; the people
router already had this shape and is untouched.

```bash
make step1        # before: 2 failed, 4 passed
                  #   FAILED test_foreign_member_cannot_read_foreign_event
                  #   FAILED test_foreign_admin_patch_is_denied_and_row_unchanged
make step1        # after:  6 passed
make demo         # after:  "No leaks. The events router carries the tenant predicate."
```

**Common wrong answers.**
- *Filter in Python after the fetch:* `[e for e in db.query(Event).all() if e.org_id == …]` — the
  foreign rows were already read into the process; any serializer or log downstream leaks them.
  Signals the student thinks filtering is a display concern.
- *`verify_org_member(actor, event.org_id)` after loading:* returns 403, which confirms the row
  exists and lets a valid account enumerate the id space. Signals the student read "deny" but not
  `SignUpFlow/docs/API_AUTHORIZATION.md:21-24`.
- *Editing the test to expect 403:* the auto-fail "tests weakened to pass".

**Grading note.** Ask for the demo output before and after. A real pass has `'stolen'` in the
before and `'Sunday rota'` in the after.

## Step 2 — Qualifications grant nothing

**Reference answer.** Two one-line fixes:

```python
# src/miniflow/dependencies.py  (SignUpFlow/api/dependencies.py:15-17)
return bool(person.roles and "admin" in person.roles)

# src/miniflow/roles.py  (SignUpFlow/api/roles.py:49) — stop lowercasing; refuse the ambiguous case
values = list(dict.fromkeys(value.strip() for value in roles))
...
for value in qualifications:
    if value.casefold() in PERMISSION_ROLES:
        raise ValueError(f"{value!r} is an ambiguous permission role")
```

```bash
make step2        # before: 4 failed, 3 passed  (invite 201, create_event 201, self-promotion 200, "ADMIN" repaired)
make step2        # after:  7 passed
```

**Common wrong answers.** *(i)* `"admin" in roles or "coordinator" in roles` — every invented
qualification mints a privilege. *(ii)* Fixing the gate but leaving `.lower()`: three tests go green
and `test_uppercase_admin_is_ambiguous_not_repaired` stays red; normalization must refuse, not
repair. *(iii)* Returning 404 from the invite route for non-admins — that hides a route, it does not
make an authorization decision.

**Grading note.** Ask what `normalize_roles(["ADMIN"])` produces. A real pass quotes "is an
ambiguous permission role"; a fake says "we normalize it to admin".

## Step 3 — Route policy + drift test

**Reference answer.** Add `"update_event"` to `ADMIN_OPERATIONS` in
`src/miniflow/route_auth_policy.py`. The shipped test already compares the policy with the live
route table both ways and walks each dependency tree (`SignUpFlow/tests/unit/test_api_route_auth_policy.py`).

```bash
make step3        # before: 1 failed, 3 passed
                  #   AssertionError: mounted but unclassified: ['update_event']
make step3        # after:  4 passed
# induced miswire: create_event -> Depends(get_current_user)
make step3        # 1 failed, 3 passed
                  #   FAILED test_every_classified_route_is_wired_as_its_policy_says
                  #   AssertionError: create_event
                  #   assert 'get_current_admin_user' in {'get_current_user', 'get_db', ...}
# restored
make step3        # 4 passed
```

**Common wrong answers.** Classifying `update_event` as `member` (green on set equality, red on
wiring — read the second failure). Recording only the green run. Miswiring a `member` route to the
admin gate and calling that the demonstration — it is a different, weaker failure (over-restriction,
not privilege escalation); the rubric asks for an `admin` route demoted.

**Grading note.** The pasted red must name `create_event` and `get_current_admin_user`. No red
run, no proof the guard works.

## Step 4 — Manifest validator

**Reference answer.** Three additions to `tests/playbooks/coverage.py`, in the shape of
`SignUpFlow/tests/playbooks/coverage.py:42-46`:

```python
class ScenarioCoverage(BaseModel):
    ...
    @model_validator(mode="after")
    def validate_status_tiers(self) -> Self:
        if self.status in {"automated", "partial"} and not EXECUTABLE_TIERS.intersection(self.tiers):
            raise ValueError("automated or partial scenarios require an executable tier")
        if self.status in {"manual", "blocked"} and "manual" not in self.tiers:
            raise ValueError("manual or blocked scenarios require the manual tier")
        return self

def load_coverage_manifest(path=..., fixture=None):
    ...
    missing = REQUIRED_SCENARIOS - manifest.scenario_ids
    if missing:
        raise ValueError(f"Invalid playbook coverage manifest {path}: missing required scenarios {sorted(missing)}")
    if fixture is not None:
        drills = {d["id"] for d in fixture["drills"]} - manifest.scenario_ids
        if drills:
            raise ValueError(f"Invalid playbook coverage manifest {path}: fixture drills without a manifest row {sorted(drills)}")
    return manifest
```

```bash
make step4        # before: 4 failed, 2 passed   (each "DID NOT RAISE")
make step4        # after:  6 passed
# induced removal: delete the MF-03 row from tests/playbooks/coverage.json
make lab-m5       # ERROR: Invalid playbook coverage manifest .../coverage.json: missing required scenarios ['MF-03']
                  # make: *** [Makefile:21: lab-m5] Error 4        <- pytest usage error: nothing collected
# restored
make lab-m5       # 51 passed, 23 skipped
```

Then the honesty edit in `coverage.json`: MF-02 and MF-03 → `"status": "automated"`, `"tiers":
["api"]`, evidence = the test ids that now pass (e.g.
`tests/test_lab1_isolation.py::test_foreign_admin_patch_is_denied_and_row_unchanged`). PF-04
stays `"manual"` — mini-flow has no solver.

**Common wrong answers.** Checking required ids inside a test instead of the loader (removal then
fails one test instead of killing collection — `SignUpFlow/tests/playbooks/plugin.py:37-45` is the
mechanism). Marking PF-04 `automated` because "the drill is in the fixture". Deleting the
uncomfortable row instead of marking it `blocked`.

**Grading note.** A real pass shows `Error 4` with zero tests run; a fake shows `1 failed`.

## Step 5 — Pass gate

```bash
make pass-gate
# 74 passed        coverage 100%
```

## Common student failures across the lab

1. **Fixing before recording.** The four `make stepN` red runs and the two `LEAK` lines are half
   the evidence; a submission that starts green has no "before".
2. **Filtering in Python after the fetch.** The predicate belongs in the query
   (`SignUpFlow/docs/API_AUTHORIZATION.md:59-76`): "Every query that can reach organization data must
   carry the concrete tenant predicate required by the route's policy."
3. **Weakening the guard to match the app.** Any diff under `mini-flow/tests/test_lab*.py` other
   than the un-skip is an auto-fail.
4. **A drift test or validator that has never failed.** Both induced reds, pasted, or the guard is
   unproven.

## Self-check table

| Criterion | Self-verification |
|---|---|
| Baseline recorded first | Evidence log opens with `51 passed, 23 skipped` and two `LEAK` lines |
| Every event query carries the tenant predicate | `grep -n "db.query(Event)" mini-flow/src/miniflow/routers/events.py` shows `org_id` on every hit |
| Forbidden write leaves the row unchanged | `make step1` → `6 passed`; `make demo` title is `'Sunday rota'` |
| Qualification grants no admin right | `make step2` → `7 passed`; `["ADMIN"]` raises "ambiguous" |
| Policy covers every mounted route | `make step3` → `4 passed` |
| Drift is caught | Red run naming `create_event` saved, then green |
| Removal fails before collection | `Error 4` line saved, then `51 passed, 23 skipped` |
| Manifest is honest | MF-02/MF-03 `automated` with test ids; PF-04 `manual` with reason |
| Pass gate | `make pass-gate` → `74 passed`, coverage ≥ 90, with date, environment, head SHA, limitation |
