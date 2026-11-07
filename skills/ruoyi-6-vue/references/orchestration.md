# LiteFlow 规则编排参考

只在任务涉及 LiteFlow、业务规则链、流程节点编排、复杂审批链路或把多步业务拆成可配置组件时加载。普通 CRUD 和工作流基础审批不自动加载。

## 6.0.0 源码事实

- LiteFlow 公共能力在 `ruoyi-common/ruoyi-common-liteflow`；`LiteFlowAutoConfiguration` 注册通用节点，`LiteFlowUtils.execute(chainId, context)` 调用 `FlowExecutor.execute2Resp` 并透传失败原因。
- 当前工作流模块用 LiteFlow 编排 `startProcessChain`、`completeTaskChain`、`taskOperationChain`、`deleteInstanceChain` 等链路，规则文件在 `ruoyi-modules/ruoyi-workflow/src/main/resources/liteflow/*.el.xml`。
- 内置节点包括 `noop`、`alwaysTrue`、`alwaysFalse`、`contextRequired`、`fail` 等；业务节点用 `@LiteflowComponent("name")` 注册。
- 配置前缀是 `liteflow`，`rule-source` 指向 classpath 规则文件；当前 `liteflow.enable` 跟随 `warm-flow.enabled`，`metrics.enabled` 有版本兼容性关闭项。

## 先判断是否真的需要

| 需求 | 选择 |
|---|---|
| 两三个固定步骤、只在一个 Service 内 | 直接写 Service 方法；不要为简单顺序引入规则引擎 |
| 多分支、可配置顺序、节点复用、复杂业务编排 | 评估 LiteFlow，并沿用现有规则文件风格 |
| 人工审批、待办/已办、流程定义 | 用 Warm-Flow，不把工作流状态塞进 LiteFlow |
| 定时/分布式任务 | 用 SnailJob；LiteFlow 不负责调度 |
| 跨系统可靠消息 | 用现有 MQ/消息能力；LiteFlow 不替代消息中间件 |

## 实现边界

1. **规则文件可读**：chain 和 component 命名表达业务动作，节点职责单一；不要把大段业务逻辑藏在 XML 表达式里。
2. **上下文明确**：执行上下文只包含节点需要的业务数据，字段有类型和校验；不把 Entity、请求头、令牌或大对象全量透传。
3. **失败语义**：节点失败要抛业务异常或返回明确失败原因，`LiteFlowUtils` 会保留原始异常；不要吞异常后继续走成功链。
4. **事务边界**：LiteFlow 负责编排，不自动保证跨节点事务。先读现有 `@Transactional`/锁/事务事件，明确哪些节点在同一事务内。
5. **幂等与重试**：链路可能被重复触发；使用业务唯一键、状态条件或锁，不能假设编排只执行一次。
6. **可观测性**：日志带 chainId、关键业务标识和失败节点；规则变更要可追溯。当前 LiteFlow metrics 可能因版本兼容关闭，不能把它当作唯一监控。
7. **开关与版本**：确认 `liteflow.enable`、规则文件路径和 Starter 版本；关闭时业务要明确不可用或回退，不静默执行半条链。

## 验证

- 验证顺序、条件分支、失败节点、空上下文和异常透传；确认失败不会误报成功。
- 对重复执行、并发执行和事务回滚做针对性验证；只重测受影响链路。
- 涉及工作流页面时，最终仍按 `page-acceptance` 验证发起、审批、驳回和状态展示。

官方参考：[LiteFlow 文档](https://liteflow.cc/)。规则语法、组件接口和版本行为以目标工程为准。
