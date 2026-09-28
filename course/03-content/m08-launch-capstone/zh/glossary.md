# 术语表 — M8：发布：销售页、邮件序列与结业项目

> 十八个术语，按英文字母顺序排列。「出处」是要打开的文件——每一条都能在本仓库中找到。定义是本模块所教的定义，
> 而不是一本通用的营销词典。

**验收标准（Acceptance criteria）** — 一个故事必须满足的具体、可测试的条件，按 Given/When/Then 书写。验收标准含糊时，结业项目的第 1 个维度就不达标。*出处：* `SignUpFlow/specs/014-security-hardening/spec.md`；`03-content/m08-launch-capstone/lab.md` 第 2 步。

**内测折扣交换（Beta-discount trade）** — 以创始期折扣明确交换一段推荐语和一次反馈访谈，在结账时约定。它之所以诚实，是因为买家知道这份折扣换的是什么。*出处：* `04-sales/pricing-and-platforms.md`（发布价格政策）。

**开放购买（Cart open）** — 第 4 封邮件，也是报价变得可以购买的时刻；课程的购买开放 10–14 天。它是转化阶段的第一封邮件。*出处：* `04-sales/launch-plan.md`。

**转化阶段（Conversion phase）** — 最后四封邮件（开放购买 → 异议拆解 → 证明 → 最后提醒），它们花掉预热阶段赢得的信任。*出处：* `04-sales/launch-plan.md`；`00-research/02-course-market-research.md` §E。

**截止日期诚实原则（Deadline honesty）** — 这条规则要求发布截止日期必须对应一个真实的变化——关闭购买、价格结束——因为会重置或反复出现的截止日期会教名单学会等待。*出处：* `04-sales/pricing-and-platforms.md`（"no fake countdowns"）。

**邮件送达率（Deliverability）** — 邮件到底能不能进入收件箱；通过发件域名上的 SPF、DKIM 和 DMARC 来配置，Gmail 和 Yahoo 对批量发件人强制执行。它位于每一个转化数字的上游。*出处：* `04-sales/launch-plan.md`（开头和运营检查清单）。

**证据记录（Evidence record）** — 结业项目必需的附件：命令及结果、产物链接，以及一份局限清单。含糊其辞（「测试通过」）会让第 3 个维度不达标。*出处：* `01-design/assessment-and-rubrics.md`（结业项目证据记录）。

**失败即关闭（Fail-closed）** — 一种仅本地模式：凡是无法验证为本地的，一律拒绝，而不是退回到云端模型。它是第 1 类产品的纪律产物。*出处：* `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift`；`03-content/m08-launch-capstone/lesson.md` M8.3。

**发布证据日志（Launch evidence log）** — 记录实际名单规模、送达、打开、点击、各封邮件的转化以及收入的日志，保留下来，是为了让下一个收入模型从观察中推导出来。*出处：* `04-sales/launch-plan.md`（要记录的指标）。

**引流产品（Lead product）** — 在邮件序列运行之前建立名单的免费资产；课程用的是一次 30 分钟的 AI 产品拆解。*出处：* `04-sales/launch-plan.md`（免费引流产品）。

**单一行动号召（One CTA）** — 恰好一个行动号召，无论出现在哪里都逐字重复。两个相互竞争的按钮会给读者一个什么都不做的出口。*出处：* `04-sales/landing-page.md`（首屏、定价、最后提醒）。

**证明资产（Proof asset）** — 一件你已经拥有、能支撑页面上某条主张的产物：一个打了标签的仓库、一行带日期的证据、一个覆盖率数字、一个规格文件夹、一张来源追溯表、一段演示。*出处：* `03-content/m08-launch-capstone/lesson.md` M8.1 的清单表。

**预留推荐语位（Reserved testimonial slot）** — 一个标明了的、空着的推荐语占位，附一条诚实说明，用来代替编造社会认同。课程的页面按之前/之后/结果的格式预留了三个。*出处：* `04-sales/landing-page.md`（推荐语）。

**从规格到交付的循环（Spec-to-Ship Loop）** — 课程的六个阶段：研究 → 规格 → 构建 → 验证 → 发布 → 证明。结业项目在一个产品上执行全部六个阶段。*出处：* `00-research/00-synthesis.md`。

**StoryBrand 立场（StoryBrand stance）** — 学员是英雄、讲师是向导的定位规则；写「你将交付」，而不是「我将教你」。*出处：* `00-research/02-course-market-research.md` §E。

**租户隔离（Tenant isolation）** — 强制每一条查询和每一个路由都限定在一个组织之内，并用使用真实 JWT 的负路径测试来验证。它是第 2 类产品的纪律产物。*出处：* `SignUpFlow/docs/TESTING.md`；`03-content/m08-launch-capstone/lab.md`。

**转变式标题（Transformation headline）** — 一句可证伪的、陈述目的地而不是内容的话。它是八个部分中的第一个。*出处：* `00-research/02-course-market-research.md` §E；`04-sales/landing-page.md`。

**预热阶段（Warmup phase）** — 最初三封邮件（起源故事 → 转变证明 → 免费工具），它们赢得信任，不提出任何购买请求。*出处：* `04-sales/launch-plan.md`。

## 容易弄错的术语

- **预热与转化（Warmup vs. conversion）** — 预热赢得推销的资格；转化花掉它。在预热阶段推销的邮件，是一封放错了位置的转化邮件。
- **预留位与占位推荐语（Reserved slot vs. placeholder testimonial）** — 预留位是空的，并且如实标明；占位推荐语是一段你自己写的引语。后者就是编造。
- **引流产品与课程（Lead product vs. the course）** — 免费的拆解是一个建立名单的工具，它交付的是一种方法的微缩版；它不是付费产品的打折版本。
- **通过徽章与记录的证据（A passing badge vs. recorded evidence）** — 徽章是当前状态；证据记录是一条命令、它的计数、一个日期和它的局限。只有后者经得起差距评审。
- **页面长度与页面质量（Page length vs. page quality）** — 长度跟随价格和利害；它是你必须回答的异议的产物，绝不是周全程度的替代指标。

## 精选资源

1. `04-sales/landing-page.md` — 完整的示例页面；把它当作八个按顺序展开的步骤来读，并原样照搬预留位的做法。
2. `04-sales/launch-plan.md` — 七封邮件的序列及其主题行，外加你在第一次发送之前要运行的运营检查清单。
3. `04-sales/pricing-and-platforms.md` — 价格阶梯，以及把关你写的每一份材料的诚实营销清单。
4. `00-research/02-course-market-research.md` §E — 结构、阶段划分、最后 48 小时数据和收入公式的主要来源。
5. `01-design/assessment-and-rubrics.md` — 五维度结业项目评分细则和证据记录模板，在实验中重新列出。
6. `03-content/m08-launch-capstone/lab.md` — 按产品原型划分的范围表、必需产物检查清单、验收清单。
7. `SignUpFlow/docs/playbooks/validation.md` — 你的证据记录所模仿的格式：计数、日期、环境，以及仍然可见的失败。
8. `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift` — 失败即关闭的仅本地行为的参考实现，你的第 1 类纪律产物以它为衡量标准。
