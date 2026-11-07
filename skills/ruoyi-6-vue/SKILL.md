---
name: ruoyi-6-vue
description: "RuoYi-Vue-Plus 6.0.0 + Vue 3 开发配置：以 p0-integration 提交 61b9ee20 为固定事实基线，按任务只加载编码规范、后端、API 契约、前端、CRUD、数据库、页面设计及工作流、任务、搜索、消息、AI/MCP等条件参考，提供 6.0.0 源码约束、复用检查与验证门禁。用于已确认的 RuoYi 6.x Vue 项目；也是全局默认技术 profile。触发：ruoyi-6-vue、RuoYi-Vue-Plus 6.0.0、若依Plus、plus-ui、Vue 页面、Java 业务代码、SQL、Warm-Flow、SnailJob、Elasticsearch、MQTT、AI、MCP。"
---

# RuoYi 6.0 Vue Development Profile

这是 **RuoYi-Vue-Plus 6.0.0 + Vue** 的单一技术入口，不按后端、前端、数据库拆成多个技能。先读 [common.md](references/common.md)，再只加载当前任务真正涉及的领域参考。

## 事实优先级

1. 本地 `D:\FDE\RuoYi-Vue-Plus` 的 `codex/p0-integration` 分支固定提交 `61b9ee20c3452febe1d03c6e013c0b4de11237f1`（后端 `revision=6.0.0`、`plus-ui` 6.0.0）和当前项目自己的真实源码。
2. 当前项目自己的 `AGENTS.md`、`docs/agents/coding-standards.md` 和项目源码。
3. 本技能中以提交 `61b9ee20` 核对过的约束。
4. [官方文档地图](references/docs-map.md) 指向的 RuoYi-Plus 文档站；该站正文默认以 3.5.x 为主线，只借鉴章节组织与思路，不能替代固定提交的源码事实。
5. 通用 Spring Boot、MyBatis-Plus、Vue、Element Plus 习惯。

发生冲突时，以提交 `61b9ee20` 的源码和框架邻近实现为准，不以分支后续 HEAD 覆盖基线事实。不要用示例路径、旧版 API、旧模板或文档站版本号猜目标工程。本项目没有代码生成器操作环节；基础 CRUD 和全部业务代码都由 AI 参照真实 demo、邻近业务实现和 `ruoyi-gen` 模板结构直接编写，不运行生成器、不下载 zip、不导入生成包。`codex/p0-integration` 中业务模块可作为项目现状的只读证据，但不把业务实现抽成通用 skill。

## Load Map

| 任务范围 | 必读 | 按需追加 |
|---|---|---|
| 任何 RuoYi 6.0.0 业务改动 | [common.md](references/common.md) | — |
| 写或改业务代码前 | [coding-standards.md](references/coding-standards.md) | 对应后端/前端/数据库规范 |
| 新增普通 CRUD 或树表 CRUD | [crud.md](references/crud.md) | 新增/改表加 [database.md](references/database.md)；新增接口加 [api-contract.md](references/api-contract.md)；改 Vue 加 [frontend.md](references/frontend.md) + [frontend-shell.md](references/frontend-shell.md)；涉及权限加 [access-control.md](references/access-control.md)；可见页面加 [ui-design.md](references/ui-design.md) |
| 模块归属、跨模块调用、请求链路、启动配置 | common | [architecture.md](references/architecture.md) |
| Java / Spring Boot / MyBatis-Plus / Sa-Token | common + coding-standards | [backend.md](references/backend.md) |
| 新增/修改 REST 接口、响应、分页、错误或加密契约 | common + coding-standards | [api-contract.md](references/api-contract.md) + [backend.md](references/backend.md) + [frontend.md](references/frontend.md) |
| plus-ui Vue 3 / TypeScript / Element Plus | common + coding-standards | [frontend.md](references/frontend.md) |
| 请求封装、路由、Pinia、布局、hooks、页面骨架 | common + frontend | [frontend-shell.md](references/frontend-shell.md) |
| 表结构 / SQL / 字典 / 参数 / 菜单 | common | [database.md](references/database.md) |
| 可见页面、布局、样式、仪表盘 | common + frontend（改 Vue 时） | [ui-design.md](references/ui-design.md) |
| Warm-Flow 流程定义、发起流程、待办/已办、审批与业务集成 | common + backend | [workflow.md](references/workflow.md) |
| SnailJob、定时任务、分布式调度、失败重试、任务日志 | common + backend | [snail-job.md](references/snail-job.md) |
| Excel 导入/导出、模板、字典转换、大批量导出 | common + backend | [excel.md](references/excel.md) |
| 文件上传/下载、OSS、附件字段、预览和存储配置 | common | [file-oss.md](references/file-oss.md) |
| WebSocket/SSE、站内消息、实时通知、消息推送 | common | [messaging.md](references/messaging.md) |
| 菜单/按钮权限、数据范围、字段脱敏 | common | [access-control.md](references/access-control.md) |
| AI / Snail AI / MCP Server/Client / 智能体集成 | common + backend | [ai-mcp.md](references/ai-mcp.md) |
| MQTT 客户端、设备接入、主题订阅与发布 | common + backend | [mqtt.md](references/mqtt.md) |
| Elasticsearch / Easy-ES、全文检索、索引同步 | common + backend | [search.md](references/search.md) |
| 社交登录 / JustAuth / OAuth 回调与账号绑定 | common + backend | [social-login.md](references/social-login.md) |
| 邮件、短信、验证码、外部通知通道 | common + backend | [mail-sms.md](references/mail-sms.md) |
| Redis 缓存、分布式锁、防重复、限流、队列 | common + backend | [cache-lock.md](references/cache-lock.md) |
| API 加解密、字段加密、密钥与密文迁移 | common + backend | [encryption.md](references/encryption.md) |
| LiteFlow 业务规则编排、复杂链路 | common + backend | [orchestration.md](references/orchestration.md) |
| 操作日志、登录日志、审计、Actuator、接口文档 | common + backend | [observability.md](references/observability.md) |
| 多语言、消息资源、翻译字段 | common + frontend | [i18n.md](references/i18n.md) |
| 动态数据源、主从库、多库访问、跨库事务 | common + backend + database | [dynamic-datasource.md](references/dynamic-datasource.md) |
| 需要查官方规范或功能说明 | common | [docs-map.md](references/docs-map.md) |
| 前后端或全栈切片 | common | 对应领域文件全部加载 |

本 profile 的唯一目标栈是 **RuoYi-Vue-Plus 6.0.0 + plus-ui 6.0.0 + Element Plus**。Soybean 等外部仓库只作为信息结构和交互思路的外部借鉴，不进入本 Load Map，不作为技术 profile，也不代表目标项目可以混用其组件或代码。

页面可见改动还要按 `frontend-design` 的方法设计；`ui-design.md` 负责把 RuoYi 业务页收敛到既有产品边界。开发阶段只做代码层面的静态核对，不启动浏览器；视觉结论和交互验证必须由用户主动发起的 `page-acceptance` 产生。

## Process

1. **定位版本与边界**：读取目标工程的 `pom.xml`、模块 POM、`package.json`/锁文件和现有目录；确认当前模块、构建命令与实际前端位置。固定基线提交 `61b9ee20` 是 Java 21、Spring Boot 4.1.1、MyBatis-Plus 3.5.17，前端 `plus-ui` 6.0.0（Vue 3.5.42、Element Plus 2.14.5、Vite 8.2.2），但以目标工程实际版本为准。`codex/p0-integration` 中前端与后端同仓，仍需分别读取各自清单。
2. **加载最小参考集**：按 Load Map 只读本次范围。跨模块改动再追加对应文件，不预读全部。
3. **先看真实实现**：修改现有模块前读目标 Controller/Service/Mapper、Vue 页面/API/hooks。新增 CRUD 时读同模块邻近实现和 `ruoyi-demo` / `plus-ui` demo，照实际分层直接手写完整的前后端代码。数据库改动先看现有表、字典、参数和脚本方言。
4. **做复用检查**：按 [common.md 的复用检查](references/common.md#repository-reuse-check) 搜索并读取候选实现、调用方和行为差异；确认现有能力不满足后才新增。跨模块调用优先 `ruoyi-api` 的接口与 DTO。
5. **实现与验证**：只做已确认范围；修改 Entity/BO/VO 映射后执行实际 Maven 编译以触发 MapStruct。前端执行项目已有的实际构建；独立类型检查不替代构建。通过 [Standards Gate](../rules/entry-protocol.md#standards-gate) 后才算完成当前阶段；页面行为与外观另走页面验收。

## Stage Integration

| 当前阶段 | 本配置提供 |
|---|---|
| think / grill | 框架复用、字段落列与 JSON、归属与审计、权限、可空更新、唯一性和状态流转；不打破单问题访谈节奏 |
| story | 把 DDL、Entity/BO/VO、API、权限、页面交互和验证写进现有 Issue 范围与验收标准 |
| implement | 读邻近实现，按现有分层直接编码；映射变更后编译；保留工作流的门禁 |
| page-acceptance | 按 [page-acceptance](../page-acceptance/SKILL.md) 走真实 Vue 页面；具体浏览器命令见 [RuoYi 页面验收速查](../page-acceptance/references/ruoyi-6-vue-browser.md) |
| debug | 结合缺陷证据检查对应层级；先复现和定位，再改动 |
| review | Test 视角看可观察契约，Code 视角看框架/映射/前端约定，Impact 视角看权限、后台身份、脚本和跨模块影响 |

## Gotchas

| 现象 | 规则 |
|---|---|
| 把原版 RuoYi 写法混进 Plus | 禁止 `SecurityUtils`、`@PreAuthorize`、`AjaxResult`、`TableDataInfo`、`BeanUtils.copyProperties`；以目标源码的 Plus 接口为准 |
| 把框架版本与业务模块版本硬绑 | 以提交 `61b9ee20` 的根 POM 和 `plus-ui/package.json` 为准；分别读取，不根据业务模块名推断版本 |
| 每个配置都新建表 | 先查 `sys_config`、`sys_dict_*`、`sys_oss` 与现有业务表；配置、枚举和业务记录分开判断 |
| 已有工具被新 helper 覆盖 | 执行复用检查；写出选中的现有方法，或说明新增实现的具体缺口 |
| 后台任务直接取登录人 | 明确任务身份、归属和数据范围；`DataPermissionHelper.ignore` 只在有理由的范围内使用 |
| 普通 CRUD 误加载工作流或调度知识 | 只有任务实际涉及 Warm-Flow 或 SnailJob 时才读对应参考；模块目录存在不代表本次要改它 |
| 把外部 UI 仓库当目标方案 | 只借鉴信息层级和交互，不引入 Naive UI、Soybean 组件或另一套请求层；目标栈始终是 plus-ui + Element Plus |
| 寻找代码生成器或模板脚手架 | 本项目没有生成器操作环节。基础 CRUD 由 AI 参照真实 demo、邻近业务实现和 `ruoyi-gen` 模板结构直接编写；不运行生成器、不下载 zip、不导入生成包，最终实现以目标项目真实源码为准 |
| 把组件 name 硬等于菜单路由 name | 菜单路由名由后端 `routeName + menuId` 生成，页面加载器再用该名包装组件；不要手工假设两者是同一字符串。保持组件 name 稳定，并检查 keep-alive |
| 只编译就宣称页面完成 | 编译只证明代码可构建；可见页面必须实际渲染验收 |
| 单领域任务加载全部参考 | 按 Load Map 加载；不要把“相关”理解成“全部” |
| 把外部文档多租户方案套进本项目 | 固定基线未启用多租户；业务表不新增 `tenant_id`，不新增租户拦截器或租户管理页 |

## Output

```text
Profile: ruoyi-6-vue — <scope; observed backend/frontend versions>
Loaded: common + <domain references>
Source evidence: <paths read>
Reuse evidence: <searched scope; reused path#method or concrete gap>
Applicable checks: <passed / findings / not applicable>
Page evidence: <rendered check or not applicable / not run>
Unfinished: <none / failed or blocked checks and next action>
```
