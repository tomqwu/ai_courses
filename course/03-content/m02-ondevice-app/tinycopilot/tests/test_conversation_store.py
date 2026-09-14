"""ConversationStore specs - mirrors ConversationStoreTests in ListenToMeCore.

The contract under test: partials are kept separate from finals, a final with
the same id supersedes its partial, ``recent_context`` is a newest-first-fit
window that always keeps at least one segment, and ``transcript_text`` lists
finals oldest-first.
"""

from __future__ import annotations

import pytest

from conftest import make_segment

from tinycopilot.conversation_store import (
    DEFAULT_CONTEXT_CHARS,
    ConversationStore,
    TranscriptSegment,
)


class TestSegments:
    def test_partial_is_kept_separate_from_finals(self):
        store = ConversationStore()
        partial = make_segment("s1", "others", "so what about the", is_final=False)
        store.apply(partial)
        assert store.partial is partial
        assert store.final_segments == ()

    def test_final_with_same_id_supersedes_the_partial(self):
        store = ConversationStore()
        store.apply(make_segment("s1", "others", "so what about the", is_final=False))
        store.apply(make_segment("s1", "others", "so what about the budget?", is_final=True))
        assert store.partial is None
        assert [segment.text for segment in store.final_segments] == [
            "so what about the budget?"
        ]

    def test_a_later_partial_replaces_the_earlier_one(self):
        store = ConversationStore()
        store.apply(make_segment("s1", "you", "we should", is_final=False))
        store.apply(make_segment("s1", "you", "we should ship Friday", is_final=False))
        assert store.partial.text == "we should ship Friday"
        assert store.final_segments == ()

    def test_invalid_source_is_rejected(self):
        with pytest.raises(ValueError, match="source"):
            TranscriptSegment(id="x", source="robot", text="hi")

    def test_source_is_normalized_to_lowercase(self):
        assert make_segment("x", "You", "hi").source == "you"

    def test_labeled_line_uses_speaker_attribution(self):
        assert make_segment("s1", "others", "hi?").labeled() == "Others: hi?"
        assert make_segment("s1", "you", "hi").labeled() == "You: hi"


class TestRecentContext:
    def test_empty_store_yields_empty_context(self):
        assert ConversationStore().recent_context() == ""

    def test_budget_keeps_only_the_newest_segments(self):
        store = ConversationStore()
        for i in range(6):
            store.apply(make_segment(f"s{i}", "others", f"line-{i:02d} " + "y" * 44, ts=float(i)))
        # each labeled line is 60 chars + 1 joining newline: 3 lines = 182 <= 200 < 4 lines
        lines = store.recent_context(max_chars=200).splitlines()
        assert len(lines) == 3
        assert lines[0].startswith("Others: line-03")
        assert lines[-1].startswith("Others: line-05")
        assert "line-00" not in store.recent_context(max_chars=200)

    def test_budget_always_keeps_at_least_one_segment(self):
        store = ConversationStore()
        store.apply(make_segment("s0", "you", "x" * 5000))
        assert "x" * 5000 in store.recent_context(max_chars=100)

    def test_partial_counts_as_the_newest_segment(self):
        store = ConversationStore()
        store.apply(make_segment("s0", "others", "final line", ts=0.0))
        store.apply(make_segment("s1", "you", "partial line", is_final=False, ts=1.0))
        lines = store.recent_context().splitlines()
        assert lines == ["Others: final line", "You: partial line"]

    def test_lines_stay_in_chronological_order(self):
        store = ConversationStore()
        for i in range(3):
            store.apply(make_segment(f"s{i}", "others", f"utterance {i}", ts=float(i)))
        assert store.recent_context().splitlines() == [
            "Others: utterance 0",
            "Others: utterance 1",
            "Others: utterance 2",
        ]

    def test_non_positive_budget_is_rejected(self):
        store = ConversationStore()
        with pytest.raises(ValueError, match="max_chars"):
            store.recent_context(max_chars=0)

    def test_default_budget_is_4000_chars(self):
        assert DEFAULT_CONTEXT_CHARS == 4000
        store = ConversationStore()
        for i in range(10):
            store.apply(make_segment(f"s{i}", "others", f"seg{i} " + "z" * 900, ts=float(i)))
        context = store.recent_context()
        assert len(context) <= 4000
        assert "seg9" in context and "seg8" in context
        assert "seg0" not in context


class TestTranscriptText:
    def test_lists_finals_oldest_first_and_skips_partials(self):
        store = ConversationStore()
        store.apply(make_segment("s0", "you", "hello", ts=0.0))
        store.apply(make_segment("s1", "others", "hi there", ts=1.0))
        store.apply(make_segment("s2", "others", "mid-sentence", is_final=False, ts=2.0))
        assert store.transcript_text() == "You: hello\nOthers: hi there"

    def test_empty_store_transcript_is_empty(self):
        assert ConversationStore().transcript_text() == ""