"""Prompt builder specs - mirrors PromptBuilderTests.swift.

The contract under test: the Listener prompt carries the verbatim
never-invent contract, the Quick prompt is anti-preamble, persona and language
directives are appended to EVERY role, ResponseAction ships >= 6 templated
actions, and every build is deterministic (pure functions, no I/O).
"""

from __future__ import annotations

import pytest

from tinycopilot.copilot import CopilotRole
from tinycopilot.prompts import (
    LISTENER_CONTRACT,
    ResponseAction,
    build_system_prompt,
    build_user_prompt,
)

ALL_ROLES = list(CopilotRole)


class TestBaseSystemPrompts:
    @pytest.mark.parametrize("role", ALL_ROLES)
    def test_every_role_has_a_distinct_base_prompt(self, role):
        assert len({build_system_prompt(r) for r in ALL_ROLES}) == 3

    def test_listener_prompt_carries_the_verbatim_contract(self):
        listener = build_system_prompt(CopilotRole.LISTENER)
        assert LISTENER_CONTRACT in listener
        assert LISTENER_CONTRACT == (
            "Never invent an owner, deadline, agreement, or completion. "
            "Mark missing details as unstated."
        )
        assert listener.count(LISTENER_CONTRACT) == 1  # the constant and prompt cannot drift
        for section in ("Summary", "Decisions", "Actions", "Open questions"):
            assert section in listener  # the four listener sections exist

    def test_quick_prompt_is_anti_preamble(self):
        quick = build_system_prompt(CopilotRole.QUICK)
        assert "No preamble" in quick
        assert "1-3 short sentences" in quick

    def test_deep_prompt_prefers_depth_over_brevity(self):
        assert "depth over brevity" in build_system_prompt(CopilotRole.DEEP)


class TestDirectives:
    @pytest.mark.parametrize("role", ALL_ROLES)
    def test_persona_is_appended_to_every_role(self, role):
        base = build_system_prompt(role)
        with_persona = build_system_prompt(role, persona="Socratic tutor")
        assert "Socratic tutor" in with_persona
        assert "Persona guidance:" in with_persona
        assert with_persona.startswith(base)  # directive appended, base untouched

    @pytest.mark.parametrize("role", ALL_ROLES)
    def test_language_directive_is_appended_to_every_role(self, role):
        prompt = build_system_prompt(role, response_language="German")
        assert "Always respond in German." in prompt

    def test_persona_and_language_stack_in_a_fixed_order(self):
        prompt = build_system_prompt(
            CopilotRole.QUICK, persona="Socratic tutor", response_language="German"
        )
        base = prompt.index(build_system_prompt(CopilotRole.QUICK))
        persona = prompt.index("Persona guidance: Socratic tutor")
        language = prompt.index("Always respond in German.")
        assert base < persona < language

    @pytest.mark.parametrize("role", ALL_ROLES)
    def test_role_accepts_enum_and_lowercase_string(self, role):
        assert build_system_prompt(role) == build_system_prompt(role.value)

    @pytest.mark.parametrize("bad_role", ["unknown", "", "listenerx", 42])
    def test_unknown_role_raises(self, bad_role):
        with pytest.raises(ValueError, match="unknown copilot role"):
            build_system_prompt(bad_role)

    def test_builds_are_deterministic(self):
        first = build_system_prompt(CopilotRole.LISTENER, persona="p", response_language="l")
        second = build_system_prompt(CopilotRole.LISTENER, persona="p", response_language="l")
        assert first == second
        assert build_user_prompt(CopilotRole.DEEP, "ctx", "q?") == build_user_prompt(
            CopilotRole.DEEP, "ctx", "q?"
        )


class TestResponseActions:
    def test_catalog_has_at_least_six_actions(self):
        assert len(ResponseAction) >= 6

    def test_the_six_core_actions_exist(self):
        names = {action.name for action in ResponseAction}
        assert {
            "ANSWER_QUESTION",
            "RECAP",
            "ACTION_ITEMS",
            "CLARIFY",
            "COUNTERPOINT",
            "DRAFT_REPLY",
        } <= names

    @pytest.mark.parametrize("action", list(ResponseAction))
    def test_every_action_has_a_short_instruction(self, action):
        instruction = action.instruction
        assert isinstance(instruction, str)
        assert 10 < len(instruction) < 200

    def test_instructions_are_distinct(self):
        instructions = [action.instruction for action in ResponseAction]
        assert len(set(instructions)) == len(instructions)

    def test_action_items_inherits_the_listener_contract(self):
        assert "Mark missing details as unstated" in ResponseAction.ACTION_ITEMS.instruction


class TestUserPrompt:
    def test_contains_task_question_and_context(self):
        prompt = build_user_prompt(
            CopilotRole.QUICK, "Others: what about the budget?", question="where do we stand?"
        )
        assert prompt.startswith("Task: Answer the question below")
        assert 'Question: "where do we stand?"' in prompt
        assert "Others: what about the budget?" in prompt

    def test_default_task_per_role_without_a_question(self):
        assert build_user_prompt(CopilotRole.QUICK, "ctx").startswith(
            "Task: Answer the user's request using the conversation context."
        )
        assert build_user_prompt(CopilotRole.LISTENER, "ctx").startswith(
            "Task: Summarize the conversation so far."
        )
        assert build_user_prompt(CopilotRole.DEEP, "ctx").startswith(
            "Task: Analyze the conversation in depth."
        )

    def test_an_action_overrides_the_task_line(self):
        prompt = build_user_prompt(CopilotRole.QUICK, "ctx", action=ResponseAction.RECAP)
        assert prompt.startswith(f"Task: {ResponseAction.RECAP.instruction}")

    def test_empty_context_gets_a_placeholder(self):
        assert "(no transcript yet)" in build_user_prompt(CopilotRole.QUICK, "   ")

    def test_unknown_role_raises(self):
        with pytest.raises(ValueError, match="unknown copilot role"):
            build_user_prompt("nope", "ctx")