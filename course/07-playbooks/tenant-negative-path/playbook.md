# Multi-Tenant Negative-Path Test Kit

When many customers share one database, one missing filter shows one customer's data to another. Coding agents write queries fast, and every query they write is another chance to forget the tenant. This kit is for builders of multi-tenant SaaS APIs. When you finish, you will have a tenancy rule written as a check, a status contract, a test matrix of actors against operations, real-credential tests proving tenant A cannot read, write or enumerate tenant B (guessed IDs included), tests proving a credential works only in the tenant that issued it, and a route-policy test that fails when a new route ships unclassified.

## The method

1. **Write the rule as a check an agent can obey.** Put it in the instructions file every agent reads, in imperative voice with no adjectives. The model: "Every database query MUST filter by `org_id`" and "A missing `org_id` filter is a cross-tenant data leak. Treat it as a P0 bug." (`SignUpFlow/AGENTS.md:57`, `SignUpFlow/AGENTS.md:61`). Add the rule that protects every filter downstream: "Never read user state from the request body." (`SignUpFlow/AGENTS.md:58`). Identity and tenant come only from the validated credential.

2. **Write the status contract before any test.** Four situations, four codes, written down: an invalid token is `401`; a missing token gets one code you choose and pin; an authenticated actor naming an explicit foreign organization is `403`; "a guessed resource identifier is looked up inside the actor's tenant and returns `404` whether it is foreign or absent" (`SignUpFlow/docs/API_AUTHORIZATION.md:21-24`). The last row stops enumeration. If a foreign ID returned `403`, any valid account could walk your ID space and learn which rows exist. When a foreign ID and an absent ID give the same answer, the walk learns nothing.

3. **Bind every credential to one tenant.** Put the tenant in the token beside the subject. On every request, reload the person by ID **and** tenant **and** active status, and return `401` if nothing matches (`SignUpFlow/api/dependencies.py:97-121`). A valid signature is not enough. A token whose tenant claim is missing or wrong, or whose person is inactive or deleted, must fail (`SignUpFlow/docs/API_AUTHORIZATION.md:28-33`).

4. **Put the tenant predicate in the query, not after it.** Load every target through the actor's tenant: `id == target_id AND org_id == actor.org_id`, then `404` if nothing matches (`SignUpFlow/api/dependencies.py:61-66`). Two tempting fixes fail. Filtering in application code after the fetch has already read the foreign rows into your process. Loading the row and then checking membership returns `403`, which confirms that the row exists.

5. **Build the matrix.** Rows are operations: list, read by ID, update by ID, delete by ID, create under an explicit organization. Columns are actors: anonymous, invalid token, the owner, a same-tenant peer, a same-tenant admin, a foreign member, a foreign admin. Every cell holds one exact status. Add a column for a well-formed ID that matches no row anywhere; it must match the foreign column exactly.

6. **Write the tests with real credentials, and assert exact codes.** Create both tenants through your real signup path and use the tokens your API issued. Mocked auth proves nothing about tenancy. Assert one status per cell, never a set such as `in (401, 403)`, because a set passes whichever code the framework happens to return. For every denied write, snapshot the row from a fresh database session, attempt the write, assert the status, then assert the snapshot is unchanged: "Assert forbidden writes leave database state unchanged" (`SignUpFlow/docs/API_AUTHORIZATION.md:107-108`). For every list, assert that no foreign identifier appears anywhere in the response body.

7. **Make the route policy executable.** Keep one mapping that classifies every operation (`public`, `member`, `admin`, plus any token-scoped classes you need). One test compares the mapping with the live route table in both directions, which catches missing and stale entries. It then walks each route's dependency tree and asserts the wiring: admin routes depend on the admin gate, member routes on the authenticated user, public routes on neither (`SignUpFlow/tests/unit/test_api_route_auth_policy.py:20-38`).

8. **Prove every guard can fail.** Break each one on purpose and record the red run: remove a tenant predicate, demote an admin route to the member dependency. Restore it and record the green run. A guard you have never seen fail is a hope, not a test.

9. **Follow a change protocol for every new route.** Classify it first. Put the tenant filter in the route's own query. Add real-credential tests for anonymous, invalid, member, same-tenant admin and foreign-admin actors. Assert that forbidden writes change nothing and that exports are filtered before serialization. Then run the matrix locally (`SignUpFlow/docs/API_AUTHORIZATION.md:101-118`). A warning in the log is observability. The filter in the query is the control (`SignUpFlow/docs/API_AUTHORIZATION.md:116-118`).

## Template

**Rule block for your agent instructions file.**

```markdown
## Multi-tenancy (project-critical)
- Every database query MUST filter by `org_id`. A missing filter is a P0 bug.
- Identity and tenant come only from the validated credential. Never read them from the request body.
- Load targets through the actor's tenant: foreign or absent -> 404.

| Situation                                   | Status |
|---------------------------------------------|--------|
| Invalid or expired token                    | 401    |
| Missing token on a protected route          | <pin one: 401 or 403> |
| Token whose tenant claim matches no active membership | 401 |
| Explicit foreign organization in the path   | 403    |
| Guessed ID, foreign or absent               | 404    |
```

**The test matrix.** Copy it, add your operations, and fill every cell before you write a test. The codes shown are one example policy, where members read and only admins write; for self-service resources the owner column differs from the peer column.

```markdown
| Operation            | anon | invalid | owner | peer (same tenant) | admin (same tenant) | foreign member | foreign admin | absent ID |
|----------------------|------|---------|-------|--------------------|---------------------|----------------|---------------|-----------|
| GET  /items          | 401  | 401     | 200   | 200                | 200                 | own rows only  | own rows only | n/a       |
| GET  /items/{id}     | 401  | 401     | 200   | 200                | 200                 | 404            | 404           | 404       |
| PATCH /items/{id}    | 401  | 401     | 403   | 403                | 200                 | 404 + row unchanged | 404 + row unchanged | 404 |
| POST /orgs/{org}/items | 401 | 401    | 403   | 403                | 201                 | 403 + no row   | 403 + no row  | n/a       |
| DELETE /items/{id}   | 401  | 401     | 403   | 403                | 204                 | 404 + row kept | 404 + row kept | 404      |
```

**Negative-path tests** (pytest with FastAPI's `TestClient`; rename to your routes).

```python
import uuid, pytest
from myapp.db import SessionLocal
from myapp.models import Item
from myapp.security import create_access_token
# signup, invite_and_accept, create_item: helpers that call your real API and return
# the issued token (mini-flow's tests/support.py is a complete example).

def snapshot(item_id):
    """Read the row from a fresh session, never from an object the test already holds."""
    with SessionLocal() as db:
        row = db.get(Item, item_id)
        return None if row is None else {"org_id": row.org_id, "title": row.title}

@pytest.fixture
def two_tenants(client):
    a = signup(client, "Tenant A", "admin@a.example")      # real signup, real token
    b = signup(client, "Tenant B", "admin@b.example")
    b_member = invite_and_accept(client, b, "m@b.example", ["volunteer"])
    item = create_item(client, a, "Sunday rota")
    return a, b, b_member, item

def test_foreign_read_is_404(client, two_tenants):
    _, _, b_member, item = two_tenants
    r = client.get(f"/api/items/{item['id']}", headers=b_member.headers)
    assert r.status_code == 404

def test_foreign_and_absent_ids_look_identical(client, two_tenants):
    _, b, _, item = two_tenants
    foreign = client.get(f"/api/items/{item['id']}", headers=b.headers)
    absent = client.get(f"/api/items/{uuid.uuid4().hex}", headers=b.headers)
    assert (foreign.status_code, foreign.json()) == (absent.status_code, absent.json())

def test_foreign_write_is_denied_and_row_unchanged(client, two_tenants):
    _, b, _, item = two_tenants
    before = snapshot(item["id"])
    r = client.patch(f"/api/items/{item['id']}", json={"title": "stolen"}, headers=b.headers)
    assert r.status_code == 404          # the contract
    assert snapshot(item["id"]) == before  # the control: nothing was written

def test_list_never_contains_foreign_rows(client, two_tenants):
    a, b, _, item = two_tenants
    r = client.get(f"/api/orgs/{b.org_id}/items", headers=b.headers)
    assert r.status_code == 200 and item["id"] not in r.text

def test_explicit_foreign_org_is_403(client, two_tenants):
    a, _, b_member, _ = two_tenants
    assert client.get(f"/api/orgs/{a.org_id}/items", headers=b_member.headers).status_code == 403

@pytest.mark.parametrize("org_claim", [None, "wrong-tenant"])
def test_token_bound_to_tenant(client, two_tenants, org_claim):
    a, b, _, _ = two_tenants
    claims = {"sub": a.person_id}
    if org_claim:
        claims["org_id"] = b.org_id          # validly signed, wrong tenant
    token = create_access_token(claims)
    r = client.get("/api/people/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 401
```

**Route-policy drift test** (FastAPI; `iter_route_contexts` is the helper both reference test files use).

```python
from fastapi.routing import APIRoute, iter_route_contexts
from myapp.main import app
from myapp.route_auth_policy import ROUTE_AUTH_POLICY   # {"list_items": "member", ...}

def deps(route):
    names, pending = set(), list(route.dependant.dependencies)
    while pending:
        d = pending.pop(); names.add(getattr(d.call, "__name__", str(d.call))); pending.extend(d.dependencies)
    return names

def test_policy_matches_live_routes_and_wiring():
    live = {r.name: r for r in iter_route_contexts(app.routes)
            if isinstance(r.original_route, APIRoute)
            and (r.path.startswith("/api") or r.path in {"/health"})}  # every path you classify
    assert set(ROUTE_AUTH_POLICY) == set(live)            # missing and stale
    for name, policy in ROUTE_AUTH_POLICY.items():         # miswired
        d = deps(live[name])
        if policy == "admin":
            assert "get_current_admin_user" in d, name
        elif policy == "member":
            assert "get_current_user" in d, name
        else:
            assert not d & {"get_current_user", "get_current_admin_user"}, name
```

## Checklist

- [ ] The tenancy rule and the status table sit in the file every coding agent reads.
- [ ] The missing-token status is pinned to one code, and a test asserts that code.
- [ ] Every token carries a tenant claim; the user reload filters by ID, tenant and active status.
- [ ] Tests cover a missing tenant claim, a wrong tenant claim, an inactive person and an expired token: all `401`.
- [ ] Every lookup by ID carries the tenant predicate inside the query.
- [ ] Every cell of the matrix has a test asserting one exact status, never a set.
- [ ] A foreign ID and an absent ID return identical status and body.
- [ ] Every denied write asserts an unchanged fresh-session snapshot, or an unchanged row count.
- [ ] Every list and export test asserts that no foreign identifier appears in the body.
- [ ] The route-policy test compares the live route table both ways and walks dependencies.
- [ ] A red run is recorded for a removed tenant predicate and for a miswired admin route, each followed by a green run.
- [ ] All tenancy tests use credentials issued by the real auth path; none mock authentication.

## Worked example from a real repo

**The runnable starter.** `mini-flow` is a lab-scale FastAPI, SQLAlchemy 2 and JWT app that mirrors SignUpFlow's authorization shape: three tables, tokens carrying `sub` and `org_id`, the same four-row status contract, and one deliberate leak. Its events router loads by primary key only: `db.query(Event).filter(Event.id == event_id)` (`course/03-content/m05-security-tests/mini-flow/src/miniflow/routers/events.py`, `get_event` and `update_event`). Its people router is the correct shape. `make demo` shows the leak before any test does. Run on 2026-09-26, it printed (abridged: IDs replaced, spacing compressed):

```text
GET   /api/organizations/<grace_org>/people -> 403  ok    explicit foreign org: policy denial
GET   /api/people/<grace_person>            -> 404  ok    guessed id, looked up inside own tenant
GET   /api/events/<grace_event>             -> 200  LEAK  (contract says 404)    guessed id, events router
PATCH /api/events/<grace_event>             -> 200  LEAK  (contract says 404)    foreign write, events router
GET   /api/people/me  (no token)            -> 403  ok    missing bearer token
GET   /api/people/me  (garbage token)       -> 401  ok    invalid bearer token
Grace's event title in the database is now: 'stolen'
```

A valid token from one tenant read and overwrote another tenant's row. The fix is one predicate, `Event.org_id == actor.org_id`, inside both queries. After it, the same demo reports "No leaks" and the title still reads `'Sunday rota'`. This kit's templates were run against mini-flow on 2026-09-26, with `Item` renamed to its `Event` routes: the seven negative-path test cases pass on the fixed app and three fail on the leaky starter; the route-policy test passes, then fails with `AssertionError: create_event` when that route is demoted to the member dependency.

**The real repo.** SignUpFlow at commit c550d46, a multi-tenant scheduling SaaS on FastAPI.

- *The matrix in one test.* `SignUpFlow/tests/api/test_scheduling_tenant_boundaries.py:197-219` walks one availability path through six actors: anonymous `401`, invalid token `401`, owner `200`, same-tenant peer `403`, same-tenant admin `200`, foreign admin `404`. The forbidden writes return `403` and `404`, and the test then asserts no row was written.
- *The unchanged-state assertion.* A foreign-tenant create is denied and the row count is compared before and after (`SignUpFlow/tests/api/test_scheduling_tenant_boundaries.py:301-308`). A foreign delete returns `404` and the row is still there (`SignUpFlow/tests/api/test_scheduling_tenant_boundaries.py:310-312`). The own-tenant list is searched for a foreign person's ID (`SignUpFlow/tests/api/test_scheduling_tenant_boundaries.py:273`).
- *Tenant-bound tokens.* A token with no tenant claim, and one with a foreign tenant claim, both get `401` (`SignUpFlow/tests/api/test_access_token_tenancy.py:40-53`).
- *The policy.* Five classes (`SignUpFlow/api/route_auth_policy.py:168-174`). By this kit's count at c550d46 they hold 145 operations: 7 public, 6 public-token, 4 public-callback, 50 member and 78 admin.
- *What a loose assertion hides.* The doc says a missing token "retains FastAPI HTTPBearer's `403`" (`SignUpFlow/docs/API_AUTHORIZATION.md:21-22`). The repo pins FastAPI 0.141.1 (`SignUpFlow/poetry.lock:1036-1037`), and in a minimal app on that version `HTTPBearer()` answers a missing token with `401` (run 2026-09-26). The repo's own boundary test asserts `401` for a request with no token (`SignUpFlow/tests/api/test_scheduling_tenant_boundaries.py:207`), while an older test accepts either code (`SignUpFlow/tests/api/test_multi_tenant.py:116-121`). The set-valued assertion is how the doc and the runtime drifted apart without a red run. mini-flow pins `403` explicitly with `HTTPBearer(auto_error=False)` and says why (`course/03-content/m05-security-tests/mini-flow/src/miniflow/dependencies.py:24-29`). Either code is defensible. An unpinned one is not.
- *Where the next leak starts.* `get_person_by_id` loads a person by primary key with no tenant predicate (`SignUpFlow/api/dependencies.py:20-30`). At this commit its only caller is its own unit test, so it leaks nothing today. An agent looking for a helper will find it first. Grep your own code for ID lookups without a tenant column.

## Self-check

The runnable self-check is `mini-flow`. It lives in the AI Product Studio course repository at `course/03-content/m05-security-tests/mini-flow/`; run the commands below from that repository's root. It is **not** stdlib-only: `make setup` installs FastAPI, SQLAlchemy 2, Pydantic 2, PyJWT, httpx, pytest and pytest-cov. It needs Python 3.11 or later and no database server.

```bash
make -C course/03-content/m05-security-tests/mini-flow setup lab-m5
```

Expected, re-run 2026-09-26 on Python 3.11.15: `51 passed, 23 skipped`, coverage 100% against a floor of 90. Then:

| Command | Starter (before fixes) | Pass |
|---|---|---|
| `make step1` (isolation tests) | `2 failed, 4 passed` | `6 passed` |
| `make step3` (route policy) | `1 failed, 3 passed` | `4 passed` |
| `make pass-gate` (all four steps) | `11 failed, 63 passed` | `74 passed`, coverage 100% |
| `make demo` | two `LEAK` lines, title `'stolen'` | "No leaks", title `'Sunday rota'` |

The starter numbers above are from runs on 2026-09-26. The `74 passed` was confirmed the same day on a scratch copy with the four reference fixes applied. Steps 2 and 4 cover a qualification that must not grant admin rights and a coverage manifest; they sit outside this kit but ride the same gate. Do not edit the tests to pass. Fix the app, then break the guard on purpose and record the red run: once step 3 is green, demote `create_event` to `get_current_user` and `make step3` fails with `AssertionError: create_event`.

**On your own app**, score each row pass or fail. **Pass = every row.**

| Row | Pass when |
|---|---|
| Contract | The status table is written and each row has a test asserting one exact code |
| Matrix | Every cell of your filled matrix maps to a named test |
| Enumeration | The foreign-versus-absent test compares status and body, and passes |
| State | Every denied write has an unchanged-snapshot or row-count assertion |
| Credentials | Missing tenant claim, wrong tenant claim, inactive person: `401`, tested |
| Policy | The live-route test passes, and a recorded miswire made it fail |
| Real auth | `grep` finds no auth mocks in the tenancy test files |

## Limits

- This kit proves isolation at the API tier for the operations and inputs you test. It does not prove isolation in the database, the deployment or a provider. SignUpFlow says the same of its own two-tenant acceptance run: "application-level local evidence; it does not certify deployment, provider, or database-infrastructure isolation" (`SignUpFlow/docs/API_AUTHORIZATION.md:61-66`).
- The route-policy test proves classification and dependency wiring, not the query. A member route can depend on the right gate and still query without a tenant filter. Only the matrix tests catch that.
- It does not cover background jobs, caches, search indexes, file storage, logs, analytics, timing side channels, or browser flows such as CSRF.
- It does not design your permission model beyond one admin gate.
- A green matrix shows no leak for the inputs tried. It does not show there is none.

## Sources

- SignUpFlow at commit c550d46: `SignUpFlow/AGENTS.md`, `SignUpFlow/docs/API_AUTHORIZATION.md`, `SignUpFlow/api/dependencies.py`, `SignUpFlow/api/route_auth_policy.py`, `SignUpFlow/tests/unit/test_api_route_auth_policy.py`, `SignUpFlow/tests/api/test_scheduling_tenant_boundaries.py`, `SignUpFlow/tests/api/test_access_token_tenancy.py`, `SignUpFlow/tests/api/test_multi_tenant.py`, `SignUpFlow/poetry.lock`.
- mini-flow: `course/03-content/m05-security-tests/mini-flow/` in the AI Product Studio course repository (README, Makefile, `src/miniflow/`, `tests/`).
- The missing-token behaviour of `HTTPBearer()` on FastAPI 0.141.1 was measured in a five-line app on 2026-09-26, not taken from documentation.

This kit is drawn from Module 5 of the AI Product Studio course.
