# 术语表 M3 — 隐私、测试与交付

> 术语按英文字母顺序排列。「出处」是一个你可以打开的文件指针，而不是一个你必须相信的定义。

**Bundle ID 与 TCC 授权（Bundle id / TCC）** — macOS 按 bundle id *加上*二进制文件的代码签名要求来登记麦克风和屏幕录制授权，所以开发构建和发布构建需要各自独立的 id ——
`ListenToMe/docs/RELEASING.md:41-52`。

**云端别名（Cloud alias）** — 一个以 `:cloud` 结尾的模型名（或者一个名字听起来像本地、实际由远端支撑的模型），它在本地守护进程上安装并列出，推理却在远程运行 ——
`ListenToMe/docs/manual-smoke-test.md`；`ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:16`。

**契约测试（Contract test）** — 一种测试 mock 只能假设的真实接缝的测试——这里指针对一个运行中的 Ollama 守护进程检验 NDJSON 请求形态和流式解析——放在 CI 之外，由一个环境变量门控 —— `ListenToMe/Tests/ListenToMeCoreTests/OllamaContractE2ETests.swift:4-22`。

**覆盖率底线（Coverage floor）** — 一道硬性 CI 关卡，当总行覆盖率跌破阈值时让构建失败；它换来的是对未经测试的核心逻辑的强制约束，除此之外什么也换不来 ——
`ListenToMe/scripts/check-coverage.sh`；`ListenToMe/.github/workflows/ci.yml:36-42`。

**完成的定义（Definition of Done）** — 在 ListenToMe 中，指合并到 `main`、必需检查全绿、测试通过、文档已更新；发布是一个独立的、批量进行的步骤。只有一个重新下载、校验和匹配、并且标签位于源提交上的产物，才可以称为已发布 ——
`ListenToMe/AGENTS.md:13-18, 55-82`；`ListenToMe/docs/RELEASING.md:33-39`。

**依赖锁差异检查（Dependency-lock diff）** — 当签入的依赖锁文件与生成的工作区的已解析锁文件出现偏差时，让构建失败的 CI 步骤 —— `ListenToMe/.github/workflows/ci.yml:24, 35`。

**失败即关闭（Fail closed）** — 一种让失败路径成为安全路径的设计：缺失、格式错误或意外的元数据会拒绝请求，而不是让它继续 ——
`ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:17-24`。

**优雅降级（Graceful degradation）** — 关闭 AI 后，采集、转写和保存照常工作；app 是降级，而不是停止 —— `ListenToMe/README.md`，“AI processing mode”。

**回环地址白名单（LOCAL_HOSTS / loopback allowlist）** — 仅本地模式唯一信任的主机：
`localhost`、`127.0.0.1`、`::1`。其他任何主机都会在写出提示词之前抛出异常 ——
`ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:145-147`。

**人工冒烟测试（Manual smoke test）** — 覆盖麦克风采集、系统音频和实时语音转文字的层级，这些都需要一个 GUI 会话和手动授权——一份编号的、可重复的脚本 ——
`ListenToMe/docs/manual-smoke-test.md:1-7`。

**指标与结论（Metric vs. verdict）** — 覆盖率和测试数量是入场费；一次验证你*交付*了什么的评审才是结论 —— `ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md:5`。

**隐私模式（`PrivacyMode`）** — 用户选择的显式三路模式开关（`off`/`local`/`cloud`）；添加云端密钥从不切换它 —— `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:3-13`；
TinyCopilot 中的对应实现：`course/03-content/m02-ondevice-app/tinycopilot/src/tinycopilot/privacy.py:28-45`。

**拒绝重定向（Redirect refusal (`RejectRedirects`)）** — 一个拒绝每一个 3xx、而不是跟随它的传输层，让会议文本永远无法被悄悄转发——Swift 中的 URLSession 委托是
`ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:138-142, 208-214`；Python 孪生实现用
`follow_redirects=False` 构建 httpx，并在遇到 3xx 时抛出异常，见
`course/03-content/m02-ondevice-app/tinycopilot/src/tinycopilot/ollama_provider.py:50-92`。

**测试层级（Test tier）** — 真正能观察到一个风险的最便宜的层：单元（模拟）→ 契约（真实模型，你的机器）→ 人工冒烟（真实音频，真实权限） —— `ListenToMe/docs/manual-smoke-test.md`。

**信任边界（Trust boundary）** — 一项保证的诚实边界。仅本地模式信任已安装的本地 Ollama 服务及其元数据；它校验的是一份自我描述，而不是守护进程本身 ——
`ListenToMe/README.md`，“Privacy”。

**如实的模式标签（Truthful mode label）** — 一个说明数据去向、而不是说明功能有多好的标签——例如 “Ollama Cloud — sends transcript and context” ——
`ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:3-13`。

**本地模型校验函数（`verify_local_model()`）** — 失败即关闭的 `/api/show` 检查：`remote_host` 和 `remote_model` 不存在，`details.format` 和 `model_info` 存在且非空 ——
`course/03-content/m02-ondevice-app/tinycopilot/src/tinycopilot/privacy.py:101-145`。

## 容易弄错的术语

- **本地与已验证本地（Local vs. verified local）** — localhost URL 或模型名只是一个地址；已验证本地是一个说明权重已下载的元数据结果。只有后者才是证据。
- **覆盖率与正确性（Coverage vs. correctness）** — 覆盖率说明你的测试执行了哪些行。它对设计是否服务于用户只字未提；G01 就待在 97.24% 的覆盖率之内。
- **已测试与已交付（Tested vs. shipped）** — 一个全绿的测试套件验证你构建的东西。一次评审验证用户需要的东西。1.3.0 的建议取决于后者，而不是前者。
- **主动选择云端与默认云端（Cloud opted-in vs. cloud by default）** — 主动选择是用户做出并看得见的模式选择。默认走云端按原则不在范围内（`ListenToMe/CLAUDE.md`）。
- **跳过与删除（Skipped vs. deleted）** — 一个需要基础设施的测试应当随套件交付，并带着写明的理由跳过，绝不能被悄悄移除，也不能让它把 CI 挂住。

## 精选资源

- `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift` — 用二十四行讲完整个隐私论证：模式、如实的标签，以及失败即关闭的守卫。
- `ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift` — 看主机强制、逐请求校验和重定向拒绝如何层层包裹一次聊天调用。
- `ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md` — 诚实的评审压过绿色指标的最清晰的现成例子。
- `ListenToMe/docs/RELEASING.md` — 一次止于校验和的发布的具体做法，外加为什么 TCC 迫使你使用两个 bundle id。
- `ListenToMe/docs/competition-analysis.md` — 一张有出处、带日期、有限定的表格；实验 M3 第 4 步照搬它的结构。
- `ListenToMe/docs/manual-smoke-test.md` — 如何为 CI 无法运行的那个层级写文档。
- `course/03-content/m02-ondevice-app/tinycopilot/README.md` — Python 实验的已验证状态，以及一段话的隐私模型。
- `course/01-design/assessment-and-rubrics.md` — 实验、测验和结业项目的权重如何组合。
