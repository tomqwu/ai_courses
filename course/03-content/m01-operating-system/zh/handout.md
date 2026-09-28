# 讲义 M1 — AI 产品操作系统

**一句话心智模型：** 治理文件约束智能体，spec-kit 产物告诉它要构建什么，而一份带日期的证据记录（evidence record）证明实际验证了什么。

## 循环

```text
constitution.md  →  AGENTS.md  →  spec.md  →  plan.md (GATE)  →  tasks.md  →  red test  →  green test  →  evidence-log.md
   principles         baseline      WHAT         HOW + check       exact paths    fail         pass          record + limits
```

## 决策表——哪个文件，哪项职责

| 你想说的是…… | 放进 | 绝不要放进 |
|---|---|---|
| 一条绝不能偏离的原则 | `constitution.md`（≤80 行） | `tasks.md` |
| 一条适用于每个智能体的规则 | `AGENTS.md`（≤200 行） | 规格 |
| 只有 Claude Code 需要的内容 | `CLAUDE.md`，放在 `@AGENTS.md` 下面 | `AGENTS.md` 的第二份副本 |
| 一条必须每次都成立的规则 | `.claude/settings.json` 中的一个钩子 | 一句智能体可能跳过的话 |
| 用户需要什么，不涉及技术 | `spec.md` | `plan.md` |
| 用哪个库、为什么、否决了什么 | `research.md` / `plan.md` | `spec.md` |
| 要改的确切文件，先写测试 | `tasks.md` | 其他任何地方 |
| 你运行了什么、没有验证什么 | `docs/evidence-log.md` | 只写在提交信息里 |

## 留好这些命令和模板

```bash
mkdir my-studio && cd my-studio && git init
python3 -m venv .venv && source .venv/bin/activate && pip install pytest
python3 -m pytest tests/ -q          # red, then green
git rev-parse HEAD                   # the revision your evidence pins
wc -l constitution.md AGENTS.md CLAUDE.md   # ≤80; AGENTS.md + CLAUDE.md ≤200
bash scripts/check-evidence-log.sh; echo $?  # the hook's check: 2 blocks, 0 passes
```

```markdown
## Evidence — <project> — <feature> — <YYYY-MM-DD>
Commands (with results):
- <command> → <N passed, M skipped, K failed>
Environment: <OS, Python version>
Revision: <git rev-parse HEAD>
Limitations / not verified:
- <at least one honest line>
```

规则改写检验：**「对 X 要小心」** → **「每条查询都按 org_id 过滤。」** 如果一个陌生人无法
检查一条规则是否被遵守，就改写它。

## 要打开的指针

- `SignUpFlow/.specify/memory/constitution.md` — 85 行，唯一的事实来源。
- `SignUpFlow/AGENTS.md` — 188 行；写作风格、优先级、防幻觉、PR 规则。
- `SignUpFlow/CLAUDE.md` — 154 行（2026-09-16）；Claude 附加说明，但它在第 5 行链接到 `AGENTS.md`，而本应导入它。
- `SignUpFlow/docs/SPEC_KIT_SETUP.md` — 1.0 之前的命令顺序（spec-kit 1.0 增加了 converge）。
- `SignUpFlow/specs/019-sms-notifications/tasks.md` — 一条真实、可执行的任务行。
- `SignUpFlow/docs/playbooks/validation.md` — 证据行、失败和局限。
- `ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md` — 「不要推广 1.3.0」。

## 三个坑

1. **只有绿、没有红的运行不是 TDD。** 先记录失败的输出，再记录通过的输出。
2. **「未验证」是必填字段。** 如果你的证据条目没有局限，它就是不完整的——而不是干净的。
3. **写了库名的规格就是计划。** 把技术挡在 `spec.md` 之外；检查清单关卡会拒绝它。

## 满足以下条件，你就完成了……

- [ ] `constitution.md` 存在，≤80 行，≥3 条原则，有自主权配置。
- [ ] `AGENTS.md` 存在，≤200 行，每条规则都是祈使语气且可验证。
- [ ] `CLAUDE.md` 以 `@AGENTS.md` 开头；证据日志检查对一条残缺条目以 2 退出，对你的条目以 0 退出。
- [ ] `specs/001-todo-command/` 包含 `spec.md`（2 个用户故事）、`plan.md`（关卡已通过）、`tasks.md`（≥5 个任务，精确路径，先写测试）。
- [ ] 红色的 pytest 输出已保存，然后是绿色运行：`python3 -m pytest tests/ -q` 以 0 退出。
- [ ] 证据条目包含命令、计数、日期、环境、局限和 head SHA。
- [ ] 有一条提交正文遵循 Summary / Changed files / Validation / Follow-ups 格式。

**记住：** 覆盖率告诉你测试了什么；只有一份诚实的记录才能告诉你交付了什么。
