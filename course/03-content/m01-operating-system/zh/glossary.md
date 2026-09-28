# 术语表 M1 — AI 产品操作系统

按英文字母顺序排列。每个术语：先给定义，再给出处。

- **通用智能体规则文件（AGENTS.md）** — 跨智能体的基线规则文件，Codex CLI、Cursor、Aider、Jules、OpenHands、Sourcegraph Amp 和 Factory 等工具会原生读取它；一种由 Linux 基金会旗下的 Agentic AI Foundation 管理的开放格式。只保留一份，并让 `CLAUDE.md` 用 `@AGENTS.md` 导入它。在 SignUpFlow 中它有 188 行。（`SignUpFlow/AGENTS.md:3`）
- **防幻觉规则（Anti-hallucination rules）** — 让编造的事实可被检查的禁令：不要虚构路径、名称、命令或标识符；引用之前先 grep；从权威来源读取事实；请求有歧义时给出 2–3 个选项。（`SignUpFlow/AGENTS.md`，"Anti-hallucination"）
- **自主权配置（Autonomy configuration）** — 宪章中规定智能体可以独立做什么的部分。SignUpFlow 的配置是：`YOLO Mode: DISABLED`、`Git Autonomy: ENABLED (Commit changes when done)`。（`SignUpFlow/.specify/memory/constitution.md`，"Autonomy Configuration"）
- **项目宪章（Constitution）** — 最短、也最权威的治理文件：少数绝不能偏离的原则，外加当前的验证策略。SignUpFlow 的宪章有 85 行，位于所有智能体指令文件之上。（`SignUpFlow/.specify/memory/constitution.md`）
- **宪章检查关卡（Constitution Check gate）** — `plan.md` 中明确的通过/不通过检查点，必须在第 0 阶段研究之前通过，并在第 1 阶段设计之后重新检查。（`SignUpFlow/specs/014-security-hardening/plan.md`）
- **完成的定义（Definition of Done (DoD)）** — 衡量「已交付」而不是「已构建」的标准：在已安装的生产应用中验证受影响的行为，并把过时的文档视为失败，而不是后续事项。（`ListenToMe/AGENTS.md`、`ListenToMe/CLAUDE.md`）
- **证据记录（Evidence record）** — 一份带日期、固定到具体版本的验证记录：命令及其结果、环境、head SHA，以及一份明确列出哪些未经验证的清单。（`SignUpFlow/docs/playbooks/validation.md`；模板见 `03-content/m01-operating-system/lesson.md`，§M1.3）
- **钩子脚本（Hook）** — Claude Code 在某个生命周期事件时运行的脚本，在 `.claude/settings.json` 中配置；退出码 2 会阻止该动作，这让它成为强制执行层，而规则只是建议。实验 M1 的 `Stop` 钩子运行证据日志检查。（`03-content/m01-operating-system/lab.md`，第 8 步）
- **指令优先级（Instruction hierarchy）** — 规则重叠时的五级优先顺序，外加一条决胜规则：遵循更具体、更安全的那一条。（`SignUpFlow/AGENTS.md`，"Agent instruction hierarchy"）
- **无 CI 本地验证（No-CI local validation）** — SignUpFlow 的既定策略：所有评审、分析、迁移、测试和产物验证都在本地运行，并为已推送的版本记录证据，而不是要求托管检查。（`SignUpFlow/.specify/memory/constitution.md`，"Current Validation Policy (2026-09-13)"）
- **规则晋级（Rule graduation）** — 一条观察成为规则的流水线：记录在 `docs/research-log.md` 中，在一次真实的改动上试用，然后提升进 `AGENTS.md` 或某个智能体专属文件。（`SignUpFlow/docs/ai-agent-coding-strategy.md`）
- **自查对照（Self-review mapping）** — 实现计划末尾的一节，把每条规格要点对应到满足它的任务，这样就不会有任何东西被悄悄漏掉。（`ListenToMe/docs/superpowers/plans/2026-06-18-listentome-mvp.md`）
- **规格驱动工具包（Spec-kit）** — GitHub 的规格驱动工具包，在 `specs/` 下产出一个产物文件夹。1.0 版运行一次 constitution，然后在 Claude Code 中以 `/speckit-*` 技能的形式依次运行 specify → plan → tasks → implement → converge；SignUpFlow 1.0 之前的配置使用 `/speckit.*` 名称。（`SignUpFlow/docs/SPEC_KIT_SETUP.md:9-18`）
- **规格（做什么）（Spec (the WHAT)）** — 与技术无关、说明用户需要什么的陈述：按优先级排列、可独立测试的用户故事，配 Given/When/Then 验收场景和成功标准。（`SignUpFlow/specs/014-security-hardening/spec.md`）
- **任务行（Task line）** — `tasks.md` 中一条可执行的条目，采用 `[ID] [P?] [Story]` 格式，带精确的文件路径，并且先写测试。真实的例子："T027 [US1] Implement POST /api/sms/send endpoint per contracts/sms-api.md in api/routers/sms.py"。（`SignUpFlow/specs/019-sms-notifications/tasks.md`）
- **YAGNI 非目标（YAGNI non-goals）** — 一份明确列出产品不做什么的清单，写进设计规格，让范围无法悄悄扩大。ListenToMe 的是：没有云后端、账号、计费、多用户，也没有隐蔽模式。（`ListenToMe/docs/superpowers/specs/2026-06-18-listentome-design.md`，§2）

## 容易弄错的术语

- **规则与指南（Rule vs. guideline）** — 规则是可验证的（「每条查询都按 `org_id` 过滤」）；指南只是建议（「多租户要小心」），不属于指令文件。
- **`spec.md` 与 `plan.md`（`spec.md` vs. `plan.md`）** — 规格是「做什么」，不提任何技术；计划是「怎么做」，把技术决策放在一道关卡之后。
- **覆盖率与可信度（Coverage vs. confidence）** — 覆盖率说明哪些行运行过；它并不能证明可靠性，这就是为什么一个覆盖率 97.24% 的版本仍然被建议*不要*推广。
- **“测试通过”与证据（"Tests passed" vs. evidence）** — 没有命令、日期、环境和版本的计数只是一个说法；证据是可审计的。
- **基线与覆盖规则（Baseline vs. override）** — `AGENTS.md` 是通用基线，但一条更具体、更安全的按路径限定的规则会在冲突中胜出。

## 精选资源

1. `SignUpFlow/AGENTS.md` — 写作风格、五级优先级和防幻觉规则；把它当作你自己基线的范本来读。
2. `SignUpFlow/.specify/memory/constitution.md` — 85 行，展示一份宪章只需包含多少内容就足以具有权威。
3. `SignUpFlow/docs/ai-agent-coding-strategy.md` — 规则晋级流水线，以及只保留一个权威来源背后的理由。
4. `SignUpFlow/docs/SPEC_KIT_SETUP.md` — 这个仓库 1.0 之前的命令顺序；和 spec-kit 1.0 的 README（github.com/github/spec-kit）对照着读，看看变了什么。
5. `SignUpFlow/specs/019-sms-notifications/tasks.md` — 读一条真实的任务行，照搬它「路径 + 契约 + 顺序」的形态。
6. `SignUpFlow/docs/playbooks/validation.md` — 证据记录的范本：1,464 个通过的那一行、点击竞态、835 个 mypy 错误，以及局限那一段。
7. `ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md` — 那份尽管覆盖率很高、仍然说「不要推广」的诚实自评。
8. `ai_qe/docs/principles.md` — 四个主张层级；按谁能确认它来给每个数字贴标签的纪律。
