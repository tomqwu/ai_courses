# 测验 M9 — 用 GitHub Pages 发布产品目录

> 8 道题（6 道选择题，2 道简答题）· 答案见下文 · 对应讲义分段 M9.1–M9.3

## 题目

**Q1 (MC).** 你在 Windows 上刚运行了 `winget install --id GitHub.cli --source winget`，它报告安装成功。在同一个终端窗口里，`gh --version` 却说系统不认识这条命令。正确的下一步是什么？

- a) 卸载 GitHub CLI，再重新安装
- b) 关掉这个终端，打开一个新窗口，再运行一次 `gh --version`
- c) 从 PowerShell 换到命令提示符（Command Prompt）
- d) 改用 Homebrew 安装 CLI

**Q2 (MC).** 你的环境检查打印了三行 PASS 和一行 FAIL："git does not know your name and email yet"。这个 FAIL 实际上会阻止你做什么？

- a) 克隆任何仓库
- b) 用 `gh auth login` 登录 GitHub
- c) 进行提交，因为每次提交都会记录一个名字和一个邮箱
- d) 在浏览器里打开 `index.html`

**Q3 (MC).** 你打开一个终端，运行 `gh repo clone tomqwu/ai_courses`，然后去 `code` 文件夹里看，项目却不在那里。最可能发生了什么？

- a) 克隆悄无声息地失败了
- b) 你运行它时不在 `code` 里，所以新文件夹建在了终端当时所在的位置——通常是你的主目录
- c) 克隆下来的仓库在你运行 `git status` 之前是隐藏的
- d) `gh repo clone` 只会下载一个 zip 文件

**Q4 (MC).** 编辑完 `products.js` 后，你运行了 `git add .` 和 `git commit -m "Add my products"`，但二十分钟后，已发布的网站仍然显示旧产品。`git status` 显示 "Your branch is ahead of 'origin/main' by 1 commit." 缺了什么？

- a) `git push`——在你推送之前，这次提交只存在于你的电脑上
- b) 什么都不缺；GitHub Pages 可能需要一天
- c) `.nojekyll` 文件
- d) 重新保存 Pages 设置

**Q5 (MC).** 为什么起始项目把产品放在 `products.js` 里，而不是放在一个 `products.json` 文件里？

- a) JSON 无法保存价格
- b) GitHub Pages 不发布 `.json` 文件
- c) 浏览器不允许从你的磁盘上打开的页面读取一个单独的数据文件，但会运行用 `<script>` 标签加载的脚本——所以双击就能预览，不需要服务器
- d) JavaScript 比 JSON 加载得更快

**Q6 (MC).** 一位朋友想给他的 GitHub Pages 产品目录加上购物车和银行卡支付，让顾客不离开页面就能付款。GitHub 自己的限制页面对此怎么说？

- a) 在付费计划上是允许的
- b) 只要网站保持在 1 GB 以内就允许
- c) Pages 不允许被用作免费托管，来经营线上业务或电子商务网站，或任何主要用于商业交易的网站——所以产品目录应该链接到托管在别处的结账页面
- d) 只要仓库是公开的就允许

**Q7 (Short answer).** 一位用 Mac 的同学贴出这样一段话：「我运行了 Homebrew 的安装命令，它也跑完了，可现在 `brew install gh` 显示 `command not found: brew`。」写出你会发的回复：最可能的原因、修复方法，以及之后他们怎样不靠猜测就能证明整个环境已经就绪。

**Q8 (Short answer).** 你的产品目录已经上线。一位店主请你把他们的产品加上去，当天就发布，还提到他们「以后」想接受银行卡付款。描述你会为其中一个产品对 `products.js` 做的修改、你会运行哪四条命令组成的循环来发布它、你会怎样确认它已经上线，以及关于付款你会告诉他们什么。

## Answer key

**A1: b.** 安装一个工具会改变终端查找命令的位置，而已经打开的窗口看不到这个变化。GitHub CLI 自己的 Windows 安装说明要求在安装后打开一个新的终端窗口——而不只是新标签页。（a）把时间浪费在一次本来就成功了的安装上；（c）有同样的问题，因为它仍然是一个旧窗口；（d）是 macOS 的包管理器。*（目标：M9.1 — `github.com/cli/cli`，`docs/install_windows.md`；`course/03-content/m09-github-pages/setup/check-setup.ps1`。）*

**A2: c.** Git 会在每次提交上标记一个名字和一个邮箱，没有它们就拒绝提交。克隆、登录和预览在没有身份信息时都能进行，这就是为什么检查脚本要单独用一行来测试它。修复方法是检查脚本打印出的那两行 `git config --global`。*（目标：M9.1 — `course/03-content/m09-github-pages/setup/check-setup.sh`。）*

**A3: b.** 克隆会在终端当前所在的文件夹里新建一个文件夹。终端打开时位于你的主目录，所以一打开就输入的克隆命令会落在那里，而不是 `code` 里。克隆之前先运行 `pwd`，或者先 `cd ~/code`。（a）有可能，但会打印一条错误；（c）和（d）是错的。*（目标：M9.2。）*

**A4: a.** `commit` 在你的电脑上保存一个版本；`push` 把它发送到 GitHub，而 Pages 只发布 GitHub 上已有的内容。"Ahead of 'origin/main' by 1 commit" 正是 Git 在说这件事。推送后最多可能需要 10 分钟才会发布，所以（b）在时间和原因上都错了。（c）影响的是网站如何构建，而不是你的提交是否到达。*（目标：M9.2、M9.3 — `github.com/github/docs`，`data/reusables/pages/twenty-minutes-to-publish.md`。）*

**A5: c.** 这个设计选择是为了预览：浏览器会阻止从磁盘打开的页面去获取一个单独的文件，但会运行用标签加载的脚本。把数据放在一个脚本里，意味着双击打开的预览和发布出去的页面是同一批文件，中间没有任何步骤。AI × QE 在更大的规模上做了同样的数据与布局分离，用一个供模板遍历的数据文件。*（目标：M9.3 — `course/03-content/m09-github-pages/catalog-starter/products.js`、`ai_qe/CONTRIBUTING.md:23`。）*

**A6: c.** GitHub Pages「不打算、也不允许被用作免费的网站托管服务，来经营你的线上业务、电子商务网站，或任何其他主要以促成商业交易或提供商业软件即服务为目的的网站」。计划、大小限制和可见性都改变不了这一点。一个介绍产品并链接到在别处运行的结账页面的产品目录，才是 Pages 允许的形态，这就是为什么起始项目有 `buyUrl` 而没有购物车。*（目标：M9.3 — `github.com/github/docs`，`content/pages/getting-started-with-github-pages/github-pages-limits.md`。）*

**A7.** 一个好的回复会指出原因：Homebrew 安装程序结束时会打印几行 shell 设置说明，用来把 `brew` 加进终端，而这几行被跳过了——在 Apple 芯片的 Mac 上，Homebrew 位于 `/opt/homebrew`，在这几行运行之前，终端不会去那里查找。修复方法是往回翻，原样复制这几行，运行它们，然后打开一个新的终端窗口。证明不是「`brew` 现在能用了」，而是环境检查：运行 `bash check-setup.sh`，直到它打印 **4 of 4 checks passed**，并粘贴进证据日志，因为它一次就测试了 Git、CLI、身份和登录。任何给出了原因、修复方法和一个会实际运行的检查的回复都可以接受；只说「全部重装」而不给原因的，不予接受。*（目标：M9.1 — `github.com/Homebrew/install`，README；`course/03-content/m09-github-pages/setup/check-setup.sh`。）*

**A8.** 一个好的答案涵盖四件事。**修改**：在 `products.js` 里加一个块，包含 `id`、`name`、`category`、写成数字的 `price` 和 `summary`，逗号完好；再加一个指向店主在别处运营的结账页面的 `buyUrl`，或者不写 `buyUrl`，让按钮显示 "Ask about this"。**循环**：`git status`、`git add .`、带一条说明改了什么的 `git commit -m`、`git push`——然后 `git status` 显示工作区干净。**确认上线**：Actions 标签页里的 pages build and deployment 运行变绿，然后在线地址显示出这个产品，最多等 10 分钟。**付款**：Pages 不能托管网店，所以付款要留在托管于别处的结账页面上，由产品目录链接过去——要在他们围绕购物车动手构建之前就说清楚。只在本地预览就称之为已发布的答案，或者承诺在页面上收款的答案，要扣分。*（目标：M9.2、M9.3 — `github.com/github/docs`，`content/pages/getting-started-with-github-pages/github-pages-limits.md`。）*

## 目标 → 考核对应表

`course/03-content/m09-github-pages/lesson.md` 里每一条「学完本模块，你能够」，以及检查它的内容。

| 目标（lesson.md） | 由谁检查 |
|---|---|
| 在 Windows 或 macOS 上**安装** Git 和 GitHub CLI，登录，并用脚本证明环境已经配好 | Q1、Q2、Q7；实验 M9 第 1 步，检查清单第 1 项 |
| 在终端里**浏览**文件夹 | Q3；实验 M9 第 2–3 步，检查清单第 2 项 |
| **克隆**、修改，并用 status → add → commit → push 送回去 | Q3、Q4、Q8；实验 M9 第 4 步和第 6 步，检查清单第 3–4 项 |
| 用 GitHub Pages 从分支**发布**静态网站，并找到它的地址 | Q4、Q5、Q8；实验 M9 第 5、7、8 步，检查清单第 5、7、8 项 |
| **说清** GitHub Pages 用来做什么、不用来做什么 | Q6、Q8；实验 M9 第 5 步，检查清单第 6 项 |
