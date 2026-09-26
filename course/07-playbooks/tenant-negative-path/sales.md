# Sales Page: Multi-Tenant Negative-Path Test Kit

> Single-playbook page in the eight-section anatomy of `course/04-sales/landing-page.md`: headline, who it is for, problem, outcomes, proof, testimonials, FAQ, pricing with one call to action.

## 1. Headline

**Prove, with tests, that one customer can never read, change or enumerate another customer's data.**

A rule, a status contract, a test matrix and copy-paste tests for multi-tenant SaaS APIs.

## 2. Who it is for, and who it is not for

**For you if you:**
- run one database for many customers, or are about to;
- let coding agents write queries and want a net that catches a forgotten tenant filter;
- write FastAPI or a similar framework and can read pytest (the patterns port to other stacks).

**Not for you if you:**
- give each customer a separate database and never share a process;
- want a penetration test or a compliance certificate;
- need browser, CSRF or infrastructure isolation (this kit stops at the API).

## 3. The problem

Most multi-tenant bugs are one missing `WHERE org_id = …`. The request carries a valid token, the endpoint returns `200`, and the happy-path suite stays green. A foreign ID that returns `403` instead of `404` tells an attacker the row exists. A test that accepts "401 or 403" lets your documentation and your runtime disagree for months. None of these show up until you test from the other tenant's side.

## 4. What you will be able to do

- Write the tenancy rule and a four-row status contract in the file every agent reads.
- Bind every credential to one tenant and test the missing, wrong and inactive cases.
- Fill a test matrix of actors against operations, with one exact status per cell.
- Prove a guessed ID reveals nothing: foreign and absent IDs return identical responses.
- Prove a denied write changed nothing, with a fresh-session snapshot.
- Fail the build when a new route ships unclassified or wired to the wrong gate.

## 5. Proof

- **A runnable starter with known numbers.** `mini-flow` ships one deliberate cross-tenant leak. On 2026-09-26, `make lab-m5` gave `51 passed, 23 skipped` at 100% coverage, and `make demo` showed a valid token from one tenant reading and overwriting another tenant's row. The kit's own template tests fail on that leak and pass once the tenant predicate is in the query. It lives in the course repository at `course/03-content/m05-security-tests/mini-flow/`.
- **A real repository that does this.** SignUpFlow walks one path through six actors with exact codes (`SignUpFlow/tests/api/test_scheduling_tenant_boundaries.py:197-219`), asserts unchanged state after denied writes (`SignUpFlow/tests/api/test_scheduling_tenant_boundaries.py:301-312`), and fails when a route is missing, stale or miswired (`SignUpFlow/tests/unit/test_api_route_auth_policy.py:20-38`).
- **An honest finding.** The kit shows where that same repository's documented missing-token code (`SignUpFlow/docs/API_AUTHORIZATION.md:21-22`) and its runtime disagree, and why a loose assertion hid it (`SignUpFlow/tests/api/test_multi_tenant.py:116-121`).

The kit comes from the AI Product Studio course by Tom Wu, who built SignUpFlow with coding agents (`course/04-sales/landing-page.md`).

## 6. Testimonials

None yet. No buyer has used this kit, and this page will not invent one. Real results will appear here in before, after and result form.

## 7. FAQ

**Is the starter included?** The starter lives in the AI Product Studio course repository. The kit names its path and the exact output each command should print. Whether it ships with the kit is the owner's decision.

**Do I need FastAPI?** The templates use FastAPI and pytest. The rule, the contract, the matrix and the unchanged-row pattern apply to any web stack.

**Does it cover row-level security in the database?** No. The Limits section says what it does not prove.

**Is this the whole course?** No. It is one extracted method from the AI Product Studio course.

## 8. Price

**Proposed: $49** (proposed; the owner sets the final price). The course prices a module at about $44 (`course/04-sales/pricing-and-platforms.md:10`). This kit covers two segments of one module and points at a runnable starter with verified numbers, so it sits at that rate.

[**Get the kit →**]
