# Sales Page: Agent-Executable Specs

> Single-playbook page in the eight-section anatomy of `course/04-sales/landing-page.md`: headline, who it is for, problem, outcomes, proof, testimonials, FAQ, pricing with one call to action.

## 1. Headline

**Write specs a fresh agent session can build from, without asking you a single question.**

A checklist, a scripted stranger test and a drift-check script for spec-driven development with coding agents.

## 2. Who it is for, and who it is not for

**For you if you:**
- hand features to coding agents and keep answering the same questions in chat;
- use spec-kit, or write spec, plan and task files by hand, and want a gate before planning;
- have watched generated task files cite paths that do not exist.

**Not for you if you:**
- want a spec-kit installation tutorial (this assumes you can run the tool);
- need product discovery (this starts once you know what to build);
- want a security or compliance review method.

## 3. The problem

An agent that cannot ask questions guesses. It guesses file paths, error keys and limits, and the guesses look like working code. The artifacts that should prevent this are themselves generated. A checklist can grade itself 100% while printing a wrong count. A plan can mark finished files "PENDING". A task can target a directory deleted months earlier. Nobody notices until the agent builds against them.

## 4. What you will be able to do

- Run the spec-kit 1.0 loop with two extra gates: bounded clarification and a requirements checklist that must pass before planning.
- Write stories, scenarios and requirements a test author can assert with no further decisions.
- Prove agent-executability with a scripted stranger test: a fresh session implements story 1 and logs every question; pass is zero spec-owed rows.
- Run a copy-paste drift-check script that exits 1 on unresolved markers and dead paths, and prints the counts and status lines to reconcile.
- Check a spec's numbers against the code that should enforce them.

## 5. Proof

Everything below is checkable in the SignUpFlow repository at commit c550d46.

- The drift-check script was run on a real spec folder on 2026-09-26. It found a self-graded checklist reporting "5xP1" (`SignUpFlow/specs/014-security-hardening/checklists/requirements.md:32`) where the spec has six P1 stories, three artifacts marked "(PENDING)" that exist (`SignUpFlow/specs/014-security-hardening/plan.md:216-219`), and 14 task paths under directories that do not exist, in another spec folder (`SignUpFlow/specs/000-user-onboarding/tasks.md:40`).
- The spec-to-code check found a "blocked for 15 minutes" scenario (`SignUpFlow/specs/014-security-hardening/spec.md:30`) with no lockout in the limiter that enforces login limits (`SignUpFlow/api/utils/rate_limiter.py:108-120`).
- The template rules the playbook quotes were checked against spec-kit v1.0.12 on the same day.

The playbook comes from the AI Product Studio course by Tom Wu, who built SignUpFlow with coding agents (`course/04-sales/landing-page.md`). The findings above are in his own repository, and the playbook publishes them instead of hiding them.

## 6. Testimonials

None yet. No buyer has used this playbook, and this page will not invent one. When real buyers report results, they will appear here in before, after and result form.

## 7. FAQ

**Do I need spec-kit?** No. The method works on hand-written spec, plan and task files. The spec-kit command names are there for readers who use it.

**Which agent?** Any coding agent that can start a fresh session on a clean clone.

**What does the self-check need?** Bash and grep for the script, plus one fresh agent session for the stranger test.

**Does passing mean my spec is right?** No. It means an agent can execute it. The playbook's Limits section says so.

**Is this the whole course?** No. It is one extracted method from the AI Product Studio course, which covers much more.

## 8. Price

**Proposed: $39** (proposed; the owner sets the final price). The course prices a module at about $44 (`course/04-sales/pricing-and-platforms.md:10`); this playbook covers two segments of one module, so it sits just below that rate.

[**Get the playbook →**]
