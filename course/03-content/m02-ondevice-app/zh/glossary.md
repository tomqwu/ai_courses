# 术语表 M2 — 端侧 AI 应用：架构

除非以 `ListenToMe/` 开头，指针都相对于克隆下来的仓库根目录；课程指针相对于课程根目录。

## 术语

- **:cloud 别名（:cloud alias）** — 一个由*本地*守护进程从远端后端提供服务的模型。它的名字以 `:cloud` 或 `-cloud` 结尾，或者 `/api/tags` 报告了 `remote_host`/`remote_model`。`ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:66-72`；`course/03-content/m02-ondevice-app/tinycopilot/src/tinycopilot/model_router.py`。
- **音频采集接缝（AudioCapturing）** — 采集这一层的协议接缝。Core 声明到达什么音频；`App/` 提供 `AVAudioEngine` 和 ScreenCaptureKit。`ListenToMe/Sources/ListenToMeCore/Capture.swift:4`。
- **上下文窗口（Context window (`recentContext`)）** — 按字符预算截取、发送给提示词的那一段转写文本。从最新的开始往回装，默认 4,000 个字符，永不为空。`ListenToMe/Sources/ListenToMeCore/ConversationStore.swift:76-87`。
- **Copilot 角色枚举（CopilotRole）** — 以枚举表示的三个 AI 角色：`listener`、`quick`、`deep`。路由、提示词和取消都以它为键。`ListenToMe/Sources/ListenToMeCore/CopilotRole.swift:5-7`。
- **防抖（Debounce）** — 两次主动触发之间的最短间隔。ListenToMe 的默认值是 8 秒。`ListenToMe/Sources/ListenToMeCore/ContextEngine.swift:8,41-50`。
- **生成令牌（Generation token）** — 一个按角色的计数器，用来使进行中的流失效。切换模型，令牌加一，旧流的增量就不再被写入。`ListenToMe/Sources/ListenToMeCore/MeetingSession.swift:204-221,803-880`。
- **模型提供方接缝（LLMProvider）** — 提供方这一层的协议接缝。Core 通过它流式获取文本；`OllamaProvider` 通过 HTTP 实现它，`AppleIntelligenceProvider` 在设备上实现它。`ListenToMe/Sources/ListenToMeCore/LLMProvider.swift:13`。
- **本地优先的默认值（Local-first defaults）** — 自动选择时先把云端别名过滤掉。只有在不存在任何本地模型时，才选择云端模型。`ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:80-95`。
- **逐行 JSON 格式（NDJSON）** — 以换行分隔的 JSON，Ollama 的流式格式。每行一个 JSON 对象，携带一段增量或 `done: true`。`ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:3-34`。
- **临时结果与最终结果（Partial vs. final）** — 进行中的实时文本，与已定稿的语句。临时结果从不进入已定稿日志；id 相同的最终结果会取代它的临时结果。`course/03-content/m02-ondevice-app/tinycopilot/src/tinycopilot/conversation_store.py`。
- **人设指令（Persona directive）** — 附加到每个角色系统提示词后面的预设指导。手动面板和自动评审走同一条代码路径。`ListenToMe/Sources/ListenToMeCore/Prompt.swift:245-260`。
- **主动触发关卡（Proactive gate）** — 主动回答触发之前的四个条件。已定稿、来自 `.others`、通过问题检测、在防抖窗口之外。`ListenToMe/Sources/ListenToMeCore/ContextEngine.swift:41-50`。
- **提示词构建层（PromptBuilder）** — 纯函数式的提示词构造层。一个由静态函数组成的公开枚举：上下文进，请求出，没有 I/O。`ListenToMe/Sources/ListenToMeCore/Prompt.swift`。
- **协议接缝（Protocol seam）** — 由纯核心声明、由平台胶水代码实现的协议。三个接缝是 `AudioCapturing`、`Transcribing`、`LLMProvider`；正是它们让测试无需硬件就能运行。
- **词首前缀匹配（Token-prefix matching）** — 能力标记只在词首匹配，绝不作为子串匹配。它防止 `gemini` 被当作 `mini` 降级。`ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:13-18`。
- **类型化流错误（Typed stream errors (`OllamaStreamError`)）** — 流式调用的失败模型。流内错误事件对应 `.server`，`done` 始终没有到达对应 `.incomplete`，没有任何可见文本到达对应 `.empty`；`.unreachable` 和 `.thinkingOnly` 分别覆盖服务器无响应和只有推理的回复。`ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:79-104,216-236`。
- **语音活动检测（VAD）** — 找出语句边界的语音活动检测。37 行：RMS 能量、0.02 的阈值、0.8 秒的尾部静音。`ListenToMe/Sources/ListenToMeCore/VAD.swift`。
- **已验证本地（Verified local）** — 一种失败即关闭的元数据检查，而不是主机名检查。除非 `remote_host` 和 `remote_model` 都不存在，否则 `isVerifiedLocal` 会拒绝该模型。`ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:17-24`。

## 容易弄错的术语

- **本地与已验证本地（Local vs. verified local）** — 一个 `localhost` URL 证明不了什么——本地守护进程也可以提供由云端支撑的别名；只有 `/api/show` 元数据检查（M3）才能证明本地性。
- **覆盖率与正确性（Coverage vs. correctness）** — 旧的提供方拥有 97.24% 的覆盖率，*同时*让截断的流以成功告终（`ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md`，差距 G06）。测试验证的是已经构建出来的东西，而不是它是否正确。
- **防抖与「等安静下来」（Debounce vs. "wait for quiet."）** 这里的防抖不会一直等到局面平静下来；它在*一次触发之后*的 8 秒内阻止再次触发，所以一连串提问只会产生恰好一个回答。
- **临时结果与最终结果（Partial vs. final）** — 临时结果是会被替换的显示状态；把它当作对话历史，正是存储的双容器设计所要防止的缺陷。
- **词首前缀与子串（Token-prefix vs. substring）** — `"gemini"` 包含 `"mini"`，但并不是以它作为某个词的开头；子串匹配会把整个模型家族路由错。

## 精选资源

- `ListenToMe/docs/superpowers/specs/2026-06-18-listentome-design.md` §3–§4.4 — 已批准的架构，以及问题检测「有意保持简单，以后可以替换」的理由。
- `ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md` — 差距 G06；仓库中最清楚地说明「诚实的失败模型胜过更多覆盖率」的一课。
- `ListenToMe/docs/SHARED-LIVE-SUMMARY.md` — 每一项主动触发预算（5 秒一批、24 个字符的入选门槛、3,072 个 token、30 秒/16 KiB 的上限），以及确定它们的那次观察。
- `ListenToMe/Sources/ListenToMeCore/ConversationStore.swift` — 反复阅读 `recentContext`，直到「永不为空」的保证一目了然；实验会重新实现它。
- `course/03-content/m02-ondevice-app/tinycopilot/tests/test_model_router.py` — 词首前缀匹配和本地优先默认值的可执行规格，包括 `gemini` 这个反例。
- `course/03-content/m02-ondevice-app/tinycopilot/tests/test_ollama_provider.py` — 失败流的规格；在编写提供方之前先读它。
- `ListenToMe/Sources/ListenToMeCore/VAD.swift` — 37 行代码，展示了在需要模型之前，一个阈值和一个计时器能走多远。
