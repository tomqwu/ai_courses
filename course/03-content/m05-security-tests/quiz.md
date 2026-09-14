# Quiz M5 — The Spec-Driven SaaS: Multi-Tenant Security & Acceptance
> Part of AI Product Studio (APS-3) · 8 questions (6 MC + 2 short answer) · Answer key included

**Q1.** `AGENTS.md` says "A missing `org_id` filter is a cross-tenant data leak. Treat it as a P0 bug." Why P0 rather than a normal bug?

A. It slows queries down without an index on `org_id`.
B. One unfiltered query can return another tenant's rows to a valid, authenticated user — the worst failure a multi-tenant SaaS has, at the highest severity.
C. It only matters on admin routes; volunteer routes are read-only and safe.
D. SQLAlchemy adds tenant filters automatically once the model declares `org_id`.

**Q2.** A church's worship coordinator needs to lead services but should not manage the organization. What does SignUpFlow grant?

A. A department-scoped `worship_manager` permission role.
B. `admin`, since they lead a ministry — qualifications imply trust.
C. Access role `volunteer` plus the scheduling qualification `worship_leader` — qualifications never confer permissions.
D. Two permission roles, `volunteer` and `admin`, normalized into one array.

**Q3.** A logged-in member requests a person id that exists in another tenant. What response prevents resource enumeration, and why?

A. `403` — the requester must learn the resource exists but is not theirs.
B. `404` — the id is looked up inside the actor's tenant, so a foreign resource and a nonexistent one are indistinguishable.
C. `401` — the token must be re-validated for each target resource.
D. `403` everywhere is safer than mixing codes; attackers cannot learn anything from a single status code.

**Q4.** What does `tests/unit/test_api_route_auth_policy.py` actually compare?

A. The OpenAPI snapshot against the generated mobile client.
B. The policy dict in `api/route_auth_policy.py` against the live route table — failing on missing, stale, or miswired routes (e.g., policy says `admin` but the route wired `get_current_user`).
C. The README's route list against `CLAUDE.md`'s route list.
D. Each route's docstring against its dependency declarations.

**Q5.** Which tier pairing matches what each tier proves (per `docs/TESTING.md`)?

A. Unit tier uses real JWT; API tier mocks the database for speed.
B. API tier proves authentication over real HTTP with real JWT; integration tier uses the real DB (mocking it is a named anti-pattern); browser tier runs Playwright against a disposable live app; contract tier snapshots OpenAPI.
C. All seven tiers run in one pytest process for a single evidence count.
D. Playwright tests replace the web tier, so HTMX workflows need no coverage.

**Q6.** The browser playbook checks every published roster itself rather than trusting the solver's metrics. What does the independent oracle verify, and why isn't a health score of 100 enough?

A. It verifies the solver ran; health 100 means zero soft penalties, so it is sufficient.
B. It verifies exact role counts, distinct qualified assignees, non-overlap, and balanced loads — recomputed from the roster, because the health score is the solver's own output (0 on any hard violation, else 100 − soft/10), and self-reported scores are not an oracle.
C. It verifies page load times at 360px and 1440px.
D. It verifies only the critical role, since other roles are soft constraints.

**Q7.** In `docs/playbooks/coverage.json`, what does a scenario with status `blocked` mean — and why does the validator require such rows to include the `manual` tier? Why is "blocked" better than quietly deleting the row?

**Q8.** Write the test assertion sequence for: "volunteer A cannot edit volunteer B's availability, and B's record is unchanged." Name each assertion in order, the status code you expect, and the one assertion most teams forget.

---

## Answer key

**Q1 — B.** The filter is the tenant boundary; missing it exposes cross-tenant data to a perfectly valid session — P0 because it is a data-leak class, not a performance or style issue. *(Objective M5.1 — `AGENTS.md`, "Multi-tenancy and auth".)*

**Q2 — C.** Exactly one permission role (`volunteer`|`admin`) plus qualifications in the same array, never treated as permissions: "Do not grant admin access merely because someone leads a ministry" (`docs/playbooks/church.md`); `normalize_roles` rejects a second permission role ("Select exactly one account access role", `api/roles.py`). *(Objective M5.2.)*

**Q3 — B.** "A guessed resource identifier is looked up inside the actor's tenant and returns `404` whether it is foreign or absent" (`docs/API_AUTHORIZATION.md`); `get_person_in_actor_org` implements the lookup (`api/dependencies.py`). A, D are the enumeration misconceptions — a uniform 403 confirms existence. *(Objective M5.1.)*

**Q4 — B.** Set equality between `ROUTE_AUTH_POLICY` and the live routes catches missing/stale; the dependency-tree walk catches miswiring — the mechanism in `tests/unit/test_api_route_auth_policy.py` against `api/route_auth_policy.py`. *(Objective M5.2.)*

**Q5 — B.** Unit = mocked auth; API/security = real JWT on isolated SQLite; integration = real DB (mocking it is the named anti-pattern in `AGENTS.md`); browser = Playwright on a disposable live app; contract = OpenAPI snapshots (`docs/TESTING.md`); tiers run in separate processes. *(Objective M5.3.)*

**Q6 — B.** The oracle checks role counts, distinct qualified assignees, non-overlap, and balanced loads "before publication at both browser widths" (`docs/playbooks/README.md`); health = 0.0 with any hard violation, else `max(0.0, 100.0 - soft_score/10)` (`api/core/solver/heuristics.py`) — the solver cannot grade its own homework. *(Objective M5.3.)*

**Q7 — Acceptable answer:** `blocked` means a required scenario that cannot currently run — remaining work, "not passed scenarios" (`docs/playbooks/church.md`); the validator forces `manual`/`blocked` rows to carry the `manual` tier so they cannot masquerade as automated (`tests/playbooks/coverage.py`). Deleting the row is worse: required ids are pinned (BO-01..12; CH-01..08), so removal fails collection before any test runs — the manifest keeps scope honest instead of shrinking it. A `blocked` row is evidence of honesty; a missing row is a silent coverage lie. *(Objective M5.3 — `tests/playbooks/coverage.py`, `tests/playbooks/plugin.py`.)*

**Q8 — Acceptable sequence:** (1) authenticate as A with a real JWT; (2) snapshot B's availability row (or record its hash) before the attempt; (3) attempt the edit as A; (4) assert the denial — 403 for a same-tenant peer, 404 if B is foreign or absent (looked up inside A's tenant); (5) re-read B's record and assert it is byte-for-byte unchanged. The forgotten assertion is (5) — "assert forbidden writes leave database state unchanged" is step 4 of SignUpFlow's change protocol (`docs/API_AUTHORIZATION.md`); BO-03's browser drill "compares both records before and after to prove that the denial did not mutate the target member" (`docs/playbooks/README.md`). *(Objective M5.1/M5.2.)*