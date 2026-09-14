#!/usr/bin/env python3
"""Captions: turn timed speech into WebVTT/SRT cues that provably match the approved script.

The contract this module exists to enforce (ported from ai_qe's
`tools/validate_narration.py:53-54`):

    words(captions) == words(manifest transcript) == words(script text)

where `words()` is `re.findall(r"[a-z0-9]+", text.lower())` — so case, punctuation and line
breaks are irrelevant, but a changed/added/dropped *word* is a hard failure. That single
equality is what makes a caption trustworthy: it cannot drift from either the audio or the script.

Two timing sources are supported, and the difference is recorded rather than hidden:

  * ``character-alignment`` — the TTS provider returned a timestamp per character (ElevenLabs
    ``/with-timestamps``). Cue boundaries are exact.
  * ``sentence-measured`` — each sentence was synthesized separately and its real duration
    measured (the local preview provider). Cue boundaries are exact at sentence level and
    distributed proportionally inside a sentence. Labelled approximate because that is what it is.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

# Cue-shaping limits. These are deliberately the same shape ai_qe uses
# (tools/captions_from_alignment.py:87-150): <=42 chars/line, <=2 lines, <=7 s.
MAX_CHARS = 42
MAX_LINES = 2
MAX_SECONDS = 7.0
MIN_SECONDS = 0.8
MIN_CHARS = 24          # a cue shorter than this is not worth breaking for

WORD_RE = re.compile(r"[a-z0-9]+")
SENTENCE_END_RE = re.compile(r"[.!?][\"')\]]*$")

# Abbreviations whose full stop must not end a sentence. Matched as a whole token: an earlier
# version replaced substrings, so "seams." contained "ms." and two sentences silently merged.
ABBREVIATIONS = {"e.g.", "i.e.", "etc.", "vs.", "cf.", "approx.", "no.", "fig.", "dr.", "mr.", "ms."}


def sentence_groups(tokens: list[str]) -> list[list[int]]:
    """Group token indices into sentences. This is THE sentence rule for the whole pipeline.

    The provider measures one duration per sentence and the captioner distributes those durations
    over tokens, so both must agree exactly. When they were implemented separately they disagreed
    (5 sentences vs 6 groups), and the caption timing for the tail of the slide was scrambled.
    """
    spans: list[list[int]] = []
    current: list[int] = []
    for i, token in enumerate(tokens):
        current.append(i)
        if SENTENCE_END_RE.search(token) and token.lower() not in ABBREVIATIONS:
            spans.append(current)
            current = []
    if current:
        spans.append(current)
    return spans


def proportional_sentences(text: str, duration: float) -> list[tuple[float, float]]:
    """Spread a known total duration over sentences by character share.

    Used when the provider gives no per-sentence timing (an external take, or a paid response with
    only character alignment). The result is honest but approximate, which is why callers record
    `caption_method: proportional-generation` rather than claiming an alignment.
    """
    from providers import split_sentences          # local import avoids an import cycle at module load
    sentences = split_sentences(text)
    weights = [max(1, len(s)) for s in sentences]
    total = sum(weights) or 1
    spans, cursor = [], 0.0
    for weight in weights:
        share = duration * weight / total
        spans.append((cursor, cursor + share))
        cursor += share
    return spans


def sentence_texts(text: str) -> list[str]:
    """Split text into sentences using the shared rule."""
    tokens = text.split()
    groups = sentence_groups(tokens)
    return [" ".join(tokens[g[0]:g[-1] + 1]) for g in groups] or [text.strip()]



def words(text: str) -> list[str]:
    """The canonical word sequence used for every equality check."""
    return WORD_RE.findall(text.lower())


def to_clock(seconds: float) -> str:
    """WebVTT timestamp: HH:MM:SS.mmm."""
    ms = max(0, int(round(seconds * 1000)))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def from_clock(value: str) -> float:
    """Parse a WebVTT/SRT timestamp (MM:SS.mmm or HH:MM:SS,mmm). Tolerant of 1-3 decimals."""
    value = value.strip().replace(",", ".")
    if not re.fullmatch(r"(?:\d{1,3}:)?\d{1,2}:\d{1,2}(?:\.\d{1,3})?", value):
        raise ValueError(f"bad timestamp: {value!r}")
    parts = value.split(":")
    seconds = 0.0
    for part in parts:
        seconds = seconds * 60 + float(part)
    return seconds


# ---------------------------------------------------------------- pronunciation

def load_pronunciations(path: Path) -> dict[str, str]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    table = data.get("substitutions", data)
    if not isinstance(table, dict) or not all(isinstance(v, str) for v in table.values()):
        raise ValueError(f"{path}: expected {{'display': 'spoken'}} pairs")
    return table


def spoken_tokens(display_text: str, table: dict[str, str]) -> tuple[str, list[list[int]]]:
    """Return (speakText, spans) where spans[i] lists the spoken-token indices owned by display
    token i. Every spoken token appears in exactly one span, in order, so timing can be mapped back
    to the display token exactly.

    Two rules keep the mapping unambiguous:
      * a single-token key may expand ("Testcontainers" -> "Test containers");
      * a multi-word key must preserve its word count ("REST Assured" -> "Rest Assured"), because a
        phrase that changed length could not be attributed to one display token per spoken token.

    Matching is case-sensitive and phrase-aware (longest key first) and ignores surrounding
    punctuation, so "PostgreSQL," still matches the key "PostgreSQL" and keeps its comma.
    """
    keys = sorted(table, key=lambda k: (-len(k.split()), -len(k)))
    display = display_text.split()
    out: list[str] = []
    spans: list[list[int]] = []
    i = 0
    while i < len(display):
        matched = False
        for key in keys:
            parts = key.split()
            if i + len(parts) > len(display):
                continue
            window = display[i:i + len(parts)]
            if [re.sub(r"^\W+|\W+$", "", w) for w in window] != [re.sub(r"^\W+|\W+$", "", p) for p in parts]:
                continue
            pieces = table[key].split()
            if len(parts) > 1 and len(pieces) != len(parts):
                continue                                   # phrase must preserve word count
            # Preserve the display token's own leading/trailing punctuation around the phrase.
            lead = re.match(r"^\W*", window[0]).group(0)
            trail = re.search(r"\W*$", window[-1]).group(0)
            pieces[0] = lead + pieces[0]
            pieces[-1] = pieces[-1] + trail
            if len(parts) == 1:
                span = list(range(len(out), len(out) + len(pieces)))
                out.extend(pieces)
                spans.append(span)
            else:
                for piece in pieces:
                    spans.append([len(out)])
                    out.append(piece)
            i += len(parts)
            matched = True
            break
        if not matched:
            spans.append([len(out)])
            out.append(display[i])
            i += 1
    return " ".join(out), spans


# ---------------------------------------------------------------- cue shaping

@dataclass
class Cue:
    start: float
    end: float
    text: str

    def as_dict(self) -> dict:
        return {"start": round(self.start, 3), "end": round(self.end, 3), "text": self.text}


@dataclass
class Synthesis:
    """What a provider returns: the audio on disk plus enough timing to build cues."""
    duration: float
    method: str                              # character-alignment | sentence-measured
    sentences: list[tuple[float, float]] = field(default_factory=list)
    tokens: list[tuple[float, float]] | None = None    # per *spoken* token, when available
    receipt: dict = field(default_factory=dict)


def _sentence_spans(tokens: list[str], times: list[tuple[float, float]]) -> list[list[int]]:
    """Deprecated alias for `sentence_groups`; kept so existing tests keep working."""
    return sentence_groups(tokens)


def _wrap(text: str, max_chars: int = MAX_CHARS) -> list[str]:
    """Greedy wrap to at most `max_chars` per line (2 lines max => caller splits long runs)."""
    lines, line = [], ""
    for word in text.split():
        candidate = f"{line} {word}".strip()
        if line and len(candidate) > max_chars:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines


def build_cues(display_text: str, synth: Synthesis, table: dict[str, str] | None = None) -> list[Cue]:
    """Shape a synthesis into cues whose concatenated words equal `display_text` exactly.

    A cue is closed only when the next token would break a hard limit (2 lines, 42 chars/line,
    7 s), so cues stay as close to natural phrase length as the limits allow. Sentence boundaries
    are handled upstream: the preview provider measures one real duration per sentence, so the
    distributed times already follow sentence rhythm.
    """
    table = table or {}
    speak, spans = spoken_tokens(display_text, table)
    display = display_text.split()
    if not display:
        return []

    spoken = speak.split()
    token_times: list[tuple[float, float]] = [(0.0, 0.0)] * len(display)

    if synth.tokens and len(synth.tokens) == len(spoken):
        # One display token may own several spoken tokens; take the span that covers them all.
        for i, group in enumerate(spans):
            starts = [synth.tokens[j][0] for j in group]
            ends = [synth.tokens[j][1] for j in group]
            token_times[i] = (min(starts), max(ends))
    else:
        groups = sentence_groups(spoken)
        # The provider measures one duration per sentence; if it saw a different number of sentences
        # than the text actually contains, every downstream time would be attributed to the wrong
        # words. That is a bug, not a condition to paper over, so refuse to build captions.
        if len(groups) != len(synth.sentences):
            raise ValueError(
                f"provider measured {len(synth.sentences)} sentence(s) but the narrated text has "
                f"{len(groups)}; provider and captioner disagree")
        for index, group in enumerate(groups):
            lo, hi = group[0], group[-1]
            members = [i for i in range(len(display)) if lo <= spans[i][0] <= hi]
            if not members:
                continue
            start, end = synth.sentences[index]
            weights = [max(1, len(display[i])) for i in members]
            total = sum(weights)
            cursor = start
            for i, weight in zip(members, weights):
                share = (end - start) * weight / total
                token_times[i] = (cursor, cursor + share)
                cursor += share
        # Safety net: force non-decreasing, positive durations so a rounding artefact can never
        # produce a backwards cue. Correct input never reaches this branch.
        previous = 0.0
        for i, (start, end) in enumerate(token_times):
            if start < previous or end <= start:
                token_times[i] = (previous, previous + 0.01)
            previous = token_times[i][1]

    cues: list[Cue] = []
    current: list[int] = []

    def flush() -> None:
        cues.append(Cue(token_times[current[0]][0], token_times[current[-1]][1],
                        " ".join(display[j] for j in current)))

    for i, token in enumerate(display):
        if current:
            candidate = " ".join(display[j] for j in current + [i])
            wrapped = _wrap(candidate)
            too_wide = len(wrapped) > MAX_LINES or any(len(line) > MAX_CHARS for line in wrapped)
            too_long = token_times[i][1] - token_times[current[0]][0] > MAX_SECONDS
            if too_wide or too_long:
                flush()
                current = [i]
                continue
        current.append(i)
        # Once a sentence is complete and the cue can stand on its own, end the cue there: a caption
        # that straddles two sentences reads worse than a slightly short one.
        if SENTENCE_END_RE.search(display[i]):
            span = token_times[i][1] - token_times[current[0]][0]
            width = len(" ".join(display[j] for j in current))
            if width >= MIN_CHARS or span >= MIN_SECONDS * 2.5:
                flush()
                current = []
    if current:
        flush()

    # Never emit a sliver: absorb a too-short cue into the previous one — but only if the combined
    # text still wraps inside the line limits. Merging without re-checking produced 2-line cues of up
    # to 97 characters, which is unreadable and breaks the contract.
    merged: list[Cue] = []
    for cue in cues:
        if merged and (cue.end - cue.start) < MIN_SECONDS:
            combined = f"{merged[-1].text} {cue.text}"
            wrapped = _wrap(combined)
            if len(wrapped) <= MAX_LINES and all(len(line) <= MAX_CHARS for line in wrapped):
                merged[-1] = Cue(merged[-1].start, cue.end, combined)
                continue
        merged.append(cue)
    # A short cue that could not be merged keeps its text and gets a readable minimum duration,
    # clamped so it never runs into the next cue.
    for i, cue in enumerate(merged):
        if cue.end - cue.start < MIN_SECONDS:
            wanted = cue.start + MIN_SECONDS
            limit = merged[i + 1].start if i + 1 < len(merged) else synth.duration
            merged[i] = Cue(cue.start, max(cue.end, min(wanted, limit)), cue.text)
    if len(merged) > 1 and (merged[-1].end - merged[-1].start) < MIN_SECONDS:
        combined = f"{merged[-2].text} {merged[-1].text}"
        wrapped = _wrap(combined)
        if len(wrapped) <= MAX_LINES and all(len(line) <= MAX_CHARS for line in wrapped):
            merged[-2] = Cue(merged[-2].start, merged[-1].end, combined)
            merged.pop()
    # Captions are only trustworthy if time moves forward. Assert it here, at the one place every
    # caption file is produced from.
    for i, cue in enumerate(merged):
        if cue.end <= cue.start:
            raise ValueError(f"cue {i} has non-positive duration ({cue.start:.3f}–{cue.end:.3f})")
        if i and cue.start < merged[i - 1].start:
            raise ValueError(f"cue {i} starts before cue {i - 1} — timings are out of order")
    return merged


# ---------------------------------------------------------------- serialisation

def write_vtt(cues: list[Cue], path: Path) -> None:
    body = ["WEBVTT", ""]
    for cue in cues:
        body.append(f"{to_clock(cue.start)} --> {to_clock(cue.end)}")
        body.append(cue.text)
        body.append("")
    Path(path).write_text("\n".join(body), encoding="utf-8")


def write_srt(cues: list[Cue], path: Path) -> None:
    body = []
    for n, cue in enumerate(cues, 1):
        body.append(str(n))
        body.append(f"{to_clock(cue.start).replace('.', ',')} --> {to_clock(cue.end).replace('.', ',')}")
        body.append(cue.text)
        body.append("")
    Path(path).write_text("\n".join(body), encoding="utf-8")


def parse_vtt(text: str) -> list[Cue]:
    """Strict-ish parse mirroring ai_qe's `parseCaptions` (assets/js/narration-media.js:8-25).

    Rejects a file that is not WebVTT and strips markup so cue text is never executable.
    """
    if not re.match(r"^\ufeff?WEBVTT(?:\s|$)", text):
        raise ValueError("not a WebVTT file")
    text = text.lstrip("\ufeff").replace("\r", "")
    cues: list[Cue] = []
    for block in re.split(r"\n\s*\n", text):
        lines = block.split("\n")
        if not lines or re.match(r"^(?:WEBVTT|NOTE|STYLE|REGION)(?:\s|$)", lines[0]):
            continue
        idx = next((i for i, l in enumerate(lines) if "-->" in l), -1)
        if idx < 0:
            continue
        m = re.match(r"^(\S+)\s+-->\s+(\S+)", lines[idx])
        if not m:
            continue
        start, end = from_clock(m.group(1)), from_clock(m.group(2))
        body = " ".join(lines[idx + 1:])
        body = re.sub(r"<[^>]*>", "", body)
        body = (body.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
                    .replace("&nbsp;", " ").replace("&quot;", '"'))
        body = re.sub(r"[ \t]+", " ", body).strip()
        if end > start and body:
            cues.append(Cue(start, end, body))
    if not cues:
        raise ValueError("no cues")
    return sorted(cues, key=lambda c: c.start)


def check_caption_words(cues: list[Cue], expected: str) -> None:
    """Raise unless the cue words equal the expected words exactly."""
    got, want = words(" ".join(c.text for c in cues)), words(expected)
    if got != want:
        for i, (a, b) in enumerate(zip(got, want)):
            if a != b:
                raise ValueError(f"caption/script word mismatch at word {i}: {a!r} != {b!r}")
        raise ValueError(f"caption/script word count mismatch: {len(got)} cues-words vs {len(want)} script-words")
