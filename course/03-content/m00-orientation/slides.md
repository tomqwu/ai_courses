---
marp: true
theme: aps
paginate: true
title: M0 — Orientation: Three Products, One Method
---

## M0 — Orientation: Three Products, One Method

- **Promise:** run real production software before Module 1
- **Duration:** ~30 minutes
- **Prerequisites:** none
- **Outcome:** three repos cloned, one solver run, one local model

<!-- NOTES: Welcome. In the next thirty minutes you will not watch anyone else build anything — you will clone three real products, run one of them end to end, and pull a local model onto your own machine. That is deliberate. Most courses lose people at the first hard lab; here the first win happens in Module 0, in under fifteen minutes, with output you can paste into the community. Keep a terminal open beside this video. Timing: 1 minute. Transition: next we name what you will be able to do by the end. -->

---

## By the end you can…

- Describe the three AI product archetypes
- Name each case-study repo and its proof asset
- Explain the six Spec-to-Ship Loop stages
- Run the SignUpFlow solver and capture a health score
- Pull and run a local LLM with Ollama
- Post your first-win note to the community

<!-- NOTES: These six outcomes are the quiz blueprint and the lab checklist, so treat them as the contract for this module. Notice the verbs: describe, name, explain, run, pull, post. Every one is something I can check from an artifact you paste — none of them is "understand". That is the course standard, copied from the case-study repos themselves: if it cannot be observed, it does not count as done. Timing: 2 minutes. Transition: first, the three archetypes and why these particular three. -->

---

## M0.1 — Three archetypes, one method

<!-- _diagram: grid -->

- Type 1: native on-device AI app
- Type 2: spec-driven AI SaaS
- Type 3: expertise content product

- Different technical centers of gravity
- Same method behind all three
- You learn the method once, three times

<!-- NOTES: Almost everything a solo technical builder can ship falls into one of these three shapes. Type 1 lives on the user's device and sells privacy and speed. Type 2 lives on a server and sells reliability and multi-user trust. Type 3 sells verified knowledge — a research artifact, not software. The technical skills barely overlap. The method does, and that repetition is the whole pedagogical bet of this course. Timing: 3 minutes. Transition: meet Type 1, ListenToMe. -->

---

## Type 1 — ListenToMe (on-device app)

- macOS meeting copilot: on-device transcription, real-time AI help
- Model choice: local Ollama or cloud with your key
- Proof: 96% core-coverage badge — `ListenToMe/README.md`
- Proof: notarized release DMGs on GitHub Releases
- Proof: 12-row competitor table — `ListenToMe/docs/competition-analysis.md`

<!-- NOTES: ListenToMe is a real macOS app you can download and run. It captures your microphone and the meeting's system audio, transcribes locally, then streams AI answers through whichever model you pick. Open the README and scroll to the coverage badge — that is a number produced by a test run, not a marketing line. Then open the competition analysis: twelve rows, each claim sourced and dated. That file is positioning work done as research, and it is the reason the product has a defensible one-liner. Timing: 4 minutes. Transition: Type 2 is server-side, and its proof asset looks completely different. -->

---

## Type 2 — SignUpFlow (spec-driven SaaS)

- Multi-tenant volunteer scheduling: FastAPI + SQLAlchemy
- Greedy solver auto-generates fair rosters
- YAML workspace in, JSON solution out
- Proof: "1,464 passed, 21 skipped" — `SignUpFlow/docs/playbooks/validation.md`
- Proof: 17 spec folders under `SignUpFlow/specs/`
- Proof: 7 test tiers — `SignUpFlow/docs/TESTING.md`

<!-- NOTES: SignUpFlow schedules volunteers for churches, leagues, and non-profits. Every feature starts as a specification folder and ends as tested code — seventeen of those folders exist today. The proof asset here is a dated evidence line in a validation playbook, written by the engineer at the time of the run. Read the exact wording: "1,464 passed, 21 skipped." Skips are counted, not hidden. In Module 5 you will learn why that record, including its failures, is more valuable than a green badge. Timing: 4 minutes. Transition: the third archetype is not an app at all. -->

---

## Type 3 — AI × QE (expertise product)

- Research-backed briefing site on AI in quality engineering
- 116 narrated slides across 4 decks
- 10 current PDF editions
- Proof: per-claim provenance — `ai_qe/README.md`
- Proof: own 14-finding site audit — `ai_qe/research/reviews/site-audit-2026-09-06.md`

<!-- NOTES: AI × QE is content as a product. The 116-slide figure is 21 plus 33 plus 26 plus 36, defined in the briefing-room data file, and it ships as PDF editions. What makes it credible is not the volume — it is that every claim carries provenance, and the author published a fourteen-finding audit of his own site. He is more skeptical of his own claims than his audience is. That is the entire sales strategy for a Type 3 product. Timing: 4 minutes. Transition: so what do all these proof assets have in common? -->

---

## Production-grade means proof you can open

| Archetype | Proof asset | Pointer |
|---|---|---|
| On-device app | 96% core-coverage badge | `ListenToMe/README.md` |
| Spec-driven SaaS | "1,464 passed, 21 skipped" | `SignUpFlow/docs/playbooks/validation.md` |
| Expertise product | 14-finding self-audit | `ai_qe/research/reviews/site-audit-2026-09-06.md` |

- Every asset is a file, dated or machine-checkable
- None of them is a testimonial

```markdown
<!-- ListenToMe/README.md -->
![Coverage](https://img.shields.io/badge/Core_coverage-96%25-brightgreen)

<!-- SignUpFlow/docs/playbooks/validation.md:88 -->
1,464 passed, 21 skipped. The opt-in example runs above are additional evidence,

<!-- ai_qe/research/reviews/site-audit-2026-09-06.md -->
**AI × QE site review — 6 September 2026**

Reviewed edition: **1.2.1**, commit `fd1133…`
```

<!-- NOTES: Here is the definition this course runs on: production-grade means a shipped artifact with proof you can open and verify. A badge generated by a coverage run, a dated evidence line, a published audit with per-finding acceptance criteria. All three are files. A testimonial, a "finished" claim in a README, or a repository merely existing are not evidence. Your labs will be graded against this same bar, which is why every lab ends in an artifact and every artifact ends in evidence. Timing: 3 minutes. Transition: these three products share one repeatable loop. -->

---

## M0.2 — The Spec-to-Ship Loop

<!-- _diagram: loop -->

- Study: research, competition, positioning
- Spec: what an agent can execute
- Build: TDD, small reviewable edits
- Validate: tests, coverage floors, playbooks
- Release: notarize, edition, deploy
- Prove: evidence, provenance, honest claims

<!-- NOTES: Six stages, and you will run all six in every module of this course. Study produces a positioning artifact, not a slogan. Spec produces something a fresh agent session could execute without conversation memory. Build is tests first. Validate is a record, not a feeling. Release is signing, editioning, deploying. Prove is the honest account of what was verified and what was not. Copy this diagram into your notes — you will reuse it immediately. Timing: 5 minutes. Transition: each stage has a real artifact behind it. Open these files. -->

---

## Stages 1–3 — real artifacts

| Stage | Artifact | Pointer |
|---|---|---|
| Study | 12-row competitor table | `ListenToMe/docs/competition-analysis.md` |
| Study | "Baseline before solutioning." | `ai_qe/docs/principles.md` |
| Spec | Given/When/Then stories | `SignUpFlow/specs/014-security-hardening/spec.md` |
| Build | Checkbox tasks with file paths | `SignUpFlow/specs/019-sms-notifications/tasks.md` |

<!-- NOTES: Open each of these as we go. The competitor table is Study because positioning is research you can cite. The first principle in the AI × QE principles file is literally "Baseline before solutioning" — measure before you claim. The SignUpFlow spec uses prioritized stories with Given/When/Then acceptance scenarios, and note that spec 014 has no tasks file; the tasks format is best read from spec 019, which has one. Build turns a spec into checkbox tasks that cite exact file paths, tests first. Timing: 6 minutes. Transition: stages 4 through 6, where honesty starts to matter more than code. -->

---

## Stages 4–6 — real artifacts

| Stage | Artifact | Pointer |
|---|---|---|
| Validate | 7 test tiers, dated counts | `SignUpFlow/docs/TESTING.md` |
| Validate | 95% coverage floor by script | `ListenToMe/README.md` |
| Release | Signed, notarized DMGs | `ListenToMe/AGENTS.md` |
| Prove | "Do not promote the existing 1.3.0 DMG" | `ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md` |

<!-- NOTES: Validate is where most builders stop. ListenToMe enforces a ninety-five percent coverage floor with a script, and SignUpFlow runs seven tiers in separate processes. Release is signing, notarizing, and staple — the ListenToMe agent file requires releases to target an exact source commit. Then Prove, in the last row: a review that told the author not to promote a build that had 97.24% coverage. That decision is the rarest artifact in software, and it is the spine of this course. Timing: 6 minutes. Transition: why one method across three products? -->

---

## Prove is the spine

- Tests validate what you built
- Evidence discipline validates what you shipped
- SignUpFlow's record keeps its failures
- A browser click race; mypy debt marked "not a pass"
- Pointer: `SignUpFlow/docs/playbooks/validation.md`

<!-- NOTES: Read that validation playbook and you will find the engineer listing his own failures: a browser timing race that made a test flaky, and a type-checking debt line that says explicitly "not a pass." He could have deleted both lines. Keeping them is what makes the passing numbers believable. When you write your capstone evidence record, the failures section is not optional — a record with no limitations reads as unverified, because it usually is. Timing: 4 minutes. Transition: now the method, applied by you, in the next twelve minutes. -->

---

## M0.3 — Set up and get your first win

- Clone the three case studies
- Verify Python 3.11 or newer
- Install Ollama, pull a small local model
- Run SignUpFlow's solver on sample data
- Run TinyCopilot's test suite
- Post your first win

<!-- NOTES: Everything in this segment is a command you type, not a concept you remember. The whole sequence is under fifteen minutes and most of that is download time. Do it live with me, in order, and do not skip the test suite at the end — it is the exact acceptance gate you will re-implement in Module 2, and seeing it green now tells you your environment is real. Timing: 1 minute. Transition: first three commands, clone. -->

---

## First ship-win — clone and run the solver

```bash
git clone https://github.com/tomqwu/ListenToMe.git
git clone https://github.com/tomqwu/SignUpFlow.git
git clone https://github.com/tomqwu/ai_qe.git
cd SignUpFlow && make setup
poetry run python -m api.cli.main init my-church
poetry run python -m api.cli.main solve my-church
```

- Capture the `Health score:` line
- Sample output: `Health score: 100.0/100`
- Saved to `my-church/output/solution.json`

<!-- NOTES: `make setup` installs the Poetry environment, runs migrations, and seeds data. Then `init` writes three YAML files — organization, people, events — and `solve` runs the real greedy scheduler. The sample workspace prints a health score of 100.0 out of 100, with zero hard and zero soft violations and a fairness standard deviation of 0.43. That health-score line is your first artifact. Keep the raw terminal output; do not retype it from memory. Timing: 5 minutes. Transition: now the local model. -->

---

## Local LLM in three commands

```bash
ollama pull qwen3:0.6b
ollama list
ollama run qwen3:0.6b "Reply with exactly: PONG"
```

- No API key, no cloud bill
- No transcript leaves your machine
- Module 2 builds a copilot on this foundation

<!-- NOTES: Install Ollama first, then pull a small model. The run command is your first local completion: one prompt, one answer, entirely on your hardware. Look at `ollama list` carefully — it is also the diagnostic for the one environment quirk in this lab. If every name it shows ends in `:cloud`, those are cloud-backed aliases, not local models, and a localhost URL proves nothing about where your text goes. We exploit that distinction in Module 3. Timing: 4 minutes. Transition: two valid environments, and you may have the second one. -->

---

## Two valid environments (say which you have)

- **Local model pulled:** `qwen3:0.6b` in `ollama list`
- **Only `:cloud` aliases:** still a valid, instructive setup
- Both complete Lab M0 and Lab M2
- Tell the difference by the `:cloud` suffix
- Pointer: `course/03-content/m02-ondevice-app/tinycopilot/README.md`

<!-- NOTES: I want to be explicit, because students with an unusual daemon sometimes think they are blocked. If `ollama list` shows only cloud aliases, you are not blocked. That environment is valid for Module 0 and Module 2 — for Module 2 you either pull a genuinely local model or run roles in cloud mode. Module 3's privacy lab is richer with a local model, and the fail-closed test passes either way. State which environment you have in your first-win post. Timing: 3 minutes. Transition: the lab turns all of this into a pass or fail checkpoint. -->

---

## Lab M0 — Environment Setup & First Ship-Win

- **Goal:** every tool installed and proven with real output
- **Time:** 20–40 minutes, mostly downloads
- **Pass gate:** solver output with health score
- **Pass gate:** `ollama list` shows at least one model
- **Pass gate:** TinyCopilot suite green, or the missing dependency named
- Guide: `course/03-content/m00-orientation/lab.md`

<!-- NOTES: The lab has six steps and a six-item acceptance checklist — clone, Python version, Ollama, solver, TinyCopilot tests, community post. The TinyCopilot suite is the Module 2 reference implementation; run it from the course folder with pytest, or `make lab-m2`. Expected result: 191 passed at 100% coverage, with a ninety percent floor enforced. If a dependency is missing, name the exact missing package in your evidence log instead of guessing — an honest partial is a pass, an invented green is the only automatic fail. Timing: 3 minutes. Transition: quick check of your knowledge. -->

---

## Quiz M0

- 8 questions: 6 multiple choice, 2 short answer
- Archetypes, proof assets, loop stages, environment
- Pass standard: 75% average across the course
- Open-book by design — the pointers are the point
- File: `course/03-content/m00-orientation/quiz.md`

<!-- NOTES: Two of the eight questions are short answer and are graded against a model answer, so write them as applications, not definitions. One asks for the exact two solver commands after setup and the line to capture. Another hands you a friend's product idea and asks which archetype it is and which repo to study for the method. If you can answer those two, you have the module. Take the quiz after the lab, not before — several questions are easier once you have seen the real output. Timing: 1 minute. Transition: recap. -->

---

## Recap

- Three repos, three archetypes, one method
- Production-grade = proof you can open
- Loop: Study, Spec, Build, Validate, Release, Prove
- Prove means recording failures too
- You already ran production software and a local model
- Keep both outputs in your evidence log

<!-- NOTES: If you remember three things: the archetypes each have a distinct proof asset; the loop has six stages with a real artifact at each; and Prove is the stage that separates a portfolio project from a product. You have already run a production scheduler and a local language model before Module 1 — that is the first win, and it is banked. Paste both outputs into the evidence log you started today, with the date on each entry. Timing: 2 minutes. Transition: one question to take into the community. -->

---

## Discussion prompt

- Post: solver health score + `ollama list` + archetype note
- Answer: which proof asset surprised you most?
- Would it survive a skeptical customer opening the file?
- Reply to one peer: the archetype that fits their goal
- Disagreement welcome — point at the reason

<!-- NOTES: Your post has three parts: the solver output including the health-score line, your `ollama list`, and one sentence naming which archetype you want to build by week 8. Then the real question: which proof asset from this module surprised you, and would it survive a skeptical customer opening the file? Reply to one other student and tell them which archetype you think their goal belongs to. If you disagree with them, say why and point at the file. Timing: 2 minutes. Transition: Module 1 builds your own operating system. -->
