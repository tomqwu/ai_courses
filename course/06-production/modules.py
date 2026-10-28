# course/06-production/modules.py
"""The course's modules, in one place (#ladder).

Every list of modules in the build, the gate and the site reads this: the deep modules M0–M9
(the verified engineering course) and the beginner ladder L0–L5 (for non-coders, linking into the
deep modules). Order is outline order. A module is registered here and nowhere else.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

CONTENT = Path(__file__).resolve().parents[1] / "03-content"
ID_RE = re.compile(r"^([ml])(\d+)$")
TAG = r"[ML]\d+"
SEG = r"[ML]\d+\.\d+"


@dataclass(frozen=True)
class Module:
    id: str
    folder: str
    family: str                 # "deep" (M0–M9) or "ladder" (L0–L5)
    outline_en: str
    outline_zh: str
    segments: tuple[int, int] = (3, 3)   # teaching segments allowed (min, max)
    quiz: tuple[int, int] = (8, 8)       # knowledge-check questions allowed (min, max)
    figures: bool = True                 # held to the figures coverage rule


def _deep(mid, folder, en, zh):
    return Module(mid, folder, "deep", en, zh)


MODULES: list[Module] = [
    _deep("m00", "m00-orientation", "Orientation", "导览"),
    _deep("m01", "m01-operating-system", "The operating system", "操作系统"),
    _deep("m02", "m02-ondevice-app", "On-device: architecture", "端侧：架构"),
    _deep("m03", "m03-privacy-ship", "On-device: privacy & shipping", "端侧：隐私与发布"),
    _deep("m04", "m04-spec-driven-saas", "Spec-driven SaaS", "规格驱动 SaaS"),
    _deep("m05", "m05-security-tests", "Multi-tenant security", "多租户安全"),
    _deep("m06", "m06-expertise-product", "The expertise product", "专业知识产品"),
    _deep("m07", "m07-monetize", "Monetize", "变现"),
    _deep("m08", "m08-launch-capstone", "Launch & capstone", "发布与毕业项目"),
    _deep("m09", "m09-github-pages", "Ship with GitHub Pages", "用 GitHub Pages 发布"),
]
IDS = [m.id for m in MODULES]
_BY_ID = {m.id: m for m in MODULES}


def get(module_id: str) -> Module:
    return _BY_ID[module_id]


def _parts(module_id: str) -> tuple[str, int]:
    m = ID_RE.match(module_id)
    if not m:
        raise ValueError(f"not a module id: {module_id!r}")
    return m.group(1), int(m.group(2))


def tag(module_id: str) -> str:
    prefix, n = _parts(module_id)
    return f"{prefix.upper()}{n}"


def number(module_id: str) -> int:
    return _parts(module_id)[1]


def family(module_id: str) -> str:
    return "ladder" if _parts(module_id)[0] == "l" else "deep"


def next_id(module_id: str) -> str | None:
    same = [m.id for m in MODULES if m.family == family(module_id)]
    i = same.index(module_id)
    return same[i + 1] if i + 1 < len(same) else None


def kicker(module_id: str, lang: str = "en") -> str:
    n = number(module_id)
    if family(module_id) == "ladder":
        return f"阶梯第 {n} 级" if lang == "zh" else f"Ladder step {n}"
    return f"模块 {n}" if lang == "zh" else f"Module {n}"


def expected_units() -> int:
    """Intro, the declared segments, lab, check and summary, per module."""
    return sum(4 + m.segments[0] for m in MODULES)
