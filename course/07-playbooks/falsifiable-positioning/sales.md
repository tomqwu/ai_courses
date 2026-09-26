# Sales Page: Competition Table to Falsifiable One-Liner

## [Hero]

# A positioning sentence a skeptical buyer can check, clause by clause.

A standalone playbook: build a dated comparison table where every cell carries a source or says "unverified", derive a one-liner whose every clause traces to a column, and run the deletion test to find which clauses separate you from rivals and which are decoration.

**You leave with:** a table template, a one-liner worksheet, a deletion-test table, a "what we don't do" list, and a script that flags unsourced cells.

## [Who this is for — and isn't]

**For you if you:**
- Are about to write a landing page, store listing or README headline for a technical product.
- Have a tagline made of adjectives ("powerful, private, modern") and cannot say which rival each word rules out.
- Sell to engineers, who will open your competitor's pricing page to check you.

**Not for you if you:**
- Want brand voice or copywriting style. This is about what the sentence claims, not how it sounds.
- Have no rivals you can name and visit. The method needs at least five.

## [The problem]

A tagline made of adjectives cannot be wrong, so it cannot persuade anyone who checks. A falsifiable line can be wrong, and a buyer who checks it and finds it true believes it. The harder problem is drift: a line that was true when written stops separating you as rivals catch up. ListenToMe's own analysis records this: on-device, bring-your-own-model and free/open-source became "table stakes within that open-source cluster rather than a differentiator" (`ListenToMe/docs/competition-analysis.md:82`).

## [What you get]

- `playbook.md`: ten numbered steps, templates for `docs/competition.md` and `docs/positioning.md`, the `check_table.py` script, a checklist, a worked example, a scored self-check and a list of limits.
- A full deletion test run on a real 14-row table, showing which clauses of a published one-liner still do separating work.

## [What you'll be able to do]

- Fill a comparison table without a single price from memory, with uncertainty stated in the cell.
- Write a one-liner in the form wedge × differentiators × audience, and map every clause to a column.
- Run the deletion test, cut redundant clauses in order, and name the row each surviving clause keeps out.
- Turn ambiguous words such as "free" into the reading your table proves.
- List what your product does not do, and answer the three objections your own table invites.

## [Proof]

- The worked example is ListenToMe's real analysis: a dated header with a qualification rule (`ListenToMe/docs/competition-analysis.md:3`), a 14-row table (`ListenToMe/docs/competition-analysis.md:20-35`), and a published one-liner (`ListenToMe/docs/competition-analysis.md:88`).
- The playbook runs the deletion test on it and reports the result, including that the README and the analysis carry two different versions of the sentence (`ListenToMe/README.md:7`).
- `check_table.py` was run on 2026-09-26 against a passing file, a failing file, and ListenToMe's table; the outputs are in the playbook.

## [Instructor]

Written from the AI Product Studio course by Tom Wu, who builds in public. ListenToMe is his; the playbook tests his own published sentence and reports where it falls short.

## [Testimonials]

None yet. No buyer has used this playbook. This section stays empty until one does.

## [FAQ]

**My product has no privacy angle.** Replace the "on-device" column with your own main axis. The method is the same.

**Does the script check that my sources are right?** No. It checks that every cell cites one and every web source has a URL and a read date. You still open one at random.

**Is this legal advice on comparative advertising?** No. It does not cover the rules for naming competitors.

**Refunds?** Set by the owner with the final price. This draft promises none.

## [Pricing]

**$29** (proposed; the owner sets the final price).

The full AI Product Studio course ($399, `course/04-sales/landing-page.md`) teaches this method inside a nine-module path that goes on to pricing and a full sales page. If you are building the whole product, it is the better value.

## [Final call]

Write the sentence your rivals' own pricing pages would prove, and cut every word they would not.
