# AI Product Studio — complete narration transcript

Every word spoken in the course, in order. The words are the approved narration scripts; they match the captions word for word and do not change when the release voice is recorded.

- [M0 — Orientation: Three Products, One Method](#m00) — 19 slides, 10m 2s
- [M1 — The AI Product Operating System](#m01) — 25 slides, 14m 23s
- [M2 — The On-Device AI App: Architecture](#m02) — 26 slides, 15m 4s
- [M3 — The On-Device AI App: Privacy, Testing, Shipping](#m03) — 27 slides, 14m 58s
- [M4 — The Spec-Driven SaaS: From Idea to Executable Spec](#m04) — 28 slides, 18m 16s
- [M5 — Multi-Tenant Security & the Acceptance Gate](#m05) — 25 slides, 16m 32s
- [M6 — The Expertise Product: Evidence, Routing, Editions](#m06) — 28 slides, 16m 14s
- [M7 — Monetize: Pricing, Packaging, Positioning](#m07) — 28 slides, 15m 47s
- [M8 — Launch: Sales Page, Email Arc, Capstone](#m08) — 27 slides, 14m 21s

<a id="m00"></a>

# M0 — Orientation: Three Products, One Method
## Narration transcript

**19 slides · 19 narrated · 10m 2s of audio**

**Voice:** mixed — 18 of 19 recordings are preview audio spoken by a synthesized voice; the rest were recorded separately. The words below are the approved narration.

The text below is what is spoken on each slide, in order. It is the same text as the captions and the approved narration script, checked word for word by `course/06-production/narration/validate_narration.py`.

---

### Slide 1

*27.4s · character-alignment*

> Welcome. In the next thirty minutes you will not watch anyone else build anything. You will clone three real products, run one of them end to end, and pull a local model onto your own machine. The promise of this module is real production software running before Module 1, with no prerequisites. By the end you will have three repos cloned, one solver run, and one local model. Keep a terminal open beside this video.

### Slide 2 — By the end you can…

*23.2s · sentence-measured*

> These six outcomes are the quiz blueprint and the lab checklist, so treat them as the contract for this module. Notice the verbs: describe, name, explain, run, pull, post. Every one of them is something checkable from an artifact you paste, and none of them is understand. That standard is copied from the case-study repos themselves: if it cannot be observed, it does not count as done.

### Slide 3 — M0.1 — Three archetypes, one method

*23.4s · sentence-measured*

> Almost everything a solo technical builder can ship falls into one of three shapes. Type 1 is a native on-device AI app, type 2 is a spec-driven AI SaaS, and type 3 is an expertise content product. Their technical centers of gravity barely overlap. The method behind them does, and that is the whole pedagogical bet of this course: you learn the method once and watch it instantiated three times.

### Slide 4 — Type 1 — ListenToMe (on-device app)

*31.2s · sentence-measured*

> ListenToMe is a real macOS meeting copilot you can download and run. It captures your microphone and the meeting's system audio, transcribes locally, then streams AI answers through whichever model you pick: local Ollama, or a cloud provider with your own key. Its proof assets are openable files. The 96% core-coverage badge in the README is a number produced by a test run, not a marketing line. The competition analysis is fourteen rows, each claim sourced and dated, which is positioning work done as research.

### Slide 5 — Type 2 — SignUpFlow (spec-driven SaaS)

*34.9s · sentence-measured*

> SignUpFlow schedules volunteers for churches, leagues, and non-profits, built on FastAPI and SQLAlchemy. A greedy solver auto-generates fair rosters: YAML workspace in, JSON solution out. Every feature starts as a specification folder and ends as tested code, and seventeen of those folders exist today. The proof asset is a dated evidence line in a validation playbook: 1,464 passed, 21 skipped. The skips are counted, not hidden, and in Module 5 you will learn why that record is more valuable than a green badge.

### Slide 6 — Type 3 — AI × QE (expertise product)

*34.2s · sentence-measured*

> The third archetype is content as a product: a research-backed briefing site on AI in quality engineering. It ships 116 narrated slides across four decks and ten current PDF editions; the 116 figure is 21 plus 33 plus 26 plus 36, defined in the briefing-room data file. What makes it credible is not the volume. Every claim carries provenance, and the author published a fourteen-finding audit of his own site. He is more skeptical of his own claims than his audience is, and that is the entire sales strategy for a type 3 product.

### Slide 7 — Production-grade means proof you can open

*38.8s · sentence-measured*

> Here is the definition this course runs on: production-grade means a shipped artifact with proof you can open and verify — and all three proofs are now on the slide, verbatim. The on-device app shows a ninety-six percent core-coverage badge in its README. The spec-driven SaaS shows the line 1,464 passed, 21 skipped, dated. The expertise product carries a fourteen-finding self-audit, reviewed edition one point two one. Every asset is a file, dated or machine-checkable, and none of them is a testimonial. A finished claim in a README, or a repository merely existing, is not evidence, and your labs are graded against this same bar.

### Slide 8 — M0.2 — The Spec-to-Ship Loop

*35.8s · sentence-measured*

> The Spec-to-Ship Loop has six stages, and you will run all six in every module: Study, Spec, Build, Validate, Release, Prove. Study produces research, competition, and positioning, which is an artifact rather than a slogan. Spec produces something a fresh agent session could execute without conversation memory. Build is tests first, in small reviewable edits. Validate is tests, coverage floors, and playbooks, which is a record rather than a feeling. Release is signing, editioning, and deploying. Prove is the honest account of what was verified and what was not.

### Slide 9 — Stages 1–3 — real artifacts

*32.7s · sentence-measured*

> Open each of these files as you go. The fourteen-row competitor table is Study, because positioning is research you can cite. The first principle in the AI and QE principles file is literally baseline before solutioning: measure before you claim. Spec appears as Given/When/Then acceptance stories in a security-hardening spec. Note that spec 014 has no tasks file, so the tasks format is best read from spec 019, which has one. Build turns a spec into checkbox tasks that cite exact file paths, tests first.

### Slide 10 — Stages 4–6 — real artifacts

*32.3s · sentence-measured*

> Validate is where most builders stop. ListenToMe enforces a ninety-five percent coverage floor with a script, and SignUpFlow runs seven test tiers in separate processes with dated counts. Release is signing and notarizing: the ListenToMe agent file requires signed, notarized DMGs that target an exact source commit. Then look at Prove, in the last row. A review told the author not to promote a build that already had 97.24% coverage. That decision is the rarest artifact in software, and it is the spine of this course.

### Slide 11 — Prove is the spine

*29.3s · sentence-measured*

> Read SignUpFlow's validation playbook and you will find the engineer listing his own failures: a browser click race that made a test flaky, and a type-checking debt line that says explicitly, not a pass. He could have deleted both lines. Keeping them is what makes the passing numbers believable. Tests validate what you built; evidence discipline validates what you shipped. When you write your capstone evidence record, the failures section is not optional, because a record with no limitations reads as unverified.

### Slide 12 — M0.3 — Set up and get your first win

*33.2s · sentence-measured*

> Everything in this segment is a command you type, not a concept you remember. Clone the three case studies, verify you have Python 3.11 or newer, install Ollama and pull a small local model, run SignUpFlow's solver on the sample data, and post your first win. The whole sequence takes about thirty minutes, and most of that is download time. Do it in order, and before Module 1 do not skip the TinyCopilot test suite. It is the exact acceptance gate you will re-implement in Module 2, and seeing it green now tells you your environment is real.

### Slide 13 — First ship-win — clone and run the solver

*36.7s · sentence-measured*

> Clone the three repositories first, then, inside SignUpFlow, run make setup. That installs the Poetry environment, runs migrations, and seeds data. The init command writes three YAML files: organization, people, and events. The solve command runs the real greedy scheduler. On the sample workspace it prints a health-score line, the violation counts, and a fairness standard deviation. The numbers are whatever the revision you cloned produces; at the current head the sample scores zero out of one hundred with two hard violations, and that is fine. Capture the whole block around the health-score line and keep the raw terminal output, because the run record is your first artifact, not the number. Do not retype it from memory.

### Slide 14 — Local LLM in three commands

*29.1s · sentence-measured*

> Install Ollama first, then run ollama pull qwen3:0.6b to fetch a small model, and check ollama list to confirm it is there. The run command is your first local completion: one prompt, one answer, entirely on your hardware. There is no API key and no cloud bill, and no transcript leaves your machine. Module 2 builds a copilot on exactly this foundation. Look at the list output carefully, because it is also the diagnostic for the one environment quirk in this lab.

### Slide 15 — Two valid environments (say which you have)

*36.0s · sentence-measured*

> I want to be explicit, because students with an unusual daemon sometimes think they are blocked. If ollama list shows the local model qwen3:0.6b, you have a local setup. If every name it shows ends in the cloud suffix, those are cloud-backed aliases, not local models, and you are still not blocked: that environment is valid for Module 0 and Module 2. For Module 2 you either pull a genuinely local model or run roles in cloud mode. Module 3's privacy lab is richer with a local model, and the fail-closed test passes either way. State which environment you have in your first-win post.

### Slide 16 — Lab M0 — Environment Setup & First Ship-Win

*35.0s · sentence-measured*

> The lab has five steps and a six-item acceptance checklist: clone the repos, check your Python version, install Ollama, run the solver, start your evidence log, and post to the community. The goal is every tool installed and proven with real output, and the pass gate is two things: the solver block with its health-score line, and an ollama list showing at least one model. Before Module 1, run the TinyCopilot suite; it is the Module 2 gate, green or a missing dependency you can name. If a dependency is missing, name the exact package in your evidence log instead of guessing. An honest partial is a pass; an invented green is the only automatic fail.

### Slide 17 — Quiz M0

*32.7s · sentence-measured*

> The quiz has eight questions: six multiple choice and two short answer, covering archetypes, proof assets, loop stages, and your environment. It is open-book by design, because the file pointers are the point. The two short-answer questions are graded against a model answer, so write them as applications, not definitions. One asks for the exact two solver commands after setup and the line to capture. Another hands you a friend's product idea and asks which archetype it is and which repo to study. Take the quiz after the lab, not before.

### Slide 18 — Recap

*30.6s · sentence-measured*

> If you remember three things, make them these. Each archetype has a distinct proof asset. The loop has six stages, Study, Spec, Build, Validate, Release, and Prove, with a real artifact at every stage. And Prove is the stage that separates a portfolio project from a product, because it means recording failures too. You have already run a production scheduler and a local language model before Module 1. That first win is banked, so paste both outputs into your evidence log with the date on each entry.

### Slide 19 — Discussion prompt

*25.6s · sentence-measured*

> Your first-win post has three parts: the solver output including the health-score line, your ollama list, and one sentence naming which archetype you want to build by week eight. Then the real question. Which proof asset from this module surprised you, and would it survive a skeptical customer opening the file? Reply to one other student and tell them which archetype you think their goal belongs to. If you disagree with them, say why and point at the file.

<a id="m01"></a>

# M1 — The AI Product Operating System
## Narration transcript

**25 slides · 25 narrated · 14m 23s of audio**

**Voice:** preview narration — a free local voice, not the finished release recording. The audio is spoken by a synthesized voice, not a human recording. The words below are the approved narration and do not change when the release voice is recorded.

The text below is what is spoken on each slide, in order. It is the same text as the captions and the approved narration script, checked word for word by `course/06-production/narration/validate_narration.py`.

---

### Slide 1

*35.5s · sentence-measured*

> Welcome to Module 1, the AI product operating system. Module 0 gave you three shipped products and one loop. This module hands you the machinery that made them shippable by one engineer working with AI agents: governance, specification, and evidence discipline. The promise is simple. You govern agents, specify work, and record evidence, all inside your own repository. We cover three segments in about sixty minutes. By the end you will have written your own constitution and AGENTS.md and run one complete spec-to-TDD loop. That artifact is the deliverable, not the notes.

### Slide 2 — By the end you can…

*35.6s · sentence-measured*

> Here are the four capabilities this module delivers, and each one is checkable. Notice they are verbs: write, apply, turn, record. Not understand governance. You will write layered agent rules that are imperative, verifiable, and under about two hundred lines. You will apply the five-level instruction hierarchy and the anti-hallucination rules. You will turn one story into a scenario and a task. And you will record validation evidence with commands, counts, the date, limits, and the head SHA. The lab closes the loop with one red-then-green pytest run, recorded honestly.

### Slide 3 — Why governance comes before product type

*29.6s · sentence-measured*

> This is the module's core argument. Agents do not replace process; they raise the stakes for it. Code now appears at agent speed, while verification stays at human speed. So the bottleneck moves: specifying what you want, verifying what you got, and admitting the limits of what was actually validated. The product archetypes differ in what they build, never in how they govern the build. Most builders skip this part and pay for it later. SignUpFlow's deep read makes the same point in its first section.

### Slide 4 — Segment M1.1 — The four-file instruction stack

*30.0s · sentence-measured*

> Segment one is governance, and it starts with the stack. Four files, one canonical source. The baseline lives in AGENTS.md, and Codex CLI, Cursor, Aider, Jules, OpenHands, Sourcegraph Amp, and Factory all read it. Claude Code does not read AGENTS.md natively, so CLAUDE.md links to it at the top and adds Claude-specific addenda. Copilot needs its own restatement file under .github. The constitution sits above all of the agent files as the single source of truth.

### Slide 5 — Proof: the stack, with real line counts

*37.3s · sentence-measured*

> These lengths are real, and you can check them yourself — and the constitution's own head is now on the slide. The constitution is eighty-five lines, and it opens with one sentence of purpose: a roster and scheduling system with email and SMS notifications. AGENTS.md is one hundred eighty-eight. CLAUDE.md is one hundred fifty-four, and the Copilot instructions file is one hundred twenty-seven. All four sit under the roughly two-hundred-line cap that the house style sets. Open them in your own clone and count if you want to verify. Why the cap matters: a rule file an agent cannot hold in context is a rule file it will not follow.

### Slide 6 — House style: a rule must be verifiable

*30.3s · sentence-measured*

> This is the heart of the house style. Every rule must be verifiable. Write in imperative voice, not as a suggestion. A stranger should be able to check whether the rule was followed without asking you anything. Numbers beat adjectives, which is why the cap is stated as under roughly two hundred lines. Commands beat prose, so name the exact check. The repo states the contrast directly: filter every query by org_id, not be careful with multi-tenancy. A rule an agent cannot check is a vibe, not a rule.

### Slide 7 — The contrast table

*33.5s · sentence-measured*

> Here are four rewrites, all drawn from AGENTS.md. Watch what changes each time. Be careful with multi-tenancy becomes a filter on org_id. Keep files manageable becomes a number: each file under about two hundred lines. Value test coverage becomes an action plus a check command: write tests first, run make test-unit. And handle secrets safely becomes a greppable prohibition: never commit secrets, read them from environment variables. Careful cannot be executed or checked; a filter can. In the lab you will rewrite rules like these yourself.

### Slide 8 — What a constitution holds

*34.2s · sentence-measured*

> A constitution is not a longer AGENTS.md. It holds only the few things that must never drift. SignUpFlow's version is eighty-five lines with four principles: Native First, which prefers plain Poetry and SQLite over Docker locally; Test-Driven Implementation; Simplicity and YAGNI; and Safety and Reliability. Safety is concrete. Email and SMS are disabled by default, and payments must be mocked or disabled locally. Autonomy is fixed too: YOLO mode is disabled, and agents may commit finished work but never run unchecked destructive commands.

### Slide 9 — Precedence: five levels, one tie-breaker

*32.7s · sentence-measured*

> When rules overlap, AGENTS.md gives you five levels and one tie-breaker. First, the user's request in the current task. Second, repository rules in CLAUDE.md and AGENTS.md. Third, path-scoped rules under the .github instructions folder. Fourth, general guidance from the AI agent coding strategy doc. Fifth, inferred best practice. The tie-breaker is the sentence to memorize: follow the more specific and safer one. That is how a specific path rule can beat a general baseline without anyone maintaining a precedence matrix.

### Slide 10 — Anti-hallucination rules

*34.5s · sentence-measured*

> Hallucination is the biggest failure mode of agent-assisted work, so it gets rules rather than advice. Do not invent file paths, function names, route paths, commands, URLs, or identifiers. Grep the repo before referencing anything. For facts like schema fields and environment variable names, read them from the canonical source; do not recall from memory. When a request is ambiguous, present two or three differentiated options instead of guessing. And encode a hard-stop checklist for research tasks. Each of these is checkable against a transcript.

### Slide 11 — How rules graduate

*29.7s · sentence-measured*

> New rules do not go straight into AGENTS.md. They graduate. An observation is recorded in the research log, which exists so that exploratory notes never become silent rules. The rule is then tested on at least one real change. Only after that is it promoted into AGENTS.md. The source row moves from pending to extracted to promoted. And if the rule generalizes, it is upstreamed to the shared GenAI Common repository. Rules earn their place the way features do: by surviving contact with real work.

### Slide 12 — Segment M1.2 — The spec-kit pipeline

*34.9s · sentence-measured*

> Segment two is specification. SignUpFlow builds features through GitHub's spec-kit slash commands, in this order: constitution, specify, clarify, plan, checklist, tasks, analyze, and implement. Each step produces a file, and those files are the interface between your intent and an agent session that has no memory of your conversation. The output is a folder of artifacts under specs. Seventeen spec folders exist in the repo today, so this is not theory. The pipeline's answer to the agent did the wrong thing is almost always the spec did not say.

### Slide 13 — Each artifact has one job

*37.3s · sentence-measured*

> Each artifact has exactly one job, and this table is the spine of the segment. The spec file is the what: prioritized P1, P2, and P3 stories with Given/When/Then scenarios, and it stays technology-agnostic. Research and plan hold the decisions and the how, with plan behind a Constitution Check gate. Data-model defines entities and relationships before code exists. Contracts hold per-domain interfaces, errors, and test sketches. Checklists are the quality gate before planning, while quickstart is the timed deployment path. Tasks are checkbox items with exact file paths.

### Slide 14 — Proof: the artifacts are real files

*35.5s · sentence-measured*

> This is proof, not description — and the real task lines are now on the slide. Seventeen folders sit under the SignUpFlow specs directory. Spec nineteen's task list reads: T027, implement POST /api/sms/send endpoint per contracts/sms-api.md in api/routers/sms.py — and T028 right below it, the message-history endpoint. The Constitution gate lives in spec fourteen's plan. And spec fourteen has no tasks file at all. A folder that stops at planning is a legitimate state, and the record says so rather than inventing a file that is not there.

### Slide 15 — Story → scenario → task

*36.5s · sentence-measured*

> Watch the abstraction drop. A sentence of intent becomes a checkable scenario, and then a task. The story is: as a volunteer, I can block dates so the solver skips me. The scenario gets concrete: given a blocked period covering a specific date, when an admin runs the solver, then the volunteer receives no assignment and the solution reports zero hard violations. The task line carries an ID, a priority marker, and a story tag, plus exact file paths, and it names the contract, the test file, and the order of work. Test first: the failing test is the task's first deliverable.

### Slide 16 — ListenToMe's variant: protocols and non-goals

*34.9s · sentence-measured*

> ListenToMe runs the same discipline in Swift. Its design spec pins protocol-level interfaces with exact Swift signatures so implementations stay swappable: AudioCapturing and Transcribing. It also writes down YAGNI non-goals: no cloud backend, no accounts, no billing, no multi-user, and no covert or stealth mode. Its implementation plan is a two-thousand-four-hundred-ten-line TDD task list that ends with a self-review mapping every spec bullet to tasks. On-device speech-to-text behind a swappable Transcribing protocol maps to tasks ten and thirteen, checked.

### Slide 17 — Segment M1.3 — No CI checks, by policy

*32.9s · sentence-measured*

> Segment three is evidence discipline. SignUpFlow runs no CI checks, and that is deliberate: a tested policy, not an omission. The constitution's Current Validation Policy says to run everything locally and never recreate hosted checks or require CI statuses. There is even a policy-regression test guarding that rule. The argument is this. A hosted check tells you pass or fail and nothing about the commands, the environment, or the limits. So the evidence travels with the revision instead. A hosted check is a snapshot; evidence is a record.

### Slide 18 — Proof: the evidence line

*43.3s · sentence-measured*

> Here is the full-suite line from Module 0, and here is where it lives: the validation playbook in the SignUpFlow docs, not TESTING.md. Four hundred twenty unit tests passed, with twenty-one skipped. Four hundred forty-four API tests, sixteen CLI tests, and three hundred twenty-five integration tests passed. Across the backend, web, contract, and browser suites, one thousand four hundred sixty-four passed and twenty-one skipped. Note the second bullet carefully: the file is dated September twelfth, twenty twenty-six, and was demoted to historical reference the next day. It is evidence of a past run, not a live status badge. The follow-up validation starts from a pinned head SHA.

### Slide 19 — Include the failures

*32.3s · sentence-measured*

> The record's hardest discipline is what it includes. Three moves. First, a real failure is named: an older recurring-event browser test exposed a click race, the fix is recorded, and the initial failure stays in the document rather than being hidden. Second, known debt is named as debt: full API mypy has eight hundred thirty-five errors in forty files, and the record says not a pass instead of rounding it away. Third, the record closes with limits, listing what was not verified. An evidence record that cannot say not verified is marketing.

### Slide 20 — Done means verified in the shipped thing

*40.0s · sentence-measured*

> Tests validate what you built; the Definition of Done validates what you shipped. ListenToMe requires the maintainer to verify affected behavior in the installed production app. For audio changes, you verify actual system-audio transcription labeled OTHERS; a permission toggle or microphone pickup is not proof. Its checklist also states that stale docs are a Definition-of-Done failure, not a follow-up. And the strongest artifact in all three repos is a gap review recommending against promoting version one point three point zero, despite two hundred fifteen passing Core tests and ninety-seven point two four percent coverage, because those numbers do not establish capture reliability.

### Slide 21 — Your evidence-log template

*31.6s · sentence-measured*

> Copy this template verbatim and use it in every lab for the rest of the course. It has five fields: the heading with project, feature, and date; the commands with their results in passed, skipped, and failed counts; the environment with operating system and Python version; the revision from git rev-parse HEAD; and the limitations, which must include at least one entry. If a run failed and you fixed it and re-ran, record both lines. The field students leave empty is limitations, and that is exactly the field that separates a record from a badge.

### Slide 22 — Lab M1 — build your operating system

*35.1s · sentence-measured*

> Now you build your own version of all of it. Lab M1 takes about two hours. You create a starter repo and write a constitution of at most eighty lines and an AGENTS.md of at most two hundred. Then a spec folder for a small todo command feature: the spec, a plan with its gate, and tasks. Then you run the TDD loop for real: failing test first, watch it fail, implement, watch pytest pass. You record the red run, the green run, the environment, the head SHA, and your limitations. The pass gate is objective: the artifacts exist and pytest exits zero.

### Slide 23 — Quiz M1

*34.2s · sentence-measured*

> Check your understanding before the workshop. Quiz M1 has eight questions: six multiple choice and two short answer. It covers rule verifiability, the precedence hierarchy, the job of each spec-kit artifact, and evidence discipline. The short answers are applications, not recall. Question seven asks you to write a Given/When/Then scenario plus a task line. Question eight asks for a full evidence entry that keeps a flaky failure visible. Take the quiz before the workshop, because the labs are graded on evidence, and we want live time for the rules you rewrote.

### Slide 24 — Recap

*45.8s · sentence-measured*

> Six lines, one idea each. Governance: a eighty-five-line constitution above a one-hundred-eighty-eight-line baseline, with every rule verifiable. Precedence: five levels, and the more specific and safer rule wins. Anti-hallucination: grep first, read canonical sources, offer options when a request is ambiguous. The spec pipeline: what, then decisions, then how, then tasks. Evidence: commands, counts, date, environment, limits, and head SHA, with the failures included, because not a pass is a valid result. If you remember nothing else: a rule you cannot check is a vibe, a spec without exact paths is not executable, and an evidence record without limitations is marketing.

### Slide 25 — Discussion prompt

*26.6s · sentence-measured*

> One discussion prompt to close the module. Post the vague rule and its verifiable rewrite, your before and after. Post the evidence entry you wrote from Module 0. Then read two classmates' AGENTS.md rules and answer a single question: could you personally check whether their rule was followed, without asking them anything? If not, name the exact word that makes it uncheckable. That comment is the whole skill. It is the same test this repo applies to itself.

<a id="m02"></a>

# M2 — The On-Device AI App: Architecture
## Narration transcript

**26 slides · 26 narrated · 15m 4s of audio**

**Voice:** preview narration — a free local voice, not the finished release recording. The audio is spoken by a synthesized voice, not a human recording. The words below are the approved narration and do not change when the release voice is recorded.

The text below is what is spoken on each slide, in order. It is the same text as the captions and the approved narration script, checked word for word by `course/06-production/narration/validate_narration.py`.

---

### Slide 1

*29.6s · sentence-measured*

> Welcome to Module 2, The On-Device AI App: Architecture. Today the abstraction ends. We open ListenToMe, a shipped macOS meeting copilot, and read the actual pipeline it runs, stage by stage. Then, in the lab, you rebuild that core in Python as TinyCopilot until two hundred one tests pass. The module runs about seventy-five minutes of lesson plus a three-hour lab. By the end, you will be able to point at a Swift file for every stage and defend each decision.

### Slide 2 — By the end you can…

*35.8s · sentence-measured*

> These six bullets are the whole contract of this module. You will sketch the pipeline from capture through transcribe, context, prompt, and route. You will name the file that implements each stage, and justify the three protocol seams. You will route models per role, cancel stale streams, write prompt builders as pure functions, and type streaming errors so truncation fails loudly. Notice what is not here: no prompt engineering tricks and no model benchmarks. This module is about architecture, where decisions live and how they are proved, and each objective maps to one lab step and at least one quiz question.

### Slide 3 — M2.1 — One pipeline, two layers

*30.5s · sentence-measured*

> Here is the whole system in one line. Microphone audio is tagged as you, system audio as others, and both arrive as PCM chunks. The pipeline then runs capture, transcribe, store, context, prompt, and route. The split is the important part: everything in the App folder touches hardware, and everything in ListenToMeCore is pure. The three seams are AudioCapturing, Transcribing, and LLMProvider. That layering is what makes the pipeline fully runnable in a unit test against mocks.

### Slide 4 — Capture is thin on purpose

*29.9s · sentence-measured*

> Capture is thin on purpose. DualChannelCapture taps two sources, the microphone and system audio, converts both to mono Float PCM, and emits them as audio chunks. The microphone tap tags its buffers as you, and the ScreenCaptureKit callback tags its buffers as others. That single tag is why the app can label You versus Others with no diarization model at all. Capture is bound to hardware, so it is the least testable code in the system, and that is exactly why it is kept as thin as possible.

### Slide 5 — Three protocol seams

*46.8s · sentence-measured*

> A seam is a protocol the pure core owns and the platform side implements, and the core declares three of them. The table shows all three; the code shows two. AudioCapturing exposes a status stream, a chunk stream, and start and stop, and the app implements it with AVAudioEngine and ScreenCaptureKit. Transcribing says partials and finals arrive, implemented by SpeechAnalyzer or WhisperKit. LLMProvider is the smallest: an id and one streaming function returning an async throwing stream of strings, implemented by an Ollama HTTP client. The core never names AVFoundation or Ollama; it only names these protocols, and that inversion is what lets the test suite inject mocks. Add a fourth transcription engine tomorrow, and nothing below the Transcribing protocol changes.

### Slide 6 — Three engines, one seam

*34.6s · sentence-measured*

> One seam, three engines. SpeechAnalyzer is the default and needs one analyzer per source, unlike the legacy speech recognizer, which has a process-global limit. WhisperKit is opt-in and works in batches, so it emits finalized segments only. Notice the prepare contract: warm up before audio arrives, so feed never blocks and the opening seconds of a meeting are not dropped. WhisperKit trades live partials for stronger multilingual quality, because Apple's on-device Speech picks one primary language and does not code-switch. Add an engine, and nothing downstream changes.

### Slide 7 — The store and its budget

*44.6s · sentence-measured*

> ConversationStore is the single source of truth. It keeps a log of finals plus one current partial, and applying a result appends finals and replaces the partial. The context window walks utterances newest-first, keeping each while it fits, and always keeps the newest even if that one alone exceeds the budget, so the window is never empty. The code on this slide is the real signature from ContextEngine: buildContext takes the store, optional notes, and a maxChars budget that defaults to 4,000 characters. Recap and action-item prompts get 100,000, because they have to cover the whole conversation. Notice the budget is a parameter with a default at the call surface, not a constant buried in a function body — tests can see it and labs can vary it.

### Slide 8 — When the engine gives no partials

*31.9s · sentence-measured*

> WhisperKit buffers audio, so something has to decide where an utterance ends. The core voice activity detector is thirty-seven lines. It measures root-mean-square energy per frame with a threshold of 0.02, and a trailing silence window of 0.8 seconds. It returns true exactly once, on the frame where silence after speech first exceeds that duration, so it fires once per utterance boundary. There is no machine learning model here, just a threshold and a timer. Spend the cheap heuristic where a model would be overkill.

### Slide 9 — The newest segment always survives

*43.0s · sentence-measured*

> This is the first proof slide, and it sets a pattern for the course: every claim we make has a file pointer you can open, and that pointer resolves. The loop is eleven lines. It walks utterances newest-first and breaks before exceeding the budget, but only once something is already collected. That is the entire guarantee, and it lives in the guard: the newest segment is always included, even when it alone blows the budget, so the context window is never empty. The default budget of 4,000 characters lives in ContextEngine. Read the loop rather than trusting the bullets — the comment in the source states exactly what to verify. The 96 percent core coverage badge and the 95 percent floor are downstream consequences of this kind of layering.

### Slide 10 — M2.2 — Three roles, three models

*37.8s · sentence-measured*

> Section M2.2 is about routing, and it starts with roles. Listener, Quick, and Deep are an enum in the core, not a UI accident. Listener keeps a rolling summary and refreshes continuously, so speed beats depth, while Quick answers on a global hotkey and fires proactively, so latency is the whole game. Deep is on-demand long reasoning, where strength matters more than speed. The app shows four panes, Transcript, Listener, Quick, and Deep, each with its own model dropdown. "Just use the best model everywhere" fails twice: it burns latency where you do not need it, and it pins the product to one model's quirks.

### Slide 11 — Local-first role defaults

*31.3s · sentence-measured*

> ModelRanking picks a default for each role automatically. Quick gets a model with a fast marker such as flash, mini, nano, lite, small, or fast, or the lightest one available. Deep gets a strong marker such as pro, reason, think, coder, code, ultra, max, or large, or the heaviest. The Cloud filter is a privacy default, not a speed one: an unpinned pane must never silently send a transcript to Ollama Cloud. Cloud models are selected only when no local model exists.

### Slide 12 — Token-prefix, not substring

*46.7s · sentence-measured*

> Here is a small check with a large blast radius. The router splits the model name into tokens, on the usual separators — dash, colon, dot, slash, space — and lets a marker match only at a token start. Look at gemini-2.5-flash: it contains the letters m-i-n-i, so a raw substring check would call it mini and rank it as fast. The token-prefix check rejects that hit, because mini is not a token in that name; hasPrefix runs against each token, never the raw string. One wrong check misroutes an entire model family, and no test fails unless you wrote the near-miss test. TinyCopilot ships exactly that test: test_gemini_is_not_demoted_as_mini. Both functions on the slide are pure — no I/O — which is what makes them fully unit-testable.

### Slide 13 — Generation tokens kill stale streams

*31.3s · sentence-measured*

> Switching models mid-answer creates a subtle correctness bug, and the fix is a generation counter. MeetingSession keeps one counter per role. When you call set model, it cancels in-flight work and bumps the counter. The streaming loop then guards every write against that counter, so switch mid-answer and the old tokens die on the floor. Without it, a slow answer from the previous model finishes after the switch and displays under the new model's name, and users read that as the new model being wrong. Cancellation is a correctness feature, not an optimization.

### Slide 14 — PromptBuilder is pure

*32.5s · sentence-measured*

> Prompt is a public enum of static functions in the core. It performs no input or output, holds no state, and reads no clock. Context goes in, an LLMRequest comes out, and the same inputs always produce the same string. Purity is not a style preference here: the tests assert the built text directly, so prompt regressions are caught in milliseconds without a network call or a model. That is the only way to keep nine response actions across three roles honest. In TinyCopilot, any hidden state or randomness will fail the determinism test.

### Slide 15 — Three base prompts, three contracts

*33.4s · sentence-measured*

> Each role has its own base prompt and its own contract. Quick gets no preamble and must answer in one to three sentences. Listener must never invent an owner, a deadline, an agreement, or a completion. Deep prefers depth over brevity, with no padding. The Listener contract exists because its summary feeds back into the Quick and Deep prompts, so one hallucinated owner would propagate everywhere; it is blocked at the source. Nine response actions layer on top, and persona directives append to every role, so a preset like Interview shapes all three identically.

### Slide 16 — Only completed summaries ground other roles

*27.8s · sentence-measured*

> Open MeetingSession and count the summary properties: there are two, not one. The live value is what you see on screen, and it is cleared while a refresh streams. The completed value is separate, and only that one is injected into other roles' prompts. The misconception to kill here is that more context is always better, so you should inject whatever is on screen. An in-flight summary is a confident-looking half-answer, and Quick would treat it as fact. A half-answer is worse than no answer.

### Slide 17 — M2.3 — Proactive is restraint

*26.8s · sentence-measured*

> Section M2.3. Proactive sounds like it needs intelligence; it actually needs restraint. Question detection is twenty-eight lines of code, deliberately simple and swappable later. The design spec calls for a lightweight heuristic, debounced so it fires at most once every few seconds. Ship the cheap heuristic behind a seam and spend your complexity elsewhere. The trigger is about five percent of the work; the discipline around it is the other ninety-five.

### Slide 18 — QuestionDetector: three rules

*32.4s · sentence-measured*

> The detector has three rules. A segment ends in a question mark. It starts with an interrogative such as what, why, or how, or contains a word-boundary phrase cue such as can you, any thoughts, or walk me through. The word starts is load-bearing: the interrogative rule applies only to the first token. Phrase cues are matched on word boundaries, so many thoughts never triggers any thoughts, and we cannot use your laptop never triggers can you. Those near-misses are the tests people most often forget to write, so TinyCopilot ships eight of them for you.

### Slide 19 — The gate: finalized, others, debounced

*28.1s · sentence-measured*

> Detection alone does not fire the feature. Four conditions have to hold. The segment must be finalized, it must come from others, it must pass detection, and at least eight seconds must have passed since the last fire. The others condition is the one people miss: you do not want the app answering your own rhetorical questions. The debounce matters too, because without it two heated minutes of questions flood the pane with overlapping suggestions. One trigger, one answer, then quiet.

### Slide 20 — Typed streaming errors

*48.5s · sentence-measured*

> Ollama streams newline-delimited JSON over the chat endpoint, and it can return HTTP 200 and then an error object inside the stream, so the provider types its failures as an enum with three cases. A server error is an in-stream error event. Incomplete means the lines ended without a done flag, and empty means the stream completed with no visible text. Each case carries a user-facing message, so truncation can never finish as success. Ollama's own API documentation now shows the final line of a stream carrying done: true plus a done reason such as stop — the provider trusts none of that until the answer is complete and non-empty. This design is a scar, not a guess: a review found the old provider let truncated streams pass while two hundred and fifteen core tests were green and coverage sat above ninety-seven percent.

### Slide 21 — Flicker is information; silence is a lie

*28.3s · sentence-measured*

> Open the review and read gap G06. The test suite validated what had been built, and what had been built was wrong. Two booleans, a completion flag and a content flag, are what the streaming loop now tracks. The fix was not more coverage; it was an honest failure model. Swallowing stream errors to avoid UI flicker is exactly backwards, because the user then gets a silently incomplete answer instead of a retry affordance. Flicker is information; silence is a lie.

### Slide 22 — Budgets come from observation

*36.7s · sentence-measured*

> Every number on this slide is a cost ceiling, not a feature. Quick evaluation forces thinking off and temperature zero. The 3,072-token cap was chosen from a real truncation: live testing showed planning text leaking through even with thinking off, which exhausted the former 1,600-token budget halfway through valid JSON. The cap is the smallest budget that stopped that observed truncation. Speech batches run five seconds with a twenty-four character eligibility rule, and response caps are thirty seconds or sixteen kibibytes. Summaries refresh every thirty seconds and Deep every sixty, serially.

### Slide 23 — Lab M2 — Build TinyCopilot's core

*35.3s · sentence-measured*

> Lab M2 is where you build TinyCopilot's core. You will delete six Python modules, one at a time, and re-implement them test-first. The tests are the spec, and the reference implementation is your answer key. Start by running the full suite green, then read copilot.py, then delete a module. Expect a collection error on deletion: that is your real red run, and you should capture it before you go green. When the lab finishes, make lab-m2 reports two hundred one tests passed at full coverage, the floor of ninety is enforced, and make demo prints three role outputs from a real model.

### Slide 24 — Quiz M2 — eight questions

*36.6s · sentence-measured*

> The quiz has eight questions: six multiple choice and two short answer. The topics mirror the module: pipeline order and the coverage enabler, role defaults on three installed models, generation counters and prompt purity, the never-invent contract, streaming error cases, and debounce conditions. The distractors encode the misconceptions we taught against, such as the strongest model is best everywhere, localhost proves local, and queue the old stream's tokens. The short answers ask you to apply the ideas, not recall them. Do the quiz before the workshop, and we will review the two most-missed items live.

### Slide 25 — Recap

*34.6s · sentence-measured*

> Three segments, three sentences. M2.1: one pipeline, with decisions in a pure core, hardware in thin glue, and three protocol seams. M2.2: models routed per role, matching by token prefix, and cancellation by generation counter. M2.3: a cheap twenty-eight-line heuristic, a hard gate with an eight-second debounce, and typed streaming errors. Every stage has a file pointer you can open, and every number is a measured ceiling. If you remember one thing, remember that the architecture is what makes the honesty possible.

### Slide 26 — Discussion prompt

*29.8s · sentence-measured*

> Here is your discussion prompt for the week. A stakeholder says: point the biggest model at it. Your job is to answer with architecture, not opinion: name the trigger, the debounce, and the budget, and cite at least three ListenToMe files. Then name one failure mode the stakeholder's design loses, for example no debounce means overlapping suggestions, or no typed errors means silent truncation. Aim for about one hundred fifty words and post it to the community; we grade it on those file pointers.

<a id="m03"></a>

# M3 — The On-Device AI App: Privacy, Testing, Shipping
## Narration transcript

**27 slides · 27 narrated · 14m 58s of audio**

**Voice:** preview narration — a free local voice, not the finished release recording. The audio is spoken by a synthesized voice, not a human recording. The words below are the approved narration and do not change when the release voice is recorded.

The text below is what is spoken on each slide, in order. It is the same text as the captions and the approved narration script, checked word for word by `course/06-production/narration/validate_narration.py`.

---

### Slide 1 — M3 — Privacy, Testing, Shipping

*25.6s · sentence-measured*

> Welcome to Module 3. Module 2 gave you a TinyCopilot core that runs; today you make it trustworthy and sellable. The module makes three moves. You engineer a local-only mode that fails closed, you test in tiers so each risk sits in a tier that can actually observe it, and you ship against a definition of done that ends at a verified download. The case study is ListenToMe, and every claim in this module has a file pointer you can open.

### Slide 2 — By the end you can…

*35.2s · sentence-measured*

> Here are the five objectives, and you should read them as promises. You will engineer a fail-closed local-only mode: metadata verification, loopback host allowlists, redirect refusal, and labels that tell the truth. You will verify model metadata on every request by asking the daemon what it is about to run. You will test in tiers and admit what continuous integration structurally cannot test. You will ship to a checksum-verified artifact, where the release ends with you downloading your own build. And you will position your product from a sourced competitor table, with a one-liner whose every clause traces to a column.

### Slide 3 — M3.1 — Privacy is a mode, not a slogan

*31.4s · sentence-measured*

> The core idea of this segment is that privacy is not an adjective in marketing. It is a mode switch in Settings. ListenToMe exposes an enum called AI processing mode with four cases, and here is the cloud label: Ollama Cloud, sends transcript and context. Read it again, because it names the data it ships. That is the standard for every mode label you write. Then the boundary rule: pasting an API key stores the key and changes nothing about routing. Opting in to cloud is a deliberate act, never a side effect of configuration.

### Slide 4 — Proof: the mode enum and its labels

*40.8s · sentence-measured*

> Here is the proof, and now it is on the slide: the AIProcessingMode enum from ModelPrivacy.swift, lines three through thirteen. Four cases: off, local, apple, cloud. Four labels, each written to be true rather than to sell, and the code block is the enum itself. The one to memorize is cloud: it does not say enhanced; it says it sends the transcript and context. Read the labels on the slide — they are the strings the app actually ships. The README section on AI processing mode carries the key rule: adding a key alone does not switch modes. A user cannot drift onto cloud without a deliberate, visible choice; the mode is the contract, and the label tells the truth about it.

### Slide 5 — A localhost URL proves nothing

*30.6s · sentence-measured*

> This is the failure the whole segment guards against. The obvious implementation is to check that the server URL is localhost and call it done. ListenToMe's code carries a comment rejecting exactly that shortcut, and here is why. If you pull a model whose name ends in colon-cloud, it installs through your local daemon, it appears in ollama list like any other model, and it answers through your localhost URL. But the compute happens somewhere else. The gap review states it plainly: a local endpoint is not proof of local inference.

### Slide 6 — What `/api/show` must show

*28.1s · sentence-measured*

> The fix is to ask the daemon, on every request, to describe the model it is about to run, and to accept only the description of a downloaded local model. There are four requirements. There must be no remote host field and no remote model field, and the details format and the model info must both be non-empty. The first two catch a cloud alias. The last two prove the shape of a downloaded model that carries its weights locally. Anything else fails closed, as one conditional that returns false.

### Slide 7 — Proof: `isVerifiedLocal` fails closed

*41.9s · sentence-measured*

> This guard is the exhibit on the slide: ModelPrivacy.swift, lines seventeen to twenty-four, one guard clause. Parse the JSON. Require the remote host and remote model fields to be absent. Require the details format and the model info to be non-empty. Otherwise return false — and because the failure path is the default, missing metadata, malformed JSON, and unexpected fields all reject. Follow the guard line by line: every condition must hold for the function to say true, and any surprise says false. The trust boundary is the daemon's self-description, verified structurally. A localhost URL or a model name alone is insufficient — that is exactly what the doc comment states.

### Slide 8 — Three defenses around the check

*37.7s · sentence-measured*

> In local-only mode, three layers run before every chat request. First, the base URL host must be localhost, 127.0.0.1, or the IPv6 loopback address. Anything else throws before a single byte of your prompt is written. Second, the provider posts to the show endpoint and requires an HTTP two hundred response plus a verified-local metadata result, and this is re-verified on every request, so switching models mid-session cannot skip the check. Third, redirects. You can read all three defenses in OllamaProvider.swift, lines one hundred thirty-eight to one hundred fifty-seven.

### Slide 9 — Redirects refused

*34.3s · sentence-measured*

> Most HTTP stacks follow redirects silently by default. That matters here, because even a server that passed the local metadata check could answer your chat request with a redirect to anywhere, and the stack would helpfully forward your meeting text along with it. ListenToMe refuses, and the refusal is on the slide: a small delegate class, RejectRedirects, whose redirection handler answers nil for every redirect, so the request dies instead of following. The class name is the policy — redirects are not an edge case to configure away; they are a channel your meeting text must never travel.

### Slide 10 — Fail closed by default

*28.9s · sentence-measured*

> Fail-closed design shapes defaults too. ModelRanking.roleDefaults filters cloud-suffixed models out of automatic selection entirely. Cloud is auto-picked only when no local chat model exists, which means the user set a cloud key and opted in. Underneath that sits the product principle in CLAUDE.md: anything that would send data off-device by default is out of scope. And turning AI off is a real option, not turning the app off. Capture, transcription, and saving all keep working.

### Slide 11 — Claim → engineering enforcement

*35.6s · sentence-measured*

> This table is the discipline to copy. Your transcript never leaves your Mac is enforced by local mode, the host check, and the metadata check. Cloud aliases cannot sneak in, because the verification guard fails closed. Text cannot be silently forwarded, because redirects are refused. Adding a key never changes privacy, because the mode is an explicit user setting. Local by default, because the ranking filters cloud models. Every privacy promise needs a row whose second column is code a reviewer can open. If a claim has no second column, you do not have a claim, you have copy.

### Slide 12 — M3.2 — Testing is tier assignment

*26.4s · sentence-measured*

> Testing is tier assignment. That is the reframe for this segment. For each risk, name the cheapest tier that can actually observe it. Unit tests with a mocked transport cover your logic. A contract test against a real daemon covers the seam that a mock can only assume. A human smoke test covers audio and permissions. What you cannot do is promote a risk to a tier that cannot see it. Pretending continuous integration covers the top tier just makes your README lie.

### Slide 13 — The 95% coverage floor

*43.9s · sentence-measured*

> ListenToMe's continuous integration enforces a ninety-five percent line-coverage floor on the core package as a hard gate, and the gate is now on the slide. The script takes the threshold as its first argument, runs the suite with coverage enabled, computes total line coverage through llvm-cov, prints a per-file report so you can see where you stand, and the awk comparison exits non-zero below the threshold — one line of arithmetic deciding whether the build passes. Here is what that buys you: nobody adds untested logic to the core without either testing it or consciously arguing for an exception. Here is what it does not buy: correctness, GUI behavior, audio quality, or the first-run experience. The floor is a floor, not a ceiling of proof.

### Slide 14 — Proof: the floor bites in CI

*34.9s · sentence-measured*

> The coverage step sits in the continuous integration workflow at lines thirty-six to forty-two — the YAML on the slide is that step, and the logic lives in the script it calls. The workflow has three jobs: the macOS app build, the iOS app build, and the core suite with the coverage floor. The two build jobs also run a dependency-lock diff, so the artifact you test is built from locked dependencies rather than whatever resolves that day. That is release discipline appearing in the pipeline, not in a document: the floor is invoked with a literal ninety-five in the job step, where every contributor can read it.

### Slide 15 — The contract test CI can't run

*32.2s · sentence-measured*

> Continuous integration cannot reach an Ollama daemon or audio hardware, so the real-language-model contract test lives outside it, behind the make e2e target. That target runs a real completion through the actual provider against your local daemon, auto-selecting an installed chat model. Why call it a contract test? Because it tests the seam that mocks can only assume: that your request format, your streaming parser, and your error typing work against the real thing. Every unit test used a mock. This one run is the only evidence that the mock was honest.

### Slide 16 — Proof: a test that skips, not hides

*39.1s · sentence-measured*

> This test is OllamaContractE2ETests.swift, lines four to twenty-two, and the skip is the exhibit: XCTSkipUnless on an environment variable, so a normal swift test run and continuous integration never touch the network — the test is skipped loudly, with a message that says how to run it, not hidden behind a silent pass. The make e2e target sets that gate and selects the model. The assertion is deliberately minimal but real: stream a completion for a fixed prompt through the same provider code the app uses, and require non-empty streamed content. Skipped is a state CI reports honestly; a test that cannot run in CI but can run on your Mac is still worth shipping.

### Slide 17 — The tier only a human can run

*35.1s · sentence-measured*

> Above the contract test sits the manual tier. Microphone capture, system-audio capture, and live speech-to-text all require a GUI session and manual permission grants, so no script can run them for you. The manual smoke test document opens by stating exactly what the make e2e target already covers and what this document covers that cannot be automated. It is a numbered, repeatable script: grant the permissions, speak a sentence, play audio from another app, and confirm the labels. A testing strategy that pretends continuous integration covers this tier just makes your README lie.

### Slide 18 — The review that said no

*33.6s · sentence-measured*

> On September tenth, twenty twenty-six, a production review of the one point three point zero candidate produced a thirty-four-item gap inventory, each item with a priority and an evidence class. The team had two hundred fifteen passing core tests and ninety-seven point two four percent coverage in hand. The review still recommended not promoting the release. Item G01 is the privacy hole from earlier in this module, sitting happily inside ninety-seven percent coverage, because the tests tested what was built. Tests validate what you built. Review validates what you shipped.

### Slide 19 — M3.3 — Done ends at a verified download

*33.5s · sentence-measured*

> ListenToMe's AGENTS.md makes release the default end of any fix or feature. A local build, a local install, or a draft pull request is not the end of the workflow. There are six steps: implement and run tests, lint, and coverage; verify in the installed production app; bump the version and notes; commit, push, and verify hosted continuous integration; publish the signed, notarized disk image targeting the exact source commit; and finally, download the published asset and verify its checksum. That last step is the one most projects skip.

### Slide 20 — Proof: download it and check the hash

*29.3s · sentence-measured*

> The mechanics are in the releasing document, around lines one hundred twenty to one hundred thirty-four. After publishing, you download the hosted asset and compare its SHA-256 hash against the verified local disk image, and you create the release with the target pinned to the exact commit, so the tag cannot silently point at a different one. The policy also has an honesty clause: if a real blocker stops publication, name the blocker and preserve the candidate. Do not describe the work as released.

### Slide 21 — Two bundle ids, on purpose

*35.6s · sentence-measured*

> Dev builds are a separate app from the release, with one bundle identifier for dev and one for release. The reason is macOS privacy plumbing. TCC, the subsystem that holds your Microphone and Screen Recording grants, keys those grants by bundle identifier plus the binary's code-signing requirement. A Developer ID signature and an Apple Development signature produce requirements that can never satisfy each other. Share one bundle identifier and installing either build silently invalidates the other's grants. The result is not an error or a crash. It is a toggle that stays on while capture returns nothing.

### Slide 22 — Competition analysis as an engineering artifact

*31.2s · sentence-measured*

> The other half of shipping is knowing and proving what your product is against what already exists. ListenToMe's competition analysis is built like a test suite. It opens with a dated header stating that where a detail could not be confirmed from a primary source, it is qualified with approximately or reportedly. The table is fourteen rows by nine columns, and every competitor entry ends with a source URL. The analysis names the structural tension: nearly every commercial product runs its AI in the cloud, even when it markets itself as local-first.

### Slide 23 — The one-liner and its columns

*36.9s · sentence-measured*

> The analysis does not invent a slogan. It identifies a corner almost no commercial competitor fills, and then derives the line from the table. So the one-liner reads: the free, open-source, fully on-device meeting copilot for macOS, bring your own model. Free traces to the price column, fully on-device to the on-device column, meeting copilot to focus, bring your own model to the multi-model column, and macOS to platform. Every clause traces to a column, and deleting any clause would make the line false against the table. That is the deliverable: specific and falsifiable, not mood music.

### Slide 24 — Lab M3 — Harden, Prove, Position

*35.8s · sentence-measured*

> Lab M3 is three hours and takes TinyCopilot from works to trustworthy. Step one, write the red-team test first: a mocked show response with a remote host set must be rejected in local mode. Then implement the privacy mode, the local model verification, host enforcement, and redirect refusal. Step two, add the real-language-model contract test, gated by the LAB_E2E environment variable. Step three, set the coverage floor and record a failure run. Step four, build the comparison table. The pass gate is make lab-m3 finishing green with forty-nine tests passed.

### Slide 25 — Quiz M3

*27.8s · sentence-measured*

> Quiz M3 has eight questions: six multiple choice and two short answer. They cover the three segments. Fail-closed design and why a localhost URL is not proof. Redirect rejection and the mechanics of the coverage floor. Tier assignment, and why review matters more than metrics. And positioning derived from the columns of a sourced table. One question maps to one segment objective, so the quiz checks the promises from the start of the module. Take it before the workshop.

### Slide 26 — Recap

*25.0s · sentence-measured*

> Five sentences to carry out of this module. Privacy is a mode, with truthful labels, and metadata is verified on every request. A localhost URL proves nothing, because a local daemon can serve cloud aliases. Test in tiers, and remember that coverage is the entry fee, not the verdict. Done means a verified download, not a local build. And positioning derives from a sourced, qualified table.

### Slide 27 — Discussion prompt

*27.8s · sentence-measured*

> Here is your closing prompt. Post the privacy claim you are least sure you can enforce, the one that sounds best in marketing, plus the code or test that would prove it if you wrote it. Then answer the harder question: where does your guarantee actually end? ListenToMe answers with a single clause, that it trusts the installed local Ollama service and its metadata. What is your product's equivalent sentence, and would you put it on your sales page? Then reply to one peer and name the defense they left out.

<a id="m04"></a>

# M4 — The Spec-Driven SaaS: From Idea to Executable Spec
## Narration transcript

**28 slides · 28 narrated · 18m 16s of audio**

**Voice:** preview narration — a free local voice, not the finished release recording. The audio is spoken by a synthesized voice, not a human recording. The words below are the approved narration and do not change when the release voice is recorded.

The text below is what is spoken on each slide, in order. It is the same text as the captions and the approved narration script, checked word for word by `course/06-production/narration/validate_narration.py`.

---

### Slide 1 — M4 — The Spec-Driven SaaS

*36.0s · sentence-measured*

> Welcome to Module 4, the Spec-Driven SaaS. In Module 1 you got the operating system; today we run it at production scale on a real multi-tenant SaaS. The promise is narrow and testable: by the end, you can produce a spec folder complete enough that a fresh agent session, with no chat history and no memory of your reasoning, can implement story one without asking a single question. Our case study is SignUpFlow, which drives features with spec-kit slash commands, and its seventeen spec folders are the evidence. Expect roughly seventy-five minutes of lesson, plus a ninety to one hundred twenty minute lab.

### Slide 2 — By the end you can…

*38.0s · sentence-measured*

> Read these as six verbs, not topics: each is something you will do in the lab. You will walk a production spec folder artifact by artifact, run the chain from specify through clarify, plan, checklist, and tasks, and judge specs by the stranger test. You will enforce the checklist gate's pass rules, record change with severity-tagged review, and catch drift in generated artifacts. The last two separate a demo from a deliverable. Anyone can generate a beautiful spec folder; the discipline is reviewing it locally with findings that name a severity and a file. If you remember two things today: the stranger test and the drift checks.

### Slide 3 — M4.1 — The command chain

*33.0s · sentence-measured*

> Here is the entire mechanism, and its whole virtue is that it is boring. Each slash command reads what the last one wrote, so nothing is carried in anyone's head. Specify writes the WHAT, clarify burns a small question budget, then research, data model, and plan add the HOW and the Constitution Check. The checklist gates, contracts pin the seams, and tasks turn it into work. The command definitions live in the dot-claude commands folder and the templates in dot-specify templates, both openable in the clone. Notice there is exactly one gate, and it is cheap.

### Slide 4 — Proof: `spec.md` owns WHAT

*44.1s · sentence-measured*

> The spec file owns the WHAT, and now it is on the slide. In the security-hardening spec you will find eight user stories, six of them P1 and two P2, forty-four functional requirements all phrased System MUST, seven edge cases, and twelve success criteria. Read the two exhibits: a requirement line — the system must enforce rate limits on authentication endpoints, blocking requests after five failed attempts within five minutes per IP — and the first story's scenario, given a user attempts to log in, when they fail authentication five times within five minutes, then further login attempts are blocked for fifteen minutes. The same numbers appear in both, and zero technologies are named — no Redis, no SQL anywhere in the spec.

### Slide 5 — Proof: `research.md` — decisions with receipts

*41.1s · sentence-measured*

> Research settles technology, and it does so with receipts. This file is nine hundred sixty-five lines holding eight numbered decisions, each with the same anatomy: the decision, the options evaluated with pros and cons, the rationale, then implementation details. The exhibit is the real first decision, verbatim: Decision 1, Rate Limiting Infrastructure, use Redis for rate limit storage, not in-memory. That is the shape every decision follows, and the consistency is the point — a new engineer can read any one of the eight and know exactly how the argument was made. Decision two chooses TOTP over SMS the same way: options, evidence, a verdict you can audit.

### Slide 6 — Proof: `plan.md` — HOW, plus one absence

*41.4s · sentence-measured*

> The plan owns the HOW, and it opens with a gate that is now on the slide, verbatim. Constitution Check, gate: must pass before Phase 0 research, re-check after Phase 1 design. The check walks the project's seven principles and gives each one a verdict, ending with the line Constitution Violations: NONE and a Complexity Justification marked not applicable because there are no violations to justify. The template says to fill the Complexity Tracking table only when violations exist, which is why it is empty here. Every file the plan touches is annotated NEW or MODIFY. One honest absence: there is no data-model.md in this plan, because security spans entities rather than adding one.

### Slide 7 — Proof: `contracts/` — six seams

*39.2s · sentence-measured*

> The contract folder is where WHAT and HOW first meet. This feature has six contracts, and together they run to four thousand six hundred sixty-one lines: rate limiting, the two-factor API, audit logging, CSRF, session, and password reset. The exhibit is the rate-limiting config table's first rows, and the numbers should look familiar: a POST to the login endpoint, a five-minute window, five attempts, per IP, fifteen-minute lockout. The contract repeats the spec's numbers rather than inventing its own — that is what makes them checkable. Each contract also carries the key schema, the error keys, a test sketch, and benchmarks.

### Slide 8 — Proof: the gate and the quickstart

*41.5s · sentence-measured*

> The quickstart is six hundred forty-three lines of timed deployment with exact commands, plus prerequisites, a verification checklist, and troubleshooting. The requirements checklist is fifty lines and grades three groups: Content Quality, Requirement Completeness, and Feature Readiness. Its first rule bans implementation details — a spec-quality rule, enforced by a checklist. And the verdict is on the slide, verbatim: all checks passed, quality score one hundred percent, all checklist items passed. It was validated on October twenty-second, twenty twenty-five, generated by the speckit checklist command. The grade is a gate output, not a self-assessment in a README.

### Slide 9 — Proof: `tasks.md` — Phase 2, and the gap

*38.8s · sentence-measured*

> Here is the honest gap in the exemplar, now flanked by the real format. This feature was specced down to four thousand lines of contracts and never generated a task breakdown; its plan's Next Steps still lists that command as Phase 2. So read the real format from the tasks on the slide, which come from the onboarding feature: checkboxes with an ID, an optional parallel marker, a story tag, and exact file paths. T017 creates a method in api/services/onboarding_service.py — the task names the file it will touch before any code exists. That is what makes a plan executable by a fresh session: no archaeology, just pointers.

### Slide 10 — M4.2 — The stranger test

*35.3s · sentence-measured*

> The constitution's Context A defines the Ralph loop. Started by a shell script, or by any prompt mentioning implement spec, the agent must pick the highest priority incomplete spec from the specs folder, complete all acceptance criteria, and output a done promise when it is one hundred percent finished. That agent has no chat history, and in Ralph mode no appetite for questions. So the quality test for every artifact is one sentence: delete the conversation — could a stranger implement this? Everything in this segment follows from that. First consequence: the split between WHAT and HOW.

### Slide 11 — WHAT vs HOW

*44.8s · sentence-measured*

> Kill the misconception: a good spec does not contain the schema. The spec describes user-visible behavior in technology-agnostic terms. The plan carries languages, versions, storage choices, and performance targets. The gate's rule is explicit — no implementation details such as languages, frameworks, or APIs — and schema SQL belongs to the data model, the contracts, and the migrations. Entities in the spec are described without implementation. That separation buys you something real. This feature's spec recorded an open decision to use an in-memory cache with a database backup, dated TBD; research later chose Redis and rejected in-memory outright. The requirement never changed, and the reversal is on the record.

### Slide 12 — Every story is an MVP slice

*34.6s · sentence-measured*

> The spec template mandates it: each user story must be independently testable, meaning if you implement just one of them you still have a viable MVP. Independently developed, tested, deployed, demonstrated. Every story in the security-hardening spec carries its own independent test line; story one's is to simulate failed logins and verify both the lockout and the message shown. Three consequences follow. A partial implementation still ships value. A pull request can carry exactly one story. And the task file groups work by story, with a checkpoint after each one.

### Slide 13 — Scenarios ready to become tests

*39.4s · sentence-measured*

> Recall story one's first scenario: fail five times in five minutes, then blocked for fifteen minutes. Those numbers recur downstream like a refrain. They become functional requirement zero zero one, the first row of the rate-limiting contract's config table, and an assertion in a test sketch. A scenario is done when the person writing the test needs to make no further decisions. Contrast the anti-examples. Then the system is secure cannot be coded against. Then authentication failures are handled appropriately names no observable outcome. Both fail the gate's rule that requirements must be testable and unambiguous. Write Then-clauses that a test could assert tomorrow.

### Slide 14 — Bounded clarification

*42.6s · sentence-measured*

> What about what you genuinely do not know yet? Drafts may mark a requirement with a needs-clarification placeholder — for example, a requirement that authenticates users without naming the method. But the checklist's Requirement Completeness group requires that no markers remain before planning. There are two resolution paths. The clarify command runs before plan on a deliberately small budget; this feature's next steps cap it at three questions. Or you document a default in Assumptions, which is how this spec settled ninety-day log retention, one-hour token expiry, and a thirty-second TOTP tolerance. An honest footnote: the clarify command definition says up to five questions, a drift we will return to.

### Slide 15 — The gate's pass rules

*41.7s · sentence-measured*

> The gate has three groups, and every item is binary. Content Quality checks that there are no implementation details, that the spec focuses on user value, and that a non-technical stakeholder can read it. Requirement Completeness checks that no markers remain, that requirements are testable and unambiguous, that success criteria are measurable, and that scope, dependencies, and assumptions are defined. Feature Readiness checks that every requirement has acceptance criteria, that scenarios cover the primary flows, and that no implementation leaked in. Calling checklists bureaucracy is backwards: this is the last cheap moment before you spend an autonomous implementation loop on a spec with a hole in it.

### Slide 16 — Tasks cite exact file paths

*39.2s · sentence-measured*

> Why is a path mandatory in a task? Because a fresh agent session has no idea how your project is arranged, and the repository's own anti-hallucination rule forbids inventing structure. It says: do not invent file paths, function names, route paths, commands, URLs, or identifiers; grep the repo before referencing. A task like update the backend forces the agent either to guess, which is how hallucinated endpoints happen, or to burn budget rediscovering your layout. A task that names the file makes its first action a grep that confirms rather than invents. Tasks can just say update the backend is the misconception to unlearn today.

### Slide 17 — Contracts are the seams between sessions

*32.9s · sentence-measured*

> A contract is the interface between the session that designed the feature and the different session that implements it. Those two share nothing but the files on disk, so the seam has to be written down: request and response shapes, error keys, the Redis key schema, and a test sketch. In the rate-limiting contract, the config table is where the spec's WHAT and the plan's HOW first meet, with the same five, five, and fifteen numbers, now carrying per-IP scope and a key format. Miss the contract and the implementing agent invents the error keys, and your frontend never matches.

### Slide 18 — Constitution Check — and the Ralph loop

*40.9s · sentence-measured*

> An agent writing a plan will cheerfully violate your principles, skipping end-to-end tests or adding infrastructure nobody asked for, because it has not internalized them. The Constitution Check forces the plan to walk each principle with a verdict and evidence, and any violation must be argued in the Complexity Tracking table, filled only if violations exist. Here: seven principles, seven verdicts, zero violations, an empty table. Now close the loop with the Ralph context. An agent that must complete all acceptance criteria and cannot ask questions is safe exactly to the degree your artifacts are complete. The pipeline is the precondition for autonomy, not ceremony around it.

### Slide 19 — M4.3 — One PR per story

*29.3s · sentence-measured*

> The task file is built for one pull request per story. Tasks are grouped by story, tests are written first and fail, and there is a checkpoint after each group — the template's line is, stop at any checkpoint to validate story independently. A pull request carrying exactly one story is reviewable in one sitting, demoable to a stakeholder, and revertable without dragging unrelated changes back out. This is not process for its own sake. It is what makes the Validation section short enough to be honest.

### Slide 20 — The PR body format

*42.3s · sentence-measured*

> The pull request body has four fixed sections. Summary names the change in one line per change. Changed files gives a path and a reason for each. Validation records the commands you ran and their results. Follow-ups records known gaps, deferred work, and open questions. Behind that format are the rules: run the full test target for every pull request, and note that there is no continuous integration, so all validation runs locally. Record commands, outcomes, limitations, and the pushed head SHA. Merge only after local validation and review are recorded and GitHub reports the branch mergeable. Never fabricate status checks, bypass protections, or treat missing evidence as success.

### Slide 21 — Local code review

*43.7s · sentence-measured*

> The repository's review policy is itself a file, and it states that Ollama is not a code-review provider — the former hosted gate is retired, so do not recreate it. The checklist is concrete: record the pull request's head and base SHAs, inspect the complete diff along with affected source, tests, and agent instructions, and check correctness, security, organization isolation, authorization, API contracts, migrations, and negative-path test coverage. Report findings with a severity and a file and line reference, then fix blocking issues and re-review the final diff. Two hard lines: do not claim independent review when the builder performed the review itself, and missing review is not approval.

### Slide 22 — Drift case 1: the stale path

*40.0s · sentence-measured*

> Now the part that surprises people: generated files lie. Open the onboarding task file and read line three. It says the input is design documents from the specs zero two zero user onboarding folder. But the folder is specs zero zero zero user onboarding. The feature was renumbered at some point, and the generated task file kept the stale path. Nothing failed. No test caught it, no warning fired. It just sat in a generated artifact, waiting for an agent to follow a dead end. Everything in a spec folder is generated output, and generation is where hallucination risk concentrates, so generated artifacts deserve the same suspicion as generated code.

### Slide 23 — Drift cases 2–3: count and directory

*44.9s · sentence-measured*

> Two more drift cases, both inside the exemplar folder. Case two: the requirements checklist prints eight prioritized user stories, five P1, two P2, zero P3 — but the spec marks six P1 stories: rate limiting, audit logging, CSRF, session invalidation, input validation, and password reset. The same checklist then lists those six while still printing five P1. The one hundred percent quality score did not catch it; only reading the checklist against the spec did. Case three: the onboarding tasks file assigns a migration to a migrations versions path, and no migrations directory exists — migrations live under alembic versions. Both files were generated, and both were wrong.

### Slide 24 — Countermeasures: grep, recount, open

*40.9s · sentence-measured*

> The repository already has the rules that target this drift. Operating loop step six says: search for stale commands, counts, check names, and feature-state claims before declaring done. The anti-hallucination rule says: grep the repo before referencing. So the countermeasures are mechanical. Grep every path a generated file cites and confirm it exists — that catches the nonexistent migrations directory. Recount every count against its source — that catches the five-P1 claim against six P1 stories. And never accept a self-reported score as a substitute for opening the file, which is the habit that catches the stale path. In the lab you run these on your own checklist.

### Slide 25 — Lab M4 — Spec a Real Feature

*39.6s · sentence-measured*

> The lab is ninety to one hundred twenty minutes, the whole module compressed into one deliverable: a complete spec folder for one real feature. Work in your own project's specs folder, or extend SignUpFlow if you have no SaaS of your own. You need seven artifacts, the same set we walked: spec, research, data model, plan, contract, checklist, and tasks. Two things are graded unusually strictly. Every task must name an exact file path that exists in your repository, and your checklist must survive your own drift checks — grep each cited path, recount each count. The pass gate is that a stranger implements story one with zero questions.

### Slide 26 — Quiz M4

*38.6s · sentence-measured*

> The quiz has eight questions, six multiple choice and two short answer, mapping to the three segments. It covers artifact responsibilities, gate rules, the task format, and the research decision format, and one question is the drift-check question. The distractors encode the misconceptions we taught against: that a spec may contain code, that secure is a testable Then-clause, that a task may name no file. Question eight asks you to name the two countermeasure habits from AGENTS dot M D and say which drift case each would have caught. Grep catches the nonexistent migrations directory; recounting catches the five-P1 claim against six P1 stories.

### Slide 27 — Recap

*37.5s · sentence-measured*

> Six lines to take away. The pipeline is a chain where each command consumes the previous file. The exemplar shows the full set at scale: eight stories, forty-four functional requirements, seven edge cases, twelve success criteria, eight research decisions, and six contracts totaling four thousand six hundred sixty-one lines — and one honest gap, no tasks file. Quality has a single test, the stranger test, and the gate enforces its consequences. The change record is a format, not a feeling. And generated artifacts drift, so grep paths and recount counts before you cite anything.

### Slide 28 — Discussion prompt

*34.8s · sentence-measured*

> Post to the community with this template. Name the feature you would spec first. Name the artifact you were most tempted to skip, and what breaks without it. Name the hardest thing to make stranger-testable. And name one drift check you now run, whether that is a grep or a recount. The third line matters most: name the specific scenario, requirement, or task you had to sharpen, and say what was vague before. Then read two classmates' posts and comment on one with a single question — would their sharpest acceptance scenario let you implement without asking anything? That is the stranger test, applied to each other.

<a id="m05"></a>

# M5 — Multi-Tenant Security & the Acceptance Gate
## Narration transcript

**25 slides · 25 narrated · 16m 32s of audio**

**Voice:** preview narration — a free local voice, not the finished release recording. The audio is spoken by a synthesized voice, not a human recording. The words below are the approved narration and do not change when the release voice is recorded.

The text below is what is spoken on each slide, in order. It is the same text as the captions and the approved narration script, checked word for word by `course/06-production/narration/validate_narration.py`.

---

### Slide 1

*31.4s · sentence-measured*

> Welcome to Module 5, the security and acceptance gate of the SaaS track. Two questions drive everything here. First, can one tenant ever see another tenant's data? Second, how do you prove the whole product works operationally, not just functionally? Your case study is SignUpFlow, a multi-tenant volunteer-scheduling API where churches and basketball leagues share one database. By the end you will hold two artifacts: negative-path tests that prove isolation, and a playbook manifest that admits what is not yet proven.

### Slide 2 — By the end you can…

*39.6s · sentence-measured*

> These are six verbs, not six topics, and every one is something you do in the lab. Enforce tenant isolation with a dependency. Bind tokens to a tenant and reload active rows. Choose your 401, 403, and 404 semantics deliberately. Separate permission roles from qualifications. Make the authorization matrix executable. Design acceptance around tiers, playbooks, and an honest manifest. The through-line matters: agents generate queries at machine speed, and every generated query is a chance to forget a tenant filter. So the answer is not to be careful. It is rules a machine can check and tests that catch drift.

### Slide 3 — M5.1 — The rule lives in `AGENTS.md`

*37.3s · sentence-measured*

> Here is the rule, and it lives in AGENTS.md. Every database query must filter by org_id. A missing org_id filter is a cross-tenant data leak, and you treat it as a P0 bug. Notice where that rule sits: not in a security wiki, but in the cross-agent baseline that Codex CLI, Cursor, Aider, Jules, OpenHands, Sourcegraph Amp, and Factory all read natively. Every agent that opens the repo to write a query reads it first. And the wording matters: filter every query by org_id is a check, while be careful with multi-tenancy is a vibe. A P0 bug is not a severity you negotiate in triage.

### Slide 4 — M5.1 — Three mechanical enforcers

*40.4s · sentence-measured*

> A rule needs mechanisms, or it is decoration. One file holds three enforcers. verify_org_member compares the person's org_id to the org_id in the request and raises 403 when they differ. get_current_user decodes the JWT, requires both the subject and org_id claims, then reloads the person with a three-way filter: id, tenant, and active status. Anything else is 401, so the token only points at a row that must still exist and still belong to that tenant. get_current_admin_user wraps it and raises 403 unless the role is admin. One line makes it safe: never read user state from the request body, because the body is attacker-controlled.

### Slide 5 — M5.1 — Deliberate status semantics

*39.9s · sentence-measured*

> Four rows, and each one is a decision rather than an accident. An invalid bearer token returns 401, because the credential itself failed and nothing is known about the requester. A missing bearer token on a protected route stays at 403, because that is FastAPI HTTPBearer's default, and SignUpFlow documents the behavior it actually has instead of fixing it on REST-purism grounds. An authenticated actor who names a foreign organization gets 403: valid credential, wrong tenant, a policy denial. And a guessed resource identifier returns 404. Hold on to that last one, because it is the mechanism on the next slide.

### Slide 6 — M5.1 — Enumeration dies at `404`

*35.1s · sentence-measured*

> Enumeration dies with one query shape, and the query is now on the slide. get_person_in_actor_org loads the target row with both the id and the actor's organization in the WHERE clause, and raises 404 when nothing matches. So a foreign person and a nonexistent person produce the same answer: a miss. That matters, because a 403 would say exists, but not yours, and an attacker with a perfectly valid account could then walk your id space and map which of your resources exist. Read the exhibit: the filter carries both conditions, the miss raises, and nothing else in the function can leak existence.

### Slide 7 — M5.1 — Growth is invitation-only

*36.2s · sentence-measured*

> How does anyone get into a tenant in the first place? Tenancy is sealed at account creation. The signup endpoint atomically creates a new organization and its first admin, and it never joins an existing organization. There is no public endpoint that creates an empty organization, so a stranger cannot insert themselves into your tenant. Later accounts need a single-use invitation. Growth is invitation-only by construction, and the coverage manifest pins that rule as BO-02: invitations are single-use, and qualifications do not grant administrator access. That last phrase is the whole of the next segment.

### Slide 8 — Proof M5.1 — the rule you can grep

*38.4s · sentence-measured*

> This is the proof slide for segment M5.1, so write these five pointers into your evidence log now: the P0 rule and its classification, the membership and actor-organization lookup, the tenant-bound reload, and the four status rows. They are your provenance for everything you claim in the lab. And the rule itself is now on the slide, exactly as it lives in the baseline document — the grep target: every database query MUST filter by org_id, and a missing filter is a cross-tenant data leak, a P0 bug. The pattern to learn is the shape: rule in the baseline, mechanism in the dependency, contract in the authorization doc, and a test for each.

### Slide 9 — M5.2 — Two vocabularies, one array

*39.3s · sentence-measured*

> A person in SignUpFlow carries one roles array holding two unrelated kinds of strings. Permission roles describe what an account may do, and there are two: admin and volunteer. Qualifications describe what a person can do, things like usher, coach, and worship leader, and the solver uses them to fill role slots. They share the array; they never share meaning. The trap is the natural-language one: she leads worship, so she should have the admin toggle. The church playbook refuses it in one sentence, do not grant admin access merely because someone leads a ministry, and its actors table shows the worship coordinator as volunteer plus worship leader, not admin.

### Slide 10 — M5.2 — Drifted input fails loudly

*40.3s · sentence-measured*

> The policy is not prose; it is executable, and now it is on the slide. In roles.py, normalize_roles takes an admin-supplied array and makes account access explicit, as its docstring says. Exact matches to the permission roles set are permission roles; everything else is treated as a qualification. But the drift cases fail loudly, and both refusals are visible in the exhibit. A case-folded collision like uppercase ADMIN raises: it is an ambiguous permission role. And if the array carries two permission roles, the function raises with the message select exactly one account access role. Those refusals are what make the vocabulary safe: drift can never silently become a permission.

### Slide 11 — M5.2 — The authorization matrix, made executable

*40.0s · sentence-measured*

> Knowing the rules is not enough. Every mounted route has to obey them. The file route_auth_policy.py names every FastAPI operation and assigns it to exactly one of five policy classes. In the current clone there are seven public operations, six scoped-token operations, two public callbacks, fifty member operations, and seventy-eight admin operations, which is 143 classified operations in total. The route auth policy dictionary is the executable source of truth, and the authorization document opens by saying exactly that. A matrix written only in prose rots the first time someone adds a route. A dictionary plus a test does not.

### Slide 12 — M5.2 — Three classes of drift

*37.3s · sentence-measured*

> The enforcement is 37 lines, and it catches three failure classes. Missing means a route with no policy entry; stale means a policy entry with no route. Both are set equality between the policy dictionary and the live route table, so an unclassified route fails the assertion, and an entry for a deleted route fails in reverse. Miswiring is the subtle one. For each classified route, the test collects its dependency tree and asserts that admin routes depend on the admin gate, member routes on the member dependency, and public routes on neither. A policy entry that says admin while the route wired the member dependency is caught mechanically.

### Slide 13 — Proof M5.2 — matrix + gate + protocol

*51.7s · sentence-measured*

> This is the proof slide for M5.2, and the exhibit is the policy file's own docstring: reviewed authentication policy for every mounted API operation, deliberately keyed by FastAPI operation name, because a unit test compares this mapping with the live route table — so a new API route cannot ship without an explicit public, token, member, or administrator classification. Count the classes yourself when you open the file: five sets, 143 operations total. The six-step protocol is what you will write into your own contribution guide. Change the policy entry, apply actor-derived filters in the route query itself, add real-JWT tests for anonymous, invalid, member, same-tenant admin, and foreign admin actors, assert that forbidden writes leave the database unchanged, and refresh the OpenAPI snapshot.

### Slide 14 — M5.2 — The six-step change protocol

*37.1s · sentence-measured*

> Read these six steps as a checklist you can paste into a pull request template. Step two is where the shortcut lives. Apply actor-derived tenant and ownership filters in the route query itself, not in a helper you hope gets called. Step three names five actors you must test with real JWTs: anonymous, invalid, member, same-tenant admin, and foreign admin. Step four is the one most teams skip. A denied write that mutates the database anyway is a security bug wearing a test-green costume, so assert the denial and the unchanged row. Step six is local, because SignUpFlow runs no continuous integration.

### Slide 15 — M5.3 — Seven tiers, separate processes

*40.4s · sentence-measured*

> Seven tiers, and each one proves something the others cannot. Unit tests are fast regressions with mocked auth. The API and security tier runs real HTTP with real JWTs against isolated SQLite, and that is where your isolation tests live. The CLI tier proves the headless path. Integration uses a real database, and mocking the database there is a named anti-pattern. Web covers cookies and HTMX in process; contract snapshots OpenAPI compatibility; browser runs Playwright against a disposable live app. They run in separate processes because the API and browser event-loop fixtures differ. The make test-all target keeps them apart and stops on failure.

### Slide 16 — Proof M5.3 — dated evidence, with a retirement plan

*46.5s · sentence-measured*

> Here is the number you may quote, and exactly how to quote it. In the validation playbook, dated the twelfth of September 2026, the recorded full-suite evidence is 1,464 passed and 21 skipped across the backend, web, contract, and browser suites. The complete unit tier alone was 399 passed and 21 skipped. Now read the banner on the slide, verbatim from the file: historical reference, reclassified the next day, the original observations and counts retained as historical context, not current policy or live test status — use the current testing and merge guide instead. That banner is the mechanism to copy: evidence gets a date, evidence gets retired, and the retirement is visible in the document itself.

### Slide 17 — M5.3 — Playbook acceptance: test the failure mode

*44.6s · sentence-measured*

> Test tiers prove the machinery works; playbooks prove the product can be operated. The playbooks directory ships two six-week scenarios, church and basketball. The church actors table forces every actor into one of three buckets: admin, volunteer plus qualification, or explicitly human. The ministry approver is human organizational responsibility, not a new permission level. The flagship drill is CH-04: block both worship leaders for Sunday of week four, then attempt publication. Acceptance is that the service reports missing worship leadership, publication is rejected, and the prior roster stays live. That tests a failure mode, not the happy path. Acceptance criteria about rejection are what separate a demo from a product.

### Slide 18 — M5.3 — Fixtures parameterize real tests

*42.4s · sentence-measured*

> The scenarios are executable because they are data. The church JSON fixture declares the domain, the workflow, the event, the roles headcount map, the secondary event, the critical role, and drill selectors. A pytest plugin discovers those files, parameterizes tests with stable IDs, and supports a playbook selector. The API tier runs them with real JWT identities against isolated in-memory SQLite, and the browser tier starts the real application on a temporary database at 360 pixels and 1440 pixels. Seven distinct qualified people per event is the fixture's promise. The next slide asks who checks whether the solver kept that promise.

### Slide 19 — M5.3 — An independent oracle, not self-report

*35.9s · sentence-measured*

> Every solve is checked by an independent oracle, and independent is the load-bearing word. The oracle recomputes correctness from the published roster itself: exact role counts, distinct qualified assignees, no person in two slots of one event, no overlaps, and interchangeable people's baseline loads differing by at most one. It never asks the solver whether the solver did a good job. That matters, because the solver's own metric is brutally simple: health is zero if any hard violation exists, otherwise 100 minus the soft score divided by ten. A self-reported score is not an oracle.

### Slide 20 — M5.3 — The manifest is honest by construction

*40.7s · sentence-measured*

> The coverage manifest binds every scenario to an actor, a precondition, an operation, an expected result, execution tiers, evidence paths, and a status. Four statuses exist, and two coupling rules make dishonesty structurally hard. Automated or partial rows must include an executable tier, and manual or blocked rows must include the manual tier. So a blocked scenario cannot be dressed up as automated. In the current manifest all 35 bundled rows are automated, with four carrying a manual tier alongside, which means the reserved statuses are the vocabulary for admitting what is not yet proven. Partial or blocked rows are remaining work, not passed scenarios.

### Slide 21 — M5.3 — Validation happens before collection

*42.8s · sentence-measured*

> The manifest is validated before collection, and that is the detail worth copying. The plugin's configure hook loads the manifest and cross-checks it. Any value error becomes a usage error, so the run dies before a single test executes. The validators are structural, not cosmetic. Shared scenarios must be exactly BO-01 through BO-12. Each domain must carry exactly CH-01 through CH-08 plus its domain drills, and each domain must declare exactly one admin actor and at least one human responsibility boundary. Remove a bundled domain, required scenario, administrator, boundary, or qualification, and collection fails. Scope cannot shrink silently.

### Slide 22 — Lab M5 — Isolate and accept

*40.0s · sentence-measured*

> Lab M5 is pass or fail, about three hours, four steps. You build a minimal FastAPI app with three tables and JWT auth. Step one proves isolation with real-JWT tests: snapshot the target row, attempt the forbidden write, assert the denial, then re-read and assert the row is identical. Step two proves a volunteer with the usher qualification cannot invite. Step three builds a route policy and drift test, and deliberately miswires a route to record the red run. Step four authors a fixture, manifest, and validator, then removes a required id to record that failure. A drift test you have never seen fail is a hope, not a test.

### Slide 23 — Quiz M5 — six MC, two written

*37.4s · sentence-measured*

> The quiz has eight questions: six multiple choice and two short answer. The distractors are the misconceptions we taught against. That 403 is safer than 404, that qualifications imply trust, that SQLAlchemy adds tenant filters automatically, and that all seven tiers run in one process. Question eight is the one to draft before you submit: write the assertion sequence proving volunteer A cannot edit volunteer B's availability and that B's record is unchanged. Name each assertion in order, the status code, and the one assertion most teams forget. The hint is in the module: it involves a forbidden write and an unchanged row.

### Slide 24 — Recap

*41.5s · sentence-measured*

> Six lines, three segments, one through-line. In M5.1, the rule lives in the baseline every agent reads, three mechanisms enforce it, and guessed ids return 404 so enumeration dies. In M5.2, exactly one permission role, qualifications share the array but never confer authority, and the authorization matrix is a dictionary a test compares to the live app. In M5.3, seven tiers each prove something different, playbook acceptance criteria are about rejection, the oracle recomputes from the roster, and the manifest is validated before collection. The through-line: agents generate queries at machine speed, so the guard has to be mechanical.

### Slide 25 — Discussion prompt

*36.4s · sentence-measured*

> Your discussion prompt for this module. Your product stores data for multiple customers, and a teammate argues that foreign keys are enough, so you do not need org filters on every query. Write the reply. Use at least three SignUpFlow file pointers: the P0 rule, the dependency that enforces membership, and the status contract. Name the mechanism that fails without the filter, the status code a guessed foreign id should return and why, and the first test assertion you would write. The hint from the lesson: it involves a forbidden write and an unchanged row. That is the habit this module builds, an argument that ends in a check.

<a id="m06"></a>

# M6 — The Expertise Product: Evidence, Routing, Editions
## Narration transcript

**28 slides · 28 narrated · 16m 14s of audio**

**Voice:** preview narration — a free local voice, not the finished release recording. The audio is spoken by a synthesized voice, not a human recording. The words below are the approved narration and do not change when the release voice is recorded.

The text below is what is spoken on each slide, in order. It is the same text as the captions and the approved narration script, checked word for word by `course/06-production/narration/validate_narration.py`.

---

### Slide 1

*32.8s · sentence-measured*

> Welcome to Module 6, where we take on the third archetype: packaging expertise itself. Modules 2 and 3 shipped an on-device app, and Modules 4 and 5 specced and hardened a SaaS. Here the product is your own research base. Your case study is AI and QE, a research-backed presentation site about modernizing quality engineering in regulated financial services. Its topic is banking QA, but the discipline transfers to any field. The promise of this module is narrow and testable: you will learn to publish claims that a skeptic can audit.

### Slide 2 — By the end you can…

*27.3s · sentence-measured*

> These six outcomes are the module's contract: they are the quiz blueprint and the lab checklist. Notice the verbs — label, keep, hash, re-cut, run, design. Each one produces an artifact someone else can check. That is the standard the case-study repositories hold themselves to: if it cannot be observed, it does not count. The lab turns all six into a single deliverable, a twelve-slide mini-briefing with a provenance table and two audience routes.

### Slide 3 — M6.1 — Credibility is the product

*30.7s · sentence-measured*

> Segment M6.1 makes one argument: in this archetype, trust is the product, and trust is engineered like software. AI and QE looks like an ordinary content site — four narrated decks, a fintech case study, research pages, downloadable PDFs. Underneath, every number carries a citation, a date, a sample, a method and an epistemic label. The site even publishes the things it could not verify. Over the next twenty-five minutes we will take that apart, file by file.

### Slide 4 — The citation is the evidence

*31.5s · sentence-measured*

> Here is the rule that sounds obvious and is almost never followed: the citation is the evidence, and no vendor is endorsed. Every benchmark record carries a date, a sample, a method and a unit, plus whether the result was self-reported or measured, who sponsored it, and what claim it can support. That last field is the one people skip. A number without a stated limit is not evidence; it is an advertisement. Anything unverifiable is listed as unverifiable, and no client or partner is ever named — only the bank, or the sponsor.

### Slide 5 — Benchmark records, side by side

*40.1s · sentence-measured*

> Read two records and the difference becomes visible, and both are now on the slide. The METR entry says AI-allowed issues took nineteen percent longer, with a confidence interval from plus two to plus thirty-nine percent, across two hundred and forty-six real issues. Developers expected twenty-four percent faster, and afterwards believed twenty percent faster — the measured record and the perception point in opposite directions. The Peng entry says fifty-five point eight percent faster, with ninety-five freelancers on one synthetic task. Both records are measured, not self-reported — but one is independent and one is vendor-affiliated, and each record's Supports line states which claim it can carry.

### Slide 6 — Log before you publish

*34.0s · sentence-measured*

> Research gets logged before it reaches a slide. The research log is an intake queue: a new entry is dated and filed first, then it goes into the topic page. Entries are structured as Question, Checked, Outcome, Changed. In the initial evidence base, the outcome states plainly that the only independent randomized controlled trial is negative. And the site keeps a Not verified list, including the World Quality Report cost-of-quality share and any Gartner AI-testing productivity figure. Deleting that list would be easy. Keeping it is what makes the other four entries believable.

### Slide 7 — Provenance manifests

*37.1s · sentence-measured*

> Three files exist only to record where content came from, and the manifest's honest failure is now on the slide. The document manifest lists eleven retrievals, each with a URL, a retrieval date, a status, and a SHA-256 hash of the downloaded file. Entry M02 is the McKinsey PDF, and its status is unavailable, with the reason recorded word for word: the read operation timed out. Read the JSON. A manifest that only logged successes would be a brochure; a logged failure proves the manifest is real. And images are covered too — visual-provenance.md gives even images provenance.

### Slide 8 — Four levels of "saving"

*37.1s · sentence-measured*

> This table comes from the principles file, and the whole site runs on it. Every number is labelled with one of four levels. Task-level efficiency is the net time reduction for one activity, after review and correction, and a pilot can confirm it. QA capacity released is human hours freed across the workflow, and it needs a baseline time capture. A hard-dollar saving is budgeted cost that Finance can actually remove, against a named budget line. Total software-spend impact is broader engineering cost, and it must never be mislabelled as a QA saving. Read the third column: each level names who can confirm it, and it is not you.

### Slide 9 — The mixing error

*33.1s · sentence-measured*

> Now watch the mixing error happen. Take Peng's measured fifty-five point eight percent and try to sell it as a budget number. Coding is roughly sixteen percent of developer time, and code generation is twenty-five to thirty-five percent of idea-to-launch. So a fifty percent task gain dilutes to single digits of total engineering time, before any redeployment or headcount decision. The reading-the-evidence page states that dilution. The same paragraph flags the nineteen percent, the ten to fifteen percent and the roughly two-times figures as perception or per-task numbers.

### Slide 10 — Publish your own audit

*38.2s · sentence-measured*

> The strongest credibility move is to publish your own audit. This review of the site lists fourteen findings: four high priority, nine medium, one lower. Finding R01 is a content inconsistency between two different base-case economics — the site caught its own numbers disagreeing. A companion remediation file is a three-column table: finding, implemented response, verification. A later record even lists deliberate non-changes, such as not hiding weak economics or relabelling unknown results as observed. Findings, responses and refusals all stay published, and skeptics stop asking whether they should believe you.

### Slide 11 — M6.2 — One research base, many audiences

*33.2s · sentence-measured*

> Segment M6.2 is about distribution without duplication. The site has one hundred and sixteen narrated slides, and it serves them as four decks along two axes: executive or technical, and banking scenario or industry perspective. An executive gets the strategic cut. A technical lead gets contracts, sequencing and evidence schemas. Both trace back to the same source records, and nothing is forked, so a correction lands once and appears everywhere. We will also see how one questionnaire turns the same body of work into qualified leads.

### Slide 12 — 116 slides, four decks

*39.5s · sentence-measured*

> The arithmetic shows that nothing is forked. The banking executive deck has twenty-one slides; banking technical, thirty-three; industry executive, twenty-six; industry technical, thirty-six. That is one hundred and sixteen narrated slides across four decks, with running times from twenty-five to sixty minutes. In the briefing room data file, each deck is declared as data: audience, series, cover, URL, PDF prefix, edition, slide count, duration and a full outline keyed by stable slide number. Because the outlines live in data rather than in four hand-maintained documents, the counts stay honest and the routes can be generated.

### Slide 13 — Routes over stable slide IDs

*34.4s · sentence-measured*

> Routes are the second layer. The briefing routes file declares curated sequences over the same stable slide identifiers. The banking executive route plays fourteen of the twenty-one slides, and it declares slide twelve, the brainstorm-questions slide, as its closing endpoint. The full order retains everything. The README's rule is that focused routes end on a decision discussion, while full decks keep the supporting material. The invariant is the slide identifier: a route reorders and omits, but it never rewrites. So a shared route link still resolves to the same slide next quarter.

### Slide 14 — Script the meeting, not the deck

*33.4s · sentence-measured*

> The deck exists to run a meeting, so script the meeting instead. The briefings index suggests a thirty-minute conversation in three parts. Align for five minutes: which part of QA creates the most delay or repeated work? Explore for fifteen: follow one workflow and show the platform services behind it. Agree for ten: choose the process, the owner and the evidence needed for a first pilot, landing on the discovery guide. Notice the shape. It spends half the meeting on the buyer's problem and closes on a decision, not on a feature list. The deck is not the product.

### Slide 15 — Sell the decision, not the transformation

*33.7s · sentence-measured*

> The wording rules here are exact, and they matter. Use phrases like a working hypothesis to be tested on the bank's own data, and say that capacity released is not a saving until Finance confirms how it is captured. Avoid saying that industry benchmarks show thirty to fifty percent productivity gains. Avoid an ROI figure before a pilot has measured anything, and avoid squad-level headcount arithmetic. The executive message ends on the line to remember: the decision today is whether to fund the first two phases, not whether to transform QA. A bounded ask is a decidable ask.

### Slide 16 — The questionnaire is lead qualification

*41.0s · sentence-measured*

> The questionnaire is not a survey; it is the funnel's filter. There is one form, role-routed at the first question, so respondents complete the sections they own and leave unknowns blank. Executive sponsors, Finance and procurement answer Sections 1, 5B and 6. Engineering, delivery, QE and platform leaders answer Sections 2, 3, 4, 5A and 6. Questions that define success — what success means, the autonomy ceiling, the go/no-go threshold — are single-select, because a nuanced multi-select produced no signal. Ranges stay mutually exclusive and gap-free, and an unknown option exists so that a guess is never recorded as data.

### Slide 17 — The failed form, dissected

*38.5s · sentence-measured*

> The same file dissects the form that failed. It had twenty-nine questions and one hundred and eighty-six checkbox options, across nineteen multi-select questions. That takes a knowledgeable respondent twenty to thirty minutes, not fifteen, because every option has to be read before a selection limit applies. And no single respondent could answer all six sections: an executive cannot answer flaky-test questions, and a quality engineering director cannot answer Finance-recognition questions. The largest omission was the financial-capture set. Without it, the same four percent capacity result can be booked as a saving, as cost avoidance, or as nothing.

### Slide 18 — M6.3 — Content as code

*34.9s · sentence-measured*

> Segment M6.3 applies software release discipline to content, and two ideas carry it. First, editions: the site version and the content editions move independently, so a player fix does not invalidate a client's PDF. Second, tests: content changes must pass a build, and a slide that overflows a projector viewport fails like a unit test. Published editions are never overwritten, and changelogs record what was deliberately retained. We then take the same discipline to the commercial end of the funnel, where the product is a phased pilot that measures rather than promises.

### Slide 19 — Editions: site vs content

*35.2s · sentence-measured*

> The release file keeps five separate fields, and the separation is the point. The version identifies the site and the player. The slide, fintech, questionnaire and research editions each move on their own schedule. Here the version advanced to one point twenty-four point one, while the slide edition deliberately stayed at one point twenty-four point zero. The rule is that public content changes require a new edition before deployment, and content changes without one are rejected on main. Why keep two numbers? Because a client holding a version one point twenty-four point zero PDF needs to know exactly what they have.

### Slide 20 — Changelogs record what is retained

*39.5s · sentence-measured*

> Open the changelog at version one point twenty-four point one. It says subtitles now use the available player width, and then it states explicitly that audio, subtitle timing and the version one point twenty-four point zero PDF editions remain unchanged. That sentence is the discipline: a changelog records what changed and what was deliberately retained. Immutability is enforced, not aspirational, because the contributing guide says an existing published edition is never overwritten. One tool assembles the PDFs, the MP4, the captions and the source registers with checksums, and the publish tool verifies the SHA-256 digests before anything goes out.

### Slide 21 — `make check` — content needs tests

*42.9s · sentence-measured*

> Content needs tests, so the check target is models, build, site, browser — and the Makefile line is now on the slide, four words that everything hangs off. The models step runs the npm tests, the Python unit tests, narration validation with require-complete, and contract validation. The browser step runs five CI-identical groups — playback, flows, site, models and architecture — in both Chromium and WebKit, at three viewports: 1280 by 720, 1920 by 1080, and 375 by 812. An overflowing slide fails like a unit test. Links are checked too, and a 200 alone is not proof.

### Slide 22 — Hash-gate the media

*34.5s · sentence-measured*

> One hundred and sixteen slides carry recorded narration, so a silent slide edit would desynchronize the voice from the slide. The narration-review tool hashes each rendered slide together with its script, its recording, and its caption-flow definitions, and every verdict lives in a JSON file like the entry on the slide: a decision, and a reason written in full sentences. If a destination changes, you must make a deliberate choice — retained or refreshed — and record why. Never reset the baseline to silence a stale-review failure: a baseline reset rubber-stamps the drift you erased.

### Slide 23 — The pilot is the product

*31.0s · sentence-measured*

> The pilot is the product, and the whole funnel points at it. There are five phases, zero through four, each with an objective, a duration, deliverables and a cost ceiling. Effort is quoted in person-day ranges and deliberately never converted to dollars, and every phase ends with a written go/no-go memo signed by the sponsor. Measurement freezes the goal before any result exists: you record the primary outcome and the acceptance criteria before you observe pilot results, and you never choose a different success metric after seeing a favourable one.

### Slide 24 — Gates live in data

*33.9s · sentence-measured*

> The exact boundaries live in data, not in prose that someone can soften later. You need a fifteen percent net-effort improvement to go, with a ten percent review band. The baseline runs three weeks, the pilot eight weeks, across two observed releases, with at least thirty comparable tasks per arm and one possible extension of up to four weeks. Here is the rule that separates this from every pilot you have suffered: a confidence interval that crosses ten or fifteen percent is insufficient evidence for that boundary, even when the point estimate looks favourable. A noisy result is no result.

### Slide 25 — Lab M6 — Build a mini-briefing

*32.7s · sentence-measured*

> Lab M6 is the checkpoint for the third archetype. You produce five artifacts. A research log with at least six dated entries in the Question, Checked, Outcome, Changed format, including at least two not-verified items. A provenance table with one row per claim. A twelve-slide outline where every quantitative slide cites a row by number. Two routes over those same twelve slides, one executive and one technical. And an edition decision record for a hypothetical version two. The pass conditions are binary, and nothing is graded on taste.

### Slide 26 — Quiz M6

*32.2s · sentence-measured*

> The quiz has eight questions, each mapped to exactly one segment objective, and that mapping is printed with the answer key. Six are multiple choice and two are short answer. The multiple-choice distractors are the misconceptions we taught against: treating a working HTTP response as proof of a claim, choosing a balanced combination on the outcome question, bumping every edition together, extending a pilot until the interval excludes the boundary, and republishing over a released edition. Take the quiz after the lab. The two short answers are the real assessment.

### Slide 27 — Recap

*32.1s · sentence-measured*

> Six lines to carry out of this module. The citation is the evidence, and research gets logged before it reaches a slide. Label every number with one of the four levels and never mix them. Publish your own audit: fourteen findings, a remediation table, and refusals that stay published. Route one research base of one hundred and sixteen slides into four decks whose guided routes end on a decision. Put content under edition discipline, where tests gate the change and published editions are immutable. And finally, sell measurement, not outcomes.

### Slide 28 — Discussion prompt

*30.6s · sentence-measured*

> Before you go, here is a discussion prompt. Find one quantitative claim from your field's public discourse that mixes the levels — a task-level number presented as a budget saving, or a self-reported figure presented as measured. Post the claim as written, name the level it actually belongs to, name the level it is being sold as, and write an honest replacement in one sentence, borrowing the tone of the Use list from the slide-language file. Then answer the real question: does the honest wording weaken the pitch, or sharpen the ask?

<a id="m07"></a>

# M7 — Monetize: Pricing, Packaging, Positioning
## Narration transcript

**28 slides · 28 narrated · 15m 47s of audio**

**Voice:** preview narration — a free local voice, not the finished release recording. The audio is spoken by a synthesized voice, not a human recording. The words below are the approved narration and do not change when the release voice is recorded.

The text below is what is spoken on each slide, in order. It is the same text as the captions and the approved narration script, checked word for word by `course/06-production/narration/validate_narration.py`.

---

### Slide 1

*29.7s · sentence-measured*

> Welcome to M7, Monetize: Pricing, Packaging, and Positioning. In Modules 1 through 6 you built three working product cores; today you price them. The promise is plain. By the end of this module you will have chosen a pricing model per archetype from a sourced table, computed a cost floor, and written a positioning line a skeptical engineer can falsify. We have about 60 minutes together, roughly 20 minutes per segment, and we start with the one decision rule that removes the guesswork.

### Slide 2 — By the end you can…

*40.9s · sentence-measured*

> Treat these as six graded outcomes, not aspirations. You will price each archetype from competitive evidence, compute a cost floor before setting a price, and package transformation and artifacts rather than video hours. You will choose platforms by channel economics, deliberately, and derive a falsifiable positioning one-liner. You will also survive the skeptical-engineer review. Lab M7 asks for all six artifacts: a sourced pricing table, a decision worksheet, a one-liner with a clause-to-column mapping, a packaging page with explicit exclusions, three answered buyer objections, and the honest-marketing checklist run. Quiz M7 checks the same objectives.

### Slide 3 — M7.1 — Price the way your costs recur

*31.2s · sentence-measured*

> Here is the thesis for this segment. Every monthly-priced tool in this category runs per-user compute in the cloud; every one-time-priced tool runs inference on the user's machine. That gives you the rule. If your per-user costs recur monthly, price monthly. If they do not recur, a subscription is a tax your users can audit you against. Cloud per-user compute costs recur every month, and that recurring cost is what makes a subscription honest. On-device compute recurs zero times per user. Start with evidence, then choose the model.

### Slide 4 — The competitor table is your raw material

*36.1s · sentence-measured*

> This is the file where the pattern is recorded: the competition analysis document, holding thirteen competitor rows plus ListenToMe, dated September 2026. The header is now on the slide, and the header is the convention: every price fact is stated as of that date, and where a detail could not be confirmed from a primary source it is qualified as approximately or reportedly. The price column carries model, price, and channel — the commercial tiers in that column run about eight to one hundred forty-nine dollars a month. Read rows, never headlines: the table is raw material for your own positioning, not a market summary to quote.

### Slide 5 — Recurring compute sets the model

*30.2s · sentence-measured*

> Walk these four rows. Granola and Otter both spend per user per month on cloud transcription and cloud summarization, so their monthly price is a pass-through of a recurring cost. Fireflies runs cloud ASR and cloud AI, and prices monthly as well. MacWhisper runs Whisper on-device, so its marginal cost per user is near zero, and it charges once, about 59 euros or roughly $69. The pattern is structural, not stylistic: the pricing model tracks who pays for the compute.

### Slide 6 — Free and open-source is a price

*33.8s · sentence-measured*

> A price of zero is a decision, not an absence of one. ListenToMe prices at $0 under an MIT license, and it offers code open for inspection against rivals charging $8 to $149 a month. Free still has a business model attached. The paying surfaces named in the syllabus are the reputation funnel, support, and a Pro tier. The peer evidence is Natively, whose row reads free personal with Pro via lifetime or yearly. State the rule: the paid tier sits above a complete free core, never as a repair of a deliberately crippled one.

### Slide 7 — The wedge rivals cannot copy cheaply

*34.3s · sentence-measured*

> There are two category tensions. The first is privacy versus convenience: nearly every commercial product processes audio and runs its AI in the cloud, even when it markets itself as local-first, and the local part usually means just audio capture. The second is opinionated versus open: most products lock you to one undisclosed transcription engine and one summarization LLM. The wedge holds because their monthly price pays for the cloud compute that this wedge removes. Copying it means rebuilding the pipeline and the revenue line at once. Durable wedges are expensive in business-model terms.

### Slide 8 — Type 2: gate what is not proven

*35.6s · sentence-measured*

> Open the SignUpFlow README section on provider-backed features. Billing routes remain in the codebase under the versioned API, and SMS routes under their own path, but both return 404 by default behind two flags, billing-enabled false and sms-enabled false. Paid billing and SMS are deferred, and the complete scheduling workflow does not require them. The project's agent rules go further: core scheduling must not require either paid integration. That bars two failure modes at once. You never charge for a path that is not trustworthy yet, and you never gate the core workflow to force upgrades.

### Slide 9 — Invitation growth produces the billing event

*29.7s · sentence-measured*

> The README's onboarding section says existing organizations reject public signup, and every later member is added through an administrator-created invitation. The signup route creates the organization and its first admin atomically, and later members join by token, with no email required. That makes growth and billing the same event. Every new member is an invited org member, so per-seat pricing tracks real adoption, and the person who invites is the person who pays. Design the growth loop so it emits the billing event.

### Slide 10 — The funnel that sells measurement

*39.8s · sentence-measured*

> The AI QE funnel is visible in its own files, not in a pitch deck. The evidence site routes the visitor through four path cards ending at a discovery page, which ends in a questionnaire download. The engagement data records the staged timeline: two weeks of sponsor alignment, four to six weeks of baseline and readiness, an eight to ten week capped pilot, then one to two quarters of limited validation. Read the table as a qualification sequence. The free evidence site qualifies trust, the questionnaire qualifies fit and scope, fixed-fee discovery qualifies budget and sponsor, the capped phased pilot decides whether to scale, and validation earns renewal on evidence.

### Slide 11 — Sell measurement, not outcomes

*35.3s · sentence-measured*

> This consultancy never promises a savings number. The executive workshop shows questionnaire results as questions rather than conclusions, with no savings number yet, and that is deliberate. The pricing-integrity device is the benefits-realization register, which ties every claimed saving to a Finance-owned budget row, so an inflated number is checkable by the client's own finance function. Price what you deliver: discovery, baseline, and an instrumented pilot. Let outcomes belong to the register. As your action step, write one sentence per archetype naming who pays, and when.

### Slide 12 — Action step — M7.1

*30.3s · sentence-measured*

> This two-minute action step closes segment one. Write one sentence per archetype naming the pricing model for your product, who pays, and at which stage they pay. Here are two worked shapes. One: a one-time price justified by a zero marginal cost. Two: a per-seat price, billed at the moment an admin invites another member. Post your three sentences to the community. Lab M7 will make you defend each sentence with a sourced table and a cost floor, so the sentence is a claim, not a preference.

### Slide 13 — M7.2 — Cohort and self-paced are different products

*42.0s · sentence-measured*

> Same content, two value propositions. As a rule of thumb, self-paced courses sit around $97 to $297, while a live four-week cohort runs $500 to $2,000 or more. Maven's published benchmarks give the shape of the cohort price: eight to twelve live hours plus projects prices at $1,200 to $1,800, and twelve to twenty live hours plus a capstone prices at $1,800 to $2,450. The cohort buyer is paying for live instruction, peer interaction, and feedback, which is exactly what those live-hour bands price. You will use these bands as a comparator in Lab M7.

### Slide 14 — The fraction-of-live-price rule

*34.1s · sentence-measured*

> Here is the rule that connects the two prices, and the research line is now on the slide. Self-paced should be priced as seventy to eighty-five percent of the live cohort price, but only if it keeps projects, async feedback or office hours, and community. Strip all three and the research verdict is blunt: a stack of Zoom recordings is not a self-paced course. A bare video library should not be sold at all — the sentence sits in the market research file with the percentages next to it, so the rule and its exception travel together. Ask what the buyer can show for the money, at every rung of the ladder.

### Slide 15 — Marketplace vs own platform

*36.0s · sentence-measured*

> This decision is not about reach alone; it is about margin and the customer list. Udemy pays a 37% marketplace payout, and marketplace-wide that worked out to 32 cents per dollar in 2025. The platform controls pricing, down to $9.99 flash sales, and there is no student-email export, so you do not keep the customer relationship. Own-platform creators instead charge $50 to $200 or more. Use the marketplace for discovery and validation, never as your primary channel. The course's own platform table is the worked decision.

### Slide 16 — Store vs direct is reach vs margin

*37.6s · sentence-measured*

> MacWhisper is the natural experiment, because it sells on two channels at once. On Gumroad it is about 59 euros, roughly $69, as a one-time purchase. On the App Store the same product runs $6.99 a month up to $99.99 lifetime. The store adds subscription expectations and brings reach, but it takes a cut and owns the customer. Direct gives you margin and the email address. Direct is not a compromise for a small team, because the release machinery already exists: signed, notarized, stapled releases targeting an exact commit. Choose per product.

### Slide 17 — Compute the floor before the price

*30.0s · sentence-measured*

> This is the course's own arithmetic, and the line is now on the slide. Walk it: Maven's per-course fee on enrollment, Thinkific at about fifty-four a month or a Gumroad-only start, Circle at about forty-nine a month or zero on Discord, and email at about twenty-nine — roughly eighty to one hundred thirty dollars a month in fixed cost plus per-enrollment fees. At the three hundred ninety-nine dollar self-paced tier, that is about two sales a month to break even. A price below your floor is a subsidy: you fund every sale you make.

### Slide 18 — The worked example is this course

*51.1s · sentence-measured*

> Now read that method applied to a real product: this course. A $0 lead product feeds a $399 self-paced tier, a $1,490 cohort with a $990 founding price, and a $2,500 to $4,000 team tier for three to five seats. Each rung is defended in both directions. Why not cheaper: courses priced at $950 or more earn 50 to 100% more per landing-page visit, and $500 to $1,500 programs complete at 53 to 68%, against 18 to 25% at $97 to $197. Why not more: no public testimonials exist yet, and raising price before social proof inverts the trust order. The founding discount buys a testimonial and an interview.

### Slide 19 — Action step — M7.2

*28.3s · sentence-measured*

> Two artifacts, both short. First, compute your monthly cost floor: hosting, API keys, and amortized dev time. Dev counts as zero only if it truly is, the way SignUpFlow's SQLite-in-dev line is zero. Second, write your two-sentence why-not-cheaper argument, citing one benchmark from the market research. Post both to the community, and paste both into the Lab M7 worksheet. They paste directly, so the post is not busywork.

### Slide 20 — M7.3 — The hero is the buyer

*29.6s · sentence-measured*

> The reframe here is grammatical. The buyer is the subject of every sentence, and you are the guide who has already walked the path. Every page section answers the buyer's question: does this get me there, and can I trust you? For a technical audience, the proof assets are concrete: the repos, the demos, the dated evidence lines, and the test badges you have been recording since Module 1. Shipped projects are social proof. Never invent a testimonial, and ship beta before claiming social proof.

### Slide 21 — Sales-page anatomy: eight sections

*44.0s · sentence-measured*

> This eight-section template is drawn from more than 32,000 courses, and the research records that a restructure along these lines took one creator from 1% to 8% conversion. The sections are: a transformation headline; who it is for and who it is not; problem and stakes; outcomes per module; instructor proof in 100 to 150 words; testimonials with before, after, and result; an FAQ of real objections; and transparent pricing with one call to action. Length scales with price, from 800 to 1,200 words under $200, up to 2,000 to 3,000 for $500-plus or cold traffic. Today, draft the skeleton and write sections one, two, and five.

### Slide 22 — Skepticism converts

*28.8s · sentence-measured*

> This is the strongest evidence in the module, and it comes from a real product's own files. The AI QE site publishes that the only independent randomized controlled trial is negative, and it stamps its planning numbers with the qualifier that planning inputs are not observed client results. The observed effect is that the executive's question changes. Why should I believe you becomes: when can we start? Qualified claims with sources are a premium signal, because you audited yourself harder than the buyer would.

### Slide 23 — Derive the one-liner from the table

*34.0s · sentence-measured*

> Here is the one-liner: ListenToMe is the free, open-source, fully on-device meeting copilot for macOS. Bring your own model, run it private, and shape it to any conversation. This sentence was derived, not composed; it was built clause by clause from the comparison table, and each clause maps to a column that proves it, from the price column for free to the focus presets for the last clause. Apply the deletion test out loud. Remove a clause and the sentence must become false against a specific row; if no row would notice, the clause is decoration, and it gets cut.

### Slide 24 — Action step — M7.3

*27.4s · sentence-measured*

> Insist on for real for sections one, two, and five: a transformation headline, who it is and is not for, and instructor proof citing an artifact that exists, whether a repo, a test run, or a dated evidence line. The honest-limitation line is the one that earns the rest of the page its credibility, so write it even when it stings. Post the headline and the limitation to the community for peer review. Module 8 turns the skeleton into the full sales page.

### Slide 25 — Lab M7 — Price and position your product

*38.4s · sentence-measured*

> Lab M7 runs two hours, in your product repo, as a pricing document and a positioning document, or one combined monetization document. Five steps: a sourced pricing table with at least five rows; a decision worksheet with a rationale of at least 150 words; a one-liner plus its clause-to-column mapping; a packaging page with explicit exclusions; and three buyer objections, answered. The pass gate is that every acceptance-checklist item is objectively verifiable. Watch the two most common failures: prices recalled from memory instead of retrieved, and a subscription attached to a product with no recurring per-user cost.

### Slide 26 — Quiz M7 — what it checks

*26.2s · sentence-measured*

> The quiz has six multiple-choice questions and two short answers. It checks that your model matches your cost structure when costs recur, flag-gating what is not proven, the funnel order and what each stage qualifies, the fraction-of-live-price rule, and the one-liner format with honest limitations. Six of eight passes, consistent with the module standard. The quiz is open-book in spirit: every answer is traceable to a file pointer in the answer key.

### Slide 27 — Recap

*26.8s · sentence-measured*

> Compress the module to six lines. Price the way your costs recur. Wedges must be costly in business-model terms. Gate the unproven, but never gate the core. Sell measurement, and let outcomes belong to the register. Package the transformation, not the recording. Derive the one-liner, and qualify every number. If you remember one thing, make it the first line and the last: the model tracks the cost structure, and every number carries a source.

### Slide 28 — Discussion prompt

*26.5s · sentence-measured*

> This prompt is deliberately uncomfortable. Name the claim on your draft page you are least comfortable defending to a skeptical engineer, then write its what-this-doesn't-prove version and the source you would attach, and decide whether you would publish the qualified version, and why. In your peer replies, name one clause in a peer's one-liner that their own table would falsify, and one clause that survives the deletion test. This closes the module and seeds Lab M7 Step 5.

<a id="m08"></a>

# M8 — Launch: Sales Page, Email Arc, Capstone
## Narration transcript

**27 slides · 27 narrated · 14m 21s of audio**

**Voice:** preview narration — a free local voice, not the finished release recording. The audio is spoken by a synthesized voice, not a human recording. The words below are the approved narration and do not change when the release voice is recorded.

The text below is what is spoken on each slide, in order. It is the same text as the captions and the approved narration script, checked word for word by `course/06-production/narration/validate_narration.py`.

---

### Slide 1

*25.1s · sentence-measured*

> Welcome to the final module. Modules one through seven built the machine: the operating system, three builds, and the monetization package. This module closes the loop with the three things that turn shipped work into a business — the page that sells, the emails that arrive, and a capstone that ships version one with recorded evidence. Every example here is checkable against the course's own sales assets, which are the worked examples.

### Slide 2 — By the end you can…

*32.8s · sentence-measured*

> Six abilities, and four of them are writing or modeling tasks; the other two are shipping tasks. Notice the verbs: write, source, run, model, ship, deliver. Nothing here says understand marketing. By the end you will write a converting sales page in eight evidence-backed sections, source every proof claim from artifacts you already own, run a seven-email arc with deliverability configured first, model launch revenue and then record actuals honestly, ship version one through the full Spec-to-Ship Loop, and deliver a five-minute demo that ends on limits.

### Slide 3 — The page is a sequence, not a pile

*27.4s · sentence-measured*

> A page is an argument in eight moves, in order, and each section has one job. Sell the destination first, then prove it. The order carries the conversion, not the volume. That anatomy comes from a template distilled across thirty-two thousand courses and one point three million enrollments. One creator restructured an existing page onto this order and moved from one percent to eight percent conversion. Read that carefully: it was the order, not new copywriting tricks.

### Slide 4 — The eight sections (M8.1)

*37.2s · sentence-measured*

> Here is the core rule: eight sections, eight jobs. The transformation headline is a falsifiable sentence naming the destination. The who-it-is-for section qualifies the right buyer in and repels the wrong one, which cuts refunds and protects completion. Then come problem and stakes, curriculum as outcomes, a short instructor bio, testimonials, an FAQ that answers the real objections plainly, and transparent pricing with one repeated call to action. Section five is capped at one hundred to one hundred fifty words because relevance beats autobiography, and section eight is a discipline problem, not a copy problem.

### Slide 5 — Proof: the course's own page maps row for row

*40.7s · sentence-measured*

> Open the course's landing page beside this and check each row — and the headline and the is-not list are now on the slide. The headline is one falsifiable sentence: ship three real AI products, learn from code that actually shipped. The for and is-not lists are explicit — not for you if you have never written code, want prompt-engineering trivia, or need an enterprise compliance curriculum. The problem section names three things that are always missing, and the curriculum table lists abilities rather than topics. The proof section is three named repos with checkable numbers. The testimonial section has three reserved slots — reserved, not filled — a real-objection FAQ, three tiers, and one CTA.

### Slide 6 — Section 4 is where technical pages fail

*27.4s · sentence-measured*

> Technical authors default to a syllabus: week three covers privacy. That describes content, not a change in the reader, and the reader cannot evaluate it. The house standard is an outcome line. Week three, run an LLM locally: you will ship a hardened local-only mode. Same content, but now it is a claim the buyer can hold you to, and it maps straight to a lab checkpoint. Write one line per module. If you cannot name the ability, the module is not finished.

### Slide 7 — Section 8: pricing discipline

*26.3s · sentence-measured*

> Two rules, both mechanical. First, every tier and every price is visible, with no hidden price and no contact-us tier unless it genuinely is a contact tier. Second, exactly one call to action, repeated verbatim at the top, middle, and bottom. Competing calls to action leak the click and give the reader a way to do nothing. The pricing file also commits to no fake countdowns, and that same policy is what your launch arc depends on.

### Slide 8 — No testimonials yet? Say so.

*29.8s · sentence-measured*

> This is the honest-move slide. The course had no students when the page was written, so it invented none and reserved three slots instead, labeled with the before, after, result format. What carried the section meanwhile was the badge strip: three repositories, a coverage number, a dated test count, and a slide count. For a technical audience, real shipped projects are the social proof. A founder-written quote is fabrication, and the evidence discipline from module one applies to marketing identically.

### Slide 9 — Proof: your M1–M7 inventory feeds the page

*33.1s · sentence-measured*

> Every row here is an artifact you already own. A public repository with a tag or URL feeds the hero proof line. A dated evidence line feeds the proof section and the bio. A coverage number or test badge feeds the badge strip. A spec folder a buyer can read feeds the proof section, and a provenance table with reconciled claims feeds the type three proof. The recorded demo from the capstone substitutes for a testimonial before you have buyers. If a claim has no row in this inventory, you have two honest options: build the proof, or state the gap and reserve the slot.

### Slide 10 — Length follows price

*30.8s · sentence-measured*

> Length follows price, and the reason is stakes. The more a reader pays and the less they know you, the more objections the page has to answer. Under two hundred dollars, target eight hundred to twelve hundred words. Five hundred dollars or more, or cold traffic, target two to three thousand. The course's own page runs about nineteen hundred words of copy for a three hundred ninety-nine to one thousand four hundred ninety dollar offer. Longer always converts better is false in both directions, so set your word target before you draft.

### Slide 11 — M8.2 — Two phases, seven emails

*32.4s · sentence-measured*

> The arc has two phases and seven emails, and the phase structure never changes. Warmup earns trust; it does not sell. Conversion spends the trust that warmup earned. Warmup covers the origin story, transformation proof, and a free tool. Conversion covers cart open, objections, proof, and the final call. Read the free tool email as the hinge: it delivers your method in miniature in ten minutes, which is the only honest way to ask for attention later. One idea per email, one call to action per email, no exceptions.

### Slide 12 — The seven emails

*33.1s · sentence-measured*

> The launch plan's own arc is the worked example, so adapt it rather than admire it. Email one is the origin story and its receipts. Email two walks one artifact end to end. Email three delivers the method in miniature. Then cart open with offer, mechanics, price and guarantee; an objection teardown that treats the FAQ as answers, not marketing; a testimonial only if it is real; and a short final call with a real deadline. Warmup runs week minus four to minus one in notify-me mode, and the cart opens at week zero for ten to fourteen days.

### Slide 13 — Warmup does not sell

*31.7s · sentence-measured*

> This is the most common launch mistake, and it is expensive. If every email asks for money, the list learns that opening your email costs something, and by the time the cart actually opens your open rate has collapsed. The idea that all emails should sell is the taught-against error. Warmup runs weeks minus four to minus one with the page in notify-me mode. The cart opens at week zero for ten to fourteen days, objections come at plus one, proof at plus two, and the final call in the last seventy-two hours. The free lead product builds the list first.

### Slide 14 — The final 48 hours

*31.2s · sentence-measured*

> Forty-two to fifty-five percent of enrollments arrive in the final forty-eight hours. That figure is why the deadline exists at all. It describes how buyers behave, which means deferred decisions collapse at a real deadline. That makes the deadline load-bearing, and its honesty a revenue asset. A resetting countdown trains the list to wait, and the next launch's final forty-eight hours pay the price. The cart actually closes and the price actually ends. For real urgency in a first launch, use the founding discount with a stated end date.

### Slide 15 — Model it before you run it

*38.9s · sentence-measured*

> Multiply the five factors in order: list, times open rate, times click rate, times page conversion, times price. Twelve hundred subscribers at thirty-eight percent open, fifteen percent click, sixteen percent page conversion and a seven hundred ninety-seven dollar price gives about eight thousand seven hundred sixty-seven dollars, which is roughly four hundred fifty-six opens, sixty-eight clicks, and eleven enrollments. Warm lists convert two to five percent overall, so one pass is deliberately conservative, because each conversion email sends the reader through the funnel again. Then record actuals after the launch and re-derive the model.

### Slide 16 — Five levers, five honest moves

*32.4s · sentence-measured*

> Five levers, and each one has an honest move. Build the list with the free tool and repository readmes, and never purchase a list, because a bought list destroys sender reputation and every other lever with it. Open rate comes from skeptic subject lines, list scrubbing, and opt-in only. Click rate comes from one call to action matched to the email's one idea. Page conversion is the module 8.1 page, which is exactly why that page comes first: it multiplies everything upstream. Price is module seven's decision, not launch-week panic.

### Slide 17 — Proof: deliverability is upstream of every number

*38.5s · sentence-measured*

> No math survives the spam folder, so this work comes before the sequence is queued, not after the first weak send — and the prerequisite lines are now on the slide, verbatim from the launch plan. Configure SPF, DKIM, and DMARC before the first email. Gmail and Yahoo enforce this for bulk senders, so it is an infrastructure requirement now, not a best practice. Test-send to a Gmail and a corporate address — the checklist says verified, not assumed. Scrub hard bounces and keep the list opt-in only. A spam-folder email has an open rate of zero, and every percentage in the sequence is downstream of that checkbox.

### Slide 18 — The beta-discount trade

*33.7s · sentence-measured*

> Email six needs a before, after, result testimonial, and you have no buyers yet. So you trade cohort one's discount for proof. The course's own founding tier is nine hundred ninety dollars against one thousand four hundred ninety, and the trade is now on the slide, stated on the page exactly as the learner should state theirs: founding cohort, nine ninety, in exchange for a testimonial and feedback. The discount has a reason and a receipt; a discount with no reason trains buyers to wait. The cautionary tale is in the research: Udemy's nine-ninety-nine spiral.

### Slide 19 — M8.3 — The capstone contract

*31.4s · sentence-measured*

> Here is the capstone contract: one archetype, one shippable scope, and the complete Spec-to-Ship Loop with evidence. The rubric scores the loop, not the size, and no dimension counts lines of code. That means a deliberately small product taken through study, spec, build, validate, release and prove will out-score a sprawling build that never reached validation. A small complete loop beats a sprawling half-loop. If you are trying to touch all three archetypes, you are building the wrong thing, because the labs already gave you all three.

### Slide 20 — Proof: the loop, mapped to what you built

*34.3s · sentence-measured*

> The capstone extends your labs; it does not restart them. Every row's middle column is a real artifact from an earlier module: the competitor table, the spec-kit folder, the contract test, the playbook manifest, the tagged release. The third column says what the capstone must add or re-run for the shipped scope. Reuse and cite for study, the folder or equivalent for spec, a failing test first for build, tiers run and recorded for validate, a verified tag or URL for release, and evidence, page, arc and demo for prove. Read the lab's scope table before you choose.

### Slide 21 — The five dimensions (3 = meets)

*35.2s · sentence-measured*

> Five dimensions, zero to five each, weighted equally, and three means meets. Spec quality means complete artifacts and testable stories. Build discipline means a failing test first and small commits. Evidence honesty means commands, counts, a date, and limits. Dimension four is the archetype-dependent one: privacy and safety engineering for the on-device and SaaS types, claim discipline for the expertise type. Launch-readiness covers positioning, page, arc and demo. The pass rule has two halves: at least eighty percent total, and no dimension below three.

### Slide 22 — The evidence record: three blocks

*31.1s · sentence-measured*

> The evidence record has three blocks, and they are non-negotiable. Commands run, with results, means the command and its pass or fail counts, not a summary sentence. Artifact links means the repository at a tag, the spec folder, the evidence log, and the sales page draft. Limitations means the honest list, failures included. The gap review that said do not ship is worth more to your grade than a green badge. State what the agent did versus what you verified. A fabricated result is the only automatic fail.

### Slide 23 — The five-minute demo

*29.0s · sentence-measured*

> Four beats, five minutes. The problem beat is thirty seconds, so resist the origin story. The loop walkthrough gets two minutes and one artifact per stage, which forces you to have one. The live demo is two minutes of the thing actually running; if it cannot run, that is a finding. Then evidence and limits in the last thirty seconds, ending on limits, where a technical audience decides whether to believe the first four minutes. Record it or run it live at demo day, and keep it to five thirty or less.

### Slide 24 — Lab M8 — Capstone

*30.2s · sentence-measured*

> This is the largest lab in the course: six to ten hours over one to two weeks, ending at demo day in week eight for the cohort. The goal is to ship version one through the full loop with evidence. Your deliverables are the spec, the test-driven work, validation, release, page, arc and demo. The pass gate is the rubric at eighty percent or better, with nothing below three. The public link must be verified from a clean browser, the evidence record complete, and the peer score exchanged. Post the plan first.

### Slide 25 — Quiz M8

*31.7s · sentence-measured*

> Take the quiz before the workshop, whether cohort or self-paced. It is eight questions: six multiple choice and two short answer. The distractors are the misconceptions we taught against, so expect longer pages always convert better, draft your own testimonials, all emails should sell, and the capstone is graded on code size. The two short answers are applications: compute a revenue model and say which improvements you would refuse, and list the evidence record's three blocks plus the one automatic fail. The key is in the quiz file.

### Slide 26 — Recap — the loop, closed

*28.4s · sentence-measured*

> Six lines, and they are the module. The page is eight sections in a proven order, sized by price. Proof comes from artifacts you already own, or from a reserved slot with an honest note; never invent social proof. Warmup earns, conversion spends, and the deadline stays real. Model revenue, configure deliverability, then record actuals. The capstone is one archetype and one scope with the whole loop complete, because the rubric scores the loop, not the size.

### Slide 27 — Discussion prompt

*27.8s · sentence-measured*

> This is the closing prompt of the course. Name the one claim on your draft page you are least sure you can source, then either point at the artifact that makes it honest, such as a test badge, a dated evidence line, a spec folder, or the demo, or write the honest placeholder sentence if no artifact exists yet. Then do the useful half: read a peer's post and name a proof asset they already own but forgot. The course answered this exact problem with three reserved slots and a badge strip.
