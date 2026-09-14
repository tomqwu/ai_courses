# Narrated Learner Site — design

> How the course becomes something a learner can **watch and listen to**, not just read.
> Ported from the `ai_qe` publication pipeline (studied at `ai_qe/tools/`, `ai_qe/assets/js/`,
> `ai_qe/assets/data/narration-guides.json`, `narration-flows.json` and `narration-provenance.json`). Read this before changing anything under `narration/`.

## 1. The pattern, as it exists in `ai_qe`

`ai_qe` publishes four narrated slide decks (116 slides) as a Jekyll site. The chain is:

```
author script  →  validate scripts  →  TTS (ElevenLabs)  →  alignment  →  captions (.vtt)
      →  import into assets/audio/<edition>/<deck>/  →  manifest (narration.json)
      →  validate (coverage, duration, sha256, captions≡transcript≡script)  →  build + review gate
```

The parts worth copying, and why:

| Mechanism | Where it lives in `ai_qe` | Why it matters |
|---|---|---|
| **Three-artifact separation**: `narration-scripts.json` (approved words) · `narration.json` (recorded media) · `narration-provenance.json` (who/what/when/evidence) | `ai_qe/assets/data/` | The script is the source of truth; the recording is a *derived* asset that can be regenerated without re-authoring. The provenance file is separate because it answers a different question ("may I claim this is a real voice/production?") than the manifest ("which file plays on slide 7?"). |
| **`text` vs `speakText`** | `narration-scripts.json` | What the learner reads must be correct technical prose; what the voice says may need respelling ("PostgreSQL" → "Postgres"). `ai_qe` keeps both as fields per slide. **We keep the separation but not the field**: respellings live in one `pronunciations.json` table, applied automatically, so there is a single mechanism and the mapping back to display tokens stays deterministic. |
| **Captions are generated from the same alignment as the audio**, then checked word-for-word against the approved script | `tools/captions_from_alignment.py`, `tools/validate_narration.py:53-54` | This is what makes captions trustworthy: they cannot drift from either the audio or the script, and a mismatch fails the build. |
| **Integrity is checked, not asserted**: per-file `sha256` + `ffprobe` duration ±0.2 s re-verified on every run | `tools/validate_narration.py:48-51` | Catches a swapped or re-encoded file that would otherwise silently desync captions. |
| **Player built at runtime and injected before a known anchor**, with `--narration-height` reserved via `ResizeObserver` | `assets/js/narration.js:31-62` | The deck's own HTML stays clean and printable; the player never reflows the slide mid-playback. |
| **`audio.currentTime` is the single clock** for captions and any synchronized visual | `narration.js:71-76, 85-87` | No parallel timers to drift. |
| **Audio focus has exactly one owner per frame tree**, with a broadcasting fallback | `assets/js/narration-media.js:39-83` | Two tabs (or an embedded iframe) can never talk over each other. |
| **Never autoplay on load**; auto-advance is opt-out and validates `source` + `expectedSlide` before acting | `narration.js:192`, `decks.js:114` | Autoplay is hostile; a stale advance must not move a deck the user has since navigated. |
| **A wall-clock pause between slides** (~2 s) that survives playback-rate changes and is cancelled by any invalidation | `narration.js:104-125` | Gives the learner a beat to read before the next slide, and never fights the user. |
| **Graceful degradation**: caption fetch failure offers *Retry captions* and the transcript; print and no-JS keep the deck readable | `narration.js:149`, `narration.css:66` | A media failure degrades the lesson instead of breaking it. |

## 2. What we port, change, and reject

**Ported as-is (same mechanism, our own smaller code):** the three-artifact separation, the
read-versus-speak separation, alignment-derived captions, the validate-everything contract, the
runtime-injected player with reserved height, `currentTime` as the only clock, single-owner audio
focus, never-autoplay, the wall-clock inter-slide pause, caption failure → retry + transcript,
print/no-JS degradation.

**Changed, deliberately:**

| Change | Reason |
|---|---|
| **Pure-Python site generator** (`build_site.py`) instead of Jekyll | The course repo has no runtime dependency and no build step today; `verify.py` is plain Python. Adding Ruby+bundler to read a course would be a step backwards, and the generator is ~300 lines because our slide subset is small. |
| **Manifest lives next to the audio it describes** (`narration/manifest.json`), and the site build copies both | `ai_qe` splits data (`assets/data/`) from media (`assets/audio/`) across two Jekyll roots; one directory keeps the pairing obvious and lets `validate_narration.py` run without a build. |
| **Two TTS providers behind one interface** — `elevenlabs` (final voice) and `say` (local preview) | The final voice needs a paid API key. The preview provider makes the whole pipeline testable and the site *listenable* today, with no key and no cost. Provenance records which one produced each file, so a preview can never be mistaken for the release voice. |
| **Approximate captions are labelled as approximate** | ElevenLabs gives character-level alignment, so cue times are exact. The preview provider gives only a duration, so cue times are distributed proportionally. The manifest records `caption_method` per slide, and the validator refuses to let a proportional file claim to be aligned. |
| **Total deck duration, resume position, and a `prefers-reduced-motion` branch for auto-advance** | `ai_qe` has none of these (`narration.js` never reads the deck-level `duration`; there is no progress memory; the 2 s pause ignores reduced-motion). Small additions, real learner wins. |
| **Audience routes become *paths*** — `full` (all slides) and `core` (the non-optional spine) | Our decks have no evp/technical split, but the `sequence()` indirection from `decks.js:16-21` is worth keeping: it is what lets prev/next, keyboard, the picker, and auto-advance all follow one subset definition. |
| **Respellings live in one table, not per-slide** | A per-slide `speak` field means two places can disagree about how a word is spoken, and the restoration mapping stops being checkable. One table with a word-count rule (a phrase key must preserve its word count) keeps every spoken token mapped to exactly one display token. |
| **One sentence rule, shared by the provider and the captioner** | Learned the hard way: `split_sentences` and the caption grouper were written separately, and an abbreviation guard that matched `ms.` *inside* `seams.` made the provider measure 5 sentences for 6 groups. The tail of every affected slide then received timings from the wrong part of the clip. Both now call `captions.sentence_groups`, and a count mismatch raises instead of silently degrading. |
| **Caption timing is asserted monotonic** | Every generated file passes a check that cue times only move forward and every cue has positive duration, so a future timing regression fails the build rather than shipping scrambled captions. |

**Rejected:**

- **ElevenLabs as a hard requirement.** `ai_qe`'s generator refuses to run below a paid tier
  (`generate_elevenlabs_narration.py:61-63`). We keep the paid path as the *default for release* but never
  make the course unbuildable without it.
- **A Playwright browser suite as the only proof the player works.** We adopt the *assertions* worth having
  (never autoplay, caption text exact, the pause is ≥1.8 s even at 1.25×, mobile overflow ≤1 px) as small
  headless checks where cheap, but we do not gate the course on a browser install.
- **Two generators at once.** Not a feature to port, but a way to lose work: the manifest is
  read-modify-written after every slide, so a second run interleaves those writes. `generate_narration.py`
  now takes an exclusive lock and refuses to start.
- **`speakText` letter-spacing tricks.** `ai_qe` forbids "A I"/"Q E" in `speakText` and respells instead
  (`test_generate_elevenlabs_narration.py:30-31`); we adopt the rule, not the specific words.

## 3. Layout

```
course/06-production/narration/          ← the pipeline (source of truth)
  DESIGN.md                              ← this file
  scripts/mNN.json                       ← approved narration words per deck (authored)
  manifest.json                          ← recordings: audio, captions, transcript, duration, sha256
  provenance.json                        ← provider, basis, receipt, evidence per recording
  pronunciations.json                    ← spoken → display restoration table (the only respelling mechanism)
  captions.py                            ← VTT/SRT write + strict parse + word-equality rule
  providers.py                           ← elevenlabs | say, one interface
  generate_narration.py                  ← CLI: plan | generate | verify
  import_narration.py                    ← bring in an externally recorded take
  validate_narration.py                  ← the contract; --require-complete gates release
  test_captions.py                       ← 30 tests, incl. the sentence-rule regression
  README.md                              ← operator's guide

course/learner-site/assets/audio/<edition>/<deck>/slide-N.{mp3,vtt}   ← generated, gitignored

course/learner-site/                     ← the learner experience
  build_site.py                          ← slides.md + manifest → static site
  check_player.py                        ← headless browser check (no npm install)
  assets/player.js · narration-media.js · player.css
  index.html (generated, gitignored) · mNN.html (generated, gitignored)
```

## 4. Honesty rules for this pipeline

1. **A recording never claims to be something it is not.** `provenance.json` records `provider`,
   `basis` (`aligned-generation` | `proportional-generation` | `sentence-measured-preview` | `external-recording`), and either a
   receipt or an explicit note that none exists — mirroring `ai_qe`'s own admission that 105 of its 114
   entries carry a production record rather than a per-file receipt.
2. **Preview audio is labelled in the UI**, not just in the data. A deck playing preview narration says so
   on the player (`data-voice="preview"` renders a visible badge), because a learner should never be told
   that a synthetic placeholder is the finished product.
3. **Narration adds no facts.** Every spoken sentence is derived from that slide's own content and speaker
   notes. If a slide is thin, the narration is short rather than embellished — the validator enforces a
   minimum, not a target.
4. **No number, quote, or claim appears in narration that is not in the course already.** The narration
   inherits the course's pointer discipline by construction: it is written from the same slides that were
   pointer-verified.
