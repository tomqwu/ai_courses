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
| `course/03-content/mNN-slug/` | One module: lesson, slides (Marp), lab, quiz, and the 8 banded artifacts |
| `course/06-production/narration/scripts/mNN.json` | The approved spoken narration, per slide (source of truth for audio and captions) |
| `course/06-production/verify.py` | Package gate: artifacts, bands, pointers, anchors, exhibits, narration, site |
| `course/06-production/pointer-anchors.json` | Line ranges pinned to the text they must contain |
| `course/06-production/facts.json` | Case-study numbers the course quotes, re-derived by `check_facts.py` |
| `course/learner-site/` | Site generator (`build_site.py`) and browser checks (`check_player.py`, `check_features.py`) |
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
- **Every slide fits its 16:9 frame with the narration panel present** (`check_player.py --strict-fit`).
  Trim; do not split slides or change type sizes.
- **Narration never speaks a line number.** The words in `scripts/mNN.json` are what is recorded and
  captioned. If you change them, keep the slide's `NOTES` and the `video-scripts.md` narration
  consistent, regenerate transcripts (`make -C course transcripts`), and add the slide to the
  re-recording list in the PR.
- **Never skip, disable or loosen a check to get green.** Fix the content or the check's real bug.
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

## Workflow: commit, push, merge when CI passes

This is the standing process for every change in this repository. The owner has authorised it.

1. Work on a branch, never directly on `main`.
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
   Publish the site when learner-facing content changed (see the skill, step "Publish").
