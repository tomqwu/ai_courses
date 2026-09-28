---
marp: true
theme: aps
paginate: true
title: M5 — 多租户安全与验收关卡
---

# M5 — 多租户安全与验收关卡

**承诺：** 先用测试证明租户隔离，再证明产品可运营。
**时长：** 约 75 分钟讲授 + 约 3 小时实验 M5。
**案例研究：** SignUpFlow · `api/dependencies.py`、`docs/playbooks/coverage.json`

```figure
kind: architecture
alt: 许多租户共用一个数据库；本模块最后产出两件产物——证明隔离的负路径测试，以及一份承认尚未证明之处的运营手册清单。
source: SignUpFlow/api/dependencies.py · SignUpFlow/docs/playbooks/coverage.json
layer: 一个数据库，多个租户 @ 你的案例研究是 SignUpFlow
  box: 一个教会组织
  box: 一个篮球联赛组织
  box: 每条查询都带 org_id (seam)
layer: 你将拿到的产物 (hl) @ 学完本模块，你会拿到
  box: 负路径测试 — 隔离，已证明
  box: 运营手册清单 — 承认尚未证明之处
```

<!-- NOTES: 欢迎来到第 5 模块，这是 SaaS 路线的安全与验收关卡。今天的一切都围绕两个问题。第一：一个租户是否可能看到另一个租户的数据？第二：你如何证明整个产品在运营层面可用，而不只是功能上可用？案例研究是 SignUpFlow——一个多租户的志愿者排班 API，教会和篮球联赛共用同一个数据库。承诺是一对产物：证明隔离的负路径测试，外加一份承认尚未证明之处的运营手册清单。时间安排：M5.1 约 25 分钟，M5.2 约 25 分钟，M5.3 约 25 分钟，然后是三小时的实验。过渡：下面就是你将能做到的事。 -->

---

## 学完本模块，你能够……

- 用依赖项**强制实施**租户隔离
- 把令牌**绑定**到租户，重新加载活跃记录
- 有意识地**确定** 401/403/404 语义
- 把权限角色与资格**分离**
- 把授权矩阵**做成**可执行的
- **设计**验收：测试层级、运营手册、诚实的清单

<!-- NOTES: 把这些读成六个动词，而不是六个主题。每一个都是你在实验中要做的事。强制实施、绑定、确定、分离、落实、设计。前三个是隔离的纪律；中间两个是授权的纪律；最后一个是验收的纪律。注意贯穿始终的主线：智能体以机器的速度生成查询，而每一条生成的查询都可能漏掉租户过滤。所以答案不是「小心一点」——而是机器能检查的规则，以及能抓住漂移的测试。如果你只记住一张幻灯片，就记住下一张的 P0 规则。过渡：从规则本身开始。 -->

---

## M5.1 — 规则写在 `AGENTS.md` 里

```figure
kind: compare
alt: 一条智能体能检查的规则——每条查询都按 org_id 过滤，缺少过滤就是 P0 级泄露——对比一句谁也无法验证的空话。
source: SignUpFlow/AGENTS.md:57,61
column: 一条检查 (good) @ 每一条数据库查询都必须按
  item: 每一条数据库查询都必须按 `org_id` 过滤
  item: 缺少过滤就是跨租户泄露
  item: 把它当作 P0 缺陷处理
column: 一种感觉 (bad) @ 而且措辞很重要
  item: 「多租户要小心」
```

- 每个智能体写查询之前都会读到的基线。

`SignUpFlow/AGENTS.md:57,61`

<!-- NOTES: 在屏幕上打开 `AGENTS.md`，把第 57 行和第 61 行大声读出来。注意它放在哪里：不是安全 wiki，而是 Codex CLI、Cursor、Aider、Jules、OpenHands、Sourcegraph Amp 和 Factory 都会原生读取的跨智能体基线。这个位置正是关键——每个为了写查询而打开仓库的智能体，都会先读到这条 P0 规则。再注意措辞。「每条查询都按 `org_id` 过滤」是一条检查。「多租户要小心」只是一种感觉。文化规则只有具体到这种程度才起作用。P0 缺陷不是你在分诊时讨价还价的严重级别：那条查询不能上线。过渡：规则需要机制，否则只是装饰。 -->

---

## M5.1 — 三个机械化的执行机制

```figure
kind: system
alt: 一个请求穿过 SignUpFlow 的租户边界——解码 JWT，按 id、org_id 和活跃状态重新加载人员；管理员路由再加一道角色检查；路由检查路径中的组织；每条查询都按 org_id 过滤；任何一步失败都在触碰数据之前返回 401 或 403。
source: SignUpFlow/api/dependencies.py:46-160 · SignUpFlow/api/routers/people.py:271-274
layer: 请求
  node req: Bearer JWT — 声明：sub + org_id
layer: api/dependencies.py (seam) @ 一个文件里有三个执行机制
  node user: get_current_user — 按 id、org_id 和活跃状态重新加载 @ 一个文件里有三个执行机制
  node admin: get_current_admin_user — 角色必须是 admin @ 其他任何情况都是 401
layer: 路由
  node member: verify_org_member — person.org_id == 路径中的 org_id @ 一个文件里有三个执行机制
  node query: 每条查询 — 按 org_id 过滤 (hl)
layer: 结果
  node db: 该租户自己的数据行
  node deny: 401 · 403 — 什么都没碰
edge: req -> user — 身份只来自凭证 (hl) @ 有一行让这一切变得安全
edge: user -> admin — 管理员路由 @ 其他任何情况都是 401
edge: user -> member
edge: member -> query — 同一组织
edge: query -> db
edge: user -> deny — 401：令牌无效，或无此记录 @ 其他任何情况都是 401
edge: member -> deny — 403：他人的组织
edge: admin -> deny — 403：不是管理员 @ 其他任何情况都是 401
```

- 身份只来自凭证。
- 「永远不要从请求体读取用户状态。」

`SignUpFlow/api/dependencies.py:46,78,138` · `SignUpFlow/AGENTS.md:58`

<!-- NOTES: 一个文件，三个执行机制。`verify_org_member(person, org_id)` 比较 `person.org_id != org_id`，不一致就抛出 403，消息是 "Access denied: not a member of this organization"，见第 46 到 58 行。`get_current_user` 解码 JWT，要求带有 `sub` 和 `org_id` 两个声明，然后用三重过滤重新加载这个人：id、租户和活跃状态——其他任何情况都是 401，所以令牌只是*指向*一行记录，这行记录必须仍然存在、仍然属于该租户。`get_current_admin_user` 包装了它，除非角色是 admin，否则抛出 403。让这一切变得安全的是 AGENTS.md 的第 58 行：永远不要从请求体读取用户状态。请求体是攻击者可控的输入。过渡：id 对不上时，你返回什么？ -->

---

## M5.1 — 有意设计的状态码语义

| 情形 | 状态码 |
|---|---|
| bearer 令牌无效 | `401` |
| 受保护路由缺少 bearer 令牌 | 文档 `403`；运行时和测试 `401` |
| 已认证的操作者指定他人的组织 | `403` |
| 猜测的资源标识符 | `404` |

`SignUpFlow/docs/API_AUTHORIZATION.md:21-24`

<!-- NOTES: 四行，每一行都是决定，而不是偶然。bearer 令牌无效返回 401，因为凭证本身失败了——对请求者一无所知。缺少 bearer 令牌是发生漂移的那一行：文档写的是 HTTPBearer 的 403，但在锁定的 FastAPI 0.141.1 上，HTTPBearer 返回 401，SignUpFlow 自己的边界测试也断言 401。测试跟上了，文档没有。mini-flow 明确锁定 403，所以无论选哪个，它的选择都写了下来，也经过测试。明确指定他人组织返回 403：凭证有效，租户不对，是策略拒绝。最后一行最重要：猜测的资源标识符返回 404。把这一点记到下一张幻灯片。过渡：为什么是 404，而不是 403？ -->

---

## M5.1 — 枚举止于 `404`

- 目标**先通过操作者的组织**加载。
- 他人的资源与不存在的资源看起来完全一样。
- 统一返回 `403` 反而会确认资源存在。

```python
def get_person_in_actor_org(person_id: str, actor: Person,
                            db: Session) -> Person:
    """Load a person only through the authenticated actor's tenant."""
    person = db.query(Person).filter(
        Person.id == person_id, Person.org_id == actor.org_id).first()
    if person is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Person not found")
    return person
```

`SignUpFlow/api/dependencies.py:61-66`

<!-- NOTES: 这就是防枚举机制，它只是一种查询形态。`get_person_in_actor_org` 在 WHERE 子句里同时带上 id 和操作者的组织来加载目标行，匹配不到就抛出 404。所以一个他人的人员和一个不存在的人员得到同样的回答：查无此项。如果他人的 id 返回 403——「存在，但不是你的」——一个拥有完全合法账号的攻击者就可以遍历你的 id 空间，摸清有哪些资源存在。可用时间路由用的是同一个模式：同租户的同事得到 403，他人的或不存在的人员得到 404。要学的不是哪个状态码在哲学上正确；而是一个没有写进文档的状态码就是一条未经规定的信息通道。过渡：一开始，任何人是怎么进入一个租户的？ -->

---

## M5.1 — 增长只能通过邀请

- `POST /auth/signup` 同时创建组织**和**第一位管理员。
- 它从不加入已有组织。
- 没有创建空组织的公开端点。
- 后续账号需要一次性邀请。
- 资格从不授予管理员权限。

`SignUpFlow/AGENTS.md:59` · `docs/playbooks/coverage.json`（BO-02）

<!-- NOTES: 租户关系在创建账号时就封闭了。注册以原子方式创建一个新组织及其第一位管理员，AGENTS.md 写得很明确：永远不要用它加入已有组织；后续账号需要邀请。反面同样重要——没有任何公开端点能创建空组织，所以陌生人无法把自己插进你的租户。增长在构造上就只能通过邀请，覆盖清单中的 BO-02 把这条规则固定下来：邀请只能使用一次，资格不授予管理员权限。过渡：最后这句话就是 M5.2 的全部内容——权限与资格。 -->

---

## 证明 M5.1 — 可以 grep 到的规则

- `SignUpFlow/AGENTS.md:57` — `org_id` 规则。
- `SignUpFlow/AGENTS.md:61` — 它的 P0 分级。
- `SignUpFlow/api/dependencies.py:46-66` — 成员身份查找。
- `SignUpFlow/api/dependencies.py:78-121` — 绑定租户的重新加载。
- `SignUpFlow/docs/API_AUTHORIZATION.md:21-24` — 状态码各行。

```text
- Every database query MUST filter by `org_id`. …
- …
- A missing `org_id` filter is a cross-tenant data leak.
  Treat it as a P0 bug.
```

<!-- NOTES: 这是 M5.1 分段的证明幻灯片，现在就把这五个指针写进你的证据日志——它们是你在实验中所有主张的出处。要学的模式是：规则写在基线里，机制写在依赖项里，契约写在授权文档里，每一项都有测试。当你为自己的项目写租户章节时，你照搬的是这个四段式的形态，而不是文字。提醒一点：一条警告缺少过滤的日志只是可观测性；查询里的过滤才是控制措施。过渡：接下来是共用一个 JSON 数组的两套词汇。 -->

---

## M5.2 — 两套词汇，一个数组

```figure
kind: architecture
alt: 一个 roles 数组装着两套毫不相干的词汇——决定账号能做什么的权限角色，以及求解器用来填补空位的资格。
source: SignUpFlow/api/roles.py:8
layer: 权限角色 — 账号可以做什么；恰好一个 @ 权限角色描述
  box: admin
  box: volunteer
layer: 资格 — 一个人能做什么；求解器据此填补空位 @ 资格描述
  box: usher
  box: coach
  box: worship_leader
  box: sound
```

- 同一个 `roles` 数组——但含义从不相通。
- 资格从不授予管理员权力。

`SignUpFlow/api/roles.py:8` · `docs/playbooks/church.md:26`

<!-- NOTES: 一个 Person 带有一个 roles 数组，里面放着两种毫不相干的字符串。权限角色是一个账号*可以做*什么，恰好有两个：admin 和 volunteer，由 api/roles.py 第 8 行的 frozenset 强制执行。资格是一个人*能做*什么——usher、coach、worship_leader——求解器用它们填补角色空位。它们共用数组；但从不共享含义。陷阱来自自然语言：「她带领敬拜，所以应该给她打开管理员开关。」Church.md 用一句话拒绝了它：不要仅仅因为某人带领一个事工就授予管理员权限。它的操作者表把敬拜协调人列为 volunteer 加 worship_leader，而不是 admin。过渡：这条策略不是散文——它是可执行的。 -->

---

## M5.2 — 漂移的输入会大声失败

- 精确匹配 → 权限角色；其余一律 → 资格。

```python
def normalize_roles(roles: Iterable[str]) -> list[str]:
    """Validate an admin-selected role array and
    make account access explicit."""
    # …
        if value.casefold() in PERMISSION_ROLES:
            raise ValueError(
                f"{value!r} is an ambiguous permission role")
        # …
    if len(permission_roles) > 1:
        raise ValueError("Select exactly one account access role")
    # …
```

`SignUpFlow/api/roles.py:38-53`

<!-- NOTES: 打开 `api/roles.py`，把 `normalize_roles` 从头读到尾。数据形态容纳两套词汇；策略让它们互不相交。与 `PERMISSION_ROLES` 精确匹配的是权限角色；其余都是资格——但像 "ADMIN" 这样经大小写折叠后冲突的值会抛出异常，多于一个权限角色则抛出 "Select exactly one account access role"。这就是设计原则：漂移的输入要大声失败，而不是悄悄提权。静默的规范化正是资格变成特权的途径。过渡：知道规则还不够——每一个挂载的路由都必须遵守它们。 -->

---

## M5.2 — 让授权矩阵可执行

- `api/route_auth_policy.py` 为每个路由归类，共五类。
- `public` 7 · `public-token` 6 · `public-callback` 4。
- `member` 50 · `admin` 78。
- `ROUTE_AUTH_POLICY` 是可执行的唯一事实来源。
- 文档描述意图；字典把意图编码下来。

`SignUpFlow/api/route_auth_policy.py:8-171` · `docs/API_AUTHORIZATION.md:3`

<!-- NOTES: 这是 M5.2 的核心。`api/route_auth_policy.py` 列出每一个 FastAPI 操作，并把它归入五个策略类别中的恰好一个。在当前克隆中的数量是：7 个公开操作、6 个限定范围令牌操作、4 个公开回调、50 个成员操作和 78 个管理员操作。第 168 行的 ROUTE_AUTH_POLICY 字典是可执行的唯一事实来源，`docs/API_AUTHORIZATION.md` 开篇就是这么说的。只用散文写成的矩阵，在第一次有人新增路由时就会腐烂；字典加一个测试就不会。过渡：下面就是让它保持正确的那个测试。 -->

---

## M5.2 — 三类漂移

- **缺失：** 有路由却没有策略条目
- **过期：** 有策略条目却没有路由
- **错接：** 策略写的是 `admin`，路由用的却是 `get_current_user`

- 测试遍历 `app.routes`，断言集合相等。
- 再遍历每个路由的依赖树。

`SignUpFlow/tests/unit/test_api_route_auth_policy.py`（38 行）

<!-- NOTES: 强制执行只有 38 行，却能抓住三类失败。缺失和过期都是策略字典与实时路由表之间的集合相等比较：新增路由却不归类，断言失败；给已删除的路由留着条目，它会反向失败。错接是最隐蔽的一类——对每个已归类的路由，测试收集它依赖树中的名字，并断言管理员路由依赖 `get_current_admin_user`，成员路由依赖 `get_current_user`，公开路由两者都不依赖。如果策略条目写的是 admin，而路由不小心接上了成员依赖项，这会被机械地抓住。过渡：在你亲眼看到它失败之前，这个测试只是一种希望。 -->

---

## 证明 M5.2 — 矩阵 + 关卡 + 协议

```python
"""Reviewed authentication policy for every mounted API operation.

The policy is deliberately keyed by FastAPI operation name. A unit
test compares this mapping with the live route table, so a new API
route cannot ship without an explicit public, token, member, or
administrator classification.
"""
```

- 矩阵：`SignUpFlow/api/route_auth_policy.py:1-171`
- 关卡：`SignUpFlow/tests/unit/test_api_route_auth_policy.py`
- 协议：`SignUpFlow/docs/API_AUTHORIZATION.md:101-118`

<!-- NOTES: M5.2 的证明幻灯片。打开文件时自己数一数类别——五个集合，总共 145 个操作。授权文档末尾的六步协议，就是你要写进自己贡献指南的内容：修改策略条目，在路由查询本身中应用由操作者推导出的过滤，为匿名、无效、成员、同租户管理员和他租户管理员添加真实 JWT 测试，断言被禁止的写入不改变数据库，刷新 OpenAPI 快照，然后在本地运行矩阵和排班回归测试。协议最后一条规则堵死了捷径：不要把租户警告监听器当作授权。过渡：第四步是团队常常跳过的一步，而 M5.3 讲的就是如何证明这类事情。 -->

---

## M5.2 — 六步变更协议

<!-- _diagram: steps -->

1. 更新该路由的策略条目。
2. **就在查询本身中**按租户过滤。
3. 为五类操作者添加真实 JWT 测试。
4. 断言被禁止的写入不改变数据库。
5. 刷新 OpenAPI 快照和客户端。
6. 在本地运行矩阵和排班回归测试。

`SignUpFlow/docs/API_AUTHORIZATION.md:101-118`

<!-- NOTES: 把这些当作可以粘贴进拉取请求模板的检查清单来读。第二步正是捷径藏身之处——在路由查询本身中应用由操作者推导出的租户与所有权过滤，而不是放在一个你希望会被调用的辅助函数里。第三步列出五类操作者：匿名、无效、成员、同租户管理员和他租户管理员。第四步是大多数团队会跳过的一步：被拒绝的写入如果仍然改动了数据库，那就是一个披着测试全绿外衣的安全缺陷，所以要断言拒绝，*也*要断言那一行没有变化。第六步在本地进行，因为 SignUpFlow 不运行 CI。过渡：这就把我们带到了验收——七个层级和一份诚实的清单。 -->

---

## M5.3 — 七个层级，各自独立的进程

```figure
kind: architecture
alt: SignUpFlow 的七个测试层级，每一层都证明其他层证明不了的东西；浏览器层级在独立进程中运行，因为它的事件循环不同。
source: SignUpFlow/docs/TESTING.md:38-46
layer: 进程内的层级
  box: 单元 — 模拟鉴权 @ 单元测试是快速的
  box: API — 真实 JWT，真实 HTTP (hl) @ API 与安全层级
  box: CLI — YAML 输入，JSON 输出 @ CLI 层级
  box: 集成 — 真实数据库 @ 集成测试使用真实数据库
  box: Web — cookie 和 HTMX @ Web 层级在进程内覆盖
  box: 契约 — OpenAPI 快照 @ Web 层级在进程内覆盖
layer: 独立进程 (seam) @ 它们在各自独立的进程中运行
  box: 浏览器 — 在可丢弃的实时应用上运行 Playwright
```

- 不要把 API 层级和浏览器层级放在同一个进程里。

`SignUpFlow/docs/TESTING.md:38-46,49-50` · `make test-all`

<!-- NOTES: 七个层级，每一个都证明其他层级证明不了的东西。单元层级是使用模拟鉴权的快速回归测试。API 与安全层级在隔离的 SQLite 上用真实 JWT 跑真实 HTTP——你的隔离测试就放在这里。CLI 层级证明无界面的路径；集成层级使用真实数据库，在这里模拟数据库是 AGENTS.md 中被点名的反模式。Web 层级在进程内覆盖 cookie 和 HTMX；契约层级对 OpenAPI 兼容性做快照；浏览器层级用 Playwright 测试一个可丢弃的实时应用。它们在各自独立的进程中运行，因为 API 与浏览器的事件循环夹具不同——`make test-all` 把它们分开，遇到失败即停止。过渡：记录下来的证据是什么样子的？ -->

---

## 证明 M5.3 — 带日期的证据，以及退役计划

```text
# Acceptance evidence - 2026-09-12

> Historical reference. Reclassified on 2026-09-13; the original
> observations, counts, timing estimates, commands, and CI proposals
> below are retained as historical context, not current policy or
> live test status. Use the [current testing and merge guide](…)
> and the repository README instead.
```

- `SignUpFlow/docs/playbooks/validation.md:1-6` — 横幅。
- `:88` — 四个套件合计 "1,464 passed, 21 skipped"。
- `:36` — 完整单元层级："399 passed, 21 skipped"。

<!-- NOTES: 这里是你可以引用的数字，以及引用它的确切方式。在 `docs/playbooks/validation.md` 中，日期为 2026-09-12，记录的全套件证据是后端、Web、契约和浏览器套件合计 "1,464 passed, 21 skipped"；仅完整的单元层级就是 "399 passed, 21 skipped"。现在读第 3 行的横幅：该文件在 2026-09-13 被重新归类为历史参考，"not current policy or live test status"，而 `docs/TESTING.md` 才是当前有效的。带日期的证据是证据。带日期*且*有退役计划的证据才是纪律。永远不要把 1,464 当作今天的状态来引用。过渡：测试层级证明机器能运转；运营手册证明产品能被运营。 -->

---

## M5.3 — 运营手册验收：测试失败模式

- 两段为期六周的旅程：教会和篮球。
- 操作者表：管理员、志愿者 + 资格、人。
- 中断演练 CH-01..CH-08，各带验收标准。
- CH-04：两位敬拜带领都不可用，尝试发布。
- 验收：发布**被拒绝**，之前的排班表保持生效。

`SignUpFlow/docs/playbooks/church.md:14-24,73`

<!-- NOTES: 测试层级证明机器能运转；运营手册证明产品能被运营。`docs/playbooks/` 提供两个为期六周的运营场景。Church.md 的操作者表迫使每个操作者归入管理员、志愿者加资格，或明确由人承担——事工审批人是 "Human organizational responsibility"，而不是新的权限级别。旗舰演练是 CH-04：把第 4 周周日的两位敬拜带领都设为不可用，然后尝试发布。验收标准是：恰好是那一场礼拜报告缺少带领，发布被拒绝，之前的排班表保持生效。读懂它测的是什么：不是正常路径，而是一种失败模式。关于拒绝的验收标准，正是演示和产品的分界线。过渡：这些场景是数据，所以测试可以运行它们。 -->

---

## M5.3 — 夹具为真实测试提供参数

- `docs/playbooks/church.json` 声明领域、角色和人数。
- 每场活动七位不同的人员。
- pytest 插件发现夹具；`--playbook` 负责选择。
- API 层级：真实 JWT，隔离的内存 SQLite。
- 浏览器层级：真实应用，宽度 **360px 和 1440px**。

`SignUpFlow/docs/playbooks/church.json` · `tests/playbooks/plugin.py` · `README.md:28-42`

<!-- NOTES: 这些场景之所以可执行，是因为它们是数据。`church.json` 声明了领域、工作流、活动、角色人数映射、次要活动、关键角色和演练选择器。一个 pytest 插件发现这些文件，用稳定的 ID 参数化测试，并支持 `--playbook` 和 `--playbook-dir`。API 层级用真实的 JWT 身份在隔离的内存 SQLite 上运行它们；浏览器层级在临时数据库上以 360 和 1440 像素宽度启动真实应用。每场活动七位不同的合格人员，是这个夹具的承诺。过渡：那么，谁来检查求解器是否兑现了这个承诺？ -->

---

## M5.3 — 独立判定器，而不是自我报告

- 判定器从发布的排班表重新计算正确性。
- 角色人数精确，指派人员各不相同且合格。
- 不重叠；可互换人员的负载相差不超过一。
- 健康分 = 有硬约束违规时为 0，否则为 100 − 软约束分/10。
- 求解器不能给自己的作业打分。

`SignUpFlow/docs/playbooks/README.md:37-38` · `api/core/solver/heuristics.py:321-323`

<!-- NOTES: 每一次求解都由一个独立判定器检查，而*独立*是承重的那个词。判定器从排班表本身重新计算正确性：角色人数精确、指派人员各不相同且合格、同一个人不会占用同一场活动的两个位置、没有时间重叠，并且可互换人员的基准负载相差不超过一。它从不去问求解器自己干得好不好——这很重要，因为求解器自己的指标简单得近乎粗暴：只要存在任何硬约束违规，健康分就是零，否则是一百减去软约束分除以十。自己报告的分数不是判定器。过渡：接下来是把这一切绑在一起的清单。 -->

---

## M5.3 — 清单在构造上就是诚实的

- `docs/playbooks/coverage.json` — 35 行，全部为 `automated`。
- 四种状态：`automated`/`partial`/`manual`/`blocked`。
- `automated`/`partial` 必须引用一个可执行层级。
- `manual`/`blocked` 必须包含 `manual` 层级。
- blocked 的行无法冒充 automated。

`SignUpFlow/tests/playbooks/coverage.py:19,43-46` · `SignUpFlow/docs/playbooks/README.md:84-87`

<!-- NOTES: `coverage.json` 把每个场景绑定到操作者、前提条件、操作、预期结果、层级、证据路径和一个状态。状态共有四种，两条耦合规则让不诚实在结构上很难成立：automated 或 partial 行必须包含一个可执行层级，manual 或 blocked 行必须包含 manual 层级。所以一个 blocked 的场景*不可能*被伪装成 automated。在当前清单中，全部 35 行内置场景都是 automated，其中四行同时带有 manual 层级——所以保留的那些状态是用来承认尚未证明之处的词汇。Church.md 的解读很准确：partial 或 blocked 行是剩余工作，而不是已通过的场景。过渡：而且校验器在收集之前就运行。 -->

---

## M5.3 — 校验发生在收集之前

- 插件的 `pytest_configure` 加载并交叉检查清单。
- 任何 `ValueError` 都会变成 `pytest.UsageError`。
- 在任何一个测试执行之前，这次运行就终止了。
- 共享场景必须恰好是 BO-01..12。
- 移除一个必需场景 → 收集失败。

`SignUpFlow/tests/playbooks/plugin.py:37-45` · `tests/playbooks/coverage.py:87-155`

<!-- NOTES: 清单在收集之前就被校验，这是值得照搬的细节。插件的 `pytest_configure` 钩子加载清单并交叉检查它；任何 ValueError 都会变成 pytest.UsageError，所以在任何一个测试执行之前，这次运行就终止了。这些校验器是结构性的，而不是装饰性的：共享场景必须恰好是 BO-01 到 BO-12，每个领域必须恰好包含 CH-01 到 CH-08 以及领域演练，每个领域必须声明恰好一个管理员操作者和至少一个人的职责边界。移除一个内置领域、必需场景、管理员、边界或资格，收集就会失败。范围不可能悄悄缩小。过渡：现在是你的实验。 -->

---

## 实验 M5 — 隔离与验收

- **构建：** 三张表、JWT、每一行都带 `org_id`。

<!-- _diagram: steps -->

- 隔离测试 + 被禁止的写入不改变数据库。
- 资格被证明不带任何管理员权限（403）。
- 路由策略 + 漂移测试；先看到红。
- 夹具 + 清单 + 校验器；先看到红。

- **通过关卡：** 所有负路径全绿；两次人为引发的失败都已记录。

`03-content/m05-security-tests/lab.md` · `SignUpFlow/tests/playbooks/examples/food-bank.json`

<!-- NOTES: 实验 M5 只分通过和不通过，大约三小时，共四步。你要构建一个最小的 FastAPI 应用，包含三张表——organizations、people、events——以及 JWT 鉴权。第一步用真实 JWT 测试证明隔离，其中包括大多数团队会忘掉的那条断言：给目标行拍快照，尝试被禁止的写入，断言被拒绝，重新读取，断言该行完全相同。第二步把资格存进 roles 数组，并证明带有 usher 资格的志愿者无法发出邀请。第三步构建路由策略和漂移测试，你必须故意错接一个路由，在修复之前记录下红色的运行结果。第四步参照 `tests/playbooks/examples/food-bank.json` 编写一个运营手册夹具，外加清单和校验器，你还必须移除一个必需的 id，并同样记录那次失败。一个你从未见过失败的漂移测试只是一种希望，而不是测试。过渡：快速做一下测验。 -->

---

## 测验 M5 — 六道选择题，两道简答题

- P0 严重级别 · 权限与资格
- 枚举与 `404` 的决定
- 漂移测试实际比较的是什么
- 层级的对应关系与独立判定器
- 清单的诚实 · 被遗忘的断言

`03-content/m05-security-tests/quiz.md`

<!-- NOTES: 八道题，六道选择题，两道简答题。选择题的干扰项正是我们在课上纠正的误解：认为 403 比 404 更安全，认为资格意味着信任，认为 SQLAlchemy 会自动加上租户过滤，认为七个层级都在一个进程里运行。第八题最好在提交前先起草：写出一组断言序列，证明志愿者 A 不能编辑志愿者 B 的可用时间，并且 B 的记录没有改变。按顺序写出每一条断言、状态码，以及大多数团队会忘掉的那一条断言。提示：它涉及一次被禁止的写入和一行没有变化的记录。过渡：回顾。 -->

---

## 回顾

- **M5.1** — P0 规则 + 三个执行机制 + 以 404 防枚举。
- **M5.2** — 一个权限角色；资格从不赋予权力。
- **M5.2** — 策略字典可执行；测试抓住漂移。
- **M5.3** — 七个层级在独立进程中运行；带日期的证据会退役。
- **M5.3** — 运营手册测试拒绝；判定器是独立的。
- **M5.3** — 清单状态相互耦合；校验先于收集。

<!-- NOTES: 六行、三个分段、一条主线。M5.1：规则写在每个智能体都会读的基线里，三个机制强制执行它，猜测的 id 返回 404，于是枚举失效。M5.2：恰好一个权限角色，资格共用数组但从不赋予权力，授权矩阵是一个由测试与实时应用比对的字典。M5.3：七个层级各自证明不同的东西，运营手册的验收标准关乎拒绝，判定器从排班表重新计算，清单在收集之前就被校验。主线是：智能体以机器的速度生成查询，所以防护也必须是机械化的。过渡：讨论题是你把它用到自己产品上的地方。 -->

---

## 讨论题

- 你的产品为多个客户存储数据。
- 一位同事说：「有外键就够了——不需要组织过滤。」
- 用**三个** SignUpFlow 文件指针回复。
- 指出没有过滤时失效的机制。
- 指出猜测的他人 id 应返回的状态码。
- 指出你会写的第一条测试断言。

<!-- NOTES: 发到社区，约 150 字。一位同事认为，带外键的 ORM 就够了，不需要在每条查询上加组织过滤。写出你的回复。至少使用三个 SignUpFlow 文件指针——P0 规则、强制执行成员身份的依赖项，以及状态码契约，是最明显的三个。指出没有过滤时失效的机制、猜测的他人 id 应当返回的状态码及其原因，以及你会最先写的那条测试断言。课程里的提示是：它涉及一次被禁止的写入和一行没有变化的记录。这就是本模块要培养的习惯——一个以检查收尾的论证。 -->
