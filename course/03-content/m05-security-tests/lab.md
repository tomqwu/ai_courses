# Lab M5 — Isolate and Accept
> Part of AI Product Studio (APS-3) · Pass/fail checkpoint for Module 5 · Companion lesson: `lesson.md`

## Goal

**Prove tenant isolation with tests, and design playbook acceptance.** You leave with two artifacts: (1) a FastAPI app whose tenant boundaries are enforced by real-JWT negative-path tests — including proof that a forbidden write leaves the database unchanged — plus an executable route policy and a qualifications field that provably grants no admin rights; (2) one playbook JSON fixture and a manifest of required scenarios with honest statuses, validated by pytest.

## Prerequisites

- Module 4 complete: your spec folder exists and passed the requirements checklist. If you specced "availability time-off" or "invitation links" for a SignUpFlow-style app, implement that feature here.
- Students who did M4 **on SignUpFlow itself**: extend the cloned repo directly — its seven-tier suite (`docs/TESTING.md`) is your regression net, and `api/dependencies.py` is your reference implementation.
- Python 3.11+, FastAPI, SQLAlchemy, Pydantic 2, `python-jose` (or `PyJWT`), `passlib[bcrypt]`, pytest, httpx.

## Time

~3 hours. Steps 1–2 are ~45 minutes each for a small app; steps 3–4 ~45 minutes each.

## The app shape (no starter repo — define it minimally)

Because this course ships no starter for the SaaS track, the lab fixes the app shape: a **FastAPI app with three tables — `organizations`, `people`, `events` — and JWT auth**. Every `person` and `event` row carries `org_id`; every `person` carries a `roles` JSON array. The JWT carries `sub` (person id) and `org_id`. Copy the pattern from SignUpFlow's `api/dependencies.py`: `get_current_user` reloads the person by `Person.id == sub AND Person.org_id == token_org_id AND status == "active"` (401 otherwise); `verify_org_member(person, org_id)` raises 403 on mismatch; `get_current_admin_user` gates on the `admin` role. If you have your own SaaS, map its two most tenant-sensitive resources onto steps 1–2.

## Steps

**1. Isolate two resources by `org_id` (TDD).** Pick two resources (e.g., people + events). Add `org_id` columns and a `verify_org_member` dependency; load target rows through the actor's organization (SignUpFlow's `get_person_in_actor_org` pattern: foreign or absent → 404; explicit foreign org → 403). Write real-JWT tests — no mocked auth for these: (a) same-tenant member reads own rows OK; (b) foreign-tenant member gets 403 naming a foreign org, and 404 for a guessed id inside their tenant; (c) **assert the DB is unchanged after the forbidden write** — snapshot the target row, attempt the write as the foreign member, assert the denial status, re-read the row, assert it is identical. SignUpFlow makes this step 4 of its change protocol: "Assert forbidden writes leave database state unchanged" (`docs/API_AUTHORIZATION.md`). Use a real test database — "Mocking the database in integration tests" is a named anti-pattern (`AGENTS.md`).

**2. Add a qualifications field — and prove it grants nothing.** Store qualifications (e.g., `"usher"`, `"greeter"`) in the same roles JSON array, permission role still exactly one of `volunteer`/`admin` (normalize input like `api/roles.py`'s `normalize_roles`; reject `"ADMIN"` as ambiguous). Write the test: a person with roles `["volunteer", "usher"]` calls the invite endpoint → **403**. "Do not grant admin access merely because someone leads a ministry" (`docs/playbooks/church.md`).

**3. Build the route policy table + drift test.** Create `route_policy.py`: a dict naming every mounted route as `public` / `member` / `admin` (SignUpFlow uses five classes in `api/route_auth_policy.py`; three suffice here). Write a test that walks the live route table (`app.routes`, filtered to your API paths), asserts set equality (missing/stale), then verifies wiring: policy `admin` ⇒ `get_current_admin_user` in the dependency tree, `member` ⇒ `get_current_user` (the mechanism in `tests/unit/test_api_route_auth_policy.py`). **Demonstrate the drift test works:** deliberately miswire one route (swap its dependency), run, record the red failure; fix it, run, record green. A drift test you have never seen fail is a hope, not a test.

**4. Author one playbook fixture + manifest + validator.** Fixture (modeled on SignUpFlow's `docs/playbooks/church.json` shape — the repo's own minimal example is `tests/playbooks/examples/food-bank.json`), extended with one disruption drill for this lab:

```json
{
  "id": "food-bank",
  "version": 1,
  "workflow": "six_week_roster",
  "name": "Food Bank acceptance sandbox",
  "event": "Packing shift",
  "secondary_event": "Preparation",
  "critical_role": "coordinator",
  "roles": {"packer": 2, "coordinator": 1},
  "drills": [
    {"id": "PF-04",
     "operation": "Block both coordinators for week 4 and attempt publication",
     "expected": "Regeneration must not publish an incomplete roster; prior roster stays live"}
  ]
}
```

(The drill mirrors CH-04: "publication is rejected and the prior roster stays live", `docs/playbooks/church.md`.) Then a tiny manifest of required scenarios with honest statuses — `automated` / `partial` / `manual` / `blocked` — and a pytest validator that (a) fails when a required scenario id is missing from the fixture, (b) rejects statuses outside the four allowed, (c) enforces SignUpFlow's coupling rules: `automated`/`partial` rows must cite a test id; `manual`/`blocked` rows must include the `manual` tier (`tests/playbooks/coverage.py`, lines 43–46). **Demonstrate it:** remove a required id, run, record the failure; restore, run, record green.

## Acceptance checklist (all must be true)

- [ ] Isolation tests green: same-tenant member reads own rows OK; foreign-tenant member denied (403 explicit foreign org / 404 guessed id inside their tenant).
- [ ] The forbidden-write test asserts the DB row is unchanged after the denied request (before/after comparison present).
- [ ] Qualification-no-admin test green: `"usher"` (or your equivalent) cannot invite people — 403, not 404, not success.
- [ ] Route policy table classifies **every** mounted route; suite green.
- [ ] Drift test caught the deliberate miswire — both the red and the green run are recorded.
- [ ] Playbook fixture + manifest exist and validate green.
- [ ] Removing a required scenario id fails the validator — both the failing and passing runs are recorded.
- [ ] Manifest statuses are honest: no `automated` without a test id; `blocked`/`manual` rows carry the manual tier — and evidence is recorded in the Module 1 evidence-log format (commands, outcomes/counts, date, environment, limitations).

## Evidence to record

Per the M1 evidence format: every command with its pass/fail counts, the date, your environment, and limitations. Include both induced failures (miswired route, removed scenario id) with their red output — the failure demonstrations *are* the evidence that your guards work. Close with one limitation you have not proven (e.g., "no browser tier yet — isolation proven at API level only").

## Stretch goals

- **Two-tenant browser check (BO-12 pattern):** run two tenants in one app with Playwright at **360px and 1440px**; each admin sees only its own directory; a volunteer is denied admin surface, invitations, and publication (`docs/playbooks/README.md`, BO-12).
- **Port one CH drill to your domain:** e.g., CH-05 (invite a qualified replacement → regeneration fills the gap without substituting another qualification).

## Discussion prompt

Post to the community with the template:

> **Lab M5 — [your name]**
> Red run I'm most glad I have: [miswire or removed-scenario failure, pasted]
> What the failure proved: [one sentence]
> My manifest's honest status: [one scenario with status ≠ automated, and why]