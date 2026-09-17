#!/usr/bin/env python3
"""TTS providers behind one interface.

Both providers return a `ProviderResult`: the audio path, its true duration, the timing source, the
per-sentence spans, and (when the provider can give it) a real timestamp per spoken token. Captions
are always shaped from the *display* text in `captions.py`; this module only supplies timing.

  * `elevenlabs` — the release voice. POSTs to `/v1/text-to-speech/<voice>/with-timestamps`, which
    returns a character-level alignment. Requires ELEVENLABS_API_KEY and a paid tier. Never retries a
    charged request on network uncertainty: a second call could bill twice for the same sentence, so
    the operator is told to check provider history instead (the rule ai_qe learned the same way,
    `ai_qe/tools/generate_elevenlabs_narration.py:93-94`).
  * `say` / `espeak` — the local preview. Synthesizes one sentence at a time with macOS `say` or
    Linux `espeak-ng`, measures each with ffprobe, and concatenates. Sentence timing is therefore
    real; word timing inside a sentence is distributed proportionally. No key, no cost, no network —
    which is what makes the pipeline testable, the site listenable before the release voice exists,
    and the gate runnable on a Linux CI runner.
"""
from __future__ import annotations

import base64
import json
import os
import sys
import re
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from captions import (ABBREVIATIONS, proportional_sentences,   # noqa: E402
                      sentence_texts)  # the one sentence rule and one timing fallback

API_ROOT = "https://api.elevenlabs.io/v1"
PAID_TIERS = {"creator", "pro", "scale", "business", "enterprise"}

class ProviderError(RuntimeError):
    pass


@dataclass
class ProviderResult:
    path: Path
    duration: float
    method: str                                   # character-alignment | sentence-measured
    sentences: list[tuple[float, float]] = field(default_factory=list)
    tokens: list[tuple[float, float]] | None = None
    receipt: dict = field(default_factory=dict)


# ---------------------------------------------------------------- helpers

def split_sentences(text: str) -> list[str]:
    """Split narration into sentences for per-sentence synthesis.

    Sentence-level timing is what makes the preview provider's captions honest: each cue group is a
    real measured duration, not a guess. Delegates to `captions.sentence_texts` so the sentence
    count always matches the groups the captioner builds.
    """
    return sentence_texts(text)


def probe_duration(path: Path) -> float:
    """True duration in seconds via ffprobe. Raises rather than guessing."""
    if not shutil.which("ffprobe"):
        raise ProviderError("ffprobe not found — install ffmpeg (needed to measure audio duration)")
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout
    return float(json.loads(out)["format"]["duration"])


def _ffmpeg(args: list[str]) -> None:
    if not shutil.which("ffmpeg"):
        raise ProviderError("ffmpeg not found — install ffmpeg (needed to assemble preview audio)")
    proc = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        raise ProviderError(f"ffmpeg failed: {proc.stderr.strip()[:400]}")


# ---------------------------------------------------------------- local preview

class LocalSentenceProvider:
    """A free, offline preview voice that is honest about timing.

    Each sentence is synthesized on its own, measured with ffprobe, and the pieces are concatenated
    with a fixed gap, so every caption group carries a real measured duration. Subclasses supply the
    one thing that differs between local engines: how to speak a sentence into a file.
    """
    name = "local preview"
    part_suffix = ".wav"
    bitrate = "64k"   # preview only: mono 64k keeps a full course to ~20 MB locally

    def __init__(self, voice: str, rate: int, gap_seconds: float = 0.28):
        self.voice = voice
        self.rate = rate
        self.gap = gap_seconds

    def _speak(self, sentence: str, part: Path) -> None:      # pragma: no cover — per engine
        raise NotImplementedError

    def receipt(self, sentences: int) -> dict:
        return {"provider": self.name, "voice": self.voice, "rate": self.rate,
                "sentences": sentences, "gap_seconds": self.gap}

    def synthesize(self, text: str, out_path: Path) -> ProviderResult:
        sentences = split_sentences(text)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            silence = tmpdir / f"silence{self.part_suffix}"
            _ffmpeg(["-f", "lavfi", "-i", "anullsrc=r=22050:cl=mono", "-t", f"{self.gap}",
                     "-c:a", "pcm_s16le", str(silence)])
            pieces: list[Path] = []
            spans: list[tuple[float, float]] = []
            cursor = 0.0
            for index, sentence in enumerate(sentences):
                part = tmpdir / f"part{index:03d}{self.part_suffix}"
                self._speak(sentence, part)
                duration = probe_duration(part)
                spans.append((cursor, cursor + duration))
                cursor += duration
                pieces.append(part)
                if index < len(sentences) - 1:
                    pieces.append(silence)
                    cursor += self.gap
            listing = tmpdir / "concat.txt"
            listing.write_text("".join(f"file '{p.as_posix()}'\n" for p in pieces), encoding="utf-8")
            _ffmpeg(["-f", "concat", "-safe", "0", "-i", str(listing),
                     "-ac", "1", "-c:a", "libmp3lame", "-b:a", self.bitrate, "-ar", "44100", str(out_path)])
        return ProviderResult(
            path=out_path,
            duration=probe_duration(out_path),
            method="sentence-measured",
            sentences=spans,
            tokens=None,
            receipt=self.receipt(len(sentences)),
        )


class SayProvider(LocalSentenceProvider):
    """macOS `say`: free, offline, sentence-accurate. Preview quality, honestly labelled."""
    name = "macOS say"
    part_suffix = ".aiff"

    def __init__(self, voice: str = "Samantha", rate: int = 175, gap_seconds: float = 0.28):
        if not shutil.which("say"):
            raise ProviderError("macOS `say` not found — use --provider espeak on Linux, "
                                "--provider elevenlabs for the release voice, or run on macOS")
        super().__init__(voice, rate, gap_seconds)

    def available_voices(self) -> list[str]:
        out = subprocess.run(["say", "-v", "?"], capture_output=True, text=True).stdout
        return [line.split()[0] for line in out.splitlines() if line.strip()]

    def _speak(self, sentence: str, part: Path) -> None:
        subprocess.run(["say", "-v", self.voice, "-r", str(self.rate), "-o", str(part), sentence],
                       check=True, capture_output=True)


class EspeakProvider(LocalSentenceProvider):
    """`espeak-ng`: the same preview on Linux and CI runners, where `say` does not exist.

    Rougher than `say`, and labelled the same way: sentence-measured preview, never the release
    voice. `apt-get install espeak-ng ffmpeg` is the whole setup.
    """
    name = "espeak-ng"
    part_suffix = ".wav"

    def __init__(self, voice: str = "en-us", rate: int = 165, gap_seconds: float = 0.28):
        self.binary = shutil.which("espeak-ng") or shutil.which("espeak")
        if not self.binary:
            raise ProviderError("espeak-ng not found — `apt-get install espeak-ng ffmpeg`, "
                                "or use --provider say on macOS")
        super().__init__(voice, rate, gap_seconds)

    def available_voices(self) -> list[str]:
        out = subprocess.run([self.binary, "--voices=en"], capture_output=True, text=True).stdout
        return [line.split()[3] for line in out.splitlines()[1:] if len(line.split()) > 3]

    def _speak(self, sentence: str, part: Path) -> None:
        # Text goes on stdin so a sentence that starts with "-" is never read as a flag.
        subprocess.run([self.binary, "-v", self.voice, "-s", str(self.rate), "-w", str(part), "--stdin"],
                       input=sentence, text=True, check=True, capture_output=True)


PREVIEW_PROVIDERS = {"say": SayProvider, "espeak": EspeakProvider}


def preview_provider_for_this_machine() -> str:
    """The preview engine this machine has: `say` on macOS, `espeak` where espeak-ng is installed."""
    if shutil.which("say"):
        return "say"
    if shutil.which("espeak-ng") or shutil.which("espeak"):
        return "espeak"
    raise ProviderError("no local preview voice: install espeak-ng (Linux) or run on macOS for `say`")


# ---------------------------------------------------------------- elevenlabs

class ElevenLabsProvider:
    """The release voice. Character-level alignment gives exact cue timings."""
    name = "ElevenLabs"

    def __init__(self, voice_id: str, model_id: str = "eleven_v3",
                 output_format: str = "mp3_44100_128", voice_settings: dict | None = None,
                 language_code: str = "en", api_key: str | None = None):
        self.voice_id = voice_id
        self.model_id = model_id
        self.output_format = output_format
        self.voice_settings = voice_settings or {
            "stability": 0.5, "similarity_boost": 0.75, "style": 0.0, "use_speaker_boost": True,
        }
        self.language_code = language_code
        key = api_key or os.environ.get("ELEVENLABS_API_KEY")
        if not key:
            raise ProviderError(
                "ELEVENLABS_API_KEY is not set. Export it, or run with --provider say for a local "
                "preview. The key is read from the environment and never written to disk."
            )
        self._key = key

    def synthesize(self, text: str, out_path: Path) -> ProviderResult:
        if not text.strip():
            raise ProviderError("refusing to send empty text")
        if len(text) > 5000:
            raise ProviderError(f"text is {len(text)} chars; the API limit is 5000")
        url = f"{API_ROOT}/text-to-speech/{self.voice_id}/with-timestamps?output_format={self.output_format}"
        payload = {
            "text": text,
            "model_id": self.model_id,
            "language_code": self.language_code,
            "voice_settings": self.voice_settings,
        }
        request = urllib.request.Request(
            url, data=json.dumps(payload).encode("utf-8"), method="POST",
            headers={"xi-api-key": self._key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
        )
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                body = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:                      # never echo the key
            detail = exc.read().decode("utf-8", "replace")[:300]
            raise ProviderError(f"ElevenLabs HTTP {exc.code}: {detail}") from None
        except (urllib.error.URLError, TimeoutError) as exc:
            raise ProviderError(
                f"network failure calling ElevenLabs ({exc}). This request may have been charged — "
                "check provider history before re-running, do not blindly retry."
            ) from None

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(base64.b64decode(body["audio_base64"]))
        alignment = body.get("alignment") or {}
        characters = alignment.get("characters") or []
        starts = alignment.get("character_start_times_seconds") or []
        ends = alignment.get("character_end_times_seconds") or []

        method, tokens = "sentence-measured", None
        if characters and len(characters) == len(text) and len(starts) == len(characters) == len(ends):
            tokens = self._token_times(text, starts, ends)
            method = "character-alignment"
        result = ProviderResult(
            path=out_path,
            duration=probe_duration(out_path),
            method=method,
            sentences=[],
            tokens=tokens,
            receipt={
                "provider": self.name, "voice_id": self.voice_id, "model_id": self.model_id,
                "output_format": self.output_format, "characters": len(text),
                "alignment_matched": method == "character-alignment",
            },
        )
        if method != "character-alignment":
            # Alignment did not line up with the sent text (provider normalisation): fall back to
            # distributing the measured duration over sentences, and say so in the receipt.
            result.receipt["note"] = "provider alignment length differed from request; used proportional fallback"
            result.sentences = self._proportional_sentences(text, result.duration)
        return result

    @staticmethod
    def _token_times(text: str, starts: list[float], ends: list[float]) -> list[tuple[float, float]]:
        """Map character timings onto whitespace tokens of the sent text."""
        spans: list[tuple[float, float]] = []
        for match in re.finditer(r"\S+", text):
            lo, hi = match.start(), match.end() - 1
            spans.append((float(starts[lo]), float(ends[hi])))
        return spans

    @staticmethod
    def _proportional_sentences(text: str, duration: float) -> list[tuple[float, float]]:
        return proportional_sentences(text, duration)


def available_cost_estimate(scripts: dict, deck_ids: list[str] | None = None) -> dict:
    """Count characters that a full generation would send — the number the provider bills on."""
    decks = scripts.get("decks", scripts)
    total_chars = total_slides = 0
    per_deck = {}
    for deck_id, deck in decks.items():
        if deck_ids and deck_id not in deck_ids:
            continue
        chars = sum(len(slide["text"]) for slide in deck["slides"].values())
        per_deck[deck_id] = {"slides": len(deck["slides"]), "characters": chars}
        total_chars += chars
        total_slides += len(deck["slides"])
    return {"slides": total_slides, "characters": total_chars, "per_deck": per_deck}
