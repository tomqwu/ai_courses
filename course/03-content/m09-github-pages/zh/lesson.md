# 第 9 模块 — 用 GitHub Pages 发布产品目录
> AI Product Studio（APS-3）的一部分 · 免费、可独立学习 · 约 45 分钟讲授，另加 60–90 分钟上机操作（大部分时间花在安装上）· 无前置要求：如果你从没用过终端，先学这一个

## 概览

本课程里的每个产品，最终都需要一个陌生人也能打开的页面：它是什么、多少钱、怎么买到。本模块就来做这个页面，并用 **GitHub Pages** 把它免费放到互联网上——起点是一台还没装任何工具的电脑。本模块写给从没打开过终端（terminal）的人。如果你用过，可以略读 M9.1 和 M9.2 两个分段，直接去做实验。

学完本模块，你会拥有三样可以拿出来给人看的东西。一个能证明自身配置的终端：一个脚本打印出四行 PASS。一个你创建、克隆（clone）、修改并从终端推送（push）的 GitHub 仓库（repository）。以及一个公开的产品目录，地址形如 `https://<your-username>.github.io/<repository-name>/`，带筛选、搜索，而且每个产品上都有一个能用的 "Buy" 或 "Ask about this" 按钮。

你要做的网站故意很小：三个你要编辑的文件，外加一个你永远不碰的文件。没有框架，没有构建步骤，除了 Git 本身之外什么都不用装。这不是给初学者的折中方案。本课程自己的专业领域案例研究用的也是同样的结构，只是规模大得多：**AI × QE 是一个 GitHub Pages 网站**，发布在 `tomqwu.github.io/ai_qe`（`ai_qe/_config.yml:5`、`ai_qe/_config.yml:13`），它把四张简报卡片放在一个数据文件里，由一个模板把它们绘制到页面上（`ai_qe/CONTRIBUTING.md:23`）。你的产品目录把产品放在一个数据文件里，由一个脚本把它们绘制到页面上。同样的思路，更少的活动部件。

本模块的每条命令都同时给出 **Windows** 和 **macOS** 两个版本，并排列出。Linux 用户可以照着 macOS 那一栏做；装好 Git 和 GitHub CLI 之后，命令都是一样的。

**学完本模块，你能够：**

- 在 Windows 或 macOS 上安装 Git 和 GitHub CLI，登录，并用脚本而不是猜测来证明环境已经配好。
- 在终端里浏览电脑上的文件夹：知道自己在哪里，列出这里有什么，进入再退出，以及新建一个文件夹。
- 把一个仓库克隆到你的电脑上，修改它，再用 `status → add → commit → push` 把改动送回去。
- 用 GitHub Pages 从一个分支发布静态网站，并找到它的公开地址。
- 说清 GitHub Pages 是用来做什么的、不是用来做什么的——包括为什么产品目录必须链接到外部的结账页面，而不能做成一个网店。

## M9.1 — 你的工具：已安装，并已证明（约 15 分钟）

### 目标

安装 Git 和 GitHub CLI，告诉 Git 你是谁，从终端登录 GitHub，然后运行一个检查，证明这四项都已完成，而不是想当然。

### 讲解

**这些工具是什么。** *Git* 记录一个文件夹的各个版本：你保存的每一次改动都是一次*提交*（commit），你随时可以回到它。*GitHub* 是一个网站，它保存那个文件夹的一份副本，这份副本叫作*仓库*（repository），只要你要求，它还能把仓库发布出去。*GitHub CLI* 是一条名为 `gh` 的命令，让你在终端里和 GitHub 打交道——创建仓库、登录、克隆——而不必在网站上一路点击。*终端*（terminal）是一个窗口，你在里面输入命令，而不是用鼠标点击。

**打开终端。**

| | Windows | macOS |
|---|---|---|
| 应用 | **Terminal**（Windows 11）或 **PowerShell**——按 Windows 键，输入 `terminal`，按 Enter | **Terminal**——按 Cmd+Space，输入 `terminal`，按 Enter |
| 你会看到 | 一行以 `PS C:\Users\ada>` 结尾的字 | 一行以 `ada@Adas-Mac ~ %` 结尾的字 |

这一行就是*提示符*（prompt）。它在等你输入。本模块里的一切都在它后面输入，然后按 Enter 运行。

**安装包管理器。** 包管理器（package manager）用一条命令安装软件，之后也用同样的方式更新它。两个系统各有一个。

- **Windows** 用 **winget**，也就是 Windows 包管理器（Windows Package Manager）。它随微软的 App Installer 软件包一起提供，需要 Windows 10 1809 或更高版本，或者 Windows 11（`github.com/microsoft/winget-cli`，README）。输入 `winget --version`。如果终端说它不认识 `winget`，就从 Microsoft Store 安装 **App Installer**，然后打开一个新终端。
- **macOS** 用 **Homebrew**。用 Homebrew 官方说明里的那一行命令安装它：

  ```bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```

  它会要你输入 Mac 的密码，顺带安装 Apple 的 Command Line Tools，在 Apple 芯片的 Mac 上会装到 `/opt/homebrew`（`github.com/Homebrew/install`，README）。安装结束时，它会打印几行 shell 设置说明，作用是把 `brew` 加进你的终端。原样复制并运行它们——跳过它们，正是之后 `brew` 出现 "not found" 的常见原因。

**安装 Git 和 GitHub CLI。**

| | Windows | macOS |
|---|---|---|
| Git | `winget install --id Git.Git -e --source winget` | `brew install git` |
| GitHub CLI | `winget install --id GitHub.cli --source winget` | `brew install gh` |
| 然后 | 关掉终端，打开一个**新窗口** | 什么都不用做——已经可以用了 |

在 Windows 上，最容易绊倒人的是最后一行。安装一个工具会改变终端查找命令的位置列表，而一个已经打开的终端看不到这个变化；GitHub CLI 自己的说明要求打开一个新窗口，而不只是新标签页（`github.com/cli/cli`，`docs/install_windows.md`）。包名用的是维护者发布的名字：Windows 软件包仓库里的 `Git.Git`（`github.com/microsoft/winget-pkgs`，`manifests/g/Git/Git`），GitHub CLI 的 Windows 安装说明里的 `GitHub.cli`，以及 Homebrew 里的 `git` 和 `gh`（`github.com/cli/cli`，`docs/install_macos.md`）。

**告诉 Git 你是谁。** 每次提交都会记录一个名字和一个邮箱。设置一次，这台电脑上的每个仓库都会用它：

```bash
git config --global user.name "Ada Example"
git config --global user.email "ada@example.com"
```

用你 GitHub 账号上的邮箱；如果你不想公开自己的邮箱，也可以用 GitHub 在邮箱设置里提供的私密 "noreply" 地址。

**从终端登录 GitHub。**

```bash
gh auth login
```

它会问四个问题。依次回答 **GitHub.com**、**HTTPS**，对「用你的 GitHub 凭据认证 Git」回答 **Yes**，最后选 **Login with a web browser**。它会显示一个一次性验证码，打开你的浏览器，你把验证码粘贴进去。默认就是这个浏览器流程（`github.com/cli/cli`，`pkg/cmd/auth/login/login.go`）。之后，`git` 推送到你的仓库时就不会每次都要你输入密码。

**证明它。** 配置机器这一步，是人们最常以为已经做完、其实并没有做完的步骤。所以本模块附带一个检查，它查看这四项，并为缺失的每一项打印修复方法（`course/03-content/m09-github-pages/setup/check-setup.sh`、`course/03-content/m09-github-pages/setup/check-setup.ps1`）。在包含脚本的文件夹里，运行适合你系统的那一个：

| Windows | macOS |
|---|---|
| `powershell -ExecutionPolicy Bypass -File .\check-setup.ps1` | `bash check-setup.sh` |

配置完成时，它打印四行 PASS 和 **4 of 4 checks passed**。少于四项时，它会打印一行 FAIL，附上能修复它的确切命令——在没有 Homebrew 的 Mac 上，它会先打印 Homebrew 的安装命令。修好第一个 FAIL，打开一个新终端，再运行一次。Windows 上的参数 `-ExecutionPolicy Bypass` 让这一个脚本能够运行，而不改变你电脑上针对其他任何脚本的设置。

### 行动步骤

运行检查，直到它显示 4 of 4，然后把完整输出粘贴到一个名为 `evidence.md` 的新文件里——在本模块剩下的部分，你会一直往里添加内容。如果途中某一步失败了，把失败也粘贴进去，连同修好它的方法。这份记录比一份干净的记录更有价值。

## M9.2 — 学会找路，然后克隆（约 15 分钟）

### 目标

知道自己在文件夹树中的位置，进出文件夹，新建一个文件夹，把一个仓库克隆进去——然后用四条命令组成的循环把改动送回去。

### 讲解

**你总是身处某个位置。** 终端总有一个*当前文件夹*，就像文件窗口总是显示某一个文件夹。终端刚打开时，这个文件夹就是你的**主目录**（home folder）：Windows 上是 `C:\Users\ada`，Mac 上是 `/Users/ada`。两个系统都允许你把主目录写成 `~`。

| 你想做什么 | Windows（PowerShell） | macOS | 说明 |
|---|---|---|---|
| 我在哪里？ | `pwd` | `pwd` | 打印当前文件夹 |
| 这里有什么？ | `ls` | `ls` | PowerShell 也接受 `dir` |
| 进入一个文件夹 | `cd code` | `cd code` | 相对于你当前的位置 |
| 回到上一级 | `cd ..` | `cd ..` | 两个点表示「上一级文件夹」 |
| 回到主目录 | `cd ~` | `cd ~` | 在任何地方都可以 |
| 新建一个文件夹 | `mkdir code` | `mkdir code` | |
| 在文件窗口里打开这个文件夹 | `start .` | `open .` | 一个点表示「这里」 |
| 帮你补全长名字 | 按 Tab | 按 Tab | 避免打错字的最快方法 |

**绝对路径和相对路径。** 从磁盘顶层开始的路径是*绝对路径*（absolute path）：`C:\Users\ada\code` 或 `/Users/ada/code`。从你当前位置开始的路径是*相对路径*（relative path）：`code`，或 `..\Documents`。Windows 用反斜杠 `\` 分隔文件夹，macOS 用正斜杠 `/`。在 Windows 上，PowerShell 两种都接受，所以 `cd code/my-catalog` 在两个系统上都能用——这是件小事，但当你从网上复制命令时，能省下很多困惑。

**带空格的名字需要加引号。** `cd My Projects` 会试图进入一个叫 `My` 的文件夹。要输入 `cd "My Projects"`，或者干脆不在项目文件夹名里用空格，大多数开发者都是这么做的：写 `my-catalog`，而不是 `My Catalog`。

**把项目放在同一个地方。** 在主目录里建一个名为 `code` 的文件夹，把每个仓库都放进去。这样，「我的项目在哪？」永远只有一个答案：

```bash
cd ~
mkdir code
cd code
pwd
```

在 Mac 上，最后一行打印 `/Users/ada/code`；在 Windows 上打印 `C:\Users\ada\code`，位于 `Path` 标题下方。

**克隆就是把一个仓库复制到你的电脑上，连同它的历史。** 有两种方式，效果相同：

```bash
gh repo clone tomqwu/ai_courses
git clone https://github.com/tomqwu/ai_courses.git
```

`gh repo clone` 接受简短的 `owner/name` 形式，并使用你设置好的登录；`git clone` 接受完整地址，也就是你在任何仓库的绿色 **Code** 按钮上看到的那个。无论用哪一条，都会在你当前所在的文件夹里新建一个以仓库命名的文件夹。反过来说，这正是初学者最常犯的错误：在主目录里克隆，然后在 `code` 里找不到项目。先运行 `pwd`。

**把改动送回去的循环。** 一旦一个文件夹成了仓库，每次改动都经过同样的四条命令：

| 命令 | 它做什么 | 你应该看到什么 |
|---|---|---|
| `git status` | 显示自上次提交以来改了什么 | 列出标为 modified 或 untracked 的文件 |
| `git add .` | 把这个文件夹里的每一处改动都选入下一次提交 | 什么都没有；不出声就是成功 |
| `git commit -m "Say what changed"` | 把这些改动保存为一个版本，附上你的说明 | 一行带短编号和文件数量的输出 |
| `git push` | 把你的新提交发送到 GitHub | 一行以 `main -> main` 结尾的输出 |

下面是这个循环在产品目录起始项目上的真实运行结果，所在文件夹克隆自一个只有 README 的仓库（输出完全是 Git 打印出来的原样；你的短编号会不一样）：

```text
$ git status
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
	modified:   README.md

Untracked files:
	.nojekyll
	app.js
	index.html
	products.js
	styles.css

$ git commit -m "Add the catalog starter"
[main c02f59f] Add the catalog starter
 6 files changed, 497 insertions(+), 1 deletion(-)

$ git push
   699905a..c02f59f  main -> main
```

每一次都要在前后各看一遍 `git status`。之前，它告诉你将要提交什么。之后，**nothing to commit, working tree clean** 告诉你全部都送上去了。

### 行动步骤

在你的 `code` 文件夹里，用任意一条命令克隆本课程的仓库，`cd` 进入它，运行 `ls`。然后用 `cd ..` 回到上一级，运行 `pwd` 证明你在哪里。把两段输出都添加到 `evidence.md`。

## M9.3 — 做出产品目录，然后发布（约 15 分钟）

### 目标

把起始项目变成你自己的产品目录，在你的电脑上预览，用 GitHub Pages 发布它，并说清这个托管平台允许什么、不允许什么。

### 讲解

**起始项目有五个文件，你只改其中一个。** 它位于 `course/03-content/m09-github-pages/catalog-starter/`：

| 文件 | 它是什么 | 要改吗？ |
|---|---|---|
| `products.js` | 你的店名、联系方式，以及一个产品列表 | **要** |
| `index.html` | 页面 | 顶部附近的两行：搜索结果里显示的描述 |
| `styles.css` | 颜色和布局 | 只改 `:root` 里的颜色，想改就改 |
| `app.js` | 绘制卡片、分类按钮、搜索和排序 | 不改 |
| `.nojekyll` | 一个空文件 | 不改——保留它 |

每个产品是一个小块，包含名称、分类、价格和一句话简介。加上 `image` 可以显示照片，加上 `buyUrl` 可以链接到外部的结账页面；没有它时，按钮会变成 **Ask about this**，点击会打开一封邮件。你用到的每个分类，都会出现一个筛选按钮。

**为什么产品放在 `.js` 文件里，而不是 `.json` 文件里。** 浏览器不允许从你的磁盘上打开的页面去读取一个单独的数据文件，但会运行用 `<script>` 标签加载的脚本。把产品放在 `products.js` 里，意味着你可以双击 `index.html`，看到的正是全世界将会看到的样子，不需要服务器，不需要安装，也不需要构建。这也是为什么预览是可信的：在你的电脑和发布出去的网站之间，没有任何一步会改变显示的内容。

**把数据和布局分开。** AI × QE 在更大的规模上做着同样的事：它首页的卡片来自 `_data/briefing_room.json`，即「那四张展示卡片」（`ai_qe/CONTRIBUTING.md:23`），再由一个模板遍历这个文件把它们绘制出来（`ai_qe/releases.md:222`）。一个产品有变化时，你只改一个数据文件里的一个条目。谁都不需要去碰页面。

**预览它。** 在文件窗口里双击 `index.html`。或者在终端里，在项目文件夹中运行：

| Windows | macOS |
|---|---|
| `start index.html` | `open index.html` |

起始项目就是这样检查过的：在无头浏览器里直接从磁盘打开，分别在手机和桌面宽度、浅色和深色模式下查看：六个产品都能渲染，筛选、搜索和排序都能用，没有任何横向滚动，每一处文字都达到 WCAG AA 对比度的最低要求（`course/03-content/m09-github-pages/catalog-starter/README.md`）。

**发布它。** GitHub Pages 把一个仓库里的文件发布成网站。对于这样的项目，步骤来自 GitHub 官方文档（`github.com/github/docs`，`content/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site.md`）：

1. 在 GitHub 上打开你的仓库，选择 **Settings**（设置），然后在左侧栏选择 **Pages**。
2. 在 **Build and deployment**（构建与部署）下，把 **Source**（来源）设为 **Deploy from a branch**（从分支部署）。
3. 选择分支 `main` 和文件夹 `/ (root)`，然后点 **Save**（保存）。

网站会出现在 `https://<your-username>.github.io/<repository-name>/`——这是项目网站的地址格式（`github.com/github/docs`，`content/pages/getting-started-with-github-pages/what-is-github-pages.md`）——GitHub 说，推送之后，一次改动最多可能需要 10 分钟才会发布。网站上线后，同一个 Settings 页面上的 **Visit site** 按钮会显示确切的地址。之后的每次 `git push` 都会重新发布它；你永远不需要重复这些步骤。

`.nojekyll` 文件在这里很关键。默认情况下，GitHub Pages 会让每个网站都经过 **Jekyll** 处理，这是一个把模板转换成页面的工具；一个空的 `.nojekyll` 文件会关掉它，这样你的文件就会按原样发布。

**两种发布方式，同一个托管平台。** 你的产品目录用的是最简单的模式：按原样发布一个分支。AI × QE 用的是另一种：一个 GitHub Actions 工作流，用 Jekyll 构建网站，对链接、旁白和 PDF 版本运行自己的检查，全部通过之后才部署（`ai_qe/.github/workflows/pages.yml:77`、`ai_qe/.github/workflows/pages.yml:155`）。部署步骤需要两项显式权限：`pages: write` 和 `id-token: write`（`ai_qe/.github/workflows/pages.yml:148-149`）。今天这些你都不需要。要点在于，托管平台是同一个，一个网站可以从一种模式成长到另一种，而不必搬家。

**GitHub Pages 用来做什么，不用来做什么。** GitHub 公布了这些限制，对一个产品目录来说它们很宽裕（`github.com/github/docs`，`content/pages/getting-started-with-github-pages/github-pages-limits.md`）：

| 限制 | 数值 | 类型 |
|---|---|---|
| 已发布网站的大小 | 1 GB | 硬限制 |
| 带宽 | 每月 100 GB | 软限制 |
| 构建 | 每小时 10 次 | 软限制 |
| 单次部署 | 10 分钟后超时 | 硬限制 |

在免费账号上，**公开**仓库可以免费使用 Pages；从**私有**仓库发布则需要付费计划（`github.com/github/docs`，`data/reusables/gated-features/pages.md`）。

决定整个设计的那条规则，是那个页面上的最后一条：GitHub Pages「不打算、也不允许被用作免费的网站托管服务，来经营你的线上业务、电子商务网站，或任何其他主要以促成商业交易或提供商业软件即服务为目的的网站」。一个介绍你的产品的目录没问题。一个网店则不行。这就是起始项目没有购物车、也没有结账功能的原因：每个产品都可以用 `buyUrl` 链接到一个在专为收款而建的地方运行的结账页面，而产品目录保持 Pages 允许它成为的样子。从一开始就这样构建，以后就没有什么需要推倒重来。

### 行动步骤

把六个示例产品换成至少三个你自己的产品——真实的产品，或者你在本课程中正在构建的产品。双击预览，然后在 `evidence.md` 里写一行，说明你的 "Buy" 按钮将指向哪里，或者为什么它暂时显示 "Ask about this"。

## 回顾

- **工具，已证明。** Git 记录版本；GitHub 保存并发布它们；`gh` 在终端里操作 GitHub。在 Windows 上用 winget 安装，在 macOS 上用 Homebrew 安装；在 Windows 上安装后打开一个新窗口；设置你的名字和邮箱；运行 `gh auth login`；然后运行环境检查（setup check），直到它显示 4 of 4。
- **文件夹。** `pwd`、`ls`、`cd`、`cd ..`、`mkdir` 在两个系统的 PowerShell 和 Terminal 里用法相同。把项目放在 `~/code` 里。克隆之前先看 `pwd`。
- **循环。** `git status → git add . → git commit -m "…" → git push`，前后各看一遍 `status`。
- **发布。** Settings → Pages → Deploy from a branch → `main`、`/ (root)` → Save。地址是 `https://<username>.github.io/<repository>/`，每次推送后最多 10 分钟生效。
- **边界。** Pages 展示产品；它不销售产品。链接到外部的结账页面。

## 讨论题

贴出你的产品目录地址，以及配置过程中出过的一个问题，附上修好它的那一行命令。然后在手机上打开一位同学的产品目录，告诉他们你试着点的第一个没有按你预期工作的东西。

## 资料来源

于 2026-09-26 从维护者自己的仓库读取。编写本模块的环境无法访问渲染后的文档网站，所以每个来源都是构建这些网站所用的源文件。

- GitHub Pages：从分支发布、网站类型和地址、限制和禁止用途、计划可用性、发布时间——`github.com/github/docs`，`content/pages/getting-started-with-github-pages/` 和 `data/reusables/`。
- GitHub CLI：Windows 和 macOS 的安装命令、开新窗口的说明、`gh auth login`、`gh repo create` 的参数——`github.com/cli/cli`，`docs/install_windows.md`、`docs/install_macos.md`、`pkg/cmd/auth/login/login.go`、`pkg/cmd/repo/create/create.go`。
- Git for Windows 的软件包 id `Git.Git`——`github.com/microsoft/winget-pkgs`，`manifests/g/Git/Git`。
- winget 的系统要求和 App Installer——`github.com/microsoft/winget-cli`，README。
- Homebrew 安装命令、Command Line Tools、`/opt/homebrew`——`github.com/Homebrew/install`，README；Git formula——`github.com/Homebrew/homebrew-core`，`Formula/g/git.rb`。
