# Quiz 1 — The AI Product Operating System

> 8 questions · 6 multiple choice + 2 short answer · Answer key at the end with objective refs.

## Questions

### Q1 (M1.1)

Which rule is written in SignUpFlow's house style for agent instructions?

- a) "Be careful with multi-tenancy."
- b) "Filter every query by org_id."
- c) "Multi-tenancy is important, keep it in mind."
- d) "Developers should value tenant isolation."

### Q2 (M1.1)

An agent hits a conflict between a general rule in `docs/ai-agent-coding-strategy.md` (level 4) and a more specific, safer path-scoped rule under `.github/instructions/` (level 3). Per SignUpFlow's instruction hierarchy, it must:

- a) Follow `AGENTS.md` regardless, since it is the universal baseline
- b) Follow the more specific and safer one — the path-scoped rule
- c) Follow the most recently updated file
- d) Stop and ask the user, since any conflict blocks work

### Q3 (M1.1)

Before referencing a file path, function name, or schema field in its output, an agent working in SignUpFlow must:

- a) Recall it from memory and flag uncertainty in a comment
- b) Grep the repo / read the canonical source, and not recall from memory
- c) Present 2-3 candidate paths and let the user pick one
- d) Trust its training data, since the repo is public

### Q4 (M1.2)

Which pairing of spec-kit artifact to job is correct?

- a) spec.md = the HOW with library choices; research.md = the WHAT users need
- b) spec.md = the WHAT, technology-agnostic; research.md = numbered decisions with rejected alternatives; tasks.md = checkbox tasks citing exact file paths
- c) tasks.md = prose guidance for agents; contracts/ = the deployment guide
- d) quickstart.md = the quality gate before planning; checklists/requirements.md = the timed deployment guide

### Q5 (M1.2)

Which task line follows the repo's tasks.md format?

- a) "Improve the SMS feature when convenient"
- b) "[US1] Make SMS work — the agent decides which files to touch"
- c) "T027 [US1] Implement POST /api/sms/send endpoint per contracts/sms-api.md in api/routers/sms.py"
- d) "Write SMS code, then write some tests afterwards"

### Q6 (M1.3)

Which line belongs in an honest validation record, and why?

- a) "All green — ship it."
- b) "Tests passed (trust me)."
- c) "Full API mypy: 835 errors in 40 files; not a pass." — because records include known debt and failures
- d) "No local record needed — adding more CI is always better."

### Q7 (M1.2 — short answer)

For the story "As a volunteer, I can block dates so the solver skips me," write one Given/When/Then acceptance scenario and one tasks.md-format task line citing an exact file path.

### Q8 (M1.3 — short answer)

Your test run: 12 passed, then 1 failed on a timing flake; after a fix, 13 passed. Write the evidence entry in the prescribed format — commands, counts, date, environment, limitations, head SHA — without hiding the failure.

## Answer key

### Q1 — b — "Filter every query by org_id" is imperative and checkable; "be careful" is a vibe (`SignUpFlow/AGENTS.md`, "House style"). (objective: M1.1 — write verifiable rules)

### Q2 — b — The hierarchy's single tie-breaker is "follow the more specific and safer one"; AGENTS.md is the baseline, not an override of more specific rules (`SignUpFlow/AGENTS.md`). (objective: M1.1 — apply precedence)

### Q3 — b — AGENTS.md forbids inventing identifiers — grep the repo and read facts from the canonical source; the 2-3-options rule covers ambiguous requests, not fact recall (`SignUpFlow/AGENTS.md`, "Anti-hallucination"). (objective: M1.1 — apply anti-hallucination rules)

### Q4 — b — spec.md is the technology-agnostic WHAT, research.md holds numbered decisions with rejected alternatives, tasks.md holds checkbox tasks with exact paths; the other options swap the jobs (`SignUpFlow/docs/SPEC_KIT_SETUP.md`). (objective: M1.2 — state each artifact's job)

### Q5 — c — The format is `[ID] [P?] [Story]` with exact file paths and tests first; option c is a real line (`SignUpFlow/specs/019-sms-notifications/tasks.md`). (objective: M1.2 — write executable task lines)

### Q6 — c — Records include known debt and failures, and never fabricate; "more CI is always better" is the misconception the no-CI policy argues against — hosted checks don't record what you validated (`SignUpFlow/docs/playbooks/validation.md`). (objective: M1.3 — record honest evidence)

### Q7 — Model answer — Scenario: "Given Sarah has a blocked-date period covering 2026-04-23, When an admin runs the solver for that week, Then Sarah gets no assignment and the solution reports zero hard violations." Task: "- [ ] T031 [P] [US1] Implement POST /api/v1/availability/time-off in api/routers/availability.py: write the failing test in tests/api/test_availability.py first." (objective: M1.2 — turn a story into a checkable scenario and an executable task)

### Q8 — Model answer — "## Evidence — todo — 2026-09-14 / Commands: `python3 -m pytest tests/ -q` → 12 passed, 1 failed (timing flake); after fix → 13 passed / Environment: macOS 15, Python 3.11.9 / Revision: <head SHA> / Limitations: flake not root-caused; CLI tested by hand only." The failure stays in the record — "this initial failure is not omitted from the evidence" (`SignUpFlow/docs/playbooks/validation.md`). (objective: M1.3 — write an evidence record with failures included)