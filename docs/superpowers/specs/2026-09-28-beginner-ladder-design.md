# The beginner ladder — design

Date: 2026-09-28. Status: approved in conversation with the owner; this document is the record.

## Why

Two pieces of owner feedback:

1. The course should climb a ladder a newcomer recognises: foundation → a static website → a complex
   website → an iPhone app → selling it.
2. Learners without a computer-science background find the content dry and hard to follow. The
   current modules open on repository pointers, line ranges and code exhibits: proof for an
   engineer, noise for a founder, designer or small-business owner.

## Decisions

| Question | Decision |
|---|---|
| Who the ladder is for | **Non-coders who want to ship**: founders, designers, domain experts, small-business owners. They build with an AI agent; every concept is explained from zero. |
| How to get there | **A new beginner ladder on top of today's modules.** The ten existing modules (M0–M9) stay, unchanged, as the "peek inside" library the ladder links into, and as the depth engineers and the paid paths keep using. |
| The ladder | Five rungs, six modules (L0–L5); the content product (ai_qe) is folded into the static-website rung as its real-world example. |
| The app rung | ListenToMe's **iOS app** first (it has `iOS/`, `iOSShared/`, a share extension; the core package targets iOS 18 and macOS 15), then the same app on the Mac. |
| How a unit teaches | **Story → do it → check it worked → peek inside.** |
| Which AI tool | **Tool-agnostic**: every step reads "ask your agent to…", with short notes for Claude Code, Codex, Cursor and Copilot only where they differ. |

## The ladder

| Rung | Module | The learner ships | Real-world example | Peek inside |
|---|---|---|---|---|
| 0 Foundation | **L0 — Your computer, your AI agent** | tools installed; a first request to an agent; a rules file it follows | the three products, as a tour | M9 (setup), M0, M1 |
| 1 Static website | **L1 — Your first website** | a one-page site of their own, live on GitHub Pages | ai_qe, a real Pages site with citations | M9, M6 |
| 2 Complex website | **L2 — A website with logins and a database** | a small sign-up app running on their machine | SignUpFlow | M4 |
| | **L3 — Keep users' data apart, and prove it** | a test that shows one user cannot see another's data | SignUpFlow | M5 |
| 3 Phone app | **L4 — An iPhone app with AI on the device** | a small app in the iPhone Simulator, then on the Mac | ListenToMe (iOS → macOS) | M2, M3 |
| 4 Sell & launch | **L5 — Price it and launch it** | a price, a one-page sales page, a launch email | this course | M7, M8 |

Each L-module is 30–45 minutes of reading and listening plus one guided build; the whole ladder is a
weekend or two of evenings. L4 needs a Mac with Xcode and says so on its first screen; every other
rung works on Windows and macOS.

## A ladder module

An L-module has 3–4 units. Every unit has the same four parts, in this order:

1. **The story (1–2 minutes).** A plain situation with a picture ("Maria runs a bakery. She wants a
   page that shows today's bread and takes pre-orders."), then *what you will have at the end*, shown
   as a screenshot of the finished thing. A new idea is explained here with an everyday comparison,
   only when the unit needs it ("a database is a spreadsheet the website can read and write").
2. **Do it.** A numbered, guided build with the learner's agent. Each step has three parts:
   - **Ask your agent** — the exact request to paste.
   - **You should see** — a screenshot or the words that appear.
   - **If you see something else** — the two or three common problems, and what to type next.

   Tool-specific notes sit in a collapsed box only where the tools differ.
3. **Check it worked.** Two to four items the learner can verify by looking, never by reading code
   ("the page opens at your-name.github.io"; "a second user cannot see the first user's orders").
4. **Peek inside** (collapsed, optional). "How the real product does it": one figure from the case
   study, two or three sentences, and a link to the M-module part that teaches it (*SignUpFlow does
   this in one file → M5, part 4*). Code, commands the learner does not run, and repo pointers live
   here and only here.

Narration stays (the text is on the page, as on every Learn page), and so does a short check: 4–5
"which would you do?" scenario questions per module, not recall.

## Writing standard for ladder modules

A new section of `course/01-design/content-standards.md`, "Writing for the ladder":

- **Plain words first.** Every technical word is explained in the sentence that first uses it, and is
  in the module glossary with a one-line plain meaning. Sentences short; one idea each.
- **The learner is the subject.** Steps are about *your* site and *your* app; the case study appears
  in the story and in peek inside, not in the steps.
- **No code in the main path.** Code blocks and repository paths appear only inside peek inside and
  inside "Ask your agent" paste boxes.
- **Tested for real.** Every "Ask your agent" step has been run with a real agent before it ships.
  The run is kept in the module's `runs/` folder (dated transcript and screenshots), and "You should
  see" shows what that run produced — not what it should have.
- **Both editions.** A ladder module ships in English and Chinese together (the Chinese edition,
  #121), held to the same parity check.

What the gate checks, for L-modules only:

- no fenced code or repository path outside peek inside and paste boxes;
- sentence length and a list of jargon words that must be explained (the list lives beside the
  check and grows);
- every peek-inside link resolves to an existing M-module part;
- a `runs/` record exists for every build step, and its screenshots are in the figure manifest;
- the Chinese sources match part for part and are stamped (`zh_edition.py`).

## Site

- **Sources:** `course/03-content/l0-…` to `l5-…`, the same files as an M-module (slides, lesson,
  handout, glossary, lab, quiz, narration, `zh/`) plus `runs/`. Built into the same Learn / Read /
  Lab / Check modes with the existing machinery (narration, progress, search, both editions).
- **One new block** in the slide and lesson Markdown for a guided step (ask / see / if not), and one
  for peek inside; both render in the existing page frame and in the Chinese edition.
- **Home and paths:** the home page leads with the ladder; the paths page gains "The ladder: from
  zero to shipped". The M-modules sit under "Go deeper"; the current paid paths stay as they are.

## Adding content over time

Content will keep being added: new rungs, new units, new peek-inside links, new languages of the
same material. The procedure lives in the `course-content` skill
(`.claude/skills/course-content/SKILL.md`), which every contributor — person or agent — loads before
touching course content. This design adds to it:

1. **"Add a ladder module or unit"** — the file set, the four-part unit, the guided-step and
   peek-inside blocks with a copyable example, where the module is registered (deck list, verify,
   paths, the unit count), the `runs/` record, and the two editions.
2. **"Run a build step for real"** — how to run an "Ask your agent" step with an agent, what to keep
   (dated transcript, screenshots through the screenshot pipeline), and how to update "You should
   see" from the run.
3. **"Link a peek inside"** — how to choose the M-module part, and the check that keeps the link valid
   when M-modules change.
4. **"Keep the Chinese edition current"** — already required by AGENTS.md; restated for ladder
   modules, which are translated as they are written rather than after.
5. **"Writing for non-coders"** — the checklist from the writing standard, with a before/after
   example rewritten from an existing M-module passage.

AGENTS.md gets one line in its map and one rule: *the ladder is written for non-coders; its main
path carries no code, and every build step is run for real before it ships.*

## Order of work

1. Finish what is in flight: ship the Chinese edition (#121); then fix the English-source issues the
   translators reported (a list collected in #121) and re-stamp the Chinese.
2. Build the ladder machinery (guided-step and peek-inside blocks, the L-module checks, the ladder on
   the home and paths pages) and the skill's new procedures.
3. **L1 — Your first website** as the pilot: the smallest real build, doable on Windows or Mac.
   Review it with the owner before writing the rest.
4. Then L0 → L2 → L3 → L5 → L4 (the iPhone rung last: it needs Xcode and the most real-run testing).
5. Each module is its own issue and PR, merged to `main` when green, in both editions.

## Out of scope

- Rewriting M0–M9. They stay the verified depth; ladder modules link into them.
- A Chinese narration voice (the recordings stay the English preview voice; #21 decides the release
  voice).
- New case-study repositories.
