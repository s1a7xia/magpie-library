# RuoYi-Vue-Plus 6.0 后端开发规范

用于 Java 21、Spring Boot、MyBatis-Plus、Sa-Token 业务代码。接口契约另读 [api-contract.md](api-contract.md)，编码总则读 [coding-standards.md](coding-standards.md)，模块边界读 [architecture.md](architecture.md)。

## 1. 分层和文件

```text
controller/XxxController
    -> service/IXxxService
    -> service/impl/XxxServiceImpl
    -> mapper/XxxMapper extends BaseMapperPlus<Entity, Vo>
```

- Controller 只负责请求接收、校验、权限、日志、响应转换；不写业务编排，不直接调用 Mapper。
- Service 接口放业务能力；实现类负责业务校验、查询编排、事务、缓存和并发控制。
- 不新增独立 DAO/Repository 层。数据访问由 `ServiceImpl` 直接依赖 Mapper。
- Entity 只承载持久化字段；BO 承载请求；VO 承载展示、翻译、脱敏和导出；不把 Entity 直接暴露给 Controller。
- 跨模块能力优先使用 `ruoyi-api` 的接口和 DTO，不直接注入其他模块的 ServiceImpl 或 Mapper。

## 2. Entity / BO / VO

### Entity

- 继承 `org.dromara.common.mybatis.core.domain.BaseEntity`；该基类提供 `createDept`、`createBy`、`createTime`、`updateBy`、`updateTime`。
- 主键不由基类提供；按表结构加 `@TableId(value = "...")`。雪花 ID 使用 `Long`。
- 按需使用 `@TableName`、`@TableLogic`、`@Version`、`@TableField`、`@OrderBy`。不要假设所有业务表都有逻辑删除或乐观锁。
- JSON 对象/集合：`@TableName(autoResultMap = true)` + `@TableField(typeHandler = JacksonTypeHandler.class)`；Entity、BO、VO 类型同构。
- 映射为 `String` 的 JSON 字段就始终按字符串处理，不要一边是对象、一边是字符串。

### BO

- 使用 `@AutoMapper(target = Xxx.class, reverseConvertGenerate = false)`。
- 新增/修改字段使用 `AddGroup` / `EditGroup`；主键在 `EditGroup` 必填。
- 字符串必填用 `@NotBlank`，对象/数字必填用 `@NotNull`；长度、格式、范围按业务语义校验。
- 查询 BO 可以复用同一个类，但不要把只用于页面的字段硬塞进 Entity。

### VO

- 使用 `@AutoMapper(target = Xxx.class)`。
- 导出字段沿用 Fesod 注解；展示名称优先 `@Translation`；敏感字段用现有 `@Sensitive` 或出口脱敏。
- VO 不返回密码、令牌、密钥等敏感字段；导出、消息、日志使用同一脱敏策略。

修改 Entity/BO/VO 映射后必须实际执行 Maven 编译，让 MapStruct 生成实现。

## 3. Mapper 与查询

- 优先继承 `BaseMapperPlus<Xxx, XxxVo>`，使用 `selectVoById`、`selectVoList`、`selectVoPage` 等现有方法。
- 简单条件用 `LambdaQueryWrapper`、`QueryBuilder` 或项目现有 Wrapper；复杂联表再沿用 MPJ/XML。
- 查询条件集中在 `buildQueryWrapper`；每个可选条件先判空，模糊查询只用在该字段确实允许时。
- 空 ID 集合先返回空结果，禁止生成无条件全表查询。
- 分页使用 `PageQuery.build()` 和 `PageResult.build(records, total)`；分页必须在数据库完成。`PageQuery` 未传 `pageSize` 时默认接近全量，业务列表要补有限默认值和上限校验。
- 列表关联展示优先批量查询或 `@Translation`，避免 N+1。

## 4. Service

- Service 返回领域结果或 `PageResult`/`List`/`Boolean`，不返回 `R<T>`。
- 业务阻断抛 `ServiceException`；不要用返回 `false` 代替需要解释的业务错误。
- 保存前校验放在 Service；唯一性优先数据库约束，必要时配合条件查询和并发处理。
- 多表写入使用 `@Transactional(rollbackFor = Exception.class)`；单表简单写入不机械加事务。
- 事务注解放在公共方法上；同类自调用不会经过 Spring 代理。
- 当前登录人、部门和账号用 `LoginHelper`；后台任务、异步线程、外部回调不得强依赖登录态，要显式确定身份和归属。
- `DataPermissionHelper.ignore` 只包住有明确理由的最小范围，并记录原因。
- 缓存、锁、Excel、文件、消息等能力优先复用现有模块和注解，不在业务 Service 里复制底层实现。

## 5. Controller

- 延续 `BaseController`、构造注入、`@Validated`、`@RestController`、`@RequestMapping`。
- 权限统一 `@SaCheckPermission("{module}:{business}:{action}")`；写操作加 `@Log`；重复提交敏感的 POST/PUT 按需 `@RepeatSubmit`。
- 普通列表：`R<PageResult<XxxVo>> list(@Validated(QueryGroup.class) XxxBo bo, PageQuery pageQuery)`。这是 demo 的现有写法；模板中的 `list(XxxBo, PageQuery)` 只作结构参考，不直接混用签名。
- 树表列表：`R<List<XxxVo>> list(XxxBo bo)`。
- 详情：`R<XxxVo> getInfo(@NotNull @PathVariable Long id)`。
- 新增/修改：`R<Void>` + `toAjax(...)`；新增用 `AddGroup`，修改用 `EditGroup`。
- 删除：`@DeleteMapping("/{ids}")` + `@PathVariable Long[] ids`；`@NotEmpty` 保护空主键。
- 导出/导入按 [api-contract.md](api-contract.md)；导出复用列表查询条件和数据权限。
- Controller 方法命名沿用真实项目：`list`、`getInfo`、`add`、`edit`、`remove`、`export`、`importData`。

## 6. 校验、异常和日志

- Controller 层用 `@Validated` 分组校验；非 Controller 层用 `ValidatorUtils.validate(bo, Group.class)`。
- `ServiceException` 由全局异常处理输出，不要在 Controller 里手写另一套错误码。
- 不吞异常、不返回底层堆栈；需要补充上下文时保留异常 cause。
- `@Log` 的标题、业务类型和操作对象准确；不记录密码、令牌、密钥和完整个人敏感信息。
- 日志用参数化占位符，不拼字符串；排障日志不长期保留全量请求体。

## 7. 配置与字典

- 可变阈值、开关、周期优先 `sys_config`，通过 `ConfigService` 读取，并提供初始化 SQL。
- 状态、类型等固定枚举优先 `sys_dict_*`，数据库保存 `dict_value`，前后端类型一致。
- 不为可变配置单独建业务表，不把环境相关地址和凭据硬编码进代码。
- 修改公共配置键、默认值或权限字符前，搜索所有调用方和前端引用。

## 8. 复用与边界

- 写代码前执行 [common.md 的复用检查](common.md#repository-reuse-check)。
- 集合、树、字符串、日期、对象转换、校验、脱敏优先用 `ruoyi-common-core` 的现有工具。
- 公共模块只承载稳定、跨模块的技术能力；单模块业务规则留在所属模块。
- 修改 common 或公共 API 时检查所有调用方，评估爆炸半径；不做范围外重构。

## 9. 验证清单

- [ ] 分层为 Controller -> Service -> Mapper，没有新增 DAO 层。
- [ ] Entity/BO/VO 职责清楚，映射注解正确，修改后已实际编译。
- [ ] 查询条件有空值保护，空集合不变成全表查询，分页在数据库完成。
- [ ] 写操作有权限、校验、必要事务和并发处理。
- [ ] 权限字符与菜单、前端按钮、数据范围一致。
- [ ] 鉴权、响应和对象转换使用本项目既有封装，无重复工具、无敏感信息入日志。
- [ ] 只编译受影响的后端模块；页面行为另行验收。
