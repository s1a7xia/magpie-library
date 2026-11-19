# 技能选型与交付闭环

更新日期：2026-11-19。本文记录当前 19 个技能的取舍依据和最短交付路线，不代替项目授权。

## 当前结论

- **唯一入口**：Magpie 资源库。
- **唯一安装位置**：`~/.codex/skills`，全部为指向 Magpie 的 Junction。
- **技能总数**：19 个。
- **隐式触发**：3 个，`ruoyi6`、`database-design`、`grill-with-docs`。
- **显式调用**：16 个，只有用户点名才进入。
- **调用方式**：统一使用短名，如 `$wayfinder`、`$to-spec`、`$code-review`。
- **不再使用**：Codex 插件副本、`mattpocock-skills-zh` 命名空间、`magpie-skills` 聚合路由。

技能存在不等于已经加载；规则里写了“应先读取”也不等于模型每轮必然执行。最终以本轮实际读取的 `SKILL.md` 为准。

## 从需求到产品交付

```text
新项目 / 新模块
  -> 读项目 AGENTS.md、仓库、调用链、Git、状态文档和已有术语/ADR
  -> Default 模式澄清目标、角色、核心流程、数据对象、复用能力、
     非目标、验收人、明确授权
  -> Plan 模式收敛模块边界、页面/菜单/路由、API、权限、状态、
     数据对象、验收标准、首批切片

已有项目的明确任务
  -> 读项目事实和当前授权

按复杂度选择最短路径
  ├─ 目标、验收、修改点清楚
  │    -> 直接实现，不强制创建 PRD、spec 或 tickets
  ├─ 单会话内存在会改变结果的真实歧义
  │    -> grill-with-docs
  └─ 大型、跨会话、关键未知互相阻塞
       -> $wayfinder 建决策地图
            ├─ 外部事实不明：$research
            ├─ 必须看 UI/行为效果：$prototype
            └─ 业务决策/术语未定：$grilling + $domain-modeling

涉及持久化对象、字段、关系、状态、唯一性、生命周期、删除/历史、
JSONB 或迁移
  -> database-design 先形成数据契约

需要核对框架落点和复用边界
  -> ruoyi6 对照仓库确认真实实现位置

方案已收敛，需要持久记录
  -> $to-spec 固化可验收规格

存在多个可独立验收的纵向切片或真实阻塞依赖
  -> $to-tickets

实现
  ├─ 默认：当前 Codex 会话直接实现
  └─ 涉及 RuoYi 代码时叠加 ruoyi6

验证与交付
  -> 按当前任务授权执行最小验证并记录证据
  -> 仅明确要求时 $code-review
  -> 预发布、UAT、生产发布、客户验收是独立审批门
```

这张图的重点不是“每个任务都走完全程”，而是每一跳都只在有实际需要时发生。简单改动直接实现；大型工作才需要决策地图、规格和拆票。

## 技能分层

### 隐式触发：3 个

这三项由 `instructions/codex.md` 明确要求，模型在当前场景应先读取对应 `SKILL.md`：

| 技能 | 触发条件 | 作用 |
|---|---|---|
| `ruoyi6` | 修改 RuoYi-Vue-Plus 的 `ruoyi-modules/ruoyi-*` 后端，或 `plus-ui-React/src` 对应页面、API、类型、路由、菜单、组件前 | 核对真实复用点、后端分层、BO/VO、前端链路、权限、字典、菜单和增量 SQL |
| `database-design` | 讨论或修改持久化对象、表、字段语义、归属、关系、状态、唯一性、生命周期、删除/历史、JSONB、迁移时 | 先确认数据契约，避免在规格或实现中臆造模型 |
| `grill-with-docs` | 单会话内存在会改变结果的真实歧义时 | 持续追问并沉淀领域术语和 ADR；目标与验收明确则直接实现 |

这三项是“优先读取”，不是确定性 hook，也不能替代对项目事实的核对。

### 需求与决策：7 个显式技能

| 技能 | 作用 | 何时使用 |
|---|---|---|
| `$ask-matt` | 路径不清时选择最短可靠路线 | 用户明确要求导航，或方案阶段确实无法判断下一步 |
| `$triage` | 对外部 Issue/PR 分类、补证据、形成 agent-ready brief | 已有外部需求池需要整理；不处理刚由 `$to-tickets` 产出的票 |
| `$wayfinder` | 为单个会话装不下的大型工作建立决策地图和 decision tickets | 跨会话、多未知互相阻塞；只规划路线，不直接交付功能 |
| `$grilling` | 用设计树和 frontier 对计划、设计或想法做压力测试 | 需要深挖决策，不一定需要写文档 |
| `$domain-modeling` | 统一领域语言、边界、生命周期，沉淀词汇表和 ADR | 术语或边界不稳定，后续规格会因此反复 |
| `$research` | 用一手来源补齐外部事实 | API、框架版本、第三方能力、规范事实未明 |
| `$prototype` | 用一次性样品验证 UI、状态模型或业务逻辑 | 纸面讨论无法判断效果 |

### 规格、实现与交付：9 个显式技能

| 技能 | 作用 | 何时使用 |
|---|---|---|
| `$to-spec` | 把已确认内容合成为可验收规格，不做新访谈 | 需要持久记录、交接、复杂变更或多轮实现 |
| `$to-tickets` | 拆成带阻塞关系的纵向交付切片 | 存在多个可独立验收的切片或真实依赖 |
| `$code-review` | Standards + Spec 双轴只读审查 | 用户明确要求审查；调用即授权两个并行只读审查子代理 |
| `$retro` | 复盘一次会话并改进 agent 环境 | 用户明确要求复盘 |
| `$handoff` | 生成可携带的跨会话交接文档 | 要换 harness、目录、同事或阶段中途分叉 |
| `$setup-matt-pocock-skills` | 配置 tracker、triage labels 和领域文档布局 | 大型或多阶段项目首次进入 spec/ticket 流程前 |
| `$writing-for-agents` | 编写技能、`AGENTS.md` 等 agent 文档 | 用户明确要求维护 agent 指令或技能 |
| `$frontend-design` | 深度视觉设计 | 用户明确要求页面美化、整页改版或明确视觉方向 |
| `$answer-me-with-html` | 生成视觉解释页 | 用户明确要求可视化说明 |

## 为什么保留这 19 个

| 目标 | 保留能力 |
|---|---|
| 需求不清楚，但一个会话能问清 | `grill-with-docs` + `$grilling` + `$domain-modeling` |
| 工作跨会话，关键未知互相阻塞 | `$wayfinder` |
| 外部事实不明确 | `$research` |
| 必须看效果才能决策 | `$prototype` |
| 从讨论进入可验收规格 | `$to-spec` |
| 从规格进入可独立验收的交付顺序 | `$to-tickets` |
| 项目第一次建立规格/票务和领域文档约定 | `$setup-matt-pocock-skills` |
| 默认实现和 RuoYi 技术规范 | 当前会话 + `ruoyi6` |
| 数据模型不被顺手臆造 | `database-design` |
| 明确要求时的质量审查 | `$code-review` |
| 明确要求时的复盘、交接和文档维护 | `$retro`、`$handoff`、`$writing-for-agents` |
| 外部需求池整理 | `$triage` |
| 路径导航和视觉支撑 | `$ask-matt`、`$frontend-design`、`$answer-me-with-html` |

## 刻意不纳入

| 能力 | 不纳入原因 |
|---|---|
| `tdd` | 当前工作流不默认授权测试；需要 TDD 时按项目测试规范直接执行，不常驻技能。 |
| `diagnosing-bugs` | 困难缺陷按项目规则定位根因，必要时用 `$research` 或 `$prototype` 获取证据。 |
| `codebase-design` | 当前任务按通用设计原则和项目现有架构处理。 |
| `improve-codebase-architecture` | 不把架构巡检设为日常前置步骤。 |
| `pr` | PR 正文按项目现有模板直接编写。 |
| `grill-me` | 与 `$grilling`、`grill-with-docs` 重叠，避免多个入口误路由。 |
| `wizard` | 生成 bash 向导，不符合当前 Windows/PowerShell 主环境。 |
| `teach`、`wait-what`、`to-questionnaire` | 非默认工程交付链路，低频需求直接处理。 |
| `claude-handoff`、`loop-me` | 与当前 Codex 连续交付模型不匹配或属于未完成能力。 |
| `in-progress/*` | 作者明确标为未完成，不能作为可靠交付基础设施。 |
| `misc/*` | 面向特定编辑器或项目脚手架，不构成通用闭环。 |
| `api-regression` | 登录方式属于项目/agent 事实，不再单独维护技能；接口验证按当前任务授权直接执行。 |

## 维护

- 修改任何技能都编辑 Magpie 资源库 `skills/<name>/`，再执行 `magpie library sync`。
- `implement` 和 `implement-spec` 已删除，不再提供；实现由当前 Codex 会话直接完成，不增加独立实现入口、实现子代理或 worktree 编排层。
- 公开仓库只保留同一份 `skills/`，不再镜像 Codex 插件目录。
- 新会话统一使用短名调用，例如 `$wayfinder`，不再使用 `$mattpocock-skills-zh:wayfinder`。
- 新增或删除技能时，同时更新 `~/.config/magpie/library.json`、本文、README、脱敏快照和公开镜像。
- 上游来源和许可见 [THIRD-PARTY.md](THIRD-PARTY.md)。
