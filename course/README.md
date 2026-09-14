# AI Product Studio — Course Package

**A complete, market-ready online course: "AI Product Studio: Build, Ship & Sell 3 Types of AI Products"**

Built from a deep study of three production open-source repositories by the same engineer — each a different archetype of AI product:

| Archetype | Case-study repo (cloned here) | Proof assets |
|---|---|---|
| 1. Native on-device AI app | `../ListenToMe/` — macOS/iOS meeting copilot | 96% core coverage · notarized releases · 12-competitor analysis |
| 2. Spec-driven AI SaaS | `../SignUpFlow/` — volunteer-scheduling platform | 1,464 dated tests · 7 tiers · 17 spec folders |
| 3. Expertise content product | `../ai_qe/` — "AI × QE" briefing site | 116 cited slides · provenance · published self-audit |

## What's in this package

```
course/
├── README.md                       ← you are here (package map)
├── 00-research/                    ← the deep research behind the course
│   ├── 00-synthesis.md            ← the unified method (Spec-to-Ship Loop) drawn from all 3 repos
│   ├── 01-listentome-deep-read.md ← architecture, privacy engineering, release discipline (with file pointers)
│   ├── 02-signupflow-deep-read.md ← spec-kit methodology, 7-tier testing, multi-tenant security
│   ├── 02-course-market-research.md ← how to create/sell courses: frameworks, completion stats, pricing, platforms (all cited)
│   └── 03-ai-qe-deep-read.md      ← evidence discipline, audience routing, editions, consulting funnel
├── 01-design/                      ← course design (read first)
│   ├── positioning.md             ← concept, audience, promise, differentiation, pricing ladder, voice standards
│   ├── curriculum.md              ← master syllabus: 9 modules, objectives, labs, quizzes (the authoring brief)
│   └── assessment-and-rubrics.md  ← grading weights, quiz rules, lab standard, capstone rubric
├── 02-instructor/
│   └── instructor-guide.md         ← cohort cadence, workshop scripts (I do/We do/You do), stuck-point table, grading workflow
├── 03-content/                    ← the course itself (9 modules)
│   ├── m00-orientation/           ← lesson + lab + quiz
│   ├── m01-operating-system/     ← lesson + lab + quiz
│   ├── m02-ondevice-app/         ← lesson + lab + quiz + tinycopilot/ (runnable, tested lab code)
│   ├── m03-privacy-ship/         ← lesson + lab + quiz
│   ├── m04-spec-driven-saas/      ← lesson + lab + quiz
│   ├── m05-security-tests/        ← lesson + lab + quiz
│   ├── m06-expertise-product/    ← lesson + lab + quiz + evidence-dataset.md (student-facing claims data)
│   ├── m07-monetize/             ← lesson + lab + quiz
│   └── m08-launch-capstone/      ← lesson + lab (capstone) + quiz
└── 04-sales/                       ← the course's own go-to-market
    ├── landing-page.md           ← complete sales-page copy (~2,250 words, publish-ready)
    ├── pricing-and-platforms.md  ← price ladder ($399 self-paced / $1,490 cohort / $2.5k team) with decision record
    ├── launch-plan.md            ← launch timeline, 7-email arc, operations checklist, metrics
    └── lead-product-teardown.md  ← the free lead product (3-email mini-course + 10-point checklist)
```

## How to use this package

**To understand the course:** read `01-design/positioning.md`, then `01-design/curriculum.md`.

**To teach it:** start with `02-instructor/instructor-guide.md`. Each module folder contains the master lesson (readable as-is, or record each `M#.#` segment as a 5–15 minute video), the lab (with objective acceptance checklists), and the quiz (with answer keys).

**To run the labs yourself:** the Module 2/3 labs use `03-content/m02-ondevice-app/tinycopilot/` — a complete, tested Python reference implementation that mirrors ListenToMe's architecture (see its README). **Verified status as shipped:** `make lab-m2` → 191 passed, 100% coverage (floor 90 enforced); `make lab-m3` → 49 passed; `make e2e` → 2 passed against a live Ollama daemon; `make demo` → three role outputs. Requirements: Python 3.11+ (TinyCopilot itself also runs on 3.10), pytest, httpx, and Ollama (`ollama pull qwen3:0.6b` for a local model).

**To sell it:** `04-sales/` is publish-ready: landing-page copy, pricing rationale grounded in 2025–26 platform benchmarks, and a full launch plan with the 7-email arc.

## Course at a glance

- **9 modules · 27 lesson segments · 9 labs (incl. the capstone) · 72 quiz questions (8 per module)**
- Formats: self-paced ($399) or 8-week cohort ($1,490) — see `04-sales/pricing-and-platforms.md`
- Core labs: Python + Ollama (macOS/Linux/Windows); Swift stretch track maps labs onto the real ListenToMe code
- Every claim in every file carries a source pointer — the course practices the evidence discipline it teaches

## Honesty notes (the standard this package holds itself to)

- All facts about the three case-study repos were read from the cloned repos in this workspace and carry file pointers; verify before publishing (repos evolve).
- Market-research claims cite their sources in `00-research/02-course-market-research.md`; stats like completion rates and price bands are industry research, not guarantees.
- Testimonials do not exist yet: the landing page reserves slots and says so. Run the founding cohort first (see `04-sales/launch-plan.md`).