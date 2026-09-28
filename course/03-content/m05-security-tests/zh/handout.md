# 讲义 M5 — 多租户安全与验收关卡

**一句话心智模型：** 租户隔离（tenant isolation）是一条由测试可检查的机制来强制执行的 P0 规则；验收是一座测试层级金字塔，外加一份用状态承认尚未证明之处的清单。

## 规则 → 机制 → 检查的阶梯

```text
RULE        every query filters by org_id          SignUpFlow/AGENTS.md:57,61
MECHANISM   verify_org_member · tenant-bound reload · admin gate
                                                   api/dependencies.py:46,78,138
CONTRACT    401 invalid · 403 foreign org · 404 guessed id
                                                   docs/API_AUTHORIZATION.md:21-24
CHECK       route policy vs. live routes; negative-path tests
                                                   tests/unit/test_api_route_auth_policy.py
EVIDENCE    command + counts + date + head SHA + limitations
                                                   docs/playbooks/validation.md
```

## 决策表

| 情形 | 答案 | 原因 |
|---|---|---|
| 请求他人的 id | `404` | 在操作者的租户内查找；他人的与不存在的看起来完全一样 |
| 操作者指定他人的组织 | `403` | 凭证有效，租户不对——这是策略拒绝 |
| bearer 令牌无效 | `401` | 凭证本身失败了 |
| 缺少 bearer 令牌 | `403`（mini-flow） | 已锁定并经过测试；SignUpFlow：文档 403，测试 401 |
| 某人带领一个事工 | `volunteer` + 资格 | 资格从不赋予权力 |
| 新增了路由却未归类 | 测试失败 | 与实时路由表做集合相等比较 |
| 场景尚未被证明 | 状态 `blocked` + `manual` 层级 | 删除这一行反而会让收集失败 |

## 留好这些命令和模板

```bash
make lab-m5      # baseline: 51 passed, 23 skipped — record first
make demo        # two LEAK lines before step 1; zero after
make step1 … step4        # red on the starter, then green
make step3       # miswire create_event → red; restore → green
make lab-m5      # delete MF-03 → Error 4; restore → green
make pass-gate   # 74 passed
```

```markdown
## Evidence — Lab M5 — <YYYY-MM-DD>
Commands (with results):
- <command> → <N passed, M skipped, K failed>
Induced failures recorded: <miswired route> · <removed scenario id>
Environment: <OS, Python version>   Revision: <git rev-parse HEAD>
Limitations / not verified:
- <at least one honest line>
```

## 要打开的指针

- `SignUpFlow/AGENTS.md:57-61` — P0 租户规则，以及「永远不要从请求体读取用户状态」。
- `SignUpFlow/api/dependencies.py:46-121` — 三个执行机制的原文。
- `SignUpFlow/api/roles.py:38-53` — `normalize_roles` 的拒绝逻辑。
- `SignUpFlow/api/route_auth_policy.py:8-171` — 五个类别，可执行矩阵。
- `SignUpFlow/tests/unit/test_api_route_auth_policy.py` — 缺失、过期、错接。
- `SignUpFlow/docs/API_AUTHORIZATION.md:101-118` — 六步变更协议。
- `SignUpFlow/docs/TESTING.md:38-50` — 七个层级，各自独立的进程。
- `SignUpFlow/docs/playbooks/coverage.json` + `tests/playbooks/coverage.py:19,43-46` — 清单。
- `SignUpFlow/tests/playbooks/examples/food-bank.json` — 最小的夹具形态。

## 三个坑

1. **在 Python 里过滤不等于隔离。** `[e for e in all_rows if e.org_id == ...]` 已经把另一个租户的数据行读进了你的进程。谓词应该写在查询里。
2. **一个你从未见过失败的漂移测试只是一种希望。** 先记录人为引发的红，再记录绿——错接*和*被移除的场景 id 都要如此。
3. **自我报告的「所有测试都通过」不是证据。** 没有命令、计数、日期、版本和局限，就没有证据。

## 满足以下条件，你就完成了……

- [ ] 每条 event 查询都带有租户谓词；`make demo` 显示零泄露。
- [ ] 七个负路径用例全部通过：自己的数据行 200、他人组织 403、猜测的 id 404、PATCH 404、
      无效令牌 401、缺少令牌 403、租户声明不匹配 401。
- [ ] 被禁止的写入被拒绝，**并且**尝试之后该行逐字节相同。
- [ ] `["volunteer","usher"]` 从邀请端点得到 `403`。
- [ ] 路由策略为每个已挂载路由归类；漂移测试抓住了一次故意的错接。
- [ ] 运营手册夹具和清单通过校验；移除一个必需 id 会让校验器失败。
- [ ] 至少有一个清单状态不是 `automated`，并附有原因。
- [ ] 证据条目包含命令、计数、日期、环境、head SHA 和一条局限。

**记住：** 查询里的过滤才是控制措施；一条警告日志只是可观测性。
