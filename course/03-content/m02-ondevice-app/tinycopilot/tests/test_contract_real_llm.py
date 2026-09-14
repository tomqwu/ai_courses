"""The real-LLM contract test - mirrors OllamaContractE2ETests.swift (``make e2e``).

CI can't reach an Ollama daemon, so this file is skipped unless LAB_E2E=1 is
set. It is a *contract* test, not a privacy test: it runs against whatever
model the router auto-selects - including ``:cloud`` aliases on a cloud-only
daemon, which is fine here because the point is only to prove the streaming
contract holds against the real daemon.
"""

from __future__ import annotations

import os

import pytest

from tinycopilot.model_router import fetch_models, role_defaults
from tinycopilot.ollama_provider import OllamaProvider

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.skipif(
        not os.environ.get("LAB_E2E"),
        reason="set LAB_E2E=1 to run the real-LLM contract test against a running Ollama daemon",
    ),
]

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")


def test_the_router_finds_chat_models_on_the_daemon():
    models = fetch_models(OLLAMA_BASE_URL)
    assert models, "the daemon has no models installed"
    defaults = role_defaults(models)
    assert defaults, "the daemon has models, but none that can chat"
    assert set(defaults) == {"listener", "quick", "deep"}


def test_a_real_streaming_completion_keeps_the_contract():
    models = fetch_models(OLLAMA_BASE_URL)
    model = role_defaults(models).get("quick") or models[0].name
    provider = OllamaProvider(OLLAMA_BASE_URL, model)
    deltas = list(
        provider.stream_chat(
            [{"role": "user", "content": "Reply with exactly: PONG"}],
            options={"think": False, "temperature": 0.0},
        )
    )
    assert deltas, "the stream produced no deltas"
    text = "".join(deltas).strip()
    assert text, "the completion was empty"
    assert "PONG" in text.upper(), f"expected PONG in the reply, got: {text!r}"