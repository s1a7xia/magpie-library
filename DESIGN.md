# 当前设计：Magpie / Codex / Alma / Herdr

更新日期：2026-11-13。本文描述**当前实际生效**的结构，不是理想蓝图。每条结论都对应本机可核对的配置或命令输出；未验证的项在下文明确标出。

## 0. 一句话

Magpie 是唯一的配置源，负责把指令、技能、MCP、模型写进各个 Agent；Codex 是唯一的默认开发者；Alma 是按需启动的观察与协调面板，通过 Herdr 管理 Codex 会话。

```text
        ┌──────────────────────────────┐
        │  Magpie 资源库（唯一源）      │
        │  instructions / skills /      │
        │  MCP / 模型 / 备份同步        │
        └───────────┬──────────────────┘
                    │ magpie library sync
        ┌───────────┴───────────┐
        │                       │
   ┌────▼─────┐          ┌──────▼──────┐
   │  Codex   │          │    Alma     │
   │ 开发写入 │          │ 观察/协调    │
   └────┬─────┘          └──────┬──────┘
        │  MCP hub/codex         │ MCP hub/alma（0 工具）
        │                        │ Herdr CLI / API
        └────────┬───────────────┘
                 │
          ┌──────▼──────┐
          │   Herdr     │
          │ 会话/终端    │
          └─────────────┘
```

## 1. 分层与所有权

| 层 | 唯一职责 | 载体 | 谁写 |
|---|---|---|---|
| Magpie | 指令、技能、MCP、模型的配置源 | `~/.config/magpie/library/` + `library.json` | 用户 / 经授权的 Agent |
| 全局指令 | 项目无关的角色、授权、验证与交付边界 | `instructions.md`，可选 `instructions/<agent>.md` | 只在资源库改 |
| 技能 | 阶段方法与检查门槛 | `library/skills/` | 只在资源库改 |
| 工程阶段 | 需求、设计、实现、调试、审查、文档 | `dev-skills` 插件 | 插件版本管理 |
| 项目事实 | 技术栈、命令、端口、项目授权 | 项目内 `AGENTS.md` 与项目文档 | 项目仓库 |
| 执行 | 搜索、数据库、Git、SSH、图片 | Magpie 托管的 MCP + 宿主内置工具 | Magpie / Codex |
| 运行观察 | 会话、通知、审批、持久协调 | Alma + Herdr | Alma |

边界规则：

- 规则只写边界和路由，不写长篇流程；流程放技能。
- 技能不复制全局规则，避免两处同时维护。
- 项目文档不放全局规则，全局规则不放业务细节。
- 生成物（Codex `AGENTS.md`、Alma `USER.md`）不手改。

## 2. 指令分发

```text
instructions.md                    ← 唯一正文
  ├─ + instructions/codex.md       ← Codex 专属追加
  └─ + instructions/alma.md        ← Alma 专属追加
```

分发结果：

| 目标 | 路径 | 形态 |
|---|---|---|
| Codex | `~/.codex/AGENTS.md` | 用户自有段 + `magpie:begin` … `magpie:end` 块 |
| Alma | `~/.config/alma/USER.md` | `magpie:begin` … `magpie:end` 块 |

当前 `instructions.agents = ["alma", "codex"]`。块外内容属于用户，Magpie 更新不会覆盖。

## 3. 技能分发

- `sharedSkills = true`，`skillRouter = true`。
- 资源库技能 6 个：`answer-me-with-html`、`api-regression`、`database-design`、`frontend-design`、`ruoyi6`、`team-orchestration`。
- `~/.agents/skills/` 的每一项都是指向资源库的 **Junction**，不是副本。
- Alma 的 `~/.config/alma/skills/team-orchestration` 也是 Junction，指向 `~/.agents/skills/`。
- 逐 Agent 勾选独立于共享目录：共享目录可见 ≠ 该 Agent 已启用。

当前勾选：

| 技能 | Codex | Alma |
|---|---|---|
| `answer-me-with-html` | ✓ | |
| `api-regression` | ✓ | |
| `database-design` | ✓ | |
| `frontend-design` | ✓ | |
| `ruoyi6` | ✓ | |
| `team-orchestration` | ✓ | ✓ |

工程阶段不在资源库，由 `dev-skills` 插件提供，当前 **0.2.11**，共 10 个技能：

`dev-workflow`（唯一入口）、`think`、`grill`、`story`、`implement`、`debug`、`review`、`research`、`rules`、`setup-project`。

`dev-workflow` 只做路由，不要求每次走完全部阶段。

## 4. MCP 拓扑

`mcpHub = true`：资源库登记 9 项，由 Magpie 统一启动和转发。

```text
资源库 9 项 ──► Magpie hub ──┬─► /mcp/magpie/hub/codex  （9 项全量）
                             └─► /mcp/magpie/hub/alma    （0 工具）
```

| 服务 | 传输 | 用途 |
|---|---|---|
| `context7` | HTTP | 库与框架官方文档 |
| `dbhub` | stdio | PostgreSQL 只读取证 / 获授权操作 |
| `gitee` | HTTP | Gitee 仓库与 Issue/PR |
| `github` | HTTP | GitHub 仓库与 Issue/PR |
| `magpie-image` | stdio | 图片生成 |
| `magpie-memory` | stdio | 跨 Agent 结构化记忆 |
| `magpie-vision` | stdio | 图像识别 |
| `magpie-web-search` | stdio | 联网搜索 |
| `ssh` | stdio | 已登记 SSH 目标 |

为什么 Alma 的 hub 是空的：Alma 的职责是观察和协调，不需要开发工具集。给它 0 工具可以避免协调上下文顺手改代码或写库。Alma 自己的会话、通知、审批和 Herdr 能力由 Alma 应用自身提供，不经过 MCP。

宿主内置工具（浏览器、computer-use、app-tools 等）不属于这 9 项，换机按 Codex 自身配置恢复。

## 5. 模型路由

```text
Codex ──► http://127.0.0.1:3425/v1            model_provider = "magpie"
Alma  ──► http://127.0.0.1:3425/v1            provider "magpie"
        （两者都经由本机 Magpie 网关，再由网关路由到上游）
```

当前两边模型都是 `group/ds4.1-light`，Effort 为 `low`。`group/*` 是 Magpie 的路由组，成员和优先级在 Magpie 内维护，不写进资源库。

Alma 自身另有四个模型引用，全部指向同一个 Magpie provider：

| 配置项 | 用途 |
|---|---|
| `chat.defaultModel` | Alma 主对话 |
| `weixin.defaultModel` | 微信通道 |
| `toolModel.model` | Alma 内部工具调用 |
| `imageGen.model` | 图片生成 |

这四项属于 Alma 机器状态，不在资源库；Magpie 只接管 Alma 的 `model` 字段。

## 6. Alma / Herdr 运行观察

```text
微信 / 手机 App ──► Alma（localhost:23001）──► Herdr ──► Codex 会话
                              │
                              └─► mobile relay（relay.alma.now，端到端加密）
```

- Alma 服务：`alma-server`，监听 `127.0.0.1:23001`。
- Herdr：`herdr-core serve` + `herdr server`，会话持久，pane 可在重启后恢复。
- Codex 集成：`SessionStart` hook 执行 `~/.codex/herdr-agent-state.ps1`，把会话 ID 上报给所在 pane。
- Alma 通过 `alma herdr new|send|chats|workspaces|follow|answer` 管理这些 pane。

### 6.1 远程可见性矩阵（重要）

| 会话类型 | 手机/微信能看到执行情况 | 原因 |
|---|---|---|
| 在 Herdr pane 中运行的 Codex | ✅ 能 | pane 有 `HERDR_PANE_ID`，Alma 通过 Herdr 读取状态和输出 |
| Alma 自己的会话（含微信来源） | ✅ 能 | 就是 Alma 的 thread |
| Codex Desktop 直接打开的会话 | ❌ 不能 | 没有 Herdr pane 标记，不在 Alma 的发现范围 |
| 普通终端里直接跑的 `codex` | ❌ 不能 | 同上，除非通过 Herdr 启动 |

结论：**要远程看实时执行情况，必须让 Codex 跑在 Herdr 里**。不需要用户手动开 Herdr，让 Alma 发起即可。

### 6.2 邀请跟随

`alma herdr follow --pane <id>` 只在 Alma 会话内有效（需要 `ALMA_THREAD_ID`）。在外部终端直接调用会返回 `missing_thread`，这是设计行为，不是故障。

## 7. 发布与备份

两套机制，职责不同：

| 机制 | 内容 | 频率 | 是否含密钥 |
|---|---|---|---|
| WebDAV 同步（`sync.json`） | 资源库、Agent 配置、供应商、登录态、记忆、设置 | 每 30 分钟 | 是，加密 |
| Git 仓库 `s1a7xia/magpie-library` | 可阅读的指令、技能、设计和使用说明 | 手动提交 | 否 |

Git 仓库是**可读副本**，不是运行备份。只克隆仓库不等于能力已安装；换机仍应先恢复 Magpie 加密备份。

本机生效目录 `~/.config/magpie/library/` 不带 `.git`。发布流程是：改资源库 → `magpie library sync` → 复制到发布工作副本 → 提交推送。

## 8. 设计取舍

已被采纳的取舍：

- **单一配置源**：不做第二套技能路由器，避免双所有权。
- **Alma 零开发工具**：观察者不该顺手成为写入者。
- **不改写 Codex 全部配置**：Magpie 只写模型与 MCP 入口，sandbox、hooks、项目信任等仍归 Codex。
- **技能走 Junction**：改一处即可生效，避免六份副本漂移。

明确不做：

- 不引入独立技能路由运行时（当前 6 + 10 个技能规模不需要）。
- 不把密钥、DSN、登录态写进 Git。
- 不让 Alma 自动成为第二个产品写作者。
- 不为“可能会用到”预留抽象层。

## 9. 当前已知边界

1. Codex Desktop 会话不可被 Alma 观察，除非改跑在 Herdr。
2. Alma 的 provider 模型列表少于 Magpie 网关暴露的模型（缺 8 个 `our-free-model/*`），不影响现有链路。
3. MCP 只做了工具暴露与最小调用验证，未对所有目标系统做全量业务测试。
4. `dbhub` 绑定本机 PostgreSQL，`ssh` 依赖 `ssh-profiles.json`，换机需重配。
5. 版本未锁定：Magpie `0.1.3887`、Codex `0.167.2`、Alma `0.4.579`、`dev-skills` `0.2.11`、Herdr `0.9.5` / `herdr-core` `0.1.20`。
