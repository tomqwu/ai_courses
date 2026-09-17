# Lab M0 — Solutions & Reference Answers

> Scope: every step in `course/03-content/m00-orientation/lab.md`. Runnable outputs are verbatim where
> the environment is standard; environment-specific parts are marked. Numbers follow
> `course/01-design/content-standards.md` §0.2.

## Step 1 — Clone the three case studies

**Reference answer.** Three sibling directories exist in the workspace root and each is a real git
checkout, not a downloaded zip: `ListenToMe/`, `SignUpFlow/`, `ai_qe/`. Name the folder you cloned
into.

```bash
git clone https://github.com/tomqwu/ListenToMe.git
git clone https://github.com/tomqwu/SignUpFlow.git
git clone https://github.com/tomqwu/ai_qe.git
ls -d ListenToMe SignUpFlow ai_qe   # all three print
```

**Common wrong answers.**
- *Cloned one repo and read the other two on GitHub.* Fails: the lab's later steps and every module
  pointer assume local files. Signals the student is treating pointers as decoration.
- *Cloned into nested folders and lost track of paths.* Fails later; `cd ../course/...` in the
  "Before Module 1" block breaks.
- *Downloaded ZIPs.* `make setup` and `pytest` still work, but `git log` evidence and tagged releases
  do not. Signals a shortcut that will cost time in M1.

**Grading note.** Real pass: the student pastes `ls` output showing all three directories. A
plausible fake is a list of GitHub URLs with no local listing.

## Step 2 — Verify Python

**Reference answer.** `python3 --version` prints 3.11 or newer. SignUpFlow's build gate is stricter
than "3.11+": its `check-python` target accepts 3.11 through 3.13 only, and prints the exact band on
failure (`SignUpFlow/Makefile`). TinyCopilot itself also runs on 3.10
(`course/03-content/m02-ondevice-app/tinycopilot/README.md`).

```bash
python3 --version          # e.g. Python 3.12.4
python3 -c "import sys; print(sys.version_info >= (3,11))"   # True
```

**Common wrong answers.**
- *Python 3.9 or 3.10 reported as "close enough".* SignUpFlow will refuse at `make setup`.
- *`python --version` shows 3.14 but `python3` shows 3.12.* Two interpreters; `poetry` picks the one
  on its PATH, so state which one Poetry resolved. Signals an environment the student cannot yet
  explain.
- *Pasted a version without running the command.* Checked by re-running it.

**Grading note.** A real pass includes the command and its output on the same line of the evidence
log, dated.

## Step 3 — Ollama and a local model

**Reference answer.** Ollama installed, one model pulled, one completion returned, and — the
discriminating part of this step — the student states which listed names are local and which carry
the `:cloud` suffix.

```bash
ollama pull qwen3:0.6b
ollama list                 # qwen3:0.6b present, no :cloud suffix
ollama run qwen3:0.6b "Reply with exactly: PONG"
# PONG
```

**Common failures and fixes.**

| Symptom | Cause | Fix |
|---|---|---|
| `command not found: ollama` | Daemon not installed or not on PATH | Install from <https://ollama.com/download>, restart the shell |
| `Error: model 'qwen3:0.6b' not found` | `pull` skipped or still running | `ollama pull qwen3:0.6b`, then re-run `list` |
| `ollama list` shows only `name:cloud` entries | Cloud-backed aliases; no weights on disk | Valid — pull `qwen3:0.6b` or use cloud mode in M2 (`course/02-instructor/instructor-guide.md`) |
| Daemon not reachable on `localhost:11434` | Service stopped | Start Ollama, confirm with `ollama list` |

**Common wrong answers.**
- *Calls the `:cloud` aliases "local models".* The whole point of the third lab row. A localhost URL
  proves nothing about where the text is processed.
- *Claims a completion without showing it.* The single-line prompt makes output short enough to
  paste; no reason to summarize.

**Grading note.** Accept either environment. Fail only the student who cannot say which kind they
have. The `:cloud`-only case is explicitly allowed by content-standards §0.5 ("two outcomes are
valid").

## Step 4 — Run the SignUpFlow solver

**Reference answer.** `make setup` completes, then `init` creates the workspace and `solve` prints the
summary. The captured artifact is the whole block around the health-score line.

```bash
cd SignUpFlow && make setup
poetry run python -m api.cli.main init my-church
poetry run python -m api.cli.main solve my-church
```

Expected output at the 2026-09-16 SignUpFlow head (the `Health score:` line is printed by
`SignUpFlow/api/cli/main.py:193`; the README's "CLI Examples" show the commands, not this block):

```
Created workspace at my-church/
  org.yaml      — organization config
  people.yaml   — volunteers and their roles
  events.yaml   — events to schedule

Workspace: my-church
People:    5
Events:    2
Range:     <today+7> → <today+14>
Mode:      relaxed

Solved in 0ms
Health score: 0.0/100
Assignments:  2
Violations:   2 hard, 0 soft
Fairness:     stdev=0.50

Hard violations:
  - Role sound_tech needs 1, got 0
  - Role sound_tech needs 1, got 0
Solution saved to my-church/output/solution.json
```

`Solved in …ms` and the `Range:` dates vary by machine and day. The score, counts, and stdev are
whatever the sample workspace produces at the revision cloned — an older sample printed `100.0/100`
with `0 hard, 0 soft`; the current one does not, and a student who pastes `100.0/100` today did not run it.

**Common failures and fixes.**

| Symptom | Cause | Fix |
|---|---|---|
| `❌ Poetry is not installed or not in PATH` | Poetry missing (`SignUpFlow/Makefile`, `check-poetry`) | `make install-poetry`, then `export PATH="$HOME/.local/bin:$PATH"` and reopen the shell |
| `❌ Python 3.11 through 3.13 required` | Interpreter outside the band | Install 3.11–3.13 and re-run `make setup` |
| `make setup` starts, then dies mid-install | Network or lockfile drift | Re-run `make setup`; read the last line it printed before exiting |
| `No such file or directory: my-church` | `init` skipped | Run `init my-church` before `solve` |

**Common wrong answers.**
- *Pastes only the `Health score:` line.* Incomplete — the summary block is the evidence.
- *Hand-edits the number, or "corrects" `0.0` to `100.0`.* The value is not graded, the run record
  is; an edited score is detectable (the violations and stdev lines will not match) and it is
  fabrication, the one automatic fail (`course/01-design/assessment-and-rubrics.md`).
- *Runs `solve` on the wrong workspace.* Output names the workspace; check it.

**Grading note.** Real pass: the full block, including the `Solution saved to …` line proving the run
wrote a file. Fake: a lone health-score line with no workspace summary.

## Step 5 — Post the first win

**Reference answer.** One community post containing (a) the solver summary block with its health-score
line, (b) `ollama list` with each entry labeled local or `:cloud`, (c) one sentence naming archetype 1,
2, or 3 for the student's week-8 goal.

**Common wrong answers.**
- *"Done!"* with no output attached.
- *Picks all three archetypes.* The post asks for one; the capstone also requires one.
- *Pastes a screenshot the text evidence should carry.* Acceptable, but the log still needs the text.

**Grading note.** The post is the completion lever (`course/02-instructor/instructor-guide.md` §1) and a
checklist item; a missing post is *Developing*, chased by the instructor — not an auto-fail. The pass
gate is the solver block plus a non-empty `ollama list`.

## Before Module 1 (stretch) — Run the TinyCopilot tests

**Reference answer.** From `course/03-content/m02-ondevice-app/tinycopilot`, install the three test
dependencies, then run the suite. This is Module 2's pass gate (`make lab-m2`), recorded now, graded
in Lab M2.

```bash
cd ../course/03-content/m02-ondevice-app/tinycopilot
python3 -m pip install pytest pytest-cov httpx
make lab-m2        # or: python3 -m pytest tests -q
```

Expected: **201 passed**, coverage **100%**, with a **90%** floor enforced by
`--cov-fail-under` (`tinycopilot/Makefile`). Related gates: `make lab-m3` → **49 passed**;
`make e2e` → **2 passed** against a live daemon; the 2 contract tests skip without `LAB_E2E=1`.
These match content-standards §0.2.

**Common failures and fixes.**

| Symptom | Cause | Fix |
|---|---|---|
| `error: externally-managed-environment` | PEP 668: system Python refuses global pip installs | `python3 -m venv .venv && source .venv/bin/activate`, then install pytest, pytest-cov, httpx inside it |
| `file or directory not found: tests` | Ran pytest from the repo root | `cd` into `tinycopilot/` first |
| `make lab-m2` fails the coverage floor | Deleted or unimported a module | Expected in Lab M2's exercise — but for M0 the suite must be green as shipped |
| Import errors on httpx | Dependency not installed | Install it inside the active interpreter |

**Common wrong answers.**
- *Reports "all tests pass" without a summary line.* The `N passed` line is the artifact.
- *Runs `make e2e` and reports failures.* Without `LAB_E2E=1` the contract tests skip; with it and no
  daemon they fail. M0 needs neither.
- *Names the missing dependency vaguely ("something with pytest").* The lab accepts a partial, but it
  must name the package.

**Grading note.** Accept a green suite or a named, exact missing dependency. Reject a claim of green
with no pytest summary — that is the one automatic fail, even on a stretch item.

## Stretch goals

- macOS: `make run` in `ListenToMe/` launches the real app (macOS 26 + Xcode).
- Any OS: `cat ai_qe/_data/release.yml` shows the separated version fields — `version`,
  `slide_edition`, `fintech_edition`, `questionnaire_edition`, `research_edition`.

## Self-check table

| Criterion | Self-verification |
|---|---|
| Three repos present | `ls -d ListenToMe SignUpFlow ai_qe` |
| Python in band | `python3 --version` prints 3.11–3.13 |
| Model present | `ollama list` shows ≥1 entry; suffix noted |
| Completion returned | `ollama run qwen3:0.6b "Reply with exactly: PONG"` |
| Solver ran | Full block: `Health score:` line + `Solution saved to …` pasted |
| Environment recorded | Evidence-log entry dated, outputs pasted verbatim |
| First win posted | Community post has all three parts |
| Before Module 1: TinyCopilot | `make lab-m2` → `201 passed`, coverage `100%` (or the exact missing package) |
