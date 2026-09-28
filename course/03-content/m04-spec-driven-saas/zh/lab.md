# 实验 M4 — 为一个真实功能写规格，经得起陌生人测试

> **目标：** 为*你自己*产品的一个真实功能产出一个完整的 spec-kit 文件夹，让它通过 SignUpFlow 运行的同一道关卡，并证明一个陌生人仅凭 `tasks.md` 就能实现故事 1。
> **前置条件：** 课程 M4；一个为你的 SaaS 准备的功能想法（对 SignUpFlow 这类应用的建议：**志愿者请假 / 可用时间窗口**或**邀请链接**；如果你在做别的东西——就为你自己的功能写规格）。**时间：** 90–120 分钟。

你将在**你自己的项目**（如果还没有，就用一个草稿仓库）中新建的 `specs/001-your-feature/` 文件夹里工作。SignUpFlow 的真实文件夹就是你的模板——边做边打开它们，但不要盲目照抄。你在第 7 步运行的陌生人是脚本化的：提示词、报告格式和通过规则都在本文件旁边的 `stranger-prompt.md` 中——在第 1 步之前读它，因为知道陌生人会被问什么，正是让第 1 步写得清晰锐利的原因。

## 步骤

1. **选定功能，编写 `spec.md`（只写做什么）。** 遵循 SignUpFlow 仓库中的 `.specify/templates/spec-template.md`：≥3 个用户故事，每个都有一行 "Independent Test"（每个故事都是一个可行的 MVP 切片），以及 Then 子句可测试的 Given/When/Then 场景——要数字，不要感觉（「5 分钟内认证失败 5 次 → 锁定 15 分钟」，`specs/014-security-hardening/spec.md` US1，就是范本）。添加 ≥8 条功能需求，以及可衡量、与技术无关的成功标准。**零实现细节**——没有语言、框架或模式 SQL；实体的描述要 "without implementation"。
2. **在继续之前解决每一个未知项。** 不得遗留任何 `[NEEDS CLARIFICATION]` 标记（`specs/014-security-hardening/checklists/requirements.md` 中的关卡规则）。现在就提出一组有限的问题（最多 3 个，按 014 自己的做法），或者明确记录每个默认值，写成一条需求，或放进 Assumptions 部分——014 把 1 小时的令牌有效期写成了需求（FR-013、FR-036）。
3. **编写 `research.md`（第 0 阶段）。** ≥3 个编号决策，每个都带备选方案**以及否决的理由**——采用 `specs/014-security-hardening/research.md` 决策 1 的格式（选择 Redis，直接否决内存方案）。没有被否决方案的决策只是一种偏好，而不是决策。
4. **编写 `data-model.md`、`plan.md` 和一份 `contracts/<seam>.md`。** `plan.md` 负责怎么做（技术栈、版本、存储、性能目标），并且必须包含一个明确的**宪章检查（Constitution Check）**：你项目宪章的每一条原则对应一行结论（SignUpFlow 的是 `.specify/memory/constitution.md`；在你自己的仓库中使用实验 M1 的项目宪章）。任何违规都放进复杂度追踪（Complexity Tracking）表并附上论证——"Fill ONLY if Constitution Check has violations that must be justified"（`.specify/templates/plan-template.md`）。契约钉住一条真实的接缝：请求/响应形态、错误键和测试草图（范本：`specs/014-security-hardening/contracts/rate-limiting.md`）。
5. **编写 `tasks.md`（第 2 阶段）。** 采用模板格式的勾选任务——`[ID] [P?] [US#] description`——按 Setup → Foundational → 每个故事一个阶段（测试先写，并且先失败）→ Polish 组织，每个故事之后有一个检查点。**每个任务都写明一个在你的仓库中存在的精确文件路径**（"Include exact file paths in descriptions"，`.specify/templates/tasks-template.md`；"T017 [P] [US1] Implement create_wizard_state method in api/services/onboarding_service.py"，`specs/000-user-onboarding/tasks.md`，就是范本）。
6. **编写 `checklists/requirements.md`，诚实地给自己打分。** 三组，全部是通过/不通过：Content Quality、Requirement Completeness、Feature Readiness（结构与 014 的相同）。然后对你自己生成的文件运行 M4.3 中的**漂移检查**：grep 它引用的每一条路径并确认文件存在；对照 `spec.md` 重数每一个计数（故事、FR、优先级）；确认没有遗留 `[NEEDS CLARIFICATION]`。014 自评的 "Quality Score: 100%" 在六个 P1 功能旁边打印了 "5xP1"——自报的分数抓不住漂移；你的 grep 可以。
7. **陌生人测试（通过关卡）。** 提交这个文件夹，然后运行 `stranger-prompt.md` 中的**脚本化陌生人**：在一个干净的克隆上，把它的提示词粘贴进任意编码智能体的一个全新会话，除了仓库之外不提供任何上下文，让它在不问你任何问题的情况下实现故事 1。它会返回一份固定格式的报告——它构建了什么、它能检查哪些验收场景，以及它记录下的每一个问题（Q）和假设（A）。使用 `stranger-prompt.md` 中的表格，把每一行 Q/A 标为 **spec-owed** 或 **environment-owed**。**通过 = 零行 spec-owed。** 只要有一行 spec-owed，就说明规格有漏洞：打磨那个让陌生人缺少信息的产物，然后在一个新的全新会话中重新运行。**学习小组选项：** 按同样的规则和同样的报告格式，把文件夹交给一位同伴。

## 验收清单

- [ ] `spec.md`：≥3 个故事，每个都可独立测试并有一行 "Independent Test"；Given/When/Then 的 Then 子句带数字；≥8 条 FR；成功标准可衡量且与技术无关；没有实现细节
- [ ] 任何地方都没有 `[NEEDS CLARIFICATION]`；未知项通过提问或记录在 Assumptions 中得到解决
- [ ] `research.md`：≥3 个编号决策，每个都带一个被否决的方案和原因
- [ ] `plan.md`：宪章检查为每条原则给出结论；违规在复杂度追踪中论证
- [ ] ≥1 份契约，包含形态、错误键和测试草图
- [ ] `tasks.md`：勾选框格式，带 `[US#]` 关联，测试先行的阶段，每个故事一个检查点，每个任务都有精确的文件路径
- [ ] `checklists/requirements.md`：三组全部通过；漂移检查已运行（路径已 grep，计数已重数）
- [ ] 陌生人测试：一份针对故事 1 的 `=== STRANGER REPORT ===`（脚本化的智能体会话，或使用同样格式的同伴），**零行 spec-owed 的 Q/A**；此前每次运行的行都已标注，并展示被打磨产物修改前/后的样子

## 证据记录

在你的证据日志中记录：检查清单的三条通过行及今天的日期；你运行的漂移检查命令及其输出；以及每一份原样的陌生人报告，附上运行日期、每行 Q/A 的标注，以及两次运行之间被打磨的产物。格式遵循实验 M1 中的课程证据日志模板。

## 拓展目标

- 对*之前*某个项目的规格运行 `/speckit-checklist` 式的自评，找出一个漂移案例（过期路径或错误计数）——然后修复产物，而不是症状。
- 一次坐下来，从你自己的 tasks.md 实现故事 1，测试先行，并用 M4.3 中的四段式 PR 格式记录诚实的 Validation 部分（包括失败）。
- 如果你用 spec-kit 1.0 实现，在 `/speckit-implement` 之后运行 `/speckit-converge` 并记录其结果——"Converged"，或它追加的 `## Phase N: Convergence` 任务。然后无论如何都要运行你自己的漂移检查：converge 读取你的产物，但不审计它们。

## 讨论题

贴出你的陌生人报告中的 `Counts` 块，以及一次未通过的运行中的一行 spec-owed：说出让陌生人缺少信息的产物，并展示被打磨的那一行修改前/后的样子。如果你的第一次运行就通过了，就贴出 environment-owed 的行，并说明为什么每一行都不是规格该负责的。
