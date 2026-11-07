# Magpie 工程组合拳（私有）

这是一套跨项目的 AI 工程协作基线：把**通用规则、工程技能、工具连接**统一放进 Magpie 资源库，再由 Magpie 分发给 Codex 等 Agent。

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

仓库私有，主要用于溯源和阅读。**日常生效的源头不是本仓库**，而是本机 Magpie 资源库 `~/.config/magpie/library/`；本仓库是它的可读、可 diff、可回滚副本。

> 换电脑时，先用 Magpie 的同步备份恢复资源库、凭据和运行配置，再考虑克隆本仓库。完整依赖与恢复步骤见 [DEPENDENCIES.md](DEPENDENCIES.md)。

## 这套东西由什么组成

| 层 | 作用 | 当前载体 |
|---|---|---|
| 全局规则 | 说明什么能做、什么必须停、何时提交、何时验收 | `instructions.md`，同步到 Codex 的 `AGENTS.md` |
| 技能 | 把不同阶段的方法、检查门槛和输出约定固化 | `skills/` 下的 20 个技能 |
| 工具 | 搜索、文档、代码托管、数据库、SSH、图片和浏览器操作 | Magpie 托管的 7 个 MCP，加上本机 CLI |

三层各司其职：

- 规则不承载长篇流程，只负责边界和路由。
- 技能不重复复制全局规则，只负责本阶段怎么做。
- MCP 和 CLI 是执行能力，不代表已经连接、已经授权或已经验证。

## 项目怎么跑起来

### 0. 首次进入项目：`setup-project`

在新项目或协作方式发生明显变化时，明确要求“按通用资源库配置这个项目”。这是进入整套工作流的入口。

它会根据仓库事实生成或更新：

- `AGENTS.md` 中的协作与工程原则；
- `docs/agents/` 下的项目状态、决策、验证证据、文档路径、Issue 跟踪和编码标准；
- 前后端实际编译命令；
- 可选的多 Agent 协作或微信查看入口。

默认按 **RuoYi-Vue-Plus** 工艺配置，不额外询问、不做框架探测。遇到非 RuoYi 项目时，用一句话排除即可。微信入口是可选能力，不启用时项目仍可独立运行。

### 1. 需求和方案：`think` -> `grill`

- 需求确实模糊、存在多个实质不同方案时，使用 `think`。
- `think` 完成后自动进入 `grill`；也可以直接手动启动 `grill`。
- `research` 可以独立发起，也可以由 `think`、`implement`、`debug` 在执行中隐式触发。技术调研必须联网取权威来源。
- 复杂、跨步骤或草稿化的执行请求，主代理按 `prompt-engineering` 内部整理任务契约；简单任务不套这层流程。

`grill` 每次只问一个必须由人拍板的问题，并给出推荐答案。能从代码、表结构、文档回答的事实由 AI 自查，不反问用户。

结束时必须落盘：

- PRD 状态改为 `Grilled`；
- 术语同步到 `CONTEXT.md`；
- 满足条件的关键取舍写入 ADR；
- 用 `answer-me-with-html` 生成 `docs/baseline/PRD-NNNN-<slug>.html` 基线页。

基线页是给人快速确认“我们是否真的达成一致”的视图，PRD 才是事实源。基线冻结后，需求和验收标准是合同；后续变化写入 PRD 的 `Change Log`，不能绕过 PRD 直接改实现。

### 2. 拆任务：`story`

只有状态为 `Grilled` 的 PRD 才能进入 `story`。它把基线拆成可独立验收的纵向切片，并记录：

- 每个切片的验收标准；
- `blocked-by` 依赖；
- 适合 Agent 执行还是需要人处理；
- 本地切片清单和远端 Issue 的对应关系。

`story` 完成后停下，不自动进入开发。由用户决定是否开始一批切片。

### 3. 开发：`implement`

`implement` 只在用户明确调用时进入，一次处理一批已确认的切片。

每个切片：

1. 按验收标准做最小充分改动；
2. 自动加载 `ruoyi-plus-dev`；涉及前端视图时自动加载 `frontend-design`；
3. 只编译受影响的一侧，并核对 diff；
4. 更新 PRD 和项目运行态文档；
5. 在**当前同一分支**提交并推送一次，提交信息带切片说明；
6. 标记为 `Dev Complete`。

开发阶段**不打开浏览器**，不执行页面验收，不运行全量测试。无人值守执行到这一层就停，不依赖登录态、验证码或人工测试环境。

整批完成后，输出切片、提交、推送和编译证据，并提示可以开始页面验收。

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

验收通过后才把范围从 `Dev Complete` 改为 `Accepted`，并把 URL、角色、路径、边界、控制台/网络结果和证据写入 `docs/agents/verification.md`。

### 5. 完整审查：`review`

`review` 只能由用户明确发起，不能替代页面验收，也不会因为 `implement` 完成而自动运行。

它从测试、代码、影响三个视角检查当前改动。确认的缺陷进入 `debug`；设计、风格或可维护性建议只列出，由用户决定是否处理。修复后重测受影响页面，不默认全批回归。

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

## 20 个技能

### 流程

| 技能 | 作用 |
|---|---|
| `engineering-workflow` | 根据当前情形选择阶段，避免机械串联全部技能 |
| `setup-project` | 初始化或重配项目协作基线，是进入完整流程的入口 |
| `think` | 发散、收敛方案，生成初始 PRD |
| `grill` | 逐项拷问未决问题，冻结业务基线并生成基线页 |
| `research` | 联网查权威资料，形成可追溯的技术调研记录 |
| `story` | 从冻结基线拆纵向切片和依赖 |
| `implement` | 按批实现切片，编译、提交、推送，停在页面验收前 |
| `debug` | 根因定位和系统性修复 |
| `review` | 用户明确发起的三视角完整审查 |
| `prompt-engineering` | 把复杂或草稿化请求整理为任务契约后再执行 |

### 质量

| 技能 | 作用 |
|---|---|
| `page-acceptance` | 在真实浏览器完成页面、交互、数据和权限验收 |
| `frontend-design` | 业务页在既有组件系统内提升质感；独立展示页可做完整视觉设计 |
| `rules` | 共享入口协议、反模式和工程原则，不是独立任务技能 |

### 工具与环境

| 技能 | 作用 |
|---|---|
| `agent-browser` | 浏览器自动化 CLI；当前机器尚未安装，页面验收会优先使用当前 Agent 已有的浏览器能力 |
| `powershell-windows` | Windows PowerShell 的可靠写法与常见坑 |
| `answer-me-with-html` | 把复杂结论、架构和流程生成单页 HTML；基线页由它渲染 |

### 项目与协作

| 技能 | 作用 |
|---|---|
| `project-context` | 维护跨会话的项目状态、决策和验证证据 |
| `ai-collaboration` | 定义 Codex、dsh 和可选微信入口的职责边界 |
| `scm-collaboration` | GitHub、GitLab、Gitee 或本地任务跟踪的统一流程 |
| `ruoyi-plus-dev` | RuoYi-Vue-Plus 前后端和 SQL 的团队工艺与检查门槛 |

## 文档怎么分工

初始化后的项目通常按以下职责保存事实：

| 位置 | 记录什么 |
|---|---|
| `AGENTS.md` | 当前项目必须遵守的协作、工程和命令约定 |
| `docs/agents/project-state.md` | 当前目标、进度、阻塞、下一步和真实编译命令 |
| `docs/agents/project-decisions.md` | 已确认、跨任务有效的决策 |
| `docs/agents/verification.md` | 带版本、命令、结果和来源的验证证据 |
| `docs/prd/` | PRD、验收标准和变更记录 |
| `docs/adr/` | 重要的架构与实现取舍 |
| `docs/baseline/` | 冻结基线的可视 HTML 页面 |
| `docs/research/` | 可复用的技术调研记录和索引 |
| `CONTEXT.md` | 业务术语表，不写实现细节 |

文档记录必须区分 Agent 实测、用户确认和未验证项。原始聊天历史不是项目事实，凭证、完整认证头和私密数据不进入文档、提交或截图。

## 前端和 RuoYi 的默认口径

写 `.vue`、`.tsx`、样式、组件或布局时，自动按 `frontend-design` 处理：

- **业务 CRUD 页**使用 Enhance 模式：保留 Element Plus 表格、表单、弹窗、分页、字典标签等既有行为，把力气用在层级、间距、状态语义、空状态和详情抽屉。
- **登录页、工作台、态势大屏等展示页**使用 Design 模式，可以做深色主题、KPI 卡片和图表联动。
- 禁止把廉价渐变字、无意义毛玻璃、卡片左侧粗色条当成默认“高级感”。
- 交付前核对横向溢出、按钮折行、深色模式对比度和 `z-index` 遮挡。

修改 RuoYi-Vue-Plus 后端、plus-ui 或 SQL 时，自动加载 `ruoyi-plus-dev`；框架复用、权限、数据权限、加解密和字段映射以项目实际版本为准。

## 依赖摘要

当前基线使用：

- Magpie `0.1.3233`
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
| `skills/` | 20 个技能及其引用、模板和脚本 |
| `README.md` | 组合介绍、工作流与使用说明 |
| `DEPENDENCIES.md` | 运行依赖、MCP、恢复与校验 |

## 维护和发布

技能与指令的编辑源是 Magpie 资源库，不是本仓库。

正确顺序：

1. 修改 `~/.config/magpie/library/` 中的源文件；
2. 运行：

   ```powershell
   magpie library sync
   python "$env:USERPROFILE\.config\magpie\library\skills\engineering-workflow\scripts\verify-library.py"
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
- `agent-browser` 当前未安装；页面验收仍可使用当前 Agent 的浏览器能力，但跨机器一致性需要补齐安装。
- 全局指令目前只分发给 Codex；20 个技能在共享目录中，但各 Agent 的逐项勾选不同。
- 不启用工程编排 Hook 和子代理；主代理负责判断、执行和交付。

## 永不入库

- API 密钥、令牌、认证头；
- 数据库连接串和密码；
- 浏览器登录态与订阅凭据；
- WebDAV/S3/GitHub 同步密码和 passphrase；
- 生产数据、个人数据、完整隐私日志；
- 运行时缓存、`__pycache__`、编辑备份和 `*.magpie-backup`。
