# 讲义 M7 — 变现：定价、包装与定位

**一句话心智模型：** 成本怎样重复发生，就怎样定价；包装买家能拿得出手的转变；每个主张都从一个你能指出来的表格行推导出来。

## 决策表——根据成本结构选择模式

| 产品原型 | 成本结构 | 模式 | 谁付费 / 何时付费 |
|---|---|---|---|
| 类型 1 端侧应用 | 没有重复发生的每用户算力 | 免费核心 + 一次性 Pro（或 $0 + 口碑漏斗、支持服务、Pro） | 用户，在下载时 |
| 类型 2 SaaS | 重复发生的托管 + 数据 + 按席位计的服务 | 按席位分档；付费路径在被证明之前用开关关闭 | 组织管理员，在邀请成员时 |
| 类型 3 专业知识 | 重复发生的时间投入，分发的边际成本为零 | 分阶段漏斗：免费站点 → 问卷 → 固定费用探查 → 有上限的试点 → 验证 | 发起人，按每个有边界的阶段 |

三者通用的规则：低于成本底线（cost floor）的价格不是价格，而是补贴。

## 值得记住的五个做法

1. **先算底线。** 保本点 = 固定底线 ÷（价格 − 手续费 − 可变成本）。推理成本线 =
   调用次数 × token 数 ÷ 1,000 × 费率——端侧或 BYOK 时对你来说是 $0；写明谁付费（M7.2）。
2. **每个价格单元格都要有来源。** URL + 检索日期；未经确认的单元格写上「大约」或
   「据报道」——这是 `ListenToMe/docs/competition-analysis.md` 中的约定。
3. **直播价比例。** 自学版 = 直播价的 70–85%，*前提是*保留项目 + 反馈 +
   社区；否则它「根本不应该出售」（`course/00-research/02-course-market-research.md` §C）。
4. **门控尚未证明的部分。** 已注册但返回 404 的路由（`BILLING_ENABLED=false`、`SMS_ENABLED=false`）；
   「核心排班不得依赖任何一项付费集成」（`SignUpFlow/AGENTS.md`）。
5. **定位一句话 = 形容词楔子 × 差异点 × 受众。** 每个分句都对应一列；做
   删除测试（`ListenToMe/docs/competition-analysis.md:88`）。

## 工作表模板（粘贴进 `docs/pricing.md`）

```markdown
Cost floor: $__/mo — hosting $__, API keys $__, dev time $__ amortized
Inference: __ calls × __ tokens ÷ 1,000 × $__ = $__/user-mo — paid by <me|BYOK|hardware>
Comparator band: $__ (low) to $__ (high) — rows: <names>
Value anchor: replaces <hours|headcount|subscription> worth ~$__
Chosen model: <one-time|free+Pro|per-seat|usage|outcome|hybrid|BYOK> — because <cost line>
Tiers: <name> $__ — included: <…>; NOT included: <…> — because <…>
Launch price: $__ — founding $__, deadline <date>, traded for <testimonial|feedback>
Rationale ≥150 words, citing specific table rows: <…>
```

## 要打开的指针

- `ListenToMe/docs/competition-analysis.md` — 14 行的价格表，以及定位语（第 88 行）。
- `ListenToMe/docs/RELEASING.md` — 直销渠道的发布机制。
- `SignUpFlow/README.md` — “Provider-backed Features”；`SignUpFlow/AGENTS.md` — 门控规则。
- `ai_qe/index.md`、`ai_qe/discovery.md`、`ai_qe/_data/engagement.json` — 漏斗和分阶段合作。
- `course/00-research/02-course-market-research.md` §C–§E — 价格区间、平台、页面结构。
- `course/04-sales/pricing-and-platforms.md` — 实例记录：底线、阶梯、诚实营销清单。
- `course/00-research/03-ai-qe-deep-read.md` §1、§3、§4 — 测量定价和有限定的主张。

## 三个坑

1. **凭记忆定价。** 没有 URL 和日期的价格就是伪造的证据——直接判为不通过。
2. **没有重复成本却收订阅。** 如果你表格的成本列写的是端侧，月费就是一笔买家可以审计的收费。
3. **无法证伪的定位。** 「最好的 AI 工具」无论删掉哪个分句都不会被打破；如果没有任何一行会察觉，这句话什么也卖不出去。

## 满足以下条件，你就完成了……

- [ ] ≥5 个竞品行，每个价格单元格都有 URL + 检索日期，不确定的单元格已加限定。
- [ ] 工作表已完成：底线和推理成本线的输入都有标注，保本点可以复算，另有区间、锚点、模式、档位和价格。
- [ ] 理由 ≥150 词，并点名具体的竞品行。
- [ ] 定位语附有分句 → 列/能力的映射；通过删除测试。
- [ ] 包装页的每个档位都有一句明确的「不包含——因为」。
- [ ] 三个来自你自己表格的买家异议，每个都用一行或一个指针回答。
- [ ] 已运行诚实营销清单，五项的通过情况都有引文。
- [ ] 已记录结论：「一位怀疑派工程师会为此付费吗？」——以及哪个异议差点让结论翻转。
