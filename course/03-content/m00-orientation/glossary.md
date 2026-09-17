# M0 Glossary — Orientation

> Terms are alphabetical. "Where it lives" is a file you can open; if a pointer stops resolving, tell
> the instructor rather than paraphrasing from memory.

**Archetype** — One of the three product shapes this course builds: on-device app, spec-driven SaaS,
expertise product. They differ in technical center of gravity, not in method. — `course/03-content/m00-orientation/lesson.md`

**Case study** — One of the three public repos used as worked examples throughout the course:
ListenToMe, SignUpFlow, AI × QE. — `course/01-design/curriculum.md`

**`:cloud` alias** — An Ollama model name ending in `:cloud` that is backed by a hosted service rather
than weights on your disk. Its presence means the daemon can reach a cloud model; it says nothing
about where your text is processed. — `course/03-content/m02-ondevice-app/tinycopilot/README.md`

**Coverage floor** — A minimum test-coverage percentage that fails the run when missed. ListenToMe
enforces 95% by script; TinyCopilot enforces 90% via `--cov-fail-under`. — `ListenToMe/README.md`;
`course/03-content/m02-ondevice-app/tinycopilot/Makefile`

**Edition** — A versioned, immutable release of content. AI × QE tracks separate version fields so a
slide change and a site change are distinct publication events. — `ai_qe/_data/release.yml`

**Evidence log** — The dated, append-only record of commands and outputs a student keeps all course;
it becomes the capstone's evidence record. — `course/03-content/m00-orientation/lab.md`

**Fail closed** — A safety default that refuses the operation when a required proof is missing. In
M3, a model without verified-local metadata is rejected rather than trusted. — `course/03-content/m03-privacy-ship/lesson.md`

**Health score** — The solver's 0–100 quality metric for a generated roster, printed by
`api.cli.main solve` (`SignUpFlow/api/cli/main.py:193`). Its value depends on the revision: at the
2026-09-16 head the sample workspace prints `0.0/100` with two hard violations. — `SignUpFlow/README.md`

**Local model** — A model whose weights run on your machine. In M0 the example is `qwen3:0.6b`; the
point of pulling one is that no API key and no cloud bill are involved. — `course/03-content/m00-orientation/lesson.md`

**Loop journal** — The single file, started in M0.2, where a student records one line per loop stage
touched by each action step. — `course/03-content/m00-orientation/lesson.md`

**On-device** — Processing that happens on the user's hardware, so audio or text need not leave the
machine. ListenToMe is the on-device case study. — `ListenToMe/README.md`

**Proof asset** — Verifiable evidence inside a repo — a coverage badge, a dated test-evidence line, a
provenance file, a published self-audit. Not a testimonial, not a README claim. — `course/01-design/content-standards.md`

**Provenance** — The traced origin of a claim: source, retrieval date, and claim type. Every AI × QE
claim carries it, and M6 requires it of student briefings. — `ai_qe/README.md`

**Spec kit** — The artifact set behind one feature: spec, research, plan, contracts, quickstart,
checklists, tasks. SignUpFlow has 17 such folders. — `SignUpFlow/specs/`

**Spec-to-Ship Loop** — The six-stage method used in every module: Study → Spec → Build → Validate →
Release → Prove, with a real artifact at each stage. — `course/00-research/00-synthesis.md`

**Tenant isolation** — The rule that every database query filters by `org_id`, so one organization can
never read another's rows. A missing filter is a P0 bug. — `SignUpFlow/AGENTS.md`

**Test tier** — One layer of the test pyramid run in its own process. SignUpFlow documents seven
tiers; the full local suite once recorded "1,464 passed, 21 skipped". — `SignUpFlow/docs/TESTING.md`; `SignUpFlow/docs/playbooks/validation.md`

**Verified local** — A local model accepted only after metadata proves it is not remote-backed:
`remote_host`/`remote_model` absent, format/model-info present. A `localhost` URL alone is not proof.
— `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift`

**YAGNI non-goals** — The explicit list of what a design refuses to build. ListenToMe's spec says:
no cloud backend, accounts, billing, or multi-user. — `ListenToMe/docs/superpowers/specs/2026-06-18-listentome-design.md`

## Terms people get wrong

- **Local model vs. verified local** — "Runs on localhost" is an address; "verified local" is metadata
  proof that the backing model is not remote. Only the second survives M3's red-team test.
- **Proof asset vs. README claim** — A claim is prose someone typed; a proof asset is a machine
  output or a dated record. Both can appear in a README; only one is evidence.
- **Acceptance criteria vs. success criteria** — Acceptance criteria say when a story is done
  (Given/When/Then); success criteria say whether the feature succeeded in the world. A spec needs
  both, separately. — `SignUpFlow/specs/014-security-hardening/spec.md`
- **Validate vs. Prove** — Validation shows the thing you built passes its tests; Prove is the honest
  record of what was and was not verified, including the failures. ListenToMe's "do not promote 1.3.0"
  review is Prove, not Validate. — `ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md`
- **Release vs. Prove** — A release is an artifact you publish; it becomes proof only when it is
  signed, dated, and traceable to a source commit. — `ListenToMe/AGENTS.md`

## Curated resources

1. `course/03-content/m00-orientation/lesson.md` — the module script; read it once before the lab.
2. `SignUpFlow/README.md` — the solver "CLI Example" gives the exact output your lab must match.
3. `course/03-content/m02-ondevice-app/tinycopilot/README.md` — the M2 lab reference and the
   privacy lab explained in one paragraph.
4. `ListenToMe/docs/competition-analysis.md` — the best model in the course for turning research into
   positioning.
5. `SignUpFlow/docs/playbooks/validation.md` — read the failures section; it is the honesty standard.
6. `ai_qe/docs/principles.md` — short, and its "baseline before solutioning" principle governs every
   module.
7. `course/00-research/00-synthesis.md` — the derivation of the loop and the transferable principles,
   if you want the method's sources.
8. `course/01-design/content-standards.md` §0.2 — the verified-numbers list; check claims here before stating
   them.
