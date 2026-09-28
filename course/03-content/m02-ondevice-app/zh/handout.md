# 讲义 M2 — 端侧 AI 应用：架构

**一句话心智模型：** 把每一个决策都放进位于协议接缝（protocol seam）之后的纯核心，平台层只留下硬件胶水代码，然后用不需要麦克风、不需要屏幕采集、也不需要模型的测试来证明这些决策。

## 流水线，以及每个阶段在哪里

```
mic (.you) · system audio (.others)
      │ PCM chunks
      ▼
capture ─▶ transcribe ─▶ store/context ─▶ prompt ─▶ route ─▶ streamed deltas
 App/       Transcribing   ConversationStore  PromptBuilder  MeetingSession
            seam           (Core, pure)       (Core, pure)   (Core, pure)
```

| 阶段 | ListenToMe 文件 | TinyCopilot 模块 |
|---|---|---|
| 采集（胶水） | `App/DualChannelCapture.swift` | （预先准备的转写文本） |
| 转写接缝 | `Sources/ListenToMeCore/Transcriber.swift` | `conversation_store.py` 的输入 |
| 存储 + 窗口 | `Sources/ListenToMeCore/ConversationStore.swift` | `conversation_store.py` |
| 主动触发关卡 | `Sources/ListenToMeCore/QuestionDetector.swift` | `question_detector.py` |
| 提示词（纯） | `Sources/ListenToMeCore/Prompt.swift` | `prompts.py` |
| 排序 / 路由 | `Sources/ListenToMeCore/ModelRanking.swift` | `model_router.py` |
| 流式错误 | `Sources/ListenToMeCore/OllamaProvider.swift` | `ollama_provider.py` |
| 编排 | `Sources/ListenToMeCore/MeetingSession.swift` | `copilot.py` |

## 值得记住的决策表

| 决策 | 规则 | 如果你弄错了 |
|---|---|---|
| 上下文窗口 | 从最新的开始往回装；总是 ≥1 个片段 | 上下文为空或陈旧 |
| 问题线索 | 词首前缀 / 词边界，绝不用子串 | `gemini` 被误读为 `mini` |
| 默认模型 | 本地优先；只有没有本地模型时才用 `:cloud` | 转写文本悄悄离开 Mac |
| 切换模型 | 生成计数器加一；守护每一次写入 | 过期的回答显示在新模型的名下 |
| Listener 依据 | 只用*已完成*的摘要 | 半个答案被当作事实 |
| 流结束 | 要求 `done` **并且**有可见文本 | 截断以成功告终 |
| 平台模型 | 多一个 `LLMProvider`；检查可用性，逐个角色测量 | 一个没通过其角色测试的模型照样发布 |

## 留好这些命令

```bash
cd course/03-content/m02-ondevice-app/tinycopilot
make lab-m2     # unit suite + coverage floor 90  → 208 passed, 100%
make lab-m3     # M3 privacy suite must stay green → 56 passed
make e2e        # real-LLM contract test (needs LAB_E2E=1)
make demo       # scripted meeting, three role outputs
pytest tests/test_model_router.py -q   # 40 passed
pytest tests/ -m "not e2e" --collect-only -q | tail -1
```

## 要打开的文件

- `ListenToMe/Sources/ListenToMeCore/ConversationStore.swift:76-87` — 永不为空的窗口。
- `ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:13-18, 80-95` — 词首前缀，本地优先。
- `ListenToMe/Sources/ListenToMeCore/Prompt.swift:129-152` — 三个基础提示词。
- `ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:79-104, 216-236` — 类型化错误。
- `ListenToMe/Sources/ListenToMeCore/ContextEngine.swift:41-50` — 主动触发关卡。
- `ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md` — 差距 G06，那道伤疤。
- `tinycopilot/tests/test_ollama_provider.py` — 失败流的规格。
- `ListenToMe/SharedPlatform/AppleIntelligenceProvider.swift:17-25` — 同一个接缝之后的平台模型。
- `course/03-content/m02-ondevice-app/appendix-models-2026-09.md` — 带日期的模型对照表；实验的默认模型仍是 `qwen3:0.6b`。

## 三个坑

1. **删除一个模块得到的是 ImportError，而不是失败的测试。** `__init__.py` 重新导出了所有模块，所以 `make lab-m2` 以退出码 4 结束，一个测试也没运行。这就是红色运行；逐个测试的规格在测试文件里。
2. **`gemini` 包含 `mini`。** 任何基于子串的标记检查都会把整个模型家族路由错。要在词首匹配。
3. **实验的文字说明说 Listener 会得到一个不同的快速模型；测试却不是这样。** 按测试来实现——Listener 和 Quick 都得到最快的那个模型。

## 满足以下条件，你就完成了……

- [ ] `make lab-m2` 以 0 退出，208 passed，并达到 90 的覆盖率底线。
- [ ] 你的证据日志中有六次红色运行（ImportError，退出码 4），每一次都在对应的绿色运行之前。
- [ ] `make lab-m3` 仍然打印 56 passed。
- [ ] `make demo` 打印出 Listener、Quick 和 Deep 的输出，并且模型名可见。
- [ ] 你的日志用一两句话解释了每个模块从红到绿的过程。
- [ ] 路由器测试证明了本地优先的默认值；提供方测试证明了截断的流会抛出类型化错误。
