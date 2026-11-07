# Database Reference

用于表结构、DDL、Entity/Mapper 映射、SQL、分页、事务、并发、字典、参数、菜单和数据库变更。先读 [common.md](common.md) 的流程、复用检查和交付门禁。

## 1. 事实优先级与只读核对

- 目标工程的表结构、Entity、Mapper XML、`script/sql/` 和现有业务实现是事实源；DDL 与映射代码由 AI 直接编写，本项目没有代码生成器环节。
- 文档站只借鉴章节组织和规范，正文可能仍以 3.5.x 为主；6.0.0 的类名、字段类型和 SQL 方言必须回固定提交 `61b9ee20c3452febe1d03c6e013c0b4de11237f1` 源码核对。
- 查数据库结构前先确认连接的是哪个环境；连接可用不等于允许写入。执行 DDL、批量更新、清理或迁移前必须有明确授权。
- 数据模型先回答：业务身份、归属、状态、生命周期、唯一性、查询方式、权限范围和保留期限；不要只按页面字段建表。

## 2. 先复用框架数据

- 用户、部门、角色、岗位、字典、参数、文件、客户端等先查 `sys_user`、`sys_dept`、`sys_role`、`sys_post`、`sys_dict_type`、`sys_dict_data`、`sys_config`、`sys_oss`、`sys_client` 等现有表，按明确语义引用其 ID 或编码。
- 不为同义组织、状态或配置另建体系；不把可在 `sys_config` 管理的运行参数做成新表。
- 菜单、按钮权限和字典变更要有可执行的数据脚本；前端权限字符、后端 `@SaCheckPermission` 与 `sys_menu.perms` 保持一致。
- 业务数据与系统配置分开：业务实体不要混进字典/参数表；可变阈值优先 `sys_config`，固定枚举优先字典或代码常量。

## 3. 表与字段

- 表和列使用小写下划线；Entity 字段、DDL、BO/VO 和前端类型的命名映射保持一致。
- 继承 `BaseEntity` 时对齐五个审计字段：`create_dept`、`create_by`、`update_by` 为 `Long`，`create_time`、`update_time` 为 `LocalDateTime`。创建信息不等于业务归属或外部事件时间。
- 主键不由 `BaseEntity` 提供；`@TableId` 策略必须与 DDL 和 ID 生成方式一致。固定基线默认 `ASSIGN_ID` 雪花 ID，前端传输保留精度。
- `status`、`del_flag`、`version`、`remark` 均按需求添加，不假设基类自带。启用逻辑删除或乐观锁时，要同时接入对应机制。
- 本项目未启用多租户，业务表不新增 `tenant_id`。`script/sql/ry_workflow.sql` 中的 `tenant_id` 是 Warm-Flow 自带结构，不代表业务租户能力。
- 默认优先单表建模。只有当数据具备独立的查询边界、生命周期、权限、约束、引用关系，或行数与增长速度无法由主表稳定承载时，才拆子表；不要为了“看起来规范”预先拆表。
- 身份、状态、权限、唯一键、常用筛选与排序列落成真实列；需要 SQL 查询的字段不要只藏在 JSON 中。
- 审计自动填充、DDL 默认值和自定义 SQL 分别核对；时间类型、时区、字典值和前后端契约一致。
- 金额、比例、计数等字段明确精度、范围和空值语义；不要用浮点数代替金额。

## 4. Entity / BO / VO 与 DDL 映射

- Entity 使用 `@TableName("...")` 绑定真实表名；主键用 `@TableId(value = "...")`，策略与 DDL 一致。联合主键/关联表可用 `IdType.INPUT`，但仍要保证唯一性。
- 逻辑删除字段用 `@TableLogic`；启用后查询自动带删除条件，唯一索引设计要避免“删除后无法重建同值”。确认全局逻辑删除配置和字段默认值。
- 非表字段用 `@TableField(exist = false)`；自动填充字段用 `@TableField(fill = ...)`，并与 `MetaObjectHandler` 的实际字段名一致。
- 乐观锁字段用 `@Version` 时需要数据库列、实体类型和更新入口都正确；只加注解不处理更新结果仍可能丢并发。
- JSON 对象/集合字段：`@TableName(autoResultMap = true)` + `@TableField(typeHandler = JacksonTypeHandler.class)`；Entity、BO、VO 类型同构。
- 数据库列类型与 Java 类型要对齐：`bigint`/雪花 ID 用 `Long`，时间用 `LocalDateTime`，布尔/状态按项目实际约定；不要用 `Integer` 承接可能增长的大 ID。
- 修改 Entity/BO/VO 字段后执行 Maven 编译，让 MapStruct 实现重新生成；只改 XML 或 DDL 时也要核对查询字段和结果映射。

## 5. SQL 脚本与方言

- 表结构、字典、系统参数、菜单和初始化数据提供配套脚本。固定提交的初始化入口是 `script/sql/`，根目录按业务域放置 `ry_vue.sql`、`ry_ai.sql`、`ry_job.sql`、`ry_workflow.sql`；`oracle/`、`postgres/`、`sqlserver/` 维护方言版本，但不是每个业务域都在每个方言目录下齐全。该提交的业务增量另在 `docs/sql/`（如 `20261031_platform_base_increment.sql`），且没有 `script/sql/update/` 目录；不要照搬后续分支的目录说明。
- 该提交的 `application-dev.yml` 默认数据源是 PostgreSQL（`jdbc:postgresql://localhost:5432/postgres`），MySQL、Oracle、SQL Server 在注释示例中。写 SQL 和选择脚本前先读目标项目实际 profile 与方言；不要把默认环境当成 MySQL。
- 当前可核对到的脚本包括 `ry_vue.sql`、`ry_job.sql`、`ry_workflow.sql`、`ry_ai.sql` 及对应方言；业务增量脚本按固定提交实际位置放在 `docs/sql/`。新增业务脚本沿用目标项目现状的命名和目录习惯，不要只更新 MySQL。
- 脚本要可重复执行或有明确的版本/幂等策略；初始化数据避免重复主键、重复字典和重复菜单。生产变更优先增量脚本，不重跑全量初始化。
- DDL 明确主键、非空、默认值、注释、字符集/排序规则、索引名和约束名；避免绑定单一数据库的专属语法，确需方言差异时分别提供并说明。
- 菜单/字典/参数数据要包含明确 ID、父级、排序、权限字符、状态和删除标志；不要复制示例菜单的权限或 ID。
- 大字段、JSON、文本和索引的长度限制按目标数据库版本验证；MySQL 的索引前缀、Oracle 的标识符长度、PostgreSQL 的类型转换不能互相照搬。

## 6. 查询、分页与性能

- 优先 `BaseMapperPlus<Entity, Vo>`；简单条件用 `QueryBuilder` 或现有 Lambda Wrapper，复杂联表再沿用项目已有的 MPJ/XML，不引入第二套查询框架。
- 分页使用 `PageQuery.build()` 和 `PageResult`，分页必须在数据库完成；Controller 不自己截取全量列表。
- 空 ID 集合先返回空结果，不能把 `in ()` 退化成全表查询或无条件下拉。
- 模糊查询有边界：不要对无索引大字段做无界 `%keyword%`；常用筛选、关联和排序列建立合适索引。
- 列表关联数据批量读取，避免 N+1；能通过 `@Translation` 或现有批量查询展示的名称，不重复写逐行查询。
- 导出复用列表查询条件和数据权限；大批量导出/导入使用项目现有批处理、多 Sheet、ZIP 或异步方案。
- 关注执行计划和慢 SQL；SQL 日志只在排查时开启，生产不要长期打印全量参数。

## 7. 约束、并发与更新语义

- 明确业务唯一性、外键/引用关系、可空性、默认值和索引；唯一性优先由数据库约束保证，不能只靠应用先查后写。
- 并发更新使用乐观锁、条件更新或分布式锁，并检查更新行数；不要“查到就更新”后假设没有竞争。
- 允许清空的字段更新时，用 `LambdaUpdateWrapper.set(Xxx::getField, null)` 显式置空，不能依赖全局 `NOT_NULL` 更新策略。
- 删除与历史保留规则明确：物理删除、逻辑删除、归档表和审计保留不能混用；逻辑删除后仍要满足业务唯一性。
- 批量插入/更新使用 `insertBatch`/`updateBatchById` 或明确批大小；大数据量分批提交，避免单事务过大。
- 多表写入明确事务边界、失败补偿和锁顺序；跨数据源操作见 [dynamic-datasource.md](dynamic-datasource.md)。

## 8. 数据权限

- 功能权限和数据权限分开：能进入页面不代表能看全部数据；列表、详情、导出、批量操作和关联选择都要检查数据范围。
- 数据权限使用现有 `@DataPermission`、`DataPermissionHelper` 和 `DataScopeType`；SQL 中的数据范围列必须与别名一致。
- `DataPermissionHelper.ignore` 只在有明确理由的最小范围使用，并记录原因；后台任务没有登录态时显式确定身份和范围。
- 不引入租户维度：固定提交的 MyBatis 拦截器链没有租户插件，`ry_vue.sql`、`ry_ai.sql`、`ry_job.sql` 也没有 `tenant_id`。隔离按现有 `@DataPermission`、用户、部门和角色解决。
- 修改 Warm-Flow 脚本时，保留其自带 `tenant_id` 兼容列；不把该字段扩散到业务表、业务实体或前端类型。

## 9. 数据库变更与验证

1. **只读核对**：确认环境、库名、表结构、数据量、索引、现有字典/参数/菜单和调用方。
2. **设计变更**：写清 DDL/增量 SQL、Entity/BO/VO/Mapper、权限、数据迁移和回滚；先评估锁表、耗时和磁盘。
3. **执行**：数据库写入、生产执行和批量变更需要明确授权；执行前备份或准备可恢复点。
4. **验证**：核对约束、索引、默认值、字符集、字典值、菜单权限和初始化数据；用代表性查询检查性能。
5. **收口**：更新项目文档和验证记录，区分已执行、已观察和未验证项；不把本地成功当成生产成功。

## 10. 交付检查

- [ ] 现有表、字典、参数、菜单和框架能力已检索，新增结构有具体缺口理由。
- [ ] DDL、Entity、BO/VO、Mapper、前端类型和字典值逐项对齐。
- [ ] 主键、审计字段、逻辑删除、乐观锁、JSON 和可空更新语义一致。
- [ ] 唯一约束、索引、分页、空集合和模糊查询有明确处理。
- [ ] 多方言脚本、菜单/字典/参数数据可执行且可重复。
- [ ] 数据权限覆盖列表、详情、导出和写操作；业务表没有多租户字段。
- [ ] 数据库变更已按授权执行并记录验证证据，或明确标注未执行。
