# 讲义 — M6（专业知识产品）

**心智模型。** 在专业知识这种产品原型（archetype）中，产品不是内容本身，而是内容的可审计性：
一个研究库，每项主张都带着日期、样本、方法、单位和层级，在带版本号、经过测试、不可变的发布之下，
重新剪辑成面向特定受众的路线。

## 决策表 — 我主张的是哪个层级？

| 如果这个数字是…… | 它属于 | 必须由谁确认 |
|---|---|---|
| 单项活动在评审和修正之后的净时间 | 任务级效率 | 你自己做过的试点 |
| 采纳之后，整个工作流中腾出的人工工时 | 释放的产能 | 试点加基线工时采集 |
| 可以削减或规避的预算成本 | 硬性节省 | 财务部门，对应指名的预算科目 |
| 更宽泛的工程或交付成本 | 总支出影响 | 财务部门和 CIO 办公室 |
| 一个建模或规划情景 | **示意** | 没有人——在幻灯片上标明 |

混用这些层级是 AI 商业论证中最常见的错误（`ai_qe/docs/principles.md`）。

## 值得留存的模板和命令

**基准记录（benchmark record）字段**（一个数字进入幻灯片之前，七个字段全部齐备）：
`date · sample · method · unit · self-reported vs measured · sponsor · what claim it supports`

**来源行：**
`| # | Claim (exact slide wording) | Source URL | Retrieved | Level 1–4 | Epistemic label | What it supports |`

**路线声明：**
```yaml
executive: { slides: [1, 3, 6, 9, 11, 12], closing: 12 }
technical: { slides: [1, 3, 4, 5, 7, 8, 10, 9, 11, 12], closing: 12 }
full_order: [1,2,3,4,5,6,7,8,9,10,11,12]
```

```bash
grep -ciE 'not verified' docs/research-log.md    # your honest list is not empty
grep -n 'unavailable' research/document-manifest.json   # failures are logged
python3 -m json.tool _data/pilot_gates.json      # gates are data, not prose
make check                                        # models → build → site → browser
```

**版次决策模板：** 改了什么 · **刻意保留**了什么 · 哪个版次（edition）升级
（`version` 还是 `slide_edition`，按 `ai_qe/_data/release.yml` 中的区分）。

## 要打开的指针

- `ai_qe/CONTRIBUTING.md` — “Research conventions”；发布验证。
- `ai_qe/docs/evidence/benchmarks.md` — METR 和 Peng 两条记录，从头读到尾。
- `ai_qe/docs/research-log.md` — 未验证清单和未决问题清单。
- `ai_qe/research/document-manifest.json` — 11 次带哈希的检索，包括失败的 M02。
- `ai_qe/docs/principles.md` — “节省”的四个层级，原文照录。
- `ai_qe/_data/briefing_routes.json` — 基于稳定幻灯片 ID 的路线；`closing`。
- `ai_qe/docs/economics/slide-language.md` — Use 和 Avoid 两份措辞清单。
- `ai_qe/docs/method/discovery-questionnaire.md` — 按角色分流，以及失败表单的事后复盘。
- `ai_qe/docs/method/phased-pilot.md` 和 `ai_qe/_data/pilot_gates.json` — 冻结的标准和关口。

## 三个坑

1. **一个能打开的链接不是证据。** 链接检查拒绝把一次成功的 HTTP 响应当作主张正确的证明
   （`ai_qe/CONTRIBUTING.md`）。要么有日期、样本、方法和单位，要么就没有这一行。
2. **绝不要把所有版次一起升级。** 只改播放器的补丁推进 `version`，并刻意保留 `slide_edition`；
   变更日志要写明保留了什么（`ai_qe/releases.md`）。
3. **跨越关口的置信区间不是「差一点」。** 对该边界而言，它就是证据不足，
   “even if its point estimate appears favorable”（`ai_qe/docs/method/phased-pilot.md`）。

## 满足以下条件，你就完成了……

- [ ] `research-log.md` 有 ≥6 条带日期的条目，其中 ≥2 条标为未验证或未决。
- [ ] 每张含量化内容的幻灯片都按编号引用一行来源，没有孤立的数字。
- [ ] 每一行都带有来源 URL、检索日期和主张层级。
- [ ] 每张含量化内容的幻灯片都在幻灯片本身上标明认知标签。
- [ ] 高管路线恰好 6 张幻灯片，其决策请求被原文引用。
- [ ] 技术路线保留了 ≥3 张被高管路线跳过的证据幻灯片。
- [ ] 版次记录把站点与内容分开，并写明 v2 保留了什么。
- [ ] 一位具名的同伴书面确认没有任何未引用的量化主张。
