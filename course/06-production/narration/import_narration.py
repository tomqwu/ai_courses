#!/usr/bin/env python3
"""Import an externally recorded take for a slide (a human narrator, or audio recorded elsewhere).

  python3 import_narration.py --deck m00 --slide slide-3 --audio ~/takes/m00-3.mp3 \\
      --captions ~/takes/m00-3.vtt --note "Recorded by AL, 2026-02-04, Neumann TLM 103"

  # no caption file? captions are generated proportionally and labelled as such
  python3 import_narration.py --deck m00 --slide slide-3 --audio ~/takes/m00-3.mp3

What it does, and refuses to do:

  * Copies the audio into the edition's asset directory and records its true duration and sha256.
  * If you supply captions, they are parsed and their words are compared against the approved script.
    A mismatch is a hard failure: an imported take must say exactly what the script approved.
  * If you do not, timing is spread over the sentences by character share and the recording is marked
    `caption_method: proportional-generation`, so nobody mistakes it for an alignment.
  * Records `basis: external-recording` with the source path and the source file's hash as evidence,
    because "where did this come from?" is the question an imported file always raises.

The audio is never modified, and the approved script is never edited to match a recording — that
direction of drift is exactly what the word-equality check exists to prevent.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from captions import (build_cues, check_caption_words, load_pronunciations, parse_vtt,
                      proportional_sentences, words, write_srt, write_vtt)
from narration_data import (EDITION, PRONUNCIATIONS_PATH, PROVENANCE_PATH, VOICE_PATH, audio_abs,
                            audio_rel, load_manifest, load_scripts, read_json, save_manifest,
                            sha256_file, write_json)
from providers import ProviderError, probe_duration


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--deck", required=True)
    parser.add_argument("--slide", required=True)
    parser.add_argument("--audio", required=True, help="path to the recorded audio file")
    parser.add_argument("--captions", help="path to a .vtt for the take (optional)")
    parser.add_argument("--note", default="", help="provenance note: who, when, how")
    parser.add_argument("--srt", action="store_true")
    args = parser.parse_args(argv)

    scripts = load_scripts()
    deck = scripts["decks"].get(args.deck)
    if not deck:
        print(f"unknown deck {args.deck!r}", file=sys.stderr)
        return 2
    slide = deck["slides"].get(args.slide)
    if not slide:
        print(f"unknown slide {args.slide!r} in {args.deck}", file=sys.stderr)
        return 2

    source = Path(os.path.expanduser(args.audio))
    if not source.is_file():
        print(f"audio not found: {source}", file=sys.stderr)
        return 2

    rel_mp3 = audio_rel(args.deck, args.slide)
    rel_vtt = audio_rel(args.deck, args.slide, suffix="vtt")
    abs_mp3, abs_vtt = audio_abs(rel_mp3), audio_abs(rel_vtt)
    text = slide["text"].strip()

    try:
        duration = probe_duration(source)
    except ProviderError as exc:
        print(f"cannot measure the take: {exc}", file=sys.stderr)
        return 2
    if not (0 < duration < 600):
        print(f"implausible duration {duration:.2f}s — is this the right file?", file=sys.stderr)
        return 2

    # Captions first: if they disagree with the script, nothing is copied.
    supplied_words = None
    if args.captions:
        caption_path = Path(os.path.expanduser(args.captions))
        if not caption_path.is_file():
            print(f"captions not found: {caption_path}", file=sys.stderr)
            return 2
        try:
            supplied = parse_vtt(caption_path.read_text(encoding="utf-8"))
        except ValueError as exc:
            print(f"unreadable captions: {exc}", file=sys.stderr)
            return 2
        supplied_words = words(" ".join(cue.text for cue in supplied))
        if supplied_words != words(text):
            print("the supplied captions do not match the approved script word for word:\n"
                  f"  captions: {len(supplied_words)} words\n  script:   {len(words(text))} words\n"
                  "Either re-record to the approved words, or update the script deliberately and "
                  "re-record. This tool will not silently reconcile the two.", file=sys.stderr)
            return 1
        caption_note = "imported captions"
        method = "imported-from-recording"
    else:
        caption_note = "generated proportionally from the take's duration"
        method = "proportional-generation"

    abs_mp3.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, abs_mp3)

    if args.captions:
        shutil.copy2(Path(os.path.expanduser(args.captions)), abs_vtt)
    else:
        table = load_pronunciations(PRONUNCIATIONS_PATH)
        from captions import Synthesis
        synth = Synthesis(duration=duration, method=method,
                          sentences=proportional_sentences(text, duration), tokens=None, receipt={})
        cues = build_cues(text, synth, table)
        check_caption_words(cues, text)
        write_vtt(cues, abs_vtt)
    if args.srt:
        write_srt(parse_vtt(abs_vtt.read_text(encoding="utf-8")), abs_vtt.with_suffix(".srt"))

    digest = sha256_file(abs_mp3)
    source_digest = sha256_file(source)
    voice_cfg = read_json(VOICE_PATH, {}) or {}

    manifest = load_manifest()
    manifest.setdefault("decks", {}).setdefault(
        args.deck, {"label": deck["label"], "slides": {}})["slides"][args.slide] = {
        "audio": rel_mp3, "captions": rel_vtt, "transcript": text, "title": slide["title"],
        "duration": round(duration, 3), "sha256": digest,
        "voice": args.note or "externally recorded", "provider": "external",
        "caption_method": method,
    }
    for entry in manifest["decks"].values():
        entry["duration"] = round(sum(s.get("duration", 0) for s in entry["slides"].values()), 2)
    recorded = sum(len(e["slides"]) for e in manifest["decks"].values())
    manifest["complete"] = bool(recorded) and all(
        len(manifest["decks"].get(d, {}).get("slides", {})) == len(v["slides"])
        for d, v in scripts["decks"].items())
    save_manifest(manifest)

    provenance = read_json(PROVENANCE_PATH, None) or {"schema": 1, "recordings": []}
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    provenance["recordings"] = [r for r in provenance["recordings"] if r.get("audio") != rel_mp3]
    provenance["recordings"].append({
        "audio": rel_mp3, "sha256": digest, "provider": "external", "basis": "external-recording",
        "voice": args.note or "externally recorded", "caption_method": method,
        "generated_at": None, "received_at": stamp,
        "receipt": None,
        "evidence": {"source_path": str(source), "source_sha256": source_digest,
                     "imported_at": stamp, "edition": EDITION},
        "note": args.note or "Imported take with no further attribution supplied.",
    })
    write_json(PROVENANCE_PATH, provenance)

    print(f"imported {source.name} → {rel_mp3}")
    print(f"  duration : {duration:.2f}s")
    print(f"  captions : {rel_vtt} ({caption_note})")
    print(f"  basis    : external-recording")
    print(f"  script   : matched word for word ({len(words(text))} words)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
