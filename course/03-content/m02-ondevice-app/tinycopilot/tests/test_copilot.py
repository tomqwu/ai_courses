"""Copilot specs with a mock provider - mirrors MeetingSessionTests.

The contract under test: ingest folds segments and fires a proactive Quick
answer only for triggered questions; generation tokens cancel a stale stream
when the model switches mid-flight; only a *completed* listener summary is
injected into Quick/Deep prompts (never the in-flight one); persona and
language thread through every role's system prompt.
"""

from __future__ import annotations

import pytest

from conftest import BASE_URL, FakeClock, FakeTransport, make_chat_events, make_segment

from tinycopilot.conversation_store import ConversationStore
from tinycopilot.copilot import Copilot, CopilotRole
from tinycopilot.question_detector import QuestionDetector


def make_copilot(transport, *, models_by_role=None, clock=None, persona=None, response_language=None):
    store = ConversationStore()
    detector = QuestionDetector(clock=clock or FakeClock())
    models = models_by_role if models_by_role is not None else {
        role: f"model-{role.value}" for role in CopilotRole
    }
    copilot = Copilot(
        BASE_URL,
        store,
        detector,
        models,
        transport=transport,
        persona=persona,
        response_language=response_language,
    )
    return copilot, store, detector


class TestIngest:
    def test_a_question_from_others_fires_a_proactive_quick_answer(self):
        transport = FakeTransport(events=make_chat_events("Store partials", " separately."))
        copilot, store, _ = make_copilot(transport)
        answer = copilot.ingest(
            make_segment("s1", "others", "Can you walk me through the store?", is_final=True)
        )
        assert answer == "Store partials separately."
        path, payload = transport.requests[0]
        assert path == "/api/chat"
        assert payload["model"] == "model-quick"
        assert "No preamble" in payload["messages"][0]["content"]  # the Quick system prompt
        assert "Can you walk me through the store?" in payload["messages"][1]["content"]
        assert len(store.final_segments) == 1  # the segment was folded into the store

    @pytest.mark.parametrize(
        "segment",
        [
            make_segment("s1", "you", "What do you think?", is_final=True),  # own voice
            make_segment("s1", "others", "what about the budg", is_final=False),  # partial
            make_segment("s1", "others", "ok, sounds good", is_final=True),  # not a question
        ],
    )
    def test_no_trigger_means_no_request(self, segment):
        transport = FakeTransport(events=make_chat_events("never used"))
        copilot, _, _ = make_copilot(transport)
        assert copilot.ingest(segment) is None
        assert transport.requests == []

    def test_the_debounce_limits_proactive_answers(self):
        clock = FakeClock()
        transport = FakeTransport(events=make_chat_events("answer"))
        copilot, _, _ = make_copilot(transport, clock=clock)
        first = copilot.ingest(make_segment("s1", "others", "first question?", is_final=True))
        second = copilot.ingest(make_segment("s2", "others", "second question?", is_final=True))
        assert first == "answer"
        assert second is None  # inside the 8 s window
        assert len(transport.requests) == 1


class TestGenerate:
    def test_streams_deltas_for_a_role(self):
        transport = FakeTransport(events=make_chat_events("a", "b"))
        copilot, _, _ = make_copilot(transport)
        assert "".join(copilot.generate(CopilotRole.DEEP, question="risks?")) == "ab"
        assert transport.last_payload["model"] == "model-deep"

    def test_quick_generation_uses_quick_evaluation_options(self):
        # mirrors LLMRequest.Purpose.quickEvaluation: think off, temperature 0
        transport = FakeTransport(events=make_chat_events("ok"))
        copilot, _, _ = make_copilot(transport)
        list(copilot.generate(CopilotRole.QUICK, question="q?"))
        assert transport.last_payload["think"] is False
        assert transport.last_payload["temperature"] == 0.0

    def test_other_roles_leave_thinking_to_the_model(self):
        transport = FakeTransport(events=make_chat_events("ok"))
        copilot, _, _ = make_copilot(transport)
        list(copilot.generate(CopilotRole.LISTENER))
        assert "think" not in transport.last_payload

    def test_a_role_without_a_model_raises(self):
        copilot, _, _ = make_copilot(FakeTransport(), models_by_role={})
        with pytest.raises(ValueError, match="listener"):
            list(copilot.generate(CopilotRole.LISTENER))

    def test_an_unknown_role_string_raises(self):
        copilot, _, _ = make_copilot(FakeTransport())
        with pytest.raises(ValueError, match="unknown copilot role"):
            copilot.set_model("nope", "some-model")

    def test_persona_and_language_thread_into_the_system_prompt(self):
        transport = FakeTransport(events=make_chat_events("ok"))
        copilot, _, _ = make_copilot(
            transport, persona="Socratic tutor", response_language="German"
        )
        list(copilot.generate(CopilotRole.LISTENER))
        system_prompt = transport.last_payload["messages"][0]["content"]
        assert "Socratic tutor" in system_prompt
        assert "Always respond in German." in system_prompt

    def test_context_comes_from_the_store_window(self):
        transport = FakeTransport(events=make_chat_events("ok"))
        copilot, _, _ = make_copilot(transport)
        copilot.ingest(make_segment("s1", "others", "we agreed to ship Friday", is_final=True))
        list(copilot.generate(CopilotRole.QUICK, question="what did we agree?"))
        user_prompt = transport.last_payload["messages"][1]["content"]
        assert "Others: we agreed to ship Friday" in user_prompt


class TestSetModel:
    def test_switching_models_mid_stream_cancels_stale_deltas(self):
        transport = FakeTransport(events=make_chat_events("a", "b", "c", "d"))
        copilot, _, _ = make_copilot(transport)
        stream = copilot.generate(CopilotRole.QUICK, question="q?")
        assert next(stream) == "a"  # the first delta arrives...
        copilot.set_model(CopilotRole.QUICK, "other-model")  # ...then the model changes mid-stream
        assert list(stream) == []  # stale deltas are dropped, never yielded
        assert copilot.providers[CopilotRole.QUICK].model == "other-model"
        # other roles are untouched
        assert copilot.providers[CopilotRole.LISTENER].model == "model-listener"

    def test_a_newer_generation_supersedes_the_older_one(self):
        transport = FakeTransport(events=make_chat_events("a", "b", "c"))
        copilot, _, _ = make_copilot(transport)
        first = copilot.generate(CopilotRole.QUICK, question="q1?")
        assert next(first) == "a"
        second = copilot.generate(CopilotRole.QUICK, question="q2?")  # cancels the first
        assert list(first) == []
        assert list(second) == ["a", "b", "c"]

    def test_models_property_reports_the_configured_models(self):
        copilot, _, _ = make_copilot(FakeTransport())
        assert copilot.models == {
            "listener": "model-listener",
            "quick": "model-quick",
            "deep": "model-deep",
        }
        copilot.set_model("deep", "qwen3:32b")  # plain strings work as roles too
        assert copilot.models["deep"] == "qwen3:32b"


class TestListenerGrounding:
    def test_only_completed_listener_summaries_are_injected(self):
        transport = FakeTransport(
            responses=[(200, make_chat_events("The team decided ", "to ship Friday."))],
            events=make_chat_events("later"),
        )
        copilot, _, _ = make_copilot(transport)

        listener_stream = copilot.generate(CopilotRole.LISTENER)
        next(listener_stream)  # the listener is now in flight with a partial summary
        assert copilot.last_completed_listener_summary is None

        # Quick while the listener streams must NOT see the in-flight summary
        list(copilot.generate(CopilotRole.QUICK, question="q?"))
        quick_prompt = transport.last_payload["messages"][1]["content"]
        assert "ship Friday" not in quick_prompt

        # finishing the listener commits the summary...
        assert list(listener_stream) == ["to ship Friday."]
        assert copilot.last_completed_listener_summary == "The team decided to ship Friday."

        # ...so Quick and Deep now see it, with its grounding marker
        list(copilot.generate(CopilotRole.QUICK, question="q?"))
        quick_prompt = transport.last_payload["messages"][1]["content"]
        assert "Completed listener summary:" in quick_prompt
        assert "The team decided to ship Friday." in quick_prompt
        list(copilot.generate(CopilotRole.DEEP, question="q?"))
        deep_prompt = transport.last_payload["messages"][1]["content"]
        assert "The team decided to ship Friday." in deep_prompt

        # ...but the listener itself never reads its own summary
        list(copilot.generate(CopilotRole.LISTENER))
        listener_prompt = transport.last_payload["messages"][1]["content"]
        assert "The team decided to ship Friday." not in listener_prompt

    def test_a_cancelled_listener_never_commits_a_summary(self):
        transport = FakeTransport(events=make_chat_events("half ", "baked"))
        copilot, _, _ = make_copilot(transport)
        stream = copilot.generate(CopilotRole.LISTENER)
        next(stream)
        copilot.set_model(CopilotRole.LISTENER, "other")  # switch mid-stream
        assert list(stream) == []
        assert copilot.last_completed_listener_summary is None