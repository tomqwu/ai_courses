"""ModelRouter specs - mirrors ModelRankingTests.swift.

The contract under test: token-prefix matching ('gemini' is not demoted as
'mini'), parameter-size parsing, boost/demote weights, /api/tags discovery
through the transport seam, and local-first role defaults that fall back to
cloud only when no local model exists.
"""

from __future__ import annotations

import json

import pytest

from conftest import BASE_URL, FakeTransport

from tinycopilot.model_router import (
    ModelInfo,
    capability_score,
    fetch_models,
    good_for,
    is_chat_model,
    is_local,
    rank_models,
    role_defaults,
)
from tinycopilot.ollama_provider import ServerError

TAGS_BODY = {
    "models": [
        {
            "name": "qwen3:0.6b",
            "details": {"format": "gguf", "parameter_size": "751.63M"},
            "capabilities": ["completion", "thinking"],
        },
        {
            "name": "glm-5.3:cloud",
            "remote_host": "https://ollama.com",
            "remote_model": "glm-5.3",
            "details": {"format": "", "parameter_size": "753B"},
            "capabilities": ["completion"],
        },
    ]
}


def model(name, **kwargs):
    return ModelInfo(name=name, **kwargs)


class TestFetchModels:
    def test_parses_tags_entries(self):
        transport = FakeTransport(events=[json.dumps(TAGS_BODY)])
        models = fetch_models(BASE_URL, transport=transport)
        path, payload = transport.requests[0]
        assert path == "/api/tags"
        assert payload is None  # a GET, not a POST
        assert [m.name for m in models] == ["qwen3:0.6b", "glm-5.3:cloud"]
        qwen, glm = models
        assert is_local(qwen) is True
        assert qwen.capabilities == ("completion", "thinking")
        assert qwen.parameter_size == "751.63M"
        assert qwen.family == "qwen3"
        assert is_local(glm) is False
        assert glm.remote_host == "https://ollama.com"
        assert glm.remote_model == "glm-5.3"

    def test_http_error_raises(self):
        with pytest.raises(ServerError):
            fetch_models(BASE_URL, transport=FakeTransport(status=500, events=[]))

    def test_invalid_json_raises(self):
        with pytest.raises(ServerError):
            fetch_models(BASE_URL, transport=FakeTransport(events=["{oops"]))

    def test_the_real_httpx_transport_uses_get_for_tags(self, monkeypatch):
        calls = []

        class FakeResponse:
            status_code = 200
            headers = {}

            def read(self):
                return b""

            def iter_lines(self):
                yield json.dumps(TAGS_BODY)

            def close(self):
                pass

        class FakeClient:
            def __init__(self, **kwargs):
                pass

            def build_request(self, method, path, json=None):
                calls.append((method, path, json))
                return (method, path, json)

            def send(self, request, stream=False):
                return FakeResponse()

            def close(self):
                pass

        monkeypatch.setattr("httpx.Client", FakeClient)
        assert [m.name for m in fetch_models(BASE_URL)] == ["qwen3:0.6b", "glm-5.3:cloud"]
        assert calls[0][0] == "GET"
        assert calls[0][1] == "/api/tags"


class TestIsLocal:
    def test_plain_model_is_local(self):
        assert is_local(model("qwen3:0.6b")) is True

    @pytest.mark.parametrize("name", ["glm-5.3:cloud", "deepseek-v4-pro:cloud"])
    def test_cloud_alias_names_are_not_local(self, name):
        assert is_local(model(name)) is False

    def test_remote_metadata_is_not_local(self):
        assert is_local(model("my-model", remote_host="https://ollama.com")) is False
        assert is_local(model("my-model", remote_model="glm-5.3")) is False


class TestIsChatModel:
    def test_completion_capability_is_chat(self):
        assert is_chat_model(model("qwen3:0.6b", capabilities=("completion",))) is True

    def test_embedding_only_is_not_chat(self):
        assert is_chat_model(model("nomic-embed-text:latest", capabilities=("embedding",))) is False

    def test_unknown_capabilities_default_to_chat(self):
        assert is_chat_model(model("mystery-model")) is True


class TestCapabilityScore:
    @pytest.mark.parametrize(
        "name, params",
        [
            ("qwen3:0.6b", 0.6),
            ("llama3:70b", 70.0),
            ("deepseek-r1:1.5t", 1500.0),
            ("qwen3.6:35b-a3b-coding-mxfp4", 35.0),  # the '3.6' must not parse as a size
            ("qwen3", 0.0),  # a bare version number is not a parameter size
        ],
    )
    def test_parameter_size_comes_from_the_name(self, name, params):
        assert capability_score(model(name)) == pytest.approx(params)

    def test_parameter_size_falls_back_to_tags_metadata(self):
        assert capability_score(model("mystery", parameter_size="753B")) == pytest.approx(753.0)
        # the name wins when both state a size
        assert capability_score(model("qwen3:0.6b", parameter_size="753B")) == pytest.approx(0.6)

    @pytest.mark.parametrize(
        "name",
        [
            "deepseek-v4-pro:32b",
            "qwen3-max:32b",
            "qwen3-coder:32b",
            "deepseek-r1-reasoner:32b",
        ],
    )
    def test_boost_tokens_raise_the_score(self, name):
        assert capability_score(model(name)) == pytest.approx(52.0)

    @pytest.mark.parametrize(
        "name",
        ["deepseek-v4-flash:32b", "gemma-mini:32b", "glm-lite:32b", "llama-small:32b"],
    )
    def test_demote_tokens_lower_the_score(self, name):
        assert capability_score(model(name)) == pytest.approx(12.0)

    def test_gemini_is_not_demoted_as_mini(self):
        # token-prefix matching: 'gemini' merely *contains* 'mini'
        assert capability_score(model("gemini-2.0:12b")) == pytest.approx(12.0)
        assert capability_score(model("gemma-mini:12b")) == pytest.approx(-8.0)
        ranked = rank_models([model("gemma-mini:12b"), model("gemini-2.0:12b")])
        assert ranked[0].name == "gemini-2.0:12b"


class TestRankModels:
    def test_ranks_strongest_first(self):
        ranked = rank_models(
            [
                model("qwen3:0.6b"),
                model("deepseek-v4-flash:32b"),
                model("deepseek-v4-pro:32b"),
            ]
        )
        assert [m.name for m in ranked] == [
            "deepseek-v4-pro:32b",
            "deepseek-v4-flash:32b",
            "qwen3:0.6b",
        ]

    def test_ties_break_by_name_for_determinism(self):
        assert [m.name for m in rank_models([model("b-model"), model("a-model")])] == [
            "a-model",
            "b-model",
        ]

    def test_does_not_mutate_the_input(self):
        models = [model("qwen3:0.6b"), model("llama3:70b")]
        ranked = rank_models(models)
        assert ranked is not models
        assert models[0].name == "qwen3:0.6b"

    def test_empty_input_ranks_empty(self):
        assert rank_models([]) == []


class TestRoleDefaults:
    def test_mixed_list_stays_local_first(self):
        models = [
            model("qwen3:0.6b"),
            model("qwen3:32b"),
            model(
                "kimi-k3:cloud",
                remote_host="https://ollama.com",
                remote_model="kimi-k3",
                parameter_size="2.81T",
            ),
        ]
        assert role_defaults(models) == {
            "listener": "qwen3:0.6b",
            "quick": "qwen3:0.6b",
            "deep": "qwen3:32b",
        }

    def test_local_only_list(self):
        models = [model("qwen3:0.6b"), model("llama3:70b")]
        assert role_defaults(models) == {
            "listener": "qwen3:0.6b",
            "quick": "qwen3:0.6b",
            "deep": "llama3:70b",
        }

    def test_cloud_only_list_falls_back_to_cloud(self):
        models = [
            model("glm-5.3:cloud", remote_host="https://ollama.com", remote_model="glm-5.3"),
            model(
                "deepseek-v4-pro:cloud",
                remote_host="https://ollama.com",
                remote_model="deepseek-v4-pro",
            ),
        ]
        defaults = role_defaults(models)
        assert defaults["deep"] == "deepseek-v4-pro:cloud"  # the pro boost wins
        assert defaults["quick"] == "glm-5.3:cloud"  # lowest score = fastest pick

    def test_empty_list_yields_no_defaults(self):
        assert role_defaults([]) == {}

    def test_a_single_model_serves_every_role(self):
        defaults = role_defaults([model("qwen3:0.6b")])
        assert defaults == {"listener": "qwen3:0.6b", "quick": "qwen3:0.6b", "deep": "qwen3:0.6b"}

    def test_embedding_models_are_never_auto_picked(self):
        models = [
            model("nomic-embed-text:latest", capabilities=("embedding",)),
            model("qwen3:0.6b", capabilities=("completion",)),
        ]
        assert set(role_defaults(models).values()) == {"qwen3:0.6b"}

    def test_an_embedding_only_daemon_yields_no_defaults(self):
        only_embed = [model("nomic-embed-text:latest", capabilities=("embedding",))]
        assert role_defaults(only_embed) == {}

    def test_prefer_local_false_lets_cloud_win(self):
        models = [
            model("qwen3:0.6b"),
            model(
                "kimi-k3:cloud",
                remote_host="https://ollama.com",
                remote_model="kimi-k3",
                parameter_size="2.81T",
            ),
        ]
        assert role_defaults(models, prefer_local=False)["deep"] == "kimi-k3:cloud"


class TestGoodForHints:
    def test_family_hint_comes_from_the_name(self):
        assert model("glm-5.3:cloud").family == "glm-5.3"
        assert model("qwen3:0.6b").family == "qwen3"

    def test_hints_for_known_and_unknown_families(self):
        assert "fast local notes" in good_for(model("qwen3:0.6b"))
        assert "strong general chat" in good_for(model("glm-5.3:cloud"))
        assert good_for(model("totally-unknown-family")) == "general chat"