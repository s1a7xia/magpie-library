# MQTT 与物联网消息参考

只在任务涉及 MQTT 客户端、设备接入、主题订阅/发布、物联网消息或第三方 MQTT Broker 时加载。普通 CRUD 不加载。

## 6.1.0 源码事实

- MQTT 公共能力在 `ruoyi-common/ruoyi-common-mqtt`，使用 `mica-mqtt-client-spring-boot-starter`。
- `MqttAutoConfiguration` 由 `mqtt.client.enabled=true` 条件启用，注册连接监听器、全局消息监听器和虚拟线程执行器。
- `MqttClientConnectListener` 处理连接成功/断开和重连扩展点；`MqttClientGlobalMessageListener` 接收所有已订阅消息。
- 开发配置键是 `mqtt.client.*`，包含 `ip`、`port`、`client-id`、账号密码、超时、重连、协议版本、缓冲区、心跳、SSL 等。默认关闭。
- 当前公共层只有连接和监听骨架，没有通用业务 Topic 模型。业务订阅、发布、设备归属和消息落库应由所属业务模块实现或复用项目现有实现。

## 实现边界

1. **先读现有设备模型和 Topic 约定**：确认设备标识、部门归属、Topic 命名、QoS、保留消息和消息格式；不要为单个页面另建一套 MQTT 客户端。
2. **连接标识唯一**：`client-id` 在多实例部署中不能重复；多实例消费需要明确共享订阅、分区或每实例独立 client-id。
3. **消息幂等**：MQTT 可能重复投递，业务处理使用消息 ID、业务唯一键或状态条件更新；不要假设“收到一次只处理一次”。
4. **线程与背压**：消息回调不阻塞 I/O 线程；重活进入受控线程池/队列。队列和消息大小有上限，避免内存堆积。
5. **安全**：使用配置注入的 Broker 凭证和 TLS，不在代码、日志或文档写明文密码；订阅主题也要做权限和部门数据范围隔离。
6. **断线可恢复**：明确 QoS、保留会话、重连行为和离线消息策略；业务状态不能只依赖“实时收到”，必要时落库并补偿。
7. **不混用消息层**：站内实时通知优先现有 `ruoyi-common-push`；MQTT 是设备/外部 Broker 协议，不是内部 WebSocket 的替代品。

## 验证

- 在测试 Broker 上验证连接、订阅、发布、断开重连和关闭开关后的行为；不要在生产 Broker 做破坏性测试。
- 用重复消息、非法 payload、超大消息和断线场景验证幂等、拒绝与恢复。
- 涉及设备页面时，在真实 UI 验证设备状态、消息展示和刷新后的持久化；UI 验收不能只看 MQTT 日志。

官方参考：[mica-mqtt Spring Client](https://mica-mqtt.dreamlu.net/guide/spring/client.html)、[MQTT 5 规范](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html)。配置键和 Starter 版本以目标工程为准。
