---
marp: true
theme: aps
paginate: true
title: M1 — AI 产品操作系统
---

<!-- _class: lead -->
# M1 — AI 产品操作系统

**承诺：** 在你自己的仓库里治理智能体、规定工作、记录证据。

```figure
kind: flow
alt: AI 产品操作系统——治理、规格和证据——最终落到你自己的宪章、AGENTS.md，以及一次从规格到 TDD 的循环。
step: 治理 — 宪章 · AGENTS.md @ 本模块交给你的
step: 规格 — spec-kit，每一步一个文件 @ 本模块交给你的
step: 证据 — 命令、计数、局限 @ 本模块交给你的
step: 你的仓库 (hl) — 宪章、AGENTS.md、一次从规格到 TDD 的循环 @ 学完本模块，你会写出
```

**时长：** 约 60 分钟 · 3 个分段 · 实验 M1 约 2 小时

<!-- NOTES: 欢迎来到第 1 模块。第 0 模块给了你三个已交付的产品和一个循环；本模块交给你的，是让一位工程师与 AI 智能体协作就能交付这些产品的那套机制。治理、规格、证据纪律——三个部分，三个分段。学完本模块，你会写出自己的宪章和 AGENTS.md，并完整跑通一次从规格到 TDD 的循环。交付物是这些产物，而不是笔记。过渡：先准确说明你将能做到什么。时间：1 分钟。 -->

---

## 学完本模块，你能够……

- 写出分层的智能体规则：祈使语气、可验证、不超过约 200 行。
- 应用五级指令优先级和防幻觉规则。
- 把一个用户故事转化为一个场景和一个任务。
- 用命令、计数、日期、局限和 head SHA 记录验证证据。

<!-- NOTES: 四项能力，每一项都可以检查。注意它们都是动词：写、应用、转化、记录。而不是「理解治理」。你会按产物评分，而这里的每一件产物都是你起始仓库里的一个文件。实验闭合这个循环：一份宪章、一份 AGENTS.md、一个规格文件夹，以及一次如实记录的先红后绿的 pytest 运行。过渡：第一项能力——治理。时间：2 分钟。 -->

---

## 为什么治理先于产品类型

```figure
kind: compare
alt: 代码如今以智能体的速度到来，而验证仍停留在人的速度，于是瓶颈转移到说清要什么、验证得到了什么，以及承认局限。
column: 智能体抬高了利害 (bad) @ 代码现在以智能体的速度出现
  item: 代码以智能体的速度出现
  item: 验证仍是人的速度
column: 瓶颈转移到 (good) @ 于是瓶颈转移了
  item: 说清你要什么
  item: 验证你得到了什么
  item: 承认验证范围的局限
```

- 产品原型各不相同；操作系统完全一样。
- 大多数构建者跳过它，然后为此付出代价。

<!-- NOTES: 这是本模块的论点。当代码生成得很快时，稀缺的资源就不再是打字。而是清楚地说明你要什么、检查你是否得到了它，以及如实说明实际验证了什么。SignUpFlow 的深度解读在第一节里提出了这一点。三种产品原型的区别在于构建什么，而从不在于如何治理构建过程。过渡：下面就是负责治理的那套指令栈。时间：2 分钟。 -->

---

## M1.1 — 四文件指令栈

一个权威来源，多个分发文件。

```figure
kind: system
alt: 一个权威来源，多个分发文件——宪章位于 AGENTS.md 之上，多数编码智能体原生读取 AGENTS.md；CLAUDE.md 为 Claude Code 导入它，一份重述文件把规则带给 Copilot。
source: SignUpFlow/.specify/memory/constitution.md · SignUpFlow/AGENTS.md · SignUpFlow/CLAUDE.md
layer: 事实来源 @ 宪章位于所有智能体文件之上
  node const: .specify/memory/constitution.md (hl) — 位于所有智能体文件之上
layer: 基线 @ 基线写在 AGENTS.md 里
  node agents: AGENTS.md — 通用基线
layer: 分发文件
  node claude: CLAUDE.md — 你的版本导入 @AGENTS.md @ SignUpFlow 的 CLAUDE.md
  node copilot: .github/copilot-instructions.md — 一份重述 @ Copilot 需要
layer: 读取它们的智能体
  node many: Codex CLI · Cursor · Aider · Jules · OpenHands · Amp · Factory @ 基线写在 AGENTS.md 里
  node cc: Claude Code @ 所以在你自己的仓库里
  node ghc: GitHub Copilot @ Copilot 需要
edge: const -> agents — 唯一的事实来源 @ 宪章位于所有智能体文件之上
edge: agents -> many — 原生读取 @ 基线写在 AGENTS.md 里
edge: agents -> claude — 导入，而不只是链接 (hl) @ 所以在你自己的仓库里
edge: agents -> copilot — 重述 @ Copilot 需要
edge: claude -> cc — 启动时加载 @ 所以在你自己的仓库里
edge: copilot -> ghc @ Copilot 需要
```

<!-- NOTES: 四个文件，一个权威来源。基线写在 AGENTS.md 里，由 Codex CLI、Cursor、Aider、Jules、OpenHands、Sourcegraph Amp 和 Factory 读取。SignUpFlow 的 CLAUDE.md 在开头链接到它，并补充 Claude 专用的附加说明。链接不等于导入：Claude Code 只有在自己决定时才会打开被链接的文件，所以你自己的 CLAUDE.md 要用一行 at 符号导入 AGENTS.md，两个文件在启动时一起加载。Copilot 需要自己的一份重述文件。宪章是位于它们所有之上的唯一事实来源。过渡：下一张幻灯片证明这些长度是真实的。时间：3 分钟。 -->

---

<!-- _class: proof -->
## 证据：指令栈与真实行数

| SignUpFlow 文件 | 行数 | 作用 |
|---|---|---|
| `.specify/memory/constitution.md` | 85 | 原则，唯一的事实来源 |
| `AGENTS.md` | 188 | 通用基线 |
| `CLAUDE.md` | 154 | 交叉引用加附加说明 |
| `.github/copilot-instructions.md` | 127 | 给 Copilot 的重述 |

```markdown
# SignUpFlow Constitution
> A roster and scheduling system with email/SMS notifications.
```

指针：`SignUpFlow/.specify/memory/constitution.md:1-3`

<!-- NOTES: 在你自己的克隆里打开这四个文件，数一数。宪章 85 行，AGENTS.md 188 行，CLAUDE.md 154 行，Copilot 文件 127 行——全都在写作风格规定的约 200 行上限之内。课文把它做成了一张表，你可以用 wc -l 核对。为什么这很重要：智能体无法装进上下文的规则文件，就是它不会遵守的规则文件。过渡：短是必要条件，但不充分——规则还必须可检查。时间：3 分钟。 -->

---

## 写作风格：规则必须可验证

- 用祈使语气，而不是建议。
- 陌生人能检查它是否被遵守。
- 数字胜过形容词：「不超过约 200 行」。
- 命令胜过散文：写出确切的检查。
- 智能体无法检查的规则只是一种感觉。

<!-- NOTES: 这是写作风格的核心。仓库直接写明了这种对比：每条规则都必须可验证——要写「每条查询都按 org_id 过滤」，而不是「多租户要小心」。「小心」无法执行，也无法检查；过滤可以。同样的检验也适用于你在实验 M1 中写的文件：一个陌生人能否在不问你任何问题的情况下，检查这条规则是否被遵守？过渡：用四条真实的规则来做这个检验。时间：3 分钟。 -->

---

## 对照表

| 坏规则 | 好规则 |
|---|---|
| 「多租户要小心」 | 「每条查询都按 `org_id` 过滤」 |
| 「保持文件易于管理」 | 「每个文件不超过约 200 行」 |
| 「重视测试覆盖率」 | 「先写测试；运行 `make test-unit`」 |
| 「妥善处理密钥」 | 「永远不要提交密钥；从环境变量读取」 |

指针：`SignUpFlow/AGENTS.md`，"House style" 和 "Safety"

<!-- NOTES: 四组改写，全部取自 AGENTS.md。看看每一次变了什么。「小心」变成了一个过滤。「易于管理」变成了一个数字。「重视覆盖率」变成了一个动作加一条检查命令。「妥善」变成了一条可以 grep 的禁令：永远不要提交 X。这就是你在实验中要做的练习，也是讨论题——把你的改写前后对比发出来。过渡：宪章是规则中的一个特殊子集。时间：3 分钟。 -->

---

## 宪章里放什么

85 行里的四条原则——只保留绝不能偏离的东西。

| 原则 | 它固定了什么 |
|---|---|
| 原生优先（Native First） | 本地用 Poetry + SQLite，不用 Docker |
| 测试驱动实现（Test-Driven Implementation） | 先写最小的失败测试 |
| 简单与 YAGNI（Simplicity & YAGNI） | 只构建确切需要的东西，不多做 |
| 安全与可靠（Safety & Reliability） | `EMAIL_ENABLED=false`、`SMS_ENABLED=false` |

- 支付在本地必须（MUST）被模拟或关闭。
- 自主权是固定的：YOLO DISABLED，Git autonomy ENABLED。

指针：`SignUpFlow/.specify/memory/constitution.md:41-53`

<!-- NOTES: 宪章不是更长的 AGENTS.md。它只保存少数绝不能偏离的东西。SignUpFlow 的四条原则是：原生优先——本地开发优先用普通的 Poetry 和 SQLite 而不是 Docker——测试驱动实现、简单与 YAGNI，以及安全与可靠。安全这一条是具体的：电子邮件和短信默认关闭，支付被模拟或关闭。自主权同样是固定的：智能体可以提交完成的工作，但绝不能运行未经检查的破坏性命令。过渡：两条规则冲突时，哪一条胜出？时间：3 分钟。 -->

---

## 优先级：五个级别，一条决胜规则

| # | 规则来源 |
|---|---|
| 1 | 当前任务中用户的请求 |
| 2 | 仓库规则：`CLAUDE.md` 和 `AGENTS.md` |
| 3 | `.github/instructions/` 下按路径限定的规则 |
| 4 | `docs/ai-agent-coding-strategy.md` 中的指导 |
| 5 | 推断出的最佳实践 |

决胜规则：**遵循更具体、更安全的那一条。**

指针：`SignUpFlow/AGENTS.md:153-161`

<!-- NOTES: AGENTS.md 中的五个级别。用户的请求位于最高级并胜出。仓库规则紧随其后。给 Copilot 的按路径限定的规则排第三。通用的策略指导排第四，推断出的最佳实践排最后。规则重叠时唯一的决胜规则就是要背下来的那句话：遵循更具体、更安全的那一条。正因如此，一条具体的路径规则可以胜过通用基线，而无需任何人维护一张优先级矩阵。过渡：让智能体在事实上保持诚实的那些规则。时间：3 分钟。 -->

---

## 防幻觉规则

- 不要虚构路径、函数名、路由或标识符。
- 引用任何东西之前先 grep 仓库。
- 从权威来源读取事实；不要凭记忆回想。
- 请求有歧义？给出 2-3 个有区别的选项。
- 为研究类任务写好一份硬性停止检查清单。

<!-- NOTES: 幻觉是智能体辅助工作中最大的失败模式，所以它得到的是规则，而不是建议。AGENTS.md 禁止虚构文件路径、函数名、路由路径、命令、URL 或标识符——先 grep。对于 schema 字段和环境变量名，要从权威来源读取，不要凭记忆回想。请求有歧义时，给出两到三个有区别的选项，而不是猜测。每一条都可以对照对话记录来检查。过渡：规则不是一出生就成形的；它们要逐级晋升。时间：3 分钟。 -->

---

## 规则如何晋级

- 观察记录在 `docs/research-log.md` 中。
- 至少在一次真实的改动上试用。
- 只有在那之后才提升进 `AGENTS.md`。

<!-- _diagram: flow -->

- `pending`
- `extracted`
- `promoted`

- 来源行按 `pending → extracted → promoted` 推进。
- 如果它具有普遍性，就推送到上游的 `GenAI_Common`。

<!-- NOTES: 新规则不会直接进入 AGENTS.md。策略文档定义了这条流水线：一条观察先落在 docs/research-log.md 里，这个文件的存在正是为了让探索性笔记永远不会变成无声的规则。它要在一次真实的改动上试用。只有在那之后才会被提升。source-repos 中的那一行从 pending 变为 extracted，再变为 promoted；如果它具有普遍性，就会被推送到上游的 tomqwu/GenAI_Common。规则赢得一席之地的方式与功能一样：经受住真实工作的检验。过渡：这就是治理；接下来是治理所保护的那些产物。时间：3 分钟。 -->

---

## M1.2 — spec-kit 流水线

<!-- _diagram: flow -->

- `/speckit-constitution`
- `/speckit-specify`
- `/speckit-plan`
- `/speckit-tasks`
- `/speckit-implement`
- `/speckit-converge`

- 可选：clarify、checklist、analyze。SignUpFlow 用的是旧的带点号名称。
- 输出：`specs/` 下的一个产物文件夹；SignUpFlow 有 17 个。

<!-- NOTES: spec-kit 1.0 每个项目运行一次 constitution，然后对每个功能依次运行 specify、plan、tasks、implement 和 converge；converge 对照规格检查代码，并把任何未完成的工作作为新任务加进来。clarify、checklist 和 analyze 是可选的。SignUpFlow 的文档仍然用旧的带点号名称来指代同样的步骤。每一步产出一个文件，这些文件就是你的意图与一个不记得你们对话的智能体会话之间的接口。仓库里有十七个规格文件夹，所以这不是理论。对于「智能体做错了」，这条流水线的回答几乎总是「规格没有写」。过渡：每个产物恰好只有一项职责。时间：3 分钟。 -->

---

## 每个产物只有一项职责

| 产物 | 职责 |
|---|---|
| `spec.md` | 「做什么」（WHAT）：P1/P2/P3 用户故事，Given/When/Then |
| `research.md` | 带编号的决策，附被否决的备选方案 |
| `data-model.md` | 实体与关系，先于代码 |
| `plan.md` | 「怎么做」（HOW），位于宪章检查关卡之后 |
| `contracts/` | 按领域划分的接口、错误、测试草图 |
| `quickstart.md` | 带验证的限时部署路径 |
| `checklists/` | 规划之前的质量关卡 |
| `tasks.md` | 带精确文件路径的勾选任务 |

<!-- NOTES: 这张表是本分段的主干，测验会考这些对应关系。最容易混淆的两对：spec.md 是与技术无关的「做什么」，而 research.md 和 plan.md 保存决策和「怎么做」。另外，checklists 是规划之前的质量关卡，而 quickstart 是部署路径。规格 014 自己的检查清单证实了这种划分：规格描述能力而不规定「怎么做」，技术选择推迟到规划阶段。过渡：下一张幻灯片是证据，其中包括一个被有意缺省的产物。时间：4 分钟。 -->

---

<!-- _class: proof -->
## 证据：这些产物都是真实的文件

- `SignUpFlow/specs/` 下的规格文件夹——共 17 个。
- 真实的任务行：`SignUpFlow/specs/019-sms-notifications/tasks.md`
- 真实的关卡：`SignUpFlow/specs/014-security-hardening/plan.md`
- 真实的检查清单：`.../014-security-hardening/checklists/requirements.md`
- 规格 014 **没有** `tasks.md`。

```markdown
- [ ] T027 [US1] Implement POST /api/sms/send endpoint per contracts/sms-api.md
  in api/routers/sms.py
- [ ] T028 [P] [US1] Implement GET /api/sms/messages endpoint (message history)
  per contracts/sms-api.md in api/routers/sms.py
```

<!-- NOTES: 是证据，而不是描述。SignUpFlow/specs/ 下有十七个文件夹。任务行 "T027 [US1] Implement POST /api/sms/send endpoint per contracts/sms-api.md in api/routers/sms.py" 是规格 019 中真实的一行。宪章检查关卡的那句话真实存在于规格 014 的计划中。再注意深度解读中的一个诚实细节：规格 014 没有 tasks.md。一个停在规划阶段的文件夹是合法的状态，记录也如实说明这一点，而不是虚构一个文件。过渡：一个用户故事如何变得可执行。时间：3 分钟。 -->

---

## 用户故事 → 场景 → 任务

- 用户故事：「作为志愿者，我可以屏蔽某些日期。」
- 场景：假设有一段屏蔽期，那么硬约束违规为零。
- 任务行（示意）：`[ID] [P?] [Story]` 加上精确路径。

```text illustrative
- [ ] T031 [P] [US1] Implement POST /api/v1/availability/time-off in
      api/routers/availability.py per contracts/availability-api.md:
      volunteer submits blocked dates; write the failing test in
      tests/api/test_availability.py first
```

- 测试优先：失败的测试是这个任务的第一个交付物。

指针：`SignUpFlow/api/routers/availability.py`

<!-- NOTES: 注意抽象层级的下降。一句意图变成一个可检查的场景，带有日期、可衡量的结果和一个具名的产物。然后它变成一个任务，写明要改的文件、要遵循的契约、要先写的测试文件，以及工作顺序。一个全新的智能体会话——或者一位队友——无需再做任何沟通就能执行它。这正是这条流水线的全部意义：规格是人的意图与智能体执行之间的接口。过渡：ListenToMe 用 Swift 践行同样的纪律。时间：4 分钟。 -->

---

## ListenToMe 的变体：协议与非目标

- 设计规格用 Swift 签名定义协议层接口。
- 可替换：`AudioCapturing`、`Transcribing`。
- YAGNI 非目标：没有云后端、账号、计费。
- 没有隐蔽或「潜行」模式。
- 2,410 行的 TDD 计划以一份从规格到任务的自查结尾。

<!-- NOTES: 同样的纪律，换了一种语言。ListenToMe 的设计规格固定了协议层接口，让实现保持可替换，并写下了非目标：没有云后端、账号、计费、多用户，也没有隐蔽模式。它的实现计划是一份 2,410 行的 TDD 任务清单，结尾是一份把每条规格要点对应到任务的自查——例如，「端侧语音转文字位于可替换的 Transcribing 协议之后」对应任务 10 和 13，已勾选。非目标和自查，正是防止一份由智能体构建的计划自行其是的东西。过渡：最后一个分段讲证据。时间：3 分钟。 -->

---

## M1.3 — 没有 CI 检查，这是策略

- 只在本地验证是一项经过测试的策略，而不是疏漏。
- 「永远不要重建托管检查，也不要要求 CI 状态。」

```figure
kind: compare
alt: 托管检查是一张通过或失败的快照，对命令、环境和局限只字不提；证据记录把三者都写明。
source: SignUpFlow/.specify/memory/constitution.md:34-39
column: 托管检查 (bad) @ 托管检查告诉你的
  item: 一张通过/失败的快照
  item: 对环境只字不提
  item: 对局限只字不提
column: 证据记录 (good) @ 所以证据改为随版本
  item: 命令、计数、日期
  item: 写明环境
  item: 列出哪些未经验证
```

指针：`SignUpFlow/.specify/memory/constitution.md:34-39`

<!-- NOTES: SignUpFlow 不运行任何 CI 检查。这是一项有意为之、经过测试的策略，写在其宪章的「当前验证策略」（Current Validation Policy）中，并且 tests/unit/test_local_validation_policy.py 中有一个策略回归测试守护着它。论点是：托管检查告诉你的只有通过或失败，对命令、环境和局限只字不提。用更有力的东西来替代它——证据随版本一起流转。每个 PR 都记录命令、结果、局限和已推送的 head SHA。过渡：下面就是那份记录，原文照录。时间：3 分钟。 -->

---

<!-- _class: proof -->
## 证据：证据行

```text
make test-all: 420 unit tests passed, 21 skipped;
444 API, 16 CLI, and 325 integration tests passed.
Across backend, web, contract and browser suites: 1,464 passed, 21 skipped.
```

- 指针：`SignUpFlow/docs/playbooks/validation.md`
- 日期为 2026-09-12；2026-09-13 被降级为历史参考。
- 后续验证从 `cccc6f7` 开始——一个固定的 head SHA。

<!-- NOTES: 这就是第 0 模块里的那一行，它的确切位置是：SignUpFlow 中的 docs/playbooks/validation.md，而不是 TESTING.md。仔细看第二条要点。这个文件的日期是 2026-09-12，并在 2026-09-13 被重新归类为历史参考，所以它是过去一次运行的证据，而不是实时状态徽章。后续验证从提交 cccc6f7 开始，把证据固定到一个确切的版本上。没有日期和 SHA 的计数不是证据。过渡：记录最难的纪律在于它包含什么。时间：4 分钟。 -->

---

## 把失败写进去

- 一次浏览器点击竞态被记录下来，而不是被隐藏。
- 「这次最初的失败没有从证据中省略。」
- 一份不能写出「未验证」的证据记录就是营销。

```text
| Full API mypy | Existing debt: 835 errors in 40 files; not a pass |

Do not count manual operational drills, external delivery, PostgreSQL, DST,
venue scheduling or full tenant isolation as verified by these runs.
```

指针：`SignUpFlow/docs/playbooks/validation.md:45, 69-70`

<!-- NOTES: 三个动作。第一，点名一次真实的失败：一个较早的周期性活动浏览器测试暴露了一个点击竞态；修复被记录下来，最初的失败留在文档中。第二，已知的技术债按债务来命名：完整 API 的 mypy 在 40 个文件中有 835 个错误，记录写的是 "not a pass"，而不是把它四舍五入掉。第三，记录以局限收尾：不要把人工运营演练、外部投递、PostgreSQL、DST、场地排期或完整的租户隔离算作已验证。过渡：测试全绿之后，「完成」意味着什么。时间：3 分钟。 -->

---

## 完成意味着在交付的东西上验证过

- 测试验证你构建的东西；DoD 验证你交付的东西。
- 在已安装的生产应用中验证。
- 过时的文档是完成的定义上的失败。
- ListenToMe 自己的评审写道：不要推广 1.3.0。

> 对于音频改动，要验证真实的系统音频转写被标注为 OTHERS；
> 一个权限开关或麦克风拾音不算证明。

指针：`ListenToMe/AGENTS.md:21-23`

<!-- NOTES: ListenToMe 的完成的定义要求维护者在已安装的生产应用中验证受影响的行为。对于音频改动，要验证真实的系统音频转写被标注为 OTHERS——一个权限开关或麦克风拾音不算证明。它的检查清单还写明：过时的文档是完成的定义上的失败，而不是后续事项。三个仓库中最有力的产物，是那份建议不要推广 1.3.0 的差距评审，尽管有 215 个通过的 Core 测试和 97.24% 的覆盖率，因为这些数字并不能证明采集的可靠性。过渡：现在就复制这个模板。时间：3 分钟。 -->

---

## 你的证据日志模板

```markdown template
## Evidence — <project> — <feature> — <YYYY-MM-DD>
Commands (with results):
- <command> → <N passed, M skipped, K failed>
Environment: <OS, Python version, machine notes>
Revision: <`git rev-parse HEAD` output>
Limitations / not verified:
- <honest list — include at least one>
```

<!-- NOTES: 原样复制它，在本课程余下的每个实验中使用。如果某次运行失败，你修复后重新运行，两行都要记录。如果你跳过了什么，就写下这次跳过。学员总是留空的那个字段是局限，而正是这个字段把一份记录和一枚徽章区分开来。这个习惯占每个实验成绩的百分之二十。过渡：现在构建属于你自己的整套东西。时间：3 分钟。 -->

---

## 实验 M1 — 构建你的操作系统

<!-- _diagram: steps -->

- 写 `constitution.md`（≤80 行）、`AGENTS.md`（≤200 行）和 `CLAUDE.md`。
- 写 `specs/001-todo-command/`：规格、带关卡的计划、任务。
- 跑 TDD：先写失败的测试，再实现，`pytest -q` 变绿。
- 记录红、绿、环境、head SHA、局限；由一个钩子检查。

通过关卡：产物存在；`pytest tests/ -q` 以 0 退出。

<!-- NOTES: 两小时。你创建一个起始仓库，写一份不超过八十行的宪章和一份不超过两百行的 AGENTS.md，再加一个导入它的 CLAUDE.md，以及一个检查你证据日志的钩子，然后为一个小型 todo CLI 功能写一个规格文件夹。接着真正跑一次循环：写失败的测试，看着它们失败，实现，看着它们通过，提交。通过关卡是客观的：产物存在，并且 pytest 以零退出。证据条目不是可选的——它就是这个实验的意义所在。过渡：用测验检查你的理解。时间：3 分钟。 -->

---

## 测验 M1

- 8 道题：6 道选择题，2 道简答题。
- 涵盖规则可验证性、优先级、产物职责、证据。
- 简答题考应用，而不是记忆。
- 在研讨会之前完成；实验按证据评分。

<!-- NOTES: 八道题，六道选择题，两道简答题。第 7 题要求你写一个 Given/When/Then 场景和一条任务行；第 8 题要求一份完整的证据条目，并让一次不稳定的失败保持可见。这两项正是本模块真正要教的技能。在研讨会之前完成测验，这样我们就能把现场时间花在你改写的规则上，而不是花在定义上。过渡：回顾。时间：1 分钟。 -->

---

## 回顾

- 治理：85 行的宪章、188 行的基线，每条规则都可验证。
- 优先级：五个级别；更具体、更安全的规则胜出。
- 防幻觉：先 grep；读权威来源；给出选项。
- 规格流水线：做什么 → 决策 → 怎么做 → 任务。
- 证据：命令、计数、日期、环境、局限、head SHA。
- 把失败写进去；「不算通过」也是有效的。

<!-- NOTES: 六行，每行一个观点。如果别的都记不住，就记住这些：无法检查的规则只是一种感觉；没有精确路径的规格无法执行；没有局限的证据记录就是营销。这三句话就是本模块。其余一切都是实现它们的机制。过渡：用一道讨论题收尾。时间：2 分钟。 -->

---

## 讨论

- 发布你改写前 → 改写后的规则。
- 发布你在第 0 模块写的证据条目。
- 评审两位同学的规则。
- 自问：我能在不问他们任何问题的情况下检查它吗？
- 指出让它无法检查的那个词。

<!-- NOTES: 发布那条模糊的规则和它可验证的改写，外加你在第 0 模块写的证据条目。然后读两位同学的 AGENTS.md 规则，回答一个问题：你能否在不问他们任何问题的情况下，亲自检查他们的规则是否被遵守？如果不能，就指出让它无法检查的那个确切的词。这条评论就是全部的技能——它正是这个仓库用来检验自己的同一个测试。时间：2 分钟；结束本分段。 -->
