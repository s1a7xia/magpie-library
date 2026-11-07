# RuoYi-Vue-Plus 6.1.0 Architecture

用于判断改动应放在哪个模块、能否跨模块调用，以及新增接口需要接哪些框架机制。技术事实来自本地 `codex/p0-integration` 的 6.1.0 源码；目录存在不等于本次依赖已接入。

## 1. 模块边界

```text
ruoyi-admin/                 启动入口、Web 登录控制器、application*.yml
ruoyi-api/                   跨模块接口、DTO、事件；只依赖 ruoyi-common-core
ruoyi-common/                25 个通用能力模块；由 BOM 统一版本
ruoyi-modules/               可运行的业务/系统模块
ruoyi-extend/                monitor-admin、snailjob-server、snailai-server
plus-ui/                     Vue 3 + TypeScript + Element Plus 管理端
script/sql/                  初始化与按方言的数据库脚本
```

依赖方向按实际调用链：

```text
ruoyi-admin ──> ruoyi-modules
     │               │
     ├──────────────> ruoyi-api <── ruoyi-common-*
     │
     └──────────────> ruoyi-common-*

ruoyi-api ──> ruoyi-common-core
common 模块之间按 POM 的真实依赖调用，不凭包名猜方向。
```

- `ruoyi-api` 是跨模块契约层，不承载 Controller、Mapper、业务实现或前端可直接调用的 REST 接口。
- `ruoyi-common-*` 提供可复用技术能力；业务规则、状态流转和模块专属查询留在 `ruoyi-modules/<module>`。
- `ruoyi-admin` 负责装配与启动。除登录、验证码、首页等应用级入口外，不把业务 CRUD 堆进 admin。
- 当前项目的业务实现位于 `ruoyi-secops`，可作为“项目现状”只读参考；不把其中的业务表、字段、权限或流程写成通用 skill 规则。

## 2. 后端调用边界

### 同模块

`Controller -> Service 接口 -> ServiceImpl -> Mapper`。Controller 不直接调 Mapper；ServiceImpl 不返回 `R<T>`。简单查询可以留在 ServiceImpl，复杂联表才引入 MPJ 或 XML。

### 跨模块

- 需要调用其他模块能力时，先查 `ruoyi-api` 是否已有接口和 DTO。
- 消费方注入 API 接口，不注入其他模块的 Service 实现、Mapper 或内部 Entity。
- 新增跨模块契约时，接口与 DTO 放 `ruoyi-api/src/main/java/org/dromara/<domain>/api/`，由提供方模块实现；只暴露调用方真正需要的数据，不返回内部聚合。
- 已有模式可参考 `org.dromara.system.api.UserService` 由 `SysUserServiceImpl` 实现，或 `ConfigService`、`DictService` 的消费方式。先读接口和实现，再决定是否扩展，别新建平行服务。
- 需要异步解耦时先查项目已有事件机制；不为一次调用引入消息中间件。

### 模块接入

新增 Maven 模块时才需要同时核对：根 `pom.xml` 的 `<modules>`、依赖管理、`ruoyi-admin/pom.xml` 的运行依赖、包扫描范围和前端路由。普通业务功能通常加在现有业务模块内，不新建模块。

## 3. 通用模块职责

按任务加载，不要求全部记住：

| 能力 | 模块 | 常见入口 |
|---|---|---|
| 响应、分页、异常、校验、常量、基础工具 | `ruoyi-common-core` | `R`、`PageResult`、`ServiceException`、`AddGroup/EditGroup/QueryGroup`、`MapstructUtils`、`StreamUtils` |
| Web 基类、全局异常、XSS、CORS、验证码 | `ruoyi-common-web` | `BaseController`、`GlobalExceptionHandler`、`ResponseEnhancementAdvice` |
| MyBatis-Plus、分页、逻辑删除、乐观锁、数据权限 | `ruoyi-common-mybatis` | `BaseMapperPlus`、`PageQuery`、`QueryBuilder`、`@DataPermission`、`BaseEntity` |
| Sa-Token、登录用户、权限实现、客户端规则 | `ruoyi-common-satoken`、`ruoyi-common-security` | `LoginHelper`、`SaTokenConfig`、`SecurityConfig` |
| 缓存、锁、限流、重复提交 | `ruoyi-common-redis` | 现有注解与工具，按 [cache-lock.md](cache-lock.md) |
| 操作日志、登录日志、审计 | `ruoyi-common-log` | `@Log`、`BusinessType` |
| 翻译、脱敏 | `ruoyi-common-translation`、`ruoyi-common-sensitive` | `@Translation`、`@Sensitive` |
| Excel、OSS、邮件、短信、推送、社交通知 | 对应 `ruoyi-common-*` | 先读现有注解、Builder、Service，不绕过封装 |

通用模块里的类是框架公共 API。修改它们前先搜索调用方并评估爆炸半径；只有多个模块都需要的稳定能力才上提，单模块需求不要污染 common。

## 4. 请求链路

```text
前端 request
  -> Axios 拦截器：token、clientid、语言、重复提交、RSA/AES
  -> SaInterceptor：登录态、强制改密、clientid 一致性、客户端路径/IP 规则
  -> Controller：@SaCheckPermission、@Validated、@Log、@RepeatSubmit
  -> Service：业务校验、事务、数据权限
  -> Mapper：Wrapper/MPJ/XML，分页与逻辑删除
  -> R<T> / PageResult<T>
  -> ResponseEnhancementAdvice：翻译、脱敏等出站增强
  -> Axios 响应拦截器：解密、code 分支、错误提示
```

- 前端 API 必须经过 `@/utils/request`，由拦截器完成鉴权、加密、错误处理和重复提交保护；不写裸 Axios、`fetch` 或脚本绕过。
- 后端 Controller 的权限字符、菜单 `perms`、前端 `v-hasPermi`/`checkPermi` 必须一致。
- 分页统一 `PageQuery`；普通响应 `R<T>`；业务阻断抛 `ServiceException`，不要手写 HTTP 错误响应替代现有全局处理。
- 返回 JSON 时的翻译和脱敏由出站增强与注解完成；不要在前端隐藏敏感字段，也不要在 Controller 手工拼装同一套转换。

## 5. 配置与启动

- `ruoyi-admin/src/main/resources/application.yml` 是公共配置，`application-dev.yml` / `application-prod.yml` 管环境差异；业务模块还可以通过自己的 `application*.yml` 或 `@PropertySource` 提供默认配置。
- `application.yml` 默认端口 8080，context-path `/`；本地 dev 默认 `profiles.active=dev`，数据库与 Redis 配置需按当前环境读取，不能把示例凭据写进交付。
- 运行入口是 `org.dromara.DromaraApplication`。只编译模块时用实际 Maven 命令；需要启动时先确认数据库、Redis 和已启用外部依赖，不要因为配置文件存在就假定服务可用。
- 可调业务阈值、开关和周期优先 `sys_config`，通过 `ConfigService` 读取，并附初始化 SQL；不要为可变参数建业务表或把值散落硬编码。
- `@SaCheckPermission` 只控制功能权限；数据范围由 `@DataPermission` 和 SQL 列映射控制，两者不能互相替代。

## 6. 新增一个垂直功能时的决策顺序

1. 判断它属于现有业务模块还是公共能力；默认加在现有模块，不新建 Maven 子模块。
2. 找出同模块的邻近 Controller/Service/Mapper/VO 和前端兄弟页面，按实际实现确定分层与风格。
3. 先查 `ruoyi-api`、`ruoyi-common-*` 和现有业务 Service 是否已有组织、用户、字典、参数、文件、消息等能力。
4. 定义 DDL、Entity、BO、VO、API、TypeScript 类型、权限字符和菜单/字典数据，保证一条链路命名一致。
5. 需要异步、流程、调度、缓存、搜索或外部通道时，只加载对应领域文件，不把全栈能力一次塞进普通 CRUD。
6. 改完只验证受影响的一侧；页面可见改动另行验收，不由“能编译”推导为“页面可用”。

## 7. 反模式

- 把业务逻辑塞进 Controller，或让 Controller 直接依赖 Mapper。
- 跨模块直接注入别人的 ServiceImpl、Mapper、Entity，绕过 `ruoyi-api`。
- 单模块需求上提到 `ruoyi-common`，导致公共 API 被业务语义污染。
- 看到目录里有某能力就假定已启用；以 POM、配置、Bean 和实际调用链为准。
- 为普通 CRUD 引入新的消息队列、分布式事务、第二套 ORM 或前端请求库。
- 修改 common 公共方法却不检查所有调用方，或顺手重构范围外代码。
