---
name: ruoyi-6-vue
description: "RuoYi-Vue-Plus 6.0.0 + Vue 3 开发规范。规定 Java 后端分层与接口、plus-ui 页面与组件、数据库建模与 SQL，以及新增业务 CRUD 的落地顺序。用于 RuoYi 6.x Vue 项目和全局默认技术 profile。触发：ruoyi-6-vue、RuoYi-Vue-Plus、若依Plus、plus-ui、Vue 页面、Java 业务代码、SQL。"
---

# RuoYi-Vue-Plus 6.0 + Vue 开发规范

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
ruoyi-modules/ruoyi-*/       其它业务模块
plus-ui/src/                 Vue 3 + TypeScript + Element Plus
script/sql/                  初始化 SQL
docs/sql/                    业务增量 SQL
```

写代码前先读同模块的 Controller、ServiceImpl、Mapper、BO、VO 和兄弟 Vue 页面。目录存在不等于能力已启用；以 POM、配置、Bean 和调用链为准。

## 改动定位

| 要改什么 | 先看哪里 |
|---|---|
| 登录、会话、动态路由 | `plus-ui/src/views/login.vue`、`permission.ts`、`store/modules/user.ts`、`store/modules/permission.ts` |
| 布局、导航、页签、设置 | `layout/components/`、`store/modules/app.ts`、`store/modules/settings.ts` |
| 业务页面、复用组件、组合式函数 | `views/`、`components/`、`hooks/` |
| 请求、鉴权、加解密、权限判断 | `utils/request.ts`、`utils/auth.ts`、`utils/crypto.ts`、`utils/permission.ts` |
| API 类型、全局类型 | `api/<module>/<business>/types.ts`、`types/` |
| 主题、布局和组件样式 | `assets/styles/tokens/`、`assets/styles/layout/`、`assets/styles/components/` |
| 系统、工作流、任务、消息、OSS、AI、搜索 | 对应的 `ruoyi-modules/ruoyi-*`、`ruoyi-common-*` 现有实现 |

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
- 不改需求范围外的代码；修改公共组件或公共方法前检查所有调用方。

## 新增 CRUD

1. 定字段契约：表名、模块、业务名、主键、数据库/Java/TS 类型、查询方式、录入、列表、字典、必填、唯一键、权限前缀。
2. 写 DDL 和字典、参数、菜单 SQL；确认数据库方言和现有脚本位置。
3. 写 Entity、BO、VO、Mapper、Service、Controller；列表分页，树表返回列表。
4. 写 `types.ts`、`api/index.ts`、`index.vue`；先查询、表格、分页，再弹窗、校验、提交。
5. 后端编译，前端构建；页面可见改动留给 `page-acceptance` 验收。

普通单表按 `TestDemoController` 和 `views/demo/demo/index.vue`；树表按 `TestTreeController` 和 `views/demo/tree/index.vue`。两者签名和导出方法不同，不混用。

## 交付检查

- [ ] 分层、命名、包路径和同模块现有实现一致。
- [ ] 字段在表、Entity、BO/VO、TS 类型、页面标签和字典中一致。
- [ ] 分页、空集合、唯一性、事务、数据权限和权限字符已处理。
- [ ] 复用了现有组件、hooks、工具和公共能力。
- [ ] 后端已编译，前端已构建；未做页面验收时明确写“开发完成、未验收”。

输出：加载的规范、参考的源码路径、复用项、实际执行的构建、未完成项。
