# Facilitation Kit — M1 Live Session (90 minutes)

> Week 1 of the cohort, per `02-instructor/instructor-guide.md` §2. Students arrive having read M1 and
> started Lab M1. The workshop formula is **I do / We do / You do**; the whole session ends with a
> binary artifact on screen. Scripts below are written for live delivery at roughly 90–110 words per
> minute, with pauses — not the 130 wpm of recorded video.

## Timing table

| Min | Activity | Mode | Artifacts |
|---|---|---|---|
| 0–2 | Opening hook: the unverifiable rule | I do | Slide 6 |
| 2–10 | The four-file stack and the 85-line constitution | I do | `SignUpFlow/.specify/memory/constitution.md`, `SignUpFlow/AGENTS.md` |
| 10–20 | Walk a real spec folder: the gate and a task line | I do | `SignUpFlow/specs/014-security-hardening/plan.md`, `SignUpFlow/specs/019-sms-notifications/tasks.md` |
| 20–32 | Rewrite one bad rule, live, and break it first | We do | Shared editor |
| 32–42 | Precedence and anti-hallucination drill | We do | `SignUpFlow/AGENTS.md` |
| 42–50 | Break | — | — |
| 50–66 | Breakout: write three rules for your own repo | You do | Posted `rules.md` |
| 66–78 | Breakout: reconstruct an evidence record from a failure | You do | Posted evidence entry |
| 78–85 | Debrief: what did the artifact prove? | You do | Two posted deliverables |
| 85–90 | Close and hand off to Lab M1 | I do | Lab M1 |

## Opening hook (0–2 min)

"Type this rule into your `AGENTS.md`: *be careful with multi-tenancy.* Now imagine handing that to a
stranger and asking: was it followed? You cannot answer. Neither can an agent. SignUpFlow's own
baseline makes the contrast in one line — *filter every query by `org_id`, not be careful with
multi-tenancy.* A filter is executable and checkable; careful is a feeling. In the next ninety minutes
we are going to take every vague rule you have ever written and find the command that proves it. That
is not a writing exercise. It is the difference between a rule and a wish."

## Breakout instructions

**Group size:** 3. **Roles:** a writer (types), a prover (invents the check command or inspection that
would prove each rule), and a skeptic (tries to break the rule by finding a case it does not cover).
Rotate roles between the two breakouts. **Time:** 16 minutes, then 12.

**Deliverable 1 — post exactly this:** a fenced `rules.md` block with three lines — one constitution
principle with a MUST or a default-off stance, one baseline `AGENTS.md` rule in imperative form, one
dated research-log observation from something the group actually hit. Under each line, one sentence:
*the command or inspection that proves it.*

**Exact prompt:** "Write three rules you would not be embarrassed to have an agent follow. For each,
name the artifact a stranger would open, or the command they would run, to check it. If you cannot name
one, rewrite the rule until you can."

**Deliverable 2 — post exactly this:** an evidence entry in the six-field format for a deliberately
failed run — commands with the failure line, counts, date, environment, revision, and limitations. The
failure stays in.

**Exact prompt:** "Here is a run that failed and then passed. Write the record as if you were the
careful engineer who ran it. Do not delete the failure. Name one thing the run does not verify."

## Discussion prompts

1. **"What makes a rule checkable?"** Probe: *read me your weakest rule — now what command proves it?*
   Strong answers name a command, a grep, or a file inspection, not a value.
2. **"The user's request is level 1; a path-scoped rule is level 3. Give me a conflict."** Probe: *which
   is more specific? which is safer?* Strong answers apply "follow the more specific and safer one"
   rather than defaulting to `AGENTS.md`.
3. **"Why would a production SaaS refuse CI?"** Probe: *what does a hosted check fail to record?*
   Strong answers name commands, environment, date, limits, and the revision — and note that hosted
   checks are not the only way to be rigorous.
4. **"What does 97.24% coverage prove?"** Probe: *what did that release review refuse to conclude?*
   Strong answers cite the ListenToMe gap review's "do not promote 1.3.0" and say coverage does not
   establish reliability.

## Watch-fors

| Symptom | 30-second intervention |
|---|---|
| "My constitution feels fake" (empty brackets) | "Steal structure, not content. Open `SignUpFlow/.specify/memory/constitution.md` — 85 lines — and write YOUR three principles. Imperative, verifiable, under 80 lines." |
| Rules come back as adjectives ("robust", "clean") | "Circle the adjective. What command would contradict it? That command is your rule." |
| Spec leaks `sqlite3` or `argparse` | "Run the checklist gate out loud: no implementation details. Move the library choice to `plan.md`." |
| Green run posted with no red run | "Show me the failing output first. A green-only record is an auto-fail — not because you cheated, because the evidence is incomplete." |
| Blank limitations field | "Name one thing your run does not verify. In-memory only? CLI by hand? Write it." |

## Post-session checklist

Record as evidence: attendance; the two posted deliverables per group; the most common unverifiable
word encountered (this drives the week-2 We-do); the quiz M0+M1 item analysis; and any rule that more
than 30% of the room wrote badly. Post to the community within 24 hours: a pinned thread titled
"M1 — before → after rule rewrites", the two best `rules.md` blocks (with permission), and the
instructor's own rewritten rule so students see the standard applied to you. Confirm every student
knows the Lab M1 pass gate is `python3 -m pytest tests/ -q` exiting 0 with the red run recorded.
