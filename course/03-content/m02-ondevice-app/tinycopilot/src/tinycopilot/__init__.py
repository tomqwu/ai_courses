"""TinyCopilot - a compact, fully working Python twin of ListenToMe's copilot core.

The hands-on lab for Module 2 (architecture) and Module 3 (privacy, testing,
shipping) of the AI Product Studio course. Every module docstring names the
Swift file it mirrors under ListenToMe's pure ``ListenToMeCore`` package.
"""

from .conversation_store import ConversationStore, TranscriptSegment
from .question_detector import QuestionDetector, is_question
from .copilot import Copilot, CopilotRole
from .model_router import (
    ModelInfo,
    capability_score,
    fetch_models,
    good_for,
    is_chat_model,
    is_local,
    rank_models,
    role_defaults,
)
from .ollama_provider import (
    EmptyResponseError,
    IncompleteStreamError,
    LLMError,
    OllamaProvider,
    ServerError,
)
from .privacy import (
    PrivacyMode,
    PrivacyViolation,
    assert_host_local,
    guard_request,
    verify_local_model,
)

__all__ = [
    "ConversationStore",
    "TranscriptSegment",
    "QuestionDetector",
    "is_question",
    "Copilot",
    "CopilotRole",
    "ModelInfo",
    "capability_score",
    "fetch_models",
    "good_for",
    "is_chat_model",
    "is_local",
    "rank_models",
    "role_defaults",
    "EmptyResponseError",
    "IncompleteStreamError",
    "LLMError",
    "OllamaProvider",
    "ServerError",
    "PrivacyMode",
    "PrivacyViolation",
    "assert_host_local",
    "guard_request",
    "verify_local_model",
]