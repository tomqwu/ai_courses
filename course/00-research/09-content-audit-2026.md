# Content Audit: The Nine Modules Against Their Own Standard (September 2026)

> An instructional-design audit of `03-content/` graded against `01-design/content-standards.md`,
> `01-design/assessment-and-rubrics.md` and `01-design/curriculum.md`, with the three case-study repos
> cloned so numeric claims and line-range pointers could be checked. Every finding carries a pointer.
> Read with `04-platform-review-2026.md`, which turns these findings into a plan.
>
> Pointer shorthand: `C/` = `03-content/`, `D/` = `01-design/`.

## Summary grades

| Area | Grade | One line |
|---|---|---|
| Objectives → assessment mapping | B− | Verbs are measurable; about six objectives have no assessment, and Lab M0 grades something no objective names |
| Cognitive load / sequencing | C+ | The spike is real at M2 and larger at M5 (no starter); the "30-minute first win" is not 30 minutes |
| Lab quality | C | Lab M3's first three steps are already solved in the shipped repo; two red-run templates invite fabricated output |
| Quiz quality | B− | Keys present; strong misconception distractors in M3/M5/M6; six of 18 short answers are recall; one double-correct item; one lab/quiz contradiction |
| Voice / consistency | B− | Voice is clean; several "verified" numbers are stale; one line-range pointer is wrong; `verify.py` does not check line ranges |
| Depth | B | M3, M5 and M6 are strong; M7 is thinnest and self-referential |
| Platform reusability | C+ | 40–85% repo-specific by module; M6, M1.1/M1.3, M3.1 and M5.1–5.2 are extractable playbooks |
| 2026 topic coverage | D | No evals, prompt injection, cost/latency, observability, retrieval, tool/MCP design, or SaaS deployment |

## 1. Learning objectives and assessment mapping

**Verbs are measurable throughout.** Every lesson's "By the end you can" block uses Bloom-level verbs, and quiz keys print an objective reference per item as `D/assessment-and-rubrics.md` requires.

**Objectives with no assessment:**

- **M3.3 shipping half** — "Ship with a Definition of Done that ends at a published, downloaded, checksum-verified artifact" (`C/m03-privacy-ship/lesson.md:13`, taught at lines 119–121). Quiz M3 has no shipping item and Lab M3 step 4 is positioning only (`C/m03-privacy-ship/lab.md:43-51`). The heaviest, most Mac-specific content in the module is never checked.
- **M6 "Design a pilot offer with go/no-go gates"** (`C/m06-expertise-product/lesson.md:25`) — quiz only; Lab M6 has no pilot deliverable.
- **M7 "choose platforms by channel economics"** (`C/m07-monetize/lesson.md:9`) — quiz Q6 only; no lab step.
- **M8.2 deliverability (SPF/DKIM/DMARC)** (`C/m08-launch-capstone/lesson.md:73`) — no quiz item, no lab checklist line.
- **M2.1 "name the file that implements each stage"** (`C/m02-ondevice-app/lesson.md:14`) — Q1 tests order only; the lab builds Python, not Swift file names.

**Assessments with no objective:**

- **Lab M0 step 5 / rubric group C (25 points)** grades running the TinyCopilot suite (`C/m00-orientation/lab.md`, `lab-rubrics.md`). No M0 objective mentions TinyCopilot; the curriculum's Lab M0 pass gate is "solver output + `ollama list`" (`D/curriculum.md:61`).
- **Quiz M4 Q5** is labelled M4.1 in the question but keyed M4.2; Q1 and Q8 are keyed to two segments, against the "exactly one segment" rule.
- **M0 pass-gate contradiction:** the facilitation close says the pass gate is the solver output plus a non-empty `ollama list` (`C/m00-orientation/facilitation.md:92`) while the rubric auto-fails on "no community post".

Course-level count mismatch: `D/assessment-and-rubrics.md:10` says "64 total" quiz questions; `D/curriculum.md:182` says 72. Nine quizzes × 8 = 72.

## 2. Cognitive load and sequencing

**Time-on-task as written:** M0 20–40 min → M1 ~2 h → M2 ~3 h → M3 ~3 h → M4 90–120 min → M5 ~3 h → M6 ~2.5 h → M7 ~2 h → M8 6–10 h.

**The chasm is at M2, and a bigger one at M5.**

- M2 asks the student to delete and re-implement six modules (1,079 source lines, 160 tests) test-first in "~3 hours… 25–30 minutes each" (`C/m02-ondevice-app/lab.md:17`). That is a 3× jump from M1's two-test todo loop, with the answer key in the same tree — which the rubric must then police with an auto-fail for a byte-identical restore.
- M5 is worse: "Because this course ships no starter for the SaaS track" (`C/m05-security-tests/lab.md:20`), the student must stand up a FastAPI + SQLAlchemy + JWT app *before* any of the four graded steps, in "~3 hours". The curriculum promised "the provided `mini-flow` FastAPI starter" (`D/curriculum.md:131`). **This is the single biggest sequencing gap.**
- M4 is a relief valve (writing only), though the lab says 90–120 minutes and the curriculum budgets 3 hours.

**M0's "30-minute first win" is not 30 minutes on a fresh machine.** Install Poetry, `make setup` (env + migrations + seed), install Ollama, pull a model, create a venv, install pytest, run 191 tests. The module gives four different durations ("~30 minutes", "under 15 minutes", "the next twenty minutes", "20–40 minutes"); the honest number is 45–90 minutes.

**Prerequisites** are stated per lab but incomplete: Lab M4 needs the SignUpFlow clone for templates and an agent session for the stranger test; Lab M5 lists libraries but not a database; Lab M6 does not say the dataset's source records live in the `ai_qe` clone.

## 3. Lab quality

**Lab M3 is pre-solved as written.** `src/tinycopilot/privacy.py`, `tests/test_privacy.py` (31 tests, inside the 191), `tests/test_contract_real_llm.py` and `--cov-fail-under=90` in the Makefile all ship. The lab never tells the student to delete anything, yet the rubric's top row demands "a captured red run *precedes* the green run" and the solutions assert "Before the fix, `verify_local_model` does not exist" — false for the tree they hold. Lab M2 even requires `make lab-m3` to stay green (`C/m02-ondevice-app/lab.md:43`), locking the M3 deliverable in place.

**Lab M3 step 2 contradicts the repo it points at.** The lab says a cloud-only daemon means the contract test cannot run and to mock instead (`C/m03-privacy-ship/lab.md:34`); the TinyCopilot README and the test itself say the contract test runs against whatever model the router selects, including `:cloud` aliases, because "it is a *contract* test, not a privacy test". The lab also says `--cov=tinycopilot`; the Makefile uses `--cov=src/tinycopilot`.

**Two red-run templates invite the exact fabrication the rubrics auto-fail.** Lab M1's template says "`pytest` (before implementation) → 2 failed" (`C/m01-operating-system/lab.md:96`); the solutions admit the real red is a `ModuleNotFoundError` collection error, and the rubric auto-fails "a test count the recorded run does not produce". Lab M2 says "capture the red output — those failures are your spec" (`C/m02-ondevice-app/lab.md:30`); the solutions say deleting a module produces a collection error (exit 4), not failing tests. Fix the lab text, not the solutions.

**Pass criteria are mostly binary, with three exceptions.** Lab M4's gate is a judgment-based stranger test needing a peer or an agent session; Lab M6 requires a *named* peer reviewer as a checklist item, a rubric row and an auto-fail — a hard blocker for self-paced buyers; Lab M2's "explains each module's test-first cycle" is not binary.

**Environment burden per lab:**

| Lab | Needs | Mac-only? |
|---|---|---|
| M0 | git, Python 3.11–3.13, Poetry, `make setup` (migrations), Ollama + model, venv, pytest/pytest-cov/httpx, community account | Stretch only |
| M1 | Python, pytest, git | No |
| M2 | M0 stack + Ollama running for `make demo` | Swift stretch |
| M3 | M2 + daemon for `LAB_E2E=1`; web access for five competitor sites | Swift stretch |
| M4 | SignUpFlow clone (templates); a peer or an agent CLI for the stranger test | No |
| M5 | FastAPI, SQLAlchemy, Pydantic 2, a JWT library, passlib, pytest, httpx, a test DB; Playwright for stretch — **no starter** | No |
| M6 | ai_qe clone (source records); a named peer reviewer | No |
| M7 | Web access; the course's own honest-marketing checklist | No |
| M8 | Public GitHub, a static host or deploy target, screen recording, a community pair | No |

Four M4 artifacts hardcode the author's machine path (`/Users/tomwu/…`): `C/m04-spec-driven-saas/solutions.md:7`, `facilitation.md:5`, `video-scripts.md:5`, `glossary.md:3-4`. The three deep-reads in `00-research/` do too.

## 4. Quiz quality

**Answer keys** are present in all nine with rationale and objective refs. Title format drifts (`Quiz 0`, `Quiz 1`, `Quiz 4` vs `Quiz M2`…); the standard mandates `Quiz M#`.

**Recall vs application.** The standard says short answers ask for applications. Recall items: M0 Q7 ("write the exact two commands"), M2 Q7/Q8 (name the three stream-error cases), M3 Q7, M4 Q7 ("name the two hard lines"), M8 Q8 ("list the required blocks"). Genuine application items to use as models: M1 Q7/Q8, M3 Q8, M5 Q8, M6 Q7, M7 Q7/Q8, M8 Q6.

**Distractors.** Strong, misconception-encoded sets in M3 (fail-open vs silent migration; "97% coverage means ship it"), M5 (uniform-403 enumeration), M6 (CI crossing a boundary). Weak: M1 Q6 "Tests passed (trust me)"; M2 Q5 "Swift enums compile faster"; M8 Q1 (all wrong orders are absurd, so the item tests nothing).

**Ambiguous or double-correct:**

- **M4 Q5** (`C/m04-spec-driven-saas/quiz.md:45-50`): option c, "so the path can be grepped to confirm it exists", is literally what the lesson teaches, alongside keyed d.
- **M2 Q3**: the key says Listener gets "a distinct fast/light pick". True for Swift (`ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:74-77`), false for the TinyCopilot the student just built (`role_defaults` maps listener and quick to the same fastest model, `tinycopilot/src/tinycopilot/model_router.py:176`), and the lab says "the tests are authoritative here". The quiz penalises the lab.
- **M8 Q6 key** offers two numbers ("≈$900… ≈$1,005 — accept either"). Pick one convention.
- **M7 quiz** invents "6/8 required to pass"; the standard is a ≥75% *average*, with no per-quiz threshold.

## 5. Voice and consistency

**Voice** is compliant: no "in this section we will" in any lesson, lab or quiz; no hype.

**Numbers outside the §0.2 whitelist that no longer verify** (checked against the clones on 2026-09-17):

- "33 modules" in `ListenToMeCore` (`C/m02-ondevice-app/lesson.md:8`; `D/curriculum.md:85`) — the directory has **45** Swift files.
- Constitution **79** / `AGENTS.md` **177** / `CLAUDE.md` **143** lines (`C/m01-operating-system/lesson.md:29-31`, `lab.md:30`, `solutions.md:60`, the "real line counts" proof slide) — now **85 / 188 / 154**. The Lab M1 exemplar now exceeds the lab's own ≤80-line cap.
- "10 current PDF editions" (`C/m00-orientation/lesson.md:42`) — not in `ai_qe/README.md`; sourced only to the deep-read.
- "~460 lines of Python" (`tinycopilot/README.md:6`) — source is 1,079 lines; 460 is *statements*.
- "`Health score: 100.0/100`… verbatim from `SignUpFlow/README.md`" (`C/m00-orientation/lesson.md:111`; `solutions.md:96`) — the README has no such block; the string is emitted by `SignUpFlow/api/cli/main.py`.

Plus the five §0.2 facts `06-production/check_facts.py` reports as drifted: competitor table 12 → 14 rows; latest ListenToMe release v1.3.0 → v1.4.4; `AGENTS.md` 177 → 188; constitution 79 → 85; SignUpFlow tests 1,464 recorded vs 1,766 test functions on disk.

**Line-range pointers are unverified.** `verify.py` strips `:lines` before checking (`06-production/verify.py:92`), so "1,052 pointers resolve" means paths only. Sample failure: `C/m03-privacy-ship/lesson.md:57,61` cites `ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:99-119` for the host check, the per-request `/api/show` and `RejectRedirects`; those lines are the stream-completion guard block, and the real code is around lines 140–157 and 208. The lab inherits the drift. `ModelPrivacy.swift:3-13` and `:15-24` do check out.

**Contradictions across artifacts:** the Lab M5 starter; Lab M4 time; quiz totals 64 vs 72; M2 lab vs quiz on Listener routing; the M0 pass gate; Lab M3 vs the README on the contract test; the M3 lesson says three modes then shows four cases including `.apple` while the lab's `PrivacyMode` has three; the M8.2 objective says a 7–10 email arc and the lab says five.

**Duplication:** each lesson's recap restates 30–40% of the segment text; handouts restate the recap; the capstone rubric is copied three times (`D/assessment-and-rubrics.md`, `C/m08-launch-capstone/lesson.md`, `lab.md`); the four-level claim table appears in `C/m06-expertise-product/lesson.md` and `evidence-dataset.md`.

## 6. Depth

**Strongest: M3, then M5 and M6.** M3.1's claim → enforcement table and M3.3's clause → column table are genuine method. M5's status-semantics table, three drift classes, and "assert the denial *and* the unchanged row" are directly reusable. M6's four-level ladder and the questionnaire post-mortem are the best-argued content in the course. M1.2's story → scenario → task worked example is the template every module should copy.

**Thin:**

- **M7 is the weakest module.** It is a compendium of research quotes about *selling courses* applied to three products it never prices. The cost floor gets one sentence for the SaaS type and no worked floor for any archetype; per-seat pricing gets no number; the only worked example is "this course", so a student building an app or SaaS learns how a $399 course was priced.
- **M2 teaches by narrated tour** — 30+ line-number citations describe what ListenToMe did; there is no design exercise before the lab.
- **M8.2** compresses launch mechanics into one revenue line.

## 7. Reusability as a platform

Estimated share of content that is case-study-specific (would need rewriting to teach against a different repo):

| Module | Repo-specific | Extractable playbook |
|---|---|---|
| M0 | ~85% | none (orientation) |
| M1 | ~55% | **Agent governance files + evidence log** — M1.1, M1.3 and the two solutions exemplars stand alone |
| M2 | ~80% | TinyCopilot itself is the reusable asset, not the lesson |
| M3 | ~60% | **Fail-closed local-only mode** (M3.1) and **competition table → falsifiable one-liner** (M3.3); M3.2 CI and M3.3 notarization are macOS-only |
| M4 | ~50% | **Agent-executable spec checklist + drift checks** (M4.2–M4.3; spec-kit is public tooling) |
| M5 | ~55% | **Multi-tenant negative-path test kit** (M5.1–M5.2) |
| M6 | ~40% | **Evidence-cited briefing** — the most portable module; ai_qe is illustration, not load-bearing |
| M7 | ~30% repo / ~50% *course*-specific | only the Type 1 comparator method |
| M8 | ~20% repo / ~60% course-launch-specific | capstone rubric + evidence-record template |

## 8. Missing 2026 topics

Across all nine lessons there are zero hits for "prompt injection", "embedding", "MCP", "tool call", "tracing" or "jailbreak"; "latency" appears only in M2; "eval" hits are "quick evaluation", not LLM evals.

- **Evals** — absent. The nearest analogues are M3.2's contract test and M5's independent oracle. Fits as a fourth tier in M3.2 and as a claim level in M6.
- **Prompt injection / LLM security** — absent, and glaring: M2 feeds untrusted transcript text straight into prompts and fires proactively on it. A "transcript says 'ignore previous instructions'" red-team test belongs beside the cloud-alias red-team in Lab M3.
- **Cost / latency engineering** — only M2.3's budgets; no token-cost model anywhere; M7's pricing ignores inference cost except in one quiz stem.
- **Observability** — no logging or tracing of LLM calls; M5.2's "a log line that warns is observability; the filter in the query is the control" is the natural hook.
- **Retrieval** — the 4,000-character window is the only retrieval.
- **Agent tool design / MCP** — the course uses agents to build but never builds one; a tool schema is a contract (M4 `contracts/`).
- **Deployment for the SaaS type** — M5 stops at tests; the capstone lets a SaaS ship as "public repo tag" instead of a URL.

## 9. Top 15 fixes, ranked by impact

1. **Lab M3 pre-solved** — add a step 0 that removes `privacy.py`, `test_privacy.py`, `test_contract_real_llm.py` and the coverage floor (or ship an `m3-start` branch); align `lab.md`, `solutions.md`, `lab-rubrics.md` and Lab M2's `make lab-m3` gate.
2. **Lab M5 starter** — ship the promised `mini-flow` or rewrite the lab with an honest 6–8 hour budget.
3. **Stale "verified" counts** — 33 → 45; 79/177/143 → 85/188/154; add them to §0.2 (or `06-production/facts.json`) or delete the numbers.
4. **Line-range pointers** — make `verify.py` check `:start-end` ranges and fix `C/m03-privacy-ship/lesson.md:57,61` and `lab.md:23-24`.
5. **Lab M2 step 2 wording** — replace "capture the red output — those failures are your spec" with the exit-4 collection-error reality plus a stub-then-fail step.
6. **Quiz M2 Q3 vs TinyCopilot** — make `role_defaults` pick a distinct Listener, or reword Q3 as Swift-only.
7. **Lab M1 red template** — "→ 2 failed" becomes "→ 1 error (ModuleNotFoundError)", or add "create an empty `todo.py` first".
8. **Remove the author's machine paths** from the four M4 artifacts and the three deep-reads.
9. **M0 first win** — one duration everywhere; move the TinyCopilot suite to stretch; reconcile the pass gate.
10. **Convert recall short answers to application** — M0 Q7, M2 Q7/Q8, M3 Q7, M4 Q7, M8 Q8.
11. **Quiz hygiene** — fix M4 Q5; single-objective keys for M4 Q1/Q5/Q8; rename `Quiz 0/1/4`; delete the invented "6/8 to pass"; pick one number in M8 Q6.
12. **Add prompt injection** — one row in M3.1's claim → enforcement table and a transcript-injection red-team test in Lab M3.
13. **M7 worked pricing for a Type 1 and a Type 2 product** — a cost floor with real inference and hosting numbers and one tier table each, replacing the "this course" example.
14. **Self-paced unblockers** — a scripted agent-session prompt as the default "stranger" for Lab M4, and a self-check alternative to Lab M6's named peer reviewer.
15. **Cut or re-derive unsourced numbers** — "10 current PDF editions", "~460 lines", and the `SignUpFlow/README.md` attribution for the health-score block.

Also: assess M3.3's shipping objective (a tag + checksum step in Lab M3) and M8.2's deliverability objective, since both are taught at length and never checked.
