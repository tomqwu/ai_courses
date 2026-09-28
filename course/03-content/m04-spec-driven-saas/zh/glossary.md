# 术语表 M4 — 规格驱动的 SaaS

> 每个「出处」指针都在工作区根目录下解析，`course/`、`SignUpFlow/`、`ListenToMe/` 和 `ai_qe/` 在那里是同级目录。SignUpFlow 的路径相对于 `SignUpFlow/`。

- **验收场景（Acceptance scenario）** — 用户故事中的一条 Given/When/Then 陈述，其 Then 子句是一个可观察、可量化的结果。— `SignUpFlow/specs/014-security-hardening/spec.md`（US1）。
- **复杂度追踪（Complexity Tracking）** — 计划中的一张表，*只有*在宪章检查记录了需要论证的违规时才必须填写。— `SignUpFlow/.specify/templates/plan-template.md`。
- **宪章检查（Constitution Check）** — 计划逐条对照原则的合规检查；这道关卡必须在第 0 阶段研究之前通过，并在第 1 阶段设计之后重新检查。— `SignUpFlow/.specify/templates/plan-template.md`。
- **契约（Contract）** — 设计功能的会话与实现它的会话之间的书面接口：请求/响应形态、错误键、键模式、测试草图。— `SignUpFlow/specs/014-security-hardening/contracts/rate-limiting.md`。
- **数据模型文件（`data-model.md`）** — 列出实体及其关键字段、不含实现；功能有传统实体时存在，当基础设施横跨许多实体时缺席（如 014）。— `SignUpFlow/specs/000-user-onboarding/data-model.md`。
- **漂移（Drift）** — 生成的产物与生成它的来源不一致；SignUpFlow 中有三个已验证的案例。— `SignUpFlow/specs/000-user-onboarding/tasks.md`（第 3 行）。
- **功能需求（Functional requirement (FR)）** — 一条带编号、与技术无关的 "System MUST…" 陈述；014 有 44 条。— `SignUpFlow/specs/014-security-hardening/spec.md`。
- **独立测试（Independent Test）** — 每个故事都有的一行，证明这个故事本身就是一个可行的 MVP 切片。— `SignUpFlow/.specify/templates/spec-template.md`。
- **[待澄清] 标记（`[NEEDS CLARIFICATION]`）** — 模板中表示未决决策的标记；关卡要求在规划之前一个都不剩。— `SignUpFlow/.specify/templates/spec-template.md`。
- **第 0 / 第 1 阶段（Phase 0 / Phase 1）** — 一个功能的研究阶段（有据可查的决策）和设计阶段（数据模型、契约、快速上手文档）。— `SignUpFlow/specs/014-security-hardening/plan.md`。
- **计划文件（`plan.md`）** — 负责怎么做：语言、版本、存储、性能目标，以及带 `[NEW]`/`[MODIFY]` 标注的项目结构。— `SignUpFlow/specs/014-security-hardening/plan.md`。
- **Ralph 循环（Ralph loop）** — 项目宪章的 Context A：一个智能体挑选优先级最高的未完成规格，完成*全部*验收标准，并报告 `<promise>DONE</promise>`。— `SignUpFlow/.specify/memory/constitution.md`。
- **研究文件（`research.md`）** — 第 0 阶段的决策：评估过的选项、理由，以及被否决的方案。— `SignUpFlow/specs/014-security-hardening/research.md`。
- **规格文件夹（Spec folder）** — 一个功能自成一体的指令集（`spec.md`、`research.md`、`plan.md`、`contracts/`、`tasks.md`……）；SignUpFlow 在 `specs/` 下有 17 个。— `SignUpFlow/specs/`。
- **规格驱动工具包（Spec-kit）** — GitHub 的规格驱动工具包。1.0 版（2026-08-21）先运行一次 `/speckit-constitution`，然后是 `/speckit-specify` → `/speckit-plan` → `/speckit-tasks` → `/speckit-implement` ⇄ `/speckit-converge`，其中 converge 把未完成的工作追加到 `tasks.md`，直到报告 "Converged"；clarify、checklist 和 analyze 是可选的。SignUpFlow 1.0 之前的配置把它们拼写为 `/speckit.*`，并且没有 converge。— `SignUpFlow/docs/SPEC_KIT_SETUP.md:9-18`；github.com/github/spec-kit（2026-09-26 阅读）。
- **陌生人测试（Stranger test）** — 唯一的质量测试：一个没有任何对话记忆的全新智能体会话，仅凭产物就能完成实现。— `course/03-content/m04-spec-driven-saas/lesson.md`（M4.2）。
- **成功标准（Success criteria (SC)）** — 可衡量、与技术无关的结果；014 有 12 条。— `SignUpFlow/specs/014-security-hardening/spec.md`。
- **任务文件（`tasks.md`）** — 第 2 阶段的产出：`[ID] [P?] [US#]` 格式的勾选任务，测试先行，精确的文件路径，每个故事一个检查点。— `SignUpFlow/specs/000-user-onboarding/tasks.md`。

## 容易弄错的术语

- **验收标准与成功标准（Acceptance criteria vs. success criteria）** — 验收标准描述一个场景的可观察结果（锁定 15 分钟）；成功标准是功能层面的可衡量目标（100% 的暴力破解尝试被拦截）。两者都放在 `spec.md` 中，把它们混在一起会让两者都无法评分。
- **做什么与怎么做（WHAT vs. HOW）** — 做什么是用户可见的行为，属于 `spec.md`；怎么做是技术栈、版本和存储，属于 `plan.md`。关卡的第一条规则会让提到某项技术的规格不通过。
- **已生成与已验证（Generated vs. verified）** — 已生成表示是某条 spec-kit 命令写出了它（`/speckit-tasks`、`/speckit-checklist`、`/speckit-converge`）；已验证表示你 grep 了它的路径、重数了它的计数。"Quality Score: 100%" 是生成的，不是验证过的。
- **[P] 与 [US#] 标记（`[P]` vs. `[US#]`）** — `[P]` 标记一个可以与相邻任务并行的任务（不同文件，没有依赖）；`[US#]` 把任务绑定到它所服务的用户故事。两者是正交的，不是同义词。
- **评审与批准（Review vs. approval）** — 一次记录在案、带严重级别和文件/行号发现的本地评审才是评审；批准需要这次评审，外加针对已推送的 head/base 的成功本地验证。"Missing review is not approval"（`SignUpFlow/AGENTS.md`，PR 规则 4）。

## 精选资源

- `SignUpFlow/specs/014-security-hardening/` — 范例产物集：8 个故事、44 条 FR、8 个决策、6 份契约，没有 `tasks.md`。
- `SignUpFlow/specs/014-security-hardening/checklists/requirements.md` — 关卡，以及 100% 的分数没能抓住的 "5xP1" 计数；把它和 `spec.md` 放在一起读。
- `SignUpFlow/specs/000-user-onboarding/tasks.md` — 真实的任务格式；以 T017 为范本行；第 3 行和迁移任务作为漂移示例。
- `SignUpFlow/.specify/templates/spec-template.md`、`plan-template.md`、`tasks-template.md` — 定义产物集合以及本模块引用的每条规则的三个模板。
- `SignUpFlow/.specify/memory/constitution.md` — Context A（Ralph 循环），以及宪章检查逐条走过的那些原则。
- `SignUpFlow/docs/ai-pr-review.md` — 本地评审检查清单、严重级别/文件行号规则，以及关于自我评审和批准的两条硬性底线。
- `course/03-content/m04-spec-driven-saas/lab.md` — 实验 M4 的七个步骤，以及你据以评分的验收清单。
