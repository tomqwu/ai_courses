# M0 Handout — Orientation (one page, print me)

**Mental model in one sentence:** three archetypes — on-device app, spec-driven SaaS, expertise
product — are all built with one loop, **Study → Spec → Build → Validate → Release → Prove**, and
"done" always means a file someone can open.

## Pick your archetype

| If you want to build… | Archetype | Study this repo | Its proof asset |
|---|---|---|---|
| A private, fast app that runs on the user's machine | 1 — on-device AI app | ListenToMe | 96% core-coverage badge (`ListenToMe/README.md`) |
| A multi-user web product with features agents can implement | 2 — spec-driven SaaS | SignUpFlow | "1,464 passed, 21 skipped" (`SignUpFlow/docs/playbooks/validation.md`) |
| A research-backed briefing, course, or report | 3 — expertise product | AI × QE | 14-finding self-audit (`ai_qe/research/reviews/site-audit-2026-09-06.md`) |

## The loop, with one real artifact per stage

```
STUDY    12-row competitor table     ListenToMe/docs/competition-analysis.md
SPEC     Given/When/Then stories     SignUpFlow/specs/014-security-hardening/spec.md
BUILD    checkbox tasks, tests first SignUpFlow/specs/019-sms-notifications/tasks.md
VALIDATE 7 test tiers, dated counts  SignUpFlow/docs/TESTING.md
RELEASE  signed + notarized DMGs     ListenToMe/AGENTS.md
PROVE    "do not promote 1.3.0"      ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md
```

## Commands worth keeping

```bash
git clone https://github.com/tomqwu/ListenToMe.git   # + SignUpFlow, ai_qe
python3 --version                                    # want 3.11–3.13
ollama pull qwen3:0.6b && ollama list                # :cloud suffix = not local
ollama run qwen3:0.6b "Reply with exactly: PONG"
cd SignUpFlow && make setup                          # Poetry env + migrations + seed
poetry run python -m api.cli.main init my-church
poetry run python -m api.cli.main solve my-church     # capture "Health score:"
cd ../course/03-content/m02-ondevice-app/tinycopilot && make lab-m2
```

Sample solver output (stable parts): `People: 5`, `Events: 2`, `Health score: 100.0/100`,
`Violations: 0 hard, 0 soft`, `Fairness: stdev=0.43`, `Solution saved to my-church/output/solution.json`.
`Solved in 0ms` varies by machine.

`make lab-m2` → **191 passed**, coverage **100%** (90% floor). `make lab-m3` → **49 passed**.
`make e2e` → **2 passed** with a live daemon; 2 contract tests skip without `LAB_E2E=1`.

## Files to open

- `course/03-content/m00-orientation/lesson.md` — the module script
- `course/03-content/m00-orientation/lab.md` — steps and acceptance checklist
- `course/03-content/m00-orientation/quiz.md` — 8 questions
- `course/03-content/m02-ondevice-app/tinycopilot/README.md` — the M2 lab reference
- `SignUpFlow/README.md` — solver "CLI Example"
- `ai_qe/README.md` — publication records

## Three gotchas

1. **A `:cloud` name is not a local model.** `ollama list` entries ending in `:cloud` are cloud-backed
   aliases; a localhost URL proves nothing about where text is processed. Both environments are valid
   for M0 — say which one you have.
2. **`pip install` on system Python can refuse to run** (PEP 668, "externally-managed-environment").
   Create a virtual environment first, then install `pytest pytest-cov httpx`.
3. **Python 3.10 or 3.14 stops `make setup`.** SignUpFlow's build gate accepts 3.11 through 3.13 and
   prints the band on failure.

## You're done when…

- [ ] `ls -d ListenToMe SignUpFlow ai_qe` prints all three
- [ ] `python3 --version` shows 3.11–3.13
- [ ] `ollama list` shows ≥1 model, and you can label it local or `:cloud`
- [ ] Solver ran; the `Health score:` line and the `Solution saved to …` line are pasted
- [ ] `make lab-m2` shows `191 passed` (or the exact missing dependency is named)
- [ ] Evidence-log entry written with the date
- [ ] First-win post up: solver output + `ollama list` + your archetype sentence
