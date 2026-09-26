# mini-flow — the Module 5 lab for AI Product Studio

A lab-scale multi-tenant FastAPI + SQLAlchemy 2 + JWT app that mirrors the authorization shape of
[SignUpFlow](https://github.com/tomqwu/SignUpFlow) — the volunteer-scheduling SaaS the Module 5
lesson dissects — in ~600 lines of Python. Three tables (`organizations`, `people`, `events`),
one permission role per person plus scheduling qualifications in the same JSON array, tokens that
carry `sub` and `org_id`, and the same 401/403/404 contract as `SignUpFlow/docs/API_AUTHORIZATION.md:21-24`.

**How the course uses this repo:** *the starter is deliberately incomplete, and the lab tests
are the spec.* `make lab-m5` is green as shipped. The four graded steps of Lab M5 ship as tests
that are **skipped until you un-skip them** (`make step1` … `make step4`), and every one of them
is red against the starter because the starter carries one named defect per step. You fix the
app until the step is green, then break the guard on purpose and record the red run. The
reference fixes are in `../solutions.md`; the point is to earn them.

## Layout (each module maps to its SignUpFlow counterpart)

| File | Mirrors (in `SignUpFlow/`) | Job |
|---|---|---|
| `src/miniflow/security.py` | `api/security.py` | HS256 JWT with `sub` + `org_id` + `exp`; PBKDF2 passwords (stdlib, no bcrypt build step) |
| `src/miniflow/dependencies.py` | `api/dependencies.py:15-17,46,61-66,78,138` | `get_current_user` reloads by id **and** tenant **and** active status; `verify_org_member` (403); `get_person_in_actor_org` (404); `get_current_admin_user`; `check_admin_permission` |
| `src/miniflow/roles.py` | `api/roles.py:38-53` | `normalize_roles`: exactly one of `volunteer`/`admin`, qualifications kept beside it, never treated as permissions (`AGENTS.md:60`) |
| `src/miniflow/route_auth_policy.py` | `api/route_auth_policy.py` | every operation name classified `public` / `member` / `admin` (SignUpFlow uses five classes) |
| `src/miniflow/routers/auth.py` | `api/routers/auth.py` | atomic signup (org + first admin), login, single-use invitation acceptance; no public join |
| `src/miniflow/routers/people.py` | `api/routers/people.py` | the **reference** router — every query carries the tenant predicate |
| `src/miniflow/routers/events.py` | `api/routers/events.py` | the router "added last" — see the intentional gaps below |
| `src/miniflow/{db,models,schemas,main}.py` | `api/{database,models,schemas,main}.py` | SQLite engine, three models, Pydantic bodies that never carry identity or tenant, app factory |
| `tests/playbooks/coverage.py` + `coverage.json` | `tests/playbooks/coverage.py`, `docs/playbooks/coverage.json` | the manifest of required scenarios with honest statuses, validated in `pytest_configure` before any test collects (`tests/playbooks/plugin.py:37-45`) |
| `tests/playbooks/examples/food-bank.json` | `tests/playbooks/examples/food-bank.json` | the minimal fixture shape, plus one disruption drill (PF-04) |
| `tests/test_{auth,people,events,status_contract,roles,playbook_baseline}.py` | `tests/api/`, `tests/unit/` | the baseline: real signups, real JWTs, real rows; 401/403/404 pinned |
| `tests/test_lab{1,2,3,4}_*.py` | see each file's docstring | the four graded hooks, marked `@pytest.mark.lab(step=N)` |
| `demo.py` | — | two tenants in one database; prints the status each cross-tenant probe returns against the contract |

## Setup

```bash
# 1. Python 3.11+ (the course standard, matching SignUpFlow's floor)
make setup          # fastapi, sqlalchemy>=2, pydantic>=2, PyJWT, httpx, pytest, pytest-cov

# 2. From this folder:
make lab-m5         # baseline suite + coverage floor >= 90; the four lab steps are skipped
make step1          # un-skip one step (red on the shipped starter)
make lab-m5 STEPS=1,2,3,4   # == make pass-gate: the Lab M5 pass gate
make demo           # watch Tokyo's admin read and overwrite Grace's event
```

## Verified status (as shipped)

Re-run on 2026-09-17 with Python 3.11.15, FastAPI 0.141.1, SQLAlchemy 2.0.54, pydantic 2.13.5,
PyJWT 2.14.0, pytest 9.1.1:

- `make lab-m5` → **51 passed, 23 skipped**, coverage **100%** (floor 90 enforced via `--cov-fail-under`), no warnings
- `make step1` → 2 failed, 4 passed · `make step2` → 4 failed, 3 passed · `make step3` → 1 failed, 3 passed · `make step4` → 4 failed, 2 passed
- `make pass-gate` → **11 failed, 63 passed** on the starter, by design; **74 passed, 100%** once the four fixes in `../solutions.md` are applied
- `make demo` → two `LEAK` lines on the starter, and Grace's event title reads `'stolen'` afterwards; zero after step 1

## The intentional gaps (do not "fix" these before the lab)

Each gap is one named defect, each is exposed by exactly one step's tests, and each has a
line-level counterpart in the real repo.

| Step | Gap in the starter | Where | Exposed by | The real thing |
|---|---|---|---|---|
| 1 | `get_event` and `update_event` load by primary key only — a foreign tenant can read and overwrite the row with a valid token | `src/miniflow/routers/events.py` | `tests/test_lab1_isolation.py` (2 red) | `SignUpFlow/api/dependencies.py:61-66` |
| 2 | `check_admin_permission` returns True for *any* role that is not `volunteer`, so `usher` is an admin; `normalize_roles` case-folds `"ADMIN"` into `admin` instead of refusing it | `src/miniflow/dependencies.py`, `src/miniflow/roles.py` | `tests/test_lab2_qualifications.py` (4 red) | `SignUpFlow/api/dependencies.py:15-17`, `SignUpFlow/api/roles.py:49` |
| 3 | `update_event` is mounted but never classified in the route policy | `src/miniflow/route_auth_policy.py` | `tests/test_lab3_route_policy.py` (1 red) | `SignUpFlow/tests/unit/test_api_route_auth_policy.py` |
| 4 | `load_coverage_manifest` never checks `REQUIRED_SCENARIOS`, never cross-checks the fixture's drills, and `ScenarioCoverage` has no status/tier coupling rule — a removed scenario passes silently | `tests/playbooks/coverage.py` | `tests/test_lab4_manifest.py` (4 red) | `SignUpFlow/tests/playbooks/coverage.py:42-46`, `SignUpFlow/docs/playbooks/README.md:84-87` |

Everything else is meant to be correct. If a baseline test goes red while you work, you broke
something the lab did not ask you to touch.

What mini-flow does **not** mirror, on purpose: bcrypt (PBKDF2 from the stdlib instead), refresh
and password-reset tokens, the browser/HTMX tier, CSRF, the solver and roster publication (which
is why the PF-04 drill is honestly `manual` in the manifest), and SignUpFlow's five policy classes
(three suffice here).

## Course pointers

- Lesson: `../lesson.md` (M5.1 tenancy as a P0 rule, M5.2 permissions ≠ qualifications, M5.3 the honest manifest)
- Lab: `../lab.md` · reference answers: `../solutions.md` · rubric: `../lab-rubrics.md`
- The real code beside every file above: `SignUpFlow/api/dependencies.py`, `SignUpFlow/api/route_auth_policy.py`, `SignUpFlow/tests/playbooks/coverage.py`, `SignUpFlow/AGENTS.md:57-61`
