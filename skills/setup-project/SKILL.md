---
name: setup-project
description: "Initialize or reconfigure a repository's engineering setup: project state, domain docs, compile and run commands, coding profile, and optional issue tracker. Use when the user says 按通用资源库配置这个项目 or asks to refresh project collaboration. Not required for every task."
---

# Setup Project

为当前仓库建立后续技能需要读取的项目事实。它是初始化/重配入口，不是每次开发的前置门槛；已有 `docs/agents/` 时可重复运行，只更新变化部分。

## Global-first 默认

全局 Magpie 指令是工作原则、工作流、编译口径、页面验收时机和 Git 规则的唯一来源。项目只保存**项目事实**，不复制全局流程。

- 默认不创建、不修改 `AGENTS.md` / `CLAUDE.md`。
- 如果文件已存在或用户明确要求，只写项目事实和指向 `docs/agents/` 的短指针。
- 项目专属原则（文件大小、依赖检查路径、验证命令）写入 `docs/agents/coding-standards.md`。
- 默认技术 profile 是 `ruoyi6`（RuoYi-Vue-Plus 6.x + React；实际版本从当前项目根 `pom.xml` 和 `plus-ui-React/package.json` 读取）。不通过框架签名探测、不单独问“是不是 RuoYi”；用户明确说非 RuoYi 时，记录 `Technical profile: none` 或用户指定的替代 profile 及理由。
- Hook 默认不安装。项目明确启用时，只登记项目级适配器和职责，不修改机器级 Hook 索引；事件边界见 [Hook 护栏](../rules/hook-guardrails.md)。

## 产出

| 文件 | 内容 |
|---|---|
| `docs/agents/domain.md` | `CONTEXT.md`、PRD、ADR、research 的实际路径 |
| `docs/agents/coding-standards.md` | 项目约定、技术 profile、源码证据、实际编译与启动命令 |
| `docs/agents/project-state.md` | 当前目标、阶段面板、阻塞、下一步、前后端编译命令、启动命令与端口 |
| `docs/agents/project-decisions.md` | 已确认、跨任务有效的决策 |
| `docs/agents/verification.md` | 带版本/提交、命令、结果、日期的验证证据 |
| `docs/agents/language.md` | 文档语言 |
| `docs/agents/issue-tracker.md` | 可选：本地 Markdown 或远端 Issue 跟踪方式 |
| `docs/agents/triage-labels.md` | 可选：Issue 标签映射 |
| `docs/agents/repo-map.md` | 多仓时记录仓库职责和主跟踪仓库 |
| `AGENTS.md` / `CLAUDE.md` | 仅已存在或用户明确要求时更新，写短指针 |

这些文件是消费者技能的读取入口，具体读取顺序见 [Skill Entry Protocol](../rules/entry-protocol.md)。

遇到结构性迁移、旧项目配置审计或需要完整重跑清单时，再读 [REFERENCE.md](REFERENCE.md)；普通首次初始化和只更新少量字段不需要预读。

## Process

**Step 1 — Explore.** 检测仓库根、remote、已有 `AGENTS.md`/`CLAUDE.md`、已有 `docs/agents/`、单仓/单包/多仓结构、前后端目录、构建文件和现有文档。已有配置时先读全，不覆盖用户手写内容。重跑时额外扫描已有指令和项目文档中的过期技能/profile 引用：`engineering-workflow`、`ruoyi-plus-dev`、`project-context`、`prompt-engineering`、`scm-collaboration`、已删除的 Vue 长期前端规范，以及与实际 `Technical profile` 不一致的流程说明。发现漂移只报告并纳入差异草案，确认后再改；不静默保留过期引用。

**Step 2 — Detect.** 识别项目结构、实际前端位置、后端模块、数据库脚本、测试/构建/启动命令、监听端口、Issue 跟踪现状。无法从仓库确认的多仓关系才问用户。

**Step 3 — Present.** 先展示检测到的默认配置：结构、Issue 跟踪、领域文档、语言、技术 profile、编译命令、启动命令和端口。更新时展示与当前配置的差异，并列出过期技能/profile 引用及其所在文件。

**Step 4 — Ask overrides.** 一次性展示完整草案，只问“是否需要调整”；用户要改时按 A–H 逐项处理，每次只问一个决定：

- A. Issue Tracker：默认本地 Markdown；需要 GitHub/GitLab/Gitee 时记录平台和读取方式。
- B. Triage Labels：默认五项标准角色，可自定义。
- C. Domain Docs：默认根 `CONTEXT.md`、`docs/prd/`、`docs/adr/`、`docs/research/`；多仓时写 `repo-map.md`。
- D. Documentation Language：默认跟随用户当前语言。
- E. Project Engineering Principles：只写项目实际需要的范围、文件大小、依赖检查路径和快速命令；不复制通用原则全文。
- F. Coding Standards：默认 `ruoyi6`；非 RuoYi 项目记录 `none` 或替代 profile 及理由。把 profile 的硬约束摘到项目配置，避免未加载 profile 时完全看不见。
- G. Project Handoff / Compile & Run Commands：写实际后端、前端编译命令、启动命令、工作目录和监听端口。启动命令只登记、不在初始化时启动服务；从构建文件、脚本和已有运行说明读取，无法确认时标为待确认，不猜端口。默认只编译受影响一侧，跳过测试、lint 和独立类型检查。
- H. Project AGENTS.md / CLAUDE.md：默认跳过；仅在文件已存在或用户明确要求时更新短指针。

**Step 5 — Confirm.** 写出前展示完整文件草案；更新时只展示变化文件。不要用占位符生成真实项目配置。

**Step 6 — Write.** 先写 `docs/agents/`，最后按需更新 `AGENTS.md`/`CLAUDE.md`。`project-state.md` 使用实际目标、阶段、编译命令、启动命令和端口；没有活动批次时把未开始阶段写 `N/A`，不要留模板文字。`project-decisions.md`、`verification.md` 没有内容时写“暂无记录”，不要留空模板。写 `domain.md` 前扫描真实 PRD/ADR/research 文件名。

**Step 7 — Done.** 列出已配置文件和下一步。建议从 `/think` 或 `/research` 开始；`implement` 只在明确调用时进入。

## 重跑与一致性

- 重跑时先读现有配置，比较实际结构，不重写未变化文件。
- 发现 PRD/ADR/research 命名、语言或格式漂移时先报告，确认后再改；不自动翻译或批量重命名。
- 重跑结束必须报告过期引用检查结果：每个文件、命中的旧技能/profile 名或 Vue 长期规范，以及“已修复 / 待用户确认 / 无需变更”。不能把引用检查藏在探索步骤里而不出现在交付结果中。
- 项目配置变化后，提示重新运行受影响的阶段；不自动启动实现或页面验收。

## Gotchas

| 现象 | 规则 |
|---|---|
| 没看 remote 就假设 GitHub | Step 1 先运行 `git remote -v` |
| 单仓/多仓判断错误 | Step 2 检查 workspace、子项目和同级仓库 |
| 创建了不需要的 AGENTS.md | 默认跳过；只写项目事实或短指针 |
| 把全局工作流复制进项目文件 | 全局指令是唯一来源；项目只写事实 |
| 技术 profile 靠探测框架签名决定 | 默认 `ruoyi6`；非 RuoYi 由用户明确说明后记录 `none` 或替代 profile |
| 编译或启动命令是猜的 | 从 `pom.xml`、`package.json`、CI、脚本和已有运行说明读取；端口从配置读取 |
| 多仓没有主跟踪仓库 | 写 `repo-map.md`，明确哪个仓库拥有主 Issue/PRD |
| 生成文件留模板占位符 | 用实际事实或“暂无记录”，不把模板当配置 |
| 重跑覆盖手写内容 | 先读、展示 diff、只改确认部分 |
| 旧技能名或 Vue 长期规范仍留在 `AGENTS.md` / `docs/agents/` | Step 1 扫描过期引用，展示差异；确认后改成当前技能名、React profile 和 `docs/agents/` 指针 |

## Output

**首次运行：**

```text
Setup complete.

Configuration:
- Project structure: <single / monorepo / multi-repo>
- Issue tracker: <local / GitHub / GitLab / Gitee / other>
- Coding standards: <ruoyi6 / none / other>
- Triage labels: <defaults / customised>
- Domain docs: <single-context / multi-context>
- Documentation language: <Chinese / English / other>

Updated files:
- docs/agents/domain.md
- docs/agents/coding-standards.md
- docs/agents/project-state.md
- docs/agents/project-decisions.md
- docs/agents/verification.md
- docs/agents/language.md
- docs/agents/issue-tracker.md (if configured)
- docs/agents/triage-labels.md (if configured)
- docs/agents/repo-map.md (multi-repo only)
- AGENTS.md / CLAUDE.md (only when already existed or explicitly requested)

Stage complete; stop here.

Next (user-initiated): `/think` for a new feature, `/research` for a technical question, or `/implement` only when slices are already approved.
```

**重跑：** 只列变化文件、漂移检查结果、过期引用检查结果和下一步。过期引用逐项写清文件、命中项和处理状态（已修复 / 待用户确认 / 无需变更）。`implement`、`page-acceptance` 不因初始化完成而自动开始。
