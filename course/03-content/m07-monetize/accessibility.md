# Accessibility — M7: Monetize: Pricing, Packaging, Positioning

> Applies to the M7 deck (`slides.md`), scripts (`video-scripts.md`), facilitation
> (`facilitation.md`), and every student artifact the module asks for. The deck must be usable with
> screen reader, keyboard, no audio, and print.

## Deck accessibility

- **Contrast.** The shared `aps` theme (`course/06-production/slides/aps.css`) sets body text
  `#f2f4f8` on `#0f1115` and code `#e6edf7` on `#1b1f27`; its header states body text and code exceed
  WCAG AA (7:1+). Do not override these colours in M7 slides. In print, the theme switches to
  `#111318` on `#ffffff` with headings `#0b5f8a` — verify any exported PDF opens in that light state.
- **Minimum size.** Body is 30px; slide tables render at 0.72em (~21.6px) and code blocks at 0.66em
  (~19.8px). Keep the M7 comparison table to the four rows in `slides.md`; do not shrink tables below
  ~20px.
- **Never encode meaning in colour alone.** The theme's own rule: every accent also carries a label.
  M7's evidence slides use `<!-- _class: proof -->`, which renders a dashed border *and* the word
  "PROOF ·" before the title. A red/green price comparison is not acceptable; write "above the floor"
  / "below the floor."
- **Alt text.** The deck uses no images and renders with no external assets. If you add a diagram,
  give it alt text and restate its meaning in a bullet; alt text never replaces the spoken explanation.
- **Text-only diagrams.** The clause→column mapping and the funnel are tables, which read correctly in
  linear order. Keep that pattern; do not replace either with an arrow graphic.

## Code and pointer accessibility

- **Line length.** Keep code blocks ≤10 lines; never wrap a `grep` command, because screen readers
  insert pauses that change meaning.
- **Read code aloud, don't point at it.** Every command spoken in a script is also written in the
  narration column, flags spelled out character by character.
- **Announce every pointer.** Whenever a file is shown, say it as well: "SignUpFlow, README dot M D,
  Provider-backed Features." Students listening without the screen must be able to open the same file.

## Transcript structure

- **Chapter markers keyed to beats.** Each transcript carries the beats table's timestamps as
  chapters — `00:00 Cold open`, `01:30 Cloud costs`, `06:30 Type 2 gating`, `11:15 Action step`
  (M7.1), and the equivalent rows for M7.2 and M7.3.
- **Speaker labels.** One label, `INSTRUCTOR:`, throughout; any on-screen quote is labelled
  `ON SCREEN (quoted):` so a reader can tell narration from quoted repo text.
- **Pacing.** Scripts target ~130 words/minute. For captions, that yields roughly 12–16 words per
  caption line; break long numbers into their own caption so "one hundred forty-nine dollars a month"
  is not split across a cue.

## Captions

- **Commands and flags always captioned**, never auto-generated only: `BILLING_ENABLED=false`,
  `SMS_ENABLED=false`, `grep -c 'reportedly\|approximately'`.
- **File paths spelled out** in the caption text exactly as they appear on disk, including the
  hyphenated folder names (`course/04-sales/pricing-and-platforms.md`).
- **Non-English terms.** Read currencies in both forms — "approximately fifty-nine euros, roughly
  sixty-nine US dollars" — and gloss any non-English term in the same caption.
- **Numbers with qualifiers** keep the qualifier: caption "reportedly" and "approximately" as spoken.

## Accommodations

- **Extended time.** Lab M7 is ~2 hours; allow 3 hours where a student must retrieve prices from
  primary sources or write in a second language. The stretch items are never required.
- **No-audio path.** `handout.md` must be sufficient on its own: mental model, decision table,
  worksheet template, pointers, gotchas, and the "you're done when" checklist. A student who cannot
  watch any video can complete Lab M7 from the handout plus `lesson.md` and `lab.md`.
- **Two-outcome labs as an equity note.** In M2/M3, an Ollama daemon with only `:cloud` aliases is a
  valid environment, and so is one with a local model pulled; no student is blocked by hardware. In
  M7 the equivalent is product ownership: a student with no shipped product of their own may price a
  case-study product instead (the instructor guide's default option for M4 — extend SignUpFlow itself),
  and the rubric grades the evidence, not the choice of subject.
- **Print.** The handout prints on one page, and `aps.css` yields legible light-mode PDFs.
