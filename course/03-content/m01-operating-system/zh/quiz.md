# 测验 M1 — AI 产品操作系统

> 8 道题 · 6 道选择题 + 2 道简答题 · 答案附在最后，并标明对应目标。

## 题目

### Q1 (M1.1)

以下哪条规则是按 SignUpFlow 给智能体指令定下的写作风格写的？

- a) 「多租户要小心。」
- b) 「每条查询都按 org_id 过滤。」
- c) 「多租户很重要，要记在心上。」
- d) 「开发者应当重视租户隔离。」

### Q2 (M1.1)

一个智能体遇到了冲突：一边是 `docs/ai-agent-coding-strategy.md` 中的一条通用规则（第 4 级），另一边是 `.github/instructions/` 下一条更具体、更安全的按路径限定的规则（第 3 级）。按照 SignUpFlow 的指令优先级，它必须：

- a) 无论如何都遵循 `AGENTS.md`，因为它是通用基线
- b) 遵循更具体、更安全的那一条——按路径限定的规则
- c) 遵循最近更新的那个文件
- d) 停下来询问用户，因为任何冲突都会阻塞工作

### Q3 (M1.1)

在输出中引用一个文件路径、函数名或 schema 字段之前，在 SignUpFlow 中工作的智能体必须：

- a) 凭记忆回想，并在注释中标注不确定
- b) 相信它的训练数据，因为这个仓库是公开的
- c) 给出 2-3 个候选路径，让用户挑一个
- d) grep 仓库 / 读取权威来源，不凭记忆回想

### Q4 (M1.2)

以下哪一组 spec-kit 产物与职责的对应是正确的？

- a) spec.md = 带库选型的「怎么做」；research.md = 用户需要的「做什么」
- b) tasks.md = 给智能体的散文式指导；contracts/ = 部署指南
- c) spec.md = 与技术无关的「做什么」；research.md = 带编号的决策，附被否决的备选方案；tasks.md = 引用精确文件路径的勾选任务
- d) quickstart.md = 规划之前的质量关卡；checklists/requirements.md = 限时的部署指南

### Q5 (M1.3)

一位队友说：「AI 助手显然让我变快了——我能感觉到。」METR 2025 年的随机对照研究（证据数据集第 1 行）让你可以怎样回应？

- a) 「在那项研究中，有经验的维护者在自己的仓库上被测得慢了 19%，而他们自认为快了 20%——所以感觉上的提速不是证据。它并不说明 AI 让所有人都变慢：它只是一项针对 16 个人的任务层级研究，而且 2026 年后续研究的置信区间跨过了零」
- b) 「你说得对：这项研究测得有经验的开发者用 AI 快了 19%」
- c) 「这项研究证明 AI 助手削减了工程预算，所以从金额上看这种感觉是对的」
- d) 「这项研究证明 AI 让每个开发者都变慢，所以别再用了」

### Q6 (M1.3)

以下哪一行属于一份诚实的验证记录？为什么？

- a) 「全绿——发布吧。」
- b) 「`make test-all` 全绿；为了让记录干净，21 个被跳过的测试没有写进记录。」
- c) 「Full API mypy：40 个文件中有 835 个错误；not a pass。」——因为记录要包含已知的技术债和失败
- d) 「不需要本地记录——加更多 CI 总是更好。」

### Q7 (M1.2 — short answer)

针对用户故事「作为志愿者，我可以屏蔽某些日期，让求解器跳过我」，写一个 Given/When/Then 验收场景，以及一条采用 tasks.md 格式、引用精确文件路径的任务行。

### Q8 (M1.3 — short answer)

你的测试运行结果：12 个通过，然后有 1 个因时序不稳定而失败；修复之后，13 个通过。按规定格式写出证据条目——命令、计数、日期、环境、局限、head SHA——不要隐藏这次失败。

## Answer key

### Q1 — b — 「每条查询都按 org_id 过滤」是祈使的、可检查的；「要小心」只是一种感觉（`SignUpFlow/AGENTS.md`，"House style"）。（目标：M1.1 — 写出可验证的规则）

### Q2 — b — 优先级唯一的决胜规则是「遵循更具体、更安全的那一条」；AGENTS.md 是基线，不会覆盖更具体的规则（`SignUpFlow/AGENTS.md`）。（目标：M1.1 — 应用优先级）

### Q3 — d — AGENTS.md 禁止虚构标识符——要 grep 仓库，并从权威来源读取事实；「2-3 个选项」规则针对的是有歧义的请求，而不是回想事实（`SignUpFlow/AGENTS.md`，"Anti-hallucination"）。（目标：M1.1 — 应用防幻觉规则）

### Q4 — c — spec.md 是与技术无关的「做什么」，research.md 保存带编号、附被否决备选方案的决策，tasks.md 保存带精确路径的勾选任务；其他选项都把职责调换了（`SignUpFlow/docs/SPEC_KIT_SETUP.md`）。（目标：M1.2 — 说出每个产物的职责）

### Q5 — a — 第 1 行是来自一项独立随机对照试验的任务层级证据：测得慢了 19%（CI +2% 到 +39%），而自认为快了 20%，所以这种感觉恰恰是记录绝不能用来替代的东西。第 2 行说明了（d）为什么言过其实：2026 年后续研究的点估计是 −18% 和 −4%，两个区间都跨过零，这是无定论，而不是「更慢」。（c）跳了层级：任务层级的结果对释放的产能或预算什么也说明不了，这正是 M6 点名的那种混淆错误。（b）把正负号读反了。感受到的速度和测得的速度之间的这道鸿沟，正是 M1 存在的理由：写下来的规则、陌生人能执行的规格，以及用证据记录代替印象（`course/03-content/m06-expertise-product/evidence-dataset.md`，第 1–2 行）。（目标：M1.3 — 为什么证据要取代感觉）

### Q6 — c — 记录要包含已知的技术债和失败，并且永远不伪造；（b）隐藏了真实记录会计入的跳过数（"1,464 passed, 21 skipped"）；「加更多 CI 总是更好」正是无 CI 策略所反驳的误解——托管检查并不记录你验证了什么（`SignUpFlow/docs/playbooks/validation.md`）。（目标：M1.3 — 记录诚实的证据）

### Q7 — Model answer — 场景：「假设（Given）Sarah 有一段覆盖 2026-04-23 的屏蔽期，当（When）管理员为那一周运行求解器时，那么（Then）Sarah 不会被分配，并且解报告零个硬约束违规。」任务："- [ ] T031 [P] [US1] Implement POST /api/v1/availability/time-off in api/routers/availability.py: write the failing test in tests/api/test_availability.py first."（目标：M1.2 — 把一个用户故事转化为可检查的场景和可执行的任务）

### Q8 — Model answer — "## Evidence — todo — 2026-09-14 / Commands: `python3 -m pytest tests/ -q` → 12 passed, 1 failed (timing flake); after fix → 13 passed / Environment: macOS 15, Python 3.11.9 / Revision: <head SHA> / Limitations: flake not root-caused; CLI tested by hand only." 失败留在记录里——「这次最初的失败没有从证据中省略」（`SignUpFlow/docs/playbooks/validation.md`）。（目标：M1.3 — 写一份包含失败的证据记录）
