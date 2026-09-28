# 第 1 模块 — AI 产品操作系统
> AI Product Studio（APS-3）的一部分 · 约 60 分钟 · 前置：第 0 模块

## 概览

第 0 模块给了你三个已交付的产品和一个循环。本模块交给你的，是让*一位工程师与 AI 智能体协作*就能交付它们的那套机制：**AI 产品操作系统（AI product operating system）**。它有三个部分，恰好对应本模块的三个分段。第一，**治理（governance）**——SignUpFlow 如何用一套分层的指令文件约束它合作的每一个智能体，这些文件简短、采用祈使语气、可验证。第二，**规格（specification）**——spec-kit 的产物流水线，把一个想法变成全新的智能体会话在没有任何对话上下文的情况下也能执行的任务。第三，**证据纪律（evidence discipline）**——把验证记录成带日期、固定到 SHA、包含失败的证据，而不是一种感觉。

为什么这要先于任何产品类型？因为 AI 智能体并不取代流程，而是抬高了流程的利害。当代码以智能体的速度生成时，瓶颈就转移到说清你要什么、验证你得到了什么，以及如实说明实际验证了什么（`00-research/02-signupflow-deep-read.md`，§1）。产品原型各不相同，操作系统却是同一个——而它恰恰是大多数构建者跳过、然后为此付出代价的那一部分。

**为什么要治理：用数字说话，而且只说到每个数字能支撑的层级。** 支持规则、规格和证据记录的理由并不是讲师的个人偏好。本课程自己的证据数据集记录了独立的测量结果（`course/03-content/m06-expertise-product/evidence-dataset.md`，第 1–2 行）：

| 行 | 发现 | 主张层级 | 它说明了什么、没有说明什么 |
|---|---|---|---|
| 1 | METR 2025：有经验的维护者在自己的仓库上使用 AI 时**慢了 19%**（CI +2% 到 +39%），而他们*自认为*快了 20% | 任务层级，实测，独立随机对照试验，16 名开发者，246 个 issue | 感受到的速度和测得的速度可能指向相反的方向。它并没有说明 AI 让所有人都变慢 |
| 2 | METR 2026 年 2 月的后续研究：−18% 和 −4%，**两个置信区间都跨过零**；57 名开发者，800+ 个任务 | 任务层级，无定论 | 效应无论朝哪个方向都尚无定论——这本身就是测量你自己的理由 |

DORA 2025 年的报告基于一项从业者调查补充了一个相关性：采用 AI 与更高的交付吞吐量*以及*更高的交付不稳定性同时出现，AI 放大的是团队原有的任何实践（`course/00-research/08-domain-currency-2026.md`，领域 2）。把它读作方向，而不是一个测得的效应。两者合起来说明了一件事：当智能体以机器的速度产出代码时，「进展顺利」的印象是你手头最不可靠的信号。本模块的一切，都是用一个陌生人能检查的东西来替代这种印象。

贯穿始终的案例研究是 SignUpFlow——第 0 模块中的规格驱动 SaaS——由 ListenToMe 和 AI × QE 提供变体和诚实的范例。在实验（`m01-operating-system/lab.md`）中，你会构建自己的起始仓库——`constitution.md`、一份 `AGENTS.md` 和一个导入它的 `CLAUDE.md`、规格模板、一份研究日志，以及一个检查你证据日志的钩子——并在一个小型 CLI 功能上跑通一次完整的规格 → 计划 → TDD 迷你循环。

**学完本模块，你能够：**

- 以祈使、可验证的形式写出分层的智能体规则——一份宪章，以及一份由 `CLAUDE.md` 导入的 `AGENTS.md`——且不超过约 200 行的上限。
- 为一项工作在规则、钩子、技能和子智能体之间做出选择，并说出每一种做不到什么。
- 应用五级指令优先级（「遵循更具体、更安全的那一条」）以及智能体必须遵守的防幻觉规则。
- 描述每个 spec-kit 产物的职责（spec、research、data-model、plan、contracts、quickstart、checklist、tasks），并把一个用户故事转化为一个验收场景外加一条任务行。
- 按规定格式记录验证证据——命令、计数、日期、环境、局限、head SHA——并把失败包括在内。

## M1.1 — 用宪章和规则文件治理智能体（约 20 分钟）

### 目标

把 SignUpFlow 的分层指令栈解释为一份由 `CLAUDE.md` 导入的 `AGENTS.md`，按它的写作风格写规则，应用让智能体保持诚实的优先级和防幻觉规则，并判断一条规则何时应该改为钩子、技能或子智能体。

### 讲解

**指令栈：一份 `AGENTS.md`，由 `CLAUDE.md` 导入。** 在你的 SignUpFlow 克隆中打开这四个文件，记下它们的长度：

- `.specify/memory/constitution.md` — **85 行**。项目原则，「位于所有智能体文件之上的唯一事实来源」（`SignUpFlow/AGENTS.md:181`）。它定义了两种运行情境（Ralph 实现循环与交互式聊天）、四条原则、一份自主权配置（autonomy configuration），以及当前的验证策略。
- `AGENTS.md` — **188 行**。每个智能体共享的那一份基线，「由 Codex CLI、Cursor、Aider、Jules、OpenHands、Sourcegraph Amp、Factory 以及其他读取 `AGENTS.md` 的工具使用」（`SignUpFlow/AGENTS.md:3`）。`AGENTS.md` 是一种开放格式，「现由 Linux 基金会旗下的 Agentic AI Foundation 管理」（agents.md 网站自己的源码，`github.com/agentsmd/agents.md`，2026-09-26 查阅）。
- `CLAUDE.md` — **154 行**（截至 2026-09-16）。Claude 专用的附加说明，通过第 5 行的一个 markdown 链接指向 `AGENTS.md`（`SignUpFlow/CLAUDE.md:5`）。
- `.github/copilot-instructions.md` — 给 Copilot 的一份重述，Copilot 需要它自己的文件。

**导入，而不是链接。** Claude Code 的记忆文档（code.claude.com/docs/en/memory，2026-09-26 查阅）写清了 Claude 会加载什么。只有 `AGENTS.md`、没有 `CLAUDE.md` 时，Claude Code v2.1.277 或更高版本会自己读取 `AGENTS.md`。两个文件都存在时，它读取「只有你的 `CLAUDE.md` 文件」。`CLAUDE.md` 导入了 `AGENTS.md` 时，它两者都读。导入只需一行，`@AGENTS.md`，并且「被导入的文件会在启动时展开并加载进上下文」。链接不等于导入：对于「一个用文字告诉 Claude 去读 `AGENTS.md` 的 `CLAUDE.md`」，同一页写道「只有当 Claude 决定打开这个文件时，它才会看到 `AGENTS.md`」。这正是 SignUpFlow 的配置。它的 `AGENTS.md` 仍然给出了当初的理由——「Claude Code 不会原生读取这个文件」（`SignUpFlow/AGENTS.md:5`）——写下时属实，如今已经过时。对 SignUpFlow 来说，导入只有一行，却不是一行就能修好的事：把它 188 行的 `AGENTS.md` 导入 154 行的 `CLAUDE.md`，会加载 342 行，远超下面的预算，所以 `CLAUDE.md` 得先缩减到只剩 Claude 专用的附加说明。你自己的仓库则从一开始就用现在的方式：所有共享内容都放在 `AGENTS.md` 里，`CLAUDE.md` 只放导入语句和 Claude Code 专有的内容。

```markdown
@AGENTS.md

## Claude Code addenda
- A Stop hook runs scripts/check-evidence-log.sh. When it blocks, fix the entry it names.
```

没有任何内容写两遍，Codex、Cursor 和 Claude 读的是同一份基线。有一个代价要知道：导入会完整加载，所以行数预算要把 `AGENTS.md` 和附加说明加在一起算。同一页写道「每个 CLAUDE.md 文件的目标是不超过 200 行」，而被导入的文件「仍然会在启动时加载并进入上下文窗口」。

有三个特性让这套指令栈奏效。**一个权威来源，多个分发文件**——基线写在 `AGENTS.md` 里，其他文件导入、引用或重述它，而不是复制文字（`SignUpFlow/docs/ai-agent-coding-strategy.md`，"Single source, multi-host"）。**文件要短**——写作风格（house style）规定：「每个指令文件不超过约 200 行。按主题拆分，而不是嵌套」（`SignUpFlow/AGENTS.md`）。**祈使、可验证的规则**——这是写作风格的核心，以对比的形式写出：

> 「每条规则都必须可验证。`Filter every query by org_id.` 而不是 `Be careful with multi-tenancy`。」（`SignUpFlow/AGENTS.md`，"House style"）

智能体无法检查的规则只是一种感觉，不是规则。写你自己的规则时，用这张对照表：

| 坏规则（不可验证） | 好规则（可验证） | 原因 |
|---|---|---|
| 「多租户要小心」 | 「每条查询都按 `org_id` 过滤」（`SignUpFlow/AGENTS.md`） | 「小心」无法执行，也无法检查；过滤可以 |
| 「保持指令文件易于管理」 | 「每个指令文件不超过约 200 行」（`SignUpFlow/AGENTS.md`） | 数字可以检查；「易于管理」只是一种感觉 |
| 「重视测试覆盖率」 | 「先写测试（TDD）：写失败的测试，实现到让它通过，运行 `make test-unit`」（`SignUpFlow/AGENTS.md`） | 写明了动作和检查命令 |
| 「妥善处理密钥」 | 「永远不要提交密钥、API key、JWT 签名密钥……从环境变量中读取它们」（`SignUpFlow/AGENTS.md`，"Safety"） | 「永远不要提交 X」可以 grep；「妥善」不行 |

**宪章（constitution）里放什么。** SignUpFlow 85 行的宪章只保留绝不能偏离的东西：四条原则——*原生优先*（Native First，本地开发优先用普通的 Poetry + SQLite 而不是 Docker）、*测试驱动实现*（Test-Driven Implementation）、*简单与 YAGNI*（Simplicity & YAGNI，「只构建确切需要的东西，不多做。」），以及*安全与可靠*（Safety & Reliability）：电子邮件和短信「必须（MUST）默认关闭（`EMAIL_ENABLED=false`、`SMS_ENABLED=false`……）」，支付「必须（MUST）被模拟或关闭」（`SignUpFlow/.specify/memory/constitution.md`）。它还固定了**自主权**：「YOLO Mode: DISABLED / Git Autonomy: ENABLED (Commit changes when done)」——智能体可以提交完成的工作，但绝不能运行未经检查的破坏性命令；`AGENTS.md` 补充了「不确定一个操作是否可逆时，停下来询问」（`SignUpFlow/AGENTS.md`，"Safety"）。

**优先级。** 规则重叠时，`AGENTS.md` 给出一个五级的指令优先级（instruction hierarchy）和一条决胜规则：「遵循更具体、更安全的那一条。」

1. 当前任务中用户的请求。
2. `CLAUDE.md` 和 `AGENTS.md` 中的仓库专属规则。
3. `.github/instructions/` 下按路径限定的规则（Copilot）。
4. `docs/ai-agent-coding-strategy.md` 中的通用指导。
5. 推断出的最佳实践。

（`SignUpFlow/AGENTS.md`，"Agent instruction hierarchy"）

**防幻觉（anti-hallucination）。** 同一个文件里的这些规则，正是你的智能体最需要的：

> 「不要虚构文件路径、函数名、路由路径、命令、URL 或标识符。引用之前先 grep 仓库。」（`SignUpFlow/AGENTS.md`，"Anti-hallucination"）

> 「请求有歧义时，给出 2-3 个有区别的选项，而不是猜测。」（`SignUpFlow/AGENTS.md`，"Anti-hallucination"）

对于 schema 字段或环境变量名这类事实：「从权威来源读取它们。不要凭记忆回想」（`SignUpFlow/AGENTS.md`）。这些规则把幻觉——智能体辅助工作中最大的失败模式——变成一条可以检查的禁令。

**规则如何晋级。** 新规则不会直接进入 `AGENTS.md`。它们要沿着 `docs/ai-agent-coding-strategy.md`（"How rules graduate"）定义的流水线逐级晋升，即规则晋级（rule graduation）：一条观察先记录在 `docs/research-log.md` 中（这个文件的存在正是为了让「探索性笔记永远不会变成无声的规则」——`SignUpFlow/docs/research-log.md`）；它至少要在一次真实的改动上试用；只有在那之后，它才会被提升进 `AGENTS.md` 或某个智能体专属文件；`docs/source-repos.md` 中的来源行按 `pending → extracted → promoted` 推进；如果它具有普遍性，就会被推送到上游的 `tomqwu/GenAI_Common`。规则赢得一席之地的方式与功能一样：经受住真实工作的检验。

**规则、钩子、技能还是子智能体。** 规则只适合智能体应当*知道*的东西。Claude Code 把 `CLAUDE.md` 视为「上下文，而不是强制执行的配置」（code.claude.com/docs/en/memory），它的最佳实践页面划出了界线：「与只起建议作用的 CLAUDE.md 指令不同，钩子是确定性的，保证动作一定发生」（code.claude.com/docs/en/best-practices；两者均于 2026-09-26 查阅）。Anthropic 关于保持 `CLAUDE.md` 简短的建议由此而来：把流程移进技能（skill），把特定路径的规则移进 `.claude/rules/`，把每次都必须成立的东西移进钩子脚本（hook）。本课程关于怎么写规则的要求依然成立——祈使、可验证、不超过约 200 行。这张表补充了每种机制用来做什么、做不到什么，以及何时该用它：

| 机制 | 用来做什么 | 做不到什么 | 何时该用它 |
|---|---|---|---|
| **规则**——`AGENTS.md` 或 `CLAUDE.md` 中的一行，或 `.claude/rules/` 中的一个文件（`paths:` 列表让它只在 Claude 读取匹配文件时加载） | 智能体每次会话都需要的事实和约定：命令、禁令、写作风格 | 保证任何事。它是模型权衡的上下文，文件一长就会被稀释 | Claude 把一个约定或命令弄错了两次，而代码又无法向它展示正确的那一个 |
| **钩子**——在 `.claude/settings.json` 中绑定到某个事件的脚本：`Stop` 在 Claude 结束一轮时运行，`PreToolUse` 在工具调用之前运行 | 强制执行。退出码 2 会阻止工具调用，或者让 Claude 继续工作，Claude 会读取脚本的 stderr | 判断含义。它检查的是脚本能判定的东西，比如某个字段是否存在、某个 SHA 能否解析，而从不检查证据是否属实。它只在 Claude Code 内部运行，你在自己的终端里提交时不会运行 | 一条规则必须每次都成立，而且脚本能判定它 |
| **技能**——`.claude/skills/<name>/SKILL.md`，在相关时加载或以 `/<name>` 运行；spec-kit 1.0 的 `/speckit-plan` 就是一个 | 会让 `CLAUDE.md` 膨胀的流程或参考资料：发布检查清单、风格指南 | 强制执行任何事。Claude「会解读这些指令；结果可能不同」，而且默认情况下它的描述会加载进每一次会话 | 你第三次把同一段多步骤流程粘贴进聊天 |
| **子智能体**——`.claude/agents/<name>.md`，或者「用一个子智能体来……」 | 一个拥有自己的上下文窗口和工具列表、只返回摘要的工作者：大范围调研，或者由一个没写这段代码的会话来评审 | 看到你的对话——它只拿到你传给它的内容，外加 `CLAUDE.md`。它不强制执行任何事，它的摘要仍然是一个需要检查的说法 | 一项旁支任务会淹没你的上下文，或者这项工作需要一个没写它的评审者 |

（来源：code.claude.com/docs/en/features-overview 和 code.claude.com/docs/en/hooks，2026-09-26 查阅。）SignUpFlow 的 `.claude/` 文件夹里只有它的 spec-kit 命令（`SignUpFlow/.claude/commands/`）——没有钩子、技能、子智能体或规则文件。它在 Claude Code 之外应用了钩子的原则：它的受保护智能体运行器会让一次被禁止的 Git 变更失败，「即使智能体忽略命令错误并打印 DONE」（`SignUpFlow/docs/AGENT_RUNNER.md:27-29`），并且有一个策略回归测试守护着无 CI 规则（`SignUpFlow/tests/unit/test_local_validation_policy.py`）。一条绝不能被打破的规则，要配一个由脚本运行的检查，而不是一句由模型阅读的话。实验 M1 会给你的起始仓库配上这样一个钩子。

### 行动步骤

打开你的循环日志（loop journal），为**你自己的起始仓库起草三条规则**，每层一条：一条宪章原则（一句话，带 MUST 或默认关闭的安全立场）、一条 `AGENTS.md` 基线规则（祈使 + 可验证）、一条研究日志观察（带日期，来自你在第 0 模块中真实遇到的事——一次安装小问题也算）。改写任何没通过这项检验的规则：*一个陌生人能检查它是否被遵守吗？* 然后挑出你最不放心让智能体遵守的那条规则，从上表中为它选定机制——它继续作为规则，还是改成钩子？在实验 M1 中，这些会变成你真正的文件。

## M1.2 — 规格 → 计划 → 智能体能执行的任务（约 20 分钟）

### 目标

说出每个 spec-kit 产物及其一句话职责，并把一个用户故事转化为一个验收场景外加一条智能体无需对话上下文就能执行的任务行。

### 讲解

SignUpFlow 的功能是用 GitHub 的 spec-kit 构建的，它的命令会在 `specs/` 下产出一个产物文件夹。这个仓库在 2025 年 10 月安装了 spec-kit，文档里记录的是旧的带点号命令名——`/speckit.specify` → `/speckit.clarify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.analyze` → `/speckit.implement`，再用 `/speckit.checklist` 检查需求（`SignUpFlow/docs/SPEC_KIT_SETUP.md:9-18`）。spec-kit 1.0（2026-08-21 发布）把同样的步骤作为技能安装进 Claude Code：每个项目运行一次 `/speckit-constitution`，然后每个功能依次运行 `/speckit-specify` → `/speckit-plan` → `/speckit-tasks` → `/speckit-implement` → `/speckit-converge`，clarify、checklist 和 analyze 是可选的（github.com/github/spec-kit README，2026-09-26 查阅）。M4.1 会逐一讲解其中的差异。产物没有变。这样的文件夹有十七个（`SignUpFlow/specs/`）。每个产物只有一项职责：

| 产物 | 职责（一句话） |
|---|---|
| `spec.md` | **做什么（WHAT）**，与技术无关：按优先级排列的用户故事（P1/P2/P3，每个都可独立测试——一个 MVP 切片）、Given/When/Then 验收场景、边界情况、成功标准 |
| `research.md` | 决策：带编号的条目，包含评估过的选项、理由和被否决的备选方案——"## Decision 1: Rate Limiting Infrastructure"（`SignUpFlow/specs/014-security-hardening/research.md`） |
| `data-model.md` | 实体和关系，先于代码存在 |
| `plan.md` | **怎么做（HOW）**：技术背景加一道关卡——「*关卡：必须在第 0 阶段研究之前通过。第 1 阶段设计之后重新检查*」（`SignUpFlow/specs/014-security-hardening/plan.md`，"Constitution Check"） |
| `contracts/` | 按领域划分的接口：类定义、错误键、测试草图、基准——规格 014 有 6 个契约文件（`00-research/02-signupflow-deep-read.md`，§2） |
| `quickstart.md` | 带验证检查清单的限时部署路径 |
| `checklists/requirements.md` | 规划之前的质量关卡：「没有实现细节（语言、框架、API）」「没有残留的 [NEEDS CLARIFICATION] 标记」「需求可测试且无歧义」（`SignUpFlow/specs/014-security-hardening/checklists/requirements.md`） |
| `tasks.md` | 可执行的清单：采用 `[ID] [P?] [Story]` 格式的勾选任务、精确的文件路径、先写测试 |

有两条纪律最要紧。**规格写做什么，不写怎么做。** 规格（the WHAT）说明*用户需要什么*；技术决策写在 `research.md` 和 `plan.md` 里。规格 014 自己的检查清单证实了这种划分：规格描述安全能力「而不规定怎么做」，技术选择推迟到规划阶段（`SignUpFlow/specs/014-security-hardening/checklists/requirements.md`）。**引用精确的路径。** 任务行（task line）写明要改的文件，这样一个没有对话记忆的智能体也能执行——真实的例子：「`T027 [US1] Implement POST /api/sms/send endpoint per contracts/sms-api.md in api/routers/sms.py`」（`SignUpFlow/specs/019-sms-notifications/tasks.md`）。

**ListenToMe 的变体**是用 Swift 践行的同一种纪律。它的设计规格定义了协议层接口——`AudioCapturing`、`Transcribing`，带精确的 Swift 签名——让实现保持可替换（`ListenToMe/docs/superpowers/specs/2026-06-18-listentome-design.md`，§4）——还有一份 **YAGNI 非目标（YAGNI non-goals）**清单：「没有云后端、账号、计费或多用户……没有隐蔽/『潜行』模式」（§2）。它的实现计划是一份 2,410 行的 TDD 任务清单（「写失败的测试，看着它失败，写最少的代码，看着它通过，提交」），结尾是一份**把每条规格要点对应到任务的自查对照（self-review mapping）**：「端侧 STT 位于可替换的 `Transcribing` 协议之后 → 任务 10、13。✅」（`ListenToMe/docs/superpowers/plans/2026-06-18-listentome-mvp.md`）。非目标和自查，正是防止一份由智能体构建的计划自行其是的东西。

**一个完整的例子——从用户故事到可执行的一行。** 从 SignUpFlow 的领域里取一个贴近真实的用户故事（志愿者确实可以屏蔽日期；这个功能以可用时间路由的形式存在——`SignUpFlow/api/routers/availability.py`，「管理人员的可用时间和休假」）：

> **US1（P1）：** 作为志愿者，我可以屏蔽某些日期，让求解器跳过我。

把它转化为一个验收场景（acceptance scenario）：

> **假设（Given）**志愿者 Sarah 有一段覆盖 2026-04-23 的屏蔽期，**当（When）**管理员为那一周运行求解器时，**那么（Then）** Sarah 不会被分配，并且解报告零个硬约束违规。

然后用仓库的真实格式写一条任务行：

```text
- [ ] T031 [P] [US1] Implement POST /api/v1/availability/time-off in
      api/routers/availability.py per contracts/availability-api.md: volunteer
      submits blocked dates; write the failing test in tests/api/test_availability.py first
```

注意刚才发生了什么：一句意图变成了一个*可检查的*场景（日期、预期结果、一个可衡量的主张），以及一个写明文件、契约、测试文件和顺序（先写测试）的任务。一个全新的智能体会话——或者一位队友——无需再做任何沟通就能执行它。这正是这条流水线的全部意义：**规格是人的意图与智能体执行之间的接口**（`00-research/00-synthesis.md`）。

### 行动步骤

挑一个你在本课程中真正想构建的功能（任何产品原型都行）。在你的循环日志中写下：一句话的用户故事并标上优先级、一个 Given/When/Then 验收场景，以及一条引用你将创建的精确文件路径的任务行。在实验 M1 中，它会变成你起始仓库里的 `specs/001-todo-command/`——形态相同，功能更小。

## M1.3 — 证据纪律：验证是一份记录，而不是一种感觉（约 20 分钟）

### 目标

解释 SignUpFlow 的无 CI 本地验证策略，按它的确切格式写一份证据记录，并在你自己的工作中践行「把失败写进去」。

### 讲解

SignUpFlow **不运行任何 CI 检查**。这是一项有意为之、经过测试的策略，而不是疏漏，即无 CI 本地验证（no-CI local validation）：「没有 CI 检查。所有代码评审、静态分析、迁移、测试、安全扫描和产物验证都在本地运行。为已推送的版本记录证据；永远不要重建托管检查，也不要要求 CI 状态」（`SignUpFlow/.specify/memory/constitution.md`，"Current Validation Policy (2026-09-13)"）。甚至有一个策略回归测试守护着它（`SignUpFlow/tests/unit/test_local_validation_policy.py`）。

一个生产级 SaaS 为什么要拒绝 CI？因为托管检查并不是一份*你验证了什么的记录*——它是一张通过/失败的快照，对命令、环境和局限只字不提。SignUpFlow 用更有力的东西替代了它：**证据随版本一起流转。** 每个 PR 都在本地运行 `make test-all`，并「在 PR 中记录命令、结果、局限和已推送的 head SHA」（`SignUpFlow/AGENTS.md`，PR 规则）——包括计数、带日期、写明环境。你在第 0 模块见过的那条全套件结果行位于 `docs/playbooks/validation.md`："make test-all: 420 unit tests passed, 21 skipped; 444 API, 16 CLI, and 325 integration tests passed... 1,464 passed, 21 skipped"，后续验证「从 `cccc6f7` 开始」——一个把证据固定到确切版本的 head SHA。

硬性规则：**「不要伪造状态检查、绕过保护措施，或把缺失的证据当作成功」**（`SignUpFlow/AGENTS.md`，PR 规则）。感觉是绿的，不等于套件是绿的。

**把失败写进去。** 同一份验证记录展示了这在实践中意味着什么。一次浏览器时序竞态被记录下来，而不是被隐藏：「一个较早的周期性活动浏览器测试暴露了一个点击竞态；在点击它新渲染出的 Delete 控件之前，要等待 HTMX 稳定」——并且「这次最初的失败没有从证据中省略」（`SignUpFlow/docs/playbooks/validation.md`）。已知的技术债按债务来命名："Full API mypy | Existing debt: 835 errors in 40 files; not a pass"（`SignUpFlow/docs/playbooks/validation.md`）。记录以局限收尾：「不要把人工运营演练、外部投递、PostgreSQL、DST、场地排期或完整的租户隔离算作已被这些运行验证」（`SignUpFlow/docs/playbooks/validation.md`）。一份不能写出「未验证」的证据记录（evidence record）不是证据——它是营销。

**完成的定义意味着在真实的东西上验证过。** ListenToMe 的完成的定义（Definition of Done, DoD）要求维护者「在已安装的生产应用中验证受影响的行为。对于音频改动，要验证真实的系统音频转写被标注为 OTHERS；**一个权限开关或麦克风拾音不算证明**」（`ListenToMe/AGENTS.md`）。它的检查清单还会扫一遍这次改动涉及的每一份文档：「**过时的文档是完成的定义上的失败**，而不是后续事项」（`ListenToMe/CLAUDE.md`）。测试验证的是你构建的东西；完成的定义验证的是你交付的东西。

**诚实评审的模式。** 三个仓库中最有力的产物，是 ListenToMe 对自己发布候选版本做的差距评审：「**建议：不要把现有的 1.3.0 DMG 作为一个经过广泛验证的生产版本来推广。**」——*尽管*有「215 个通过的 Core 测试，以及 97.24% 的 Core 覆盖率」，因为这些数字「并不能证明采集的可靠性、持久保存、准确的说话人归属，或可用的首次运行体验」（`ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md`）。AI × QE 把同样的诚实当作一种习惯来践行：它的研究日志要求「每个条目都记录问题、检查了什么、结果，以及网站上改了什么」（`ai_qe/docs/research-log.md`），并且它公开了自己一份包含 14 项发现的网站审计（`ai_qe/research/reviews/site-audit-2026-09-06.md`）。覆盖率告诉你测试了什么。只有一份诚实的记录才能告诉你交付了什么。

**你的证据日志模板。** 原样复制它，在本课程的每个实验中使用：

```markdown
## Evidence — <project> — <feature> — <YYYY-MM-DD>
Commands (with results):
- <command> → <N passed, M skipped, K failed>
- ...
Environment: <OS, Python version, machine notes>
Revision: <`git rev-parse HEAD` output>
Limitations / not verified:
- <honest list — include at least one>
```

如果某次运行失败，你修复后重新运行，两行都要记录。如果你跳过了什么，就写下这次跳过。承认一次失败的记录，比隐藏失败的徽章更有价值。

### 行动步骤

打开你的循环日志，现在就写一条证据条目，记录你在第 0 模块中做的那次 SignUpFlow 求解器运行（或你今天运行过的任何命令）：确切的命令、结果行、你的环境、日期，以及至少一条局限（例如「仅限示例数据；健康分来自 my-church 工作区，不是真实租户」）。然后对照上面的模板检查——每个字段都要填上。这个习惯在之后的每个实验中都占你成绩的 20%。

## 回顾

- **治理：** 一份 85 行的宪章位于一份 188 行、每个智能体都会读的 `AGENTS.md` 之上。`CLAUDE.md` 用 `@AGENTS.md` 导入它，只补充 Claude 的附加说明；SignUpFlow 154 行的 `CLAUDE.md` 仍然用的是链接。每个文件都采用祈使语气、可验证、不超过约 200 行（`SignUpFlow/.specify/memory/constitution.md`、`SignUpFlow/AGENTS.md`、`SignUpFlow/CLAUDE.md:5`）。
- **机制：** 规则提供建议，钩子强制执行，技能承载流程，子智能体隔离工作。一条必须每次都成立的规则要变成钩子（code.claude.com/docs/en/best-practices，2026-09-26 查阅）。
- **优先级：** 五个级别，冲突时「遵循更具体、更安全的那一条」（`SignUpFlow/AGENTS.md`）。
- **防幻觉：** 引用之前先 grep；从权威来源读取事实；有歧义时给出 2-3 个有区别的选项（`SignUpFlow/AGENTS.md`）。
- **规则晋级：** 研究日志中的观察 → 在真实改动上试用 → 提升 → 推送到上游（`SignUpFlow/docs/ai-agent-coding-strategy.md`）。
- **规格流水线：** spec（做什么，P1/P2/P3，Given/When/Then）→ research（带编号的决策）→ data-model → plan（宪章检查关卡）→ contracts → quickstart → checklist 关卡 → tasks（`[ID] [P?] [Story]`、精确路径、先写测试）。
- **证据：** 命令、计数、日期、环境、局限、head SHA；永远不要伪造检查；把失败写进去——点击竞态和 mypy 的 "not a pass" 那一行就是范例（`SignUpFlow/docs/playbooks/validation.md`）。
- **完成就是真的完成：** 在已安装的应用中验证过（「一个权限开关不算证明」）、文档是最新的，并且在证据表明应当如此时，诚实的评审会说「不要推广」（`ListenToMe/AGENTS.md`、`ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md`）。

## 讨论题

发布你从模糊改写为可验证的那一条规则（改写前 → 改写后），外加你刚写的第 0 模块证据条目。然后读两位同学的规则并回答：**你能否在不问他们任何问题的情况下，亲自检查他们的规则是否被遵守？** 如果不能，就说出是哪个词让它无法检查——这条评论就是全部的技能。
