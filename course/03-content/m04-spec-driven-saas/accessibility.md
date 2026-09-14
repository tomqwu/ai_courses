# M4 — Accessibility, Transcripts & Captions

> Applies to `slides.md`, `video-scripts.md`, and `handout.md` in this module. The deck theme is shared:
> `course/06-production/slides/aps.css`.

## Deck accessibility

- **Contrast.** The `aps` theme states its own budget: "body text and code on dark background exceed WCAG
  AA (7:1+)" (`06-production/slides/aps.css:3`). Never restyle a slide to a lighter accent than
  `--aps-accent` (`#7dd3fc`) on `--aps-bg` (`#0f1115`); if you edit the theme, re-check contrast before
  rendering.
- **Minimum size.** Body text is 30px and code blocks 0.82em of that, roughly 25px
  (`06-production/slides/aps.css:22`, `:71`). Do not add per-slide font overrides; if a slide doesn't fit
  at theme size, cut bullets rather than shrink type.
- **Never encode meaning in colour alone.** The theme says it outright: "Meaning is never encoded in
  colour alone; every accent also carries a label" (`06-production/slides/aps.css:4`). In this module that
  matters for the pass/fail idea — write "PASS" or "FAIL" next to any colour, and do not let the drift
  cases appear only as red text.
- **Alt text.** The deck references no images, which is the rule here: if you add a visual (a screenshot of
  `checklists/requirements.md`, say), it needs alt text in the Markdown image tag, and the same information
  must also exist as text on the slide. ASCII and tables are preferred for this reason — the pipeline
  diagram is ASCII.

## Code accessibility

- **Line length.** Keep code and fenced blocks under ~80 characters. The long pointers are the hazard:
  `specs/014-security-hardening/checklists/requirements.md` will wrap. Put it on its own line, never inside
  a sentence.
- **Reading code aloud.** Read the *decision*, not the punctuation: "the config table's first row sets a
  five-minute window, five attempts, per IP, fifteen-minute lockout." Announce operators when they carry
  meaning ("grep…piped to xargs ls"). Never spell out braces.
- **Pointers must be spoken as well as shown.** Every pointer that appears on screen — `specs/014-…`,
  `AGENTS.md`, `.specify/templates/tasks-template.md` — is also said aloud in the narration. A listener
  without the slide needs the same evidence a viewer gets; this is why `video-scripts.md` puts pointers in
  the "on screen" column and repeats them in the spoken beat.

## Transcript structure

- **Chapter markers** keyed to the segment beats. Use the beat timestamps already in `video-scripts.md`
  (`0:15`, `0:45`, `1:20`, …) as chapter titles, one per beat, named for what is on screen.
- **Speaker labels.** One speaker per segment; label consistently (`SPEAKER:`) so captions auto-align. Mark
  non-speech events in brackets: `[types command]`, `[opens file]`.
- **Pacing.** Scripts assume ~130 words/min (`video-scripts.md` header), which leaves caption reading time.
  Do not tighten that pace in editing; if a segment must shrink, cut a beat, not the pauses.

## Captions

- **Caption everything spoken**, including commands typed on screen: a caption carries what was said; a
  code block does not. Caption read-aloud commands verbatim.
- **Spell out paths and identifiers** in the caption track rather than relying on visual proximity:
  "specs/zero-one-four-security-hardening". Same for `AGENTS.md`, `tstzrange`, `alembic`, `idempotent`.
- **Non-English terms.** Reproduce the original and give the English in the caption on first use; for this
  module that covers i18n (`specs/012-i18n-system`), "Ralph loop", and any student's domain vocabulary. If
  a term is a code identifier, keep the identifier's exact casing in captions and speech.

## Accommodations

- **Extended time.** Lab M4 is estimated at 90–120 minutes; grant 1.5× without discussion. The stranger
  test is the slowest step and the pass gate — never compress it to fit the clock.
- **No-audio path.** `handout.md` is designed to stand alone: mental model, pipeline diagram, commands,
  pointer list, gotchas, and the "you're done when…" checklist. A student who cannot use audio must be able
  to complete Lab M4 from the handout plus the lesson text. Test that claim before publishing: read the
  handout without the deck and name one thing it fails to convey.
- **Equity note — no hardware blocks this lab.** M4 needs no model and no GPU. If a student's environment
  only exposes `:cloud` Ollama aliases (the M2/M3 situation in
  `02-instructor/instructor-guide.md:41`), the stranger test can be run by a peer instead of an agent
  session, and that peer transcript is equally valid evidence. Both are legitimate passes; state this at
  the start so no student self-selects out.
