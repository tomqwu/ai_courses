# AI Product Studio — agent guide

A sellable course that teaches engineers to ship AI products, built on three real repositories
(ListenToMe, SignUpFlow, ai_qe) as case studies. Everything a learner sees is generated from
Markdown and JSON in `course/`, checked by one gate, and published as a static site.

**Adding or changing course content? Use the `course-content` skill**
(`.claude/skills/course-content/SKILL.md`). It is the end-to-end procedure for new modules,
segments, learning paths, playbooks, narration edits, and publishing.

## Map

| Path | What it is |
|---|---|
| `course/01-design/content-standards.md` | The content standard: artifacts, word bands, deck rules, exhibits, slide fit |
| `course/03-content/mNN-slug/` | One module: lesson, slides (the parts of its Learn page), lab, quiz, and the 8 banded artifacts |
| `course/06-production/narration/scripts/mNN.json` | The approved spoken narration, per slide (source of truth for audio and captions) |
| `course/06-production/verify.py` | Package gate: artifacts, bands, pointers, anchors, exhibits, narration, site |
| `course/06-production/pointer-anchors.json` | Line ranges pinned to the text they must contain |
| `course/06-production/facts.json` | Case-study numbers the course quotes, re-derived by `check_facts.py` |
| `course/03-content/mNN-slug/zh/`, `narration/scripts-zh/` | The Chinese edition's sources (built into `zh/`); rules in `course/01-design/zh-translation-guide.md` |
| `course/03-content/_basics/basics.json` | The Basics glossary: everyday software words in plain language (EN + 中文); their first use in each part links to a card |
| `course/learner-site/site-flags.json` | Site feature flags. `pricing` is **off**: the site's own pages show no prices until it is turned on |
| `course/06-production/terms-zh.json` | Every glossary term's Chinese name and one-line definition — the names the translation uses |
| `course/learner-site/` | Site generator (`build_site.py`; every page in the `site_shell.py` frame) and browser checks (`check_player.py`, `check_features.py`) |
| `course/05-tracks/`, `course/07-playbooks/` | Paid learning-path bundles; standalone playbooks |
| `course/check.sh`, `.github/workflows/gate.yml` | The gate, locally and in CI |
| `ListenToMe/`, `SignUpFlow/`, `ai_qe/` | Case-study clones at pinned commits (git-ignored, read-only) |

Clone the case studies beside `course/` at the commits `gate.yml` pins before running the gate:
`ListenToMe a9bde8e`, `SignUpFlow c550d46`, `ai_qe 6388f0a`.

## Rules that the gate enforces (do not work around them)

- **Every claim about a case study cites a pointer** (`Repo/path:N-M`) that resolves at the pinned
  commit. When a lesson leans on a range, anchor it in `pointer-anchors.json`, keyed exactly as written.
- **A slide exhibit (fenced block) is a true copy of a file the slide cites**, within the cited range.
  Rewrapping and `…` elisions are allowed. Anything else declares itself in the info string:
  ` ```bash commands `, ` ```text output `, ` ```markdown template `, ` ```text illustrative `.
- **There are no slides on the site; every page is a full page** (#112). Each `---` section of
  `slides.md` is a *part* of the module's Learn page (`mNN.html`, anchor `#slide-N`), shown at full
  width with its narration as text. Nothing on a page may be clipped (`check_player.py --strict-fit`,
  measured at 1600x1000 and 1280x800). Do not shrink type or cut substance to fit anything. Do not
  split or renumber parts (numbers key the narration, audio and deep links).
- **Narration never speaks a line number.** The words in `scripts/mNN.json` are what is recorded and
  captioned. If you change them, keep the slide's `NOTES` and the `video-scripts.md` narration
  consistent, regenerate transcripts (`make -C course transcripts`), and add the slide to the
  re-recording list in the PR.
- **Never skip, disable or loosen a check to get green.** Fix the content or the check's real bug.
- **Explain every technical word.** The course is read by people who have never programmed. A word a
  newcomer could stumble on (repository, API, token…) belongs in `03-content/_basics/basics.json`
  (plain meaning, an everyday comparison, both languages); its first use in each part then links to
  a card automatically. Add it to that file's `watch` list so the gate keeps it explained.
- **The Chinese edition moves with the English.** Change a module's English and carry the change into
  its `zh/` sources (and `scripts-zh/`), then `python3 course/06-production/zh_edition.py stamp mNN`.
  The gate fails a module whose English changed since its Chinese was stamped, whose Chinese does not
  match part for part (same parts, exhibits, pointers, steps, questions, keys), or whose built pages
  leave English untranslated. Every glossary term also needs its entry in `terms-zh.json`.
- **Numbers that drift** (test counts, coverage, file sizes) live in `facts.json`; update the pin when
  the source changes, never the literal alone.

## Verify before you push

```bash
python3 course/06-production/verify.py            # package gate (fast)
python3 course/learner-site/build_site.py --check  # committed transcripts match the scripts
bash course/check.sh                               # the full gate, as CI runs it
```

The full gate needs preview audio. CI records it with `espeak-ng`; locally:

```bash
python3 course/06-production/narration/generate_narration.py generate --provider espeak
make -C course transcripts && bash course/check.sh
```

**Generated files are never committed.** After a local audio run, restore them before committing:

```bash
git checkout course/06-production/narration/manifest.json course/06-production/narration/provenance.json
rm -rf course/learner-site/assets/audio/aps-1.0.0
make -C course transcripts && python3 course/learner-site/build_site.py --check
```

## Workflow: every change ends merged to `main`

This is the standing process for **every** change in this repository — content, code, CI, docs and
these instructions alike. The owner has authorised it. A change is not done until it is on `main`:
committed, pushed, merged. Nothing is left uncommitted, unpushed or sitting in an open PR at the end of
a piece of work.

1. Work on a branch, never directly on `main`. After a merge, restart the branch from the new `main`.
2. Run the checks above. Fix everything they report.
3. Commit with a message that says what changed and why. Push the branch.
4. Open a pull request, or update the one already open for the branch. Reference the issues it
   closes, and list any slides whose narration needs re-recording.
5. Wait for the `gate` workflow on the PR's head commit: both jobs, `package gate (check.sh)` and
   `lab suites (TinyCopilot, mini-flow)`. Watch the PR's events; do not poll in a loop.
6. **When CI is green and the PR has no conflicts and no unresolved review threads, mark it ready
   and merge it** with a merge commit, so commit SHAs cited in issues stay valid on `main`.
7. If CI is red, fix the cause and push again. Never merge on red, never force-push `main`, and
   never bypass a required check.
8. After merging, close the issues the PR finished, each with the evidence (commands and output).
9. **The site deploys itself.** The push to `main` re-runs the gate, and its `deploy` job builds the
   learner site from that commit and publishes it to <https://tomqwu.github.io/ai_courses/> (Pages
   serves the `gh-pages` branch, which only ever holds build output — never edit it by hand; the
   `deploy` job fails if Pages is set to serve anything else, #88). Check
   the `deploy` job went green on `main`; if it failed, fixing it is part of the same change. Publish
   by hand (`make -C course publish-audio`) only to ship the recordings.
