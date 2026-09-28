"""Learning paths — the Microsoft Learn hierarchy, applied to this course.

Microsoft Learn organises training as a strict four-level hierarchy:

    Career path -> Learning path -> Module -> Unit

and every module follows one fixed unit grammar:

    Introduction -> content units -> Exercise -> Knowledge check -> Summary

This course already had every level; it just did not surface one. The mapping is:

    Learning path  = a track bundle in course/05-tracks/   (4 of them)
    Module         = m00-m08, plus the free m09            (10)
    Unit           = a lesson segment, plus intro/lab/quiz/summary (70 total)

Durations are *measured* from the narration manifest, not estimated, which is the one place this
deliberately beats the model it copies. Lab times are quoted from the module's own source because a
lab's working time is not narration and must never be inferred from it.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

import figures as FIG
import site_shell as SH

COURSE_DIR = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------- unit model

NUM = re.compile(r"^[mM](\d+)$")
SEGMENT = re.compile(r"^M\d+\.\d+$")
LAB = re.compile(r"^(?:Lab|实验)\s*M\d+")
QUIZ = re.compile(r"^(?:Quiz|测验)\s*M\d+")
SUMMARY = re.compile(r"^(Recap|Summary|Discussion|回顾|总结|讨论)", re.I)

KIND_LABEL = {
    "intro": "Introduction",
    "segment": "Lesson",
    "lab": "Exercise",
    "quiz": "Knowledge check",
    "summary": "Summary",
}
KIND_LABEL_ZH = {"intro": "导论", "segment": "课文", "lab": "练习", "quiz": "知识测验", "summary": "总结"}


def module_units(deck: dict) -> list[dict]:
    """Partition a deck's slides into units, in order, covering every slide exactly once.

    The boundary rules are read off the course's own structure rather than invented:

    * slides 1-2 are always the cover and the "By the end you can…" objectives, so they are the
      module's Introduction (Microsoft's first unit) in every deck without exception;
    * a slide whose *title* opens ``Lab M#``, ``Quiz M#`` or ``Recap`` starts an Exercise, a
      knowledge check or a Summary — matched on the title, because the deck chrome deliberately
      falls back to the module tag for these and never shows ``Quiz M#`` as a kicker;
    * a slide whose kicker is ``M#.#`` starts that segment;
    * a module that marks fewer segments than it declares (m08 has no ``M8.1`` heading at all)
      still opens segment 1 at the first content slide, which is what the declared count means.

    ``check_player.py`` asserts the result covers every slide exactly once, so a future edit to a
    deck that breaks a boundary fails the gate rather than silently mis-grouping a unit.
    """
    number = int(NUM.match(deck["id"]).group(1))
    units: list[dict] = []
    current: dict | None = None
    seen_segment = False

    for slide in deck["slides"]:
        title, kicker, n = slide["title"], slide["kicker"], slide["number"]
        if n <= 2:
            kind, uid, label = "intro", "intro", "Introduction"
        elif LAB.match(title) or LAB.match(kicker):
            kind, uid = "lab", "lab"
            label = re.sub(r"^(?:Lab|实验)\s*M\d+\s*(—\s*)?", "", title).strip() or "Lab"
        elif QUIZ.match(title):
            kind, uid, label = "quiz", "quiz", "Knowledge check"
        elif SUMMARY.match(title) or (current and current["kind"] == "summary"):
            kind, uid, label = "summary", "summary", "Summary"
        elif SEGMENT.match(kicker):
            kind, uid, label = "segment", kicker, title
            seen_segment = True
        elif not seen_segment:
            kind, uid, label = "segment", f"M{number}.1", title
            seen_segment = True
        else:
            kind, uid, label = current["kind"], current["id"], current["label"]

        if current is None or uid != current["id"]:
            current = {"kind": kind, "id": uid, "label": label, "deck": deck["id"],
                       "first": n, "last": n, "slides": 1}
            units.append(current)
        else:
            current["last"] = n
            current["slides"] += 1

    for unit in units:
        unit["title"] = (unit["id"] if unit["kind"] == "segment"
                         else KIND_LABEL[unit["kind"]])
        unit["href"] = f"{deck['id']}.html#slide-{unit['first']}"
    return units


# ---------------------------------------------------------------- source facts

# Lab working time, quoted from each module's own source. A lab is hours of hands-on work whose
# narration is a one-slide introduction, so its narration seconds must never stand in for its
# duration. Where lab.md states a time that wins; otherwise the deck front matter is quoted.
LAB_TIME_FALLBACK = {
    "m01": "~2 hours", "m02": "~3 hours", "m04": "90–120 minutes",
    "m05": "~3 hours", "m06": "~2.5 hours",
}
LAB_TIME_RE = re.compile(r"\*\*(?:Time|时间)[:：]\*\*\s*([^·|\n]+?)\s*(?=·|\||$)", re.M)
LAB_TIME_RE2 = re.compile(r"(?:^|[·>])\s*(?:Time:|时间：)\s*([^·|\n]+?)\s*(?=·|\||$)", re.M)
PREREQ_RE = re.compile(r"(?:Prerequisites?:?|前置条件：?)\*{0,2}\s*([^·|\n]+?)\s*(?=\s*·|\s*\*\*|\s*\||$)", re.M)
NOT_STATED = "not stated in the module source"
NOT_STATED_ZH = "模块源文件中未说明"
LAB_TIME_FALLBACK_ZH = {"m01": "约 2 小时", "m02": "约 3 小时", "m04": "90–120 分钟", "m05": "约 3 小时", "m06": "约 2.5 小时"}


def _lab_file(deck_id: str) -> Path | None:
    # the edition's own lab: the Chinese edition quotes its Chinese source (#121)
    matches = sorted(COURSE_DIR.glob(f"03-content/{deck_id}-*/{'zh/' if SH.LANG == 'zh' else ''}lab.md"))
    return matches[0] if matches else None


def lab_time(deck_id: str) -> str:
    path = _lab_file(deck_id)
    if path:
        text = path.read_text(encoding="utf-8")
        for pattern in (LAB_TIME_RE, LAB_TIME_RE2):
            match = pattern.search(text)
            if match:
                value = match.group(1).strip().strip("*").strip()
                if value:
                    return value
    if SH.LANG == "zh":
        return LAB_TIME_FALLBACK_ZH.get(deck_id, NOT_STATED_ZH)
    return LAB_TIME_FALLBACK.get(deck_id, NOT_STATED)


def _clean_prereq(value: str) -> str:
    """Tidy a prerequisite pulled out of a lab header.

    Lab headers are prose, and some wrap mid-sentence, so a capture can end inside an unclosed
    bracket. Rather than print half a parenthetical, cut back to the last balanced point — and say
    so plainly rather than guessing at the missing words.
    """
    value = re.sub(r"^[-*\u2022]\s*", "", value.strip())
    value = re.sub(r"\s+", " ", value).strip().strip("*").strip()
    if value.count("(") > value.count(")"):
        value = value[:value.rindex("(")].strip().rstrip(";,:")
    value = value.rstrip(" .;:")
    if not value or value.lower() in {"none", "n/a", "no prerequisites"}:
        return SH.T("None stated", "未说明")
    return value[:1].upper() + value[1:]


def lab_prereq(deck_id: str) -> str:
    path = _lab_file(deck_id)
    if path:
        match = PREREQ_RE.search(path.read_text(encoding="utf-8"))
        if match:
            return _clean_prereq(match.group(1))
    return SH.T(NOT_STATED, NOT_STATED_ZH)


def cover_facts(deck: dict) -> dict:
    """Promise and lesson length, read from the cover slide's body (not the YAML front matter)."""
    # The cover's figure (#99) is the module's picture, not its promise: its words stay out of it.
    body = FIG.FIGURE_HTML.sub("", deck["slides"][0].get("html", ""))
    text = re.sub(r"<[^>]+>", " ", body)
    text = html.unescape(re.sub(r"\s+", " ", text))
    promise = re.search(r"(?:Promise:|承诺：)\s*(.+?)\s*(?:Duration:|时长：|$)", text)
    duration = re.search(r"(?:Duration:|时长：)\s*(.+?)\s*$", text)
    return {"promise": promise.group(1).strip() if promise else "",
            "lesson_length": duration.group(1).strip() if duration else ""}


def objectives(deck: dict) -> list[str]:
    """The objectives list from slide 2 (“By the end you can…”)."""
    return re.findall(r"<li>(.*?)</li>", deck["slides"][1].get("html", ""), re.S)


# ---------------------------------------------------------------- the paths

# `core` modules are taught in full; `slice` modules contribute only the named segments. Both are
# copied from each bundle's own `bundle-map.md` rather than inferred from the module list.
TRACKS = [
    {
        "slug": "aps",
        "title": "The full studio course",
        "medium": "All three types",
        "kicker": "All three product types",
        "promise": "Build, ship and sell all three kinds of AI product — and finish with a scored "
                   "capstone, a launch arc and a defensible price.",
        "core": ["m00", "m01", "m02", "m03", "m04", "m05", "m06", "m07", "m08"],
        "slice": {},
        "price": "$399 self-paced · $1,490 cohort",
        "level": "Beginner to intermediate",
        "role": "Founder · Product engineer",
        "status": "full",
        "page": None,  # the full course is the module index itself
    },
    {
        # Type 1 — the product is an app. Case study: ListenToMe (Swift/macOS).
        "slug": "on-device-app",
        "title": "On-Device AI Apps",
        "medium": "App",
        "kicker": "Type 1 · AI with an app",
        "promise": "Ship a local-first AI app whose privacy claims are enforced in code and proven "
                   "by tests.",
        "core": ["m00", "m01", "m02", "m03"],
        # Straight from the bundle map. `exclude` names the units the map lists as NOT included,
        # `partial` the ones included only in part. Without this the path page listed all seven M8
        # units — including M8.3, Lab M8 and Quiz M8 — and counted their narration as if taught.
        "slice": {
            "m07": {"note": "All three segments · Lab M7 steps 1–5 · Quiz M7",
                    "exclude": [], "partial": ["lab"]},
            "m08": {"note": "Segments M8.1–M8.2 only",
                    "exclude": ["M8.3", "lab", "quiz"], "partial": []},
        },
        "excluded": [
            ("M4 · M5 — the Spec-Driven SaaS track", "m04", "m05"),
            ("M6 — the Expertise track", "m06", None),
            ("M8.3 capstone, Lab M8 and Quiz M8", "m08", None),
        ],
        "price": "$199",
        "level": "Beginner to intermediate",
        "role": "iOS / macOS engineer · Indie developer",
        "subject": "Local-first AI · Privacy engineering",
        # Quoted from bundle-map.md: "17 of 27 teaching segments · 4 of 8 full labs ·
        # 5 of 9 quizzes (40 of 72 questions)". The model is asserted against these.
        "measured": {"segments": (17, 27), "labs": (4, 8), "quizzes": (5, 9), "questions": (40, 72)},
        "counts_source": "bundle-map.md",
        "status": "built",
        "page": "path-on-device-app.html",
    },
    {
        # Type 2 — the product is a web service. Case study: SignUpFlow (FastAPI).
        "slug": "spec-driven-saas",
        "title": "Spec-Driven AI SaaS",
        "medium": "Web",
        "kicker": "Type 2 · AI with the web",
        "promise": "A spec folder that survives a stranger test, and acceptance evidence that "
                   "survives a skeptical auditor.",
        "core": ["m00", "m01", "m04", "m05"],
        # The launch slice here has NO lab and NO quiz — the week-6 capstone worksheet replaces
        # Lab M7, and Quiz M7/M8 are excluded. That is why this path has 4 quizzes, not 5.
        "slice": {
            "m07": {"note": "Segments M7.1–M7.3 · no lab, no quiz",
                    "exclude": ["lab", "quiz"], "partial": []},
            "m08": {"note": "Segments M8.1–M8.2 only",
                    "exclude": ["M8.3", "lab", "quiz"], "partial": []},
        },
        "excluded": [
            ("M2 · M3 — the On-Device track", "m02", "m03"),
            ("M6 — the Expertise track", "m06", None),
            ("M8.3 capstone, Lab M7/M8 and Quiz M7/M8", "m08", None),
        ],
        "price": "$199",
        "level": "Intermediate",
        "role": "Backend engineer · SaaS builder",
        "subject": "Multi-tenant security · Acceptance evidence",
        # Quoted from bundle-map.md: "4 modules in full + 1 cross-module slice ...; 17 of 27 lesson
        # segments; 4 labs; 4 of 9 quizzes (32 of 72 questions)".
        "measured": {"segments": (17, 27), "labs": (4, 8), "quizzes": (4, 9), "questions": (32, 72)},
        "counts_source": "bundle-map.md",
        "status": "built",
        "page": "path-spec-driven-saas.html",
    },
    {
        # Type 3 — the product is content: a learning product, a presentation, or a sales pitch.
        # Case study: ai_qe, whose own 116-slide narrated briefing site is this same shape.
        "slug": "expertise-product",
        "title": "Expertise as a Product",
        "medium": "Content",
        "kicker": "Type 3 · AI with content",
        "promise": "Every published claim carries a date, sample, method, unit and level — and the "
                   "funnel sells a measurement, not a promise.",
        "core": ["m00", "m01", "m06"],
        # Unlike the other two, this path keeps M8.3 and Quiz M8 — but the capstone and the lab are
        # the Type 3 row only, so both are marked partial rather than excluded.
        "slice": {
            "m07": {"note": "Segments M7.1–M7.3 · Lab M7 for the Type 3 offer only · Quiz M7",
                    "exclude": [], "partial": ["lab"]},
            "m08": {"note": "M8.1–M8.3 · capstone is the Type 3 row only · Quiz M8",
                    "exclude": [], "partial": ["M8.3", "lab"]},
        },
        "excluded": [
            ("M2 · M3 — the On-Device track", "m02", "m03"),
            ("M4 · M5 — the Spec-Driven SaaS track", "m04", "m05"),
            ("The Type 1 / Type 2 capstone and lab rows", "m08", None),
        ],
        "price": "$199",
        "level": "Intermediate",
        "role": "Consultant · Domain expert · Educator",
        "subject": "Evidence products · Learning and sales content",
        # No total is stated anywhere in this bundle map, so none is asserted. The counts are
        # derived from its own rows and labelled as derived rather than quoted.
        "measured": None,
        "counts_source": "derived from bundle-map.md rows (no course-wide total is stated there)",
        "status": "built",
        "page": "path-expertise-product.html",
    },
    {
        # Free and standalone: the on-ramp for anyone who cannot yet clone a repository, and a
        # publishable page for any product in the course. Outside the paid course's certificate.
        # Case study: ai_qe, which is itself a GitHub Pages site.
        "slug": "github-pages",
        "title": "Ship a Website with GitHub Pages",
        "medium": "Website",
        "kicker": "Free · Start here if the terminal is new",
        "promise": "From nothing installed to a public product catalog: Git, the GitHub CLI, "
                   "folders, cloning and publishing, on Windows and macOS.",
        "core": ["m09"],
        "slice": {},
        "excluded": [
            ("The paid course, M0–M8 — this path is free and stands alone", "m00", "m08"),
        ],
        "price": "Free",
        "level": "Beginner",
        "role": "New to the terminal · Small-business owner",
        "subject": "Git · GitHub CLI · GitHub Pages",
        "measured": None,
        "counts_source": "the module itself",
        "status": "built",
        "page": "path-github-pages.html",
    },
]

TRACK_BY_SLUG = {t["slug"]: t for t in TRACKS}

# The Chinese edition's words for each path (#121). Structure, modules and counts are the English
# entry's; only what a learner reads changes.
TRACKS_ZH = {
    "aps": {
        "title": "完整工作室课程", "medium": "全部三类", "kicker": "全部三类产品",
        "promise": "构建、发布并销售全部三类 AI 产品——最后完成一个评分的毕业项目、一套发布节奏和一个站得住的定价。",
        "price": "自学 $399 · 训练营 $1,490", "level": "入门到中级", "role": "创始人 · 产品工程师",
    },
    "on-device-app": {
        "title": "端侧 AI 应用", "medium": "应用", "kicker": "类型 1 · 带应用的 AI",
        "promise": "发布一个本地优先的 AI 应用，它的隐私承诺由代码强制执行，并由测试证明。",
        "slice_notes": {"m07": "全部三个分段 · 实验 M7 第 1–5 步 · 测验 M7", "m08": "仅分段 M8.1–M8.2"},
        "excluded": ["M4 · M5——规格驱动 SaaS 路线", "M6——专业知识路线", "M8.3 毕业项目、实验 M8 和测验 M8"],
        "price": "$199", "level": "入门到中级", "role": "iOS / macOS 工程师 · 独立开发者",
        "subject": "本地优先 AI · 隐私工程",
    },
    "spec-driven-saas": {
        "title": "规格驱动 AI SaaS", "medium": "Web", "kicker": "类型 2 · 带 Web 的 AI",
        "promise": "一个经得起陌生人测试的规格文件夹，以及经得起多疑审计者的验收证据。",
        "slice_notes": {"m07": "分段 M7.1–M7.3 · 无实验、无测验", "m08": "仅分段 M8.1–M8.2"},
        "excluded": ["M2 · M3——端侧路线", "M6——专业知识路线", "M8.3 毕业项目、实验 M7/M8 和测验 M7/M8"],
        "price": "$199", "level": "中级", "role": "后端工程师 · SaaS 构建者",
        "subject": "多租户安全 · 验收证据",
    },
    "expertise-product": {
        "title": "把专业知识做成产品", "medium": "内容", "kicker": "类型 3 · 带内容的 AI",
        "promise": "每个公开的主张都带有日期、样本、方法、单位和层级——漏斗卖的是一项测量，而不是一个承诺。",
        "slice_notes": {"m07": "分段 M7.1–M7.3 · 实验 M7 仅限类型 3 的报价 · 测验 M7",
                        "m08": "M8.1–M8.3 · 毕业项目仅限类型 3 一行 · 测验 M8"},
        "excluded": ["M2 · M3——端侧路线", "M4 · M5——规格驱动 SaaS 路线", "类型 1 / 类型 2 的毕业项目和实验行"],
        "price": "$199", "level": "中级", "role": "顾问 · 领域专家 · 教育者",
        "subject": "证据产品 · 学习与销售内容",
        "counts_source": "由 bundle-map.md 的各行推算（那里没有给出全课程总数）",
    },
    "github-pages": {
        "title": "用 GitHub Pages 发布网站", "medium": "网站", "kicker": "免费 · 终端新手从这里开始",
        "promise": "从什么都没安装，到一个公开的产品目录：Git、GitHub CLI、文件夹、克隆和发布，Windows 和 macOS 都适用。",
        "excluded": ["付费课程 M0–M8——本路线免费且独立"],
        "price": "免费", "level": "入门", "role": "终端新手 · 小企业主",
        "subject": "Git · GitHub CLI · GitHub Pages", "counts_source": "模块本身",
    },
}


def tracks() -> list[dict]:
    """The paths, in the words of the edition being written."""
    if SH.LANG != "zh":
        return TRACKS
    out = []
    for t in TRACKS:
        zh = TRACKS_ZH.get(t["slug"], {})
        loc = {**t, **{k: v for k, v in zh.items() if k not in ("slice_notes", "excluded")}}
        if zh.get("slice_notes"):
            loc["slice"] = {m: {**v, "note": zh["slice_notes"].get(m, v["note"])} for m, v in t["slice"].items()}
        if zh.get("excluded") and t.get("excluded"):
            loc["excluded"] = [(label, a, b) for label, (_, a, b) in zip(zh["excluded"], t["excluded"])]
        out.append(loc)
    return out


def slice_spec(track: dict, deck_id: str) -> dict:
    spec = (track.get("slice") or {}).get(deck_id) or {}
    return spec if isinstance(spec, dict) else {"note": spec, "exclude": [], "partial": []}


def track_units(track: dict, units_by_deck: dict[str, list[dict]]) -> list[dict]:
    """Every unit a path actually includes, in path order, tagged full or slice.

    Units the bundle map excludes are dropped here rather than rendered: a path's unit count and its
    narration total must describe what the buyer gets, not what the parent module contains.
    """
    out = []
    for deck_id in track["core"]:
        for unit in units_by_deck.get(deck_id, []):
            out.append({**unit, "inclusion": "full"})
    for deck_id in (track.get("slice") or {}):
        spec = slice_spec(track, deck_id)
        for unit in units_by_deck.get(deck_id, []):
            if unit["id"] in spec["exclude"]:
                continue
            out.append({**unit, "inclusion": "slice", "note": spec["note"],
                        "partial": unit["id"] in spec["partial"]})
    return out


def paths_for_module(deck_id: str, tracks: list[dict] | None = None) -> list[dict]:
    """Every built track that includes this module, and how it includes it.

    M0 and M1 are shared by all three paths in full; M7 and M8 are sliced into all three, each with
    a different exclude list. A module page that named only one owner path would misdescribe the
    other two, so the module page renders one row per path instead of a single "Part of…" line.
    """
    out = []
    for track in (tracks if tracks is not None else TRACKS):
        if track["status"] != "built":
            continue
        if deck_id in track["core"]:
            out.append({"track": track, "inclusion": "full", "spec": {}})
        elif deck_id in (track.get("slice") or {}):
            out.append({"track": track, "inclusion": "slice",
                        "spec": slice_spec(track, deck_id)})
    return out


def track_minutes(track: dict, units_by_deck: dict[str, list[dict]],
                  seconds: dict[str, float]) -> float:
    """Measured narration seconds for the slide-backed units a path includes."""
    total = 0.0
    for deck_id in list(track["core"]) + list(track.get("slice") or {}):
        for unit in units_by_deck.get(deck_id, []):
            total += seconds.get(f"{deck_id}:{unit['id']}", 0.0)
    return total


def unit_seconds(units_by_deck: dict[str, list[dict]], manifest: dict) -> dict[str, float]:
    """Measured narration seconds per unit, summed from the manifest's per-slide durations."""
    out: dict[str, float] = {}
    for deck_id, units in units_by_deck.items():
        entries = (manifest.get("decks", {}).get(deck_id, {}) or {}).get("slides", {})
        for unit in units:
            out[f"{deck_id}:{unit['id']}"] = sum(
                float((entries.get(f"slide-{i}") or {}).get("duration", 0) or 0)
                for i in range(unit["first"], unit["last"] + 1))
    return out


def fmt_minutes(seconds_value: float) -> str:
    minutes = seconds_value / 60.0
    if minutes < 1:
        return SH.T(f"{seconds_value:.0f} sec", f"{seconds_value:.0f} 秒")
    return SH.T(f"{minutes:.1f} min".replace(".0 min", " min"), f"{minutes:.1f} 分钟".replace(".0 分钟", " 分钟"))


# ---------------------------------------------------------------- pages

def _plural(n: int, noun: str) -> str:
    return f"{n} {noun}" + ("" if n == 1 else "s")


def _at_a_glance(items: list[tuple[str, str]]) -> str:
    """Microsoft Learn's metadata block: every value is a filter in their catalogue, a fact here."""
    cells = "".join(
        f'<div class="aga-item"><dt>{html.escape(key)}</dt><dd>{html.escape(value)}</dd></div>'
        for key, value in items if value)
    return f'<dl class="at-a-glance">{cells}</dl>'


def path_cards_html(tracks: list[dict], units_by_deck: dict[str, list[dict]],
                    seconds: dict[str, float], site_base: str) -> str:
    """The path chooser. Rendered once and used on both the landing page and the paths page, so the
    two cannot drift: the landing page is the paths GUI now, not a page that happens to link to it."""
    cards = []
    for track in tracks:
        units = track_units(track, units_by_deck)
        minutes = track_minutes(track, units_by_deck, seconds)
        live = bool(track["page"]) and track["status"] == "built"
        if live:
            status = f'<span class="voice-chip is-release">{SH.T("path page", "路线页面")}</span>'
            href, target = f"{site_base}/{track['page']}", SH.T("Open this path", "打开这条路线")
        elif track["status"] == "full":
            # The full course is not a page that failed to build — it is the module index itself.
            status = f'<span class="voice-chip is-release">{SH.T("all nine modules", "全部九个模块")}</span>'
            href, target = f"{site_base}/index.html", SH.T("Browse all modules", "浏览全部模块")
        else:
            status = f'<span class="voice-chip is-text">{SH.T("page not built yet", "页面尚未构建")}</span>'
            href, target = f"{site_base}/index.html", SH.T("Browse the modules", "浏览模块")
        modules = len(track["core"]) + len(track.get("slice") or {})
        unit_ids = ",".join(f"{u['deck']}:{u['id']}" for u in units)
        cards.append(f"""<article class="path-card">
  <div class="path-head">
    <p class="path-kicker">{html.escape(track['kicker'])}</p>
    <h3><a href="{href}">{html.escape(track['title'])}</a></h3>
    <p class="path-meta">{SH.T(f'{modules} module{"" if modules == 1 else "s"} · {len(units)} units · {fmt_minutes(minutes)} of narration', f"{modules} 个模块 · {len(units)} 个单元 · 讲解 {fmt_minutes(minutes)}")}</p>
    <p class="card-progress"><span class="card-bar" data-ring-units="{unit_ids}" role="img" aria-label="progress"><span class="card-bar-fill"></span></span>
      <span class="card-count" data-ring-text></span></p>
  </div>
  <div class="path-body">
    <p class="path-promise">{html.escape(track['promise'])}</p>
    {_at_a_glance([(SH.T("You build", "你将构建"), track["medium"]), (SH.T("Level", "难度"), track["level"]),
                   (SH.T("Role", "角色"), track["role"]), (SH.T("Price", "价格"), track["price"])])}
    <p class="path-status">{status}</p>
    <a class="btn-primary" href="{href}">{target} →</a>
  </div>
</article>""")
    return chr(10).join(cards)


def paths_page(tracks: list[dict], units_by_deck: dict[str, list[dict]],
               seconds: dict[str, float], site_base: str, brand: str) -> str:
    cards = path_cards_html(tracks, units_by_deck, seconds, site_base)

    total_units = sum(len(u) for u in units_by_deck.values())
    head = SH.page_head(
        "Learning paths", SH.T("Four ways into the same method.", "进入同一套方法的四条路线。"),
        SH.T("""The three products this course is built from are three <em>types</em> of AI
      product — an <strong>app</strong>, a <strong>web service</strong>, and a
      <strong>content product</strong> like a learning site, a presentation or a sales pitch. Each
      track path teaches one of those types end to end; the full studio course teaches all three. The
      method is identical in every path — same lessons, labs and quizzes, nothing rewritten or watered
      down — and each path states exactly what it leaves out.""",
             """本课程所依托的三个产品，是 AI 产品的三种<em>类型</em>：一个<strong>应用</strong>、一个
      <strong>Web 服务</strong>，以及一个<strong>内容产品</strong>（比如学习网站、演示或销售文案）。每条专项路线
      完整地教其中一种类型；完整工作室课程三种都教。每条路线的方法完全相同——同样的课文、实验和测验，
      没有改写或删减——并且每条路线都写明它不包含什么。"""),
        f"""<ul class="site-facts">
      <li>{SH.T(f"{len(tracks)} paths", f"{len(tracks)} 条路线")}</li>
      <li>{SH.T(f"{len(units_by_deck)} modules · {total_units} units", f"{len(units_by_deck)} 个模块 · {total_units} 个单元")}</li>
      <li>{SH.T("Measured durations", "时长均为实测")}</li>
    </ul>""")
    unit_grammar = SH.T("""<h2>What a unit is</h2>
    <p>Every module in this course is built the same way, and the path pages show it:</p>
    <ol class="unit-grammar">
      <li><strong>Introduction</strong> — the cover and the module's objectives</li>
      <li><strong>Lesson</strong> — three teaching segments, 27 across the course</li>
      <li><strong>Exercise</strong> — one hands-on lab per module</li>
      <li><strong>Knowledge check</strong> — eight questions per module, 72 across the course</li>
      <li><strong>Summary</strong> — the recap and the discussion prompt</li>
    </ol>
    <p class="index-footnote">Every duration on these pages is measured from the recorded narration,
      not estimated. Lab times are quoted from each module's own source, because a lab is hours of
      hands-on work and its narration is a single part.</p>""", """<h2>什么是单元</h2>
    <p>本课程的每个模块都按同样的方式构建，路线页面也这样呈现：</p>
    <ol class="unit-grammar">
      <li><strong>导论</strong>——封面和本模块的目标</li>
      <li><strong>课文</strong>——三个教学分段，全课程共 27 个</li>
      <li><strong>练习</strong>——每个模块一个动手实验</li>
      <li><strong>知识测验</strong>——每个模块八道题，全课程共 72 道</li>
      <li><strong>总结</strong>——回顾和讨论题</li>
    </ol>
    <p class="index-footnote">这些页面上的每个时长都来自录制讲解的实测，而非估算。实验时间引自各模块自己的
      源文件，因为一个实验要数小时的动手操作，而它的讲解只有一个部分。</p>""")
    body = f"""{head}
  <div class="section-heading">
    <h2>{SH.T("Choose by what you want to build", "按你想构建的东西选择")}</h2>
    <span class="section-note">{SH.T("A unit is one lesson segment, a lab, or a knowledge check — the level at which you actually sit down and learn something.", "一个单元是一个课程分段、一个实验或一次知识测验——也就是你真正坐下来学一样东西的粒度。")}</span>
  </div>
  <div class="path-grid">
{cards}
  </div>
  <section class="how-to">
    {unit_grammar}
  </section>"""
    return SH.document(SH.T("Learning paths — AI Product Studio", "学习路线 — AI Product Studio"),
                       SH.T("Four learning paths through one AI product course: the full studio course and "
                            "three single-archetype tracks.", "同一门 AI 产品课程的四条学习路线：完整工作室课程，以及三条单一类型的专项路线。"),
                       body, site_base, "paths",
                       crumbs=[("Course", f"{site_base}/index.html"), ("Learning paths", None)])


def path_page(track: dict, decks_by_id: dict[str, dict], units_by_deck: dict[str, list[dict]],
              seconds: dict[str, float], site_base: str, brand: str,
              built_modules: set[str] | None = None) -> str:
    built_modules = built_modules or set()
    units = track_units(track, units_by_deck)
    minutes = track_minutes(track, units_by_deck, seconds)
    live = track["page"] and track["status"] == "built"
    cards = []
    for deck_id in track["core"]:
        deck = decks_by_id[deck_id]
        facts = cover_facts(deck)
        deck_units = units_by_deck[deck_id]
        deck_minutes = sum(seconds.get(f"{deck_id}:{u['id']}", 0) for u in deck_units)
        cards.append(_module_row(deck, deck_units, deck_minutes, site_base, built_modules, "full", ""))
    for deck_id in (track.get("slice") or {}):
        spec = slice_spec(track, deck_id)
        deck = decks_by_id[deck_id]
        deck_units = units_by_deck[deck_id]
        kept = [u for u in deck_units if u["id"] not in spec["exclude"]]
        deck_minutes = sum(seconds.get(f"{deck_id}:{u['id']}", 0) for u in kept)
        cards.append(_module_row(deck, deck_units, deck_minutes, site_base, built_modules,
                                 "slice", spec))

    measured = track.get("measured") or {}
    included = track_units(track, units_by_deck)
    derived = {
        "segments": sum(1 for u in included if u["kind"] == "segment"),
        "labs": sum(1 for u in included if u["kind"] == "lab" and u["inclusion"] == "full"),
        "quizzes": sum(1 for u in included if u["kind"] == "quiz"),
        "questions": 8 * sum(1 for u in included if u["kind"] == "quiz"),
    }
    labels = ((SH.T("Teaching segments", "教学分段"), "segments"), (SH.T("Full labs", "完整实验"), "labs"),
              (SH.T("Quizzes", "测验"), "quizzes"), (SH.T("Quiz questions", "测验题"), "questions"))

    def cell(key: str) -> str:
        got = derived[key]
        if measured and key in measured:
            return SH.T(f"{got} of {measured[key][1]}", f"{got} / {measured[key][1]}")
        return f"{got} <span class=\"derived-mark\">{SH.T('derived', '推算')}</span>"

    rows = "".join(f'<tr><th scope="row">{label}</th><td>{cell(key)}</td></tr>'
                   for label, key in labels)
    source = track.get("counts_source", "the bundle map")
    note = (SH.T(f'Counted from {html.escape(source)}.', f'统计自 {html.escape(source)}。')
            if measured else
            SH.T(f'{html.escape(source)} — so these are counted from the rows, not quoted from a total.',
                 f'{html.escape(source)}——所以这些数字是逐行统计的，而不是引用某个总数。'))
    counts = f"""<section class="path-section">
    <h2>{SH.T("What this path includes", "这条路线包含什么")}</h2>
    <p class="section-note">{note}</p>
    <table class="counts-table">
      <caption>{SH.T("This path compared with the full studio course", "这条路线与完整工作室课程的对比")}</caption>
      <thead><tr><th scope="col">{SH.T("Item", "项目")}</th><th scope="col">{SH.T("In this path", "本路线")}</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </section>"""

    excluded = ""
    if track.get("excluded"):
        items = "".join(f"<li>{html.escape(label)}</li>" for label, _a, _b in track["excluded"])
        excluded = f"""<section class="path-section">
    <h2>{SH.T("Not in this path", "不在这条路线中")}</h2>
    <p class="section-note">{SH.T("Stated plainly rather than discovered at checkout.", "直接写明，而不是等到结账时才发现。")}</p>
    <ul class="excluded-list">{items}</ul>
  </section>"""

    head = SH.page_head(
        SH.T(f"Learning path · {_plural(len(track['core']) + len(track.get('slice') or {}), 'module')} · {len(units)} units",
             f"学习路线 · {len(track['core']) + len(track.get('slice') or {})} 个模块 · {len(units)} 个单元"),
        html.escape(track["title"]), html.escape(track["promise"]),
        _at_a_glance([(SH.T("You build", "你将构建"), track["medium"]), (SH.T("Level", "难度"), track["level"]),
                      (SH.T("Role", "角色"), track["role"]),
                      (SH.T("Subject", "主题"), track.get("subject", SH.T("AI product engineering", "AI 产品工程"))),
                      (SH.T("Duration", "时长"), SH.T(f"{fmt_minutes(minutes)} of narration + lab time", f"讲解 {fmt_minutes(minutes)} + 实验时间")),
                      (SH.T("Price", "价格"), track["price"])]))
    scope_note = SH.T("""<h2>The honest scope note</h2>
    <p>This path is not a separate course. It sequences and frames the parent course's modules for one
      archetype and reuses its lesson, lab and quiz artifacts — nothing is rewritten, reordered or
      watered down, and the slice of M7/M8 is scoped rather than summarised.</p>
    <p class="index-footnote">Durations are measured from the recorded narration. Lab times are quoted
      from each module's source. Nothing on this page is an estimate presented as a measurement.</p>""", """<h2>坦率的范围说明</h2>
    <p>这条路线不是一门独立的课程。它为一种产品类型编排并组织母课程的模块，复用其课文、实验和测验——
      没有改写、重排或删减，M7/M8 的切片是限定范围，而不是概括。</p>
    <p class="index-footnote">时长来自录制讲解的实测。实验时间引自各模块的源文件。本页没有任何把估算当作实测的数字。</p>""")
    body = f"""{head}
  <section class="path-section">
    <h2>{SH.T("Prerequisites", "前置条件")}</h2>
    <p>{html.escape(track.get('prereq') or SH.T('None. Module 0 assumes no prior setup beyond a machine that can run Python.', '无。模块 0 只要求一台能运行 Python 的电脑，无需其他准备。'))}</p>
  </section>
  <div class="section-heading">
    <h2>{SH.T("Modules in this path", "这条路线的模块")}</h2>
    <span class="section-note">{SH.T("In order. A slice module contributes only the named segments — the rest belongs to another path.", "按顺序排列。切片模块只贡献列出的分段——其余部分属于其他路线。")}</span>
  </div>
  <div class="module-list">
{chr(10).join(cards)}
  </div>
{counts}
{excluded}
  <section class="path-section">
    {scope_note}
  </section>"""
    return SH.document(SH.T(f"{track['title']} — learning path — AI Product Studio", f"{track['title']} — 学习路线 — AI Product Studio"), track["promise"], body,
                       site_base, "path-page",
                       crumbs=[("Course", f"{site_base}/index.html"),
                               ("Learning paths", f"{site_base}/paths.html"), (track["title"], None)],
                       body_attrs=f' data-path="{html.escape(track["slug"], quote=True)}"')


def _module_row(deck: dict, units: list[dict], minutes: float, site_base: str,
                built_modules: set[str], inclusion: str, spec: dict | str) -> str:
    """One module row on a path page.

    A slice module lists *all* its units, including the ones this path leaves out, and marks them.
    Showing the exclusion is the point: "M8 — Launch" appearing in a path that does not teach the
    capstone would otherwise read as though it did.
    """
    spec = spec if isinstance(spec, dict) else {}
    exclude = set(spec.get("exclude") or ())
    partial = set(spec.get("partial") or ())
    facts = cover_facts(deck)
    short = re.sub(r"^M\d+\s*—\s*", "", deck["label"]).strip()
    number = int(NUM.match(deck["id"]).group(1))
    chip = (f'<span class="inclusion-chip is-full">{SH.T("full module", "完整模块")}</span>' if inclusion == "full"
            else f'<span class="inclusion-chip is-slice">{SH.T("slice", "切片")}</span>')

    rows = []
    for unit in units:
        label = f'<a href="{site_base}/{unit["href"]}">{html.escape(unit["title"])}</a>'
        kind = f'<span class="unit-kind">{html.escape(KIND_LABEL[unit["kind"]])}</span>'
        if unit["id"] in exclude:
            rows.append(f'<li class="is-excluded">{label}{kind}'
                        f'<span class="unit-mark">{SH.T("not in this path", "不在本路线")}</span></li>')
        elif unit["id"] in partial:
            rows.append(f'<li>{label}{kind}'
                        f'<span class="unit-mark is-partial">{SH.T("part only", "仅部分")}</span></li>')
        else:
            rows.append(f'<li>{label}{kind}</li>')

    included = len(units) - len(exclude)
    count = (SH.T(f"{included} of {len(units)} units", f"{included} / {len(units)} 个单元") if exclude
             else SH.T(f"{len(units)} units", f"{len(units)} 个单元"))
    note = f'<p class="slice-note">{html.escape(spec["note"])}</p>' if spec.get("note") else ""
    href = (f"{site_base}/module-{deck['id']}.html" if deck["id"] in built_modules
            else f"{site_base}/{deck['id']}.html")
    return f"""<article class="module-row">
  <div class="module-head">
    <p class="module-number">{SH.T(f"Module {number}", f"模块 {number}")} {chip}</p>
    <h3><a href="{href}">{html.escape(short)}</a></h3>
    <p class="module-promise">{html.escape(facts['promise'])}</p>
    <p class="module-meta">{count} · {SH.T(f"{fmt_minutes(minutes)} of narration", f"讲解 {fmt_minutes(minutes)}")}</p>
    {note}
  </div>
  <ol class="module-units">{"".join(rows)}</ol>
</article>"""


def module_page(deck: dict, units: list[dict], seconds: dict[str, float], site_base: str,
                brand: str, tracks_for: list[dict], text_only: bool, hero: str = "") -> str:
    """Microsoft Learn's module page: objectives, prerequisites, then the ordered unit list.

    `tracks_for` is every built path that includes this module. Modules are shared between paths —
    M0 and M1 open all three, M7 and M8 are sliced into all three — so the page says so per path
    rather than claiming a single owner.
    """
    number = int(NUM.match(deck["id"]).group(1))
    short = re.sub(r"^M\d+\s*—\s*", "", deck["label"]).strip()
    facts = cover_facts(deck)
    objectives_html = "".join(f"<li>{item}</li>" for item in objectives(deck))
    total = sum(seconds.get(f"{deck['id']}:{u['id']}", 0) for u in units)

    mediums = " · ".join(entry["track"]["medium"] for entry in tracks_for) or SH.T("All three types", "全部三类")
    path_rows = []
    for entry in tracks_for:
        track, inclusion, spec = entry["track"], entry["inclusion"], entry["spec"]
        excluded = spec.get("exclude") or []
        partial = spec.get("partial") or []
        if inclusion == "full":
            chip = f'<span class="inclusion-chip is-full">{SH.T("full module", "完整模块")}</span>'
            note = SH.T("Every unit of this module is in the path.", "本模块的每个单元都在这条路线中。")
        else:
            chip = f'<span class="inclusion-chip is-slice">{SH.T("slice", "切片")}</span>'
            bits = []
            sep = SH.T(", ", "、")
            if excluded:
                bits.append(SH.T("not in this path: ", "不在本路线：") + sep.join(
                    html.escape(SH.unit_name(u)) for u in units if u["id"] in excluded))
            if partial:
                bits.append(SH.T("part only: ", "仅部分：") + sep.join(
                    html.escape(SH.unit_name(u)) for u in units if u["id"] in partial))
            note = html.escape(spec.get("note", "")) + (" — " + "; ".join(bits) if bits else "")
        href = f"{site_base}/{track['page']}" if track.get("page") else f"{site_base}/index.html"
        path_rows.append(f"""<li class="path-line">
  <span class="path-line-medium">{html.escape(track['medium'])}</span>
  <a class="path-line-title" href="{href}">{html.escape(track['title'])}</a>
  {chip}
  <span class="path-line-note">{note}</span>
</li>""")
    paths_section = f"""<section class="path-section">
    <h2>{SH.T("Paths through this module", "经过本模块的路线")}</h2>
    <p class="section-note">{SH.T(f"Shared by {len(tracks_for)} of the paths.", f"{len(tracks_for)} 条路线共用。") if len(tracks_for) > 1 else SH.T("This module belongs to one path.", "本模块属于一条路线。")}</p>
    <ul class="module-paths">{"".join(path_rows)}</ul>
  </section>""" if tracks_for else ""

    rows = []
    for index, unit in enumerate(units, 1):
        seconds_value = seconds.get(f"{deck['id']}:{unit['id']}", 0)
        if unit["kind"] == "lab":
            # the duration only: a source's "~30 minutes including downloads (…)" is a sentence,
            # and a unit row is one line
            quoted = lab_time(deck["id"])
            duration = re.match(r"(?:~|约)?\s*[\d.]+(?:\s*[–-]\s*[\d.]+)?\s*(?:minutes?\b|mins?\b|hours?\b|小时|分钟)", quoted)
            said = duration.group(0) if duration else quoted
            time_text = SH.T(f'{fmt_minutes(seconds_value)} narrated · {said} hands-on',
                             f'讲解 {fmt_minutes(seconds_value)} · 动手 {said}')
        else:
            time_text = fmt_minutes(seconds_value)
        extra = ""
        if unit["kind"] == "lab":
            extra = f'<a class="unit-open" href="{site_base}/lab-{deck["id"]}.html">{SH.T("Checklist →", "清单 →")}</a>'
        elif unit["kind"] == "quiz":
            extra = f'<a class="unit-open" href="{site_base}/quiz-{deck["id"]}.html">{SH.T("Take it →", "去作答 →")}</a>'
        elif unit["kind"] == "segment":
            extra = f'<a class="unit-open" href="{site_base}/lesson-{deck["id"]}.html">{SH.T("Read →", "阅读 →")}</a>'
        # A unit row is a link with its recorded status (#84) — never a checkbox. shell.js colours it
        # from the progress store, which only records what the learner did.
        uid = f"{deck['id']}:{html.escape(unit['id'])}"
        rows.append(f"""<li class="unit">
  <a class="unit-link" href="{site_base}/{SH.unit_href(deck['id'], unit)}" data-unit="{uid}" data-first="{unit['first']}" data-last="{unit['last']}">
    {SH.STATUS_ICON}
    <span class="unit-kind">{html.escape(KIND_LABEL[unit['kind']])}</span>
    <span class="unit-title">{html.escape(SH.unit_name(unit))}</span>
    <span class="unit-time">{html.escape(time_text)}</span>
    {SH.STATUS_TEXT}
  </a>
  {extra if unit["kind"] == "segment" else ""}
</li>""")

    if len(tracks_for) == 1 and tracks_for[0]["track"].get("page"):
        path_link = (f'<a href="{site_base}/{tracks_for[0]["track"]["page"]}">'
                     f'{html.escape(tracks_for[0]["track"]["title"])}</a>')
    else:
        path_link = f'<a href="{site_base}/paths.html">{SH.T("the learning paths", "学习路线")}</a>'

    head = SH.page_head(
        SH.T(f"Module {number} · {len(units)} units · {fmt_minutes(total)} of narration",
             f"模块 {number} · {len(units)} 个单元 · 讲解 {fmt_minutes(total)}"), html.escape(short),
        html.escape(facts["promise"]),
        _at_a_glance([(SH.T("Paths", "路线"), mediums),
                      (SH.T("Level", "难度"), tracks_for[0]["track"]["level"] if tracks_for
                       else SH.T("Beginner to intermediate", "入门到中级")),
                      (SH.T("Lesson", "课文"), facts["lesson_length"]),
                      (SH.T("Lab", "实验"), lab_time(deck["id"]))])
)
    # The module's landing point (#74): where to begin, or where the learner stopped. The build writes
    # "Start"; shell.js turns it into "Resume · slide N" from the stored position in this deck.
    first_unit = units[0] if units else None
    start = f"""<section class="module-start" data-module-start="{deck['id']}" aria-label="Start this module">
    <a class="btn-start" href="{site_base}/{first_unit['href'] if first_unit else deck['id'] + '.html'}" data-start-link>
      <svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M7 4l13 8-13 8z" fill="currentColor" stroke="none"/></svg>
      <span data-start-label>{SH.T("Start module", "开始本模块")}</span></a>
    <p class="module-start-note" data-start-note>{html.escape(SH.T(f"Begins with the {KIND_LABEL[first_unit['kind']].lower()}, then {len(units) - 1} more units.", f"从{KIND_LABEL_ZH[first_unit['kind']]}开始，之后还有 {len(units) - 1} 个单元。") if first_unit else "")}</p>
    <p class="module-next" data-module-next hidden>{SH.T("Next:", "下一步：")} <a href="#" data-module-next-link></a></p>
  </section>"""
    # The module at a glance (#99): the cover slide's figure — the whole system or method, with this
    # module's part marked — so the page opens on a picture of what is taught, not a list.
    hero_section = (f'<section class="path-section module-hero" aria-label="The module at a glance">{hero}</section>'
                    if hero else "")
    progress_note = SH.T(f"""Progress is recorded from what you do, never ticked by hand: a lesson unit
      when its narration plays through its last part or you read it to the end; the
      lab when its checklist is complete and its evidence entry is exported; the knowledge check at
      75%. It is stored in this browser only — <a href="{site_base}/index.html">export or import</a> it
      from the course home.""", f"""进度只根据你的实际操作记录，从不手动勾选：课文单元在讲解播放到最后一部分、或你读到结尾时记录；
      实验在清单完成且证据条目导出时记录；知识测验在达到 75% 时记录。进度只保存在此浏览器中——可在课程首页
      <a href="{site_base}/index.html">导出或导入</a>。""")
    body = f"""{head}
{start}
{hero_section}
  <section class="path-section">
    <h2>{SH.T("Learning objectives", "学习目标")}</h2>
    <ul class="objectives">{objectives_html}</ul>
  </section>
  <section class="path-section">
    <h2>{SH.T("Prerequisites", "前置条件")}</h2>
    <p>{html.escape(lab_prereq(deck['id']))}</p>
  </section>
{paths_section}
  <div class="section-heading">
    <h2>{SH.T("Units in this module", "本模块的单元")}</h2>
    <span class="section-note">{SH.T("Work them in order. Each unit opens where it is taught — its first part, the lab or the knowledge check.", "按顺序学习。每个单元都在它被讲授的地方打开——它的第一个部分、实验或知识测验。")}</span>
  </div>
  <div class="progress-wrap" data-module-progress="{deck['id']}" data-module-units="{",".join(f"{deck['id']}:{u['id']}" for u in units)}">
    <p class="progress-line">{SH.T(f'<strong data-progress-count>0 of {len(units)}</strong> units recorded', f'已记录 <strong data-progress-count>0 / {len(units)}</strong> 个单元')}
      <span class="progress-bar" role="progressbar" aria-label="Units recorded" aria-valuemin="0"
            aria-valuemax="{len(units)}" aria-valuenow="0"><span data-progress-fill></span></span></p>
    <p class="progress-note">{progress_note}</p>
  </div>
  <ol class="unit-list">
{chr(10).join(rows)}
  </ol>
  <section class="path-section">
    <a class="btn-quiet" href="{site_base}/transcript-{deck['id']}.html">{SH.T("Read the transcript", "阅读文字稿")}</a>
    <p class="index-footnote">{SH.T(f"Part of {path_link}.", f"属于{path_link}。")} {SH.T('This is the text-first copy: narration and captions are not published here, so units are read and presented rather than played.', '这是纯文本版：此处不发布讲解音频和字幕，所以单元以阅读为主，而不是播放。') if text_only else SH.T('Units carry narration, captions and a transcript.', '单元带有讲解、字幕和文字稿。')}</p>
  </section>"""
    return SH.document(f"{short} — module — AI Product Studio", facts["promise"], body, site_base,
                       "module-page", crumbs=SH.module_crumbs(site_base, deck, None),
                       deck_id=deck["id"], current="module", mode="overview")
