---
marp: true
theme: aps
paginate: true
title: M4 — 规格驱动的 SaaS：从想法到可执行规格
---

# M4 — 规格驱动的 SaaS

**承诺：** 产出一个陌生人拿来就能实现的规格文件夹。
**时长：** 约 75 分钟讲授 + 90–120 分钟实验 M4。
**案例研究：** SignUpFlow · `specs/014-security-hardening/`

```figure
kind: flow
alt: 一个足够完整的规格文件夹：一个没有聊天记录的全新智能体会话，不提任何问题就能实现故事 1。
source: SignUpFlow/specs/014-security-hardening/spec.md
step: 你的规格文件夹 — spec · plan · tasks @ 承诺范围很窄
step: 一个全新的智能体会话 (seam) — 没有聊天记录，不提问题 @ 承诺范围很窄
step: 故事 1，已实现 (hl) @ 承诺范围很窄
```

<!-- NOTES: 欢迎来到第 4 模块。在 M1 中你拿到了一套操作系统；今天我们在一个真实的多租户 SaaS 上以生产规模运行它。承诺范围很窄，而且可以检验：学完本模块，你能产出一个足够完整的规格文件夹，让一个全新的智能体会话——没有聊天记录，也不记得你的任何推理——不问你一个问题就能实现故事 1。SignUpFlow 用 spec-kit 的斜杠命令驱动功能开发，它的 17 个规格文件夹就是证据。时间安排：M4.1 约 25 分钟，走读一个文件夹；M4.2 约 25 分钟，讲质量；M4.3 约 25 分钟，讲如何诚实地交付。过渡：首先，看整条流水线的形态。 -->

---

## 学完本模块，你能够……

- **逐一走读**一个生产环境的规格文件夹，一个产物接一个产物
- **运行** specify → clarify → checklist → plan → tasks
- 用陌生人测试**评判**规格
- **执行**检查清单关卡的通过规则
- 用标注严重级别的评审**记录**变更
- **抓住**生成产物中的漂移

<!-- NOTES: 把这些读成六个动词，而不是六个主题——每一个都是你在实验中要亲手做的事，而不只是听说过的事。走读、运行、评判、执行、记录、抓住。最后两项正是演示与交付物的分界线：谁都能生成一个漂亮的规格文件夹；真正的纪律在于在本地评审它，让每条发现都写明严重级别和文件，并以怀疑而不是信任来对待生成的文件。如果今天你只记住两张幻灯片，就记住陌生人测试和漂移检查。过渡：先用一张图看整条流水线。 -->

---

## M4.1 — 命令链

```figure
kind: flow
alt: spec-kit 命令链——每条命令读取上一条写下的内容，在任何规划之前只有一道代价很低的关卡：检查清单。
step: specify — 做什么（WHAT） @ specify 写下
step: clarify — 最多 3 个问题 @ specify 写下
step: checklist (hl) — 唯一的关卡，在 plan 之前 @ 检查清单在任何规划之前
step: plan — 怎么做（HOW）：研究 · 数据模型 · 契约 · 宪章检查 @ 然后 plan 补上
step: tasks @ tasks 把它变成
step: implement ⇄ converge — 直到 Converged @ Spec-kit 1.0 让这个循环闭合
```

SignUpFlow 早于 1.0：带点号的命令位于 `.claude/commands/`。

<!-- NOTES: 这就是整个机制，它最大的优点就是乏味。每条斜杠命令都读取上一条写下的内容；没有任何东西要靠谁的脑子记着。`/speckit.specify` 写下做什么（WHAT）和需求检查清单；`/speckit.clarify` 消耗一个很小的提问预算；检查清单在任何规划之前把关；plan 补上怎么做（HOW）——研究决策、数据模型、钉住接缝的契约，以及宪章检查；tasks 把它变成工作。Spec-kit 1.0 让循环闭合：先 implement，再 converge——它对照规格检查代码，把未完成的工作追加为任务，直到报告 Converged。SignUpFlow 早于 1.0，所以它带点号的命令定义放在 `.claude/commands/` 中，模板放在 `.specify/templates/` 中——两者都能在克隆中打开。注意，这里只有一道关卡，而且代价很低。过渡：现在走读文件夹本身，从做什么开始。 -->

---

## 证明：`spec.md` 负责做什么（WHAT）

- 8 个故事；**六个 P1**，两个 P2
- 44 条 FR，全部是 "System MUST…"
- 7 个边界情况 · 12 条成功标准
- 带真实数字的 Given/When/Then
- 不提任何技术——没有 Redis，没有 SQL

```markdown
- **FR-001**: System MUST enforce rate limits on authentication endpoints, blocking
  requests after 5 failed attempts within 5 minutes per IP address
- …

1. **Given** a user attempts to log in, **When** they fail authentication 5 times
   within 5 minutes, **Then** further login attempts are blocked for 15 minutes
```

`specs/014-security-hardening/spec.md`

<!-- NOTES: 在屏幕上打开这个文件。US1 原文："Given a user attempts to log in, When they fail authentication 5 times within 5 minutes, Then further login attempts are blocked for 15 minutes." 这三个数字——5、5、15——会再次出现在一条 FR 里、一行契约配置里，以及一个测试断言里。这种反复出现正是重点。故事下面是分成九个类别组的 44 条功能需求，每一条都以 "System MUST" 表述，没有一条提到技术。八个故事中有六个 P1、两个 P2——数一数，因为 M4.3 会展示一个把它们数错了的生成文件。过渡：做什么敲定行为；研究敲定技术。 -->

---

## 证明：`research.md`——有据可查的决策

- 8 个编号决策，每个结构相同

<!-- _diagram: flow -->

- 决策
- 选项
- 理由
- 实现

- 决策 1：Redis，直接否决内存方案
- 决策 2：TOTP 优于 SMS

```markdown
## Decision 1: Rate Limiting Infrastructure

### Decision
**Use Redis for rate limit storage** (not in-memory)
```

`specs/014-security-hardening/research.md`

<!-- NOTES: 965 行，八个决策。结构从不变化：决策本身、评估过的选项及其利弊、理由，然后是实现细节。决策 1 选择 Redis，并指出内存计数器在重启时会丢失，也无法在多个 API 实例之间共享。决策 2 否决了 SMS，因为 NIST SP 800-63B 已弃用它，而且 SIM 卡交换攻击有大量记录。这里有一条值得照搬的规则：没有被否决方案的决策只是偏好，不是决策。把这个文件当作一份「未走之路」的记录来读。过渡：接下来，是 014 刻意没有的那个产物。 -->

---

## 证明：`plan.md`——怎么做（HOW），外加一处缺席

- **宪章检查（Constitution Check）**关卡：七条原则，七个结论
- 这里没有 `data-model.md`——安全横跨多个实体

```markdown
## Constitution Check
*GATE: Must pass before Phase 0 research.
Re-check after Phase 1 design.*
…
**Constitution Violations**: NONE
**Complexity Justification**: N/A (no violations to justify)
```

`specs/014-security-hardening/plan.md`, `.specify/templates/plan-template.md`

<!-- NOTES: 关卡那一行用的是模板的原话："Must pass before Phase 0 research. Re-check after Phase 1 design." 计划 014 逐条走过七条原则——User-First Testing（E2E 强制）、Security-First、Multi-tenant Isolation、Coverage Excellence、i18n by Default、Code Quality、Clear Documentation——为每条给出结论和证据，最后是零违规和一张空的 Complexity Tracking 表。注意这处诚实的缺席：014 没有 data-model.md，因为安全基础设施横跨许多实体，计划也明说了这一点。另外六个规格确实有它——模板定义了完整的集合；每个功能自己决定哪些产物值得保留。过渡：怎么做在契约中与做什么相遇。 -->

---

## 证明：`contracts/`——六条接缝

- rate-limiting 681 · 2fa-api 823 · audit-logging 900
- csrf 708 · session 748 · password-reset 801
- 合计 **4,661 行**
- 配置表重复了规格中的数字

```markdown
### Default Rate Limits
| Endpoint | Window | Limit | Scope | Lockout |
|----------|--------|-------|-------|---------|
| `POST /api/auth/login` | 5 min | 5 attempts | Per IP | 15 min |
| `POST /api/auth/signup` | 1 hour | 3 accounts | Per IP | 1 hour |
```

`specs/014-security-hardening/contracts/rate-limiting.md`

<!-- NOTES: 六份契约，合计 4,661 行。限流配置表的第一行是 `POST /api/auth/login`，5 分钟窗口，5 次尝试，按 IP，锁定 15 分钟——与 US1 验收场景同样的 5/5/15，现在还附上了范围和键格式。这正是契约的用途：它是做什么与怎么做第一次交汇的地方，也是任何一方都不得在边界上即兴发挥的地方。它还带有国际化错误消息、监控指标、测试草图和性能基准。如果你在实验中只精心写一个产物，就写契约。过渡：部署与关卡。 -->

---

## 证明：关卡与快速上手文档

- `quickstart.md`："10-Minute Deployment"，按时间分步
- `checklists/requirements.md`：三组通过/不通过检查
- 2025-10-22 由 specify 步骤自带的检查完成验证

```markdown
## Validation Results
✅ **ALL CHECKS PASSED**
…
**Quality Score**: 100% (all checklist items passed)
```

`SignUpFlow/specs/014-security-hardening/quickstart.md`
`SignUpFlow/specs/014-security-hardening/checklists/requirements.md:38-44`

<!-- NOTES: 快速上手文档是 643 行按时间分步的部署说明，带有像 `poetry add pyotp==2.9.0` 这样的精确命令。检查清单有 50 行，对三组内容评分：Content Quality、Requirement Completeness、Feature Readiness。它的第一条规则就是执行做什么/怎么做分离的那一行——"No implementation details"——结尾是 100% 的质量分。记住这个数字。在 M4.3 中，我会给你看这个文件里一个错误的计数，而 100% 并没有抓住它。自评的关卡告诉你的是作者相信什么；只有对照规格去读，才能告诉你什么是真的。过渡：然后是 014 从未得到的那个文件。 -->

---

## 证明：`tasks.md`——第 2 阶段，以及缺口

- 014 **没有** `tasks.md`
- 它的计划仍列着 "Phase 2: Run `/speckit.tasks`"
- `[P]` 表示并行，`[US#]` 表示故事，路径精确到文件

```markdown
- [ ] T017 [P] [US1] Implement create_wizard_state method
  in api/services/onboarding_service.py
- [ ] T002 [P] Create onboarding directory structure
  (api/services/, frontend/js/, tests/)
```

`specs/000-user-onboarding/tasks.md`, `.specify/templates/tasks-template.md`

<!-- NOTES: 这是范例中诚实的缺口：014 的规格细到四千行契约，却从未生成任务分解——它的计划中的 Next Steps 仍然列着第 2 阶段。所以我们到别处去读真实的格式。模板中：勾选框 `[ID] [P?] [US#]`，`[P]` 标记可并行的工作，`[US#]` 把每个任务绑定到一个故事，还有指令 "Include exact file paths in descriptions." 然后是 `specs/000-user-onboarding/tasks.md`，467 行，第 66 行原文："T017 [P] [US1] Implement create_wizard_state method in api/services/onboarding_service.py." 每个任务都写明了一个文件。过渡：M4.1 到此结束——那么，什么样的规格才算好？ -->

---

## M4.2 — 陌生人测试

```figure
kind: flow
alt: Ralph 循环——一个只被告知 implement spec 的智能体，挑选优先级最高的未完成规格，满足每一条验收标准并输出完成承诺，没有历史，也不提问。
step: "implement spec" (seam) — 没有聊天记录，没有追问 @ 由一个 shell 脚本启动
step: 挑选优先级最高的未完成规格 @ 由一个 shell 脚本启动
step: 完成每一条验收标准 @ 由一个 shell 脚本启动
step: 输出完成承诺 @ 由一个 shell 脚本启动
```

- 所以：删掉对话——陌生人还能实现吗？
- 下面的每条规则都因此而存在

`.specify/memory/constitution.md`, Context A

<!-- NOTES: 项目宪章的 Context A 定义了 Ralph 循环：由 `ralph-loop.sh` 或一个提到 "implement spec" 的提示词启动，智能体必须 "Pick highest priority incomplete spec (from `specs/`)"、"Complete ALL acceptance criteria"，并在 100% 完成时输出 `<promise>DONE</promise>`。这个智能体没有聊天记录。在 Ralph 模式下，它无意提问。所以每个产物的质量测试是：删掉对话——陌生人还能实现吗？这一分段的一切都由这一句话而来。过渡：第一个推论，做什么与怎么做的分离。 -->

---

## 做什么与怎么做（WHAT vs HOW）

- `spec.md`：用户可见的行为，与技术无关
- `plan.md`：语言、版本、存储、性能目标
- 关卡规则："No implementation details (languages, frameworks, APIs)"
- 模式 SQL 属于数据模型、契约和迁移
- 规格中的 "Key Entities" 描述字段，**不涉及实现**

`.specify/templates/spec-template.md`, `checklists/requirements.md`

<!-- NOTES: 在这里破除一个常见误解：好的规格不包含数据库模式。实体的描述不涉及实现；SQL 放在数据模型和迁移中。而且这种分离能带来实实在在的好处。014 的规格把 Open Decision 1 记为使用内存缓存并以数据库作备份——日期为 TBD——然后研究的决策 1 选择 Redis 作为存储，并直接否决了内存方案。需求从未改变；这次反转被记录在案。如果怎么做泄漏进了规格，这次反转就会变成一次规格修改。过渡：推论二，把故事当作 MVP 切片。 -->

---

## 每个故事都是一个 MVP 切片

- 模板：每个故事都 "INDEPENDENTLY TESTABLE"
- 只实现一个故事，你仍然交付了价值
- 014 的每个故事都有自己的 "Independent Test" 行
- US1：模拟登录失败，验证锁定，验证提示信息
- 任务按故事分组，正是出于这个原因

`.specify/templates/spec-template.md`, `specs/014-security-hardening/spec.md`

<!-- NOTES: 规格模板明确要求："Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them, you should still have a viable MVP." 独立开发、测试、部署、演示。014 的每个故事都有一行 Independent Test；US1 的是模拟登录失败，并同时验证锁定和显示的提示信息。由此得出三个推论：部分实现仍然可以交付，一个 PR 可以只承载一个故事，任务文件按故事组织工作，每个故事之后有一个检查点。过渡：而故事内部的场景有它们自己的标准。 -->

---

## 可以直接变成测试的场景

- 「5 分钟内失败 5 次 → 锁定 15 分钟」
- 这些数字以 FR、契约行、测试断言的形式再次出现
- 标准：写测试的人无需做任何决定
- 「Then 系统是安全的」通不过关卡
- 「得到恰当处理」也一样——对照什么写代码？

`specs/014-security-hardening/spec.md` US1

<!-- NOTES: 回想 US1 的第一个场景。数字 5、5 和 15 像副歌一样在下游反复出现：它们变成 FR-001、限流契约配置表的第一行，以及测试草图中的一个断言。当写测试的人不需要再做任何决定时，一个场景才算完成。对比反面例子：「Then 系统是安全的」无法对照着写代码；「Then 认证失败会得到恰当处理」没有指出任何可观察的结果。两者都违反了关卡的规则：需求必须可测试且无歧义。写出明天就能被测试断言的 Then 子句。过渡：那你确实还不知道的东西怎么办？ -->

---

## 有边界的澄清

- 草稿可以标记 `[NEEDS CLARIFICATION: …]`
- 关卡要求在规划前一个都不剩
- 早问，别常问——014 写的是 "max 3 questions"
- 或者在 Assumptions 中记录一个默认值
- 014 把 1 小时令牌和 ±30 秒 TOTP 写成了需求

`.specify/templates/spec-template.md`, `specs/014-security-hardening/spec.md`

<!-- NOTES: 模板展示了这个标记的用法：FR-006 通过 `[NEEDS CLARIFICATION: auth method not specified]` 认证用户。但检查清单的 Requirement Completeness 组要求在规划之前不能留下任何标记。两条解决途径。`/speckit.clarify` 在 `/speckit.plan` 之前运行，预算被刻意压得很小——014 自己的 Next Steps 写着 "Run `/speckit.clarify` if clarifications needed (max 3 questions)"。或者你明确记录一个默认值。014 把 1 小时的令牌有效期和 ±30 秒的 TOTP 容差写成了功能需求，而它生成的检查清单备注却声称它们放在 Assumptions 中——请对照规格核对这条备注。诚实的脚注：clarify 的命令定义目前写的是最多 5 个问题——这是一处我们会回头讨论的漂移。过渡：下面是关卡真正的通过规则。 -->

---

## 关卡的通过规则

| 组 | 示例规则 |
|---|---|
| Content Quality | 没有实现细节 |
| Requirement Completeness | 没有遗留的 NEEDS CLARIFICATION |
| Feature Readiness | 场景覆盖主要流程 |

全部是通过/不通过。这是拦下一份坏规格代价最低的地方。

<!-- NOTES: 三组，每一项都是二元的。Content Quality：没有实现细节，聚焦用户价值，非技术干系人可读。Requirement Completeness：没有未解决的标记，可测试且无歧义，成功标准可衡量且与技术无关，场景和边界情况已定义，范围有界，依赖和假设已识别。Feature Readiness：每条 FR 都有验收标准，场景覆盖主要流程，没有实现泄漏。「检查清单是官僚主义」恰恰说反了：这是你在一份有漏洞的规格上花掉一整个自主实现循环之前，最后一个代价低廉的时刻。过渡：任务，以及为什么路径如此重要。 -->

---

## 任务要引用精确的文件路径

- 模板："Include exact file paths in descriptions"
- 全新的会话不知道你的项目布局
- `AGENTS.md`："Do not invent file paths… Grep the repo"
- 「更新后端」只会逼出猜测或浪费
- 有了路径，第一步就是一次**确认**性的 grep

`.specify/templates/tasks-template.md`, `AGENTS.md`

<!-- NOTES: 为什么路径是必需的？因为全新的智能体会话完全不知道你的项目是怎么组织的，而仓库自己的防幻觉规则禁止编造结构："Do not invent file paths, function names, route paths, commands, URLs, or identifiers. Grep the repo before referencing." 像「更新后端」这样的任务，要么逼智能体去猜——幻觉端点就是这么来的——要么让它耗费预算重新摸索布局。写明文件的任务，会让它的第一个动作变成一次确认而非编造的 grep。「任务可以写『更新后端』」就是今天要摒弃的误解。过渡：契约，它存在的理由与此相同。 -->

---

## 契约是会话之间的接缝

```figure
kind: system
alt: spec-kit 的会话之间不共享记忆，只共享文件——设计会话写下 spec、plan、contracts 和 tasks，一个全新的实现会话读取它们（由契约钉住接缝），然后才写代码和测试。
source: SignUpFlow/specs/014-security-hardening/contracts/rate-limiting.md
layer: 设计会话 @ 契约是设计这个功能的会话
  node design: specify · plan · tasks — 一个带着对话的会话
layer: 磁盘上的文件 — 唯一的共享状态 (hl) @ 这两个会话之间
  node spec: spec.md — 做什么
  node plan: plan.md — 怎么做
  node contracts: contracts/ (seam) — 形态 · 错误键 · 键模式 · 测试草图
  node tasks: tasks.md
layer: 实现会话 — 没有聊天记录 @ 契约是设计这个功能的会话
  node impl: implement — 一个全新的智能体会话
  node code: 代码 + 测试
edge: design -> spec
edge: design -> plan
edge: design -> contracts — 写下来
edge: design -> tasks
edge: spec -> impl
edge: contracts -> impl — 钉住接缝 (hl) @ 这两个会话之间
edge: tasks -> impl
edge: impl -> code
```
- 限流配置行重复了 US1 的 5/5/15

`specs/014-security-hardening/contracts/rate-limiting.md`

<!-- NOTES: 契约是设计这个功能的会话与实现它的另一个会话之间的接口。这两者之间除了磁盘上的文件什么也不共享，所以接缝必须写下来：请求和响应的形态、错误键、Redis 键模式，以及一个测试草图。在 `contracts/rate-limiting.md` 中，配置表是规格的做什么与计划的怎么做第一次交汇的地方——同样的 5/5/15，现在附上了按 IP 的范围和键格式。漏掉契约，实现它的智能体就会自己编造错误键，你的前端就永远对不上。过渡：让计划保持诚实的那道关卡。 -->

---

## 宪章检查——以及 Ralph 循环

- "Must pass before Phase 0 research. Re-check after Phase 1"
- 迫使计划逐条走过每一条原则
- 违规必须在 Complexity Tracking 中论证
- 014：七条原则，零违规，空表
- 一个要完成全部（ALL）标准的智能体承受不起歧义

`.specify/templates/plan-template.md`, `.specify/memory/constitution.md`

<!-- NOTES: 一个写计划的智能体会兴高采烈地违反你的原则——跳过 E2E、添加没人要的基础设施——因为它并没有内化这些原则。这项检查迫使计划逐条走过每一条原则，给出结论和证据，任何违规都必须在 Complexity Tracking 表中论证，而模板说这张表「只有」存在违规时才填写。014：七条原则，七个结论，零违规，空表。用 Context A 让循环闭合：一个必须完成「全部」验收标准、又不能提问的智能体，它的安全程度恰好等于你的产物的完整程度。这条流水线是自主性的前提条件，而不是围绕它的仪式。过渡：现在讲诚实的变更记录。 -->

---

## M4.3 — 一个故事一个 PR

```figure
kind: flow
alt: 按故事分组、测试先行的任务，每个故事之后有一个用来单独验证它的检查点，每个故事一个拉取请求——可评审、可演示、可回滚。
source: SignUpFlow/.specify/templates/tasks-template.md
step: 按故事分组的任务 — 先写测试，并且测试先失败 @ 任务按故事分组
step: 检查点 (seam) — 单独验证这个故事 @ 任务按故事分组
step: 一个故事一个 PR (hl) — 一次看完即可评审 · 可演示 · 可回滚 @ 只承载一个故事的拉取请求
```

- 测试先行的阶段让 PR 自带证据

`.specify/templates/tasks-template.md`

<!-- NOTES: 任务文件是为一个故事一个 PR 而设计的：任务按故事分组，测试先写并且先失败，每组之后有一个检查点——模板的原话是 "Stop at any checkpoint to validate story independently." 只承载一个故事的 PR，一次就能评审完，可以演示给干系人，也可以回滚而不会把无关的改动一并拖出来。这不是为了流程而流程；正是它让 Validation 部分足够短，短到能保持诚实。过渡：而这个部分有固定的形态。 -->

---

## PR 正文格式

```text
Summary:
- one-line per change
Changed files:
- path: reason
Validation:
- what you ran (commands and result)
Follow-ups:
- known gaps, deferred work, or open questions
```

`SignUpFlow/AGENTS.md:138-149`（"PR and commit format"）

<!-- NOTES: 四个部分，固定不变。Summary 说明改动；Changed files 给出路径和原因；Validation 记录你运行的命令及其结果；Follow-ups 记录已知缺口、推迟的工作和未决问题。背后的规则：每个 PR 都运行 `make test-all`，没有 CI——所有验证都在本地运行，所以要记录命令、结果、局限和已推送的 head SHA。只有在本地验证和评审都已记录、并且 GitHub 报告可合并之后才能合并。并且永远不要 "fabricate status checks, bypass protections, or treat missing evidence as success." 一个记录了失败的 Validation 部分仍然是证据；没有命令的「测试通过」不是。 -->

---

## 本地代码评审

- `docs/ai-pr-review.md` 取代了已退役的评审关卡
- 记录 head 与 base SHA；检查完整的 diff
- 正确性、安全、组织隔离、迁移、负路径
- 发现必须带**严重级别**和**文件/行号**
- "Missing review is not approval"（`AGENTS.md`，规则 4）

`docs/ai-pr-review.md`

<!-- NOTES: 仓库的评审策略本身就是一个文件，它明确声明 Ollama 不是代码评审提供方——之前托管的关卡已经退役，不要重建它。检查清单：记录 PR 的 head 和 base SHA；结合受影响的源码、测试和智能体指令检查完整的 diff；检查正确性、安全、组织隔离、授权、API 契约、迁移、用户工作流和负路径测试覆盖；报告带严重级别和文件/行号引用的发现；修复阻塞性问题，并重新评审最终的 diff。两条硬性底线："Do not claim independent review when the builder performed the review itself"，以及 AGENTS 规则 4："Missing review is not approval." 过渡：现在是让人意外的部分——生成的文件会说谎。 -->

---

## 漂移案例 1：过期的路径

- `specs/000-user-onboarding/tasks.md` 第 3 行：
- "Input: Design documents from `/specs/020-user-onboarding/`"
- 实际文件夹是 `specs/000-user-onboarding`
- 功能被重新编号了；生成器保留了旧路径
- 没有失败。没有警告。它就那样待在那里。

`specs/000-user-onboarding/tasks.md`

<!-- NOTES: 打开这个文件，读一读靠近顶部的 Input 那一行："Input: Design documents from `/specs/020-user-onboarding/`"。实际文件夹是 `specs/000-user-onboarding`。这个功能在某个时候被重新编号了，而生成的任务文件保留了过期的路径。没有任何东西失败，没有测试抓住它，也没有触发警告——它就那样待在一个生成的产物里，等着某个智能体顺着它走进死胡同。规格文件夹里的一切都是生成的输出：`/speckit.tasks` 写出了那个文件，`/speckit.checklist` 给另一个打了分。生成正是幻觉风险集中的地方，所以生成的产物理应受到与生成的代码同等的怀疑。过渡：还有两个，都在范例文件夹里。 -->

---

## 漂移案例 2–3：计数与目录

- 检查清单打印 "8 stories: 5xP1, 2xP2, 0xP3"
- 规格中有**六个** P1 故事——US1–4、US7、US8
- 同一份检查清单随后列出了六个 P1 功能
- 任务把迁移指派到 `migrations/versions/…`
- 不存在 `migrations/` 目录——迁移在 `alembic/versions/` 中

`specs/014-security-hardening/checklists/requirements.md`, `specs/000-user-onboarding/tasks.md`

<!-- NOTES: 案例二：`specs/014-security-hardening/checklists/requirements.md` 报告 "8 prioritized user stories: 5xP1, 2xP2, 0xP3"——但规格标出了六个 P1 故事：限流、审计日志、CSRF、会话失效、输入校验、密码重置。同一份检查清单的备注随后列出了这六个，却打印着 "5xP1"。100% 的质量分没有抓住它；只有对照规格去读检查清单才抓住了。案例三：onboarding 的任务文件把迁移指派到 `migrations/versions/add_onboarding_tables.py`，而根本不存在 `migrations/` 目录——迁移放在 `alembic/versions/` 中。两个文件都是生成的，也都错了。过渡：仓库里已经有对策。 -->

---

## 对策：grep、重数、打开

- `AGENTS.md` 第 6 步：搜索过期的命令和计数
- 防幻觉规则：引用之前先 grep 仓库
- 每一个计数都对照来源重数一遍
- 永远不要让自报的分数代替打开文件
- 把规格文件夹当作生成的输出，而不是金科玉律

`AGENTS.md` (operating loop step 6; anti-hallucination rule)

<!-- NOTES: 仓库里已经有针对这一点的规则。操作循环第 6 步："Search for stale commands, counts, check names, and feature-state claims before declaring done." 还有防幻觉规则："Grep the repo before referencing." 所以对策是机械化的。grep 生成文件引用的每一条路径并确认它存在——这能抓住案例三。对照来源重数每一个计数——这能抓住案例二。永远不要把自报的分数当作打开文件的替代品，正是这个习惯能抓住案例一。在实验 M4 中，你要在自己的检查清单上运行这些检查。过渡：轮到你了。 -->

---

## 实验 M4 — 为一个真实功能写规格

**目标：** 为一个真实功能产出完整的规格文件夹。
**通过关卡：** 一个陌生人零提问地实现故事 1。
**产物：** spec · research · data-model · plan · contract · checklist · tasks。
**漂移检查：** grep 每一条路径，重数每一个计数。

`lab.md` · 建议的功能：可用时间窗口或邀请链接

<!-- NOTES: 实验时长 90 到 120 分钟，是把整个模块压缩成一件交付物。你将在自己项目中的 `specs/001-your-feature/` 里工作；如果你没有自己的 SaaS，就扩展 SignUpFlow——讲师指南的默认选项是一个换班请求功能。七个产物，正是我们走读过的那一套。有两项评分格外严格：每个任务都必须写明一个在你的仓库中确实存在的精确文件路径，而且你的检查清单必须经得住你自己的漂移检查——grep 每一条引用的路径，重数每一个计数。然后由一位同伴或一个全新的智能体会话，在没有任何上下文的情况下尝试实现故事 1。记录下他们问了什么。过渡：接下来是测验。 -->

---

## 测验 M4

- 8 道题 · 6 道选择题，2 道简答题
- 产物职责 · 关卡规则
- 任务格式 · 研究决策格式
- 其中一题是漂移检查题

`quiz.md`

<!-- NOTES: 八道题，对应三个分段。干扰项编码了我们一直在纠正的误解：规格可以包含代码，「安全」是一个可测试的 Then 子句，任务可以不写文件。第 8 题要求你说出 `AGENTS.md` 中的两个对策习惯，并说明每个习惯会抓住哪个漂移案例——grep 抓住不存在的 migrations 目录，重数抓住 "5xP1" 与六个 P1 故事的矛盾。带目标出处的答案在文件末尾。过渡：回顾。 -->

---

## 回顾

- 一条命令链：每一步消费上一步的产出
- 014：8 个故事、44 条 FR、12 条标准、7 个边界情况
- 8 个研究决策、6 份契约、4,661 行、没有 tasks.md
- 一个质量测试：陌生人测试
- 诚实的记录：一个故事一个 PR；严重级别 + 文件/行号
- 生成的产物会漂移——grep 路径，重数计数

`lesson.md` · `specs/014-security-hardening/`

<!-- NOTES: 带走六行要点。流水线是一条链，每条命令消费前一个文件。范例在真实规模上展示了这一整套：八个故事、44 条 FR、七个边界情况、十二条成功标准、八个研究决策、六份契约合计 4,661 行——以及一处诚实的缺口：没有任务文件。质量只有一个测试，就是陌生人测试，而关卡强制执行它的各项推论。变更记录是一种格式，而不是一种感觉。生成的产物会漂移，所以在引用任何东西之前，先 grep 路径、重数计数。过渡：讨论题。 -->

---

## 讨论题

> 我会最先写规格的功能：[一句话]
> 我最想跳过的产物：[产物] → [什么会坏掉]
> 最难做到经得起陌生人测试的：[一行]
> 我现在会做的一项漂移检查：[grep 或重数]

然后评论一位同学最犀利的场景。

`lesson.md`，“讨论题”

<!-- NOTES: 用这个模板在社区发帖。第三行最重要——写出你不得不打磨的那个具体场景、需求或任务，并说明它之前哪里含糊。然后读两位同学的帖子，并在其中一篇下用一个问题评论：他们最犀利的验收场景，能让你不提任何问题就实现吗？这就是互相施加的陌生人测试。如果你是自定进度的学员，这种同伴交流也是你满足实验 M4 通过关卡的方式。 -->

