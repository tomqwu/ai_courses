# Accessibility — M6 (The Expertise Product)

> Applies to `slides.md`, `video-scripts.md`, `handout.md` and the Lab M6 artifacts. The goal: a
> student who cannot see the screen, cannot hear the audio, or reads at a different pace still reaches
> the same capabilities and the same lab pass gate.

## Deck accessibility (`06-production/slides/aps.css`)

The theme's header states the standard: body text and code on the dark background exceed WCAG AA
(7:1+). `--aps-fg` `#f2f4f8` on `--aps-bg` `#0f1115`, headings in accent `#7dd3fc`, `section` at
`font-size: 30px` with `1.42` line height.
- **Minimum font size.** The smallest text is `pre` at `0.66em` and tables at `0.72em` — about 20px
  and 22px at the base. Never shrink code or tables to fit; cut bullets. The deck caps at 6 bullets
  and 10 words each for that reason.
- **Never encode meaning in colour alone.** The theme already enforces two cases: `em` renders in warn
  `#fbbf24` but is declared `font-style: normal`, and proof slides carry a dashed border *and* a
  `PROOF ·` text prefix. Every epistemic label — *measured*, *self-reported*, *vendor-affiliated*,
  *illustrative* — is written as text in this module, never implied by colour.
- **Alt-text rule.** The deck needs no external assets; diagrams are tables. Any added visual needs
  alt text carrying the takeaway and the pointer, not the word "diagram" — e.g. "Table: four decks,
  slide counts 21, 33, 26, 36, totalling 116 narrated slides."

## Code accessibility

- **Line length.** Keep command lines under roughly 72 characters so nothing wraps at the `pre` size;
  every code block here is ≤10 lines.
- **How to read code aloud.** Three passes, in order: the file pointer, the rule or value, then the
  command that checks it. Never read a path and a flag in the same breath.
- **Announce every pointer verbally.** A path on a slide is invisible to an audio-only student. Every
  proof slide's notes speak its pointer in full — "ai_qe slash docs slash evidence slash benchmarks
  dot md" the first time.

## Transcript structure

- **Chapter markers keyed to the segment beats.** Publish the `video-scripts.md` timestamps as
  chapters (`0:15 Research conventions`, `2:45 The not-verified list`, `4:15 Four levels of saving`).
- **Speaker labels.** Single presenter: label every line `Instructor:` and label inserted demo audio
  separately. Never merge narration with on-screen text.
- **Pacing.** Scripts target ~130 words per minute; caption lines break at clause boundaries, not at
  the average. Keep the pause after each number (19%, 55.8%, 116, 30 tasks) — comprehension happens
  there.

## Captions

- **Caption every command read aloud, verbatim, including flags.** Spoken "grep case-insensitive for
  not verified" captions as `grep -ciE 'not verified' docs/research-log.md`.
- **Spell out file paths on first use**, then shorten: `ai_qe/research/document-manifest.json` becomes
  "the document manifest" afterwards.
- **Acronyms and non-English terms.** Gloss on first use: QE → "quality engineering"; RCT →
  "randomized controlled trial"; SHA → "a cryptographic file hash"; CI → in M6.1 say "confidence
  interval" in full, because the module also prints CI/CD elsewhere. If a presenter quotes
  `ai_qe/maintainers/narration.md` on rejected voice candidates, caption the term and its translation
  together, never the untranslated term alone.

## Accommodations

- **Extended time.** Lab M6 is estimated at ~2.5 hours; provide 1.5× (about 3.75 hours) on request.
  The deliverable is documents, not a timed exam, so an extension changes no rubric row.
- **No-audio path.** `handout.md` must suffice on its own: mental model, level-decision table,
  templates, pointers, gotchas, done-when checklist. It introduces no claim the lesson does not make,
  so a deaf or hard-of-hearing student loses nothing by skipping the videos.
- **No-hardware note (equity).** Unlike the M2–M3 labs, Lab M6 needs no Ollama daemon, no local model
  and no paid API: the default dataset is in `evidence-dataset.md` and every source record is in the
  clone. Say this out loud — no student is blocked by hardware here. If a student's own source fails
  to fetch, record it in the manifest style of `ai_qe/research/document-manifest.json`
  (`status: unavailable` plus the reason); the acceptance checklist still passes.
- **Screen-reader path.** Rubric and checklist tables use real header rows and short cells. Students
  who prefer linear reading follow the "You're done when…" checklist in `handout.md`, which maps
  one-to-one to the lab's acceptance checklist.
