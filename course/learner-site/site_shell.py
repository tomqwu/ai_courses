"""The app shell (#73): one course outline and one top bar, on every page.

Before this, every page opened on a ~500px navy hero, and nothing on a page said where it sat in the
course: ten modules times nine tabs made about ninety pages with no outline between them. Now every
page is the same frame:

    skip link · course outline (264px, a drawer below 1024px) · top bar (breadcrumb, the four
    modes, search) · the page itself, its title in the content column

The outline is rendered at build time from the unit model the path and module pages already use
(`site_paths.module_units`), so it can only list units the site has. `shell.js` colours it from the
learner's stored progress — done, in progress, not started, each a different shape and a word, not
a colour alone — and follows the player from slide to slide.

`configure()` is called once per build with the parsed decks; every page generator then calls
`document()` (or, for the deck page, `sidebar()` and `topbar()` inside its own layout).
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

_CTX: dict = {"modules": [], "tracks": []}

# The four modes of a module (#74 folds the other tabs into them). Learn is the module as a narrated
# page (#112; the key stays "watch" so links and stored state keep resolving), Read the lesson text,
# Lab the exercise, Check the knowledge check.
# The edition being written (#121): "en" at the site root, "zh" in `zh/`. Set by build_site per
# edition; `T()` picks a template's own wording for it where a sentence carries markup.
LANG = "en"
# Whether the Chinese edition is built, so the language switch has somewhere to go.
EDITIONS = ("en",)


def T(en: str, zh: str) -> str:
    return zh if LANG == "zh" else en


FLAGS_PATH = Path(__file__).resolve().parent / "site-flags.json"


def flag(name: str) -> bool:
    """A site feature flag from site-flags.json (e.g. `pricing`); an unknown flag is off."""
    try:
        return bool(json.loads(FLAGS_PATH.read_text(encoding="utf-8")).get(name, False))
    except (OSError, ValueError):
        return False


MODES = (("watch", "Learn", "{d}.html"), ("read", "Read", "lesson-{d}.html"),
         ("lab", "Lab", "lab-{d}.html"), ("check", "Check", "quiz-{d}.html"))
# The modes' icons: shown only in the phone's bottom tab bar (#81), where the label alone is small.
MODE_ICONS = {
    "watch": '<path d="M8 5l11 7-11 7z"/>',
    "read": '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v16H6.5A2.5 2.5 0 0 0 4 21.5z"/><path d="M4 5.5v16"/>',
    "lab": '<path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.8 3h10.4a2 2 0 0 0 1.8-3l-5-9V3"/>',
    "check": '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l3 3 5-6"/>',
}

# One glyph with three states. CSS shows the ring, the half disc or the check according to the
# row's status class, so "done" and "in progress" differ in shape as well as colour; the word is in
# the row's visually hidden status text.
STATUS_ICON = ('<svg class="status-icon" viewBox="0 0 20 20" aria-hidden="true" focusable="false">'
               '<circle class="st-ring" cx="10" cy="10" r="7.6"/>'
               '<path class="st-half" d="M10 2.4a7.6 7.6 0 0 1 0 15.2z"/>'
               '<path class="st-check" d="M6.2 10.4l2.6 2.6 5-5.4"/></svg>')
STATUS_TEXT = '<span class="sr-only" data-status-text>not started</span>'

SEARCH_ICON = ('<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
               '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>')
MENU_ICON = ('<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
             '<path d="M4 7h16M4 12h16M4 17h16"/></svg>')
# The course mark: a cobalt tile with the A of the wordmark. Decorative — the name is always beside it.
BRAND_MARK = ('<svg class="brand-mark" viewBox="0 0 32 32" aria-hidden="true" focusable="false">'
              '<rect width="32" height="32" rx="7" fill="#2446c8"/>'
              '<path d="M9 21.6 16 9.4l7 12.2" fill="none" stroke="#f6f4ef" stroke-width="2.3" '
              'stroke-linejoin="round" stroke-linecap="round"/>'
              '<path d="M12.3 18.3h7.4" stroke="#f6f4ef" stroke-width="2.3" stroke-linecap="round"/>'
              '</svg>')
HOME_ICON = ('<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
             '<path d="M4 11l8-6 8 6v8a1 1 0 0 1-1 1h-4v-6h-6v6H5a1 1 0 0 1-1-1z"/></svg>')


# The outline's own names: one line each in a 264px column. A deck title such as "The On-Device AI
# App: Privacy, Testing, Shipping" wraps to three lines there, and two modules share its first half.
# A module missing here falls back to its title up to the colon.
OUTLINE_NAMES = {
    "m00": "Orientation", "m01": "The operating system", "m02": "On-device: architecture",
    "m03": "On-device: privacy & shipping", "m04": "Spec-driven SaaS", "m05": "Multi-tenant security",
    "m06": "The expertise product", "m07": "Monetize", "m08": "Launch & capstone",
    "m09": "Ship with GitHub Pages",
}


def short_label(deck: dict) -> str:
    return re.sub(r"^M\d+\s*—\s*", "", deck["label"]).strip()


OUTLINE_NAMES_ZH = {
    "m00": "导览", "m01": "操作系统", "m02": "端侧：架构", "m03": "端侧：隐私与发布",
    "m04": "规格驱动 SaaS", "m05": "多租户安全", "m06": "专业知识产品", "m07": "变现",
    "m08": "发布与毕业项目", "m09": "用 GitHub Pages 发布",
}


def outline_name(deck: dict) -> str:
    names = OUTLINE_NAMES_ZH if LANG == "zh" else OUTLINE_NAMES
    return names.get(deck["id"]) or short_label(deck).split(":")[0].strip()


def unit_href(deck_id: str, unit: dict) -> str:
    """Where a unit opens: the lab and the knowledge check have their own pages; the rest are slides."""
    if unit["kind"] == "lab":
        return f"lab-{deck_id}.html"
    if unit["kind"] == "quiz":
        return f"quiz-{deck_id}.html"
    return unit["href"]


def unit_name(unit: dict) -> str:
    """`M2.1 One pipeline, two layers` for a segment; the unit's kind for the others."""
    if unit["kind"] == "segment":
        return f"{unit['id']} {unit['label']}"
    if unit["kind"] == "lab":
        return T(f"Lab M{int(unit['deck'][1:])}", f"实验 M{int(unit['deck'][1:])}")
    return T(unit["title"], {"Introduction": "导论", "Knowledge check": "知识测验", "Summary": "总结"}.get(unit["title"], unit["title"]))


def configure(decks: list[dict], units_by_deck: dict[str, list[dict]], tracks: list[dict]) -> None:
    """Record what the outline lists. Called once per build, before any page is written."""
    import site_paths as SP                                     # noqa: PLC0415 - avoids a cycle
    import site_content as SC                                   # noqa: PLC0415
    from narration_data import COURSE_DIR                       # noqa: PLC0415

    def terms(deck: dict) -> int:
        path = COURSE_DIR / deck["source"].rsplit("/", 1)[0] / "glossary.md"
        return len(SC.parse_glossary(SC.read(path))) if path.is_file() else 0
    _CTX["modules"] = [{"id": d["id"], "number": int(d["id"][1:]), "short": outline_name(d),
                        "units": units_by_deck.get(d["id"], []), "terms": terms(d)} for d in decks]
    shown = []
    for track in tracks:
        if track["status"] not in ("built", "full"):
            continue
        included: dict[str, list[str]] = {}
        for unit in SP.track_units(track, units_by_deck):
            included.setdefault(unit["deck"], []).append(f"{unit['deck']}:{unit['id']}")
        shown.append({"slug": track["slug"], "title": track["title"],
                      "href": track["page"] or "index.html",
                      "modules": [[deck_id, ids] for deck_id, ids in included.items()]})
    _CTX["tracks"] = shown


def _path_block(site_base: str) -> str:
    """The learner's path and its progress: one segment per module. Rendered for the full course;
    `shell.js` re-renders it for the path the learner last opened."""
    tracks = _CTX["tracks"]
    track = next((t for t in tracks if t["slug"] == "aps"), tracks[0] if tracks else None)
    if not track:
        return ""
    segments = "".join(f'<li data-seg="{deck_id}"></li>' for deck_id, _ids in track["modules"])
    total = len(track["modules"])
    return (f'<section class="outline-path" aria-labelledby="outline-path-label" data-outline-path>'
            f'<p class="outline-label" id="outline-path-label">Your path</p>'
            f'<p class="outline-path-title"><a href="{site_base}/{track["href"]}" data-path-title>'
            f'{html.escape(track["title"])}</a></p>'
            f'<ol class="path-segments" aria-hidden="true" data-path-segments>{segments}</ol>'
            f'<p class="outline-path-count" data-path-count>0 of {total} modules complete</p>'
            f'<a class="outline-path-change" href="{site_base}/paths.html">Change path</a>'
            f'</section>')


def sidebar(site_base: str, deck_id: str | None = None, current: str | None = None) -> str:
    """The course outline.

    `deck_id` expands that module to its units. `current` names what this page is: "home",
    "module" (the module overview), a unit id ("M2.1", "lab", "quiz"…), one of the module's texts
    ("handout", "module-glossary", "transcript"), or the course's "glossary" or "evidence".
    """
    rows = []
    for module in _CTX["modules"]:
        mid = module["id"]
        unit_ids = ",".join(f"{mid}:{u['id']}" for u in module["units"])
        here = mid == deck_id
        link_current = ' aria-current="page"' if here and current == "module" else ""
        units = ""
        if here:
            items = []
            for unit in module["units"]:
                uid = f"{mid}:{unit['id']}"
                mark = ""
                if unit["id"] == current:
                    mark = ' aria-current="page"' if unit["kind"] in ("lab", "quiz") else ' aria-current="location"'
                items.append(
                    f'<li><a href="{site_base}/{unit_href(mid, unit)}" data-unit="{html.escape(uid)}"'
                    f' data-first="{unit["first"]}" data-last="{unit["last"]}"{mark}>'
                    f'{STATUS_ICON}<span class="outline-unit-name">{html.escape(unit_name(unit))}</span>'
                    f'{STATUS_TEXT}</a></li>')
            units = f'<ol class="outline-units" aria-label="Units in Module {module["number"]}">{"".join(items)}</ol>'
            # The module's reference texts, as the Watch artboard lists them under the units (#74).
            extras = []
            for key, label, href in (("handout", "Handout · one page", f"handout-{mid}.html"),
                                     ("module-glossary", f"Glossary · {module['terms']} terms",
                                      f"glossary-{mid}.html"),
                                     ("transcript", "Transcript", f"transcript-{mid}.html")):
                mark = ' aria-current="page"' if current == key else ""
                extras.append(f'<li><a href="{site_base}/{href}"{mark}>{label}</a></li>')
            units += f'<ul class="outline-extras" aria-label="Module {module["number"]} texts">{"".join(extras)}</ul>'
        rows.append(
            f'<li class="outline-module{" is-open" if here else ""}" data-module="{mid}"'
            f' data-module-units="{html.escape(unit_ids)}">'
            f'<a href="{site_base}/module-{mid}.html"{link_current}>{STATUS_ICON}'
            f'<span class="outline-num">M{module["number"]}</span>'
            f'<span class="outline-name">{html.escape(module["short"])}</span>{STATUS_TEXT}</a>'
            f'{units}</li>')
    tracks_json = html.escape(json.dumps(_CTX["tracks"], separators=(",", ":")), quote=True)
    deck_attr = f' data-deck="{deck_id}"' if deck_id else ""
    home_current = ' aria-current="page"' if current == "home" else ""
    foot = []
    for key, label, href in (("glossary", "Glossary", "glossary.html"),
                             ("evidence", "Your evidence log", "evidence.html")):
        mark = ' aria-current="page"' if current == key else ""
        foot.append(f'<a href="{site_base}/{href}"{mark}>{label}</a>')
    return (f'<nav class="app-outline" id="app-outline" aria-label="Course outline" data-outline'
            f' data-tracks="{tracks_json}"{deck_attr}>'
            f'<div class="outline-head">'
            f'<a class="outline-brand" href="{site_base}/index.html">{BRAND_MARK}'
            f'<span>AI Product Studio</span></a>'
            f'<button type="button" class="outline-close" data-outline-close aria-label="Close the outline">'
            f'<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
            f'<path d="M6 6l12 12M18 6L6 18"/></svg></button></div>'
            f'<button type="button" class="outline-search" data-search-open>{SEARCH_ICON}'
            f'<span>Search the course</span><kbd>⌘K</kbd></button>'
            f'{_path_block(site_base)}'
            f'<a class="outline-home" href="{site_base}/index.html"{home_current}>{HOME_ICON}Home</a>'
            f'<p class="outline-label" id="outline-modules-label">Modules</p>'
            f'<ol class="outline-modules" aria-labelledby="outline-modules-label">{"".join(rows)}</ol>'
            f'<div class="outline-foot">{"".join(foot)}</div>'
            f'</nav>')


MODE_HINTS = {
    "watch": ("Narrated, part by part", "逐部分讲解"),
    "read": ("The lesson as text", "课文全文"),
    "lab": ("Hands-on, pass/fail", "动手实验，通过/不通过"),
    "check": ("Test what you learned", "检验所学"),
}


def module_tabs(site_base: str, deck_id: str, mode: str | None) -> str:
    """The module's four modes as large tabs under the page title, on every module page. They stick
    under the top bar while the page scrolls. A phone shows the same modes as its bottom tab bar
    instead (the top bar's copy), so these are hidden there."""
    links = []
    for key, label, pattern in MODES:
        mark = ' aria-current="page"' if key == mode else ""
        hint = T(*MODE_HINTS[key])
        links.append(
            f'<a href="{site_base}/{pattern.format(d=deck_id)}"{mark}>'
            f'<svg class="icon tab-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{MODE_ICONS[key]}</svg>'
            f'<span class="tab-text"><span class="tab-name">{label}</span><span class="tab-hint">{hint}</span></span></a>')
    return f'<nav class="mode-tabs" aria-label="Module mode">{"".join(links)}</nav>'


def with_tabs(content: str, tabs: str) -> str:
    """The tabs go straight after the page title block, or first if a page has none."""
    start = content.find('<header class="page-head')
    end = content.find("</header>", start) if start >= 0 else -1
    if end < 0:
        return tabs + content
    end += len("</header>")
    return content[:end] + tabs + content[end:]


def topbar(site_base: str, crumbs: list[tuple[str, str | None]], deck_id: str | None = None,
           mode: str | None = None) -> str:
    """Breadcrumb, the module's four modes (on module pages), and search."""
    parts = []
    for label, href in crumbs:
        parts.append(f'<a href="{href}">{html.escape(label)}</a>' if href
                     else f'<span aria-current="page">{html.escape(label)}</span>')
    trail = '<span class="crumb-sep" aria-hidden="true">/</span>'.join(parts)
    modes = ""
    if deck_id:
        links = []
        for key, label, pattern in MODES:
            mark = ' aria-current="page"' if key == mode else ""
            icon = (f'<svg class="icon mode-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
                    f'{MODE_ICONS[key]}</svg>')
            links.append(f'<a href="{site_base}/{pattern.format(d=deck_id)}"{mark}>{icon}<span>{label}</span></a>')
        modes = f'<nav class="mode-switch" aria-label="Module mode">{"".join(links)}</nav>'
    # On a phone the breadcrumb gives way to a title: where you are, and what this page is (#81).
    where = crumbs[-2][0] if len(crumbs) > 1 else ""
    title = (f'<p class="app-bar-title" aria-hidden="true"><span>{html.escape(where)}</span>'
             f'<strong>{html.escape(crumbs[-1][0])}</strong></p>') if crumbs else ""
    return (f'<header class="app-bar">'
            f'<button type="button" class="app-bar-menu" data-outline-toggle aria-controls="app-outline"'
            f' aria-expanded="false">{MENU_ICON}<span>Outline</span></button>'
            f'<nav class="app-crumbs" aria-label="Breadcrumb">{trail}</nav>'
            f'{title}{modes}'
            f'{lang_switch(site_base)}'
            f'<button type="button" class="app-bar-search" data-search-open'
            f' aria-label="Search the course" title="Search the course (⌘K or /)">{SEARCH_ICON}</button>'
            f'</header>')


def lang_switch(site_base: str) -> str:
    """EN | 中文 (#116, #121): the same page in the other edition. The build points each link at the
    other edition's home; locale.js points it at this very page (and part) once the page loads."""
    if "zh" not in EDITIONS:
        return ""
    en_home = f"{site_base}/index.html"
    zh_home = "index.html" if LANG == "zh" else f"{site_base}/zh/index.html"
    here = ' aria-current="true"'
    return (f'<nav class="lang-switch" aria-label="Language · 语言">'
            f'<a href="{en_home}" data-lang="en" hreflang="en" lang="en"{here if LANG == "en" else ""}>EN</a>'
            f'<a href="{zh_home}" data-lang="zh" hreflang="zh-Hans" lang="zh-Hans"{here if LANG == "zh" else ""}>中文</a>'
            f'</nav>')


def module_crumbs(site_base: str, deck: dict, here: str | None) -> list[tuple[str, str | None]]:
    """Course / M2 · Short title / here."""
    module = (f"M{int(deck['id'][1:])} · {short_label(deck)}",
              None if here is None else f"{site_base}/module-{deck['id']}.html")
    trail = [("Course", f"{site_base}/index.html"), module]
    if here:
        trail.append((here, None))
    return trail


def page_head(kicker: str, title_html: str, lede_html: str = "", extra: str = "") -> str:
    """The page title, in the content column: no hero band (#73)."""
    kicker_html = f'<p class="page-kicker">{html.escape(kicker)}</p>' if kicker else ""
    lede = f'<p class="page-lede">{lede_html}</p>' if lede_html else ""
    return f'<header class="page-head">{kicker_html}<h1>{title_html}</h1>{lede}{extra}</header>'


def fonts(site_base: str) -> str:
    return (f'<link rel="preload" href="{site_base}/assets/fonts/ibm-plex-sans-latin.woff2" as="font" type="font/woff2" crossorigin>\n'
            f'<link rel="preload" href="{site_base}/assets/fonts/bricolage-grotesque-latin.woff2" as="font" type="font/woff2" crossorigin>\n'
            f'<link rel="stylesheet" href="{site_base}/assets/player.css">')


def document(title: str, description: str, content: str, site_base: str, body_class: str, *,
             crumbs: list[tuple[str, str | None]], deck_id: str | None = None,
             current: str | None = None, mode: str | None = None,
             scripts: tuple[str, ...] = (), body_attrs: str = "") -> str:
    """A whole page in the shell. `content` is everything inside <main>, page head included."""
    tags = "".join(f'<script src="{site_base}/assets/{s}" defer></script>'
                   for s in ("progress.js", "shell.js", "search.js", "figures.js", "terms.js") + tuple(scripts))
    deck_attr = f' data-deck="{deck_id}"' if deck_id else ""
    # Page links in the Chinese edition stay in `zh/`; assets and recordings are one level up.
    page_base = "." if LANG == "zh" else site_base
    ui = f'<script src="{site_base}/assets/ui-zh.js"></script>\n' if LANG == "zh" else ""
    return f"""<!doctype html>
<html lang="{'zh-Hans' if LANG == 'zh' else 'en'}"{' class="is-zh"' if LANG == 'zh' else ''} data-editions="{' '.join(EDITIONS)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
{fonts(site_base)}
{ui}<script src="{site_base}/assets/locale.js"></script>
</head>
<body class="app-page {body_class}" data-site-base="{site_base}" data-page-base="{page_base}" data-lang="{LANG}"{deck_attr}{body_attrs}>
<a class="skip-link" href="#content">Skip to content</a>
<div class="app">
{sidebar(site_base, deck_id, current)}
<div class="app-main">
{topbar(site_base, crumbs, deck_id, mode)}
<main id="content" class="app-content" tabindex="-1">
{with_tabs(content, module_tabs(site_base, deck_id, mode)) if deck_id and mode else content}
</main>
</div>
</div>
<div class="outline-backdrop" data-outline-backdrop hidden></div>
{tags}
</body>
</html>
"""

