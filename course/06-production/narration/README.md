# Narration pipeline

Turns the nine module decks into narrated, captioned audio that a learner can watch and listen to.
Design rationale — and what was learned from `ai_qe` — is in [DESIGN.md](DESIGN.md). This file is
the operator's guide.

## Quick start

```bash
cd course

make narration-plan      # what would be generated, and the character count a paid voice bills on
make narration-preview   # free, offline, sentence-accurate preview voice (needs macOS `say` + ffmpeg)
make site                # build the learner site
make check               # validate scripts, media, decks, and the site build
```

`make narration` (the release voice) needs `ELEVENLABS_API_KEY` in the environment and a paid tier.
It fails loudly when the key is absent rather than silently producing a preview.

## The three files, and why they are separate

| File | Question it answers | Authored or derived? |
|---|---|---|
| `scripts/mNN.json` | What are the approved words? | **Authored.** The source of truth. |
| `manifest.json` | Which file plays on slide 7, how long is it, what does it hash to? | Derived — regenerate any time. |
| `provenance.json` | Who produced it, on what basis, and is there a receipt? | Written alongside the audio. |

Keeping them apart means the words can be edited and re-recorded without touching playback data, and
playback data can be rebuilt without re-authoring a single sentence.

### Script schema

```json
{
  "label": "M0 — Orientation: Three Products, One Method",
  "slides": {
    "slide-1": { "title": "Welcome to AI Product Studio", "text": "Spoken narration…" }
  }
}
```

* `text` is what the narrator reads **and** what the captions and transcript must match word for word.
* Respellings for the voice live in **`pronunciations.json`**, applied automatically — there is no
  per-slide override field, so there is exactly one mechanism and validation stays deterministic.
* A substitution may expand a single token (`Testcontainers` → `Test containers`) but a multi-word key
  must keep its word count, so every spoken token maps back to exactly one display token.

### Manifest schema

```json
{
  "edition": "aps-1.0.0",
  "complete": true,
  "voice": "ElevenLabs / Chris — Charming, Down-to-Earth",
  "decks": {
    "m00": {
      "label": "M0 — …",
      "duration": 512.4,
      "slides": {
        "slide-1": {
          "audio": "/assets/audio/aps-1.0.0/m00/slide-1.mp3",
          "captions": "/assets/audio/aps-1.0.0/m00/slide-1.vtt",
          "transcript": "Spoken narration…",
          "title": "Welcome to AI Product Studio",
          "duration": 24.45,
          "sha256": "…",
          "voice": "ElevenLabs / Chris — Charming, Down-to-Earth",
          "provider": "ElevenLabs",
          "caption_method": "character-alignment"
        }
      }
    }
  }
}
```

## Commands

```bash
# plan (no writes, no cost)
python3 generate_narration.py plan
python3 generate_narration.py plan --deck m04

# preview voice — free, offline
python3 generate_narration.py generate --provider say
python3 generate_narration.py generate --provider say --deck m00 --slide slide-3 --force

# release voice — needs ELEVENLABS_API_KEY
python3 generate_narration.py generate --provider elevenlabs --deck m00

# the contract
python3 validate_narration.py --scripts-only
python3 validate_narration.py --require-complete
python3 validate_narration.py --no-media          # skip hashing/probing (fast)
```

Generation is **idempotent and crash-safe**: it skips slides that already exist, re-derives their hash
and duration, and saves the manifest after every single slide. A run that dies on slide 140 has still
banked 139 recordings, and re-running only fills the gaps. A lock file (`.generate.lock`) refuses two
concurrent runs, because both would read-modify-write the manifest and lose work.

## Tests

```bash
make -C course test        # or: cd course/06-production/narration && python3 test_captions.py
```

* `test_captions.py` (32) — the word-equality invariant, pronunciation span mapping, the shared
  sentence rule, cue monotonicity and cue width.
* `test_providers.py` (13) — the ElevenLabs release path driven through a **stubbed transport** with a
  real encode and a real `ffprobe`, asserting the request we build, the alignment we parse, the
  proportional fallback when alignment does not line up, and that a network failure is never retried.

The release voice cannot be exercised without a paid key, and a release path that is never run is how
one rots. What is faked is the socket; what is verified is our code. Nothing here proves the *voice* is
good — only a real key does that (issue #21).

## What the contract enforces

`validate_narration.py` fails (never warns) on any of these:

| Check | Why |
|---|---|
| Every deck has a script; slide keys are exactly the deck's real slides | A missing slide makes the deck go quiet halfway through |
| Title and text non-empty; 25–190 words | Catches a stub, and catches a "narration" that is really an essay |
| No `Timing:` / `Transition:` / `<!--` in spoken text | Presenter directives must not be read aloud |
| Audio and captions live under `/assets/audio/` and exist | Catches a manifest pointing at a deleted or misplaced file |
| Duration `0 < d < 600` and within 0.2 s of ffprobe | Catches a truncated or swapped file |
| sha256 matches the manifest | Catches a re-encode that would desync captions from audio |
| **Cue words == transcript words == approved script words** | The invariant that makes captions trustworthy |
| Cue text ≤ 2 lines of 42 chars; cues chronological | Readability and no negative-duration cues |
| Voice + caption_method present on every recording | A recording must say how it was produced |
| Every recording has a provenance entry with a known basis | Prevents an unattributed file shipping |
| A preview recording may not claim aligned captions | Prevents a placeholder being described as the release voice |

## Swapping the voice

1. Set `voice_id` (and optionally `model_id` / `voice_settings`) in `voice.json`.
   The default is the same public voice the `ai_qe` decks use, so both products sound like one publisher.
2. `export ELEVENLABS_API_KEY=…`
3. `make narration` — existing preview files are **not** overwritten unless you pass `--force`.
   To replace previews with the release voice, re-record that deck explicitly:

   ```bash
   python3 generate_narration.py generate --provider elevenlabs --deck m00 --force
   ```

4. `make site && make check`.

`provenance.json` records `basis` per recording, so a mixed run (some preview, some release) is
visible rather than hidden. The player shows a visible "preview narration" badge whenever a deck's
recordings are all preview.

## Adding a new deck

1. Author `scripts/mNN.json` from that module's `slides.md` (one entry per slide, keyed `slide-1`…).
   Use the module's speaker notes as the source; remove presenter directives; invent no facts.
2. Add the deck id to `DECK_IDS` in `narration_data.py`.
3. `python3 validate_narration.py --scripts-only` → then generate → `make site`.

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `provider unavailable: ELEVENLABS_API_KEY is not set` | Use `--provider say`, or export the key. The key is read from the environment only and never written to disk. |
| `another generation run is already in progress` | A previous run is still going, or a stale `.generate.lock` exists. Check with `pgrep -fl generate_narration`, then delete the lock. |
| `network failure calling ElevenLabs … may have been charged` | Do **not** blind-retry: a second call could bill twice for the same sentence. Check provider history first. |
| `captions differ from the approved script` | The script was edited after recording. Re-record that slide (`--force`), or revert the script. |
| `duration drift … vs … recorded` | The file was replaced or re-encoded. Re-record the slide. |
| `cc stayed disabled` (browser check) | The `.vtt` is missing or not valid WebVTT. Run `validate_narration.py` without `--no-media`. |
| Preview sounds robotic | It is `say`, not the release voice. That is the point of the label: set the key and run `make narration`. |

## What is committed, and what is generated

**Committed:** the scripts, the manifest, the provenance, the pronunciation and voice config, the
pipeline and its tests, the site builder, and the player assets.

**Generated (gitignored):** the audio and captions under `learner-site/assets/audio/`, the deck HTML,
and `learner-site/narration.json`. Audio is ~90 minutes of speech; at the preview encode (mono 64k)
that is about 20 MB, and at the release encode roughly three times that. Regenerating is one command,
and shipping placeholder audio in version control would be worse than generating it.
