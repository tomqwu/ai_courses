# 测验 M2 — 端侧 AI 应用：架构
> AI Product Studio（APS-3）的一部分 · 8 道题（6 道选择题 + 2 道简答题）· 附答案

**Q1.** 一位参会者提出的问题触发了一次主动的 Quick 回应。数据在 ListenToMe 中是按什么顺序流动的？

A. 采集 → 存储 → 转写 → 路由 → 提示词
B. 采集 → 转写 → 存储 → 上下文/提示词 → 路由
C. 转写 → 采集 → 路由 → 存储 → 提示词
D. 采集 → 路由 → 转写 → 提示词 → 存储

**Q2.** ListenToMeCore 在一个实时音频产品上拿到了 96% 的覆盖率徽章。是什么让这成为可能？

A. CI 为测试任务提供了麦克风和系统音频硬件。
B. 所有决策逻辑都位于一个纯 SwiftPM 包中，处在 `AudioCapturing`/`Transcribing`/`LLMProvider` 接缝之后，所以测试针对模拟对象运行，不需要硬件或网络。
C. 覆盖率只在 `App/` 胶水代码上测量，而这部分很小。
D. 95% 底线脚本会排除任何没有测试的模块。

**Q3.** 在 ListenToMe 的 Swift 核心中，一个本地 Ollama 服务器上有三个模型：`qwen3:0.6b`、`deepseek-v4-pro`、`gemini-2.5-flash`。`ModelRanking.roleDefaults` 会如何分配？（按 Swift 实现作答。TinyCopilot 的 Python `role_defaults` 有意简化了这一点，给 Listener 和 Quick 分配同一个最快的模型——在实验中，以它的测试为准。）

A. 三个角色都得到 `deepseek-v4-pro`——最强的模型处处最好。
B. Quick = `gemini-2.5-flash`（快速标记），Deep = `deepseek-v4-pro`（强力标记），Listener = `qwen3:0.6b`（Quick 和 Deep 选走之后剩下的最轻的模型）。
C. Listener = `deepseek-v4-pro`，因为它写的输出最长。
D. 不存在默认值；用户必须手动为三个面板全部选择模型。

**Q4.** `MeetingSession` 为每个角色保留一个 `responseGenerations` 计数器。它是做什么用的？

A. 计费——统计每个角色生成的 token 数。
B. 在角色的模型改变时，使进行中的流失效，这样过期的回答就不会显示在新模型的名下。
C. 在切换模型后重启 Ollama 守护进程。
D. 把旧流的 token 排队，等新模型完成后再合并进去。

**Q5.** 你正在克隆下来的仓库中追踪 采集 → 转写 → 上下文 → 提示词。哪个选项给出了*实现*每个阶段的文件？

A. 采集：`Sources/ListenToMeCore/Capture.swift` · 转写：`Sources/ListenToMeCore/Transcriber.swift` · 转写日志 + 上下文窗口：`Sources/ListenToMeCore/ConversationStore.swift` · 提示词字符串：`Sources/ListenToMeCore/ContextEngine.swift`
B. 采集：`App/DualChannelCapture.swift` · 转写：位于 `Transcribing` 接缝之后的 `App/SpeechAnalyzerTranscriber.swift`（以及两个备选引擎）· 转写日志 + 上下文窗口：`Sources/ListenToMeCore/ConversationStore.swift` · 提示词字符串：`Sources/ListenToMeCore/Prompt.swift`
C. 四个阶段都在 `App/MeetingView.swift` 中——采集、转写、存储和提示词都留在显示它们的视图里，这样流水线可以在一个文件里从上读到下。
D. 采集：`App/DualChannelCapture.swift` · 转写：`Sources/ListenToMeCore/VAD.swift` · 转写日志：`Sources/ListenToMeCore/MeetingSession.swift` · 提示词字符串：`Sources/ListenToMeCore/ModelRouter.swift`

**Q6.** 为什么 Listener 的系统提示词要写 "Never invent an owner, deadline, agreement, or completion. Mark missing details as unstated"？

A. 为了让滚动摘要保持在 3,072 个 token 的预算之内。
B. 本地 Ollama 模型无法可靠地从转写文本中抄出名字，所以提到任何人都不安全。
C. Listener 的摘要会被注入 Quick/Deep 的提示词，所以一个编造出来的承诺会扩散到下游的每一个回答中；与之配套的规则是只注入*已完成*的摘要。
D. 会议转写方面的法律要求标出未说明的细节。

**Q7.** 一位测试人员报告：「Quick 面板把一个 40 个 token 的回答显示为已完成，但模型其实在一句话中间就停了——NDJSON 流结束时没有出现 `done: true` 这一行。」根据 `OllamaProvider.streamEvents` 中的类型化错误设计，说出这是哪一个 `OllamaStreamError` 情况，说明提供方必须怎么做，而不是把部分文本当作完整回答返回，并写出本来能抓住它的那一个单元测试（TinyCopilot 或 Swift 均可）。

**Q8.** 关于你的主动 Quick 触发器，有两份缺陷报告：（1）在一轮快速问答中，它十秒内触发了三次；（2）它有一次回答了*你自己*提的问题，而不是参会者提的问题。根据 `ContextEngine.shouldFireProactive` 中的守卫条件，说出每份报告违反了哪个条件，说出两份报告都没有提到的那个条件，并写出锁定修复的两个单元测试用例。

---

## Answer key

**Q1 — B.** 数据块依次流经 采集 → `Transcribing` 接缝 → `ConversationStore` → 提示词组装 → 按角色的提供方；没有任何环节会跳过存储或打乱顺序。*（目标：M2.1 流水线 — `docs/superpowers/specs/2026-06-18-listentome-design.md` §3、§5。）*

**Q2 — B.** 每一个决策都位于纯核心中、在三个协议接缝之后，所以测试套件针对模拟对象运行——不需要硬件，不需要网络。*（目标：M2.1 协议接缝 — `Sources/ListenToMeCore/Transcriber.swift`、`README.md` 徽章。）*

**Q3 — B.** Swift 从排好序的候选池中按角色挑选：第一个匹配快速标记的 → Quick，排除 Quick 所选之后最强的强力标记匹配 → Deep，然后 Listener = 第二个快速模型，如果没有，就取剩下最轻的模型——这里是 `qwen3:0.6b`。TinyCopilot 的 `role_defaults` 有意把 `listener` 和 `quick` 映射到同一个最快的模型（`tinycopilot/src/tinycopilot/model_router.py:176`），所以不要把这个答案带进实验。*（目标：M2.2 角色路由 — 标记见 `ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:49-54`，挑选逻辑见 `ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:91-111`。）*

**Q4 — B.** `setModel` 调用 `cancelResponse`，后者把生成编号加一；流式循环用它守护每一次写入，所以过期的 token 不会在切换之后落地。*（目标：M2.2 过期流的取消 — `ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:204-221, 803-880`。）*

**Q5 — B.** Core 声明接缝；App 提供实现。`Capture.swift` 是 `AudioCapturing` 协议，而且它自己就这么说——"Real impl lives in the app target"（`ListenToMe/Sources/ListenToMeCore/Capture.swift:3-9`）——提供实现的是 `ListenToMe/App/DualChannelCapture.swift:8-10` 中的麦克风 + ScreenCaptureKit tap；`Transcriber.swift:4` 声明了 `Transcribing`，三个引擎位于它之后的 `App/` 中。日志和永不为空的上下文窗口是 `ConversationStore.recentContext`（`ListenToMe/Sources/ListenToMeCore/ConversationStore.swift:76-87`）；提示词字符串由纯的 `PromptBuilder` 构建（`ListenToMe/Sources/ListenToMeCore/Prompt.swift:87`）。A 把两个协议文件误当成了实现，并把提示词放进了 `ContextEngine.swift`，而后者只是 "assembles prompt context and decides when to fire a proactive suggestion"（`ListenToMe/Sources/ListenToMeCore/ContextEngine.swift:3`）。C 是本节所反对的那种不分层的形态——一个拥有整条流水线的视图无法做单元测试，而 96% 的核心徽章恰恰依赖于它不这样做。D 换进了三个做别的事的文件：`VAD.swift` 按能量和静音找出语句边界，`MeetingSession.swift` 负责按角色的路由和取消，而 `ModelRouter.swift` "holds the registered providers and routes streaming requests to the active one"（`ListenToMe/Sources/ListenToMeCore/ModelRouter.swift:4-6`）。*（目标：M2.1 说出实现每个阶段的文件 — `ListenToMe/Sources/ListenToMeCore/Capture.swift:3-9`；`ListenToMe/Sources/ListenToMeCore/Transcriber.swift:4`；`ListenToMe/App/DualChannelCapture.swift:8-10`；`ListenToMe/Sources/ListenToMeCore/ConversationStore.swift:76-87`；`ListenToMe/Sources/ListenToMeCore/Prompt.swift:87`。）*

**Q6 — C.** Listener 的摘要为下游的每个面板提供依据，所以一个编造出来的承诺会扩散开来；只有 `lastCompletedListenerSummary` 会被注入。*（目标：M2.2 绝不编造约定 — `ListenToMe/Sources/ListenToMeCore/Prompt.swift:137-145`。）*

**Q7 — Acceptable answer:** `.incomplete`——行来源在没有 `done: true` 事件的情况下结束了（抛出位置在 `ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:101`；枚举在 `ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:216-224`）。提供方必须*抛出*它，这样流就以一个面板会显示出来的错误结束（"The response ended before completion. Partial text is kept; retry the request."），而绝不是以成功结束——吞掉它就会把截断变成看似完成，这正是差距 G06 的发现。测试：一个伪造的传输层先产出若干内容行，然后在没有 `done: true` 的情况下关闭；断言提供方抛出 `IncompleteStreamError`（`tinycopilot/src/tinycopilot/ollama_provider.py:32`）或 `OllamaStreamError.incomplete`，而不是返回那段部分字符串。*（目标：M2.3 类型化的流式错误。）*

**Q8 — Acceptable answer:** （1）违反了 8 秒防抖——每个窗口最多触发一次（`now - lastFire >= debounce`）；（2）违反了 `segment.source == .others`——你自己的问题永远不会触发。两份报告都没有提到的条件是 `segment.isFinal`（检测器还必须把这段文本判定为问题）。测试：两个相隔 3 秒的已定稿 `.others` 问题 → 第二次调用返回 `false`；一个来自 `.you` 的已定稿问题 → `false`。*（目标：M2.3 有界的主动触发 — `ListenToMe/Sources/ListenToMeCore/ContextEngine.swift:41-50`；TinyCopilot 在 `tinycopilot/src/tinycopilot/question_detector.py` 中的 `QuestionDetector.should_fire` 执行同样的四项检查。）*
## 目标 → 评估对照表

`course/03-content/m02-ondevice-app/lesson.md` 中每一条「学完本模块，你能够」，以及检查它的方式。

| 目标（lesson.md） | 检查方式 |
|---|---|
| 解释并画出 采集 → 转写 → 上下文 → 提示词 → 路由 这条流水线，并说出实现每个阶段的文件 | Q1（阶段顺序）、Q5（每个阶段的文件，接缝与实现之分）；实验 M2 在 `tinycopilot/src/tinycopilot/` 中重建同样的阶段 |
| 为三个协议接缝给出理由，并实现一个会话存储，它带有按字符预算的上下文窗口，且总是至少保留最新的片段 | Q2（为什么接缝让 96% 的徽章成为可能）；实验 M2 的 `conversation_store.py` 及其在 `make lab-m2` 中的测试（201 passed） |
| 用本地优先的默认值、词首前缀匹配，以及切换模型时对过期流的取消，把不同的模型路由给不同的角色 | Q3（角色默认值）、Q4（按角色的生成计数器）；实验 M2 的 `model_router.py` |
| 把提示词构建器写成纯函数——包括一份「绝不编造」的据实约定和一种不要开场白的风格 | Q6（为什么 Listener 约定对下游至关重要）；实验 M2 的 `prompts.py`，逐字符串断言 |
| 用一个有意保持简单、放在防抖之后的问题检测器，加入主动行为 | Q8（每个缺陷违反了哪个守卫条件，以及锁定修复的两个测试）；实验 M2 的 `question_detector.py` |
| 为流式错误定义类型，让截断或空的响应永远不可能以成功告终 | Q7（说出情况、提供方必须怎么做，以及抓住它的测试）；实验 M2 的 `ollama_provider.py`，实验 M3 第 1 步 |
