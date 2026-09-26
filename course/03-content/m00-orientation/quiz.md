# Quiz M0 — Orientation

> 8 questions · 6 multiple choice + 2 short answer · Answer key at the end with objective refs.

## Questions

### Q1 (M0.1)

Which product archetype is ListenToMe an example of?

- a) The spec-driven AI SaaS
- b) The native on-device AI app
- c) The expertise content product
- d) A cloud AI API wrapper service

### Q2 (M0.1)

What is SignUpFlow's dated-evidence proof asset, as cited in this module?

- a) A green CI badge on every pull request
- b) A testimonial from a church in the README
- c) "1,464 passed, 21 skipped" recorded in `docs/playbooks/validation.md`
- d) Its 96% core-coverage badge

### Q3 (M0.1)

In this course, calling a case study "production-grade" means most nearly:

- a) The repository is public on GitHub
- b) The README says the product is finished
- c) A shipped artifact exists with proof you can open and verify — a dated evidence line, a badge, or a provenance file
- d) The product has paying customers

### Q4 (M0.2)

ListenToMe's 14-row competitor comparison table is an artifact of which Spec-to-Ship Loop stage?

- a) Spec
- b) Build
- c) Study
- d) Prove

### Q5 (M0.2)

Which artifact belongs to the **Prove** stage of the loop?

- a) The signed, notarized release DMG
- b) The gap review that recommends "do not promote the existing 1.3.0 DMG" despite 97.24% coverage
- c) The spec with Given/When/Then acceptance scenarios
- d) The 95% coverage-floor script

### Q6 (M0.3)

Which statement about the course environment is true?

- a) Every lab requires a Mac because the case studies are Swift apps
- b) Core labs run on Python + Ollama on macOS, Linux, and Windows; the Swift stretch track requires a Mac
- c) Local LLM labs require a paid API key
- d) Ollama runs only on macOS

### Q7 (M0.3 — short answer)

A classmate's first-win post reads, in full: "`make setup` worked. `Health score: 100.0/100`." Write the reply you would post: the two commands (after `make setup`) their evidence has to show they ran, the lines of solver output they must paste around the score for it to count as a run record, and whether the post passes Lab M0 as it stands.

### Q8 (M0.1 — short answer)

A friend wants to build: a paid web app that drafts LinkedIn posts from a founder's own articles, where every feature is written as a spec that AI agents implement. Which archetype is it, which case-study repo should they study for the *method*, and in one sentence — why?

## Answer key

### Q1 — b — ListenToMe is a native macOS meeting copilot: on-device transcription plus real-time AI, private and model-optional (`ListenToMe/README.md`). (objective: M0.1 — describe the three archetypes)

### Q2 — c — The dated line "1,464 passed, 21 skipped" lives in `SignUpFlow/docs/playbooks/validation.md`; the 96% badge belongs to ListenToMe. (objective: M0.1 — name each repo's proof asset)

### Q3 — c — A proof asset is a file you can open and verify (badge, dated evidence, provenance, published self-audit); publicity and README claims are not evidence. (objective: M0.1 — define production-grade)

### Q4 — c — The competitor table with sourced, dated claims is Study-stage work — positioning as a research artifact (`ListenToMe/docs/competition-analysis.md`). (objective: M0.2 — map artifacts to loop stages)

### Q5 — b — Prove means honest records of what was and wasn't verified, including a self-review that blocks a release; the DMG is Release, the spec is Spec, the coverage script is Validate. (objective: M0.2 — distinguish Prove from Release/Validate)

### Q6 — b — Core labs are Python 3.11+ with free local Ollama models on all major OSes; only the Swift stretch track needs a Mac (`ListenToMe/README.md`). (objective: M0.3 — know your environment)

### Q7 — Model answer — The two commands are `poetry run python -m api.cli.main init my-church` and `poetry run python -m api.cli.main solve my-church`. The score has to sit inside the block `solve` prints: the workspace header (`Workspace:`, `People: 5`, `Events: 2`, `Mode:`) above it and `Solution saved to my-church/output/solution.json` below it — the score line itself is emitted by `SignUpFlow/api/cli/main.py:193`, and its value depends on the SignUpFlow revision (at the 2026-09-16 head the sample workspace prints `0.0/100` with two hard violations), so a lone `100.0/100` is a warning sign, not proof. As posted it does not pass: a score with no run record is Lab M0 auto-fail 3, and the other half of the pass gate — a non-empty `ollama list` — is missing. (objective: M0.3 — run the solver and capture its health score)

### Q8 — Model answer — Archetype 2 (spec-driven AI SaaS): a multi-user web product whose features are specified for agent implementation — study SignUpFlow, which shows the same spec-kit → tasks → tested-feature method with 17 spec folders and 7 test tiers. (objective: M0.1 — classify products into archetypes)