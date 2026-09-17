# Course Positioning & Concept

## Course name

**AI Product Studio: Build, Ship & Sell 3 Types of AI Products**

- Short name: **AI Product Studio**
- Course code: **APS-3** (used in file/module naming)
- Tagline: *Study three real, shipped AI products. Build your own. Sell what you build.*

## The transformation promise (backward design outcome)

By the end of this course, you will have **built the working core of three portfolio-grade AI products** — an on-device AI app, a spec-driven SaaS feature set, and an evidence-based expertise product — using the same AI-assisted workflow that shipped the three production open-source apps you study in class. You will leave with public repositories, recorded validation evidence, a pricing and positioning package for the product you choose to take to market, and a repeatable operating system for shipping your next one.

One sentence: **"Ship three types of AI products from real open-source codebases — and leave with the skills, public repos, and sales assets to build and sell your own."**

## The three archetypes (and why these three)

The course is built around three production repositories by the same engineer, each representing a distinct *type* of AI product — together covering essentially the whole space of things a solo technical builder can ship:

| # | Archetype | Case-study repo | You build (lab track) | Monetization pattern |
|---|---|---|---|---|
| 1 | **The native on-device AI app** — private, real-time, model-optional | ListenToMe (macOS/iOS meeting copilot; 96% core coverage; signed public releases) | **TinyCopilot** — a working multi-role AI copilot core with local model routing (Python/Ollama; Swift stretch goal) | One-time purchase / open-source + reputation (category rivals: $8–149/mo) |
| 2 | **The spec-driven AI SaaS** — multi-tenant, agent-built, production-tested | SignUpFlow (FastAPI volunteer-scheduling SaaS; 17 spec folders; 1,464 tests across 7 tiers) | A **real feature of your own SaaS**, specced with the full spec-kit workflow and hardened with tenant tests | SaaS subscription (billing gated until proven) |
| 3 | **The expertise content product** — research-backed, audience-routed, evidence-cited | AI × QE (116 narrated slides, provenance files, editioned releases, consulting funnel) | A **mini-briefing** — a 12-slide evidence-cited deck with two audience routes and a provenance table | Consulting / workshops / content products |

**Why it works:** the three types have *different* technical centers of gravity (edge AI + privacy engineering; server-side architecture + security; research + content ops) but the *same* underlying method — the Spec-to-Ship Loop. Students learn the method once and see it instantiated three times, which is what makes it stick.

## Target audience

**Primary:** intermediate software engineers (≈2+ years experience) who want to (a) build real AI products, (b) use AI coding agents professionally instead of casually, and (c) eventually monetize what they build. Comfortable with Python **or** Swift, git, and the command line. No prior LLM/API experience assumed; no Mac required for the core labs (Ollama runs on all major OSes; Swift is a stretch track).

**Secondary:** indie hackers and technical founders choosing their first AI product; senior engineers, tech leads and consultants who want to productize their expertise (archetype 3 maps directly to consulting offerings).

**Not for:** absolute coding beginners; people who want prompt-engineering trivia or "AI side hustle" content without shipping anything; teams seeking an AI-governance compliance course (that's a different, enterprise product).

## Differentiators (why this course, honestly stated)

1. **Real production codebases, not toy apps.** Students clone and study three apps that actually shipped: ListenToMe (MIT, notarized releases, 96% core test coverage, 13-competitor analysis in-repo), SignUpFlow (1,464 passing tests recorded with dates and SHAs, 17 spec-kit feature folders, executable authorization matrix), AI × QE (116 slides with per-claim provenance, published self-audit with remediations). Every case-study claim in the course cites a file students can open.
2. **The method is the product.** Most AI courses teach API calls. This one teaches the *operating system* — constitution, agent rule files, spec-kit, evidence discipline, playbook acceptance — that lets one engineer ship three product types with AI agents doing the heavy lifting.
3. **Monetization is built in, per archetype.** App pricing (one-time vs subscription, from the ListenToMe competitive table), SaaS packaging (feature-gating, billing readiness from SignUpFlow), and expertise-product funnels (questionnaire → discovery → phased pilot from AI × QE). Module 7 turns each student's own build into a priced, packaged offer.
4. **The course practices what it teaches.** Claims are sourced and qualified exactly the way the source repos do it — every number in this course package carries its evidence pointer. Students are taught to demand this standard, and see it modeled in their own materials.

## Proof assets (to display on the sales page)

- ListenToMe: 96% core coverage badge, signed DMG releases, competition table (Granola ~$14–35/user/mo, Otter ~$8–30, Cluely $19.99–149.99/mo — vs free/open-source).
- SignUpFlow: dated evidence "1,464 passed / 21 skipped (2026-09-12)", 7-tier pyramid diagram, coverage.json manifest, spec-kit folder tree.
- AI × QE: 116 slides / 4 decks / 10 PDFs, research log with "not verified" sections, self-audit remediation table, edition changelog.

## Course format

- **9 modules** (M0 orientation + M1–M8): 27 lesson segments total (3 per module, 5–15 min each as videos; the written lessons here are the master scripts).
- **Every lesson ends with an action step** (a commit, a test run, or a discussion post). Every module ends with a **lab** whose acceptance is objective (tests pass, artifact deploys, table reconciles) and a **quiz** (8 questions, answer key included).
- **Self-paced or 8-week cohort.** Cohort cadence: one module per week, weekly 90-minute "I do / We do / You do" workshop, capstone demo day in week 8; drip during the cohort, then lifetime access unlocks.
- **Language/stack note:** core labs are Python + Ollama (runs anywhere, free); Swift tracks are provided as stretch goals for Mac/iOS developers using ListenToMe itself as the reference implementation.

## Pricing (grounded in 2025–26 platform research)

| Tier | Price | Contents |
|---|---|---|
| **Free lead product** | $0 | *The 30-Minute AI Product Teardown* (Gumroad/YouTube) — teardown of one repo, seed email list |
| **Studio (self-paced)** | **$399** | All modules, labs, quizzes, community access, capstone rubric (self-grade) |
| **Studio Live (cohort)** | **$1,490** | 8-week cohort: weekly workshops, instructor code review on 3 labs, capstone review + demo day. Beta cohort #1: $990 in exchange for testimonials |
| **Team (enterprise)** | **$2,500–4,000** (3–5 seats) | Private cohort or workshop, private code review, team capstone review |

Rationale: Maven's published benchmarks put technical cohorts with 12–20 live hours + projects + capstone at $1,800–2,450; our first cohort is priced at the entry of that band and the beta discount buys testimonials. Self-paced at ~27% of cohort price matches the "fraction of live price" rule with community and projects retained. Expected completion is boosted by price (research: $500–1,500 programs complete at 53–68%) and by the weekly lab checkpoints.

## Platform plan

- **Cohort:** Maven (cohort-native, technical audience, ≥$950 price points earn best per-visit) — or Thinkific if self-managing.
- **Self-paced:** Thinkific or Teachable (sales pages + payments).
- **Community:** Circle or Discord (lesson-level discussion prompts are the +14-point completion lever).
- **Lead product:** Gumroad.
- **Never:** Udemy as primary (37% payout, $9.99 pricing, no email export).

## Naming, voice, and standards for all course materials

- Address the student as **you**; instructor voice is first person, direct, warm but exact.
- **Every factual claim about the three repos carries a file pointer** (e.g., `SignUpFlow/AGENTS.md`, `docs/TESTING.md`) — students must be able to verify everything.
- **No hype numbers.** If a stat is self-reported or vendor-sponsored, label it. Borrow AI × QE's four claim levels where relevant.
- Imperative, verifiable instructions (the repos' own house style): "Run X", "Add Y to Z", never "consider adding".
- Modules are numbered M0–M8; lesson segments M#.# (e.g., M2.3); labs `Lab M#`; quizzes `Quiz M#`. Checkpoints are phrased as pass/fail artifacts.