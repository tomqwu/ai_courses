# 讲义 M0 — 导览（一页，可打印）

**一句话心智模型：** 三种产品原型（archetype）——端侧应用、规格驱动的 SaaS、专业知识产品——都用同一个循环构建：**研究 → 规格 → 构建 → 验证 → 发布 → 证明**，而「完成」永远意味着一个别人能打开的文件。

## 选择你的产品原型

| 如果你想构建…… | 产品原型 | 研究这个仓库 | 它的证明资产 |
|---|---|---|---|
| 一个在用户机器上运行的、私密且快速的应用 | 1 — 端侧 AI 应用 | ListenToMe | 96% 核心覆盖率徽章（`ListenToMe/README.md`） |
| 一个多用户 Web 产品，功能可由智能体实现 | 2 — 规格驱动的 SaaS | SignUpFlow | "1,464 passed, 21 skipped"（`SignUpFlow/docs/playbooks/validation.md`） |
| 一份以研究为支撑的简报、课程或报告 | 3 — 专业知识产品 | AI × QE | 包含 14 项发现的自我审计（`ai_qe/research/reviews/site-audit-2026-09-06.md`） |

## 循环，每个阶段一件真实产物

```
STUDY    14-row competitor table     ListenToMe/docs/competition-analysis.md
SPEC     Given/When/Then stories     SignUpFlow/specs/014-security-hardening/spec.md
BUILD    checkbox tasks, tests first SignUpFlow/specs/019-sms-notifications/tasks.md
VALIDATE 7 test tiers, dated counts  SignUpFlow/docs/TESTING.md
RELEASE  signed + notarized DMGs     ListenToMe/AGENTS.md
PROVE    "do not promote 1.3.0"      ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md
```

## 值得保留的命令

```bash
git clone https://github.com/tomqwu/ListenToMe.git   # + SignUpFlow, ai_qe
python3 --version                                    # want 3.11–3.13
ollama pull qwen3:0.6b && ollama list                # :cloud suffix = not local
ollama run qwen3:0.6b "Reply with exactly: PONG"
cd SignUpFlow && make setup                          # Poetry env + migrations + seed
poetry run python -m api.cli.main init my-church
poetry run python -m api.cli.main solve my-church     # capture the whole block
cd ../course/03-content/m02-ondevice-app/tinycopilot && make lab-m2   # before Module 1
```

2026-09-16 head 上的求解器输出：`People: 5`、`Events: 2`、`Health score: 0.0/100`、
`Violations: 2 hard, 0 soft`、`Fairness: stdev=0.50`、`Solution saved to my-church/output/solution.json`
（`SignUpFlow/api/cli/main.py:193` 打印分数那一行；这个值随版本变化——记录你的运行实际打印的内容）。`Solved in …ms` 和 `Range:` 因机器和日期而异。

进入第 1 模块之前：`make lab-m2` → **208 passed**，覆盖率 **100%**（底线 90%）。`make lab-m3` → **56 passed**。
`make e2e` → 守护进程运行时 **2 passed**；没有 `LAB_E2E=1` 时，2 个契约测试会被跳过。

## 要打开的文件

- `course/03-content/m00-orientation/lesson.md` — 模块讲稿
- `course/03-content/m00-orientation/lab.md` — 步骤和验收清单
- `course/03-content/m00-orientation/quiz.md` — 8 道题
- `course/03-content/m02-ondevice-app/tinycopilot/README.md` — M2 实验参考
- `SignUpFlow/README.md` — 求解器 "CLI Examples"；`SignUpFlow/api/cli/main.py` 打印摘要块
- `ai_qe/README.md` — 发布记录

## 三个常见陷阱

1. **`:cloud` 名字不是本地模型。** `ollama list` 中以 `:cloud` 结尾的条目是云端托管的别名；localhost URL
   并不能证明文本在哪里被处理。两种环境对 M0 都有效——说明你用的是哪一种。
2. **在系统 Python 上，`pip install` 可能会拒绝运行**（PEP 668，"externally-managed-environment"）。
   先创建虚拟环境，再安装 `pytest pytest-cov httpx`。
3. **Python 3.10 或 3.14 会让 `make setup` 停下。** SignUpFlow 的构建关卡接受 3.11 到 3.13，
   失败时会打印这个区间。

## 完成的标志……

- [ ] `ls -d ListenToMe SignUpFlow ai_qe` 三个都打印出来
- [ ] `python3 --version` 显示 3.11–3.13
- [ ] `ollama list` 显示 ≥1 个模型，而且你能把它标为本地或 `:cloud`
- [ ] 求解器已运行；包含 `Health score:` 和 `Solution saved to …` 两行的完整输出块已粘贴
- [ ] 已写下带日期的证据日志条目
- [ ] 首个成果帖已发布：求解器输出 + `ollama list` + 你的产品原型那句话
- [ ] 进入第 1 模块之前：`make lab-m2` 显示 `208 passed`（或者写出了确切的缺失依赖）
