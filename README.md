# Magpie 工程组合拳（RuoYi 6.0 Vue 版）

这是一套以 **RuoYi-Vue-Plus 6.0.0 + Vue 3 + Element Plus** 为主线的 AI 工程协作基线：把通用规则、工程技能、项目文档和工具连接统一放进 Magpie 资源库，再由 Magpie 分发给 Codex 等 Agent。

它解决的不是“让 AI 多写一点代码”，而是让每次开发都遵循同一条可追溯的路径：

```text
项目初始化
  -> 需求收敛
  -> 基线冻结
  -> 拆成可验收的切片
  -> 逐片实现、编译、提交
  -> 真实页面验收
  -> 完整审查
  -> 收尾
```

本仓库公开用于阅读、参考和溯源。**日常生效的源头不是本仓库**，而是本机 Magpie 资源库 `~/.config/magpie/library/`；本仓库是它的可读、可 diff、可回滚副本。

> 换电脑时，先用 Magpie 的同步备份恢复资源库、凭据和运行配置，再考虑克隆本仓库。完整依赖与恢复步骤见 [DEPENDENCIES.md](DEPENDENCIES.md)。

## 这一版改了什么

相比上一版 20 个技能：

- 保留 8 个显式流程：`setup-project`、`think`、`grill`、`story`、`implement`、`page-acceptance`、`review`、`debug`。
- 保留 2 个技术与设计技能：`ruoyi-6-vue`、`frontend-design`。
- 保留 6 个支撑/环境技能：`research`、`rules`、`answer-me-with-html`、`agent-browser`、`powershell-windows`、`ai-collaboration`。
- 删除 4 个重复层：`engineering-workflow`、`project-context`、`prompt-engineering`、`scm-collaboration`。它们的工作分别回到全局指令、`setup-project`、任务契约和平台 MCP/CLI。
- 把 RuoYi 技术层从 `ruoyi-plus-dev` 收敛为 `ruoyi-6-vue`，只保留 6.0.0 + Vue 需要的后端、前端、数据库、页面设计和官方文档地图。
- 在 `ruoyi-6-vue` 内按需增加 Warm-Flow、SnailJob 和 Soybean 条件参考；普通业务 CRUD 不预读这些领域知识。
- 不再照搬参考站的 40/83 个技能。参考站提供的是**文档地图和工程思路**，不是直接复制清单。

当前是 **16 个技能**，不是一条每次都要走完的流水线；会话只加载当前阶段真正需要的技能。

## 这套东西由什么组成

| 层 | 作用 | 当前载体 |
|---|---|---|
| 全局规则 | 说明什么能做、什么必须停、何时提交、何时验收 | `instructions.md`，同步到 Codex 的 `AGENTS.md` |
| 技能 | 把不同阶段的方法、检查门槛和输出约定固化 | `skills/` 下的 16 个技能 |
| 项目事实 | 当前目标、决策、验证证据、编译命令 | 项目内 `docs/agents/`，由 `setup-project` 创建 |
| 工具 | 搜索、文档、代码托管、数据库、SSH、图片和浏览器操作 | Magpie 托管的 7 个 MCP，加上本机 CLI |

各层各司其职：

- 规则不承载长篇流程，只负责边界和路由。
- 技能不重复复制全局规则，只负责本阶段怎么做。
- MCP 和 CLI 是执行能力，不代表已经连接、已经授权或已经验证。

## 项目怎么跑起来

先按任务规模选路径，不把完整流程套在单点改动上：

| 路径 | 适用 | 执行方式 |
|---|---|---|
| **Direct** | 错字、样式微调、单文件小修等明确低风险改动 | 主代理直接实现并核对 diff，不建 PRD |
| **Slice** | 已有冻结基线，只推进一个或少量已拆切片 | `implement` |
| **Baseline** | 新需求、多方案、跨模块、验收口径不清 | `think` → `grill` → `story` → `implement` |

### 0. 首次进入项目：`setup-project`

在新项目或协作方式发生明显变化时，明确要求“按通用资源库配置这个项目”。这是项目初始化与重配置入口，不是每个日常开发任务的前置门槛。

它会根据仓库事实生成或更新：

- `docs/agents/domain.md`、`coding-standards.md`、`project-state.md`、`project-decisions.md`、`verification.md`、`language.md`；
- 可选的 `issue-tracker.md`、`triage-labels.md`、`repo-map.md`、`ai-collaboration.md`；
- 可选的 `AGENTS.md` / `CLAUDE.md` 短指针（默认不创建，只写项目事实）；
- 前后端实际编译命令；
- 可选的多 Agent 协作或微信查看入口。

默认按 `ruoyi-6-vue`（RuoYi-Vue-Plus 6.0.0 + Vue）配置，不额外询问、不做框架探测。遇到非 RuoYi 项目时，在初始化时把 `Technical profile: none` 或选定的替代 profile 和理由写入项目配置；后续项目配置覆盖全局默认。微信入口是可选能力，不启用时项目仍可独立运行。

### 1. 需求和方案：`think` -> `grill`

- 需求确实模糊、存在多个实质不同方案时，使用 `think`。
- `think` 完成后自动进入 `grill`；也可以直接手动启动 `grill`。
- `research` 可以独立发起，也可以由 `think`、`implement`、`debug` 在执行中隐式触发。技术调研必须联网取权威来源，优先 `magpie-web-search`，其次 `context7`。
- `grill` 每次只问一个必须由人拍板的问题，并给出推荐答案。能从代码、表结构、文档回答的事实由 AI 自查，不反问用户。

结束时必须落盘：

- PRD 状态改为 `Grilled`；
- 术语同步到 `CONTEXT.md`；
- 满足条件的关键取舍写入 ADR；
- 用 `answer-me-with-html` 生成 `docs/baseline/PRD-NNNN-<slug>.html` 基线页。

基线页是给人快速确认“我们是否真的达成一致”的视图，PRD 才是事实源。基线冻结后，需求和验收标准是合同；后续变化写入 PRD 的 `Change Log`，不能绕过 PRD 直接改实现。

### 2. 拆任务：`story`

只有状态为 `Grilled` 的 PRD 才能进入 `story`。它把基线拆成可独立验收的纵向切片，并记录：

- 每个切片的验收标准；
- 每条 PRD 验收标准由哪个切片承接（`Covers`）；
- `blocked-by` 依赖；
- 适合 Agent 执行还是需要人处理；
- 本地切片清单和可选远端 Issue 的对应关系。

拆片前必须先做基线一致性检查：PRD 已冻结、无未决项、每条需求至少有一条可观察的验收标准、验收标准能追溯到需求、范围不矛盾、依赖无环。不通过就回 `grill`，不拿自相矛盾的基线拆任务。

默认把切片写回 PRD 的 `Sliced into`，本地 Markdown 就是事实源。只有项目配置了远端 Issue 跟踪且用户明确要求时才发布远端 Issue。`story` 完成后停下，不自动进入开发。

### 3. 开发：`implement`

`implement` 只在用户明确调用时进入，一次处理一批已确认的切片。`goal` 只能从 `implement` 起步，不从 think/story 自动进入。

每个切片：

1. 按验收标准做最小充分改动；
2. 默认加载 `ruoyi-6-vue`；涉及前端视图时自动加载 `frontend-design`；
3. 只编译受影响的一侧，并核对 diff；
4. 更新 PRD 中本切片状态；
5. 在**当前同一分支**提交并推送一次，提交信息带切片说明；
6. 标记为 `Dev Complete`。

开发阶段**不打开浏览器**，不执行页面验收，不运行全量测试。无人值守执行到这一层就停，不依赖登录态、验证码或人工测试环境。

整批完成后，先做覆盖门：每条需求和验收标准都有 `Dev Complete` 切片承接；更新 `project-state.md` 和 `verification.md`；输出切片、提交、推送和编译证据，并提示可以开始页面验收。

### 4. 页面验收：`page-acceptance`

页面验收是独立的、由用户主动发起的阶段：

```text
implement -> Dev Complete -> 用户发起 page-acceptance -> Accepted -> 用户发起 review
```

核心规则：

- 只通过真实前端 UI 操作，不写脚本直接请求后端 API。
- 先检查首屏、控制台和网络请求，再走一条主路径加一个边界。
- 增删改查优先完成 Create -> Read -> Update -> Delete 闭环，并清理测试数据。
- 元素引用在路由、弹窗、下拉框、表格刷新后立即失效，必须重新取可交互元素快照。
- 不抓取完整组件 DOM；不把读取源码当作视觉验收。
- 失败时结合控制台、网络和代码定位根因，修复后只重测受影响路径。
- 验证、修复、重测最多三轮，超限停止并报告。

RuoYi 6.0 Vue 的会话复用、`snapshot -i`、五步 CRUD 和错误闭环见 `skills/page-acceptance/references/ruoyi-6-vue-browser.md`。

验收通过后才把范围从 `Dev Complete` 改为 `Accepted`，并把 URL、角色、路径、边界、控制台/网络结果和证据写入 `docs/agents/verification.md`。

### 5. 完整审查：`review`

`review` 只能由用户明确发起，不能替代页面验收，也不会因为 `implement` 完成而自动运行。

它从测试、代码、影响三个视角检查当前改动；RuoYi-Vue-Plus 默认不写测试，因此测试视角只检查现有测试或明确要求执行的检查，不为审查擅自新增测试。确认的缺陷进入 `debug`；设计、风格或可维护性建议只列出，由用户决定是否处理。修复后重测受影响页面，不默认全批回归。

### 6. 收尾

`Accepted` 仍不等于 `Done`。只有项目约定的收尾条件满足后才是 `Done`，包括需要时的完整审查、文档同步和 Git 状态核验。

## 状态机

| 状态 | 含义 | 谁能推进 |
|---|---|---|
| `Draft` | 需求仍在形成 | `think` / 用户 |
| `Grilled` | 决策已收敛，基线冻结 | `grill` |
| `Sliced` | 已拆成有依赖关系的可验收切片 | `story` |
| `In Progress` | 正在按切片实现 | `implement` |
| `Dev Complete` | 代码完成、编译通过、已提交推送，但未做页面验收 | `implement` |
| `Accepted` | 声明的页面范围已在真实浏览器通过 | `page-acceptance` |
| `Done` | 项目收尾条件全部满足 | 用户 / 项目约定 |

关键边界：

- 页面验收通过是 `Accepted`，不是直接 `Done`。
- `review` 不能绕过页面验收。
- 编译通过不等于界面可用，代码审查也不能替代渲染验证。
- 不是每个小任务都要走完整流水线；临时修复和明确的小改动可以直接处理。

## 常用请求

| 你说什么 | 会进入什么环节 |
|---|---|
| “按通用资源库配置这个项目” | `setup-project` |
| “这个需求先帮我想想方案” | `think`，完成后自动进入 `grill` |
| “把这个方案往死里拷问” | 直接 `grill` |
| “调研一下这个版本的最佳实践” | `research` |
| “把冻结的基线拆成任务” | `story` |
| “按这批切片开始实现” | `implement` |
| “开始页面测试，验收这几个页面” | `page-acceptance` |
| “完整审查这批改动” | `review` |
| “这里报错了 / 回归了” | `debug` |
| “开始做，但先别提交” | 直接开发，保留本地改动，不提交 |
| “测试没问题，可以收尾” | 同步受影响文档并完成已授权的 Git 收尾 |

## 技能分层

### 核心流程（8）

| 技能 | 作用 |
|---|---|
| `setup-project` | 初始化或重配项目协作基线，是项目配置入口 |
| `think` | 发散、收敛方案，生成初始 PRD |
| `grill` | 逐项拷问未决问题，冻结业务基线并生成基线页 |
| `story` | 从冻结基线拆纵向切片和依赖 |
| `implement` | 按批实现切片，编译、提交、推送，停在页面验收前 |
| `page-acceptance` | 在真实浏览器完成页面、视觉、交互、数据和权限验收 |
| `review` | 用户明确发起的三视角完整审查 |
| `debug` | 根因定位和系统性修复 |

### 技术与设计（2）

| 技能 | 作用 |
|---|---|
| `ruoyi-6-vue` | RuoYi-Vue-Plus 6.0.0 + Vue 单一技术入口；按任务加载后端、前端、数据库、页面设计和官方文档地图 |
| `frontend-design` | 业务页在既有组件系统内提升质感；独立展示页可做完整视觉设计 |

### 支撑与环境（6）

| 技能 | 作用 |
|---|---|
| `research` | 联网查权威资料，形成可追溯的技术调研记录 |
| `rules` | 共享入口协议、反模式和工程原则，不是独立任务技能 |
| `answer-me-with-html` | 把复杂结论、架构和流程生成单页 HTML；基线页由它渲染 |
| `agent-browser` | 浏览器自动化技能；页面验收优先使用当前 Agent 已有浏览器能力 |
| `powershell-windows` | Windows PowerShell 的可靠写法与常见坑 |
| `ai-collaboration` | 定义 Codex、dsh 和可选微信入口的职责边界 |

### 维护规则

- 新增技能前先确认三件事：有独立触发词、有独立产物、不能作为现有技能的参考文件。缺一项就扩展原技能，不新建。
- 技能正文只写本阶段方法；全局约束、编译口径、提交边界不重复抄写。
- 删除或合并低频技能优先于继续添加；共享模式下的技能越少，路由和上下文成本越低。
- 每次改完运行 `python scripts/verify-library.py`，检查技能清单、frontmatter、全量 Markdown 相对链接、同步和凭证提示。

## RuoYi 6.0 Vue 技术层

`ruoyi-6-vue` 不按后端、前端、数据库拆成多个技能，而是单一入口按需加载：

| 任务 | 读取 |
|---|---|
| 任何 RuoYi 业务改动 | `references/common.md` |
| Java / Spring Boot / MyBatis-Plus / Sa-Token | `references/backend.md` |
| Vue 3 / TypeScript / Element Plus | `references/frontend.md` |
| 表结构 / SQL / 字典 / 参数 / 菜单 | `references/database.md` |
| 可见页面、布局、样式、仪表盘 | `references/ui-design.md` |
| Warm-Flow 流程定义、发起流程、待办/已办、审批与业务集成 | `references/workflow.md` |
| SnailJob、定时任务、分布式调度、失败重试、任务日志 | `references/snail-job.md` |
| Excel 导入/导出、模板、字典转换、大批量导出 | `references/excel.md` |
| 文件上传/下载、OSS、附件字段、预览和存储配置 | `references/file-oss.md` |
| WebSocket/SSE、站内消息、实时通知、消息推送 | `references/messaging.md` |
| 菜单/按钮权限、数据范围、字段脱敏、多租户判断 | `references/access-control.md` |
| 目标前端实际采用 Soybean Admin + Naive UI | `references/soybean-ui.md`（仅该前端） |
| 需要查官方规范或功能说明 | `references/docs-map.md` |

普通业务 CRUD 只加载 `common` 和对应的后端/前端/数据库文件；工作流、SnailJob 和 Soybean 都是条件参考，不因模块存在而预读。Soybean 是可选前端变体，不替代默认的 `plus-ui + Element Plus`。

业务功能参考的边界：

- **已覆盖**：Excel、文件/OSS、实时消息、权限/数据范围/多租户判断、Warm-Flow、SnailJob。
- **暂不单独展开**：AI/MCP、MQTT、Elasticsearch、社交登录、短信/邮件等。遇到真实任务时先读目标源码和现有模块，不预建一套通用知识。
- **多租户**：`ruoyi-p0` 当前没有完整租户链路，`access-control.md` 只要求先判断项目是否真的启用，不把文档站的完整多租户方案当成 6.0.0 源码事实。

事实优先级：目标工程源码 > 6.0.0 源码核对过的约束 > 官方文档地图（正文默认 3.5.x）> 通用框架习惯。不要用文档站的 3.5.x 类名或配置直接覆盖 6.0.0 项目。

## 文档怎么分工

初始化后的项目通常按以下职责保存事实：

| 位置 | 记录什么 |
|---|---|
| `AGENTS.md` / `CLAUDE.md`（可选） | 项目已有或明确要求时使用；只写项目事实和 `docs/agents/` 指针，不复制全局工作流、编译、页面验收和 Git 规则 |
| `docs/agents/domain.md` | CONTEXT、PRD、ADR、research 的实际路径 |
| `docs/agents/coding-standards.md` | 项目约定、技术 profile、源码证据、实际编译命令 |
| `docs/agents/project-state.md` | 当前目标、阶段面板、阻塞、下一步和真实编译命令 |
| `docs/agents/project-decisions.md` | 已确认、跨任务有效的决策 |
| `docs/agents/verification.md` | 带版本、命令、结果和来源的验证证据 |
| `docs/prd/` | PRD、验收标准和变更记录 |
| `docs/adr/` | 重要的架构与实现取舍 |
| `docs/baseline/` | 冻结基线的可视 HTML 页面 |
| `docs/research/` | 可复用的技术调研记录和索引 |
| `CONTEXT.md` | 业务术语表，不写实现细节 |

文档记录必须区分 Agent 实测、用户确认和未验证项。原始聊天历史不是项目事实，凭证、完整认证头和私密数据不进入文档、提交或截图。

## 依赖摘要

当前基线使用：

- Magpie `0.1.3255`
- Codex
- Node.js `v24.17.0`、npm `11.13.0`
- Python `3.13.14`
- Git `2.54.0`
- `gh 2.103.2`、`glab 1.128.0`（按托管平台选用）
- `rtk 1.1.0`
- Chrome 和 Edge

MCP 由 Magpie 统一托管，当前登记 7 个：`context7`、`dbhub`、`gitee`、`github`、`magpie-image`、`magpie-web-search`、`ssh`。

版本、Agent 分发矩阵、凭据位置、换机恢复、校验和故障处理见 [DEPENDENCIES.md](DEPENDENCIES.md)。

## 目录

| 路径 | 说明 |
|---|---|
| `instructions.md` | 通用协作指令正文 |
| `skills/` | 16 个技能及其引用、模板和脚本 |
| `scripts/verify-library.py` | 资源库结构、链接、同步和凭证提示检查 |
| `README.md` | 组合介绍、工作流与使用说明 |
| `DEPENDENCIES.md` | 运行依赖、MCP、恢复与校验 |

## 维护和发布

技能与指令的编辑源是 Magpie 资源库，不是本仓库。

正确顺序：

1. 修改 `~/.config/magpie/library/` 中的源文件；
2. 运行：

   ```powershell
   magpie library sync
   python "$env:USERPROFILE\.config\magpie\library\scripts\verify-library.py"
   ```

3. 确认 `~/.agents/skills` 与源一致；
4. 把同一组改动同步到本仓库；
5. 只提交本次文档或技能变更，核对 diff 后推送；
6. 核验本地 `HEAD`、`origin/main` 和远端引用一致。

直接在本仓库改技能不会生效：下一次 `magpie library sync` 会以本机资源库为准覆盖差异。

## 已知边界

- 本仓库只保存可阅读的规则和技能，不保存 API 密钥、登录态、同步密码或机器专属配置。
- “已登记 MCP”不等于“当前会话已连通”；需要实际调用一次才算验证。
- `dbhub` 依赖本机 PostgreSQL 和正确的 DSN，换机后目标可能变化。
- `agent-browser` 技能已安装，但 CLI 未在当前 PATH；页面验收优先使用当前 Agent 的浏览器能力。需要跨机器一致行为时执行 `npm i -g agent-browser && agent-browser install`，并在新会话确认。
- 全局指令目前只分发给 Codex；16 个技能在共享目录中，但各 Agent 的逐项勾选不同。
- 不启用工程编排 Hook 和子代理；主代理负责判断、执行和交付。

## 永不入库

- API 密钥、令牌、认证头；
- 数据库连接串和密码；
- 浏览器登录态与订阅凭据；
- WebDAV/S3/GitHub 同步密码和 passphrase；
- 生产数据、个人数据、完整隐私日志；
- 运行时缓存、`__pycache__`、编辑备份和 `*.magpie-backup`。
