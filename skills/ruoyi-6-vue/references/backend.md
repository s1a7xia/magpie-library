# Backend Reference

用于 Java / Spring Boot / MyBatis-Plus / Sa-Token 业务代码。先读 [common.md](common.md) 的流程、复用检查和交付门禁。涉及模块归属或跨模块调用时再读 [architecture.md](architecture.md)，不要仅按包名决定依赖。

## 对象职责与映射

- Entity 只承载持久化字段；BO 承载新增/修改/查询请求与校验；VO 承载展示、翻译、脱敏和导出。不要直接把 Entity 暴露给 Controller。
- 沿用模块现有的 `BaseEntity`、`@TableName`、`@TableId`、`@TableLogic`、`@TableField` 和校验分组；不要另造一套分层。
- BO/VO 与 Entity 的转换沿用 `@AutoMapper` 和 `MapstructUtils`。修改 Entity/BO/VO 映射字段后必须执行 Maven 编译，让 MapStruct 实现重新生成。
- 请求校验按语义使用 `@NotBlank`、`@Size`、`@Email`、`@Xss` 或项目现有校验；展示敏感字段沿用 `@Sensitive`，关联名称优先复用 `@Translation`。

### JSON 字段

- 映射为对象、Map 或集合时，Entity 的 `@TableName` 必须开启 `autoResultMap = true`，字段标注 `@TableField(typeHandler = JacksonTypeHandler.class)`，并保持 Entity/BO/VO 类型同构。
- 若字段声明为 `String`，前端与后端必须统一按 JSON 字符串处理，不要一边按对象一边按字符串。
- 选择 JSON 前确认查询方式和数据库方言支持；需要独立约束、权限或生命周期的数据应拆表，而不是继续塞进 JSON。

## Mapper

- 优先继承 `BaseMapperPlus<Entity, Vo>`；需要联表时再沿用项目已有的 `MPJBaseMapper`/XML 方式，不引入第二套查询框架。
- 简单条件优先 `QueryBuilder` 或现有 Wrapper；复杂 SQL 才写 XML。数据权限列必须与 SQL 别名一致。
- 批量写入优先 `baseMapper.insertBatch`。允许清空的字段更新时，用 `LambdaUpdateWrapper.set(Xxx::getField, null)` 显式置空，不能依赖全局 `NOT_NULL` 策略。
- 空 ID 集合先返回空结果，不得退化成无条件全表查询；分页必须在数据库完成。

## Service

- Service 承载业务校验、编排和事务，不返回 `R<T>`；业务阻断统一抛 `ServiceException`。
- 保留保存/删除校验、原子写入事务、缓存失效和并发条件；不要只靠应用层“先查后写”保证唯一性。
- 列表关联数据优先批量读取，配合 `StreamUtils`；能用 `@Translation` 的展示字段不重复写查询。
- 当前登录人、部门和账号统一使用 `LoginHelper`；集合与字符串优先复用 `StreamUtils`、`StringUtils`、Hutool 及项目现有工具。
- 定时任务、异步线程、外部回调等无登录态场景不得强依赖 `LoginHelper`。显式设置审计/归属字段，明确任务身份和数据范围；`DataPermissionHelper.ignore` 只包住有理由的范围。

## Controller

- 沿用 `BaseController`、构造注入、`@Validated`、`@SaCheckPermission`、`@Log`，按需 `@RepeatSubmit`。权限标识必须与前端按钮和菜单一致。
- 普通响应使用 `R<T>`；分页入参把业务查询对象与 `PageQuery` 分开接收，Service 返回 `PageResult<Vo>`，Controller 返回 `R<PageResult<Vo>>`。树表通常返回 `R<List<Vo>>`。
- 导出/导入复用 `ExcelBuilder` 和当前 Fesod 注解；导出范围与数据权限和列表查询一致。文件流直接写响应。
- 操作日志不要记录密码、令牌、密钥或不必要的个人数据。

## 跨模块与配置

- 跨模块调用优先 `ruoyi-api` 的接口和 DTO，不直接依赖其他模块的 Service 实现类。
- 全局阈值、开关、同步周期和运行策略优先 `sys_config`：后端通过 `ConfigService` 读取，并提供初始化 SQL。不要为可变配置单独建表，也不要硬编码到 yml。
- 状态、类型等枚举优先 `sys_dict_*`，数据库保存 `dict_value`，前后端类型一致；状态转换仍在 Service 校验。
- 复用文件、用户、部门、角色、岗位、OSS 等框架能力前，先读实际接口和数据范围，不按名称猜测。

## 注释与验证

- 公共 API、Entity/BO/VO 字段和业务方法使用简洁 JavaDoc；命名、格式和注解顺序遵循目标模块与 `.editorconfig`。
- 至少编译受影响的后端模块；映射、Lombok 或泛型改动要确认注解处理器实际运行。编译失败或环境缺失时，交付状态为未完成并记录具体输出。
- 加代码前完成 [common.md 的复用检查](common.md#repository-reuse-check)，审查时同样检查是否重复实现了已有工具。
