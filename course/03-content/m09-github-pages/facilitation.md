# Facilitation — M9: Ship a Product Catalog with GitHub Pages

> For an instructor running this module live, in a cohort session or a workshop. Self-paced learners
> can skip this file. The module is free and standalone, so the room may hold people who have never
> used a terminal next to people who use one daily; plan for both.

## Before the session

**Send the installs ahead.** Installs are the only part of this module that can take an unpredictable
amount of time, and a room of people waiting on downloads is a lost hour. Two days before, send the
Step 0–1 instructions from `lab.md` with one request: run the setup check and reply with the last line
it printed. Anyone who replies **4 of 4** can skip the first twenty minutes.

**Know which systems are in the room.** Ask for Windows or macOS with the reply. Windows machines
issued by an employer sometimes block `winget` or App Installer by policy; find out before the
session, not during it. For those learners the fallback is to install Git for Windows and the GitHub
CLI from their release pages, then run the same setup check.

**Have a spare repository to show.** Publish the starter to a repository of your own the day before,
so you can show a live address and the Actions tab while the room's first builds are still running.

## Timing

| Block | Minutes | What happens |
|---|---|---|
| Opening and outcomes | 5 | Slides 1–2; the five outcomes read as the lab checklist |
| M9.1 tools, proven | 20 | Everyone at **4 of 4** before moving on |
| M9.2 folders and cloning | 15 | Paths, then the course cloned into `~/code` |
| M9.3 build and publish | 20 | Starter copied, products edited, Pages enabled |
| The wait, used well | 10 | While builds run: the limits and the no-shop rule |
| Republish and share | 15 | Step 8, then the discussion prompt |
| **Total** | **85** | |

## Running each segment

**M9.1.** Do not move on until every learner shows 4 of 4 or has a named blocker. Walk the room with
one question: *which window did you install from, and which one are you running the check in?* It
resolves most Windows failures in one sentence. On Macs, the usual failure is the skipped Homebrew
setup lines; ask the learner to scroll up.

**M9.2.** Make everyone type `pwd` before they clone, out loud if the room is small. The most common
lost ten minutes in this module is a clone in the home folder and a search for it in `code`. Show Tab
completion early; it prevents half the typos you would otherwise fix.

**M9.3.** Learners who finish early should add photos (the lab's stretch) or a second category, not
move ahead to publishing alone: publishing is the moment worth sharing as a room. When you reach the
no-shop rule, read GitHub's own sentence from the limits page aloud rather than paraphrasing it. It is
more persuasive in the original, and it explains why the starter has no cart.

## Breakout prompts

1. *Pair on the phone test.* Swap addresses with a partner. Each opens the other's catalog on a phone
   and reports the first thing they tapped that did not do what they expected.
2. *Where does the button go?* Each pair decides, for one real product, where its `buyUrl` would point:
   a payment link, a marketplace listing, or "Ask about this". Say why out loud.
3. *Read a real pipeline.* Stronger learners open `ai_qe/.github/workflows/pages.yml` and list three
   checks it runs before deploying that their branch-published catalog does not.

## Common failures, and the one-line fix

| Symptom | Cause | Fix |
|---|---|---|
| "is not recognized" after an install | the window predates the install | open a new window |
| `brew: command not found` | Homebrew's setup lines skipped | scroll up, run them |
| check says 3 of 4, identity missing | `git config` never run | the two `git config --global` lines |
| `gh auth login` stuck on the code | browser opened a different account | sign out in the browser, retry |
| "products.js did not load" | a missing comma | the browser console names the line |
| 404 at the address | build still running, or `/docs` chosen | wait; choose `/ (root)` |

## Closing

End on the discussion prompt: every learner posts an address and the setup step that took longest,
with the line that fixed it. That list, collected across cohorts, is the best input for improving the
setup check itself.

## After the session

Collect two things from every learner within a day: the published address, and the evidence file's
list of failures with their fixes. Anyone without an address gets a direct message naming the step
their evidence stopped at, not a general reminder. Add any new failure to the table above, and if it
could be detected, to the setup check itself.
