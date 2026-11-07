# 数据库开发规范

## 建模

- 默认单表。只有子数据有独立查询边界、生命周期、权限、约束或数据量时才拆子表。
- 先确定业务身份、归属、状态、生命周期、唯一性、查询方式、权限范围和保留期限。
- 用户、部门、角色、岗位、字典、参数、文件优先复用 `sys_user`、`sys_dept`、`sys_role`、`sys_post`、`sys_dict_*`、`sys_config`、`sys_oss`。
- 状态、类型用 `sys_dict_*`；可变开关、阈值、周期用 `sys_config`；业务记录才建表。
- 需要筛选、排序、约束的值落真实列，不藏在 JSON 中。

## 命名与字段

- 表、列用小写下划线。
- 主键默认 `id`；雪花 ID 用 `bigint` / `Long`，前端用 `string | number`。
- 继承 `BaseEntity` 的审计列为：

```text
create_dept  bigint
create_by    bigint
create_time  timestamp
update_by    bigint
update_time  timestamp
```

- `status`、`del_flag`、`version`、`remark` 按需添加，不假设基类自带。
- 金额用 `decimal` 明确精度；不要用浮点数。
- 可空性、默认值、唯一约束按业务明确；唯一性优先数据库约束。
- 表和字段写注释，术语与页面、字典、Java 字段一致。

## 索引

- 主键、业务唯一键、常用筛选和排序列建索引。
- 复合索引按查询顺序设计，范围列放在等值列之后。
- 低选择性字段不单独建索引；外键按实际查询决定。
- 逻辑删除表的唯一索引要评估删除后同值重建。
- 索引语法按实际数据库方言，不互抄 MySQL、PostgreSQL、Oracle、SQL Server。

## Entity 映射

- `@TableName` 绑定表，`@TableId` 策略与 DDL 一致。
- 逻辑删除 `@TableLogic`；乐观锁 `@Version`；自动填充字段与 `MetaObjectHandler` 一致。
- 非表字段 `@TableField(exist = false)`。
- JSON 字段用 `autoResultMap = true` + `JacksonTypeHandler`，Entity/BO/VO 同构。
- 可空字段更新要清空时显式 `.set(field, null)`。
- 修改映射后编译后端，让 MapStruct 重新生成。

## SQL 脚本

- 初始化脚本在 `script/sql/`；方言目录为 `postgres/`、`oracle/`、`sqlserver/`。
- 各方言覆盖不完全一致；新增前先看目标目录已有文件，例如 AI 初始化只在 PostgreSQL 目录提供。
- 业务增量放 `docs/sql/`，沿用现有命名。
- 新增脚本至少覆盖项目实际使用的方言。
- 初始化脚本要可重复执行或有明确幂等策略，避免重复主键、字典和菜单。
- 生产变更优先增量脚本，不重跑全量初始化。
- DDL 写清主键、非空、默认值、注释、索引和约束。
- 菜单/字典/参数 SQL 写清 ID、父级、排序、权限字符、状态和删除标志。

## 查询与性能

- 优先 `BaseMapperPlus<Entity, Vo>` 和 `QueryBuilder`；复杂联表再沿用 MPJ/XML。
- 分页在数据库完成；`PageQuery` 未传 `pageSize` 时默认接近全量，业务接口必须限制默认值和上限。
- 空 ID 集合直接返回空结果，禁止退化成全表查询。
- 模糊查询只用于允许字段；无索引大字段不做无界 `%keyword%`。
- 关联展示批量查询，避免 N+1。
- 导出复用列表查询条件和数据权限。

## 约束、并发与事务

- 业务唯一性、引用关系、可空性、默认值和索引明确。
- 并发更新用 `@Version`、条件更新或现有锁，并检查影响行数。
- 物理删除、逻辑删除、归档和审计保留不能混用。
- 批量写入用 `insertBatch` / `updateBatchById` 或明确批大小。
- 多表写入明确事务边界和锁顺序；跨数据源另读现有动态数据源实现。

## 数据权限与安全

- 功能权限和数据权限分开；列表、详情、导出、批量操作都检查数据范围。
- 用现有 `@DataPermission`、`DataPermissionHelper`、`DataScopeType`；SQL 列名与别名一致。
- SQL 参数绑定或 Wrapper，不拼接用户输入；排序字段做白名单校验。
- 数据库写入、DDL、迁移和清理需要明确授权；连接可用不等于允许写。

## 检查

- [ ] 默认单表；拆表有明确边界。
- [ ] 现有表、字典、参数、菜单已检索。
- [ ] 主键、审计、逻辑删除、乐观锁、JSON、可空更新一致。
- [ ] 唯一约束、索引、分页和空集合正确。
- [ ] DDL、Entity、BO/VO、TS 类型、字典值一致。
- [ ] 菜单、字典、参数脚本可执行，权限字符一致。
