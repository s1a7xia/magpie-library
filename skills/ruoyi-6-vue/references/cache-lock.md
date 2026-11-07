# 缓存、分布式锁、幂等、限流与队列参考

只在任务涉及 Redis 缓存、Caffeine/Spring Cache、分布式锁、防重复提交、接口限流、延迟/优先队列、序列号或跨实例协调时加载。普通 CRUD 不加载。

## 6.0.0 源码事实

- Redis 公共能力在 `ruoyi-common/ruoyi-common-redis`，底层使用 Redisson，另有 Spring Cache 管理器和 Caffeine 相关配置。
- `CacheUtils` 操作 Spring Cache 的 cache name + key；`RedisUtils` 提供对象缓存、TTL、分布式限流、发布订阅、原子 set-if-absent 等；`QueueUtils` 提供普通/优先阻塞队列和元素订阅。
- `@RepeatSubmit` 通过 Redis 原子键防重复提交，默认 5 秒，间隔小于 1 秒会报错；成功请求保留键到期，失败/异常会删除键。
- `@RateLimiter` 支持 `time`、`count`、`limitType`（默认/IP/集群）和 SpEL key；底层是 Redisson 令牌桶。
- 分布式锁使用 Lock4j；`Lock4jConfig` 在获取失败时统一抛 `ServiceException`。业务示例见 `@Lock4j(keys = {"#key"})`。
- Spring Cache 通过 `PlusSpringCacheManager` 接入 Redisson；现有系统模块用 `CacheUtils` 失效字典、参数、部门和 OSS 配置缓存。

## 选择最轻的机制

| 需求 | 先选 |
|---|---|
| 同一请求短时间重复点击 | `@RepeatSubmit`，不要自己写 Redis key |
| 接口/用户/IP 频率限制 | `@RateLimiter`，按全局/IP/集群选择 `LimitType` |
| 避免同一业务键并发执行 | `@Lock4j` 或现有条件更新；锁范围要小 |
| 字典、参数、配置等读多写少数据 | Spring Cache + 现有 `CacheUtils` 失效 |
| 轻量异步任务 | 现有 `QueueUtils`，但先判断是否需要可靠消息 |
| 大数据量、跨系统可靠消息 | 不用 Redis 队列硬扛；评估项目现有 MQ/消息平台 |

## 实现边界

1. **先查现有缓存名和 key**：沿用 `CacheNames`、`GlobalConstants` 和现有失效点；不要为同一数据造第二套缓存。
2. **缓存一致性**：明确写入、更新、删除后的失效顺序；数据库提交成功后失效缓存，失败路径不要留下“新缓存 + 旧数据库”。
3. **TTL 与容量**：所有缓存有合理过期和容量边界；不要把用户敏感数据、令牌或大对象长期放 Redis。
4. **锁的粒度与超时**：锁键包含业务唯一维度，获取超时和持有时间有上限；锁内不做远程调用或长事务。多实例部署不能只用 JVM 锁。
5. **幂等不是锁**：重复消息/重试需要业务唯一键、状态条件更新或幂等表；分布式锁只能降低并发，不能替代持久化幂等。
6. **限流键**：限流按真实维度（接口、用户、IP、租户）设计，避免所有用户共享一个过窄 key，也避免 key 可被用户伪造。
7. **队列可靠性**：Redis 队列用于轻量场景；进程崩溃、消费失败和重试要有明确处理，重要消息落业务表或使用可靠 MQ。
8. **降级**：Redis 不可用时明确拒绝、降级数据库还是短时本地缓存；不要静默把限流/锁当作成功。

## 验证

- 验证首次成功、重复请求被拒、失败后可重试、TTL 到期和并发多实例行为。
- 缓存验证命中/未命中、更新后失效、删除后重建和 Redis 重启；不要只测单实例。
- 锁/限流验证超时提示、不同用户/IP 隔离和集群模式；页面验收关注重复点击、错误提示和按钮 loading。

官方参考：[Redisson](https://redisson.org/)、[Lock4j](https://github.com/baomidou/lock4j)、[Spring Cache](https://docs.spring.io/spring-framework/reference/integration/cache.html)。具体工具方法和配置以目标工程为准。
