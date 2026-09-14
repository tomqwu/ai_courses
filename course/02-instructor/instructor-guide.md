# Instructor Guide: AI Product Studio (APS-3)

> How to teach this course — self-paced or 8-week cohort. Read with: `01-design/curriculum.md` (scope), `01-design/assessment-and-rubrics.md` (grading), `04-sales/launch-plan.md` (cohort mechanics).

## 1. What you are teaching (and the one risk to manage)

The course's promise is transformation-by-building: students ship three lab-scale products and the method that produced the real case studies. The single biggest risk is the **Module 2 Chasm** (40–50% drop-off when the first hard lab hits — per the completion research). Your defenses, in order:

1. **M0's 30-minute first win** (solver runs + model pulled) — never skip it; personally welcome every student who posts it.
2. **Objective lab checkpoints** — students never wonder "am I doing this right?" for long; tests tell them.
3. **Weekly discussion prompts** — the +14-point completion lever; respond within 24h for the first three weeks.
4. **Price** — the cohort tier's sunk cost is working *for* you; don't apologize for it.

## 2. Cohort cadence (8 weeks)

| Week | Pre-work (before workshop) | Workshop (90 min) | You grade |
|---|---|---|---|
| 1 | M0 + M1 lessons; Lab M1 started | M1 workshop: I-do (walk a real spec folder from SignUpFlow) / We-do (draft one AGENTS.md rule live) / You-do (students critique a bad rule in pairs) | Quiz M0+M1 |
| 2 | Finish Lab M1; M2 lessons | M2 workshop: live-build `conversation_store.py` TDD against a test; TinyCopilot repo tour | Lab M1 evidence |
| 3 | Lab M2 (TinyCopilot green) | M3 workshop: live red-team of a cloud alias; run `make e2e` live; coverage-floor failure demo | Lab M2 + Quiz M2 |
| 4 | M4 lessons; pick their SaaS feature | M4 workshop: spec one feature live from student suggestions; run the checklist gate on it | Lab M3 evidence |
| 5 | Lab M4 (spec folder) | M5 workshop: tenant-isolation test live; deliberately miswire a route and watch the drift test fail | Lab M4 + Quiz M4 |
| 6 | Lab M5; M6 lessons | M6 workshop: turn one research log entry into a slide + provenance row live; route it two ways | Lab M5 + Quiz M5 |
| 7 | Lab M6; M7 lessons | M7 workshop: price three student products live against the comparators; positioning one-liners | Lab M6 + Quiz M6/M7 |
| 8 | Capstone sprint; M8 lessons | **Demo day**: 5-minute demos, peer rubric scoring, testimonials + feedback interviews | Capstone rubric |

Workshop formula is always **I do / We do / You do** (≈25/35/30 min split). Record everything; recordings go to lifetime access.

## 3. Workshop scripts (core moves)

- **I-do = case study, not slide-reading.** Open the actual repo file on screen (e.g., `SignUpFlow/specs/014-security-hardening/plan.md`, `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift`). Narrate decisions, not lines.
- **We-do = one artifact, live.** Build the smallest complete thing (one rule, one test, one provenance row). Deliberately include one mistake and fix it — students learn recovery, not perfection.
- **You-do = pair work with a binary outcome.** Every exercise ends in something that visibly passes or fails. Debrief by asking "what did the artifact prove?"

## 4. Common stuck points and unblock scripts

| Where students stall | Symptom | Unblock |
|---|---|---|
| M1: "my constitution feels fake" | Empty template values | Have them steal structure, not content: read `SignUpFlow/.specify/memory/constitution.md` (79 lines), then write THEIR three principles. Rules: imperative + verifiable + ≤80 lines |
| M2: mock-LLM tests feel pointless | "When do we use the real model?" | Point at ListenToMe: 96% coverage comes from mockable seams; the real model lives in `make e2e`/Lab M3. Unit tests are the 90%, contract tests the 10% that matters |
| M2: Ollama cloud-only daemon | `ollama list` shows only `:cloud` names | That IS the M3 lab environment. For M2 either pull `qwen3:0.6b` or run roles against a `:cloud` model in CLOUD mode |
| M3: `verify_local_model` fails everything | They have no local model pulled | Intended! The red-team test passes while live mode rejects — that's fail-closed working. Pull `qwen3:0.6b` to see the accept path |
| M4: spec wants to include code | Implementation leakage in spec.md | Run the checklist gate out loud; move the code to plan/contracts; spec stays WHAT |
| M4: writer's block on "real feature" | No SaaS of their own | Default option: extend SignUpFlow itself (it's cloned) — e.g., "swap requests" feature |
| M5: drift test won't fail when miswired | Test compares wrong tables | Check they compare policy file vs. live route table (or fixture registry vs. collected tests), not two static lists |
| M6: "my topic has no data" | Empty provenance table | Use the provided AI-testing-evidence dataset (from the ai_qe research pack) or pick their work domain; rule: no row, no claim — write "not verified" rows instead |
| M7: price anxiety | "Nobody would pay X" | Run the worksheet: floor (costs), comparators (sourced), value anchor (what the artifact replaces). Undercharging 2–5× is the documented failure mode |
| Capstone scope explosion | Trying to build all three | Contract with them: ONE archetype, ONE shippable scope, the loop complete. The rubric scores the loop, not the size |

## 5. Grading workflow (keep it under 3 h/week at 40 students)

- **Quizzes:** auto-grade; scan the item-analysis weekly; if >30% miss a question, re-teach that objective in the workshop's We-do.
- **Labs:** students post evidence in the lab thread; you review Labs M1, M2 (or M4), M5 deeply (the cohort's promised reviews) — others are peer/self-reviewed against the printed checklists. Use the evidence format itself as the grading rubric: commands+outputs present? checklist items honestly binary? limitations listed?
- **Capstone:** score the 5-dimension rubric; peer scores first (demo day), instructor score final. Book 30-minute feedback interviews for the founding cohort (the testimonial trade).

## 6. Academic honesty (the one real rule)

Students may use AI agents for everything — the course teaches that — but their evidence record must say what the agent did and what they verified. A fabricated test output or evidence line is the only automatic fail. Say this in week 1; it's the culture the case-study repos model.

## 7. Self-paced mode adjustments

- Labs are self-verified against the checklists; capstone is peer-reviewed (pair students in the community by week-4 check-in).
- Post a weekly "office hours thread"; pin the top 3 stuck points + unblocks from the table above.
- Award the certificate on evidence (all labs + quizzes ≥75% + capstone ≥80%), not on time.

## 8. Course upkeep (Definition of Done for instructors)

- Keep repo file pointers exact: before each cohort, re-clone the three case-study repos and spot-check every pointer in the lessons (the repos' own rule: search for stale commands, counts, and check names).
- Update evidence numbers (coverage badge, test counts, editions) if the repos changed.
- Log each cohort: NPS, completion %, stuck points, revenue vs. model — an evidence record for the course itself.

## 9. One-page cheat sheet (print for the first workshop)

**The loop:** Study → Spec → Build → Validate → Release → Prove.
**The rules:** imperative & verifiable; tests first; evidence, not vibes; fail closed; ship small; prove the limits.
**The three builds:** TinyCopilot (M2–M3) · Spec-kit + tenant tests (M4–M5) · Mini-briefing (M6).
**The ask:** one archetype, shipped, with evidence, by demo day.