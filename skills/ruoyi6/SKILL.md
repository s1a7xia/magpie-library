---
name: ruoyi6
description: "RuoYi-Vue-Plus 6.x 业务模块开发规范。先判定任务与业务形态，扫描框架已有能力，再确定契约和最小实现；覆盖 Java 后端、React/Ant Design Pro 前端、PostgreSQL 数据建模与按需集成。用于 RuoYi 6.x + plus-ui-React 项目和全局默认技术 profile。触发：ruoyi6、RuoYi-Vue-Plus、若依Plus、plus-ui-React、React 页面、Java 业务代码、PostgreSQL、改字段、加接口、加页面、加权限。"
---

# RuoYi-Vue-Plus 6.x 业务开发

## 加载

| 任务 | 必读 |
|---|---|
| 任何业务模块或功能 | 本页 |
| 写或改 Java 后端 | [backend.md](references/backend.md) |
| 写或改 React 页面、API | [frontend.md](references/frontend.md) |
| 建表、改字段、写 SQL | [database.md](references/database.md) |
| 需要字符串、集合、转换、JSON、日期、树、文件、IP、SQL 工具 | [utils.md](references/utils.md) |
| 选事务、幂等、缓存、异步、并发、编排、序列、导出、审计 | [capabilities.md](references/capabilities.md) |
| 需要按作者源码改写的后端骨架 | [templates.md](references/templates.md) |
| 按业务场景定位作者真实实现 | [author-patterns.md](references/author-patterns.md) |
| 新建完整 React 单表/树表页面 | [frontend-templates.md](references/frontend-templates.md) |
| 工作流、定时任务、AI、监控 | 需求确实涉及才读 [optional-integrations.md](references/optional-integrations.md) |
| 消息、MQTT、搜索 | 按需；先查 `ruoyi-api` 和现有模块入口，不另造通用层 |

技能中的外部项目只贡献组织角度和工程思路。技术事实以当前 checkout 为准：后端看根 `pom.xml`，前端看 `plus-ui-React/package.json`，不把固定提交或外部文档当成当前事实。当前基线是 RuoYi-Vue-Plus 6.1.x + Spring Boot 4.x + Java 21 + React 19 + Ant Design 6；不要套用 Spring Boot 3 / JDK 17 或旧版前端写法。

绝大多数业务模块只依赖 `ruoyi-common`、`ruoyi-system` 和自身所在分层。工作流、AI、定时任务、MQTT、监控等是可选能力，不是业务模块前置依赖。

## 工程定位

```text
ruoyi-admin/                         启动与登录入口
ruoyi-api/                           跨模块接口和 DTO
ruoyi-common/                        公共技术能力；业务模块核心复用来源
ruoyi-modules/ruoyi-system/          用户、角色、部门、菜单、字典、参数、OSS
ruoyi-modules/ruoyi-<业务>/          业务模块；新增功能主要落点
ruoyi-modules/ruoyi-demo/            CRUD、树表、Excel 等框架示例；只做骨架参考
ruoyi-modules/ruoyi-gen/             生成模板；只查模板和字段映射，不运行生成器
ruoyi-modules/ruoyi-* 其它            工作流、AI、定时任务等按需能力
ruoyi-extend/                        独立进程：monitor-admin、snailjob-server、snailai-server
plus-ui-React/                       React 19 + TypeScript + Umi Max + Ant Design ProComponents
script/sql/                          框架初始化与升级 SQL；update/ 是框架升级脚本
项目登记的 SQL 目录                   业务增量 SQL；未登记时先确认落点，不假设固定路径
```

写代码前先读同模块 Controller、ServiceImpl、Mapper、BO、VO 和相邻 React 页面，确认现有接口和调用方式。目录存在不等于能力已启用；以当前源码、POM、配置、Bean 和调用链为准。

`ruoyi-workflow`、`ruoyi-ai`、`ruoyi-job` 与业务代码在同一个 Spring 进程内，通过 `ruoyi-api` 或现有 Bean 调用；`ruoyi-extend/` 下是独立服务，只能通过客户端、HTTP 或消息交互。业务模块默认不依赖它们。

### 取样优先级

按下列顺序确认框架写法；目标业务模块只用于查业务事实和集成约束，不用来证明代码模式正确：

1. `ruoyi-system` 的作者维护实现和 `ruoyi-demo` 的业务示例。
2. `ruoyi-common-*`、`ruoyi-api` 和 `plus-ui-React` 的公共 hooks、组件、工具。
3. `ruoyi-gen` 与 `plus-ui-React/gen` 模板，用于补充标准 CRUD 字段和文件落点。
4. 通用 Spring Boot / MyBatis-Plus / React / Ant Design 习惯。

## 任务判型

| 任务 | 最小做法 |
|---|---|
| 新建完整模块/CRUD | 业务判型 → 复用扫描 → 契约门 → 表/字典/菜单 → 后端 → React API/页面 → 动态路由登记 |
| 增量修改现有模块 | 先读现有契约和调用链，只补本次字段、接口、交互或能力 |
| 只补 API/types | 对齐已有后端 BO/VO 和当前 `request`/`types` 约定，不顺手改页面 |
| 修改公共能力 | 搜全部调用方，保持签名兼容；必要时编译受影响模块，不顺手重构 |
## 业务与机制判型

### 业务判型

| 形态 | 最小做法 |
|---|---|
| 普通单表 | 按 `demo/demo` 做列表、详情和编辑 |
| 树形分类 | 按 `demo/tree`，用 `parentId`、`TreeBuildUtils`、`ProFormTreeSelect`；先确认移动和删除子树规则 |
| 主从记录 | 主表承载主体；重复明细、关系约束或独立生命周期需要单独表达时拆子表，不为未来可能性预建 |
| 状态流转 | 显式状态、合法迁移、操作权限和失败恢复；变更走 Service |
| 审批业务 | 复用 `WorkflowService` 和 React workflow 组件，不另造审批引擎 |
| 只读报表 | 只做查询、聚合、导出和图表，不硬造增删改接口 |
| 导入/批处理 | 复用 `ExcelBuilder` 和现有 Upload/导入模式，明确幂等键、错误行反馈和部分失败策略 |
| 定时/异步任务 | 先复用 Job、SnailJob、消息和队列能力，业务表只存业务结果 |
| 外部接入 | 用独立连接器或适配器隔离协议、重试和第三方字段 |
| 纯配置/枚举 | 可变开关、阈值、周期用 `sys_config`；可枚举值用 `sys_dict_*` |

一个需求可以组合多种形态。选择能覆盖当前验收标准的最小组合，不提前搭平台。

### 机制判型

业务判型决定“做成什么形状”，机制判型决定“靠什么保障”。命中任一信号才读 [capabilities.md](references/capabilities.md)，不要自己写：

| 信号 | 该确认的事 |
|---|---|
| 一次请求写多处 | 是否需要事务，事务边界在哪 |
| 会被重复提交或重复投递 | 唯一约束、幂等表还是短时防重 |
| 高频读取或热点数据 | 先加索引/批量，再考虑缓存 |
| 响应慢、可延后 | 同步能否接受，用异步、队列还是定时 |
| 多人/多线程改同一数据 | 乐观锁、条件更新还是分布式锁 |
| 有多个状态和分支 | 状态字段、LiteFlow 还是工作流 |
| 需要业务单号或流水号 | 是否用 `SequenceUtils` |
| 列表要显示别的模块名称 | 用 `@Translation` 还是批量查询 |
| 涉及敏感或加密字段 | 展示脱敏、存储加密还是传输加密 |
| 有关键写操作 | 是否要 `@Log` 审计 |

没命中就不引入。

### 框架复用扫描

开始写文件前按顺序检查，并在输出中列出实际复用入口和缺口：

1. 数据库：现有表、字典、参数、菜单和增量 SQL，优先扩展已有对象。
2. 后端：`ruoyi-api`、`ruoyi-common-*`、`ruoyi-system`、`ruoyi-demo`。
3. 前端：`plus-ui-React/src/components`、`hooks`、`utils`、`api`、`pages` 和现有页面壳。
4. 模板：优先作者 demo；`ruoyi-gen/src/main/resources/fm/java`、`fm/react`、`fm/sql`、`fm/xml` 和 `plus-ui-React/gen` 只核对字段映射与文件落点。忽略 `fm/vue` 历史模板。

确认输入、返回值、权限、事务和异常行为适合当前场景后再调用。能力接近但接口不合用时，优先薄包装或扩展已有实现。不要仅凭类名或方法名记忆调用，使用前读当前源码确认签名。

**必须留下可核对的产出**。动手前写清：

```text
任务判型：<新建 / 增量 / 只补 API / 公共能力>
业务判型：<形态>；组合：<...>
机制命中：事务=<要/不要，理由>；幂等=<...>；缓存=<...>；异步=<...>；并发=<...>；其他=<...>
复用入口：<具体的类/组件/hook/接口>
缺口：<必须新写的最小部分>
```

没有明确理由就把某类标成“不需要”。跳过这段直接写 CRUD 视为未完成第一步。

## 业务契约门

建表和写 API 前至少明确下列事项。能从 PRD、代码、SQL 或表结构回答的，AI 自查，不把事实问题反问用户。

| 契约 | 必须明确 |
|---|---|
| 主体与归属 | 业务对象是什么，归属用户、部门、组织还是无归属 |
| 可见范围 | 列表、详情、导出、批量操作分别受什么功能权限和数据权限约束 |
| 状态与生命周期 | 有哪些状态、谁触发、允许哪些迁移、终态及失败恢复 |
| 唯一与幂等 | 哪个业务键不能重复；重复提交、导入或外部回调如何识别 |
| 删除语义 | 物理删除、逻辑删除、归档、注销还是保留历史；被引用时如何处理 |
| 历史与审计 | 哪些变化留痕、保留多久、是否需要版本或操作记录 |
| 并发 | 唯一约束、乐观锁、条件更新还是现有锁；冲突时如何反馈 |
| 查询与容量 | 搜索、排序、分页、导出规模、索引和是否异步 |
| 集成边界 | 同步或异步、超时、重试、补偿及第三方字段如何隔离 |

普通 CRUD 不强制新建 ADR；跨切片或长期有效的关键取舍才写入 ADR。没有明确业务规则时，不自行发明状态机、唯一键或删除策略。

## 本地参考实现

| 场景 | 优先参考 |
|---|---|
| 单表后端完整链路 | `ruoyi-demo` 的 `TestDemoController`、`TestDemoServiceImpl`、`TestDemoMapper`、`TestDemo`、`TestDemoBo`、`TestDemoVo` |
| 树表后端 | `TestTreeController`、`TestTreeServiceImpl`、`TestTreeMapper` |
| 单表 React 完整链路 | `plus-ui-React/src/api/demo/demo/{index,types}.ts`、`src/pages/demo/demo/index.tsx` |
| 树表 React | `src/pages/demo/tree/index.tsx` |
| 复杂页面 | `src/pages/system/user/index.tsx`、`src/pages/system/client/index.tsx` |
| Excel、导入、导出 | `TestDemoController.importData`、`TestExcelController`、`ExportDemoVo`；React 导入参考 `system/user/components/UserImportModal.tsx` |
| 生成器模板 | 后端 `ruoyi-gen/.../fm/java/`、`fm/xml/`，React 页面 `ruoyi-gen/.../fm/react/`，前端 `plus-ui-React/gen/`；只查结构，不运行生成器 |

框架示例和公共能力才是可复制模板。目标项目已有业务模块只用于确认字段、权限和集成约束，不复制其架构或页面实现。

## 改动定位

| 要改什么 | 必须同步的位置 | 先读哪里 | 验证 |
|---|---|---|---|
| 新增业务模块/CRUD | 契约/复用扫描 → 表/字典/菜单 → Entity、BO、VO、Mapper、Service、Controller → `types.ts`、`api/index.ts`、`pages/.../index.tsx` → `dynamicPage.tsx` | `TestDemo*`、`pages/demo/demo` | 后端编译 + 前端构建；页面另行验收 |
| 新增字段 | DDL → Entity → BO/VO → Mapper 查询条件 → React 类型 → 搜索、表格、表单、字典/Excel | 同表现有字段；同模块页面只核对字段、路由和权限 | 字段全链路一致，构建通过 |
| 新增接口 | Controller → Service 接口/实现 → Mapper → `api/index.ts` → `types.ts` → 页面调用 | 作者同类接口；当前模块契约只核对字段和集成约束 | 路径、权限、响应类型一致 |
| 新增/修改页面 | `pages/<module>/<business>/index.tsx`，必要时同目录子组件；请求放 `api/` → 登记 `dynamicPage.tsx` | 写法取 `pages/demo/demo`、`pages/demo/tree` 和公共组件 | 保留 Ant Design/ProComponents 组件和页面壳，构建通过 |
| 新增/修改权限 | `sys_menu.perms` → `@SaCheckPermission` → `hasPermi(userInfo, [...])` | 相邻菜单和角色授权 SQL | 三处权限字符完全一致 |
| 导入/导出 | VO 的 `@ExcelProperty`、`ExcelBuilder`、`importData`/`export`、React `useTableExport`/`download` | `TestDemoController.importData`、`TestExcelController`、`UserImportModal` | 导入模板、错误行提示、导出字段正确 |
| 字典/参数 | `sys_dict_type`、`sys_dict_data`、`sys_config` → `useDict`/`DictTag`/`dictOptions` 或配置读取 | 相邻字典、参数 SQL | 字典值、默认值、页面显示一致 |
| 修改公共组件/工具 | `components/common`、`hooks`、`utils` 或 `ruoyi-common-*` | 搜索全部调用方 | 至少编译受影响模块，不顺手重构 |
| 工作流、任务、消息、OSS、AI、搜索 | 对应 `ruoyi-modules/ruoyi-*`、`ruoyi-common-*`、`ruoyi-api` | 现有 Bean、配置和调用链 | 先复用，跨模块只依赖接口 |

登录与静态路由看 `plus-ui-React/src/pages/login.tsx`、`config/config.ts`；动态路由和菜单映射看 `src/pages/dynamicPage.tsx`、`src/stores/permissionStore.ts`、`src/utils/menu.tsx`；布局、页签和设置看 `src/layouts/BasicLayout.tsx`、`src/stores/{appStore,tagsViewStore}.ts`；请求、鉴权、加解密、权限看 `src/api/request.ts`、`src/utils/{auth,crypto,permission}.ts`；主题和页面样式看 `src/assets/styles/`。

## 前后端联动门

接口和页面必须作为一条契约同时核对，不能一侧完成就宣布开发完成：

| 契约 | 后端 | 前端 |
|---|---|---|
| 路径与方法 | `@RequestMapping`、HTTP 方法和参数位置 | `src/api` 的 URL、`method`、`params`/`data` |
| 响应结构 | `R<T>`、`PageResult<T>` 的 `rows`/`total` | `Promise<R<T>>`、`res.data.rows`/`res.data.total` |
| 字段 | Entity/BO/VO，含必填、类型和可空性 | `types.ts` 的 `VO`/`Form`/`Query` 和页面字段 |
| 权限 | `sys_menu.perms` + `@SaCheckPermission` | `hasPermi(userInfo, [...])` 使用完全相同的权限字符 |
| 状态与排序 | `changeStatus` / `updateSort` 入参和返回 | `Switch` / 排序控件及失败回滚 |
| 查询范围 | `PageQuery`、`params.begin*/end*`、排序白名单 | `toPageQuery`、`useDateRangeQuery`、`withTableSort` |
| 导入导出 | VO 注解、接口方法与文件流 | `useTableExport` / `download` / `Upload`，文件名和错误反馈 |
| 文件与富文本 | OSS ID 字段和存储值 | `FileUpload`、`ImageUpload` 保存逗号分隔 OSS ID；`RichTextEditor` 内容用 `oss://<ossId>` 标记 |

只后端或只前端时，仍检查另一侧现有契约是否已存在；不存在时明确列为未完成项，不假设另一侧会自动适配。

## 硬规则

- 第一要务是让业务模块形成**完整实现闭环**：接口、页面、菜单、权限和必要配置齐备。构建通过不代表服务已启动、页面已运行或权限已验收；这些由用户发起的 `page-acceptance` 确认。
- 业务口径不清晰时按“TODO 占位 + 当前业务下推荐的临时行为”推进，不阻塞无关功能。TODO 写明未决事项、临时方案理由和确认人；不可逆或可能扩大数据权限的动作不擅自放开。
- TODO 只用于“业务未定”，不能用于“功能未做”。数据没接、接口没写、页面没画、编译不过都属于未完成。
- 后端固定 `Controller -> Service 接口 -> ServiceImpl -> Mapper`，不新增 DAO/Repository 层。
- Entity 只做持久化，BO 接请求，VO 做展示、翻译、脱敏和导出；不把 Entity 暴露给 Controller。
- 普通响应 `R<T>`，分页 `PageResult<T>`（`total` + `rows`），业务阻断抛 `ServiceException`。
- 接口权限用 `@SaCheckPermission`；当前用户用 `LoginHelper`；对象转换用 `MapstructUtils`。
- 功能权限不等于数据权限。列表、详情、导出、批量操作必须遵守 `@DataPermission`。
- 前端请求只走 `@/api/request`，返回 `Promise<R<T>>`；页面读 `res.data.rows/total`，不引入 `AxiosPromise`。
- 页面固定 `src/pages/<module>/<business>/index.tsx`；请求和类型放 `src/api/<module>/<business>/`；新页面必须登记 `dynamicPage.tsx`。
- 主键和关联 ID 用 `string | number`，防止雪花 ID 在前端丢精度。
- 复用 `PageContainer`、`ProTable`、`ModalForm`、`RowActions`、`DictTag`、`TreePanel`、选择器、上传组件和现有 hooks，不复制。
- 新增能力前先证明现有能力不能满足；有同类能力时扩展、组合或薄包装，不 fork、不复制，不建第二套请求层、权限判断、字典、分页、上传、用户选择或流程实现。
- 跨模块读取用户、部门、角色、岗位、参数、消息、OSS、工作流等能力只走 `ruoyi-api`；不注入其他模块的 ServiceImpl、Mapper 或 Entity。
- 默认单表。主体下有可重复的结构化明细、需要关系约束，或子数据有独立查询边界、生命周期、权限、约束或数据量需求时拆子表；不为未来可能性预建。
- 状态、类型用 `sys_dict_*`；可变开关、阈值、周期用 `sys_config`；不为此建业务表。
- 权限字符在 `sys_menu.perms`、`@SaCheckPermission`、`hasPermi` 三处一致。
- 业务路径、包名、表前缀、权限前缀沿用项目登记；新业务不得混用框架 `/system` 命名或另起一套缩写。
- 不把生成器输出当作事实源；模板只用于确认字段命名、注解和文件落点。
- 后端不暴露 Entity，前端不改写后端字段；跨层字段名不一致时，在 BO/VO 边界修正。
- 已有复杂模块的树筛选、导入导出、列显隐、详情抽屉、分配页面和路由跳转必须保留；只做本需求范围内的增量修改。
- 不改需求范围外的代码；修改公共组件或公共方法前检查所有调用方。

## 实施闭环

1. 判任务、业务和机制，扫描已有能力，写下复用入口和缺口。
2. 过业务契约门，确定字段、状态、唯一性、删除、权限、查询和集成边界。
3. 选最小模板，确定表名、模块、业务名、主键、数据库/Java/TS 类型和权限前缀。
4. 写 DDL 和字典、参数、菜单 SQL；未指定新数据库选型时默认 PostgreSQL，并沿用当前脚本位置和方言。
5. 写 Entity、BO、VO、Mapper、Service 接口、ServiceImpl、Controller；列表分页，树表返回列表。
6. 写 `types.ts`、`api/index.ts`、`pages/<module>/<business>/index.tsx`；先查询、表格、分页，再弹窗、校验、提交。
7. 新建页面时登记 `dynamicPage.tsx`；核对菜单 `component`、权限字符和路由行为。
8. 接菜单和权限：目录 `M`、页面菜单 `C`、按钮 `F`；权限字符与后端注解、前端 `hasPermi` 一致。
9. 过前后端联动门，核对字段、路径、权限、查询、导入导出和文件契约。
10. 后端编译，前端构建；代码、菜单和权限配置完整后标 `Dev Complete`。页面可见改动交给用户发起 `page-acceptance`。
11. 收口前清点 TODO，确认没有把“没做完”伪装成 TODO。

普通单表以 `TestDemoController` 和 `pages/demo/demo/index.tsx` 为骨架，树表以 `TestTreeController` 和 `pages/demo/tree/index.tsx` 为骨架；两者签名和导出方法不同，不混用。业务有主从、状态、权限、导入、异步或外部接入时，先按 [author-patterns.md](references/author-patterns.md) 定位对应实现。

新增字段的最小链路是：`DDL -> Entity -> BO -> VO -> Mapper/查询条件 -> types.ts -> 页面查询/表格/表单 -> 字典或 Excel`。只改 Entity 和页面、不改 BO/VO 或 TS 类型属于未完成。

## 交付检查

- [ ] **实现闭环完整**：本次范围内的代码、菜单、权限和必要配置齐备，后端编译及前端构建通过。服务启动、页面可进入、权限实际生效和主路径运行结果只在 `page-acceptance` 后标为已验收。
- [ ] **TODO 已清点**：每条写明“没定什么 / 临时怎么做 / 找谁确认”，并登记到 `docs/agents/project-state.md` 或 PRD。
- [ ] 分层、命名和包路径符合本规范及项目登记约定。
- [ ] 已判定任务、业务形态，并扫描数据库、后端、前端和框架示例中的可复用能力。
- [ ] 已过机制判型，没有惯性套用或该用未用。
- [ ] 归属、状态、唯一性、删除、权限、并发和集成边界有明确依据。
- [ ] 字段在表、Entity、BO/VO、React 类型、页面标签和字典中一致。
- [ ] 分页、空集合、唯一性、事务、数据权限和权限字符已处理。
- [ ] 复用了现有组件、hooks、工具、跨模块 API 和公共能力；没有照抄业务模块或另造第二套实现。
- [ ] 已核对前后端路径、响应、字段、权限、查询、导入导出和文件契约。
- [ ] 新 React 页面已登记 `dynamicPage.tsx`，菜单、权限、API 和类型保持一致。
- [ ] 后端已编译，前端已构建；未做页面验收时明确写“开发完成、未验收”。
- [ ] 没把生成器或外部框架文档当作当前代码事实。

输出：加载的规范、参考的源码路径、复用项、实际构建、**TODO 清单**、未完成项。
