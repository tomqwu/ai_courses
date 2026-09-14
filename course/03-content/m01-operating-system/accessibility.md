# Accessibility — M1 (The AI Product Operating System)

> Applies to `slides.md`, `video-scripts.md`, `handout.md`, and the lab artifacts. A student who cannot
> see the screen, cannot hear the audio, or reads at a different pace must still reach the same four
> capabilities and the same pass gate.

## Deck accessibility (`06-production/slides/aps.css`)

The `aps` theme's own header states the standard: body text and code on the dark background exceed
WCAG AA (7:1+). `--aps-fg` `#f2f4f8` sits on `--aps-bg` `#0f1115`, headings use accent `#7dd3fc`, and
`section` is set at `font-size: 30px` with `1.42` line height. Keep it.

- **Minimum font size.** The smallest text is `pre` at `0.66em` and tables at `0.72em` — about **20px
  and 22px** at the 30px base. Never shrink code or tables below that to fit more on a slide; cut
  bullets instead. Hence the 6-bullet, 10-word caps.
- **Never encode meaning in colour alone.** The theme enforces this: `em` renders in warn `#fbbf24` but
  is declared `font-style: normal` so emphasis survives without italics, and proof slides carry both a
  dashed border and a `PROOF ·` text prefix. Write "failing" and "passing" as text; never rely on a
  terminal's colour.
- **Alt text rule.** No external assets are used; diagrams are ASCII or tables. If a presenter adds a
  visual, its alt text carries the takeaway *and* the pointer — e.g. "Table: four SignUpFlow
  instruction files with line counts 79, 177, 143, 119."
- **Print/PDF.** `@media print` flips to white background with `#111318` text, so the handout and an
  exported deck stay readable without colour.

## Code accessibility

- **Line length.** SignUpFlow caps source lines at 100 characters (`SignUpFlow/AGENTS.md`, "Code
  style"). On slides, keep code under ~**72 characters** so nothing wraps at `pre` size.
- **How to read code aloud.** Three passes, always in order: the file pointer, the rule or signature,
  then the command that checks it.
- **Announce every pointer verbally.** A path shown on a slide is invisible to an audio-only student.
  Every proof slide's notes speak the pointer in full, and the video beats do too.

## Transcript structure

- **Chapters keyed to the beats.** Publish the timestamps from `video-scripts.md` as chapters (`0:15
  The four-file stack`, `4:00 House style`, `8:15 Evidence template`) so a student can jump to a
  concept.
- **Speaker labels.** Label narration `Instructor:`; label inserted demo audio separately. Never merge
  narration with on-screen text.
- **Pacing.** Scripts target **~130 words per minute**, about 2.2 words per second. Break caption lines
  at clause boundaries, not at the average. Keep the pause after each number (1,464; 835; 97.24%) as a
  marker; that is where comprehension happens.

## Captions

- **Caption every command verbatim, including flags.** If the narrator says "pytest dash q", the
  caption reads `python3 -m pytest tests/ -q` so a student copying from captions gets a runnable command.
- **Spell out file paths on first use.** Read `SignUpFlow/docs/playbooks/validation.md` as "SignUpFlow
  slash docs slash playbooks slash validation dot md", then say "the validation playbook".
- **Non-English terms and acronyms.** Gloss on first use: YAGNI → "You Aren't Gonna Need It"; SHA →
  "the Git commit hash"; mypy → "the Python type checker". The module adds no non-English prose; if one
  is added, caption original and translation together.

## Accommodations

- **Extended time.** Lab M1 is ~2 hours; provide 1.5× (3 hours) on request. It produces a repo, not a
  timed exam, so no rubric criterion changes.
- **No-audio path.** `handout.md` must suffice alone: mental model, decision table, commands, pointers,
  gotchas, done-when checklist. It adds no claim the lesson does not make, so skipping the videos loses
  no content. Adding teaching to the handout is a bug, not a bonus.
- **Two-outcome equity note.** M1 needs only Python and pytest — no Ollama daemon, no local model, no
  paid API. The "local model vs. only-`:cloud` daemon" split that affects the M2–M3 labs does not apply.
  No student is blocked by hardware, and grading never depends on it.
- **Screen-reader path.** Rubric and checklist tables use real header rows and short cells. Linear
  readers can follow the "You're done when…" checklist in `handout.md`; it maps one-to-one to the lab's
  acceptance checklist.
