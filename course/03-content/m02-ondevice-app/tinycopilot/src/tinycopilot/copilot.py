"""The orchestrator: roles, per-role models, streaming, and cancellation.

Mirrors ``Sources/ListenToMeCore/MeetingSession.swift``: per-role providers and
generation tokens (``set_model`` cancels the role's in-flight stream so a stale
answer can never arrive under a new model's name), plus the Listener-to-Quick/Deep
grounding rule - only a **completed** listener summary is ever injected into
other roles' prompts, never the in-flight one.
"""

from __future__ import annotations

from collections.abc import Iterator
from enum import Enum

from .conversation_store import ConversationStore, TranscriptSegment
from .ollama_provider import OllamaProvider, Transport
from .prompts import build_system_prompt, build_user_prompt
from .question_detector import QuestionDetector

#: Mirrors ``LLMRequest.Purpose.quickEvaluation``: quick answers get no thinking
#: preamble and want deterministic output.
_QUICK_OPTIONS = {"think": False, "temperature": 0.0}


class CopilotRole(Enum):
    """The three AI roles, mirroring ``CopilotRole.swift`` (listener / quick / deep)."""

    LISTENER = "listener"
    QUICK = "quick"
    DEEP = "deep"


def _as_role(role: "CopilotRole | str") -> CopilotRole:
    """Accept a CopilotRole member or its lowercase name ('quick', ...)."""
    if isinstance(role, CopilotRole):
        return role
    try:
        return CopilotRole(str(role).strip().lower())
    except ValueError:
        raise ValueError(
            f"unknown copilot role {role!r}; expected one of {[r.value for r in CopilotRole]}"
        ) from None


class Copilot:
    """Wires store, detector, and per-role providers into one copilot loop.

    ``models_by_role`` maps each role (enum member or its name) to a model
    name; ``transport`` is the provider seam tests fake. ``persona`` and
    ``response_language`` thread through every role's system prompt, exactly
    like ListenToMe's preset persona guidance.
    """

    def __init__(
        self,
        ollama_base_url: str,
        store: ConversationStore,
        detector: QuestionDetector,
        models_by_role: "dict",
        transport: Transport | None = None,
        persona: str | None = None,
        response_language: str | None = None,
    ) -> None:
        self.ollama_base_url = ollama_base_url.rstrip("/")
        self.store = store
        self.detector = detector
        self.persona = persona
        self.response_language = response_language
        self._transport = transport
        self.providers: dict[CopilotRole, OllamaProvider] = {}
        # Per-role generation tokens (MeetingSession's responseGenerations):
        # every new generation or model switch bumps the token, and a stream
        # whose token no longer matches stops yielding - stale deltas drop.
        self._generations: dict[CopilotRole, int] = {role: 0 for role in CopilotRole}
        #: The last **completed** listener summary; in-flight ones never land here.
        self.last_completed_listener_summary: str | None = None
        for role, model_name in dict(models_by_role or {}).items():
            self.set_model(role, model_name)

    def set_model(self, role: "CopilotRole | str", name: str) -> None:
        """Point a role at a model; the role's in-flight generation is cancelled."""
        role = _as_role(role)
        self._generations[role] += 1
        self.providers[role] = OllamaProvider(self.ollama_base_url, name, transport=self._transport)

    @property
    def models(self) -> "dict[str, str | None]":
        """The configured model name per role (None when a role has no model yet)."""
        return {
            role.value: self.providers[role].model if role in self.providers else None
            for role in CopilotRole
        }

    def ingest(self, segment: TranscriptSegment) -> "str | None":
        """Fold a segment into the store; if it fires the detector, answer it with Quick.

        Returns the proactive Quick answer, or None when nothing fired.
        """
        self.store.apply(segment)
        if not self.detector.should_fire(segment):
            return None
        answer = "".join(self.generate(CopilotRole.QUICK, question=segment.text.strip()))
        return answer or None

    def generate(self, role: "CopilotRole | str", question: "str | None" = None) -> Iterator[str]:
        """Start a role's answer and return its delta stream.

        The generation token is taken eagerly - the moment ``generate`` is
        called - so a second ``generate`` (or a ``set_model``) immediately
        cancels any in-flight stream for that role. Quick/Deep prompts are
        grounded in the last *completed* listener summary (never an in-flight
        one), and iteration stops early when this generation goes stale, so a
        stale stream can never write output under the new model's name.
        """
        role = _as_role(role)
        provider = self.providers.get(role)
        if provider is None:
            raise ValueError(f"no model configured for role {role.value!r}; call set_model() first")
        token = self._generations[role] + 1
        self._generations[role] = token

        system_prompt = build_system_prompt(
            role, persona=self.persona, response_language=self.response_language
        )
        context = self.store.recent_context()
        if role is not CopilotRole.LISTENER:
            summary = self.last_completed_listener_summary
            if summary:
                context = f"Completed listener summary:\n{summary}\n\nTranscript:\n{context}"
        user_prompt = build_user_prompt(role, context, question=question)
        options = _QUICK_OPTIONS if role is CopilotRole.QUICK else None
        return self._stream_answer(role, provider, token, system_prompt, user_prompt, options)

    def _stream_answer(
        self,
        role: CopilotRole,
        provider: OllamaProvider,
        token: int,
        system_prompt: str,
        user_prompt: str,
        options: "dict | None",
    ) -> Iterator[str]:
        """Yield the answer's deltas; stop the moment this generation goes stale."""
        parts: list[str] = []
        for delta in provider.stream_chat(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            options=options,
        ):
            if self._generations[role] != token:
                return  # cancelled by set_model or a newer generation - drop stale deltas
            parts.append(delta)
            yield delta
        if role is CopilotRole.LISTENER and self._generations[role] == token:
            self.last_completed_listener_summary = "".join(parts).strip() or None