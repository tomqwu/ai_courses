# 实验 M2 — 构建 TinyCopilot 的核心（Python + Ollama）
> AI Product Studio（APS-3）的一部分 · 第 2 模块的通过/不通过检查点 · 配套课程：`lesson.md`

## 目标

构建 **TinyCopilot** 的可运行核心——一个用 Python 编写、镜像 ListenToMe 架构的多角色 AI 助手：一个带按字符预算的上下文窗口（context window）的会话存储、一个带防抖（debounce）的问题检测器、三个角色的纯提示词构建器、带本地优先默认值（local-first defaults）的按角色模型路由、带类型化错误的 Ollama 流式调用，以及一个把角色接到模型上、并按角色取消的编排器。实验 M3 之后会用一个失败即关闭的仅本地模式来加固这同一个核心，所以不要破坏它的测试。

## 前置条件

- 已完成第 1 模块（你有一个起始仓库，里面有 `constitution.md`、`AGENTS.md`、`specs/` 和一份证据日志）。
- PATH 中有 Python 3.11+。
- 已安装并运行 Ollama，并拉取了一个模型：`ollama pull qwen3:0.6b`（任何小型聊天模型都可以；记下它的名字）。
- 本模块文件夹中的 `tinycopilot/` 参考仓库。

## 时间

约 3 小时。让测试来驱动时，六个模块平均每个 25–30 分钟。

## 起始项目

`tinycopilot/` 文件夹是一个*参考实现加一整套测试*。要用一种特定的纪律对待它：**测试就是规格，参考实现就是参考答案。** 你将删除六个标出的模块，并以 TDD 的方式把每一个重新实现到变绿——卡住时去读参考答案是正当的，不跑测试就照抄则不是。Makefile 负责运行一切：

- `make lab-m2` — 运行本模块的测试套件，并强制执行覆盖率底线（90）。
- `make demo` — 用你真实的 Ollama 模型，把一小段预先准备的转写文本送过全部三个角色。
- `make lab-m3` — 实验 M3 的隐私测试套件。它的文件（`src/tinycopilot/privacy.py`、`tests/test_privacy.py`、`tests/test_contract_real_llm.py`）作为参考解答随本实验一起提供；实验 M3 的 `make m3-start` 会在那个实验开始前把它们暂时移走。在本实验中不要动它们——`test_privacy.py` 的 35 个测试已经在 `make lab-m2` 中运行。

## 步骤

1. 在动任何东西之前运行 `make lab-m2`。确认测试套件是绿的，覆盖率底线也通过。你看到的是完成后的参考答案——花十分钟阅读 `src/tinycopilot/copilot.py`，在删除之前看清各个部分是如何连接的。
2. 删除第一个模块的实现：`git rm src/tinycopilot/conversation_store.py`（所有模块都在 `src/tinycopilot/` 下；它们的测试是 `tests/test_<module>.py`）。运行 `make lab-m2`，并**把红色输出记录**到你的证据日志中。它不是一份失败测试的列表：`src/tinycopilot/__init__.py:8-34` 重新导出了每个模块，而 `tests/conftest.py:13` 导入了这个包，所以 pytest 在收集阶段就停下，报出 `ModuleNotFoundError: No module named 'tinycopilot.conversation_store'`，退出码 4，一个测试也没运行。把它原样记录为红色结果；你的规格是测试文件，而不是这条错误；一旦某个桩实现能被导入，红色就会变成断言级别的失败。
3. 根据测试文件（`test_conversation_store.py`）重新实现 `conversation_store.py`：应用已定稿与临时的片段，以及 `recent_context(max_chars)`，在字符预算内保留最新的片段——总是至少保留最新的那一条。运行 `make lab-m2`，直到变绿。
4. 删除 `question_detector.py`，并根据 `test_question_detector.py` 重新实现它：结尾的 "?"、开头的疑问词、按词边界匹配的短语线索。要包含防抖测试——一连串提问在每个窗口内最多触发一次。
5. 删除 `prompts.py`，并根据 `test_prompts.py` 重新实现它：三个基础角色提示词（不要开场白的 Quick、绝不编造的 Listener、深度优先于简洁的 Deep）、追加到每个角色上的人设指令，以及按角色的用户消息构建器。这些必须是纯函数——没有 I/O。
6. 删除 `model_router.py`，并根据 `test_model_router.py` 重新实现它：词首前缀标记匹配（不能有子串误命中——"gemini" 绝不能匹配 "mini"）、角色默认值（Listener 和 Quick 都取**最快**的模型，Deep 取**最强**的模型，模型不够时角色共用一个模型），以及把 `:cloud` 排除在本地优先默认值之外。**有记录的差异：** ListenToMe 的 Swift `ModelRanking.roleDefaults` 在有可用模型时，还会为 Listener 额外挑选*第二个、不同的*快速模型（`ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:91-111`）；本实验的可执行规格不这样做，在这里以测试为准。按测试来实现，并记下这个差异——注意到重新实现简化了一条规则，正是本课程教你要记录而不是隐藏的那种漂移。
7. 删除 `ollama_provider.py`，并根据 `test_ollama_provider.py` 重新实现它：针对 `http://localhost:11434/api/chat` 的流式聊天，带一个可注入的传输层（测试使用伪造实现）、NDJSON 行解析，以及类型化错误——流内的 `{"error": ...}`、截断的流（没有 `done`）和空的流（没有内容）都必须各自抛出不同的错误类型，绝不返回成功。
8. 删除 `copilot.py`，并根据 `test_copilot.py` 重新实现它：编排器把每个角色路由到它的模型，构建该角色的提示词，以流式获取响应，并且——通过每个角色一个的生成计数器——在角色的模型于中途切换时取消过期的流（被切换掉的模型绝不能写入输出）。
9. 运行演示：`make demo`。它用你拉取的模型，把一小段转写文本送过全部三个角色。记录输出——Listener 的摘要、Quick 的建议、Deep 的回答。

## 验收清单（必须全部满足）

- [ ] 全部六个模块重新实现之后，`make lab-m2` 以 0 退出。
- [ ] 对全部六个模块，你的证据日志都显示了每次绿色运行*之前*的一次红色运行。
- [ ] `make lab-m2` 在 `tests/test_privacy.py` 未经修改的情况下为绿——它的 35 个测试包含在那 208 个之中。实验 M3 的 `privacy.py` 及其测试作为参考随本实验提供，并由实验 M3 的 `make m3-start` 暂时移走；现在还不要在它们的基础上构建。
- [ ] 覆盖率底线在 90 处通过（包含在 `make lab-m2` 中）。
- [ ] `make demo` 打印出来自至少一个真实模型的三个不同的角色输出（Listener、Quick、Deep）。
- [ ] 你的证据日志为每个模块用一两句话解释了它的测试先行循环。
- [ ] 路由器测试证明 Deep 得到最强的模型，Listener 和 Quick 得到最快的模型，模型不够时角色共用一个模型——并且你的证据日志记下了 Swift 与 Python 之间的差异（第 6 步）。
- [ ] 提供方测试证明截断的流和空的流会抛出类型化错误，并且绝不以成功告终。

## 证据记录

对每个模块：删除后失败的 `make lab-m2` 输出、重新实现后通过的输出，以及一句话，说明测试规定了哪些提示词里没有说到的东西。然后记录最终完整的 `make lab-m2` 运行（包括覆盖率那一行），以及完整的 `make demo` 输出记录，其中模型名可见。使用课程的证据格式：命令、结果、日期、环境、局限。

## 拓展目标

- **Swift 路线（仅限 Mac）：** 打开真实的 ListenToMeCore 文件，把每个 Python 模块对应到它的 Swift 对应物——`conversation_store.py` → `Sources/ListenToMeCore/ConversationStore.swift`，`question_detector.py` → `QuestionDetector.swift`，`prompts.py` → `Prompt.swift`，`model_router.py` → `ModelRanking.swift`（+ `MeetingSession` 的路由），`ollama_provider.py` → `OllamaProvider.swift`，`copilot.py` → `MeetingSession.swift`。写下 Swift 版本做出、而你的 Python 版本没有做出的两个设计决策，以及原因。
- **加第四个角色**（例如一个 "Critique" 角色）：它自己的基础提示词、默认模型规则、下拉菜单和测试。遵循同样的红 → 绿循环。
- **给存储加一个 VAD 式的分段启发式规则：** 仿照 `Sources/ListenToMeCore/VAD.swift`，用一个 RMS 阈值和尾部静音规则把一整块扁平的转写文本切分成语句，并用测试证明每个边界都恰好触发一次。

## 讨论题

发到社区：你的 `make demo` 输出，外加对这个问题的回答——六个模块中，哪一个在「我以为它应该做什么」与「测试说它必须做什么」之间差距最大？使用以下模板：

> **TinyCopilot M2 — [你的名字]**
> 演示输出：[粘贴]
> 最出乎意料的模块：[模块]——我原以为是 [X]；测试规定的是 [Y]，因为 [基于一个 ListenToMe 文件指针的理由]。
