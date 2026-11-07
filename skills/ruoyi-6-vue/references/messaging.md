# 消息推送参考

只在任务涉及 WebSocket、SSE、站内消息、实时通知、审批提醒或前后端消息订阅时加载。普通 CRUD 不加载。

## 6.0.0 源码事实

- 统一推送能力在 `ruoyi-common/ruoyi-common-push`，配置前缀是 `message`；当前实现支持 `sse` 和 `websocket` 两种传输，默认传输以 `MessageProperties` 为准。
- 关键入口包括 `PushHelper`、`PushDTO`、`PushSessionManager`、`SseEmitterSessionManager`、`WebSocketSessionManager`、`MessageTopicListener` 和 `SseController`。
- `MessageTopicListener` 在应用启动后订阅消息主题：指定 `userIds` 时单发，否则全局广播；业务不要绕开统一推送层直接维护一套 WebSocket 会话。
- 统一访问路径由 `message.path` 配置，常见为 `/resource/message`；前端连接、鉴权和心跳要沿用项目现有实现。

## 实现边界

1. **先确认传输方式**：读目标工程 `message.transport` 和现有前端连接代码；不要同时引入新的 SSE、WebSocket 和轮询三套方案。
2. **使用统一入口**：业务事件构造 `PushDTO`，通过 `PushHelper`/会话管理器发送；不要在业务代码里自建连接表或静态 Map。
3. **身份和数据范围**：单发按用户标识，广播只用于真正全局的消息；广播还要核对目标用户的数据范围，避免越权泄露。
4. **可靠性和幂等**：实时推送不是持久消息队列。重要通知要落业务记录或复用现有消息表，断线重连后能补读；重复事件不要重复弹通知。
5. **失败不阻断主业务**：先读现有发送调用的事务和异常策略；不要因为推送失败回滚已成功的业务写入，也不要吞掉所有错误。
6. **安全和容量**：连接鉴权、允许来源、消息大小、心跳和超时沿用配置；不把令牌、完整个人数据或内部异常直接广播。

## 页面验收

- 验证连接建立、收到一条单发消息和一条广播消息；断线重连后不重复、不丢失关键状态。
- 检查无权限用户、跨部门用户和未登录连接的行为。
- 涉及通知中心时，同时检查未读计数、已读状态和刷新后的持久化结果。

外部工程参考：[消息推送最佳实践](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/features/message-push.md)。传输默认值和前端连接方式以目标源码为准。
