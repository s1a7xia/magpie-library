# 当前设计：Magpie + Codex

更新日期：2026-11-19。本文描述**当前实际生效**的结构，不是理想蓝图。每条结论都对应本机可核对的配置或命令输出；未验证的项在正文明确标出。

## 0. 一句话

Magpie 是唯一的工程配置源，负责把全局指令、技能、MCP 和模型配置写进 Codex；Codex 是唯一的默认开发者，负责从需求到交付验收的闭环。Alma 是用户自行使用的独立应用，不属于这套团队与分发链。

```text
        ┌──────────────────────────────┐
        │  Magpie 资源库（唯一工程源）  │
        │  instructions / skills /      │
        │  MCP / 模型 / 备份同步        │
        └───────────┬──────────────────┘
                    │ magpie library sync
              ┌─────▼─────┐
              │   Codex   │
              │ 开发与交付 │
              └─────┬─────┘
                    │ MCP hub/codex + 宿主工具
                    ▼
              项目代码与业务环境
```

## 1. 分层与所有权

| 层 | 唯一职责 | 载体 | 谁写 |
|---|---|---|---|
| Magpie | 指令、技能、MCP、模型的工程配置源 | `~/.config/magpie/library/` + `library.json` | 用户 / 经授权的 Agent |
| 全局指令 | 项目无关的工作原则、授权、验证与交付边界 | `instructions.md` + `instructions/codex.md` | 只在资源库改 |
| 技能 | 业务规范与可选支撑能力 | `library/skills/`（4 个本地技能）+ Codex 技能插件（16 个） | 本地技能只在资源库改；插件在插件源目录改 |
| 项目事实 | 技术栈、命令、端口、项目授权 | 项目内 `AGENTS.md` 与项目文档 | 项目仓库 |
| 执行 | 搜索、数据库、Git、SSH、图片、浏览器 | Magpie 托管的 MCP + Codex 宿主工具 | Magpie / Codex |

边界规则：

- 规则只写边界和路由，不写长篇流程；流程放技能。
- 技能不复制全局规则，避免两处同时维护。
- 项目文档不放全局规则，全局规则不放业务细节。
- `~/.codex/AGENTS.md` 的 Magpie 生成块不手改。

项目状态记录属于项目事实，不进入 Magpie 全局规则。默认路径为 `docs/project-state.md`；已有状态文档或任务板直接复用。`setup-matt-pocock-skills` 只配置 issue tracker、triage labels 和领域文档布局，不创建状态文档；状态记录由当前任务按需建立和维护。

## 2. 指令分发

```text
instructions.md                    ← 公共正文
instructions/codex.md              ← Codex 专属补充
  └─► ~/.codex/AGENTS.md           ← 合并写入 magpie:begin … magpie:end 块
```

当前 `instructions.agents = ["codex"]`。Magpie 生成的块外内容属于用户，Magpie 更新不会覆盖。

Alma 的 `USER.md` 不再包含 Magpie 生成块；Alma 的指令、记忆与人格由 Alma 自己维护。

## 3. 技能分发

- `sharedSkills = false`，`skillRouter = true`；使用混合分发，避免把高频核心入口藏在路由后面。
- Magpie 资源库只剩 4 个本地技能：`ruoyi6`、`database-design` 直接暴露；`frontend-design`、`answer-me-with-html` 经 `~/.codex/skills/magpie-skills/.skills` 按需读取。它们都是指向资源库的 **Junction**。
- Matt Pocock 的 16 个简体中文技能由 Codex 插件 `mattpocock-skills-zh@magpie-mattpocock-zh` 提供，与 Magpie 直接技能互不重复。`grill-with-docs`、`grilling`、`domain-modeling`、`research`、`prototype`、`to-spec`、`writing-for-agents` 可由模型按 description 选择；`ask-matt`、`triage`、`wayfinder`、`to-tickets`、`setup-matt-pocock-skills`、`implement-spec`、`code-review`、`retro`、`handoff` 由元数据限制为显式调用，必须由用户确认后进入。当前 Codex 专属指令只补充 `ruoyi6`、`database-design`、`grill-with-docs` 三条优先触发路径。
- `~/.agents/skills/` 不再承载共享技能；Alma 的个人技能目录也不包含 Magpie Junction。

```text
Codex 自带技能匹配
  ├─ ruoyi6 / database-design（直接）
  ├─ magpie-skills（frontend-design / answer-me-with-html）
  └─ 16 个 Matt 中文插件技能
       └─ 路径不清时建议 ask-matt，用户确认后进入
```

工程阶段由 Codex 自己判断最短路径。小改动直接实现；当前会话能收敛时用 `grill-with-docs`；只有大型、跨会话且未知互相依赖时才建议 `wayfinder`，由用户确认后建决策地图。`research` 补外部事实，`prototype` 解决难以文字判断的 UI/行为问题，`grilling + domain-modeling` 收敛业务决策和领域术语；需要持久规格时用 `to-spec`，存在多个可交付切片或真实依赖时才建议 `to-tickets`。路径仍不清时建议 `ask-matt`，用户确认后导航。Codex 默认在当前会话实现；明确要求 `implement-spec` 时，由该技能启动隔离 worktree 的实现编排。`code-review` 仅在明确审查请求时调用，并由该请求授权启动两个并行只读审查子代理。

`wayfinder` 默认使用 `.scratch/<effort>/wayfinder.md` 和 `tickets/`，`to-spec` 默认使用 `.scratch/<feature-slug>/spec.md`，`to-tickets` 默认使用 `.scratch/<feature-slug>/issues/`，只有配置了外部 tracker 且获授权时才写 Issue；`grilling`、`research`、`wayfinder`、`implement-spec` 被当前任务调用时，即按其定义授权所需子代理，`prototype` 默认保留本地工件，其他委派、测试、提交和发布仍受全局授权控制。

## 4. MCP 拓扑

`mcpHub = true`：资源库登记 9 项，由 Magpie 统一启动和转发；`context7` 只勾选给 Codex，其余 8 项仍保留 Alma 的残留勾选，但 Alma 运行时未连接这些服务。

```text
资源库 9 项 ──► Magpie hub /mcp/magpie/hub/codex
```

| 服务 | 传输 | 用途 |
|---|---|---|
| `context7` | HTTP | 库与框架官方文档 |
| `dbx` | stdio | 数据库查询 / 获授权操作；目标按当前会话配置 |
| `gitee` | HTTP | Gitee 仓库与 Issue/PR |
| `github` | HTTP | GitHub 仓库与 Issue/PR |
| `magpie-image` | stdio | 图片生成与编辑 |
| `magpie-memory` | stdio | 跨 Agent 结构化记忆 |
| `magpie-vision` | stdio | 图像识别 |
| `magpie-web-search` | stdio | 联网搜索 |
| `ssh` | stdio | 已登记 SSH 目标 |

Alma 的 `~/.config/alma/mcp.json` 当前为 `{"mcpServers":{}}`，不再直连资源库 MCP，也不再保留 `hub/alma` 入口。Alma 自己的会话、通知、审批和 Herdr 能力由 Alma 应用自身提供，不经过 Magpie。`library.json` 中 8 项 MCP 仍带有 `alma` 勾选，这是配置残留；Alma 的运行时 MCP 列表为空，当前开发链只使用 Codex。

宿主内置工具（浏览器、computer-use、app-tools 等）不属于这 9 项，换机按 Codex 自身配置恢复。

## 5. 模型路由

```text
Codex ──► http://127.0.0.1:3425/v1            model_provider = "magpie"
```

Magpie 网关再按当前路由组选择上游模型。当前配置以 `~/.codex/config.toml` 为准；模型名和路由组成员不写进资源库。

## 6. 发布与备份

两套机制，职责不同：

| 机制 | 内容 | 频率 | 是否含密钥 |
|---|---|---|---|
| WebDAV 同步（`sync.json`） | 资源库、Agent 配置、供应商、登录态、设置 | 每 30 分钟 | 是，加密 |
| Git 仓库 `s1a7xia/magpie-library` | 可阅读的指令、4 个本地技能、16 个插件技能、3 条公开工程偏好、设计和使用说明 | 手动提交 | 否 |

Git 仓库是**可读副本**，不是运行备份。只克隆仓库不等于能力已安装；换机仍应先恢复 Magpie 加密备份。

本机生效目录 `~/.config/magpie/library/` 不带 `.git`。发布流程是：改资源库 → `magpie library sync` → 复制到发布工作副本 → 提交推送。

## 7. 设计取舍

已被采纳的取舍：

- **单一配置源**：不做第二套技能路由器，避免双所有权。
- **Codex 唯一开发闭环**：不让第二个 Agent 默认参与产品写入或交付。
- **不改写 Codex 全部配置**：Magpie 只写模型、MCP 入口和生成规则，sandbox、hooks、项目信任等仍归 Codex。
- **技能走 Junction**：改一处即可生效，避免多份副本漂移。

明确不做：

- 不恢复固定多 Agent 流水线。
- 不把密钥、DSN、登录态写进 Git。
- 不为“可能会用到”预留抽象层。

## 8. 当前已知边界

1. MCP 只做了工具暴露与最小调用验证，未对所有目标系统做全量业务测试。
2. `dbx` 的目标库绑定当前会话配置，`ssh` 依赖 `ssh-profiles.json`，换机需重配。
3. 版本未锁定：Magpie `0.1.4395`、Codex `0.169.0`。
4. Alma 已退出 Magpie 分发链，但其自身聊天、记忆、通知、微信和 Herdr 行为不在本资源库的管理范围内。
