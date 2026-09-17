# M0 Facilitation Kit — One 90-Minute Live Session

> Use with `course/02-instructor/instructor-guide.md` (§1 first-win defense, §4 stuck points) and
> `course/03-content/m00-orientation/lab.md`. This is the onboarding workshop: by minute 90 every student has
> run real software and posted it.

## Timing table (sums to 90)

| Min | Activity | Mode | Artifacts |
|---|---|---|---|
| 0–2 | Opening hook | I do | This one-pager on screen |
| 2–12 | Archetype tour: open one proof file per repo | I do | `ListenToMe/README.md`, `SignUpFlow/docs/playbooks/validation.md`, `ai_qe/research/reviews/site-audit-2026-09-06.md` |
| 12–22 | The Spec-to-Ship Loop, one artifact per stage | I do | ASCII loop diagram + `ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md` |
| 22–30 | Live solver run; health-score line on screen | I do | `Health score: 100.0/100` |
| 30–50 | Breakout: clone + solve + post the summary | We do | Pasted solver block in the thread |
| 50–62 | Debrief: read three posts aloud; diagnose `:cloud` | We do | `ollama list` outputs |
| 62–80 | Archetype triage on real product ideas | You do | One-line archetype + repo-to-study per idea |
| 80–85 | Two pair reports | You do | Spoken, 60 s each |
| 85–90 | Close: evidence log, Lab M0, next week | I do | Checklist on screen |

## Opening hook (2 min) — script

"Show of hands: who has started an AI course before and stopped in week two? Keep your hand up —
that is the normal outcome, and it is not about you. It happens because the first hard lab arrives
before the first win. So we are inverting it. In the next twenty minutes you will clone three real
production products, run one of them, and pull a language model onto your own laptop. No API key. If
you leave tonight with a health score and an `ollama list` output, you are past the place most people
quit. Everything else in this course builds on that."

## Archetype tour (10 min)

Open the three proof files in this order and narrate decisions, not lines: the 96% core-coverage badge
(someone ran a coverage tool and rendered the number), the dated "1,464 passed, 21 skipped" line
(skips counted, not hidden), and the 14-finding self-audit (the author auditing his own site). Ask
once, aloud: "Which of these could a marketing team have written by hand?" None — that is the point.

## Loop walkthrough (10 min)

Draw the six stages live. For each, open one file and stop at the number: the 14-row competitor table
(Study), the Given/When/Then spec (Spec), the checkbox tasks with file paths (Build), the seven test
tiers (Validate), the signed DMGs (Release), and the review that says do not promote the 1.3.0 build
despite 97.24% coverage (Prove). Say plainly: Prove is the stage most portfolios are missing, and the
capstone rubric scores it.

## Breakout instructions

**Group size:** pairs (trios when the room is odd). **Roles:** *driver* types and shares their screen;
*navigator* reads the steps and watches for the first error line. Swap roles at step 4.

**Deliverable each pair must post to the thread, in one message:** (1) the solver summary block
including the `Health score:` line and the `Solution saved to …` line; (2) their `ollama list` output
with each entry labeled local or `:cloud`; (3) the exact line of `course/03-content/m00-orientation/lab.md` they are stuck on, if any.

**Exact prompt:** "Clone the three repos, run `make setup`, then `init my-church` and `solve
my-church`. Capture the full summary block — not just the health score. Then run `ollama list` and
label every entry local or `:cloud`. If something fails, post the failing command and the last error
line rather than a summary of it. You have twenty minutes; posting partial output beats finishing
quietly."

## Discussion prompts

1. **"Which proof asset surprised you most — and would it survive a skeptical customer opening the
   file?"** *Probe:* "What exactly would they see on the second page?" *Strong answer* names the file,
   the number, and what an unfriendly reader could still dispute.
2. **"Your daemon shows only `:cloud` names. Are you blocked?"** *Probe:* "What does the suffix tell
   you about where the text goes?" *Strong answer:* not blocked; those are cloud-backed aliases, valid
   for M0 and M2 (cloud mode), and M3's privacy lab becomes richer with a genuinely local model.
3. **"Which archetype is your week-8 product, and which repo do you study for the method?"** *Probe:*
   "What would you have to refuse to build to finish in eight weeks?" *Strong answer* picks one
   archetype, names the repo, and states a non-goal — the ListenToMe spec has one for exactly this
   reason.
4. **"Whose evidence record is more trustworthy: one with no failures, or one that lists its
   limitations?"** *Probe:* "Find the failure line in SignUpFlow's validation playbook." *Strong
   answer* points at the flaky browser race and the mypy debt marked "not a pass", and explains that
   the failures make the passing counts believable.

## Watch-fors (30-second interventions)

| Stuck point | 30-second intervention |
|---|---|
| `make setup` stops with `❌ Poetry is not installed or not in PATH` | "Run `make install-poetry`, then `export PATH="$HOME/.local/bin:$PATH"` in this shell and re-run `make setup`." |
| `pip install pytest pytest-cov httpx` returns `externally-managed-environment` | "That is PEP 668, not a broken Python. `python3 -m venv .venv && source .venv/bin/activate`, then install inside it." |
| `ollama list` shows only `:cloud` aliases | "You are not blocked. Label them and move on; for M2 either pull `qwen3:0.6b` or run roles in cloud mode." |
| `python3 --version` shows 3.10 or 3.14 | "SignUpFlow's gate is 3.11 through 3.13. Install that band, then re-run `make setup`." |
| Student pastes a health score with no summary block | "Paste the whole block; the `Solution saved to …` line proves the run wrote a file." |
| "This is just setup, when do we build?" | "You already ran a production scheduler. That is the win; Module 1 turns it into your own repo." |

## Close (5 min) — script

"Three things before you go. One: paste tonight's outputs into your evidence log with today's date —
that log becomes your capstone's evidence record. Two: finish Lab M0, all six checklist items; the
community post is one of them, and the pass gate is the solver output plus a non-empty `ollama list`.
Three: state your archetype, one of the three, because Module 1 starts building your own operating
system and the capstone contract is one archetype, one shippable scope, the loop complete."

## Post-session checklist

- [ ] Record which students posted a first win (the completion lever — instructor guide §1)
- [ ] Note every distinct error line seen, and append new ones to the watch-fors table
- [ ] Confirm each pair posted a deliverable; DM anyone missing
- [ ] Post the recording plus the top three stuck points and their fixes
- [ ] Log the session: attendance, completion %, and the archetypes chosen
- [ ] Verify pointers used tonight still resolve before the next cohort
  (`course/02-instructor/instructor-guide.md` §8)
