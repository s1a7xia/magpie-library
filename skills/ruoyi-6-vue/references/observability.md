# 操作日志、登录日志与可观测性参考

只在任务涉及操作日志、登录日志、审计、监控端点、错误追踪、日志脱敏或运行状态页面时加载。普通 CRUD 只在需要新增 `@Log` 时参考本文件的相关小节。

## 6.0.0 源码事实

- 操作日志公共能力在 `ruoyi-common/ruoyi-common-log`：`@Log(title, businessType, operatorType, isSaveRequestData, isSaveResponseData, excludeParamNames)` 由 `LogAspect` 拦截，发布 `OperLogEvent`，再由系统模块落库。
- `BusinessType` 包含 OTHER、INSERT、UPDATE、DELETE、GRANT、EXPORT、IMPORT、FORCE、GENCODE、CLEAN；操作类型要表达真实动作，不把所有写操作都标成 UPDATE。
- 日志会记录 URI、客户端、用户/部门、方法、请求方式、参数、响应、耗时和异常；单字段有长度上限，敏感参数通过 `excludeParamNames` 排除。
- 登录日志由认证流程写入 `sys_login_info`；操作日志、登录日志分别有查询、导出、删除和清理接口与权限。
- Spring Boot Actuator 通过 `management.endpoints.web.exposure.include` 暴露；当前配置包含健康、日志文件等端点，生产环境要按安全要求收紧。
- SpringDoc 在 `ruoyi-common-doc`，默认 `/api-docs` 和分组配置；接口文档也是信息暴露面，不能默认公开敏感接口说明。

## 实现边界

1. **只记录必要信息**：新增/修改/删除/导入/导出/授权等关键动作使用 `@Log`；查询和纯展示接口不滥用日志，避免噪声和存储膨胀。
2. **参数脱敏**：密码、令牌、密钥、验证码、完整手机号/邮箱等通过 `excludeParamNames` 或现有脱敏机制排除；不要为了排查把完整请求体写入日志。
3. **响应控制**：大响应、文件流、敏感业务数据关闭 `isSaveResponseData`；日志失败不能影响主业务。
4. **身份与归属**：日志用户来自登录态；后台任务/外部回调没有登录态时，明确系统身份和业务归属，不伪造当前用户。
5. **错误可追踪**：业务异常保留可定位的错误码/请求 ID；对外返回统一提示，对内日志保留必要堆栈但不泄露敏感值。
6. **监控与告警**：健康检查、指标、日志端点是运维能力，不等同业务验收；新增指标/告警要明确数据源、阈值和责任人。
7. **生产暴露面**：Actuator、SpringDoc、调试端点和日志下载按环境收紧；不要默认把全部端点暴露到公网。

## 验证

- 新增/修改/删除各触发一次日志，核对操作人、模块、类型、参数、结果和耗时；敏感字段确认已脱敏。
- 验证日志查询、导出、删除/清理权限；无权限用户不能通过接口或页面读取。
- 涉及监控页面时按 `page-acceptance` 验证数据加载、空状态、时间范围和错误提示。

官方参考：[Spring Boot Actuator](https://docs.spring.io/spring-boot/reference/actuator/index.html)、[SpringDoc](https://springdoc.org/)。端点和日志字段以目标工程为准。
