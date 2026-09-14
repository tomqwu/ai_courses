# Module 5 — The Spec-Driven SaaS: Multi-Tenant Security & Acceptance
> Part of AI Product Studio (APS-3) · ~75 minutes · Prerequisites: Module 4

## Overview

Module 4 turned a feature into an artifact set an agent could execute. This module asks the two questions a multi-tenant SaaS must answer before it deserves customers: **can one tenant ever see another tenant's data?** and **how do you prove the whole product works, operationally, not just functionally?** Your case study is SignUpFlow — a multi-tenant volunteer-scheduling API for churches, sports leagues, and non-profits on FastAPI + SQLAlchemy 2.0 + Pydantic 2, with JWT (HS256, 24h expiry) + bcrypt auth (`SignUpFlow/AGENTS.md`, "Repository purpose"). Churches and basketball leagues share one deployment and one database; if tenant isolation fails anywhere, a children's ministry rota leaks to a sports league — the kind of bug that ends a SaaS.

So Module 5 is two disciplines in one. First, **multi-tenancy as a cultural rule enforced by mechanisms**: an `org_id` filter classified as a P0 bug, a dependency that fails cross-tenant requests, tokens bound to a tenant, and status codes chosen so attackers cannot enumerate resources. Second, **acceptance as architecture**: a seven-tier test pyramid, operational playbooks with disruption drills, JSON fixtures that parameterize real test tiers, and a coverage manifest whose honesty is enforced by pytest itself. The through-line for an AI-assisted builder: agents generate queries at machine speed, and every generated query is a chance to forget a tenant filter — so the answer is rules that are verifiable ("Filter every query by `org_id`." not "Be careful with multi-tenancy" — `AGENTS.md`, "House style") and tests that catch every drift.

**By the end of this module you can:**

- Enforce tenant isolation with a dependency (`verify_org_member`), tenant-bound tokens, and deliberate 401/403/404 semantics that prevent resource enumeration.
- Separate permission roles (`volunteer`/`admin`) from scheduling qualifications (`usher`, `coach`) in the same data, and explain why conflating them is a security bug.
- Make an authorization matrix executable: a policy file that classifies every route, plus a test that fails on missing, stale, or miswired routes.
- Design playbook acceptance: six-week operational scenarios, disruption drills, an independent oracle, and a coverage manifest whose statuses (automated/partial/manual/blocked) are honest by construction.

> **Pointer convention.** SignUpFlow pointers are relative to the cloned repo root (e.g., `api/dependencies.py` = `SignUpFlow/api/dependencies.py`). Open every file the action steps name — the pointers are this course's provenance.

## Segment M5.1 — Multi-tenancy as a P0 cultural rule (~25 min)

### Objective

Explain why SignUpFlow classifies a missing `org_id` filter as a P0 bug, trace the three mechanisms that enforce isolation (the membership check, the tenant-bound token reload, the admin gate), and adopt status-code semantics that leak no information to an attacker.

### Lesson

Start with the rule, quoted in full from `AGENTS.md` ("Multi-tenancy and auth (project-critical)"):

> "Every database query MUST filter by `org_id`." … "A missing `org_id` filter is a cross-tenant data leak. Treat it as a P0 bug."

Notice where this lives: not in a security wiki, but in `AGENTS.md` — the universal baseline consumed by Codex CLI, Cursor, Aider, Jules, OpenHands, Sourcegraph Amp, and Factory (`AGENTS.md`, header). That placement is the point. Any agent that opens the repo to write a query reads the P0 rule first, and the rule is written in the house style: imperative, verifiable, no judgment call. A "P0 bug" is not a severity you negotiate during triage — a query that skips the filter does not ship. Cultural rules only work when they are this concrete; "be careful with multi-tenancy" is a vibe, "Filter every query by `org_id`" is a check.

The rule has three mechanical enforcers in `api/dependencies.py`:

1. **Membership check.** `verify_org_member(person, org_id)` compares `person.org_id != org_id` and raises `403` with "Access denied: not a member of this organization" (`api/dependencies.py`, lines 46–58). Routes that take an explicit organization or person reference call it before any query runs.
2. **Tenant-bound credential reload.** `get_current_user` decodes the JWT, requires both the `sub` (person id) and the `org_id` claims to be strings, then reloads the person with a single three-way filter: `Person.id == person_id`, `Person.org_id == token_org_id`, `Person.status == "active"` (`api/dependencies.py`, lines 97–121). Anything else is `401`. The person is not trusted from the token alone and not trusted from the request body — the token *points at* a row that must still exist, still be active, and still belong to the tenant the token was issued for. This is what `docs/API_AUTHORIZATION.md` calls "Session And Tenant Binding": every access token and browser session carries both the person `sub` and the `org_id`, and "a missing tenant claim, mismatched tenant claim, inactive membership, or deleted person invalidates the credential" (lines 28–33).
3. **The admin gate.** `get_current_admin_user` wraps `get_current_user` and raises `403` "Admin access required" unless the loaded person has the documented admin role (`api/dependencies.py`, lines 138–153).

Routes protect themselves with `Depends(get_current_user)` or `Depends(get_current_admin_user)`, and the rule that makes the whole pattern safe is one line in `AGENTS.md`: "**Never read user state from the request body.**" The body is attacker-controlled input; identity and tenant come only from the validated credential. The moment a route accepts `user_id` or `org_id` from JSON and trusts it, no downstream filter saves you.

**Bootstrap and growth.** Tenancy is sealed at account creation. `POST /auth/signup` "atomically creates a new organization and its first `admin`. Never use it to join an existing organization; all later accounts require an invitation" (`AGENTS.md`, line 59). `CLAUDE.md` states the negative space: signup "rejects an existing organization ID," "there is no public empty-organization endpoint," and later accounts join only through administrator-created invitations. No public surface lets a stranger insert themselves into your tenant — growth is invitation-only by construction, and invitations are single-use tokens (BO-02 in `docs/playbooks/coverage.json`: "Invitations are single-use and qualifications do not grant administrator access").

**Deliberate status semantics.** Multi-tenant APIs leak information through error codes as surely as through data. SignUpFlow's contract is written down and tested (`docs/API_AUTHORIZATION.md`, lines 21–24):

| Situation | Status | Why |
|---|---|---|
| Invalid bearer token | `401` | The credential itself failed — nothing is known about the requester. |
| Missing bearer token on a protected route | `403` | FastAPI `HTTPBearer`'s default, retained deliberately and documented. |
| Authenticated actor naming an explicit foreign organization | `403` | Valid credential, wrong tenant — a policy denial, not an auth failure. |
| Guessed resource identifier | `404` | "a guessed resource identifier is looked up inside the actor's tenant and returns `404` whether it is foreign or absent." |

The last row is the anti-enumeration mechanism. If a foreign id returned `403` ("exists, but not yours"), an attacker with a valid account could walk your id space and map which resources exist. Instead, target rows are loaded *through the actor's organization* first — `get_person_in_actor_org` queries `Person.id == person_id AND Person.org_id == actor.org_id` and raises `404` if nothing matches (`api/dependencies.py`, lines 61–66) — so a foreign person and a nonexistent person are indistinguishable. The `docs/API_AUTHORIZATION.md` scheduling table applies the pattern per route family: availability reads load "the target person through the actor's organization first; same-tenant peers receive `403`, foreign or absent people receive `404`" (line 47). Enumeration dies because both answers look like a miss.

One subtlety: many teams "fix" the missing-bearer case to `401` on REST-purism grounds. SignUpFlow instead documents the behavior it actually has (HTTPBearer's `403`) and tests it. The lesson is not which code is philosophically correct — it is that a status contract must be *deliberate and enforced*, because an undocumented status code is an unspecified information channel.

### Action step

1. Open `AGENTS.md` ("Multi-tenancy and auth") and copy the P0 sentence into your evidence log, verbatim.
2. Open `api/dependencies.py`. Find `verify_org_member`, `get_person_in_actor_org`, and the three-way `Person` filter inside `get_current_user`. Write one sentence each on what they refuse.
3. Open `docs/API_AUTHORIZATION.md` and copy the four-row status semantics into your evidence log.
4. In your own project's `AGENTS.md`: write your P0 tenancy rule and your 401/403/404 table. Imperative voice, no adjectives.

## Segment M5.2 — RBAC done right: permissions ≠ qualifications (~25 min)

### Objective

Keep two vocabularies that share a JSON array from contaminating each other — what an account *may do* (permissions) versus what a person *can do* (qualifications) — and make the whole authorization surface executable so drift fails a test rather than a customer.

### Lesson

A `Person` in SignUpFlow carries one `roles` JSON array holding two unrelated kinds of strings (`api/models.py` via `CLAUDE.md` "Key Patterns"). **Permission roles** are exactly one of `volunteer` or `admin` — enforced by the frozenset `PERMISSION_ROLES = {"admin", "volunteer"}` (`api/roles.py`, line 8) and by the rule "Grant exactly one permission role" (`AGENTS.md`, line 60). A `volunteer` views own data and manages availability; an `admin` gets full CRUD, the solver, and invitations (`CLAUDE.md`, "RBAC"). **Scheduling qualifications** — `usher`, `coach`, `worship_leader`, `musician`, `sound`, `children_leader` — live in the *same* array but are "never interpreted as permissions" (`AGENTS.md`, line 60). The solver uses them to decide who may fill a role slot; no code path uses them to decide who may administer.

The trap this prevents is the natural-language one: "she leads worship, so she should have the admin toggle." `docs/playbooks/church.md` refuses it in one sentence — "**Do not grant admin access merely because someone leads a ministry.** The app has only admin/volunteer access levels, not department-scoped manager permissions" (lines 26–27). The actors table above that line shows the Worship coordinator — operationally the most important volunteer — with access `volunteer` plus qualification `worship_leader`, not `admin` (line 19). The product has no "manager of the music ministry" authority level; pretending a qualification is one would mint a new privilege every time someone invents a skill string.

The separation is executable in `api/roles.py`. `normalize_roles` sorts an admin-supplied array: exact matches to `PERMISSION_ROLES` are permission roles, anything else is a qualification — but a case-folded collision (`"ADMIN"`) raises `"is an ambiguous permission role"`, and more than one permission role raises `"Select exactly one account access role"` (lines 38–53). `parse_qualifications` rejects qualification strings that casefold to `admin`/`volunteer` (lines 19–20). The data shape admits both vocabularies; the policy keeps them disjoint, and drifted input fails loudly instead of escalating quietly.

**The executable authorization matrix.** Knowing the rules is not enough — SignUpFlow checks that every mounted route obeys them, on every test run. `api/route_auth_policy.py` classifies every FastAPI operation by name into exactly five policy classes: `public` (7 operations — `signup`, `login`, `health_check`, …), `public-token` (scoped-token routes: invitation accept/verify, refresh, password reset, calendar feed), `public-callback` (the Twilio webhooks, disabled by default), `member` (50 operations), and `admin` (78 operations, including `create_invitation`, `solve_schedule`, `publish_solution`) — 143 classified operations in total. The `ROUTE_AUTH_POLICY` dict is the executable source of truth; `docs/API_AUTHORIZATION.md` opens by saying exactly that (lines 3–9).

The enforcement is `tests/unit/test_api_route_auth_policy.py` — 37 lines that fail on three classes of drift:

- **Missing:** the test walks the live route table (`app.routes`, filtered to `/api` plus `/health`/`/ready`) and asserts `set(ROUTE_AUTH_POLICY) == set(routes)` — add a route without classifying it and set equality fails.
- **Stale:** the same assertion fails in reverse when a policy entry names a route that no longer exists.
- **Miswired:** for each classified route, the test collects the names of its dependency tree and asserts wiring: `admin` routes must depend on `get_current_admin_user`, `member` routes on `get_current_user`, and public routes on neither (`tests/unit/test_api_route_auth_policy.py`, lines 19–37).

A policy entry that says `admin` while the route accidentally wired `get_current_user` is caught mechanically. This is the matrix made executable: the doc describes intent, the dict encodes it, the test compares the dict to the live app.

**The six-step change protocol.** `docs/API_AUTHORIZATION.md` (lines 59–76) prescribes how to change authorization safely:

1. Add or change the route's explicit entry in `api/route_auth_policy.py`.
2. Apply actor-derived tenant and ownership filters **in the route query itself** — not in a helper you hope gets called.
3. Add real-JWT tests for anonymous, invalid, member, same-tenant admin, and foreign-admin actors wherever the operation can expose tenant data or mutate state.
4. Assert forbidden writes leave database state unchanged, and exports receive an already-filtered dataset before serialization.
5. Refresh the OpenAPI snapshot and the generated mobile client when the contract changes.
6. Run the matrix and scheduling regressions locally:

```bash
poetry run pytest tests/unit/test_api_route_auth_policy.py tests/api/test_access_token_tenancy.py tests/api/test_scheduling_tenant_boundaries.py tests/security/test_authentication.py -q
```

The protocol closes with the rule that kills the tempting shortcut: "Do not use the tenancy warning listener as authorization. Every query that can reach organization data must carry the concrete tenant predicate required by the route's policy" (`docs/API_AUTHORIZATION.md`, lines 74–76). A log line that warns about a missing filter is observability; the filter in the query is the control.

Step 4 deserves emphasis because it is the one most teams skip: a denied write that mutates the database anyway is a security bug wearing a test-green costume. Assert the denial *and* the unchanged row.

### Action step

1. Open `api/roles.py` and read `normalize_roles` end to end. Record the two `ValueError` messages and what input triggers each.
2. Open `api/route_auth_policy.py`. Confirm `signup` sits in `PUBLIC_OPERATIONS` and `publish_solution` in `ADMIN_OPERATIONS`, and count the five policy classes.
3. Open `tests/unit/test_api_route_auth_policy.py` and label its three failure classes in your own words: missing, stale, miswired.
4. Write the six-step protocol into your project's contribution guide, replacing each SignUpFlow path with your own equivalents.

## Segment M5.3 — Acceptance: seven tiers, playbooks, and an honest manifest (~25 min)

### Objective

Design acceptance as a tier pyramid that proves different properties per tier, playbook scenarios that test failure modes a feature list cannot, and a coverage manifest whose honesty is validated by pytest before a single test collects.

### Lesson

**The seven-tier pyramid.** `docs/TESTING.md` (2026-09-14 policy) defines seven Python tiers, each run in a separate process by `make test-all` — API and browser event-loop fixtures differ, so combining them in one pytest process is forbidden (lines 48–50):

1. **Unit** (`tests/unit/`) — fast regressions, mocked auth via `conftest.py`; proves business logic.
2. **API + security** (`tests/api/`, `tests/security/`) — real HTTP, real JWT, isolated SQLite; proves authentication, tenancy, the route contract.
3. **CLI** (`tests/cli/`) — subprocess, YAML in, JSON out; proves the headless path.
4. **Integration** (`tests/integration/`) — real database; proves persistence. Mocking the DB here is a named anti-pattern (`AGENTS.md`).
5. **Web** (`tests/web/`) — in-process cookie and HTMX workflows; proves the server-rendered surface.
6. **Contract** (`tests/contract/`) — OpenAPI snapshot compatibility; proves clients don't break.
7. **Browser** (`tests/e2e/`) — Playwright against a disposable live app; proves a human-shaped journey.

The full-suite evidence is recorded, dated, and bounded: "1,464 passed, 21 skipped" across backend, web, contract, and browser suites in `docs/playbooks/validation.md` ("Acceptance evidence - 2026-09-12"). That file also carries its own demotion banner — reclassified 2026-09-13 as historical reference, "not current policy or live test status" — while `docs/TESTING.md` remains current. Evidence with a date is evidence; evidence with a date *and a retirement plan* is discipline.

**Playbook acceptance.** Test tiers prove the machinery works; playbooks prove the product can be *operated*. `docs/playbooks/` ships two six-week operational scenarios — church and basketball — plus shared journeys. `church.md` is genuinely operational, in three ways:

- An **actors/access table**: every actor's access level is one of `admin`, `volunteer + qualification`, or explicitly human — the Ministry approver's access is "Human organizational responsibility" (`church.md`, lines 14–24).
- A **weekly operating rhythm**: Monday the administrator reviews the horizon; Tuesday members record absences; Friday gaps are resolved and the roster published; after service, follow-ups are recorded (lines 51–61).
- **Disruption drills with acceptance criteria** — CH-01 through CH-08. The flagship is CH-04: "Block both worship leaders for Sunday week 4 and attempt publication" → acceptance: "**Exactly that service reports missing worship leadership; publication is rejected and the prior roster stays live**" (line 73). Read what that tests: not the happy path, but the *failure mode* — an incomplete regeneration may not destroy the published roster. Acceptance criteria about rejection are what separate a demo from a product.

The shared journeys BO-01..12 (baseline roster, availability self-service, recurrence, rolling horizon, local mail capture, calendar, account recovery, **two-tenant isolation**, late cover, qualification changes, schedule changes) and domain drills CH-D01..03 / BB-D01..03 bind both domains to the same journeys; every row lives in `docs/playbooks/coverage.json`.

The scenarios are executable because they are data. `docs/playbooks/church.json` (13 lines) declares the domain: `id`, `version`, `workflow: "six_week_roster"`, `name`, `event`, a `roles` headcount map (`worship_leader: 1, musician: 2, sound: 1, usher: 2, children_leader: 1` — seven distinct people per event), `secondary_event`, `critical_role`, and drill selectors like `late_cover_roles`. A pytest plugin (`tests/playbooks/plugin.py`) discovers these JSON files, parameterizes tests with stable IDs, and supports `--playbook` / `--playbook-dir`; the API tier runs them with real JWT identities against isolated in-memory SQLite, and the browser tier starts the real application on a temporary database — at **360px and 1440px** (`docs/playbooks/README.md`, lines 28–38). The browser journey invites fourteen baseline members plus a qualified replacement and builds six primary plus six rehearsal sessions from the fixture, then verifies the complete 84-slot roster.

Every solve is checked by an **independent oracle**: "An independent oracle checks exact role counts, distinct qualified assignees, non-overlap, and balanced loads before publication at both browser widths" (`docs/playbooks/README.md`, lines 37–38). *Independent* is the load-bearing word — the oracle recomputes correctness from the roster itself: seven distinct qualified people per event, no person in two slots of one event, no overlaps, and interchangeable people's baseline loads differing by at most one (CH-01, `church.md`, line 70). It never asks the solver whether the solver did a good job.

**The honest manifest.** `docs/playbooks/coverage.json` binds every BO/CH/BB scenario to actor, precondition, operation, expected result, execution tiers, evidence paths, and a **status**. Four statuses exist (`tests/playbooks/coverage.py`, line 18): `automated`, `partial`, `manual`, `blocked`. Two coupling rules make dishonesty structurally hard (lines 43–46): `automated` or `partial` rows must include an executable tier, and `manual` or `blocked` rows must include the `manual` tier — a blocked scenario therefore *cannot* be dressed up as automated. `church.md` states the reading: "its partial or blocked rows are remaining work, not passed scenarios" (lines 11–12).

The manifest is validated **before collection**: the plugin's `pytest_configure` hook loads and cross-checks it, and any `ValueError` becomes `pytest.UsageError` — the run dies before a single test executes (`tests/playbooks/plugin.py`, lines 37–45). The validators are structural, not cosmetic: shared scenarios must be exactly BO-01..12; each domain must carry exactly CH-01..08 plus CH-D01..03; each domain must declare exactly one `admin` actor and at least one `human` responsibility boundary; actor qualifications must match the playbook fixture's roles (`tests/playbooks/coverage.py`, lines 87–103, 117–128, 131–155). As the README puts it: "Removing a bundled domain, required scenario, administrator, human boundary, or scheduling qualification fails collection" (`docs/playbooks/README.md`, lines 85–87). In the current manifest all bundled rows are `automated` — several carrying a `manual` tier alongside (CH-D02, CH-D03, BB-D01, BB-D03) — so the reserved statuses are the vocabulary for admitting what is *not* yet proven. That is the manifest's honesty contract: statuses describe reality, and removing an uncomfortable row breaks the build.

**The solver cameo — classic algorithm, agent-built, oracle-guarded.** The scheduling core is `GreedyHeuristicSolver`, 357 lines in `api/core/solver/heuristics.py` ("Feasible-first greedy solver"): sort events; for each required role, filter candidates by qualification, overlap, vacation, and hard constraints; score the rest by soft-constraint penalties plus a fairness term (`penalty += assignment_count * 10`, line 239) minus a change-minimization bonus (default weight 100, lines 35 and 243–244) when the (event, person) pair was in the prior published solution; pick the lowest penalty. Its metrics are brutally simple: **health score = 0.0 if any hard violation exists, else `max(0.0, 100.0 - soft_score / 10)`** (lines 318–323), and **fairness = the standard deviation of per-person assignment counts** (lines 305–313). The algorithm is classic; what makes it course material is the traceable AI-assisted evolution — the change-min code comment points straight at its spec: "Loose match (event_id, person_id) — see specs/020-solver-quality-changemin" (lines 36–37) — and the oracle checks every solve it produces. Even the input language is fenced: the REST constraints DSL supports exactly three predicates (`max_assignments` hard, `min_gap_hours` hard, `cooldown` soft-weighted — `docs/SCHEDULING_CONSTRAINTS.md`), invalid input returns `422`, never a silent no-op, and the doc closes the fence in one line: "**The REST mapper is not an arbitrary expression language.**" (lines 82–85). Classic algorithm, agent-built, oracle-guarded — and honest about its limits: "attendance, ministry suitability, actual communication and service execution remain human responsibilities, not inferred from a green solver score" (`church.md`, lines 63–64).

### Action step

1. Open `docs/playbooks/coverage.json`. Find one `automated` scenario (e.g., BO-04) and one row whose `tiers` include `manual` (e.g., CH-D02). Then open `tests/playbooks/coverage.py`, find the four allowed statuses and the two coupling rules, and post to the community: what would a `blocked` row mean, and why can a blocked row never look automated?
2. In a scratch copy, delete one BO id from `coverage.json` and run `poetry run pytest tests/api --collect-only -q`. Watch the run fail in `pytest_configure` — before any test collects. Record the error, then revert.
3. Open `docs/playbooks/church.json` and copy its shape into your evidence log — you will author your own fixture in Lab M5.
4. Trace one AI-assisted feature end to end: open `specs/020-solver-quality-changemin/spec.md`, then find the comment in `api/core/solver/heuristics.py` (lines 36–37) that cites it, then the CH-03/CH-04 oracle rows that guard it.

## Recap

- **M5.1 — Tenancy is a P0 rule with mechanisms.** Every query filters by `org_id`; a missing filter is "a cross-tenant data leak. Treat it as a P0 bug" (`AGENTS.md`). `verify_org_member` enforces membership (`api/dependencies.py`), tokens bind person `sub` + `org_id` and reload an active person by both, signup atomically creates org + first admin with no public join, and the 401/403/404 contract makes guessed ids `404` inside the actor's tenant so foreign and absent resources are indistinguishable — enumeration dies.
- **M5.2 — Permissions ≠ qualifications.** Exactly one permission role (`volunteer`/`admin`); qualifications (`usher`, `coach`, `worship_leader`) share the array but never confer authority — "Do not grant admin access merely because someone leads a ministry" (`docs/playbooks/church.md`). `api/route_auth_policy.py` classifies every mounted route into five classes; `tests/unit/test_api_route_auth_policy.py` fails on missing, stale, or miswired routes; and the six-step `docs/API_AUTHORIZATION.md` protocol ends by asserting forbidden writes leave the DB unchanged.
- **M5.3 — Acceptance is tiers + playbooks + an honest manifest.** Seven tiers each prove something different (mocked-auth unit through real-app Playwright at 360px/1440px); playbooks test failure modes (CH-04: publication rejected, prior roster stays live); JSON fixtures parameterize API and browser tiers behind an independent oracle (exact role counts, distinct qualified assignees, non-overlap, loads within one); and `coverage.json` statuses (automated/partial/manual/blocked) are coupled to tiers and validated before collection — removing a scenario fails the run. The 357-line greedy solver (health = 0 on any hard violation, else 100 − soft/10) is classic code, agent-evolved under a spec pointer, and oracle-guarded.

## Discussion prompt

Post to the community (~150 words): your product stores data for multiple customers. A teammate argues "an ORM with foreign keys is enough — we don't need org filters on every query." Using at least three SignUpFlow file pointers, write the reply: name the mechanism that fails without the filter, the status code a guessed foreign id should return and why, and the one test assertion you would write first to prove your point (hint: it involves a forbidden write and an unchanged row).