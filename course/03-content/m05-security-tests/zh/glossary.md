# 术语表 M5 — 多租户安全与验收关卡

按英文字母顺序排列。每个术语：先给定义，再给出处。

- **验收关卡（Acceptance gate）** — 产品必须被证明可运营、而不只是功能可用的检查点：运营手册场景、中断演练，以及一份承认尚未证明之行的清单。（`SignUpFlow/docs/playbooks/coverage.json`；`docs/playbooks/church.md`）
- **可执行授权矩阵（Authorization matrix (executable)）** — 一个把每个已挂载路由归类为 public/ member/ admin 的字典，配有一个测试，把字典与实时路由表以及每个路由的依赖树进行比较。（`SignUpFlow/api/route_auth_policy.py:8-171`；测试在 `tests/unit/test_api_route_auth_policy.py`）
- **跨租户数据泄露（Cross-tenant data leak）** — 一次未过滤的查询把另一个组织的数据行返回给一个合法的、已认证的用户；SignUpFlow 把它定为 P0 缺陷。（`SignUpFlow/AGENTS.md:57,61`）
- **覆盖清单（Coverage manifest）** — 一个机器可读的文件，把每个场景绑定到操作者、前提条件、操作、预期结果、层级、证据路径和一个状态；pytest 在收集之前校验它。（`SignUpFlow/docs/playbooks/coverage.json`；`tests/playbooks/plugin.py:37-45`）
- **覆盖状态（Coverage status）** — 恰好四个取值之一——`automated`、`partial`、`manual`、`blocked`——与层级相互耦合，因此 blocked 的行无法冒充 automated。（`SignUpFlow/tests/playbooks/coverage.py:19,43-46`）
- **中断演练（Disruption drill）** — 一个故意打破正常路径、并规定拒绝应当是什么样子的场景，例如 CH-04 中两位敬拜带领都不可用、发布被拒绝。（`SignUpFlow/docs/playbooks/church.md:73`）
- **证据记录（Evidence record）** — 一份带日期、绑定到具体版本的验证记录：命令及其结果、环境、head SHA，以及一份明确列出哪些未经验证的清单。（`SignUpFlow/docs/playbooks/validation.md`；模板见 `03-content/m01-operating-system/handout.md`）
- **独立判定器（Independent oracle）** — 一种检查，从产出的产物本身重新计算正确性，而不是去问产出者：角色人数精确、指派人员各不相同且合格、不重叠、负载均衡。（`SignUpFlow/docs/playbooks/README.md:37-38`）
- **仅限邀请的增长（Invitation-only growth）** — 注册以原子方式创建一个组织及其第一位管理员，且从不加入已有组织；后续账号通过管理员创建的一次性邀请加入。（`SignUpFlow/AGENTS.md:59`；`docs/playbooks/coverage.json` 中的 BO-02）
- **负路径测试（Negative-path test）** — 断言拒绝及其状态码、而不是成功情形的测试：即 `03-content/m05-security-tests/solutions.md` 第 1 步中的七个用例。（`SignUpFlow/docs/API_AUTHORIZATION.md:21-24`）
- **无 CI 本地验证（No-CI local validation）** — SignUpFlow 的既定策略：所有评审、测试和产物验证都在本地运行，证据记录在已推送的 head SHA 上，而不是依赖托管的检查。（`SignUpFlow/docs/ai-pr-review.md`；`tests/unit/test_local_validation_policy.py`）
- **最高级缺陷（P0 bug）** — SignUpFlow 给缺少 `org_id` 过滤定的严重级别：不在分诊中讨价还价，这样的查询不能上线。（`SignUpFlow/AGENTS.md:61`）
- **权限角色（Permission role）** — 一个账号可以做什么；恰好是 `admin` 或 `volunteer` 之一，由一个 frozenset 和一条拒绝两个角色的规范化规则强制执行。（`SignUpFlow/api/roles.py:8,38-53`）
- **资格（Qualification）** — 一个人能做什么（`usher`、`coach`、`worship_leader`、`sound`）；与权限角色存放在同一个 `roles` 数组中，但从不被解释为权力。（`SignUpFlow/api/roles.py:12`；`docs/playbooks/church.md:26`）
- **资源枚举（Resource enumeration）** — 通过观察错误码摸清哪些资源存在；对策是通过操作者的组织加载目标行，使他人的 id 和不存在的 id 都返回 `404`。（`SignUpFlow/docs/API_AUTHORIZATION.md:23`；`api/dependencies.py:61-66`）
- **已评审的提交 SHA（Reviewed head SHA）** — 本地评审及其证据所绑定的版本；源码一旦改变，旧证据就失效，必须重新检查。（`SignUpFlow/docs/ai-pr-review.md`，本地评审检查清单第 1 项和第 5 项）
- **绑定租户的凭证（Tenant-bound credential）** — 一个同时携带人员 `sub` 和 `org_id` 的 JWT 或会话，两者都必需，并在请求继续之前对照一个活跃的成员身份重新加载。（`SignUpFlow/api/dependencies.py:78-121`；`docs/API_AUTHORIZATION.md:28-33`）
- **测试层级（Test tier）** — 七种用途之一，各自在独立进程中运行：单元、API/安全、CLI、集成、Web、契约、浏览器。（`SignUpFlow/docs/TESTING.md:38-46,49-50`）

## 容易弄错的术语

- **权限角色与资格（Permission role vs. qualification）** — 权限角色决定权力；资格决定能否担任某个班次。它们共用一个 JSON 数组，除此之外毫无共同之处。
- **对他人 id 返回 403 还是 404（`403` vs. `404` for a foreign id）** — `403` 确认了资源存在；`404` 是防枚举的回答，因为查找发生在操作者的租户之内。
- **健康分与独立判定（Health score vs. oracle）** — 健康分是求解器给自己打分（有任何硬约束违规即为 0，否则为 `100 − soft/10`）；判定器则从排班表重新计算正确性。
- **blocked 与删除（`blocked` vs. deleted）** — `blocked` 是可见的剩余工作，必须带 `manual` 层级；删除这一行会让收集失败，那是一个无声的覆盖谎言。
- **本地验证与已验证本地（Local validation vs. verified local）** — 在本地运行一条命令是一个动作；已验证本地意味着命令、计数、日期、环境和 head SHA 都已记录。

## 精选资源

1. `SignUpFlow/AGENTS.md:57-61` — 每个智能体都会读的基线中的 P0 规则；转述之前先读原文措辞。
2. `SignUpFlow/docs/API_AUTHORIZATION.md` — 状态码契约、可执行矩阵和六步变更协议，都在这一个文件里。
3. `SignUpFlow/tests/unit/test_api_route_auth_policy.py` — 38 行代码，抓住缺失、过期和错接的路由；是本课程中最短的完整漂移测试。
4. `SignUpFlow/tests/playbooks/coverage.py` — 四种状态和两条耦合规则，让清单在构造上就是诚实的。
5. `SignUpFlow/docs/playbooks/church.md` — 一张真实的操作者表、一套每周运营节奏，以及 CH-01..CH-08 的验收标准。
6. `SignUpFlow/docs/TESTING.md` — 七层级表格，以及各层级在独立进程中运行的原因。
7. `SignUpFlow/docs/playbooks/validation.md` — 证据格式，外加一条降级横幅，展示一个数字如何随其日期一同退役。
8. `SignUpFlow/tests/playbooks/examples/food-bank.json` — 你可以为自己的实验夹具照搬的最小夹具形态。
