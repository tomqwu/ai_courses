"""Fail-closed privacy modes: verified-local models, loopback-only hosts, truthful labels.

Mirrors ``Sources/ListenToMeCore/ModelPrivacy.swift`` (``isVerifiedLocal``),
``AIProcessingMode.swift`` (off / local / cloud), and the localhost-host
enforcement plus ``RejectRedirects`` behavior in ``OllamaProvider.swift``.

The threat model this module defends against: a *local* daemon can serve
cloud-backed aliases, so a localhost URL or a model's name is never proof of
localness - only the daemon's own metadata, verified on every request, is.
"""

from __future__ import annotations

import json
from enum import Enum
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from .ollama_provider import Transport, httpx_transport

if TYPE_CHECKING:  # pragma: no cover - exists only for type checkers (no runtime cycle)
    from .model_router import ModelInfo

#: The only hosts LOCAL mode trusts (ListenToMe's loopback allowlist).
LOCAL_HOSTS = frozenset({"localhost", "127.0.0.1", "::1"})


class PrivacyMode(Enum):
    """The three-way mode switch, mirroring ``AIProcessingMode``.

    Adding a cloud key never switches modes by itself - the user's explicit
    choice does.
    """

    OFF = "off"
    LOCAL = "local"
    CLOUD = "cloud"


class PrivacyViolation(Exception):
    """A request would break the mode's data-flow promise. Raised, never logged."""


def _as_mode(mode: "PrivacyMode | str") -> PrivacyMode:
    if isinstance(mode, PrivacyMode):
        return mode
    return PrivacyMode(str(mode).strip().lower())


def _host_of(base_url: str) -> str:
    """Extract the lowercase hostname from a base URL (bare 'localhost:11434' works too)."""
    url = base_url if "://" in base_url else f"http://{base_url}"
    return (urlparse(url).hostname or "").lower()


def assert_host_local(base_url: str) -> str:
    """Require a loopback host and return it; anything else is a violation.

    Mirrors the LOCAL-mode host enforcement in OllamaProvider.swift: in
    local-only mode the provider additionally requires the host to be
    localhost, 127.0.0.1, or ::1.
    """
    host = _host_of(base_url)
    if host not in LOCAL_HOSTS:
        raise PrivacyViolation(
            f"LOCAL mode requires a loopback Ollama host (localhost, 127.0.0.1, or ::1); "
            f"got {host!r} from {base_url!r}"
        )
    return host


def _parse_show_body(body: str) -> "dict | None":
    """Parse /api/show output: one JSON object, or NDJSON objects merged into one dict."""
    try:
        data = json.loads(body)
        return data if isinstance(data, dict) else None
    except json.JSONDecodeError:
        merged: dict = {}
        for line in body.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                chunk = json.loads(line)
            except json.JSONDecodeError:
                return None
            if not isinstance(chunk, dict):
                return None
            merged.update(chunk)
        return merged or None


def verify_local_model(base_url: str, name: str, transport: Transport | None = None) -> tuple[bool, str]:
    """Fail-closed verification of a model's /api/show metadata.

    Mirrors ``ModelPrivacy.isVerifiedLocal``: returns ``(True, reason)`` only
    when ``remote_host``/``remote_model`` are absent, ``details.format`` is
    non-empty, and ``model_info`` is non-empty. Every failure - unreachable
    daemon, bad status, unparsable body, missing metadata - fails closed with
    a truthful reason.
    """
    transport = transport or httpx_transport(base_url)
    try:
        status, lines = transport("/api/show", {"model": name})
        body = "\n".join(str(line) for line in lines)
    except Exception as exc:  # includes LLMError raised by the transport seam
        return False, f"cannot verify {name!r} against {base_url}: {exc}"
    if status != 200:
        return False, f"Ollama returned HTTP {status} for /api/show of {name!r}"
    info = _parse_show_body(body)
    if info is None:
        return False, f"invalid JSON from /api/show for {name!r}"
    remote_host = info.get("remote_host")
    remote_model = info.get("remote_model")
    if remote_host or remote_model:
        return False, (
            f"{name!r} is a cloud alias (remote_host={remote_host!r}, "
            f"remote_model={remote_model!r}); using it would send the transcript "
            "and context off this device"
        )
    details = info.get("details")
    model_format = details.get("format") if isinstance(details, dict) else None
    if not model_format:
        return False, (
            f"{name!r} has no details.format metadata - a model's name or a localhost "
            "URL is not proof it is local (a local daemon can serve cloud aliases), "
            "so this fails closed"
        )
    model_info = info.get("model_info")
    if not model_info:
        return False, f"{name!r} has no model_info metadata; cannot prove it is local, so this fails closed"
    return True, (
        f"verified local: format={model_format!r}, {len(model_info)} model_info keys, "
        "no remote_host or remote_model"
    )


def guard_request(
    mode: "PrivacyMode | str",
    base_url: str,
    model_info: "ModelInfo",
    transport: Transport | None = None,
) -> str:
    """Gate one request on the mode's promise, returning its truthful label.

    - OFF: no AI request may happen at all - capture and transcription keep working.
    - LOCAL: loopback host + fail-closed metadata verification, on every request.
    - CLOUD: the local-only checks are bypassed (the user opted in), but the
      label stays truthful about what leaves the device.

    Raises ``PrivacyViolation`` instead of returning a scary string - a
    refused request must be impossible to mistake for a permitted one.
    """
    mode = _as_mode(mode)
    if mode is PrivacyMode.OFF:
        raise PrivacyViolation(
            "AI is off: no transcript or context is sent anywhere. "
            "Capture, transcription, and saving keep working without AI."
        )
    if mode is PrivacyMode.LOCAL:
        if model_info.remote_host or model_info.remote_model:
            raise PrivacyViolation(
                f"LOCAL mode refuses model {model_info.name!r}: it is a cloud alias "
                f"(remote_host={model_info.remote_host!r}) - it would send the "
                "transcript and context off this device"
            )
        host = assert_host_local(base_url)
        ok, reason = verify_local_model(base_url, model_info.name, transport=transport)
        if not ok:
            raise PrivacyViolation(f"LOCAL mode refuses model {model_info.name!r}: {reason}")
        return (
            f"LOCAL model {model_info.name!r} on {host}: "
            "transcript and context stay on this device."
        )
    # CLOUD: bypass the local-only checks, keep the label truthful.
    if model_info.remote_host or model_info.remote_model:
        return (
            f"Ollama Cloud model {model_info.name!r} via {model_info.remote_host}: "
            "sends transcript and context off this device."
        )
    host = _host_of(base_url)
    if host in LOCAL_HOSTS:
        return (
            f"CLOUD mode with local model {model_info.name!r} on {host}: "
            "transcript and context stay on this device."
        )
    return (
        f"CLOUD mode: model {model_info.name!r} at {base_url} - "
        "sends transcript and context to that host."
    )