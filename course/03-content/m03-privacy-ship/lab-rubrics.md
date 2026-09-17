# Lab Rubrics M3 — Harden, Prove, Position

> Lab M3 is a **pass/fail checkpoint** inside the 60% module-lab component
> (`course/01-design/assessment-and-rubrics.md`). This rubric is how an instructor tells a real pass
> from a plausible fake. Every criterion is observable and names the evidence submitted.
> **Weights sum to 100.**

## Rubric

| # | Criterion (step) | Weight | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|---|
| 1 | Red-team test proven first (Steps 0–1) | 15 | Step 0's `make lab-m3` red (`ModuleNotFoundError`, exit 4, after `make m3-start`) captured, then the red-team assertion failure, then green; a variant with empty `details.format` also fails | Red-team test exists and passes; Step 0's red captured but the assertion-level red only mentioned | Test written after the implementation, or covering only `remote_host`, or no Step 0 run | No cloud-alias test, or it asserts only the exception type, or the lab was done on the un-parked reference | `make m3-start` output, `pytest` output for the red and green runs, the test function |
| 2 | Four defenses, one test each (Step 1) | 20 | Metadata rule, host allowlist, per-request verification and redirect refusal each have a passing test; the redirect test asserts no forwarding | All four covered; one test asserts weakly (e.g. no message match) | Two or three covered; one implemented without a test | Fewer than two defenses implemented or tested | `make lab-m3` output (49 passed) and the four test names |
| 3 | Fail-closed semantics (Step 1) | 10 | Missing `details`, empty `model_info`, malformed JSON, non-200 and an unreachable transport all return `False`/raise, each with a truthful reason naming the failed check | Missing-metadata and non-loopback cases fail closed | Some failure paths default to proceeding (fail-open) | Fail-open in the metadata or host check | Test list covering each negative case; one printed reason string |
| 4 | Gated real-LLM contract test (Step 2) | 15 | Without `LAB_E2E`: 2 skipped with a stated reason; with it: 2 passed through the student's own `OllamaProvider` on the router's pick, `:cloud` or local; daemon case documented | Runs through the provider with a minimum-content assertion; one of the two runs recorded | Calls the daemon directly, asserts only "no exception", or is gated on local-only mode so a cloud-only daemon skips it | No contract test, or deleted/hidden rather than skipped, or replaced by a mocked stream | Both command outputs, plus the daemon state (local model or only `:cloud`) |
| 5 | Coverage floor bites (Step 3) | 15 | `COV_FLOOR` back at 90; failure run captured with a non-zero exit naming the floor; success run showing the floor reached; the skipped module named | Both runs captured, one without an exit code | Only the success run, or the floor configured but never shown failing | Floor absent, or set on a target that emits no coverage | Two command outputs with exit codes |
| 6 | Sourced comparison table (Step 4) | 10 | ≥5 competitors, ≥6 columns, every cell a URL or `unverified`; uncertain claims qualified "approximately"/"reportedly" | ≥5 rows and ≥6 columns; one or two URLs missing | Table exists but has memory-only prices or unlabeled cells | Fewer than 5 rows or fewer than 6 columns | `docs/competition.md` |
| 7 | Positioning one-liner (Step 4) | 5 | Every clause annotated with the column proving it; deleting a clause makes the line false against the table | One-liner present, most clauses traced | Adjectives with no column behind them | No one-liner, or no clause traceable | The annotated clause-to-column list |
| 8 | Tag and checksum (Step 5) | 10 | Annotated `v0.1.0` at the tested commit (`git describe --tags --exact-match` shown); the wheel's SHA-256 line, the `OK` from a `-c` re-check on a copy outside the repo, *and* the `FAILED` from a corrupted copy; the rung named *candidate, not published* | Tag, digest line and the `OK` run recorded; the corrupted-copy `FAILED` or the rung statement missing | Tag exists but the digest was taken once with no re-check, or the tag disagrees with `pyproject.toml`'s version | No tag, no checksum, or the artifact called "released" with nothing pushed or downloaded | `git describe`, `git rev-parse`, the digest line, and both `-c` outputs (`sha256sum` or `shasum -a 256`) |
| | **Total** | **100** | | | | | |

## Auto-fail list

Any one of these fails Lab M3 regardless of the rows above:

1. **Fabricated evidence** — an invented command output, test count, coverage percentage, or source
   URL. This is the course's only automatic fail (`course/01-design/assessment-and-rubrics.md`).
2. **Green with no red** — Step 0, Step 1 or Step 3 submitted with a passing run and no recorded
   failure run, where the step requires both.
3. **Tests weakened to pass** — deleting or skipping the cloud-alias, missing-metadata,
   non-loopback or redirect test; lowering `--cov-fail-under` to make the failure run green.
4. **Local-only checks bypassed for a cloud-only daemon** — removing the metadata guard, or routing
   around it, so Step 1 "passes" on a `:cloud`-only machine. Document the daemon state instead;
   Step 2's contract test is unaffected, running in the provider's default mode.
5. **Fail-open metadata rule** — a missing `details` or `model_info` key treated as acceptable
   rather than a rejection.
6. **Memory-only competitor pricing** — a price cell with no source URL and no `unverified` mark.
7. **A borrowed digest** — a checksum line copied from `solutions.md` or a peer rather than printed
   by the student's own run. A wheel's `.dist-info` entries carry the build time, so two honest
   builds of one commit differ; an identical digest is a copy.

## Calibration notes

**Proficient is the pass bar** on every row; a submission may be Developing on one row (weight ≤15)
and still pass overall, but auto-fails are absolute. Use the evidence record itself as the
cross-check: it must name what the agent did and what the student verified. When a row is ambiguous,
ask for the command again live — a real pass reproduces, a plausible fake does not.

**Consistency with course weights.** Scoring this checkpoint does not change quiz (20%) or capstone
(20%) weighting. Lab M8 reuses the same evidence under C2 "Build discipline" and C4 "Discipline
artifact", and its "Tagged release or deployed URL" deliverable is row 8 with the tag pushed for
real — so a strong Lab M3 submission feeds straight into the capstone score.
