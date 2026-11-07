# 邮件与短信参考

只在任务涉及邮件发送、短信验证码、通知通道、SMTP、短信服务商或消息模板时加载。普通 CRUD 不加载。

## 6.1.0 源码事实

- 邮件能力在 `ruoyi-common/ruoyi-common-mail`：`MailBuilder` 提供收件人、抄送、密送、主题、文本/HTML 正文、内联图片和附件，再调用 `send()` 返回 message-id。
- 邮件配置前缀是 `mail`，由 `MailProperties` 映射 SMTP host、port、auth、user、pass、from、STARTTLS、SSL、超时等；`MailConfig` 注册全局 `MailAccount`。默认 `enabled: false` 时不要假设可发送。
- 短信能力在 `ruoyi-common/ruoyi-common-sms`，基于 SMS4J；`SmsAutoConfiguration` 注册以 Redis 实现的 `PlusSmsDao` 和 `SmsExceptionHandler`。
- 短信配置前缀是 `sms`，包含 `config-type`、`restricted`、`minute-max`、`account-max` 和 `blends.<配置名>` 多厂商配置；业务通过 `SmsFactory.getSmsBlend("<配置名>")` 选择通道。
- 现有登录验证码和 demo 已有邮件/短信调用示例；先读目标模块的现有实现和模板，不要复制 demo 到生产业务。

## 实现边界

1. **先选通道**：站内通知优先 `ruoyi-common-push`；只有确实需要外部邮件/短信时才接入本模块。不要为每个业务页面新建发送客户端。
2. **模板与内容**：验证码、通知正文和变量由业务模板生成；避免把用户输入直接拼进 HTML 邮件，防止注入和钓鱼内容。
3. **频控与防刷**：验证码发送必须有账号/IP 维度频控、有效期、一次性消费和失败上限；沿用 `sms.restricted`、`minute-max`、`account-max` 或现有验证码逻辑。
4. **异步与事务**：发送是外部副作用，不应让主业务事务因通道短暂失败而无限阻塞；按现有事件/异步策略处理，并记录可重试状态。
5. **失败可见**：区分参数错误、频控、厂商失败和网络超时；不要吞异常后提示“发送成功”。日志不记录验证码、手机号全量、邮箱全量或 SMTP 密码。
6. **配置隔离**：多环境使用不同发件账号和短信签名；密钥、授权码和 webhook 不写入代码、文档或提交。
7. **收件人校验**：服务端校验邮箱/手机号格式和归属；短信内容符合厂商签名/模板要求，邮件主题和正文长度有边界。

## 验证

- 在测试邮箱/测试手机号验证发送成功、模板变量、附件/HTML（如适用）和失败提示；生产通道只做经授权的最小验证。
- 验证频控、验证码过期、错误验证码、重复提交和通道不可用。
- 涉及配置页面时按 `page-acceptance` 验证保存、脱敏显示和连接测试；不要把真实密钥显示在页面。

官方参考：[Hutool Mail](https://hutool.cn/docs/#/extra/%E9%82%AE%E4%BB%B6%E5%B7%A5%E5%85%B7-MailUtil)、[SMS4J 文档](https://sms4j.com/)。配置键、模板和发送 API 以目标源码为准。
