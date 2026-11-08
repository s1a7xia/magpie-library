---
name: ruoyi-6-vue
description: "RuoYi-Vue-Plus 6.x + Vue 3 业务模块开发规范。先判定业务形态并扫描框架已有能力，再确定业务契约和最小实现；规定 Java 后端分层与接口、plus-ui 页面与组件、数据库建模与 SQL。用于 RuoYi 6.x Vue 项目和全局默认技术 profile。触发：ruoyi-6-vue、RuoYi-Vue-Plus、若依Plus、plus-ui、Vue 页面、Java 业务代码、SQL、改字段、加接口、加页面、加权限。"
---

# RuoYi-Vue-Plus 6.x + Vue 开发规范

## 加载

| 任务 | 必读 |
|---|---|
| 任何业务模块或新功能 | 本页的“业务模块落地” |
| 写或改 Java 后端 | [backend.md](references/backend.md) |
| 写或改 Vue 页面、API | [frontend.md](references/frontend.md) |
| 建表、改字段、写 SQL | [database.md](references/database.md) |
| 写后端业务，需要字符串、集合、对象转换、JSON、日期、树、文件、IP、SQL 工具 | [utils.md](references/utils.md) |
| 新增完整 CRUD | 后端 + 前端 + 数据库 |
| 工作流、任务、消息、AI、MQTT 等 | 先查 `ruoyi-api` 和现有模块入口，不另造通用层 |

作者仓库的 `.codex/skills/ruoyi-plus-ai-coding` 与 `.codex/skills/frontend-crud-coding` 是外部参考，不直接加载。它们覆盖的规则已合并进本技能；若与本技能冲突，以当前项目真实代码和本技能为准。

## 工程定位

```text
ruoyi-admin/                 启动与登录入口
ruoyi-api/                   跨模块接口和 DTO
ruoyi-common/                公共技术能力
ruoyi-modules/ruoyi-system/  用户、角色、部门、菜单、字典、参数、OSS
ruoyi-modules/ruoyi-demo/    CRUD、树表、Excel、MQTT、MCP、ES 示例
ruoyi-modules/ruoyi-gen/     生成模板，只用于查漏，不运行生成器
ruoyi-modules/ruoyi-*/       其它模块；业务模块只用于了解集成约束，不作为模板
plus-ui/src/                 Vue 3 + TypeScript + Element Plus
script/sql/                  初始化 SQL
docs/sql/                    业务增量 SQL
```

写代码前先读同模块的 Controller、ServiceImpl、Mapper、BO、VO 和兄弟 Vue 页面，确认现有接口和调用方式。目录存在不等于能力已启用；以当前源码、POM、配置、Bean 和调用链为准。已有业务模块可以帮助理解集成边界，但不要复制其中的分层、命名、组件或公共能力实现。

### 取样优先级

出现冲突时按下列顺序取样，不拿“更通用”的写法覆盖项目已形成的强约定：

1. 目标模块内最近似的真实实现，以及它与前端 API、页面、权限的联动。
2. `ruoyi-common-*`、`ruoyi-api` 和当前项目公共 hooks、组件、工具的既有约定。
3. `ruoyi-gen` 后端模板和 `plus-ui/gen` 前端模板。
4. 通用 Spring Boot / MyBatis-Plus / Vue / Element Plus 习惯。

模板只补骨架和字段映射。目标模块已有数据权限、联表、缓存、导入导出、审批、树筛选或特殊交互时，增量扩展，不能回退成模板裸产物。

版本和依赖事实从当前 checkout 读取：后端看根 `pom.xml`，前端看 `plus-ui/package.json`。本技能不把某个固定补丁版本或提交号当作代码事实，代码变化后以实际文件为准。

## 业务模块落地

顺序固定为：**业务判型 -> 框架复用扫描 -> 业务契约门 -> 选择最小模板 -> 实现与编译 -> 前后端联动检查**。不要先套 CRUD 模板再倒推业务。

### 业务判型

| 形态 | 最小做法 |
|---|---|
| 普通单表 | 按 `demo/demo` 做列表、详情和编辑 |
| 树形分类 | 按 `demo/tree`，用 `parentId`、`TreeBuildUtils`、`TreePanel`；先确认移动和删除子树规则 |
| 主从记录 | 主表承载主体；子表只在有独立查询、生命周期、权限、约束或数据量时拆 |
| 状态流转 | 显式状态、合法迁移、操作权限和失败恢复；变更走 Service |
| 审批业务 | 复用 `WorkflowService` 和前端 `Process/*`，不另造审批引擎 |
| 只读报表 | 只做查询、聚合、导出和图表，不硬造增删改接口 |
| 导入/批处理 | 复用 `ExcelBuilder`，明确幂等键、错误行反馈和部分失败策略 |
| 定时/异步任务 | 先复用 Job、SnailJob、消息和队列能力，业务表只存业务结果 |
| 外部接入 | 用独立连接器或适配器隔离协议、重试和第三方字段 |
| 纯配置/枚举 | 可变开关、阈值、周期用 `sys_config`；可枚举值用 `sys_dict_*` |

一个需求可以组合多种形态，例如“主从 + 审批”或“树形分类 + 导入”。选择能覆盖当前验收标准的最小组合，不提前搭平台。

### 框架复用扫描

开始写文件前按顺序检查，并在输出中列出实际复用入口和缺口：

1. 数据库：现有表、字典、参数、菜单和增量 SQL，优先扩展已有对象。
2. 后端：`ruoyi-api` 跨模块接口、`ruoyi-common-*` 公共能力、`ruoyi-system` 系统能力、`ruoyi-demo` 框架示例。
3. 前端：`plus-ui/src/components`、`hooks`、`utils`、`api` 和页面壳。
4. 模板：优先 `ruoyi-demo` 的单表、树表和 Excel；`ruoyi-gen` 只核对字段映射和文件落点。

不能只看类名判断复用。确认输入、返回值、权限、事务和异常行为适合当前场景后再调用；能力接近但接口不合用时，优先薄包装或扩展现有实现。

### 业务契约门

建表和写 API 前，至少明确下列事项。能从 PRD、代码、SQL 或表结构回答的，AI 自查，不把事实问题反问用户。

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

普通 CRUD 不强制新建 ADR；跨切片或长期有效的关键取舍才写入 ADR，其余结论留在 PRD、`project-decisions.md` 或 SQL 注释中。没有明确业务规则时，不自行发明状态机、唯一键或删除策略。

### 选择最小模板

- 普通单表：`TestDemoController` + `views/demo/demo/index.vue`。
- 树表：`TestTreeController` + `views/demo/tree/index.vue`。
- 导入导出：`TestExcelController` + `ExportDemoVo` + demo 页面导出入口。
- 其它形态：先复用对应模块能力，只补业务自己的 Controller、Service、DTO 和页面。

模板只提供文件落点和调用方式，不是业务事实源。不要因为模板有某个字段、按钮或接口，就把它带进当前需求。

后端模板位于 `ruoyi-modules/ruoyi-gen/src/main/resources/fm/java/` 和 `fm/xml/`；前端模板位于 `plus-ui/gen/`。查找顺序是“同模块真实实现 -> 公共能力 -> 模板”；没有同类真实实现时才用模板生成骨架。只借鉴模板的字段、权限、导出、状态/排序和日期范围结构，最终代码必须符合当前项目的 hooks、组件和页面壳。

## 本地参考实现

| 场景 | 优先参考 |
|---|---|
| 单表后端完整链路 | `ruoyi-modules/ruoyi-demo/.../TestDemoController.java`、`TestDemoServiceImpl.java`、`TestDemoMapper.java`、`TestDemo.java`、`TestDemoBo.java`、`TestDemoVo.java` |
| 树表后端 | `TestTreeController.java`、`TestTreeServiceImpl.java`、`TestTreeMapper.java` |
| 单表前端完整链路 | `plus-ui/src/api/demo/demo/{index,types}.ts`、`plus-ui/src/views/demo/demo/index.vue` |
| 树表前端 | `plus-ui/src/views/demo/tree/index.vue` |
| Excel、导入、导出 | `TestExcelController.java`、`ExportDemoVo.java`、`demo/demo/index.vue` 的导出入口 |
| 生成器模板 | `ruoyi-modules/ruoyi-gen/src/main/resources/fm/`；只查模板和字段映射，不运行生成器 |

框架示例和公共能力才是可复制模板。目标项目已有业务模块只用于确认字段、权限和集成约束，不复制其架构或页面实现。没有同类框架示例时，单表以 `demo/demo` 为骨架，树表以 `demo/tree` 为骨架，不混用两者签名和导出方式。

## 改动定位

| 要改什么 | 必须同步的位置 | 先读哪里 | 验证 |
|---|---|---|---|
| 新增业务模块/CRUD | 契约/复用扫描 → 表/字典/菜单 → Entity、BO、VO、Mapper、Service、Controller → `types.ts`、`api/index.ts`、`views/<module>/<business>/index.vue` | `TestDemo*`、`views/demo/demo` | 后端编译 + 前端构建；页面另行验收 |
| 新增字段 | DDL → Entity → BO/VO → Mapper 查询条件 → 前端类型 → 搜索、表格、表单、字典/Excel | 同表现有字段和同模块页面 | 字段全链路一致，构建通过 |
| 新增接口 | Controller → Service 接口/实现 → Mapper → `api/index.ts` → `types.ts` → 页面调用 | 同模块相邻接口 | 路径、权限、响应类型一致 |
| 新增/修改页面 | `views/<module>/<business>/index.vue`，必要时同目录子组件；请求放 `api/` | 同模块 2–3 个兄弟页面 | 保留 Element Plus 组件和页面壳，构建通过 |
| 新增/修改权限 | `sys_menu.perms` → `@SaCheckPermission` → `v-hasPermi` / `checkPermi` | 相邻菜单和角色授权 SQL | 三处权限字符完全一致 |
| 导入/导出 | VO 的 `@ExcelProperty`、`ExcelBuilder`、`importData`/`export`、前端 `download` | `TestExcelController`、`ExportDemoVo` | 导入模板、错误行提示、导出字段正确 |
| 字典/参数 | `sys_dict_type`、`sys_dict_data`、`sys_config` → `useDict`/`DictTag` 或配置读取 | 相邻字典、参数 SQL | 字典值、默认值、页面显示一致 |
| 修改公共组件/工具 | `components/`、`hooks/`、`utils/` 或 `ruoyi-common-*` | 搜索全部调用方 | 至少编译受影响模块，不顺手重构 |
| 定位工作流、任务、消息、OSS、AI、搜索 | 对应 `ruoyi-modules/ruoyi-*`、`ruoyi-common-*`、`ruoyi-api` | 现有 Bean、配置和调用链 | 先复用，跨模块只依赖接口 |

登录、会话、动态路由看 `views/login.vue`、`permission.ts`、`store/modules/user.ts`、`store/modules/permission.ts`；布局、导航、页签、设置看 `layout/components/`、`store/modules/app.ts`、`store/modules/settings.ts`；请求、鉴权、加解密、权限判断看 `utils/request.ts`、`utils/auth.ts`、`utils/crypto.ts`、`utils/permission.ts`；主题和页面样式看 `assets/styles/tokens/`、`assets/styles/layout/`、`assets/styles/components/`。

## 前后端联动门

接口和页面必须作为一条契约同时核对，不能一侧完成就宣布开发完成：

| 契约 | 后端 | 前端 |
|---|---|---|
| 路径与方法 | `@RequestMapping`、HTTP 方法和参数位置 | `src/api` 的 URL、`method`、`params`/`data` |
| 响应结构 | `R<T>`、`PageResult<T>` 的 `rows`/`total` | `AxiosPromise<T>`、`res.data.rows`/`res.data.total` |
| 字段 | Entity/BO/VO，含必填、类型和可空性 | `types.ts` 的 `VO`/`Form`/`Query` 和页面字段 |
| 权限 | `sys_menu.perms` + `@SaCheckPermission` | `v-hasPermi` / `checkPermi` 使用完全相同的权限字符 |
| 状态与排序 | `changeStatus` / `updateSort` 入参和返回 | `el-switch` / 排序控件及失败回滚 |
| 查询范围 | `PageQuery`、`params.begin*/end*`、排序白名单 | 日期范围、分页、排序参数的字段名与格式 |
| 导入导出 | VO 注解、接口方法与文件流 | 上传/下载入口、文件名和错误反馈 |
| 文件与富文本 | OSS ID 字段和存储值 | `FileUpload`、`ImageUpload`、`Editor` 的 `ossId` / `oss://` 约定 |

只后端或只前端时，仍检查另一侧现有契约是否已存在；不存在时明确列为未完成项，不假设另一侧会自动适配。

## 硬规则

- 后端固定 `Controller -> Service 接口 -> ServiceImpl -> Mapper`，不新增 DAO/Repository 层。
- Entity 只做持久化，BO 接请求，VO 做展示、翻译、脱敏和导出；不把 Entity 暴露给 Controller。
- 普通响应 `R<T>`，分页 `PageResult<T>`（`total` + `rows`），业务阻断抛 `ServiceException`。
- 接口权限用 `@SaCheckPermission`；当前用户用 `LoginHelper`；对象转换用 `MapstructUtils`。
- 功能权限不等于数据权限。列表、详情、导出、批量操作必须遵守 `@DataPermission`。
- 前端请求只走 `@/utils/request`，返回 `AxiosPromise<T>`；页面读 `res.data.rows/total`。
- 页面固定 `views/<module>/<business>/index.vue`；请求和类型放 `api/<module>/<business>/`。
- 主键和关联 ID 用 `string | number`，防止雪花 ID 在前端丢精度。
- 复用 `Pagination`、`RightToolbar`、`DictTag`、`TreePanel`、选择器、上传组件和现有 hooks，不复制。
- 新增能力前先证明现有能力不能满足；有同类能力时扩展、组合或薄包装，不 fork、不复制，不建第二套请求层、权限判断、字典、分页、上传、用户选择或流程实现。
- 跨模块读取用户、部门、角色、岗位、参数、消息、OSS、工作流等能力只走 `ruoyi-api`；不注入其他模块的 ServiceImpl、Mapper 或 Entity。
- 默认单表。只有独立查询边界、生命周期、权限或数据量需要时才拆子表。
- 状态、类型用 `sys_dict_*`；可变开关、阈值、周期用 `sys_config`；不为此建业务表。
- 权限字符在 `sys_menu.perms`、`@SaCheckPermission`、`v-hasPermi` / `checkPermi` 三处一致。
- 业务路径、包名、表前缀、权限前缀沿用项目登记；新业务不得混用框架 `/system` 命名或另起一套缩写。
- 不把生成器输出当作事实源；模板只用于确认字段命名、注解和文件落点，最终代码按本规范、框架示例和当前项目登记约定写。
- 前端请求默认使用 `import request from '@/utils/request'`；不要写成命名导入。
- 后端不暴露 Entity，前端不改写后端字段；跨层字段名不一致时，在 BO/VO 边界修正，不在页面拼第二套映射。
- 已有复杂模块（如 user、role、workflow）的树筛选、导入导出、列显隐、详情抽屉、分配页面和路由跳转必须保留；只做本需求范围内的增量修改。
- 不改需求范围外的代码；修改公共组件或公共方法前检查所有调用方。

## 实施闭环

1. 判型并扫描已有能力，写下复用入口和缺口。
2. 过业务契约门，确定字段、状态、唯一性、删除、权限、查询和集成边界。
3. 选择最小模板，确定表名、模块、业务名、主键、数据库/Java/TS 类型和权限前缀。
4. 写 DDL 和字典、参数、菜单 SQL；确认数据库方言和现有脚本位置。
5. 写 Entity、BO、VO、Mapper、Service 接口、ServiceImpl、Controller；列表分页，树表返回列表。
6. 写 `types.ts`、`api/index.ts`、`index.vue`；先查询、表格、分页，再弹窗、校验、提交。
7. 接菜单和权限：新增目录/菜单用 `C`，按钮用 `F`；权限字符与后端注解、前端指令一致。
8. 过前后端联动门，核对字段、路径、权限、查询、导入导出和文件契约。
9. 后端编译，前端构建；页面可见改动只标 `Dev Complete`，交给用户发起 `page-acceptance`。

普通单表按 `TestDemoController` 和 `views/demo/demo/index.vue`；树表按 `TestTreeController` 和 `views/demo/tree/index.vue`。两者签名和导出方法不同，不混用。

新增字段的最小链路是：`DDL -> Entity -> BO -> VO -> Mapper/查询条件 -> types.ts -> 页面查询/表格/表单 -> 字典或 Excel`。只改 Entity 和页面、不改 BO/VO 或 TS 类型，属于未完成。

## 交付检查

- [ ] 分层、命名和包路径符合本规范及项目登记约定。
- [ ] 已判定业务形态，并扫描数据库、后端、前端和框架示例中的可复用能力。
- [ ] 归属、状态、唯一性、删除、权限、并发和集成边界有明确依据。
- [ ] 字段在表、Entity、BO/VO、TS 类型、页面标签和字典中一致。
- [ ] 分页、空集合、唯一性、事务、数据权限和权限字符已处理。
- [ ] 复用了现有组件、hooks、工具、跨模块 API 和公共能力；没有照抄业务模块或另造第二套实现。
- [ ] 已按“同模块真实实现 -> 公共能力 -> 模板 -> 通用习惯”取样，并保留目标模块的复杂增强。
- [ ] 已核对前后端路径、响应、字段、权限、查询、导入导出和文件契约。
- [ ] 后端已编译，前端已构建；未做页面验收时明确写“开发完成、未验收”。
- [ ] 没把生成器、外部框架文档或旧提交当作当前代码事实。

输出：加载的规范、参考的源码路径、复用项、实际执行的构建、未完成项。
