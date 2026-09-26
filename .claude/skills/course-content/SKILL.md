---
name: course-content
description: End-to-end procedure for adding or changing course content in this repository and publishing it — a new module, a new segment or lesson, a new learning path or paid track, a standalone playbook, slide/lab/quiz/narration edits, re-recording narration, or publishing the learner site. Use whenever there is a new course idea, new content, or a new path to ship, before touching course/.
---

# Course content: from idea to published

The course is Markdown and JSON in `course/`; a generator builds the learner site; one gate
(`course/check.sh`, CI `gate.yml`) proves it; `course/publish_site.py` publishes it to the
`gh-pages` branch. Read `AGENTS.md` for the rules and the commit → PR → merge-on-green workflow.
The standard every artifact is held to is `course/01-design/content-standards.md` — read §0–§2
before writing.

## 1. Decide the shape

| The idea is… | Make | Where |
|---|---|---|
| A new topic a learner needs, 30–60 min, with its own lab | a **module** | `course/03-content/mNN-slug/` (section 2) |
| A missing step inside an existing module | a **segment** edit | that module's lesson, slides, video script, quiz (section 3) |
| A new way through existing modules for an audience | a **learning path** | `site_paths.TRACKS`; if sold, a bundle in `course/05-tracks/` (section 4) |
| One method that works without the course | a **playbook** | `course/07-playbooks/<slug>/` (section 5) |
| A fact changed in a case-study repo | a **drift fix** | every artifact that states it, plus `facts.json` / anchors (section 3) |

Ground every claim in a case study at its pinned commit (`ListenToMe a9bde8e`, `SignUpFlow c550d46`,
`ai_qe 6388f0a`, cloned beside `course/`). Read the source; never write a pointer from memory.

## 2. A new module

Copy the structure of the newest module (`m09-github-pages`) — it is the reference for every file.

**Files** (`course/03-content/mNN-slug/`):

| File | Contract |
|---|---|
| `lesson.md` | 3 teaching segments headed `## MN.1 — …`, `## MN.2 — …`, `## MN.3 — …` (the unit model expects exactly 3) |
| `slides.md` | Marp front matter (`marp: true`, `theme: aps`, `paginate: true`, `title: MN — …`); 18–28 slides; ≤ 6 bullets of ≤ 10 words; a `<!-- NOTES: … -->` on every slide; sequence: title (`<!-- _class: lead -->`), "By the end you can…", segment slides, ≥ 1 proof slide per segment (`<!-- _class: proof -->`, pointer on the slide), lab, quiz, recap, discussion |
| `lab.md` | `## Step N — title (~time)` steps; `## Acceptance checklist (binary …)` with `- [ ]` boxes (the site persists them); evidence to record |
| `quiz.md` | `**Q1 (MC).**` with `- a)`…`- d)` options; `## Answer key`; `## Objective → assessment map` |
| `lab-rubrics.md` | 4 levels; an `## Auto-fail` section (the lab page shows it beside the checklist) — 600–1,100 words |
| `solutions.md` 800–1,600 · `video-scripts.md` 1,200–2,100 · `handout.md` 400–650 · `facilitation.md` 800–1,250 · `glossary.md` 500–900 (10–18 terms as `**Term** — definition`) · `accessibility.md` 400–900 | word bands are checked |

**Narration** — `course/06-production/narration/scripts/mNN.json`:
`{"label": "MN — Title", "slides": {"slide-1": {"title": "…", "text": "…"}, …}}`, one entry per
slide in deck order, 25–190 words each, written to be spoken: no line numbers, no symbols read
aloud awkwardly (add pronunciations to `narration/pronunciations.json`, e.g. `"gh": "G H"`).
Keep each slide's NOTES and its `video-scripts.md` rows consistent with the spoken text.

**Register the module** (every one of these, or the gate or the site misses it):

1. `course/06-production/narration/narration_data.py` — add `"mNN"` to `DECK_IDS`.
2. `course/06-production/verify.py` — add the folder to `MODULES`.
3. `course/06-production/build-glossary.py` — add the folder to its module list, then run it
   (`python3 course/06-production/build-glossary.py`) to regenerate `glossary-master.md`.
4. `course/learner-site/site_paths.py` — put the module in at least one `TRACKS` entry (a new free
   path, like M9's, or a paid bundle); update the docstring's module and unit counts.
5. `course/learner-site/check_player.py` `check_units()` — raise the literal unit total by 7
   (intro + 3 segments + lab + quiz + summary). It is a literal on purpose.
6. `course/README.md` package map; and any sales or landing copy that counts modules. Decide
   whether the module is inside the paid certificate before touching "nine modules" claims.
7. If the lab ships code (a starter, scripts, a test suite), add its suite to the `labs` job in
   `.github/workflows/gate.yml`.

## 3. Editing existing content

- **Change a fact** everywhere it appears: `grep -rn` the value and the pointer across the module
  (lesson, slides, NOTES, video script, handout, glossary, quiz, solutions, rubrics) and across
  `course/`. If the number is pinned in `facts.json`, update the pin; if a range is anchored in
  `pointer-anchors.json`, update the key and its token together.
- **Change spoken words** only in all three places: `scripts/mNN.json` (what is recorded), the
  slide's NOTES, and the `video-scripts.md` narration. Then `make -C course transcripts`, and list
  the slide for re-recording in the PR.
- **Trim to fit**, never split or renumber: slide numbers key the narration, audio, units and deep
  links. Cut bullets the exhibit or narration already carries; trim exhibits to the narrated lines
  with `…` and correct the cited range.
- **Exhibits** are copies of the cited file within the cited range, or declare
  `commands` / `output` / `template` / `illustrative` after the fence language. An illustrative
  example is also labelled so in the visible slide text.

## 4. A learning path or paid track

- Free or site-only path: add an entry to `TRACKS` in `course/learner-site/site_paths.py`
  (`slug`, `title`, `medium`, `core` modules taught in full, optional `slice` of named segments,
  `status: "built"`, `page`). Measured counts in the entry are asserted by `check_player.py`.
- Paid bundle: `course/05-tracks/<slug>/` with the five files in `verify.py` `BUNDLE_FILES`
  (`README.md`, `syllabus.md`, `sales-page.md`, `pricing.md`, `bundle-map.md`), and add the slug to
  `BUNDLES`. Prices are proposals until the owner sets them; say so.

## 5. A standalone playbook

`course/07-playbooks/<slug>/playbook.md` (1,500–3,000 words) with the sections in order — The
method, Template, Checklist, Worked example, Self-check, Limits, Sources — and `sales.md`
(400–750 words, price labelled a proposal). It must stand alone: no "Lab M3", "M3.1" or
"as we saw". Add a row to `course/07-playbooks/README.md`.

## 6. Build and check (fast loop)

```bash
python3 course/06-production/slides/deck_lint.py course/03-content/*/slides.md
python3 course/06-production/narration/validate_narration.py --scripts-only
python3 course/learner-site/build_site.py            # site + transcripts + search
python3 course/06-production/verify.py               # everything except audio passes locally
make -C course serve                                 # look at it: http://localhost:8043
```

Slide fit, with the narration panel present (needs preview audio, section 7):
`python3 course/learner-site/check_player.py --all --strict-fit`. When measuring a single slide in
your own script, open each slide in a fresh browser context — the player resumes from
localStorage, which overrides the deep link.

## 7. Full gate, exactly as CI runs it

```bash
python3 course/learner-site/build_site.py --check      # committed transcripts match the scripts
python3 course/06-production/narration/generate_narration.py generate --provider espeak
make -C course transcripts
bash course/check.sh                                   # must end: GATE PASSED
```

Then restore the generated files before committing (AGENTS.md, "Generated files are never
committed"). Commit the sources plus the regenerated `transcripts/`, `proof.json`, `search.json`
and `glossary-master.md`.

## 8. Ship

Follow AGENTS.md "Workflow": branch → commit → push → PR (issues it closes, re-recording list) →
merge with a merge commit once the `gate` workflow is green on the head commit → close issues with
evidence.

## 9. Publish

After the merge, from `main`:

```bash
make -C course publish          # runs the gate, then pushes the built site to gh-pages (text-first)
make -C course publish-audio    # same, with recordings and captions, once the release voice exists
```

Release voice: `make -C course narration` (needs `ELEVENLABS_API_KEY`). A human take:
`python3 course/06-production/narration/import_narration.py --deck mNN --slide slide-N --audio …`
— its captions must match the approved script word for word.

## Pitfalls this repo has already hit

- A bare pointer like `checklists/requirements.md` matches many files and is not checked; write
  `SignUpFlow/specs/<feature>/checklists/requirements.md:38-44`.
- Anchor keys are the pointer exactly as written; changing a range orphans its anchor (the gate
  reports the stale key).
- The type scale is fixed (title ≥ 2.5× body, ≤ 8 sizes per slide); fit problems are content
  problems.
- Preview audio runs rewrite `manifest.json` and `provenance.json`; committing them breaks CI.
- `course/learner-site/*.html` is build output and is not committed; the site on Pages comes only
  from `publish_site.py`.
