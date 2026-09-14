# Accessibility M5 — Multi-Tenant Security & the Acceptance Gate

> Applies to `slides.md`, `video-scripts.md`, `handout.md`, and the Lab M5 artifacts. The goal: a
> student who cannot see the screen, cannot hear the audio, or reads at a different pace still reaches
> the four lab steps and the same pass gate.

## Deck accessibility (`06-production/slides/aps.css`)

The `aps` tokens — `--aps-bg: #0f1115`, `--aps-fg: #f2f4f8`, accent `#7dd3fc`, warn `#fbbf24`
(`aps.css:9-13`) — exceed WCAG AA on the dark background; `section` uses `font-size: 30px`,
`line-height: 1.42` (`aps.css:22-23`).

- **Minimum font size.** The smallest text is `pre` at `0.66em` (`aps.css:81`) and tables at `0.72em`
  (`aps.css:93`) — about **20px and 22px** at the 30px base. Never shrink either to fit more content;
  cut bullets. The 6-bullet, 10-word cap exists for that reason.
- **Never encode meaning in colour alone.** The theme already does this: `em` renders in warn
  `#fbbf24` but declares `font-style: normal` (`aps.css:60`) so emphasis survives without italics, and
  proof slides use a 2px dashed accent border (`aps.css:120`). In this module, every red/green
  reference is also text: say "the red run" and "the green run", never rely on terminal colour. The
  status-code table is a table, not a colour legend.
- **Alt-text rule.** The deck renders with no external assets; diagrams are ASCII or tables — the rule
  → mechanism → contract ladder in `handout.md` is a `text` block, announced as "a five-row ladder:
  rule, mechanism, contract, check, evidence." Any added visual needs alt text carrying the takeaway
  and a pointer, not the word "diagram".
- **Print/PDF.** `@media print` (`aps.css:148`) flips to a light background: the exported deck and
  handout stay readable without colour.

## Code accessibility

- **Line length.** SignUpFlow's house style caps source lines at 100 characters (`SignUpFlow/AGENTS.md`,
  "Code style"). On slides, keep code under roughly **72 characters** so nothing wraps at `pre` size.
  Every block in this module is ≤10 lines.
- **How to read code aloud.** Three passes, always in order: (1) the file pointer, (2) the rule or
  signature, (3) the command that checks it. Example: "In `SignUpFlow/api/dependencies.py:61-66`,
  `get_person_in_actor_org` filters by person id **and** the actor's org. The check is `404`."
- **Announce every pointer verbally.** A path on a slide is invisible to an audio-only student. Say
  the full path, then the section: "`api/route_auth_policy.py`, the `ROUTE_AUTH_POLICY` dict." Never
  say "the file we looked at earlier."

## Transcript structure

- **Chapter markers keyed to the beats.** One chapter per segment (`M5.1`, `M5.2`, `M5.3`), with
  sub-chapters at each beats-table row: `M5.1 · 06:00 · the four status codes`. The timestamps in
  `video-scripts.md` are the chapter keys.
- **Speaker labels.** Single presenter: `[INSTRUCTOR]`; a terminal response read aloud is
  `[TERMINAL]`, verbatim — never paraphrase a failure message.
- **Pacing for captions.** Scripts are budgeted at ~130 wpm; keep transcript lines short and never
  split a file path across a caption break.

## Captions

- Caption **every command read aloud**, character-exact, including `poetry run pytest tests/api
  --collect-only -q` and `grep -rn "db.query(" app/ | grep -v org_id`.
- Caption **file paths spelled out**, not just shown: "`tests/playbooks/coverage.py`, line nineteen."
- Status codes are words: caption "four oh four", not "404".
- **Non-English terms.** None appear here. The rule stands: caption a non-English term in its original
  script with an English gloss in parentheses; never transliterate silently.

## Accommodations

- **Extended time.** Lab M5's four steps are independent: submit 1–2 and carry 3–4 to the next week —
  the pass gate is per-row (`lab-rubrics.md`).
- **No-audio path.** `handout.md` plus `solutions.md` are sufficient to complete the lab; no command,
  pointer, or negative-path case exists only in the audio. `slides.md` notes are not required reading.
- **Hardware equity.** Lab M5 needs Python 3.11+, FastAPI, SQLAlchemy, Pydantic 2, pytest and httpx —
  no GPU, no Ollama daemon, no external network. Students who hit the two-outcome hardware split in
  M2/M3 (a local model vs. a daemon with only `:cloud` aliases) are fully unblocked here. The
  two-tenant Playwright stretch goal is optional; the API-level isolation proof satisfies every
  graded row.
- **Screen-reader path.** Terminal output is the primary artifact: copy pytest summaries and JSON
  fixtures into the evidence log as text, not screenshots — that also satisfies "commands + counts".
