# Warm-Flow 工作流参考

只在任务实际涉及流程定义、发起流程、审批办理、待办/已办、流程状态或业务审批集成时加载。普通 CRUD 不需要读本文件。

## 6.1.0 源码事实

- 工作流是独立业务模块 `ruoyi-modules/ruoyi-workflow`，不是通用工具包。
- 引擎为 Warm-Flow，规则编排另有 LiteFlow；模块 POM 引 `warm-flow-mybatis-plus-sb4-starter`、`warm-flow-plugin-ui-sb-web` 和 `ruoyi-common-liteflow`。
- 工作流 Bean 普遍标注 `@ConditionalOnEnable`，由 `warm-flow.enabled=true` 控制；开关关闭时不要假设 Controller、Service 或监听器仍可用。
- 跨模块调用入口是 `ruoyi-api` 的 `org.dromara.workflow.api.WorkflowService` 及其 DTO，不直接依赖工作流模块的 Service 实现或 Controller。
- 常见控制器为 `FlwDefinitionController`、`FlwInstanceController`、`FlwTaskController`、`FlwCategoryController`、`FlwSpelController`；具体接口和权限字符以目标版本源码为准。

## 先定位任务属于哪一层

| 需求 | 先读 |
|---|---|
| 业务数据提交后发起审批 | `ruoyi-api/.../WorkflowService.java`、`StartProcessDTO`、`StartProcessReturnDTO`、业务模块现有调用 |
| 审批人办理、驳回、转办、加签 | `FlwTaskController`、`FlwTaskServiceImpl`、`CompleteTaskDTO` 及现有页面 |
| 流程定义、发布、导入、复制 | `FlwDefinitionController`、`FlwDefinitionServiceImpl` |
| 流程实例、变量、业务状态 | `FlwInstanceController`、`WorkflowService`、流程变量读取 |
| 审批通知、业务副作用 | `listener/`、`event/`、`handler/` 和现有事件订阅 |

先判断目标工程是否保留工作流模块；不要因为上游文档存在某个接口，就在裁剪过的项目里凭空创建它。

## 业务集成边界

1. **业务表和流程表分开**：业务模块保存业务事实与流程状态摘要；Warm-Flow 保存定义、实例、任务和历史。不要复制一套审批表。
2. **业务唯一键稳定**：`businessId` 必须能唯一定位业务记录，并在重复提交、重试和并发下保持幂等；发起前检查是否已有活动实例。
3. **变量保持最小**：按现有调用把业务详情放入约定的 `variables.entity`；不要把所有数据库字段、凭证或无关个人信息塞进流程变量。
4. **事务边界明确**：先读现有发起和办理实现，确认业务写入、流程启动、消息通知各自的事务和失败补偿；不要假设跨库操作天然原子。
5. **身份明确**：前台审批使用登录人；后台任务、定时任务或系统回调没有登录态，不能强依赖 `LoginHelper`。确需后台发起或办理时，按 `WorkflowService` 现有约定设置身份/忽略标记，并限制数据范围。
6. **状态由流程事实反推**：列表展示的审批状态要与实例、当前任务或历史记录一致；不要只靠前端按钮改本地状态。

## 权限与页面

- 菜单、按钮、Controller 的 `@SaCheckPermission` 和前端 `v-hasPermi` 必须使用同一权限字符。
- 待办、已办、抄送和流程定义管理是不同数据范围；不要只按前端菜单可见性判断权限。
- 页面验收至少覆盖：发起后生成实例、待办出现、办理后流转、重复提交不重复发起、无权限用户不可操作。
- 流程设计器、流程图和复杂审批页属于可见交互，最终仍按 `page-acceptance` 在真实页面验证。

## 最低验证

- 修改 Entity/BO/VO 映射后编译受影响后端模块。
- 不直接脚本调用加密 API；页面流程通过真实前端 UI 验证。
- 记录所用 `warm-flow.enabled`、流程定义编码、业务 ID、任务 ID 和实际结果，不在记录中写令牌或个人敏感数据。

官方参考：[工作流模块](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/backend/modules/workflow/index.md)、[流程定义](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/backend/modules/workflow/definition.md)、[流程实例](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/backend/modules/workflow/instance.md)、[任务](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/backend/modules/workflow/task.md)。文档版本可能落后于 6.1.0，类名、配置和接口以源码为准。
