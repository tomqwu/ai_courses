# 第 0 模块 — 导览：三个产品，一套方法
> AI Product Studio（APS-3）的一部分 · 约 30 分钟讲授，外加约 30 分钟拿到首个成果（大部分是下载）· 无前置条件

## 概览

大多数 AI 课程教你调用 API。本课程教你交付产品，案例研究是三个真实的、已投入生产的开源应用——由一位工程师构建，AI 智能体承担了大部分繁重工作。你会把三个都克隆下来，在第一次课上端到端运行其中一个，然后用第 1–8 模块构建三个你自己的、达到作品集水准的产品：一个端侧 AI 应用、一套规格驱动的 SaaS 功能，以及一件引证有据的专业知识产物。最后，你要为其中一个定价、打包并做推介。

三个案例研究（case study）都在 GitHub 上公开：

| # | 产品原型 | 案例研究 | 它是什么 |
|---|---|---|---|
| 1 | 端侧原生 AI 应用 | **ListenToMe**（`github.com/tomqwu/ListenToMe`） | 一个 macOS 会议助手：端侧转录，加上通过你选择的本地或云端模型提供的实时 AI 帮助（`ListenToMe/README.md`） |
| 2 | 规格驱动的 AI SaaS | **SignUpFlow**（`github.com/tomqwu/SignUpFlow`） | 一个多租户志愿者排班 SaaS：FastAPI + 一个自动生成公平排班表的贪心求解器（`SignUpFlow/README.md`） |
| 3 | 专业知识内容产品 | **AI × QE**（`github.com/tomqwu/ai_qe`） | 一个以研究为支撑的简报站点：4 套带讲解的演示文稿、PDF 版次，以及一个咨询漏斗（`ai_qe/README.md`） |

为什么是这三个？它们的技术重心各不相同——边缘 AI 与隐私工程；服务端架构与安全；研究与内容运营——但它们是用*同一套方法*构建的，即**从规格到交付的循环（Spec-to-Ship Loop）**：**研究（Study）→ 规格（Spec）→ 构建（Build）→ 验证（Validate）→ 发布（Release）→ 证明（Prove）**（完整推导见 `00-research/00-synthesis.md`）。你只学一次方法，然后看它被实例化三次；正是这种重复让它扎根。

开始之前有两点预期。第一，**本课程中每一条事实性主张都带有一个文件指针**，比如（`SignUpFlow/AGENTS.md`）——如果你无法打开某个文件来验证一条主张，那条主张就是错的，你应该指出来。第二，**核心实验使用 Python 3.11+ 和 Ollama**，两者都免费，可在 macOS、Linux 和 Windows 上运行；Swift 拓展路线（第 2–3 模块）以 ListenToMe 本身作为参考实现，需要一台 Mac。不假定你有任何 LLM 经验。

**学完本模块，你能够：**

- 描述三种 AI 产品原型（archetype），说出每个案例研究仓库及其证明资产（proof asset）。
- 解释从规格到交付的循环的六个阶段，并为每个阶段指出一件真实的产物。
- 在一个示例工作区上运行 SignUpFlow 求解器，并记录它的健康分（health score）。
- 在你自己的机器上用 Ollama 拉取并运行一个本地 LLM。
- 在社区发布一条目标 + 环境说明——你的首个成果帖。

## M0.1 — 为什么是三种类型，为什么是这三个（约 8 分钟）

### 目标

描述三种 AI 产品原型（archetype），说出每个案例研究仓库，并说明「生产级」在本课程中的含义：不是演示，而是一件已交付的产物，附带你能打开的证明。

### 讲解

这三种产品原型基本覆盖了一个独立技术构建者能交付的一切，而每个案例研究都带有**证明资产（proof asset）**——仓库本身中可验证的证据，而不是营销主张。

**类型 1：端侧原生 AI 应用——ListenToMe。** 一个实时 macOS 应用，采集你的麦克风和会议的系统音频，在端侧转录，并通过你选择的模型流式输出 AI 回复——本地的 Ollama，或使用你自己密钥的云端服务商（`ListenToMe/README.md`）。证明资产：README 上渲染的 **96% 核心覆盖率徽章**（`ListenToMe/README.md`）；发布在 GitHub Releases 上的**经过公证的发布版 DMG**（"Grab the notarized `.dmg` from Releases"——`ListenToMe/README.md`）；以及一张 **14 行的竞品对比表**，其中的主张都有来源和日期（`ListenToMe/docs/competition-analysis.md`）。这张表也是产品定位的依据："the free, open-source, fully on-device meeting copilot"——表格显示，这是一个没有商业对手占据的市场角落（`ListenToMe/docs/competition-analysis.md`）。

**类型 2：规格驱动的 AI SaaS——SignUpFlow。** 一个面向教会和联赛的多租户志愿者排班平台：FastAPI + SQLAlchemy、JWT 鉴权、一个贪心启发式求解器，以及一个 YAML 输入/JSON 输出的 CLI（`SignUpFlow/AGENTS.md`，"Repository purpose"；它同时提供的 HTMX Web 应用见 `SignUpFlow/README.md:288`）。证明资产：**带日期的测试证据**——完整本地套件 "1,464 passed, 21 skipped"（`SignUpFlow/docs/playbooks/validation.md`）；`SignUpFlow/specs/` 下的 **17 个 spec-kit 文件夹**，每个都是一套完整的规格→计划→任务包；以及由 `make test-all` 在各自独立进程中运行的**七层测试金字塔**（`SignUpFlow/docs/TESTING.md`）。

**类型 3：专业知识内容产品——AI × QE。** 一个以研究为支撑的简报站点，主题是用 AI 让质量工程现代化。证明资产：**分布在 4 套演示文稿中的 116 张幻灯片**——21 + 33 + 26 + 36，定义在 `ai_qe/_data/briefing_room.json` 中——以及 **10 个现行 PDF 版次**——4 套完整演示文稿、4 条引导路线、研究配套材料和问卷，版次以 `ai_qe/_data/release.yml` 所列为准，截至 2026-09-10 在 `ai_qe/assets/pdf/` 中清点（`00-research/03-ai-qe-deep-read.md`；另见 `ai_qe/README.md`，"Publication records"）；还有一份**公开的自我审计**：对自家站点的一份包含 14 项发现的评审，逐项附有证据和验收标准（`ai_qe/research/reviews/site-audit-2026-09-06.md`）。

注意这九项证明资产的共同点：**每一项都是一个你能打开的文件，带日期或可由机器检查，而不是用户推荐语。**这也是本课程衡量你的作品的标准——每个实验都以一件产物结束，每件产物都以证据结束。

为什么要把这三个*放在一起*？因为它们共享一套方法。课程的研究综述把它提炼为十条可迁移的原则——「记录证据，而不是感觉」；「写智能体能执行的规格」；「把诚实变现」（`00-research/00-synthesis.md`）——第 1–8 模块则依次通过这三种产品原型来教这套方法。

### 行动步骤

浏览三个 README——`ListenToMe/README.md`、`SignUpFlow/README.md`、`ai_qe/README.md`——在每个里面找到一项证明资产（一个徽章、一行带日期的证据、一条发布记录）。然后写一段两句话的「哪种产品原型属于我」说明：三者中你最想在第 8 周之前构建哪一种，以及一件你以前交付过的东西。保存好；你会在 M0.3 中发布它。

## M0.2 — 方法：从规格到交付的循环（约 10 分钟）

### 目标

按顺序说出循环的六个阶段，并为每个阶段从案例研究仓库中指出一件真实的产物。

### 讲解

这就是你将在本课程每个模块中运行的循环：

```
1. STUDY    → 2. SPEC    → 3. BUILD    → 4. VALIDATE  → 5. RELEASE  → 6. PROVE
(research,     (specs an    (agents +     (tests,        (notarize,     (evidence,
 competition    agent can    TDD, small    coverage       TestFlight,    provenance,
 analysis,      execute)     reviewable   floors,        editions)      honest claims)
 positioning)                edits)        playbooks)
```

每个阶段背后都有一件真实的产物。边读边打开这些文件：

1. **研究（Study）。** ListenToMe 的 14 行竞品表，逐条主张都有来源（`ListenToMe/docs/competition-analysis.md`）；AI × QE 的第一条原则："**Baseline before solutioning.**"（`ai_qe/docs/principles.md`）。定位是一件研究产物，而不是一句口号。
2. **规格（Spec）。** SignUpFlow 的 spec.md 文件包含带优先级的用户故事（P1/P2/P3），配有 **Given/When/Then** 验收场景（`SignUpFlow/specs/014-security-hardening/spec.md`）；ListenToMe 的设计规格定义了协议级接口，*以及*一份 YAGNI 非目标（YAGNI non-goals）清单——"No cloud backend, accounts, billing, or multi-user"（`ListenToMe/docs/superpowers/specs/2026-06-18-listentome-design.md`）。
3. **构建（Build）。** SignUpFlow 的 tasks.md 把每份规格变成带确切文件路径的复选框任务，测试先写（`SignUpFlow/specs/019-sms-notifications/tasks.md`）；ListenToMe 的实现计划是一份 2,410 行的 TDD 任务清单，最后是一次自查，把每条规格要点对应到一个任务（`ListenToMe/docs/superpowers/plans/2026-06-18-listentome-mvp.md`）。
4. **验证（Validate）。** SignUpFlow 的七个测试层级和带日期的计数（`SignUpFlow/docs/playbooks/validation.md`）；ListenToMe 由脚本强制执行的 **95% 覆盖率底线**（`ListenToMe/README.md`）。
5. **发布（Release）。** ListenToMe 发布经过签名 + 公证、对应确切源码提交的 DMG（`ListenToMe/AGENTS.md`）；AI × QE 发布不可变的、按版次编排的版本——"Public content changes require a new edition before deployment"（`ai_qe/README.md`）。
6. **证明（Prove）。** ListenToMe 公开了一份差距评审，尽管核心覆盖率达到 97.24%，结论仍是 "**do not promote the existing 1.3.0 DMG**"（`ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md`）；AI × QE 公开了对自家站点的 14 项发现审计（`ai_qe/research/reviews/site-audit-2026-09-06.md`）；SignUpFlow 的验证记录包含了它的失败——一次浏览器点击竞争，以及一行写着 "not a pass" 的 mypy 欠账（`SignUpFlow/docs/playbooks/validation.md`）。

第 6 阶段最罕见，也是本课程的主干：对哪些已验证、哪些未验证、哪些失败了的诚实记录。测试验证你构建的东西；证据纪律验证你交付的东西。

### 行动步骤

把上面的循环图抄进你的笔记，然后开始你的**循环日志（loop journal）**——一个你整门课都会维护的单一文件。以后每个行动步骤，你涉及的每个阶段各记一行。第一条：在下面的 M0.3 中，你会做一次微型的研究（读 README）、构建（运行求解器）和证明（发布输出）。

## M0.3 — 搭建环境，拿到首个成果（约 12 分钟讲授；约 30 分钟动手）

### 目标

克隆全部三个仓库，在本地运行 SignUpFlow 求解器并记录其健康分（health score），然后用 Ollama 运行你的第一次本地 LLM 补全。

### 讲解

现在就动手——整个流程大约 30 分钟，大部分是下载（`make setup`、Ollama 安装程序和模型拉取）。你需要 git 和 Python 3.11+（SignUpFlow 自己的最低版本——`SignUpFlow/AGENTS.md`，"Code style"）。

**1. 克隆三个案例研究：**

```bash
git clone https://github.com/tomqwu/ListenToMe.git
git clone https://github.com/tomqwu/SignUpFlow.git
git clone https://github.com/tomqwu/ai_qe.git
```

**2. 用三条命令运行一个真实的生产求解器**（出自 `SignUpFlow/README.md` 的 "Quick Start" 和 "CLI Example"）：

```bash
cd SignUpFlow && make setup     # Poetry env + migrations + seed data
poetry run python -m api.cli.main init my-church
poetry run python -m api.cli.main solve my-church
```

`solve` 会打印工作区摘要和求解器的结果——人员、活动、一行**健康分**、硬/软约束违规，以及公平性标准差——并把解保存到 `my-church/output/solution.json`。这一行由 `SignUpFlow/api/cli/main.py:193` 输出（`Health score: {health_score:.1f}/100`）；它的*值*取决于你克隆的 SignUpFlow 版本下示例工作区产出的结果，而不是 README 承诺的某个数字——在 2026-09-16 的 head 上，`init my-church` + `solve my-church` 打印 `Health score: 0.0/100` 和 `Violations: 2 hard, 0 soft`（两个 `sound_tech` 岗位都没有填上），而一个更早的示例打印过 `100.0/100`。**截取健康分那一行及其前后的几行**；这是你的第一件产物，重点不是那个数字——而是运行记录。

**3. 安装 Ollama，并拉取一个真正的本地模型**（来自 <https://ollama.com/download>）：

```bash
ollama pull qwen3:0.6b
ollama list                     # confirm the model is present
ollama run qwen3:0.6b "Reply with exactly: PONG"
```

最后那条命令是你的第一次本地 LLM 补全：不需要 API 密钥，没有云端账单，没有数据离开你的机器。第 2 模块将正是在这个基础上构建你自己的多角色助手。

> **Windows 说明。** Ollama 可在 Windows、macOS 和 Linux 上运行，而本课程的每个核心实验都是 Python + Ollama——所以 Windows 和 Linux 用户完全具备学习主线的条件。**Swift 拓展路线**（第 2–3 模块中「同一实验的 Swift 版」附录）需要一台装有 Xcode 的 Mac，因为 ListenToMe 面向 macOS（`ListenToMe/README.md`）。SignUpFlow 的 `make` 目标在任何装有 Python 3.11+ 和 Poetry 的环境中都能用。

为什么要在第 0 模块就急着跑通求解器？因为任何构建者课程最难的部分，都是从「看」到「跑」之间的鸿沟。在大约三十分钟内——其中大部分是下载时间——你就会执行过真实的生产软件和一个真实的本地模型。这就是首个成果，它正是用来跨越「第 2 模块鸿沟」的，大多数课程都在那里流失学员。

### 行动步骤

在社区发布你的首个成果：（1）包含健康分那一行的求解器输出，（2）你的 `ollama list` 输出，（3）你在 M0.1 写的两句话「哪种产品原型属于我」说明。然后完成**实验 M0**（`m00-orientation/lab.md`）——它的清单把这一段变成你的第一个通过/不通过检查点；通过关卡是求解器输出块加上非空的 `ollama list`。它的「进入第 1 模块之前」部分（运行 TinyCopilot 套件、开始你的证据日志）就是第 2 模块的起点。

## 回顾

- 三种产品原型，三个真实仓库：**ListenToMe**（端侧 AI 应用；96% 核心覆盖率徽章、经过公证的 DMG、14 行竞品表），**SignUpFlow**（规格驱动的 SaaS；1,464 passed / 21 skipped 的带日期证据、17 个规格文件夹、7 个测试层级），**AI × QE**（专业知识产品；截至 2026-09-10 的 116 张幻灯片 / 4 套演示文稿 / 10 个现行 PDF 版次、来源追溯文件、一份公开的 14 项发现自我审计）。
- 三者背后是同一套方法：**从规格到交付的循环（Spec-to-Ship Loop）**——研究、规格、构建、验证、发布、证明——每个阶段都有一件真实、可打开的产物。
- 生产级意味着你能打开的证明：一个徽章、一行带日期的证据、一个来源追溯文件——而不是用户推荐语。
- 你的环境：处处都是 Python 3.11+ 和 Ollama；只有 Swift 拓展路线需要 Mac。
- 你已经端到端运行过一个案例研究和一个本地 LLM——把两份输出都保存在证据日志里，并在进入第 1 模块之前运行 TinyCopilot 套件。

## 讨论题

发布你的首个成果回帖（求解器健康分 + `ollama list` + 你的产品原型说明），然后再用一句话回答：**M0.1 中哪项证明资产最让你意外？如果一位持怀疑态度的客户打开这个文件，它站得住吗？**回复另一位同学的帖子，写出你认为适合*他的*目标的产品原型——只要指出理由，欢迎提出不同意见。
