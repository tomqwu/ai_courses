# 讲义 — M9：用 GitHub Pages 发布产品目录

放在终端旁边的一页纸。Windows 命令适用于 PowerShell。

## 安装并证明

| | Windows | macOS |
|---|---|---|
| 包管理器 | `winget --version`（不行就从 Store 安装 App Installer） | Homebrew 的安装命令，然后运行它打印出的设置命令 |
| Git | `winget install --id Git.Git -e --source winget` | `brew install git` |
| GitHub CLI | `winget install --id GitHub.cli --source winget` | `brew install gh` |
| 安装之后 | **打开一个新的终端窗口** | — |
| 证明它 | `powershell -ExecutionPolicy Bypass -File .\check-setup.ps1` | `bash check-setup.sh` |

每台电脑一次：

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
gh auth login        # GitHub.com → HTTPS → Yes → Login with a web browser
```

## 学会找路

| | 两个系统通用 |
|---|---|
| 我在哪里？ | `pwd` |
| 这里有什么？ | `ls` |
| 进入 / 上一级 / 主目录 | `cd code` · `cd ..` · `cd ~` |
| 新建文件夹 | `mkdir code` |
| 在文件窗口里打开 | `start .`（Windows）· `open .`（macOS） |

把每个项目都放在 `~/code` 里。文件夹名里不要有空格。按 Tab 补全名字。

## 克隆，然后是循环

```bash
cd ~/code
gh repo clone owner/name          # or: git clone https://github.com/owner/name.git
git status                        # what changed?
git add .                         # choose every change
git commit -m "Say what changed"  # save one version
git push                          # send it to GitHub
```

克隆会落在你当前所在的文件夹里。`push` 之后，`git status` 应该显示 **working tree clean**。

## 发布

仓库 → **Settings** → **Pages** → Source 选 **Deploy from a branch** → `main`、`/ (root)` → **Save**。
地址：`https://<username>.github.io/<repository>/`。每次推送后最多 10 分钟生效。

## 限制

已发布网站 1 GB · 带宽每月 100 GB（软限制）· 每小时 10 次构建（软限制）· 每次部署 10 分钟。
公开仓库免费。

**Pages 展示产品；它不销售产品。** GitHub 的条款禁止在 Pages 上经营网店。把每个产品的 `buyUrl`
链接到在别处运行的结账页面，或者干脆不写，按钮就会显示 "Ask about this"。

## 出了问题时

| 你看到 | 这样做 |
|---|---|
| 刚安装完，某条命令 "is not recognized" | 打开一个新的终端窗口 |
| `brew: command not found` | 运行 Homebrew 打印出的设置命令 |
| "products.js did not load" | 找到缺失的逗号；浏览器控制台会指出是哪一行 |
| "ahead of 'origin/main' by 1 commit" | `git push` |
| 你的地址显示 404 | 等待 Actions 运行完成；检查文件夹是否为 `/ (root)` |
