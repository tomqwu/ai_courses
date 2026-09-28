# 术语表 M0 — 导览

> 术语按英文字母顺序排列。「出处」是一个你能打开的文件；如果某个指针无法解析，请告诉讲师，
> 而不要凭记忆转述。

**产品原型（Archetype）** — 本课程构建的三种产品形态之一：端侧应用、规格驱动的 SaaS、
专业知识产品。它们的区别在于技术重心，而不在方法。 — `course/03-content/m00-orientation/lesson.md`

**案例研究（Case study）** — 整个课程中用作实例的三个公开仓库之一：
ListenToMe、SignUpFlow、AI × QE。 — `course/01-design/curriculum.md`

**`:cloud` 别名（`:cloud` alias）** — 以 `:cloud` 结尾的 Ollama 模型名，背后是托管服务，而不是你磁盘上的
权重。它的存在说明守护进程能访问云端模型；但它完全说明不了你的文本在哪里被处理。 — `course/03-content/m02-ondevice-app/tinycopilot/README.md`

**覆盖率底线（Coverage floor）** — 一个最低测试覆盖率百分比，未达到时运行失败。ListenToMe
用脚本强制执行 95%；TinyCopilot 通过 `--cov-fail-under` 强制执行 90%。 — `ListenToMe/README.md`；
`course/03-content/m02-ondevice-app/tinycopilot/Makefile`

**版次（Edition）** — 内容的一个带版本号、不可变的发布。AI × QE 维护彼此独立的版本字段，因此一次
幻灯片变更和一次站点变更是两个不同的发布事件。 — `ai_qe/_data/release.yml`

**证据日志（Evidence log）** — 学员整门课都维护的、带日期、只追加的命令与输出记录；
它会成为结业项目的证据记录。 — `course/03-content/m00-orientation/lab.md`

**失败即关闭（Fail closed）** — 缺少必需的证明时拒绝操作的安全默认。在
M3 中，没有经过验证的本地元数据的模型会被拒绝，而不是被信任。 — `course/03-content/m03-privacy-ship/lesson.md`

**健康分（Health score）** — 求解器为生成的排班表打出的 0–100 质量指标，由
`api.cli.main solve` 打印（`SignUpFlow/api/cli/main.py:193`）。它的值取决于版本：在
2026-09-16 的 head 上，示例工作区打印 `0.0/100`，有两个硬约束违规。 — `SignUpFlow/README.md`

**本地模型（Local model）** — 权重在你的机器上运行的模型。在 M0 中，例子是 `qwen3:0.6b`；拉取一个
本地模型的意义在于不涉及 API 密钥，也没有云端账单。 — `course/03-content/m00-orientation/lesson.md`

**循环日志（Loop journal）** — 从 M0.2 开始的单一文件，学员在其中为每个行动步骤涉及的每个循环阶段
记一行。 — `course/03-content/m00-orientation/lesson.md`

**端侧（On-device）** — 在用户自己的硬件上进行的处理，因此音频或文本不必离开
设备。ListenToMe 是端侧的案例研究。 — `ListenToMe/README.md`

**证明资产（Proof asset）** — 仓库中可验证的证据——覆盖率徽章、一行带日期的测试证据、一个
来源追溯文件、一份公开的自我审计。不是用户推荐语，也不是 README 里的主张。 — `course/01-design/content-standards.md`

**来源追溯（Provenance）** — 一条主张可追溯的出处：来源、检索日期和主张类型。AI × QE 的每条
主张都带有它，M6 也要求学员的简报具备它。 — `ai_qe/README.md`

**规格套件（Spec kit）** — 一个功能背后的产物集合：规格、研究、计划、契约、快速上手、
检查清单、任务。SignUpFlow 有 17 个这样的文件夹。 — `SignUpFlow/specs/`

**从规格到交付的循环（Spec-to-Ship Loop）** — 每个模块都使用的六阶段方法：研究 → 规格 → 构建 → 验证 →
发布 → 证明，每个阶段都有一件真实的产物。 — `course/00-research/00-synthesis.md`

**租户隔离（Tenant isolation）** — 每一条数据库查询都按 `org_id` 过滤的规则，这样一个组织
永远读不到另一个组织的数据行。缺少过滤就是 P0 缺陷。 — `SignUpFlow/AGENTS.md`

**测试层级（Test tier）** — 测试金字塔中在独立进程里运行的一层。SignUpFlow 记录了七个
层级；完整的本地套件曾记录 "1,464 passed, 21 skipped"。 — `SignUpFlow/docs/TESTING.md`；`SignUpFlow/docs/playbooks/validation.md`

**已验证本地（Verified local）** — 只有在元数据证明它不是远端托管时才被接受的本地模型：
`remote_host`/`remote_model` 不存在，format/model-info 存在。单凭 `localhost` URL 不构成证明。
— `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift`

**YAGNI 非目标（YAGNI non-goals）** — 一个设计明确拒绝构建之物的清单。ListenToMe 的规格写道：
不做云端后端、账号、计费或多用户。 — `ListenToMe/docs/superpowers/specs/2026-06-18-listentome-design.md`

## 容易弄错的术语

- **本地模型与已验证本地（Local model vs. verified local）** — 「在 localhost 上运行」是一个地址；「已验证本地」是
  证明背后模型不是远端的元数据证据。只有后者能通过 M3 的红队测试。
- **证明资产与 README 主张（Proof asset vs. README claim）** — 主张是某人敲出来的文字；证明资产是机器
  输出或带日期的记录。两者都可能出现在 README 里；只有一个是证据。
- **验收标准与成功标准（Acceptance criteria vs. success criteria）** — 验收标准说明一个故事何时完成
  （Given/When/Then）；成功标准说明这个功能在真实世界中是否成功。一份规格两者都需要，
  而且要分开写。 — `SignUpFlow/specs/014-security-hardening/spec.md`
- **验证与证明（Validate vs. Prove）** — 验证表明你构建的东西通过了它的测试；证明是对哪些
  已验证、哪些未验证的诚实记录，包括失败。ListenToMe 的 "do not promote 1.3.0"
  评审属于证明，而不是验证。 — `ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md`
- **发布与证明（Release vs. Prove）** — 发布是你公开的一件产物；只有当它经过签名、带有日期，
  并能追溯到一个源码提交时，它才成为证明。 — `ListenToMe/AGENTS.md`

## 精选资源

1. `course/03-content/m00-orientation/lesson.md` — 模块讲稿；做实验前通读一遍。
2. `SignUpFlow/README.md` — 求解器的 "CLI Example" 给出了你的实验必须对上的确切输出。
3. `course/03-content/m02-ondevice-app/tinycopilot/README.md` — M2 实验参考，外加用一段话讲清的
   隐私实验。
4. `ListenToMe/docs/competition-analysis.md` — 本课程中把研究转化为定位的最佳
   范例。
5. `SignUpFlow/docs/playbooks/validation.md` — 读读失败部分；它就是诚实的标准。
6. `ai_qe/docs/principles.md` — 很短，它的 "baseline before solutioning" 原则贯穿每个
   模块。
7. `course/00-research/00-synthesis.md` — 循环和可迁移原则的推导过程，
   如果你想了解这套方法的来源。
8. `course/01-design/content-standards.md` §0.2 — 已核实数字清单；陈述数字之前先在这里
   核对。
