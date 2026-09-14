# Solutions — Lab M1

> Grade the *properties* — under the cap, imperative, verifiable, gate present, red before green — not
> the prose. The two exemplars are real, submittable artifacts; they are not the only pass.

## Exemplar A — `constitution.md` (36 lines, cap 80)

```markdown
# My Studio Constitution
## Principles
1. Test-Driven Implementation: write the failing test first; a change is not done
   until `python3 -m pytest tests/ -q` passes.
2. Simplicity & YAGNI: build exactly what the task needs, nothing more. No storage
   file, no dates, no config until a task names it.
3. Safety & Reliability: never commit secrets or API keys; read them from
   environment variables. External delivery (email, SMS, payments) stays disabled
   by default until a task enables it.
4. Docs stay current: a stale doc is a Definition-of-Done failure.
## Autonomy Configuration
- YOLO Mode: DISABLED
- Git Autonomy: ENABLED (commit when a task completes and tests pass)
- When unsure whether an action is reversible, stop and ask.
## Current Validation Policy
- No CI checks. Run formatting, tests and review locally.
- Record commands, counts, environment, limitations and the pushed head SHA.
```

## Exemplar B — `AGENTS.md` (48 lines, cap 200)

```markdown
# AGENTS.md
Cross-agent baseline for my-studio. Consumed by any agent that reads AGENTS.md.
## House style
- Use imperative voice. Each rule must be verifiable.
- Keep this file under ~200 lines. Split by topic rather than nest.
## Anti-hallucination
- Do not invent file paths, function names, or commands. Grep the repo first.
- When the request is ambiguous, present 2-3 differentiated options.
- For facts (env var names, schema fields), read the canonical source. Do not recall.
## Safety
- Never commit secrets or API keys: `git diff --cached | grep -iE 'api[_-]?key|secret|token'`
  must return nothing meaningful.
- Never run `rm -rf`, `git push --force`, or `git reset --hard` without authorization.
- When unsure whether an action is reversible, stop and ask.
## TDD rules
- Write the failing test first, watch it fail, implement, watch it pass.
- Add a negative-path assertion for every feature (missing id, malformed input).
## Validation checklist (before declaring done)
- [ ] `python3 -m pytest tests/ -q` passes.
- [ ] No secrets in the diff (command above returns nothing meaningful).
- [ ] Docs touched by the change are updated; stale docs are a failure.
- [ ] Evidence entry written in `docs/evidence-log.md` with commands, counts,
      environment, head SHA, and limitations.
## Commit format
Summary / Changed files / Validation / Follow-ups.
```

**Why these pass.** Every line is an action or prohibition a stranger can check; both are under the
cap; neither copies SignUpFlow's content, only its structure
(`SignUpFlow/.specify/memory/constitution.md` is 79 lines; `SignUpFlow/AGENTS.md` is 177).

## Step solutions

### Step 1 — Create the repo
Reference: a git repo with `.venv` and `pytest`, plus `specs/001-todo-command/`, `docs/`, `tests/`, and
both log files. Expected: `python3 -m pytest --version` prints a 7.x or 8.x version — **varies**.
Wrong: (a) no `git init`, so Step 9's evidence has no SHA — signals writing, not shipping. (b) pytest
installed globally, not in `.venv`. Grading note: run `git rev-parse HEAD` yourself; if it errors, the
repo was never initialized.

### Steps 2–3 — `constitution.md` and `AGENTS.md`
Reference: Exemplars A and B. Expected: `wc -l` → `36 constitution.md`, `48 AGENTS.md` (any ≤80 / ≤200).
Wrong: (a) empty `[<your rule>]` brackets left in — the instructor guide calls this "my constitution
feels fake". (b) "be careful" rules that fail the stranger test. (c) `YOLO Mode: ENABLED`, which
cannot grade as a safety stance. (d) AGENTS.md over 200 lines with nested prose.
Grading note: pick one rule at random and ask "what command proves this was followed?" A real pass
answers with a command; a plausible fake answers with a feeling.

### Step 4 — `specs/001-todo-command/spec.md`
Reference: two independently testable stories, each with ≥1 Given/When/Then, no technology named. US1's
scenario must fix the shape `{"id": 1, "title": "write spec", "done": false}` so the test is derivable.
Wrong: (a) `sqlite3` or `argparse` named — implementation leakage the checklist gate forbids. (b) one
story covering add, list and done. (c) no concrete expected values. Grading note: if it cannot become
`tests/test_todo.py` without asking a question, it is not executable.

### Step 5 — `plan.md`
Reference: a `Constitution Check — GATE` section with an explicit verdict per principle, placed before
the tasks. Wrong: (a) gate present but unchecked. (b) principles listed with no verdict. (c) gate after
the tasks. Grading note: the gate must be *passed* — look for `[x]` or "passed" per principle.

### Step 6 — `tasks.md`
Reference: ≥5 tasks in `[ID] [P?] [Story]` format, exact paths, tests first.
```text
- [ ] T001 [P] [US1] Create tests/test_todo.py: failing tests for add + list
- [ ] T002 [US1] Create todo.py: TodoStore.add(title) -> int, TodoStore.list()
- [ ] T003 [P] [US2] Add failing test for done to tests/test_todo.py
- [ ] T004 [US2] Extend todo.py: TodoStore.done(todo_id)
- [ ] T005 Add CLI dispatch in todo.py: add/list/done via sys.argv
```
Wrong: (a) "make the todo work" with no path. (b) code tasks with no test task first. Grading note: a
task line is executable if a fresh agent session could start it with no conversation.

### Step 7 — Run the loop (red, then green)
Reference: `tests/test_todo.py` as in the lab; `todo.py` holds `TodoStore` over a list of dicts.
**Red run.** With no `todo.py`, pytest reports a collection error, not two failures:
```text
$ python3 -m pytest tests/ -q
ERROR tests/test_todo.py
ModuleNotFoundError: No module named 'todo'
1 error in 0.03s
```
Record that as what happened. For the literal "2 failed" line in the lab template, create an empty
`todo.py` stub first so both tests collect and fail. Either passes; a fabricated "2 failed" over a
`ModuleNotFoundError` does not.
**Green run.** After implementing `add`, `list`, and `done`:
```text
$ python3 -m pytest tests/ -q
2 passed in 0.01s
```
The count `2` is fixed by the two tests; the timing suffix varies. Wrong: (a) green with no red —
auto-fail. (b) tests edited after failing to match the implementation. Grading note: the red line must
precede the green line and name the same command.

### Step 8 — `docs/evidence-log.md`
Reference: all six fields, with at least one limitation.
```markdown
## Evidence — my-studio — todo command — <YYYY-MM-DD>
Commands (with results):
- python3 -m pytest tests/ -q (before implementation) → 1 error: ModuleNotFoundError
- python3 -m pytest tests/ -q (after implementation) → 2 passed
Environment: macOS 15, Python 3.11.9
Revision: <output of `git rev-parse HEAD`>
Limitations / not verified:
- In-memory store only; CLI arg handling tested by hand, not automated.
```
Wrong: (a) "all passed" with no command. (b) empty limitations. (c) a placeholder SHA. Grading note:
`git rev-parse HEAD` must return the SHA printed in the entry.

### Step 9 — Commit
Reference: imperative subject; body with `Summary`, `Changed files`, `Validation`, `Follow-ups`
(`SignUpFlow/AGENTS.md`, "PR and commit format"), repeating both pytest lines. Wrong: (a) a
Conventional Commit prefix the repo does not require. (b) no validation block. Grading note: run the
recorded command; it must agree with the commit body.

## Self-check table

| Criterion | Self-verification |
|---|---|
| Constitution ≤80 lines, ≥3 principles, autonomy config | `wc -l constitution.md`; read the headings |
| AGENTS.md ≤200 lines, rules verifiable | `wc -l AGENTS.md`; stranger-test 3 rules |
| spec.md has 2 stories, each with Given/When/Then | Search for `Given` — expect ≥2 |
| plan.md gate explicitly passed | Search `GATE`; confirm a verdict per principle |
| tasks.md ≥5 tasks with paths, tests first | T001 and T002 order |
| Red run recorded before green | Evidence entries in order, exact commands |
| Green run exits 0 | `python3 -m pytest tests/ -q; echo $?` → `2 passed`, exit `0` |
| Six evidence fields; research log; commit body | SHA matches `git rev-parse HEAD`; `git log -1` |
