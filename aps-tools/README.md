# aps-tools — three checkers that keep documentation honest

Free, standard library only. No install, no network, nothing written to disk, nothing
sent anywhere. Copy the folder into any repository and run the scripts.

They exist because documentation fails in three specific ways, and each failure is cheap to detect
and expensive to discover from a reader's complaint:

| Tool | The failure it catches | Run it |
|---|---|---|
| `pointer_lint.py` | A claim points at a file or line range that has moved or gone | `python3 pointer_lint.py docs/` |
| `facts_drift.py` | A number stated as fact was true when written and is not true now | `python3 facts_drift.py --facts facts.json --docs docs/` |
| `agents_audit.py` | An agent rule file grew past reading, or filled with advice nobody can check | `python3 agents_audit.py AGENTS.md` |

Requires Python 3.11 or newer. Run the tests with `python3 test_aps_tools.py` — 19 tests, no
dependencies.

## pointer_lint.py — every claim carries a pointer, and every pointer resolves

A pointer is a backticked path in Markdown, optionally with line numbers:

```
`SignUpFlow/AGENTS.md`            the file must exist
`api/routers/events.py:88`        line 88 must exist in it
`src/Prompt.swift:73-81, 99`      every range must lie inside the file
```

```bash
python3 pointer_lint.py docs/                                   # lint one folder
python3 pointer_lint.py --base .. --roots ListenToMe,SignUpFlow course/
python3 pointer_lint.py --json .                                # machine-readable
```

`--roots` restricts linting to pointers whose first path segment is one of the named directories,
which is how you lint prose that points into sibling repositories without tripping over every other
backticked string. Exit status is 1 when anything fails to resolve, so it drops into a pre-commit
hook or a CI step.

What a clean run looks like on the repository this folder ships in, with the three case-study
repositories cloned beside it:

```
$ python3 aps-tools/pointer_lint.py --base . --roots ListenToMe,SignUpFlow,ai_qe course
1130 pointer(s) in 161 file(s), 275 line range(s) checked against .
```

A line range is the part people skip, and it is the part that rots fastest: a file that gains ten
lines at the top silently invalidates every line number below it while the file itself still exists.

## facts_drift.py — the numbers are re-derived, not remembered

Pointers prove a file still exists. Nothing proves the *numbers* are still true, and numbers are
what a skeptical reader checks you on. Pin the ones you are willing to state, re-derive each from
the source, and let the tool name the documents that still print an old value.

```bash
python3 facts_drift.py --facts facts.json --base . --docs docs/
python3 facts_drift.py --facts facts.json --strict     # exit 1 on any drift
```

`facts.json` is **data, not code**. Derivations are declarative and nothing in the file is ever
executed, so a facts file arriving in a pull request cannot run commands on your machine. Copy
`facts.example.json` and edit the paths. The kinds:

| Kind | Derives | Keys |
|---|---|---|
| `file_lines` | line count of a file | `path` |
| `glob_count` | number of files matching a glob | `glob` |
| `glob_lines` | total lines across a glob | `glob` |
| `regex_count` | number of matches in a file | `path`, `pattern`, `ignorecase` |
| `regex_capture` | a captured group (a version, a tag) | `path`, `pattern`, `group`, `cast` |
| `line_of` | line number where a pattern first appears | `path`, `pattern` |
| `table_rows` | data rows in a Markdown table | `path`, `after` |

Each fact may carry `literals`: exact strings to search for when that fact drifts, so
re-verification is a targeted edit rather than a re-read of every document.

```
$ python3 aps-tools/facts_drift.py --facts aps-tools/facts.example.json --base . --docs docs/
agents_md.lines              188           188  ok
constitution.lines            85            85  ok
core.swift_files              45            45  ok
core.swift_lines            5194          5194  ok
health_score.line            193           193  ok
competitors.rows              14            14  ok

all 6 pinned facts re-derive to their pinned values
```

Advisory by default, because a number that moved upstream is not a defect in your document — it is
a re-verification task. `--strict` is for the moment before you publish, where a stale number *is* a
defect.

## agents_audit.py — rules a stranger could check

An agent rule file fails in two directions. It grows past the point where it is read in full on
every task, and it fills with advice no one can verify: "be careful with tenancy", "use good
judgement", "where possible, prefer composition". A rule that cannot be checked cannot be enforced,
so it is decoration that costs context.

```bash
python3 agents_audit.py AGENTS.md
python3 agents_audit.py --max-lines 200 --min-checkable 0.8 AGENTS.md CLAUDE.md
python3 agents_audit.py --json .specify/memory/constitution.md
```

Each rule lands in one of three buckets:

- **checkable** — names a path, a command, a number or a concrete artifact
  ("Every database query MUST filter by `org_id`");
- **vague** — hedged or subjective, and the report names the phrase that makes it so;
- **unenforced** — imperative, but naming nothing a reader could open or run
  ("You MUST write clean code").

Duplicates are reported with the line of the rule they repeat. Exit status is 1 when a file is over
its line budget or below `--min-checkable`.

Measured on the three repositories this course is built from:

```
SignUpFlow/AGENTS.md                      188 lines · 87 rules · 69% checkable
SignUpFlow/CLAUDE.md                      154 lines · 17 rules · 76% checkable
SignUpFlow/.specify/memory/constitution.md 85 lines · 10 rules · 50% checkable
```

The constitution scoring lowest is not a defect: a constitution states principles that the rule
files below it turn into checkable rules. Read the score as a question — *which file is supposed to
be checkable, and is it?* — rather than a grade.

## Using all three in CI

```yaml
- run: python3 aps-tools/pointer_lint.py --roots src,docs docs/
- run: python3 aps-tools/facts_drift.py --facts facts.json --docs docs/ --strict
- run: python3 aps-tools/agents_audit.py --min-checkable 0.7 AGENTS.md
```

Each exits non-zero on failure and prints `path:line` for every problem, so the failure is a place
to go rather than a verdict to argue with.

## Where these came from

They are the working tools behind [AI Product Studio](https://github.com/tomqwu/ai_courses), a
course that reverse-engineers three production repositories and states nothing it cannot point at.
The course's own gate runs versions of all three against 161 documents on every change. The tools
are free and self-contained on purpose: the method is worth more than the course, and you can check
the method without buying anything.

These tools are free to copy and use. The repository has no `LICENSE` file yet, which is a decision
the owner still has to make, so treat that as pending rather than as a permission granted here.
Issues and pull requests are welcome at
[github.com/tomqwu/ai_courses](https://github.com/tomqwu/ai_courses).
