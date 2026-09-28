# 第 2 模块 — 端侧 AI 应用：架构
> AI Product Studio（APS-3）的一部分 · 约 75 分钟 · 前置：第 1 模块

## 概览

```figure
kind: scene
alt: 笔记本电脑上的一场视频会议，通话旁边有一个助手面板正在给出建议。
scene: meeting.svg
caption: ListenToMe 的用途——一个在通话旁边、而不是在通话之中的助手
```

第 1 模块给了你一套 AI 辅助构建的操作系统。本模块打开第一种产品原型（archetype）：**原生端侧（on-device）AI 应用**——一个实时系统，它采集外部世界，在本地对其进行推理，并让用户掌控离开这台机器的每一个字节。你的案例研究是 ListenToMe，一个免费、开源的 macOS 会议助手：它收听你的麦克风和其他参会者的系统音频，在端侧实时转写，并通过 Ollama、用你选择的模型以流式方式提供 AI 帮助（`README.md`）。它由一位工程师发布，带着 96% 的核心覆盖率徽章——这只有靠你即将学习的这套架构才能做到。

这种产品原型的核心工程问题是：真正有意思的决策——分段、上下文窗口、问题检测、模型路由、提示词组装、流错误处理——全都位于音频硬件和一个实时运行的 LLM 守护进程的下游，而这两者 CI 运行器都碰不到。ListenToMe 的答案是一道硬分界。每一个决策都放在 `Sources/ListenToMeCore` 中，这是一个纯 SwiftPM 包，含 45 个 Swift 源文件（截至 2026-09-16 共 5,194 行），运行测试不需要麦克风、不需要屏幕采集，也不需要网络；`App/` 只放平台胶水代码——AVAudioEngine、ScreenCaptureKit、Speech、SwiftUI。两侧在三个协议接缝（protocol seam）处相遇：`AudioCapturing`、`Transcribing` 和 `LLMProvider`。整条流水线在单元测试中针对模拟对象运行；只有那层薄薄的胶水代码留给人去做冒烟测试。

在本模块中，你将端到端地追踪这条流水线（M2.1），学习三个 AI 角色如何被路由到不同的模型、并按角色取消（M2.2），并看到「主动智能」实际上是一个廉价的启发式规则，外面包裹着预算、防抖和类型化错误（M2.3）。在实验中，你将构建 TinyCopilot——用 Python + Ollama 实现的同一套架构，小到一次就能完成。

**学完本模块，你能够：**

- 解释并画出 采集 → 转写 → 上下文 → 提示词 → 路由 这条流水线，并说出实现每个阶段的文件。
- 为三个协议接缝给出理由，并实现一个会话存储，它带有按字符预算的上下文窗口，且总是至少保留最新的片段。
- 用本地优先的默认值、词首前缀匹配，以及切换模型时对过期流的取消，把不同的模型路由给不同的角色。
- 把提示词构建器写成纯函数——包括一份「绝不编造」的据实约定和一种不要开场白的风格。
- 用一个有意保持简单、放在防抖之后的问题检测器，加入主动行为。
- 为流式错误定义类型，让截断或空的响应永远不可能以成功告终。

> **指针约定。** ListenToMe 的指针都相对于克隆下来的仓库根目录。打开行动步骤中提到的每一个文件——这些指针是本课程的出处。

## M2.1 — 采集→转写→上下文→提示词→路由流水线（约 25 分钟）

### 目标

解释 ListenToMe 的分层架构：说出各层，说出三个协议接缝，并论证「纯核心 / 应用胶水」这一划分。凭记忆画出流水线，并在代码中找到每个阶段。

### 讲解

从已发布的产品出发，倒着往回走。ListenToMe 实时采集两路音频——你的麦克风（标记为 **You**），以及通过 ScreenCaptureKit 获取的其他参会者的系统音频（标记为 **Others**）——并给每个 AI 面板配上各自的模型（`README.md`，"Why ListenToMe"）。已批准的设计规格描述了一个单进程 SwiftUI 应用，其中 "audio and ASR run off the main actor; UI observes published state"（`docs/superpowers/specs/2026-06-18-listentome-design.md`，§3）。下面是实际发布的流水线——改编自该规格的架构图（§3），把规格中单一的 Response/Summary 引擎换成了实际发布的三个角色（`Sources/ListenToMeCore/CopilotRole.swift`）：

```
      mic (.you)  ·  system audio (.others)
                     PCM chunks
                        │
      ┌──────────────────▼─────────────────┐
      │ DualChannelCapture (App/ glue)     │   seam: AudioCapturing
      └──────────────────┬─────────────────┘
                        ▼
      ┌────────────────────────────────────┐
      │ Transcriber (protocol seam)        │   seam: Transcribing
      │  SpeechAnalyzer (default)          │
      │  SpeechRecognizer (legacy)         │
      │  WhisperKit (opt-in)               │
      └──────────────────┬─────────────────┘
        partial + finalized segments
                        ▼
      ┌────────────────────────────────────┐
      │ ConversationStore                  │
      │  rolling utterance log;            │
      │  recentContext ≤ 4,000 chars       │
      └──────────────────┬─────────────────┘
                        ▼
  hotkey ─────────────┐
  QuestionDetector ───┴─▶ ContextEngine ─▶ PromptBuilder (pure)
  + 8 s debounce             Listener / Quick / Deep prompts
                      │
                      ▼
      ┌────────────────────────────────────┐
      │ MeetingSession per-role routing    │   seam: LLMProvider
      │  model + provider per role;        │
      │  generation token per role         │
      │  → OllamaProvider /api/chat        │
      └──────────────────┬─────────────────┘
              streamed token deltas
                      ▼
         Listener · Quick · Deep panes
```

**第 1 层——采集。** `App/DualChannelCapture.swift` 在 `AVAudioEngine` 的输入节点上接入麦克风，并为系统音频创建一个 ScreenCaptureKit `SCStream`，"converting both to mono Float PCM and emitting `AudioChunk`s"（见其头部注释，`ListenToMe/App/DualChannelCapture.swift:8-9`）。每个缓冲区都带有一个 `SpeakerSource` 标记——麦克风 tap 标记为 `.you`（`ListenToMe/App/DualChannelCapture.swift:143`），`SCStream` 回调标记为 `.others`（`ListenToMe/App/DualChannelCapture.swift:324`）。正是这一个标记，让应用零成本地获得说话人归属："You" 与 "Others"，无需说话人分离模型。采集是产品中最难测试的代码，所以它也是最薄的。

**第 2 层——转写接缝。** Core 声明协议；App 提供引擎。`Sources/ListenToMeCore/Transcriber.swift` 定义了 `Transcribing`——`prepare()`、`feed(_:)`、`finish()`——并附有成文的约定：`prepare()` 在喂入任何音频*之前*预热流水线（下载模型、启动分析器），这样 `feed` 永远不会阻塞，会议开头的几秒也不会丢失；而且它在预热过程中必须响应取消。这一个接缝后面有三个引擎，在设置中选择：

- **`SpeechAnalyzerTranscriber`**（默认）：Apple 在 macOS 26 中提供的 SpeechAnalyzer。每个来源一个分析器，所以两个声道可以并发转写，"unlike SFSpeechRecognizer"，后者有同一时间只能进行一个识别的限制（`ListenToMe/App/SpeechAnalyzerTranscriber.swift:6-39`）。
- **`SpeechRecognizerTranscriber`**（旧版）：较早的 `SFSpeechRecognizer`，每个来源一个识别任务。它可能触发 Apple 的进程级全局活跃识别上限，报错 `kAFAssistantErrorDomain 1100`——README 的已知限制中记录了这一点，这也是 `MeetingSession` 保留一个停止排空任务的原因，这样快速重启时就不会同时运行两个这样的识别器（`ListenToMe/README.md:374-376`；`ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:164-166`）。
- **`WhisperKitTranscriber`**（需主动开启）：一个批处理转写器。它缓冲每个来源的音频，使用 Core 的 `VADSegmenter` 找出语句边界，只输出*已定稿*的片段——用实时的临时结果换取 "Whisper's stronger multilingual / code-switching quality"（`ListenToMe/App/WhisperKitTranscriber.swift:6-13`）。之所以有这种取舍，是因为 Apple 的端侧 Speech "selects one primary language; it does not auto-detect or code-switch"（`ListenToMe/App/MeetingView.swift:106-107`）——普通话与英语混说的场景，正是 WhisperKit 的用武之地。

接缝才是关键：下游的一切都分辨不出片段是哪个引擎产生的——加第四个引擎，协议之下什么都不用改。

**第 3 层——存储与上下文窗口。** `Sources/ListenToMeCore/ConversationStore.swift` 是唯一的事实来源：一份有序的、已定稿的 `TranscriptSegment` 日志，外加每个来源当前的临时结果（`apply(_:)` 追加最终结果，替换临时结果）。上下文窗口（context window）是 `recentContext(maxChars:)`：从最新的语句开始往回走，片段放得进预算就保留，并且总是包含最近的那一条，即使它单独就超出预算——窗口永远不会为空（`ListenToMe/Sources/ListenToMeCore/ConversationStore.swift:76-87`）。默认预算是 4,000 个字符（`ContextEngine.buildContext`，`ListenToMe/Sources/ListenToMeCore/ContextEngine.swift:12`），而预算随意图变化：`MeetingSession.transcriptBudget(for:)` 给回顾和行动项提示词 100,000 个字符，因为它们必须覆盖整场对话，而即时回答只拿到最近的窗口（`ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:582-587`）。

**语句边界从哪里来。** 当引擎不以流式输出临时结果时（WhisperKit），必须有某个东西来决定一句话在哪里结束。Core 的语音活动检测（VAD）只有 37 行：`rms(of:)` 逐帧计算均方根能量，`VADSegmenter`（默认值：语音阈值 0.02，尾部静音 0.8 秒）返回 `true` "exactly once, on the frame where trailing silence after speech first exceeds `silenceDuration`"（`Sources/ListenToMeCore/VAD.swift`）。没有机器学习模型——只有一个阈值和一个计时器，由 `Tests/ListenToMeCoreTests/VADTests.swift` 验证。

**分层为什么值得。** 上面标为 Core 的一切都是纯的：没有麦克风，没有网络，没有界面。这就是一个实时音频产品能拿到 96% 核心覆盖率徽章、并在 CI 中强制执行 95% 底线的原因（`README.md` 徽章；`scripts/check-coverage.sh`，默认阈值 95）。胶水代码无法做单元测试，所以要把它压到最少；逻辑可以，所以要把产品放在那里。你的 TinyCopilot 实验完全照搬这个形态：一个由预先准备的转写文件来满足的转写接缝，其余一切都是纯的、经过测试的。

**离开 Mac 的同一种产品原型。** 上面只有胶水代码是 Apple 专属的。核心及其三个接缝才是架构；平台只决定两件事：哪些系统服务可以填充 `Transcribing` 和 `LLMProvider`，以及在信任它们之前你必须检查什么。截至 2026 年 9 月，每个主要的客户端平台都提供了一套端侧技术栈。下表压缩概括了每个平台提供什么、限制什么，以及哪些仍然是你自己的代码。每个单元格都是厂商对自家产品的描述；每一项的来源、读取日期和证据等级见 `course/03-content/m02-ondevice-app/appendix-models-2026-09.md`。

| | Apple | Windows | Android |
|---|---|---|---|
| **操作系统提供的语言模型** | Foundation Models：端侧的 Apple Intelligence 模型，OS 26+。从 OS 27 起，一个 `LanguageModel` 协议让任何提供方都能接入同一套 API | 在 Copilot+ PC 上，通过 Windows AI API 使用 Phi Silica。Foundry Local：在任何 Windows 硬件上，通过兼容 OpenAI 的 API 提供 20 多个开源 LLM 和语音模型 | 通过 ML Kit GenAI Prompt API 使用 Gemini Nano，由 AICore 系统服务运行 |
| **语音** | SpeechAnalyzer，ListenToMe 的默认引擎 | 通过 Foundry Local 使用 Whisper，或较早的 Windows SDK 识别器 | ML Kit GenAI 语音识别 |
| **自带模型** | Core AI（在 WWDC26 上发布）和 MLX | Windows ML：ONNX Runtime，带有由 Windows 安装和更新的 NPU、GPU 和 CPU 执行提供方。直接在其上运行 LLM 被标为 Preview | LiteRT-LM，其 Kotlin API 被标为 Stable |
| **它限制什么** | 一台支持 Apple Intelligence 的设备、一个受支持的地区，以及用户的主动开启。窗口很小：ListenToMe 把每个 Apple 提示词限制在 8,000 个字符以内 | Phi Silica 需要 Copilot+ PC 和一个解锁令牌，并且不在中国提供。Foundry Local 的 WinML 构建在没有 GPU 直通的虚拟机上会返回一个*成功但为空*的响应，而且运行时 "may collect usage data and send it to Microsoft" | 提示词输入少于 4,000 个 token，每个应用有推理配额，而模型可能仍在下载中。Prompt API 是 beta 版（`1.0.0-beta4`） |
| **你仍然要写的** | 一个可用性降级方案、一个提示词预算，以及映射为用户能据以行动的消息的错误 | 同上，外加一条降级链。Microsoft 自己的示例从 Phi Silica 降到 Foundry Local 再降到 Azure；一个本地优先的产品止步于 Foundry Local，或者先征得同意 | 同上，外加下载状态（`DOWNLOADABLE`、`DOWNLOADING`）和配额错误 |

有三件事是这张表改变不了的。**决策仍然归你。** 上下文窗口、问题关卡、角色路由、提示词和类型化的流错误，不在任何平台的 API 里；在每个操作系统上，它们都位于你的核心中。**平台模型是一个提供方，而不是一套架构。** ListenToMe 已经两次填充了 `LLMProvider`。在 `OllamaProvider` 旁边是 `AppleIntelligenceProvider`，它在生成之前检查可用性（`ListenToMe/SharedPlatform/AppleIntelligenceProvider.swift:17-25`），拒绝超出预算的提示词，而不是基于截断后的提示词作答（`ListenToMe/SharedPlatform/AppleIntelligenceProvider.swift:80-85`），并把每个 Foundation Models 错误转换成一条指明出路的消息（`ListenToMe/SharedPlatform/AppleIntelligenceProvider.swift:42-65`）。应用在一个闭包里二选一地挑选提供方（`ListenToMe/App/MeetingView.swift:176-180`）。**端侧不等于足够好。** ListenToMe 曾尝试把 Apple 模型用作自动的 Quick 评估器："The native Auto experiment failed the quality gate (3/7 cases …)"，所以它仍被排除在两个应用目标之外（`ListenToMe/docs/SHARED-LIVE-SUMMARY.md:64-68`）。在发布之前，要针对每个平台模型逐个角色进行测量。Foundry Local 的空成功是从另一面发出的同一个警告：它正是 M2.3 的 `.empty` 错误所要拒绝的那种流。

**本课程运行的是什么。** 各个实验都是用 Python 对接 Ollama，而 Ollama 可以安装在 macOS、Windows 和 Linux 上。实验 M2 中的 Swift 路线是本课程唯一提供的平台代码，而且只能在 Mac 上运行（`lab.md`，"Swift track"）。这里不提供任何 Windows 或 Android 代码，表中的一切也都没有经过本课程构建或测量。如果你的目标是 Windows 或 Android，架构可以原样迁移：移植核心，然后在同样的接缝后面写一个 `LLMProvider` 和一个转写适配器，并像 TinyCopilot 那样针对伪造实现来测试它们。

### 行动步骤

打开克隆下来的仓库，亲眼验证每一个论断；把发现记录在你的证据日志中：

1. 打开 `Sources/ListenToMeCore/ConversationStore.swift`，阅读 `recentContext(maxChars:)`。在代码中确认：即使最新的语句超出预算，它也会被包含。
2. 打开 `App/DualChannelCapture.swift`，找到缓冲区被标记为 `.you` 和 `.others` 的两处（麦克风 tap 和 `SCStream` 输出回调）。
3. 打开 `Sources/ListenToMeCore/Transcriber.swift`，记下 `prepare()` 的约定：在音频之前预热，并响应取消。
4. 在证据日志中凭记忆画出流水线图，并写出实现每个阶段的文件。
5. 打开 `ListenToMe/SharedPlatform/AppleIntelligenceProvider.swift:17-25`，抄下三个 `.unavailable` 情况。针对你将要发布的平台，根据上表写出对应的检查，以及你的界面对每种情况显示什么。

## M2.2 — 按角色的模型路由与提示词构建器（约 25 分钟）

### 目标

解释为什么一个 AI 角色 ≠ 一个模型，用本地优先的默认值为每个角色分配合适的模型，在切换模型时取消过期的流，并把提示词构建器写成带据实约定的纯函数。

### 讲解

ListenToMe 的界面显示四个面板——Transcript、Listener、Quick、Deep——并且 "Each AI pane's model is set from a model picker in the left status rail"（`ListenToMe/README.md:120-121`），还标注了 "good for" 提示（`ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:119-159`）。角色是一个枚举，而不是界面上的偶然产物：`listener`、`quick`、`deep`（`Sources/ListenToMeCore/CopilotRole.swift`）。Quick 通过全局快捷键作答，还会主动触发——它必须快（`ListenToMe/README.md:101-105`）。Deep 按需给出长推理回答——它应该强（`ListenToMe/README.md:106`）。Listener 维护一份滚动摘要（`ListenToMe/README.md:100`），它 "auto-refreshes continuously, so speed beats depth"（`ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:74-78`）。

那个诱人的设计——「处处都用最好的模型」——错了两次。它在不需要强度的角色上浪费延迟，还把整个产品绑死在某一个模型的怪癖上。按角色路由把模型选择变成了一份用户看得见、改得了的按面板预算。

**本地优先的默认值（local-first defaults）。** 应用发现已安装的模型时，会调用 `ModelRanking.roleDefaults(from:local:)`（`ListenToMe/App/MeetingView.swift:845`；逻辑在 `ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:91-111`）。Quick 得到一个精选的快速模型——匹配 `fastPatterns`（flash、mini、nano、lite、small、fast）——否则就选最轻的。Deep 得到一个精选的强力模型——匹配 `strongPatterns`（pro、reason、think、coder、code、ultra、max、large）——否则就选最重的，而且是从 Quick 没选走的模型里挑，这样一个同时匹配两组标记的名字就不会让两个面板落到同一个模型上。Listener 得到第二个快速模型，与 Quick 和 Deep 都不同，因为它持续刷新。这些默认值是**本地优先**的：只要 Ollama 自己的 `/api/show` 元数据已经把任何一个模型验证为本地模型，就只考虑这些模型（当本地性未知时，以 `:cloud` 或 `-cloud` 名称作为后备判断），所以一个没有固定模型的面板永远不会悄悄把转写文本发送到 Ollama Cloud；只有在不存在任何本地模型时，才会自动选中云端模型（`ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:80-95`）。"good for" 提示来自同一个文件：`describe(_:)` 把大约二十个已知的模型家族映射为一行提示，并以关键词启发式规则作为后备（`ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:119-159`）。

**选哪些模型？调研放在一份带日期的附录里。** 上面的规则比任何模型清单都更长寿；清单则不然。仅 Qwen 一家就在 2026 年 2 月到 8 月之间发布了 Qwen3.5、3.6 和 3.8，所以本课不收录任何模型调研。对照表是 `course/03-content/m02-ondevice-app/appendix-models-2026-09.md`：家族、规模、各自擅长什么、在哪里运行，每一行都附有来源及其读取日期。日期就在文件名里。调研过时后，会有一份新的带日期文件取代它，这个指针随之改变；其他什么都不变。实验的默认模型不随调研变动。`qwen3:0.6b` 仍然是 `lab.md` 要你拉取的模型，也是 TinyCopilot 的演示和隐私测试所指定的模型，因为它能在任何笔记本电脑上运行，而不是因为它在哪方面胜出。ListenToMe 在代码中也体现了同样的分工：路由基于两个简短的标记列表（`ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:49-54`），而 `describe(_:)` 的提示是一张手工维护的、包含 21 个模型家族的表（`ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:119-143`），它会像任何调研一样过时。规则老得慢；清单老得快。给清单标上日期。

**词首前缀匹配（token-prefix matching）。** 为了在名字中检测 "mini"，`ModelRanking` 把名字拆成小写的词，检查是否有某个词*以*该标记*开头*——"Token-prefix matching (not raw substring) rejects cross-token false hits like `gemini` ⊃ `mini`"（`ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:13-18`）。原始的子串检查会把每个 Gemini 模型都排为「快速」，因为 "gemini" 包含 "mini"——你的默认值会对整个模型家族悄悄出错。

**生成令牌（generation token）——终结过期的流。** `MeetingSession` 按角色维护 `models`、`providers` 和 `responseGenerations` 三个字典（`ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:123, 144, 169-170`）。`setModel(_:_)` 调用 `cancelResponse(_:)`，后者取消该角色进行中的任务，并把它的生成计数器加一（`ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:204-221`）。流式循环记下自己的生成编号，并用 `generation == responseGenerations[role]` 守护每一次写入（`ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:803-880`），所以当你在回答中途切换模型时，旧流的 token 会被直接丢弃——没有这一点，旧模型的一个慢回答就可能在切换*之后*才完成，并显示在新模型的名下。

**提示词构建器是纯函数。** `PromptBuilder` 是一个 `public enum`，只有静态函数，零 I/O（`Sources/ListenToMeCore/Prompt.swift`）：上下文进，`LLMRequest` 出。正是这种纯粹性让提示词可以做单元测试（`Tests/ListenToMeCoreTests/PromptBuilderTests.swift`）——你对构建出的字符串做断言，不需要模型。随产品发布的有三个基础系统提示词：

- **Quick** 不要开场白："Be concise and conversational. No preamble, no 'As an AI', no restating the question, no meta-commentary. Prefer 1-3 short sentences or a tight bullet list. If a question was asked, answer it directly first."（`ListenToMe/Sources/ListenToMeCore/Prompt.swift:129-135`）。在一个你以会议节奏阅读的面板里，每一个开场白字眼都是一笔延迟税。
- **Listener** 承载据实约定："Never invent an owner, deadline, agreement, or completion. Mark missing details as unstated."（`ListenToMe/Sources/ListenToMeCore/Prompt.swift:137-145`）。Listener 的输出会回流到其他面板的提示词中，所以一个幻觉出来的负责人就会扩散到所有地方；这份约定在源头把它挡住。
- **Deep** 反转了 Quick 的预算："Be thorough and precise — depth is valued over brevity here."（`ListenToMe/Sources/ListenToMeCore/Prompt.swift:147-152`）。

在基础提示词之上是 **9 个响应动作**——`answerQuestion`、`recap`、`followUp`、`proactive`、`actionItems`、`clarify`、`counterpoint`、`keyTerms`、`draftReply`——每个都有独立的 Quick 和 Deep 指令变体（`ListenToMe/Sources/ListenToMeCore/Prompt.swift:14-24, 154-201`）。而 `systemWithDirectives(_:_)` 会把所选预设的人设指导和一条响应语言指令追加到*每个*面板的系统提示词中（`ListenToMe/Sources/ListenToMeCore/Prompt.swift:245-260`）——手动面板和自动评审走同一条路径，所以像 Interview 这样的预设会以完全相同的方式塑造全部三个角色。

**Listener→Quick/Deep 的依据。** Quick 和 Deep 的提示词以 Listener 的摘要为依据——但只用最后一份*已完成*的摘要。`MeetingSession` 把 `lastCompletedListenerSummary` 与 `listenerSummary` 分开保存，后者是实时显示的值，在刷新以流式进行时会被清空，"so a proactive Quick can't read an empty/partial in-flight summary"（`ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:53, 81-84`）。它只在一个地方被读取，即 `clampedContext`，它同时构建 Quick 和 Deep 的提示词（`ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:601-605, 640-653`）。常见的误解——「上下文越多越好，屏幕上有什么就注入什么」——恰恰在这里失败：一份进行中的摘要比没有摘要*更糟*，因为它是看起来很自信的半个答案。只注入已完成的工作。

### 行动步骤

1. 打开 `Sources/ListenToMeCore/Prompt.swift`。找到 Listener 的绝不编造约定，以及 Quick 面板那句不要开场白的话。把两者抄进你的证据日志，并各写一句话，说明删掉这一行会坏掉什么。
2. 打开 `Sources/ListenToMeCore/ModelRanking.swift`，手工追踪 `hasMarker("gemini-2.5-flash", "mini")`；然后与 `"gemini-2.5-flash".contains("mini")` 对比。记录两个结果。
3. 打开 `ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:204-221` 和 `ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:803-880`：从 `setModel` 跟进到 `cancelResponse`，那里把生成计数器加一，再找到流式循环检查它的地方。
4. 运行 `ollama list`。在证据日志中，把你已安装的每个模型分配给 Listener/Quick/Deep，并用上面的规则为每个选择给出理由。如果你只有 `qwen3:0.6b`，就改为从附录中挑一个 Quick 候选和一个 Deep 候选，并在每个选择旁写上附录的读取日期。

## M2.3 — 不靠魔法的主动智能（约 25 分钟）

### 目标

用一个放在防抖之后、有意保持简单的启发式规则实现主动触发，并把流式失败当作类型化的、可见的错误来处理——自动化要在预算之内进行，而不是凭感觉。

### 讲解

「主动」听起来需要智能。它需要的是克制。ListenToMe 的问题检测器只有 28 行：`Sources/ListenToMeCore/QuestionDetector.swift` 把一条已定稿的语句判定为问题，条件是它以 "?" 结尾、*以*疑问词*开头*（what、why、how、when、where、who、which、whose），或者包含一个按词边界匹配的短语线索（"can you"、"could you"、"any thoughts"、"walk me through"、…）。设计规格是有意这样选择的：问题检测是一个 "lightweight heuristic … Debounced so it fires at most once per N seconds. Kept deliberately simple; swappable later"（`docs/superpowers/specs/2026-06-18-listentome-design.md`，§4.4）。把廉价的启发式规则*放在接缝后面*上线，保留换成分类器的选项，把你的复杂度预算花在别处。

克制来自关卡。`ContextEngine.shouldFireProactive(for:now:)` 只有在以下条件全部满足时才会触发：片段已定稿、来自 `.others`（是别人在问*你*——而不是你在自言自语）、通过问题检测，**并且**距离上次触发已经过去至少 `debounce` 秒（默认 8 秒）（`ListenToMe/Sources/ListenToMeCore/ContextEngine.swift:8, 41-50`）。没有防抖（debounce），两分钟激烈的连续提问就会让面板被重叠的建议淹没。一次触发，一个回答，然后安静。

**带类型化错误的流式处理。** `OllamaProvider` 以 `stream: true` 向 `/api/chat` 发送 POST 请求，并把响应作为 NDJSON 行读取——每一行都是一个 JSON 对象，携带一段消息增量或 `done: true`（`ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:159-177`；`lineSource` 可以注入，这样测试就能喂入预先准备的行：`ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:42-50`）。有三个细节让它达到生产级：

1. **流内错误事件。** Ollama 可能先以 HTTP 200 应答，然后在流中途发送 `{"error": "..."}`。提供方解析每一行，发现这种情况时抛出 `OllamaStreamError.server(error)`（`ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:84-86`）。
2. **完成标志。** 流式循环跟踪 `completed`（见到了 `done: true`）和 `producedContent`（至少产出了一段非空白的增量）。如果各行结束时没有 `done`，它抛出 `.incomplete`；如果流「完成」了却没有内容，它抛出 `.empty`，或者在模型只发送了推理内容时抛出 `.thinkingOnly`（`ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:79-104`）。因此，一个截断的或空的流*不可能以成功告终*。
3. **类型化的情况。** `OllamaStreamError` 有五种情况——`.server(String)`、`.unreachable(String)`、`.incomplete`、`.empty`、`.thinkingOnly`——每种都带有一条面向用户的消息；`.incomplete` 甚至会告诉你部分文本已被保留（`ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:216-236`）。

这个设计是一道伤疤，而不是猜测。2026 年 9 月的设计与差距评审发现，*旧的*提供方忽略了 Ollama 的流内错误，并让 "truncated/empty streams … finish as success"——差距 G06，P0——而当时项目显示有 215 个 Core 测试通过、覆盖率 97.24%（`ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md:5, 51`）。测试验证的是已经构建出来的东西；而构建出来的东西是错的。修复不是更多的覆盖率——而是一个诚实的失败模型。反复出现的误解「为了避免界面闪烁而吞掉流错误」恰恰是本末倒置：用户得到的是一个悄无声息的不完整回答，而不是一个重试的入口。闪烁是信息；沉默是谎言。

**预算来自观察。** 自动的 Quick 评估以 `LLMRequest.Purpose.quickEvaluation` 运行，它强制设定 `think: false`、temperature 0，以及 3,072 个 token 的输出上限（`ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:62-63`）。为什么是 3,072？GLM 实时测试 "exposed planning text despite `think: false`, exhausting the former 1,600-token budget halfway through valid final JSON"——所以 Quick 现在允许生成 3,072 个 token、30 秒的截止时间，同时保留 16 KiB 的响应上限（`ListenToMe/docs/SHARED-LIVE-SUMMARY.md:102`）。这个数字不是理论推导；它是能阻止那次实际观察到的截断的最小预算。当你自己的上限在实时测试中被突破时，也要用同样的方式提高它们——依据证据。

**在预算之内自动化。** 共享实时摘要引擎——Core 中的 `LiveSummaryScheduler`、`QuickSummaryContext`、`AutomaticReviewCoordinator`，记录在 `docs/SHARED-LIVE-SUMMARY.md` 中——就是「主动」在生产环境中的样子：事件驱动，处处有界。

- 语音在评估前**按五秒一批**；一个非最终的假设需要**去除首尾空白后 24 个字符**才具备入选资格（`ListenToMe/docs/SHARED-LIVE-SUMMARY.md:8-10`；阈值是 `ConversationStore.provisionalMinimumCharacters`，`ListenToMe/Sources/ListenToMeCore/ConversationStore.swift:89-92`，在 `ListenToMe/Sources/ListenToMeCore/QuickSummaryContext.swift:65-66` 中应用）。
- **输入没有变化就不轮询**——"Timers exist only for queued work or a failed request"（`ListenToMe/Sources/ListenToMeCore/AutomaticReviewCoordinator.swift:59`）。
- 响应上限为 **30 秒 / 16 KiB**（`ListenToMe/docs/SHARED-LIVE-SUMMARY.md:31`）。
- 当一次 Quick 评估建议时，完整的 **Summary** 和 **Deep** 评审会**串行**运行——Summary 最多每 30 秒一次，Deep 每 60 秒一次；第一个符合条件的评审立即开始，而输入没有变化时，不能重新生成一个已完成的评审（`ListenToMe/Sources/ListenToMeCore/AutomaticReviewCoordinator.swift:107`；`ListenToMe/docs/SHARED-LIVE-SUMMARY.md:96`）。

这里的每个数字都是成本上限，而不是功能。这就是本节的要点：主动智能是 5% 的触发器——一个 28 行的启发式规则——加上 95% 的纪律：防抖、预算、上限、类型化的失败。

### 行动步骤

1. 打开 `Sources/ListenToMeCore/QuestionDetector.swift`，列出它的三条规则，并注明哪条规则要求线索出现在语句的*开头*。
2. 打开 `Sources/ListenToMeCore/OllamaProvider.swift`，找到让截断的流和空的流失败的两个布尔值。然后在证据日志中写下：一个流产出了 "The best ans"，然后在没有 `done` 的情况下结束——触发的是哪一个 `OllamaStreamError` 情况，用户看到的是什么？
3. 打开 `docs/SHARED-LIVE-SUMMARY.md`，找到解释 Quick 评估预算为什么是 3,072 个 token 的那句话。
4. 审视你自己的产品想法：写出它的主动触发器、防抖窗口和单次响应预算——三个数字，不要形容词。

## 回顾

- **M2.1** — 流水线是 采集 → 转写 → 存储/上下文 → 提示词 → 路由。平台胶水代码位于 `App/`；每一个决策都位于纯 Core 中，在 `AudioCapturing`、`Transcribing`、`LLMProvider` 之后。三个转写引擎在同一个接缝后面切换；`ConversationStore.recentContext` 强制执行一个字符预算（默认 4,000），并且总是至少保留最新的片段；当引擎无法分段时，一个 37 行的 VAD 负责切分语句。这种划分与平台无关：Apple、Windows 和 Android 各自都提供一套能填充同样接缝的端侧技术栈，而每个平台都把可用性检查、预算和错误消息留给你来做。
- **M2.2** — 三个角色（Listener/Quick/Deep）使用不同的模型：本地优先的 `roleDefaults`（快速→Quick，强力→Deep，另一个不同的快速→Listener），词首前缀匹配拒绝 "gemini ⊃ mini" 这类误命中，生成令牌在切换模型时取消过期的流。`PromptBuilder` 是纯的——不要开场白的 Quick、绝不编造的 Listener、深度优先于简洁的 Deep——外加贯穿每个面板的 9 个响应动作和人设指令。只有*已完成*的 Listener 摘要才能为 Quick/Deep 提供依据。模型调研放在一份带日期的附录里；`qwen3:0.6b` 仍然是实验的默认模型。
- **M2.3** — 主动 = 一个位于接缝之后、28 行的问题启发式规则，由针对已定稿 `.others` 片段的 8 秒防抖把关。流式错误是类型化的（`.server`/`.incomplete`/`.empty`），所以截断无法冒充成功——这是对差距 G06 的修复。各项预算（Quick 3,072 个 token、5 秒一批、24 个字符的入选门槛、30 秒/16 KiB 的上限、30 秒/60 秒的评审间隔）都来自观察到的失败，而不是猜测。

## 讨论题

把你的回答发到社区：一位利益相关者提议，你的助手「应该自己知道什么时候该帮忙——把最大的模型接上去，让它自己决定」。利用本模块的证据（至少引用三个 ListenToMe 文件），写一篇约 150 字的回复，说明：（a）触发器实际上会是什么，（b）你会在它周围加上什么样的防抖和预算，以及（c）你的设计能防止、而他们的设计防止不了的是哪一种失败模式。
