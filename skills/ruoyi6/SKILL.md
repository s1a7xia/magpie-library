---
name: ruoyi6
description: "RuoYi-Vue-Plus 6.x 业务模块开发规范。按任务规模判定后，引导复用当前框架已有能力，再按需加载 Java 后端、React/Ant Design Pro 与可选集成规范。数据库建模、落表和迁移统一加载 database-design；用于实际 RuoYi-Vue-Plus 6.x + plus-ui-React 项目或项目明确选定的 ruoyi6 profile，不因通用 Java、React 或 PostgreSQL 任务自动套用。"
---

# RuoYi-Vue-Plus 6.x 业务开发

本技能是技术入口，不是一套每次都要走完的仪式。先判断任务规模，再从能力地图定位需要读的 reference；入口只保留路由、边界和少量硬规则，深度内容只在对应文件中维护一份。

先遵守入口协议的项目 profile 选择（含 `none`）。在适用范围内，任何会修改 RuoYi 代码或字段/API/权限契约的开发、修复或审查任务中都先加载本技能，不区分 Direct、`implement`、`debug` 还是 `review`。纯文档、只读规划或只读诊断且不修改代码时可不加载。

## 事实源与边界

技术事实以当前 checkout 为准：后端看根 `pom.xml` 和后端源码，前端看 `plus-ui-React/package.json` 和 React 源码。外部项目只提供组织角度和工程思路，不把固定提交、旧类名或外部文档当成当前事实。

当前作者基线约为 RuoYi-Vue-Plus 6.1.x、Spring Boot 4.x、Java 21、React 19、Ant Design 6；实际版本和依赖始终以项目构建文件为准，版本号不是兼容性承诺。前端只按 `plus-ui-React` 的 React/Ant Design ProComponents 实现。

普通业务模块默认依赖 `ruoyi-common`、`ruoyi-system` 和自身分层。工作流、AI、定时任务、MQTT、监控等只在需求确实需要时读取 [optional-integrations.md](references/optional-integrations.md)。

## 任务分级

| 级别 | 适用 | 执行方式 |
|---|---|---|
| **Direct** | 错字、样式微调、单文件小修、明确的局部改动 | 只读相关代码和对应 reference，直接修改并核对 diff；不建完整判型矩阵，不扩大范围。 |
| **Increment** | 现有模块的增量字段、接口、页面、权限 | 先读本次涉及一侧的现有契约和调用链，完成相关前后端联动；只执行与改动相关的复用和机制检查。 |
| **New Module** | 新业务模块、完整 CRUD、跨模块契约或验收口径不清 | 完成业务判型、机制判型、复用扫描、契约门，再选最小模板并形成完整闭环。 |

修改公共组件、公共方法或跨模块 API 时，按公共能力改动处理：先搜全部调用方，保持兼容，只验证受影响范围。任务分级不是跳过事实检查；只是让小改动不承担完整新模块的仪式。

## 能力地图

先按需求信号定位能力，再读对应 reference。不要在入口猜测 API，也不要把所有能力都预读一遍。

| 需求信号 | 先读 | 关键动作 |
|---|---|---|
| 新模块、CRUD、字段、表关系 | [database-design](../database-design/SKILL.md)、[backend.md](references/backend.md) | 数据库模型先加载唯一入口 `database-design`；再按本参考落 Java/前端源码。 |
| 单表查询、分页、联表、数据权限 | [backend.md](references/backend.md) | 先看 `BaseMapperPlus`、`QueryBuilder`、`LambdaQueryCondition`；按查询入口表选型。 |
| 事务、幂等、缓存、异步、并发、状态编排 | [capabilities.md](references/capabilities.md) | 命中信号才引入，说明选择理由和失败边界。 |
| 字符串、集合、对象、JSON、日期、树、文件、IP、SQL 工具 | [utils.md](references/utils.md) | 先找项目已有工具，使用前读当前方法签名。 |
| 用户、部门、角色、字典、参数、OSS、消息 | [backend.md](references/backend.md) | 跨模块能力走 `ruoyi-api`；不复制系统模块实现。 |
| 展示名称、翻译、脱敏、导入导出 | [backend.md](references/backend.md)、[author-patterns.md](references/author-patterns.md) | 先复用 `@Translation`、`ExcelBuilder` 和作者示例；需要新增翻译类型时看扩展入口。 |
| React 页面、API、类型、hooks、样式 | [frontend.md](references/frontend.md) | 按现有页面壳、公共组件和 hooks 组合；请求统一走 `@/api/request`。 |
| 新页面或布局调整 | [frontend.md](references/frontend.md) | 先按用户任务选页面形态并应用视觉基线；单表/树表才取对应模板，新业务页面登记动态路由。用户明确要求美化或深度改版时，可再叠加 `frontend-design`。 |
| 菜单、字典、参数 SQL、字段链路 | [database-design](../database-design/SKILL.md) | SQL、约束和迁移按唯一入口核对；菜单/权限源码链路按本技能核对。 |
| 工作流、任务、AI、监控 | [optional-integrations.md](references/optional-integrations.md) | 只在有当前验收标准时接入，区分同进程模块和独立服务。 |

需要按业务场景定位作者真实实现时读 [author-patterns.md](references/author-patterns.md)；需要完整后端骨架时读 [templates.md](references/templates.md)。

## 取样与复用

框架作者维护的 `ruoyi-system`、`ruoyi-demo`、`ruoyi-common-*` 和 `ruoyi-api` 是优先取样来源。`ruoyi-gen` 模板和 `plus-ui-React/gen` 只用于核对字段、注解和文件落点，不运行生成器，也不把生成结果当成事实源。

目标业务模块只用于确认已有字段、权限、路由和集成约束，不作为代码质量范本。不要因为相邻模块已有某种写法就机械复制；先确认它符合当前源码和本次业务契约。

New Module 在写文件前按以下顺序扫描，并在需要时列出实际复用入口和最小缺口：

1. 数据库：现有表、字典、参数、菜单和增量 SQL。
2. 后端：`ruoyi-api`、`ruoyi-common-*`、`ruoyi-system`、`ruoyi-demo`。
3. 前端：`plus-ui-React/src/components`、`hooks`、`utils`、`api`、`pages` 和现有页面壳。
4. 机制：按 [capabilities.md](references/capabilities.md) 检查事务、幂等、缓存、异步、并发、翻译和审计。

Direct 只沿直接受影响文件和调用方读取；Increment 只读本次涉及的数据库、后端、前端和机制，不为了“确认全貌”扩读无关模块。

能力接近但接口不完全适用时，优先扩展、组合或薄包装；不要新建第二套请求层、权限判断、字典、分页、上传、用户选择或流程实现。

## 业务契约门

新建模块或改变外部可见行为前，确认以下契约。能从 PRD、代码、SQL 或表结构回答的由 AI 自查，不反问用户：

| 契约 | 需要明确 |
|---|---|
| 主体与归属 | 业务对象是什么；归属由服务端确定还是允许选择，是否允许转移；关联对象是否可操作 |
| 可见范围 | 列表、详情、导出和批量操作分别受什么功能权限和数据权限约束 |
| 状态与生命周期 | 状态、触发者、合法迁移、终态和失败恢复 |
| 唯一与幂等 | 业务唯一键、重复提交、导入和外部回调如何识别 |
| 删除语义 | 物理删除、逻辑删除、归档还是保留历史；被引用时如何处理 |
| 历史与审计 | 哪些变化留痕、保留多久、是否需要版本或操作记录 |
| 并发与容量 | 锁、条件更新、分页、导出规模、索引和异步边界 |
| 集成边界 | 同步或异步、超时、重试、补偿和第三方字段隔离 |

普通单表不为了未来可能拆主从、预埋状态机或建立通用扩展表。业务口径未定时，先按当前业务最安全、最推荐的默认做法完整实现接口、页面、数据和反馈，并用固定格式 `TODO(待确认)` 记录“待确认什么 / 当前推荐实现 / 后续是否需要调整 / 找谁确认”；TODO 不阻塞当前切片，但不得留下空白按钮、半实现或跳过校验。不可逆动作或扩大权限的动作不擅自放开，停止受影响动作并报告。

## 实施闭环

### New Module

1. 从用户业务动作及成功/失败结果判业务形态和机制，再定位框架能力；提交、审批、执行、重试、统计等不强套增删改查。
2. 过业务契约门，确定表、字段、状态、唯一性、删除、权限、查询和集成边界。
3. 选择最小结构：单表参考 `TestDemo*`，树表参考 `TestTree*`；其它业务组合框架能力。新建 Maven 模块时另核对 [backend.md](references/backend.md) 的装配入口。
4. 写 DDL、字典、参数和菜单 SQL；项目未另行指定数据库时默认 PostgreSQL，并沿用当前脚本落点。
5. 按业务契约实现后端分层；普通单表骨架见 [templates.md](references/templates.md)，业务动作使用对应入参和 Service 方法。
6. 涉及页面创建或布局调整时按 [frontend.md](references/frontend.md) 选择页面形态、信息层级和视觉基线，再组合组件；单表/树表参考 [frontend-templates.md](references/frontend-templates.md)，报表、大屏、工作区不套 CRUD 布局。用户明确要求页面美化、深度视觉设计或整页改版时，再叠加 `frontend-design`；它不会替代本文件的组件与行为边界。纯 API/类型改动不加载设计技能。
7. 登记 `dynamicPage.tsx`，核对菜单 `component`、路由、权限字符和页面壳。
8. 过前后端联动门：路径、方法、响应、字段、权限、查询、导入导出和文件契约。
9. 页面可见改动完成后直接做真实浏览器检查；其它范围按目标执行最小验证。记录实现、验证、Git 独立状态，不把构建通过说成业务验收。

### Increment

只读本次实际涉及的 Controller、Service、Mapper、BO/VO、API、页面或数据库脚本，确认要补的字段、接口、交互或能力。跨层有依赖时补齐对应契约；保留已有复杂交互，不顺手重构，不复制相邻模块的整套实现。

### Direct

定位相关代码和一处必要 reference，完成最小修改；不需要输出完整业务判型矩阵。若修改公共方法、路由、请求层或权限标识，按 Increment 的联动检查处理。

## 前后端联动门

接口和页面必须作为同一条契约核对，不能一侧完成就宣布开发完成：

| 契约 | 后端 | 前端 |
|---|---|---|
| 路径与方法 | `@RequestMapping`、HTTP 方法和参数位置 | `src/api` 的 URL、`method`、`params`/`data` |
| 响应结构 | `R<T>`、`PageResult<T>` 的 `rows`/`total` | `Promise<R<T>>`、`res.data.rows`/`res.data.total` |
| 字段 | Entity/BO/VO，含必填、类型和可空性 | `types.ts` 的 `VO`/`Form`/`Query` 和页面字段 |
| 权限 | `sys_menu.perms` + `@SaCheckPermission` | `hasPermi(userInfo, [...])` 使用完全相同的权限字符 |
| 查询范围 | `PageQuery`、`params.begin*/end*`、排序白名单 | `toPageQuery`、`useDateRangeQuery`、`withTableSort` |
| 导入导出 | VO 注解、接口方法与文件流 | `useTableExport` / `download` / `Upload` |
| 文件与富文本 | OSS ID 字段和存储值 | `FileUpload`、`ImageUpload` 保存逗号分隔 OSS ID；`RichTextEditor` 使用 `oss://<ossId>` |

只检查本次业务实际需要的调用链。后台任务、回调或内部接口可以没有页面；只有本次范围需要的另一侧契约缺失时才列为未完成项。

## 硬规则

- 优先复用作者维护的实现和当前源码，不把生成器输出当作事实源。
- 后端固定 `Controller -> Service 接口 -> ServiceImpl -> Mapper`，不新增 DAO/Repository 层。
- Entity 只做持久化，BO 接请求，VO 做展示、翻译、脱敏和导出；不把 Entity 暴露给 Controller。
- 普通响应 `R<T>`，分页 `PageResult<T>`；业务阻断抛 `ServiceException`。
- 功能权限用 `@SaCheckPermission`；有数据归属和可见范围要求时使用 `@DataPermission`，列表、详情、更新和删除保持一致。两者不能互相替代。
- 前端请求只走 `@/api/request`，主键和关联 ID 用 `string | number`，雪花 ID 不丢精度。
- 新页面放 `src/pages/<module>/<business>/index.tsx`，请求和类型放 `src/api/<module>/<business>/`，并登记 `dynamicPage.tsx`。
- 复用 `PageContainer`、`ProTable`、`ModalForm`、`RowActions`、`DictTag`、`TreePanel`、选择器、上传组件和现有 hooks。
- 数据库模型、新表、关系、约束、索引和迁移只按 [database-design](../database-design/SKILL.md) 判断；本技能只负责 Java/React 分层和字段链路。
- 可枚举字典和运行期参数复用系统既有表；是否建业务表由 `database-design` 的复用准入决定。
- 权限字符在菜单 SQL、`@SaCheckPermission` 和 `hasPermi` 三处一致。
- 业务口径未定时按当前业务推荐做法完整实现，并用 `TODO(待确认)` 标注“待确认什么 / 当前推荐实现 / 后续调整点 / 找谁确认”；TODO 不是 `grill` 入口，也不能掩盖接口、页面、数据或编译未完成。

## 按需扩展

需要新增翻译实现时，先看 [backend.md](references/backend.md) 的翻译扩展边界；需要新增工具方法时，先看 [utils.md](references/utils.md) 和公共模块门槛；需要新增工作流条件装配时，先看 [optional-integrations.md](references/optional-integrations.md)。

## 交付检查

只在当前任务范围内检查：

- [ ] 任务级别和实际改动一致；Direct 没有扩成完整模块，New Module 没有漏掉契约或闭环。
- [ ] 已使用当前源码核实复用入口、方法签名、权限和返回结构。
- [ ] 新增字段或接口已完成数据库、后端、前端和菜单/权限联动。
- [ ] 新页面已登记 `dynamicPage.tsx`，没有绕过统一请求层。
- [ ] 业务未定项已按推荐做法完整实现，并留下“待确认什么 / 当前推荐实现 / 后续是否需要调整 / 找谁确认”的 TODO。
- [ ] 未运行的页面或运行检查明确标为“未验证”；未运行的检查不伪称通过。

输出按任务规模给结果：修改了哪些范围、实际复用入口、执行了什么构建、TODO 和未完成项；Direct 任务不必输出完整新模块报告。
