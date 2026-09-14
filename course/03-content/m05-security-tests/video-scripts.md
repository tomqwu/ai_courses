# Video Scripts M5 — Multi-Tenant Security & the Acceptance Gate

> One recording per segment. Pacing: ~130 words per minute. Timestamps are for a single unbroken take;
> cut points are marked in each beats table. Every pointer named on screen is also read aloud.

## M5.1 — Multi-tenancy as a P0 cultural rule

**Target runtime:** 11 min · **Word budget:** ~1,430 words at 130 wpm (the beats below are
abbreviated narration cues, not a full transcript).

**Cold open (≈15 s).** "A league administrator calls `GET /people/{id}` with a valid token. The
handler queries by primary key — no `org_id` — and returns a church's volunteer, home address and
all. Nobody hacked anything. One query forgot one filter. SignUpFlow calls that a P0 bug, and this
segment is the rule plus the three mechanisms that make it true."

| Timestamp | On screen | Narration |
|---|---|---|
| 0:15 | `SignUpFlow/AGENTS.md`, lines 57 and 61 | Read both lines. Explain the placement: this is the baseline that Codex CLI, Cursor, Aider, Jules, OpenHands, Sourcegraph Amp and Factory read before writing a query. "Filter every query by `org_id`" is a check; "be careful with multi-tenancy" is a vibe. |
| 2:00 | `api/dependencies.py:46-58` | `verify_org_member` compares `person.org_id != org_id` and raises 403 "Access denied: not a member of this organization". Routes that take an explicit org or person call it before any query. |
| 3:30 | `api/dependencies.py:78-121` | The tenant-bound reload. The JWT's `sub` and `org_id` claims are both required; the person is reloaded by id **and** tenant **and** active status. A deleted or deactivated person invalidates the credential. The token points at a row; it does not replace it. |
| 5:00 | `AGENTS.md:58` | "Never read user state from the request body." The body is attacker-controlled. The moment a route trusts `org_id` from JSON, no downstream filter saves you. |
| 6:00 | `docs/API_AUTHORIZATION.md:21-24` | The four-row status contract. 401 invalid token; 403 missing token (HTTPBearer's default, documented rather than "fixed"); 403 explicit foreign org; 404 guessed id. |
| 7:30 | `api/dependencies.py:61-66` | Why 404. `get_person_in_actor_org` filters by id **and** the actor's org, so foreign and absent look identical. A uniform 403 confirms existence and lets an account enumerate your id space. |
| 9:00 | `AGENTS.md:59`; `docs/playbooks/coverage.json` BO-02 | Bootstrap: signup atomically creates org plus first admin; no public empty-org endpoint; later accounts need single-use invitations. Growth is invitation-only by construction. |

**Demo cue.** Terminal and editor side by side. Open `api/dependencies.py`, scroll to line 61, and
highlight the two predicates in the `filter(...)`. Then open `docs/API_AUTHORIZATION.md` and read
the last status row. What the viewer should notice: the status code is a *design decision*, tested,
not an accident of the framework.

**Action-step close.** Do lesson action steps 1–4: copy the P0 sentence verbatim into your evidence
log; open `api/dependencies.py` and write one sentence each on what `verify_org_member`,
`get_person_in_actor_org`, and the three-way `Person` filter refuse; copy the four-row table; then
write your own project's P0 rule and status table in imperative voice.

**Recording notes.**
- Enlarge the `filter(...)` call and the four-row table; those are the two things viewers must read.
- If over time, cut the signup bootstrap beat to one sentence — it returns in M5.2.
- Do not say the 403-on-missing-token is "wrong" or "a FastAPI bug". It is documented and tested.
- Do not quote any test count in this segment; the evidence number belongs to M5.3 and carries a date.

## M5.2 — RBAC done right: permissions ≠ qualifications

**Target runtime:** 10 min · **Word budget:** ~1,300 words at 130 wpm (abbreviated narration cues).

**Cold open (≈15 s).** "A worship coordinator leads services every Sunday and is the most important
volunteer in the building. The natural request is: make her an admin. Church.md refuses it in one
sentence — do not grant admin access merely because someone leads a ministry. This segment is why
that refusal is a data-model decision, and how the whole authorization surface becomes a test."

| Timestamp | On screen | Narration |
|---|---|---|
| 0:15 | `api/roles.py:8`; `CLAUDE.md` "RBAC" | One `roles` JSON array, two vocabularies. Permission roles: exactly `admin` or `volunteer`. Qualifications: `usher`, `coach`, `worship_leader`, `sound`, `musician`, `children_leader`. Different questions: what may this account do vs. what can this person do. |
| 1:45 | `docs/playbooks/church.md:14-24` | The actors table. The Worship coordinator is `volunteer + worship_leader`; the Ministry approver is "Human organizational responsibility". No department-scoped manager level exists. |
| 3:00 | `api/roles.py:38-53` | `normalize_roles`. Exact matches are permission roles; everything else is a qualification; `"ADMIN"` raises "is an ambiguous permission role"; two permission roles raise "Select exactly one account access role". Drift fails loudly. |
| 4:30 | `api/route_auth_policy.py:8-171` | The executable matrix. Five classes: public (7), public-token (6), public-callback (2), member (50), admin (78). `ROUTE_AUTH_POLICY` is the source of truth; `docs/API_AUTHORIZATION.md:3` says so. |
| 6:00 | `tests/unit/test_api_route_auth_policy.py` | 37 lines, three failure classes. Missing and stale are set equality against the live route table; miswiring walks each route's dependency tree — admin routes must depend on `get_current_admin_user`, member routes on `get_current_user`, public routes on neither. |
| 7:30 | `docs/API_AUTHORIZATION.md:59-76` | The six-step change protocol, read as a PR checklist. Emphasise step 2 (filter in the route query itself, not a helper) and step 4 (assert forbidden writes leave the database unchanged). |
| 8:45 | `docs/API_AUTHORIZATION.md:74-76` | Close the fence: "Do not use the tenancy warning listener as authorization." A warning log is observability; the filter is the control. |

**Demo cue.** Open `api/route_auth_policy.py` and show one `admin` name, then open the matching route
in the routers and point at `Depends(get_current_admin_user)`. Then state the miswire out loud: if
that `Depends` said `get_current_user`, the dict would still say admin and the test would still fail.
Viewers should notice that intent lives in one file and enforcement in another, and the test is the
bridge.

**Action-step close.** Lesson action steps 1–4: record the two `ValueError` messages and their
triggering inputs; confirm `signup` is public and `publish_solution` is admin and count the five
classes; label the three drift failure classes in your own words; paste the six-step protocol into
your contribution guide with your own paths.

**Recording notes.**
- Enlarge the dependency-tree assertion in the test; it is the least obvious of the three checks.
- If over time, compress the actors-table beat to one example and keep the `normalize_roles` beat.
- Do not claim the five class counts are permanent — they are read from `api/route_auth_policy.py`
  in this clone and will change as routes ship.
- Do not imply a drift test is proven; say plainly that it is only proven once seen failing.

## M5.3 — Acceptance: seven tiers, playbooks, and an honest manifest

**Target runtime:** 12 min · **Word budget:** ~1,560 words at 130 wpm (abbreviated narration cues).

**Cold open (≈15 s).** "A solver reports health 100. A pipeline says 1,464 tests passed. Both are
true, and neither proves the product can be operated — because a blocked worship leader was never
tested for, and the count is dated 2026-09-12 and formally retired the next day. This segment builds
acceptance that admits what it has not proven."

| Timestamp | On screen | Narration |
|---|---|---|
| 0:15 | `docs/TESTING.md:38-46` | Seven tiers and what each proves: unit (mocked auth), API/security (real JWT, isolated SQLite), CLI (YAML→JSON subprocess), integration (real DB), web (cookies/HTMX), contract (OpenAPI snapshots), browser (Playwright on a disposable app). |
| 1:45 | `docs/TESTING.md:49-50` | Separate processes, and why: API and browser event-loop fixtures differ. `make test-all` keeps them apart and stops on failure. One process for one number is how suites lie. |
| 3:00 | `docs/playbooks/validation.md:1,88,3` | The dated evidence: "Acceptance evidence - 2026-09-12"; "1,464 passed, 21 skipped"; the unit tier "399 passed, 21 skipped". Then the banner: reclassified 2026-09-13 as historical reference, not current status. Quote it with its date or not at all. |
| 4:30 | `docs/playbooks/church.md:73` | CH-04, the flagship drill: block both worship leaders for Sunday week 4 and attempt publication. Acceptance: exactly that service reports missing leadership, publication is rejected, and the prior roster stays live. Failure-mode acceptance is what separates a product from a demo. |
| 6:00 | `docs/playbooks/church.json`; `tests/playbooks/plugin.py` | Fixtures as data: domain, event, roles headcounts (seven distinct people per event), secondary event, critical role, drill selectors. The plugin discovers them, parameterizes with stable ids, supports `--playbook`. |
| 7:30 | `docs/playbooks/README.md:37-38` | The independent oracle: exact role counts, distinct qualified assignees, non-overlap, balanced loads, at 360 and 1440 pixels. `api/core/solver/heuristics.py:321-323`: health is 0 on any hard violation, else 100 − soft/10. The solver cannot grade its own homework. |
| 9:00 | `docs/playbooks/coverage.json`; `tests/playbooks/coverage.py:19,43-46` | The manifest: 35 rows, all `automated`, four carrying `manual` alongside. Four statuses; automated/partial need an executable tier; manual/blocked must include the manual tier, so `blocked` cannot masquerade as automated. |
| 10:30 | `tests/playbooks/plugin.py:37-45` | Validation before collection: `pytest_configure` cross-checks the manifest, and any `ValueError` becomes `pytest.UsageError`. Remove a required scenario and the run dies before a test executes. |

**Demo cue.** In the terminal, delete one BO id from a scratch copy of `coverage.json` and run
`poetry run pytest tests/api --collect-only -q`. The viewer should notice the failure arrives during
configuration — no test dots, no partial results — then revert. That is the manifest defending its
own scope.

**Action-step close.** Lesson action steps 1–4: post what a `blocked` row means and why it can never
look automated; record the pre-collection failure; copy `church.json`'s shape for your own fixture;
trace spec 020 → the comment in `api/core/solver/heuristics.py:36` → the CH-03/CH-04 oracle rows.

**Recording notes.**
- Enlarge the coverage.json schema and the two coupling rules; they are the takeaway artifact.
- If over time, cut the fixture-discovery beat and keep CH-04, the oracle, and the manifest.
- Always say the 1,464 is historical; never present it as current test status.
- Do not call the oracle "automated review" or imply it replaces human review.
