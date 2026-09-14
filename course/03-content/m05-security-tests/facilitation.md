# Facilitation M5 — Multi-Tenant Security & the Acceptance Gate

> One 90-minute cohort session for Module 5. Students arrive with Lab M4 done (a spec folder that
> passed the requirements checklist) and leave with the four Lab M5 steps started and one induced
> failure recorded. Mode labels: **I do** (instructor demonstrates), **We do** (whole room), **You
> do** (breakout).

## Timing table (sums to 90)

| Min | Activity | Mode | Artifacts |
|---|---|---|---|
| 2 | Opening hook: the valid-token leak | I do | `api/dependencies.py` on screen |
| 10 | Walk the rule → mechanism → contract ladder | I do | `AGENTS.md:57-61`, `docs/API_AUTHORIZATION.md:21-24` |
| 12 | Breakout 1: hunt the unfiltered query | We do | Each group posts the leaky line + org |
| 8 | Debrief 1: which failure class is it? | We do | Whiteboard of the seven negative cases |
| 12 | Live miswire: drift test red → green | I do | `tests/unit/test_api_route_auth_policy.py` |
| 14 | Breakout 2: write your route policy + drift test | You do | `route_policy.py` + failing test output |
| 6 | Debrief 2: what the red run proved | We do | Two groups paste their red output |
| 10 | Manifest demo: delete a scenario, watch collection die | I do | `docs/playbooks/coverage.json`, `plugin.py:37-45` |
| 8 | Breakout 3: honesty audit of your own manifest | You do | One row with status ≠ `automated` |
| 3 | Debrief 3: blocked vs. deleted | We do | Community post drafts |
| 5 | Close: evidence, limitation, next step | I do | Evidence-log template |

## Opening hook (2 min)

"A league administrator calls `GET /people/{person_id}` with a valid token. The query is
`db.query(Person).filter(Person.id == person_id).first()` — no tenant predicate. It returns a church
volunteer's name, rota and contact details. Nobody hacked anything; one generated query forgot one
filter. `SignUpFlow/AGENTS.md:61` calls that a P0 bug. In the next ninety minutes you will find that
line in your own work, watch a guard fail on purpose, and leave with a manifest that tells the truth
about what you have not proven."

## Close (5 min)

"Three things to take away. First, the rule: every query filters by `org_id`, and the filter lives in
the query, not in Python after the fetch — `docs/API_AUTHORIZATION.md:59-76`. Second, the guard: your
route policy is a dict and your test compares it to the live app, so a miswired dependency fails
before a customer finds it — `tests/unit/test_api_route_auth_policy.py`. Third, the honesty:
`docs/playbooks/coverage.json` has four statuses, and `blocked` is better than deleted, because a
removed scenario fails collection (`tests/playbooks/plugin.py:37-45`) while a blocked row is visible
remaining work. Before you close your laptop: paste the red output for your induced failure into the
lab thread, and write one limitation you have not proven. Evidence with a limitation is credible;
evidence without one is a claim."

## Breakout instructions

Groups of **3–4**. Rotate three roles: **driver** (shares screen, types), **skeptic** (argues for the
attacker: "can I enumerate ids? can I write?"), **recorder** (owns the posted deliverable). Timeboxed;
the driver must be a different person in each breakout.

**Breakout 1 — hunt the unfiltered query (12 min).** Exact prompt: *"Run
`grep -rn "db.query(" app/ | grep -v org_id`. For each hit, paste the line, name the route that
reaches it, and write the status code a foreign id would return after the fix. If you have no hits,
invent one: write a plausible query that omits `org_id` and say which of the seven negative cases
catches it."* **Deliverable to post:** the leaky line plus its route and intended status code.

**Breakout 2 — write your route policy + drift test (14 min).** Exact prompt: *"List every mounted
route, assign each to `public` / `member` / `admin`, and write the set-equality assertion against
`app.routes` plus the dependency-tree check. Then deliberately miswire one `admin` route to
`get_current_user`, run it, and paste the red output."* **Deliverable to post:** the policy dict and
the raw red run.

**Breakout 3 — honesty audit (8 min).** Exact prompt: *"Pick one scenario you cannot currently
prove. Give it a status from `automated`/`partial`/`manual`/`blocked` and the tiers that justify it —
remember `manual`/`blocked` must include the `manual` tier. Write one sentence on why deleting the
row instead would be worse."* **Deliverable to post:** the manifest row plus the sentence.

## Discussion prompts

1. **"Foreign keys are enough — we don't need org filters."** *Follow-up probe:* "Which mechanism
   fails first if that is true?" *Strong answer:* none of them save you — a primary-key lookup
   returns the foreign row before any membership check can matter; the filter in the query is the
   control (`docs/API_AUTHORIZATION.md:59-76`), and a warning log is only observability
   (`:74-76`).
2. **"A guessed foreign id should return 403 so the client knows it is not allowed."**
   *Probe:* "What does that tell an attacker with a valid account?" *Strong answer:* it confirms
   existence; `404` keeps foreign and absent indistinguishable (`api/dependencies.py:61-66`), which
   is why the status contract is tested.
3. **"The solver reports health 100, so the roster is good."** *Probe:* "Who computed that score, and
   what does the oracle recompute?" *Strong answer:* the solver computed its own metric — 0 on any
   hard violation, else `max(0, 100 − soft/10)` (`api/core/solver/heuristics.py:321-323`); the
   independent oracle recomputes role counts, distinct qualified assignees, non-overlap and balanced
   loads from the roster (`docs/playbooks/README.md:37-38`).
4. **"We'll mark that scenario `blocked` and fix it next sprint."** *Probe:* "What stops the row from
   quietly disappearing?" *Strong answer:* the coupling rules at `tests/playbooks/coverage.py:43-46`
   force a `manual` tier on blocked rows so they cannot look automated, and required ids are pinned,
   so removal fails collection (`docs/playbooks/README.md:84-87`).

## Watch-fors

| Stuck point | 30-second intervention |
|---|---|
| Drift test won't fail when miswired | Check the test compares the **policy file to the live route table** (`app.routes`), not two static lists (`02-instructor/instructor-guide.md`, M5 row). |
| Mocked auth in the isolation tier | Ask them to show the real JWT fixture; mocked auth belongs in `tests/unit/`, not in the tenancy evidence. |
| "Denied" without the unchanged-row assert | Say the sentence: "step 4 of the change protocol is assert forbidden writes leave the database unchanged" (`docs/API_AUTHORIZATION.md:65`). |
| Everything marked `automated` | Ask which tier executes each row; a row with no executable tier fails the validator. |
| Deleting an inconvenient scenario | Demonstrate the pre-collection failure, then have them restore it and set `blocked` + `manual`. |

## Post-session checklist

Record as evidence: the session date and attendance; one pasted red run from each breakout (miswire,
removed scenario id) submitted to the lab thread; the list of groups whose route policy missed a
mounted route; and the two-or-three limitations students named. Post to the community: the timing
table outcomes, one anonymised leaky query with its fix, and the reminder that the dated
"1,464 passed, 21 skipped" in `docs/playbooks/validation.md` is historical reference — quote it with
its 2026-09-12 date or not at all.
