#!/usr/bin/env python3
"""TinyCopilot demo - a scripted meeting run through all three roles.

Feeds a multi-turn transcript (You/Others segments, one question that fires a
proactive Quick answer, one that lands inside the debounce window), then runs
LISTENER, QUICK, and DEEP against the models auto-selected by the router,
printing each role's truthful privacy label first.

Usage:
    python3 demo.py [--base-url URL] [--mode auto|off|local|cloud] [--model NAME]

Degrades gracefully: no daemon, no models, or a refused privacy guard each
print a clear message instead of a traceback.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Run from a fresh checkout without installing: put src/ on sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from tinycopilot.conversation_store import ConversationStore, TranscriptSegment
from tinycopilot.copilot import Copilot, CopilotRole
from tinycopilot.model_router import (
    ModelInfo,
    fetch_models,
    good_for,
    is_chat_model,
    is_local,
    role_defaults,
)
from tinycopilot.ollama_provider import LLMError
from tinycopilot.privacy import PrivacyMode, PrivacyViolation, guard_request
from tinycopilot.question_detector import (
    DEFAULT_DEBOUNCE_SECONDS,
    QuestionDetector,
    is_question,
)

DEFAULT_BASE_URL = "http://localhost:11434"
DEFAULT_PERSONA = "a concise, encouraging teaching assistant for a hands-on engineering lab"

#: The scripted meeting: (source, text, is_final).
SCRIPT = [
    ("others", "Morning everyone. Today we are scoping the TinyCopilot lab for Module 2.", True),
    ("you", "Thanks. I reviewed the curriculum notes last night.", True),
    # A question that fires the proactive Quick answer:
    ("others", "Can you walk me through how the conversation store handles partial transcripts?", True),
    # A second question inside the debounce window - deliberately skipped:
    ("others", "Also, what about the privacy module? Do we fail closed when metadata is missing?", True),
    ("others", "Right. And we still need to decide the coverage floor for the lab.", True),
    ("you", "I would say ninety percent to start.", True),
    ("others", "One more thing: the e2e contract test", False),  # a partial...
    ("others", "One more thing: the e2e contract test must stay outside CI.", True),  # ...then its final
]

#: One explicit question per role for the labeled role runs (Listener summarizes).
ROLE_QUESTIONS = {
    CopilotRole.LISTENER: None,
    CopilotRole.QUICK: "Where did we land on the coverage floor?",
    CopilotRole.DEEP: "What risks remain in shipping this lab to students this week?",
}


class ScriptedClock:
    """Injectable clock that advances a fixed step on every read.

    The detector reads the clock only when a question is in play, so with
    step=5.0 the second scripted question lands 5 s after the first - inside
    the 8 s debounce window - making that part of the demo deterministic no
    matter how long the LLM takes.
    """

    def __init__(self, step: float = 5.0) -> None:
        self._step = step
        self._now = 0.0

    def __call__(self) -> float:
        self._now += self._step
        return self._now


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Run the TinyCopilot scripted meeting demo.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL,
                        help=f"Ollama base URL (default: {DEFAULT_BASE_URL})")
    parser.add_argument("--mode", choices=("auto", "off", "local", "cloud"), default="auto",
                        help="privacy mode; 'auto' picks LOCAL when a local chat model exists, else CLOUD")
    parser.add_argument("--model", default=None,
                        help="force one model for every role (skips per-role auto-selection)")
    parser.add_argument("--persona", default=DEFAULT_PERSONA,
                        help="persona guidance threaded into every role's prompt")
    return parser.parse_args(argv)


def resolve_mode(args, chat_models):
    if args.mode != "auto":
        return PrivacyMode(args.mode)
    return PrivacyMode.LOCAL if any(is_local(m) for m in chat_models) else PrivacyMode.CLOUD


def feed_script(copilot: Copilot) -> None:
    print("\n--- Live transcript feed (scripted) ---")
    for i, (source, text, is_final) in enumerate(SCRIPT):
        segment = TranscriptSegment(id=f"s{i}", source=source, text=text, is_final=is_final, ts=float(i))
        kind = "FINAL" if is_final else "partial"
        print(f"\n[{kind:>6}] {segment.speaker_label}: {text}")
        answer = copilot.ingest(segment)
        if answer:
            print(f">>> proactive Quick fired (model {copilot.models['quick']}):\n{answer}")
        elif segment.is_final and segment.source == "others" and is_question(segment.text):
            print(
                f">>> question detected, but the {DEFAULT_DEBOUNCE_SECONDS:g} s debounce window "
                "is still open - skipped (mirrors ListenToMe)"
            )


def run_roles(copilot: Copilot, allowed: dict) -> bool:
    """Run each allowed role once, streaming live. Returns True if any output appeared."""
    produced_any = False
    for role, question in ROLE_QUESTIONS.items():
        print(f"\n{'=' * 66}")
        if role not in allowed:
            print(f"{role.value.upper()} - skipped: its model did not pass the privacy guard")
            continue
        print(f"{role.value.upper()} - model: {copilot.models[role.value]}")
        if question:
            print(f"question: {question}")
        print("-" * 66)
        produced = False
        try:
            for delta in copilot.generate(role, question=question):
                print(delta, end="", flush=True)
                produced = True
            print()
        except LLMError as exc:
            print(f"\n[generation failed] {exc}")
        produced_any = produced_any or produced
    return produced_any


def run_capture_only() -> int:
    """AI is off: capture, transcription, and saving keep working - no AI requests."""
    store = ConversationStore()
    print(f"\nAI is off - no AI requests happen. Capture and transcription continue:")
    for i, (source, text, is_final) in enumerate(SCRIPT):
        segment = TranscriptSegment(id=f"s{i}", source=source, text=text, is_final=is_final, ts=float(i))
        store.apply(segment)
        kind = "FINAL" if is_final else "partial"
        print(f"  [{kind:>6}] {segment.speaker_label}: {text}")
        if segment.is_final and segment.source == "others" and is_question(segment.text):
            print("           (a question was asked - with AI off, no proactive answer is generated)")
    print("\nSaved transcript:")
    print(store.transcript_text())
    return 0


def main(argv=None) -> int:
    args = parse_args(argv)
    print(f"TinyCopilot demo - Ollama at {args.base_url}")

    try:
        models = fetch_models(args.base_url)
    except LLMError as exc:
        print(f"\nCannot reach an Ollama daemon at {args.base_url}:\n  {exc}", file=sys.stderr)
        print("Start one (`ollama serve`) and pull a model (`ollama pull qwen3:0.6b`), then re-run.",
              file=sys.stderr)
        return 1

    if not models:
        print(f"\nThe daemon at {args.base_url} has no models installed.", file=sys.stderr)
        print("Pull one first, e.g.:  ollama pull qwen3:0.6b", file=sys.stderr)
        return 1

    chat_models = [m for m in models if is_chat_model(m)]
    if not chat_models:
        print("\nThe daemon has models, but none of them can chat (embedding-only?).", file=sys.stderr)
        print("Pull a chat model first, e.g.:  ollama pull qwen3:0.6b", file=sys.stderr)
        return 1

    print(f"\nInstalled models ({len(models)}):")
    for m in models:
        kind = "local" if is_local(m) else "CLOUD"
        print(f"  {m.name:<38} [{kind:<5}] good for: {good_for(m)}")

    mode = resolve_mode(args, chat_models)
    print(f"\nPrivacy mode: {mode.value.upper()}")
    if mode is PrivacyMode.OFF:
        return run_capture_only()

    defaults = role_defaults(chat_models)
    allowed: dict = {}
    for role in CopilotRole:
        name = args.model or defaults.get(role.value, "")
        info = next((m for m in models if m.name == name), ModelInfo(name=name))
        try:
            label = guard_request(mode, args.base_url, info)
        except PrivacyViolation as exc:
            print(f"  {role.value:<9} {name or '<no model>':<38} REFUSED: {exc}")
            continue
        print(f"  {role.value:<9} {name:<38} {label}")
        allowed[role] = name

    if not allowed:
        print("\nNo role passed the privacy guard - nothing can run.", file=sys.stderr)
        print("Try `--mode cloud` (explicitly opting in), or pull a local model:  ollama pull qwen3:0.6b",
              file=sys.stderr)
        return 1

    store = ConversationStore()
    detector = QuestionDetector(clock=ScriptedClock())
    copilot = Copilot(args.base_url, store, detector, allowed, persona=args.persona)
    print(f"\nPersona guidance (threaded into every role): {copilot.persona}")
    feed_script(copilot)

    print(f"\n{'=' * 66}\nFinalized transcript (store.transcript_text()):\n{'=' * 66}")
    print(store.transcript_text())

    produced = run_roles(copilot, allowed)
    if not produced:
        print("\nNo role produced output - see the errors above.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())