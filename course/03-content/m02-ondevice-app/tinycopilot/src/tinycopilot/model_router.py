"""Model discovery, capability ranking, and local-first role defaults.

Mirrors ``Sources/ListenToMeCore/ModelRanking.swift`` (plus the MVP-era
``ModelRouter.swift`` registry): parameter-size parsing, token-prefix name
matching, the pro/flash boost and demote weights, and ``role_defaults`` -
Quick and Listener get the fastest model, Deep the strongest, and ``:cloud``
models are filtered out of auto-selection unless no local model exists.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass

from .ollama_provider import ServerError, Transport, httpx_transport

#: Name tokens that hint at a stronger model (ModelRanking's capability boosts).
BOOST_TOKENS = ("pro", "reason", "coder", "max")
#: Name tokens that hint at a faster, lighter model (ModelRanking's demotions).
DEMOTE_TOKENS = ("flash", "mini", "lite", "small")
#: What one boost/demote token is worth, in parameter-size units (billions).
HINT_WEIGHT = 20.0

_PARAM_RE = re.compile(r"(\d+(?:\.\d+)?)\s*([tTbBmM])")


def _parse_params(text: str) -> float:
    """Parse a stated parameter size like '0.6b', '751.63M', or '2.81T' into billions.

    Returns 0.0 when no size is stated. A bare number does not count: the
    '3' in 'qwen3' is a version, not a size.
    """
    match = _PARAM_RE.search(text)
    if not match:
        return 0.0
    unit = match.group(2).lower()
    multiplier = {"t": 1000.0, "b": 1.0, "m": 0.001}[unit]
    return float(match.group(1)) * multiplier


def _tokens(name: str) -> list[str]:
    """Split a model name into lowercase word tokens: 'gemma-mini:12b' -> ['gemma', 'mini', '12b']."""
    return re.findall(r"[a-z0-9]+", name.lower())


def _has_cue(tokens: list[str], cue: str) -> bool:
    """Token-prefix matching: the cue must match a whole token from its start.

    This is the fix for the classic 'gemini' contains 'mini' false hit:
    'gemini' does not *start with* 'mini', so gemini models are never demoted
    as minis, while 'mini' and 'ministral' both are.
    """
    return any(token == cue or token.startswith(cue) for token in tokens)


@dataclass(frozen=True)
class ModelInfo:
    """What the router needs to know about one installed model.

    Mirrors a row of ListenToMe's per-pane model dropdown: the name plus the
    cloud-alias fields from /api/tags, with the family hint derived from the
    name (the part before ':').
    """

    name: str
    remote_host: str | None = None
    remote_model: str | None = None
    capabilities: tuple[str, ...] = ()
    parameter_size: str = ""

    @property
    def family(self) -> str:
        """Family hint from the name, like the dropdown's family grouping."""
        return self.name.split(":", 1)[0].strip().lower() or self.name.strip().lower()


def is_local(model: ModelInfo) -> bool:
    """True when the model is not a cloud alias (no remote fields, no ':cloud' name)."""
    return not model.remote_host and not model.remote_model and ":cloud" not in model.name.lower()


def is_chat_model(model: ModelInfo) -> bool:
    """True when the model can chat (embedding-only models are excluded)."""
    return not model.capabilities or "completion" in model.capabilities


def capability_score(model: ModelInfo) -> float:
    """Capability score: parameter size + boost hints - demote hints.

    Bigger is stronger; the *lowest* score is the fastest pick. Parameter size
    dominates; name hints adjust by ``HINT_WEIGHT`` each.
    """
    params = _parse_params(model.name) or _parse_params(model.parameter_size)
    tokens = _tokens(model.name)
    score = params
    score += sum(HINT_WEIGHT for cue in BOOST_TOKENS if _has_cue(tokens, cue))
    score -= sum(HINT_WEIGHT for cue in DEMOTE_TOKENS if _has_cue(tokens, cue))
    return score


def rank_models(models: "list[ModelInfo]") -> "list[ModelInfo]":
    """Rank models strongest-first (ties broken by name, so order is deterministic)."""
    return sorted(models, key=lambda model: (-capability_score(model), model.name))


#: Curated "good for" hints, mirroring the dropdown hints in ListenToMe.
GOOD_FOR_HINTS: dict[str, str] = {
    "qwen": "fast local notes and multilingual transcripts",
    "glm": "strong general chat and meeting summaries",
    "deepseek": "reasoning-heavy analysis",
    "kimi": "long-context and vision",
    "llama": "dependable general chat",
    "gemma": "compact quick answers",
    "mistral": "compact quick answers",
    "ministral": "compact quick answers",
    "phi": "tiny quick answers",
    "gpt-oss": "balanced open-weight analysis",
    "nomic-embed": "embeddings only - not for chat",
}


def good_for(model: ModelInfo) -> str:
    """The human hint shown next to a model in a dropdown row."""
    for family, hint in GOOD_FOR_HINTS.items():
        if model.family.startswith(family):
            return hint
    return "general chat"


def fetch_models(base_url: str, transport: Transport | None = None) -> "list[ModelInfo]":
    """List installed models via GET /api/tags, through the injectable transport seam."""
    transport = transport or httpx_transport(base_url)
    status, lines = transport("/api/tags", None)
    if status >= 300:
        body = "\n".join(str(line) for line in lines)[:300]
        raise ServerError(f"Ollama returned HTTP {status} for /api/tags: {body.strip()!r}")
    body = "\n".join(str(line) for line in lines)
    try:
        data = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ServerError(f"invalid JSON from /api/tags: {exc}") from exc
    models: list[ModelInfo] = []
    for entry in data.get("models", []):
        details = entry.get("details") or {}
        models.append(
            ModelInfo(
                name=str(entry.get("name", "")),
                remote_host=entry.get("remote_host") or None,
                remote_model=entry.get("remote_model") or None,
                capabilities=tuple(entry.get("capabilities") or ()),
                parameter_size=str(details.get("parameter_size") or ""),
            )
        )
    return models


def role_defaults(models: "list[ModelInfo]", prefer_local: bool = True) -> dict[str, str]:
    """Auto-assign a model per role: Listener/Quick = fastest, Deep = strongest.

    Local-first, mirroring ``ModelRanking.roleDefaults``: ``:cloud`` models
    are filtered out of auto-selection **unless no local model exists** (the
    user set a cloud key, opting in). Returns ``{}`` when no chat model is
    available - callers degrade from there.
    """
    chat_models = [model for model in models if is_chat_model(model)]
    pool = chat_models
    if prefer_local:
        local_models = [model for model in chat_models if is_local(model)]
        if local_models:
            pool = local_models
    if not pool:
        return {}
    ranked = rank_models(pool)
    strongest, fastest = ranked[0], ranked[-1]
    return {"listener": fastest.name, "quick": fastest.name, "deep": strongest.name}