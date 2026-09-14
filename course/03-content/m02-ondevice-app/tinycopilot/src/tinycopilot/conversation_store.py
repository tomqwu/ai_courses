"""Rolling conversation store with a character budget.

Mirrors ``Sources/ListenToMeCore/ConversationStore.swift``: a finalized-utterance
log plus the current partial, where ``recent_context(max_chars)`` keeps the
newest segments that fit the budget (default 4,000 chars) and always keeps at
least one segment when anything has been said.
"""

from __future__ import annotations

from dataclasses import dataclass

#: Speaker sources, mirroring ``SpeakerSource`` (``.you`` / ``.others``) in ListenToMe.
SOURCE_YOU = "you"
SOURCE_OTHERS = "others"

_SOURCE_LABELS = {SOURCE_YOU: "You", SOURCE_OTHERS: "Others"}

#: Default context budget in characters (ListenToMe's ConversationStore uses the same 4,000).
DEFAULT_CONTEXT_CHARS = 4000


@dataclass(frozen=True)
class TranscriptSegment:
    """One utterance of transcript, tagged with its speaker source.

    Mirrors the ``TranscriptSegment`` value type in ``ConversationStore.swift``:
    ``id`` comes from the transcriber, ``is_final`` distinguishes a settled
    utterance from the live partial, and ``ts`` is seconds from an injectable
    clock so tests never need to sleep.
    """

    id: str
    source: str
    text: str
    is_final: bool = False
    ts: float = 0.0

    def __post_init__(self) -> None:
        source = self.source.strip().lower()
        if source not in _SOURCE_LABELS:
            raise ValueError(f"source must be 'you' or 'others', got {self.source!r}")
        object.__setattr__(self, "source", source)

    @property
    def speaker_label(self) -> str:
        """Display label - 'You' or 'Others' - like ListenToMe's pane attribution."""
        return _SOURCE_LABELS[self.source]

    def labeled(self) -> str:
        """Format as one attributed transcript line, e.g. ``"Others: any thoughts?"``."""
        return f"{self.speaker_label}: {self.text}"


class ConversationStore:
    """Finalized-utterance log plus the current partial.

    Mirrors ``ConversationStore.swift``. Partials never enter the finalized
    log; a finalized segment with the same id supersedes the partial it grew
    from. ``recent_context`` is the character-budgeted window that the prompt
    builders consume.
    """

    def __init__(self) -> None:
        self._finals: list[TranscriptSegment] = []
        self._partial: TranscriptSegment | None = None

    @property
    def final_segments(self) -> tuple[TranscriptSegment, ...]:
        """The finalized utterances, oldest first."""
        return tuple(self._finals)

    @property
    def partial(self) -> TranscriptSegment | None:
        """The in-flight (not yet final) utterance, if any."""
        return self._partial

    def apply(self, segment: TranscriptSegment) -> None:
        """Fold one segment into the store (mirrors ``apply(_:)``)."""
        if segment.is_final:
            if self._partial is not None and self._partial.id == segment.id:
                self._partial = None  # the finalized utterance supersedes its partial
            self._finals.append(segment)
        else:
            self._partial = segment

    def recent_context(self, max_chars: int = DEFAULT_CONTEXT_CHARS) -> str:
        """Newest-first-fit window over the conversation, as speaker-labeled lines.

        Walks the segments newest-to-oldest, keeping each while it fits the
        budget; the newest segment is always kept even when it alone exceeds
        the budget (``recentContext``'s "always at least one" guarantee). The
        current partial, when present, counts as the newest segment.
        """
        if max_chars <= 0:
            raise ValueError(f"max_chars must be positive, got {max_chars}")
        segments = list(self._finals)
        if self._partial is not None:
            segments.append(self._partial)
        chosen: list[TranscriptSegment] = []
        used = 0
        for segment in reversed(segments):
            line = segment.labeled()
            cost = len(line) + (1 if chosen else 0)  # +1 for the joining newline
            if chosen and used + cost > max_chars:
                break
            chosen.append(segment)
            used += cost
        chosen.reverse()
        return "\n".join(segment.labeled() for segment in chosen)

    def transcript_text(self) -> str:
        """The full finalized transcript, oldest first (what export and save use)."""
        return "\n".join(segment.labeled() for segment in self._finals)