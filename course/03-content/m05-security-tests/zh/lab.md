# 实验 M5 — 隔离与验收
> AI Product Studio（APS-3）的一部分 · 第 5 模块的通过/不通过检查点 · 配套课程：`lesson.md`

## 目标

**用测试证明租户隔离，并设计运营手册验收。** 你最终会带走两件产物：（1）`mini-flow` FastAPI 应用，它的租户边界由真实 JWT 的负路径测试（negative-path test）强制保证——包括证明被禁止的写入不改变数据库——外加一份可执行的路由策略，以及一个可证明不授予任何管理员权限的资格字段；（2）一个运营手册 JSON 夹具（fixture）和一份列出必需场景、状态诚实的清单，由 pytest 在任何测试被收集之前完成校验。

## 前置条件

- 已完成第 4 模块：你的规格文件夹已经存在，并通过了需求检查清单。
- PATH 中有 Python 3.11+。
- **起始项目：** 本模块文件夹中的 `mini-flow/`。在其中运行 `make setup`（FastAPI、SQLAlchemy 2、Pydantic 2、PyJWT、httpx、pytest、pytest-cov——没有需要编译的依赖，也不需要数据库服务器）。
- 在 **SignUpFlow 本身**上完成 M4 的学员，可以改为扩展克隆下来的仓库——它的七层测试套件（`SignUpFlow/docs/TESTING.md`）就是你的回归安全网，`SignUpFlow/api/dependencies.py` 是参考实现。把它最涉及租户的两个资源对应到第 1–2 步上，并保持同样的证据格式。

## 时间

约 3 小时。第 0 步 15 分钟；第 1–2 步各约 40 分钟；第 3–4 步各约 35 分钟；证据和帖子 20 分钟。起始项目已经提供了应用、夹具和测试——你的时间花在读懂红色输出、修对那一行上，而不是花在搭脚手架上。

## 起始项目

`mini-flow/` 以实验的规模复刻了 SignUpFlow 的授权形态（它的 README 有逐个文件的说明）。三张表——`organizations`、`people`、`events`——每个人员行和活动行上都有 `org_id`；一个 `roles` JSON 数组，装着恰好一个权限角色加上任意资格；HS256 令牌携带 `sub` 和 `org_id`。`get_current_user` 按 `id AND org_id AND status == "active"` 重新加载人员（否则返回 401），`verify_org_member` 在明确指定他人组织时抛出 403，`get_person_in_actor_org` 对他人的*或*不存在的 id 返回 404——这正是 `SignUpFlow/docs/API_AUTHORIZATION.md:21-24` 的契约。

**起始项目是故意不完整的。** 每个实验步骤都以带 `@pytest.mark.lab(step=N)` 标记的测试形式提供。它们在 `make lab-m5` 中被跳过，由 `make stepN`（或通过关卡 `make lab-m5 STEPS=1,2,3,4`）取消跳过。每一步在出厂代码上都是红的，因为起始项目为每一步都埋了一个有名字的缺陷（README 中的“intentional gaps”表逐一列出）。你的任务不是写测试——而是读懂测试、修好应用，然后亲手弄坏自己的防护，并记录下红色结果。

## 步骤

**0. 运行基线，并复现泄露。** `make lab-m5` → 预期 `51 passed, 23 skipped`，覆盖率 100%。记录下来。然后运行 `make demo`，读那两行 `LEAK`：Tokyo 的管理员持有一个完全合法的 Tokyo 令牌，读取了 Grace 的活动并覆盖了它的标题。把这两行粘贴进你的证据日志——它们就是「修复前」。

**1. 按 `org_id` 隔离 events 路由（TDD）。** `make step1` → `2 failed, 4 passed`。打开 `mini-flow/tests/test_lab1_isolation.py`，读懂原因：`src/miniflow/routers/events.py` 在 `get_event` 和 `update_event` 中只按主键加载 `Event`。按照 `src/miniflow/routers/people.py` 对人员已经采用的方式修复——租户谓词要**写进查询**（`Event.org_id == actor.org_id`），他人的和不存在的都返回 404。`make step1` → `6 passed`。然后重新运行 `make demo`：零泄露，标题仍然是 `'Sunday rota'`。真正要紧的测试是 `test_foreign_admin_patch_is_denied_and_row_unchanged`：它用一个全新的会话给该行拍快照，以他租户管理员的身份尝试写入，断言 404，然后断言快照完全相同——这就是 SignUpFlow 变更协议的第 4 步，「断言被禁止的写入不改变数据库状态」（`SignUpFlow/docs/API_AUTHORIZATION.md:59-76`）。这里每个测试的鉴权都是真实的；「在集成测试中模拟数据库」是一个被点名的反模式（`SignUpFlow/AGENTS.md`）。

**2. 证明资格不授予任何权限。** `make step2` → `4 failed, 3 passed`。两个缺陷：`src/miniflow/dependencies.py` 中的 `check_admin_permission` 把管理员权限授予任何不是 `volunteer` 的角色——于是一个引座员可以发出邀请、创建活动、给自己升级权限——而 `src/miniflow/roles.py` 中的 `normalize_roles` 把 `"ADMIN"` 大小写折叠成 `admin`，而不是拒绝它。参考实现各只有一行：`SignUpFlow/api/dependencies.py:15-17`（当且仅当 `"admin" in roles` 时才是管理员）和 `SignUpFlow/api/roles.py:49`（`is an ambiguous permission role`）。`make step2` → `7 passed`。「不要仅仅因为某人带领一个事工就授予管理员权限」（`SignUpFlow/docs/playbooks/church.md:26`）。

**3. 补全路由策略，然后证明漂移测试真的咬人。** `make step3` → `1 failed, 3 passed`：`update_event` 已挂载，但在 `src/miniflow/route_auth_policy.py` 中未归类。为它归类（`admin`）→ `4 passed`。测试遍历**实时**路由表（`iter_route_contexts(app.routes)`），双向断言集合相等，然后遍历每个路由的依赖树：`admin` ⇒ `get_current_admin_user`，`member` ⇒ `get_current_user`，`public` ⇒ 两者都不依赖——这就是 `SignUpFlow/tests/unit/test_api_route_auth_policy.py` 的机制。**现在证明它有效：** 在 `src/miniflow/routers/events.py` 中，把 `create_event` 的依赖从 `get_current_admin_user` 改成 `get_current_user`，运行 `make step3`，记录红色结果（`AssertionError: create_event`）。改回来，再运行一次，记录绿色结果。一个你从未见过失败的漂移测试只是一种希望，而不是测试。

**4. 让清单在场景被移除时失败。** `make step4` → `4 failed, 2 passed`。夹具（`tests/playbooks/examples/food-bank.json`，即 SignUpFlow 自己的最小形态再加一个 PF-04 演练）和清单（`tests/playbooks/coverage.json`，四个状态诚实的场景）都已存在；`tests/playbooks/coverage.py` 中的校验器只检查 JSON 形态。按照 `SignUpFlow/tests/playbooks/coverage.py:42-46` 的形态加上三样东西：`ScenarioCoverage` 上的状态/层级耦合校验器（`automated`/`partial` 需要一个可执行层级；`manual`/`blocked` 需要 `manual` 层级）、`load_coverage_manifest` 中的 `REQUIRED_SCENARIOS` 检查，以及一项交叉检查，确保夹具中的每个演练都有对应的清单行。`make step4` → `6 passed`。**然后现场演示：** 从 `coverage.json` 删除 `MF-03` 行，运行 `make lab-m5`，看着收集在任何测试运行之前就终止——`ERROR: Invalid playbook coverage manifest …: missing required scenarios ['MF-03']`——与 `SignUpFlow/tests/playbooks/plugin.py:37-45` 相同的收集前失败。把这一行恢复。最后，让清单重新变得诚实：MF-02 和 MF-03 之前是 `blocked`，因为它们的测试被跳过了；既然它们现在是绿的，就把它们设为 `automated`，并以测试 id 作为证据。PF-04 保持 `manual`——mini-flow 没有求解器，清单必须如实说明。

**5. 通过关卡。** `make pass-gate` → `74 passed`，覆盖率 100%。连同日期、你的环境和 `git rev-parse HEAD` 一起记录下来。

## 验收清单（必须全部满足）

- [ ] 在任何改动**之前**记录了 `make lab-m5` 的绿色结果（`51 passed, 23 skipped`，覆盖率 100%），并把 `make demo` 的两行 `LEAK` 作为「修复前」粘贴进来。
- [ ] 第 1 步为绿：对活动的他租户读取和他租户 PATCH 都返回 404；修改前后的行快照断言通过；`make demo` 显示零泄露。
- [ ] 第 2 步为绿：`["volunteer", "usher"]` 在邀请、创建活动和自我升级权限时都得到 403；`normalize_roles(["ADMIN"])` 抛出 "ambiguous"。
- [ ] 第 3 步为绿：每个已挂载路由都已归类；人为错接 `create_event` 产生了一次红色运行，**并且**恢复后产生了一次绿色运行——两者都已粘贴。
- [ ] 第 4 步为绿：从 `coverage.json` 移除 `MF-03` 会让运行在收集之前终止——错误行已粘贴——并且恢复后的运行为绿。
- [ ] 清单状态是诚实的：MF-02 和 MF-03 现在是 `automated`，以测试 id 作为证据；PF-04 仍是 `manual`，并附有原因。
- [ ] `make pass-gate` → `74 passed`，覆盖率 ≥ 90，连同日期、环境和 head SHA 一起粘贴。
- [ ] 证据按第 1 模块的格式记录，并至少包含一条你尚未证明的局限。

## 证据记录

按照 M1 的证据格式：每条命令及其通过/失败计数、日期、你的环境、head SHA 和局限。包括修复*之前*的四次 `make stepN` 红色运行、两次人为引发的失败（错接的 `create_event`、被移除的 `MF-03`）及其红色输出，以及两次 `make demo` 运行。这些失败演示*本身*就是你的防护有效的证据。最后写一条你尚未证明的局限（例如「隔离只在 API 层级得到证明——没有浏览器层级；PF-04 是 manual，因为没有求解器」）。

## 拓展目标

- **双租户浏览器检查（BO-12 模式）：** 加一个最小的 HTML 界面，在一个应用中运行两个租户，用 Playwright 在 **360px 和 1440px** 下测试；每个管理员只能看到自己的目录（`SignUpFlow/docs/playbooks/README.md`，BO-12）。
- **把一个 CH 演练移植到你的领域：** 例如 CH-05（邀请一位合格的替补 → 空缺被填补，且没有用其他资格代替），作为第二个 `drills` 条目，并把它的清单行如实标为 `manual`。
- **你自己的 SaaS：** 针对你第 4 模块规格中最涉及租户的两个资源重复第 1–3 步，复用 `tests/support.py` 的快照模式。

## 讨论题

用以下模板发到社区：

> **实验 M5 — [你的名字]**
> 我最庆幸自己保留下来的红色运行：[错接或移除场景的失败，粘贴]
> 这次失败证明了什么：[一句话]
> 我的清单中诚实的状态：[一个状态 ≠ automated 的场景，以及原因]
