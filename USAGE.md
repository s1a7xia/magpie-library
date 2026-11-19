# 当前工作流机制与日常用法

更新日期：2026-11-19。这是使用说明，不替代项目授权。

当前主线是 **Magpie + Codex**：Magpie 负责全局规则、技能和 MCP 的配置分发，Codex 负责从需求到交付验收的完整开发闭环。Alma 作为独立应用自行使用，不属于这套开发团队。

## 0. 只需记住三句话

1. **日常开发直接向 Codex 说目标**，不用先选 Agent、MCP 或 Skill。
2. **要连续交付就说**：`按闭环做：<目标>。验收：<能观察到的结果>。` 运行测试和页面检查仍要在当次明确要求。
3. **需求、设计、代码、文档和 Git 都在 Codex 当前项目中完成**；不要把项目事实搬进全局规则。

完整任务示例：

```text
按闭环做：给主机列表增加负责人筛选。验收：管理员可按负责人筛选，
清空后恢复全量，普通角色仍只看到授权组织数据；完成相关测试、页面验证
和受影响文档，按项目规则处理 Git。
```

Codex 会先读代码、写出简短的需求摘要与验收项；只有会改变结果的问题才问你。之后连续完成实现、授权范围内验证、修复、文档和 Git 收尾，不再逐阶段等你确认。新增表、扩大权限、不可逆写库、部署/发布仍单独授权。

## 1. 各层只负责一件事

| 层 | 唯一职责 | 在哪里维护 |
|---|---|---|
| Magpie | 全局指令、模型、MCP、Skills 的配置源 | `~/.config/magpie/library/` |
| 项目 `AGENTS.md` | 该项目技术栈、真实命令、项目授权和特殊边界 | 项目根目录 |
| MCP | 搜索、数据库、Git 托管、SSH、图片、浏览器等执行能力 | Magpie 托管，Codex 通过 Magpie Hub 使用；宿主内置工具另算 |
| Skills | 按任务加载的方法和检查清单 | 4 个本地技能直接暴露，其中 `ruoyi6`、`database-design` 优先触发，`frontend-design`、`answer-me-with-html` 显式调用；16 个 Matt 中文技能由 Codex 插件提供，仅 `grill-with-docs` 可隐式选择 |
| Codex | 唯一默认开发者、文档写入者和 Git 收尾者 | 当前项目会话 |

项目事实、PRD、决策和验证证据留在项目内，不复制到全局规则，也不另建跨项目控制台账。共享指令只描述工程边界；通用工程阶段使用 Matt Pocock 的中文插件技能，`$mattpocock-skills-zh:ask-matt` 只在 Codex 说明需要后由用户确认进入，不替代 Codex 自带技能匹配。大型、跨会话或多阶段项目复用一份状态记录，见 [README.md](README.md#项目状态文档)。

## 2. 按任务选择最短路径

| 你怎么说 | Codex 怎么做 |
|---|---|
| “把这个按钮文案改一下” | 读相关代码，最小修改，核对 diff；未授权不额外跑构建 |
| “排查这个接口 500 并最小修复” | 先定位根因，再修直接受影响路径；测试按当前授权执行 |
| “按闭环做：……。验收：……” | 在当前授权内连续实现、核对、审查和收尾；未另明确测试或运行验收时，不把静态核对写成运行通过 |
| “先整理需求，不改代码” | 输出需求、边界、验收项和未决问题，然后停止 |
| “这个方案我还没定，先分析” | 按需进行需求与方案收敛；PRD、Issue 和切片按项目已有记录决定 |

任务清楚时不需要手动指定技能。大型、跨会话或多阶段项目在首次使用 spec/ticket 流程前，先建议并确认 `$mattpocock-skills-zh:setup-matt-pocock-skills`；它配置 issue tracker、triage labels 和领域文档布局，不创建状态文档。`triage`、`retro`、`handoff` 同样按显式技能处理，只在对应场景下建议。小项目和小改动不强制初始化。

RuoYi 项目从原始需求进入时，先以当前仓库为事实基线盘点作者框架和相邻模块的复用能力，将功能切片区分为复用、配置/扩展、新开发；同时明确首个可交付主干的功能结构、页面/菜单/路由、API、字典/参数、权限、数据及验收。需求或方案未收敛时按需用计划模式和 `grill-with-docs`；讨论到持久化对象、字段、一行语义、归属、状态、关系、唯一性、删除/历史或 JSONB 时，需求阶段就加载 `database-design`，在规格进入实现前确认数据契约。方案定稿且需要持久记录时使用 `$mattpocock-skills-zh:to-spec`；存在多个可独立验收的纵向切片或真实依赖时，先建议 `$mattpocock-skills-zh:to-tickets`，用户确认后再拆。简单单次改动跳过完整 PRD 和任务拆分。进入 RuoYi 代码实现由 `ruoyi6` 承接；明确要求审查或 API/页面验收时才调用对应技能。

流程导航与阶段入口是插件提供的 `ask-matt`、`triage`、`wayfinder`、`grill-with-docs`、`grilling`、`domain-modeling`、`research`、`prototype`、`to-spec`、`to-tickets`、`implement-spec`、`code-review`、`retro`、`setup-matt-pocock-skills`、`handoff` 和 `writing-for-agents`；业务规范是本地的 `ruoyi6`、`database-design`、`frontend-design`，展现支撑是 `answer-me-with-html`。这 4 个本地技能全部直接暴露；不使用 `magpie-skills` 聚合层。未选技能（如 `tdd`、`implement`、`diagnosing-bugs`、`codebase-design`、`pr`）不在当前集合中，不能把它们当作可调用能力。

技能可见性由插件/本地技能元数据决定，不是路径 hook。当前只有 3 条优先触发：RuoYi 代码读取 `ruoyi6`、持久化模型讨论读取 `database-design`、单会话真实歧义读取 `grill-with-docs`。其余 15 个插件技能和 `frontend-design`、`answer-me-with-html` 均由 `allow_implicit_invocation: false` 限制为显式调用，不会出现在模型的隐式技能列表。写在规则里不等于执行时必然加载，最终以本轮实际读取的 `SKILL.md` 为准。

显式调用插件技能要写完整命名空间：`$mattpocock-skills-zh:wayfinder`、`$mattpocock-skills-zh:research`、`$mattpocock-skills-zh:to-spec`。本地技能直接写 `$ruoyi6`、`$database-design`、`$frontend-design`、`$answer-me-with-html`。

`$mattpocock-skills-zh:wayfinder` 只用于大型、跨会话且决策互相依赖的工作。默认地图是 `.scratch/<effort>/wayfinder.md`，决策票据在其 `tickets/` 子目录；没有外部 tracker 授权时不会创建或修改 Issue。`$mattpocock-skills-zh:research` 使用后台调研子代理继续查证，`$mattpocock-skills-zh:prototype` 默认保留本地可丢弃产物，`$mattpocock-skills-zh:to-spec` 写 `.scratch/<feature-slug>/spec.md`，`$mattpocock-skills-zh:to-tickets` 写 `.scratch/<feature-slug>/issues/`。`grilling`、`research`、`wayfinder`、`implement-spec`、`code-review` 的子代理上限由各自 `SKILL.md` 定义；其他子代理、测试、提交、push 和发布仍需任务中的明确授权。

## 3. 闭环怎么验收

Codex 最终按三列交付：

| 验收项 | 实际证据 | 未验证边界 |
|---|---|---|
| 用户可观察的结果 | 测试/构建结果、真实页面路径、数据库只读证据或用户确认 | 未授权、环境不可用或未覆盖的情况 |

- 编译通过只证明构建成立，不证明页面或业务可用。
- MCP 已连接只证明工具可调用，不证明操作已获授权。
- Git 提交只证明版本状态，不证明功能已验收。
- 只有你明确要求页面运行检查时才使用浏览器；未要求时把页面行为标为未验证。无 UI 影响需经调用链确认后记 `N/A` 及理由。

普通任务由 Codex 自查。只有你明确要求 `$mattpocock-skills-zh:code-review` 时才进行规范与规格双轴审查；该请求本身就授权启动两个并行的只读 Standards/Spec 审查子代理，无需再确认。授权仅限只读审查，不允许修改、测试、提交、推送、部署或写外部系统；当前宿主无法并行时，才在当前会话串行完成两轴并明确标记为降级。审查发现的问题只在当前实现授权范围内修复，再复检受影响部分。

## 4. 权限和停止边界

| 动作 | 默认边界 |
|---|---|
| 阅读相关代码、调用链和项目文档 | 当前任务需要即可读取 |
| 修改代码、受影响文档 | 用户要求实现或闭环时执行 |
| 测试、构建、lint、类型检查、页面验证 | 用户明确要求测试、验收或运行验证时执行相关最小范围；“按闭环做”本身不授予测试权限 |
| 新增表、扩大权限、不可逆数据写入 | 说明影响并单独取得当前授权 |
| 提交、推送 | 按项目已有明确授权；混杂归属不明时停止并报告 |
| 合并、部署、发布、资金和凭证操作 | 单独授权，不因闭环或审查通过自动获得 |

一个工作区同一时间只有一个写入者，默认 Codex。子代理和审查上下文默认只读；缺证据就报告阻塞，不伪造完成。

## 5. 配置和换机

- 全局公共规则改 `instructions.md`，Codex 专属规则改 `instructions/codex.md`，再执行 `magpie library sync`。
- 本地技能修改直接改资源库 `skills/<name>/`；4 个本地技能都从 `~/.codex/skills` 直接读取，按任务需要手动打开对应 `SKILL.md`。Matt 中文技能修改插件源目录后，提升插件版本并重新安装。
- Codex 自带技能匹配负责第一层选择；路径不清时先说明为何需要 `$mattpocock-skills-zh:ask-matt`，用户确认后再进入。需要某个本地技能时，直接读取 `~/.codex/skills/<name>/SKILL.md`。
- 公开仓库镜像指令、4 个本地技能、16 个 Codex 插件技能、3 条已确认可公开的工程偏好、说明和脱敏快照；凭据、登录态、会话、未公开记忆、召回索引、运行元数据和私密配置仍由 Magpie 加密备份维护。
- 不要手改 Codex 的 Magpie 生成块。
- 项目 `AGENTS.md` 只补充项目约定，不复制全局流程。
- 换机恢复依赖、MCP 和凭据按 [DEPENDENCIES.md](DEPENDENCIES.md)；只拉 Git 仓库不等于能力已安装。

验证配置时至少运行：

```powershell
magpie library sync
python "$env:USERPROFILE\.config\magpie\library\scripts\verify-library.py"
magpie healthcheck
```

文件同步和结构检查通过，不等于模型在每个新会话必然加载正确 Skill，也不等于底层 MCP 或业务环境都可用；这些要按实际任务再验证。

## 6. 当前边界

当前开发团队只保留 Codex。Magpie 管配置分发；Codex 负责开发闭环。Alma 的会话、通知、审批、微信和 Herdr 能力由 Alma 自己维护；Alma 当前不接收 Magpie 的指令、技能或 MCP（`library.json` 与 Alma 的 `mcp.json` 已核对），也不参与本项目从需求到验收的交付。

项目状态只在大型、跨会话或多阶段项目中启用。`setup-matt-pocock-skills` 先建立 tracker 与领域文档约定；`docs/project-state.md` 由当前任务按需创建，已有状态文档或任务板就直接复用。不建立第二份状态源，也不要求小改动维护状态文档。Git 证明代码变化，业务验收仍需实际证据或用户确认。

本说明不宣称效率已被证明。评估方式应是真实任务的总耗时、有效缺陷和返工；如果发现某条规则没有改善结果，应删除或缩短它，而不是继续增加流程。
