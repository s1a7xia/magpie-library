# SnailJob 定时任务参考

只在任务明确涉及定时执行、后台批处理、分布式调度、失败重试、分片/MapReduce 或任务日志时加载。普通业务 CRUD 不加载。

## 6.1.0 源码事实

- 业务示例模块是 `ruoyi-modules/ruoyi-job`，客户端自动配置在 `ruoyi-common/ruoyi-common-job`，调度服务端在 `ruoyi-extend/ruoyi-snailjob-server`。
- 6.1.0 根 POM 使用 SnailJob `2.0.2`；客户端配置前缀是 `snail-job`，默认开发配置可能为 `enabled: false`，以目标工程配置为准。
- `SnailJobConfig` 由 `snail-job.enabled=true` 条件启用，并同时启用 Spring Scheduling 和 SnailJob 客户端。
- 普通任务示例使用 `@Component` + `@JobExecutor(name = "...")`，执行方法接收 `JobArgs` 并返回 `ExecuteResult`；MapReduce 另有 `@MapExecutor`、`@ReduceExecutor`。
- 示例覆盖普通、广播、静态分片和 MapReduce 任务；这些是示例，不要把生产业务逻辑堆进 `ruoyi-job` 的 demo 类。

## 先选实现方式

| 需求 | 选择 |
|---|---|
| 单实例、项目已有简单周期任务，且不需要统一调度或失败重试 | 先查项目现有 `@Scheduled` 用法；不要为简单需求引入额外架构 |
| 多实例调度、统一管理、失败重试、执行日志、分片或 MapReduce | 沿用 SnailJob 客户端和现有执行器模式 |
| 业务事件延迟处理、超时提醒 | 先查项目现有延迟队列/消息能力，不把所有延迟逻辑都做成 Cron |
| 普通同步业务校验或一次性脚本 | 不建定时任务 |

不要仅因依赖已存在就启用调度；新增任务前先确认部署方式、执行频率、数据范围、幂等和失败处理。官方三种方案可参见 [定时任务最佳实践](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/features/scheduled-jobs.md)，但版本和 API 以目标源码为准。

## 任务实现边界

1. **放在所属业务模块**：任务逻辑优先靠近它操作的业务数据；若需要客户端依赖，先核对模块 POM 和打包方式，不把真实业务长期放在示例模块。
2. **不依赖登录态**：任务线程没有当前用户。显式确定任务身份、部门或数据范围；不要直接调用只在前台有效的 `LoginHelper` 逻辑。
3. **幂等优先**：重试、广播和多实例都可能重复执行。使用业务唯一键、状态条件更新、幂等表或现有分布式锁，不能只靠“应该只跑一次”。
4. **结果可观察**：成功和失败都返回明确的 `ExecuteResult`，日志使用 `SnailJobLog.LOCAL`/`REMOTE` 并带任务标识；不记录令牌、密码、完整请求头或个人敏感数据。
5. **参数有边界**：只接收任务需要的参数并校验，不把任意 JSON 直接反序列化成可执行对象或 SQL。
6. **失败可恢复**：区分可重试错误和业务永久失败；不要吞异常后返回成功，也不要无上限重试。
7. **配置不硬编码**：执行组、服务地址、令牌等沿用配置和部署注入；令牌不写入代码、文档或提交。

## 验证

- 先编译受影响模块，确认执行器注解和客户端配置实际生效。
- 在测试环境用 SnailJob 管理端或项目现有触发方式执行一次，核对参数、日志、返回结果和重复执行行为；不要用脚本绕过业务鉴权直接打业务 API。
- 涉及管理页面时，按 `page-acceptance` 在真实 UI 验证任务列表、执行、日志和失败状态。
- 修改完成后记录任务名、触发方式、观察到的结果和未覆盖的边界，不写敏感配置值。
