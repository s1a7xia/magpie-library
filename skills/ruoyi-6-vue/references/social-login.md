# 社交登录与 JustAuth 参考

只在任务涉及第三方登录、OAuth 回调、JustAuth、社交账号绑定或统一身份提供商时加载。普通账号密码登录不加载。

## 6.1.0 源码事实

- 社交登录公共能力在 `ruoyi-common/ruoyi-common-social`，依赖 JustAuth 和 `ruoyi-common-redis`。
- `SocialAutoConfiguration` 注册 `AuthRedisStateCache` 作为 OAuth state 缓存；`SocialUtils` 根据 `justauth.type.<source>` 构造对应平台的授权请求。
- 目前已支持的平台分支以 `SocialUtils` 的 `switch` 为准，包括 GitHub、Gitee、QQ、微信、钉钉、企业微信、支付宝、Microsoft、MaxKey、TopIAM 等；不要根据文档列表假设某个平台已启用。
- 配置前缀是 `justauth`，包含前端回调地址 `address` 和各平台 `type`；账号密钥、client secret 必须通过部署配置或密钥管理注入。
- 系统侧社交账号关系在 `SysSocial`、`SysSocialController`、`ISysSocialService` 及 `sys_social` 表；登录入口和回调链路在 `ruoyi-admin` 的认证代码中，具体以目标源码为准。

## 实现边界

1. **先读完整回调链**：前端发起地址、后端授权 URL、state 缓存、callback、用户匹配/注册、角色和登录态写入。不要只补一个 Controller。
2. **state 必须防重放**：沿用 `AuthRedisStateCache`，校验过期和一次性使用；不要关闭 state 校验。
3. **账号绑定唯一**：`auth_id` 或平台唯一标识要有唯一约束；同一平台账号不能绑定多个内部用户，重复绑定要有明确错误。
4. **最小授权范围**：只申请业务需要的 scopes；不收集无关头像、手机号、邮箱或组织信息。
5. **身份合并谨慎**：第三方邮箱/手机号不能未经验证直接合并到已有账号；自动注册的角色、部门和数据范围要最小。
6. **密钥与回调地址**：client secret、私钥和回调地址按环境配置；日志、前端和错误响应不返回 secret、access token 或完整回调参数。
7. **失败与解绑**：取消授权、state 过期、平台拒绝、重复回调和解绑都要有可理解的结果；解绑不能破坏最后一次可用登录方式，除非产品明确允许。

## 验证

- 在测试应用上验证发起、授权、回调、登录、重复回调和 state 过期；不要用生产账号做自动化测试。
- 验证新用户注册、已有用户绑定、重复绑定、解绑和无权限状态。
- 涉及绑定页面时按 `page-acceptance` 验证入口、回调后的提示、账号列表和解绑确认。

官方参考：[JustAuth](https://www.justauth.cn/)、[OAuth 2.0 安全最佳实践](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)。平台配置和回调路径以目标工程为准。
