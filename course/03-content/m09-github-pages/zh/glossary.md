# 术语表 — M9：用 GitHub Pages 发布产品目录

按英文字母顺序排列。每个术语：先给定义，再给出处（仓库指针或课程文件）。

**绝对路径（Absolute path）** — 从磁盘顶层开始的文件夹地址，例如 `C:\Users\ada\code` 或 `/Users/ada/code`。无论你在哪里，它的含义都一样。出处：`lesson.md`，M9.2 分段。

**克隆（Clone）** — 仓库在你电脑上的一份副本，带有完整历史和指向原仓库的链接，用 `gh repo clone owner/name` 或 `git clone <address>` 生成。它会落在你当前所在的文件夹里。出处：`lab.md`，第 3 步。

**提交（Commit）** — 仓库的一个已保存版本，带有一条说明、一位作者和一个短编号，例如 `c02f59f`。先用 `git add` 选中改动，再用 `git commit -m "…"` 生成。出处：`lab.md`，第 6 步。

**从分支部署（Deploy from a branch）** — 最简单的 GitHub Pages 模式：按原样发布某一个分支和文件夹里的文件。在 Settings → Pages 下设置。出处：`lesson.md`，M9.3 分段。

**版本控制工具（Git）** — 在你电脑上记录文件夹各个版本的工具。用 `winget install --id Git.Git -e --source winget` 或 `brew install git` 安装。出处：`setup/check-setup.sh` 和 `setup/check-setup.ps1`。

**代码托管平台（GitHub）** — 保存仓库副本并能把它们发布出去的网站。它和 Git 不是一回事：Git 运行在你的电脑上，GitHub 运行在互联网上。出处：`lesson.md`，M9.1 分段。

**GitHub 命令行工具（GitHub CLI (`gh`)）** — 在终端里操作 GitHub 的命令：登录、创建仓库、克隆。用 `winget install --id GitHub.cli --source winget` 或 `brew install gh` 安装。出处：`setup/check-setup.sh`。

**静态网站托管（GitHub Pages）** — GitHub 从仓库免费托管静态网站的服务，地址为 `https://<owner>.github.io/<repository>/`。不允许用来经营网店。本课程自己的 AI × QE 网站就用它（`ai_qe/_config.yml:5`）。

**主目录（Home folder）** — 终端打开时所在的文件夹，在两个系统上都写作 `~`：Windows 上是 `C:\Users\ada`，Mac 上是 `/Users/ada`。出处：`lesson.md`，M9.2 分段。

**macOS 包管理器（Homebrew）** — macOS 的包管理器。安装时会顺带装上 Apple 的 Command Line Tools，在 Apple 芯片的 Mac 上位于 `/opt/homebrew`。出处：`lab.md`，第 1 步。

**静态站点生成器（Jekyll）** — GitHub Pages 默认运行的网站构建工具。本课程的 AI × QE 网站有意使用它（`ai_qe/.github/workflows/pages.yml:77`）；产品目录则用 `.nojekyll` 把它关掉。

**禁用 Jekyll 的标记文件（`.nojekyll`）** — 一个空文件，告诉 GitHub Pages 按原样发布文件，而不运行 Jekyll。因为名字以点开头，它默认是隐藏的。出处：`catalog-starter/.nojekyll`。

**包管理器（Package manager）** — 用一条命令安装和更新软件的工具：Windows 上是 winget，macOS 上是 Homebrew。出处：`lesson.md`，M9.1 分段。

**提示符（Prompt）** — 终端里等待你输入的那一行，在 PowerShell 里以 `>` 结尾，在 Mac 的 Terminal 里以 `%` 结尾。出处：`lesson.md`，M9.1 分段。

**推送（Push）** — 用 `git push` 把你的新提交发送到 GitHub。在你推送之前，一次提交只存在于你的电脑上，Pages 无法发布它。出处：`lab.md`，第 6 步。

**相对路径（Relative path）** — 从你当前位置出发的文件夹地址，例如 `code/my-catalog` 或 `..`。出处：`lesson.md`，M9.2 分段。

**仓库（Repository）** — 一个由 Git 记录其历史的文件夹，加上它在 GitHub 上的副本。在终端里用 `gh repo create` 创建。出处：`lab.md`，第 4 步。

**环境检查脚本（Setup check）** — 检测 Git、GitHub CLI、你的身份和你的登录状态的脚本，并为任何失败打印确切的修复方法。出处：`setup/check-setup.sh` 和 `setup/check-setup.ps1`。

**终端（Terminal）** — 一个输入命令而不是点击的窗口：Windows 上是 Terminal 或 PowerShell，macOS 上是 Terminal。出处：`lesson.md`，M9.1 分段。

**Windows 包管理器（winget）** — Windows Package Manager，随微软的 App Installer 一起提供；需要 Windows 10 1809 或更高版本。出处：`lab.md`，第 1 步。

**工作区干净（Working tree clean）** — 所有改动都已提交时 `git status` 显示的内容。推送之后，它就是一切都已送达的证明。出处：`lab.md`，第 6 步。
