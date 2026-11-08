# 数据库开发规范

## 建表前

先按 `SKILL.md` 判型、扫描现有表和字典，再确定模型。先读取当前项目的数据库配置和脚本方言；项目没有另行指定数据库或正进行新选型时，默认优先 PostgreSQL。已有项目始终沿用其实际运行的方言，不为“统一 PostgreSQL”擅自迁移或改写现有 SQL。数据库层重点确认：

1. 该对象是否已有系统表或业务表，是否能加字段、状态或关联而不是新建表。
2. 业务对象的归属、可见范围和删除语义是否明确。
3. 状态、类型是否应为 `sys_dict_*`；可变开关、阈值和周期是否应为 `sys_config`。
4. 是否需要历史、审计、版本、幂等键、外部单号和异步处理。
5. 查询、分页、导出和容量是否支持当前索引设计。

能由代码、现有 SQL 或表结构确认的事实，AI 自查；不要向用户询问表里已经存在的字段或枚举。

## 业务契约

| 契约 | 落库结果 |
|---|---|
| 主体与归属 | 主体表、所属用户/部门/组织字段及对应索引 |
| 可见范围 | 数据权限列；列表、详情、导出和批量操作使用同一范围 |
| 状态与生命周期 | 状态列、默认值、合法迁移和终态；必要时保留状态历史 |
| 唯一与幂等 | 业务唯一键、外部单号、导入批次或幂等键；优先数据库唯一约束 |
| 删除语义 | 物理删除、`del_flag` 逻辑删除、归档或注销；引用关系与历史保留 |
| 历史与审计 | 审计列、操作记录、版本列或归档表；明确保留期限 |
| 并发 | `version`、条件更新或锁；定义冲突返回 |
| 查询与容量 | 分页字段、索引、导出条件和异步边界 |
| 集成边界 | 外部字段隔离、同步状态、失败重试和补偿记录 |

普通单表不为了“以后可能拆”预建主从表或通用扩展表。没有明确删除、历史和并发要求时，不自行增加状态机、版本列或归档表。

## 建模

- 默认单表。主体下存在可重复的结构化明细、需要数据库关系约束，或子数据有独立查询边界、生命周期、权限或数据量需求时应建子表；明细不必先具备独立页面或查询接口。不要为了未来可能性预建子表。
- 先过业务契约，再确定业务身份、归属、状态、生命周期、唯一性、查询方式、权限范围和保留期限。
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
create_time  datetime（MySQL）/ timestamp（PostgreSQL）
update_by    bigint
update_time  datetime（MySQL）/ timestamp（PostgreSQL）
```

- `status`、`del_flag`、`version`、`remark` 按需添加，不假设基类自带。
- 金额用 `decimal` 明确精度；不要用浮点数。
- 可空性、默认值、唯一约束按业务明确；唯一性优先数据库约束。
- 表和字段写注释，术语与页面、字典、Java 字段一致。
- 时间类型按实际方言和现有脚本写法：PostgreSQL 项目沿用本项目的 `timestamp` 约定，MySQL 项目沿用 `datetime`；不要跨方言互抄，也不要未经项目约定就混用带/不带时区类型。
- 状态、标志类字段沿用框架的 `char(1)`，取值 `0`/`1` 或字典值，不用 `boolean`、`tinyint` 另立一套。
- 字符串长度按语义定，不统一给 `varchar(255)`：账号和名称类 30、邮箱 50、手机号 11、编码与权限标识 100、备注 500、长文本用 `text`。

## 字段变更链路

新增或修改字段时，至少同步以下位置；缺任何一环都可能出现“库里有值、接口没有、页面不显示”：

```text
DDL / 增量 SQL
  -> Entity（@TableField、类型、逻辑删除/版本）
  -> BO（新增/编辑校验分组）
  -> VO（列表展示、Excel、翻译、脱敏）
  -> Mapper 查询条件/排序
  -> plus-ui types.ts（Vo/Form/Query）
  -> 页面搜索、表格列、表单项、字典
```

- 新增必填字段先确认已有数据如何补值，不能直接给生产表加无默认值的 `NOT NULL`。
- 可空字段更新要清空时显式 `.set(field, null)`；不要依赖全局更新策略。
- 字段改名要同时检查 SQL、Java 属性、JSON 字段、TS 类型、菜单/字典和导入模板。
- 修改映射或 DTO 后编译后端，让 MapStruct 重新生成。

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
- 业务增量放 `docs/sql/`，沿用现有 `日期_业务_动作.sql` 命名和分段注释。
- 项目以 PostgreSQL 为默认选型时，新增业务 SQL 以 PostgreSQL 方言为准；只有项目确实部署其它数据库时，才补齐对应方言脚本，不为未使用的数据库维护重复版本。
- 初始化脚本要可重复执行或有明确幂等策略，避免重复主键、字典和菜单。
- 生产变更优先增量脚本，不重跑全量初始化。
- DDL 写清主键、非空、默认值、注释、索引和约束。
- 菜单/字典/参数 SQL 写清 ID、父级、排序、权限字符、状态和删除标志。

### 菜单、字典和参数

菜单 SQL 按本地增量脚本的写法使用显式 `bigint` ID，并用 `NOT EXISTS` 防止重复。下面只示意字段和幂等结构，ID、路径、组件和权限均须按当前项目实际值替换：

```sql
INSERT INTO sys_menu
    (menu_id, menu_name, parent_id, order_num, path, component, is_frame, is_cache,
     menu_type, visible, status, perms, icon, create_dept, create_by, create_time, remark)
SELECT <menu_id>, '业务名称', <parent_id>, <order_num>, '<path>', '<module>/<business>/index',
       'N', 'Y', 'C', '0', '0', '<module>:<business>:list', 'form',
       <create_dept>, <create_by>, CURRENT_TIMESTAMP, '业务菜单'
WHERE NOT EXISTS (
    SELECT 1 FROM sys_menu
    WHERE menu_id = <menu_id> OR (parent_id = <parent_id> AND path = '<path>')
);
```

按钮权限用 `menu_type = 'F'`，`perms` 与 Controller 注解、前端 `v-hasPermi` 完全一致。字典用 `sys_dict_type` + `sys_dict_data`，参数用 `sys_config`；不要为可枚举状态另建业务表，也不要在页面硬编码字典文本。当前项目的模块名、组件路径和权限前缀从已有菜单及 PRD 获取，不从示例或其它业务模块复制。

当前项目存在多个增量脚本和混合历史数据，执行前先核对目标数据库、schema、方言和已执行记录；连接可用不等于允许写入。

## 查询与性能

- 优先 `BaseMapperPlus<Entity, Vo>` 和 `QueryBuilder`；复杂联表再沿用 MPJ/XML。
- 单表链式查询优先识别 `mapper.lambda()`；可复用 Wrapper 用 `QueryBuilder.lambda()`；多表用 `QueryBuilder.lambdaJoin()`。
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
- 用现有 `@DataPermission`、`DataPermissionHelper`、`DataScopeType`；注解主要标在 Mapper，列表、详情、更新、删除都覆盖，SQL 列名与表别名一致。
- SQL 参数绑定或 Wrapper，不拼接用户输入；排序字段做白名单校验。
- 敏感字段在 VO 用 `@Sensitive` 控制响应，不把脱敏当作数据库安全边界；需要展示用户、部门、字典、OSS 值时优先 `@Translation`。
- 数据库写入、DDL、迁移和清理需要明确授权；连接可用不等于允许写。

## 检查

- [ ] 默认单表；拆主从表有当前业务依据（如重复明细、关系约束、独立生命周期或查询边界），不是为未来可能性预建。
- [ ] 已扫描现有表、字典、参数和菜单，没有为已有能力另建平行表。
- [ ] 归属、状态、唯一性、删除语义、历史审计、并发和集成边界有明确依据。
- [ ] 主键、审计、逻辑删除、乐观锁、JSON、可空更新一致。
- [ ] 唯一约束、索引、分页和空集合正确。
- [ ] DDL、Entity、BO/VO、TS 类型、字典值一致。
- [ ] 菜单、字典、参数脚本可执行，权限字符一致。
- [ ] 业务口径未定的字段或字典用 TODO 标注，并优先采用符合当前业务场景的推荐默认值，说明理由和确认人；不得套用一律拒绝或一律不处理的通用默认。涉及不可逆操作或权限扩大时不擅自放开，选择业务可接受且影响范围最小的可逆方案；DDL 仍须可执行。
