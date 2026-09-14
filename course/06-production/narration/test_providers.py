#!/usr/bin/env python3
"""Tests for the TTS providers. Run: python3 test_providers.py

The ElevenLabs adapter is the **primary** voice for this course but cannot be exercised here — it
needs a paid key this repository does not hold. Leaving the release path untested because a key is
missing is how a release path rots, so these tests drive it through a stubbed transport with a real
MP3 and a real `ffprobe` measurement. What is faked is the network call; what is verified is our code:
the request we build, the alignment we parse, the fallback we take when alignment does not line up,
and the errors we raise.

Nothing here proves the *voice* is good. Only a real key can do that (issue #21).
"""
from __future__ import annotations

import base64
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

from captions import build_cues, check_caption_words, words
from providers import ElevenLabsProvider, ProviderError, SayProvider, split_sentences

HAVE_FFMPEG = bool(shutil.which("ffmpeg")) and bool(shutil.which("ffprobe"))
SENTENCE_A = "The pipeline records a decision, not just a result."
SENTENCE_B = "Every caption is checked against the approved words."


def make_mp3(seconds: float = 4.0) -> bytes:
    """A real, probeable MP3 of silence, so duration measurement is genuine."""
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "silence.mp3"
        subprocess.run(
            ["ffmpeg", "-v", "error", "-f", "lavfi", "-i",
             f"anullsrc=r=44100:cl=mono", "-t", str(seconds),
             "-c:a", "libmp3lame", "-b:a", "64k", "-y", str(out)],
            check=True, capture_output=True)
        return out.read_bytes()


def alignment_for(text: str, duration: float) -> dict:
    """Character-level timing in the shape the API returns, spread evenly across the clip."""
    step = duration / max(1, len(text))
    return {
        "characters": list(text),
        "character_start_times_seconds": [round(i * step, 4) for i in range(len(text))],
        "character_end_times_seconds": [round((i + 1) * step, 4) for i in range(len(text))],
    }


class FakeResponse(io.BytesIO):
    def __init__(self, payload: bytes):
        super().__init__(payload)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def payload(audio: bytes, alignment: dict | None) -> bytes:
    body = {"audio_base64": base64.b64encode(audio).decode("ascii")}
    if alignment is not None:
        body["alignment"] = alignment
    return json.dumps(body).encode("utf-8")


@unittest.skipUnless(HAVE_FFMPEG, "ffmpeg/ffprobe are required to measure real audio")
class TestElevenLabsAdapter(unittest.TestCase):
    """Drive the release path with a stubbed socket but a real encode and a real probe."""

    @classmethod
    def setUpClass(cls):
        cls.audio = make_mp3(4.0)

    def provider(self, **kwargs):
        return ElevenLabsProvider(voice_id="voice-abc", api_key="test-key-not-real", **kwargs)

    def test_request_we_build_is_correct(self):
        text = f"{SENTENCE_A} {SENTENCE_B}"
        captured = {}

        def fake_urlopen(request, timeout=None):
            captured["url"] = request.full_url
            captured["headers"] = {k.lower(): v for k, v in request.header_items()}
            captured["body"] = json.loads(request.data.decode("utf-8"))
            captured["timeout"] = timeout
            return FakeResponse(payload(self.audio, alignment_for(text, 4.0)))

        with mock.patch("providers.urllib.request.urlopen", fake_urlopen):
            with tempfile.TemporaryDirectory() as tmp:
                out = Path(tmp) / "slide.mp3"
                result = self.provider().synthesize(text, out)
                self.assertTrue(out.is_file())
                self.assertEqual(out.read_bytes(), self.audio)

        self.assertIn("/text-to-speech/voice-abc/with-timestamps", captured["url"])
        self.assertIn("output_format=mp3_44100_128", captured["url"])
        self.assertEqual(captured["headers"]["xi-api-key"], "test-key-not-real")
        self.assertEqual(captured["body"]["text"], text)
        self.assertEqual(captured["body"]["model_id"], "eleven_v3")
        self.assertEqual(captured["body"]["voice_settings"]["similarity_boost"], 0.75)
        self.assertEqual(captured["timeout"], 180)
        # Duration is measured from the file, not taken on trust from the response.
        self.assertAlmostEqual(result.duration, 4.0, delta=0.15)
        self.assertEqual(result.method, "character-alignment")
        self.assertEqual(result.receipt["alignment_matched"], True)
        self.assertEqual(result.receipt["characters"], len(text))
        self.assertEqual(result.receipt["voice_id"], "voice-abc")

    def test_aligned_captions_are_word_exact_and_ordered(self):
        text = f"{SENTENCE_A} {SENTENCE_B}"
        with mock.patch("providers.urllib.request.urlopen",
                        lambda *a, **k: FakeResponse(payload(self.audio, alignment_for(text, 4.0)))):
            with tempfile.TemporaryDirectory() as tmp:
                result = self.provider().synthesize(text, Path(tmp) / "s.mp3")

        cues = build_cues(text, result, {})
        check_caption_words(cues, text)                     # raises on any drift
        self.assertEqual(" ".join(c.text for c in cues).split(), text.split())
        for i, cue in enumerate(cues):
            self.assertGreater(cue.end, cue.start)
            if i:
                self.assertGreaterEqual(cue.start, cues[i - 1].start)
        self.assertGreaterEqual(cues[0].start, 0.0)
        self.assertLessEqual(cues[-1].end, 4.0 + 0.2)


    def test_token_times_map_each_token_to_its_own_characters(self):
        """Pins the exact per-token span. Word-exactness alone cannot catch a timing regression,
        because cue text comes from the display text rather than from the alignment."""
        text = "ab cd"
        starts = [0.0, 0.1, 0.2, 0.3, 0.4]        # one 0.1 s character each
        ends = [0.1, 0.2, 0.3, 0.4, 0.5]
        spans = ElevenLabsProvider._token_times(text, starts, ends)
        # token 0 covers characters 0..1, token 1 covers characters 3..4
        self.assertEqual(len(spans), 2)
        self.assertAlmostEqual(spans[0][0], 0.0)
        self.assertAlmostEqual(spans[0][1], 0.2)
        self.assertAlmostEqual(spans[1][0], 0.3)
        self.assertAlmostEqual(spans[1][1], 0.5)

    def test_token_times_handle_multiple_spaces(self):
        text = "ab   cd"
        starts = [i * 0.1 for i in range(len(text))]
        ends = [(i + 1) * 0.1 for i in range(len(text))]
        spans = ElevenLabsProvider._token_times(text, starts, ends)
        self.assertEqual(len(spans), 2)
        self.assertAlmostEqual(spans[0][0], 0.0)
        self.assertAlmostEqual(spans[0][1], 0.2)
        self.assertAlmostEqual(spans[1][0], 0.5)   # "cd" starts at character index 5
        self.assertAlmostEqual(spans[1][1], 0.7)

    def test_aligned_cue_times_follow_the_alignment_not_an_average(self):
        """An alignment with a long gap must survive into the cue times."""
        text = "alpha beta"
        starts = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 2.0, 2.1, 2.2, 2.3]
        ends = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 2.1, 2.2, 2.3, 2.4]
        with mock.patch("providers.urllib.request.urlopen",
                        lambda *a, **k: FakeResponse(payload(self.audio, {
                            "characters": list(text),
                            "character_start_times_seconds": starts,
                            "character_end_times_seconds": ends}))):
            with tempfile.TemporaryDirectory() as tmp:
                result = self.provider().synthesize(text, Path(tmp) / "s.mp3")
        self.assertEqual(len(result.tokens), 2)
        self.assertAlmostEqual(result.tokens[0][0], 0.0)
        self.assertAlmostEqual(result.tokens[0][1], 0.5)
        self.assertAlmostEqual(result.tokens[1][0], 2.0)
        self.assertAlmostEqual(result.tokens[1][1], 2.4)
        cues = build_cues(text, result, {})
        self.assertEqual(len(cues), 1)
        # The cue's span must reflect the real end of the second word, not half the clip.
        self.assertAlmostEqual(cues[0].start, 0.0, delta=0.01)
        self.assertAlmostEqual(cues[0].end, 2.4, delta=0.01)

    def test_alignment_that_does_not_line_up_falls_back_and_says_so(self):
        text = f"{SENTENCE_A} {SENTENCE_B}"
        # The provider normalised the text, so its alignment is shorter than what we sent.
        short = alignment_for(text, 4.0)
        short["characters"] = short["characters"][:10]
        short["character_start_times_seconds"] = short["character_start_times_seconds"][:10]
        short["character_end_times_seconds"] = short["character_end_times_seconds"][:10]
        with mock.patch("providers.urllib.request.urlopen",
                        lambda *a, **k: FakeResponse(payload(self.audio, short))):
            with tempfile.TemporaryDirectory() as tmp:
                result = self.provider().synthesize(text, Path(tmp) / "s.mp3")

        self.assertEqual(result.method, "sentence-measured")
        self.assertIsNone(result.tokens)
        self.assertFalse(result.receipt["alignment_matched"])
        self.assertIn("proportional fallback", result.receipt["note"])
        self.assertEqual(len(result.sentences), len(split_sentences(text)))
        cues = build_cues(text, result, {})
        check_caption_words(cues, text)

    def test_missing_alignment_is_tolerated(self):
        text = f"{SENTENCE_A} {SENTENCE_B}"
        with mock.patch("providers.urllib.request.urlopen",
                        lambda *a, **k: FakeResponse(payload(self.audio, None))):
            with tempfile.TemporaryDirectory() as tmp:
                result = self.provider().synthesize(text, Path(tmp) / "s.mp3")
        self.assertEqual(result.method, "sentence-measured")
        check_caption_words(build_cues(text, result, {}), text)

    def test_key_comes_from_the_environment(self):
        with mock.patch.dict(os.environ, {"ELEVENLABS_API_KEY": "from-env"}, clear=False):
            p = ElevenLabsProvider(voice_id="v")
            self.assertEqual(p._key, "from-env")

    def test_missing_key_refuses_clearly(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ProviderError) as ctx:
                ElevenLabsProvider(voice_id="v")
        message = str(ctx.exception)
        self.assertIn("ELEVENLABS_API_KEY", message)
        self.assertIn("--provider say", message)            # points at the way out

    def test_http_error_is_reported_without_leaking_the_key(self):
        def raise_http(*args, **kwargs):
            raise urllib.error.HTTPError(
                "https://api.elevenlabs.io", 401, "Unauthorized", {}, io.BytesIO(b'{"detail":"bad key"}'))

        with mock.patch("providers.urllib.request.urlopen", raise_http):
            with tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(ProviderError) as ctx:
                    self.provider().synthesize("hello there", Path(tmp) / "s.mp3")
        message = str(ctx.exception)
        self.assertIn("401", message)
        self.assertNotIn("test-key-not-real", message)

    def test_network_failure_does_not_retry(self):
        """A retry after an ambiguous network failure can bill twice, so we must not retry."""
        calls = {"n": 0}

        def fail(*args, **kwargs):
            calls["n"] += 1
            raise urllib.error.URLError("connection reset")

        with mock.patch("providers.urllib.request.urlopen", fail):
            with tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(ProviderError) as ctx:
                    self.provider().synthesize("hello there", Path(tmp) / "s.mp3")
        self.assertEqual(calls["n"], 1, "the adapter retried a request that may already be charged")
        self.assertIn("may have been charged", str(ctx.exception))

    def test_refuses_empty_text_and_overlong_text(self):
        p = self.provider()
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ProviderError):
                p.synthesize("   ", Path(tmp) / "s.mp3")
            with self.assertRaises(ProviderError) as ctx:
                p.synthesize("x" * 5001, Path(tmp) / "s.mp3")
        self.assertIn("5000", str(ctx.exception))


class TestPreviewProvider(unittest.TestCase):
    @unittest.skipUnless(HAVE_FFMPEG and shutil.which("say"), "say and ffmpeg are required")
    def test_preview_measures_each_sentence(self):
        text = f"{SENTENCE_A} {SENTENCE_B}"
        with tempfile.TemporaryDirectory() as tmp:
            result = SayProvider().synthesize(text, Path(tmp) / "s.mp3")
        self.assertEqual(result.method, "sentence-measured")
        self.assertEqual(len(result.sentences), len(split_sentences(text)))
        # The measured sentences must be ordered and inside the clip.
        previous = 0.0
        for start, end in result.sentences:
            self.assertGreaterEqual(start, previous)
            self.assertGreater(end, start)
            previous = end
        cues = build_cues(text, result, {})
        check_caption_words(cues, text)
        self.assertEqual(words(" ".join(c.text for c in cues)), words(text))


if __name__ == "__main__":
    unittest.main()
