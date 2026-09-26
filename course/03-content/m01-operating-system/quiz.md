# Quiz M1 — The AI Product Operating System

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
- b) Trust its training data, since the repo is public
- c) Present 2-3 candidate paths and let the user pick one
- d) Grep the repo / read the canonical source, and not recall from memory

### Q4 (M1.2)

Which pairing of spec-kit artifact to job is correct?

- a) spec.md = the HOW with library choices; research.md = the WHAT users need
- b) tasks.md = prose guidance for agents; contracts/ = the deployment guide
- c) spec.md = the WHAT, technology-agnostic; research.md = numbered decisions with rejected alternatives; tasks.md = checkbox tasks citing exact file paths
- d) quickstart.md = the quality gate before planning; checklists/requirements.md = the timed deployment guide

### Q5 (M1.3)

A teammate says: "The AI assistant obviously makes me faster — I can feel it." What does METR's 2025 randomized study (evidence dataset row 1) let you say back?

- a) "In that study, experienced maintainers were measured 19% slower on their own repositories while believing they were 20% faster — so a felt speed-up is not evidence. It does not show AI slows everyone: it is one task-level study of 16 people, and the 2026 follow-up's intervals cross zero"
- b) "You're right: the study measured experienced developers 19% faster with AI"
- c) "The study proves AI assistants cut engineering budgets, so the feeling is right in dollars"
- d) "The study proves AI makes every developer slower, so stop using it"

### Q6 (M1.3)

Which line belongs in an honest validation record, and why?

- a) "All green — ship it."
- b) "`make test-all` green; the 21 skipped tests were left out of the record to keep it clean."
- c) "Full API mypy: 835 errors in 40 files; not a pass." — because records include known debt and failures
- d) "No local record needed — adding more CI is always better."

### Q7 (M1.2 — short answer)

For the story "As a volunteer, I can block dates so the solver skips me," write one Given/When/Then acceptance scenario and one tasks.md-format task line citing an exact file path.

### Q8 (M1.3 — short answer)

Your test run: 12 passed, then 1 failed on a timing flake; after a fix, 13 passed. Write the evidence entry in the prescribed format — commands, counts, date, environment, limitations, head SHA — without hiding the failure.

## Answer key

### Q1 — b — "Filter every query by org_id" is imperative and checkable; "be careful" is a vibe (`SignUpFlow/AGENTS.md`, "House style"). (objective: M1.1 — write verifiable rules)

### Q2 — b — The hierarchy's single tie-breaker is "follow the more specific and safer one"; AGENTS.md is the baseline, not an override of more specific rules (`SignUpFlow/AGENTS.md`). (objective: M1.1 — apply precedence)

### Q3 — d — AGENTS.md forbids inventing identifiers — grep the repo and read facts from the canonical source; the 2-3-options rule covers ambiguous requests, not fact recall (`SignUpFlow/AGENTS.md`, "Anti-hallucination"). (objective: M1.1 — apply anti-hallucination rules)

### Q4 — c — spec.md is the technology-agnostic WHAT, research.md holds numbered decisions with rejected alternatives, tasks.md holds checkbox tasks with exact paths; the other options swap the jobs (`SignUpFlow/docs/SPEC_KIT_SETUP.md`). (objective: M1.2 — state each artifact's job)

### Q5 — a — Row 1 is task-level evidence from an independent randomized trial: measured 19% slower (CI +2% to +39%) against a believed 20% faster, so the feeling is exactly what the record must not substitute for. Row 2 is why (d) overclaims: the 2026 follow-up's point estimates are −18% and −4% with both intervals crossing zero, which is inconclusive, not "slower". (c) jumps levels: a task-level result says nothing about released capacity or budget, the mixing error M6 names. (b) misreads the sign. That gap between felt and measured speed is the reason M1 exists: written rules, specs a stranger can execute, and evidence records instead of impressions (`course/03-content/m06-expertise-product/evidence-dataset.md`, rows 1–2). (objective: M1.3 — why evidence replaces a feeling)

### Q6 — c — Records include known debt and failures, and never fabricate; (b) hides the skips the real record counts ("1,464 passed, 21 skipped"); "more CI is always better" is the misconception the no-CI policy argues against — hosted checks don't record what you validated (`SignUpFlow/docs/playbooks/validation.md`). (objective: M1.3 — record honest evidence)

### Q7 — Model answer — Scenario: "Given Sarah has a blocked-date period covering 2026-04-23, When an admin runs the solver for that week, Then Sarah gets no assignment and the solution reports zero hard violations." Task: "- [ ] T031 [P] [US1] Implement POST /api/v1/availability/time-off in api/routers/availability.py: write the failing test in tests/api/test_availability.py first." (objective: M1.2 — turn a story into a checkable scenario and an executable task)

### Q8 — Model answer — "## Evidence — todo — 2026-09-14 / Commands: `python3 -m pytest tests/ -q` → 12 passed, 1 failed (timing flake); after fix → 13 passed / Environment: macOS 15, Python 3.11.9 / Revision: <head SHA> / Limitations: flake not root-caused; CLI tested by hand only." The failure stays in the record — "this initial failure is not omitted from the evidence" (`SignUpFlow/docs/playbooks/validation.md`). (objective: M1.3 — write an evidence record with failures included)