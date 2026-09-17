# Changelog

The course is versioned as dated editions, the way its third case study versions its content: an
edition names what a buyer received, and what changed since. Every line here corresponds to
commits on the branch; the gate (`make -C course check`) ran green before each edition was cut.

## v2026.09 — 2026-09-17 (current)

**Verified against** the case-study repositories at their 2026-09-16 heads: ListenToMe `a9bde8e`,
SignUpFlow `c550d46`, ai_qe `6388f0a`. `make -C course facts` re-derives every pinned number from
those clones; this edition pins 17 facts and all re-derive.

### Added
- The learner site carries the course text, not only the decks: lesson, handout and glossary
  pages per module with every repo pointer linked at the pinned commit; a merged master glossary;
  interactive knowledge checks (72 questions) with instant feedback and objective references;
  lab pages with persisted acceptance checklists and an evidence-entry export; search across
  every unit, slide, heading and term; progress that survives a reload, with export and import.
- The course home leads with what the build measured about itself: pointers resolved, facts
  re-derived, the lab starters' verified runs, and the narration contract.
- `06-production/check_facts.py` and `facts.json`: the pinned numbers re-derived from the clones,
  advisory by default and `--strict` in the gate.
- `verify.py` checks `:N-M` line ranges in every pointer, not only the path.
- Lab M3 starts from a real red: `make m3-start` parks the shipped solution.
- A devcontainer so every lab opens in Codespaces with Ollama and the three repos cloned.
- The September 2026 platform review and five research documents (`course/00-research/04`–`09`).

### Changed
- Five pinned facts re-verified and corrected across the course (competitor table 14 rows,
  `AGENTS.md` 188 lines, constitution 85, CLAUDE.md 154, Copilot file 127); the ListenToMe 1.3.0
  gap review is told as a dated record now that 1.4.x has shipped.
- Labs M1 and M2 record the red run the tooling actually produces.
- Quiz hygiene: one keyed answer per item, one objective per key, `Quiz M#` titles, 72 questions.
- The M0 first win is stated once, honestly, with the TinyCopilot suite moved to stretch.
- Lab M5 ships the `mini-flow` starter the curriculum promised.
- Every M3 pointer into `OllamaProvider.swift` points at the code it describes.

### Update window
Buyers of this edition receive every edition published through **September 2027**. Editions are
cut when the gate is green; the date on this page is the date a buyer can hold the course to.

## v2026.08 — the first complete package

Nine modules with eleven artifacts each, three track bundles, the sales package, the narrated
learner site with committed transcripts, and the verification gate. Recorded in
`course/06-production/MILESTONES.md` (Milestones 1–4).
