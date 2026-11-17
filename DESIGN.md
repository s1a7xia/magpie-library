# 当前设计：Magpie + Codex

更新日期：2026-11-17。本文描述**当前实际生效**的结构，不是理想蓝图。每条结论都对应本机可核对的配置或命令输出；未验证的项在正文明确标出。

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
| 全局指令 | 项目无关的工作原则、授权、验证与交付边界 | `instructions.md` | 只在资源库改 |
| 技能 | 工程阶段方法、业务规范与可选支撑能力 | `library/skills/`（16 个） | 只在资源库改 |
| 项目事实 | 技术栈、命令、端口、项目授权 | 项目内 `AGENTS.md` 与项目文档 | 项目仓库 |
| 执行 | 搜索、数据库、Git、SSH、图片、浏览器 | Magpie 托管的 MCP + Codex 宿主工具 | Magpie / Codex |

边界规则：

- 规则只写边界和路由，不写长篇流程；流程放技能。
- 技能不复制全局规则，避免两处同时维护。
- 项目文档不放全局规则，全局规则不放业务细节。
- `~/.codex/AGENTS.md` 的 Magpie 生成块不手改。

项目状态记录属于项目事实，不进入 Magpie 全局规则。默认路径为 `docs/project-state.md`；已有状态文档或任务板直接复用。`docs/agents/project-state.md` 这种独立路径配置不再生成，状态维护规则统一由 `skills/rules/entry-protocol.md` 的 Project State Maintenance 提供。`setup-project` 只初始化记录，不运行后台同步。

## 2. 指令分发

```text
instructions.md                    ← 唯一正文
  └─► ~/.codex/AGENTS.md           ← Codex 的 magpie:begin … magpie:end 块
```

当前 `instructions.agents = ["codex"]`。Magpie 生成的块外内容属于用户，Magpie 更新不会覆盖。

Alma 的 `USER.md` 不再包含 Magpie 生成块；Alma 的指令、记忆与人格由 Alma 自己维护。

## 3. 技能分发

- `sharedSkills = true`，`skillRouter = true`。
- 资源库 16 个技能：`agent-browser`、`answer-me-with-html`、`api-regression`、`database-design`、`debug`、`dev-workflow`、`frontend-design`、`grill`、`implement`、`research`、`review`、`rules`、`ruoyi6`、`setup-project`、`story`、`think`。
- `~/.agents/skills/` 的每一项都是指向资源库的 **Junction**，不是副本。
- `library.json` 当前把全部 16 个技能只勾选给 `codex`。
- Alma 的个人技能目录不再包含 Magpie Junction；它自己的 bundled 与 personal 技能独立管理。

工程阶段技能源自 `dev-workflow`，共 10 个：

`dev-workflow`（唯一入口）、`think`、`grill`、`story`、`implement`、`debug`、`review`、`research`、`rules`、`setup-project`。

`dev-workflow` 只做路由，不要求每次走完全部阶段。除它之外，只有 `database-design` 等业务规范可独立发现；其余阶段和 `rules` 的 `openai.yaml` 均设为 `allow_implicit_invocation: false`，由入口按需读取，避免描述常驻和路由竞争；它们仍可通过 `$think`、`$review` 等显式调用。

2026-11-17 用 `codex debug prompt-input` 实测新会话提示：资源库侧可自动发现的是 `agent-browser`、`answer-me-with-html`、`dev-workflow`、`database-design` 和 `ruoyi6`；其余内部阶段不会常驻技能描述列表。

## 4. MCP 拓扑

`mcpHub = true`：资源库登记 10 项，由 Magpie 统一启动和转发；`library.json` 当前只标记给 `codex`。

```text
资源库 10 项 ──► Magpie hub /mcp/magpie/hub/codex
```

| 服务 | 传输 | 用途 |
|---|---|---|
| `chrome-devtools` | stdio | Chrome 页面检查与调试 |
| `context7` | HTTP | 库与框架官方文档 |
| `dbhub` | stdio | PostgreSQL 只读取证 / 获授权操作 |
| `gitee` | HTTP | Gitee 仓库与 Issue/PR |
| `github` | HTTP | GitHub 仓库与 Issue/PR |
| `magpie-image` | stdio | 图片生成与编辑 |
| `magpie-memory` | stdio | 跨 Agent 结构化记忆 |
| `magpie-vision` | stdio | 图像识别 |
| `magpie-web-search` | stdio | 联网搜索 |
| `ssh` | stdio | 已登记 SSH 目标 |

Alma 的 `~/.config/alma/mcp.json` 当前为 `{"mcpServers":{}}`，不再直连资源库 MCP，也不再保留 `hub/alma` 入口。Alma 自己的会话、通知、审批和 Herdr 能力由 Alma 应用自身提供，不经过 Magpie。

宿主内置工具（浏览器、computer-use、app-tools 等）不属于这 10 项，换机按 Codex 自身配置恢复。

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
| Git 仓库 `s1a7xia/magpie-library` | 可阅读的指令、技能、设计和使用说明 | 手动提交 | 否 |

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
2. `dbhub` 绑定本机 PostgreSQL，`ssh` 依赖 `ssh-profiles.json`，换机需重配。
3. 版本未锁定：Magpie `0.1.4252`、Codex `0.169.0`。
4. Alma 已退出 Magpie 分发链，但其自身聊天、记忆、通知、微信和 Herdr 行为不在本资源库的管理范围内。
