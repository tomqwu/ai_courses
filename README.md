# AI Product Studio

**A complete, market-ready online course — "Build, Ship & Sell 3 Types of AI Products" — reverse-engineered from three production open-source repositories, verified with the same evidence discipline it teaches, and delivered as a narrated static site.**

This repository is the product. The three repositories the course is built from are cloned alongside it (they are upstream projects with their own history, so they are not vendored here):

| Archetype | Case study | Verified proof |
|---|---|---|
| Native on-device AI app | [ListenToMe](https://github.com/tomqwu/ListenToMe) — macOS/iOS meeting copilot | 96% core coverage · 95% CI coverage floor · 14-row competitor table · 1.3.0 held back on 2026-09-10 at 97.24% (1.4.4 shipped since) |
| Spec-driven AI SaaS | [SignUpFlow](https://github.com/tomqwu/SignUpFlow) — volunteer scheduling | 1,464 passing tests · 7 test tiers · 17 spec folders |
| Expertise content product | [ai_qe](https://github.com/tomqwu/ai_qe) — "AI × QE" briefing site | 116 narrated slides (21+33+26+36) · four claim levels · 14-finding self-audit |

## Start here

| I want to… | Go to |
|---|---|
| **Learn it** | `make -C course narration-preview && make -C course serve` → <http://localhost:8043> |
| **Just read it** | [`course/learner-site/transcripts/ALL.md`](course/learner-site/transcripts/ALL.md) — every word spoken, all nine modules |
| **Teach it** | [`course/02-instructor/instructor-guide.md`](course/02-instructor/instructor-guide.md) |
| **Understand the design** | [`course/01-design/positioning.md`](course/01-design/positioning.md) → [`curriculum.md`](course/01-design/curriculum.md) |
| **Sell it** | [`course/04-sales/`](course/04-sales/) — publish-ready landing page, pricing, launch plan |
| **Sell one archetype** | [`course/05-tracks/`](course/05-tracks/) — three standalone $199 bundles |
| **Verify it** | `make -C course check` (or `bash course/check.sh`) · `make -C course facts` for upstream number drift |
| **Review it** | [`course/00-research/04-platform-review-2026.md`](course/00-research/04-platform-review-2026.md) — the September 2026 review against industry practice, with the platform plan and roadmap |
| **See the whole map** | [`course/README.md`](course/README.md) — the detailed package map |

## Repository layout

```
ai_courses/
├── course/                    ← the entire sellable course package
│   ├── 00-research/           deep reads of the three repos + course-market research (cited)
│   ├── 01-design/             positioning, curriculum, content standards (binding), rubrics
│   ├── 02-instructor/         cohort cadence, workshop scripts, grading workflow
│   ├── 03-content/            the course itself — 9 modules × 11 documents
│   ├── 04-sales/              landing page, pricing ladder, launch plan, free lead product
│   ├── 05-tracks/             3 standalone bundles ($199 each)
│   ├── 06-production/         how the package is built and verified (instructor-facing)
│   │   ├── narration/         scripts → TTS → captions → manifest → validate
│   │   └── verify.py          the gate: artifacts, rubrics, bundles, decks, pointers, narration
│   ├── learner-site/          the learner-facing build — one slide at a time, narrated
│   │   └── transcripts/       committed transcripts for all nine decks + ALL.md
│   └── Makefile               narration · transcripts · site · serve · test · check
├── ListenToMe/                ← cloned separately, gitignored (see below)
├── SignUpFlow/
└── ai_qe/
```

The three case-study repos are ignored because they carry their own git history and are upstream
projects, not course content. Clone them into the repository root:

```bash
git clone https://github.com/tomqwu/ListenToMe.git
git clone https://github.com/tomqwu/SignUpFlow.git
git clone https://github.com/tomqwu/ai_qe.git
```

Only the labs and verification need them — the course text, slides, sales material and learner site
work without them.

## What is in the course

- **9 modules · 27 lesson segments · 8 module labs (M0–M7) plus the M8 capstone · 72 quiz questions**
- **11 documents per module**: lesson, lab, quiz, Marp deck with speaker notes on every slide, lab
  solutions with expected output, timed video scripts, printable handout, 90-minute facilitation kit,
  glossary, lab rubrics, accessibility/transcript notes
- **72 banded module artifacts** and **15 bundle artifacts** checked against length bands
- **9 narrated decks · 233 slides · 21,536 words of narration · 132.6 minutes of audio**, with captions,
  transcripts and keyboard navigation
- **3 sellable track bundles** at $199, or the full course at $399 self-paced / $1,490 cohort
- Core labs run on Python 3.11+ with Ollama (`ollama pull qwen3:0.6b`); a Swift stretch track maps
  them onto the real ListenToMe code

## Quick start

```bash
make -C course narration-preview   # record the free local preview voice (~8 min, no API key)
make -C course transcripts         # regenerate the committed transcripts
make -C course serve               # serve the learner site on http://localhost:8043
make -C course test                # 45 unit tests (caption engine + TTS providers)
make -C course check               # the full gate — see below
```

`make` on macOS is itself an Xcode shim and refuses to run until you accept the Xcode licence
(`sudo xcodebuild -license accept`). The gate therefore also runs without it:

```bash
bash course/check.sh               # identical steps, no make required
```

Recording the release voice needs an ElevenLabs key and spends real quota:

```bash
export ELEVENLABS_API_KEY=...
make -C course narration-plan      # what it will cost, per deck, before you spend it
make -C course narration           # record, validate, and swap the preview out
```

Generated artifacts — audio (~62 MB), the rendered HTML and the site manifest — are **not committed**.
They are one command to rebuild, and shipping placeholder audio in version control is worse than not
shipping it.

## The course online

**<https://tomqwu.github.io/ai_courses/>** — published from a `gh-pages` branch, because the repository
cannot serve the generated HTML itself:

```bash
python3 course/publish_site.py                 # publish text-first (36 files, ~1 MB, no audio)
python3 course/publish_site.py --with-audio    # publish with the recordings so narration plays
```

The published copy is **text-first**: the decks, the full design system, every transcript and the print
stylesheet all work, but the player is told there are no recordings, so nothing 404s and no Play button
offers an audio file the copy does not contain. Add the recordings — for example once the release voice
is recorded — with `--with-audio`. Either way the gate runs first and the publish is refused unless it
is green.

The slide layout is an **editorial rail** — a full-height left spine carrying the kicker, running head,
module tag, slide number and transcript link, with the title and content centred against it. It replaced
a footer-based layout that an audit of all 233 slides showed was 45% filled, top-aligned in the corner,
and running on an 11-size type scale with 17 unsystematic spacing values and 48 hex colours. The rail
composes that whitespace instead of filling it, and `check_player.py` now asserts the system's own rules
so it cannot drift back. `course/learner-site/README.md` has the measured before/after.

The live copy is text-first, so it makes no sound and offers no Play button: it is a deck you read,
present, print and search, with the full design and all 233 transcripts. That is a deliberate limit of
the published copy, not a defect of the course — and it is stated on the page itself.

The site is organised as **learning paths**, the hierarchy Microsoft Learn uses — learning path →
module → unit — with each module following the same unit grammar (Introduction → three lesson segments
→ Exercise → Knowledge check → Summary). This course already had every level; it just never surfaced
one. The 233 slides resolve into **63 units**, and `check_player.py` asserts that partition covers every
slide exactly once and agrees with the counts written by hand in `05-tracks/` — while the durations it
shows are measured from the narration manifest rather than estimated. The landing page opens with the
path chooser — *what do you want to build: an app, a web service, or a content product?* — and all three
paths are built end to end. Modules are shared between paths (M0 and M1 open all three; M7 and M8 are
sliced into all three, differently), and each module page says which paths include it and how.
See [`course/learner-site/README.md`](course/learner-site/README.md).

## Verification

`make -C course check` is the single gate, and it runs in order:

```
45 unit tests                      caption engine (32) + TTS providers (13)
validate_narration --scripts-only  9 decks, 233 slides, 21,536 words
validate_narration                 233/233 recordings: exists, duration ±0.2s, sha256,
                                   cues ordered and within limits, and
                                   captions == transcript == approved script word for word
transcripts                        10 documents match the approved scripts
build_site --check                 9 decks built; fails if a committed transcript is stale
check_player --all                 headless browser: the 16:9 frame is measured (ratio,
                                   overflow, font loaded), panel visible, captions
                                   parsed, deep links, Present/Read all/notes all work
verify.py                          artifacts · rubrics · bundles · decks · sales claims ·
                                   narration contract · learner site · 1,048 file pointers
```

`verify.py` is the same evidence discipline the course teaches, applied to the course: every claim
carries a pointer to a file, and every pointer is resolved. Run it on its own with
`python3 course/06-production/verify.py`.

The ElevenLabs release path is verified without a key by driving it through a stubbed transport with a
real encode and a real `ffprobe` — the request we build, the alignment we parse, the proportional
fallback, and the rule that a network failure is never retried (a retry may bill twice). That suite was
mutation-checked; its first version failed that check and was strengthened.

## Honest status

What is **done**: the full course package, the three track bundles, the sales material, all nine decks
narrated and captioned with the free preview voice, and a committed transcript for every module.

What is **not**:

- **The release voice is not recorded.** The course needs 130,870 ElevenLabs characters; the account
  has 89,501 remaining, and the monthly limit (127,856) cannot cover the course even from empty — so it
  takes two cycles, a tier upgrade, or a cheaper model. Until then every recording is labelled
  `sentence-measured-preview` in the provenance, and the site says so on each page and in each
  transcript. Nothing pretends the preview is the finished product. Tracked in
  [#21](https://github.com/tomqwu/ai_courses/issues/21).
- **Testimonials do not exist yet.** The landing page reserves the slots and says so rather than
  inventing them. Run a founding cohort first.
- **No `LICENSE` file.** Decide the terms before publishing or selling; the repository currently
  carries none.
- **The pinned numbers drift.** The case-study repos ship daily; five of the fourteen facts the
  content standard whitelists were already stale within five days of being pinned (ListenToMe is at
  v1.4.4, not a held-back 1.3.0; its competitor table has 14 rows, not 12; SignUpFlow's `AGENTS.md`
  and constitution have grown). `make -C course facts` measures this and names the files to edit;
  the edits themselves are Milestone 5 in
  [`course/06-production/MILESTONES.md`](course/06-production/MILESTONES.md).
- **Three labs cannot be passed as written** (M3 ships pre-solved, M5 has no starter, M1/M2 template
  a red run the tooling does not produce) — found by the September 2026 review and tracked there.
- All facts about the three case-study repos were read from the clones in this workspace and carry file
  pointers — re-verify before publishing, because upstream repos evolve.

## How it was built

1. **Research** ([`course/00-research/`](course/00-research/)) — deep reads of the three repos, plus
   cited market research on how courses and labs get built, priced and sold.
2. **Design** ([`course/01-design/`](course/01-design/)) — positioning, syllabus, and a binding content
   standard that fixes the artifact set, length bands, and the verified-numbers whitelist.
3. **Content and sales** — nine modules written to that standard, three bundles sequenced from them,
   and the course's own go-to-market.
4. **Production** ([`course/06-production/`](course/06-production/)) — narrated audio, captions,
   transcripts, and a static learner site. The narration pipeline is a port of the pattern in
   [`ai_qe`](https://github.com/tomqwu/ai_qe); what was borrowed, changed and rejected is written down
   in [`narration/DESIGN.md`](course/06-production/narration/DESIGN.md).
5. **Verification** — the gate above. It found and fixed five real errors in already-shipped content,
   and the narration work found three more; each is recorded in
   [`course/README.md`](course/README.md) and
   [`narration/DESIGN.md`](course/06-production/narration/DESIGN.md) rather than quietly patched.

Work is tracked publicly in GitHub issues across four milestones: course core (9), track bundles (3),
production and launch readiness (4, all closed), and the narrated learner site (4 of 5 closed). The
roadmap mirrors them in [`course/06-production/MILESTONES.md`](course/06-production/MILESTONES.md).
