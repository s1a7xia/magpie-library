---
name: ruoyi-6-vue
description: "RuoYi-Vue-Plus 6.x + Vue 3 开发规范。规定 Java 后端分层与接口、plus-ui 页面与组件、数据库建模与 SQL，以及新增业务 CRUD 的落地顺序。用于 RuoYi 6.x Vue 项目和全局默认技术 profile。触发：ruoyi-6-vue、RuoYi-Vue-Plus、若依Plus、plus-ui、Vue 页面、Java 业务代码、SQL、改字段、加接口、加页面、加权限。"
---

# RuoYi-Vue-Plus 6.x + Vue 开发规范

## 加载

| 任务 | 必读 |
|---|---|
| 写或改 Java 后端 | [backend.md](references/backend.md) |
| 写或改 Vue 页面、API | [frontend.md](references/frontend.md) |
| 建表、改字段、写 SQL | [database.md](references/database.md) |
| 新增完整 CRUD | 后端 + 前端 + 数据库 |
| 工作流、任务、消息、AI、MQTT 等 | 先读对应模块现有实现，不另造通用层 |

## 工程定位

```text
ruoyi-admin/                 启动与登录入口
ruoyi-api/                   跨模块接口和 DTO
ruoyi-common/                公共技术能力
ruoyi-modules/ruoyi-system/  用户、角色、部门、菜单、字典、参数、OSS
ruoyi-modules/ruoyi-demo/    CRUD、树表、Excel、MQTT、MCP、ES 示例
ruoyi-modules/ruoyi-gen/     生成模板，只用于查漏，不运行生成器
ruoyi-modules/ruoyi-*/       其它业务模块（当前项目业务模块以 README 登记为准）
plus-ui/src/                 Vue 3 + TypeScript + Element Plus
script/sql/                  初始化 SQL
docs/sql/                    业务增量 SQL
```

写代码前先读同模块的 Controller、ServiceImpl、Mapper、BO、VO 和兄弟 Vue 页面。目录存在不等于能力已启用；以当前源码、POM、配置、Bean 和调用链为准。

版本和依赖事实从当前 checkout 读取：后端看根 `pom.xml`，前端看 `plus-ui/package.json`。本技能不把某个固定补丁版本或提交号当作代码事实，代码变化后以实际文件为准。

## 本地参考实现

| 场景 | 优先参考 |
|---|---|
| 单表后端完整链路 | `ruoyi-modules/ruoyi-demo/.../TestDemoController.java`、`TestDemoServiceImpl.java`、`TestDemoMapper.java`、`TestDemo.java`、`TestDemoBo.java`、`TestDemoVo.java` |
| 树表后端 | `TestTreeController.java`、`TestTreeServiceImpl.java`、`TestTreeMapper.java` |
| 单表前端完整链路 | `plus-ui/src/api/demo/demo/{index,types}.ts`、`plus-ui/src/views/demo/demo/index.vue` |
| 树表前端 | `plus-ui/src/views/demo/tree/index.vue` |
| Excel、导入、导出 | `TestExcelController.java`、`ExportDemoVo.java`、`demo/demo/index.vue` 的导出入口 |
| 生成器模板 | `ruoyi-modules/ruoyi-gen/src/main/resources/fm/`；只查模板和字段映射，不运行生成器 |

优先复制同项目、同模块的现有实现，再按需求裁剪。没有同类页面时，单表以 `demo/demo` 为骨架，树表以 `demo/tree` 为骨架，不混用两者的接口签名、导出方式和分页结构。

## 改动定位

| 要改什么 | 必须同步的位置 | 先读哪里 | 验证 |
|---|---|---|---|
| 新增完整 CRUD | 表/字典/菜单 → Entity、BO、VO、Mapper、Service、Controller → `types.ts`、`api/index.ts`、`views/<module>/<business>/index.vue` | `TestDemo*`、`views/demo/demo` | 后端编译 + 前端构建；页面另行验收 |
| 新增字段 | DDL → Entity → BO/VO → Mapper 查询条件 → 前端类型 → 搜索、表格、表单、字典/Excel | 同表现有字段和同模块页面 | 字段全链路一致，构建通过 |
| 新增接口 | Controller → Service 接口/实现 → Mapper → `api/index.ts` → `types.ts` → 页面调用 | 同模块相邻接口 | 路径、权限、响应类型一致 |
| 新增/修改页面 | `views/<module>/<business>/index.vue`，必要时同目录子组件；请求放 `api/` | 同模块 2–3 个兄弟页面 | 保留 Element Plus 组件和页面壳，构建通过 |
| 新增/修改权限 | `sys_menu.perms` → `@SaCheckPermission` → `v-hasPermi` / `checkPermi` | 相邻菜单和角色授权 SQL | 三处权限字符完全一致 |
| 导入/导出 | VO 的 `@ExcelProperty`、`ExcelBuilder`、`importData`/`export`、前端 `download` | `TestExcelController`、`ExportDemoVo` | 导入模板、错误行提示、导出字段正确 |
| 字典/参数 | `sys_dict_type`、`sys_dict_data`、`sys_config` → `useDict`/`DictTag` 或配置读取 | 相邻字典、参数 SQL | 字典值、默认值、页面显示一致 |
| 修改公共组件/工具 | `components/`、`hooks/`、`utils/` 或 `ruoyi-common-*` | 搜索全部调用方 | 至少编译受影响模块，不顺手重构 |
| 定位工作流、任务、消息、OSS、AI、搜索 | 对应 `ruoyi-modules/ruoyi-*`、`ruoyi-common-*` | 现有 Bean、配置和调用链 | 先复用，不新造通用层 |

登录、会话、动态路由看 `views/login.vue`、`permission.ts`、`store/modules/user.ts`、`store/modules/permission.ts`；布局、导航、页签、设置看 `layout/components/`、`store/modules/app.ts`、`store/modules/settings.ts`；请求、鉴权、加解密、权限判断看 `utils/request.ts`、`utils/auth.ts`、`utils/crypto.ts`、`utils/permission.ts`；主题和页面样式看 `assets/styles/tokens/`、`assets/styles/layout/`、`assets/styles/components/`。

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
- 默认单表。只有独立查询边界、生命周期、权限或数据量需要时才拆子表。
- 状态、类型用 `sys_dict_*`；可变开关、阈值、周期用 `sys_config`；不为此建业务表。
- 权限字符在 `sys_menu.perms`、`@SaCheckPermission`、`v-hasPermi` / `checkPermi` 三处一致。
- 业务路径、包名、表前缀、权限前缀沿用项目登记；新业务不得混用框架 `/system` 命名或另起一套缩写。
- 不把生成器输出当作事实源；模板只用于确认字段命名、注解和文件落点，最终代码按当前模块现有实现写。
- 前端请求默认使用 `import request from '@/utils/request'`；不要写成命名导入。
- 不改需求范围外的代码；修改公共组件或公共方法前检查所有调用方。

## 新增 CRUD

1. 定字段契约：表名、模块、业务名、主键、数据库/Java/TS 类型、查询方式、录入、列表、字典、必填、唯一键、权限前缀。
2. 写 DDL 和字典、参数、菜单 SQL；确认数据库方言和现有脚本位置。
3. 写 Entity、BO、VO、Mapper、Service 接口、ServiceImpl、Controller；列表分页，树表返回列表。
4. 写 `types.ts`、`api/index.ts`、`index.vue`；先查询、表格、分页，再弹窗、校验、提交。
5. 接菜单和权限：新增目录/菜单用 `C`，按钮用 `F`；权限字符与后端注解、前端指令一致。
6. 后端编译，前端构建；页面可见改动只标 `Dev Complete`，交给用户发起 `page-acceptance`。

普通单表按 `TestDemoController` 和 `views/demo/demo/index.vue`；树表按 `TestTreeController` 和 `views/demo/tree/index.vue`。两者签名和导出方法不同，不混用。

新增字段的最小链路是：`DDL -> Entity -> BO -> VO -> Mapper/查询条件 -> types.ts -> 页面查询/表格/表单 -> 字典或 Excel`。只改 Entity 和页面、不改 BO/VO 或 TS 类型，属于未完成。

## 交付检查

- [ ] 分层、命名、包路径和同模块现有实现一致。
- [ ] 字段在表、Entity、BO/VO、TS 类型、页面标签和字典中一致。
- [ ] 分页、空集合、唯一性、事务、数据权限和权限字符已处理。
- [ ] 复用了现有组件、hooks、工具和公共能力。
- [ ] 后端已编译，前端已构建；未做页面验收时明确写“开发完成、未验收”。
- [ ] 没把生成器、外部框架文档或旧提交当作当前代码事实。

输出：加载的规范、参考的源码路径、复用项、实际执行的构建、未完成项。
