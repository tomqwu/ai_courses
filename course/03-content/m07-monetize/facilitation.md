# Facilitation Kit — M7 Workshop (90 minutes)

> One live session tied to M7, run in the cohort's week 7 slot. Formula: **I do / We do / You do**.
> Pre-work students must have done: M7 lessons, Quiz M7 attempt, and a draft pricing table for their
> own product (Lab M7 Step 1). Bring: the module's comparator table open in a second window.

## Timing table

| Minutes | Activity | Mode | Artifacts produced |
|---|---|---|---|
| 0:00–0:02 | Opening hook: the two prices | I do | — |
| 0:02–0:17 | Price one real product live against the table | I do | On-screen worksheet, filled |
| 0:17–0:35 | Cohort computes one cost floor and comparator band | We do | Shared floor line + band |
| 0:35–0:49 | Gate and package one tier together | We do | One tier with "NOT included" lines |
| 0:49–1:03 | Breakout A: price your own product | You do | Posted worksheet + one-liner |
| 1:03–1:18 | Breakout B: skeptical-engineer cross-review | You do | Three answered objections |
| 1:18–1:25 | Debrief: what the artifacts proved | We do | Instructor notes, stuck points |
| 1:25–1:30 | Close and lab handoff | I do | — |

Ratio ≈ 22 / 39 / 29. Sum: 90 minutes.

## Opening hook (2 min) — script

"Granola charges about fourteen dollars per user per month. MacWhisper charges about sixty-nine
dollars, once. Both transcribe meetings. One of them is pricing a cost that recurs — and the table
tells you which. In the next fifteen minutes I will price a product out loud using nothing but the
rows in `ListenToMe/docs/competition-analysis.md`, a cost floor, and one benchmark from the market
research. If you can watch me do it, you can do it. Write down the moment you disagree with me —
that disagreement is your breakout contribution."

## I-do (15 min) — price one product live

Screen-share, do not slides. Open `ListenToMe/docs/competition-analysis.md`; read the header
qualifier aloud ("approximately" / "reportedly"), then read the Granola, Otter, and MacWhisper rows.
Say the rule — if per-user costs recur monthly, price monthly; if they do not, a subscription is a
tax your users can audit. Then fill the Lab M7 worksheet on screen for a hypothetical on-device app:
floor ($0 marginal compute, dev time amortized), comparator band ($0 to ~$69 one-time), value anchor
(a ~$14–35/user/mo subscription avoided), chosen model, two tiers with exclusions, launch price.
Deliberately make one mistake — start to price at $0 because "ListenToMe is free" — then correct it
on screen: $0 is occupied, so the Pro tier must price convenience.

## We-do (18 + 14 min)

**Block one — floor and band (18 min).** Ask the cohort for their own fixed monthly lines. Build one
floor on the board, then divide by the chosen price minus per-sale fees to get break-even sales/month.
Compare against the course's own record in `course/04-sales/pricing-and-platforms.md`: ≈$80–130/mo
fixed, ~2 sales/month at $399. The teaching move is the order: floor, band, anchor, price.

**Block two — gate and package one tier (14 min).** Take one volunteer's product. Ask: *which path is
not proven yet?* Then apply `SignUpFlow/README.md`'s pattern — register the paid path, flag it off,
never let the core workflow depend on it (`SignUpFlow/AGENTS.md`: "core scheduling must not require
either paid integration"). Write one "NOT included — because" line aloud.

## Breakout instructions

**Groups:** 3–4 students, assigned by archetype where possible. **Roles:** one *pricer* (fills the
worksheet), one *skeptic* (must find the row that undercuts the price), one *scribe* (posts), and, in
groups of four, one *timekeeper*. **Time:** 14 minutes in Breakout A, 15 in Breakout B.

**Deliverable to post (one per group):** a single message containing the launch price, the one-liner,
one "NOT included — because" line, and the row name that anchors each clause.

**Exact prompt (paste to breakout channels):** *"Fill the Lab M7 worksheet for one real product: cost
floor in dollars, comparator band from a row you can open, value anchor, chosen model, two tiers with
exclusions, launch price. Then write the one-liner and map every clause to a column. Finally, name
the three objections your own table invites and answer each with a row or a file pointer. Post the
price, the one-liner, and your weakest 'NOT included' line."*

## Discussion prompts

1. **"Which row undercuts your price, and what do you say to that buyer?"** Follow-up probe: *"What
   does the row's cost column show that yours doesn't?"* Strong answer names the row, reads its cost
   structure, and either defends the delta or cuts the price.
2. **"Name a clause in your one-liner that no row would notice if you deleted it."** Probe: *"So why
   is it there?"* Strong answer cuts the clause on the spot.
3. **"What does your product deliberately not do, and who will complain?"** Probe: *"Is the
   exclusion honest packaging or a crippled core?"* Strong answer distinguishes a deferred paid path
   from a gated essential workflow.
4. **"Where did your floor change the price you wanted to charge?"** Probe: *"What did the floor
   calculation make you raise or drop?"* Strong answer shows a number moving because of arithmetic.

## Watch-fors

| Stuck point | Symptom | 30-second intervention |
|---|---|---|
| Price anxiety (instructor guide §4) | "Nobody would pay X" | Run the floor and the band out loud; undercharging 2–5× is the documented failure mode |
| Memory-only prices | Rows with no URL | "Open the page now; we wait" |
| Subscription reflex | Monthly price on an on-device product | Point at the On-device? column in their own table |
| Feature-list tiers | No "NOT included" line | Ask "what does the free tier deliberately keep?" |
| Unfalsifiable one-liner | "The best AI tool" | Run the deletion test; no clause breaks, so rewrite |
| Gating the core | "Pay to keep scheduling" | Read `SignUpFlow/AGENTS.md` line 18 aloud |

## Close (5 min) — script

"Three things to take into the lab. One: the model follows the cost structure — recurring cost,
recurring price; no recurring cost, charge once. Two: the floor comes before the price; a price below
it is a subsidy. Three: your one-liner is derived from your table, and the deletion test is the proof.
Post your worksheet, your one-liner, and your honest-limitation line before next session. Next week
is demo day preparation — Module 8 turns this page into the full sales page and the launch arc."

## Post-session checklist

- Record into the cohort log: attendance, the three most-missed quiz items, and the stuck points observed.
- Post to the community: the on-screen worksheet exemplar, the floor/band order diagram, and one anonymized objection-and-answer pair from a breakout.
- Review each group's posted price + one-liner; reply within 24 hours with one row they missed.
- Flag any table with memory-only prices for a direct message before Lab M7 is graded.
- Verify before next week that every pointer cited in the session still resolves (instructor guide §8).
