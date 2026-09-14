"""Shared test fixtures: the fake transport (our MockLLMProvider) and helpers.

Mirrors the role of ``Sources/ListenToMeCoreTests/Mocks.swift``: everything in
this file exists so the suite runs with no daemon, no network, and no
sleeping. The fake transport implements the same seam ListenToMe injects as
``lineSource``: ``post(path, payload) -> (status, NDJSON-lines)``.
"""

from __future__ import annotations

import json

from tinycopilot.conversation_store import TranscriptSegment

#: The daemon address used in unit tests - nothing ever contacts it.
BASE_URL = "http://localhost:11434"


class FakeClock:
    """Injectable seconds clock - the testable-time seam from ListenToMe's core."""

    def __init__(self, start: float = 0.0) -> None:
        self.now = float(start)

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


class FakeTransport:
    """Callable transport matching the OllamaProvider seam.

    ``transport(path, payload) -> (status, NDJSON-line iterator)``. ``events``
    is the default response; ``responses`` queues ``(status, events)`` pairs
    consumed by successive calls (each call gets a fresh iterator, like a
    real stream). Events may be dicts (auto-encoded to NDJSON) or raw strings.
    """

    def __init__(self, status: int = 200, events=None, responses=None) -> None:
        self.status = status
        self.events = list(events or [])
        self.responses = [(s, list(e)) for s, e in (responses or [])]
        self.requests: list = []

    def __call__(self, path: str, payload):
        self.requests.append((path, payload))
        if self.responses:
            status, events = self.responses.pop(0)
        else:
            status, events = self.status, self.events
        return status, self._lines(events)

    @staticmethod
    def _lines(events):
        for event in events:
            yield event if isinstance(event, str) else json.dumps(event)

    @property
    def last_payload(self):
        return self.requests[-1][1]


def make_chat_events(*deltas: str, done: bool = True) -> list:
    """Build the NDJSON event list for a chat completion yielding ``deltas``.

    The final line mirrors what Ollama really sends: ``done: true`` with no
    message content, plus stop metadata.
    """
    events = [
        {"model": "m", "message": {"role": "assistant", "content": delta}, "done": False}
        for delta in deltas
    ]
    if done:
        events.append({"model": "m", "done": True, "done_reason": "stop"})
    return events


def make_segment(
    segment_id: str,
    source: str = "others",
    text: str = "",
    is_final: bool = True,
    ts: float = 0.0,
) -> TranscriptSegment:
    """Convenience constructor for TranscriptSegment in tests."""
    return TranscriptSegment(
        id=segment_id, source=source, text=text, is_final=is_final, ts=ts
    )