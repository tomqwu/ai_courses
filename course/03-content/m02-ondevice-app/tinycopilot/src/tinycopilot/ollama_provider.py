"""Streaming chat against an Ollama daemon, with typed fail-closed errors.

Mirrors ``Sources/ListenToMeCore/OllamaProvider.swift`` and its
``OllamaStreamError`` (.server / .incomplete / .empty): NDJSON over
``/api/chat``, in-stream ``{"error": ...}`` events, and typed errors so a
truncated or empty response can never finish as success.

Redirect rejection (``RejectRedirects`` in ListenToMe's URLSession delegate):
the default transport builds its httpx client with ``follow_redirects=False``
and any 3xx response raises ``ServerError`` - meeting text must never be
silently forwarded.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Callable

import httpx


class LLMError(Exception):
    """Base class for every provider failure - no error path finishes as success."""


class ServerError(LLMError):
    """Ollama refused or failed the request (mirrors ``OllamaStreamError.server``)."""


class IncompleteStreamError(LLMError):
    """The stream ended without a done event (mirrors ``OllamaStreamError.incomplete``)."""


class EmptyResponseError(LLMError):
    """The stream finished but produced no visible text (mirrors ``OllamaStreamError.empty``)."""


#: Transport seam (the injectable ``lineSource`` in OllamaProvider.swift):
#: ``transport(path, payload) -> (status, iterator-of-NDJSON-lines)``.
#: ``payload=None`` means GET (used for /api/tags); otherwise POST with JSON.
Transport = Callable[[str, "dict | None"], "tuple[int, Iterator[str]]"]


def httpx_transport(base_url: str, reject_redirects: bool = True, timeout: float = 120.0) -> Transport:
    """Build the real streaming transport over httpx.

    One fresh httpx client per request - a lab trade-off: no connection
    pooling, but the lifetime of every response is explicit. With
    ``reject_redirects=True`` (the default) the client is created with
    ``follow_redirects=False`` and a 3xx is refused: this is the Python twin
    of ListenToMe's ``RejectRedirects`` URLSession delegate.
    """
    base = base_url.rstrip("/")

    def transport(path: str, payload: "dict | None") -> "tuple[int, Iterator[str]]":
        client = httpx.Client(
            base_url=base,
            follow_redirects=not reject_redirects,
            timeout=timeout,
        )
        try:
            if payload is None:
                request = client.build_request("GET", path)
            else:
                request = client.build_request("POST", path, json=payload)
            response = client.send(request, stream=True)
        except httpx.HTTPError as exc:
            client.close()
            raise ServerError(f"cannot reach Ollama at {base}: {exc}") from exc
        if 300 <= response.status_code < 400:
            location = response.headers.get("location", "<unknown>")
            response.close()
            client.close()
            raise ServerError(
                f"refused HTTP {response.status_code} redirect to {location} - "
                "meeting text must never be silently forwarded"
            )
        if response.status_code >= 400:
            body = response.read().decode("utf-8", "replace")[:500]
            response.close()
            client.close()
            raise ServerError(f"Ollama returned HTTP {response.status_code}: {body}")
        def lines() -> Iterator[str]:
            try:
                yield from response.iter_lines()
            finally:
                response.close()
                client.close()
        return response.status_code, lines()

    return transport


class OllamaProvider:
    """One model on one daemon, streaming chat completions as text deltas.

    ``transport`` is the only seam tests need to fake - everything else is the
    real NDJSON protocol: deltas come from ``message.content``, an in-stream
    ``{"error": ...}`` event aborts with ``ServerError``, and a stream that
    ends without ``done`` or without any visible text raises instead of
    pretending the completion succeeded.
    """

    def __init__(
        self,
        base_url: str,
        model: str,
        transport: Transport | None = None,
        reject_redirects: bool = True,
        timeout: float = 120.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.reject_redirects = reject_redirects
        self.timeout = timeout
        self._transport = transport or httpx_transport(self.base_url, reject_redirects, timeout)

    def stream_chat(
        self,
        messages: "list[dict]",
        options: "dict | None" = None,
    ) -> Iterator[str]:
        """Stream one chat completion, yielding visible text deltas.

        Raises (never returns) on failure: ``ServerError`` for HTTP >= 300 or
        an in-stream error event, ``IncompleteStreamError`` when the stream
        ends without ``done``, ``EmptyResponseError`` when nothing visible
        was accumulated. Note the raises happen as you iterate - a generator
        runs its body lazily.
        """
        payload: dict = {"model": self.model, "messages": list(messages), "stream": True}
        if options:
            payload.update(options)
        status, lines = self._transport("/api/chat", payload)
        if 300 <= status < 400:
            raise ServerError(
                f"refused HTTP {status} redirect from {self.base_url} - "
                "meeting text must never be silently forwarded"
            )
        if status >= 400:
            body = "".join(str(line) for line in lines)[:500]
            raise ServerError(
                f"Ollama returned HTTP {status} for model {self.model!r}: {body.strip()!r}"
            )
        chunks: list[str] = []
        saw_done = False
        try:
            for raw_line in lines:
                line = raw_line.strip() if isinstance(raw_line, str) else str(raw_line).strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue  # torn or keep-alive lines are skipped, never mistaken for content
                if not isinstance(event, dict):
                    continue
                if "error" in event:
                    raise ServerError(f"Ollama stream error: {event['error']}")
                if event.get("done"):
                    saw_done = True
                message = event.get("message")
                if isinstance(message, dict):
                    delta = message.get("content")
                    if delta:
                        chunks.append(delta)
                        yield delta
        except LLMError:
            raise
        except Exception as exc:  # the transport died mid-stream (connection reset, ...)
            raise IncompleteStreamError(
                f"connection lost mid-stream for model {self.model!r}: {exc}"
            ) from exc
        if not saw_done:
            raise IncompleteStreamError(f"stream ended without a done event for model {self.model!r}")
        if not "".join(chunks).strip():
            raise EmptyResponseError(f"model {self.model!r} streamed no visible text")