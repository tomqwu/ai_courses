# M0 — Video Recording Scripts

> One recording per segment. Read the narration aloud as written; it is timed for ~130 words/min.
> Open the pointer files on screen when the beat says so — the pointer is the evidence.

## M0.1 — Why three types, and why these

**Target runtime:** 8:00 · **Word budget:** ≈1,040 words at 130 wpm (beat narration below is the
condensed spine; pause on screen opens rather than filling every second with speech).

**Cold open (0:00–0:15).** "Three products. One built by an engineer who wanted meetings transcribed
on his own laptop. One that schedules church volunteers. One that is a research briefing with no app
at all. Same method, three times. Here is what that buys you."

**Beats.**

| Time | On screen | Narration |
|---|---|---|
| 0:15 | Slide: three archetypes | Almost everything a solo technical builder can ship is one of three shapes: an app that runs on the device, a multi-user service that runs on a server, or a body of verified knowledge sold as content. Your build skills differ wildly between them. Your method does not. |
| 1:30 | `ListenToMe/README.md`, coverage badge | Look at this README. The badge says ninety-six percent core coverage. That is not a claim the author typed — a test run produced it. Same page: notarized DMGs on Releases. Then open `ListenToMe/docs/competition-analysis.md`: fourteen rows, each with a source and a date. Positioning work done as research. |
| 3:00 | `SignUpFlow/docs/playbooks/validation.md` | SignUpFlow is server-side and spec-driven. Scroll to the dated line: "1,464 passed, 21 skipped." Notice that skips are counted. Seventeen spec folders live under `SignUpFlow/specs/`, and `SignUpFlow/docs/TESTING.md` describes seven test tiers run in separate processes. |
| 4:30 | `ai_qe/research/reviews/site-audit-2026-09-06.md` | The third product is not software. AI × QE is a briefing site — a hundred and sixteen slides across four decks, shipped as PDF editions. Its proof asset is this file: a fourteen-finding audit of the author's own site, with per-finding evidence and acceptance criteria. |
| 6:00 | Table: three proof assets | So here is the definition this course uses. Production-grade means a shipped artifact with proof you can open. A badge, a dated evidence line, a published audit. All three are files. None of them is a testimonial. Your labs are graded against that same bar. |
| 7:15 | Slide: action step | Skim the three READMEs and find one proof asset in each. Then write two sentences: which archetype you most want to build by week eight, and one thing you have shipped before. Keep it — you will post it in M0.3. |

**Demo cue.** Terminal and browser side by side. Open the three pointer files in order; do not scroll
past the badge, the dated line, and the audit's first finding. The viewer should notice that each
proof asset is a *file*, and that all three are dated or machine-generated.

**Action-step close.** "Two sentences, in your notes: my archetype, and one thing I have shipped.
That is the seed of your week-eight pitch."

**Recording notes.**
- Enlarge terminal font and the README badge; the numbers are the content.
- If over time, cut the AI × QE deck-count detail and keep the self-audit.
- Do not say a deck count you have not read from `ai_qe/_data/briefing_room.json`.
- Do not call ListenToMe "the best" meeting app — the competition table is sourced; superlatives are
  not.
- Keep an on-screen lower-third with `ListenToMe/docs/competition-analysis.md` while speaking.

## M0.2 — The method: the Spec-to-Ship Loop

**Target runtime:** 10:00 · **Word budget:** ≈1,300 words at 130 wpm (condensed spine below).

**Cold open (0:00–0:15).** "Most projects do not fail at coding. They fail at the moment the author
decides the work is done. This segment is six stages that make 'done' an artifact instead of a
feeling."

**Beats.**

| Time | On screen | Narration |
|---|---|---|
| 0:15 | ASCII loop diagram | Six stages: Study, Spec, Build, Validate, Release, Prove. You will run all six in every module of this course, and once more on your capstone. Copy this diagram into your notes now, because we are about to hang a real file on each stage. |
| 1:15 | `ListenToMe/docs/competition-analysis.md` | Stage one, Study. Twelve competitors, sourced claims, dated. And in `ai_qe/docs/principles.md`, the first principle is "Baseline before solutioning." Positioning is a research artifact, not a slogan. |
| 2:45 | `SignUpFlow/specs/014-security-hardening/spec.md` | Stage two, Spec. Prioritized stories, Given/When/Then acceptance scenarios. Here is an honest detail: spec 014 has no tasks file. Read the task format from `SignUpFlow/specs/019-sms-notifications/tasks.md`, where each checkbox task names an exact file path and tests come first. |
| 4:30 | `ListenToMe/docs/superpowers/specs/2026-06-18-listentome-design.md` | ListenToMe does the same job differently: a design spec with protocol-level interfaces and a non-goals list — "No cloud backend, accounts, billing, or multi-user." Writing down what you refuse to build is spec work. |
| 5:45 | `ListenToMe/README.md` coverage floor | Stages four and five. Validate: SignUpFlow's seven tiers and dated counts; ListenToMe's ninety-five percent coverage floor enforced by a script. Release: signed, notarized DMGs that target an exact source commit. |
| 7:15 | `ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md` | Stage six, Prove. This review told the author: do not promote the existing 1.3.0 build — despite ninety-seven point two four percent core coverage. Someone measured something, wrote it down, and blocked their own release. That is the rarest artifact in software. |
| 8:30 | `SignUpFlow/docs/playbooks/validation.md` | It gets harder. SignUpFlow's validation record includes a browser click race that made a test flaky, and a type-checking debt line that reads "not a pass." He could have deleted both. Keeping them is what makes the passing numbers believable. |

**Demo cue.** Screen-share the loop diagram first, then open each file at the cited location. The
viewer should notice the pattern: Study and Spec produce documents, Build and Validate produce
commands and counts, Release and Prove produce signed artifacts and honest limitations.

**Action-step close.** "Start your loop journal — one file, kept all course. For every action step
from here on, write one line per stage you touched. Your first entry is M0.3: Study the README, Build
by running the solver, Prove by posting the output."

**Recording notes.**
- Keep the loop diagram on a second monitor the whole segment; viewers need it while you talk.
- If over time, cut the ListenToMe design-spec beat and keep spec 014 plus the gap review.
- Never say the loop "guarantees" shipped products — it is a discipline, and the repos show it
  catching failures, not preventing all of them.
- Do not read the 1.3.0 coverage number without the pointer file visible next to it.
- Pause two full seconds after the gap-review line; it is the emotional center of the module.

## M0.3 — Set up and get your first win

**Target runtime:** 12:00 · **Word budget:** ≈1,560 words at 130 wpm (commands run on screen; narration
fills download waits).

**Cold open (0:00–0:15).** "By the end of this segment you will have run a production scheduler and a
local language model. No API key. No credit card. About thirty minutes, mostly downloads."

**Beats.**

| Time | On screen | Narration |
|---|---|---|
| 0:15 | Terminal: `python3 --version` | Two requirements, both free. Git, and Python 3.11 or newer. SignUpFlow's build gate accepts 3.11 through 3.13 — check yours before anything else, because a wrong interpreter burns ten minutes at the worst moment. |
| 1:00 | Terminal: three `git clone` lines | Clone all three case studies into one parent folder. Keep them siblings; every pointer in this course is written relative to that root. |
| 2:00 | Terminal: `cd SignUpFlow && make setup` | `make setup` installs the Poetry environment, runs database migrations, and seeds sample data. It may take a few minutes. Watch the output — if Poetry is missing it stops and tells you. Fix: `make install-poetry`, add `$HOME/.local/bin` to your PATH, reopen the shell. |
| 4:00 | Terminal: `init` and `solve` | Two commands. `init my-church` writes three YAML files: organization, people, events. `solve my-church` runs the real greedy scheduler. Here is the output: five people, two events, mode relaxed, then the health-score line, the violation counts, and a fairness standard deviation. The numbers are whatever the revision you cloned produces — at the current head the sample scores zero out of one hundred with two hard violations, and that is fine. The solution is written to `my-church/output/solution.json`. |
| 6:00 | Terminal: highlight health score | Capture the whole block around that health-score line — the run record is the artifact, not the number. It is your first artifact in this course, and it is not a toy — this is the same solver whose evolution you will trace from specification to code comment to test oracle in Module 5. |
| 6:45 | Terminal: `ollama pull qwen3:0.6b` | Now the local model. Install Ollama, then pull a small model. While it downloads, look at the daemon you have. Run `ollama list`. |
| 8:00 | Terminal: `ollama list` | Read the names carefully. Any name ending in colon-cloud is a cloud-backed alias, not weights on your disk. A localhost URL proves nothing about where your text is processed — that distinction becomes the Module 3 privacy lab. |
| 9:00 | Terminal: `ollama run … PONG` | One prompt: reply with exactly PONG. That answer was generated on your machine. No key, no bill, no transcript leaving the laptop. Module 2 builds a three-role copilot on exactly this foundation. |
| 10:00 | Terminal: `make lab-m2` in tinycopilot | Before Module 1, not tonight's pass gate: move to the course folder and run the TinyCopilot test suite, or `make lab-m2`. Expected: two hundred one passed, one hundred percent coverage, with a ninety percent floor enforced. If pytest is missing, install it in a virtual environment — a system Python with PEP 668 protections will refuse a global install, and the error names that clearly. |
| 11:15 | Slide: acceptance checklist | Now post your first win: the solver output including the health score, your `ollama list`, and one sentence naming the archetype you want to build by week eight. Complete Lab M0 for the full checklist. |

**Demo cue.** One terminal, one window, large font. The viewer should notice two things: the solver
summary block is machine output you record as printed, and the local model answers without any network
configuration. Keep the health-score line on screen while you talk about the module map.

**Action-step close.** "Post the three-part first win in the community, then complete Lab M0. That
checklist is your first pass-or-fail checkpoint in this course."

**Recording notes.**
- Blur nothing, but use a sample workspace only — never a real organization's data.
- If over time, cut the `make setup` walkthrough to its last two lines; keep the solver output and
  the `:cloud` explanation, which carry the teaching.
- Do not promise identical numbers; `Solved in …ms` and the `Range:` dates vary by machine and day,
  and the score moves with the SignUpFlow revision (`0.0/100`, 2 hard violations at the 2026-09-16 head).
- Do not read a health score you have not seen on screen; say what your run printed.
- Show the PEP 668 error text on screen rather than paraphrasing it.
