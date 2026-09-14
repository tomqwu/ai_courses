"""Cheap, swappable question detection for proactive help.

Mirrors ``Sources/ListenToMeCore/QuestionDetector.swift`` plus the proactive
gate in ``ContextEngine.swift`` (``shouldFireProactive``): a deliberately
simple heuristic - trailing ``?``, leading interrogatives, word-boundary
phrase cues - and a debounce window. The clock is injectable so tests never
sleep, the same "testable time" seam ListenToMe's core uses.
"""

from __future__ import annotations

import re
import time
from typing import Callable

from .conversation_store import SOURCE_OTHERS, TranscriptSegment

#: Leading interrogatives - QuestionDetector.swift's first cue family.
INTERROGATIVES = ("what", "why", "how", "when", "where", "who", "whose", "which")

#: Mid-sentence phrase cues, matched on word boundaries.
PHRASE_CUES = ("can you", "any thoughts", "walk me through", "what do you think")

#: Default debounce in seconds (ListenToMe's ContextEngine also defaults to 8 s).
DEFAULT_DEBOUNCE_SECONDS = 8.0


def is_question(text: str) -> bool:
    """Return True when ``text`` looks like a question someone just asked.

    Deliberately explainable rather than clever - the spec kept this heuristic
    swappable, and so does TinyCopilot. Contractions count as their cue word
    ("what's..." leads with "what"); cue phrases must match on word
    boundaries, so "many thoughts" never triggers the "any thoughts" cue.
    """
    normalized = text.strip().lower()
    if not normalized:
        return False
    if normalized.endswith("?"):
        return True
    words = re.findall(r"[a-z]+", normalized)
    if words and words[0] in INTERROGATIVES:
        return True
    return any(re.search(rf"\b{re.escape(cue)}\b", normalized) for cue in PHRASE_CUES)


class QuestionDetector:
    """Decides whether a segment should trigger proactive AI help.

    Fires only for finalized ``others`` segments that read as questions, at
    most once per debounce window. ``clock`` is any callable returning
    seconds (``time.monotonic`` by default) - inject a fake in tests, exactly
    like ListenToMe's testable time.
    """

    def __init__(
        self,
        debounce_seconds: float = DEFAULT_DEBOUNCE_SECONDS,
        clock: Callable[[], float] | None = None,
    ) -> None:
        self.debounce_seconds = debounce_seconds
        self._clock = clock or time.monotonic
        self._last_fired: float | None = None

    def should_fire(self, segment: TranscriptSegment) -> bool:
        """True only for finalized ``others`` questions outside the debounce window."""
        if not segment.is_final or segment.source != SOURCE_OTHERS:
            return False
        if not is_question(segment.text):
            return False
        now = self._clock()
        if self._last_fired is not None and (now - self._last_fired) < self.debounce_seconds:
            return False
        self._last_fired = now
        return True