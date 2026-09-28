# 实验 M1 — 构建你的操作系统，然后跑一次循环

> **目标：** 交付一个起始仓库，其中包含你自己的宪章、一份 `AGENTS.md` 和一个导入它的 `CLAUDE.md`、规格模板，以及一个检查你证据日志的钩子——并在一个 `todo` CLI 功能上跑通一次完整的规格 → 计划 → TDD 循环，以此证明它能用。
> **前置条件：** 已完成第 0 模块的实验；已读完第 1 模块的课文。**时间：** 约 2 小时。

## 步骤

1. **创建仓库**
   ```bash
   mkdir my-studio && cd my-studio && git init
   python3 -m venv .venv && source .venv/bin/activate
   pip install pytest
   mkdir -p specs/001-todo-command docs tests scripts .claude
   touch docs/research-log.md docs/evidence-log.md
   printf '.venv/\n__pycache__/\n' > .gitignore
   git add -A && git commit -m "Scaffold starter repo"
   ```
   第一次提交让 `git rev-parse HEAD` 有一个版本可以打印，第 8 步的证据条目需要它。
2. **写 `constitution.md`（≤80 行）** SignUpFlow 自己的宪章在本实验写成之后已经增长到 85 行（`SignUpFlow/.specify/memory/constitution.md`）；这个上限是给*你的第一份*宪章的——简洁本身就是要练的技能。复制下面的内容，然后把三处方括号部分改成你自己的：
   ```markdown
   # <Project> Constitution
   ## Principles
   1. Test-Driven Implementation: write the failing test first; the change is not
      done until `python3 -m pytest tests/ -q` passes.
   2. Simplicity & YAGNI: build exactly what's needed, nothing more.
   3. Safety & Reliability: [<your rule — e.g., never commit API keys; read them
      from environment variables>].
   ## Autonomy Configuration
   - YOLO Mode: DISABLED
   - Git Autonomy: ENABLED (commit when a task completes and tests pass)
   - When unsure whether an action is reversible, stop and ask.
   ```
   （范本：`SignUpFlow/.specify/memory/constitution.md`——85 行。）
3. **写 `AGENTS.md`（≤200 行），再写一个导入它的 `CLAUDE.md`** 每条规则都要是祈使语气且可验证；包含一份验证检查清单：
   ```markdown
   # AGENTS.md
   ## House style
   - Use imperative voice. Each rule must be verifiable.
   - Keep this file under ~200 lines.
   ## Anti-hallucination
   - Do not invent file paths, function names, or commands. Grep the repo first.
   - When the request is ambiguous, present 2-3 differentiated options.
   ## Project rules
   - [<e.g., Run pytest before declaring any change done.>]
   ## Validation checklist (before declaring done)
   - [ ] `python3 -m pytest tests/ -q` passes.
   - [ ] No secrets in the diff: `git diff | grep -iE 'api[_-]?key|secret|token'`
         returns nothing meaningful.
   - [ ] Docs touched by the change are updated; stale docs are a failure.
   ```
   然后是 `CLAUDE.md`：第一行是导入语句，下面只放 Claude Code 专有的内容。所有共享的内容都留在 `AGENTS.md` 里，这样没有任何内容写两遍。导入会完整加载 `AGENTS.md`，所以要让 `wc -l AGENTS.md CLAUDE.md` 的合计保持在 ≤200 行。
   ```markdown
   @AGENTS.md

   ## Claude Code addenda
   - A Stop hook runs `scripts/check-evidence-log.sh` after each turn. When it
     blocks, fix the entry it names; never edit the script or hook to pass.
   - Record the red run in `docs/evidence-log.md` before the green run.
   ```
   第一条附加说明指向你在第 8 步接上的钩子。在 Claude Code 中运行 `/context`，确认这个文件已经加载。其他智能体会直接读取 `AGENTS.md`，并忽略 `CLAUDE.md` 和钩子；这种情况下，就自己运行第 8 步的检查。
4. **写 `specs/001-todo-command/spec.md`**——做什么（WHAT），与技术无关，包含两个可独立测试的用户故事：
   ```markdown
   # Spec: todo command
   ## US1 (P1): Add and list todos
   As a user, I can add a todo and list all todos, so I can track work.
   - Given an empty store, When I add "write spec", Then listing shows one item
     with id 1, title "write spec", done=false.
   ## US2 (P1): Mark done
   As a user, I can mark a todo done, so completed work stops nagging me.
   - Given todo 1 exists, When I mark 1 done, Then listing shows done=true.
   ```
5. **写带关卡的 `specs/001-todo-command/plan.md`**
   ```markdown
   # Plan: todo command
   ## Constitution Check — GATE: must pass before implementation. Re-check after.
   - [x] TDD respected (tests written first). [x] YAGNI (no storage file, no dates).
   ## Tasks
   ```
6. **写 `specs/001-todo-command/tasks.md`**——精确路径，先写测试：
   ```markdown
   ## Format: [ID] [P?] [Story] — include exact file paths
   - [ ] T001 [P] [US1] Create tests/test_todo.py: failing tests for add + list
   - [ ] T002 [US1] Create todo.py: TodoStore.add(title) -> int, TodoStore.list()
   - [ ] T003 [P] [US2] Add failing test for done to tests/test_todo.py
   - [ ] T004 [US2] Extend todo.py: TodoStore.done(todo_id)
   - [ ] T005 Add CLI dispatch in todo.py: add/list/done via sys.argv
   ```
7. **用 TDD 跑这个循环** 执行 T001：先写失败的测试——
   ```python
   # tests/test_todo.py
   from todo import TodoStore

   def test_add_then_list():
       s = TodoStore()
       assert s.add("write spec") == 1
       assert s.list() == [{"id": 1, "title": "write spec", "done": False}]

   def test_done_marks_item():
       s = TodoStore()
       i = s.add("ship")
       s.done(i)
       assert s.list()[0]["done"] is True
   ```
   运行 `python3 -m pytest tests/ -q`——由于还没有 `todo.py`，pytest 会在收集阶段停止：`ERROR tests/test_todo.py`、`ModuleNotFoundError: No module named 'todo'`、`1 error`，退出码 2。这个收集错误*就是*红——原样记录下来（它不是「2 failed」；这两个测试根本没有运行）。然后执行 T002/T004：实现 `todo.py`（一个由字典组成的列表；`add` 追加并返回 id；`done` 设置标志）。再次运行 pytest——记录通过的结果（绿）。完成 T005，然后运行你的完整验证检查清单。
8. **按规定格式在 `docs/evidence-log.md` 中记录证据，然后接上检查它的钩子**
   ```markdown
   ## Evidence — my-studio — todo command — <YYYY-MM-DD>
   Commands (with results):
   - python3 -m pytest tests/ -q (before implementation) → 1 error: ModuleNotFoundError: No module named 'todo' (exit 2)
   - python3 -m pytest tests/ -q (after implementation) → <N> passed
   Environment: <OS, Python version>
   Revision: <output of `git rev-parse HEAD`>
   Limitations / not verified:
   - In-memory store only; CLI arg handling tested by hand, not automated.
   ```
   「每个条目都有全部六个字段」这条规则可以由脚本判定，所以 M1.1 中的那张表说它应该是一个钩子。把检查脚本保存为 `scripts/check-evidence-log.sh`：
   ```bash
   #!/usr/bin/env bash
   # Checks the latest entry in docs/evidence-log.md. Exit 0: no entry yet, or all
   # six fields are filled. Exit 2: something is missing (Claude Code reads stderr).
   cd "$(dirname "$0")/.." || exit 2
   log=docs/evidence-log.md
   [ -f "$log" ] || { echo "Evidence log: no $log yet."; exit 0; }
   entry=$(awk '/^## Evidence/ {f=1; b=""} f {b = b $0 "\n"} END {printf "%s", b}' "$log")
   [ -n "$entry" ] || { echo "Evidence log: no entry yet."; exit 0; }
   miss=""
   has() { printf '%s\n' "$entry" | awk "$1" || miss="$miss- $2"$'\n'; }
   has '/^## Evidence.*[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]/ {ok=1} END {exit !ok}' "a YYYY-MM-DD date in the heading"
   has '/^Commands/ {c=1; next} /^Environment:/ {c=0} c && /^- .*(→|->) *[^ <]/ {ok=1} END {exit !ok}' "a '<command> → <result>' line"
   has '/^Environment: *[^ <]/ {ok=1} END {exit !ok}' "an Environment value"
   has '/^Limitations/ {l=1; next} l && /^- *[^ <]/ {ok=1} END {exit !ok}' "at least one limitation"
   sha=$(printf '%s\n' "$entry" | sed -n 's/^Revision: *`\{0,1\}\([0-9a-f]\{7,40\}\).*/\1/p' | head -n 1)
   git cat-file -e "${sha:-none}^{commit}" 2>/dev/null || miss="$miss- a Revision SHA that exists in this repo"$'\n'
   if printf '%s\n' "$entry" | grep -q '<[^>]*>'; then miss="$miss- no <placeholders> left"$'\n'; fi
   if [ -n "$miss" ]; then
     printf 'Evidence log: the latest entry in %s needs:\n%s' "$log" "$miss" >&2
     exit 2
   fi
   echo "Evidence log: latest entry complete."
   ```
   在 `.claude/settings.json` 中把它绑定到 Claude Code 的 `Stop` 事件，这个事件在 Claude 每次结束一轮时触发：
   ```json
   {
     "hooks": {
       "Stop": [
         {
           "hooks": [
             {
               "type": "command",
               "command": "bash \"${CLAUDE_PROJECT_DIR}\"/scripts/check-evidence-log.sh"
             }
           ]
         }
       ]
     }
   }
   ```
   在信任这个检查之前先测试它：先红，后绿。从你的条目中删掉局限那一行，运行 `bash scripts/check-evidence-log.sh; echo "exit=$?"`。预期输出 `Evidence log: the latest entry in docs/evidence-log.md needs:`，接着是 `- at least one limitation`，然后是 `exit=2`。把那一行放回去，预期输出 `Evidence log: latest entry complete.` 和 `exit=0`。两次运行都要记录。在 Claude Code 会话中，`Stop` 上的退出码 2 会让 Claude 继续工作，并把脚本的 stderr 当作它的指示。连续阻止八次之后，Claude Code 会让这一轮结束（code.claude.com/docs/en/hooks，2026-09-26 查阅）。这个钩子检查的是形式：带日期的标题、一行 `command → result`、一个环境、一个在这个仓库中存在的 SHA、一条局限，以及没有 `<placeholders>`。它无法检查其中任何内容是否属实。
9. **提交** 提交正文采用 `SignUpFlow/AGENTS.md` 中的格式：Summary / Changed files / Validation / Follow-ups。

## 验收清单

- [ ] `constitution.md` 存在，≤80 行，≥3 条原则，有自主权配置
- [ ] `AGENTS.md` 存在，≤200 行，每条规则都是祈使语气 + 可验证，包含验证检查清单
- [ ] `CLAUDE.md` 以 `@AGENTS.md` 开头，只包含 Claude 附加说明；`AGENTS.md` + `CLAUDE.md` 合计 ≤200 行
- [ ] `.claude/settings.json` 把 `scripts/check-evidence-log.sh` 绑定到 `Stop`；检查的红色运行（退出码 2）和绿色运行（退出码 0）都已记录
- [ ] `specs/001-todo-command/spec.md` 有 2 个用户故事，每个都有 ≥1 个 Given/When/Then
- [ ] `plan.md` 包含一道宪章检查关卡，并明确已通过
- [ ] `tasks.md` 有 ≥5 个 `[ID] [Story]` 任务，每个都引用精确的文件路径，先写测试
- [ ] 已记录红色运行：实现之前的收集错误，输出已保存
- [ ] 绿色运行：`python3 -m pytest tests/ -q` 以 0 退出
- [ ] 证据条目包含命令、计数、日期、环境、局限、head SHA
- [ ] `docs/research-log.md` 有 ≥1 条带日期的观察
- [ ] 有一条提交正文遵循 Summary / Changed files / Validation / Follow-ups 格式

## 证据记录

在 `docs/evidence-log.md` 中保留：红色的 pytest 输出、绿色的 pytest 输出、`git rev-parse HEAD`、按第 8 步格式写的证据条目，以及 `scripts/check-evidence-log.sh` 的两次运行（先退出码 2，后退出码 0）。这个文件是你在之后每个模块中的证明资产——相当于本课程版本的 SignUpFlow `docs/playbooks/validation.md`。

## 拓展目标

- 加一个负路径测试：标记一个不存在的 id 会抛出一个明确定义的错误（`SignUpFlow/AGENTS.md` 要求每个功能都有负路径断言）。
- 让一条真实的观察完成晋级：把它带日期加进 `docs/research-log.md`，在这次改动上试用，然后提升进 `AGENTS.md`——这就是 `SignUpFlow/docs/ai-agent-coding-strategy.md` 中的完整流水线。
- 不重读本实验，跑第二个迷你循环（`specs/002-todo-remove/`）。

## 讨论题

发布你改写前 → 改写后的规则（一条你改写得可验证的模糊规则），以及你仓库的链接。然后评审一位同学的 `AGENTS.md`：你能否在不问他们任何问题的情况下，检查每条规则是否都被遵守？指出任何你无法验证的词。
