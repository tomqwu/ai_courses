# 实验 M7 — 为你的产品定价和定位

> 第 7 个实验（共 8 个）· **前置条件：** **已完成实验 M2、M4 和 M6**——选出你要推向市场的产品 · **时间：** 约 2 小时 · 通过 = 下面每个清单项都可以客观验证

**目标：** 把你在实验 M2、实验 M4 或实验 M6 中构建的产品，变成一个有定价、有包装、有定位的报价：一张有来源的定价表、一份决策工作表、一句定位一句话（positioning one-liner）、一个包装页，以及一次经得起怀疑派工程师审查的自我评审。

**在哪里做：** 在你的产品仓库中创建 `docs/pricing.md`（第 1–2、5 步）和 `docs/positioning.md`（第 3–4 步），或者用一个 `docs/monetization.md`，把全部五步作为其中的小节。每个表格单元格、价格和主张都要有来源指针——本实验的产物会直接供给第 8 模块的销售页和结业演示。

## 第 1 步 — 把你的比较表扩展成定价表

拿出你在实验 M3 中构建的比较表（如果你的产品变了，就现在重新做一张），给它加上定价列。要求：

- **≥5 个竞品行**——是你真正访问过的竞品，而不是你记得的竞品。
- 列中必须包括：**价格**、**定价模式**（一次性 / 免费 + Pro / 按席位 / 按用量 / 按结果 / 混合 / BYOK 折扣——即 M7.1 的分类），以及**价格买到了什么**（限额、席位、隐私边界、支持服务）。
- 每个价格单元格都带**来源 URL 和检索日期**。不许凭记忆定价。
- 无法从一手来源确认的单元格，标注「据报道」或「大约」——这是 ListenToMe 的约定：「凡是无法从一手来源确认的细节，都标注为『大约』或『据报道』」（`ListenToMe/docs/competition-analysis.md`，文件开头，日期为 2026-09）。照搬 MacWhisper 那一行的写法：“Pro ~€59 (~$69) one-time; App Store $6.99/mo–$99.99 lifetime”——模式、价格和渠道写在同一个单元格里。

## 第 2 步 — 定价决策工作表

填写下面的内联模板。四个输入让这个决策站得住：

- **成本底线（cost floor）**——每一项以美元计的每月固定成本（托管、数据库、邮件、开发者会员、摊销的构建时间），每一项都标上来源指针或写明是*假设*。只有真正为零的地方，开发成本才能记为 $0，比如 SignUpFlow 的「SQLite（开发）/ PostgreSQL（生产）」阶梯（`SignUpFlow/README.md`）。
- **推理成本线**——每个用户（或组织）每月的调用次数 × 每次调用的 token 数 ÷ 1,000 × 每 1,000 个 token 的费率 = 每用户每月的美元数，并写明每个档位由谁来付：你、客户自己的密钥、用户的硬件，还是平台配额。本课程中没有任何当前模型 API 费率的来源：用 URL 和检索日期取得你自己的费率，或者写明它是一个假设。一个不调用任何模型的产品写「$0——没有模型调用」。
- **对标价格区间（comparator band）**——你的表格中可比的那些行的最低到最高价格。
- **价值锚点（value anchor）**——这个产品替代了什么：工时、人员，还是某个工具订阅。

然后计算**贡献**（价格 − 支付手续费 − 达到该档位上限时的可变成本）和**保本点**（固定底线 ÷ 贡献，向上取整）；从 M7.1 的分类中选择模式、档位和发布价格；并写出一段**≥150 词、引用具体表格行**的理由。要模仿的实例是 M7.2 中的两条底线——把 TinyCopilot 做成产品（推理成本线 $8.00，每月 6 单 Pro）和一个 SignUpFlow 形态的 SaaS（每个组织 $0.30，3 个 Starter 组织覆盖现金成本）——以及本课程自己在 `course/04-sales/pricing-and-platforms.md` 中的记录：底线（$80–130/月 → 保本点约 2 单/月），以及一段从两个方向辩护的「为什么不更便宜 / 为什么不更贵」。

## 第 3 步 — 定位一句话

按 ListenToMe 的格式写出你的定位语——**形容词楔子 × 差异点 × 受众**——例如「面向 macOS 的免费、开源、完全端侧运行的会议 copilot——自带模型，私密运行，并能适配任何对话」（`ListenToMe/docs/competition-analysis.md:80`）。每个分句都必须可以追溯：在定位语下面列出分句 → 表格列或仓库能力的映射（M7.3 的课程展示了 ListenToMe 的完整映射）。做删除测试（deletion test）：删掉任何一个分句，这句话都必须对某个具体的行变成假的。如果没有任何一行会察觉，这个分句就是装饰——删掉它。

## 第 4 步 — 包装页

为每个档位写明包含什么，**以及刻意不包含什么、为什么**。这种诚实模式来自 SignUpFlow：计费和短信路由已在 API 下注册，但在 `BILLING_ENABLED=false` / `SMS_ENABLED=false` 之下返回 404——「完整的排班工作流并不依赖它们」（`SignUpFlow/README.md`，“Provider-backed Features”）。每个档位一句明确的「不包含」并不是损失收入；正是这种功能门控式的诚实，让包含清单变得可信。为产物和转变定价，而不是为数量定价——「一堆 Zoom 录像不是自学课程」（`course/00-research/02-course-market-research.md` §C）。

## 第 5 步 — 自我评审：怀疑派工程师测试

写出**买家根据你自己的表格会提出的三个最难的异议**——也就是你的表格本身会招来的那些（例如「MacWhisper 一次性 $69，为什么你的更贵？」、「Otter 的免费档就能做到这个的 80%」）。每个都用证据回答：一个带来源的表格行，或者一个带文件指针的仓库能力。如果任何一个回答需要隐瞒什么，就修改价格或页面——然后重新做这个测试。

## 工作表模板（粘贴进 `docs/pricing.md`）

```markdown
# Pricing worksheet — <product name>

Inputs (each: value — source pointer, or "assumption"):
  - paying units: <users | organisations> ____ ; usage per unit per month: ____
  - model calls per unit per month ____ ; tokens per call ____ ; rate $____ per 1,000 tokens
Fixed floor: $____/mo = hosting $____ + database $____ + email $____ + other $____
  + build ____ h × $____ ÷ ____ months
Inference-cost line: ____ calls × ____ tokens ÷ 1,000 × $____ = $____ per unit-month
  who pays, per tier: <me | customer's key (BYOK) | user's hardware | platform quota>
Payment fee: ____% + $____ per sale — <source>
Contribution: $____ price − $____ fee − $____ variable at cap = $____
Break-even: $____ floor ÷ $____ contribution = ____ → ____ sales (or organisations) a month
Comparator band: $____ (low) to $____ (high) across comparable rows: <list row names>
Value anchor: replaces <hours | headcount | a tool subscription> worth ~$____
Chosen model: <one-time | free + Pro | per-seat | usage | per-outcome | hybrid | BYOK discount> — because <the cost line it matches>
Tiers:
  - <name> $____ — included: <…>; NOT included: <…>; AI allowance/cap: <…>
  - <name> $____ — included: <…>; NOT included: <…>; AI allowance/cap: <…>
Launch price: $____ — founding/early-bird: $____, deadline <date>, the discount is traded for: <testimonial | feedback | …>
Rationale (≥150 words, cite specific table rows): <…>
```

## 验收清单（二元判定——每个框都勾上才算通过）

1. ☐ ≥5 个竞品行；每个价格单元格都有来源 URL + 检索日期；不确定的单元格标注了「据报道/大约」。
2. ☐ 工作表已完成，并且底线是算出来的，而不是一个数字：每个固定成本项和推理成本线（调用次数 × token 数 ÷ 1,000 × 费率，或「$0——没有模型调用」）都列出了输入，每个输入都标有来源指针或「假设」；每个档位都写明了由谁支付推理成本；写明了保本点 = 底线 ÷ 贡献，并且能从这些输入复算出来；没有任何付费档的定价低于它自己在上限处的可变成本。
3. ☐ 理由 ≥150 词，并按竞品名称引用具体的表格行。
4. ☐ 定位语的每个分句都可以追溯——分句 → 列/能力的映射已写出来。
5. ☐ 包装页的每个档位都有一个明确的「不包含」部分，每一项都附有理由。
6. ☐ 三个来自表格的买家异议，每个都用点名的证据回答（行 + 来源，或文件指针）。
7. ☐ 诚实营销清单通过：运行 `course/04-sales/pricing-and-platforms.md` 中的全部五项，并在每一项旁边引述它的通过情况（例如第 1 项 “Every number carries a source” → 「工作表的底线引用了平台价格；表格单元格引用了 URL，检索于 <日期>」）。
8. ☐ 用一行记录怀疑派工程师的结论：「一位怀疑派工程师会为此付费吗？」——是/否，以及哪个异议差点让结论翻转。

## 证据记录

保存在 `docs/` 中（或粘贴到社区帖子里）：带来源的定价表；工作表 + 理由；定位语 + 映射；包装页；三个异议及其回答；附引文的清单运行记录。直播班学员把工作表带到每周的工作坊接受评审；自学学员发出发布价格 + 定位语，请一位同伴回复。

## 拓展目标（可选，约 30 分钟）

- **退款政策 + 保证条款。** 用平实的语言写出来——范围、期限、买家可以保留什么。参考形态：「14 天内或第 3 模块之前（直播班），保留资料」（`course/04-sales/pricing-and-platforms.md`）。写明什么算滥用，以及哪些情况你无论如何都会兑现。
- **90 秒演示脚本。** 一个问题，一条贯穿产品的实时路径，一件在屏幕上产出的产物。这是演示日的热身：第 8 模块的结业项目要求一次 5 分钟的演示，而 90 秒的核心是必须能跑通的部分。

## 讨论题

发出你的发布价格、你的定位语，以及你预计会招来最多反对的那一句「不包含」。回复一位同伴：拿他们的定位语去对照*他们自己的*定价表——哪个分句可以被证伪，哪个是装饰，以及他们的表格引出的哪个异议他们没有回答？
