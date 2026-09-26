# Lab M5 — Isolate and Accept
> Part of AI Product Studio (APS-3) · Pass/fail checkpoint for Module 5 · Companion lesson: `lesson.md`

## Goal

**Prove tenant isolation with tests, and design playbook acceptance.** You leave with two artifacts: (1) the `mini-flow` FastAPI app with its tenant boundaries enforced by real-JWT negative-path tests — including proof that a forbidden write leaves the database unchanged — plus an executable route policy and a qualifications field that provably grants no admin rights; (2) a playbook JSON fixture and a manifest of required scenarios with honest statuses, validated by pytest before a single test collects.

## Prerequisites

- Module 4 complete: your spec folder exists and passed the requirements checklist.
- Python 3.11+ on your PATH.
- **The starter:** `mini-flow/` in this module's folder. Run `make setup` inside it (FastAPI, SQLAlchemy 2, Pydantic 2, PyJWT, httpx, pytest, pytest-cov — no compiled dependencies, no database server).
- Students who did M4 **on SignUpFlow itself** may extend the cloned repo instead — its seven-tier suite (`SignUpFlow/docs/TESTING.md`) is your regression net and `SignUpFlow/api/dependencies.py` is the reference implementation. Map its two most tenant-sensitive resources onto steps 1–2 and keep the same evidence format.

## Time

~3 hours. Step 0 is 15 minutes; steps 1–2 are ~40 minutes each; steps 3–4 ~35 minutes each; 20 minutes for evidence and the post. The starter ships the app, the fixtures and the tests — your time goes into reading the red output and fixing the right line, not into scaffolding.

## The starter

`mini-flow/` mirrors SignUpFlow's authorization shape at lab scale (its README has the file-by-file map). Three tables — `organizations`, `people`, `events` — with `org_id` on every person and event row, a `roles` JSON array holding exactly one permission role plus any qualifications, and HS256 tokens carrying `sub` and `org_id`. `get_current_user` reloads the person by `id AND org_id AND status == "active"` (401 otherwise), `verify_org_member` raises 403 on an explicit foreign org, and `get_person_in_actor_org` returns 404 for a foreign *or* absent id — the contract of `SignUpFlow/docs/API_AUTHORIZATION.md:21-24`.

**The starter is deliberately incomplete.** Each lab step ships as tests marked `@pytest.mark.lab(step=N)`. They are skipped in `make lab-m5` and un-skipped by `make stepN` (or `make lab-m5 STEPS=1,2,3,4`, the pass gate). Every step is red against the shipped code, because the starter carries one named defect per step (the README's "intentional gaps" table names each one). Your job is not to write the tests — it is to read them, fix the app, then break your own guard and record the red.

## Steps

**0. Run the baseline and the leak.** `make lab-m5` → expect `51 passed, 23 skipped`, coverage 100%. Record it. Then `make demo` and read the two `LEAK` lines: Tokyo's admin, holding a perfectly valid Tokyo token, reads Grace's event and overwrites its title. Paste those two lines into your evidence log — they are the "before".

**1. Isolate the events router by `org_id` (TDD).** `make step1` → `2 failed, 4 passed`. Open `mini-flow/tests/test_lab1_isolation.py` and read why: `src/miniflow/routers/events.py` loads `Event` by primary key only in `get_event` and `update_event`. Fix it the way `src/miniflow/routers/people.py` already does for people — the tenant predicate goes **into the query** (`Event.org_id == actor.org_id`), foreign and absent both return 404. `make step1` → `6 passed`. Then re-run `make demo`: zero leaks, and the title still reads `'Sunday rota'`. The test that matters is `test_foreign_admin_patch_is_denied_and_row_unchanged`: it snapshots the row from a fresh session, attempts the write as the foreign admin, asserts 404, then asserts the snapshot is identical — step 4 of SignUpFlow's change protocol, "Assert forbidden writes leave database state unchanged" (`SignUpFlow/docs/API_AUTHORIZATION.md:59-76`). Auth is real in every test here; "Mocking the database in integration tests" is a named anti-pattern (`SignUpFlow/AGENTS.md`).

**2. Prove a qualification grants nothing.** `make step2` → `4 failed, 3 passed`. Two defects: `check_admin_permission` in `src/miniflow/dependencies.py` grants admin to any role that is not `volunteer` — so an usher can invite, create events and promote themselves — and `normalize_roles` in `src/miniflow/roles.py` case-folds `"ADMIN"` into `admin` instead of refusing it. The references are one line each: `SignUpFlow/api/dependencies.py:15-17` (admin iff `"admin" in roles`) and `SignUpFlow/api/roles.py:49` (`is an ambiguous permission role`). `make step2` → `7 passed`. "Do not grant admin access merely because someone leads a ministry" (`SignUpFlow/docs/playbooks/church.md:26`).

**3. Complete the route policy, then prove the drift test bites.** `make step3` → `1 failed, 3 passed`: `update_event` is mounted but unclassified in `src/miniflow/route_auth_policy.py`. Classify it (`admin`) → `4 passed`. The test walks the **live** route table (`iter_route_contexts(app.routes)`), asserts set equality both ways, then walks each route's dependency tree: `admin` ⇒ `get_current_admin_user`, `member` ⇒ `get_current_user`, `public` ⇒ neither — the mechanism of `SignUpFlow/tests/unit/test_api_route_auth_policy.py`. **Now demonstrate it works:** in `src/miniflow/routers/events.py`, change `create_event`'s dependency from `get_current_admin_user` to `get_current_user`, run `make step3`, and record the red (`AssertionError: create_event`). Restore it, run again, record the green. A drift test you have never seen fail is a hope, not a test.

**4. Make the manifest fail on a removed scenario.** `make step4` → `4 failed, 2 passed`. The fixture (`tests/playbooks/examples/food-bank.json`, SignUpFlow's own minimal shape plus one PF-04 drill) and the manifest (`tests/playbooks/coverage.json`, four scenarios with honest statuses) already exist; the validator in `tests/playbooks/coverage.py` only checks JSON shape. Add three things, in the shape of `SignUpFlow/tests/playbooks/coverage.py:42-46`: a status/tier coupling validator on `ScenarioCoverage` (`automated`/`partial` need an executable tier; `manual`/`blocked` need the `manual` tier), a `REQUIRED_SCENARIOS` check in `load_coverage_manifest`, and a cross-check that every fixture drill has a manifest row. `make step4` → `6 passed`. **Then demonstrate it live:** delete the `MF-03` row from `coverage.json`, run `make lab-m5`, and watch collection die before any test runs — `ERROR: Invalid playbook coverage manifest …: missing required scenarios ['MF-03']` — the same pre-collection failure as `SignUpFlow/tests/playbooks/plugin.py:37-45`. Restore the row. Finally, make the manifest honest again: MF-02 and MF-03 were `blocked` because their tests were skipped; now that they are green, set them to `automated` with the test ids as evidence. PF-04 stays `manual` — mini-flow has no solver, and the manifest must say so.

**5. Pass gate.** `make pass-gate` → `74 passed`, coverage 100%. Record it with the date, your environment and `git rev-parse HEAD`.

## Acceptance checklist (all must be true)

- [ ] `make lab-m5` recorded green **before** any change (`51 passed, 23 skipped`, coverage 100%), and the two `make demo` `LEAK` lines pasted as the "before".
- [ ] Step 1 green: foreign read and foreign PATCH of an event both return 404; the before/after row snapshot assertion passes; `make demo` shows zero leaks.
- [ ] Step 2 green: `["volunteer", "usher"]` receives 403 from invite, event creation and self-promotion; `normalize_roles(["ADMIN"])` raises "ambiguous".
- [ ] Step 3 green: every mounted route is classified; the induced miswire of `create_event` produced a red run **and** the restore produced a green run — both pasted.
- [ ] Step 4 green: removing `MF-03` from `coverage.json` kills the run before collection — the error line pasted — and the restored run is green.
- [ ] Manifest statuses are honest: MF-02 and MF-03 now `automated` with test ids as evidence; PF-04 still `manual` with the reason.
- [ ] `make pass-gate` → `74 passed`, coverage ≥ 90, pasted with date, environment and head SHA.
- [ ] Evidence recorded in the Module 1 format with at least one limitation you have not proven.

## Evidence to record

Per the M1 evidence format: every command with its pass/fail counts, the date, your environment, the head SHA, and limitations. Include the four `make stepN` red runs *before* your fixes, both induced failures (miswired `create_event`, removed `MF-03`) with their red output, and the two `make demo` runs. The failure demonstrations *are* the evidence that your guards work. Close with one limitation you have not proven (e.g., "isolation proven at the API tier only — no browser tier; PF-04 is manual because there is no solver").

## Stretch goals

- **Two-tenant browser check (BO-12 pattern):** add a minimal HTML surface and run two tenants in one app with Playwright at **360px and 1440px**; each admin sees only its own directory (`SignUpFlow/docs/playbooks/README.md`, BO-12).
- **Port one CH drill to your domain:** e.g., CH-05 (invite a qualified replacement → the gap is filled without substituting another qualification) as a second `drills` entry, with its manifest row honestly `manual`.
- **Your own SaaS:** repeat steps 1–3 against your Module 4 spec's two most tenant-sensitive resources, reusing `tests/support.py`'s snapshot pattern.

## Discussion prompt

Post to the community with the template:

> **Lab M5 — [your name]**
> Red run I'm most glad I have: [miswire or removed-scenario failure, pasted]
> What the failure proved: [one sentence]
> My manifest's honest status: [one scenario with status ≠ automated, and why]
