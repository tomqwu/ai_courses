# Lab M4 — The Scripted Stranger

> **What this is:** the self-paced version of Lab M4's pass gate. You paste the prompt below into a
> fresh session of any coding agent, point it at your spec folder, and it implements **story 1** alone.
> It may not ask you anything. Instead it logs every question it *would* have asked and every
> assumption it made, in a fixed format you can count. **Cohort learners** may use a human peer
> instead; the peer fills in the same report.

## Why a script, and why this shape

The gate in `lab.md` step 7 is "a stranger implements story 1 from the folder alone". A stranger
that can chat with you leaks your intent into the implementation and hides the holes. The script
removes the chat: the only inputs are the files in `specs/001-your-feature/`, and the only output is
the report. SignUpFlow's own agent rules are the model — "Do not invent file paths, function names,
route paths, commands, URLs, or identifiers. Grep the repo before referencing."
(`SignUpFlow/AGENTS.md:65`) and, when a request is ambiguous, present options "rather than
guessing" (`SignUpFlow/AGENTS.md:68`). The stranger prompt keeps both rules but turns the options
into logged questions, because the point is to *find* the ambiguity, not to resolve it in the
session.

The report is checkable because SignUpFlow specs are checkable. Story 1 of spec 014 carries one
"Independent Test" line (`SignUpFlow/specs/014-security-hardening/spec.md:26`) and four numbered
Given/When/Then scenarios (`SignUpFlow/specs/014-security-hardening/spec.md:30-33`). The first one
is the shape to copy — "**When** they fail authentication 5 times within 5 minutes, **Then**
further login attempts are blocked for 15 minutes" — because a test author needs no decisions to
write it. The other three are softer ("they see clear message explaining wait time"), and noticing
that gap before the stranger does is the point of step 1. Each scenario becomes one row in the
report's acceptance table. If your story 1 has no numbered scenarios, the stranger cannot fill the
table, and that is your first finding.

## Setup (2 minutes)

1. Commit your folder. The stranger runs on a **fresh clone or a fresh worktree** of your repo, so
   nothing uncommitted leaks in.
2. Open a **new** agent session with no prior context — no memory files, no earlier chat, no
   project instructions beyond what is committed in the repo.
3. Replace the two placeholders in the prompt (`<REPO ROOT>` and `<SPEC FOLDER>`), paste, and
   walk away. Do not answer any question the session asks; if it asks one, reply only with
   "Log it as a question and continue."
4. Save the report verbatim into your evidence log. Count the rows. Apply the pass rule.

## The prompt (paste as-is)

```text
You are implementing one user story from a written specification. You have NO access to the
author. Work only from the files under <SPEC FOLDER> in the repository at <REPO ROOT>.

Rules:
1. Read spec.md, plan.md, data-model.md, research.md, contracts/, and tasks.md first.
2. Implement ONLY the tasks tagged [US1] in tasks.md, in the order given, tests first.
   Stop at the first "Checkpoint" line after the US1 phase.
3. Do not ask me anything. Every time you need information the folder does not give you,
   write it down as a QUESTION and continue with the most conservative choice you can make.
   Every time you decide something the folder leaves open, write it down as an ASSUMPTION.
4. Do not invent file paths, function names, routes, commands, or identifiers. If a task
   names a path that does not exist in the repo, do not create a substitute — log a QUESTION.
5. Do not read git history, issues, or any file outside <REPO ROOT>.
6. Run the tests you wrote. Do not modify a test to make it pass.

When you stop (checkpoint reached, or blocked), print the report below and nothing after it.
Fill every section. Use "none" for an empty list. Number every Q and A item. Do not merge items.

=== STRANGER REPORT ===
Story: <story 1 title, copied from spec.md>
Tasks attempted: <task IDs, e.g. T004-T008>
Stopped because: <checkpoint reached | blocked at T0NN: reason>

## Built
<one line per file created or changed: path — what it does>

## Acceptance scenarios
| # | Scenario (Then-clause, copied) | Checked how | Result |
|---|---|---|---|
| 1 | <copy the Then-clause> | <test name or command> | pass / fail / not checkable: <why> |

## Questions (Q)
Q1. <what you needed to know> — needed for: <task ID> — where I looked: <file(s)>
Q2. ...

## Assumptions (A)
A1. <what you decided> — instead of: <the alternative> — needed for: <task ID>
A2. ...

## Counts
QUESTIONS: <n>
ASSUMPTIONS: <n>
SCENARIOS CHECKED: <passed>/<total>
=== END REPORT ===
```

## The pass rule (binary)

Take every Q and A row and classify it with **one** of two labels. Record the label next to the row
in your evidence log.

| Label | Definition | Examples |
|---|---|---|
| **spec-owed** | The folder should have answered it: behaviour, data shapes, error keys, limits, ordering, permissions, file placement, or which test proves a scenario. | "Is the window inclusive of the end minute?" · "Which error key for an overlapping window?" · "Task T007 names `app/api/routes/availability.py` but no `routes/` package exists." |
| **environment-owed** | Outside any spec folder's job: the toolchain, credentials, or machine. | "Which test runner is installed?" · "There is no database URL in the environment." |

**Pass = zero spec-owed rows.** One spec-owed row is a hole. Sharpen the artifact it names (the
"where I looked" field tells you which one), commit, and re-run the prompt in a **new** fresh
session. The pass is the report of the run that scores zero, kept together with the earlier runs —
the trail of what you fixed is the learning, and the rubric's "sharpening" row grades it.

Two rules keep the count honest:

- **You do not get to relabel.** If you argue a Q is environment-owed, the argument must name the
  section of `spec.md`, `plan.md`, `data-model.md`, a contract, or `tasks.md` whose job it is
  *not*. "The stranger should have guessed" is not an argument; guessing is what spec 014's
  Assumptions section exists to prevent (`SignUpFlow/specs/014-security-hardening/spec.md:350-356`).
- **A "not checkable" scenario row counts as a spec-owed Q** unless its reason is environment-owed.
  A scenario the stranger cannot turn into a test is a scenario written for a reader, not a test
  author — the failure the rubric's "Numeric, assertable Then-clauses" row already grades.

## What to keep in the evidence log

- The full report of every run, verbatim, with the run date and "fresh session" stated.
- Each Q/A row's label, and for each spec-owed row: the artifact sharpened and the line
  before/after.
- The final `Counts` block. `QUESTIONS: 0` and `ASSUMPTIONS: 0` are not required — a run can pass
  with environment-owed rows. **Spec-owed: 0** is the gate.

## Cohort option — a human peer

Hand the folder to a peer with the same rules: no questions to you, story 1 only, the same report
format. Peers tend to under-report assumptions because they fill gaps from experience; ask them to
list every decision they made without a sentence in the folder telling them to. The classification
and the pass rule are identical.
