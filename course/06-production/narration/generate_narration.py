#!/usr/bin/env python3
"""Generate narrated audio + captions for the course decks.

Usage
  python3 generate_narration.py plan                      # what would be generated, and the cost
  python3 generate_narration.py generate --provider preview   # free local preview (say on macOS, espeak-ng on Linux)
  python3 generate_narration.py generate --provider elevenlabs --deck m00
  python3 generate_narration.py verify                    # run the validation contract

Design notes worth keeping (each is a lesson from ai_qe):
  * The manifest is saved after EVERY slide, so a run that dies on slide 140 has still banked 139
    recordings. A paid request is never silently thrown away.
  * The word-equality check runs BEFORE the audio is written into the manifest. If captions and the
    approved script disagree, the slide fails loudly rather than shipping a desynced deck.
  * Nothing is deleted. `--force` overwrites a recording; a plain re-run skips and re-derives the
    hash/duration, so re-running is always safe.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from captions import (build_cues, check_caption_words, load_pronunciations, spoken_tokens, write_srt,
                      write_vtt)
from narration_data import (DECK_IDS, EDITION, MANIFEST_PATH, NARRATION_DIR, PRONUNCIATIONS_PATH, PROVENANCE_PATH,
                            VOICE_PATH, audio_abs, audio_rel, load_manifest, load_scripts, read_json,
                            save_manifest, sha256_file, slide_sort_key, write_json)
from providers import (PREVIEW_PROVIDERS, ElevenLabsProvider, ProviderError, available_cost_estimate,
                       preview_provider_for_this_machine, probe_duration)


def build_provider(args):
    """Return (provider, basis, voice_label). `basis` records how the timing was obtained."""
    voice_cfg = read_json(VOICE_PATH, {}) or {}
    if args.provider == "preview":
        args.provider = preview_provider_for_this_machine()
    if args.provider in PREVIEW_PROVIDERS:
        preview = (voice_cfg.get("preview", {}) or {}).get(args.provider, {})
        kwargs = {k: preview[k] for k in ("voice", "rate", "gap_seconds") if k in preview}
        if args.voice:
            kwargs["voice"] = args.voice
        provider = PREVIEW_PROVIDERS[args.provider](**kwargs)
        return provider, "sentence-measured-preview", preview.get("label", f"{provider.name} (preview)")
    provider = ElevenLabsProvider(
        voice_id=args.voice or voice_cfg.get("voice_id", ""),
        model_id=voice_cfg.get("model_id", "eleven_v3"),
        output_format=voice_cfg.get("output_format", "mp3_44100_128"),
        voice_settings=voice_cfg.get("voice_settings"),
        language_code=voice_cfg.get("language_code", "en"),
    )
    return provider, "aligned-generation", voice_cfg.get("label", "ElevenLabs")


def selected_slides(scripts: dict, decks: list[str] | None, slides: list[str] | None):
    for deck_id in DECK_IDS:
        deck = scripts["decks"].get(deck_id)
        if not deck or (decks and deck_id not in decks):
            continue
        for slide_id in sorted(deck["slides"], key=slide_sort_key):
            if slides and slide_id not in slides:
                continue
            yield deck_id, slide_id, deck["slides"][slide_id]


def cmd_plan(args) -> int:
    scripts = load_scripts()
    voice_cfg = read_json(VOICE_PATH, {}) or {}
    estimate = available_cost_estimate(scripts, args.deck or None)
    provider = args.provider or voice_cfg.get("provider", "elevenlabs")
    print(f"provider        : {provider}")
    print(f"edition         : {EDITION}")
    print(f"decks           : {len(estimate['per_deck'])}")
    print(f"slides          : {estimate['slides']}")
    print(f"characters      : {estimate['characters']:,}  (this is what a paid provider bills on)")
    print()
    print(f"{'deck':6} {'slides':>6} {'chars':>8}  label")
    for deck_id, info in estimate["per_deck"].items():
        label = scripts["decks"][deck_id]["label"][:58]
        print(f"{deck_id:6} {info['slides']:>6} {info['characters']:>8,}  {label}")
    manifest = load_manifest()
    recorded = sum(len((manifest.get("decks", {}).get(d, {}) or {}).get("slides", {}))
                   for d in scripts["decks"])
    print(f"\nalready recorded: {recorded}/{estimate['slides']} slides (manifest complete={manifest.get('complete')})")
    if provider == "elevenlabs" and not __import__("os").environ.get("ELEVENLABS_API_KEY"):
        print("\nNOTE: ELEVENLABS_API_KEY is not set, so `generate --provider elevenlabs` will refuse.\n"
              "      Use `--provider preview` for a free local voice (say on macOS, espeak-ng on Linux), or export the key.")
    return 0


def acquire_lock():
    """Refuse to run two generators at once.

    The manifest and provenance files are read-modify-written after every slide. Two concurrent
    runs would interleave those writes and silently lose recordings, so this fails loudly instead.
    Learned the direct way: a second run was started while the first was still going.
    """
    lock = NARRATION_DIR / ".generate.lock"
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        holder = lock.read_text(encoding="utf-8").strip() if lock.exists() else "unknown"
        print(f"another generation run is already in progress (pid {holder}).\n"
              f"If that is stale, delete {lock} and re-run.", file=sys.stderr)
        return None
    os.write(fd, str(os.getpid()).encode())
    return fd


def release_lock(fd) -> None:
    if fd is None:
        return
    os.close(fd)
    (NARRATION_DIR / ".generate.lock").unlink(missing_ok=True)


def cmd_generate(args) -> int:
    lock = acquire_lock()
    if lock is None:
        return 3
    try:
        return _generate(args)
    finally:
        release_lock(lock)


def _synthesize_slide(provider, table, deck_id: str, slide_id: str, slide: dict, args) -> tuple:
    """The expensive half of one slide: speak it, time it, caption it, write the files.

    Runs in a worker thread and touches only this slide's own files, so workers never contend.
    Everything shared (manifest, provenance) is committed by the main thread as results arrive.
    """
    rel_mp3 = audio_rel(deck_id, slide_id)
    rel_vtt = audio_rel(deck_id, slide_id, suffix="vtt")
    abs_mp3, abs_vtt = audio_abs(rel_mp3), audio_abs(rel_vtt)
    text = slide["text"].strip()
    speak_text, _spans = spoken_tokens(text, table)
    try:
        result = provider.synthesize(speak_text, abs_mp3)
        cues = build_cues(text, result, table)
        check_caption_words(cues, text)          # fail BEFORE anything is committed
        write_vtt(cues, abs_vtt)
        if args.srt:
            write_srt(cues, abs_vtt.with_suffix(".srt"))
    except (ProviderError, ValueError) as exc:
        return ("fail", deck_id, slide_id, str(exc), None)
    return ("ok", deck_id, slide_id, (rel_mp3, rel_vtt, text, result, cues), None)


def _generate(args) -> int:
    scripts = load_scripts()
    if not scripts["decks"]:
        print("no narration scripts found in scripts/", file=sys.stderr)
        return 2
    table = load_pronunciations(PRONUNCIATIONS_PATH)
    try:
        provider, basis, voice_label = build_provider(args)
    except ProviderError as exc:
        print(f"provider unavailable: {exc}", file=sys.stderr)
        return 2

    manifest = load_manifest()
    provenance = read_json(PROVENANCE_PATH, None) or {"schema": 1, "recordings": []}
    manifest.setdefault("decks", {})
    manifest["provider"] = provider.name
    manifest["voice"] = voice_label
    manifest["edition"] = EDITION
    known = {rec["audio"]: rec for rec in provenance["recordings"]}

    done = skipped = failed = 0
    jobs = list(selected_slides(scripts, args.deck or None, args.slide or None))
    if args.limit:
        jobs = jobs[:args.limit]

    def commit(deck_id: str, slide_id: str, record: dict, prov: dict) -> None:
        """Bank one recording, then persist. Called only from the main thread."""
        manifest["decks"].setdefault(
            deck_id, {"label": scripts["decks"][deck_id]["label"], "slides": {}})["slides"][slide_id] = record
        provenance["recordings"] = [r for r in provenance["recordings"] if r.get("audio") != prov["audio"]]
        provenance["recordings"].append(prov)
        known[prov["audio"]] = prov
        for deck in manifest["decks"].values():
            deck["duration"] = round(sum(s.get("duration", 0) for s in deck["slides"].values()), 2)
        save_manifest(manifest)
        write_json(PROVENANCE_PATH, provenance)

    todo = []
    for deck_id, slide_id, slide in jobs:
        rel_mp3 = audio_rel(deck_id, slide_id)
        rel_vtt = audio_rel(deck_id, slide_id, suffix="vtt")
        abs_mp3 = audio_abs(rel_mp3)
        text = slide["text"].strip()
        if abs_mp3.exists() and audio_abs(rel_vtt).exists() and not args.force:
            prior = known.get(rel_mp3) or {}
            commit(deck_id, slide_id, {
                "audio": rel_mp3, "captions": rel_vtt, "transcript": text, "title": slide["title"],
                "duration": round(probe_duration(abs_mp3), 3), "sha256": sha256_file(abs_mp3),
                "voice": prior.get("voice", voice_label), "provider": prior.get("provider", provider.name),
                "caption_method": prior.get("caption_method", basis),
            }, prior or {
                "audio": rel_mp3, "sha256": sha256_file(abs_mp3), "provider": provider.name,
                "basis": basis, "voice": voice_label, "caption_method": basis,
                "generated_at": "pre-existing", "receipt": None, "evidence": None,
                "note": "Found on disk without a provenance record; adopted by a re-run.",
            })
            skipped += 1
            continue
        todo.append((deck_id, slide_id, slide))

    workers = args.workers or (4 if args.provider in PREVIEW_PROVIDERS else 1)
    if todo:
        print(f"synthesizing {len(todo)} slide(s) with {workers} worker(s)…")

    def record_for(deck_id, slide_id, payload, error):
        if error:
            failed_local = True
            return None
        rel_mp3, rel_vtt, text, result, cues = payload
        digest = sha256_file(audio_abs(rel_mp3))
        method = result.method
        slide_basis = basis if not (basis == "aligned-generation" and method != "character-alignment") \
            else "proportional-generation"
        record = {
            "audio": rel_mp3, "captions": rel_vtt, "transcript": text,
            "title": scripts["decks"][deck_id]["slides"][slide_id]["title"],
            "duration": round(result.duration, 3), "sha256": digest,
            "voice": voice_label, "provider": provider.name, "caption_method": method,
            "cues": len(cues), "words": len(text.split()),
        }
        stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        prov = {
            "audio": rel_mp3, "sha256": digest, "provider": provider.name, "basis": slide_basis,
            "voice": voice_label, "caption_method": method,
            "generated_at": stamp, "received_at": stamp, "receipt": result.receipt, "evidence": None,
            "note": ("Local preview voice generated on this machine; not the release voice."
                     if args.provider in PREVIEW_PROVIDERS else
                     "Generated against a paid voice; the provider receipt is the API response recorded here."),
        }
        return record, prov, result.duration, len(cues), method

    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        futures = {pool.submit(_synthesize_slide, provider, table, d, s, sl, args): (d, s)
                   for d, s, sl in todo}
        for future in as_completed(futures):
            deck_id, slide_id = futures[future]
            try:
                status, d, s, payload, error = future.result()
            except Exception as exc:                      # a worker bug must not kill the run
                status, d, s, payload, error = "fail", deck_id, slide_id, None, f"unexpected: {exc}"
            if status != "ok":
                failed += 1
                print(f"  FAIL {d}/{s}: {error}", file=sys.stderr)
                if args.stop_on_error:
                    for pending in futures:
                        pending.cancel()
                    break
                continue
            built = record_for(d, s, payload, None)
            record, prov, duration, cue_count, method = built
            commit(d, s, record, prov)
            done += 1
            print(f"  ok   {d}/{s}  {duration:6.2f}s  {cue_count:2} cues  ({method})")

    for deck in manifest["decks"].values():
        deck["duration"] = round(sum(s.get("duration", 0) for s in deck["slides"].values()), 2)
    recorded = sum(len(deck["slides"]) for deck in manifest["decks"].values())
    manifest["complete"] = bool(recorded) and all(
        len(manifest["decks"].get(d, {}).get("slides", {})) == len(v["slides"])
        for d, v in scripts["decks"].items())
    save_manifest(manifest)
    write_json(PROVENANCE_PATH, provenance)
    print(f"\ngenerated {done}, skipped {skipped} (already present), failed {failed}")
    print(f"manifest: {MANIFEST_PATH.name} ({recorded}/"
          f"{sum(len(v['slides']) for v in scripts['decks'].values())} slides, complete={manifest['complete']})")
    if failed:
        print("re-run to retry only the failures; existing recordings are never regenerated.")
    return 1 if failed else 0


def cmd_verify(args) -> int:
    import validate_narration
    return validate_narration.main(["--require-complete"] if args.require_complete else [])


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p_plan = sub.add_parser("plan", help="report slides/characters to generate (no writes)")
    p_plan.add_argument("--deck", action="append")
    p_plan.add_argument("--provider", choices=["elevenlabs", "say", "espeak", "preview"])
    p_plan.set_defaults(func=cmd_plan)

    p_gen = sub.add_parser("generate", help="synthesize audio + captions")
    p_gen.add_argument("--provider", choices=["elevenlabs", "say", "espeak", "preview"], default=None,
                       help="defaults to voice.json's provider; 'say' (macOS), 'espeak' (Linux) and "
                            "'preview' (whichever this machine has) need no API key")
    p_gen.add_argument("--deck", action="append", help="limit to a deck id (repeatable)")
    p_gen.add_argument("--slide", action="append", help="limit to a slide id (repeatable)")
    p_gen.add_argument("--voice", help="override the voice id/name")
    p_gen.add_argument("--limit", type=int, help="stop after N slides")
    p_gen.add_argument("--force", action="store_true", help="re-record slides that already exist")
    p_gen.add_argument("--srt", action="store_true", help="also write .srt captions")
    p_gen.add_argument("--stop-on-error", action="store_true")
    p_gen.add_argument("--workers", type=int,
                       help="parallel synthesis workers (default 4 for say, 1 for a paid provider)")
    p_gen.set_defaults(func=cmd_generate)

    p_ver = sub.add_parser("verify", help="run the narration validation contract")
    p_ver.add_argument("--require-complete", action="store_true")
    p_ver.set_defaults(func=cmd_verify)

    args = parser.parse_args(argv)
    if getattr(args, "provider", None) is None and args.command == "generate":
        args.provider = (read_json(VOICE_PATH, {}) or {}).get("provider", "elevenlabs")
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
