---
marp: true
theme: aps
paginate: true
title: M9 — 用 GitHub Pages 发布产品目录
---

<!-- _class: lead -->

# M9 — 用 GitHub Pages 发布产品目录

**AI Product Studio（APS-3）** · 约 45 分钟 · 免费、可独立学习 · 无前置要求

```figure
kind: flow
alt: 从什么都没装，到一个公开的产品目录——工具已安装并验证，一个仓库已克隆、修改并推送，一个页面已在 GitHub Pages 上线。
step: 什么都没装
step: 工具已安装并验证 @ 学完本模块，你会拥有
step: 一个你克隆、修改并推送的仓库 @ 学完本模块，你会拥有
step: 一个在 GitHub Pages 上的公开产品目录 (hl) @ 学完本模块，你会拥有
```

<!-- NOTES: 欢迎来到 M9。本模块免费，也不需要任何准备：如果你从没用过终端，先学这一个。承诺：学完时，学员的工具已安装并验证，有一个亲手克隆并推送的仓库，还有一个放在自己 github.io 地址上的公开产品目录。明确说出来：每条命令都同时给出 Windows 和 macOS 两个版本，并排列出。时间：1 分钟。过渡：五个学习成果。 -->

---

## 学完本模块，你能够……

- **安装** Git 和 GitHub CLI，并加以证明
- 在终端里**浏览**文件夹
- **克隆**、修改并推送一个仓库
- 用 GitHub Pages **发布**一个静态网站
- **说清** Pages 允许什么、禁止什么

<!-- NOTES: 把这五个成果当作提前预告的实验检查清单来读：实验 M9 为每一项都设了一条，测验 M9 也检查同样的五项。强调最后一项，因为它决定了设计：产品目录展示产品，并链接到外部的结账页面。时间：1 分钟。过渡：工具。 -->

---

## M9.1 — 四样东西，各管一件事

```figure
kind: system
alt: 四样工具，以及一次改动如何流转——你在终端里输入命令；Git 在你的文件夹里记录提交；gh 帮你登录并创建仓库；git push 把提交发送到 GitHub，GitHub 再把网站发布到 Pages 上。
layer: 你的电脑 @ Git 在你的电脑上
  node git: Git — 记录版本；每个版本是一次提交 @ Git 记录一个文件夹
  node term: 终端 — 输入命令，而不是点击 @ 终端是一个窗口
  node gh: gh — GitHub CLI (seam) @ 还有 gh
layer: 互联网 @ GitHub 在互联网上
  node github: GitHub — 保存仓库 @ GitHub 是一个网站
  node pages: GitHub Pages (hl) — 你的网站地址
edge: term -> git — git add · commit @ Git 记录一个文件夹
edge: term -> gh — gh auth login · repo create @ 还有 gh
edge: gh -> github — 操作 GitHub (seam) @ 命令行工具把两者连接起来
edge: git -> github — git push @ 命令行工具把两者连接起来
edge: github -> pages — 从分支发布 @ GitHub 是一个网站
```

<!-- NOTES: 讲得具体一点。Git 在学员的电脑上；GitHub 是一个网站；gh 在终端里把两者连接起来。初学者的困惑大多来自把 Git 和 GitHub 混为一谈，所以把区别讲一次，然后继续。时间：1 分钟。过渡：打开终端。 -->

---

## 打开终端

| | Windows | macOS |
|---|---|---|
| 应用 | Terminal 或 PowerShell | Terminal |
| 怎么打开 | 按 Windows 键，输入 `terminal`，按 Enter | 按 Cmd+Space，输入 `terminal`，按 Enter |
| 提示符 | `PS C:\Users\ada>` | `ada@Adas-Mac ~ %` |

提示符在等你。在它后面输入，然后按 Enter。

<!-- NOTES: 让每个人现在就打开终端，不要等到后面。在 Windows 11 上，这个应用叫 Terminal，它默认的 shell 是 PowerShell，本模块的每条 Windows 命令都以它为前提。指着提示符说：这里只是一个输入的地方。时间：1 分钟。过渡：安装工具。 -->

---

## 每样工具一条命令安装

Windows — PowerShell。`winget` 随 App Installer 一起提供。

```powershell commands
winget install --id Git.Git -e --source winget
winget install --id GitHub.cli --source winget
```

**然后打开一个新的终端窗口。** macOS — 先安装 Homebrew，运行它打印出的设置命令，然后：

```bash commands
brew install git
brew install gh
```

<!-- NOTES: Windows：winget 随 App Installer 提供，需要 Windows 10 1809 或更高版本；如果系统不认识它，就从 Microsoft Store 安装 App Installer。macOS：先用 Homebrew 官方的安装命令，再运行它打印出的 shell 设置命令——很多人会跳过这一步。Windows 上的坑就是加粗的那一行：安装之前打开的窗口看不到新命令，所以要打开一个新窗口，而不是新标签页。包名用的是维护者自己发布的名字：winget 仓库里的 Git.Git，以及 CLI 的 Windows 安装说明里的 GitHub.cli。时间：3 分钟，另加等待时间。过渡：身份和登录。 -->

---

## 告诉 Git 你是谁，然后登录

```bash commands
git config --global user.name "Ada Example"
git config --global user.email "ada@example.com"
gh auth login
```

依次回答 **GitHub.com**、**HTTPS**、**Yes**，然后选 **Login with a web browser**。

在浏览器里粘贴一次性验证码，之后 Git 推送就不再需要密码。

<!-- NOTES: 两行身份设置，每台电脑只需一次。如果有人不想让自己的邮箱出现在公开历史里，建议他们用 GitHub 的 noreply 地址。然后是 gh auth login：四个提问，默认走浏览器流程。之后，git 推送时会使用这些凭据。时间：2 分钟。过渡：证明它。 -->

---

<!-- _class: proof -->

## 证明：靠脚本，不靠感觉

```text output
PASS  git is installed: git version 2.43.0
FAIL  GitHub CLI (gh) is not installed
      fix: winget install --id GitHub.cli --source winget   then open a NEW terminal window
PASS  git knows who you are: Ada Example <ada@example.com>
FAIL  not signed in to GitHub from the terminal
      fix: gh auth login   (choose GitHub.com, HTTPS, yes to git credentials, ...)

2 of 4 checks passed.
```

`course/03-content/m09-github-pages/setup/check-setup.ps1` · macOS：`setup/check-setup.sh`

<!-- NOTES: 这是 Windows 脚本在 PowerShell 下的真实输出，只改了名字。要点：配置机器这一步，是人们最常以为已经做完、其实并没有做完的步骤，所以检查脚本会为每个失败给出确切的修复方法。修好第一个 FAIL，打开一个新窗口，再运行，直到 4 of 4。时间：2 分钟。过渡：行动步骤。 -->

---

## 行动步骤 — M9.1

- 运行检查，直到显示 **4 of 4**
- 把完整输出粘贴到 `evidence.md`
- 保留每一次失败，以及修好它的那一行

<!-- NOTES: 现在就创建 evidence.md。带着修复方法的失败记录，比一次干净的运行更有价值：它们正是下一位学员需要的东西。时间：30 秒，再加上安装所需的时间。过渡：学会在电脑里找路。 -->

---

## M9.2 — 你总是身处某个位置

```figure
kind: architecture
alt: 五条在 Windows 和 macOS 上完全相同的命令几乎覆盖一切——用 pwd 和 ls 查看，用 cd 移动，用 start 或 open 在窗口里看到文件夹。
layer: 查看 — Windows 和 macOS 上一样
  box: `pwd` — 我在哪里？ @ pwd 显示
  box: `ls` — 这里有什么？PowerShell 也接受 `dir` @ ls 列出
layer: 移动
  box: `cd code` — 进入一个文件夹 @ cd 后面跟
  box: `cd ..` — 回到上一级 @ cd 点点
  box: `cd ~` (hl) — 从任何地方回到主目录 @ 还有 cd 波浪号
layer: 在窗口里看到它
  box: `start .` — Windows @ 想在普通窗口里
  box: `open .` — macOS @ 想在普通窗口里
```

<!-- NOTES: 同样这五条命令，在 PowerShell 和 Mac 终端里都能用，这会让很多人意外。每条演示一次。把 Tab 补全大声说出来：它是避免打错字的最快方法。时间：3 分钟。过渡：路径。 -->

---

## 路径：绝对、相对，以及斜杠

| | Windows | macOS |
|---|---|---|
| 绝对路径：从顶层开始 | `C:\Users\ada\code` | `/Users/ada/code` |
| 相对路径：从这里开始 | `code\my-catalog` | `code/my-catalog` |
| 两边都能用 | `code/my-catalog` | `code/my-catalog` |

带空格的名字需要加引号：`cd "My Projects"`。更好的做法：不用空格，写成 `my-catalog`。

<!-- NOTES: PowerShell 接受正斜杠，所以从网上复制来的命令通常可以原样在 Windows 上运行。在最初几次课里，名字带空格这个坑浪费的时间比其他任何坑都多。时间：2 分钟。过渡：克隆。 -->

---

## 克隆：一份副本，连同历史

```bash commands
cd ~/code
pwd
gh repo clone tomqwu/ai_courses
git clone https://github.com/tomqwu/ai_courses.git
```

两条克隆命令都会在**你当前所在的位置**新建一个文件夹。先运行 `pwd`。

<!-- NOTES: gh repo clone 接受「所有者/名称」形式，并使用已有的登录；git clone 接受绿色 Code 按钮里的完整地址。常见错误是在主目录里克隆，然后在 code 里找不到项目。时间：2 分钟。过渡：把改动送回去。 -->

---

## 把改动送回去的循环

<!-- _diagram: flow -->
- `git status` — 改了什么？
- `git add .` — 选中所有改动
- `git commit -m "…"` — 保存一个版本
- `git push` — 发送到 GitHub

前后各看一遍 `git status`。之后显示干净，就说明全部送上去了。

<!-- NOTES: 四条命令，永远按这个顺序。git add 不出声就表示成功，这会让初学者不安；把这一点说出来。之后的 status 就是证明。时间：2 分钟。过渡：真实运行一遍这个循环。 -->

---

<!-- _class: proof -->

## 证明：真实运行一遍这个循环

```text output
$ git status
Untracked files:  .nojekyll  app.js  index.html  products.js  styles.css
$ git commit -m "Add the catalog starter"
[main c02f59f] Add the catalog starter
 6 files changed, 497 insertions(+), 1 deletion(-)
$ git push
   699905a..c02f59f  main -> main
$ git status
nothing to commit, working tree clean
```

<!-- NOTES: 这是 Git 在产品目录起始项目上实际打印出的循环输出，只是把未跟踪文件列表压缩成了一行。你的短编号会不一样。指着最后一行：那就是证明。时间：1 分钟。过渡：行动步骤。 -->

---

## 行动步骤 — M9.2

- `cd ~/code`，然后克隆本课程
- `cd` 进入它，运行 `ls`
- `cd ..`，然后用 `pwd` 证明你在哪里
- 把两段输出都粘贴到 `evidence.md`

<!-- NOTES: 这一段结束时，每个人都应该已经把课程克隆进 code，并在证据里留下一条 pwd。时间：30 秒，再加上克隆所需的时间。过渡：产品目录。 -->

---

## M9.3 — 五个文件，你只改一个

```figure
kind: architecture
alt: 产品目录起始项目的五个文件——编辑 products.js；只动 index.html 的一行和 styles.css 里的颜色；不要碰 app.js 和空的 .nojekyll。
source: course/03-content/m09-github-pages/catalog-starter/products.js
layer: 编辑 (hl)
  box: `products.js` — 店名、联系方式、产品 @ products.js 保存
layer: 轻轻改动
  box: `index.html` — 只改描述那一行 @ 页面本身是
  box: `styles.css` — 颜色，想改就改 @ 颜色写在
layer: 不要碰
  box: `app.js` — 卡片、筛选、搜索、排序 @ 应用脚本负责
  box: `.nojekyll` — 空文件；告诉 Pages 按原样发布 @ 还有一个名字很奇怪
```

`course/03-content/m09-github-pages/catalog-starter/`

<!-- NOTES: 起始项目故意做得很小：没有框架，没有构建步骤，除了 Git 之外什么都不用装。学员只改一个文件。时间：2 分钟。过渡：为什么数据是一个脚本。 -->

---

## 为什么数据是脚本，而不是 JSON

```js template
{
  id: "everyday-mug",
  name: "Everyday Mug",
  category: "Mugs",
  price: 32,
  summary: "A 350 ml mug with a thumb rest.",
  buyUrl: ""
}
```

从磁盘打开的页面不能读取数据文件，但可以运行脚本。双击即可预览。

<!-- NOTES: 这是唯一值得解释的设计决策。浏览器会阻止用 file:// 打开的页面去获取一个单独的 JSON 文件，但会运行用标签加载的脚本。所以预览只要双击，而且和发布出去的页面完全一样。时间：2 分钟。过渡：同样的模式，更大的规模。 -->

---

## 同样的模式，更大的网站

| | 你的产品目录 | AI × QE |
|---|---|---|
| 数据 | `products.js` | `ai_qe/_data/briefing_room.json` |
| 由谁绘制 | `app.js` | 一个模板循环，`ai_qe/releases.md:222` |
| 如何发布 | 从分支部署 | 一个带检查的 Actions 工作流 |
| 地址 | `<you>.github.io/my-catalog` | `tomqwu.github.io/ai_qe` |

`ai_qe/_config.yml:5` · `ai_qe/.github/workflows/pages.yml:155`

<!-- NOTES: 本课程自己的专业领域案例研究就是一个 GitHub Pages 网站。它的四张简报卡片放在一个数据文件里，由一个模板遍历绘制，和起始项目是同样的分离方式。区别在于发布模式：AI x QE 用 Jekyll 构建，并在 Actions 工作流里先运行自己的检查再部署。同一个托管平台，两种模式。时间：2 分钟。过渡：发布。 -->

---

## 从分支发布

<!-- _diagram: steps -->
- 仓库的 **Settings**（设置），然后 **Pages**
- Source（来源）选 **Deploy from a branch**
- 分支 `main`，文件夹 `/ (root)`
- **Save**，然后最多等十分钟

你的地址：`https://<username>.github.io/<repository>/`

<!-- NOTES: 这些是 GitHub 官方的从分支发布步骤。推送之后，一次改动最多可能需要 10 分钟才会出现；Actions 标签页会显示一次 pages build and deployment 运行。之后的每次推送都会重新发布；学员永远不需要重复这些步骤。时间：2 分钟。过渡：限制。 -->

---

## 限制，来自 GitHub 自己的页面

| 限制 | 数值 | 类型 |
|---|---|---|
| 已发布网站的大小 | 1 GB | 硬限制 |
| 带宽 | 每月 100 GB | 软限制 |
| 构建 | 每小时 10 次 | 软限制 |
| 单次部署 | 10 分钟 | 硬限制 |

**公开**仓库免费；**私有**仓库需要付费计划。

<!-- NOTES: 这四个数字全部来自 GitHub 的限制页面，计划可用性来自它的功能限制说明。对一个产品目录来说很宽裕。每张照片控制在大约 500 KB 以内，大小限制就永远不会成为问题。时间：1 分钟。过渡：决定设计的那条规则。 -->

---

## 是产品目录，不是网店

> GitHub Pages「不打算、也不允许被用作免费的网站托管服务，来经营你的线上业务、电子商务网站，或任何其他主要以促成商业交易或提供商业软件即服务为目的的网站」。

所以起始项目没有购物车。`buyUrl` 链接到在别处运行的结账页面；如果没有，按钮显示 **Ask about this**。

<!-- NOTES: 逐字引用这条规则：它来自 GitHub 自己的限制页面。这就是起始项目这样设计的原因，从一开始就按正确的方式构建，以后就没有什么需要推倒重来。时间：2 分钟。过渡：行动步骤。 -->

---

## 行动步骤 — M9.3

- 用你自己的三个产品替换示例产品
- 双击 `index.html` 预览
- 在 `evidence.md` 里记下每个按钮指向哪里

<!-- NOTES: 真实的产品，或者他们在本课程中正在构建的产品。记录按钮去向这件事，会迫使他们尽早做出收款方面的决定。时间：30 秒。过渡：实验。 -->

---

## 实验 M9 — 发布你的产品目录

| 步骤 | 完成时你会拥有 |
|---|---|
| 0–1 | 一个 GitHub 账号，以及环境检查的 **4 of 4** |
| 2–3 | `~/code`，以及克隆进去的课程 |
| 4 | 你自己的公开 `my-catalog` 仓库，已克隆 |
| 5 | 你的产品，已在你的电脑上预览 |
| 6 | 一次已推送的提交，以及干净的 `git status` |
| 7–8 | 在你手机上能打开的线上地址，然后重新发布 |

<!-- NOTES: 60 到 90 分钟，大部分时间花在安装上。八条检查清单，全部可以客观核验，最后把 evidence.md 提交进 my-catalog。时间：1 分钟。过渡：测验。 -->

---

## 测验 M9 — 考查什么

- 为什么在 Windows 上安装后要开新窗口
- 缺少身份信息实际会阻止什么
- 克隆会落在哪里，以及为什么
- `push` 做了哪些 `commit` 不做的事
- 为什么产品目录要链接到外部结账页面

<!-- NOTES: 六道选择题和两道简答题，每道对应一个目标，答案之后附有对应表。简答题是应用题：一位同学的 Homebrew 环境坏了，以及为一位店主当天发布。时间：1 分钟。过渡：回顾。 -->

---

## 回顾

- **工具，已证明：** winget 或 Homebrew，然后 **4 of 4**
- **文件夹：** `pwd`、`ls`、`cd`、`cd ..`、`mkdir`
- **循环：** status、add、commit、push
- **发布：** Settings、Pages、从 `main` 部署
- **边界：** 展示产品；链接到外部去销售

<!-- NOTES: 五行，每行对应一个学习成果。时间：1 分钟。过渡：讨论题。 -->

---

## 讨论题

贴出你的产品目录地址，以及耗时最长的那个配置步骤，附上修好它的那一行命令。

然后在手机上打开一位同学的产品目录，告诉他们你点的第一个没有按预期工作的东西。

<!-- NOTES: 后半部分是一次微型的可用性测试，大多数学员会在这里发现第一个真正的改进点。时间：1 分钟。 -->
