# 会话 Hook 验证记录

> **历史档案。** 本文记录的会话 Hook 与角色已于 2026-11-06 从 Magpie 资源库移除，仅作证据存档，不代表当前配置。当前会话开始、任务边界与收尾核对均由主代理按指令与技能直接执行。

日期：2026-11-05。环境：Windows、Codex CLI 0.166.0、Python 3.13、RTK 1.1.0。

## 本次改动

- 会话提醒脚本移入 Magpie 资源库本技能的 `scripts/engineering-session-context.py`，随技能分发。
- Magpie 的 `engineering-session-context` 命令通过 PATH 中的 `python`，从 `CODEX_HOME` 或默认 `~/.codex` 的技能目录加载脚本，去掉固定用户名和 Python 版本目录。
- 保留现有 SessionStart 触发方式、5 秒超时及当时的 RTK PreToolUse 配置；RTK PreToolUse 已在同一日的后续复核中移除，现行状态见下文。脚本只识别工程并补上下文，无项目写入、网络、测试或提交操作。
- 已执行 Magpie 同步，并通过 Codex `/hooks` 审阅、信任变更后的会话 Hook。

## 直接测试：12 项通过

以实际同步后的命令输入 Hook JSON，核对退出状态和输出：

| 测试范围 | 结果 |
|---|---|
| startup、resume、compact 三种事件输入 | 均输出工程提醒 |
| Git 子目录、worktree 的 `.git` 文件、仅有 AGENTS.md 的工程 | 均正确识别 |
| 无工程标记、缺失 cwd、相对 cwd | 均无上下文输出 |
| CODEX_HOME 迁移到含空格路径 | 正确加载分发脚本 |
| RTK 支持的 `git status --short` | 改写为 `rtk git status --short` |
| RTK 不支持的 `echo hook-rtk-check` | 不改写 |

上述事件输入测试与以下真实生命周期测试分别记录，不相互替代。

## 真实 Codex 集成测试：通过

使用本机 Codex App Server，保留现有模型配置，仅在测试会话关闭无关 Magpie MCP；没有绕过 Hook 信任。

| 场景 | 实际观察 |
|---|---|
| 配置发现与信任 | 会话 Hook、RTK 均 enabled=true、trustStatus=trusted；无加载 errors/warnings |
| 新会话首轮 | 收到 SessionStart 的 started/completed 通知；状态 completed，context 条目含工程提醒，耗时 550 ms |
| RTK 真实工具调用 | 收到 PreToolUse completed；实际 commandExecution 为 `rtk git status --short`，退出码 0；回合正常结束 |
| 新进程恢复同一会话 | SessionStart completed，context 条目含提醒，耗时 688 ms；回合正常结束 |
| 显式压缩会话后继续 | compact 请求及回合完成；下一轮 SessionStart completed，context 条目含提醒，耗时 566 ms；后续回合正常结束 |

工程技能的 `quick_validate.py` 校验通过。同步后另核对源与分发脚本一致；当时 RTK PreToolUse 配置未改，后续复核已将其移除，见下文。

## 边界与证据

- 真实生命周期证据来自独立 CLI/App Server 测试会话；没有把“同步成功”或“已信任”单独当作执行成功。未逐一验证所有桌面窗口、其他 Agent 或其他电脑。
- `codex debug prompt-input` 虽返回成功，但未包含本次 Hook 上下文，因此不作为成功证据；采用真实 Hook completed 的 context 条目及实际工具执行记录。
- 验证的是通用 Hook；没有执行若依工程的构建或业务测试，也未更改项目代码。
- 本机备份及结构化测试证据位于 `C:\Users\s1a71\.config\magpie\backups\hook-portability-20261105-144323`。其中包含私人配置，不上传或提交。
- 资源库目录不是 Git 仓库，文件保留在 Magpie 源目录，本次未创建 Git 提交。

## 后续复核：RTK Codex Hook 当前未启用

2026-11-05 后续复核发现，以上 RTK 集成测试不能代表当前安装状态。当前 `rtk verify` 报告 `RTK hook not installed`；将包含 `tool_name: Bash` 和 `tool_input.command` 的 PreToolUse JSON 输入 `rtk hook codex`，进程退出码为 0，但没有输出改写结果。RTK 版本为 1.1.0，`magpie library rtk` 显示 Codex 为 off。此前记录的真实工具调用改写可能反映当时状态，但无法由当前配置复现，故不再据此宣称 RTK Hook 正常。

核对 Codex 官方 Hook 文档（[Hooks](https://learn.chatgpt.com/docs/hooks)）后，PreToolUse 改写必须输出带 `hookSpecificOutput.hookEventName: PreToolUse`、`permissionDecision: allow` 和 `updatedInput.command` 的 JSON。当前 RTK 调用没有输出该结果。已通过 RTK 自带卸载命令移除用户级及当前工作区的 RTK Codex Hook、RTK.md 和对应 AGENTS.md 引用；Magpie SessionStart Hook 保留。RTK CLI 本身没有卸载；`rtk git status --short` 实际执行成功，`rtk verify` 的 151 项检查通过，因此输出压缩能力仍可通过显式 `rtk <command>` 使用。重新启用自动改写前，应先让 `rtk hook codex` 对有效输入实际输出符合官方契约的 JSON，并通过 Codex 工具调用验证改写。

本次复核不撤销上文已验证的 SessionStart 生命周期结果；也未重新测试 déjà 跨会话召回或所有 Codex 前端的 Hook 加载行为。

同日另将 SessionStart 的上下文提示收紧为：检测到 `project-state.md`、`project-decisions.md` 或 `verification.md` 时，先核对记录是否落后于当前 Git 状态和代码；实质任务完成时只同步确实受影响的记录，不机械重写全部文件。Hook 仍只负责提醒，不自动修改文档。

后续新增只读任务边界检查 `engineering-task-guard`：`UserPromptSubmit` 保存本轮 Git 快照，`Stop` 仅在本轮工程文件确实变化而三份运行态记录未变化时返回一次收尾提示。它不写文件、不提交、不推送；没有新事实时文档无需修改。该 Hook 是流程提醒，不是交付权限的替代品。

Magpie 资源库登记 Hook 时使用内部事件名：`prompt` 映射到 Codex 的 `UserPromptSubmit`，`turn-end` 映射到 `Stop`。首次曾误填 Codex 风格的事件名，`magpie library sync` 明确报告 `no event called user-prompt-submit` / `no event called stop`，因此未写入运行配置；改为内部事件名后同步成功。以后修改 Hook 定义时应先核对 `applied.codex.hooks` 的实际事件与 `~/.codex/hooks.json`，不能只看源配置。

`engineering-task-guard` 的行为测试通过：临时仓库中，工程文件变化而运行态记录未更新时返回 `decision=block`；运行态记录更新、缺少三份记录、无工程变化、`stop_hook_active=true`、无本轮快照时均为静默、退出码 0。首次测试发现快照比较范围不一致（记录时包含 `AGENTS.md`，结束时只比较三份运行态记录），已统一为同一范围后重跑通过。

同日优化了交付编排：默认由主代理自检后直接更新运行态文档、提交并推送到已有正常上游，不启动子代理；UI 或中高风险任务按需启动只读检查，只有用户要求独立收尾或确需隔离时才使用 `delivery-closer`。这样避免小任务被多个子代理串行拖慢，同时保留高风险任务的独立检查能力。

## 真实 Codex 端到端验证（2026-11-05）

在临时 Git 仓库和裸远程仓库中，用真实 `codex exec` 会话验证默认快速路径，不触碰现有工程：

| 场景 | 实际观察 |
|---|---|
| 明确要求实现、文档同步、提交和推送 | Codex 读取工程技能，只改目标文件，判断没有新状态事实时不改运行态文档，扫描暂存内容，创建本地提交并推送；本地与远端一致，工作区干净 |
| 只给出普通实现指令，不额外交代 Git | Codex 按默认快速路径完成实现、提交并推送，未启动子代理，验证了“只提需求”的日常用法 |
| 用户明确限定“只改这个文件” | Hook 仍触发一次文档检查，属于误提醒；随后增加显式范围排除识别并复测通过 |
| 两次真实会话中的 Hook | 观察到 `UserPromptSubmit` 保存了本轮快照，`Stop` 在代码已提交而文档未更新时触发提醒，证明 Hook 不是只登记未执行 |

端到端测试同时暴露并修复了快照语义缺口：原实现只比较工作区状态，代码已提交且工作区重新干净时，开始和结束快照相同，导致漏提醒。现已把 `HEAD` 提交号纳入快照；补测“未提交代码、文档未更新”“已提交代码、文档未更新”均触发，“代码与文档一起提交”“只提交文档”均静默。

显式范围排除补测通过：`只改 README.md，不要修改其他文件` 和 `只修改这一个文件` 均保持静默；普通“实现这个功能”仍会在文档未更新时提醒。该判断只识别明确的范围限制，不扩大为对任务内容的猜测。

以后修改 Hook 定义后应重新同步、检查信任状态，并对相关行为做定向验证；技能脚本更新也应实际验证，不以既有成功记录代替当前结果。

## 2026-11-06：交付阶段补齐

原 Stop Hook 只在“代码改动但三份运行态记录未变化”时提醒；若文档已经同步，则不会再提醒尚未提交的本任务改动，无法完整覆盖“文档更新后紧接着 Git 收尾”的固定流程。

现已扩展为只读两阶段守卫：

1. 有工程改动但运行态记录未变化：提醒核对状态、决策或验证记录；没有新事实时明确说明无需修改。
2. 文档已核对或确认无需修改，但本任务仍有未提交改动：提醒只暂存本任务路径、运行凭证扫描、创建本地提交，并在满足正常上游、非受保护/默认分支和授权条件时推送。

用户明确说“先别提交”时只停止提交提醒，文档核对仍可继续；明确说“先别改文档”时跳过文档催办、继续提醒提交；明确说“不要推送”时只提交并报告未推送。Hook 不执行写文件、`git add`、`git commit` 或 `git push`。

隔离仓库验证场景全部通过：代码改动无文档记录、代码与文档同时改动、代码与文档完整提交、只提交代码、代码先提交后补文档、用户禁止提交、用户禁止改文档、用户禁止推送、会话开始前已有未触碰脏文件、会话中修改已有脏文件、存在无关暂存时完成本任务、仅文档改动。最终回归按两阶段提醒语义及独立豁免执行 10/10 与 4/4 通过；全部在临时 Git 仓库完成，没有连接真实项目、远程、数据库或 SSH。
