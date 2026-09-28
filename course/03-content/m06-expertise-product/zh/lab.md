# 实验 M6 — 构建一份迷你简报
> AI Product Studio（APS-3）的一部分 · 第 6 模块的通过/不通过检查点 · 配套课程：`lesson.md` · 起始数据：`evidence-dataset.md` · 自查：`selfcheck.py`

## 目标

把研究变成一件**可信、卖得出去的产物**：一份 12 张幻灯片的迷你简报，其中每项量化主张都带着来源记录和认知标签（epistemic label），一套幻灯片通过声明的路线服务两类受众，一个假想的 v2 要走一遍版次纪律。这是课程评分细则中第三种产品原型的实验检查点：「一份 12 张幻灯片的迷你简报，附来源表 + 两条受众路线 + 一份版次决策。」

## 前置条件

- 已完成第 1–5 模块（你有一个起始仓库，其中有实验 M1 留下的 `docs/research-log.md`）。
- **一个你真正了解的主题。** 默认：AI 测试的证据库——`evidence-dataset.md` 中的六条起始主张（METR：完成时间*多花* 19%，CI +2% 到 +39%；Peng：快 55.8%，95 名自由职业者，与厂商有关联；Meta TestGen-LLM：类级别累计产出率 75%/57%/25%；Uber FlakyGuard：修复了 47.6% 的*可复现*不稳定测试；Google ICSE 2026：分诊准确率 90.1%，已部署在 52,635 个失败测试上；Bain：平均提升 10–15%，很少转化为钱），来源记录在 `ai_qe/docs/evidence/` 中。备选：你自己的领域，但那样你得自己去取来源——URL、检索日期、真实引文。

## 时间

约 2.5 小时。

## 步骤

1. **编写 `research-log.md`**（带日期，最新的在前，采用 AI × QE 的格式——`ai_qe/docs/research-log.md`）：至少 **6 个条目**，每个都包含 Question / Checked / Outcome / Changed，其中**至少 2 条诚实的“not verified”或“open”条目**——你找过、但无法确认的内容。先登记，再起草幻灯片；从未进入日志的主张，也永远不会进入讲稿。
2. **构建来源表**——每项主张一行，使用下面的模板。给每一行标注 `ai_qe/docs/principles.md` 中的四个层级之一（任务级效率 / 释放的产能 / 硬性节省 / 总支出影响），以及一个认知标签（实测 / 自报 / 与厂商有关联 / 示意）。
3. **列出 12 张幻灯片的大纲。** 每张**含量化内容的**幻灯片都引用 ≥1 行来源（按行号），并把认知标签*标在幻灯片上*。借用 `ai_qe/docs/economics/slide-language.md` 中的措辞规则：自报数字永远不能呈现为实测；示意情景要在幻灯片本身上标为示意。
4. **在同样这 12 张幻灯片之上声明两条路线**（稳定幻灯片 ID，参照 `ai_qe/_data/briefing_routes.json`）：一条**6 张幻灯片、以具体决策请求收尾的高管路线**（「资助第 0 和第 1 阶段」，而不是「转型 QA」——`ai_qe/docs/economics/slide-language.md`），以及一条**10 张幻灯片、保留高管路线所跳过的支撑证据的技术路线**。
5. **为一个假想的 v2 写一份版次决策记录**，其中有一张幻灯片新增了一个数字：改了什么、**刻意保留**了什么、哪些版次升级（站点还是内容）——参照 `ai_qe/releases.md` 的条目（“Audio, subtitle timing, and the v1.24.0 PDF editions remain unchanged”）和 `ai_qe/_data/release.yml` 中的区分（`version` 与 `slide_edition`）。
   然后用本文件夹中的 `edition_manifest.py`（只用标准库）让两个版次都变成机器可读的。这些命令在 PowerShell 和 Mac 终端中完全相同：

   ```bash
   python3 edition_manifest.py build your-briefing.md --edition 1.0.0 --base-url https://you.github.io/briefing/1.0.0
   ssh-keygen -t ed25519 -f "$HOME/aps_edition_key" -C "you@example.com"
   python3 edition_manifest.py sign manifest-1.0.0.json --key "$HOME/aps_edition_key" --signer you@example.com
   python3 edition_manifest.py verify manifest-1.0.0.json --signer you@example.com --allowed-signers allowed_signers
   ```

   `build` 会拒绝任何缺少 URL 或 `path:line` 来源、ISO 检索日期和层级的来源行，所以先把这些补齐。密钥放在你的主目录里，位于仓库之外；提交清单、它的 `.sig` 和 `allowed_signers`，永远不要提交密钥。现在在简报中做出 v2 的改动，然后运行 `python3 edition_manifest.py check your-briefing.md manifest-1.0.0.json`：它必须以 **1** 退出，并点出你改动的那项主张。在新编号下构建新版次（`build` 不会用不同的主张覆盖 1.0.0），同样给它签名。
6. **在你自己的文件上运行对账关卡。** 把简报——来源表、幻灯片大纲和正文——保存为一个 Markdown 文件，然后在本文件夹中运行 `python3 selfcheck.py your-briefing.md`（只用标准库，Python 3.11）。它会读取每个句子、表格行和列表项，并以 **1** 退出，列出每一处陈述了数字、却没有*在同一单元内*给出引用的地方。只有三种形式算作引用：带行锚点、用反引号括起来的仓库指针（`ai_qe/docs/evidence/benchmarks.md:31`）、一个 URL，或者一个 `[source: …]` 标签。结构性数字（「slide 3」「row 12」「Phase 0」「edition 4」）不是主张，不会被标记。**通过 = 以 0 退出。** 先运行 `python3 selfcheck.py --selftest`：它会用一段通过的和一段失败的摘录（`selfcheck-examples/good.md` 和 `selfcheck-examples/bad.md`）检查自己，让你在用它检查自己的作品之前，先看到每种判定是什么样子。这个脚本只能证明没有孤立的数字。它无法告诉你一个被引用的数字是否*正确*——这正是 `ai_qe/CONTRIBUTING.md:139-141` 拒绝把一个能解析的链接当作证据的原因——它也不会顺着 `[source: row N]` 标签去检查第 N 行本身是否有来源。以 0 退出只是底线，不是分数；评分细则的第 1–5 行仍然要靠你自己达到。

## 模板

**来源表**（每项主张一行；对账在验收时检查）：

| # | 主张（幻灯片上的原话） | 来源 URL | 检索日期 | 主张类型（层级 1–4） | 认知标签 | 它支撑什么 |
|---|---|---|---|---|---|---|
| 1 | 「开发者在 AI 辅助下*多花*了 19% 的时间（CI +2% 到 +39%）」 | https://metr.org/… | 2026-09-04 | 任务级（负面） | 实测——独立 RCT | 任务效率风险；不是产能数字 |
| 2 | … | … | … | … | … | … |

**路线声明**（稳定幻灯片 ID；closing = 决策请求那一张）：

```yaml
executive:
  slides: [1, 4, 7, 9, 11, 12]   # 6 slides
  closing: 12                    # ends on the decision ask
technical:
  slides: [1, 2, 3, 4, 5, 6, 7, 8, 9, 11]  # 10 slides — keeps the evidence
  full_order: [1,2,3,4,5,6,7,8,9,10,11,12]
```

## 验收清单（必须全部满足）

- [ ] `research-log.md` 有 ≥6 条带日期的 Question/Checked/Outcome/Changed 条目，其中 ≥2 条标为未验证/未决。
- [ ] **对账检查：** 12 张幻灯片中的每项量化主张都对应一行来源（没有孤立的数字）。
- [ ] 每一行来源都带有来源 URL、检索日期和主张类型层级。
- [ ] 高管路线恰好 6 张幻灯片，并以一个具体的决策请求收尾——在你的证据记录中**原文引用这个请求**。
- [ ] 技术路线保留了 ≥3 张被高管路线跳过的证据幻灯片（列出幻灯片 ID）。
- [ ] 每张含量化内容的幻灯片都在幻灯片本身上带有认知标签（自报 / 实测 / 与厂商有关联 / 示意）。
- [ ] 版次记录区分了站点版次与内容版次，并写明 v2 刻意保留了什么。
- [ ] 两个版次都有一份由 `edition_manifest.py` 生成的清单和一个 `verify` 接受的签名，而且用 v1 清单运行 `check` 以 1 退出，并点出 v2 改动的那项主张。
- [ ] **没有未引用的量化主张。** 自学：`python3 selfcheck.py your-briefing.md` 以 0 退出——粘贴命令及其最后一行输出。班级：由一位具名的同伴评审者书面确认同样的结论。无论哪种，都要**写明你走的是哪条路径**；班级学员同样要运行脚本，因为它能抓住读者一眼扫过时漏掉的东西。

## 证据记录

命令或操作、结果、日期、环境、局限（课程规定的格式）。包括：完整的研究日志、来源表、带引用的 12 张幻灯片大纲、原文引用了决策请求的两份路线声明、附两份清单的版次决策记录、每份清单的 `verify` 输出行和失败的 `check` 输出，以及对账证据：逐字的 `selfcheck.py` 输出及其退出状态、你走的路径（自查或具名同伴评审），如果你走的是班级路径，还要附上同伴的书面确认。如果某个来源取不到，就按 `ai_qe/research/document-manifest.json` 的清单格式记录下来（status: unavailable + reason）——一次诚实的失败也算证据。

## 拓展目标

- **为你的简报写一份 30 分钟的会议脚本**（对齐 5 / 探索 15 / 达成一致 10——`ai_qe/briefings/index.md`）：你们要对齐什么、哪些幻灯片承载探索环节，以及你用来收尾的具体约定。
- **起草一份 10 个问题、按角色分流的问卷**，遵循 `ai_qe/docs/method/discovery-questionnaire.md` 的设计规则：一份表单，在第 1 题就按角色分流；定义成功的问题采用单选；区间互斥、没有缺口，并带有「不知道」选项；至少包含一个财务信息问题。

## 讨论题

用这个模板发到社区：

> **迷你简报 M6 — [你的名字]**
> 主题：[你的主题] · 决策请求：[原文引用你的高管路线的收尾请求]
> 最难证明的一行：[主张]——我没能找到的证据是 [未验证项]，所以我 [弱化了措辞 / 删掉了它 / 把它标为示意]。
> 想问大家的一个问题：[一个你拿不准的来源或标注判断]。
