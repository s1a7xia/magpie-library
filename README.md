# Magpie + Codex 工程协作基线（任意项目）

这是一套面向任意项目的轻量工程基线：Magpie 统一维护全局规则、技能和 MCP，Codex 负责从需求到交付验收的开发闭环。RuoYi-Vue-Plus 6.x + React 是条件加载的技术层，不是所有项目的前置假设。

```text
日常：直接提需求 → Codex 实现 → 核对差异 → 按项目规则交付
闭环：目标与验收项 → 实现 → 授权范围内验证/修复 → 审查 → 验收/Git 收尾
```

**第一次使用先看 [机制与日常用法](USAGE.md)**；要理解各层如何连接，读 [当前设计](DESIGN.md)。不强制 PRD、交接文件、固定流水线或多个 Agent 并行；阶段技能仅在对应任务需要时加载。

本仓库公开用于阅读、参考和溯源。**日常生效的源头不是本仓库**，而是本机 Magpie 资源库 `~/.config/magpie/library/`；本仓库是它的可读、可 diff、可回滚副本。

> 换电脑时，先用 Magpie 的同步备份恢复资源库、凭据和运行配置，再考虑克隆本仓库。完整依赖与恢复步骤见 [DEPENDENCIES.md](DEPENDENCIES.md)。

## 当前范围

- Magpie 是全局指令、技能和 MCP 的唯一配置源。
- Codex 是唯一默认开发者，负责需求澄清、设计、实现、受影响文档和按授权的 Git 收尾。
- Alma 作为独立应用自行使用，不属于这套开发团队；Magpie 不再向 Alma 分发指令、技能或 MCP。
- 项目事实留在项目仓库；全局规则不复制业务细节，项目 `AGENTS.md` 不复制全局流程。
- 大型、跨会话或多阶段项目复用一份当前状态记录；`setup-matt-pocock-skills` 只负责初始化，执行任务的 Codex 负责在状态变化时维护。

## 这套东西由什么组成

| 层 | 作用 | 当前载体 |
|---|---|---|
| 全局规则 | 项目无关的工作原则、授权、验证与交付边界 | 唯一源 `instructions.md`，由 Magpie 分发给 Codex |
| 技能 | 工程阶段方法、业务规范和可选支撑能力 | `skills/` 下的 13 个 Magpie 技能；核心规范直接暴露，其余走 `magpie-skills` 路由 |
| 项目事实 | 当前目标、决策、验证证据、构建/启动命令与端口 | 项目现有文档；缺少专用目录不阻塞开发 |
| 工具 | 搜索、文档、代码托管、数据库、SSH、图片和浏览器操作 | Magpie 托管的 10 项 MCP，加上本机 CLI |

各层各司其职：

- 规则只写边界和路由，不承载长篇流程。
- 技能只负责本阶段怎么做，不复制全局规则。
- MCP 和 CLI 是执行能力，不代表已经连接、已经授权或已经验证。

文档记录必须区分 Agent 实测、用户确认和未验证项。原始聊天历史不是项目事实，凭证、完整认证头和私密数据不进入文档、提交或截图。

## 工程入口

通用工程阶段使用 Matt Pocock 的技能组合，不设单一路由技能：

```text
（新项目时）setup-matt-pocock-skills → 需求/计划梳理 → grill-with-docs → to-spec → to-tickets → Codex 实现 → 按需验收/审查
```

项目开发从原始需求和当前仓库开始：先盘点 RuoYi/相邻模块可复用能力，并将功能切片标为复用、配置/扩展或新开发；再讨论最小可交付主干的页面/菜单/路由、API、字典/参数、权限、数据及验收。涉及持久化对象、字段语义、身份/归属、状态、唯一性、删除/历史、关系或 JSONB 时，在需求拷打阶段加载 `database-design` 并先确认数据契约。

需求/方案未收敛时按需加载 `grill-with-docs`；定稿且需要持久记录时用 `to-spec`；只有多项任务存在依赖或切片价值时才用 `to-tickets`。简单单次改动跳过完整规格和拆票。`setup-matt-pocock-skills` 仅在项目初始化时调用，`code-review` 仅在用户明确要求审查时调用；`grilling` 和 `domain-modeling` 是 `grill-with-docs` 的依赖。调用 `code-review` 即授权两个只读审查子代理。

业务规范按场景叠加：

- `database-design`：需求/方案阶段讨论持久化对象、字段语义、身份/归属、关系、唯一性、生命周期、删除/历史、JSONB 时先加载；后续结构性变更继续使用。
- `ruoyi6`：实际修改 RuoYi-Vue-Plus 6.x + plus-ui-React 的代码、接口、权限、菜单、字段链路或已批准的数据落表。
- `frontend-design`：用户明确要求深度视觉设计或整页改版。
- `api-regression`：用户明确要求 API 回归、多账号权限或数据库终态验证。

## 环境清单

当前 MCP、插件、结构化记忆和备份边界见 [ENVIRONMENT.md](ENVIRONMENT.md)，可机器读取的脱敏清单见 [environment.snapshot.json](config/environment.snapshot.json)。公开清单不包含密钥或私人记忆正文。

## 依赖摘要

- Magpie `0.1.4395`
- Codex `0.169.0`
- Node.js `v24.17.0`、npm `11.13.0`
- Python `3.13.14`
- Git `2.54.0`
- `gh 2.103.2`、`glab 1.128.0`（按托管平台选用）
- `rtk 1.1.0`
- Chrome 和 Edge

MCP 由 Magpie 统一托管，当前登记 10 项：`chrome-devtools`、`context7`、`dbhub`、`gitee`、`github`、`magpie-image`、`magpie-memory`、`magpie-vision`、`magpie-web-search`、`ssh`。页面运行检查使用 Codex 宿主浏览器工具，不属于 Magpie 资源库 MCP。`library.json` 当前只把这些能力分发给 Codex。

版本、凭据位置、换机恢复、校验和故障处理见 [DEPENDENCIES.md](DEPENDENCIES.md)。

## 目录

| 路径 | 说明 |
|---|---|
| `instructions.md` | 全局工程指令的唯一正文源；项目规则不写回这里 |
| `skills/` | Magpie 技能及其引用、模板和脚本 |
| `scripts/verify-library.py` | 资源库结构、链接、同步和凭证提示检查 |
| `scripts/export_public_snapshot.py` | 从当前 `library.json` 生成不含凭据的公开环境快照 |
| `skills/setup-matt-pocock-skills/templates/project-state-document.md` | 大型项目的单一当前状态记录模板；已有状态文档或任务板时直接复用 |
| `memory/` | 公开镜像：当前 active 的结构化偏好，不含凭据、历史或运行状态 |
| `README.md` | 组合介绍与入口 |
| `USAGE.md` | 当前机制、调用示例、权限边界与更新方法 |
| `DESIGN.md` | 当前分层设计、分发与 MCP 拓扑 |
| `DEPENDENCIES.md` | 运行依赖、MCP、恢复与校验 |
| `ENVIRONMENT.md` | 本机插件、记忆与同步的脱敏清单 |

## 公开镜像边界

公开仓库镜像当前生效的全局指令、技能、说明、脱敏环境快照和 active 记忆，供阅读、差异比较与换机参考。`memory/` 只收录用户明确同意公开的 3 条 active 偏好正文；凭据、登录态、会话历史、模型供应商私密配置、MCP 认证头、DSN、SSH 信息、同步密码和记忆运行元数据不公开。它不是可直接覆盖本机运行目录的备份；换机时先用 Magpie 的加密备份恢复运行环境，再用本仓库核对公开配置与技能。

## 维护和发布

技能与全局指令的编辑源是 Magpie 资源库，不是生成到 Codex 的副本，也不是本仓库。

正确顺序：

1. 修改 `~/.config/magpie/library/` 中的源文件；全局规则只改 `instructions.md`；
2. 运行：

   ```powershell
   magpie library sync
   python "$env:USERPROFILE\.config\magpie\library\scripts\verify-library.py"
   ```

3. 确认 `~/.codex/skills` 与源一致，Codex 的 Magpie 块来自同一正文；
4. 把同一组改动同步到本仓库；发布副本的 `memory/` 只镜像当前 active 的全局偏好，运行元数据不公开；
5. 只提交本次文档或技能变更，核对 diff 后推送；
6. 核验本地 `HEAD`、`origin/main` 和远端引用一致。

直接在本仓库改技能不会生效：下一次 `magpie library sync` 会以本机资源库为准覆盖差异。

## 项目状态文档

`setup-matt-pocock-skills` 为大型、跨会话或多阶段项目初始化文档与任务入口。它在这类项目中建立 `docs/project-state.md`，已有状态记录或任务板则直接复用；小任务不创建。状态记录回答当前目标、下一步、当前迭代剩余工作、已知项目剩余、风险阻塞和验收证据，不复制完整 PRD、diff 或任务清单。

Git 是代码事实源，状态文档是任务事实源。开始工作前核对当前分支、工作区差异和相关提交；切片完成、范围变化、阻塞或验收决策变化时只更新变化的事实。纯问答和只读审查不修改文档。小任务不创建状态文档，缺少状态文档也不触发初始化。

状态文档默认放在 `docs/project-state.md`；项目已有状态文档或任务板时直接复用，非默认路径写进项目现有 `AGENTS.md`。`setup-matt-pocock-skills` 负责建立记录，日常维护由当前执行任务的 Codex 执行，不是后台自动同步服务。提交获准时，状态更新与相关代码在同一授权范围内收尾。

## 已知边界

- 本仓库只保存可阅读的规则和技能，不保存 API 密钥、登录态、同步密码或机器专属配置。
- “已登记 MCP”不等于“当前会话已连通”；需要实际调用一次才算验证。
- `dbhub` 依赖本机 PostgreSQL 和正确的 DSN，换机后目标可能变化。
- 显式页面运行检查使用 Codex 宿主浏览器技术；浏览器已连接不等于页面已验收。
- 全局指令由 `instructions.md` 统一维护并分发给 Codex，写入 `~/.codex/AGENTS.md`。
- Alma 的指令、技能、MCP、聊天和记忆由 Alma 自己维护，不属于 Magpie 资源库。
- 默认不安装工程 Hook 和子代理；Hook 只作为可选护栏，主代理负责判断、执行和交付。

## 永不入库

- API 密钥、令牌、认证头；
- 数据库连接串和密码；
- 浏览器登录态与订阅凭据；
- 私人聊天记录、未公开的记忆正文和机器专属状态。
