# M2 Accessibility, Transcripts & Captions

> Applies to `slides.md`, `video-scripts.md`, `handout.md`, and the lab's terminal recordings. The
> shared theme is `course/06-production/slides/aps.css`; read it beside this file.

## Deck accessibility

- **Contrast.** The `aps` theme's header comment states that body text and code on the dark background
  exceed WCAG AA at 7:1 or better. Keep it that way: do not introduce new colours, and do not put text
  on `--aps-accent` (`#7dd3fc`) or `--aps-warn` (`#fbbf24`) fills.
- **Minimum size.** `section` is 30 px. Code blocks render at `0.66em` (≈20 px), tables at `0.72em`
  (≈21.6 px), pagination at `0.55em`. Treat ~20 px as the floor: shorten a code block rather than
  letting it shrink, and never add font-size overrides.
- **Never encode meaning in colour alone.** The theme enforces this — `em` uses `--aps-warn` *and*
  non-italic styling, and proof slides carry the literal word `PROOF · ` via `section.proof h2::before`.
  If you mark a passing assertion green, also write "pass".
- **Alt text.** The deck uses no images, which is the intent ("the deck must render with no external
  assets"). If you add a diagram, give it a text description in the adjacent bullet or notes; a table
  or ASCII diagram is preferred because it is readable by a screen reader in source order.
- **Notes are not content.** Speaker notes are HTML comments and never render. Anything a student must
  know belongs on the slide or in `handout.md`, not only in `<!-- NOTES: ... -->`.

## Code accessibility

- Keep slide code blocks under ~80 characters per line; long lines force horizontal scrolling in the
  HTML export.
- Read code aloud by structure, not punctuation: "in `recent_context`, walk segments newest-first,
  break when the next line would exceed the budget, but never break before the first segment."
- **Announce every file pointer verbally as well as showing it.** "I am opening
  `Sources/ListenToMeCore/ConversationStore.swift`, lines 56 through 67" — a viewer who cannot see the
  screen still needs the path. Do the same in captions.

## Transcript structure

- Export one transcript per segment, with chapter markers at each segment start and at every demo cue
  in `video-scripts.md`: M2.1 0:00, M2.2 0:00, M2.3 0:00, relative to each recording.
- Label speakers consistently: `HOST:` for narration, `SCREEN:` for on-screen text quoted verbatim,
  `TERMINAL:` for command output. Never merge narration and terminal output into one block.
- The scripts are written for ~130 words per minute. Captions must follow that pace: split narration
  into 1–2-line cues of 32–42 characters per line and re-time if the presenter speeds up. Do not
  auto-summarise; students use transcripts to follow commands.

## Captions

- **Always caption:** every command typed (including flags), every file path, every test count, and
  every error class name (`IncompleteStreamError`, `EmptyResponseError`, `ServerError`).
- **Spell paths out in the caption** even when narration shortens them: say "ConversationStore dot
  swift," caption `ConversationStore.swift`.
- **Non-English terms.** Keep established terms (`Ollama`, `NDJSON`, `VAD`, `:` `cloud`) as written
  and add a short gloss the first time in the caption; for any non-English phrase a student's preset
  might produce, caption the English meaning rather than a transliteration.
- Provide the VTT/SRT file alongside each recording; do not rely on platform auto-captions for
  commands. Terminal output shown but not read aloud still needs a caption if it carries a number the
  student must record.

## Accommodations

- **Extended time.** The lab is advertised at ~3 hours. Allow 2× on request; the gate is the green
  suite, not the clock.
- **No-audio path.** `handout.md` is the complete no-audio substitute: pipeline diagram, decision
  table, commands, pointers, gotchas, and the "you're done when" checklist. A student who cannot
  listen must be able to pass the lab from the handout plus `lab.md` alone.
- **Two valid environments.** A daemon with a genuinely local model (`ollama pull qwen3:0.6b`) and a
  daemon with only `:cloud` aliases are both valid for M2; the cloud-only case runs with
  `make demo --mode cloud` (`02-instructor/instructor-guide.md` §4). No student is blocked by hardware,
  and grading must not privilege the local-model path.
- **Assistive tech in the terminal.** Prefer `pytest -q` summaries over long tracebacks when screen
  readers are in use, and read the `short test summary info` block aloud in recordings.
