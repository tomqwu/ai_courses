# 测验 M4 — 规格驱动的 SaaS

> 8 道题 · 6 道选择题 + 2 道简答题 · 答案在文末，附目标出处。

## 题目

### Q1 (M4.1)

在 spec-kit 流水线中，`plan.md` 负责哪些 `spec.md` 绝不能包含的内容？

- a) 用户故事和验收场景
- b) 怎么做（HOW）：语言、版本、存储和性能目标
- c) 需求检查清单关卡
- d) 仓库的项目宪章

### Q2 (M4.2)

对一个规格文件夹来说，「陌生人测试」是什么？

- a) 由团队以外的人做一次安全评审
- b) 规格必须由没有构建过这个产品的人来写
- c) 一个没有任何对话记忆的全新智能体会话，仅凭产物就能完成实现
- d) 在开始规划之前，必须有一位同伴批准规格

### Q3 (M4.2)

哪个验收场景能通过关卡的「可测试且无歧义」规则？

- a) 「Then 系统能够安全地抵御滥用」
- b) 「Then 用户获得良好的体验」
- c) 「Then 认证失败会得到恰当处理」
- d) 「Then 5 分钟内失败 5 次后，账户被锁定 15 分钟」

### Q4 (M4.2)

在开始规划之前，需求检查清单关卡要求什么？

- a) 一份已签字确认的预算和一位项目经理
- b) 没有遗留任何 `[NEEDS CLARIFICATION]` 标记；每条 FR 都有验收标准；成功标准可衡量且与技术无关
- c) 所有任务都已实现，测试全部通过
- d) 宪章检查已提交在 PR 中

### Q5 (M4.2)

为什么 `tasks.md` 中的每个任务都要引用一个精确的文件路径？

- a) 让任务列表更长、更显眼
- b) 因为路径就是任务的负责人
- c) 这样任务跟踪器就能在那个文件变更时自动关闭任务
- d) 全新的智能体会话不知道项目布局，而编造路径正是幻觉端点产生的方式

### Q6 (M4.3)

哪个 PR 的 Validation 部分遵循了本课程的证据纪律？

- a) 「测试通过 ✅」
- b) 「一切正常，可以合并」
- c) 「`make test-all`：1,410 passed, 2 failed（见备注）；浏览器套件已跳过——没有显示服务器；head SHA abc123」
- d) 「已由构建系统验证」

### Q7 (M4.3, short answer)

一个 PR 正文的 Validation 部分写着：「我自己看过 diff 了——一切正常。还没有指派评审者，为了不耽误冲刺，先合并了。」改写它，使其同时满足本课程关于评审和批准的两条硬性底线，并说明原来的每一句分别违反了哪一条。

### Q8 (M4.3, short answer)

规格 014 自评的检查清单报告了 "5xP1"，而规格中有六个 P1 故事；它的计划还把迁移指派到一个并不存在的 `migrations/` 目录。说出你应该对每个生成的产物执行的两个对策习惯（来自 `AGENTS.md`），以及每个习惯在这里会抓住什么。

---

## Answer key

- **Q1 — b.** 做什么与怎么做的分离：`spec.md` 以与技术无关的方式负责用户可见的行为；`plan.md` 负责怎么做。关卡的第一条规则强制执行这一点（"No implementation details"，`specs/014-security-hardening/checklists/requirements.md`）。（M4.1）
- **Q2 — c.** SignUpFlow 以 Ralph 循环运行实现——一个没有聊天记录、不能提问的智能体。每条产物规则之所以存在，都是因为「陌生人无法追问」。（M4.2）
- **Q3 — d.** 这些数字会以一条 FR、一行契约配置和一个测试断言的形式再次出现。另外三项直接违反关卡规则。（M4.2）
- **Q4 — b.** Requirement Completeness 组：没有遗留的 NEEDS CLARIFICATION，可测试且无歧义，成功标准可衡量且与技术无关，场景和边界情况已定义。（M4.2）
- **Q5 — d.** 与防幻觉规则相关："Do not invent file paths… Grep the repo before referencing"（`AGENTS.md`）。写明路径，会让智能体的第一个动作变成一次确认的 grep，而不是一次猜测；（c）编造了仓库并没有的工具，（a）/（b）只是装饰。（M4.2）
- **Q6 — c.** 记录了命令和结果、跳过项和局限。「一个只写『测试通过』却没有命令的 Validation 部分不是证据；一个记录了失败的 Validation 部分仍然是证据。」（M4.3）
- **Q7 —** 第 1 句违反了 "Do not claim independent review when the builder performed the review itself"（`SignUpFlow/docs/ai-pr-review.md:20-21`）——把自我评审当作评审；第 2 句违反了 "Missing review is not approval"（`SignUpFlow/AGENTS.md:94`）——没有评审者不等于通过。改写示例：「Validation：`make test-all` → <计数>，head <SHA>。作者自评（非独立评审）：发现 F1–F2 已在 <提交> 中解决。已请求 <姓名> 进行独立的本地评审；在该评审记录于此之前**不合并**。」（M4.3）
- **Q8 —** 习惯：（1）引用任何路径之前先 grep——能抓住不存在的 `migrations/versions/add_onboarding_tables.py`（迁移放在 `alembic/versions/` 中）；（2）对照来源重数计数，永远不要让自报的分数代替打开文件——能抓住 "5xP1" 与六个 P1 的漂移。出处：`AGENTS.md` 操作循环第 6 步（"Search for stale commands, counts, check names…"）以及防幻觉规则。（M4.3）
