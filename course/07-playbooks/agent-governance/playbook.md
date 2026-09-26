# Agent Governance Files and an Evidence Log

This playbook is for engineers who ship code with AI coding agents (Claude Code, Codex, Cursor, Copilot) and want two things: rules the agents follow that a stranger could check, and a record of what was validated that does not depend on anyone's memory. When you finish you will have one `AGENTS.md` that every agent reads; a `CLAUDE.md` that imports it, the pair at 200 lines or fewer; a decision for each rule on whether it stays a rule or becomes a hook, a skill or a subagent; an evidence log in a fixed six-field format; and a Claude Code `Stop` hook that keeps the agent working while the latest evidence entry is incomplete, tested red and then green.

## The method

1. **Put every shared rule in one `AGENTS.md` at the repo root.** Codex, Cursor and other agents read it directly (`SignUpFlow/AGENTS.md:3` names seven). Keep one canonical source; any other agent file imports or restates it rather than keeping a parallel copy.

2. **Make `CLAUDE.md` import it with `@AGENTS.md`, not link to it.** Claude Code's memory documentation (code.claude.com/docs/en/memory, read 2026-09-26; the vendor's own documentation) says that with both files present it reads "Your `CLAUDE.md` files only", and that "Imported files are expanded and loaded into context at launch." A link is not an import: for a `CLAUDE.md` that tells Claude in words to read `AGENTS.md`, "Claude sees `AGENTS.md` only if it decides to open the file." Put the import on line 1. Below it, write only what is specific to Claude Code.

3. **Write every rule as an imperative a stranger could check.** The test: *what command, file or number proves this rule was followed?* If the answer is a feeling, rewrite the rule.

   | Unverifiable | Verifiable | Why |
   |---|---|---|
   | "Be careful with multi-tenancy" | "Filter every query by `org_id`" | A filter can be checked; care cannot |
   | "Keep instruction files manageable" | "Keep each instruction file under ~200 lines" | A number is checkable |
   | "Value test coverage" | "Write the failing test first; run `make test-unit`" | Names the action and the check |
   | "Handle secrets safely" | "Never commit API keys; read them from environment variables" | "Never commit X" is greppable |

   (Contrasts from `SignUpFlow/AGENTS.md:33, 35, 99, 49`, in row order.)

4. **Keep the pair to 200 lines or fewer.** The same documentation says "target under 200 lines per CLAUDE.md file", and imported files "still load and enter the context window at launch". An import loads in full, so the budget covers `AGENTS.md` and the addenda together. Check with `wc -l AGENTS.md CLAUDE.md`. Split by topic rather than nesting.

5. **Add the anti-hallucination rules and one precedence line.** Forbid inventing paths, names and commands; require reading facts from the file that defines them; require 2-3 options when a request is ambiguous. For conflicts, one tie-breaker covers most cases: "follow the more specific and safer one" (`SignUpFlow/AGENTS.md:153-161`).

6. **Choose a mechanism for each rule.** Claude Code treats `CLAUDE.md` "as context, not enforced configuration" (memory page), and "Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens" (code.claude.com/docs/en/best-practices, read 2026-09-26). A rule is only for what the agent should *know*.

   | Mechanism | For | Cannot | Reach for it when |
   |---|---|---|---|
   | **Rule**: a line in `AGENTS.md` or `CLAUDE.md`, or a file in `.claude/rules/` | Facts and conventions needed every session: commands, prohibitions, house style | Guarantee anything; a long file dilutes it | The agent gets a convention wrong twice and the code cannot show it the right one |
   | **Hook**: a script bound to an event in `.claude/settings.json` (`Stop`, `PreToolUse`) | Enforcement. Exit code 2 blocks, or keeps Claude working, and Claude reads stderr | Judge meaning; a script checks form, never truth. Runs only inside Claude Code | A rule must hold every time and a script can decide it |
   | **Skill**: `.claude/skills/<name>/SKILL.md`, loaded when relevant or run as `/<name>` | A procedure that would bloat `CLAUDE.md`: a release checklist, a style guide | Enforce anything; Claude "interprets the instructions; outcome can vary" | You paste the same multi-step procedure a third time |
   | **Subagent**: `.claude/agents/<name>.md` | Work in its own context window that returns a summary: wide research, a review by a session that did not write the code | See your conversation; its summary is still a claim to check | A side task would flood your context, or the work needs an independent reviewer |

   (Sources: code.claude.com/docs/en/features-overview and code.claude.com/docs/en/hooks, read 2026-09-26.)

7. **Record every validation as an evidence entry.** Six fields: the date, each command, its result with counts, the environment, the revision SHA, and at least one limitation. If a run failed and you re-ran it, record both lines. If you skipped something, write the skip. Append new entries at the end of the file; the hook below reads only the last one.

   Why a record and not an impression: in METR's 2025 randomized trial, 16 experienced maintainers took 19% longer on 246 real issues when AI was allowed (CI +2% to +39%), and afterwards believed they had been 20% faster (`ai_qe/docs/evidence/benchmarks.md:28-44`). METR's February 2026 follow-up was inconclusive; both confidence intervals include no effect (`ai_qe/docs/evidence/benchmarks.md:50-57`). Neither shows that AI slows everyone down. Both show that how fast work felt is not evidence.

8. **Turn "every entry is complete" into a `Stop` hook, and test it red before you trust it.** The rule is one a script can decide, so by step 6 it belongs in a hook. Delete a field, run the check, see exit 2; restore it, see exit 0; record both runs.

9. **Graduate new rules; do not add them on impulse.** Record an observation, dated, in `docs/research-log.md`. Test it on at least one real change. Only then promote it into `AGENTS.md` (`SignUpFlow/docs/ai-agent-coding-strategy.md:90-106`). The separate log exists "so that exploratory notes never become silent rules" (`SignUpFlow/docs/research-log.md:24`).

## Template

**`AGENTS.md`.** Replace `my-studio` and the test command with your own. Most lines name their check; the self-check covers the rest.

```markdown
# AGENTS.md
Cross-agent baseline for my-studio. Every agent that reads AGENTS.md follows it.

## House style
- Write each rule in imperative voice and name the command, file or number that checks it.
- Keep `AGENTS.md` and `CLAUDE.md` to 200 lines or fewer together: `wc -l AGENTS.md CLAUDE.md`.

## Anti-hallucination
- Do not invent file paths, function names, commands or URLs. Run `git grep` before citing one.
- Read facts (env var names, schema fields, versions) from the file that defines them. Do not recall them.
- When a request has two or more readings, present 2-3 options and stop.

## Safety
- Never commit secrets: `git diff --cached | grep -iE 'api[_-]?key|secret|token'` returns nothing meaningful.
- Never run `rm -rf`, `git push --force` or `git reset --hard` without the user's approval for that command.
- When unsure whether an action is reversible, stop and ask.

## Tests
- Write the failing test first. Record the red run in `docs/evidence-log.md` before the green run.
- Add at least 1 negative-path test per feature (missing id, malformed input, unauthorized caller).

## Validation checklist (before declaring done)
- [ ] `python3 -m pytest tests/ -q` exits 0.
- [ ] The secrets grep in Safety returns nothing meaningful.
- [ ] Every doc that names a changed command, path or count is updated in the same commit.
- [ ] `bash scripts/check-evidence-log.sh` exits 0.

## Commit format
- Body sections, in order: `Summary`, `Changed files`, `Validation`, `Follow-ups`.
```

**`CLAUDE.md`.** The import on line 1, then only Claude Code addenda.

```markdown
@AGENTS.md

## Claude Code addenda
- A Stop hook runs `scripts/check-evidence-log.sh` after each turn. When it
  blocks, fix the entry it names; never edit the script or hook to pass.
- Record the red run in `docs/evidence-log.md` before the green run.
```

**Evidence entry.** Append one per validation to `docs/evidence-log.md`.

```markdown
## Evidence — <project> — <feature> — <YYYY-MM-DD>
Commands (with results):
- <command> → <N passed, M skipped, K failed>
- ...
Environment: <OS, Python version, machine notes>
Revision: <`git rev-parse HEAD` output>
Limitations / not verified:
- <honest list — include at least one>
```

**`scripts/check-evidence-log.sh`.** It needs at least one commit in the repo, because it checks that the recorded SHA exists.

```bash
#!/usr/bin/env bash
# Checks the latest entry in docs/evidence-log.md. Exit 0: no entry yet, or all
# six fields are filled. Exit 2: something is missing (Claude Code reads stderr).
cd "$(dirname "$0")/.." || exit 2
log=docs/evidence-log.md
[ -f "$log" ] || { echo "Evidence log: no $log yet."; exit 0; }
entry=$(awk '/^## Evidence/ {f=1; b=""} f {b = b $0 "\n"} END {printf "%s", b}' "$log")
[ -n "$entry" ] || { echo "Evidence log: no entry yet."; exit 0; }
miss=""
has() { printf '%s\n' "$entry" | awk "$1" || miss="$miss- $2"$'\n'; }
has '/^## Evidence.*[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]/ {ok=1} END {exit !ok}' "a YYYY-MM-DD date in the heading"
has '/^Commands/ {c=1; next} /^Environment:/ {c=0} c && /^- .*(→|->) *[^ <]/ {ok=1} END {exit !ok}' "a '<command> → <result>' line"
has '/^Environment: *[^ <]/ {ok=1} END {exit !ok}' "an Environment value"
has '/^Limitations/ {l=1; next} l && /^- *[^ <]/ {ok=1} END {exit !ok}' "at least one limitation"
sha=$(printf '%s\n' "$entry" | sed -n 's/^Revision: *`\{0,1\}\([0-9a-f]\{7,40\}\).*/\1/p' | head -n 1)
git cat-file -e "${sha:-none}^{commit}" 2>/dev/null || miss="$miss- a Revision SHA that exists in this repo"$'\n'
if printf '%s\n' "$entry" | grep -q '<[^>]*>'; then miss="$miss- no <placeholders> left"$'\n'; fi
if [ -n "$miss" ]; then
  printf 'Evidence log: the latest entry in %s needs:\n%s' "$log" "$miss" >&2
  exit 2
fi
echo "Evidence log: latest entry complete."
```

**`.claude/settings.json`.** Binds the check to `Stop`, which fires each time Claude finishes a turn.

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"${CLAUDE_PROJECT_DIR}\"/scripts/check-evidence-log.sh"
          }
        ]
      }
    ]
  }
}
```

In a Claude Code session, exit 2 on `Stop` keeps Claude working with the script's stderr as its instructions; after eight blocks in a row, Claude Code lets the turn end (code.claude.com/docs/en/hooks, read 2026-09-26). Another agent reads `AGENTS.md` and ignores both `CLAUDE.md` and the hook, so run the check yourself before you commit.

## Checklist

- [ ] `AGENTS.md` exists at the repo root and holds every shared rule.
- [ ] `head -1 CLAUDE.md` prints `@AGENTS.md`.
- [ ] `CLAUDE.md` restates nothing that is in `AGENTS.md`.
- [ ] `wc -l AGENTS.md CLAUDE.md` totals 200 or fewer.
- [ ] Three rules picked at random each answer "what command, file or number proves it?"
- [ ] The anti-hallucination rules and a precedence line are present.
- [ ] Every rule that must hold every time has a named hook or a stated reason why no script can decide it.
- [ ] `.claude/settings.json` is valid JSON and binds `scripts/check-evidence-log.sh` to `Stop`.
- [ ] The check was run red (exit 2) and green (exit 0), and both runs are recorded.
- [ ] The latest evidence entry has a dated heading, command → result lines, an environment, a SHA that `git cat-file -e` resolves, and at least one limitation.
- [ ] Every failed run you saw appears in the log, with its re-run.
- [ ] `docs/research-log.md` holds at least one dated observation.

## Worked example from a real repo

**SignUpFlow**, a multi-tenant volunteer-scheduling API (`SignUpFlow/AGENTS.md:11`), runs a layered stack: an 85-line constitution (`SignUpFlow/.specify/memory/constitution.md`), a 188-line `SignUpFlow/AGENTS.md`, and a 154-line `SignUpFlow/CLAUDE.md`.

- **House style as rules.** "Use imperative voice", "Each rule must be verifiable. `Filter every query by org_id.` Not `Be careful with multi-tenancy.`" and "Keep each instruction file under ~200 lines" (`SignUpFlow/AGENTS.md:30-36`).
- **Anti-hallucination.** "Do not invent file paths, function names, route paths, commands, URLs, or identifiers. Grep the repo before referencing." (`SignUpFlow/AGENTS.md:63-69`).
- **Evidence as a rule.** "Do not fabricate status checks, bypass protections, or treat missing evidence as success." (`SignUpFlow/AGENTS.md:93`).
- **The link-not-import trap, live.** `SignUpFlow/CLAUDE.md:5` reaches `AGENTS.md` through a markdown link, and `SignUpFlow/AGENTS.md:5` explains why: "Claude Code does not read this file natively". That was true when written; per the documentation quoted in step 2 it is stale. Note the budget cost of the fix: an import would load 188 + 154 = 342 lines at launch, so the fix is the import plus a trim of the addenda.
- **The hook principle, outside Claude Code.** Its guarded agent runner fails a forbidden Git mutation "even if the agent ignores the command error and prints DONE" (`SignUpFlow/docs/AGENT_RUNNER.md:27-29`). A policy-regression test guards the no-CI rule (`SignUpFlow/tests/unit/test_local_validation_policy.py`). A rule that must never break gets a check a script runs.
- **An evidence record that includes failures.** SignUpFlow's validation record names its environment (`SignUpFlow/docs/playbooks/validation.md:8-10`), keeps a browser timing failure "not omitted from the evidence" (`SignUpFlow/docs/playbooks/validation.md:50-53`), labels 835 mypy errors "Existing debt ... not a pass" (`SignUpFlow/docs/playbooks/validation.md:45`), pins follow-up runs to `cccc6f7` (`SignUpFlow/docs/playbooks/validation.md:74`), records "1,464 passed, 21 skipped" (`SignUpFlow/docs/playbooks/validation.md:86-89`), and states what the runs do not verify (`SignUpFlow/docs/playbooks/validation.md:67-70`). The file has been labelled historical reference since 2026-09-13 (`SignUpFlow/docs/playbooks/validation.md:3-6`): copy its format, not its status.

**ListenToMe** shows the limitation field doing its job. Its release review recommends "do not promote the existing 1.3.0 DMG as a broadly validated production release", because "215 passing Core tests, and 97.24% Core coverage ... do not establish capture reliability, durable saving, accurate speaker attribution, or a usable first-run experience" (`ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md:5`).

## Self-check

Run from your repo root. The audit line needs `aps-tools/agents_audit.py`, a free, standard-library checker (Python 3.11+) from github.com/tomqwu/ai_courses; copy the `aps-tools/` folder into your repo. Its README says the tools are free to copy and use; the repository has no licence file yet.

```bash
wc -l AGENTS.md CLAUDE.md                                # total: 200 or fewer
head -1 CLAUDE.md                                        # @AGENTS.md
python3 -m json.tool .claude/settings.json > /dev/null && echo "settings: valid JSON"
bash scripts/check-evidence-log.sh; echo "exit=$?"       # a complete entry: exit=0
python3 aps-tools/agents_audit.py --max-lines 200 AGENTS.md CLAUDE.md
```

Then the red run: delete the limitation line from your latest entry and run the check again. Expected, as run on 2026-09-26 (Linux, bash 5.2):

```text
Evidence log: the latest entry in docs/evidence-log.md needs:
- at least one limitation
exit=2
```

Restore the line; expect `Evidence log: latest entry complete.` and `exit=0`. A SHA that does not exist in the repo gives `- a Revision SHA that exists in this repo`; an unfilled template lists six problems.

The audit is a lexical heuristic. On the template above it reports `29 lines (within budget, limit 200) · 15 rules · 10 checkable, 0 vague, 5 unenforced (67% checkable)`. The five flags include "When unsure whether an action is reversible, stop and ask", a judgement rule kept on purpose. Its README says to read the score "as a question": for SignUpFlow it reports 69% checkable for `AGENTS.md` and 50% for the constitution, which states principles rather than checks.

**Pass criteria.** All five commands give the expected output, the red run exits 2 and names the missing field, and every line the audit flags either gains a check or has a one-sentence reason a stranger can still verify it.

## Limits

- The hook checks form, not truth: a dated heading, a result line, an environment, a SHA that exists, a limitation, no placeholders. It cannot tell whether the counts are real.
- The hook runs only inside Claude Code. Codex, Cursor and your own terminal skip it.
- The `@AGENTS.md` import and the `Stop` hook are Claude Code features, documented as of 2026-09-26. Re-read the vendor documentation before relying on either; agent tools change their loading rules.
- A rule is context the model weighs. Nothing in this playbook makes an agent obey a rule; only hooks and tests enforce.
- The audit's buckets are keyword heuristics, not a verdict on whether a rule is enforceable.
- This playbook does not cover spec-driven task planning, CI design, or security review.

## Sources

- `SignUpFlow/AGENTS.md`, `SignUpFlow/CLAUDE.md:5`, `SignUpFlow/.specify/memory/constitution.md`, `SignUpFlow/docs/ai-agent-coding-strategy.md:83-106`, `SignUpFlow/docs/research-log.md:24`, `SignUpFlow/docs/AGENT_RUNNER.md:27-29`, `SignUpFlow/tests/unit/test_local_validation_policy.py`, `SignUpFlow/docs/playbooks/validation.md`.
- `ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md:5`.
- `ai_qe/docs/evidence/benchmarks.md:28-57`: METR studies, 2025 and 2026, as summarised there.
- Claude Code documentation, the vendor's own: code.claude.com/docs/en/memory, /best-practices, /features-overview and /hooks, all read 2026-09-26.
- `aps-tools/agents_audit.py` and `aps-tools/README.md` in github.com/tomqwu/ai_courses.
- This playbook is extracted from the AI Product Studio course (github.com/tomqwu/ai_courses).
