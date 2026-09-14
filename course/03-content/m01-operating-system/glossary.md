# Glossary M1 — The AI Product Operating System

Alphabetical. Each term: definition, then where it lives.

- **AGENTS.md** — The cross-agent baseline rules file that tools such as Codex CLI, Cursor, Aider, Jules, OpenHands, Sourcegraph Amp, and Factory read natively. In SignUpFlow it is 177 lines and is restated or cross-referenced by the host-specific files. (`SignUpFlow/AGENTS.md`)
- **Anti-hallucination rules** — Prohibitions that make fabricated facts checkable: do not invent paths, names, commands, or identifiers; grep before referencing; read facts from the canonical source; offer 2–3 options when a request is ambiguous. (`SignUpFlow/AGENTS.md`, "Anti-hallucination")
- **Autonomy configuration** — The section of a constitution that fixes what an agent may do alone. SignUpFlow's: `YOLO Mode: DISABLED`, `Git Autonomy: ENABLED (Commit changes when done)`. (`SignUpFlow/.specify/memory/constitution.md`, "Autonomy Configuration")
- **Constitution** — The shortest and most authoritative governance file: the few principles that must never drift, plus the current validation policy. SignUpFlow's is 79 lines and sits above all agent instruction files. (`SignUpFlow/.specify/memory/constitution.md`)
- **Constitution Check gate** — The explicit pass/fail checkpoint in `plan.md` that must pass before Phase 0 research and be re-checked after Phase 1 design. (`SignUpFlow/specs/014-security-hardening/plan.md`)
- **Definition of Done (DoD)** — The standard for "shipped," not "built": verify the affected behavior in the installed production app, and treat stale docs as a failure rather than a follow-up. (`ListenToMe/AGENTS.md`, `ListenToMe/CLAUDE.md`)
- **Evidence record** — A dated, revision-pinned account of validation: commands with results, environment, head SHA, and an explicit list of what was not verified. (`SignUpFlow/docs/playbooks/validation.md`; template in `03-content/m01-operating-system/lesson.md`, §M1.3)
- **Instruction hierarchy** — The five-level precedence order for overlapping rules, with one tie-breaker: follow the more specific and safer one. (`SignUpFlow/AGENTS.md`, "Agent instruction hierarchy")
- **No-CI local validation** — SignUpFlow's deliberate policy of running all review, analysis, migrations, tests, and artifact validation locally and recording evidence for the pushed revision instead of requiring hosted checks. (`SignUpFlow/.specify/memory/constitution.md`, "Current Validation Policy (2026-09-13)")
- **Rule graduation** — The pipeline by which an observation becomes a rule: recorded in `docs/research-log.md`, tested on a real change, then promoted into `AGENTS.md` or a per-agent file. (`SignUpFlow/docs/ai-agent-coding-strategy.md`)
- **Self-review mapping** — A closing section of an implementation plan that maps every spec bullet to the tasks that satisfy it, so nothing silently drops. (`ListenToMe/docs/superpowers/plans/2026-06-18-listentome-mvp.md`)
- **Spec-kit** — GitHub's slash-command feature pipeline — constitution, specify, clarify, plan, checklist, tasks, analyze, implement — that produces a folder of artifacts under `specs/`. (`SignUpFlow/docs/SPEC_KIT_SETUP.md`)
- **Spec (the WHAT)** — The technology-agnostic statement of what users need: prioritized, independently testable stories with Given/When/Then acceptance scenarios and success criteria. (`SignUpFlow/specs/014-security-hardening/spec.md`)
- **Task line** — An executable entry in `tasks.md` in `[ID] [P?] [Story]` format with an exact file path and tests first. Real example: "T027 [US1] Implement POST /api/sms/send endpoint per contracts/sms-api.md in api/routers/sms.py". (`SignUpFlow/specs/019-sms-notifications/tasks.md`)
- **YAGNI non-goals** — An explicit list of what the product will not do, written into the design spec so scope cannot grow silently. ListenToMe: no cloud backend, accounts, billing, multi-user, and no covert mode. (`ListenToMe/docs/superpowers/specs/2026-06-18-listentome-design.md`, §2)

## Terms people get wrong

- **Rule vs. guideline** — A rule is verifiable ("filter every query by `org_id`"); a guideline is advice ("be careful with multi-tenancy") and does not belong in an instruction file.
- **`spec.md` vs. `plan.md`** — The spec is the WHAT and names no technology; the plan is the HOW and holds the technology decisions behind a gate.
- **Coverage vs. confidence** — Coverage says which lines ran; it does not establish reliability, which is why a 97.24%-coverage release was still recommended *against* promoting.
- **"Tests passed" vs. evidence** — Counts without a command, date, environment, and revision are a claim; evidence is auditable.
- **Baseline vs. override** — `AGENTS.md` is the universal baseline, but a more specific and safer path-scoped rule wins the conflict.

## Curated resources

1. `SignUpFlow/AGENTS.md` — the house style, the five-level hierarchy, and the anti-hallucination rules; read it as a model for your own baseline.
2. `SignUpFlow/.specify/memory/constitution.md` — 79 lines showing how little a constitution needs to hold to be authoritative.
3. `SignUpFlow/docs/ai-agent-coding-strategy.md` — the rule-graduation pipeline, with the reasoning behind one canonical source.
4. `SignUpFlow/docs/SPEC_KIT_SETUP.md` — the exact slash-command order and what each artifact is for.
5. `SignUpFlow/specs/019-sms-notifications/tasks.md` — read one real task line and copy its shape of path + contract + order.
6. `SignUpFlow/docs/playbooks/validation.md` — the model evidence record: the 1,464-passed line, the click race, the 835 mypy errors, and the limits paragraph.
7. `ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md` — the honest self-review that says "do not promote" despite high coverage.
8. `ai_qe/docs/principles.md` — the four claim levels; the discipline of labelling every number by who can confirm it.
