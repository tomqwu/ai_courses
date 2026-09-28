# 讲义 M3 — 隐私、测试与交付

**心智模型：** 隐私是一种靠工程实现的模式，而不是一个形容词——每次请求都校验模型的元数据，任何缺失都失败即关闭（fail closed），并且只让发布止于一个重新下载、经过校验和验证的产物。

## 决策表：哪个层级能看到这个风险？

| 风险 | 层级 | 为什么是这个层级而不是别的 |
|---|---|---|
| 逻辑：解析、错误类型、提示词构建器 | 单元测试，模拟传输层，在 CI 中 | 快速、确定，不需要守护进程 |
| 线上契约：请求形态、流式解析 | 真实 LLM 契约测试，在 CI 之外 | mock 只能假设这个接缝；这个测试证明它 |
| 隐私路由：这个模型真的在本地吗？ | 单元红队测试 + 逐请求的 `/api/show` | 云端别名会出现在本地守护进程上 |
| 麦克风、系统音频、权限授予 | 人工冒烟测试 | 需要一个 GUI 会话和手动授权 |
| 未经测试的核心逻辑悄悄混入 | CI 中的覆盖率底线 | 只有当有行未被执行时才失败 |

## 值得留下的五条规则

1. **模式是显式的；密钥从不切换它。** 添加云端密钥只会保存密钥；只有当用户选择云端时，路由才会改变。
2. **标签点明数据。** 是 “Ollama Cloud — sends transcript and context”，而不是 “enhanced”。
3. **逐请求校验，失败即关闭。** `remote_host`/`remote_model` 不存在，`details.format` 和 `model_info` 非空——否则拒绝。
4. **拒绝重定向。** 一个 3xx 会终止请求；文本绝不能被悄悄转发。
5. **完成 = 已合并；已发布 = 重新下载并且校验和匹配**，标签位于确切的提交上。只声称你达到的那一级：候选、已验证、已发布。

## 留好这些命令

```bash
make lab-m3                    # privacy + streaming hardening suite → 56 passed
make lab-m2                    # unit suite + coverage floor ≥90 → 208 passed, 100%
make e2e                       # real-LLM contract test (needs LAB_E2E=1, live daemon)
pytest tests/test_contract_real_llm.py -q    # 2 skipped — with a stated reason
LAB_E2E=1 pytest tests/test_contract_real_llm.py -q   # 2 passed
python -m pytest tests -m "not e2e" --cov=src/tinycopilot --cov-fail-under=90 -q
```

## 要打开的文件

- `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:3-13, 15-24` — 模式、如实的标签、失败即关闭的 `isVerifiedLocal` 守卫。
- `ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:138-157, 208-214` — 主机检查、逐请求校验、`RejectRedirects`。
- `ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:80-95` — 本地优先的自动选择。
- `ListenToMe/scripts/check-coverage.sh` + `ListenToMe/.github/workflows/ci.yml:36-42` — 底线。
- `ListenToMe/Makefile:39-53` + `ListenToMe/Tests/ListenToMeCoreTests/OllamaContractE2ETests.swift:4-22`
  — 带门控的契约测试。
- `ListenToMe/docs/manual-smoke-test.md:1-7` — 只有人能验证的东西。
- `ListenToMe/docs/RELEASING.md:33-39, 41-52` — 已发布这一级，以及 bundle id 分离。
- `ListenToMe/AGENTS.md:13-18, 55-82` — 完成即已合并；候选/已验证/已发布的阶梯。
- `ListenToMe/docs/competition-analysis.md:1-14, 70-80` — 有出处的表格与定位语。

## 三个坑

1. **localhost URL 什么也证明不了。** 一个 `:cloud` 别名会通过你的本地守护进程安装、列出并应答——而计算在远程。
2. **失败即放行藏在缺失的键里。** 如果缺少 `details` 字典时跳过检查而不是拒绝，你构建出来的就是那个反模式。
3. **你的守护进程决定第 1 步的走向。** 如果只有 `:cloud` 别名，仅本地模式会正确地拒绝一切。把它记录下来；不要削弱检查。第 0 步是 `make m3-start`：随附的答案被暂时移开，`make lab-m3` 变红——先把这个记录下来。

## 满足以下条件，就算完成……

- ☐ 在仅本地模式下，一个带 `remote_host` 的模拟 `/api/show` 被拒绝，并且先记录了红色运行。
- ☐ 缺少 `format`/`model_info` 时失败即关闭；非回环主机会抛出异常；3xx 被拒绝。
- ☐ `LAB_E2E` 契约测试通过并记录了输出——无论路由选中哪个聊天模型，包括 `:cloud` 别名；它是契约测试，不是隐私测试。
- ☐ 覆盖率底线：失败运行和成功运行都已记录。
- ☐ `docs/competition.md` 有 ≥5 行、≥6 列，每个单元格都有来源或标为 `unverified`。
- ☐ 定位语的每个分句都注明了证明它的那一列。
