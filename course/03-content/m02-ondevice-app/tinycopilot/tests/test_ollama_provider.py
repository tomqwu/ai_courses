"""OllamaProvider specs with a fake transport - mirrors OllamaProviderTests.

The contract under test: NDJSON deltas stream, in-stream ``{"error": ...}``
events raise ServerError, truncated streams raise IncompleteStreamError,
empty/whitespace streams raise EmptyResponseError, 3xx redirects are refused,
and the default httpx transport is built with follow_redirects=False. No
error path may ever finish as success.
"""

from __future__ import annotations

import json

import httpx
import pytest

from conftest import BASE_URL, FakeTransport, make_chat_events

from tinycopilot.ollama_provider import (
    EmptyResponseError,
    IncompleteStreamError,
    LLMError,
    OllamaProvider,
    ServerError,
)

MESSAGES = [{"role": "user", "content": "ping"}]


def make_provider(transport, model="test-model", **kwargs):
    return OllamaProvider(BASE_URL, model, transport=transport, **kwargs)


class TestHappyPath:
    def test_streams_deltas_and_finishes_clean(self):
        transport = FakeTransport(events=make_chat_events("Hel", "lo ", "world"))
        assert list(make_provider(transport).stream_chat(MESSAGES)) == ["Hel", "lo ", "world"]

    def test_request_shape_matches_the_ollama_chat_api(self):
        transport = FakeTransport(events=make_chat_events("ok"))
        list(make_provider(transport).stream_chat(MESSAGES, options={"think": False}))
        path, payload = transport.requests[0]
        assert path == "/api/chat"
        assert payload["model"] == "test-model"
        assert payload["messages"] == MESSAGES
        assert payload["stream"] is True
        assert payload["think"] is False

    def test_options_merge_into_the_payload(self):
        transport = FakeTransport(events=make_chat_events("ok"))
        list(make_provider(transport).stream_chat(MESSAGES, options={"temperature": 0.0}))
        assert transport.last_payload["temperature"] == 0.0

    def test_blank_and_malformed_lines_are_ignored(self):
        raw = [
            "",
            "not json at all",
            "[1, 2, 3]",  # valid JSON, but not a chat event object
            json.dumps({"message": {"content": "ok"}, "done": False}),
            json.dumps({"done": True}),
        ]
        transport = FakeTransport(events=raw)
        assert list(make_provider(transport).stream_chat(MESSAGES)) == ["ok"]

    def test_the_final_done_line_carries_no_content(self):
        # Real Ollama ends with {"done": true, ...} and no message - it must yield nothing.
        events = make_chat_events("PONG")
        assert events[-1] == {"model": "m", "done": True, "done_reason": "stop"}
        transport = FakeTransport(events=events)
        assert list(make_provider(transport).stream_chat(MESSAGES)) == ["PONG"]


class TestTypedErrors:
    def test_in_stream_error_event_raises_server_error(self):
        transport = FakeTransport(events=[{"error": "model not found"}])
        with pytest.raises(ServerError, match="model not found"):
            list(make_provider(transport).stream_chat(MESSAGES))

    def test_http_500_raises_server_error(self):
        transport = FakeTransport(status=500, events=[json.dumps({"error": "boom"})])
        with pytest.raises(ServerError, match="500"):
            list(make_provider(transport).stream_chat(MESSAGES))

    def test_http_302_redirect_is_refused(self):
        transport = FakeTransport(status=302, events=[])
        with pytest.raises(ServerError, match="redirect"):
            list(make_provider(transport).stream_chat(MESSAGES))

    def test_stream_without_done_event_is_incomplete(self):
        transport = FakeTransport(events=make_chat_events("partial", done=False))
        with pytest.raises(IncompleteStreamError):
            list(make_provider(transport).stream_chat(MESSAGES))

    def test_transport_dying_mid_stream_is_incomplete(self):
        def transport(path, payload):
            def lines():
                yield json.dumps({"message": {"content": "a"}, "done": False})
                raise RuntimeError("connection reset by peer")

            return 200, lines()

        provider = OllamaProvider(BASE_URL, "m", transport=transport)
        with pytest.raises(IncompleteStreamError, match="connection lost"):
            list(provider.stream_chat(MESSAGES))

    def test_empty_stream_raises_empty_response_error(self):
        transport = FakeTransport(
            events=[{"message": {"content": ""}, "done": False}, {"done": True}]
        )
        with pytest.raises(EmptyResponseError):
            list(make_provider(transport).stream_chat(MESSAGES))

    def test_whitespace_only_stream_raises_empty_response_error(self):
        transport = FakeTransport(events=make_chat_events(" ", "  "))
        with pytest.raises(EmptyResponseError):
            list(make_provider(transport).stream_chat(MESSAGES))

    def test_every_error_type_is_an_llm_error(self):
        for error in (ServerError, IncompleteStreamError, EmptyResponseError):
            assert issubclass(error, LLMError)


class TestRealHttpxTransport:
    """The default transport, tested by monkeypatching httpx.Client - no network."""

    @staticmethod
    def _install_fake_httpx(monkeypatch, *, status=200, lines=None, send_error=None):
        captured = {}

        class FakeResponse:
            def __init__(self):
                self.status_code = status
                self.headers = (
                    {"location": "https://evil.example.com/leak"} if status == 302 else {}
                )

            def read(self):
                return b'{"error": "nope"}'

            def iter_lines(self):
                for line in lines or []:
                    yield line

            def close(self):
                pass

        class FakeClient:
            def __init__(self, **kwargs):
                captured.update(kwargs)

            def build_request(self, method, path, json=None):
                return (method, path, json)

            def send(self, request, stream=False):
                assert stream is True, "the default transport must stream"
                if send_error is not None:
                    raise send_error
                return FakeResponse()

            def close(self):
                pass

        monkeypatch.setattr(httpx, "Client", FakeClient)
        return captured

    def test_default_transport_streams_with_follow_redirects_false(self, monkeypatch):
        captured = self._install_fake_httpx(
            monkeypatch,
            lines=[
                json.dumps({"message": {"content": "ok"}, "done": False}),
                json.dumps({"done": True}),
            ],
        )
        provider = OllamaProvider(BASE_URL, "m")
        assert provider.reject_redirects is True  # mirrors RejectRedirects
        assert list(provider.stream_chat(MESSAGES)) == ["ok"]
        assert captured["follow_redirects"] is False
        assert captured["base_url"] == BASE_URL

    def test_default_transport_refuses_a_3xx(self, monkeypatch):
        self._install_fake_httpx(monkeypatch, status=302)
        provider = OllamaProvider(BASE_URL, "m")
        with pytest.raises(ServerError, match="redirect"):
            list(provider.stream_chat(MESSAGES))

    def test_default_transport_wraps_connection_errors(self, monkeypatch):
        self._install_fake_httpx(monkeypatch, send_error=httpx.ConnectError("refused"))
        provider = OllamaProvider(BASE_URL, "m")
        with pytest.raises(ServerError, match="cannot reach"):
            list(provider.stream_chat(MESSAGES))

    def test_default_transport_surfaces_http_500(self, monkeypatch):
        self._install_fake_httpx(monkeypatch, status=500)
        provider = OllamaProvider(BASE_URL, "m")
        with pytest.raises(ServerError, match="500"):
            list(provider.stream_chat(MESSAGES))

    def test_mid_stream_httpx_error_is_incomplete(self, monkeypatch):
        class ExplodingResponse:
            status_code = 200
            headers = {}

            def read(self):
                return b""

            def iter_lines(self):
                yield json.dumps({"message": {"content": "a"}, "done": False})
                raise httpx.ReadError("socket vanished")

            def close(self):
                pass

        class FakeClient:
            def __init__(self, **kwargs):
                pass

            def build_request(self, method, path, json=None):
                return (method, path, json)

            def send(self, request, stream=False):
                return ExplodingResponse()

            def close(self):
                pass

        monkeypatch.setattr(httpx, "Client", FakeClient)
        provider = OllamaProvider(BASE_URL, "m")
        with pytest.raises(IncompleteStreamError, match="connection lost"):
            list(provider.stream_chat(MESSAGES))