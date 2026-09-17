# Accessibility — M8: Launch: Sales Page, Email Arc, Capstone

> Applies to the M8 deck, the three recordings, the lab, and the capstone demo. Theme:
> `06-production/slides/aps.css`. Structure: `03-content/m08-launch-capstone/video-scripts.md`.

## Deck accessibility

- **Contrast.** The `aps` theme sets body text `#f2f4f8` on `#0f1115` and code `#e6edf7` on `#1b1f27`;
  per the theme's header comment, both exceed WCAG AA (7:1+). The print block inverts to dark on white,
  so exported PDFs stay legible.
- **Minimum size.** Section text renders at 30px; code blocks at 0.66em (≈20px) and tables at 0.72em
  (≈22px). Nothing smaller ships. If a table will not fit, split the slide.
- **Alt text.** The deck carries no images by design (`01-design/content-standards.md` §2.1: it must render with
  no external assets), so no slide depends on alt text. Any added image needs a one-line alt description
  stating its point, not its filename.
- **Never colour alone.** The `proof` class marks an evidence slide with a dashed border *and* the word
  `PROOF ·` rendered before the heading; the accent colour is decoration, not the message. Do not
  introduce a slide where "green means pass" or "amber means caution" with no label.

## Code accessibility

- Keep code lines short enough to read without horizontal scrolling at presentation size; if a command
  wraps, break it deliberately at a flag boundary.
- Read code aloud in units: name the file, say what the test asserts, then read only the lines that
  carry the point. Never read a stack trace line by line.
- Announce every file pointer verbally as well as showing it — "open `SignUpFlow/docs/playbooks/validation.md`
  in the playbooks folder" — because a path on screen is inaccessible to a listener.
- The capstone's `git log` walkthrough should be narrated as a sequence: "this commit adds only a failing
  test; the next one makes it pass."

## Transcript structure

- **Chapters.** One chapter per beat row in `03-content/m08-launch-capstone/video-scripts.md`, using the timestamps in that table
  (for example M8.2's 0:00 timeline, 0:30 seven-email table, 2:10 deadline, 2:50 revenue model).
- **Speaker labels.** `[INSTRUCTOR]` for narration; `[SCREEN]` for a command that is typed on camera;
  `[DEMO]` for silent screen work, with a short description of what changed.
- **Pacing.** Narration is budgeted at ~130 words/min. Captions should preserve that rate rather than
  compressing; a 5-minute segment is roughly 520 spoken words plus demonstration time, so silence during
  demos must be described, not left blank.

## Captions

- Caption anything read aloud that a viewer might need to reproduce: every command, every flag, every
  file path. Spell paths out in the caption (`SignUpFlow/docs/playbooks/validation.md`), never "the
  playbooks file."
- Caption subject lines exactly as they appear, including punctuation; one idea per email hangs on
  exact wording.
- Non-English terms and product names: caption the spelling once, in the form used on screen, and use the
  same spelling in the transcript and glossary.
- Numbers read aloud get digits in the caption: "201 passed", "42 to 55 percent", "$8,767" — viewers
  compare these against their own runs.

## Accommodations

- **Extended time.** Lab M8 is budgeted at 6–10 hours over one to two weeks; permit up to double that, and
  in the cohort let demo day be recorded rather than live on request.
- **No-audio path.** `03-content/m08-launch-capstone/handout.md` must stand alone: mental model, decision
  tables, the seven keepers, pointers, and the completion checklist. A student who cannot hear the videos
  should reach the same capstone by reading the lesson, the lab, and the handout.
- **No student is blocked by hardware.** The capstone has a valid path per archetype: Type 1 and Type 2
  run against a local model *or* a daemon exposing only `:cloud` aliases (the M2/M3 two-outcome rule —
  both are valid, and the fail-closed tests are the point either way), and Type 3 needs only a static
  host. If a student's only environment is a `:cloud` daemon, grade the discipline artifact against the
  red-team path and record the environment in the evidence log rather than treating it as a gap.
- **Quiet participation.** The demo-day post and peer scoring can be written rather than spoken; the
  discussion prompt in `03-content/m08-launch-capstone/lesson.md` is the async equivalent of the live close.
