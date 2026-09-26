# Accessibility — M9: Ship a Product Catalog with GitHub Pages

> How this module works for learners who use a screen reader, the keyboard only, magnification, or
> captions, and what the catalog they publish does for their own visitors.

## The terminal

- **Screen readers.** Windows Terminal and PowerShell work with Narrator and NVDA; the Mac Terminal
  works with VoiceOver. Every command's result in this module is short, text-only output with no
  drawn boxes or colour-only meaning, so it reads line by line.
- **The setup check does not rely on colour.** Each result starts with the word PASS or FAIL, and the
  summary is a sentence — "4 of 4 checks passed" — so the outcome is spoken, not just shown green.
  Colour is added only when the output is a real terminal, and never carries meaning on its own.
- **Keyboard only.** Everything in the module except the GitHub settings page is typed. On that page,
  Settings, Pages, the Source menu, the branch and folder menus and Save are all reachable with Tab and
  Enter.
- **Magnification.** Both terminals zoom with Ctrl and plus on Windows, and Cmd and plus on a Mac. Long
  commands in the lab are written so they can be pasted rather than retyped.

## Captions

- **Caption commands exactly as typed**, flags included: `winget install --id GitHub.cli --source winget`
  must not be auto-corrected. The narration says "win get" and "G H"; the captions show `winget` and
  `gh`, which is what the learner types.
- **Spell out symbols in speech, not in captions.** The narration says "C D dot dot" and "tilde"; the
  captions show `cd ..` and `~`.
- **Numbers**: caption what is shown. The published-site limit is spoken "one gigabyte" and captioned
  `1 GB`.

## The catalog the learner publishes

The starter was checked in a headless browser at phone and desktop widths, in light and dark mode,
and passes WCAG AA text contrast throughout (`catalog-starter/README.md`). Beyond contrast:

- **A skip link** jumps past the header straight to the products.
- **Category filters are real buttons** with `aria-pressed`, so a screen reader announces which one is
  on.
- **The result count is a live region**: "2 of 6 products" is announced after a filter or a search,
  and so is the empty state.
- **Search and sort have visible labels**, not placeholder-only fields.
- **Coloured tiles are decorative** and hidden from screen readers; a real product photo carries
  `imageAlt`, which learners should fill in whenever they add `image`.
- **Every action link names its product** — "Buy Everyday Mug", not a row of identical "Buy" links.
- **Focus is always visible**, with a 3-pixel outline in both themes.

Ask learners to keep these when they change the starter. The two changes that most often break them are
removing the skip link and adding photos without `imageAlt`.

## Extended time and alternatives

- **Installs are the variable.** Lab M9 is 60–90 minutes, most of it downloads. Give extended time on
  Steps 0–1 without penalty, and let learners run the installs before a live session.
- **Managed computers.** Where an employer's policy blocks installs, a learner can complete Steps 4–8
  in a GitHub Codespace from the repository's green Code button, which provides a terminal with Git and
  the GitHub CLI already present. Record which path was used in the evidence file.
- **No-audio path.** `handout.md` is enough to finish the lab without the narration: every command,
  the publishing steps, the limits and the common failures are on it.
