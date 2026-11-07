# RuoYi-Vue-Plus 6.0 数据库与数据访问规范

用于表结构、DDL、Entity/Mapper 映射、SQL、分页、事务、并发、字典、参数、菜单和数据库变更。编码总则读 [coding-standards.md](coding-standards.md)。

## 1. 建模原则

- 默认优先单表。只有当子数据有独立查询边界、生命周期、权限、约束、引用关系，或行数增长无法由主表承载时，才拆子表。
- 先回答业务身份、归属、状态、生命周期、唯一性、查询方式、权限范围、保留期限，再画表；不按页面字段机械建表。
- 用户、部门、角色、岗位、字典、参数、文件、客户端优先复用 `sys_user`、`sys_dept`、`sys_role`、`sys_post`、`sys_dict_type`、`sys_dict_data`、`sys_config`、`sys_oss`、`sys_client`。
- 可变阈值、开关和周期优先 `sys_config`；固定状态/类型优先 `sys_dict_*`；业务记录才建业务表。
- 身份、状态、权限、唯一键、常用筛选列和排序列落成真实列；需要 SQL 查询的值不要只藏在 JSON 中。

## 2. 命名与字段

- 表和列使用小写下划线；字段名、Entity 属性、前端字段按统一业务术语映射。
- 主键默认 `id` 或项目现有命名，类型与 Entity 一致。雪花 ID 使用 `bigint` / `Long`，前端用 `string | number` 并检查 JSON 精度。
- 继承 `BaseEntity` 时审计字段为：

```text
create_dept   bigint        创建部门
create_by     bigint        创建者
create_time   timestamp     创建时间
update_by     bigint        更新者
update_time   timestamp     更新时间
```

- `status`、`del_flag`、`version`、`remark` 按需求添加，不假设基类自带。逻辑删除、乐观锁和审计填充必须同时有数据库列、Entity 注解和配置支持。
- 状态、标志位用项目实际类型（常见 `char(1)` / `varchar` / `int`）；时间用与业务一致的时区类型；金额用 `decimal` 明确精度，不用浮点数。
- 可空性、默认值和唯一约束按业务语义明确；唯一性优先数据库约束，不靠应用“先查后写”。
- 表和字段写注释；注释术语与页面标签、字典名称、Java 字段注释一致。

## 3. 索引

- 主键、唯一业务键和常用查询列建立索引；索引名沿用项目风格：普通索引 `idx_<table>_<column>`，唯一索引可用 `uk_<table>_<column>` 或项目现有 `sys_*_index1` 风格。
- PostgreSQL 脚本中常见 `create index idx_...`、`create unique index ...`；按数据库方言使用对应语法，不硬套 MySQL 的 `key` 语法。
- 复合索引按实际查询顺序设计；范围查询列放在等值列之后。
- 不为低选择性字段单独建索引；不为每个外键机械建索引，要结合实际查询。
- 逻辑删除表的唯一索引要评估删除后同值重建；必要时把删除标志纳入唯一键或采用归档策略。
- 大字段、JSON、文本和前缀索引的长度限制按数据库版本验证；MySQL 索引前缀、Oracle 标识符长度、PostgreSQL 类型转换不能互抄。

## 4. Entity 与 DDL 映射

- Entity 用 `@TableName("...")` 绑定真实表；主键 `@TableId(value = "...")` 策略与 DDL/ID 生成方式一致。
- 逻辑删除用 `@TableLogic`；乐观锁用 `@Version`；自动填充字段与 `MetaObjectHandler` 的真实字段名一致。
- 非表字段用 `@TableField(exist = false)`；JSON 对象/集合用 `autoResultMap = true` + `JacksonTypeHandler`，Entity/BO/VO 同构。
- 可空字段更新需要清空时，用 `LambdaUpdateWrapper.set(Xxx::getField, null)` 显式置空，不能依赖全局 `NOT_NULL` 策略。
- 修改 Entity/BO/VO 映射后执行 Maven 编译，让 MapStruct 重新生成；改 XML/DDL 时同时核对查询列和结果映射。

## 5. SQL 脚本与方言

- 初始化入口是 `script/sql/` 的根脚本和 `postgres/`、`oracle/`、`sqlserver/` 方言目录。各方言文件覆盖不完全一致，例如 AI 初始化只在 PostgreSQL 目录中提供；新增脚本前先看目标方言已有文件。业务增量放在 `docs/sql/`。
- 数据库方言按项目实际配置和现有脚本确定，不默认 MySQL，也不混用不同数据库的语法。
- 新增业务脚本沿用现有目录和命名；至少覆盖项目实际使用的方言。
- 初始化脚本可重复执行或有明确版本/幂等策略；避免重复主键、重复字典、重复菜单。生产变更优先增量脚本，不重跑全量初始化。
- DDL 明确主键、非空、默认值、注释、索引名和约束名；方言差异分别提供，不混用语法。
- 菜单/字典/参数 SQL 包含明确 ID、父级、排序、权限字符、状态和删除标志；不复制示例 ID 或权限。
- 数据库写入、DDL、批量更新、清理和迁移必须有明确授权；连接可用不等于允许写。

## 6. 查询、分页与性能

- 优先 `BaseMapperPlus<Entity, Vo>`；简单条件用 `QueryBuilder`/Wrapper，复杂联表再沿用 MPJ/XML。
- 分页使用 `PageQuery.build()` + `PageResult`，在数据库完成；Controller 不截取全量列表。
- 空 ID 集合先返回空结果，禁止 `in ()` 退化成全表查询。
- 模糊查询只用于允许的字段；无索引大字段不做无界 `%keyword%`。
- 列表关联数据批量读取，避免 N+1；能 `@Translation` 的展示字段不逐行查询。
- 导出复用列表查询条件和数据权限；大批量导入/导出使用现有批处理、多 Sheet、ZIP 或异步能力。
- 关注执行计划和慢 SQL；SQL 日志只在排障时开启，生产不长期打印全量参数。

## 7. 约束、并发与事务

- 明确业务唯一性、引用关系、可空性、默认值和索引；唯一性由数据库约束兜底。
- 并发更新用 `@Version`、条件更新或现有分布式锁，并检查受影响行数；不假设“查到就更新”没有竞争。
- 删除规则明确：物理删除、逻辑删除、归档和审计保留不能混用。
- 批量插入/更新用 `insertBatch`/`updateBatchById` 或明确批大小；大数据量分批提交，避免单事务过大。
- 多表写入明确事务边界、失败补偿和锁顺序；跨数据源见 [dynamic-datasource.md](dynamic-datasource.md)。

## 8. 数据权限与安全

- 功能权限和数据权限分开；列表、详情、导出、批量操作和关联选择都检查数据范围。
- 使用现有 `@DataPermission`、`DataPermissionHelper`、`DataScopeType`；SQL 数据范围列必须与别名一致。
- `DataPermissionHelper.ignore` 只在有明确理由的最小范围使用，并记录原因；后台任务显式确定身份和范围。
- SQL 使用参数绑定或 Wrapper；排序字段做白名单校验，不拼接用户输入。

## 9. 数据库变更流程

1. **只读核对**：确认环境、库名、表结构、数据量、索引、现有字典/参数/菜单和调用方。
2. **设计**：写清 DDL/增量 SQL、Entity/BO/VO/Mapper、权限、数据迁移和回滚；评估锁表、耗时和磁盘。
3. **执行**：数据库写入和生产变更需明确授权；执行前准备备份或可恢复点。
4. **验证**：核对约束、索引、默认值、字典值、菜单权限和初始化数据；用代表性查询检查性能。
5. **收口**：更新项目文档和验证记录，区分已执行、已观察和未验证项。

## 10. 检查清单

- [ ] 默认单表；确实需要拆表时有独立边界和理由。
- [ ] 现有表、字典、参数、菜单和框架能力已检索，新增结构有具体缺口。
- [ ] 主键、审计字段、逻辑删除、乐观锁、JSON 和可空更新语义一致。
- [ ] 唯一约束、索引、分页、空集合和模糊查询有明确处理。
- [ ] DDL、Entity、BO/VO、Mapper、前端类型和字典值逐项对齐。
- [ ] 菜单/字典/参数脚本可执行且可重复，权限字符三处一致。
- [ ] 数据权限覆盖列表、详情、导出和写操作，隔离按部门、用户和角色模型实现。
- [ ] 数据库变更已按授权执行并记录证据，或明确标注未执行。
