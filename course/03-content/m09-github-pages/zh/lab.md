# 实验 M9 — 发布你的产品目录

> 免费、可独立完成 · **前置条件：** 无——一台 Windows 10（1809 或更高版本）、Windows 11 或 macOS 电脑，以及一个免费的 GitHub 账号 · **时间：** 60–90 分钟，大部分时间花在安装上 · 通过 = 下面的每一条检查清单都可以客观核验

**目标：** 从一台什么都没装的电脑，走到一个位于 `https://<your-username>.github.io/my-catalog/` 的公开产品目录，它由你在终端里克隆、修改并推送的文件构建而成。

**在哪里操作。** 主目录里一个名为 `code` 的文件夹。在旁边打开一个名为 `evidence.md` 的文件，边做边往里粘贴：下面每一步都会说明要粘贴什么。

**怎么看这些命令。** Windows 和 macOS 不同时，两者都会给出。在提示符后面输入所有内容，然后按 Enter。Windows 命令适用于 **PowerShell**——Windows Terminal 里的默认环境。如果一条命令在两个系统上相同，就只显示一次。

## 第 0 步 — 创建 GitHub 账号 (~5 分钟)

如果你还没有账号，就在 `github.com` 用一个你能打开的邮箱注册。仔细选择你的用户名：它会成为你产品目录地址的一部分。把你的用户名粘贴到 `evidence.md`。

## 第 1 步 — 安装工具并证明它们 (~30 分钟，大多在等待)

打开一个终端（Windows：按 Windows 键，输入 `terminal`，按 Enter；macOS：按 Cmd+Space，输入 `terminal`，按 Enter）。

1. **包管理器。**
   - Windows：运行 `winget --version`。如果系统不认识它，就从 Microsoft Store 安装 **App Installer**，然后打开一个新的终端窗口。
   - macOS：安装 Homebrew，然后运行它在最后打印出的 shell 设置命令：
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
2. **Git 和 GitHub CLI。**

   | Windows | macOS |
   |---|---|
   | `winget install --id Git.Git -e --source winget` | `brew install git` |
   | `winget install --id GitHub.cli --source winget` | `brew install gh` |
   | **关掉终端，打开一个新窗口。** | |

3. **你的名字和邮箱**（用你 GitHub 账号上的邮箱，或者它的私密 noreply 地址）：
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   ```
4. **登录：** `gh auth login` → **GitHub.com** → **HTTPS** → **Yes**（认证 Git）→ **Login with a web browser** → 在浏览器里粘贴一次性验证码。
5. **证明它。** 环境检查脚本随课程一起提供。在你克隆课程（第 3 步）之前，先从 GitHub 只下载适合你系统的那个脚本——在浏览器里打开它，选择 **Raw**，把它保存到你的主目录——然后在那里运行：

   | Windows | macOS |
   |---|---|
   | `powershell -ExecutionPolicy Bypass -File .\check-setup.ps1` | `bash check-setup.sh` |

   脚本位于 `github.com/tomqwu/ai_courses` 里的 `course/03-content/m09-github-pages/setup/check-setup.ps1` 和 `course/03-content/m09-github-pages/setup/check-setup.sh`。修好它指出的第一个 FAIL，打开一个新终端，再运行一次，直到它打印 **4 of 4 checks passed**。

**粘贴：** 最终的检查输出，以及你途中遇到的每一个 FAIL，连同修好它的命令。

## 第 2 步 — 学会找路 (~5 分钟)

```bash
cd ~
mkdir code
cd code
pwd
ls
```

`pwd` 应该打印你的主目录，后面跟着 `code`——Mac 上是 `/Users/<you>/code`，Windows 上是 `C:\Users\<you>\code`。`ls` 暂时什么都不打印：这个文件夹是空的。如果 `mkdir` 说文件夹已经存在，也没关系，继续即可。

**粘贴：** `pwd` 的输出。

## 第 3 步 — 克隆课程，找到起始项目 (~5 分钟)

仍然在 `code` 里：

```bash
gh repo clone tomqwu/ai_courses
cd ai_courses/course/03-content/m09-github-pages/catalog-starter
ls
```

`ls` 会列出 `README.md`、`app.js`、`index.html`、`products.js` 和 `styles.css`。第五个文件 `.nojekyll` 因为名字以点开头而被隐藏：在 Mac 上用 `ls -a`，在 PowerShell 里用 `ls -Force` 可以看到它。

现在回到 `code`。下面任意一条都可以，这正是 M9.2 分段要讲的：

```bash
cd ../../../../..     # up five levels: one for each folder you went into
cd ~/code             # straight there from anywhere, using the home shortcut
```

之后运行 `pwd`，证明你落在了哪里。

**粘贴：** 在起始项目文件夹里得到的 `ls` 输出。

## 第 4 步 — 创建你自己的仓库 (~5 分钟)

在 `code` 里：

```bash
gh repo create my-catalog --public --add-readme --clone --description "My product catalog"
cd my-catalog
git status
```

`--add-readme` 会给新仓库在名为 `main` 的分支上做第一次提交，这样克隆下来就在 `main` 上，之后 `git push` 也知道该推到哪里。`git status` 会显示 **On branch main** 和 **nothing to commit, working tree clean**。

在 `my-catalog` 里面，把起始项目复制进来——包括隐藏的 `.nojekyll`：

| Windows | macOS |
|---|---|
| `Copy-Item -Recurse -Force ..\ai_courses\course\03-content\m09-github-pages\catalog-starter\* .` | `cp -R ../ai_courses/course/03-content/m09-github-pages/catalog-starter/. .` |

两种写法都会把隐藏的 `.nojekyll` 一起复制：在 PowerShell 里靠 `-Force`，在 Mac 上靠结尾的 `/.`。再运行一次 `git status`。它应该把 `README.md` 显示为 **modified**——起始项目的 README 替换了 GitHub 生成的那个——并把 `.nojekyll`、`app.js`、`index.html`、`products.js`、`styles.css` 显示为 **untracked**。如果列表里没有 `.nojekyll`，说明复制时漏掉了 `-Force` 或 `/.`；按原样再运行一次。

**粘贴：** 这次 `git status` 的输出。

## 第 5 步 — 改成你自己的，并预览 (~15 分钟)

1. 用任意文本编辑器打开 `products.js`（记事本或 TextEdit 都可以；如果用 TextEdit，先选择 **Format → Make Plain Text**）。
2. 修改 `store.name`、`store.tagline` 和 `store.contact`（你的邮箱，写成 `mailto:you@example.com`）。
3. 把示例产品换成**至少三个你自己的产品**。保留各个块之间的逗号。
4. 在 `index.html` 里，把顶部附近的 `description` 那一行改成一句介绍你的产品的话。
5. 预览：

   | Windows | macOS |
   |---|---|
   | `start index.html` | `open index.html` |

   你的产品会显示出来，你用到的每个分类都有一个分类按钮。如果页面显示 **products.js did not load**，说明少了一个逗号或引号：浏览器的开发者控制台（Windows 上按 F12，Mac 上按 Cmd+Option+I）会指出是哪一行。

**粘贴：** 一张预览截图，以及一行说明每个产品的按钮指向哪里——指向你在别处运营的结账页面的 `buyUrl`，或者暂时用 "Ask about this"。

## 第 6 步 — 提交并推送 (~5 分钟)

```bash
git status
git add .
git commit -m "Add my catalog"
git push
git log --oneline -2
git status
```

`git commit` 会打印一行以 `[main` 开头的输出，带一个短编号和改动的文件数量。`git push` 最后一行类似 `699905a..c02f59f  main -> main`。最后的 `git status` 显示 **nothing to commit, working tree clean**——这就是一切都已送达的证明。

**粘贴：** `git log --oneline -2` 的输出，以及最后一次 `git status` 的输出。

## 第 7 步 — 用 GitHub Pages 发布 (~10 分钟，含等待时间)

1. 在 GitHub 上打开你的仓库：`gh repo view --web` 会在浏览器里打开它。
2. **Settings** → **Pages**（左侧栏）。
3. 在 **Build and deployment** 下，**Source** 选 **Deploy from a branch**。Branch 选 `main`。Folder 选 `/ (root)`。点 **Save**。
4. 等待。最多可能需要 10 分钟。**Actions** 标签页会显示一个名为 **pages build and deployment** 的运行；它变绿之后，Pages 设置里会显示 **Visit site** 和你的地址。
5. 在你的电脑上**和**手机上打开 `https://<your-username>.github.io/my-catalog/`。

**粘贴：** 地址，以及一张已发布页面在你手机上的截图。

## 第 8 步 — 改一处，看着它重新发布 (~10 分钟)

在 `products.js` 里修改一个产品的价格。先预览，然后用一条说明改了什么的提交信息再跑一遍第 6 步的循环，例如 `git commit -m "Lower the mug price to 30"`。看着 **Actions** 标签页再次运行，然后重新加载已发布的页面。

**粘贴：** 新的 `git log --oneline -1`，以及从你推送到新价格出现之间的时间。

## 验收清单（二元判定——每一项都勾上才算通过）

1. ☐ 环境检查打印出 **4 of 4 checks passed**，并完整粘贴。
2. ☐ `pwd` 的输出显示你的 `code` 文件夹位于你的主目录里。
3. ☐ `my-catalog` 在 GitHub 上存在，是你从终端创建的**公开**仓库。
4. ☐ 第一次提交之前的 `git status` 列出了 `.nojekyll`、`app.js`、`index.html`、`products.js` 和 `styles.css`。
5. ☐ `products.js` 里至少有三个你自己的产品；六个示例产品一个都没有留下。
6. ☐ 每个产品的按钮要么指向托管在 GitHub Pages 之外的结账页面，要么显示 "Ask about this"——页面上没有购物车或支付表单。
7. ☐ 已发布的地址能在手机上打开，并显示你的产品。
8. ☐ 第 8 步的改动在已发布的页面上可见，它的提交也在 `git log` 里。

## 证据记录

`evidence.md` 按顺序包含：你的 GitHub 用户名；环境检查输出，以及你修好的每一次失败；`pwd`；起始项目的 `ls`；第一次提交之前的 `git status`；预览截图和按钮去向；`git log --oneline -2`；已发布的地址和手机截图；第 8 步的提交，以及它花了多久才出现。把 `evidence.md` 也提交进 `my-catalog`——这是本课程其余部分所依赖的那个习惯的第一条记录：一个主张的可信度，取决于它背后的记录。

## 拓展（可选，约 30 分钟）

- 加上真实照片：一个 `images` 文件夹，每个产品写一行 `image: "images/your-file.jpg"`，每张照片控制在大约 500 KB 以内。
- 给一个产品设置 `buyUrl`，指向支付服务商提供的支付链接或某个电商平台上的商品页面，并在手机上测试它。
- 阅读 AI × QE 的发布工作流（`ai_qe/.github/workflows/pages.yml`），用平实的话列出它在部署之前运行、而你用分支发布的产品目录没有运行的三项检查。

## 讨论题

贴出你的产品目录地址，以及耗时最长的那一个配置步骤，附上修好它的那一行命令。回复一位同学：告诉他们你在他们的产品目录上试着点的第一个没有按你预期工作的东西。
