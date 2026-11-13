# Magpie 工程协作基线（任意项目）

这是一套面向任意项目的轻量 AI 工程协作基线：把全局规则、工程技能、项目文档和工具连接统一放进 Magpie 资源库，再由 Magpie 分发给 Codex 和 Alma。RuoYi-Vue-Plus 6.x + React 是条件加载的技术层，不是所有项目的前置假设。版本和源码事实以项目实际的构建文件与当前 checkout 为准。

它解决的不是“让 AI 多写一点代码”，而是让每次开发都遵循同一条可追溯的路径：

```text
日常：直接提需求 → Codex 实现 → 核对差异 → 按项目规则交付
闭环：目标与验收项 → 实现 → 验证/修复 → 风险审查 → 验收/Git 收尾
辅助：需要远程查看、通知、审批或持久任务协调 → 启动 Alma
```

**第一次使用先看 [机制与日常用法](USAGE.md)**。不强制 PRD、交接文件、固定流水线或多个 Agent 并行；阶段技能仅在对应任务需要时加载。

本仓库公开用于阅读、参考和溯源。**日常生效的源头不是本仓库**，而是本机 Magpie 资源库 `~/.config/magpie/library/`；本仓库是它的可读、可 diff、可回滚副本。

> 换电脑时，先用 Magpie 的同步备份恢复资源库、凭据和运行配置，再考虑克隆本仓库。完整依赖与恢复步骤见 [DEPENDENCIES.md](DEPENDENCIES.md)。

## 这一版改了什么

- 把日常开发收敛为 Direct / Closure / Debug 三条路径；`think`、`grill`、`story`、`implement`、`review` 保留为按需方法，不再要求每次逐阶段调用。
- 用户说“按闭环做”或“从需求到验收”时，Codex 连续完成目标与验收项、实现、授权范围内验证/修复、风险审查和收尾；新增表、扩大权限、不可逆写库、提交部署仍按原有授权。
- 保留 3 个技术与设计技能：`ruoyi6`、`database-design`、`frontend-design`。
- 保留 3 个支撑技能：`research`、`rules`、`answer-me-with-html`。
- 删除 4 个重复层：`engineering-workflow`、`project-context`、`prompt-engineering`、`scm-collaboration`。它们的工作分别回到项目工作流配置、`setup-project`、任务契约和平台 MCP/CLI。
- 把 RuoYi 技术层从 `ruoyi-plus-dev` 收敛为 `ruoyi6`，只保留 6.x + React 需要的后端、前端、数据库和工具规范。
- `ruoyi6` 先按 Direct / Increment / New Module 分级，再通过能力地图复用框架已有实现；新模块才做完整业务判型、框架能力扫描和业务契约门。任何 RuoYi 代码或字段/API/权限契约改动都加载它，覆盖 Direct、`implement`、`debug` 和 `review`；纯文档、只读规划或诊断且不改代码时可不加载。代码骨架只保留在 `templates.md` 与 `frontend-templates.md`，现有业务模块只用于了解集成约束，不作为模板。前端只使用 `plus-ui-React` 的 React 实现。
- 不再照搬参考站的 40/83 个技能。参考站提供的是**文档地图和工程思路**，不是直接复制清单。

`dev-skills` 插件当前是 **1 个自动入口 + 9 个内部阶段**，不是一条每次都要走完的流水线；会话只加载当前任务真正需要的技能。`dev-workflow` 是唯一开发路由；`team-orchestration` 只负责明确授权的额外协作与 Alma 使用。

日常直接向 Codex 提需求；需要更细的方法控制时，再按需使用
`think` / `grill` / `story` / `review`。Direct 和 Closure 不强套
正式批次状态；状态、证据复用与缺陷回流以
当前 `dev-workflow` 入口和 Codex 全局规则为准。

## 这套东西由什么组成

| 层 | 作用 | 当前载体 |
|---|---|---|
| 全局规则 | 项目无关的角色、协作闭环、授权与改动保护 | 唯一源 `instructions.md`，由 Magpie 分发给 Codex、Alma |
| 技能 | 把不同阶段的方法、检查门槛和输出约定固化 | `skills/` 下的 Magpie 技能 |
| 项目事实 | 当前目标、决策、验证证据、编译/启动命令与端口 | 项目现有文档；缺少专用目录不阻塞开发，需要初始化时再使用 `setup-project` |
| 工具 | 搜索、文档、代码托管、数据库、SSH、图片和浏览器操作 | Magpie 托管的 MCP，加上本机 CLI |
| 运行观察 | 已连接会话、通知、审批和持久任务协调 | Alma，按需启动，不默认写代码 |

各层各司其职：

- 规则不承载长篇流程，只负责边界和路由。
- 技能不重复复制全局规则，只负责本阶段怎么做。
- MCP 和 CLI 是执行能力，不代表已经连接、已经授权或已经验证。
文档记录必须区分 Agent 实测、用户确认和未验证项。原始聊天历史不是项目事实，凭证、完整认证头和私密数据不进入文档、提交或截图。

## 环境清单

当前 MCP、社区/内置插件、结构化记忆、deja 历史召回和备份边界见 [ENVIRONMENT.md](ENVIRONMENT.md)，可机器读取的脱敏清单见 [environment.snapshot.json](config/environment.snapshot.json)。公开清单不包含密钥或私人记忆正文。

## 依赖摘要

当前基线使用：

- Magpie `0.1.3887`
- Codex `0.167.2`、Alma `0.4.575`
- Node.js `v24.17.0`、npm `11.13.0`
- Python `3.13.14`
- Git `2.54.0`
- `gh 2.103.2`、`glab 1.128.0`（按托管平台选用）
- `rtk 1.1.0`
- Chrome 和 Edge

MCP 由 Magpie 统一托管，当前登记 9 项：`context7`、`dbhub`、`gitee`、`github`、`magpie-image`、`magpie-memory`、`magpie-vision`、`magpie-web-search`、`ssh`。页面运行检查使用 Codex 宿主浏览器工具，不属于 Magpie 资源库 MCP；Alma 通过自己的 MCP 配置连接 Magpie Hub，不占用资源库里的独立条目。

版本、Agent 分发矩阵、凭据位置、换机恢复、校验和故障处理见 [DEPENDENCIES.md](DEPENDENCIES.md)。

## 目录

| 路径 | 说明 |
|---|---|
| `instructions.md` | 全局协作指令的唯一正文源；项目规则不写回这里 |
| `instructions/<agent>.md` | 可选的 Agent 专属追加内容；目前 Codex 的旧重复正文已清空 |
| `skills/` | Magpie 技能及其引用、模板和脚本 |
| `scripts/verify-library.py` | 资源库结构、链接、同步和凭证提示检查 |
| `README.md` | 组合介绍与入口 |
| `USAGE.md` | 当前机制、调用示例、权限边界与更新方法 |
| `DEPENDENCIES.md` | 运行依赖、MCP、恢复与校验 |

## 维护和发布

技能与全局指令的编辑源是 Magpie 资源库，不是生成到各 Agent 的副本，也不是本仓库。

正确顺序：

1. 修改 `~/.config/magpie/library/` 中的源文件；全局规则只改 `instructions.md`；
2. 运行：

   ```powershell
   magpie library sync
   python "$env:USERPROFILE\.config\magpie\library\scripts\verify-library.py"
   ```

3. 确认 `~/.agents/skills` 与源一致，Codex/Alma 的 Magpie 块都来自同一正文；
4. 把同一组改动同步到本仓库；
5. 只提交本次文档或技能变更，核对 diff 后推送；
6. 核验本地 `HEAD`、`origin/main` 和远端引用一致。

直接在本仓库改技能不会生效：下一次 `magpie library sync` 会以本机资源库为准覆盖差异。

## 已知边界

- 本仓库只保存可阅读的规则和技能，不保存 API 密钥、登录态、同步密码或机器专属配置。
- “已登记 MCP”不等于“当前会话已连通”；需要实际调用一次才算验证。
- `dbhub` 依赖本机 PostgreSQL 和正确的 DSN，换机后目标可能变化。
- 页面验收使用 Magpie Browser MCP 和本机 Chrome 扩展；扩展已连接不等于其他机器已恢复。换机时需重新加载扩展并确认 `/v1/magpie/browser` 返回 `connected: true`。
- 全局指令由 `instructions.md` 统一维护并分发给 `codex`、`alma`：
  Codex 写入 `~/.codex/AGENTS.md`，Alma 写入 `~/.config/alma/USER.md`。这些是生成物，不手工维护第二套规则。
- 项目仍可有自己的 `AGENTS.md`，但只写该项目的技术栈、命令、端口和授权边界，不复制全局团队规则。团队 Skill 只有一个 Magpie 源，`~/.agents/skills` 与 Alma personal 目录通过 Junction 指向它。
- 默认不安装工程 Hook 和子代理；Hook 只作为可选护栏，主代理负责判断、执行和交付。
- Alma 不随登录自动启动；需要时直接运行 `& "$env:LOCALAPPDATA\Programs\Alma\Alma.exe"`，再用 `alma status` 核对运行状态。

## 永不入库

- API 密钥、令牌、认证头；
- 数据库连接串和密码；
- 浏览器登录态与订阅凭据；
