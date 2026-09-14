#!/usr/bin/env python3
"""Tests for the caption engine. Run: python3 test_captions.py

The invariant under test is the one the whole pipeline rests on: the words a learner reads in the
captions are exactly the words in the approved script.
"""
from __future__ import annotations

import unittest

from captions import (MAX_CHARS, MAX_LINES, _wrap, sentence_groups, sentence_texts,
    Cue, Synthesis, build_cues, check_caption_words, from_clock, parse_vtt,
    spoken_tokens, to_clock, words, write_srt, write_vtt,
)
from providers import split_sentences

TABLE = {"PostgreSQL": "Postgres", "Testcontainers": "Test containers", "REST Assured": "Rest Assured"}


class TestWords(unittest.TestCase):
    def test_normalises_case_and_punctuation(self):
        self.assertEqual(words("Hello,  world!"), ["hello", "world"])
        self.assertEqual(words("PostgreSQL,"), ["postgresql"])

    def test_numbers_are_words(self):
        self.assertEqual(words("191 passed."), ["191", "passed"])


class TestClock(unittest.TestCase):
    def test_round_trip(self):
        for value in (0.0, 1.5, 61.25, 3599.999, 7200.123):
            self.assertAlmostEqual(from_clock(to_clock(value)), value, places=3)

    def test_format(self):
        self.assertEqual(to_clock(0), "00:00:00.000")
        self.assertEqual(to_clock(65.5), "00:01:05.500")

    def test_rejects_junk(self):
        for bad in ("1:2:3:4", "abc", "--:--"):
            with self.assertRaises(ValueError):
                from_clock(bad)


class TestPronunciations(unittest.TestCase):
    def test_single_token_expands_to_two(self):
        speak, spans = spoken_tokens("Use Testcontainers today", TABLE)
        self.assertEqual(speak, "Use Test containers today")
        self.assertEqual(spans, [[0], [1, 2], [3]])

    def test_punctuation_is_preserved_around_the_phrase(self):
        speak, _ = spoken_tokens("Run PostgreSQL, then stop.", TABLE)
        self.assertEqual(speak, "Run Postgres, then stop.")

    def test_multi_word_key(self):
        speak, spans = spoken_tokens("REST Assured runs", TABLE)
        self.assertEqual(speak, "Rest Assured runs")
        self.assertEqual(spans, [[0], [1], [2]])

    def test_no_table_is_identity(self):
        speak, spans = spoken_tokens("nothing changes here", {})
        self.assertEqual(speak, "nothing changes here")
        self.assertEqual(spans, [[0], [1], [2]])

    def test_spans_cover_every_spoken_token_exactly_once(self):
        """A respelling may change the spoken words; the span map must still cover them all."""
        for text in ("Use Testcontainers", "Run PostgreSQL, then stop.", "REST Assured runs"):
            speak, spans = spoken_tokens(text, TABLE)
            self.assertEqual(len(spans), len(text.split()))
            flat = [j for span in spans for j in span]
            self.assertEqual(flat, list(range(len(speak.split()))))
            self.assertTrue(all(span for span in spans))   # no display token is left untimed

    def test_phrase_that_changes_word_count_is_not_applied(self):
        """A multi-word key that would change length is skipped rather than mis-attributed."""
        speak, spans = spoken_tokens("REST Assured runs", {"REST Assured": "Restful"})
        self.assertEqual(speak, "REST Assured runs")
        self.assertEqual(spans, [[0], [1], [2]])


class TestBuildCues(unittest.TestCase):
    def test_aligned_tokens_produce_matching_words(self):
        display = "The route picks a model per role. Listener is fastest."
        tokens = [(i * 0.3, i * 0.3 + 0.3) for i in range(len(display.split()))]
        synth = Synthesis(duration=len(tokens) * 0.3, method="character-alignment", tokens=tokens)
        cues = build_cues(display, synth, TABLE)
        check_caption_words(cues, display)          # must not raise
        self.assertGreater(len(cues), 0)

    def test_sentence_measured_distributes_and_matches(self):
        display = "First sentence here. Second sentence follows."
        synth = Synthesis(duration=6.0, method="sentence-measured",
                          sentences=[(0.0, 3.0), (3.2, 6.0)])
        cues = build_cues(display, synth, TABLE)
        check_caption_words(cues, display)
        self.assertTrue(all(c.end > c.start for c in cues))
        self.assertAlmostEqual(cues[0].start, 0.0, places=2)
        self.assertLessEqual(cues[-1].end, 6.0 + 1e-6)

    def test_times_are_monotonic(self):
        display = " ".join(f"word{i}" for i in range(60))
        synth = Synthesis(duration=30.0, method="sentence-measured", sentences=[(0.0, 30.0)])
        cues = build_cues(display, synth, TABLE)
        for a, b in zip(cues, cues[1:]):
            self.assertLessEqual(a.start, b.start)
            self.assertLessEqual(a.start, a.end)
            self.assertLessEqual(a.end, b.end)
        check_caption_words(cues, display)

    def test_respects_width_limits(self):
        display = " ".join(["supercalifragilistic"] * 8)
        synth = Synthesis(duration=20.0, method="sentence-measured", sentences=[(0.0, 20.0)])
        cues = build_cues(display, synth, TABLE)
        for cue in cues:
            for line in cue.text.split("\n"):
                self.assertLessEqual(len(line), 42)
        check_caption_words(cues, display)

    def test_cues_end_at_sentence_boundaries(self):
        """A cue that straddles two sentences reads badly; break at the sentence end instead."""
        display = "Every module ends with a lab you can run. SignUpFlow ships seven test tiers now."
        synth = Synthesis(duration=8.0, method="sentence-measured",
                          sentences=[(0.0, 4.0), (4.0, 8.0)])
        cues = build_cues(display, synth, TABLE)
        check_caption_words(cues, display)
        self.assertEqual(len(cues), 2)
        self.assertTrue(cues[0].text.endswith("run."))
        self.assertTrue(cues[1].text.startswith("SignUpFlow"))

    def test_substitution_still_matches_display(self):
        display = "Start Testcontainers and PostgreSQL now."
        synth = Synthesis(duration=5.0, method="sentence-measured", sentences=[(0.0, 5.0)])
        cues = build_cues(display, synth, TABLE)
        check_caption_words(cues, display)
        self.assertIn("Testcontainers", " ".join(c.text for c in cues))
        self.assertNotIn("Test containers", " ".join(c.text for c in cues))

    def test_empty_text(self):
        self.assertEqual(build_cues("", Synthesis(duration=0, method="x")), [])


class TestMismatchDetection(unittest.TestCase):
    def test_check_raises_on_changed_word(self):
        cues = [Cue(0, 1, "the route picks a model")]
        with self.assertRaises(ValueError):
            check_caption_words(cues, "the route picks the model")

    def test_check_raises_on_dropped_word(self):
        cues = [Cue(0, 1, "the route picks")]
        with self.assertRaises(ValueError):
            check_caption_words(cues, "the route picks a model")


class TestSerialisation(unittest.TestCase):
    def test_vtt_round_trip(self):
        import tempfile
        from pathlib import Path
        cues = [Cue(0.0, 1.5, "First line."), Cue(1.5, 3.25, "Second line.")]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "x.vtt"
            write_vtt(cues, path)
            back = parse_vtt(path.read_text())
        self.assertEqual(len(back), 2)
        self.assertEqual([c.text for c in back], ["First line.", "Second line."])
        self.assertAlmostEqual(back[1].end, 3.25, places=3)

    def test_srt_round_trip_via_parse(self):
        import tempfile
        from pathlib import Path
        cues = [Cue(0.0, 1.0, "Only cue.")]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "x.srt"
            write_srt(cues, path)
            text = path.read_text()
        self.assertIn("00:00:00,000 --> 00:00:01,000", text)

    def test_parse_rejects_non_vtt(self):
        with self.assertRaises(ValueError):
            parse_vtt("not a caption file")

    def test_parse_strips_markup(self):
        vtt = "WEBVTT\n\n00:00:00.000 --> 00:00:01.000\n<v Chris><b>Hello</b> &amp; welcome\n"
        self.assertEqual(parse_vtt(vtt)[0].text, "Hello & welcome")


class TestSentenceRuleIsShared(unittest.TestCase):
    """Regression: the provider and the captioner must agree on sentence count.

    The original substring-based abbreviation guard replaced "ms." inside "seams.", merging two
    sentences; the provider then measured 5 durations for 6 groups and the tail of every affected
    slide got timings from the wrong part of the clip.
    """

    def test_abbreviation_inside_a_word_does_not_protect(self):
        self.assertEqual(len(sentence_texts("It has seams. You will see them.")), 2)
        for word in ("seams.", "forms.", "systems.", "terms.", "problems."):
            self.assertEqual(len(sentence_texts(f"Here are the {word} Next sentence.")), 2,
                             f"{word} must still end a sentence")

    def test_real_abbreviation_still_protected(self):
        self.assertEqual(len(sentence_texts("Dr. Smith left. He ran fast.")), 2)
        self.assertEqual(len(sentence_texts("Use e.g. this one. Then stop.")), 2)

    def test_provider_and_captioner_agree(self):
        samples = [
            "One. Two! Three?",
            "It has seams. You will see them.",
            "Dr. Smith left. He ran fast.",
            "no. 5 is here. Next one.",
            "A single sentence without an end",
            "Ends with a bracket.) Another one.",
        ]
        for text in samples:
            self.assertEqual(len(split_sentences(text)), len(sentence_groups(text.split())),
                             f"disagreement on {text!r}")

    def test_mismatched_sentence_count_is_rejected(self):
        text = "One sentence here. And a second one."
        synth = Synthesis(duration=4.0, method="sentence-measured",
                          sentences=[(0.0, 2.0), (2.2, 4.0)],
                          tokens=None, receipt={})
        cues = build_cues(text, synth)
        self.assertTrue(cues)
        # Drop a measured sentence: the counts no longer line up, so it must raise, not scramble.
        broken = Synthesis(duration=4.0, method="sentence-measured",
                           sentences=[(0.0, 2.0)], tokens=None, receipt={})
        with self.assertRaises(ValueError):
            build_cues(text, broken)

    def test_cues_are_chronological(self):
        text = ("The system has seams. You will route models per role, cancel stale streams, and "
                "type streaming errors so truncation fails loudly. Notice what is absent here.")
        synth = Synthesis(duration=30.0, method="sentence-measured",
                          sentences=[(0.0, 3.0), (3.2, 22.0), (22.2, 30.0)],
                          tokens=None, receipt={})
        cues = build_cues(text, synth)
        for i, cue in enumerate(cues):
            self.assertGreater(cue.end, cue.start)
            if i:
                self.assertGreaterEqual(cue.start, cues[i - 1].start)
        self.assertEqual(words(" ".join(c.text for c in cues)), words(text))

    def test_a_five_versus_six_mismatch_is_the_documented_bug(self):
        # The exact shape of the original failure: "seams." must produce its own sentence.
        text = ("You will name the file that implements each stage, and justify the three protocol "
                "seams. You will route models per role. Notice what is not here.")
        self.assertEqual(len(split_sentences(text)), 3)



class TestCueWidthIsEnforced(unittest.TestCase):
    """Regression: merging a sliver cue must not push the result past the line limits.

    A short final sentence ("question.") was merged into the previous cue unconditionally, producing
    three-line cues of up to 97 characters that the validator rejected.
    """

    def test_short_final_sentence_does_not_widen_the_previous_cue(self):
        text = ("These six bullets are the whole contract of this module. You will sketch the "
                "pipeline from capture through transcribe, context, prompt, and route. You will "
                "name the file that implements each stage, and justify the three protocol seams. "
                "You will route models per role, cancel stale streams, write prompt builders as "
                "pure functions, and type streaming errors so truncation fails loudly. Notice what "
                "is not here: no prompt engineering tricks and no model benchmarks. This module is "
                "about architecture, where decisions live and how they are proved, and each "
                "objective maps to one lab step and at least one quiz question.")
        synth = Synthesis(duration=36.0, method="sentence-measured",
                          sentences=[(0.0, 2.8), (3.1, 8.5), (8.8, 14.7), (15.0, 22.5),
                                     (22.8, 27.3), (27.6, 36.0)],
                          tokens=None, receipt={})
        cues = build_cues(text, synth)
        for cue in cues:
            wrapped = _wrap(cue.text)
            self.assertLessEqual(len(wrapped), MAX_LINES, f"too many lines: {cue.text!r}")
            self.assertTrue(all(len(line) <= MAX_CHARS for line in wrapped),
                            f"line too long: {cue.text!r}")
            self.assertGreater(cue.end, cue.start)
        self.assertEqual(words(" ".join(c.text for c in cues)), words(text))

    def test_every_cue_respects_the_limits(self):
        # A long single sentence with no early break point must still break inside the limits.
        text = ("An autonomous implementation loop needs a spec precise enough that a stranger can "
                "implement it without asking a single question about intent or scope.")
        synth = Synthesis(duration=12.0, method="sentence-measured",
                          sentences=[(0.0, 12.0)], tokens=None, receipt={})
        cues = build_cues(text, synth)
        for cue in cues:
            wrapped = _wrap(cue.text)
            self.assertLessEqual(len(wrapped), MAX_LINES)
            self.assertTrue(all(len(line) <= MAX_CHARS for line in wrapped))
        self.assertEqual(words(" ".join(c.text for c in cues)), words(text))


if __name__ == "__main__":
    unittest.main(verbosity=2)
