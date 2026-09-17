# M0 — Accessibility, Transcripts & Captions

> Applies to the M0 deck, recordings, and lab. Theme rules are grounded in
> `course/06-production/slides/aps.css`.

## Deck accessibility

- **Contrast.** The `aps` theme comment states body text and code exceed WCAG AA (7:1+) on the dark
  background: foreground `#f2f4f8` on `#0f1115`, accents `#7dd3fc`, `#fbbf24`, `#86efac` (`course/06-production/slides/aps.css`).
  Do not add new text colours; if you must, verify 4.5:1 minimum on dark.
- **Minimum size.** `section` sets a 30px body, `h2` 40px; keep bullets at body size. Code blocks
  render at `0.66em` (≈20px) and tables at `0.72em` (≈21.6px). When a code block is the teaching,
  enlarge or split it rather than showing 20px text to a room.
- **Meaning never in colour alone.** `em` is normal-style with a colour change; proof slides carry a
  `PROOF ·` text label and a dashed border, not just an accent (`course/06-production/slides/aps.css`, `section.proof`). Keep the
  word "Proof" in the heading.
- **Alt text.** M0's deck uses no images by design. If you add one, its alt text must describe the
  *claim*, not the pixels, and the same information must exist as text or in a speaker note. The deck
  must render with no external assets, so prefer text.
- **Print/PDF.** `@media print` flips to white background with dark text; check new accents, since
  light ones fail on white.

## Code accessibility

- **Line length.** SignUpFlow's house style is a 100-character maximum (`SignUpFlow/AGENTS.md`, "Code
  style"). Keep slide code blocks under ~60 characters per line so they never wrap.
- **Read code aloud.** Never say "as you can see here". Name the file, the symbol, and the value: "in
  `SignUpFlow/Makefile`, the `check-python` target fails below 3.11 or above 3.13." A listener without
  the slide must be able to reconstruct the fact.
- **Announce every pointer verbally.** A pointer that is only on screen is invisible to a listening
  student. Speak it in full: "SignUpFlow, docs, playbooks, validation dot md." Spelling beats an
  acronym the listener cannot expand.

## Transcript structure

- **Chapter markers keyed to the beats.** Open each segment's transcript with its code and title
  (`M0.1 — Why three types, and why these`), then one chapter per row of that segment's beats table in
  `course/03-content/m00-orientation/video-scripts.md`. Match the beat's "on screen" cell so a student can jump to the file being opened.
- **Speaker labels.** One presenter in M0: label lines `Instructor:`. A guest uses their name, never
  "Speaker 2".
- **Pacing.** Narration targets ~130 words per minute. Keep caption blocks to 1–2 lines, ~32
  characters, and never split a command across blocks without repeating the prompt symbol.

## Captions

- **Command lines:** caption the command exactly as typed, flags included. Do not auto-correct
  `poetry run python -m api.cli.main solve my-church` — the module is teaching that string.
- **File paths:** spell them out in captions rather than "this file", matching the spoken form above.
- **Numbers:** caption what is spoken and what is printed. The health score is spoken "zero out of
  one hundred with two hard violations" and captioned `Health score: 0.0/100` — the value the pinned
  SignUpFlow head prints for the sample workspace; if the recording shows a different revision, caption
  what that run printed. Same for `191 passed` and coverage `100%` in the stretch block.
- **Non-English terms:** this module has none in speech. For a future term, caption the original, add
  a parenthetical translation, and pronounce both.

## Accommodations

- **Extended time.** Lab M0 is about 30 minutes including downloads. Give extended time again, and let
  downloads start before the session — nothing depends on cloning live.
- **No-audio path.** `course/03-content/m00-orientation/handout.md` must suffice alone: mental model, pointer list, commands, stable
  output values, gotchas. A student who never plays the audio can finish Lab M0 from it plus
  `course/03-content/m00-orientation/lesson.md` and `course/03-content/m00-orientation/lab.md`.
- **Hardware equity — the two-outcome lab.** The lab accepts a genuinely local model or a daemon with
  only `:cloud` aliases (`course/03-content/m00-orientation/lab.md` step 3; content-standards §0.5). No student is blocked by machine
  specs, disk space, or bandwidth. The slide *"Two valid environments"* states it and
  `course/03-content/m00-orientation/facilitation.md` repeats it — say it aloud too, or cloud-only students assume they failed setup.
- **Low-bandwidth option.** The three clones are the largest downloads. On a metered connection, read
  the READMEs on GitHub instead and still complete the quiz; note in the evidence log that M2 needs
  the local copy.
