# Lab M1 — Build Your Operating System, Then Run One Loop

> **Goal:** ship a starter repo with your own constitution, `AGENTS.md`, and spec templates — and prove it works by running one full spec → plan → TDD loop on a `todo` CLI feature.
> **Prerequisites:** Module 0 lab complete; Module 1 lesson read. **Time:** ~2 hours.

## Steps

1. **Create the repo.**
   ```bash
   mkdir my-studio && cd my-studio && git init
   python3 -m venv .venv && source .venv/bin/activate
   pip install pytest
   mkdir -p specs/001-todo-command docs tests
   touch docs/research-log.md docs/evidence-log.md
   ```
2. **Write `constitution.md` (≤80 lines).** Copy, then personalize the three bracketed parts:
   ```markdown
   # <Project> Constitution
   ## Principles
   1. Test-Driven Implementation: write the failing test first; the change is not
      done until `python3 -m pytest tests/ -q` passes.
   2. Simplicity & YAGNI: build exactly what's needed, nothing more.
   3. Safety & Reliability: [<your rule — e.g., never commit API keys; read them
      from environment variables>].
   ## Autonomy Configuration
   - YOLO Mode: DISABLED
   - Git Autonomy: ENABLED (commit when a task completes and tests pass)
   - When unsure whether an action is reversible, stop and ask.
   ```
   (Model: `SignUpFlow/.specify/memory/constitution.md` — 79 lines.)
3. **Write `AGENTS.md` (≤200 lines).** Every rule imperative and verifiable; include a validation checklist:
   ```markdown
   # AGENTS.md
   ## House style
   - Use imperative voice. Each rule must be verifiable.
   - Keep this file under ~200 lines.
   ## Anti-hallucination
   - Do not invent file paths, function names, or commands. Grep the repo first.
   - When the request is ambiguous, present 2-3 differentiated options.
   ## Project rules
   - [<e.g., Run pytest before declaring any change done.>]
   ## Validation checklist (before declaring done)
   - [ ] `python3 -m pytest tests/ -q` passes.
   - [ ] No secrets in the diff: `git diff | grep -iE 'api[_-]?key|secret|token'`
         returns nothing meaningful.
   - [ ] Docs touched by the change are updated; stale docs are a failure.
   ```
4. **Write `specs/001-todo-command/spec.md`** — the WHAT, technology-agnostic, two independently testable stories:
   ```markdown
   # Spec: todo command
   ## US1 (P1): Add and list todos
   As a user, I can add a todo and list all todos, so I can track work.
   - Given an empty store, When I add "write spec", Then listing shows one item
     with id 1, title "write spec", done=false.
   ## US2 (P1): Mark done
   As a user, I can mark a todo done, so completed work stops nagging me.
   - Given todo 1 exists, When I mark 1 done, Then listing shows done=true.
   ```
5. **Write `specs/001-todo-command/plan.md`** with the gate:
   ```markdown
   # Plan: todo command
   ## Constitution Check — GATE: must pass before implementation. Re-check after.
   - [x] TDD respected (tests written first). [x] YAGNI (no storage file, no dates).
   ## Tasks
   ```
6. **Write `specs/001-todo-command/tasks.md`** — exact paths, tests first:
   ```markdown
   ## Format: [ID] [P?] [Story] — include exact file paths
   - [ ] T001 [P] [US1] Create tests/test_todo.py: failing tests for add + list
   - [ ] T002 [US1] Create todo.py: TodoStore.add(title) -> int, TodoStore.list()
   - [ ] T003 [P] [US2] Add failing test for done to tests/test_todo.py
   - [ ] T004 [US2] Extend todo.py: TodoStore.done(todo_id)
   - [ ] T005 Add CLI dispatch in todo.py: add/list/done via sys.argv
   ```
7. **Run the loop with TDD.** Execute T001: write the failing tests first —
   ```python
   # tests/test_todo.py
   from todo import TodoStore

   def test_add_then_list():
       s = TodoStore()
       assert s.add("write spec") == 1
       assert s.list() == [{"id": 1, "title": "write spec", "done": False}]

   def test_done_marks_item():
       s = TodoStore()
       i = s.add("ship")
       s.done(i)
       assert s.list()[0]["done"] is True
   ```
   Run `python3 -m pytest tests/ -q` — record the failure (red). Then execute T002/T004: implement `todo.py` (a list of dicts; `add` appends and returns the id; `done` sets the flag). Run pytest again — record the pass (green). Finish T005, then run your full validation checklist.
8. **Record evidence** in `docs/evidence-log.md`, in the prescribed format:
   ```markdown
   ## Evidence — my-studio — todo command — <YYYY-MM-DD>
   Commands (with results):
   - python3 -m pytest tests/ -q (before implementation) → 2 failed
   - python3 -m pytest tests/ -q (after implementation) → <N> passed
   Environment: <OS, Python version>
   Revision: <output of `git rev-parse HEAD`>
   Limitations / not verified:
   - In-memory store only; CLI arg handling tested by hand, not automated.
   ```
9. **Commit** with the body format from `SignUpFlow/AGENTS.md`: Summary / Changed files / Validation / Follow-ups.

## Acceptance checklist

- [ ] `constitution.md` exists, ≤80 lines, ≥3 principles, autonomy config present
- [ ] `AGENTS.md` exists, ≤200 lines, every rule imperative + verifiable, validation checklist included
- [ ] `specs/001-todo-command/spec.md` has 2 stories, each with ≥1 Given/When/Then
- [ ] `plan.md` contains a Constitution Check gate, explicitly passed
- [ ] `tasks.md` has ≥5 `[ID] [Story]` tasks, each citing an exact file path, tests first
- [ ] Red run recorded: pytest failed before implementation, output saved
- [ ] Green run: `python3 -m pytest tests/ -q` exits 0
- [ ] Evidence entry has commands, counts, date, environment, limitations, head SHA
- [ ] `docs/research-log.md` has ≥1 dated observation
- [ ] One commit body follows Summary / Changed files / Validation / Follow-ups

## Evidence to record

Keep in `docs/evidence-log.md`: the red pytest output, the green pytest output, `git rev-parse HEAD`, and your evidence entry in the Step 8 format. This file is your proof asset for every later module — the course's version of SignUpFlow's `docs/playbooks/validation.md`.

## Stretch goals

- Add a negative-path test: marking a missing id raises a defined error (`SignUpFlow/AGENTS.md` requires negative-path assertions for every feature).
- Graduate one real observation: add it dated to `docs/research-log.md`, test it on this change, then promote it into `AGENTS.md` — the full pipeline from `SignUpFlow/docs/ai-agent-coding-strategy.md`.
- Run a second mini-loop (`specs/002-todo-remove/`) without rereading this lab.

## Discussion prompt

Post your before → after rule rewrite (one vague rule you made verifiable) and a link to your repo. Then review one classmate's `AGENTS.md`: could you check every rule was followed without asking them anything? Name any word you couldn't verify.