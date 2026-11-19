# 可选能力入口

本文件只用于定位可选能力，不代表它们已经是业务模块依赖或运行前置。先确认需求需要，再按“模块 POM → 条件配置/Bean → 外部可用性”核对。

## 能力入口

| 能力 | 先看 | 启用与边界 |
|---|---|---|
| 邮件 | `ruoyi-common-mail` 的 `MailBuilder`；示例 `ruoyi-demo/.../MailSendController` | 业务模块声明依赖并配置 `mail.enabled=true` 和 SMTP；附件路径禁止由前端传入 |
| 短信 | `ruoyi-common-sms`；示例 `ruoyi-demo/.../SmsController` 的 `SmsFactory.getSmsBlend(...)` | 声明依赖并配置服务商、模板和签名；发送失败要返回真实失败，不能伪造成功 |
| 站内消息/推送 | `ruoyi-api` 的 `org.dromara.system.api.MessageService` | 业务只依赖接口；`sendMessage` 是实时推送，`publishMessage` / `publishAll` 可按现有实现落消息盒子 |
| MQTT | `ruoyi-common-mqtt`；示例 `ruoyi-demo/.../MqttController` | 声明依赖并确认 `mqtt.client.enabled=true`；主题、QoS、重连和重复消费按接入契约处理 |
| 缓存、队列、锁 | `ruoyi-common-redis` 的 `CacheUtils`、`RedisUtils`、`QueueUtils`；示例 `RedisCacheController`、`RedisLockController`、`queue/PriorityQueueController` | Redis 可能经安全等公共模块传递出现，但仍要核对业务模块能否编译、Redis 是否配置；`QueueUtils` 是轻量队列，不当作可靠 MQ |
| 持久任务 | `ruoyi-common-job` 的 SnailJob；`ruoyi-admin` 已装配 `ruoyi-job`，示例在 `ruoyi-modules/ruoyi-job/.../snailjob` | 确认 `snail-job.enabled=true` 和服务端可用；任务必须可重入、可重试并落业务结果 |
| 工作流 | `ruoyi-api` 的 `org.dromara.workflow.api.WorkflowService`；场景参考 `ruoyi-workflow/.../TestLeaveServiceImpl` | 业务只依赖接口；流程定义、办理人、回调和外部事件按工作流模块契约接入 |
| 文件/OSS | `ruoyi-api` 的 `org.dromara.system.api.OssService`；底层 `ruoyi-common-oss` 的 `OssFactory` | 优先通过 `OssService` 上传、读取；不暴露本地路径或自行拼接临时 URL |
| AI、搜索 | `ruoyi-common-ai`、`ruoyi-common-elasticsearch` 及对应模块 | 只有需求明确涉及才接入；不把可选服务变成普通业务启动前置 |

## 翻译与国际化

- 展示值翻译用 `ruoyi-common-translation` 的 `@Translation` 和 `TransConstant`；新类型实现 `TranslationInterface<T>` 并标注 `@TranslationType`，批量列表优先实现 `translationBatch(...)`。
- 用户提示国际化用 `org.dromara.common.core.utils.MessageUtils.message(...)`，不要另建消息表或硬编码语言分支。
- `@Translation` 只负责展示字段替换；它不是用户提示国际化，也不要求在业务表重复保存翻译结果。

## 事务、异步与并发

这些能力按场景选择，不预埋：

| 场景 | 入口 | 边界 |
|---|---|---|
| 多表或多处写入 | Service 公共方法上的 `@Transactional(rollbackFor = Exception.class)` | 同类自调用不触发代理；异常不能被吞 |
| 单行并发修改 | `@Version`、条件更新 | 检查影响行数，冲突要反馈 |
| 同资源并发抢占 | `@Lock4j` | 锁范围覆盖事务，粒度最小并设置超时 |
| 短时重复提交 | `@RepeatSubmit` | 只防短时重复；长期幂等靠业务唯一约束或幂等键 |
| 高频只读 | `@Cacheable` / `@CacheEvict`、`CacheUtils` | 写操作同步失效；带数据权限的列表不直接缓存 |
| 可丢失短任务 | `@Async` | 复用现有线程池；需要事务提交后触发时使用现有事件机制；异步线程没有登录态 |
| 需恢复或重试的任务 | SnailJob 等持久任务 | 任务幂等可重入，结果落库，不用 `@Async` 冒充持久任务 |

外部能力不可用时返回真实不可用或明确失败；不生成假发送、假任务或假成功状态。
