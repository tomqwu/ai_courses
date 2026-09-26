# Facilitation M3 — Cohort Kit (one 90-minute live session)

> Ties to Week 3 in `course/02-instructor/instructor-guide.md`: "M3 workshop: live red-team of a
> cloud alias; run `make e2e` live; coverage-floor failure demo." Formula is I do / We do / You do.

## Timing table

| Min | Activity | Mode | Artifacts |
|---|---|---|---|
| 0–2 | Opening hook: the cloud alias that looks local | I do | `ollama list` in a terminal |
| 2–14 | Open `ModelPrivacy.swift:15-24`; narrate decisions, not lines | I do | Swift file, deck slides 4–7 |
| 14–28 | Live red-team: write the mocked `remote_host` test, watch it fail, implement the guard | We do | `tests/test_privacy.py`, `privacy.py` |
| 28–40 | Breakout A: four defenses, one per pair | You do | Four tests, all green |
| 40–44 | Debrief A: "what did each test prove?" | We do | Test output |
| 44–52 | Coverage-floor failure demo: skip a module, watch CI go red, restore | I do | `make lab-m2` failure and success |
| 52–64 | `make e2e` live, then the skip path with `LAB_E2E` unset | I do | Terminal: 2 passed, then 2 skipped |
| 64–76 | Breakout B: competition table, five rows, source every cell | You do | `docs/competition.md` draft |
| 76–84 | One-liner workshop: each clause names its column | We do | Clause-to-column table |
| 84–90 | Close: evidence record, lab handoff, discussion prompt | I do | Lab M3 checklist |

## Opening hook (2 min)

Run `ollama list` on your machine and read out the model names. If any ends in `:cloud`, you have
your hook on screen: that model installs locally, lists locally, and answers through
`http://localhost:11434` — and its inference happens elsewhere. Ask the room: "Is this model
private?" Take three answers, then say the segment's line: a localhost URL proves nothing. Do not
resolve it yet; the next twelve minutes resolve it.

## Breakout instructions

**Breakout A (12 min).** Pairs. Assign one defense per pair so all four are covered: cloud-alias
rejection, fail-closed on missing metadata, non-loopback host rejection, redirect refusal. Roles:
one writes the mocked payload and the assertion; the other runs the test and reads the failure
message aloud. **Deliverable to post:** the test function and its output — one line per pair,
including the red run if they wrote it test-first.

> Prompt: "Write the smallest mocked transport that proves your defense. State in one sentence
> what the assertion would miss if you removed it."

**Breakout B (12 min).** Groups of three. Each group picks a product idea already in the room and
builds a five-row comparison table in `docs/competition.md`, six columns, every cell sourced or
marked `unverified`. Roles: a researcher who opens the source URL for each cell, a recorder, and a
skeptic who challenges any cell with no URL. **Deliverable to post:** the table plus one clause of
a positioning one-liner, annotated with the column that proves it.

> Prompt: "Fill every cell from a URL you visited, or write `unverified`. Memory-only pricing is a
> fail. Then name the column that makes your strongest clause true."

## Discussion prompts

1. **Which defense was hardest to test, and why?** Follow-up probe: "What does the difficulty tell
   you about where the guarantee actually lives?" A strong answer names the redirect defense — the
   failure is in the transport, not the logic, so it requires a fake at the HTTP layer — and
   concludes that untestable guarantees tend to be unenforced ones.
2. **Your daemon has only `:cloud` aliases and local mode rejects everything. Is the lab broken?**
   Follow-up: "What would 'fixing' it cost you?" A strong answer says it is fail-closed working,
   documents the daemon state, and still runs the contract test — it is a contract test, not a
   privacy test, so it runs in default mode against whatever the router picks — and never
   weakens the metadata check.
3. **The 1.3.0 review said no at 97.24% coverage. What would you have written as G01's fix?**
   Follow-up: "How would you prove the fix, given CI cannot reach a daemon?" A strong answer names
   explicit AI routing plus a per-request metadata check with a unit red-team test, and assigns
   real-model evidence to `make e2e`.
4. **Which clause of your one-liner would you delete first, and what breaks?** Follow-up: "Which
   table column would no longer support the line?" A strong answer traces every clause to a column
   and admits when a clause has none — which makes it copy, not positioning.

## Watch-fors

Aligned with `course/02-instructor/instructor-guide.md` §4.

| Stuck point | Symptom | 30-second intervention |
|---|---|---|
| `verify_local_model` fails everything | No local model pulled | Intended. The red-team test passes while live mode rejects — fail-closed working. Pull `qwen3:0.6b` to see the accept path. |
| Cloud-only daemon treated as a bug | "My lab is broken" | That is the M3 lab environment. Document it; the contract test still runs in default mode against the router's pick. |
| Fail-open slip | Check skips when `details` is absent | Ask: "What does your code return when the key is missing?" Then require an explicit `False`. |
| Redirect defense untested | Test only asserts an exception type | Require `FakeTransport(status=302)` and a `match="redirect"` assertion; note that no request may be forwarded. |
| Memory-only competitor prices | Cells with no URL | Randomly pick one cell, open its source live. If it does not match, mark the rest suspect. |
| Coverage floor "passes" anyway | Floor set on a target with no coverage data | Show the summary line must print and the exit code must change on a skipped module. |

## Close (5 min)

Restate the arc in three sentences: privacy is a mode that fails closed, testing is tier
assignment, and done means a downloaded artifact you verified. Then the handoff: Lab M3 is three
hours — red-team test first, contract test outside CI, coverage floor with both runs recorded,
`docs/competition.md` sourced. Assign the discussion prompt from `lab.md`: post your mocked
`/api/show` payload and the assertion that failed before the fix. Remind them the evidence record
must state what their agent did and what they verified.

## Post-session checklist

- Record: attendance, the breakout artifacts posted, the quiz item analysis, and the coverage-floor
  failure exit code shown live.
- Post to the community: the annotated clause-to-column table, the two valid daemon outcomes, and
  the top three stuck points from this session with their unblocks.
- Grade: Lab M2 evidence this week; Lab M3 evidence next week; review M1, M2, M5 deeply per the
  cohort promise.
- Log for course upkeep: any pointer that failed to open on screen during the session.
