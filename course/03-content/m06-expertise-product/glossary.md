# Glossary — M6 (The Expertise Product)

## Terms

**Benchmark record** — The unit of citable evidence: one finding plus date, sample, method, unit,
self-reported vs measured, sponsor, and what claim it can support. Anything unverifiable is listed as
such. Lives in `ai_qe/CONTRIBUTING.md`, "Research conventions"; examples in
`ai_qe/docs/evidence/benchmarks.md`.

**Benefits-realization register** — Finance-owned table with one row per capture mechanism: the budget
line, its owner, the earliest date it could change, and the evidence Finance will accept. Lives in
`ai_qe/docs/method/phased-pilot.md`.

**Claim level** — One of four labels that every number must carry: task-level efficiency, QA capacity
released, hard-dollar saving, total software-spend impact. Lives in `ai_qe/docs/principles.md`;
reproduced in `evidence-dataset.md`.

**Content as code** — Running published content under the same discipline as software: tests, review
gates, hashed media, editions and immutable releases. Lives in `ai_qe/Makefile` and
`ai_qe/CONTRIBUTING.md`, "Release validation".

**Edition** — A named version of one content surface, tracked separately from the site version.
Lives in `ai_qe/_data/release.yml` (`version`, `slide_edition`, `fintech_edition`,
`questionnaire_edition`, `research_edition`).

**Epistemic label** — The status of a number: measured / self-reported / vendor-affiliated /
illustrative. Lives on the slide itself, per the wording rules in
`ai_qe/docs/economics/slide-language.md`.

**Financial-capture set** — The questionnaire questions the failed form omitted: budget ownership,
variable share of spend, renewal windows, what happens to released capacity, and what Finance will
recognise as a saving. Lives in `ai_qe/docs/method/discovery-questionnaire.md`.

**Go/no-go gate** — A sponsor-signed decision boundary with a cost ceiling, a stop rule and frozen
criteria. Lives in `ai_qe/docs/method/phased-pilot.md`; the exact numbers live in
`ai_qe/_data/pilot_gates.json`.

**Guided route** — A curated sequence over stable slide IDs, with a declared `closing` slide, that
reorders and omits but never rewrites. Lives in `ai_qe/_data/briefing_routes.json`.

**Immutable release** — A published edition that is never overwritten; a new one is cut instead.
Lives in `ai_qe/CONTRIBUTING.md` and `ai_qe/releases.md`.

**Not-verified list** — Explicit published list of claims that could not be confirmed, kept alongside
the verified ones. Lives in `ai_qe/docs/research-log.md`.

**Provenance manifest** — Record of every retrieval with URL, retrieval date, status and SHA-256 hash
— including failures. Lives in `ai_qe/research/document-manifest.json`; images in
`ai_qe/research/visual-provenance.md`; voice in `ai_qe/assets/data/narration-provenance.json`.

**Research log** — The dated intake queue where a claim enters before it can reach a page: Question /
Checked / Outcome / Changed. Lives in `ai_qe/docs/research-log.md`.

**Signature qualifier** — The one sentence that labels the whole product: "Planning inputs and proposed
outcomes are not observed client results." Lives in `ai_qe/README.md`.

**Stable slide ID** — The invariant slide number that routes and shared links resolve against, so a
route can reorder without breaking a link. Lives in `ai_qe/_data/briefing_room.json` outlines.

**Sufficient evidence** — A result whose confidence interval does not cross the relevant decision
boundary. A point estimate alone is never sufficient; lives in `ai_qe/docs/method/phased-pilot.md`.

## Terms people get wrong

- **Released capacity vs. hard-dollar saving** — Freed hours are productivity until Finance names the
  budget line the spend is actually removed from; "a capacity result with no capture row is reported
  as productivity, not cash saving" (`ai_qe/docs/method/phased-pilot.md`).
- **Self-reported vs. measured** — "Organizations report 10–15% gains" is a perception figure from a
  consultancy; a measured figure has a method and an instrument, and the record says which
  (`ai_qe/docs/evidence/benchmarks.md`).
- **Site version vs. content edition** — A player-only patch advances `version` while deliberately
  retaining `slide_edition`; bumping all fields together destroys the client's ability to know what
  they hold (`ai_qe/releases.md`).
- **Not verified vs. false** — "Not verified" means a claim was sought and could not be confirmed; it
  is an honest open entry, not an accusation (`ai_qe/docs/research-log.md`).
- **Curated route vs. rewritten deck** — A route reorders and omits over stable IDs; rewording slides
  for an audience forks the content and breaks every shared link (`ai_qe/_data/briefing_routes.json`).

## Curated resources

- `ai_qe/CONTRIBUTING.md`, "Research conventions" — the seven required fields and the
  log-then-page pipeline, in the repo's own words.
- `ai_qe/docs/evidence/benchmarks.md` — read the METR and Peng records back to back; the contrast is
  the whole lesson on sponsorship and limits.
- `ai_qe/docs/principles.md` — the four levels of saving, quoted exactly, with the "who can confirm
  it" column that stops most mixing errors.
- `ai_qe/docs/method/discovery-questionnaire.md` — the post-mortem of the 29-question, 186-option
  predecessor form; the best single page on designing a qualification funnel.
- `ai_qe/docs/method/phased-pilot.md` — five phases, cost guardrails, frozen criteria and the
  ordered decision table; read beside `_data/pilot_gates.json`.
- `ai_qe/releases.md` — two adjacent changelog entries showing an edition deliberately retained.
- `course/03-content/m06-expertise-product/evidence-dataset.md` — the lab's starter claims with
  levels and epistemic status already applied.
