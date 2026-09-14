# Glossary M5 — Multi-Tenant Security & the Acceptance Gate

Alphabetical. Each term: definition, then where it lives.

- **Acceptance gate** — The point where the product must be proven operable, not merely functional: playbook scenarios, disruption drills, and a manifest that admits unproven rows. (`SignUpFlow/docs/playbooks/coverage.json`; `docs/playbooks/church.md`)
- **Authorization matrix (executable)** — A dict classifying every mounted route as public/ member/ admin, paired with a test that compares the dict to the live route table and to each route's dependency tree. (`SignUpFlow/api/route_auth_policy.py:8-171`; test in `tests/unit/test_api_route_auth_policy.py`)
- **Cross-tenant data leak** — One unfiltered query returning another organization's rows to a valid, authenticated user; SignUpFlow classifies it as a P0 bug. (`SignUpFlow/AGENTS.md:57,61`)
- **Coverage manifest** — A machine-readable file binding each scenario to actor, precondition, operation, expected result, tiers, evidence paths, and a status; pytest validates it before collection. (`SignUpFlow/docs/playbooks/coverage.json`; `tests/playbooks/plugin.py:37-45`)
- **Coverage status** — One of exactly four values — `automated`, `partial`, `manual`, `blocked` — coupled to tiers so a blocked row cannot masquerade as automated. (`SignUpFlow/tests/playbooks/coverage.py:19,43-46`)
- **Disruption drill** — A scenario that breaks the happy path on purpose and specifies what rejection must look like, such as CH-04's blocked worship leaders and rejected publication. (`SignUpFlow/docs/playbooks/church.md:73`)
- **Evidence record** — A dated, revision-pinned account of validation: commands with results, environment, head SHA, and an explicit list of what was not verified. (`SignUpFlow/docs/playbooks/validation.md`; template in `03-content/m01-operating-system/handout.md`)
- **Independent oracle** — A check that recomputes correctness from the produced artifact rather than asking the producer: exact role counts, distinct qualified assignees, non-overlap, balanced loads. (`SignUpFlow/docs/playbooks/README.md:37-38`)
- **Invitation-only growth** — Signup atomically creates an organization and its first admin and never joins an existing one; later accounts arrive through administrator-created, single-use invitations. (`SignUpFlow/AGENTS.md:59`; BO-02 in `docs/playbooks/coverage.json`)
- **Negative-path test** — A test that asserts the denial and its status code, not the success case: the seven cases in `03-content/m05-security-tests/solutions.md` step 1. (`SignUpFlow/docs/API_AUTHORIZATION.md:21-24`)
- **No-CI local validation** — SignUpFlow's deliberate policy that all review, tests, and artifact validation run locally, with evidence recorded against the pushed head SHA instead of a hosted check. (`SignUpFlow/docs/ai-pr-review.md`; `tests/unit/test_local_validation_policy.py`)
- **P0 bug** — The severity SignUpFlow assigns to a missing `org_id` filter: not a triage negotiation, a query that does not ship. (`SignUpFlow/AGENTS.md:61`)
- **Permission role** — What an account may do; exactly one of `admin` or `volunteer`, enforced by a frozenset and by a normalization rule that refuses two roles. (`SignUpFlow/api/roles.py:8,38-53`)
- **Qualification** — What a person can do (`usher`, `coach`, `worship_leader`, `sound`); stored in the same `roles` array as permission roles but never interpreted as authority. (`SignUpFlow/api/roles.py:12`; `docs/playbooks/church.md:26`)
- **Resource enumeration** — Mapping which resources exist by observing error codes; defeated by loading target rows through the actor's organization so foreign and absent ids both return `404`. (`SignUpFlow/docs/API_AUTHORIZATION.md:23`; `api/dependencies.py:61-66`)
- **Reviewed head SHA** — The revision a local review and its evidence are bound to; changing source invalidates stale evidence and forces a recheck. (`SignUpFlow/docs/ai-pr-review.md`, Local Review Checklist items 1 and 5)
- **Tenant-bound credential** — A JWT or session carrying both the person `sub` and the `org_id`, both required, and reloaded against an active membership before the request proceeds. (`SignUpFlow/api/dependencies.py:78-121`; `docs/API_AUTHORIZATION.md:28-33`)
- **Test tier** — One of seven purposes, each run in a separate process: unit, API/security, CLI, integration, web, contract, browser. (`SignUpFlow/docs/TESTING.md:38-46,49-50`)

## Terms people get wrong

- **Permission role vs. qualification** — A permission role decides authority; a qualification decides eligibility for a shift. They share one JSON array and nothing else.
- **`403` vs. `404` for a foreign id** — `403` confirms the resource exists; `404` is the anti-enumeration answer because the lookup happens inside the actor's tenant.
- **Health score vs. oracle** — The health score is the solver grading itself (0 on any hard violation, else `100 − soft/10`); the oracle recomputes correctness from the roster.
- **`blocked` vs. deleted** — `blocked` is visible remaining work with a mandatory `manual` tier; deleting the row fails collection, which is a silent coverage lie.
- **Local validation vs. verified local** — Running a command locally is an action; verified local means the command, counts, date, environment, and head SHA were recorded.

## Curated resources

1. `SignUpFlow/AGENTS.md:57-61` — the P0 rule in the baseline every agent reads; read the exact wording before paraphrasing it.
2. `SignUpFlow/docs/API_AUTHORIZATION.md` — the status contract, the executable matrix, and the six-step change protocol in one file.
3. `SignUpFlow/tests/unit/test_api_route_auth_policy.py` — 37 lines that catch missing, stale, and miswired routes; the shortest complete drift test in the course.
4. `SignUpFlow/tests/playbooks/coverage.py` — the four statuses and the two coupling rules that make the manifest honest by construction.
5. `SignUpFlow/docs/playbooks/church.md` — a real actors table, a weekly operating rhythm, and CH-01..CH-08 acceptance criteria.
6. `SignUpFlow/docs/TESTING.md` — the seven-tier table and the reason tiers run in separate processes.
7. `SignUpFlow/docs/playbooks/validation.md` — the evidence format, plus the demotion banner that shows a number retiring with its date.
8. `SignUpFlow/tests/playbooks/examples/food-bank.json` — the smallest fixture shape you can copy for your own lab fixture.
