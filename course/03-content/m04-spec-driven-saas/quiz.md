# Quiz M4 — Spec-Driven SaaS

> 8 questions · 6 multiple choice + 2 short answer · Answer key at the end with objective refs.

## Questions

### Q1 (M4.1)

In the spec-kit pipeline, what does `plan.md` own that `spec.md` must not?

- a) User stories and acceptance scenarios
- b) HOW: languages, versions, storage, and performance targets
- c) The requirements checklist gate
- d) The repository's constitution

### Q2 (M4.2)

What is "the stranger test" for a spec folder?

- a) A security review by someone outside the team
- b) The spec must be written by someone who didn't build the product
- c) A fresh agent session with zero conversation memory can implement from the artifacts alone
- d) A peer must approve the spec before planning starts

### Q3 (M4.2)

Which acceptance scenario passes the gate's "testable and unambiguous" rule?

- a) "Then the system is secure against abuse"
- b) "Then users have a good experience"
- c) "Then authentication failures are handled appropriately"
- d) "Then the account is blocked for 15 minutes after 5 failures within 5 minutes"

### Q4 (M4.2)

What does the requirements checklist gate require before planning begins?

- a) A signed-off budget and a project manager
- b) No `[NEEDS CLARIFICATION]` markers remain; every FR has acceptance criteria; success criteria are measurable and technology-agnostic
- c) All tasks implemented and tests passing
- d) The constitution check filed in the PR

### Q5 (M4.2)

Why does every task in `tasks.md` cite an exact file path?

- a) To make the task list longer and more impressive
- b) Because the path is the task's assignee
- c) So the task tracker can close the task automatically when that file changes
- d) A fresh agent session doesn't know the project layout, and inventing paths is how hallucinated endpoints happen

### Q6 (M4.3)

Which PR Validation section follows the course's evidence discipline?

- a) "Tests pass ✅"
- b) "All good, ready to merge"
- c) "`make test-all`: 1,410 passed, 2 failed (see notes); browser suite skipped — no display server; head SHA abc123"
- d) "Validated by the build system"

### Q7 (M4.3, short answer)

A PR body's Validation section reads: "Reviewed the diff myself — all good. No reviewer assigned yet, merging so we don't block the sprint." Rewrite it so it satisfies both of the course's hard lines on review and approval, and state which line each original sentence broke.

### Q8 (M4.3, short answer)

Spec 014's self-graded checklist reported "5xP1" while the spec has six P1 stories, and its plan assigned migrations to a `migrations/` directory that doesn't exist. State the two countermeasure habits (from `AGENTS.md`) you should run on every generated artifact, and what each would have caught here.

---

## Answer key

- **Q1 — b.** WHAT/HOW separation: `spec.md` owns user-visible behavior technology-agnostically; `plan.md` owns HOW. The gate's first rule enforces it ("No implementation details", `specs/014-security-hardening/checklists/requirements.md`). (M4.1)
- **Q2 — c.** SignUpFlow runs implementation as a Ralph loop — an agent with no chat history that cannot ask questions. Every artifact rule exists because "a stranger can't ask follow-ups". (M4.2)
- **Q3 — d.** Numbers that reappear as an FR, a contract config row, and a test assertion. The other three fail the gate rule outright. (M4.2)
- **Q4 — b.** Requirement Completeness group: no NEEDS CLARIFICATION remains, testable and unambiguous, measurable and technology-agnostic success criteria, scenarios and edge cases defined. (M4.2)
- **Q5 — d.** Ties to the anti-hallucination rule: "Do not invent file paths… Grep the repo before referencing" (`AGENTS.md`). A named path makes the agent's first action a grep that confirms, not a guess; (c) invents tooling the repo does not have, and (a)/(b) are decoration. (M4.2)
- **Q6 — c.** Commands and result, skips and limitations recorded. "A Validation section that says 'tests pass' with no command is not evidence; one that records a failure still is." (M4.3)
- **Q7 —** Sentence 1 breaks "Do not claim independent review when the builder performed the review itself" (`SignUpFlow/docs/ai-pr-review.md:20-21`) — a self-review presented as review; sentence 2 breaks "Missing review is not approval" (`SignUpFlow/AGENTS.md:94`) — an absent reviewer is not a pass. Rewrite, e.g.: "Validation: `make test-all` → <counts>, head <SHA>. Self-review by author (not independent): findings F1–F2 resolved in <commits>. Independent local review requested from <name>; **not merged** until that review is recorded here." (M4.3)
- **Q8 —** Habits: (1) grep every path before referencing it — catches the nonexistent `migrations/versions/add_onboarding_tables.py` (migrations live in `alembic/versions/`); (2) recount counts against their source and never let a self-reported score substitute for opening the file — catches the "5xP1" vs six-P1 drift. Sources: `AGENTS.md` operating loop step 6 ("Search for stale commands, counts, check names…") and the anti-hallucination rule. (M4.3)