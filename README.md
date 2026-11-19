# Magpie + Codex 工程协作基线（任意项目）

这是一套面向任意项目的轻量工程基线：Magpie 统一维护全局规则、技能和 MCP，Codex 负责从需求到交付验收的开发闭环。RuoYi-Vue-Plus 6.x + React 是条件加载的技术层，不是所有项目的前置假设。

```text
日常：直接提需求 → Codex 实现 → 核对差异 → 按项目规则交付
闭环：目标与验收项 → 按需收敛决策 → 实现 → 授权范围内验证/修复 → 审查 → 验收/Git 收尾
```

**第一次使用先看 [机制与日常用法](USAGE.md)**；要理解各层如何连接，读 [当前设计](DESIGN.md)。不强制 PRD、交接文件、固定流水线或多个 Agent 并行；阶段技能仅在对应任务需要时选用。

本仓库公开用于阅读、参考和溯源。**日常生效的源头不是本仓库**，而是本机 Magpie 资源库 `~/.config/magpie/library/`；本仓库是它的可读、可 diff、可回滚副本。

> 换电脑时，先用 Magpie 的同步备份恢复资源库、凭据和运行配置，再考虑克隆本仓库。完整依赖与恢复步骤见 [DEPENDENCIES.md](DEPENDENCIES.md)。

## 快速使用

```powershell
git clone git@github.com:s1a7xia/magpie-library.git
```

第一次阅读按以下顺序：

1. 本文的“当前范围”“工程入口”和“目录”，先理解各层职责；
2. [USAGE.md](USAGE.md) 看日常只说什么、Codex 如何选择技能、哪些动作需要授权；
3. [SKILLS-DECISION.md](SKILLS-DECISION.md) 看当前 20 个技能、3 条隐式触发及排除项；
4. [ENVIRONMENT.md](ENVIRONMENT.md) 和 [DEPENDENCIES.md](DEPENDENCIES.md) 看 MCP、插件、记忆与换机恢复边界。

只克隆仓库不会安装技能、连接 MCP 或恢复对话记忆。需要运行这套环境时，先安装 Magpie 并从其加密备份恢复，再把本仓库只读用于核对公开差异。

## 当前范围

- Magpie 是全局指令、技能和 MCP 的唯一配置源。
- Codex 是唯一默认开发者，负责需求澄清、设计、实现、受影响文档和按授权的 Git 收尾。
- Alma 作为独立应用自行使用，不属于这套开发团队；Magpie 不再向 Alma 分发指令、技能或 MCP。
- 项目事实留在项目仓库；全局规则不复制业务细节，项目 `AGENTS.md` 不复制全局流程。
- 大型、跨会话或多阶段项目复用一份当前状态记录；项目需要时用 `setup-matt-pocock-skills` 先确认 tracker 和领域文档布局，再由当前任务在 `docs/project-state.md` 建立状态记录。执行任务的 Codex 负责维护，小任务不强制初始化。

## 这套东西由什么组成

| 层 | 作用 | 当前载体 |
|---|---|---|
| 全局规则 | 项目无关的工作原则、授权、验证与交付边界 | 唯一源 `instructions.md` + Codex 补充 `instructions/codex.md`，由 Magpie 合并分发 |
| 技能 | 工程阶段方法、业务规范和可选支撑能力 | 20 个技能由 Magpie 分发；13 个直接暴露，7 个技能经 `magpie-skills` 聚合 |
| 项目事实 | 当前目标、决策、验证证据、构建/启动命令与端口 | 项目现有文档；缺少专用目录不阻塞开发 |
| 工具 | 搜索、文档、代码托管、数据库、SSH、图片；页面检查使用 Codex 宿主能力 | Magpie 托管的 9 项 MCP，加上本机 CLI |

各层各司其职：

- 规则只写边界和路由，不承载长篇流程。
- 技能只负责本阶段怎么做，不复制全局规则。
- MCP 和 CLI 是执行能力，不代表已经连接、已经授权或已经验证。

文档记录必须区分 Agent 实测、用户确认和未验证项。原始聊天历史不是项目事实，凭证、完整认证头和私密数据不进入文档、提交或截图。

## 工程入口

本项目以 Magpie 作为唯一技能入口。`~/.codex/skills` 直接暴露 13 个高频技能，另有 `magpie-skills` 聚合入口收纳 `answer-me-with-html`、`diagnosing-bugs`、`handoff`、`retro`、`setup-matt-pocock-skills`、`triage`、`writing-for-agents` 7 个低频或一次性配置技能；没有插件副本。Codex 每轮看到的是直接技能名称、description 和聚合入口摘要，再由当前模型按条件选择并读取对应 `SKILL.md`，不是路径匹配式的确定性自动执行。直接技能中只保留 3 条隐式触发路径：RuoYi 规格预检或代码工作读取 `ruoyi6`、持久化模型讨论读取 `database-design`、单会话真实歧义读取 `grill-with-docs`；其余 10 个直接技能默认只在用户点名时启用，已启用技能按其 `SKILL.md` 明确读取依赖技能文件时除外。7 个聚合技能不单独暴露，由 `magpie-skills` 按描述选择，或由用户明确要求经该入口使用。

```text
新项目 / 重大新模块
  -> 产品发现（Default；Plan 可选）
  -> 事实基线

已有项目明确任务
  -> 事实基线（读规则、代码、Git、状态和授权）

需求收敛
  ├─ 目标、验收和修改点清楚 -> 直接实现
  ├─ 单会话真实歧义 -> grill-with-docs
  └─ 大型、跨会话、关键未知互相阻塞
       -> 建议 $wayfinder（用户确认后建决策地图）
          ├─ research：外部事实
          ├─ prototype：UI / 行为效果
          ├─ grilling + domain-modeling：业务决策 / 术语
          └─ 路径仍不清：建议 $ask-matt（用户确认后导航）

涉及持久化对象 / 字段 / 关系 / 状态 / 唯一性 / 删除 / 迁移
  -> database-design：进入 $to-spec 前确认数据契约

RuoYi 规格前需要核对框架落点、复用边界或首个可交付主干
  -> ruoyi6：只读预检，不重做需求或产品规划

规格与切片
  -> 大型/多阶段项目首次 spec/ticket 流程：经 magpie-skills 读取 setup-matt-pocock-skills（用户确认后配置）
  -> $to-spec：需要可验收规格、交接或复杂变更
  -> 多个纵向切片或真实依赖：建议 $to-tickets（用户确认后拆）
  -> 小改或单一明确切片：跳过规格和拆票

实现 -> 授权内验证
  -> 默认当前会话直接实现；RuoYiPlus 代码改动继续按 ruoyi6 落地
  -> $code-review 仅在明确要求时
  -> 预发布、UAT、生产发布、客户验收是审批门
```

项目开发从原始需求和当前仓库开始：先盘点 RuoYi/相邻模块可复用能力，并把功能切片标为复用、配置/扩展或新开发；再明确最小可交付主干的页面/菜单/路由、API、字典/参数、权限、数据和验收。涉及持久化对象、字段语义、身份/归属、状态、唯一性、删除/历史、关系或 JSONB 时，在任何阶段都先过 `database-design`。

`wayfinder` 默认把地图写在项目内 `.scratch/<effort>/wayfinder.md`，决策票据放在同目录的 `tickets/`；只有大型、跨会话且关键未知互相阻塞时才建议建立。`to-spec` 写 `.scratch/<feature-slug>/spec.md`，`to-tickets` 写 `.scratch/<feature-slug>/issues/`；未配置外部 tracker 时都使用项目内本地 Markdown。实现始终由当前会话直接完成，不另设实现技能。子代理、提交、push 和外部 Issue 仍按当前任务授权。

13 个直接技能统一用短名调用，例如 `$wayfinder`、`$to-tickets`、`$ruoyi6`、`$database-design`、`$frontend-design`；7 个聚合技能通过 `$magpie-skills` 或直接说明“使用 answer-me-with-html/diagnosing-bugs/triage/retro/handoff/setup-matt-pocock-skills/writing-for-agents”进入。不需要也不应再写命名空间或插件前缀。

业务规范按场景叠加：

- `database-design`：需求/方案阶段讨论持久化对象、字段语义、身份/归属、关系、唯一性、生命周期、删除/历史、JSONB 时先加载；后续结构性变更继续使用。
- `ruoyi6`：规格前需核对 RuoYi 框架落点、复用边界或首个可交付主干时做只读预检；实际修改 RuoYi-Vue-Plus 6.x + plus-ui-React 的代码、接口、权限、菜单、字段链路或已批准的数据落表时必须使用。
- `frontend-design`：用户明确要求深度视觉设计或整页改版。

20 个技能全部在 Magpie 资源库 `skills/` 中维护。13 个高频技能通过 Junction 直接出现在 `~/.codex/skills`；`answer-me-with-html`、`diagnosing-bugs`、`handoff`、`retro`、`setup-matt-pocock-skills`、`triage`、`writing-for-agents` 通过 `magpie-skills` 聚合入口按描述读取，不安装同名插件副本。`ruoyi6`、`database-design` 和 `grill-with-docs` 由全局指令优先触发；其余 10 个直接技能默认只在用户点名时启用，已启用技能按其流程读取依赖文件时除外。

## 环境清单

当前 MCP、插件、结构化记忆和备份边界见 [ENVIRONMENT.md](ENVIRONMENT.md)，可机器读取的脱敏清单见 [environment.snapshot.json](config/environment.snapshot.json)。`memory/` 只镜像 3 条不含凭据和业务机密、已由用户确认可公开的工程偏好正文；Magpie 的实际运行记忆、召回索引、使用状态和机器路径不进入公开仓库。

## 依赖摘要

- Magpie `0.1.4395`
- Codex `0.169.0`
- Node.js `v24.17.0`、npm `11.13.0`
- Python `3.13.14`
- Git `2.54.0.windows.1`
- `gh 2.103.2`、`glab 1.128.0`（按托管平台选用）
- `rtk 1.2.0`
- Chrome 和 Edge

MCP 由 Magpie 统一托管，当前登记 9 项：`context7`、`dbx`、`gitee`、`github`、`magpie-image`、`magpie-memory`、`magpie-vision`、`magpie-web-search`、`ssh`。其中 `context7` 只勾选给 Codex，另外 8 项仍保留 Alma 的残留勾选，但 Alma 运行时未连接这些 MCP，当前实际使用方是 Codex。页面运行检查使用 Codex 宿主浏览器工具，不属于 Magpie 资源库 MCP。

版本、凭据位置、换机恢复、校验和故障处理见 [DEPENDENCIES.md](DEPENDENCIES.md)。

## 目录

| 路径 | 说明 |
|---|---|
| `instructions.md` | 全局工程指令的公共正文源；项目规则不写回这里 |
| `instructions/codex.md` | Codex 专属补充规则；与公共正文合并后写入 Codex |
| `skills/` | Magpie 技能及其引用、模板和脚本 |
| `memory/` | 3 条已确认可公开的 Codex 工程偏好正文；不是 Magpie 运行记忆目录 |
| `scripts/verify-library.py` | 资源库结构、链接、同步和凭证提示检查 |
| `scripts/export_public_snapshot.py` | 从当前 `library.json` 和公开记忆生成不含凭据的环境快照 |
| `scripts/export_public_memory.py` | 从运行记忆生成不含路径、索引和运行状态的公开正文镜像 |
| `scripts/scan-staged-secrets.py` | 扫描暂存区中的凭据、DSN 和认证头 |
| `README.md` | 组合介绍与入口 |
| `SKILLS-DECISION.md` | 当前技能选型、纳入/排除理由与需求到交付闭环 |
| `USAGE.md` | 当前机制、调用示例、权限边界与更新方法 |
| `DESIGN.md` | 当前分层设计、分发与 MCP 拓扑 |
| `DEPENDENCIES.md` | 运行依赖、MCP、恢复与校验 |
| `ENVIRONMENT.md` | 本机技能、MCP、记忆与同步的脱敏清单 |
| `THIRD-PARTY.md` | Matt Pocock 技能的上游来源与 MIT 许可说明 |

## 公开镜像边界

公开仓库镜像当前生效的全局指令、20 个 Magpie 技能、3 条公开工程偏好、说明和脱敏环境快照，供阅读、差异比较与换机参考。凭据、登录态、会话历史、模型供应商私密配置、MCP 认证头、DSN、SSH 信息、记忆索引/运行状态和同步密码不公开。它不是可直接覆盖本机运行目录的备份；换机时先用 Magpie 的加密备份恢复运行环境，再用本仓库核对公开配置与技能。

## 维护和发布

技能与全局指令的编辑源是 Magpie 资源库，不是生成到 Codex 的副本，也不是本仓库。

正确顺序：

1. 修改 `~/.config/magpie/library/` 中的源文件；公共规则改 `instructions.md`，Codex 专属规则改 `instructions/codex.md`；
2. 运行：

   ```powershell
   magpie library sync
   python "$env:USERPROFILE\.config\magpie\library\scripts\verify-library.py"
   ```

3. 确认 `~/.codex/skills` 与源一致，Codex 的 Magpie 块来自同一正文；
4. 把同一组改动同步到本仓库；
5. 重新生成 `config/environment.snapshot.json` 和公开记忆镜像，只提交本次文档或技能变更，运行敏感信息扫描并核对 diff 后推送；
6. 核验本地 `HEAD`、`origin/main` 和远端引用一致。

直接在本仓库改技能不会生效：下一次 `magpie library sync` 会以本机资源库为准覆盖差异。

## 项目状态文档

`setup-matt-pocock-skills` 先为大型、跨会话或多阶段项目确认 issue tracker、triage labels 和领域文档布局，写入项目 `AGENTS.md`、`docs/agents/issue-tracker.md` 和 `docs/agents/domain.md`；安装了 `triage` 时还会写入 `docs/agents/triage-labels.md`。它不创建 `docs/project-state.md`。状态记录由当前任务在这个配置基础上按需建立，已有状态文档或任务板则直接复用；小任务不创建。状态记录回答当前目标、下一步、当前迭代剩余工作、已知项目剩余、风险阻塞和验收证据，不复制完整 PRD、diff 或任务清单。

Git 是代码事实源，状态文档是任务事实源。开始工作前核对当前分支、工作区差异和相关提交；切片完成、范围变化、阻塞或验收决策变化时只更新变化的事实。纯问答和只读审查不修改文档。小任务不创建状态文档，缺少状态文档也不触发初始化。

状态文档默认放在 `docs/project-state.md`；项目已有状态文档或任务板时直接复用，非默认路径写进项目现有 `AGENTS.md`。`setup-matt-pocock-skills` 只建立 tracker 与领域文档约定，状态记录由当前任务按需创建和维护，不是后台自动同步服务。提交获准时，状态更新与相关代码在同一授权范围内收尾。

## 已知边界

- 本仓库只保存可阅读的规则和技能，不保存 API 密钥、登录态、同步密码或机器专属配置。
- “已登记 MCP”不等于“当前会话已连通”；需要实际调用一次才算验证。
- `dbx` 的数据库目标和连接参数由当前会话配置决定，换机后需要重新核对。
- 显式页面运行检查使用 Codex 宿主浏览器技术；浏览器已连接不等于页面已验收。
- 全局指令由 `instructions.md` 加 `instructions/codex.md` 合并维护并分发给 Codex，写入 `~/.codex/AGENTS.md`。
- Alma 的指令、技能、MCP、聊天和记忆由 Alma 自己维护，不属于 Magpie 资源库。
- 默认不安装工程 Hook 和子代理；Hook 只作为可选护栏，主代理负责判断、执行和交付。

## 永不入库

- API 密钥、令牌、认证头；
- 数据库连接串和密码；
- 浏览器登录态与订阅凭据；
- 私人聊天记录、未经确认可公开的记忆正文、记忆索引和机器专属状态。
