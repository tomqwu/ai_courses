"""Pure prompt builders - no I/O, no state, therefore fully unit-testable.

Mirrors ``Sources/ListenToMeCore/Prompt.swift``: the three base system prompts
(the anti-preamble Quick prompt, the Listener's never-invent contract, the
depth-over-brevity Deep prompt), the persona and response-language directives
appended to *every* role (``systemWithDirectives``), and the ``ResponseAction``
catalog behind ListenToMe's contextual action buttons.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - exists only for type checkers (no runtime cycle)
    from .copilot import CopilotRole

#: The verbatim anti-hallucination contract from Prompt.swift's listener prompt.
LISTENER_CONTRACT = (
    "Never invent an owner, deadline, agreement, or completion. "
    "Mark missing details as unstated."
)

#: The three base system prompts, keyed by role (PromptBuilder's base prompts).
SYSTEM_PROMPTS: dict[str, str] = {
    "quick": (
        "You are Quick, the user's live meeting assistant. The user is in the "
        "meeting right now, reading your answer between sentences.\n"
        "No preamble, no sign-off, no \"As an AI\" disclaimer, and never "
        "restate the question. Answer directly in 1-3 short sentences."
    ),
    "listener": (
        "You are the Listener, the meeting's note-taker. Produce a rolling "
        "summary of the conversation so far, structured in four sections "
        "(omit a section only when it is empty):\n"
        "Summary - where the discussion stands, in a few sentences.\n"
        "Decisions - what was actually decided.\n"
        "Actions - who does what, by when.\n"
        "Open questions - what remains unanswered.\n"
        + LISTENER_CONTRACT
    ),
    "deep": (
        "You are Deep, the user's analysis partner. Prefer depth over "
        "brevity: surface assumptions, risks, trade-offs, and non-obvious "
        "implications the group may be missing. Use short headers or bullets "
        "when they help, and never pad - every sentence must earn its place."
    ),
}

#: Default task line per role when neither a question nor an action is given.
ROLE_TASKS: dict[str, str] = {
    "quick": "Answer the user's request using the conversation context.",
    "listener": "Summarize the conversation so far.",
    "deep": "Analyze the conversation in depth.",
}


class ResponseAction(Enum):
    """Contextual actions with a short instruction template each.

    Mirrors ``ResponseAction`` in ``Prompt.swift`` (ListenToMe ships nine;
    TinyCopilot keeps the six core ones plus two extras).
    """

    ANSWER_QUESTION = "Answer the question below directly and concisely."
    RECAP = "Recap the conversation so far in at most 3 bullets."
    ACTION_ITEMS = (
        "List the action items, with owner and deadline only when stated. "
        "Mark missing details as unstated."
    )
    CLARIFY = "Name what is ambiguous and ask at most two clarifying questions."
    COUNTERPOINT = "Offer a polite counterpoint or a risk the group may be missing."
    DRAFT_REPLY = "Draft a short reply the user could send as-is."
    FOLLOW_UP = "Suggest up to three follow-up questions worth asking next."
    KEY_TERMS = "Define the key terms and jargon that appeared in the conversation."

    @property
    def instruction(self) -> str:
        """The action's short instruction template."""
        return self.value


def _role_name(role: "CopilotRole | str") -> str:
    """Normalize a role (enum member or plain string) to its prompt key."""
    value = getattr(role, "value", role)
    name = str(value).strip().lower()
    if name not in SYSTEM_PROMPTS:
        raise ValueError(
            f"unknown copilot role {role!r}; expected one of {sorted(SYSTEM_PROMPTS)}"
        )
    return name


def build_system_prompt(
    role: "CopilotRole | str",
    persona: str | None = None,
    response_language: str | None = None,
) -> str:
    """Base system prompt for ``role``, with persona and language directives appended.

    Mirrors ``PromptBuilder.systemWithDirectives``: the preset's persona
    guidance and the response-language directive are appended to **every**
    role - the same path manual panes and automatic reviews use.
    """
    parts = [SYSTEM_PROMPTS[_role_name(role)]]
    if persona:
        parts.append(f"Persona guidance: {persona.strip()}")
    if response_language:
        parts.append(f"Always respond in {response_language.strip()}.")
    return "\n\n".join(parts)


def build_user_prompt(
    role: "CopilotRole | str",
    context_text: str,
    question: str | None = None,
    action: ResponseAction | None = None,
) -> str:
    """Build the user message: task line, optional question, and the context window.

    Deterministic and side-effect free - same inputs, same string - which is
    what makes the prompt layer unit-testable without an LLM.
    """
    name = _role_name(role)
    if action is not None:
        task = action.instruction
    elif question and question.strip():
        task = "Answer the question below using the conversation context."
    else:
        task = ROLE_TASKS[name]
    parts = [f"Task: {task}"]
    if question and question.strip():
        parts.append(f'Question: "{question.strip()}"')
    parts.append("Conversation so far (speaker-labeled, newest last):")
    parts.append(context_text.strip() or "(no transcript yet)")
    return "\n\n".join(parts)