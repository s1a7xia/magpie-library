# AI、MCP 与智能体集成参考

只在任务涉及 Snail AI、智能体、AI 对话、OpenAPI 用户注册、MCP Server/Client 或把内部能力暴露给 AI 时加载。普通 CRUD 不加载。

## 6.0.0 源码事实

- AI 公共自动配置在 `ruoyi-common/ruoyi-common-ai`，入口是 `SnailAiConfig`；只有 `snail-ai.enabled=true` 时才启用 `@EnableSnailAiAgent` 和 `@EnableSnailAiOpenApi`。
- AI 业务模块是 `ruoyi-modules/ruoyi-ai`。当前可见 Controller 为 `SnailAiController`，路径 `/snail-ai`，`/user/register` 把当前登录用户注册为 Snail AI OpenAPI 用户；该类还受 `snail-ai.open-api.enabled=true` 控制。
- MCP 公共能力在 `ruoyi-common/ruoyi-common-mcp`：`McpAutoConfiguration` 在存在 `McpSyncClient` 时注册 `McpClientTemplate`，模板统一提供列工具、调用工具、读取资源、按 Server 查找客户端等操作。
- MCP Server 由 Spring AI 提供，默认端点为 `/mcp`，当前 `application.yml` 使用 `STREAMABLE`、`SYNC` 和注解扫描；MCP Client 默认关闭，开启时再配置 `streamable-http` 或 `stdio` 连接。
- 根 POM 还管理了 Elasticsearch Client、SMS4J、JustAuth、MQTT、SnailJob、Warm-Flow 等依赖；依赖存在不等于目标模块已启用对应功能。

## 先确认开关与边界

| 需求 | 先读 |
|---|---|
| AI 对话、智能体发布、知识库 | 目标项目 `snail-ai.*`、`SnailAiConfig`、`ruoyi-modules/ruoyi-ai`、现有前端 AI 页面 |
| OpenAPI 用户映射 | `SnailAiController`、`LoginHelper`、当前登录用户模型、`sys_user` 与外部 `externalId` 的对应关系 |
| 把系统能力暴露为 MCP Server | `spring.ai.mcp.server.*`、`@Tool`/注解扫描、现有鉴权与数据范围 |
| 调用外部 MCP Server | `spring.ai.mcp.client.*`、`McpClientTemplate`、连接超时和凭证注入 |
| 普通业务不需要 AI | 不引入 AI 依赖、不建向量表、不改请求链 |

## 实现边界

1. **先读真实入口**：不要凭文档站或 Spring AI 示例创建 Controller、Tool 或连接配置；当前项目的 AI 模块可能只是未启用的集成骨架。
2. **身份与权限**：AI 请求同样受 Sa-Token、用户、部门和数据范围约束。不要因为调用方是 AI 就跳过 `@SaCheckPermission`、归属校验或敏感字段脱敏。
3. **外部标识稳定**：注册 OpenAPI 用户时使用稳定的内部用户 ID 作为 `externalId`，不要在每次请求生成新标识；重试要幂等。
4. **工具最小暴露**：MCP 工具/资源只暴露完成任务所需的方法，参数有校验、结果有边界；不要把通用 SQL、任意文件读取或内部管理接口直接暴露。
5. **提示词与数据分离**：提示词、模型配置、知识库内容和业务权限分别管理；不把密钥、完整个人信息或内部错误直接写入提示词、日志或工具响应。
6. **超时与失败**：外部 AI/MCP 调用使用配置的超时和有限重试；失败不应破坏已提交的业务事务。长任务需要明确取消、状态和补偿方式。
7. **输出不可信**：模型输出和外部工具返回都可能错误或含指令。执行写操作前仍需服务端校验、权限检查和用户确认；不把工具输出当授权。
8. **版本与协议**：MCP 协议、Spring AI 版本和 Snail AI Starter API 会变化；以目标工程 POM、配置和实际类为准，不照搬旧版示例。

## 验证

- 关闭 AI/MCP 开关时，普通业务启动和编译不受影响；开启后能连上实际服务。
- AI 用户注册、工具调用、资源读取分别验证成功、无权限、超时和非法参数。
- 用两个角色或数据范围验证工具不会越权读取；检查日志和响应中无凭证、令牌或敏感明文。
- 涉及前端 AI 页面时，按 `page-acceptance` 在真实页面验证流式/非流式响应、取消、重试、空状态和错误提示。

官方参考：[MCP 服务端](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-server-boot-starter-docs.html)、[MCP 客户端](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-client-boot-starter-docs.html)、[Snail AI](https://snail-ai.com/)。具体 Starter、注解和配置键以固定提交 `61b9ee20` 的目标源码为准。
