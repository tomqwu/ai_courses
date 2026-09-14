# Solutions M5 — Lab M5: Isolate and Accept

> Reference answers for `lab.md`, in order. Lab M5 is a closed lab: there is a correct submission
> shape, shown below. Counts in the pytest excerpts are shapes, not fixed numbers — the app is
> yours, so the counts vary; what must match is the *shape* (a named test id, a red run and a green
> run for every induced failure). Nothing here is a TinyCopilot run, so the §0.2 lab numbers do not
> apply.

## The worked cross-tenant leak test

Steps 1 is the module in miniature. The leak is a query with no tenant predicate:

```python
# WRONG — loads by primary key only: a foreign id returns the other org's row
leaked = db.query(Event).filter(Event.id == event_id).all()
```

The fix moves the tenant into the `WHERE` clause, so a foreign row and an absent row both miss
(`SignUpFlow/api/dependencies.py:61-66` is the reference for this shape):

```python
row = (db.query(Event)
         .filter(Event.id == event_id, Event.org_id == actor.org_id)
         .first())
```

The assertion that proves the fix is a real-JWT negative-path test — denial *and* unchanged row:

```python
def test_foreign_member_denied_and_row_unchanged(client, db):
    before = row_snapshot(db, "events", EVENT_IN_ORG_A)
    r = client.patch(f"/events/{EVENT_IN_ORG_A}", json={"title": "stolen"},
                     headers=auth_headers(tokyo_admin))          # Org B's real JWT
    assert r.status_code == 404                                  # foreign id inside actor's tenant
    assert r.json()["detail"] == "Not found"
    assert row_snapshot(db, "events", EVENT_IN_ORG_A) == before    # the forgotten assertion
```

Note the two-line idea: the first assert proves the *contract* (denial, and the right code); the
second proves the *control* (nothing was written). A denied request that mutates the row anyway is a
security bug wearing a test-green costume.

## Step 1 — Isolate two resources by `org_id`

**Reference answer.** Two resources (`people`, `events`) carry a non-null `org_id`; a
`verify_org_member(person, org_id)` dependency raises `403` on mismatch; target rows load through
`get_person_in_actor_org`-style queries (`404` for foreign or absent); real-JWT tests (no mocked
auth) cover the cases below.

**Commands + expected output shape.**

```bash
pytest tests/test_isolation.py -q
# .......                                                                  [100%]
# 7 passed in 0.6s
```

**Negative-path cases a passing submission must include** (all seven):

1. Same-tenant member reads own rows → `200`.
2. Foreign member names an explicit foreign org → `403`.
3. Foreign member requests a guessed id inside their tenant → `404`.
4. Foreign member PATCHes an existing foreign row → `404`.
5. After case 4, the target row is byte-identical to the pre-request snapshot.
6. Invalid bearer token → `401`; missing bearer token on a protected route → `403`.
7. Token whose `org_id` claim matches no active membership → `401`.

**Common wrong answers.**
- *Fetch everything, filter in Python:* `[e for e in db.query(Event).all() if e.org_id == ...]` — the
  foreign rows were already read into the process; any serializer, export, or log downstream leaks
  them. Signals the student thinks filtering is a display concern.
- *`403` for every foreign id:* confirms existence and lets an account enumerate your id space.
  Signals the student read "deny" but not the status contract (`docs/API_AUTHORIZATION.md:23`).
- *Denial tested, row not:* asserts `r.status_code == 404` and stops. Signals the student copied
  the visible half of step 4 of the change protocol.

**Grading note.** A real pass shows the request failing *and* a before/after snapshot; a plausible
fake asserts the status code only.

## Step 2 — Qualifications grant nothing

**Reference answer.** `roles` stays a JSON array with exactly one of `volunteer`/`admin`;
`normalize_roles` rejects `"ADMIN"` as ambiguous and rejects two permission roles
(`SignUpFlow/api/roles.py:38-53`). The test authenticates a real JWT with `roles:
["volunteer", "usher"]` and calls the invite endpoint expecting `403` — not `404`, not success.

```bash
pytest tests/test_roles.py -q
# ...                                                                      [100%]
# 3 passed in 0.3s
```

**Common wrong answers.** *(i)* Treating any unknown string as a permission role — every invented
qualification mints a privilege. *(ii)* Returning `404` for the denied invite because the route was
never wired at all; that is a missing route, not an authorization decision. *(iii)* Lowercasing
`"ADMIN"` and accepting it as admin; normalization must refuse, not repair (`api/roles.py:48-49`).

**Grading note.** Ask what `"ADMIN"` produces. A real pass quotes "is an ambiguous permission role";
a fake says "we normalize it to admin".

## Step 3 — Route policy table + drift test

**Reference answer.** `route_policy.py` names every mounted route as `public`/`member`/`admin`; the
test walks `app.routes`, asserts set equality with the policy dict (missing + stale), then walks each
route's dependency tree (`admin` ⇒ `get_current_admin_user`, `member` ⇒ `get_current_user`). Compact
executable exemplar, in the shape of `SignUpFlow/api/route_auth_policy.py:8-171`:

```python
ROUTE_POLICY = {
    "health": "public", "signup": "public", "login": "public", "me": "member",
    "list_people": "member", "list_events": "member", "create_event": "admin",
    "create_invitation": "admin",
}
ADMIN_DEP, MEMBER_DEP = "get_current_admin_user", "get_current_user"

def test_policy_matches_live_routes(app):
    live = {r.name for r in app.routes if getattr(r, "path", "").startswith("/api")}
    assert set(ROUTE_POLICY) == live                       # missing + stale
    for route in app.routes:
        names = dependency_names(route)
        if ROUTE_POLICY.get(route.name) == "admin":
            assert ADMIN_DEP in names                      # miswired
        elif ROUTE_POLICY.get(route.name) == "member":
            assert MEMBER_DEP in names
```

**Commands + expected output.** Deliberately swap `create_event` to `get_current_user`, run, and
record the red; restore and record the green:

```bash
pytest tests/test_route_policy.py -q
# F...                                                    [100%]   # red, miswire demonstrated
pytest tests/test_route_policy.py -q
# ....                                                    [100%]   # green after restore
```

**Common wrong answers.** Comparing two static lists (the policy dict against a hand-written route
list) instead of the live app — the test can never catch a new route, which is exactly the trap named
in `02-instructor/instructor-guide.md` (M5 watch-for). Asserting only set equality misses miswiring.
Recording only the green run.

**Grading note.** Ask for the red output before the fix. No red run, no proof the guard works.

## Step 4 — Playbook fixture + manifest + validator

**Reference answer.** A fixture modeled on `SignUpFlow/tests/playbooks/examples/food-bank.json`
(the repo's minimal example carries `id`, `version`, `workflow`, `name`, `event`,
`secondary_event`, `critical_role`, `roles`) plus one drill. The manifest gives each required
scenario a status from the four at `SignUpFlow/tests/playbooks/coverage.py:19`
(`automated`/`partial`/`manual`/`blocked`), and the validator enforces the coupling rules at
`tests/playbooks/coverage.py:43-46`: `automated`/`partial` need an executable tier;
`manual`/`blocked` must include the `manual` tier. Removing a required id must fail, as
`tests/playbooks/plugin.py:37-45` fails collection.

**Commands + expected output shape.**

```bash
pytest tests/test_manifest.py -q     # after deleting a required id
# E                                                       [100%]   # validator error, not a skip
pytest tests/test_manifest.py -q     # restored
# ....                                                    [100%]
```

**Common wrong answers.** Marking everything `automated` with no test id; deleting the uncomfortable
scenario instead of marking it `blocked`; validating inside a test instead of before collection.

**Grading note.** A real manifest contains at least one row whose status is not `automated`, with a
one-line reason.

## Common student failures across the lab

1. **Filtering in Python after fetching all rows.** The tenant predicate must be in the query, per
   `docs/API_AUTHORIZATION.md:59-76`: "Every query that can reach organization data must carry the
   concrete tenant predicate required by the route's policy."
2. **Testing only the happy path.** A green same-tenant read proves nothing about the boundary; the
   seven negative cases above are the submission.
3. **Treating a self-reported "all tests pass" as evidence.** No command, no counts, no date, no
   revision is a claim, not evidence (`SignUpFlow/docs/playbooks/validation.md` is the format), and
   `docs/ai-pr-review.md` (Local Review Checklist, item 5) requires the reviewed head SHA.
4. **A drift test that has never failed.** Record the induced red for both the miswire and the
   removed scenario id; the failure demonstrations *are* the evidence.

## Self-check table

| Criterion | Self-verification |
|---|---|
| Every query carries the tenant predicate | `grep -rn "db.query(" app/ \| grep -v org_id` returns nothing |
| Forbidden write leaves the row unchanged | The before/after snapshot assertion exists and passes |
| Qualification grants no admin right | The `["volunteer","usher"]` invite test asserts `403` |
| Policy covers every mounted route | Set-equality test passes against `app.routes` |
| Drift is caught | Red run for the miswire is saved, then green |
| Manifest is honest | At least one status ≠ `automated`; coupling rules enforced |
| Removal fails validation | Red run for the deleted id is saved, then green |
| Evidence is real | Command + counts + date + environment + head SHA + limitation |
