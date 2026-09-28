---
marp: true
theme: aps
paginate: true
title: M3 — 端侧 AI 应用：隐私、测试与交付
---

## M3 — 隐私、测试与交付

从「能跑」到「可信且可交付」· 约 75 分钟 + 约 3 小时实验 · 案例研究：ListenToMe。

```figure
kind: flow
alt: 第 2 模块中能跑起来的 TinyCopilot 核心经过三步——失败即关闭的隐私、分层测试、经过验证的交付——最终成为一个经过验证的下载。
step: 一个能跑起来的核心 — 来自第 2 模块的 TinyCopilot @ 第 2 模块给了你
step: 失败即关闭的隐私 (seam) @ 你要设计一个
step: 分层测试 @ 你要设计一个
step: 经过验证的交付 @ 你要设计一个
step: 一个经过验证的下载 (hl) @ 你要设计一个
```

<!-- NOTES: 欢迎来到第 3 模块。第 2 模块给了你一个能跑起来的 TinyCopilot 核心；今天我们让它变得可信、可销售。三步：设计一个失败即关闭的仅本地模式；分层测试，让每个风险都落在真正能观察到它的层级上；按一个以经过验证的下载为终点的完成定义（Definition of Done）来交付。明确说出案例研究是 ListenToMe，每一条论断都有你可以打开的文件指针。时间：一分钟。过渡：学习目标。 -->

---

## 学完本模块，你能够……

- **设计**一个失败即关闭的仅本地模式
- 在每次请求时**校验**模型元数据
- 分层**测试**：单元、契约、人工
- **交付**一个经过校验和验证的产物
- 基于一张有出处的竞品表来**定位**

<!-- NOTES: 把这五个目标当作承诺来读。设计意味着元数据校验、回环主机白名单、拒绝重定向，以及如实的标签。校验意味着询问守护进程它即将运行的是什么。分层意味着承认 CI 在结构上无法测试的东西。交付意味着发布以你亲自下载自己的产物并核对其校验和结束。定位意味着一句每个分句都能追溯到某一列的定位语。时间：一分钟。过渡：进入 M3.1 分段。 -->

---

## M3.1 — 隐私是一种模式，不是一句口号

```figure
kind: architecture
alt: 把隐私做成用户选择的一个枚举——四种模式，各自写明数据去向——外加一条边界规则：添加密钥从不切换模式。
source: ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:3-10
layer: AI 处理模式 — 用户在设置中选择的一个枚举 @ ListenToMe 暴露了
  box: 仅本地 — 本地模型；每次请求都校验元数据
  box: Apple Intelligence — 完全在本设备上运行
  box: 云端 (seam) — 转写文本、笔记、摘要发往 Ollama Cloud
  box: 关闭 AI — 采集、转写、保存照常可用
layer: 边界规则 (hl) @ 然后是边界规则
  box: 添加密钥只会把它存起来，路由不做任何改变
  box: 选择云端是有意为之，绝不是副作用 @ 选择云端
```

`ListenToMe/README.md:199-207`

<!-- NOTES: 核心观点：隐私不是营销文案里的一个形容词，而是设置里的一个模式开关。ListenToMe 暴露了 AIProcessingMode，有四个取值。把云端的标签大声读出来："Ollama Cloud — sends transcript and context."。这个标签点明了它发送出去的数据，这就是你写的每一个模式标签都要达到的标准。然后是边界规则：粘贴一个 API 密钥只会保存这个密钥，路由不做任何改变。时间：两分钟。过渡：强制执行这一点的代码。 -->

---

## 证明：模式枚举及其标签

- README：“Adding a key alone does not switch modes”

```swift
public enum AIProcessingMode: String, CaseIterable, Sendable {
    case off, local, apple, cloud
    public var label: String { switch self {
    case .off: return "AI off — transcript only"
    case .local: return "Local Ollama models only"
    case .apple: return "Apple Intelligence — on this device"
    case .cloud: return "Ollama Cloud — sends transcript and context"
    } } }
```

`ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:3-13`

<!-- NOTES: 在屏幕上打开 ModelPrivacy.swift，读顶部的 AIProcessingMode 枚举。四个取值，四个诚实的标签。要记住的是 cloud：它没有说 "enhanced"，它说的是会发送转写文本和上下文。README 中 "AI processing mode" 一节写着关键规则：仅添加密钥不会切换模式。用户不可能因为配置的副作用而滑到云端路由上。时间：三分钟。过渡：为什么显而易见的捷径行不通。 -->

---

## localhost URL 什么也证明不了

<!-- _diagram: flow -->

- 用 `ollama pull` 拉取一个 `:cloud` 模型
- 和其他模型一样列在 `ollama list` 中
- 在 `localhost:11434` 上应答
- 计算却发生在别处

> "A localhost URL or a model name alone is insufficient."

> "A local endpoint is not proof of local inference." (G01)

`ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:16` · `ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md:46`

<!-- NOTES: 这就是整个分段要防范的失败。显而易见的实现是检查 URL 是否为 localhost，然后就算完事。ModelPrivacy.swift 里有一条注释，明确拒绝了这条捷径。原因如下：拉取一个带 `:cloud` 后缀的模型，它会通过你的本地守护进程安装，出现在 `ollama list` 中，并通过你的 localhost URL 应答，而计算发生在别处。差距评审说得很直白：本地端点并不能证明本地推理。时间：三分钟。过渡：元数据确实能证明什么。 -->

---

## `/api/show` 必须显示什么

| 应答中的字段 | 要求 | 证明什么 |
|---|---|---|
| `remote_host` | 不存在 | 不是云端别名 |
| `remote_model` | 不存在 | 不是云端别名 |
| `details.format` | 非空 | 已下载模型的形态 |
| `model_info` | 非空 | 权重保存在本地 |

- 每次请求都让守护进程描述这个模型
- 其他任何情况都失败即关闭——一个返回 `false` 的条件判断
- 指针：`ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:18-22`

<!-- NOTES: 修复方法是：每次请求都让守护进程描述它即将运行的模型，只接受一个已下载本地模型的描述。四项要求：没有 remote_host，没有 remote_model，details.format 非空，model_info 非空。前两项抓住云端别名；后两项证明这是一个在本地携带权重的已下载模型的形态。整个检查就是一个返回 false 的条件判断。时间：两分钟。过渡：守卫本身。 -->

---

## 证明：`isVerifiedLocal` 失败即关闭

```swift
public static func isVerifiedLocal(_ data: Data) -> Bool {
    guard let info = try? …jsonObject(with: data) as? [String: Any],
          info["remote_host"] == nil, info["remote_model"] == nil,
          let details = info["details"] as? [String: Any],
          let format = details["format"] as? String, !format.isEmpty,
          let modelInfo = info["model_info"] as? [String: Any],
          !modelInfo.isEmpty else { return false }
    return true
}
```

`ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:17-24`

<!-- NOTES: 展示 isVerifiedLocal。一个 guard 子句：解析 JSON，要求 remote_host 和 remote_model 不存在，要求 details.format 非空，要求 model_info 非空，否则返回 false。因为失败路径是默认路径，缺失的元数据、格式错误的 JSON 和意外的字段都会被拒绝。把信任边界大声说出来：这校验的是守护进程的自我描述，而不是守护进程本身。README 诚实地写明了这一点。时间：三分钟。过渡：围绕这项检查的三道防线。 -->

---

## 围绕检查的三道防线

```figure
kind: system
alt: 在仅本地模式下，一个聊天请求在任何会议文本离开进程之前要通过三道防线——回环主机检查、每次请求都执行的已验证本地 /api/show 检查，以及拒绝重定向的传输层——任何一道失败都会先抛出异常。
source: ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:138-157 · ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:15-24
layer: OllamaProvider — 仅本地分支
  node req: 聊天请求 — 携带会议文本
  node host: 主机检查 (seam) — localhost · 127.0.0.1 · ::1 @ 第一，基础 URL 的主机
  node show: /api/show (seam) — 200 + isVerifiedLocal，每次请求 @ 第二，提供方向
  node transport: 传输层 (seam) — 拒绝重定向 @ 第三，重定向
layer: 可能的终点
  node daemon: 本地 Ollama 守护进程 (hl)
  node fail: 抛出异常 — 在发送提示词的任何一个字节之前 @ 其他任何主机
edge: req -> host
edge: host -> show — 回环地址 @ 第二，提供方向
edge: host -> fail — 任何其他主机 @ 其他任何主机
edge: show -> transport — 已验证本地 @ 第三，重定向
edge: show -> fail — 远端或缺失的元数据 @ 第二，提供方向
edge: transport -> daemon — 不跟随任何重定向 (hl) @ 第三，重定向
edge: transport -> fail — 一个 3xx @ 第三，重定向
```

- 仅限 localhost、127.0.0.1 和 ::1
- 指针：`ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:138-157`

<!-- NOTES: 在仅本地模式下，每个聊天请求之前都要先跑三层检查。第一，基础 URL 的主机必须是 localhost、127.0.0.1 或 ::1；其他任何主机都会在写出提示词的第一个字节之前抛出异常。第二，提供方发送 /api/show，要求 HTTP 200 外加已验证本地的元数据结果；每次请求都重新校验，所以会话中途切换模型也无法跳过这项检查。第三，重定向。打开 OllamaProvider.swift，看流式请求的仅本地分支。时间：三分钟。过渡：为什么重定向很重要。 -->

---

## 拒绝重定向

- 仅本地请求带着 `RejectRedirects` 运行
- 否则你的会议文本会被悄悄转发

```swift
private final class RejectRedirects: NSObject, URLSessionTaskDelegate {
    func urlSession(_ session: URLSession, task: URLSessionTask,
        willPerformHTTPRedirection response: HTTPURLResponse,
        newRequest request: URLRequest,
        completionHandler: @escaping @Sendable (URLRequest?) -> Void) {
        completionHandler(nil)
    }
}
```

`ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:138-142, 208-214`

<!-- NOTES: 在大多数 HTTP 栈中，跟随重定向默认是静默的。即使一个通过了本地校验的服务器，也可能对 /api/chat 返回一个指向任意地址的 3xx，而 HTTP 栈会「热心地」把你的会议文本转发过去。这个委托选择拒绝：遇到任何 HTTP 重定向，它都回答 nil，请求随之终止。注释说明了原因：在仅本地模式下，绝不带着会议文本跟随重定向。没有这道防线，元数据检查就会在传输层被绕过。时间：两分钟。过渡：失败即关闭的默认值。 -->

---

## 默认失败即关闭

```swift
public static func roleDefaults(from models: [String],
        local: Set<String>? = nil) -> [CopilotRole: String] {
    let localModels = local.map { verified in
            models.filter { verified.contains($0) } }
        ?? models.filter { !looksCloudHosted($0) }
    let rankedPool = ranked(
        localModels.isEmpty ? models : localModels)
```

- `ModelRanking.roleDefaults` 过滤掉 `:cloud` 模型
- 只有在没有本地聊天模型时才自动选中云端
- 关闭 AI 后，采集、转写、保存照常可用
- 默认把数据发出设备，按原则不在范围内

`ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:91-95` · `ListenToMe/CLAUDE.md:40-41`

<!-- NOTES: 失败即关闭同样塑造默认值。ModelRanking.roleDefaults 把 `:cloud` 模型完全排除在自动选择之外；只有在不存在本地聊天模型时才会自动选中云端，而这意味着用户设置了密钥并主动选择了云端。其下是 CLAUDE.md 中的产品原则：任何默认会把数据发出设备的东西，都不在范围内。而且关闭 AI 是一个真实的选项——采集、转写和保存照常工作。时间：两分钟。过渡：值得照搬的纪律。 -->

---

## 主张 → 工程强制

| 主张 | 强制它的工程手段 |
|---|---|
| 转写文本从不离开你的 Mac | 本地模式 + 主机检查 + `/api/show` |
| 云端别名无法混进来 | `isVerifiedLocal` 失败即关闭守卫 |
| 文本无法被悄悄转发 | `RejectRedirects` 拒绝每一个 3xx |
| 添加密钥从不改变隐私 | 模式是用户的显式设置 |
| 默认本地 | `roleDefaults` 过滤 `:cloud` |
| 参与者的发言是数据，不是指令 | 围栏块；块内的闭合标签会被中和 |

`ListenToMe/Sources/ListenToMeCore/Prompt.swift:69-83`

<!-- NOTES: 这张表就是值得照搬的纪律。你的产品做出的每一个隐私承诺都必须是一行，而它的第二列是评审者能打开的代码。如果一个主张没有第二列，你拥有的就不是主张，而是文案。让学员从自己的产品点子里挑一句营销语，试着填这张表。大多数人第一次都填不出来；这正是要学的一课。时间：三分钟。过渡：测试，M3.2 分段。 -->

---

## M3.2 — 测试就是层级分配

```figure
kind: architecture
alt: 按成本堆叠的三个测试层级——CI 中的单元测试看到你的逻辑，你机器上的契约测试看到真实的接缝，人工冒烟测试看到音频和权限。
layer: 人工冒烟 — 一个 GUI 会话，手动授权 @ 人工冒烟测试覆盖
  box: 观察：麦克风、系统音频、权限
layer: 契约 — 你的机器，真实守护进程，CI 之外 @ 针对真实守护进程的契约测试
  box: 观察：mock 只能假设的那个接缝
layer: 单元 — CI，模拟的传输层 @ 使用模拟传输层的单元测试
  box: 观察：你的逻辑
```

- 指出能观察到该风险的最便宜的层级
- 假装 CI 覆盖了最顶层，只会让你的 README 撒谎

<!-- NOTES: 本分段的重新定义：测试策略就是层级分配。对每个风险，指出真正能观察到它的最便宜的层级。使用模拟传输层的单元测试覆盖逻辑。针对真实守护进程的契约测试覆盖 mock 只能假设的那个接缝。人工冒烟测试覆盖音频和权限。你不能把一个风险提升到一个看不到它的层级。时间：两分钟。过渡：底线。 -->

---

## 95% 覆盖率底线

- 换来的：没有论证，就不会有未经测试的核心逻辑
- 换不来的：正确性、GUI、音频、首次运行

```bash
THRESHOLD="${1:-95}"
…
swift test --enable-code-coverage
…
PCT=$(xcrun llvm-cov export "$EXE" \
…
awk … 'BEGIN { exit !(pct + 0 >= thr + 0) }' || {
  echo "FAIL: coverage ${PCT}% is below the ${THRESHOLD}% floor" >&2
  exit 1
}
```

`ListenToMe/scripts/check-coverage.sh:11-40`

<!-- NOTES: ListenToMe 的 CI 在 ListenToMeCore 上强制执行 95% 的行覆盖率底线，作为硬性关卡。脚本在启用覆盖率的情况下运行测试套件，计算总行覆盖率，打印逐文件报告，低于阈值时以非零状态退出。说清它换来什么：任何人都无法往核心里添加未经测试的逻辑，除非要么测试它，要么有意识地论证把底线调低。说清它换不来什么：从未构建之物的正确性、可用的 GUI、音频采集，或者一个人能顺利挺过去的首次运行体验。时间：三分钟。过渡：CI 中的这个脚本。 -->

---

## 证明：底线在 CI 中真的会拦下构建

- `scripts/check-coverage.sh 95` 在 core 作业中运行
- 低于底线时以非零状态失败
- 三个 CI 作业，外加一个依赖锁差异检查
- 指针：`ListenToMe/scripts/check-coverage.sh`；`ListenToMe/.github/workflows/ci.yml:36-42`

```yaml
  core:
    name: ListenToMeCore tests + coverage
    runs-on: macos-26
    steps:
      - uses: actions/checkout@v4
      - name: Run ListenToMeCore test suite with a 95% coverage floor
        run: ./scripts/check-coverage.sh 95
```

<!-- NOTES: 打开 CI 工作流的 core 作业，展示覆盖率这一步，然后打开脚本本身。工作流有三个作业：macOS 应用构建、iOS 应用构建，以及核心测试套件加覆盖率底线。两个构建作业还会额外运行依赖锁差异检查，所以你测试的产物是用锁定的依赖构建的。发布纪律很早就出现了。时间：三分钟。过渡：CI 无法运行的那个测试。 -->

---

## CI 无法运行的契约测试

<!-- _diagram: steps -->

- `make build` — 应用目标能编译通过
- Ollama 在 `localhost:11434` 上应答，否则停止
- 选一个已安装的聊天模型——或用 `LTM_E2E_MODEL`
- 应用包位于解析出的路径
- `LTM_E2E=1 swift test --filter OllamaContractE2ETests`

- CI 无法访问守护进程或音频硬件
- 测试 mock 只能假设的那个接缝
- 带着写明的理由跳过，从不悄悄通过

`ListenToMe/Makefile:39-54`

<!-- NOTES: CI 无法访问 Ollama 守护进程或音频硬件，所以真实 LLM 的契约测试放在 CI 之外，藏在 make e2e 后面。它通过实际的提供方、针对你的本地守护进程跑一次真实的补全，并自动选择一个已安装的聊天模型。为什么叫「契约」？因为它测试的是 mock 只能假设的那个接缝：你的请求格式、流式解析和错误类型在真实环境下是否成立。每一个单元测试都用了 mock；这一次运行是证明 mock 诚实的唯一证据。时间：三分钟。过渡：门控模式。 -->

---

## 证明：一个会跳过、而不是躲起来的测试

- `make e2e` 设置门控并选择模型
- 断言：对固定提示词，流式内容非空

```swift
func testRealOllamaStreamingProducesContent() async throws {
    let env = ProcessInfo.processInfo.environment
    try XCTSkipUnless(
      env["LTM_E2E"] == "1",
      "e2e only: set LTM_E2E=1 and run a local Ollama (use `make e2e`)"
    )
```

`ListenToMe/Tests/ListenToMeCoreTests/OllamaContractE2ETests.swift:9-14`

<!-- NOTES: 打开 OllamaContractE2ETests.swift。测试对环境变量调用 XCTSkipUnless，所以普通的 swift test 和 CI 永远不会触碰网络；make e2e 负责设置门控并选择模型。断言刻意做得最小但真实：用 app 所用的同一套提供方代码，为一个固定提示词流式生成补全，并要求内容非空。门控模式和测试本身同样重要。时间：三分钟。过渡：只有人能运行的层级。 -->

---

## 只有人能运行的层级

| `make e2e` 已经覆盖 | 只有人能覆盖 |
|---|---|
| 应用构建 | 麦克风采集 |
| 应用包路径解析 | 系统音频采集 |
| 一个真实 LLM 契约测试 | 实时语音转文字 |

- 都需要一个 GUI 会话和手动授权
- 一份编号脚本：授权、说话、播放音频、确认标签
- 说明它覆盖什么；也说明它覆盖不了什么

`ListenToMe/docs/manual-smoke-test.md:3-6`

<!-- NOTES: 契约测试之上是人工层级。麦克风采集、系统音频采集和实时语音转文字都需要一个 GUI 会话和手动授权，manual-smoke-test.md 开篇就精确说明了 make e2e 已经覆盖了什么，以及这份文档覆盖的哪些内容无法自动化。它是一份编号的、可重复的脚本。一个假装 CI 覆盖了这一层的测试策略，只会让你的 README 撒谎。时间：两分钟。过渡：那次说「不」的评审。 -->

---

## 那次说「不」的评审

> "A signed installer, 215 passing Core tests, and 97.24% Core coverage are useful foundations; they do not establish capture reliability, durable saving, accurate speaker attribution, or a usable first-run experience."

- 34 项差距清单，G01 到 G34
- 建议：不要把 1.3.0 升为正式发布
- G01：本地端点可能执行云端模型
- 测试验证你构建的东西；评审验证你交付的东西

`ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md:5, 46`

<!-- NOTES: 2026 年 9 月 10 日，一次针对 1.3.0 候选版本的生产评审产出了一份 34 项的差距清单，每一项都有优先级和证据类别。手握 215 个通过的 Core 测试和 97.24% 的覆盖率，它仍然建议不要把这个版本升为正式发布。G01 就是 M3.1 分段里的那个隐私漏洞，它安安稳稳地待在 97% 的覆盖率之内，因为测试测的是已经构建的东西。时间：四分钟。过渡：交付，M3.3 分段。 -->

---

## M3.3 — 完成即已合并；已发布要拿出证明

```figure
kind: flow
alt: 完成就是合并到 main；发布是一条独立的发布列车，有三级台阶——候选、已验证、已发布——你只能声称证据所支持的那一级。
source: ListenToMe/AGENTS.md:20-45
step: 完成 — 合并到 main，检查全绿，文档已更新 @ 一项变更
step: 发布列车 (seam) — 批量进行，每天最多一次 @ 发布是一个独立的
step: 候选 — 在本地构建并检查 @ 候选版本
step: 已验证 — 已安装应用的验收 @ 已验证
step: 已发布 (hl) — 重新下载、校验和匹配、标签锁定 @ 而已发布
```

<!-- NOTES: ListenToMe 的 AGENTS.md 区分了大多数项目混为一谈的两个词。完成意味着合并到 main、三个必需检查全绿、测试通过，并且每一份受影响的文档都已更新。发布是一条独立的、批量进行的发布列车：每天最多一次 macOS 发布，绝不是每合并一个拉取请求就发布一次。已完成工作的诚实状态是「已合并到 main，搭乘下一班发布列车」。然后是阶梯：候选版本在本地构建并检查，已验证在此基础上加上已安装应用的验收，已发布意味着重新下载、校验和匹配、标签位于确切的提交上。只声称你的证据所支持的那一级。时间：三分钟。过渡：最高一级台阶的实际做法。 -->

---

## 证明：下载它并核对哈希

- 发布之后，下载托管的产物
- 把它的 SHA-256 与本地 DMG 对比
- 创建发布时用 `--target` 锁定到该提交
- 如果受阻：说出阻碍，报告「已合并但未发布」
- 指针：`ListenToMe/AGENTS.md:55-82`、`ListenToMe/docs/RELEASING.md:33-39`

<!-- NOTES: 打开 AGENTS.md 中的验证阶梯，以及 RELEASING.md 中对应的表格。发布之后，下载托管的产物，把它的 SHA-256 与经过验证的本地 DMG 对比，并在创建发布时用 target 锁定到确切的提交，这样标签就不会悄悄指向另一个提交。绝不替换已发布的二进制文件。诚实条款：如果有阻碍让发布无法进行，就准确地说出它，保留候选版本及其证据，并把这项工作报告为已合并但未发布。时间：三分钟。过渡：开发与发布的身份。 -->

---

## 两个 bundle id，是有意为之

| 构建 | Bundle id | 签名方式 |
|---|---|---|
| Release dmg | `com.tomwu.ListenToMe` | Developer ID |
| Debug | `com.tomwu.ListenToMe.dev` | Apple Development |

- macOS TCC 按 bundle id 加签名要求来登记授权
- 共用一个 id：安装其中一个会悄悄让另一个失效
- 开关保持打开，采集却什么也拿不到

`ListenToMe/docs/RELEASING.md:43-52` · `ListenToMe/README.md:176-180`

<!-- NOTES: 开发构建是一个与正式发布分开的 app：开发版一个 bundle id，正式版一个。原因在于 macOS 的隐私机制。TCC 是保存麦克风和屏幕录制授权的子系统，它按 bundle id 加上二进制文件的代码签名要求来登记权限授权。Developer ID 签名和 Apple Development 签名产生的要求永远无法相互满足。共用一个 bundle id，安装其中任何一个都会悄悄让另一个的授权失效：一个会撒谎的开关。时间：三分钟。过渡：竞品分析。 -->

---

## 把竞品分析当作工程产物

> Last updated: 2026-09. … where a detail could not be confirmed from a primary source, it is qualified with "approximately" or "reportedly."

- 14 行 × 9 列的对比表
- 每个竞品条目都以一个来源 URL 结尾
- 「本地优先」通常只是指本地采集
- 指针：`ListenToMe/docs/competition-analysis.md:3, 14, 20-35`

<!-- NOTES: 交付的另一半，是清楚并证明你的产品相对于已有产品是什么。打开 competition-analysis.md。它像测试套件一样构建：一个带日期的开头，写明未经确认的细节都用 approximately 或 reportedly 加以限定；一张 14 行 × 9 列的表；以及逐个竞品的章节，每个条目都以一个来源 URL 结尾。这份分析点出了结构性的矛盾：几乎每一款商业产品都在云端运行它的 AI，即使它把自己宣传为本地优先。时间：三分钟。过渡：定位语。 -->

---

## 定位语及其对应的列

| 分句 | 证明它的列 |
|---|---|
| 免费 / 开源（free / open-source） | 价格（Price） |
| 完全端侧（fully on-device） | 是否端侧（On-device?） |
| 会议 copilot（meeting copilot） | 定位焦点（Focus） |
| 自带模型（bring your own model） | 多模型/自带（Multi-model/BYO） |
| 面向 macOS（for macOS） | 平台（Platform） |

<!-- NOTES: 这份分析没有凭空发明一句口号；它找出了一个几乎没有商业竞品占据的角落，然后从表格中推导出这句话。README 中的定位语：面向 macOS 的免费、开源、完全端侧运行的会议 copilot，自带你的模型，保持私密，适配任何对话。每个分句都能追溯到某一列。删掉任何一个分句，都会让这句话在表格面前变成假话。这就是交付物：具体、可证伪，而不是营造气氛的背景音乐。时间：三分钟。过渡：实验。 -->

---

## 实验 M3 — 加固、证明、定位

- 目标：让 TinyCopilot 从能跑变得可信
- 先写红队测试，再实现
- CI 之外的契约测试、覆盖率底线、对比表
- 第 5 步：打标签、算校验和、把台阶记为候选
- 通过关卡：`make lab-m3` → 56 passed
- 两种守护进程结果都有效

<!-- NOTES: 实验 M3 让 TinyCopilot 从能跑变得可信。第 0 步把随附的参考答案暂时移开，这样红色运行才是真实的。第 1 步：先写红队测试，然后实现隐私模式、本地模型校验、主机强制和重定向拒绝。第 2 步：由 LAB_E2E 门控的契约测试。第 3 步：覆盖率底线和一次记录下来的失败运行；第 3b 步：在其之上的行为评测。第 4 步：对比表。第 5 步：给经过测试的提交打标签，为产物计算校验和，并把台阶记为候选。套件关卡：make lab-m3，56 passed。时间：三分钟。过渡：测验。 -->

---

## 测验 M3

- 8 道题：6 道选择题，2 道简答题
- 失败即关闭的设计，以及为什么 localhost 不是证明
- 重定向拒绝与覆盖率底线的机制
- 层级分配，以及评审高于指标
- 从列推导出定位

<!-- NOTES: 测验 M3 有八道题，覆盖三个分段：失败即关闭的设计、为什么 localhost URL 不是证明、拒绝重定向的理由、覆盖率底线能抓住和抓不住什么、为什么契约测试放在 CI 之外、差距评审的教训，以及定位的推导。每道题对应一个分段目标。在研讨会之前完成它。时间：一分钟。过渡：回顾。 -->

---

## 回顾

- 隐私是一种模式；每次请求都校验元数据
- localhost URL 什么也证明不了；失败即关闭
- 分层测试；指标只是入场费
- 完成即已合并；已发布是一次经过验证的下载
- 定位来自一张有出处的表格

<!-- NOTES: 带走本模块的五句话。隐私是一种配有如实标签的模式，并且每次请求都校验元数据。localhost URL 什么也证明不了，因为本地守护进程可以提供云端别名。分层测试，并记住覆盖率是入场费，不是结论。完成意味着已合并，已发布意味着一次你亲自验证过的下载。定位来自一张有出处、有限定的表格。时间：两分钟。过渡：讨论题。 -->

---

## 讨论题

- 发布你最难强制执行的那个隐私主张
- 指出能证明它的代码或测试
- 你的保证实际上在哪里终止？
- 写出你的信任边界那句话
- 回复一位同伴：指出他们遗漏的那道防线

<!-- NOTES: 收尾时，请学员发布他们最没把握能强制执行的那个听起来像营销语的隐私主张，再附上假如去写、能证明它的代码或测试。然后是更难的问题：你的保证实际上在哪里终止？ListenToMe 用一个分句回答：它信任已安装的本地 Ollama 服务及其元数据。你的产品对应的那句话是什么，你会把它放到你的销售页上吗？时间：两分钟。演示文稿结束。 -->
