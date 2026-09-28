# 测验 M0 — 导览

> 8 道题 · 6 道选择题 + 2 道简答题 · 文末附答案，并标注对应目标。

## 题目

### Q1 (M0.1)

ListenToMe 是哪种产品原型的例子？

- a) 规格驱动的 AI SaaS
- b) 端侧原生 AI 应用
- c) 专业知识内容产品
- d) 云端 AI API 封装服务

### Q2 (M0.1)

按本模块的引用，SignUpFlow 的带日期证据类证明资产是什么？

- a) 每个拉取请求上的绿色 CI 徽章
- b) README 里一个教会的用户推荐语
- c) 记录在 `docs/playbooks/validation.md` 中的 "1,464 passed, 21 skipped"
- d) 它的 96% 核心覆盖率徽章

### Q3 (M0.1)

在本课程中，称一个案例研究为「生产级」，最接近的意思是：

- a) 仓库在 GitHub 上公开
- b) README 说产品已经完成
- c) 存在一件已交付的产物，并附有你能打开并验证的证明——一行带日期的证据、一个徽章或一个来源追溯文件
- d) 产品有付费客户

### Q4 (M0.2)

ListenToMe 的 14 行竞品对比表是从规格到交付的循环中哪个阶段的产物？

- a) 规格（Spec）
- b) 构建（Build）
- c) 研究（Study）
- d) 证明（Prove）

### Q5 (M0.2)

哪件产物属于循环的**证明（Prove）**阶段？

- a) 经过签名和公证的发布版 DMG
- b) 尽管覆盖率达到 97.24%，仍建议 "do not promote the existing 1.3.0 DMG" 的差距评审
- c) 带 Given/When/Then 验收场景的规格
- d) 95% 覆盖率底线脚本

### Q6 (M0.3)

关于课程环境，哪一项陈述是正确的？

- a) 每个实验都需要 Mac，因为案例研究都是 Swift 应用
- b) 核心实验在 macOS、Linux 和 Windows 上用 Python + Ollama 运行；Swift 拓展路线需要 Mac
- c) 本地 LLM 实验需要付费 API 密钥
- d) Ollama 只能在 macOS 上运行

### Q7 (M0.3 — short answer)

一位同学的首个成果帖全文是：「`make setup` 成功了。`Health score: 100.0/100`。」写出你会发布的回复：他们的证据必须显示运行过的两条命令（在 `make setup` 之后）、为了算作运行记录，他们必须在分数前后粘贴的求解器输出行，以及这个帖子按现状能否通过实验 M0。

### Q8 (M0.1 — short answer)

一位朋友想构建：一个付费 Web 应用，根据创始人自己的文章起草 LinkedIn 帖子，其中每个功能都写成由 AI 智能体实现的规格。它属于哪种产品原型？为了学习*方法*，他应该研究哪个案例研究仓库？用一句话说明原因。

## Answer key

### Q1 — b — ListenToMe 是一个原生 macOS 会议助手：端侧转录加实时 AI，私密，且模型可选（`ListenToMe/README.md`）。（目标：M0.1 — 描述三种产品原型）

### Q2 — c — 带日期的那一行 "1,464 passed, 21 skipped" 位于 `SignUpFlow/docs/playbooks/validation.md`；96% 徽章属于 ListenToMe。（目标：M0.1 — 说出每个仓库的证明资产）

### Q3 — c — 证明资产是一个你能打开并验证的文件（徽章、带日期的证据、来源追溯、公开的自我审计）；是否公开以及 README 里的主张都不是证据。（目标：M0.1 — 定义生产级）

### Q4 — c — 带有来源和日期主张的竞品表属于研究阶段的工作——把定位做成一件研究产物（`ListenToMe/docs/competition-analysis.md`）。（目标：M0.2 — 把产物对应到循环阶段）

### Q5 — b — 证明意味着对哪些已验证、哪些未验证的诚实记录，包括一份叫停发布的自我评审；DMG 属于发布，规格属于规格阶段，覆盖率脚本属于验证。（目标：M0.2 — 区分证明与发布/验证）

### Q6 — b — 核心实验是 Python 3.11+ 加免费的本地 Ollama 模型，适用于所有主流操作系统；只有 Swift 拓展路线需要 Mac（`ListenToMe/README.md`）。（目标：M0.3 — 了解你的环境）

### Q7 — Model answer — 两条命令是 `poetry run python -m api.cli.main init my-church` 和 `poetry run python -m api.cli.main solve my-church`。分数必须出现在 `solve` 打印的输出块里：上方是工作区头部（`Workspace:`、`People: 5`、`Events: 2`、`Mode:`），下方是 `Solution saved to my-church/output/solution.json`——分数那一行本身由 `SignUpFlow/api/cli/main.py:193` 输出，它的值取决于 SignUpFlow 的版本（在 2026-09-16 的 head 上，示例工作区打印 `0.0/100`，有两个硬约束违规），所以一个孤零零的 `100.0/100` 是警示信号，而不是证明。按现在的帖子，它不能通过：没有运行记录的分数属于实验 M0 的第 3 条自动不通过，而通过关卡的另一半——非空的 `ollama list`——也缺失了。（目标：M0.3 — 运行求解器并记录健康分）

### Q8 — Model answer — 产品原型 2（规格驱动的 AI SaaS）：一个多用户 Web 产品，其功能被写成规格供智能体实现——研究 SignUpFlow，它用 17 个规格文件夹和 7 个测试层级展示了同样的 spec-kit → 任务 → 经过测试的功能这一方法。（目标：M0.1 — 把产品归入产品原型）
