# Welcome Packet — Student Onboarding

Everything a new student receives before Module 0. Send email 1 on enrolment, the checklist stands alone
so it survives being forwarded, and the help section says who answers what.

---

## Email 1 — Welcome (send on enrolment)

> **Subject:** You're in — here's how to start (about 30 minutes)
>
> Welcome to **AI Product Studio**.
>
> The course has one promise: by the end you will have shipped **one real AI product** through a loop you
> can repeat, and you will be able to prove it — not with a badge, but with evidence a skeptical engineer
> can open and check.
>
> **Three things to do this week:**
> 1. Run the **setup checklist** below (about 30 minutes, mostly downloads — the Ollama installer, the model pull and `make setup`).
> 2. Post your **first win** in the community — your environment output and one sentence on which
>    archetype you want to build.
> 3. Skim **Module 0** — it is short and it makes the rest of the course faster.
>
> You do not need a Mac for the core track. Every core lab is Python + Ollama, on macOS, Linux, or Windows.
> The Swift stretch track (Modules 2–3) is optional and needs a Mac — it maps the same labs onto a real
> shipping codebase.
>
> — Tom

---

## Email 2 — The setup checklist (send 24h later if setup is incomplete)

> **Subject:** 30 minutes to be ready for Module 0
>
> Pasted below so you can forward it to yourself. If any step fails, reply with the exact error — do not
> fight it alone.
>
> [the checklist from below]

---

## Setup checklist

- [ ] **Git** installed (`git --version`)
- [ ] **Python 3.11+** (`python3 --version`; the course standard matches SignUpFlow's floor — the
      TinyCopilot lab itself also runs on 3.10)
- [ ] **pytest + httpx** (`python3 -m pip install pytest pytest-cov httpx`)
- [ ] **Ollama** installed (<https://ollama.com/download>) and running (`ollama list`)
- [ ] At least one model pulled — `ollama pull qwen3:0.6b` for a genuinely local model
- [ ] The three case-study repos cloned:
      `git clone https://github.com/tomqwu/ListenToMe.git`,
      `…/SignUpFlow.git`, `…/ai_qe.git`
- [ ] Before Module 1 (Lab M0 stretch): the TinyCopilot lab suite runs green: `make lab-m2` → **191 passed, 100% coverage**
- [ ] An evidence log started (a plain Markdown file is fine — you will use it all course)

### Known setup snags (and the fix)

| Symptom | Cause | Fix |
|---|---|---|
| `error: externally-managed-environment` on `pip install` | PEP 668 (Debian/Ubuntu, Homebrew Python) | `python3 -m pip install --user --break-system-packages pytest pytest-cov httpx`, or use a venv |
| `make lab-m2` can't find pytest | pytest installed for a different interpreter | install into the same `python3` that `make` uses (`PYTHON=python3 make lab-m2`) |
| `ollama list` shows only `:cloud` names | your daemon has cloud aliases but no local weights | either `ollama pull qwen3:0.6b`, **or** run with only cloud aliases — Module 3's lab treats "local mode rejects everything" as a *correct* result, not a failure |
| Poetry errors in the SignUpFlow step | Poetry not installed or wrong Python | `make setup` output names the missing piece; a venv with Python 3.11+ is the reliable path |
| Solver step fails on migrations | stale local DB state | follow `SignUpFlow/README.md`; the CLI is `poetry run python -m api.cli.main init <name>` |

---

## Where to get help

| Question type | Where | Expected response |
|---|---|---|
| Setup broken, command fails | Community → **#setup** with the exact command + full error output | Same day (cohort) · 1–2 days (self-paced) |
| "Is my lab submission right?" | Community → **#lab-feedback**, using the lab's acceptance checklist as the template | Peer first, instructor weekly (cohort) |
| Concept unclear | The module's discussion prompt, or office hours (cohort tier) | Office hours + async |
| Grading or certificate question | Direct message to the instructor | Within 2 business days |

**The one rule that gets you a fast answer:** paste the command you ran and its complete output. "It
doesn't work" cannot be debugged, and the course's whole method is built on recording evidence — including
the failing kind. A red run in your evidence log is progress, not embarrassment; Module 1 teaches you to
record failures precisely because that is what makes them fixable.

---

## What "done" looks like

By the end you will have:

1. A **constitution and `AGENTS.md`** for your project (≤80 and ≤200 lines) — the rules your agents follow.
2. **Three archetype builds**, each with its own evidence: a hardened on-device core (TinyCopilot), a
   spec folder that survives a stranger test, and an expertise deck whose every claim carries a level.
3. A **pricing decision** derived from a sourced competitor table, and a **sales page** in the
   8-section anatomy.
4. **One shipped capstone** — v1 of your own product, through the full Spec-to-Ship Loop, scored on the
   5-dimension rubric, with a 5-minute demo.

Everything you submit is graded on evidence you can open: commands, outcomes, dates, limitations. That is
the same standard the three case-study repos hold themselves to — and by the end, yours.
