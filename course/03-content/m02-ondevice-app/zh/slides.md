---
marp: true
theme: aps
paginate: true
title: M2 — 端侧 AI 应用：架构
---

<!-- _class: lead -->

# M2 — 端侧 AI 应用：架构

**承诺：** 追踪一条真实的端侧流水线，然后重建它的核心。 **时长：** 约 75 分钟讲授 + 约 3 小时实验。

```figure
kind: architecture
alt: ListenToMe 已发布的 Swift 流水线逐个阶段展开，以及实验中用 Python 重建为 TinyCopilot 的同样六个阶段。
source: ListenToMe/Sources/ListenToMeCore/MeetingSession.swift
layer: ListenToMe — 已发布的 macOS 会议助手，Swift (chain) @ 我们打开 ListenToMe
  box: 采集
  box: 转写
  box: 存储
  box: 上下文
  box: 提示词
  box: 路由
layer: TinyCopilot — 你用 Python 重建的版本 (chain) (hl) @ 然后在实验中
  box: 采集
  box: 转写
  box: 存储
  box: 上下文
  box: 提示词
  box: 路由
```

<!-- NOTES: 欢迎来到第 2 模块。今天抽象到此为止：我们打开 ListenToMe——一个已经发布的 macOS 会议助手——阅读它实际运行的流水线。然后在实验中，你用 Python 把这个核心重建为 TinyCopilot，直到 208 个测试全部通过。学完本模块，你能为每个阶段指出对应的 Swift 文件，并为每一个决策给出理由。（45 秒；转到学习目标。） -->

---

## 学完本模块，你能够……

- 画出 采集 → 转写 → 上下文 → 提示词 → 路由。
- 说出实现每个阶段的文件。
- 为三个协议接缝给出理由。
- 按角色路由模型，取消过期的流。
- 把提示词构建器写成纯函数。
- 为流式错误定义类型，让截断大声失败。

<!-- NOTES: 这六条要点就是本模块的全部约定。注意这里没有什么：没有提到提示词工程技巧，也没有模型基准测试。本模块讲的是架构——决策放在哪里、又如何被证明。每个目标都对应一个实验步骤和至少一道测验题。如果你能做到这六件事，今天就能通过实验 M2。（60 秒；然后进入 M2.1。） -->

---

## M2.1 — 一条流水线，两层结构

```figure
kind: system
alt: 作为一个系统的 ListenToMe。来自 App 层、带标记的音频穿过 AudioCapturing 和 Transcribing 两个接缝，进入纯核心——存储、上下文、提示词、路由器——核心只通过 LLMProvider 接缝访问模型，并把回答以流式送回各个面板。
source: ListenToMe/Sources/ListenToMeCore/MeetingSession.swift · ListenToMe/Sources/ListenToMeCore/Capture.swift:4 · ListenToMe/Sources/ListenToMeCore/Transcriber.swift:4 · ListenToMe/Sources/ListenToMeCore/LLMProvider.swift:13
layer: App/ — 接触硬件 @ 关键在于这条分界
  node mic: 麦克风 — 标记为 .you @ 麦克风音频标记为
  node sys: 系统音频 — 标记为 .others @ 麦克风音频标记为
  node panes: Listener · Quick · Deep 面板
layer: 接缝 — 由核心拥有的协议 (seam) @ 三个接缝分别是
  node cap: AudioCapturing (seam)
  node stt: Transcribing (seam)
  node llm: LLMProvider (seam)
layer: ListenToMeCore — 纯的，可针对模拟对象运行 (hl) @ 正是这种分层
  node store: 存储
  node ctx: 上下文
  node prompt: 提示词
  node route: 路由
edge: mic -> cap — PCM 数据块 @ 麦克风音频标记为
edge: sys -> cap — PCM 数据块 @ 麦克风音频标记为
edge: cap -> stt — 采集 @ 接着流水线依次运行
edge: stt -> store — 转写 @ 接着流水线依次运行
edge: store -> ctx @ 接着流水线依次运行
edge: ctx -> prompt @ 接着流水线依次运行
edge: prompt -> route @ 接着流水线依次运行
edge: route -> llm — 按角色 @ 接着流水线依次运行
edge: llm -> panes — 流式回答 @ 接着流水线依次运行
```

<!-- NOTES: 先从左到右读一遍，然后把这条分界大声说出来：`App/` 里的一切都接触硬件；`Sources/ListenToMeCore` 里的一切都是纯的。三个接缝是 `AudioCapturing`、`Transcribing` 和 `LLMProvider`。这之所以重要，是因为可测试性：整条流水线可以在单元测试中针对模拟对象完整运行。记住这张图；接下来我们逐层走一遍。（75 秒；下一张讲采集。） -->

---

## 采集层有意做薄

```swift
/// Captures the local microphone (source `.you`) and system audio (source `.others`),
/// converting both to mono Float PCM and emitting `AudioChunk`s.
final class DualChannelCapture: NSObject, AudioCapturing, @unchecked Sendable {
```

- 说话人归属零成本——无需说话人分离模型。
- 最难测试的代码，所以做得最薄。

`ListenToMe/App/DualChannelCapture.swift:8-10`

<!-- NOTES: `ListenToMe/App/DualChannelCapture.swift:8-9` 处的头部注释说明，两个来源都被转换成单声道 Float PCM，并以音频块的形式发出。麦克风的 tap 在 `ListenToMe/App/DualChannelCapture.swift:143` 把缓冲区标记为 `.you`；ScreenCaptureKit 的回调在 `ListenToMe/App/DualChannelCapture.swift:324` 把缓冲区标记为 `.others`。正是这一个标记，让应用不需要任何说话人分离就能标注 "You" 和 "Others"。采集受硬件约束，所以要尽可能做小——这条规则我们会在实验中再次用到。（70 秒；转到接缝。） -->

---

## 三个协议接缝

| 接缝 | 核心声明 | 应用提供 |
|---|---|---|
| `AudioCapturing` | 到达什么音频 | AVAudioEngine、ScreenCaptureKit |
| `Transcribing` | 临时结果与最终结果 | SpeechAnalyzer、WhisperKit |
| `LLMProvider` | 流式文本 | Ollama 客户端（在 Core 中）、Apple Intelligence |

```swift
public protocol AudioCapturing: Sendable {
    var statusUpdates: AsyncStream<CaptureStatus> { get }
    var chunks: AsyncStream<AudioChunk> { get }
    func start() async throws
    func stop()
}
```

`ListenToMe/Sources/ListenToMeCore/Capture.swift:4-9` · `LLMProvider.swift:13-22`

<!-- NOTES: 接缝是由纯核心拥有、由平台侧实现的协议。Core 从不提及 AVFoundation 或 Ollama；它只提及这三个协议。正是这种反转让测试套件能够注入模拟对象。回报是：如果明天我们加第四个转写引擎，`Transcribing` 协议之下的任何东西都不用改——存储不用改，提示词不用改，路由器也不用改。（75 秒；接下来看转写接缝内部。） -->

---

## 三个引擎，一个接缝

| 引擎 | 状态 | 取舍 |
|---|---|---|
| SpeechAnalyzer | 默认 | 每个来源一个分析器 |
| SpeechRecognizer | 旧版 | 进程级全局限制 |
| WhisperKit | 需主动开启 | 批处理，只输出已定稿片段 |

- Apple Speech 只选一种语言；不支持语码转换。
- 加一个引擎；下游什么都不用改。

`ListenToMe/Sources/ListenToMeCore/Transcriber.swift`

<!-- NOTES: `Sources/ListenToMeCore/Transcriber.swift` 定义了 `prepare()`、`feed(_:)`、`finish()`。`prepare()` 的约定很重要：在音频到来之前完成预热，这样 `feed` 永远不会阻塞，会议开头的几秒也不会丢失。`App/SpeechAnalyzerTranscriber.swift:6-39` 注明每个来源一个分析器，这一点与 `SFSpeechRecognizer` 不同。WhisperKit 用实时的临时结果换取更强的多语言质量——原因见 `ListenToMe/App/MeetingView.swift:106-107`：Apple 的端侧 Speech 只选一种主要语言。（80 秒；接下来讲存储。） -->

---

## 存储及其预算

- `ConversationStore.swift` 是唯一的事实来源。
- 最终结果日志，外加每个来源一条临时结果。
- `recentContext(maxChars:)` 从最新的开始往回走。
- 总是保留最新的一条，即使超出预算。
- 回顾和行动项的预算是 100,000。

```swift
public func buildContext(from store: ConversationStore, notes: String?,
        maxChars: Int = 4000, summary: String? = nil,
        responseLanguage: String? = nil, references: String? = nil,
        personaGuidance: String? = nil) -> PromptContext
```

`ListenToMe/Sources/ListenToMeCore/ContextEngine.swift:12-14`

<!-- NOTES: `apply(_:)` 追加最终结果，替换临时结果。窗口函数从最新的语句开始往回走，放得下就保留，并且总是包含最近的那一条，即使它单独就超出预算——窗口永远不会为空（`ListenToMe/Sources/ListenToMeCore/ConversationStore.swift:76-87`）。默认值是 4,000 个字符（`ContextEngine.swift:12`），但 `MeetingSession.transcriptBudget(for:)` 把回顾和行动项提示词提高到 100,000，因为它们必须覆盖整场对话（`ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:582-587`）。（85 秒；简单讲一下分段。） -->

---

## 当引擎不提供临时结果时

- 核心 VAD 只有 37 行；默认值 0.02、0.8 秒。

```swift
if value >= speechThreshold {
    inSpeech = true
    lastSpeechTime = time
    return false
}
if inSpeech && (time - lastSpeechTime) >= silenceDuration {
    inSpeech = false
    return true
}
```

`ListenToMe/Sources/ListenToMeCore/VAD.swift:26-34`

<!-- NOTES: WhisperKit 会缓冲音频，所以必须有某个东西来决定一句话在哪里结束。`Sources/ListenToMeCore/VAD.swift` 逐帧计算均方根能量，并且只返回一次 true：就在语音之后的尾部静音首次超过静音时长的那一帧上。由 `Tests/ListenToMeCoreTests/VADTests.swift` 验证。这是本模块反复出现的做法：在用模型会大材小用的地方，就用廉价的启发式规则。（70 秒；该上证明幻灯片了。） -->

---

<!-- _class: proof -->

## 最新的片段总能留下

- 保证：上下文永不为空。
- 回报：核心覆盖率 96%，底线 95%。

```swift hl=82
for segment in utterances.reversed() {
    let cost = TranscriptSegment.promptCharacterCost(segment)
    // Always include the most recent; otherwise stop before …
    if !collected.isEmpty && total + cost > maxChars { break }
    total += cost
    collected.append(segment)
}
```

`ListenToMe/Sources/ListenToMeCore/ConversationStore.swift:79-85`

<!-- NOTES: 这是第一张证明幻灯片。打开文件，把循环大声读出来，而不是轻信这些要点。在本课程中，证明幻灯片的意义在于：每一个论断都有一个你能打开的文件指针，而且这个指针能解析。96% 的覆盖率徽章，以及 `scripts/check-coverage.sh` 中 95% 的底线，都是这种分层带来的下游结果。（70 秒；过渡到路由。） -->

---

## M2.2 — 三个角色，三个模型

```figure
kind: screenshot
alt: ListenToMe 的窗口。转写文本占据左侧；右侧的 Listener、Quick 和 Deep 三个面板各自带有模型下拉菜单。
source: ListenToMe/Sources/ListenToMeCore/CopilotRole.swift
image: listentome-app.png
frame: none
callout: 25,19 — Transcript（转写）
callout: 53,11 — Listener：滚动摘要 · 要速度
callout: 53,41 — Quick：快捷键、主动触发 · 要速度
callout: 53,72 — Deep：长推理 · 要强度
callout: 91,11 — 每个面板都有自己的模型下拉菜单
```

<!-- NOTES: 角色是一个枚举——`Sources/ListenToMeCore/CopilotRole.swift` 中的 `listener`、`quick`、`deep`——而不是界面上的偶然产物。Quick 通过全局快捷键作答，还会主动触发，所以延迟就是一切。Deep 是按需的长推理。Listener 持续自动刷新，所以速度胜过深度。「处处都用最好的模型」会失败两次：它在不需要的地方浪费延迟，还把产品绑死在某一个模型的怪癖上。（75 秒；接下来讲默认值。） -->

---

## 本地优先的角色默认值

`ModelRanking.roleDefaults(from:local:)` 自动挑选。

| 角色 | 精选标记 | 否则 |
|---|---|---|
| Quick | flash, mini, nano, lite, small, fast | 最轻的 |
| Deep | pro, reason, think, coder, code, ultra, max, large | 最重的 |
| Listener | 第二个快速标记，不同于 Quick 的 | 剩下最轻的 |

- `:cloud` 被排除在自动选择之外。
- 只有没有本地模型时才用云端。

`ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:49-54`

<!-- NOTES: 逻辑在 `ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:91-111`，由 `ListenToMe/App/MeetingView.swift:845` 调用。快速标记包括 flash、mini、nano、lite、small、fast；强力标记包括 pro、reason、think、coder、code、ultra、max、large。本地优先过滤（`ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:80-95`）是隐私默认值，而不是速度默认值：一个没有固定模型的面板，绝不能悄悄把转写文本发送到 Ollama Cloud。"good for" 提示来自 `describe(_:)` 及其表格（`ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:119-159`）。（80 秒；现在讲那个隐蔽的缺陷。） -->

---

## 词首前缀，而不是子串

- `"gemini-2.5-flash"` 包含 `"mini"`。
- 词首检查拒绝它；子串检查接受它。
- 一个错误的检查会把整个家族路由错。

```swift
static func tokens(_ model: String) -> [String] {
    model.lowercased().split(whereSeparator: { "-:./ ".contains($0) })
        .map(String.init)
}
static func hasMarker(_ model: String, _ marker: String) -> Bool {
    tokens(model).contains { $0.hasPrefix(marker) }
}
```

`ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:7-18`

<!-- NOTES: `ModelRanking.swift:13-18` 把这一点写进了文档：词首前缀匹配而不是原始子串匹配，能拒绝跨词的误命中，比如 gemini 包含 mini。一个原始的 `contains("mini")` 会把每个 Gemini 模型都排为快速模型，你的 Quick 默认值会对整个模型家族悄悄出错——除非你写了近似反例测试，否则没有任何测试会失败。TinyCopilot 的 `test_gemini_is_not_demoted_as_mini` 正是这个测试。（70 秒；接下来讲取消。） -->

---

## 生成令牌终结过期的流

- `MeetingSession` 为每个角色保留一个生成计数器。
- `setModel(_:_)` 取消进行中的工作，并把计数器加一。
- 流式循环守护每一次写入。
- 回答中途切换：旧 token 直接作废。
- 没有它，昨天的模型会顶着今天的名字作答。

<!-- NOTES: `ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:204-221` 是 `setModel` 调用 `cancelResponse`、由后者把计数器加一的地方；`ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:803-880` 是每个流领取一个生成编号、循环在每次写入前检查它的地方。它防止的失败隐蔽而又尴尬：旧模型的一个慢回答在切换之后才完成，并显示在新模型的名下。用户会以为是新模型答错了。取消是一项正确性功能，而不是一种优化。（75 秒；接下来讲提示词。） -->

---

## PromptBuilder 是纯的

- `Prompt.swift` — 一个公开枚举，静态函数。
- 零 I/O，零状态，零时钟。
- 上下文进，`LLMRequest` 出。
- 相同输入，相同字符串，永远如此。
- 测试断言构建出的文本；不需要模型。

<!-- NOTES: 在这里，纯粹性不是风格偏好。`Tests/ListenToMeCoreTests/PromptBuilderTests.swift` 直接检查构建出的字符串，所以提示词回归能在几毫秒内被抓住，不需要网络调用，也不需要模型。这是让三个角色上的九个响应动作保持诚实的唯一方法。当你编写 TinyCopilot 的 `prompts.py` 时，任何隐藏状态或随机性都会让 `test_prompts.py` 中的确定性测试失败。（70 秒；接下来是三个基础提示词。） -->

---

## 三个基础提示词，三份约定

| 基础提示词 | 它的约定 |
|---|---|
| Quick | 不要开场白，用 1–3 句话作答 |
| Listener | 绝不编造负责人、截止日期、共识、完成状态 |
| Deep | 深度优先于简洁；相关时给出代码 |

- 九个响应动作叠加在上面。
- 人设指令追加到每个角色。

`ListenToMe/Sources/ListenToMeCore/Prompt.swift`

<!-- NOTES: 读一读 `Prompt.swift` 里的原句：Quick 在 `ListenToMe/Sources/ListenToMeCore/Prompt.swift:129-135`，Listener 在 `ListenToMe/Sources/ListenToMeCore/Prompt.swift:137-145`，Deep 在 `ListenToMe/Sources/ListenToMeCore/Prompt.swift:147-152`。Listener 约定之所以存在，是因为它的摘要会回流到 Quick 和 Deep 的提示词中——一个幻觉出来的负责人就会扩散到所有地方，所以要在源头把它挡住。`ListenToMe/Sources/ListenToMeCore/Prompt.swift:245-260` 处的 `systemWithDirectives` 把人设和语言追加到每个面板，所以像 Interview 这样的预设会以完全相同的方式塑造全部三个角色。（80 秒；证明幻灯片。） -->

---

<!-- _class: proof -->

## 只有已完成的摘要才能为其他角色提供依据

- `ListenToMe/Sources/ListenToMeCore/Prompt.swift:137-145` — 绝不编造约定。
- `ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:53, 81-84` — 两个摘要字段。
- `lastCompletedListenerSummary` — 会被注入，安全。
- 进行中的 `listenerSummary` — 只用于显示，从不注入。
- 半个答案比没有答案更糟。

<!-- NOTES: 打开 `ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:53, 81-84`，注意这里有两个属性，而不是一个。实时显示的值在刷新以流式进行时会被清空；完成值是单独的，`clampedContext` 为 Quick 和 Deep 两个提示词读取的正是它（`ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:601-605, 640-653`）。这里要破除的误解是「上下文越多越好，屏幕上有什么就注入什么」。一份进行中的摘要是看起来很自信的半个答案，而 Quick 会把它当作事实。（75 秒；M2.3。） -->

---

## M2.3 — 主动即克制

```figure
kind: flow
alt: 一条已定稿的转写语句先经过一个 28 行的问题启发式规则，再经过防抖，Quick 才会作答——触发器很小，围绕它的关卡才是真正的工作。
source: ListenToMe/Sources/ListenToMeCore/QuestionDetector.swift · ListenToMe/Sources/ListenToMeCore/ContextEngine.swift:41-50
step: 一条来自 others 的已定稿语句
step: 问题启发式规则 (seam) — 28 行，可替换 @ 问题检测只有二十八行
step: 防抖 — 每隔几秒最多一次 @ 设计规格要求
step: Quick 作答 (hl)
```

- 把廉价的启发式规则放在接缝后面上线；把复杂度花在别处。
- 触发器占 5%；纪律占 95%。

<!-- NOTES: 「主动」听起来需要智能；它需要的是克制。`Sources/ListenToMeCore/QuestionDetector.swift` 只有 28 行。`docs/superpowers/specs/2026-06-18-listentome-design.md` §4.4 中的设计规格说，问题检测是一个轻量的启发式规则，加了防抖，每 N 秒最多触发一次，有意保持简单，以后可以替换。要学的是：把触发器做成一个接缝，把精力放在它周围的关卡上。（75 秒；三条规则。） -->

---

## QuestionDetector：三条规则

```swift
if normalized.hasSuffix("?") { return true }
for cue in leadingCues where normalized == cue || normalized.hasPrefix(cue + " ") {
    return true
}
return phraseCues.contains { cue in
    let pattern = "\\b" + NSRegularExpression.escapedPattern(for: cue) + "\\b"
    return normalized.range(of: pattern, options: .regularExpression) != nil
}
```

- 线索：`"can you"`、`"any thoughts"`、`"walk me through"`。
- 近似反例不能触发："however"、"whatsapp"。

`ListenToMe/Sources/ListenToMeCore/QuestionDetector.swift:19-26`

<!-- NOTES: 「开头」这个词至关重要：疑问词规则只作用于第一个词。短语线索按词边界匹配，所以 "many thoughts" 永远不会触发 "any thoughts"，"we cannot use your laptop" 也永远不会触发 "can you"。这些近似反例是学员最常忘记写的测试。在 TinyCopilot 中，`test_question_detector.py` 已经为你准备好了——八个明确的近似反例字符串。（70 秒；关卡。） -->

---

## 关卡：已定稿、来自 others、已防抖

- 片段必须**已定稿**。
- 必须来自 `.others`。
- 必须通过检测。
- 距上次触发至少 8 秒。
- 一次触发，一个回答，然后安静。

<!-- NOTES: `ListenToMe/Sources/ListenToMeCore/ContextEngine.swift:41-50` 处的 `ContextEngine.shouldFireProactive(for:now:)` 就是全部四个条件，8 秒的防抖默认值在 `ListenToMe/Sources/ListenToMeCore/ContextEngine.swift:8`。`.others` 是人们最容易漏掉的条件：你不希望应用去回答你自己的反问。没有防抖，两分钟激烈的连续提问就会让面板被重叠的建议淹没。（70 秒；接下来讲失败。） -->

---

## 类型化的流式错误

- Ollama 可能先发 HTTP 200，再发 `{"error": ...}`。
- `.incomplete` — 各行结束时没有 `done: true`。
- 截断永远不能以成功告终。

```swift
public enum OllamaStreamError: LocalizedError {
    case server(String)
    case unreachable(String)
    case incomplete
    case empty
    case thinkingOnly
    …
```

`ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:216-224`

<!-- NOTES: `ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:42-50` 是产出原始 NDJSON 行的行来源；它可以注入，这样测试就能喂入预先准备的行。循环在 `ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:79-104` 跟踪 `completed` 和 `producedContent`。五个类型化的情况位于 `ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:216-236`，每个都带有一条面向用户的消息：`.server`、`.incomplete` 和 `.empty`，外加表示服务器从未应答的 `.unreachable`，以及表示模型推理了却始终没有作答的 `.thinkingOnly`。这个设计是一道伤疤，而不是猜测：2026 年 9 月的评审发现，旧的提供方让截断的流以成功告终——差距 G06，P0——而当时项目显示有 215 个核心测试通过、覆盖率 97.24%。（85 秒；证明幻灯片。） -->

---

<!-- _class: proof -->

## 闪烁是信息；沉默是谎言

- `ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:79-104`
- 两个标志决定成功与否：完成与内容。
- `ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md` — 差距 G06。
- 旧的提供方：截断的流以成功告终。
- 测试通过了；失败模型是错的。

<!-- NOTES: 打开那份评审，读一读差距 G06。测试套件验证的是已经构建出来的东西；而构建出来的东西是错的。修复不是更多的覆盖率，而是一个诚实的失败模型。反复出现的误解——「为了避免界面闪烁而吞掉流错误」——恰恰是本末倒置：用户得到的是一个悄无声息的不完整回答，而不是一个重试的入口。把幻灯片上这句话大声说出来：闪烁是信息，沉默是谎言。（75 秒；预算。） -->

---

## 预算来自观察

| 预算 | 取值 |
|---|---|
| Quick 评估 | `think: false`，temperature 0 |
| 输出上限 | 3,072 个 token — 来自一次真实的截断 |
| 语音批次 | 5 秒；24 个字符的入选门槛 |
| 响应上限 | 30 秒 / 16 KiB |
| 评审间隔 | Summary 30 秒，Deep 60 秒，串行 |

- 每个数字都是成本上限，而不是功能。

`ListenToMe/docs/SHARED-LIVE-SUMMARY.md`

<!-- NOTES: `ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:62-63` 为 Quick 评估强制设定 `think: false`、temperature 0，以及 3,072 个 token 的上限。为什么是 3,072？`ListenToMe/docs/SHARED-LIVE-SUMMARY.md:102` 记录了：GLM 实时测试中，即使设置了 `think: false`，规划文本仍然暴露出来，在有效 JSON 写到一半时就耗尽了之前 1,600 个 token 的预算。这个上限是能阻止那次实际观察到的截断的最小预算。共享实时摘要引擎也记录在同一个文件里：批次、入选门槛、上限、串行评审。（85 秒；实验。） -->

---

## 实验 M2 — 构建 TinyCopilot 的核心

- 删除六个 Python 模块；以 TDD 方式重新实现。
- 测试就是规格；参考实现就是参考答案。

| 命令 | 预期 |
|---|---|
| `make lab-m2` | 208 passed，覆盖率 100%；底线 90 |
| `make lab-m3` | 56 passed |
| `make demo` | 来自真实模型的三个角色输出 |

指南：`course/03-content/m02-ondevice-app/lab.md`

<!-- NOTES: 三个小时。六个模块：conversation_store、question_detector、prompts、model_router、ollama_provider、copilot。先把整套测试跑绿，阅读 `copilot.py`，然后一次删除一个模块。删除后会出现收集错误——那才是真正的红色运行——然后阅读测试文件，获取逐个测试的规格。没有记录红色运行之前，不要进入绿色运行。验收清单在 `lab.md` 中。（75 秒；接下来是测验。） -->

---

## 测验 M2 — 八道题

- 流水线顺序；让覆盖率成为可能的因素。
- 三个已安装模型下的角色默认值。
- 生成计数器；提示词纯粹性。
- 绝不编造约定。
- 流式错误的各种情况；防抖条件。
- 简答题要求运用，而不是回忆。

<!-- NOTES: 六道选择题，两道简答题。干扰项编码了我们要破除的误解：「最强的模型处处最好」、「localhost 就证明是本地」、「把旧流的 token 排队保留」。参考答案引用了确切的文件指针和目标。请在工作坊之前完成测验；我们会现场讲评错得最多的两道题。（45 秒；回顾。） -->

---

## 回顾

- **M2.1** 一条流水线；纯核心，薄胶水层，三个接缝。
- **M2.2** 按角色选模型；词首前缀；生成计数器负责取消。
- **M2.3** 廉价的启发式规则，严格的关卡，类型化的错误。
- 每个阶段都有一个你能打开的文件指针。
- 每个数字都是测量出来的上限。

<!-- NOTES: 三节内容，三句话。M2.1：决策放在纯 Core 里，硬件放在薄胶水层里。M2.2：路由按角色进行，匹配按词首前缀进行，取消靠生成计数器。M2.3：主动触发是一个 28 行的启发式规则，外加 8 秒防抖；流式失败是类型化的，所以截断永远不算成功。如果你只记住一件事，就记住：是架构让诚实成为可能。（55 秒；讨论。） -->

---

## 讨论题

- 利益相关者：「把最大的模型接上去。」
- 说出触发器、防抖、预算。
- 至少引用三个 ListenToMe 文件。
- 约 150 字；发到社区。
- 你的设计防止了哪一种失败模式？

<!-- NOTES: 这是本周的社区帖子，也是推动完成度的抓手。好的回答要说出一个具体的触发器（已定稿的 `.others` 问题）、一个明确的防抖（8 秒，或一个有理由的替代值）、一个单次响应预算，以及利益相关者的设计会丢掉的一种失败模式——例如，没有防抖就会出现重叠的建议，没有类型化错误就会出现悄无声息的截断。要求至少三个文件指针；我们就按这个评分。（50 秒；结束。） -->
