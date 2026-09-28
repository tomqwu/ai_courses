# The Chinese edition — translation guide

The site has a full Chinese edition (中文, `/zh/`). It is the same course in Chinese: every part,
lesson, lab, question and glossary entry, in the same order, with the same exhibits and answer keys.
Chinese should read as Chinese written for Chinese-speaking engineers, not as English in Chinese
words. English stays only where it is the thing itself: code, commands, file names, identifiers,
product names — and a key term's English name, in brackets, the first time it appears in a section.

`python3 course/06-production/zh_edition.py check mNN` holds a module's Chinese sources to its
English ones; the gate runs it for every module. `python3 course/06-production/zh_edition.py
sentences mNN` prints the English narration as the site splits it — translate from that.

## Files

For a module in `course/03-content/mNN-slug/`, the Chinese sources are:

| File | Translate |
|---|---|
| `zh/slides.md` | every part: title, bullets, tables, figure labels and notes, NOTES comments |
| `zh/lesson.md`, `zh/handout.md`, `zh/lab.md`, `zh/quiz.md`, `zh/glossary.md` | the whole file |
| `zh/lab-rubrics.md` | only the auto-fail section, headed `## 自动不通过` (the site shows nothing else of the rubric) |
| `course/06-production/narration/scripts-zh/mNN.json` | the narration: `{"label": "M5 — …", "slides": {"slide-1": {"title": "…", "sentences": ["…", …]}, …}}` |

## Rules that the check enforces

1. **Same structure.** The same parts (`---` separators) in the same order; the same headings at the
   same levels; the same list items, table rows, steps, checklist items and questions. Never merge,
   split, drop or add one.
2. **Code is copied, never translated.** Every fenced block (` ``` `) is byte-identical to the
   English, info string included — exhibits are true copies of real files. Inline `code`, file
   paths, commands, flags, URLs and identifiers stay exactly as written.
3. **Pointers are copied.** Every `Repo/path:N-M` stays exactly as written.
4. **One Chinese sentence per English sentence** in the narration. `sentences` has the same length
   as the English list for that part, and sentence *i* says what English sentence *i* says — the
   English recording marks the Chinese sentence it is speaking by its position. Each sentence ends
   with 。 ！ or ？. Never speak a line number (no "第 12 行").
5. **Markers the site reads stay in their form:**
   - `slides.md` front matter: `title: M5 — <中文标题>`; every `<!-- _class: … -->`,
     `<!-- _diagram: … -->` and `<!-- NOTES: … -->` comment stays (translate the notes' text).
   - Part titles keep their ids: `## M5.1 — <中文>`, `## 实验 M5 — <中文>` (for `Lab M5`),
     `## 测验 M5 — <中文>` (for `Quiz M5`), and `回顾` / `总结` / `讨论` for Recap / Summary /
     Discussion.
   - The cover's `Promise:` and `Duration:` become `承诺：` and `时长：`.
   - `lesson.md`: `## 概览` for Overview, `## M5.1 — …` for segments, `## 回顾` for Recap.
   - `lab.md`: steps are `## 第 1 步 — <中文> (~20 分钟)`; the checklist section's heading contains
     `验收清单`; the evidence section's heading starts `证据`; the header block keeps its `>` lines
     with `**目标：**`, `**前置条件：**`, `**时间：**`.
   - `quiz.md`: keep every question marker as written (`**Q1 (MC).**`, `**Q7 (Short answer).**`),
     the option letters (`- a)`), `## Answer key` and its row or `**A1: b.**` format, and the
     answer letters; write objectives as `目标：M5.1`.
   - `glossary.md`: `**<中文名>（<English term>）** — <中文定义>`, one per English term, in the
     same order. Use the Chinese name in `course/06-production/terms-zh.json`.
6. **Figures keep their shape.** In a ` ```figure ` block keep every key (`kind:`, `source:`,
   `layer:`, `box:`, `node id:`, `edge: a -> b`, …), every node id and every flag in brackets
   (`(seam)`, `(hl)`, `(good)`, `(bad)`, `(chain)`); translate `alt:`, labels and notes. The words
   after `@` must be the first few characters of one of that part's Chinese narration sentences —
   the part builds in when that sentence is spoken.

## How it should read

- **Terms:** on first use in each section, the Chinese name then the English in full-width
  brackets — 租户隔离（tenant isolation）; after that, Chinese alone. Take the Chinese names from
  `terms-zh.json`. Terms that are names (Git, GitHub, Ollama, spec-kit, SignUpFlow, Claude Code,
  `AGENTS.md`) stay in English.
- **Register:** plain, direct technical Chinese, as a senior engineer would write it. Second person
  (你). No marketing flourish that the English does not have.
- **Punctuation:** full-width Chinese punctuation (，。：；？！（）「」) in Chinese text; a space
  between Chinese and adjacent English words or numbers is not needed, but keep code and numbers
  as written (`org_id`, `401`, `95%`).
- **Numbers and units** stay as numerals: 3 小时, 25 分钟, 1,790 个指针.
- **Don't add or explain.** Same claims, same caveats, same honesty. A number stays the number.
