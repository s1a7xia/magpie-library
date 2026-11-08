# 按需能力接入

## 什么时候读这份

只有当前需求**确实用到**工作流、定时任务、AI 或监控时才读。普通业务模块（`ruoyi-common` + `ruoyi-system` + 业务自身）不需要它们，也不要为它们预留表、字段、接口或页面结构。

判断标准很简单：需求里出现审批流转、定时/异步执行、AI 对话或系统监控，才属于这里。

## 先分清两种边界

| 能力 | 位置 | 接入方式 |
|---|---|---|
| 工作流 | `ruoyi-modules/ruoyi-workflow` | 同进程，注入 `WorkflowService` 接口 |
| 定时任务 | `ruoyi-modules/ruoyi-job` | 同进程，写任务执行器 Bean |
| AI | `ruoyi-modules/ruoyi-ai` | 同进程注册当前用户；前端复用现有 AI 页面和 OpenAPI 交互 |
| 监控 | `ruoyi-extend/ruoyi-monitor-admin` | 独立进程，不写业务代码接入 |
| 任务服务端 | `ruoyi-extend/ruoyi-snailjob-server` | 独立进程，任务后台管理 |
| AI 服务端 | `ruoyi-extend/ruoyi-snailai-server` | 独立进程，AI 服务与模型管理 |

同进程的模块可以通过 `ruoyi-api` 接口或现有 Bean 调用；`ruoyi-extend` 下的服务只能通过客户端、HTTP 或消息交互，不要在业务代码里注入它们的类。

## 工作流

### 后端

业务模块依赖 `ruoyi-api` 里的 `WorkflowService` 接口，不依赖 `ruoyi-workflow` 的实现类。

典型调用点（参考 `TestLeaveServiceImpl`）：

- 业务保存成功后发起流程：构造 `StartProcessDTO`，设置 `businessId`（业务主键字符串）、`flowCode`（流程定义编码）和 `variables`（流程变量，通常包含业务详情），再调用发起方法。
- 删除业务数据时同步清理流程实例，避免流程悬挂。
- 后端发起且没有登录用户（例如定时任务）时，显式指定处理人。
- 发起失败要抛 `ServiceException` 并纳入事务，不能只记录日志。

关键约束：

- 业务表和流程实例通过 `businessId` 关联，流程状态以工作流引擎为准。业务表如需列表筛选或页面展示，可以保留由 `ProcessEvent` 同步的状态投影字段，但不能自行驱动或伪造状态迁移。
- `flowCode` 与流程后台实际发布的流程定义编码一致，不能凭示例硬编码。
- 流程变量结构由流程定义决定，改动前对照实际流程配置。
- 具体方法签名和返回结构以 `ruoyi-api` 当前源码为准。

### 前端

复用 `plus-ui-React/src/components/workflow/` 下的现有组件，不自己实现审批交互：

| 场景 | 组件 |
|---|---|
| 提交审批 | `SubmitVerify` |
| 审批操作按钮 | `ApprovalButton` |
| 审批记录 | `ApprovalRecord` |
| 流程图 | `FlowChart` / `FlowChartImage` |

页面用 `plus-ui-React/src/api/workflow/*` 的现有请求；流程定义下拉从定义查询接口获取。参考 `plus-ui-React/src/pages/workflow/leave/leaveEdit.tsx` 的组装方式。

## 定时任务

### 任务执行器

在业务模块内新增任务执行器 Bean，由主应用扫描加载，不需要改 `ruoyi-extend`：

- 注解式：`@Component` + `@JobExecutor(name = "...")`，执行方法返回 `ExecuteResult`。
- 继承式：`@Component` extends `AbstractJobExecutor`，实现 `doJobExecute`。

参考 `ruoyi-job` 下的 `TestAnnoJobExecutor`、`TestClassJobExecutor`。业务任务优先放在自己的业务模块，不往 `ruoyi-job` 里堆业务逻辑。

### 配置与启用

- 客户端配置在 `application-*.yml` 的 `snail-job` 段，`enabled` 控制启停；`SnailJobConfig` 通过同一开关决定是否装配。
- 任务分组名要和 SnailJob 后台创建的组一致，否则任务无法分派。
- 命名空间、令牌和端口沿用现有配置，不从示例另起一套。

### 能力边界

- 任务只做调度和触发，业务数据、幂等和结果落库仍在业务 Service。
- 任务要可重入：同一任务重复执行不能产生重复业务数据。
- 长时间任务拆批处理并记录进度，不在一次执行里跑完整库。
- 业务服务重启不应丢任务定义，任务定义在服务端管理，代码侧只提供执行器。

## AI

当前 AI 能力是 SnailAI 的客户端集成，业务侧通常只需要：

- 让当前登录用户在 AI 服务中建立对应关系，沿用 `api/ai/agent` 的注册接口。
- 前端复用现有 AI 页面 `plus-ui-React/src/pages/ai/chat/` 和 `plus-ui-React/src/api/ai/agent/` 的注册接口，不自己对接 gRPC 或模型接口。
- `snail-ai` 配置默认关闭，需要时再启用；`app-id`、`token` 和服务端地址由部署环境提供。

业务模块不要直接写模型调用、提示词拼装或会话存储；这些属于 AI 模块和 AI 服务端的职责。

## 监控

`ruoyi-monitor-admin` 是独立运维服务，业务模块不需要写代码接入。业务侧只保证：

- 关键操作有 `@Log` 审计。
- 异常有明确日志，不吞异常。
- 需要监控的业务指标通过现有日志或监控端配置采集，不在业务代码里自建监控上报。

## 什么时候不该引入

| 情况 | 做法 |
|---|---|
| 只是"以后可能要审批" | 不做，先用状态字段；真需要再接工作流 |
| 只是想异步一下 | 先看现有消息、队列或 `@Async` 能否满足，不必上任务平台 |
| 只是想要个 AI 文案按钮 | 先确认是否真需要 AI 服务，不要为演示引入整套依赖 |
| 只是本地调试想看指标 | 用现有日志和监控端，不在业务模块加埋点框架 |

引入按需能力会增加部署依赖、配置项和故障面。**没有明确验收标准时，默认不引入。**

## 检查

- [ ] 需求确实需要该能力，而不是预留。
- [ ] 后端只依赖 `ruoyi-api` 接口，没有注入实现类或其他模块的 Mapper、Entity。
- [ ] 前端复用 `plus-ui-React/src/components/workflow/`、`plus-ui-React/src/api/workflow/*`、`plus-ui-React/src/pages/ai/chat/` 和 `plus-ui-React/src/api/ai/agent/` 等现有入口。
- [ ] 任务执行器在业务模块内，具备幂等和失败可重试。
- [ ] 没有把 `ruoyi-extend` 的独立服务当作本地 Bean。
- [ ] 配置项沿用现有 `snail-job`、`snail-ai` 结构，没有另起一套。
- [ ] 引入的能力已写入项目文档和部署说明。
