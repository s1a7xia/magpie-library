---
name: ruoyi-6-vue
description: "RuoYi-Vue-Plus 6.0.0 + Vue 3 开发规范：按任务加载工程能力地图、编码总则、后端能力、API 契约、前端与现有组件、CRUD、数据库、页面设计及工作流、任务、搜索、消息、AI/MCP 等条件参考。用于已确认的 RuoYi 6.x Vue 项目，也是全局默认技术 profile。触发：ruoyi-6-vue、RuoYi-Vue-Plus 6.0.0、若依Plus、plus-ui、Vue 页面、Java 业务代码、SQL、Warm-Flow、SnailJob、Elasticsearch、MQTT、AI、MCP。"
---

# RuoYi-Vue-Plus 6.0 + Vue 开发规范

这是 RuoYi-Vue-Plus 6.0.0 + Vue 的单一技术入口。先读 [工程能力地图](references/source-map.md)，再按任务只加载需要的领域规范。规范明确代码应该怎么写、公共能力在哪里、页面和数据库如何落地。

## 规范优先级

1. 当前项目自己的 `AGENTS.md`、`docs/agents/coding-standards.md` 和当前源码。
2. 本技能的通用规范和项目能力入口。
3. 框架官方文档（Spring Boot、MyBatis-Plus、Sa-Token、Vue、Element Plus、Warm-Flow、SnailJob 等）。

发生冲突时，以项目现有实现和本项目约定为准；不凭示例路径、类名直觉或框架通用写法猜项目能力。

## Load Map

| 任务范围 | 必读 | 按需追加 |
|---|---|---|
| 任何 RuoYi 6.0.0 改动 | source-map | common |
| 写或改业务代码前 | coding-standards | 对应后端/前端/数据库规范 |
| 新增普通 CRUD 或树表 CRUD | crud | database + api-contract + frontend + frontend-components；改后端加 backend/backend-capabilities；涉及权限加 access-control；可见页面加 ui-design |
| 模块归属、跨模块调用、请求链路、启动配置 | common | architecture |
| Java / Spring Boot / MyBatis-Plus / Sa-Token | common + coding-standards | backend + backend-capabilities |
| 新增/修改 REST 接口、响应、分页、错误或加密契约 | common + coding-standards | api-contract + backend + frontend |
| plus-ui Vue 3 / TypeScript / Element Plus | common + coding-standards | frontend |
| 请求封装、路由、Pinia、布局、页面骨架 | common + frontend | frontend-shell |
| 现成组件、表格、分页、工具栏、选择器、上传、hooks | common + frontend | frontend-components |
| 表结构 / SQL / 字典 / 参数 / 菜单 | common | database |
| 可见页面、布局、样式、仪表盘 | common + frontend（改 Vue 时） | ui-design |
| Warm-Flow 流程定义、发起流程、待办/已办、审批与业务集成 | common + backend | workflow |
| SnailJob、定时任务、分布式调度、失败重试、任务日志 | common + backend | snail-job |
| Excel 导入/导出、模板、字典转换、大批量导出 | common + backend | excel + backend-capabilities |
| 文件上传/下载、OSS、附件字段、预览和存储配置 | common | file-oss + backend-capabilities + frontend-components |
| WebSocket/SSE、站内消息、实时通知、消息推送 | common | messaging |
| 菜单/按钮权限、数据范围、字段脱敏 | common | access-control |
| AI / Snail AI / MCP Server/Client / 智能体集成 | common + backend | ai-mcp |
| MQTT 客户端、设备接入、主题订阅与发布 | common + backend | mqtt |
| Elasticsearch / Easy-ES、全文检索、索引同步 | common + backend | search |
| 社交登录 / JustAuth / OAuth 回调与账号绑定 | common + backend | social-login |
| 邮件、短信、验证码、外部通知通道 | common + backend | mail-sms |
| Redis 缓存、分布式锁、防重复、限流、队列 | common + backend | cache-lock + backend-capabilities |
| API 加解密、字段加密、密钥与密文迁移 | common + backend | encryption + backend-capabilities |
| LiteFlow 业务规则编排、复杂链路 | common + backend | orchestration |
| 操作日志、登录日志、审计、Actuator、接口文档 | common + backend | observability |
| 多语言、消息资源、翻译字段 | common + frontend | i18n |
| 动态数据源、主从库、多库访问、跨库事务 | common + backend + database | dynamic-datasource |
| 前后端或全栈切片 | common | 对应领域文件全部加载 |

技术栈固定为 **RuoYi-Vue-Plus 6.0.0 + plus-ui 6.0.0 + Element Plus**。不引入第二套 UI、请求层、数据访问层或前端框架。

页面可见改动还要按 `frontend-design` 的方法设计；`ui-design.md` 负责收敛到本项目的页面边界。开发阶段只做代码和构建核对，不启动浏览器；页面验收由用户主动发起的 `page-acceptance` 执行。

## 开发顺序

1. **定位**：读 `pom.xml`、模块 POM、`package.json`/锁文件、目录和当前分支；确认模块、构建命令和前端位置。
2. **找样例**：按 source-map 读同模块 Controller/Service/Mapper/VO、Vue 页面/API/hooks；新增 CRUD 同时读 `ruoyi-demo` 和 `ruoyi-gen` 模板的对应分支。
3. **定契约**：字段、类型、查询、校验、权限、字典、菜单、接口、TS 类型和页面交互一次定清；契约不清不写代码。
4. **复用检查**：搜索现有工具、Service、API、组件、hooks、字典、参数和菜单；记录选中的 `path#method` 或具体缺口。
5. **实现**：按最小范围直接写目标文件；不为假想需求增加抽象、中间件、DAO 层或第二套组件。
6. **验证**：修改 Entity/BO/VO 映射后实际执行 Maven 编译触发 MapStruct；前端执行实际构建。通过 Standards Gate 后才算开发完成；页面行为另走 `page-acceptance`。

## 编码底线

- 后端固定 `Controller -> Service 接口 -> ServiceImpl -> Mapper`；不新增 DAO/Repository 层。
- Controller 只做接收、校验、权限、日志、响应；业务编排在 Service。
- Entity 表达持久化，BO 是请求，VO 是展示/导出/翻译；不把 Entity 暴露给 Controller。
- 普通响应 `R<T>`，分页 `PageResult<T>`（`total` + `rows`），业务异常 `ServiceException`。
- 前端请求只走 `@/utils/request`；返回 `AxiosPromise<T>`；页面读 `res.data.rows/total`。
- 前端主键和关联 ID 用 `string | number`；VO/Form/Query 分开；页面入口 `index.vue`。
- 权限字符在 `sys_menu.perms`、`@SaCheckPermission`、`v-hasPermi`/`checkPermi` 三处一致。
- 数据权限在 Mapper 用 `@DataPermission`，不能由前端隐藏代替。
- 状态、类型优先字典；可变阈值、开关、周期优先 `sys_config`；不为配置建业务表。
- 默认单表；只有独立查询边界、生命周期、权限、约束或数据量需要时才拆子表。
- 复用现有组件、hooks、工具、注解和 Builder；不复制 `Pagination`、`RightToolbar`、字典缓存、选择器或请求封装。
- 不做范围外重构；修改公共模块前检查所有调用方。

## 阶段衔接

| 阶段 | 本配置提供 |
|---|---|
| think / grill | 字段落列、单表/子表、审计、权限、可空更新、唯一性、状态流转和 JSON 边界 |
| story | 把 DDL、Entity/BO/VO、API、权限、菜单、页面交互和验证写进切片 |
| implement | 本地源码样例、规范、复用检查、直接编码和构建门禁 |
| page-acceptance | 真实 Vue 页面；浏览器步骤见 `page-acceptance` 的 RuoYi 速查 |
| debug | 按 Controller/Service/Mapper、请求链、组件或 DDL 分层定位 |
| review | 可观察契约、框架约定、权限、数据范围、脚本和跨模块影响 |

## 常见错误

| 现象 | 正确做法 |
|---|---|
| 鉴权、响应或转换写错工具 | 鉴权用 `LoginHelper`，响应用 `R` / `PageResult`，对象转换用 `MapstructUtils` |
| 新增 DAO 层 | `ServiceImpl` 直接依赖 `BaseMapperPlus` 子接口 |
| Service 返回 `R<T>` | Service 返回领域结果/`PageResult`/`List`/`Boolean`；Controller 包 `R` |
| 分页读 `records` | 前端读 `res.data.rows/total`；后端用 `PageResult` |
| 所有接口都加密 | 只有前端开关、`isEncrypt` 和 POST/PUT 同时成立才加密 |
| 编排接口直接写脚本 | 真实页面验收；不绕过前端 Axios 拦截器 |
| 组件名等于菜单路由名 | 菜单路由名由 `routeName + menuId` 生成；组件 name 只用于 keep-alive |
| 看到目录就认为能力已启用 | 读 POM、配置、Bean 和调用链 |
| 复用组件逻辑手写一遍 | 先查 `frontend-components.md` 和兄弟页面 |
| 普通 CRUD 加载全部领域 | 按 Load Map 只读本次范围 |
| 把编译通过当页面完成 | 可见页面必须实际渲染验收 |

## 输出

```text
Profile: ruoyi-6-vue — <scope; observed backend/frontend versions>
Loaded: source-map + common + <domain references>
Source evidence: <paths read>
Reuse evidence: <searched scope; reused path#method or concrete gap>
Applicable checks: <passed / findings / not applicable>
Page evidence: <rendered check or not run>
Unfinished: <none / failed or blocked checks and next action>
```
