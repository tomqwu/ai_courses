---
marp: true
theme: aps
paginate: true
title: M5 — Multi-Tenant Security & the Acceptance Gate
---

# M5 — Multi-Tenant Security & the Acceptance Gate

**Promise:** prove tenant isolation with tests, then prove the product is operable.
**Duration:** ~75 min lesson + ~3 h Lab M5.
**Case study:** SignUpFlow · `api/dependencies.py`, `docs/playbooks/coverage.json`

<!-- NOTES: Welcome to Module 5, the security and acceptance gate of the SaaS track. Two questions drive everything today. First: can one tenant ever see another tenant's data? Second: how do you prove the whole product works operationally, not just functionally? SignUpFlow is the case study — a multi-tenant volunteer-scheduling API where churches and basketball leagues share one database. The promise is a pair of artifacts: negative-path tests that prove isolation, plus a playbook manifest that admits what is not proven. Timing: M5.1 about 25 minutes, M5.2 about 25, M5.3 about 25, then the three-hour lab. Transition: here is exactly what you will be able to do. -->

---

## By the end you can…

- **Enforce** tenant isolation with a dependency
- **Bind** tokens to a tenant, reload active rows
- **Choose** deliberate 401/403/404 semantics
- **Separate** permission roles from qualifications
- **Make** the authorization matrix executable
- **Design** acceptance: tiers, playbooks, honest manifest

<!-- NOTES: Read these as six verbs, not six topics. Every one is something you do in the lab. Enforce, bind, choose, separate, make, design. The first three are the isolation discipline; the middle two are the authorization discipline; the last is the acceptance discipline. Notice the through-line: agents generate queries at machine speed, and every generated query is a chance to forget a tenant filter. So the answer is not "be careful" — it is rules a machine can check and tests that catch drift. If you remember one slide, remember the P0 rule on the next one. Transition: start with the rule itself. -->

---

## M5.1 — The rule lives in `AGENTS.md`

- "Every database query MUST filter by `org_id`."
- "A missing `org_id` filter is a cross-tenant data leak."
- "Treat it as a P0 bug."
- Baseline every agent reads before writing a query.
- Verifiable rule, not a vibe.

`SignUpFlow/AGENTS.md:57,61`

<!-- NOTES: Open `AGENTS.md` on screen and read lines 57 and 61 aloud. Notice where this lives: not a security wiki, but the cross-agent baseline that Codex CLI, Cursor, Aider, Jules, OpenHands, Sourcegraph Amp, and Factory all read natively. That placement is the point — every agent that opens the repo to write a query reads the P0 rule first. And notice the wording. "Filter every query by `org_id`" is a check. "Be careful with multi-tenancy" is a vibe. Cultural rules only work when they are this concrete. A P0 bug is not a severity you negotiate in triage: that query does not ship. Transition: a rule needs mechanisms, or it is decoration. -->

---

## M5.1 — Three mechanical enforcers

1. `verify_org_member` — foreign org → `403`
2. `get_current_user` — reload by id **and** `org_id`
3. `get_current_admin_user` — admin gate → `403`

- Identity from the credential only.
- "Never read user state from the request body."

`SignUpFlow/api/dependencies.py:46,78,138` · `SignUpFlow/AGENTS.md:58`

<!-- NOTES: One file, three enforcers. `verify_org_member(person, org_id)` compares `person.org_id != org_id` and raises 403 with "Access denied: not a member of this organization", lines 46 to 58. `get_current_user` decodes the JWT, requires the `sub` and `org_id` claims, then reloads the person with a three-way filter: id, tenant, and active status — anything else is 401, so the token *points at* a row that must still exist and still belong to that tenant. `get_current_admin_user` wraps it and raises 403 unless the role is admin. The line that makes it safe is line 58 of AGENTS.md: never read user state from the request body. The body is attacker-controlled input. Transition: what do you return when the ids do not match? -->

---

## M5.1 — Deliberate status semantics

| Situation | Status |
|---|---|
| Invalid bearer token | `401` |
| Missing bearer token, protected route | `403` |
| Authenticated actor names foreign org | `403` |
| Guessed resource identifier | `404` |

`SignUpFlow/docs/API_AUTHORIZATION.md:21-24`

<!-- NOTES: Four rows, and each one is a decision rather than an accident. Invalid bearer token is 401 because the credential itself failed — nothing is known about the requester. Missing bearer token stays at 403 because that is FastAPI HTTPBearer's default, and SignUpFlow documents the behavior it actually has instead of "fixing" it to 401 on REST-purism grounds. An explicit foreign organization is 403: valid credential, wrong tenant, a policy denial. The last row is the important one: a guessed resource identifier returns 404. Hold that thought for the next slide. Transition: why 404, and not 403? -->

---

## M5.1 — Enumeration dies at `404`

- Target loaded **through the actor's organization first**.
- `Person.id == person_id AND Person.org_id == actor.org_id`.
- Foreign and absent resources look identical.
- Uniform `403` would confirm existence.
- An attacker with an account could map your id space.

`SignUpFlow/api/dependencies.py:61-66` · `docs/API_AUTHORIZATION.md:23`

<!-- NOTES: This is the anti-enumeration mechanism, and it is one query shape. `get_person_in_actor_org` loads the target row with both the id and the actor's org in the WHERE clause, and raises 404 when nothing matches. So a foreign person and a nonexistent person produce the same answer: a miss. If a foreign id returned 403 — "exists, but not yours" — an attacker with a perfectly valid account could walk your id space and map which resources exist. Availability routes apply the same pattern: same-tenant peers get 403, foreign or absent people get 404. The lesson is not which code is philosophically correct; it is that an undocumented status code is an unspecified information channel. Transition: how does anyone get into a tenant in the first place? -->

---

## M5.1 — Growth is invitation-only

- `POST /auth/signup` creates org **and** first admin.
- It never joins an existing organization.
- No public empty-organization endpoint.
- Later accounts need a single-use invitation.
- A qualification never grants administrator access.

`SignUpFlow/AGENTS.md:59` · `docs/playbooks/coverage.json` (BO-02)

<!-- NOTES: Tenancy is sealed at account creation. Signup atomically creates a new organization and its first admin, and AGENTS.md is explicit: never use it to join an existing organization; later accounts require an invitation. The negative space matters too — no public endpoint creates an empty organization, so a stranger cannot insert themselves into your tenant. Growth is invitation-only by construction, and BO-02 in the coverage manifest pins the rule: invitations are single-use and qualifications do not grant administrator access. Transition: that last phrase is the whole of M5.2 — permissions versus qualifications. -->

---

## Proof M5.1 — the rule you can grep

- `SignUpFlow/AGENTS.md:57` — "Every database query MUST filter by `org_id`."
- `SignUpFlow/AGENTS.md:61` — "Treat it as a P0 bug."
- `SignUpFlow/api/dependencies.py:46-66` — membership + actor-org lookup.
- `SignUpFlow/api/dependencies.py:78-121` — tenant-bound reload.
- `SignUpFlow/docs/API_AUTHORIZATION.md:21-24` — the four status rows.

<!-- NOTES: This is the proof slide for segment M5.1, so write these five pointers into your evidence log now — they are the provenance for everything you claim in the lab. The pattern to learn: rule in the baseline, mechanism in the dependency, contract in the authorization doc, and a test for each. When you write your own project's tenancy section, you are copying this four-part shape, not the prose. One caution: a log line that warns about a missing filter is observability; the filter in the query is the control. Transition: now the two vocabularies that share one JSON array. -->

---

## M5.2 — Two vocabularies, one array

- **Permission roles:** exactly one of `admin`/`volunteer`.
- **Qualifications:** `usher`, `coach`, `worship_leader`, `sound`.
- Same `roles` JSON array — different jobs.
- Qualifications never decide authority.
- A qualification never grants admin authority.

`SignUpFlow/api/roles.py:8` · `docs/playbooks/church.md:26`

<!-- NOTES: A Person carries one roles array holding two unrelated kinds of strings. Permission roles are what an account *may do*, and there are exactly two: admin and volunteer, enforced by the frozenset at api/roles.py line 8. Qualifications are what a person *can do* — usher, coach, worship_leader — and the solver uses them to fill role slots. They share the array; they never share meaning. The trap is the natural-language one: "she leads worship, so she should have the admin toggle." Church.md refuses it in one sentence: do not grant admin access merely because someone leads a ministry. Its actors table shows the worship coordinator as volunteer plus worship_leader, not admin. Transition: the policy is not prose — it is executable. -->

---

## M5.2 — Drifted input fails loudly

- `normalize_roles` sorts an admin-supplied array.
- Exact match to `PERMISSION_ROLES` → permission role.
- Anything else → qualification.
- `"ADMIN"` → "is an ambiguous permission role".
- Two permission roles → "Select exactly one account access role".

`SignUpFlow/api/roles.py:38-53`

<!-- NOTES: Open `api/roles.py` and read `normalize_roles` end to end. The data shape admits both vocabularies; the policy keeps them disjoint. Exact matches to `PERMISSION_ROLES` are permission roles; everything else is a qualification — but a case-folded collision like "ADMIN" raises, and more than one permission role raises "Select exactly one account access role". That is the design principle: drifted input fails loudly instead of escalating quietly. A silent normalization is how a qualification becomes a privilege. Transition: knowing the rules is not enough — every mounted route has to obey them. -->

---

## M5.2 — The authorization matrix, made executable

- `api/route_auth_policy.py` classifies every route, five classes.
- `public` 7 · `public-token` 6 · `public-callback` 2.
- `member` 50 · `admin` 78.
- `ROUTE_AUTH_POLICY` is the executable source of truth.
- The doc describes intent; the dict encodes it.

`SignUpFlow/api/route_auth_policy.py:8-171` · `docs/API_AUTHORIZATION.md:3`

<!-- NOTES: This is the heart of M5.2. `api/route_auth_policy.py` names every FastAPI operation and assigns it to exactly one of five policy classes. The counts in the current clone are seven public operations, six scoped-token operations, two public callbacks, fifty member operations, and seventy-eight admin operations. The ROUTE_AUTH_POLICY dict at line 166 is the executable source of truth, and `docs/API_AUTHORIZATION.md` opens by saying exactly that. A matrix written only in prose rots the first time someone adds a route; a dict plus a test does not. Transition: here is the test that keeps it true. -->

---

## M5.2 — Three classes of drift

- **Missing:** a route with no policy entry
- **Stale:** a policy entry with no route
- **Miswired:** policy says `admin`, route uses `get_current_user`

- Test walks `app.routes`; asserts set equality.
- Then walks each route's dependency tree.

`SignUpFlow/tests/unit/test_api_route_auth_policy.py` (37 lines)

<!-- NOTES: The enforcement is 37 lines, and it catches three failure classes. Missing and stale are both set equality between the policy dict and the live route table: add a route without classifying it and the assertion fails; leave an entry for a deleted route and it fails in reverse. Miswiring is the subtle one — for each classified route the test collects the names of its dependency tree and asserts that admin routes depend on `get_current_admin_user`, member routes on `get_current_user`, and public routes on neither. A policy entry that says admin while the route accidentally wired the member dependency is caught mechanically. Transition: this test is a hope until you have seen it fail. -->

---

## Proof M5.2 — matrix + gate + protocol

- `SignUpFlow/api/route_auth_policy.py:8-171` — 5 classes, 143 operations.
- `SignUpFlow/tests/unit/test_api_route_auth_policy.py` — drift test.
- `SignUpFlow/docs/API_AUTHORIZATION.md:59-76` — six-step change protocol.
- `SignUpFlow/api/roles.py:38-53` — normalization refusals.
- `SignUpFlow/docs/playbooks/church.md:19` — volunteer + `worship_leader`.

<!-- NOTES: Proof slide for M5.2. Count the classes yourself when you open the file — five sets, 143 operations total. The six-step protocol at lines 59 to 76 of the authorization doc is what you will write into your own contribution guide: change the policy entry, apply actor-derived filters in the route query itself, add real-JWT tests for anonymous, invalid, member, same-tenant admin and foreign admin, assert forbidden writes leave the database unchanged, refresh the OpenAPI snapshot, then run the matrix and scheduling regressions locally. The protocol closes with the rule that kills the shortcut: do not use the tenancy warning listener as authorization. Transition: step four is the one teams skip, and M5.3 is about proving things like it. -->

---

## M5.2 — The six-step change protocol

1. Update the route's policy entry.
2. Filter by tenant **in the query itself**.
3. Add real-JWT tests for five actor kinds.
4. Assert forbidden writes leave the DB unchanged.
5. Refresh the OpenAPI snapshot and client.
6. Run the matrix and scheduling regressions locally.

`SignUpFlow/docs/API_AUTHORIZATION.md:59-76`

<!-- NOTES: Read these as a checklist you can paste into a pull-request template. Step two is where the shortcut lives — apply actor-derived tenant and ownership filters in the route query itself, not in a helper you hope gets called. Step three names five actors: anonymous, invalid, member, same-tenant admin, and foreign admin. Step four is the one most teams skip: a denied write that mutates the database anyway is a security bug wearing a test-green costume, so assert the denial *and* the unchanged row. Step six is local, because SignUpFlow runs no CI. Transition: that brings us to acceptance — seven tiers and an honest manifest. -->

---

## M5.3 — Seven tiers, separate processes

- Unit: mocked auth · API: real JWT, real HTTP
- CLI: YAML in, JSON out · Integration: real DB
- Web: cookies and HTMX · Contract: OpenAPI snapshots
- Browser: Playwright on a disposable live app
- Do not combine API and browser tiers in one process.

`SignUpFlow/docs/TESTING.md:38-46,49-50` · `make test-all`

<!-- NOTES: Seven tiers, each proving something the others cannot. Unit is fast regressions with mocked auth. API and security is real HTTP with real JWT on isolated SQLite — that is where your isolation tests live. CLI proves the headless path; integration uses a real database, and mocking the DB there is a named anti-pattern in AGENTS.md. Web covers cookies and HTMX in process; contract snapshots OpenAPI compatibility; browser runs Playwright against a disposable live app. They run in separate processes because the API and browser event-loop fixtures differ — `make test-all` keeps them apart and stops on failure. Transition: what does the recorded evidence look like? -->

---

## Proof M5.3 — dated evidence, with a retirement plan

- `docs/playbooks/validation.md:1` — "Acceptance evidence - 2026-09-12".
- `:88` — "1,464 passed, 21 skipped" across four suites.
- `:36` — complete unit tier: "399 passed, 21 skipped".
- `:3` — reclassified 2026-09-13 as historical reference.
- `docs/TESTING.md` remains the current policy.

`SignUpFlow/docs/playbooks/validation.md`

<!-- NOTES: Here is the number you may quote, and exactly how to quote it. In `docs/playbooks/validation.md`, dated 2026-09-12, the recorded full-suite evidence is "1,464 passed, 21 skipped" across backend, web, contract, and browser suites; the complete unit tier alone was "399 passed, 21 skipped". Now read the banner at line 3: that file was reclassified on 2026-09-13 as historical reference, "not current policy or live test status", and `docs/TESTING.md` is current. Evidence with a date is evidence. Evidence with a date *and* a retirement plan is discipline. Never quote the 1,464 as today's status. Transition: tiers prove machinery; playbooks prove the product can be operated. -->

---

## M5.3 — Playbook acceptance: test the failure mode

- Two six-week journeys: church and basketball.
- Actors table: admin, volunteer + qualification, human.
- Disruption drills CH-01..CH-08 with acceptance criteria.
- CH-04: block both worship leaders, attempt publication.
- Acceptance: publication **rejected**, prior roster stays live.

`SignUpFlow/docs/playbooks/church.md:14-24,73`

<!-- NOTES: Test tiers prove the machinery works; playbooks prove the product can be operated. `docs/playbooks/` ships two six-week operational scenarios. Church.md's actors table forces every actor into admin, volunteer plus qualification, or explicitly human — the Ministry approver is "Human organizational responsibility", not a new permission level. The flagship drill is CH-04: block both worship leaders for Sunday week 4 and attempt publication. The acceptance is that exactly that service reports missing leadership, publication is rejected, and the prior roster stays live. Read what that tests: not the happy path, but a failure mode. Acceptance criteria about rejection are what separate a demo from a product. Transition: those scenarios are data, so tests can run them. -->

---

## M5.3 — Fixtures parameterize real tests

- `docs/playbooks/church.json` declares domain, roles, headcounts.
- Seven distinct people per event.
- A pytest plugin discovers fixtures; `--playbook` selects.
- API tier: real JWT, isolated in-memory SQLite.
- Browser tier: real app at **360px and 1440px**.

`SignUpFlow/docs/playbooks/church.json` · `tests/playbooks/plugin.py` · `README.md:28-42`

<!-- NOTES: The scenarios are executable because they are data. `church.json` declares the domain, the workflow, the event, the roles headcount map, the secondary event, the critical role, and drill selectors. A pytest plugin discovers those files, parameterizes tests with stable IDs, and supports `--playbook` and `--playbook-dir`. The API tier runs them with real JWT identities against isolated in-memory SQLite; the browser tier starts the real application on a temporary database at 360 and 1440 pixels. Seven distinct qualified people per event is the fixture's promise. Transition: and who checks whether the solver kept that promise? -->

---

## M5.3 — An independent oracle, not self-report

- Oracle recomputes correctness from the published roster.
- Exact role counts, distinct qualified assignees.
- Non-overlap; interchangeable loads within one.
- Health = 0 on hard violation, else 100 − soft/10.
- The solver cannot grade its own homework.

`SignUpFlow/docs/playbooks/README.md:37-38` · `api/core/solver/heuristics.py:321-323`

<!-- NOTES: Every solve is checked by an independent oracle, and *independent* is the load-bearing word. The oracle recomputes correctness from the roster itself: exact role counts, distinct qualified assignees, no person in two slots of one event, no overlaps, and interchangeable people's baseline loads differing by at most one. It never asks the solver whether the solver did a good job — and that matters, because the solver's own metric is brutally simple: health is zero if any hard violation exists, otherwise one hundred minus soft score over ten. A self-reported score is not an oracle. Transition: now the manifest that binds all of this together. -->

---

## M5.3 — The manifest is honest by construction

- `docs/playbooks/coverage.json` — 35 rows, all `automated`.
- Four statuses: `automated`/`partial`/`manual`/`blocked`.
- `automated`/`partial` must cite an executable tier.
- `manual`/`blocked` must include the `manual` tier.
- A blocked row cannot masquerade as automated.

`SignUpFlow/tests/playbooks/coverage.py:19,43-46` · `SignUpFlow/docs/playbooks/README.md:84-87`

<!-- NOTES: `coverage.json` binds every scenario to an actor, precondition, operation, expected result, tiers, evidence paths, and a status. Four statuses exist, and two coupling rules make dishonesty structurally hard: automated or partial rows must include an executable tier, and manual or blocked rows must include the manual tier. So a blocked scenario *cannot* be dressed up as automated. In the current manifest all 35 bundled rows are automated, with four carrying a manual tier alongside — so the reserved statuses are the vocabulary for admitting what is not yet proven. Church.md's reading is exact: partial or blocked rows are remaining work, not passed scenarios. Transition: and the validator runs before collection. -->

---

## M5.3 — Validation happens before collection

- Plugin's `pytest_configure` loads and cross-checks the manifest.
- Any `ValueError` becomes `pytest.UsageError`.
- The run dies before a single test executes.
- Shared scenarios must be exactly BO-01..12.
- Remove a required scenario → collection fails.

`SignUpFlow/tests/playbooks/plugin.py:37-45` · `tests/playbooks/coverage.py:87-155`

<!-- NOTES: The manifest is validated before collection, which is the detail worth copying. The plugin's `pytest_configure` hook loads the manifest and cross-checks it; any ValueError becomes a pytest.UsageError, so the run dies before a single test executes. The validators are structural, not cosmetic: shared scenarios must be exactly BO-01 through BO-12, each domain must carry exactly CH-01 through CH-08 plus the domain drills, and each domain must declare exactly one admin actor and at least one human responsibility boundary. Removing a bundled domain, required scenario, administrator, boundary, or qualification fails collection. Scope cannot shrink silently. Transition: now your lab. -->

---

## Lab M5 — Isolate and accept

- **Build:** three tables, JWT, `org_id` on every row.
- **Step 1:** isolation tests + forbidden write leaves DB unchanged.
- **Step 2:** qualifications prove no admin rights (403).
- **Step 3:** route policy + drift test; red first.
- **Step 4:** fixture + manifest + validator; red first.
- **Pass gate:** all negative paths green; both induced failures recorded.

`03-content/m05-security-tests/lab.md` · `SignUpFlow/tests/playbooks/examples/food-bank.json`

<!-- NOTES: Lab M5 is pass/fail, about three hours, and has four steps. You build a minimal FastAPI app with three tables — organizations, people, events — and JWT auth. Step one proves isolation with real-JWT tests, including the assertion most teams forget: snapshot the target row, attempt the forbidden write, assert the denial, re-read, assert the row is identical. Step two stores qualifications in the roles array and proves a volunteer-with-usher cannot invite. Step three builds a route policy plus a drift test, and you must deliberately miswire a route and record the red run before you fix it. Step four authors a playbook fixture modeled on `tests/playbooks/examples/food-bank.json` plus a manifest and validator, and you must remove a required id and record that failure too. A drift test you have never seen fail is a hope, not a test. Transition: quick quiz check. -->

---

## Quiz M5 — six MC, two written

- P0 severity · permissions vs qualifications
- Enumeration and the `404` decision
- What the drift test actually compares
- Tier pairings and the independent oracle
- Manifest honesty · the forgotten assertion

`03-content/m05-security-tests/quiz.md`

<!-- NOTES: Eight questions, six multiple choice and two short answer. The multiple-choice distractors are the misconceptions we taught against: that 403 is safer than 404, that qualifications imply trust, that SQLAlchemy adds tenant filters automatically, that all seven tiers run in one process. Question eight is the one to draft before you submit: write the assertion sequence proving volunteer A cannot edit volunteer B's availability and B's record is unchanged. Name each assertion in order, the status code, and the one assertion most teams forget. Hint: it involves a forbidden write and an unchanged row. Transition: the recap. -->

---

## Recap

- **M5.1** — P0 rule + three enforcers + 404 anti-enumeration.
- **M5.2** — one permission role; qualifications never confer authority.
- **M5.2** — policy dict executable; test catches drift.
- **M5.3** — seven tiers in separate processes; dated evidence retires.
- **M5.3** — playbooks test rejection; the oracle is independent.
- **M5.3** — manifest statuses are coupled; validation precedes collection.

<!-- NOTES: Six lines, three segments, one through-line. M5.1: the rule is in the baseline every agent reads, three mechanisms enforce it, and guessed ids return 404 so enumeration dies. M5.2: exactly one permission role, qualifications share the array but never confer authority, and the authorization matrix is a dict a test compares to the live app. M5.3: seven tiers each prove something different, playbook acceptance criteria are about rejection, the oracle recomputes from the roster, and the manifest is validated before collection. The through-line: agents generate queries at machine speed, so the guard has to be mechanical. Transition: the discussion prompt is where you apply it to your own product. -->

---

## Discussion prompt

- Your product stores data for multiple customers.
- A teammate: "foreign keys are enough — no org filters."
- Reply with **three** SignUpFlow file pointers.
- Name the mechanism that fails without the filter.
- Name the status code for a guessed foreign id.
- Name the first test assertion you would write.

<!-- NOTES: Post to the community, about 150 words. A teammate argues that an ORM with foreign keys is enough and you do not need org filters on every query. Write the reply. Use at least three SignUpFlow file pointers — the P0 rule, the dependency that enforces membership, and the status contract are the obvious three. Name the mechanism that fails without the filter, the status code a guessed foreign id should return and why, and the one test assertion you would write first. The hint from the lesson: it involves a forbidden write and an unchanged row. That is the habit this module is trying to build — an argument that ends in a check. -->
