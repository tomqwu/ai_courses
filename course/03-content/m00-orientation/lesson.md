# Module 0 — Orientation: Three Products, One Method
> Part of AI Product Studio (APS-3) · ~30 minutes of lesson, plus ~30 minutes for the first win (mostly downloads) · No prerequisites

## Overview

Most AI courses teach you to call an API. This course teaches you to ship products, using three real, production open-source apps — built by one engineer, with AI agents doing the heavy lifting — as your case studies. You will clone all three, run one of them end to end in your first session, and then spend Modules 1–8 building three portfolio-grade products of your own: an on-device AI app, a spec-driven SaaS feature set, and an evidence-cited expertise artifact. At the end you price, package, and pitch one of them.

The three case studies, all public on GitHub:

| # | Archetype | Case study | What it is |
|---|---|---|---|
| 1 | Native on-device AI app | **ListenToMe** (`github.com/tomqwu/ListenToMe`) | A macOS meeting copilot: on-device transcription plus real-time AI help via local or cloud models you choose (`ListenToMe/README.md`) |
| 2 | Spec-driven AI SaaS | **SignUpFlow** (`github.com/tomqwu/SignUpFlow`) | A multi-tenant volunteer-scheduling SaaS: FastAPI + a greedy solver that auto-generates fair rosters (`SignUpFlow/README.md`) |
| 3 | Expertise content product | **AI × QE** (`github.com/tomqwu/ai_qe`) | A research-backed briefing site: 4 narrated decks, PDF editions, and a consulting funnel (`ai_qe/README.md`) |

Why these three? They have different technical centers of gravity — edge AI and privacy engineering; server-side architecture and security; research and content ops — but they were built with the *same method*, the **Spec-to-Ship Loop**: **Study → Spec → Build → Validate → Release → Prove** (the full derivation is in `00-research/00-synthesis.md`). You learn the method once and watch it instantiated three times; that repetition is what makes it stick.

Two expectations before we start. First, **every factual claim in this course carries a file pointer** like (`SignUpFlow/AGENTS.md`) — if you can't open a file and verify a claim, the claim is wrong, and you should say so. Second, the **core labs are Python 3.11+ and Ollama**, both free, running on macOS, Linux, and Windows; the Swift stretch track (Modules 2–3) uses ListenToMe itself as the reference implementation and requires a Mac. No prior LLM experience is assumed.

**By the end of this module you can:**

- Describe the three AI product archetypes and name each case-study repo and its proof asset.
- Explain the six stages of the Spec-to-Ship Loop and point to one real artifact per stage.
- Run the SignUpFlow solver on a sample workspace and capture its health score.
- Pull and run a local LLM with Ollama on your own machine.
- Post a goal + environment note to the community — your first-win post.

## Segment M0.1 — Why three types, and why these (~8 min)

### Objective

Describe the three AI product archetypes, name each case-study repo, and state what "production-grade" means in this course: not a demo, but a shipped artifact with proof you can open.

### Lesson

The three archetypes cover essentially everything a solo technical builder can ship, and each case study comes with **proof assets** — verifiable evidence in the repo itself, not marketing claims.

**Type 1: The native on-device AI app — ListenToMe.** A real-time macOS app that captures your mic and the meeting's system audio, transcribes on-device, and streams AI responses through a model you pick — Ollama locally, or a cloud provider with your own key (`ListenToMe/README.md`). Proof assets: a **96% core-coverage badge** rendered on the README (`ListenToMe/README.md`); **notarized release DMGs** published on GitHub Releases ("Grab the notarized `.dmg` from Releases" — `ListenToMe/README.md`); and a **14-row competitor comparison table** with sourced, dated claims (`ListenToMe/docs/competition-analysis.md`). That table is also how the product was positioned: "the free, open-source, fully on-device meeting copilot" — a corner of the market the table shows no commercial rival fills (`ListenToMe/docs/competition-analysis.md`).

**Type 2: The spec-driven AI SaaS — SignUpFlow.** A multi-tenant volunteer-scheduling platform for churches and leagues: FastAPI + SQLAlchemy, JWT auth, a greedy heuristic solver, and a YAML-in/JSON-out CLI (`SignUpFlow/AGENTS.md`, "Repository purpose"; the HTMX web app it also ships is described at `SignUpFlow/README.md:288`). Proof assets: **dated test evidence** — "1,464 passed, 21 skipped" across the full local suite (`SignUpFlow/docs/playbooks/validation.md`); **17 spec-kit folders** under `SignUpFlow/specs/`, each a complete specification→plan→tasks package; and a **seven-tier test pyramid** run in separate processes by `make test-all` (`SignUpFlow/docs/TESTING.md`).

**Type 3: The expertise content product — AI × QE.** A research-backed briefing site about modernizing quality engineering with AI. Proof assets: **116 slides across 4 decks** — 21 + 33 + 26 + 36, defined in `ai_qe/_data/briefing_room.json` — with **10 current PDF editions** — the 4 full decks, 4 guided routes, the research companion and the questionnaire at the editions `ai_qe/_data/release.yml` names, counted in `ai_qe/assets/pdf/` as of 2026-09-10 (`00-research/03-ai-qe-deep-read.md`; see also `ai_qe/README.md`, "Publication records"); and a **published self-audit**: a 14-finding review of its own site, with per-finding evidence and acceptance criteria (`ai_qe/research/reviews/site-audit-2026-09-06.md`).

Notice what all nine proof assets have in common: **each is a file you can open, dated or machine-checkable, not a testimonial.** That is the standard this course holds your work to as well — every lab ends in an artifact, and every artifact ends in evidence.

Why these three *together*? They share one method. The course research synthesis distills it into ten transferable principles — "record evidence, not vibes"; "write specs agents can execute"; "monetize honesty" (`00-research/00-synthesis.md`) — and Modules 1–8 teach that method through the three archetypes in sequence.

### Action step

Skim all three READMEs — `ListenToMe/README.md`, `SignUpFlow/README.md`, `ai_qe/README.md` — and find one proof asset in each (a badge, a dated evidence line, a publication record). Then write a two-sentence "which archetype is mine" note: which of the three you most want to build by week 8, and one thing you've shipped before. Keep it; you'll post it in M0.3.

## Segment M0.2 — The method: the Spec-to-Ship Loop (~10 min)

### Objective

Name the six loop stages in order and point to one real artifact from the case-study repos for each stage.

### Lesson

Here is the loop you will run in every module of this course:

```
1. STUDY    → 2. SPEC    → 3. BUILD    → 4. VALIDATE  → 5. RELEASE  → 6. PROVE
(research,     (specs an    (agents +     (tests,        (notarize,     (evidence,
 competition    agent can    TDD, small    coverage       TestFlight,    provenance,
 analysis,      execute)     reviewable   floors,        editions)      honest claims)
 positioning)                edits)        playbooks)
```

Each stage has a real artifact behind it. Open these as you read:

1. **Study.** ListenToMe's 14-row competitor table with per-claim sources (`ListenToMe/docs/competition-analysis.md`); AI × QE's first principle: "**Baseline before solutioning.**" (`ai_qe/docs/principles.md`). Positioning is a research artifact, not a slogan.
2. **Spec.** SignUpFlow's spec.md files carry prioritized user stories (P1/P2/P3) with **Given/When/Then** acceptance scenarios (`SignUpFlow/specs/014-security-hardening/spec.md`); ListenToMe's design spec defines protocol-level interfaces *and* a YAGNI non-goals list — "No cloud backend, accounts, billing, or multi-user" (`ListenToMe/docs/superpowers/specs/2026-06-18-listentome-design.md`).
3. **Build.** SignUpFlow's tasks.md turns each spec into checkbox tasks with exact file paths, tests written first (`SignUpFlow/specs/019-sms-notifications/tasks.md`); ListenToMe's implementation plan is a 2,410-line TDD task list ending in a self-review that maps every spec bullet to a task (`ListenToMe/docs/superpowers/plans/2026-06-18-listentome-mvp.md`).
4. **Validate.** SignUpFlow's seven test tiers and dated counts (`SignUpFlow/docs/playbooks/validation.md`); ListenToMe's **95% coverage floor** enforced by script (`ListenToMe/README.md`).
5. **Release.** ListenToMe publishes signed + notarized DMGs targeting the exact source commit (`ListenToMe/AGENTS.md`); AI × QE ships immutable, editioned releases — "Public content changes require a new edition before deployment" (`ai_qe/README.md`).
6. **Prove.** ListenToMe published a gap review that said "**do not promote the existing 1.3.0 DMG**" despite 97.24% core coverage (`ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md`); AI × QE published its own 14-finding site audit (`ai_qe/research/reviews/site-audit-2026-09-06.md`); SignUpFlow's validation record includes its failures — a browser click race and a mypy debt line reading "not a pass" (`SignUpFlow/docs/playbooks/validation.md`).

Stage 6 is the rarest and it is the spine of this course: the honest record of what was verified, what wasn't, and what failed. Tests validate what you built; evidence discipline validates what you shipped.

### Action step

Copy the loop diagram above into your notes, then start your **loop journal** — a single file you'll keep all course. For every future action step, record one line per stage you touched. First entry: for M0.3 below, you'll be doing a miniature STUDY (read the README), BUILD (run the solver), and PROVE (post output).

## Segment M0.3 — Set up and get your first win (~12 min of lesson; ~30 min at the keyboard)

### Objective

Clone all three repos, run the SignUpFlow solver locally and capture its health score, and run your first local LLM completion with Ollama.

### Lesson

Do this now — the whole sequence is about 30 minutes, most of it downloads (`make setup`, the Ollama installer and the model pull). You need git and Python 3.11+ (SignUpFlow's own floor — `SignUpFlow/AGENTS.md`, "Code style").

**1. Clone the three case studies:**

```bash
git clone https://github.com/tomqwu/ListenToMe.git
git clone https://github.com/tomqwu/SignUpFlow.git
git clone https://github.com/tomqwu/ai_qe.git
```

**2. Run a real production solver in three commands** (from `SignUpFlow/README.md`, "Quick Start" and "CLI Example"):

```bash
cd SignUpFlow && make setup     # Poetry env + migrations + seed data
poetry run python -m api.cli.main init my-church
poetry run python -m api.cli.main solve my-church
```

`solve` prints the workspace summary and the solver's result — people, events, a **health score** line, hard/soft violations, and a fairness stdev — and saves the solution to `my-church/output/solution.json`. The line is emitted by `SignUpFlow/api/cli/main.py:193` (`Health score: {health_score:.1f}/100`); its *value* is whatever the sample workspace produces at the SignUpFlow revision you cloned, not a number the README promises — at the 2026-09-16 head, `init my-church` + `solve my-church` prints `Health score: 0.0/100` with `Violations: 2 hard, 0 soft` (both `sound_tech` slots unfilled), and an older sample printed `100.0/100`. **Capture that health score line with the lines around it**; it is your first artifact, and the number is not the point — the run record is.

**3. Install Ollama and pull a genuinely local model** (from <https://ollama.com/download>):

```bash
ollama pull qwen3:0.6b
ollama list                     # confirm the model is present
ollama run qwen3:0.6b "Reply with exactly: PONG"
```

That last command is your first local LLM completion: no API key, no cloud bill, no data leaving your machine. Module 2 builds your own multi-role copilot on exactly this foundation.

> **Windows note.** Ollama runs on Windows, macOS, and Linux, and every core lab in this course is Python + Ollama — so Windows and Linux users are fully equipped for the main track. The **Swift stretch track** (Modules 2–3, "same lab in Swift" appendices) requires a Mac with Xcode, since ListenToMe targets macOS (`ListenToMe/README.md`). SignUpFlow's `make` targets work anywhere with Python 3.11+ and Poetry.

Why the rush to a working solver in Module 0? Because the hardest part of any builder course is the gap between watching and running. Within about thirty minutes — most of it download time — you will have executed real production software and a real local model. That is the first win, and it is what beats the "Module 2 chasm" where most courses lose people.

### Action step

Post your first win to the community: (1) your solver output including the health score line, (2) your `ollama list` output, and (3) your two-sentence "which archetype is mine" note from M0.1. Then complete **Lab M0** (`m00-orientation/lab.md`) — its checklist turns this segment into your first pass/fail checkpoint; the pass gate is the solver block plus a non-empty `ollama list`. Its "Before Module 1" block (run the TinyCopilot suite, start your evidence log) is where Module 2 begins.

## Recap

- Three archetypes, three real repos: **ListenToMe** (on-device AI app; 96% core-coverage badge, notarized DMGs, 14-row competitor table), **SignUpFlow** (spec-driven SaaS; 1,464 passed / 21 skipped dated evidence, 17 spec folders, 7 test tiers), **AI × QE** (expertise product; 116 slides / 4 decks / 10 current PDF editions as of 2026-09-10, provenance files, a published 14-finding self-audit).
- One method behind all three: the **Spec-to-Ship Loop** — Study, Spec, Build, Validate, Release, Prove — with a real, openable artifact at every stage.
- Production-grade means proof you can open: a badge, a dated evidence line, a provenance file — not a testimonial.
- Your environment: Python 3.11+ and Ollama everywhere; a Mac only for the Swift stretch track.
- You have already run one case study end to end and one local LLM — keep both outputs in your evidence log, and run the TinyCopilot suite before Module 1.

## Discussion prompt

Post your first-win reply (solver health score + `ollama list` + your archetype note), then answer in one more sentence: **which proof asset from M0.1 surprised you most, and would it survive a skeptical customer opening the file?** Reply to one other student's post with the archetype you think fits *their* goal — disagreeing is welcome if you point at the reason.