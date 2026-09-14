# Lab M0 — Environment Setup & First Ship-Win

> **Goal:** every tool the course needs is installed and proven with one real output — before Module 1, you have already run real software end to end.
> **Prerequisites:** none. **Time:** 20–40 minutes (mostly downloads).

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
   Capture the output: people, events, **health score**, fairness stdev, assignments.
5. **Run the TinyCopilot lab tests** (the Module 2 lab's reference implementation):
   ```bash
   cd ../course/03-content/m02-ondevice-app/tinycopilot
   python3 -m pytest tests -q    # or: make lab-m2
   ```
   All green? You've just run the exact acceptance gate you'll re-implement in Module 2.
6. **Post your first win** in the community: your solver output + your `ollama list` + one sentence on which archetype (1: on-device app, 2: SaaS, 3: expertise product) you want to build by week 8.

## Acceptance checklist

- [ ] All three repos cloned and present locally
- [ ] `python3 --version` shows 3.11+
- [ ] `ollama list` shows at least one model; you can tell which are local vs `:cloud` aliases
- [ ] Solver ran; you captured a health score line
- [ ] TinyCopilot's test suite passed (or, if a dependency is missing, you noted exactly which)
- [ ] First-win post is up

## Evidence to record

Start your **course evidence log** (you'll keep it all course): paste the solver output, `ollama list`, and the pytest summary line, each with the date.

## Stretch goals

- Mac user? Open `ListenToMe/README.md` and follow `make run` to launch the real app (requires macOS 26 + Xcode).
- Run one AI × QE check: `cd ai_qe && cat _data/release.yml` — find the five separated edition fields (site vs slide vs questionnaire vs research). That's "content as code," coming in Module 6.

## Discussion prompt

Introduce yourself with: your stack, the archetype you're most excited to build, and one thing you've shipped before (a repo link counts double).