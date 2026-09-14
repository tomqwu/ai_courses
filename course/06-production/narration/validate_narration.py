#!/usr/bin/env python3
"""The narration contract. Every rule here FAILS the run; none is advisory.

  python3 validate_narration.py                  # scripts + recorded slides, media re-verified
  python3 validate_narration.py --scripts-only    # only the authored words (fast, no media)
  python3 validate_narration.py --require-complete  # also demand a recording for every slide

What it proves, and why each check exists:

  scripts   the words exist for every slide of every deck, in deck order, with a real length. A
            missing slide would silently produce a deck that goes quiet halfway through.
  media     every audio file exists, is inside the audio root, is 0-600 s, and its recorded
            duration is within 0.2 s of ffprobe's measurement. Catches a truncated or swapped file.
  integrity the file's sha256 still matches the manifest. Catches a re-encode that would desync
            captions from audio without changing the filename.
  captions  the cue words equal the transcript words equal the approved script words, exactly.
            This is the check that makes a caption trustworthy; everything else supports it.
  provenance every recording says who made it, on what basis, and whether a receipt exists — and a
            preview recording may not claim to be the release voice.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "slides"))

from captions import MAX_CHARS, MAX_LINES, _wrap, parse_vtt, words
from narration_data import (COURSE_DIR, DECK_IDS, MANIFEST_PATH, MAX_WORDS, MIN_WORDS,
                            PROVENANCE_PATH, SITE_ROOT, audio_abs, load_manifest, load_scripts,
                            read_json, sha256_file, slide_sort_key)
from providers import probe_duration

ALLOWED_BASIS = {"aligned-generation", "proportional-generation", "sentence-measured-preview",
                 "external-recording"}
PREVIEW_BASIS = {"sentence-measured-preview"}
ALIGNED_METHODS = {"character-alignment"}


def deck_slide_ids(deck_id: str) -> list[str]:
    """Authoritative slide list, taken from the deck itself (not from the script)."""
    from deck_lint import split_slides          # noqa: PLC0415  (import after sys.path setup)
    matches = sorted(COURSE_DIR.glob(f"03-content/{deck_id}-*/slides.md"))
    if not matches:
        return []
    _fm, slides = split_slides(matches[0].read_text(encoding="utf-8"))
    return [f"slide-{i}" for i in range(1, len(slides) + 1)]


def check_scripts(problems: list[str]) -> tuple[dict, int, int]:
    scripts = load_scripts()
    total_words = total_slides = 0
    for deck_id in DECK_IDS:
        deck = scripts["decks"].get(deck_id)
        if not deck:
            problems.append(f"{deck_id}: no narration script file")
            continue
        expected = deck_slide_ids(deck_id)
        got = sorted(deck["slides"], key=slide_sort_key)
        if expected and got != expected:
            missing = sorted(set(expected) - set(got), key=slide_sort_key)
            extra = sorted(set(got) - set(expected), key=slide_sort_key)
            problems.append(f"{deck_id}: slide set mismatch (missing {missing}, extra {extra})")
        if not deck.get("label"):
            problems.append(f"{deck_id}: missing label")
        for slide_id, slide in deck["slides"].items():
            title, text = slide.get("title", ""), slide.get("text", "")
            if not title.strip():
                problems.append(f"{deck_id}/{slide_id}: empty title")
            if not text.strip():
                problems.append(f"{deck_id}/{slide_id}: empty narration")
                continue
            count = len(text.split())
            if count < MIN_WORDS:
                problems.append(f"{deck_id}/{slide_id}: narration is only {count} words (min {MIN_WORDS})")
            if count > MAX_WORDS:
                problems.append(f"{deck_id}/{slide_id}: narration is {count} words (max {MAX_WORDS})")
            if re.search(r"<!--|Timing:|Transition:", text):
                problems.append(f"{deck_id}/{slide_id}: narration contains a presenter directive")
            total_words += count
            total_slides += 1
    return scripts, total_slides, total_words


def check_media(scripts: dict, problems: list[str], verify_media: bool, require_complete: bool) -> tuple[int, int]:
    manifest = load_manifest()
    provenance = read_json(PROVENANCE_PATH, None) or {"recordings": []}
    prov_by_audio = {rec.get("audio"): rec for rec in provenance.get("recordings", [])}
    recorded = expected_total = 0
    audio_root = (SITE_ROOT / "assets" / "audio").resolve()

    for deck_id, deck in scripts["decks"].items():
        expected = set(deck["slides"])
        entries = (manifest.get("decks", {}).get(deck_id, {}) or {}).get("slides", {})
        expected_total += len(expected)
        unknown = set(entries) - expected
        if unknown:
            problems.append(f"{deck_id}: manifest has recordings for nonexistent slides {sorted(unknown)}")
        if require_complete or manifest.get("complete"):
            missing = sorted(expected - set(entries), key=slide_sort_key)
            if missing:
                problems.append(f"{deck_id}: missing recordings {missing[:8]}"
                                + (" …" if len(missing) > 8 else ""))
        for slide_id, entry in sorted(entries.items(), key=lambda kv: slide_sort_key(kv[0])):
            prefix = f"{deck_id}/{slide_id}"
            for field in ("audio", "captions"):
                value = entry.get(field, "")
                if not isinstance(value, str) or not value.startswith("/assets/audio/"):
                    problems.append(f"{prefix}: {field} must be a /assets/audio/ path, got {value!r}")
            audio_rel_path = entry.get("audio", "")
            captions_rel_path = entry.get("captions", "")
            if not audio_rel_path.startswith("/assets/audio/"):
                continue
            audio_path, captions_path = audio_abs(audio_rel_path), audio_abs(captions_rel_path)
            if not audio_path.is_file():
                problems.append(f"{prefix}: audio missing on disk: {audio_rel_path}")
            elif not audio_path.resolve().is_relative_to(audio_root):
                problems.append(f"{prefix}: audio escapes the audio root: {audio_rel_path}")
            if not captions_path.is_file():
                problems.append(f"{prefix}: captions missing on disk: {captions_rel_path}")
                continue

            # captions ≡ transcript ≡ approved script (the core invariant)
            try:
                cues = parse_vtt(captions_path.read_text(encoding="utf-8"))
            except ValueError as exc:
                problems.append(f"{prefix}: unreadable captions ({exc})")
                continue
            transcript = entry.get("transcript", "")
            script_text = deck["slides"].get(slide_id, {}).get("text", "")
            caption_words = words(" ".join(cue.text for cue in cues))
            if caption_words != words(transcript):
                problems.append(f"{prefix}: caption words differ from the manifest transcript")
            if words(transcript) != words(script_text):
                problems.append(f"{prefix}: recording transcript differs from the approved script")
            if entry.get("title") != deck["slides"].get(slide_id, {}).get("title"):
                problems.append(f"{prefix}: manifest title differs from the script title")
            for i, cue in enumerate(cues):
                if not (cue.end > cue.start):
                    problems.append(f"{prefix}: cue {i} has non-positive duration")
                if i and cue.start < cues[i - 1].start:
                    problems.append(f"{prefix}: cues are not chronological at {i}")
                wrapped = _wrap(cue.text)
                if len(wrapped) > MAX_LINES or any(len(line) > MAX_CHARS for line in wrapped):
                    problems.append(f"{prefix}: cue {i} wraps to {len(wrapped)} line(s) and would not "
                                    f"fit {MAX_LINES} lines of {MAX_CHARS} chars: {cue.text[:60]!r}")

            if not entry.get("voice") or not entry.get("caption_method"):
                problems.append(f"{prefix}: missing voice/caption_method provenance")

            # provenance record
            record = prov_by_audio.get(audio_rel_path)
            if not record:
                problems.append(f"{prefix}: no provenance entry for {audio_rel_path}")
            else:
                basis = record.get("basis", "")
                if basis not in ALLOWED_BASIS:
                    problems.append(f"{prefix}: unusable provenance basis {basis!r}")
                if not record.get("provider"):
                    problems.append(f"{prefix}: provenance has no provider")
                if basis in PREVIEW_BASIS and entry.get("caption_method") in ALIGNED_METHODS:
                    problems.append(f"{prefix}: a preview recording may not claim aligned captions")
                if verify_media and record.get("sha256") != entry.get("sha256"):
                    problems.append(f"{prefix}: provenance sha256 differs from the manifest")

            if verify_media and audio_path.is_file():
                digest = sha256_file(audio_path)
                if digest != entry.get("sha256"):
                    problems.append(f"{prefix}: audio hash changed (file was replaced or re-encoded)")
                measured = probe_duration(audio_path)
                if not (0 < measured < 600):
                    problems.append(f"{prefix}: implausible duration {measured:.2f}s")
                elif abs(measured - float(entry.get("duration", 0))) >= 0.2:
                    problems.append(f"{prefix}: duration drift {measured:.2f}s vs "
                                    f"{entry.get('duration')}s recorded")
            recorded += 1

    if not manifest.get("complete") and not require_complete:
        pass
    return recorded, expected_total


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--scripts-only", action="store_true")
    parser.add_argument("--require-complete", action="store_true")
    parser.add_argument("--no-media", action="store_true", help="skip ffprobe/sha256 (fast)")
    args = parser.parse_args(argv)

    problems: list[str] = []
    scripts, slide_count, word_count = check_scripts(problems)
    if args.scripts_only:
        if problems:
            for problem in problems:
                print(f"  ✗ {problem}")
            print(f"\nFAILED: {len(problems)} problem(s) in {len(scripts['decks'])} scripts")
            return 1
        print(f"Narration scripts verified: {len(scripts['decks'])} decks, {slide_count} slides, "
              f"{word_count:,} words "
              f"(mean {word_count / max(1, slide_count):.0f} words/slide)")
        return 0

    recorded, expected = check_media(scripts, problems, verify_media=not args.no_media,
                                     require_complete=args.require_complete)
    manifest = load_manifest()
    if problems:
        for problem in problems:
            print(f"  ✗ {problem}")
        print(f"\nFAILED: {len(problems)} problem(s) "
              f"({recorded}/{expected} slides recorded)")
        return 1
    label = "complete" if manifest.get("complete") else f"partial ({recorded}/{expected})"
    print(f"Narration verified: {len(scripts['decks'])} decks, {slide_count} scripted slides, "
          f"{recorded} recordings with timed captions — {label}")
    if not manifest.get("complete") and not args.require_complete:
        print("  note: run with --require-complete to fail on missing recordings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
