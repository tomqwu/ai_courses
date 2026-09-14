"""QuestionDetector specs - mirrors QuestionDetectorTests + the proactive gate.

The contract under test: every cue family (trailing "?", leading
interrogatives, word-boundary phrase cues) triggers; near-miss words
("however", "whatsapp", "many thoughts") do not; and ``should_fire`` gates on
finalized .others segments plus an injectable-clock debounce window.
"""

from __future__ import annotations

import pytest

from conftest import FakeClock, make_segment

from tinycopilot.question_detector import (
    DEFAULT_DEBOUNCE_SECONDS,
    QuestionDetector,
    is_question,
)


@pytest.mark.parametrize(
    "text",
    [
        "any thoughts?",
        "so, where do we stand?",
        "what",
        "what's the deadline?",  # contraction still leads with 'what'
        "why did the build break",
        "how about we skip the demo",
        "when should we ship",
        "where is the spec",
        "who owns the router",
        "whose call was that",
        "which model did you pick",
    ],
)
def test_trailing_mark_and_leading_interrogatives_are_questions(text):
    assert is_question(text) is True


@pytest.mark.parametrize(
    "text",
    [
        "can you help me with the deploy",
        "any thoughts on the budget",
        "please walk me through the architecture",
        "tell me, what do you think about the plan",
    ],
)
def test_phrase_cues_match_without_a_question_mark(text):
    assert is_question(text) is True


@pytest.mark.parametrize(
    "text",
    [
        "",
        "   ",
        "sounds good, let's ship it",
        "however you slice it, we are late",  # 'however' is not 'how'
        "the whatsapp group is noisy",  # 'whatsapp' is not 'what'
        "many thoughts were shared in the room",  # 'many' must not trigger 'any thoughts'
        "i walked them through it yesterday",  # cue is 'walk me through'
        "we cannot use your laptop",  # 'cannot' is not 'can you'
    ],
)
def test_near_misses_are_not_questions(text):
    assert is_question(text) is False


def make_detector(clock=None, debounce=8.0):
    return QuestionDetector(debounce_seconds=debounce, clock=clock or FakeClock())


class TestShouldFire:
    def test_fires_for_a_final_others_question(self):
        detector = make_detector()
        segment = make_segment("s1", "others", "can you walk me through it?", is_final=True)
        assert detector.should_fire(segment) is True

    def test_ignores_the_users_own_questions(self):
        detector = make_detector()
        assert detector.should_fire(make_segment("s1", "you", "what do you think?")) is False

    def test_ignores_partials(self):
        detector = make_detector()
        segment = make_segment("s1", "others", "what about the", is_final=False)
        assert detector.should_fire(segment) is False

    def test_ignores_non_questions(self):
        detector = make_detector()
        segment = make_segment("s1", "others", "ok great, thanks", is_final=True)
        assert detector.should_fire(segment) is False


class TestDebounce:
    def test_second_question_inside_the_window_is_debounced(self):
        clock = FakeClock()
        detector = make_detector(clock)
        first = make_segment("s1", "others", "first question?", is_final=True)
        second = make_segment("s2", "others", "second question?", is_final=True)
        assert detector.should_fire(first) is True
        clock.advance(3.0)  # 3 s later: inside the 8 s window
        assert detector.should_fire(second) is False

    def test_question_after_the_window_fires_again(self):
        clock = FakeClock()
        detector = make_detector(clock)
        assert detector.should_fire(make_segment("s1", "others", "first?")) is True
        clock.advance(8.0)  # exactly at the window edge
        assert detector.should_fire(make_segment("s2", "others", "second?")) is True

    def test_the_debounce_window_is_configurable(self):
        clock = FakeClock()
        detector = make_detector(clock, debounce=1.0)
        assert detector.should_fire(make_segment("s1", "others", "first?")) is True
        clock.advance(1.5)
        assert detector.should_fire(make_segment("s2", "others", "second?")) is True

    def test_non_questions_do_not_reset_the_window(self):
        clock = FakeClock()
        detector = make_detector(clock)
        assert detector.should_fire(make_segment("s1", "others", "real question?")) is True
        clock.advance(2.0)
        segment = make_segment("s2", "others", "just a remark", is_final=True)
        assert detector.should_fire(segment) is False  # neither fires...
        clock.advance(6.0)  # ...nor pushes the window out: 8 s after the first fire
        assert detector.should_fire(make_segment("s3", "others", "another question?")) is True

    def test_default_debounce_is_8_seconds(self):
        assert QuestionDetector().debounce_seconds == DEFAULT_DEBOUNCE_SECONDS == 8.0