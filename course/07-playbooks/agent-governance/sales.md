# Sales Page: Agent Governance Files and an Evidence Log

## [Hero]

# Rules your coding agents follow, and a record a stranger can check.

A standalone playbook: one `AGENTS.md` every agent reads, a `CLAUDE.md` that imports it, a decision table for rule vs hook vs skill vs subagent, a six-field evidence log, and a Claude Code `Stop` hook that will not let the agent stop while the latest entry is incomplete.

**You leave with:** five copy-paste files, a hook tested red and green, and a self-check you run from your repo root.

## [Who this is for — and isn't]

**For you if you:**
- Ship code with Claude Code, Codex, Cursor or Copilot and keep correcting the same mistakes.
- Have an `AGENTS.md` or `CLAUDE.md` that grew past the point anyone reads it.
- Want validation written down with commands, counts, the environment and a commit SHA.

**Not for you if you:**
- Want prompt tips. This is about files, hooks and records.
- Need an enterprise AI-governance or compliance framework.

## [The problem]

Agent rule files grow until nobody reads them in full, and fill with advice nobody can check ("be careful with multi-tenancy"). Meanwhile "it worked" is recorded as a feeling. In METR's 2025 randomized trial, experienced maintainers took 19% longer with AI allowed while believing they had been 20% faster (`ai_qe/docs/evidence/benchmarks.md:28-44`). A later METR study was inconclusive (`ai_qe/docs/evidence/benchmarks.md:50-57`). Neither shows AI slows everyone; both show that impressions are not measurements.

## [What you get]

- `playbook.md`: nine numbered steps, templates, a binary checklist, a worked example, a self-check, and a plain list of limits.
- Templates: `AGENTS.md`, `CLAUDE.md` (with the `@AGENTS.md` import), the evidence-entry format, `scripts/check-evidence-log.sh`, `.claude/settings.json`.
- The rule / hook / skill / subagent table: what each mechanism is for, what it cannot do, and when to reach for it.

## [What you'll be able to do]

- Write rules that pass one test: *what command, file or number proves this was followed?*
- Keep one canonical rule file for every agent, 200 lines or fewer with its Claude addenda.
- Decide which rules must become hooks, and prove the hook blocks before you trust it.
- Write evidence entries that include the failures and at least one limitation.

## [Proof]

- SignUpFlow's house style, "Each rule must be verifiable. `Filter every query by org_id.` Not `Be careful with multi-tenancy.`" (`SignUpFlow/AGENTS.md:33`), in a 188-line baseline file.
- An evidence record that keeps its own failures, its debt ("835 errors in 40 files; not a pass") and its limits (`SignUpFlow/docs/playbooks/validation.md:45`, `SignUpFlow/docs/playbooks/validation.md:67-70`). It is labelled historical reference; the format is what you copy.
- The hook script was run on 2026-09-26: exit 2 with the missing field named, then exit 0. The output is printed in the playbook.
- The free audit tool scores SignUpFlow's `AGENTS.md` at 69% checkable rules (`aps-tools/README.md`; re-run for this playbook).

## [Instructor]

Written from the AI Product Studio course by Tom Wu, who builds in public. The course studies three of his repositories; this playbook uses SignUpFlow and ListenToMe as its worked examples.

## [Testimonials]

None yet. No buyer has used this playbook, so there is nothing to quote. This section stays empty until one does.

## [FAQ]

**Do I need Claude Code?** For the import and the hook, yes. `AGENTS.md`, the rule-writing method and the evidence log work with any agent; outside Claude Code you run the check yourself.

**Does the hook prove my tests passed?** No. It checks form: a date, a result line, an environment, a SHA that exists, a limitation, no placeholders. It cannot check truth.

**Is the audit tool part of the price?** No. It is free in the AI Product Studio repository; the playbook shows how to read its score.

**Refunds?** Set by the owner with the final price. This draft promises none.

## [Pricing]

**$39** (proposed; the owner sets the final price).

The full AI Product Studio course ($399, `course/04-sales/landing-page.md`) includes this material and eight more modules. If you want more than governance files, it is the better value.

## [Final call]

Replace the rules nobody can check with rules a stranger can, and let a script tell you when an evidence entry is incomplete.
