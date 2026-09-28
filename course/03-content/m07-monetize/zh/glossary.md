# 术语表 — M7：变现

按英文字母顺序排列。每个术语：先给定义，再给出处（仓库指针或课程文件）。

**形容词楔子（Adjective-wedge）** — 定位一句话中承载差异点的开头形容词——竞争对手要追平就必须重建的那一部分。出处：推导出的定位语，见 `ListenToMe/docs/competition-analysis.md:88`。

**收益实现登记表（Benefits-realization register）** — 保证定价诚信的机制：把每一项声称的节省挂到一条由财务负责的预算行上，因此主张由客户自己的财务部门核对，而不是由卖方核对。出处：`course/00-research/03-ai-qe-deep-read.md` §4。

**有上限的分阶段试点（Capped phased pilot）** — 有边界的合作阶段：8–10 周，五个阶段（0–4），由发起人签字的继续/终止关口，在观察结果之前冻结验收标准。出处：`ai_qe/_data/engagement.json` 和 `ai_qe/docs/method/phased-pilot.md`。

**对标价格区间（Comparator band）** — 你自己的表格中与你的产品真正可比的那些行的最低到最高价格范围。出处：`lab.md` 第 2 步（工作表模板）。

**成本底线（Cost floor）** — 你每月的固定成本——托管、API 密钥、摊销的开发时间——换算成保本所需的每月销量。出处：`course/04-sales/pricing-and-platforms.md`，“Cost floor”。

**删除测试（Deletion test）** — 从定位一句话中删掉一个分句；如果你的表格中没有任何一行会察觉这句话变成了假的，这个分句就是装饰，要删掉。出处：`lesson.md` M7.3。

**功能门控（Feature gating）** — 在代码库中注册付费路由，但在它们所依赖的工作流变得可信之前，通过开关让它们返回 404。出处：`SignUpFlow/README.md` 的 “Provider-backed Features”，以及 `SignUpFlow/AGENTS.md`。

**固定费用探查（Fixed-fee discovery）** — 一个有边界的首次付费合作，在任何更大的承诺之前先确认预算和发起人。出处：`ai_qe/_data/engagement.json`（商务字段）。

**直播价比例规则（Fraction-of-live-price rule）** — 只有保留项目、异步反馈和社区时，自学版才定在直播档价格的 70–85%；否则光秃秃的视频库根本不应该出售。出处：`course/00-research/02-course-market-research.md` §C。

**诚实营销清单（Honest-marketing checklist）** — 每份销售材料都必须通过的五条规则：数字有来源、主张有限定、不编造推荐语、退款/截止日期政策写清楚、为转变定价。出处：`course/04-sales/pricing-and-platforms.md`。

**一次性定价（One-time pricing）** — 因为每用户边际成本不重复发生而只收一次费用——这是端侧产品的规律。例证：MacWhisper 那一行，`ListenToMe/docs/competition-analysis.md`。

**按席位定价（Per-seat pricing）** — 按席位为 SaaS 定价，让价格单位随组织的采用规模增长。出处：`lesson.md` M7.1，依据是 `SignUpFlow/README.md` 中的邀请流程。

**定位一句话（Positioning one-liner）** — 一句形如「形容词楔子 × 差异点 × 受众」的话，从比较表中逐个分句推导出来。出处：`lesson.md` M7.3。

**有限定的主张（Qualified claim）** — 同时带有来源和局限的主张，因此买家可以审计它。出处：`course/00-research/03-ai-qe-deep-read.md` §3（“planning inputs are not observed client results”）。

**口碑漏斗（Reputation funnel）** — 免费或开源产品赖以运转的营销面：代码、README、覆盖率徽章、公开的竞品分析、支持服务和一个 Pro 档。出处：`course/01-design/curriculum.md`，M7.1。

**销售页结构（Sales-page anatomy）** — 八个部分的结构：转变标题、适合谁/不适合谁、问题与利害、每个模块的成果、讲师证明、推荐语、常见问题、透明定价和唯一的行动号召。出处：`course/00-research/02-course-market-research.md` §E。

**怀疑派工程师测试（Skeptical-engineer test）** — 实验 M7 第 5 步：你自己的表格会招来的三个最难的异议，每个都用一个点名的行或一个仓库指针来回答。出处：`lab.md` 第 5 步。

**价值锚点（Value anchor）** — 你的产品所替代的东西——工时、人员或某个工具订阅——表示为一个可比较的金额。出处：`lab.md` 第 2 步。

## 容易弄错的术语

- **价格与成本底线（Price vs. cost floor）** — 价格是你的要价；底线是它下面的保本算术。低于底线的价格就是补贴，无论对标区间怎么说。
- **功能门控与门控核心（Feature gating vs. gating the core）** — 门控推迟的是一条尚未证明的*付费路径*；门控核心则让关键工作流在你付费之前停止运转。`SignUpFlow/AGENTS.md` 禁止后者。
- **有限定的主张与含糊的主张（Qualified claim vs. hedged claim）** — 有限定的主张写明它的来源和局限；含糊的说法（「效果因人而异」）两者都不写，换不来任何信任。
- **免费档与免费开源定位（Free tier vs. free-and-open positioning）** — 免费档是对付费产品的限额；免费开源是附带商业模式的 $0 价格。ListenToMe 属于后者；Natively 那一行两者兼有。
- **对标区间与最低标价（Comparator band vs. cheapest sticker price）** — 区间覆盖的是可比的行；品类里最便宜的标价通常属于另一种产品，有着不同的成本结构。

## 精选资源

1. `ListenToMe/docs/competition-analysis.md` — 12 行的表格和逐个分句推导的定位语；
   把它当作你自己表格的格式来读。
2. `SignUpFlow/README.md`（“Provider-backed Features”）+ `SignUpFlow/AGENTS.md` — 门控模式，
   以及核心不得依赖付费路径的规则。
3. `ai_qe/_data/engagement.json` + `ai_qe/docs/method/phased-pilot.md` — 分阶段漏斗及其由
   发起人签字的关口；一个有边界的专业知识报价的形态。
4. `ai_qe/docs/method/discovery-questionnaire.md` — 线索确认资产，包括对一份没人能填完的表单的
   复盘。
5. `course/00-research/02-course-market-research.md` §C–§E — 价格区间、平台经济学，以及
   八个部分的页面结构。
6. `course/04-sales/pricing-and-platforms.md` — 本课程自己的决策记录；照搬它的格式
   （底线、阶梯、为什么不更便宜、为什么不更贵、发布策略）。
7. `course/00-research/03-ai-qe-deep-read.md` §1、§3、§4 — 为什么有限定的主张能带来转化，以及
   测量是如何定价的。
8. `ai_qe/docs/economics/slide-language.md` — 哪些措辞可以、哪些不可以出现在幻灯片上；这是
   案例研究中最严格的主张纪律。
