"""Privacy specs - mirrors ModelPrivacyTests.swift.

The contract under test: ``verify_local_model`` fails closed (a cloud alias
served by a local daemon has empty ``details.format`` - a localhost URL or a
model name is not proof), ``assert_host_local`` allows only loopback hosts in
LOCAL mode, and ``guard_request`` combines the checks with truthful labels
(CLOUD bypasses local checks but never lies about what leaves the device).
"""

from __future__ import annotations

import json

import pytest

from conftest import BASE_URL, FakeTransport

from tinycopilot.model_router import ModelInfo
from tinycopilot.ollama_provider import ServerError
from tinycopilot.privacy import (
    PrivacyMode,
    PrivacyViolation,
    assert_host_local,
    guard_request,
    verify_local_model,
)

# Realistic /api/show bodies (shapes captured from an actual Ollama daemon).
LOCAL_SHOW = {
    "name": "qwen3:0.6b",
    "details": {"format": "gguf", "family": "qwen3", "parameter_size": "751.63M"},
    "model_info": {"general.architecture": "qwen3", "qwen3.block_count": 28},
}
CLOUD_ALIAS_SHOW = {
    "details": {"format": "", "parent_model": "glm-5.3"},  # cloud aliases have no format
    "model_info": {"general.architecture": "glm_dsa_moe"},
}

LOCAL_MODEL = ModelInfo(name="qwen3:0.6b")
CLOUD_MODEL = ModelInfo(
    name="glm-5.3:cloud", remote_host="https://ollama.com", remote_model="glm-5.3"
)


def show_transport(show=LOCAL_SHOW, status=200):
    return FakeTransport(status=status, events=[json.dumps(show)])


class TestVerifyLocalModel:
    def test_local_model_with_format_and_model_info_passes(self):
        transport = show_transport()
        ok, reason = verify_local_model(BASE_URL, "qwen3:0.6b", transport=transport)
        assert ok is True
        assert "verified local" in reason
        path, payload = transport.requests[0]
        assert path == "/api/show"
        assert payload == {"model": "qwen3:0.6b"}

    def test_cloud_alias_served_by_a_local_daemon_fails_closed(self):
        # The red-team case: /api/tags shows a "local" daemon, but the alias's
        # own metadata has an empty details.format.
        ok, reason = verify_local_model(BASE_URL, "glm-5.3:cloud", transport=show_transport(CLOUD_ALIAS_SHOW))
        assert ok is False
        assert "details.format" in reason
        assert "fails closed" in reason

    def test_remote_host_in_show_metadata_fails(self):
        show = {"remote_host": "https://ollama.com", "details": {"format": "gguf"}, "model_info": {"a": 1}}
        ok, reason = verify_local_model(BASE_URL, "m", transport=show_transport(show))
        assert ok is False
        assert "cloud alias" in reason
        assert "send the transcript and context off this device" in reason

    def test_remote_model_alone_also_fails(self):
        show = {"remote_model": "glm-5.3", "details": {"format": "gguf"}, "model_info": {"a": 1}}
        ok, _ = verify_local_model(BASE_URL, "m", transport=show_transport(show))
        assert ok is False

    def test_missing_details_fails_closed(self):
        ok, reason = verify_local_model(BASE_URL, "m", transport=show_transport({"model_info": {"a": 1}}))
        assert ok is False
        assert "details.format" in reason

    def test_missing_model_info_fails_closed(self):
        ok, reason = verify_local_model(
            BASE_URL, "m", transport=show_transport({"details": {"format": "gguf"}})
        )
        assert ok is False
        assert "model_info" in reason

    def test_empty_model_info_fails_closed(self):
        show = {"details": {"format": "gguf"}, "model_info": {}}
        ok, _ = verify_local_model(BASE_URL, "m", transport=show_transport(show))
        assert ok is False

    def test_http_error_fails_closed(self):
        ok, reason = verify_local_model(BASE_URL, "m", transport=FakeTransport(status=404, events=[]))
        assert ok is False
        assert "404" in reason

    def test_transport_exception_fails_closed(self):
        def unreachable(path, payload):
            raise ServerError("daemon unreachable")

        ok, reason = verify_local_model(BASE_URL, "m", transport=unreachable)
        assert ok is False
        assert "daemon unreachable" in reason

    def test_invalid_json_fails_closed(self):
        ok, _ = verify_local_model(BASE_URL, "m", transport=FakeTransport(events=["not json"]))
        assert ok is False

    def test_ndjson_show_body_is_merged_and_can_still_pass(self):
        body = [
            json.dumps({"details": {"format": "gguf"}}),
            "",  # blank separator lines are tolerated
            json.dumps({"model_info": {"general.architecture": "qwen3"}}),
        ]
        ok, reason = verify_local_model(BASE_URL, "m", transport=FakeTransport(events=body))
        assert ok is True
        assert "verified local" in reason

    def test_ndjson_show_body_with_a_non_object_chunk_fails_closed(self):
        body = [json.dumps({"details": {"format": "gguf"}}), "[1, 2, 3]"]
        ok, _ = verify_local_model(BASE_URL, "m", transport=FakeTransport(events=body))
        assert ok is False


class TestAssertHostLocal:
    @pytest.mark.parametrize(
        "base_url, host",
        [
            ("http://localhost:11434", "localhost"),
            ("http://127.0.0.1:11434", "127.0.0.1"),
            ("http://[::1]:11434", "::1"),
            ("localhost:11434", "localhost"),  # no scheme: still parsed
            ("http://localhost", "localhost"),
        ],
    )
    def test_loopback_hosts_pass(self, base_url, host):
        assert assert_host_local(base_url) == host

    @pytest.mark.parametrize(
        "base_url",
        [
            "https://ollama.com",
            "http://example.com:11434",
            "http://192.168.1.5:11434",
            "http://127.0.0.2:11434",  # only the three allowlisted loopback names pass
        ],
    )
    def test_anything_else_raises(self, base_url):
        with pytest.raises(PrivacyViolation):
            assert_host_local(base_url)

    def test_the_violation_message_names_the_host(self):
        with pytest.raises(PrivacyViolation, match="example.com"):
            assert_host_local("http://example.com:11434")


class TestGuardRequest:
    def test_off_mode_refuses_every_request(self):
        with pytest.raises(PrivacyViolation, match="off"):
            guard_request(PrivacyMode.OFF, BASE_URL, LOCAL_MODEL)

    def test_local_mode_passes_a_verified_local_model(self):
        transport = show_transport()
        label = guard_request(PrivacyMode.LOCAL, BASE_URL, LOCAL_MODEL, transport=transport)
        assert "stay on this device" in label
        assert "qwen3:0.6b" in label
        # verification happens on every request, mirroring isVerifiedLocal
        assert transport.requests[0][0] == "/api/show"

    def test_local_mode_refuses_a_cloud_alias_before_any_request(self):
        transport = show_transport()
        with pytest.raises(PrivacyViolation) as excinfo:
            guard_request(PrivacyMode.LOCAL, BASE_URL, CLOUD_MODEL, transport=transport)
        assert "cloud alias" in str(excinfo.value)
        assert transport.requests == []

    def test_local_mode_refuses_a_model_that_fails_metadata_verification(self):
        # The registry row looks local, but the daemon's own metadata says otherwise.
        suspicious = ModelInfo(name="looks-local")
        transport = show_transport(CLOUD_ALIAS_SHOW)
        with pytest.raises(PrivacyViolation) as excinfo:
            guard_request(PrivacyMode.LOCAL, BASE_URL, suspicious, transport=transport)
        assert "details.format" in str(excinfo.value)

    def test_local_mode_refuses_a_non_localhost_host(self):
        with pytest.raises(PrivacyViolation, match="loopback"):
            guard_request(
                PrivacyMode.LOCAL, "https://ollama.example.com", LOCAL_MODEL,
                transport=show_transport(),
            )

    def test_cloud_mode_bypasses_local_checks_but_stays_truthful(self):
        transport = show_transport()
        label = guard_request(
            PrivacyMode.CLOUD, "https://ollama.example.com", CLOUD_MODEL, transport=transport
        )
        assert "sends transcript and context off this device" in label
        assert transport.requests == []  # cloud mode does not demand local verification

    def test_cloud_mode_with_a_local_model_stays_truthful(self):
        label = guard_request(PrivacyMode.CLOUD, BASE_URL, LOCAL_MODEL)
        assert "stay on this device" in label

    def test_cloud_mode_at_a_remote_host_is_truthful_about_it(self):
        label = guard_request(PrivacyMode.CLOUD, "https://my-ollama.example.com", LOCAL_MODEL)
        assert "sends transcript and context" in label

    def test_mode_accepts_plain_lowercase_strings(self):
        label = guard_request("local", BASE_URL, LOCAL_MODEL, transport=show_transport())
        assert "stay on this device" in label