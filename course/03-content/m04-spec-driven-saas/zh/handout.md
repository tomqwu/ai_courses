# 讲义 M4 — 规格驱动的 SaaS（一页纸）

**心智模型：** 规格文件夹（spec folder）是写给一个对你毫无记忆的智能体的指令集——所以每个产物都必须经得起陌生人的检验，而检查清单关卡是拦下经不起检验之处的最后一个低成本位置。

## 流水线

```
specify ─ clarify ─ CHECKLIST ─ plan (research · data-model · contracts) ─ tasks ─ implement ⇄ converge
  WHAT     ≤3 Qs     before plan  HOW + Constitution Check                   Phase 2   until Converged
```

Spec-kit 1.0 把每一步命名为 `/speckit-<step>`；SignUpFlow 1.0 之前的文件夹把它们拼写为 `/speckit.<step>`，并且没有 converge。

| 产物 | 负责 | 拒绝承载 |
|---|---|---|
| `spec.md` | 做什么（WHAT）：故事、Given/When/Then、FR、成功标准 | 语言、框架、模式 SQL |
| `research.md` | 带选项、理由和被否决方案的决策 | 不声不响的偏好 |
| `data-model.md` | 实体和字段 | —（当基础设施横跨多个实体时缺席） |
| `plan.md` | 怎么做（HOW）：技术栈、版本、存储、目标 + 宪章检查 | 面向用户的行为 |
| `contracts/` | 接缝：形态、错误键、键模式、测试草图 | 边界上的凭感觉 |
| `checklists/requirements.md` | 关卡：Content Quality、Completeness、Readiness | —（是生成的，所以要验证它） |
| `tasks.md` | 按故事组织的工作，测试先行，**精确的文件路径** | 「更新后端」 |

## 留好这些命令和格式

```bash
ls specs/                                   # 17 folders in SignUpFlow
grep -rn "NEEDS CLARIFICATION" specs/       # must return zero
grep -o "FR-[0-9]\{3\}" spec.md | sort -u | wc -l   # recount against the checklist
grep -o "app/[a-z_/]*\.py" tasks.md | sort -u | xargs ls  # every cited path must exist
ls alembic/versions/                        # where migrations actually live
```

PR 正文（固定四个部分）：`Summary:` 每项改动一行 · `Changed files:` 路径：原因 ·
`Validation:` 命令及结果 · `Follow-ups:` 已知缺口和未决问题。

任务行：`- [ ] T017 [P] [US1] Implement create_wizard_state method in api/services/onboarding_service.py`

## 值得打开的文件

- `SignUpFlow/specs/014-security-hardening/spec.md` — 8 个故事、44 条 FR、7 个边界情况、12 条标准。
- `SignUpFlow/specs/014-security-hardening/plan.md` — 宪章检查，七个结论，零违规。
- `SignUpFlow/specs/014-security-hardening/contracts/rate-limiting.md` — 以配置表形式出现的 5/5/15 副歌。
- `SignUpFlow/specs/014-security-hardening/checklists/requirements.md` — 关卡，以及 "5xP1" 漂移。
- `SignUpFlow/specs/000-user-onboarding/tasks.md` — 真实的任务格式；第 3 行的过期路径；迁移漂移。
- `SignUpFlow/.specify/templates/`（`spec-template.md`、`plan-template.md`、`tasks-template.md`）— 每个功能从中取用的产物集合。
- `SignUpFlow/.specify/memory/constitution.md` — Context A，Ralph 循环自己的规则。
- `SignUpFlow/docs/ai-pr-review.md` — 本地评审检查清单和两条硬性底线。

## 三个坑

1. **技术泄漏进 `spec.md`。** 关卡的第一条规则禁止这样做。模式属于数据模型、契约和迁移——实体的描述要 "without implementation"。
2. **「Then 系统是安全的」不是场景。** 当测试作者不需要做任何决定时，一个场景才算完成；数字（5/5/15）会以 FR、契约行和断言的形式反复出现。
3. **生成的产物会漂移。** 一个过期的 `/specs/020-user-onboarding/` 路径，一份面对六个 P1 故事却打印 "5xP1" 的检查清单，被指派到一个不存在的 `migrations/` 目录的迁移。grep 路径，重数计数。

## 满足以下条件，你就完成了……

- [ ] `spec.md` 有 ≥3 个可独立测试的故事、带数字的 Then 子句、≥8 条 FR，没有实现细节。
- [ ] 没有遗留任何 `[NEEDS CLARIFICATION]` 标记；未知项记录在 Assumptions 中。
- [ ] `research.md` 有 ≥3 个决策，每个都带一个被否决的方案和原因。
- [ ] `plan.md` 为每条原则给出宪章检查结论；违规都有论证。
- [ ] 一份契约包含形态、错误键和测试草图。
- [ ] `tasks.md` 的每个任务都写明一个存在的文件路径；阶段测试先行；每个故事一个检查点。
- [ ] 在你 grep 了它的路径、重数了它的计数之后，你的检查清单仍然通过。
- [ ] 一个陌生人实现了故事 1，没有提出任何本该由文件夹回答的问题。
