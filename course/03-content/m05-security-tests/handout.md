# Handout M5 — Multi-Tenant Security & the Acceptance Gate

**Mental model in one sentence:** tenant isolation is a P0 rule enforced by mechanisms a test can
check, and acceptance is a tier pyramid plus a manifest whose statuses admit what is not proven.

## The rule → mechanism → check ladder

```text
RULE        every query filters by org_id          SignUpFlow/AGENTS.md:57,61
MECHANISM   verify_org_member · tenant-bound reload · admin gate
                                                   api/dependencies.py:46,78,138
CONTRACT    401 invalid · 403 foreign org · 404 guessed id
                                                   docs/API_AUTHORIZATION.md:21-24
CHECK       route policy vs. live routes; negative-path tests
                                                   tests/unit/test_api_route_auth_policy.py
EVIDENCE    command + counts + date + head SHA + limitations
                                                   docs/playbooks/validation.md
```

## Decision table

| Situation | Answer | Why |
|---|---|---|
| Foreign id requested | `404` | Looked up inside the actor's tenant; foreign and absent look identical |
| Actor names a foreign org | `403` | Valid credential, wrong tenant — a policy denial |
| Invalid bearer token | `401` | The credential itself failed |
| Missing bearer token | `403` | HTTPBearer's documented default, retained on purpose |
| Person leads a ministry | `volunteer` + qualification | Qualifications never confer authority |
| Route added, not classified | Test fails | Set equality against the live route table |
| Scenario not yet proven | Status `blocked` + `manual` tier | Deleting the row fails collection instead |

## Keep these commands and templates

```bash
make lab-m5      # baseline: 51 passed, 23 skipped — record first
make demo        # two LEAK lines before step 1; zero after
make step1 … step4        # red on the starter, then green
make step3       # miswire create_event → red; restore → green
make lab-m5      # delete MF-03 → Error 4; restore → green
make pass-gate   # 74 passed
```

```markdown
## Evidence — Lab M5 — <YYYY-MM-DD>
Commands (with results):
- <command> → <N passed, M skipped, K failed>
Induced failures recorded: <miswired route> · <removed scenario id>
Environment: <OS, Python version>   Revision: <git rev-parse HEAD>
Limitations / not verified:
- <at least one honest line>
```

## Pointers to open

- `SignUpFlow/AGENTS.md:57-61` — the P0 tenancy rule and "never read user state from the body".
- `SignUpFlow/api/dependencies.py:46-121` — the three enforcers, verbatim.
- `SignUpFlow/api/roles.py:38-53` — `normalize_roles` refusals.
- `SignUpFlow/api/route_auth_policy.py:8-171` — five classes, the executable matrix.
- `SignUpFlow/tests/unit/test_api_route_auth_policy.py` — missing, stale, miswired.
- `SignUpFlow/docs/API_AUTHORIZATION.md:59-76` — the six-step change protocol.
- `SignUpFlow/docs/TESTING.md:38-50` — seven tiers, separate processes.
- `SignUpFlow/docs/playbooks/coverage.json` + `tests/playbooks/coverage.py:19,43-46` — the manifest.
- `SignUpFlow/tests/playbooks/examples/food-bank.json` — the minimal fixture shape.

## Three gotchas

1. **Filtering in Python is not isolation.** `[e for e in all_rows if e.org_id == ...]` has already
   read the other tenant's rows into your process. The predicate belongs in the query.
2. **A drift test you have never seen fail is a hope.** Record the induced red before the green — for
   the miswire *and* the removed scenario id.
3. **A self-reported "all tests pass" is not evidence.** No command, counts, date, revision, and
   limitations means no evidence.

## You're done when…

- [ ] Every event query carries the tenant predicate; `make demo` shows zero leaks.
- [ ] Seven negative-path cases pass: 200 own rows, 403 foreign org, 404 guessed id, 404 PATCH,
      401 invalid token, 403 missing token, 401 mismatched tenant claim.
- [ ] The forbidden write is denied **and** the row is byte-identical after the attempt.
- [ ] `["volunteer","usher"]` receives `403` from the invite endpoint.
- [ ] Route policy classifies every mounted route; the drift test caught a deliberate miswire.
- [ ] Playbook fixture + manifest validate; removing a required id fails the validator.
- [ ] At least one manifest status is not `automated`, with a reason.
- [ ] Evidence entry has commands, counts, date, environment, head SHA, and a limitation.

**Remember:** the filter in the query is the control; a warning log is only observability.
