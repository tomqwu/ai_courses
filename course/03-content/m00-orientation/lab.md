# Lab M0 — Environment Setup & First Ship-Win

> **Goal:** every tool the course needs is installed and proven with one real output — before Module 1, you have already run real software end to end.
> **Prerequisites:** none. **Time:** ~30 minutes including downloads (`make setup`, the Ollama installer, the model pull); the "Before Module 1" block below adds ~10 minutes.
> **Pass gate:** the full solver summary block (with its `Health score:` line and the `Solution saved to …` line) plus a non-empty `ollama list`.

## Steps

1. **Clone the three case studies** (this workspace may already have them — skip to step 2 if so):
   ```bash
   git clone https://github.com/tomqwu/ListenToMe.git
   git clone https://github.com/tomqwu/SignUpFlow.git
   git clone https://github.com/tomqwu/ai_qe.git
   ```
2. **Verify your Python**: `python3 --version` → 3.11 or newer (SignUpFlow's own floor; TinyCopilot itself also runs on 3.10).
3. **Install Ollama** from <https://ollama.com/download> (macOS, Linux, Windows). Then pull a genuinely local model:
   ```bash
   ollama pull qwen3:0.6b
   ollama list          # note which names end in :cloud (cloud-backed aliases) and which don't
   ollama run qwen3:0.6b "Reply with exactly: PONG"
   ```
4. **Run the SignUpFlow solver** (a real production scheduler, in under 5 commands):
   ```bash
   cd SignUpFlow && make setup          # Poetry env + migrations (see README if you hit issues)
   poetry run python -m api.cli.main init my-church
   poetry run python -m api.cli.main solve my-church
   ```
   Capture the whole block: people, events, the **health score** line, violations, fairness stdev, assignments, and the `Solution saved to …` line. The score is whatever the sample workspace produces at the revision you cloned (`SignUpFlow/api/cli/main.py:193`) — at the 2026-09-16 head it is `0.0/100` with two hard violations. Do not "fix" the number; record it.
5. **Post your first win** in the community: your solver block + your `ollama list` (each entry labeled local or `:cloud`) + one sentence on which archetype (1: on-device app, 2: SaaS, 3: expertise product) you want to build by week 8.

## Acceptance checklist

- [ ] All three repos cloned and present locally
- [ ] `python3 --version` shows 3.11+
- [ ] `ollama list` shows at least one model; you can tell which are local vs `:cloud` aliases
- [ ] Solver ran; the full summary block, including the `Health score:` and `Solution saved to …` lines, is captured
- [ ] Evidence log started (see below)
- [ ] First-win post is up

The pass gate is the solver block plus a non-empty `ollama list`. The post is a checklist item and the completion lever (`course/02-instructor/instructor-guide.md` §1), not an auto-fail; the only auto-fail is fabricated output.

## Before Module 1

- **Start your course evidence log** (you'll keep it all course): paste the solver block and `ollama list`, each with the date and one line on what remains unverified.
- **Stretch — run the TinyCopilot lab tests** (the Module 2 lab's reference implementation, and Module 2's own pass gate):
  ```bash
  cd ../course/03-content/m02-ondevice-app/tinycopilot
  python3 -m pytest tests -q    # or: make lab-m2
  ```
  Expected: `191 passed`, coverage `100%`. If a dependency is missing, log the exact package and error line — an honest partial is fine here; Lab M2 is where this suite is graded. Add the pytest summary line to your evidence log when you have it.

## Stretch goals

- Mac user? Open `ListenToMe/README.md` and follow `make run` to launch the real app (requires macOS 26 + Xcode).
- Run one AI × QE check: `cd ai_qe && cat _data/release.yml` — find the independently versioned fields (`version`, `slide_edition`, `fintech_edition`, `questionnaire_edition`, `research_edition`). Four editions move on their own schedules; that's "content as code," coming in Module 6.

## Discussion prompt

Introduce yourself with: your stack, the archetype you're most excited to build, and one thing you've shipped before (a repo link counts double).