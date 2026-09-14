#!/usr/bin/env python3
"""Shared paths, schemas and I/O for the narration pipeline.

Three files, three different questions (the separation is ported from ai_qe):

  scripts/mNN.json   — the APPROVED WORDS. Authored by a human, reviewed, the source of truth.
  manifest.json      — the RECORDINGS. Derived: which file plays on which slide, how long it is,
                       and what its bytes hash to. Regenerable from the scripts at any time.
  provenance.json    — the BASIS. Who/what produced each recording, when, and whether a receipt
                       exists. Answers "may I claim this is the release voice?" rather than
                       "which file plays?".
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

NARRATION_DIR = Path(__file__).resolve().parent
COURSE_DIR = NARRATION_DIR.parents[1]
SITE_ROOT = COURSE_DIR / "learner-site"
SCRIPTS_DIR = NARRATION_DIR / "scripts"
MANIFEST_PATH = NARRATION_DIR / "manifest.json"
PROVENANCE_PATH = NARRATION_DIR / "provenance.json"
PRONUNCIATIONS_PATH = NARRATION_DIR / "pronunciations.json"
VOICE_PATH = NARRATION_DIR / "voice.json"

EDITION = "aps-1.0.0"
DECK_IDS = ["m00", "m01", "m02", "m03", "m04", "m05", "m06", "m07", "m08"]

# Slide-count floor/ceiling for a narration script, in words. The floor exists so a "narration"
# cannot be a stub; the ceiling keeps a slide's narration under about a minute.
MIN_WORDS, MAX_WORDS = 25, 190


def read_json(path: Path, default=None):
    if not Path(path).exists():
        return default
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_scripts() -> dict:
    decks = {}
    for deck_id in DECK_IDS:
        path = SCRIPTS_DIR / f"{deck_id}.json"
        if not path.exists():
            continue
        decks[deck_id] = read_json(path)
    return {"edition": EDITION, "decks": decks}


def audio_rel(deck_id: str, slide_id: str, edition: str = EDITION, suffix: str = "mp3") -> str:
    """Site-root-relative path, which is what the player fetches."""
    return f"/assets/audio/{edition}/{deck_id}/{slide_id}.{suffix}"


def audio_abs(rel_path: str) -> Path:
    return SITE_ROOT / rel_path.lstrip("/")


def deck_label(deck_id: str) -> str:
    return (load_scripts().get("decks", {}).get(deck_id, {}) or {}).get("label", deck_id.upper())


def slide_sort_key(slide_id: str) -> int:
    match = re.search(r"(\d+)$", slide_id)
    return int(match.group(1)) if match else 0


def empty_manifest() -> dict:
    voice = read_json(VOICE_PATH, {}) or {}
    return {
        "edition": EDITION,
        "complete": False,
        "voice": voice.get("label", "unset"),
        "provider": voice.get("provider", "unset"),
        "decks": {},
    }


def load_manifest() -> dict:
    return read_json(MANIFEST_PATH, None) or empty_manifest()


def save_manifest(manifest: dict) -> None:
    manifest["complete"] = manifest_is_complete(manifest)
    write_json(MANIFEST_PATH, manifest)


def manifest_is_complete(manifest: dict) -> bool:
    """True only when every slide of every authored deck has a recording."""
    scripts = load_scripts().get("decks", {})
    if not scripts:
        return False
    for deck_id, deck in scripts.items():
        recorded = (manifest.get("decks", {}).get(deck_id, {}) or {}).get("slides", {})
        if set(recorded) != set(deck["slides"]):
            return False
    return True
