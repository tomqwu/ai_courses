# 实验 M0 — 环境搭建与首次交付成果

> **目标：** 课程需要的每个工具都已安装，并用一次真实输出证明可用——在第 1 模块之前，你就已经端到端运行过真实软件。
> **从没用过终端，或者还不会克隆仓库？** 先学免费的第 9 模块（`course/03-content/m09-github-pages/lab.md`）：它会在 Windows 或 macOS 上安装 Git 和 GitHub CLI，用一个脚本证明安装成功，并教会本实验默认你已掌握的每一条命令。
> **前置条件：** 无。**时间：** 约 30 分钟，包括下载（`make setup`、Ollama 安装程序、模型拉取）；下面的「进入第 1 模块之前」部分再加约 10 分钟。
> **通过关卡：** 完整的求解器摘要块（包含 `Health score:` 行和 `Solution saved to …` 行），加上非空的 `ollama list`。

## 步骤

1. **克隆三个案例研究**（这个工作区可能已经有了——如果有，直接跳到第 2 步）：
   ```bash
   git clone https://github.com/tomqwu/ListenToMe.git
   git clone https://github.com/tomqwu/SignUpFlow.git
   git clone https://github.com/tomqwu/ai_qe.git
   ```
2. **确认你的 Python**：`python3 --version` → 3.11 或更新（SignUpFlow 自己的最低版本；TinyCopilot 本身在 3.10 上也能运行）。
3. **安装 Ollama**，从 <https://ollama.com/download> 下载（macOS、Linux、Windows）。然后拉取一个真正的本地模型：
   ```bash
   ollama pull qwen3:0.6b
   ollama list          # note which names end in :cloud (cloud-backed aliases) and which don't
   ollama run qwen3:0.6b "Reply with exactly: PONG"
   ```
4. **运行 SignUpFlow 求解器**（一个真实的生产排班器，不超过 5 条命令）：
   ```bash
   cd SignUpFlow && make setup          # Poetry env + migrations (see README if you hit issues)
   poetry run python -m api.cli.main init my-church
   poetry run python -m api.cli.main solve my-church
   ```
   截取整个输出块：人员、活动、**健康分（health score）**那一行、违规、公平性标准差、指派，以及 `Solution saved to …` 那一行。分数就是你克隆的版本下示例工作区产出的结果（`SignUpFlow/api/cli/main.py:193`）——在 2026-09-16 的 head 上是 `0.0/100`，有两个硬约束违规。不要去「修正」这个数字；把它记录下来。
5. **在社区发布你的首个成果**：你的求解器输出块 + 你的 `ollama list`（每个条目都标注本地或 `:cloud`）+ 一句话说明你想在第 8 周之前构建哪种产品原型（1：端侧应用，2：SaaS，3：专业知识产品）。

## 验收清单

- [ ] 三个仓库都已克隆到本地
- [ ] `python3 --version` 显示 3.11+
- [ ] `ollama list` 至少显示一个模型；你能分辨哪些是本地模型、哪些是 `:cloud` 别名
- [ ] 求解器已运行；完整的摘要块，包括 `Health score:` 和 `Solution saved to …` 两行，已经截取
- [ ] 证据日志已开始（见下文）
- [ ] 首个成果帖已发布

通过关卡是求解器输出块加上非空的 `ollama list`。帖子是一项清单条目，也是推动学员完成的抓手（`course/02-instructor/instructor-guide.md` §1），而不是自动不通过项；唯一的自动不通过是捏造输出。

## 进入第 1 模块之前

- **开始你的课程证据日志（evidence log）**（整门课都要维护）：粘贴求解器输出块和 `ollama list`，每条都附上日期，并用一行写明哪些仍未验证。
- **拓展——运行 TinyCopilot 实验测试**（第 2 模块实验的参考实现，也是第 2 模块自己的通过关卡）：
  ```bash
  cd ../course/03-content/m02-ondevice-app/tinycopilot
  python3 -m pytest tests -q    # or: make lab-m2
  ```
  预期：`208 passed`，覆盖率 `100%`。如果缺少某个依赖，记录确切的包名和错误行——在这里，诚实的部分完成没有问题；实验 M2 才是这个套件被评分的地方。拿到 pytest 汇总行后，把它加进你的证据日志。

## 拓展目标

- Mac 用户？打开 `ListenToMe/README.md`，按 `make run` 启动真实的应用（需要 macOS 26 + Xcode）。
- 运行一次 AI × QE 检查：`cd ai_qe && cat _data/release.yml`——找出各自独立的版本字段（`version`、`slide_edition`、`fintech_edition`、`questionnaire_edition`、`research_edition`）。四个版次按各自的节奏变化；这就是「内容即代码」，第 6 模块会讲到。

## 讨论题

介绍一下你自己：你的技术栈、你最想构建的产品原型，以及一件你以前交付过的东西（附上仓库链接算双倍）。
