# Beginner Ladder Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the machinery for a beginner ladder of L-modules on top of M0–M9, write the procedures for adding ladder content over time, and ship the pilot module **L1 — Your first website** in English and Chinese.

**Architecture:** One module registry (`course/06-production/modules.py`) replaces the ten hand-kept module lists and the `int(id[1:])` / `M\d+` assumptions, so an `l1` module builds, labels and links like an `m05`. Ladder units are ordinary Learn parts with five Markdown blocks (`:::ask`, `:::see`, `:::else`, `:::tools`, `:::peek`), checked by a new `verify.py` section and by the existing Chinese-edition parity check. The ladder is a new built path that the home page leads with; M-modules move under "Go deeper".

**Tech Stack:** Python 3.11 standard library (site generator, gate), vanilla JS (site), Playwright (browser checks), Markdown/JSON sources. Run everything with the repo's Python: locally `$SP/venv311/bin/python`, in CI `python3`.

Spec: `docs/superpowers/specs/2026-09-28-beginner-ladder-design.md`.

## Global Constraints

- Audience of L-modules: **non-coders who want to ship**. Every technical word is explained in the sentence that first uses it and is in the module glossary.
- Unit shape, always in this order: **story → do it (ask / see / else) → check it worked → peek inside**.
- Steps are **tool-agnostic**: "Ask your agent…"; where Claude Code, Codex, Cursor and Copilot differ, a collapsed `:::tools` note says how.
- **No fenced code and no repository path in an L-module outside `:::peek` and `:::ask`.**
- **Every `:::ask` step is run for real** before it ships; the run is kept in the module's `runs/run.json` with a dated transcript and screenshots.
- **Both editions**: an L-module ships with its `zh/` sources and `scripts-zh/` narration, parity-checked and stamped (`zh_edition.py`).
- M0–M9 content is **not rewritten** by this plan.
- AGENTS.md workflow: every change on a branch → gate → PR → merge with a **merge commit** on green → confirm the `deploy` job. Generated files are never committed (restore `manifest.json`, `provenance.json`, `transcripts` after local audio runs).
- Full local gate: copy `$SP/audio-state/*.json` into `course/06-production/narration/`, `make -C course transcripts`, `PYTHON=… bash course/check.sh`, then restore.

## File Structure

| File | Responsibility |
|---|---|
| `course/06-production/modules.py` (new) | The module registry: id, folder, family, tag, outline names, expected units, quiz size. Helpers used everywhere else. |
| `course/06-production/test_modules.py` (new) | Unit tests for the registry and id-agnostic label helpers. |
| `course/06-production/narration/narration_data.py` | `DECK_IDS` derived from the registry. |
| `course/06-production/verify.py`, `build-glossary.py`, `zh_edition.py` | Module lists and label patterns from the registry; new `check_ladder()`. |
| `course/learner-site/site_paths.py`, `build_site.py`, `site_shell.py`, `site_pages.py`, `site_content.py`, `check_player.py` | Id-agnostic numbering/labels; family-aware unit model and quiz size; ladder blocks; ladder path; home layout. |
| `course/learner-site/ladder_blocks.py` (new) | Parse and render `:::ask / :::see / :::else / :::tools / :::peek` blocks, used by slides and documents. |
| `course/learner-site/test_ladder_blocks.py` (new) | Unit tests for the blocks. |
| `course/learner-site/assets/{home,shell,search,evidence}.js` | Read a module's `tag` instead of parsing its id. |
| `course/learner-site/assets/player.css` | Styles for the ladder blocks. |
| `course/01-design/content-standards.md`, `zh-translation-guide.md`, `ladder-jargon.json` (new) | "Writing for the ladder"; block markers in Chinese; the jargon list the gate checks. |
| `course/03-content/_templates/ladder-module/` (new) | A copyable, commented L-module skeleton. |
| `.claude/skills/course-content/SKILL.md`, `AGENTS.md` | The five procedures for adding ladder content; one rule. |
| `course/03-content/l1-first-website/` (new) | The pilot module, `zh/`, `runs/`. |
| `course/06-production/narration/scripts/l1.json`, `scripts-zh/l1.json` (new) | Its narration. |

---

### Task 1: The module registry, and labels that do not assume `m`

**Files:**
- Create: `course/06-production/modules.py`, `course/06-production/test_modules.py`
- Modify: `course/06-production/narration/narration_data.py:30`, `course/06-production/verify.py:36-40,441`, `course/06-production/build-glossary.py:20-25`, `course/06-production/zh_edition.py` (label patterns), `course/learner-site/site_paths.py` (`NUM`, `SEGMENT`, `LAB`, `QUIZ`, `:66`, `:79`, `:88`, `:707-708`, `:751-752`, `:733`, `:831`), `course/learner-site/build_site.py` (`KICKER_RE`, `DECK_LABEL_RE`, cover kicker, `:271`, `:458`, `:803-804`, `:824`, `:885`, `:895`, `:1311`), `course/learner-site/site_shell.py` (`OUTLINE_NAMES*`, `short_label`, `unit_name`, `configure`, outline number, crumbs), `course/learner-site/site_pages.py` (`short_label`, `READ_UNIT`, every `int(deck["id"][1:])`, master-glossary chips, evidence rows), `course/learner-site/site_content.py` (`SEGMENT`, objectives), `course/.github` n/a
- Test: `course/06-production/test_modules.py`, plus a byte-for-byte build comparison

**Interfaces:**
- Produces (`modules.py`):
  - `@dataclass(frozen=True) class Module: id: str; folder: str; family: str; outline_en: str; outline_zh: str; segments: tuple[int, int]; quiz: tuple[int, int]; figures: bool`
  - `MODULES: list[Module]` (order = outline order), `IDS: list[str]`
  - `get(module_id) -> Module`, `tag(module_id) -> str` (`"M5"`, `"L1"`), `number(module_id) -> int`, `family(module_id) -> str` (`"deep"` or `"ladder"`)
  - `next_id(module_id) -> str | None` (next module of the same family, in registry order)
  - `kicker(module_id, lang) -> str` (`"Module 5"` / `"模块 5"`; `"Ladder step 1"` / `"阶梯第 1 级"`)
  - regex source strings: `TAG = r"[ML]\d+"`, `SEG = r"[ML]\d+\.\d+"`
  - `expected_units() -> int` (sum over modules of intro + segments + lab + quiz + summary, using each module's declared segment count)

- [ ] **Step 1: Write the failing tests**

```python
# course/06-production/test_modules.py
import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import modules as M


class Registry(unittest.TestCase):
    def test_ids_are_unique_and_folders_exist(self):
        self.assertEqual(len(M.IDS), len(set(M.IDS)))
        for m in M.MODULES:
            self.assertTrue((M.CONTENT / m.folder).is_dir(), m.folder)
            self.assertTrue(m.folder.startswith(m.id + "-"), m.folder)

    def test_tags(self):
        self.assertEqual(M.tag("m05"), "M5")
        self.assertEqual(M.tag("m00"), "M0")
        self.assertEqual(M.tag("l1"), "L1")
        self.assertEqual(M.number("l1"), 1)
        self.assertEqual(M.family("l1"), "ladder")
        self.assertEqual(M.family("m09"), "deep")

    def test_next_stays_in_family(self):
        self.assertEqual(M.next_id("m04"), "m05")
        self.assertIsNone(M.next_id("m09"))

    def test_kicker(self):
        self.assertEqual(M.kicker("m05", "en"), "Module 5")
        self.assertEqual(M.kicker("m05", "zh"), "模块 5")
        self.assertEqual(M.kicker("l1", "en"), "Ladder step 1")
        self.assertEqual(M.kicker("l1", "zh"), "阶梯第 1 级")

    def test_expected_units_for_the_deep_modules(self):
        deep = [m for m in M.MODULES if m.family == "deep"]
        self.assertEqual(sum(4 + m.segments[0] for m in deep), 70)


if __name__ == "__main__":
    unittest.main()
```

`test_kicker` and `family("l1")` need an `l1` entry. Until Task 7 creates its folder, keep `test_ids_are_unique_and_folders_exist` honest by registering `l1` in Task 7, and in this task give `tag`/`number`/`family`/`kicker` a code path that works for any id matching `^[ml]\d+$` (they parse the id; `get()` is only for registry fields).

- [ ] **Step 2: Run the tests to see them fail**

Run: `cd course/06-production && $PY test_modules.py`
Expected: `ModuleNotFoundError: No module named 'modules'`

- [ ] **Step 3: Write `modules.py`**

```python
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
```

- [ ] **Step 4: Run the tests**

Run: `cd course/06-production && $PY test_modules.py`
Expected: `test_kicker` passes for `m05` and the `l1` asserts pass (they parse the id); all tests `OK`.

- [ ] **Step 5: Snapshot the current build, to prove the refactor changes nothing**

```bash
cd course/learner-site && $PY build_site.py >/dev/null
rm -rf $SP/before && mkdir -p $SP/before && cp -R *.html zh search.json $SP/before/
```

- [ ] **Step 6: Point every module list at the registry**

`narration_data.py:30`:
```python
sys.path.insert(0, str(NARRATION_DIR.parent))
import modules as _MODULES                                  # noqa: E402
DECK_IDS = list(_MODULES.IDS)
```
(add `import sys` at the top).

`verify.py:36-40` → `MODULES = [m.folder for m in _M.MODULES]`; `:441` → `FIGURE_MODULES = [m.id for m in _M.MODULES if m.figures]` (import `modules as _M` after `sys.path` setup at the top of verify.py).

`build-glossary.py:20-25` → `MODULES = [m.folder for m in M.MODULES]`, `LABEL = {m.folder: M.tag(m.id) for m in M.MODULES}`.

`zh_edition.py`: the two `rf"^M{int(deck_id[1:])}\s*—\s*\S"` checks → `rf"^{M.tag(deck_id)}\s*—\s*\S"`; the segment-heading pattern `(M\d+\.\d+)` → `({M.SEG})`.

`site_shell.py`: delete `OUTLINE_NAMES`, `OUTLINE_NAMES_ZH`; `outline_name(deck)` returns `MOD.get(deck["id"]).outline_zh if LANG == "zh" else ….outline_en`; `short_label` uses `re.sub(rf"^{MOD.TAG}\s*—\s*", "", …)`; `unit_name` lab → `T(f"Lab {MOD.tag(d)}", f"实验 {MOD.tag(d)}")`; `configure` stores `"tag": MOD.tag(d["id"])` beside `"number"`, and the outline prints `{module["tag"]}` instead of `M{module["number"]}`; module crumbs use `MOD.tag(deck["id"])`.

`site_paths.py`: `NUM = re.compile(r"^[mMlL](\d+)$")`; `SEGMENT = re.compile(rf"^{MOD.SEG}$")`; `LAB = re.compile(rf"^(?:Lab|实验)\s*{MOD.TAG}")`; `QUIZ = re.compile(rf"^(?:Quiz|测验)\s*{MOD.TAG}")`; the lab-label `re.sub` and both `short` `re.sub`s use `MOD.TAG`; `module_units` synthetic segment id `f"{MOD.tag(deck['id'])}.1"`; every `f"Module {number}"` / `SH.T(f"Module {number}"…)` → `MOD.kicker(deck["id"], SH.LANG)`.

`build_site.py`: `KICKER_RE` replaces each `M\d+` with `[ML]\d+` (`Lab\s+[ML]\d+`, `实验\s*[ML]\d+`, `Segment\s+[ML]\d+(?:\.\d+)?`, and the leading `[ML]\d+(?:\.\d+)?`); `DECK_LABEL_RE = re.compile(rf"^({MOD.TAG})\s*—\s*(.+)$")`; cover kicker → `f"AI Product Studio · {MOD.kicker(deck_id, lang)}"` (drop "of N"); `:271` chapter test → `re.fullmatch(MOD.SEG, kicker)`; `slide_cta` patterns use `MOD.TAG`; `learn_page` `number`/`short` via `MOD`, `next_module = MOD.next_id(deck["id"])` and the "Next module" link falls back to `index.html` when it is `None`; index cards use `MOD.kicker`; `home_data` gains `"tag": MOD.tag(deck["id"])` and `"family": MOD.family(deck["id"])`.

`site_pages.py`: `short_label` → `SH.short_label`; `READ_UNIT` second entry → `re.compile(r"^(?:Segment\s+)?([ML]\d+\.\d)\b")`; each `f"Module {number}"` kicker → `MOD.kicker(deck["id"], SH.LANG)`; master-glossary chips `M{int(m[1:])}` → `{MOD.tag(m)}`; evidence rows → `MOD.kicker(lab["deck"], SH.LANG)`.

`site_content.py:294` `SEGMENT = re.compile(r"\b([ML])(\d+)\.(\d+)\b")`, and the two `f"M{seg.group(1)}.{seg.group(2)}"` → `f"{seg.group(1)}{seg.group(2)}.{seg.group(3)}"`.

In each file import the registry the way the file already imports narration helpers: `sys.path` already includes `course/06-production` in build_site; add `sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "06-production"))` where missing, then `import modules as MOD`.

- [ ] **Step 7: Rebuild and compare byte for byte**

```bash
cd course/learner-site && $PY build_site.py >/dev/null
for f in $(cd $SP/before && find . -type f); do cmp -s "$SP/before/$f" "$f" || echo "DIFF $f"; done
```
Expected: only lines where the cover kicker lost "of 10" (every `mNN.html` and `zh/mNN.html` cover) differ. Inspect one: `diff <(grep -o 'Module 5[^<]*' $SP/before/m05.html) <(grep -o 'Module 5[^<]*' m05.html)` shows `Module 5 of 10` → `Module 5`. Anything else differing is a regression — fix it before going on.

- [ ] **Step 8: Run the tests and the fast gate**

Run: `$PY course/06-production/test_modules.py && $PY course/learner-site/test_figures.py && $PY course/06-production/verify.py`
Expected: `OK`, `OK`, and verify's sections all `PASS` except the local-audio narration contract (which passes in the full procedure).

- [ ] **Step 9: Commit**

```bash
git add course/06-production/modules.py course/06-production/test_modules.py course/06-production course/learner-site
git commit -m "One module registry; labels and numbers no longer assume m-ids (#ladder)"
```

---

### Task 2: Scripts read a module's tag instead of parsing its id

**Files:**
- Modify: `course/learner-site/assets/shell.js:33`, `assets/home.js:38,50,54,65`, `assets/search.js:162,189`, `assets/evidence.js:24`, `course/learner-site/site_pages.py` (`search_index` records), `course/learner-site/site_shell.py` (`evidence` page data)
- Test: `course/learner-site/check_features.py` (existing home/search/evidence tests; one new assertion)

**Interfaces:**
- Consumes: `home_data.modules[id].tag` (Task 1); search index entries gain `"g"` (the module tag).
- Produces: JS uses `mod.tag` / `it.g`; a last-position href matches `/^([a-z]\d+)\.html#slide-(\d+)/`.

- [ ] **Step 1: Add the failing assertion** to `check_features.py`, after the search tests:

```python
    tags = page.evaluate("""async () => {
      const idx = await fetch('search.json').then(r => r.json());
      return [...new Set(idx.filter(x => x.d).map(x => x.g))]; }""")
    need(tags and all(t and t[0] in "ML" for t in tags), f"search: entries carry no module tag ({tags[:3]})")
```

- [ ] **Step 2: Run it to see it fail**

Run: `$PY course/learner-site/build_site.py >/dev/null && $PY course/learner-site/check_features.py`
Expected: `✗ search: entries carry no module tag`

- [ ] **Step 3: Implement**

`site_pages.search_index`: every `out.append({... "d": r["deck"], ...})` also sets `"g": MOD.tag(r["deck"])`; unit records likewise.

`shell.js:33` and `home.js:38`: `/^(m\d+)\.html#slide-(\d+)/` → `/^([a-z]\d+)\.html#slide-(\d+)/`.

`home.js:50` `'Module ' + mod.number` → `mod.kicker`; `:54` `'M' + mod.number` → `mod.tag`; `:65` `'Next in Module ' + mod.number` → `'Next in ' + mod.kicker` (add `"kicker": MOD.kicker(id, SH.LANG)` to `home_data` in build_site, and a `^Next in (.+)$` → `$1 的下一步` pattern to `ui-zh.json`).

`search.js:162,189` `'M' + parseInt(it.d.slice(1), 10)` → `(it.g || '')`.

`evidence.js:24` `'Module ' + parseInt(deck.slice(1), 10)` → read `row.getAttribute('data-kicker')`, and `site_pages.evidence_page` writes `data-kicker="{MOD.kicker(lab['deck'], SH.LANG)}"` on each row.

- [ ] **Step 4: Run the checks**

Run: `$PY course/learner-site/build_site.py >/dev/null && $PY course/learner-site/check_features.py`
Expected: `site features: PASS`

- [ ] **Step 5: Commit**

```bash
git add course/learner-site
git commit -m "Site scripts read a module's tag, not its id (#ladder)"
```

---

### Task 3: Family rules — how many segments and questions a module has

**Files:**
- Modify: `course/learner-site/site_content.py:420` (quiz size), `course/learner-site/check_player.py:~423-431` (segment count, unit total), `course/06-production/verify.py` (`ARTIFACTS` by family)
- Test: `course/06-production/test_modules.py` (new cases)

**Interfaces:**
- Consumes: `Module.segments`, `Module.quiz`, `MOD.expected_units()`, `MOD.family()`.
- Produces: `verify.ARTIFACTS_LADDER` (dict like `ARTIFACTS`), `verify.artifacts_for(folder) -> dict`.

- [ ] **Step 1: Failing test**

```python
    def test_ladder_modules_declare_smaller_checks(self):
        for m in M.MODULES:
            if m.family == "ladder":
                self.assertEqual(m.quiz, (4, 5))
                self.assertEqual(m.segments, (3, 4))
                self.assertFalse(m.figures)
```
(add to `Registry`). It passes vacuously until Task 7 registers `l1`; Task 7's registration must satisfy it.

- [ ] **Step 2: Implement the family rules**

`site_content.parse_quiz` — replace the fixed count:
```python
    lo, hi = MOD.get(deck_id).quiz if deck_id in MOD.IDS else (8, 8)
    if not lo <= len(questions) <= hi:
        problems.append(f"expected {lo}–{hi} questions, parsed {len(questions)}" if lo != hi
                        else f"expected {lo} questions, parsed {len(questions)}")
```

`check_player.check_units`:
```python
        lo, hi = MOD.get(deck_id).segments
        if not lo <= kinds.count("segment") <= hi:
            problems.append(f"{deck_id}: {kinds.count('segment')} segment units, expected {lo}–{hi}")
    ...
    # Declared per module in the registry, not re-counted: a deck edit that moves a unit boundary
    # should fail here. A ladder module with a fourth segment declares (4, 4).
    if total != MOD.expected_units():
        problems.append(f"unit model yields {total} units, expected {MOD.expected_units()}")
```
and replace the literal `70` comment accordingly.

`verify.py`:
```python
# A ladder module is written for non-coders: no facilitation guide, solutions or accessibility
# notes of its own (the deep modules keep theirs); its build is proven by runs/run.json instead.
ARTIFACTS_LADDER = {
    "slides.md": None,
    "handout.md": (250, 650),
    "glossary.md": (200, 900),
    "lab-rubrics.md": (150, 700),
}


def artifacts_for(folder: str) -> dict:
    return ARTIFACTS_LADDER if folder.startswith("l") else ARTIFACTS
```
and `check_artifacts()` iterates `artifacts_for(module).items()`.

- [ ] **Step 3: Run**

Run: `$PY course/06-production/test_modules.py && $PY course/06-production/verify.py | grep -E "Artifacts|RESULT"`
Expected: `OK`; `[PASS] Artifacts + length bands`.

- [ ] **Step 4: Commit**

```bash
git add course/06-production course/learner-site
git commit -m "Module families: ladder modules have 3–4 segments and a 4–5 question check (#ladder)"
```

---

### Task 4: The ladder blocks — ask, see, else, tools, peek

**Files:**
- Create: `course/learner-site/ladder_blocks.py`, `course/learner-site/test_ladder_blocks.py`
- Modify: `course/learner-site/build_site.py` (`render_blocks`), `course/learner-site/site_content.py` (`render_document`), `course/learner-site/assets/player.css`, `course/learner-site/ui-zh.json`, `course/06-production/zh_edition.py` (parity), `course/01-design/zh-translation-guide.md`

**Interfaces:**
- Produces (`ladder_blocks.py`):
  - `KINDS = ("ask", "see", "else", "tools", "peek")`
  - `split(lines: list[str]) -> list[tuple[str, list[str]]]` — `("md", lines)` runs and `(kind, body_lines)` blocks, in order
  - `render(kind: str, body_html: str, lang: str) -> str`
  - `count(text: str) -> dict[str, int]` — blocks of each kind in a Markdown text

Syntax (the same in both editions; only the text inside is translated):

```text
:::ask
Make a one-page website for my bakery. Show today's bread with prices, and a line that says
pre-orders close at 8 pm.
:::
:::see
![The page in a browser: a heading "Maria's Bakery" and three loaves with prices](runs/2026-10-01/step-2.png)
A page with your bakery's name at the top and your bread below it.
:::
:::else
- **The agent asks which tool to use** — answer: "Plain HTML and CSS, one file, no framework."
- **The page is unstyled** — ask: "Add simple styling: a warm background and a readable font."
:::
:::tools
- **Claude Code** — run it in the folder you want the site in.
- **Cursor / Copilot** — open the folder first, then paste the request into the chat.
:::
:::peek
ai_qe is a GitHub Pages site too. Its pages are plain files like yours …
→ [M9, part 12](m09.html#slide-12)
:::
```

- [ ] **Step 1: Failing tests**

```python
# course/learner-site/test_ladder_blocks.py
import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ladder_blocks as L

SAMPLE = """Intro line.
:::ask
Make a one-page website.
:::
:::see
You see a page.
:::
:::else
- **Blank page** — ask again.
:::
:::peek
`index.html` is the page.
:::
After."""


class Blocks(unittest.TestCase):
    def test_split_keeps_order(self):
        kinds = [k for k, _ in L.split(SAMPLE.splitlines())]
        self.assertEqual(kinds, ["md", "ask", "see", "else", "peek", "md"])

    def test_count(self):
        self.assertEqual(L.count(SAMPLE), {"ask": 1, "see": 1, "else": 1, "tools": 0, "peek": 1})

    def test_unclosed_block_is_an_error(self):
        with self.assertRaises(L.BlockError):
            L.split([":::ask", "text"])

    def test_render_labels_by_language(self):
        self.assertIn("Ask your agent", L.render("ask", "<p>x</p>", "en"))
        self.assertIn("让你的 AI 助手", L.render("ask", "<p>x</p>", "zh"))
        self.assertIn("<details", L.render("peek", "<p>x</p>", "en"))
        self.assertIn("<details", L.render("tools", "<p>x</p>", "en"))
        self.assertIn("data-copy", L.render("ask", "<p>x</p>", "en"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run to see it fail**

Run: `cd course/learner-site && $PY test_ladder_blocks.py`
Expected: `ModuleNotFoundError: No module named 'ladder_blocks'`

- [ ] **Step 3: Implement `ladder_blocks.py`**

```python
# course/learner-site/ladder_blocks.py
"""The blocks a ladder unit is built from (#ladder): what to ask your agent, what you should see,
what to do if you see something else, notes for a particular agent, and — collapsed — how the real
product does it.

    :::ask            the request to paste; a Copy button
    :::see            a screenshot and what it shows
    :::else           the common problems and what to type next
    :::tools          where Claude Code, Codex, Cursor and Copilot differ; collapsed
    :::peek           the case study, code and pointers; collapsed by default

The markers are the same in both editions; only the text inside is translated.
"""
from __future__ import annotations

KINDS = ("ask", "see", "else", "tools", "peek")
LABELS = {
    "en": {"ask": "Ask your agent", "see": "You should see", "else": "If you see something else",
           "tools": "Using Claude Code, Codex, Cursor or Copilot",
           "peek": "Peek inside — how the real product does it", "copy": "Copy"},
    "zh": {"ask": "让你的 AI 助手这样做", "see": "你应该看到", "else": "如果你看到的不一样",
           "tools": "使用 Claude Code、Codex、Cursor 或 Copilot 时",
           "peek": "看看里面——真实产品是怎么做的", "copy": "复制"},
}


class BlockError(ValueError):
    pass


def split(lines: list[str]) -> list[tuple[str, list[str]]]:
    out: list[tuple[str, list[str]]] = []
    buf: list[str] = []
    kind: str | None = None
    for n, line in enumerate(lines, 1):
        s = line.strip()
        if kind is None and s.startswith(":::") and s[3:] in KINDS:
            if buf:
                out.append(("md", buf))
            buf, kind = [], s[3:]
        elif kind is not None and s == ":::":
            out.append((kind, buf))
            buf, kind = [], None
        elif kind is None and s.startswith(":::") and s != ":::":
            raise BlockError(f"line {n}: unknown block {s!r} (one of {', '.join(KINDS)})")
        else:
            buf.append(line)
    if kind is not None:
        raise BlockError(f"a :::{kind} block is not closed")
    if buf:
        out.append(("md", buf))
    return out


def count(text: str) -> dict[str, int]:
    found = {k: 0 for k in KINDS}
    for kind, _ in split(text.splitlines()):
        if kind in found:
            found[kind] += 1
    return found


def render(kind: str, body_html: str, lang: str) -> str:
    t = LABELS["zh" if lang == "zh" else "en"]
    if kind in ("peek", "tools"):
        return (f'<details class="ladder-{kind}"><summary>{t[kind]}</summary>'
                f'<div class="ladder-peek-body">{body_html}</div></details>')
    copy = (f'<button type="button" class="ladder-copy" data-copy>{t["copy"]}</button>'
            if kind == "ask" else "")
    return (f'<div class="ladder-{kind}"><p class="ladder-label">{t[kind]}</p>'
            f'<div class="ladder-body">{body_html}</div>{copy}</div>')
```

- [ ] **Step 4: Wire the blocks into both renderers**

`build_site.render_blocks(lines, diagram, sentences)` — at the top:
```python
    parts = LB.split(lines)
    if len(parts) > 1 or parts and parts[0][0] != "md":
        return "\n".join(render_blocks(body, diagram, sentences) if kind == "md"
                         else LB.render(kind, render_blocks(body, "", sentences), SH.LANG)
                         for kind, body in parts)
```
(`import ladder_blocks as LB`; catch `LB.BlockError` in `parse_deck` and raise `SystemExit(f"{deck_id} part {index}: {exc}")`).

`site_content.render_document(text, …)` — the same split first; `md` runs go through the existing loop, blocks are rendered with `render_document(body)[0]` inside `LB.render(kind, …, lang)`, where `lang` is passed in by `site_pages.document_page` as `SH.LANG` (add a `lang: str = "en"` parameter).

A Copy button's script: in `assets/learn.js` and `assets/lab.js` (both pages can show `:::ask`), one delegated listener:
```js
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-copy]');
    if (!b) return;
    var text = b.parentElement.querySelector('.ladder-body').innerText.trim();
    if (navigator.clipboard) navigator.clipboard.writeText(text).then(function () {
      var was = b.textContent; b.textContent = '✓'; setTimeout(function () { b.textContent = was; }, 1200);
    });
  });
```
Put it once in `assets/shell.js` (loaded on every page) instead of twice.

CSS in `player.css` (tokens only, no hex):
```css
/* Ladder blocks (#ladder): ask → see → else, and a collapsed peek inside. */
.ladder-ask, .ladder-see, .ladder-else { position: relative; margin: 14px 0; padding: 12px 16px;
  border-radius: 10px; border: 1px solid var(--line); background: var(--surface); }
.ladder-ask { border-color: var(--accent); background: var(--accent-soft); }
.ladder-else { background: var(--wash); }
.ladder-label { margin: 0 0 6px; color: var(--accent-deep); font-size: var(--d-2); font-weight: 650;
  letter-spacing: .06em; text-transform: uppercase; }
.ladder-copy { position: absolute; top: 10px; right: 10px; min-height: 36px; padding: 0 12px;
  border: 1px solid var(--line); border-radius: 8px; background: var(--surface); }
.ladder-see img { max-width: 100%; height: auto; border-radius: 8px; border: 1px solid var(--line); }
.ladder-peek, .ladder-tools { margin: 14px 0; border-top: 1px dashed var(--line); padding-top: 8px; }
.ladder-peek summary, .ladder-tools summary { cursor: pointer; color: var(--ink-soft); font-weight: 600; }
@media (max-width: 480px) { .ladder-copy { position: static; margin-top: 8px; min-height: 44px; } }
```

`zh_edition.py` — parity: in `check_slides` per part and in `check_document`, add
```python
        if LB.count(a) != LB.count(b):
            problems.append(f"{where}: ladder blocks differ ({LB.count(b)} vs the English {LB.count(a)})")
```
(`sys.path` already includes learner-site; `import ladder_blocks as LB`). Blocks are outside fences, so `outside_fences()` is unaffected.

`zh-translation-guide.md` — under "Markers the site reads", add: "Ladder blocks keep their markers (`:::ask`, `:::see`, `:::else`, `:::tools`, `:::peek`, closing `:::`); translate what is inside, including the request in `:::ask` — a Chinese learner pastes a Chinese request."

- [ ] **Step 5: Run the tests and a build**

Run: `cd course/learner-site && $PY test_ladder_blocks.py && $PY build_site.py >/dev/null && $PY check_features.py | tail -1`
Expected: `OK`; build succeeds (no module uses the blocks yet, so the output is unchanged); `site features: PASS`.

- [ ] **Step 6: Commit**

```bash
git add course/learner-site course/06-production/zh_edition.py course/01-design/zh-translation-guide.md
git commit -m "Ladder blocks: ask, see, else, tool notes and a collapsed peek inside (#ladder)"
```

---

### Task 5: The ladder checks in the gate

**Files:**
- Create: `course/01-design/ladder-jargon.json`
- Modify: `course/06-production/verify.py` (new `check_ladder()` and its entry in `sections`)
- Test: `course/06-production/test_ladder_check.py` (new)

**Interfaces:**
- Consumes: `LB.split`, `MOD.MODULES`, the built site (`learner-site/*.html`) for link targets.
- Produces: `verify.ladder_problems(folder: Path, module_id: str, site: Path) -> list[str]` (pure, testable), and `check_ladder()` running it for every ladder module.

Rules checked (each is one clause of the spec's writing standard):
1. Outside `:::peek`, `:::tools` and `:::ask`, no fenced block and no repository pointer (`POINTER_TOKEN` from build_site).
2. English sentences outside blocks ≤ 28 words; Chinese sentences ≤ 70 characters.
3. Every word in `ladder-jargon.json` that appears outside `:::peek` also appears as a term in that module's `glossary.md` (`SC.parse_glossary`, compared case-insensitively on the term's stem).
4. Every link inside `:::peek` whose target is `mNN.html#slide-N` resolves: the page exists in the built site and has `id="slide-N"`.
5. `runs/run.json` exists, lists one entry per `:::ask` in `lab.md` and `slides.md` combined (`{"step": "slides part 5 ask 1", "date": "YYYY-MM-DD", "agent": "…", "transcript": "runs/…md", "screenshot": "runs/…png"}`), and every file it names exists.

- [ ] **Step 1: Failing tests**

```python
# course/06-production/test_ladder_check.py
import json, sys, tempfile, unittest
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify as V


def module(tmp: Path, slides: str, runs: list[dict] | None) -> Path:
    d = tmp / "l9-test"; d.mkdir()
    (d / "slides.md").write_text(slides, encoding="utf-8")
    for name in ("lesson", "handout", "lab", "quiz"):
        (d / f"{name}.md").write_text("# x\n\nPlain words.\n", encoding="utf-8")
    (d / "glossary.md").write_text("# G\n\n**Website** — pages on the internet.\n", encoding="utf-8")
    if runs is not None:
        (d / "runs").mkdir()
        for r in runs:
            for key in ("transcript", "screenshot"):
                (d / r[key]).write_text("x", encoding="utf-8")
        (d / "runs" / "run.json").write_text(json.dumps({"steps": runs}), encoding="utf-8")
    return d


class LadderCheck(unittest.TestCase):
    def test_code_outside_peek_fails(self):
        with tempfile.TemporaryDirectory() as t:
            d = module(Path(t), "---\ntitle: L9 — T\n---\n## A\n\n```bash\nls\n```\n", [])
            self.assertTrue(any("code" in p for p in V.ladder_problems(d, "l9", Path(t))))

    def test_code_inside_peek_passes(self):
        with tempfile.TemporaryDirectory() as t:
            d = module(Path(t), "---\ntitle: L9 — T\n---\n## A\n\n:::peek\n```bash\nls\n```\n:::\n", [])
            self.assertFalse([p for p in V.ladder_problems(d, "l9", Path(t)) if "code" in p])

    def test_every_ask_has_a_run(self):
        with tempfile.TemporaryDirectory() as t:
            d = module(Path(t), "---\ntitle: L9 — T\n---\n## A\n\n:::ask\nMake a page.\n:::\n", None)
            self.assertTrue(any("run.json" in p for p in V.ladder_problems(d, "l9", Path(t))))

    def test_long_sentence_fails(self):
        long = " ".join(["word"] * 40) + "."
        with tempfile.TemporaryDirectory() as t:
            d = module(Path(t), f"---\ntitle: L9 — T\n---\n## A\n\n{long}\n", [])
            self.assertTrue(any("sentence" in p for p in V.ladder_problems(d, "l9", Path(t))))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run to see it fail**

Run: `cd course/06-production && $PY test_ladder_check.py`
Expected: `AttributeError: module 'verify' has no attribute 'ladder_problems'`

- [ ] **Step 3: Implement**

`course/01-design/ladder-jargon.json`:
```json
{
 "_about": "Words a ladder module may only use once its glossary explains them (#ladder). Grow the list when a reviewer finds a word a non-coder would stumble on.",
 "words": ["repository", "commit", "terminal", "server", "database", "deploy", "API", "framework",
           "branch", "localhost", "HTML", "CSS", "JavaScript", "token", "model", "authentication",
           "tenant", "endpoint", "Xcode", "simulator", "compile"]
}
```

`verify.py`:
```python
def ladder_problems(folder: Path, module_id: str, site: Path) -> list[str]:
    """The writing standard for ladder modules (content-standards.md, "Writing for the ladder")."""
    sys.path.insert(0, str(ROOT / "learner-site"))
    import ladder_blocks as LB                                                  # noqa: PLC0415
    import site_content as SC                                                   # noqa: PLC0415
    problems: list[str] = []
    jargon = json.loads((ROOT / "01-design" / "ladder-jargon.json").read_text(encoding="utf-8"))["words"]
    glossary = " ".join(t["term"].lower() for t in SC.parse_glossary(
        (folder / "glossary.md").read_text(encoding="utf-8")))
    pointer = re.compile(r"\b(?:ListenToMe|SignUpFlow|ai_qe)/\S+")
    asks = 0
    for name in ("slides", "lesson", "handout", "lab", "quiz"):
        text = (folder / f"{name}.md").read_text(encoding="utf-8")
        for kind, body in LB.split(text.splitlines()):
            chunk = "\n".join(body)
            if kind == "ask":
                asks += name in ("slides", "lab")
                continue
            if kind == "tools":
                continue
            if kind == "peek":
                for target, anchor in re.findall(r"\]\((m\d\d\.html)#(slide-\d+)\)", chunk):
                    page = site / target
                    if page.is_file() and f'id="{anchor}"' not in page.read_text(encoding="utf-8"):
                        problems.append(f"{module_id}/{name}.md: peek link {target}#{anchor} has no such part")
                continue
            prose = re.sub(r"<!--.*?-->", " ", chunk, flags=re.S)
            if re.search(r"^```(?!figure)", prose, re.M):
                problems.append(f"{module_id}/{name}.md: code outside :::peek and :::ask")
            if pointer.search(prose):
                problems.append(f"{module_id}/{name}.md: repository path outside :::peek")
            for sentence in re.split(r"(?<=[.!?。！？])\s*", re.sub(r"```.*?```", " ", prose, flags=re.S)):
                words = len(sentence.split())
                cjk = len(re.findall(r"[一-鿿]", sentence))
                if words > 28 or cjk > 70:
                    problems.append(f"{module_id}/{name}.md: sentence too long for a non-coder: {sentence[:60]!r}…")
            for word in jargon:
                if re.search(rf"\b{re.escape(word)}\b", prose, re.I) and word.lower() not in glossary:
                    problems.append(f"{module_id}/{name}.md: {word!r} is used but not in the glossary")
    run = folder / "runs" / "run.json"
    if not run.is_file():
        problems.append(f"{module_id}: runs/run.json is missing — every :::ask step is run for real")
    else:
        steps = json.loads(run.read_text(encoding="utf-8")).get("steps", [])
        if len(steps) != asks:
            problems.append(f"{module_id}: runs/run.json records {len(steps)} runs for {asks} :::ask steps")
        for s in steps:
            for key in ("transcript", "screenshot"):
                if not (folder / s.get(key, "")).is_file():
                    problems.append(f"{module_id}: run {s.get('step')!r} names a missing {key}")
    return sorted(set(problems))


def check_ladder() -> list[str]:
    problems = []
    ladder = [m for m in _M.MODULES if m.family == "ladder"]
    for m in ladder:
        problems += ladder_problems(CONTENT / m.folder, m.id, ROOT / "learner-site")
    check_ladder.summary = f"{len(ladder)} ladder modules"
    return problems
```
(add `import json` at the top of verify.py if absent) and `("Ladder modules", check_ladder)` to `sections` after "Chinese edition".

- [ ] **Step 4: Run**

Run: `cd course/06-production && $PY test_ladder_check.py && $PY verify.py | grep -E "Ladder|RESULT"`
Expected: `OK`; `[PASS] Ladder modules (0 ladder modules)`.

- [ ] **Step 5: Add both new test files to the gate** (`course/check.sh`, after the figures unit tests):

```bash
step "unit tests — modules"         "$PYTHON" 06-production/test_modules.py
step "unit tests — ladder"          "$PYTHON" learner-site/test_ladder_blocks.py
step "unit tests — ladder check"    "$PYTHON" 06-production/test_ladder_check.py
```

- [ ] **Step 6: Commit**

```bash
git add course/01-design/ladder-jargon.json course/06-production course/check.sh
git commit -m "Gate: the ladder writing standard, peek links and real-run records (#ladder)"
```

---

### Task 6: The ladder leads the site

**Files:**
- Modify: `course/learner-site/site_paths.py` (`TRACKS`, `TRACKS_ZH`), `course/learner-site/build_site.py` (`index_page`: ladder section first, M-module grid under "Go deeper"), `course/learner-site/site_shell.py` (outline: ladder group above modules), `course/learner-site/ui-zh.json`
- Test: `course/learner-site/check_features.py` (new assertions), `course/learner-site/check_player.py` (track counts)

**Interfaces:**
- Consumes: `MOD.MODULES` families.
- Produces: a track `{"slug": "ladder", "title": "The ladder: from zero to shipped", "core": [ladder ids that exist], "status": "built", "page": "path-ladder.html", "measured": None, "counts_source": "the ladder modules themselves", …}` and its `TRACKS_ZH["ladder"]`.

- [ ] **Step 1: Failing assertions** in `check_features.py`, in the home section:

```python
    if (SITE / "module-l1.html").is_file():      # the ladder shows once it has a module
        need(page.locator(".ladder-rungs li").count() >= 1, "home: the ladder is not on the home page")
        first_h2 = page.evaluate("document.querySelector('.home-new h2, main h2')?.textContent || ''")
        need("ladder" in first_h2.lower() or "阶梯" in first_h2, f"home: the ladder is not first ({first_h2!r})")
        need(page.locator("text=Go deeper").count() >= 1, "home: the M-modules are not under 'Go deeper'")
```

- [ ] **Step 2: Run to see them fail** — `$PY check_features.py` → `✗ home: the ladder is not on the home page`.

- [ ] **Step 3: Implement**

`TRACKS` — first entry:
```python
    {
        # The beginner ladder (#ladder): for non-coders, from nothing installed to a product for sale.
        # Its core is the ladder modules that exist; rungs are added as their modules ship.
        "slug": "ladder",
        "title": "The ladder: from zero to shipped",
        "medium": "Website · web app · iPhone app",
        "kicker": "Start here · no coding background",
        "promise": "Build a website, a web app and an iPhone app with an AI agent — explained from "
                   "zero — then price and launch what you built.",
        "core": [m.id for m in MOD.MODULES if m.family == "ladder"],
        "slice": {},
        "excluded": [],
        "price": "Free while in preview",
        "level": "Beginner",
        "role": "Founder · Designer · Small-business owner",
        "subject": "Building with AI agents",
        "measured": None,
        "counts_source": "the ladder modules themselves",
        "status": "built",
        "page": "path-ladder.html",
    },
```
`TRACKS_ZH["ladder"] = {"title": "阶梯：从零到上线", "medium": "网站 · Web 应用 · iPhone 应用", "kicker": "从这里开始 · 无需编程背景", "promise": "借助 AI 助手构建一个网站、一个 Web 应用和一个 iPhone 应用——一切从零讲起——然后给你做的东西定价并发布。", "price": "预览期免费", "level": "入门", "role": "创始人 · 设计师 · 小企业主", "subject": "借助 AI 助手构建", "counts_source": "阶梯模块本身"}`.

`index_page`: before `paths_note`/`content`, build
```python
    ladder_ids = [m.id for m in MOD.MODULES if m.family == "ladder"]
    rungs = "".join(
        f'<li><a href="{site_base}/module-{d}.html"><span class="rung-tag">{MOD.tag(d)}</span>'
        f'<span class="rung-title">{html.escape(SH.short_label(decks_by_id[d]))}</span></a></li>'
        for d in ladder_ids)
    ladder_html = (f'<section class="ladder" aria-labelledby="ladder-title">'
                   f'<h2 id="ladder-title">{SH.T("The ladder: from zero to shipped", "阶梯：从零到上线")}</h2>'
                   f'<p class="section-note">{SH.T("For non-coders. Each step builds something real with your AI agent.", "写给不会编程的人。每一级都和你的 AI 助手一起做出一个真东西。")}</p>'
                   f'<ol class="ladder-rungs">{rungs}</ol></section>') if ladder_ids else ""
```
(`decks_by_id = {d["id"]: d for d in decks}`), insert `{ladder_html}` as the first thing after `{head}` in the first-time view and above "Start with what you want to build"; rename the "All modules" heading to `SH.T("Go deeper: the engineering modules", "深入：工程模块")` and render only `family == "deep"` cards there.

CSS: `.ladder-rungs { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 12px; list-style: none; padding: 0; }` and `.rung-tag { font-weight: 700; color: var(--accent-deep); margin-right: 8px; }`.

`site_shell.sidebar`: group ladder modules under a label `T("The ladder", "阶梯")` above `T("Modules", "模块")`.

`check_player.py` track assertions: skip `measured` cross-checks for `ladder` (it has `measured: None` already, so only confirm the loop's `not measured` branch accepts it).

- [ ] **Step 4: Run** — build, `$PY check_features.py` → `PASS`; `$PY check_player.py --all --strict-fit --print-skip` → passes (no ladder module yet: the ladder section is empty and hidden, the path page lists nothing — Task 7 fills it).

Because the ladder track is empty until Task 7, make both render nothing when `ladder_ids` is empty and have `check_features`'s new assertions run only when `(SITE / "module-l1.html").is_file()`.

- [ ] **Step 5: Commit**

```bash
git add course/learner-site
git commit -m "Home and paths lead with the ladder; M-modules under 'Go deeper' (#ladder)"
```

---

### Task 7: How to add ladder content — standard, template, skill, AGENTS

**Files:**
- Modify: `course/01-design/content-standards.md` (new section), `.claude/skills/course-content/SKILL.md` (five procedures), `AGENTS.md` (map row, rule), `course/learner-site/README.md` (ladder blocks)
- Create: `course/03-content/_templates/ladder-module/` with `README.md`, `slides.md`, `lesson.md`, `handout.md`, `glossary.md`, `lab.md`, `quiz.md`, `lab-rubrics.md`, `runs/run.json`, and `course/03-content/_templates/ladder-module/scripts.json`
- Test: the template is excluded from the build (folder starts with `_`, and `MOD.MODULES` does not list it); `verify.ladder_problems(template, "l9", site)` must return no problems — the template follows the rules it teaches, run files included — tested as `test_template_follows_the_standard` in `test_ladder_check.py`.

- [ ] **Step 1: Write the failing template test**

```python
    def test_template_follows_the_standard(self):
        template = HERE.parents[0] / "03-content" / "_templates" / "ladder-module"
        problems = V.ladder_problems(template, "l9", HERE.parents[0] / "learner-site")
        self.assertEqual(problems, [], problems)
```

- [ ] **Step 2: Run** → fails (`FileNotFoundError` on the template).

- [ ] **Step 3: Write the template.** Each file is a working, minimal ladder module about a toy goal ("a page that says hello"), with HTML comments saying what each part is for. `slides.md` has: cover (`title: L9 — Template title`, `Promise:` / `Duration:`), "By the end you can…", one unit with the four blocks in order (story paragraph + screenshot line, `:::ask`, `:::see`, `:::else`, a "Check it worked" list, `:::peek` linking `m09.html#slide-12`), `## Lab L9 — …`, `## Quiz L9 — …` (4 scenario questions in `quiz.md`), `## Recap`. `runs/run.json` has one entry per `:::ask` and the transcript/screenshot files it names (a 1×1 PNG and a short transcript) so the template passes its own check. `README.md` walks through copying it:

```text
cp -R course/03-content/_templates/ladder-module course/03-content/lN-your-slug
cp course/03-content/_templates/ladder-module/scripts.json course/06-production/narration/scripts/lN.json
# then: register lN in course/06-production/modules.py (family "ladder", segments (3, 4), quiz (4, 5), figures False)
```

- [ ] **Step 4: `content-standards.md` — "Writing for the ladder"** (append):

```markdown
## Writing for the ladder

Ladder modules (L0–L5) are for people who have never programmed. They are held to this, and the
gate checks what a script can (`verify.py`, "Ladder modules"):

- **A unit is story → do it → check it worked → peek inside**, in that order, every time.
- **Plain words first.** Explain every technical word in the sentence that first uses it, and give
  it a one-line plain meaning in the module glossary. Words in `01-design/ladder-jargon.json` must be
  in the glossary before a ladder module may use them (checked).
- **Short sentences**: at most 28 words in English, 70 characters in Chinese (checked).
- **The learner is the subject.** Steps are about *your* site and *your* app. The case study lives
  in the story and in peek inside.
- **No code in the main path.** Fenced code and repository paths only inside `:::peek` and
  `:::ask` (checked).
- **Tested for real.** Every `:::ask` has been run with a real agent; `runs/run.json` records the
  date, the agent, the transcript and the screenshot, and `:::see` shows what that run produced
  (checked: one run per ask, every file present).
- **Peek inside links into the deep modules** by part: `[M5, part 4](m05.html#slide-4)` (checked:
  the part exists).
- **Both editions**, written together (`zh_edition.py`).
```

- [ ] **Step 5: The skill** — add to `.claude/skills/course-content/SKILL.md`, as section "2b. A ladder module or unit":

```markdown
## 2b. A ladder module or unit (L0–L5)

Ladder modules are for non-coders; read `01-design/content-standards.md`, "Writing for the
ladder", first.

1. **Add a module**: copy `03-content/_templates/ladder-module/` (its README has the commands),
   register it in `06-production/modules.py` (`family "ladder"`), write the four-part units, and
   add its terms to `06-production/terms-zh.json`.
2. **Add a unit** to an existing ladder module: a new `## LN.K — …` part (or parts) in `slides.md`
   with story, `:::ask`/`:::see`/`:::else`, "Check it worked" and `:::peek`, its narration in
   `scripts/lN.json`, the same in `lesson.md`; if it adds a fourth segment, set the module's
   `segments` to `(4, 4)` in the registry.
3. **Run a build step for real**: open a scratch folder, give your agent exactly the `:::ask` text,
   save the transcript as `runs/<date>/<step>.md` and a screenshot through
   `learner-site/screenshots.py` as `runs/<date>/<step>.png`; add the entry to `runs/run.json`;
   rewrite `:::see` from what the run produced. Never write "You should see" from memory.
4. **Link a peek inside**: pick the M-module part that teaches the real version, link it as
   `[M5, part 4](m05.html#slide-4)`; the gate fails a link to a part that does not exist, so a later
   M-module edit that renumbers parts shows up here.
5. **Both editions**: translate the module into `zh/` and `scripts-zh/lN.json` as you write it
   (`01-design/zh-translation-guide.md`), then `python3 06-production/zh_edition.py check lN` and
   `stamp lN`.
6. **Writing for non-coders** — before you commit, reread each unit against this list: Is there a
   story before any step? Does every step say exactly what to paste and what you will see? Is any
   word in it one your parent would not know — and is it explained? Is there code outside peek?
```

- [ ] **Step 6: AGENTS.md** — map row `| course/03-content/lN-slug/, 06-production/modules.py | The beginner ladder (L-modules, for non-coders) and the one module registry |` and under "Rules that the gate enforces": `- **The ladder is written for non-coders.** Its main path carries no code, every build step is run for real before it ships (runs/run.json), and its peek-inside links resolve. Register every module in 06-production/modules.py — nowhere else.`

- [ ] **Step 7: Run** — `$PY course/06-production/test_ladder_check.py` → `OK` (template passes); build → template not built (`ls course/learner-site | grep -c l9` → 0).

- [ ] **Step 8: Commit**

```bash
git add course/01-design course/03-content/_templates .claude/skills/course-content/SKILL.md AGENTS.md course/learner-site/README.md course/06-production/test_ladder_check.py
git commit -m "How to add ladder content: standard, template, skill procedures (#ladder)"
```

---

### Task 8: L1 — Your first website (English), run for real

**Files:**
- Create: `course/03-content/l1-first-website/{slides,lesson,handout,glossary,lab,quiz,lab-rubrics}.md`, `runs/run.json` and its files, `course/06-production/narration/scripts/l1.json`
- Modify: `course/06-production/modules.py` (register `l1`), `course/06-production/terms-zh.json` (its terms), `course/learner-site/transcripts/` (regenerated)

**Interfaces:**
- Consumes: everything above.
- Produces: `Module("l1", "l1-first-website", "ladder", "Your first website", "你的第一个网站", segments=(3, 3), quiz=(4, 5), figures=False)` placed **before** `m00` in `MODULES`.

Content outline (write it from the template):

| Part(s) | Unit | Story | Ask your agent (paraphrase; the real text is written in the file) | Check it worked | Peek inside |
|---|---|---|---|---|---|
| 1–2 | Intro | Maria's bakery wants a page today's customers can open on a phone | — | — | the three products, one line each |
| 3–6 | L1.1 A page on your computer | a website is a folder of files a browser can open | make a one-page site for my (bakery / studio / club) in one `index.html` file; open it in my browser | the page opens and shows your name and three things you sell | ai_qe's `index.html` is the same kind of file → M9 part 12 |
| 7–10 | L1.2 Make it yours | changing words and colours by asking, not typing code | change the heading, add a photo, make it readable on a phone | the page looks right on your phone (browser's phone view) | how ai_qe keeps its pages consistent → M6 part N |
| 11–14 | L1.3 Put it online | GitHub Pages: free hosting from a folder | put this folder on GitHub and publish it with GitHub Pages; tell me the address | the address opens on your phone | the four clicks, and why `.nojekyll` → M9 parts 18–20 |
| 15 | Lab L1 | ship your own page | — (the lab lists the three asks as a checklist) | 5 binary items | — |
| 16 | Quiz L1 | 4 "which would you do?" scenarios | — | — | — |
| 17 | Recap | — | — | — | — |

- [ ] **Step 1: Register `l1`** in `modules.py` (above) and create the folder from the template. Run `$PY course/06-production/test_modules.py` → `OK`.

- [ ] **Step 2: Write the English sources** following the outline, the template and the writing standard. Narration: `scripts/l1.json`, 25–190 words per part, spoken plainly.

- [ ] **Step 3: Run every `:::ask` for real** (skill procedure 3). Use a scratch folder outside the repo and a real agent (Claude Code: `claude -p "<the ask text>"` in the folder, or an interactive session). Keep each transcript and a screenshot of the result (`learner-site/screenshots.py`, or the browser pane's screenshot saved as PNG). **The "Put it online" asks publish a public GitHub repository and a Pages site: ask the owner before running them, and name the repository and account in the question.** If the owner declines, run them in a throwaway account they nominate or stop and ask — do not record a run that did not happen. Rewrite each `:::see` from its run.

- [ ] **Step 4: Check** — `$PY course/06-production/verify.py | grep -E "Ladder|Artifacts|Figures|RESULT"` → `[PASS] Ladder modules (1 ladder modules)`; fix every problem it reports in the content (never loosen the check). `$PY course/06-production/narration/validate_narration.py --scripts-only` → pass.

- [ ] **Step 5: Build and look** — `$PY course/learner-site/build_site.py && make -C course transcripts`; open `l1.html`, `module-l1.html`, `lab-l1.html`, `quiz-l1.html`, `path-ladder.html`, `index.html` at 1600, 1024 and 390 wide (visual QA memory: every affected page at three sizes). The Copy button copies the ask text; peek inside is collapsed.

- [ ] **Step 6: Commit**

```bash
git add course/03-content/l1-first-website course/06-production/modules.py course/06-production/narration/scripts/l1.json course/06-production/terms-zh.json course/learner-site/transcripts
git commit -m "L1 — Your first website: the ladder's pilot module, every build step run for real (#ladder)"
```

---

### Task 9: L1 in Chinese

**Files:**
- Create: `course/03-content/l1-first-website/zh/*.md`, `course/06-production/narration/scripts-zh/l1.json`
- Modify: `course/06-production/zh-sources.json` (stamp)

- [ ] **Step 1: Translate** following `course/01-design/zh-translation-guide.md` (ladder blocks keep their markers; the `:::ask` text is translated — a Chinese learner pastes a Chinese request; screenshots may stay the English run's, captioned in Chinese).
- [ ] **Step 2: Check** — `$PY course/06-production/zh_edition.py check l1` → `[PASS] l1`; then `stamp l1`.
- [ ] **Step 3: Build and look** — `zh/l1.html`, `zh/module-l1.html`, `zh/index.html` at three sizes; `verify.py` → `[PASS] Chinese edition`, no untranslated English.
- [ ] **Step 4: Commit**

```bash
git add course/03-content/l1-first-website/zh course/06-production/narration/scripts-zh/l1.json course/06-production/zh-sources.json
git commit -m "L1 in Chinese (#ladder)"
```

---

### Task 10: Gate, ship, and hand the pilot to the owner

- [ ] **Step 1: Full gate** with the local audio procedure (Global Constraints) → `GATE PASSED: all steps green`. Restore generated files; `build_site.py --check` clean.
- [ ] **Step 2: Push, open the PR** (REST: `gh api -X POST repos/tomqwu/ai_courses/pulls …`), body lists what the owner should review in L1 and states that no narration of M0–M9 changed.
- [ ] **Step 3: Merge on green** with `merge_method=merge`; confirm `deploy the learner site (main only)` succeeded on `main`; open `https://tomqwu.github.io/ai_courses/` and `/zh/` and see the ladder first.
- [ ] **Step 4: Issues** — close the ladder machinery issue with evidence; open one issue per remaining module (L0, L2, L3, L5, L4, in that order), each pointing at skill section 2b and the template, and the L4 issue noting the Mac-and-Xcode requirement.
- [ ] **Step 5: Ask the owner to review L1** — link the live page and name what to judge: the story, the ask/see/else steps, the reading level, the Chinese.
