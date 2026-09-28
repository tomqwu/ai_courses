# 术语表 — M6（专业知识产品）

## 术语

**基准记录（Benchmark record）** — 可引用证据的单位：一个发现，加上日期、样本、方法、单位、自报还是实测、
资助方，以及它能支撑什么主张。任何无法验证的内容都如实列出。出处：`ai_qe/CONTRIBUTING.md`，
“Research conventions”；示例见 `ai_qe/docs/evidence/benchmarks.md`。

**收益实现登记表（Benefits-realization register）** — 由财务部门负责的表，每种捕获机制一行：预算科目、
负责人、它最早可能变化的日期，以及财务部门会接受的证据。出处：`ai_qe/docs/method/phased-pilot.md`。

**主张层级（Claim level）** — 每个数字都必须带的四种标签之一：任务级效率、释放的 QA 产能、硬性节省、
软件总支出影响。出处：`ai_qe/docs/principles.md`；在 `evidence-dataset.md` 中有转载。

**内容即代码（Content as code）** — 用与软件相同的纪律来管理已发布的内容：测试、评审关卡、带哈希的媒体、
版次和不可变发布。出处：`ai_qe/Makefile` 和 `ai_qe/CONTRIBUTING.md`，“Release validation”。

**版次（Edition）** — 某一个内容界面的具名版本，与站点版本分开追踪。
出处：`ai_qe/_data/release.yml`（`version`、`slide_edition`、`fintech_edition`、
`questionnaire_edition`、`research_edition`）。

**认知标签（Epistemic label）** — 一个数字的状态：实测 / 自报 / 与厂商有关联 / 示意。
按照 `ai_qe/docs/economics/slide-language.md` 中的措辞规则，直接标在幻灯片上。

**财务信息问题组（Financial-capture set）** — 那份失败的表单漏掉的问卷问题：预算归属、支出中的可变部分、
续约窗口、释放的产能会被如何处理，以及财务部门会把什么认定为节省。出处：`ai_qe/docs/method/discovery-questionnaire.md`。

**推进/终止关口（Go/no-go gate）** — 由发起人签字的决策边界，带有成本上限、停止规则和冻结的标准。
出处：`ai_qe/docs/method/phased-pilot.md`；确切数字在 `ai_qe/_data/pilot_gates.json` 中。

**引导路线（Guided route）** — 在稳定幻灯片 ID 之上精选的播放顺序，声明了 `closing` 收尾幻灯片，
只重排和省略，从不改写。出处：`ai_qe/_data/briefing_routes.json`。

**不可变发布（Immutable release）** — 已发布的版次从不覆盖；需要时另发一个新的。
出处：`ai_qe/CONTRIBUTING.md` 和 `ai_qe/releases.md`。

**未验证清单（Not-verified list）** — 一份明确公开的、无法确认的主张清单，与已证实的主张放在一起。
出处：`ai_qe/docs/research-log.md`。

**来源清单（Provenance manifest）** — 每次检索的记录，包括 URL、检索日期、状态和 SHA-256 哈希
——失败也在其中。出处：`ai_qe/research/document-manifest.json`；图片见
`ai_qe/research/visual-provenance.md`；语音见 `ai_qe/assets/data/narration-provenance.json`。

**研究日志（Research log）** — 带日期的受理队列，主张必须先进入这里才能到达页面：Question /
Checked / Outcome / Changed。出处：`ai_qe/docs/research-log.md`。

**标志性限定语（Signature qualifier）** — 给整个产品定性的那一句话：“Planning inputs and proposed
outcomes are not observed client results.”（规划输入和拟议结果不是观察到的客户结果。）出处：`ai_qe/README.md`。

**稳定幻灯片 ID（Stable slide ID）** — 路线和分享链接据以解析的不变幻灯片编号，因此路线可以重排而不破坏链接。
出处：`ai_qe/_data/briefing_room.json` 中的大纲。

**充分证据（Sufficient evidence）** — 置信区间不跨越相关决策边界的结果。单独的点估计永远不够充分；
出处：`ai_qe/docs/method/phased-pilot.md`。

## 容易弄错的术语

- **释放的产能与硬性节省（Released capacity vs. hard-dollar saving）** — 腾出的工时只是生产力，直到财务部门
  指明这笔支出实际从哪条预算科目中削减；「没有捕获行的产能结果，按生产力而不是现金节省来报告」
  （`ai_qe/docs/method/phased-pilot.md`）。
- **自报与实测（Self-reported vs. measured）** — 「组织报告有 10–15% 的提升」是咨询公司给出的感受类数字；
  实测数字有方法和测量工具，记录会写明是哪一种（`ai_qe/docs/evidence/benchmarks.md`）。
- **站点版本与内容版次（Site version vs. content edition）** — 只改播放器的补丁推进 `version`，同时刻意保留
  `slide_edition`；把所有字段一起升级，会让客户无从知道自己手里拿的是什么（`ai_qe/releases.md`）。
- **未验证与错误（Not verified vs. false）** — 「未验证」表示有人去找过这项主张但无法确认；它是一个诚实的
  未决条目，而不是指控（`ai_qe/docs/research-log.md`）。
- **精选路线与改写的讲稿（Curated route vs. rewritten deck）** — 路线在稳定 ID 之上重排和省略；为某类受众改写
  幻灯片会让内容分叉，并破坏每一个分享出去的链接（`ai_qe/_data/briefing_routes.json`）。

## 精选资源

- `ai_qe/CONTRIBUTING.md`，“Research conventions” — 七个必填字段，以及先登记日志、再进页面的流程，
  用仓库自己的话写成。
- `ai_qe/docs/evidence/benchmarks.md` — 把 METR 和 Peng 两条记录前后连着读；这个对比就是关于资助方和
  局限的全部课程。
- `ai_qe/docs/principles.md` — “节省”的四个层级，原文照录，带有能拦住大多数混用错误的「谁能确认」一列。
- `ai_qe/docs/method/discovery-questionnaire.md` — 对前身那份 29 个问题、186 个选项的表单所做的事后复盘；
  关于设计筛选漏斗的最佳单页材料。
- `ai_qe/docs/method/phased-pilot.md` — 五个阶段、成本护栏、冻结的标准和有序的决策表；配合
  `_data/pilot_gates.json` 一起读。
- `ai_qe/releases.md` — 两条相邻的变更日志条目，展示一个被刻意保留的版次。
- `course/03-content/m06-expertise-product/evidence-dataset.md` — 实验的起始主张，已经标好层级和认知状态。
