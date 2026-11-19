# 技能选型与交付闭环

更新日期：2026-11-19。本文记录当前技能集合的取舍依据，不代替项目授权。

## 当前结构

```text
新项目 / 重大新模块
  -> 产品发现（Default；Plan 可选）
  -> 事实基线
已有项目明确任务
  -> 事实基线

任何阶段涉及持久化对象 / 字段 / 关系 / 状态 / 唯一性 / 删除 / 迁移
  -> database-design：进入 $mattpocock-skills-zh:to-spec 前确认数据契约

需求收敛
  ├─ 小而明确：直接实现
  ├─ 会话内真实歧义：grill-with-docs
  └─ 大型、跨会话、未知互相阻塞：建议 $mattpocock-skills-zh:wayfinder
       ├─ 外部事实未明：research
       ├─ 设计需要看效果：prototype
       └─ 业务决策/术语：grilling + domain-modeling

规格与切片
  -> 大型/多阶段项目首次 spec/ticket 流程：建议 $mattpocock-skills-zh:setup-matt-pocock-skills（用户确认后配置）
  -> $mattpocock-skills-zh:to-spec：需要可验收规格、交接或复杂变更
  -> 多个纵向切片或真实依赖：建议 $mattpocock-skills-zh:to-tickets（用户确认后）
  -> 小改 / 单切片：跳过规格和拆票

实现 -> 按授权验收
  -> 默认当前会话实现；仅 RuoYiPlus 叠加 ruoyi6
  -> 仅明确要求时 $mattpocock-skills-zh:implement-spec
  -> $mattpocock-skills-zh:code-review / $mattpocock-skills-zh:retro：用户明确要求时
```

不是每个任务都必须走完整流程。只有 `grill-with-docs` 可由模型按技能 description 隐式选择；`ask-matt`、`triage`、`wayfinder`、`grilling`、`domain-modeling`、`research`、`prototype`、`to-spec`、`to-tickets`、`setup-matt-pocock-skills`、`implement-spec`、`code-review`、`retro`、`handoff`、`writing-for-agents` 全部由元数据限制为显式调用，必须由用户点名完整技能名后进入。当前全局指令只补充 `ruoyi6`、`database-design`、`grill-with-docs` 三条优先触发路径；它们不是确定性 hook，实际以本轮读取的 `SKILL.md` 为准。

插件技能必须带命名空间，例如 `$mattpocock-skills-zh:wayfinder`、`$mattpocock-skills-zh:to-tickets`；只写 `$wayfinder` 不会加载插件技能。`grill-with-docs` 虽可自动匹配，也支持 `$mattpocock-skills-zh:grill-with-docs` 显式调用；它内部通过相对路径读取 `grilling` 与 `domain-modeling`，不依赖这两个技能被隐式选中。

## 载体

- **Codex 插件**：`mattpocock-skills-zh`，来源为中文翻译仓库 `vinvcn/mattpocock-skills-zh-CN`。运行安装在 Codex 插件缓存；公开镜像位于 `plugins/mattpocock-skills-zh/`。
- **Magpie 直接分发**：`ruoyi6`、`database-design`、`frontend-design`、`answer-me-with-html` 全部直接暴露在 `~/.codex/skills`；`ruoyi6` 和 `database-design` 按场景优先触发，`frontend-design` 和 `answer-me-with-html` 仅在用户点名时进入；不使用 `magpie-skills` 聚合路由。
- **Matt 中文插件**：16 个流程技能独立加载，不与 Magpie 本地技能重复；只有 `grill-with-docs` 可隐式选择，其余 15 个必须由用户显式点名。

## 中文插件：16 个

### 需求与决策

| 技能 | 作用 | 默认边界 |
|---|---|---|
| `ask-matt` | 路径不清时选择最短可靠路线 | 显式导航；不替代 Codex 自带路由 |
| `triage` | 外部 Issue/PR 的分类、证据核验和 brief | 未授权时只读分析并输出本地草案 |
| `wayfinder` | 大型跨会话工作的决策地图与 decision tickets | 默认本地 `.scratch/<effort>/`；research ticket 可启只读调查子代理；外部 tracker 另授权 |
| `grill-with-docs` | 单会话内持续追问，沉淀术语和 ADR | 需要用户真实参与；不替代事实研究 |
| `grilling` | 设计树、frontier 和逐轮追问方法 | 由上层流程读取，也可独立使用 |
| `domain-modeling` | 统一领域语言、边界、生命周期和 ADR | 领域文档写入受当前任务授权约束 |

### 证据与规格

| 技能 | 作用 | 默认边界 |
|---|---|---|
| `research` | 用一手来源补齐决策事实 | 调用即启后台调研子代理，主会话继续推进 |
| `prototype` | 用一次性样品回答 UI/状态/逻辑问题 | 默认保留本地工件；不自动提交或 push |
| `to-spec` | 把已确认内容合成为可验收 spec | 默认项目内 Markdown；外部发布另授权 |
| `to-tickets` | 拆成带 blocking edges 的纵向切片 | 默认本地每票一个文件；远端另授权 |
| `setup-matt-pocock-skills` | 配置 issue tracker、triage labels 和领域文档布局 | 默认 Local markdown，不创建状态文档，不擅自改 remote/label |

### 实现、审查与交付

| 技能 | 作用 | 默认边界 |
|---|---|---|
| `implement-spec` | 按 spec 和 task graph 实现 | 调用即授权隔离 worktree 的实现/合并子代理及任务分支本地提交；push、PR、测试另授权 |
| `code-review` | Standards + Spec 双轴审查 | 显式技能；调用即授权两个并行只读审查子代理，不能并行时串行降级 |
| `retro` | 复盘一次会话并改进 agent 环境 | 只提改进候选，不擅自扩大改动 |
| `handoff` | 生成跨会话/跨目录交接文档 | 只在确需可携带交接时使用 |
| `writing-for-agents` | 编写技能、AGENTS.md 等 agent 文档 | 不替代项目规则 |

## Magpie 本地技能：4 个

| 技能 | 作用 |
|---|---|
| `ruoyi6` | RuoYi-Vue-Plus 6.x + plus-ui-React 的实现规范 |
| `database-design` | 持久化模型准入、约束、生命周期和迁移契约 |
| `frontend-design` | 用户明确要求深度视觉设计时叠加 |
| `answer-me-with-html` | 用户明确要求视觉解释页时使用 |

这 4 个技能仍在 Magpie 资源库中维护；16 个 Matt 中文技能的运行载体仍是 Codex 插件，公开仓库只保留一份只读镜像，避免在 Magpie 形成同名双份。4 个本地技能全部直接暴露在 `~/.codex/skills`；`ruoyi6`、`database-design` 由全局指令优先触发，`frontend-design`、`answer-me-with-html` 只在用户点名时进入。不使用 `magpie-skills` 聚合入口。API 回归的执行约束已收敛到全局 `instructions.md` 与 Codex 补充 `instructions/codex.md`，不再单独维护技能。

## 刻意不纳入

| 能力 | 不纳入原因 |
|---|---|
| `tdd` | 当前工作流不默认授权测试；需要 TDD 时按项目测试规范手工执行，不额外常驻技能。 |
| `implement` | 默认串联测试、审查和提交，与当前授权边界冲突；默认实现由 Codex 直接完成。 |
| `diagnosing-bugs` | 不使用未选技能；困难缺陷按项目规则定位根因，必要时用 `research` 或 `prototype` 获取证据。 |
| `codebase-design` | 未选；需要深模块词汇时在当前任务中按通用设计原则分析。 |
| `improve-codebase-architecture` | 未选；不把架构巡检设为日常前置步骤。 |
| `pr` | 未选；PR 正文按项目现有模板直接编写，不增加额外技能。 |
| `grill-me` | 与 `grilling` / `grill-with-docs` 重叠，避免多个入口误路由。 |
| `wizard` | 生成 bash 向导，不符合当前 Windows/PowerShell 主环境。 |
| `teach`、`wait-what`、`to-questionnaire` | 非默认工程交付链路，低频需求直接处理。 |
| `claude-handoff`、`loop-me` | 与当前 Codex 连续交付模型不匹配或属于未完成能力。 |
| `in-progress/*` | 作者明确标为未完成，不能作为可靠交付基础设施。 |
| `misc/*` | 面向特定编辑器/项目脚手架，不构成通用工程闭环。 |

## 维护

- Matt 中文技能只维护在插件源目录；更新翻译仓库后，提升插件版本并重新安装。
- 修改本地技能时编辑 Magpie 资源库 `skills/<name>/`，再执行 `magpie library sync`。
- 公开仓库 `skills/` 保留当前 4 个 Magpie 本地技能，`plugins/mattpocock-skills-zh/` 保留 16 个插件技能的只读镜像；运行安装仍以 Codex 插件缓存为准，不能直接编辑公开镜像来生效。
- 技能存在不等于当前会话已加载；插件已启用也不等于业务、MCP 或外部系统已验收。
