# Handout M1 — The AI Product Operating System

**Mental model in one sentence:** governance files constrain the agent, spec-kit artifacts tell it what
to build, and a dated evidence record proves what was actually validated.

## The loop

```text
constitution.md  →  AGENTS.md  →  spec.md  →  plan.md (GATE)  →  tasks.md  →  red test  →  green test  →  evidence-log.md
   principles         baseline      WHAT         HOW + check       exact paths    fail         pass          record + limits
```

## Decision table — which file, which job

| You want to say… | Put it in | Never put it in |
|---|---|---|
| A principle that must never drift | `constitution.md` (≤80 lines) | `tasks.md` |
| A rule that applies to every agent | `AGENTS.md` (≤200 lines) | the spec |
| What users need, no technology | `spec.md` | `plan.md` |
| Which library, why, and what was rejected | `research.md` / `plan.md` | `spec.md` |
| The exact file to touch, test first | `tasks.md` | anything else |
| What you ran and what you did not verify | `docs/evidence-log.md` | the commit message alone |

## Keep these commands and templates

```bash
mkdir my-studio && cd my-studio && git init
python3 -m venv .venv && source .venv/bin/activate && pip install pytest
python3 -m pytest tests/ -q          # red, then green
git rev-parse HEAD                   # the revision your evidence pins
wc -l constitution.md AGENTS.md      # prove the caps: ≤80, ≤200
```

```markdown
## Evidence — <project> — <feature> — <YYYY-MM-DD>
Commands (with results):
- <command> → <N passed, M skipped, K failed>
Environment: <OS, Python version>
Revision: <git rev-parse HEAD>
Limitations / not verified:
- <at least one honest line>
```

Rule rewrite test: **"Be careful with X"** → **"Filter every query by org_id."** If a stranger cannot
check whether a rule was followed, rewrite it.

## Pointers to open

- `SignUpFlow/.specify/memory/constitution.md` — 79 lines, the single source of truth.
- `SignUpFlow/AGENTS.md` — 177 lines; house style, hierarchy, anti-hallucination, PR rules.
- `SignUpFlow/CLAUDE.md` — 143 lines; cross-reference plus Claude addenda.
- `SignUpFlow/docs/SPEC_KIT_SETUP.md` — the slash-command pipeline.
- `SignUpFlow/specs/019-sms-notifications/tasks.md` — a real, executable task line.
- `SignUpFlow/docs/playbooks/validation.md` — the evidence line, the failures, and the limits.
- `ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md` — "do not promote 1.3.0."

## Three gotchas

1. **A green run without a red run is not TDD.** Record the failing output before the passing one.
2. **"Not verified" is a required field.** If your evidence entry has no limitations, it is incomplete — not clean.
3. **A spec that names a library is a plan.** Keep technology out of `spec.md`; the checklist gate rejects it.

## You're done when…

- [ ] `constitution.md` exists, ≤80 lines, ≥3 principles, autonomy config present.
- [ ] `AGENTS.md` exists, ≤200 lines, every rule imperative and verifiable.
- [ ] `specs/001-todo-command/` has `spec.md` (2 stories), `plan.md` (gate passed), `tasks.md` (≥5 tasks, exact paths, tests first).
- [ ] The red pytest output is saved, then the green run: `python3 -m pytest tests/ -q` exits 0.
- [ ] The evidence entry has commands, counts, date, environment, limitations, and the head SHA.
- [ ] One commit body follows Summary / Changed files / Validation / Follow-ups.

**Remember:** coverage tells you what you tested; only an honest record tells you what you shipped.
