# RuoYi-Plus 官方文档地图

这是 `ruoyi-plus-uniapp-docs` 文档站的**按需检索地图**，不是 6.0.0 源码的替代品。文档正文默认以 3.5.x 为主线；涉及 6.0.0 的类名、注解、配置、目录和接口时，必须回到目标工程源码核对。

仓库：<https://github.com/bkywksj/ruoyi-plus-uniapp-docs>
文档根目录：`src/content/docs/practices/`

## 先看什么

| 任务 | 文档页 | 用途 |
|---|---|---|
| 总体编码约定 | [standards/coding.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/standards/coding.md) | 命名、分层、注释、异常和通用风格 |
| 命名 | [standards/naming.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/standards/naming.md) | 包、类、方法、字段和前端命名 |
| 注释 | [standards/comment.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/standards/comment.md) | JavaDoc 与必要注释的边界 |
| API 设计 | [standards/api-design.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/standards/api-design.md) | 路由、请求/响应、分页和错误契约 |
| 数据库规范 | [standards/database.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/standards/database.md) | 表、字段、索引、审计和 SQL 风格 |
| 前端规范 | [standards/frontend.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/standards/frontend.md) | Vue 页面、API、状态和组件约定 |
| Git 规范 | [standards/git.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/standards/git.md) | 提交、分支和变更说明 |

## 后端分层

| 主题 | 文档页 | 什么时候读 |
|---|---|---|
| 后端总览 | [backend/overview.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/backend/overview.md) | 第一次进入一个模块 |
| Controller | [backend/controller-layer.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/backend/controller-layer.md) | 新增/修改接口、权限、日志、分页 |
| Service | [backend/service-layer.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/backend/service-layer.md) | 业务校验、事务、编排 |
| DAO / 数据访问 | [backend/dao-layer.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/backend/dao-layer.md)、[backend/data-access.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/backend/data-access.md) | Mapper、Wrapper、MPJ、联表 |
| 事务 | [backend/transaction.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/backend/transaction.md) | 多表写入、并发和回滚 |
| 校验 | [backend/validation.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/backend/validation.md) | BO 校验、分组和业务规则 |
| 异常 | [backend/exception-handling.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/backend/exception-handling.md) | `ServiceException`、全局异常和错误提示 |

## 功能与架构

| 主题 | 文档页 | 什么时候读 |
|---|---|---|
| 权限控制 | [features/permission-control.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/features/permission-control.md) | 菜单、按钮、接口权限字符 |
| 数据权限 | [features/data-permission.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/features/data-permission.md) | 部门/自定义数据范围 |
| 字段权限 | [features/field-permission.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/features/field-permission.md) | 字段脱敏、可见性 |
| Excel | [features/excel-operations.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/features/excel-operations.md) | 导入、导出、模板和批处理 |
| 定时任务 | [features/scheduled-jobs.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/features/scheduled-jobs.md) | SnailJob/定时任务的身份与幂等 |
| 工作流模块 | [backend/modules/workflow/index.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/backend/modules/workflow/index.md) | Warm-Flow 的模块边界、定义、实例和任务入口 |
| 流程定义 | [backend/modules/workflow/definition.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/backend/modules/workflow/definition.md) | 设计、发布、导入和流程定义管理 |
| 流程实例与任务 | [instance.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/backend/modules/workflow/instance.md)、[task.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/backend/modules/workflow/task.md) | 发起、审批、待办/已办和流程状态 |
| 文件处理 | [features/file-processing.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/features/file-processing.md) | OSS、上传、下载和预览 |
| 缓存 | [architecture/cache.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/architecture/cache.md) | 缓存键、失效和一致性 |
| 数据库架构 | [architecture/database.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/architecture/database.md) | 表关系、扩展和迁移 |
| 分布式 | [architecture/distributed.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/architecture/distributed.md) | 锁、消息、任务和跨服务 |
| 多租户 | [architecture/multi-tenant.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/architecture/multi-tenant.md) | 租户字段、隔离和权限 |
| 安全 | [security/auth.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/security/auth.md)、[security/api.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/security/api.md) | Sa-Token、接口加密和认证边界 |
| 代码生成器 | [engineering/code-generator.md](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/engineering/code-generator.md) | 模板、字段类型和生成后检查 |

另有一个**可选前端变体**参考：<https://github.com/m-xlsea/ruoyi-plus-soybean>。它是 RuoYi 后端 + Soybean Admin + Naive UI，不是官方 plus-ui；只在目标项目实际使用该前端时阅读 [soybean-ui.md](soybean-ui.md)。

## 使用规则

1. 先读本技能对应领域文件，再按上表只打开与当前任务直接相关的一两页。
2. 文档中的示例若与目标工程 6.0.0 源码冲突，以源码、生成器模板和同模块邻近实现为准。
3. 不把文档站的 3.5.x 版本号、类名或配置直接复制到 6.0.0 项目。
4. 需要长期复用的结论写入项目 `docs/research/`，不要只留在聊天里。
