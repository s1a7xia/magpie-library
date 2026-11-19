# RuoYi 数据落表规范

本文件只承接已批准的 Data Model Contract，把它落到当前 RuoYi 的代码、SQL 和字段链路；不重新判断表边界、关系、唯一性、生命周期、删除语义或索引策略。模型尚未确定、发生结构性变化或契约冲突时，回到 `database-design`。

## 落表依据

- 已批准的 Data Model Contract 和当前项目 `AGENTS.md`。
- 当前 checkout 的 Entity、BO/VO、Mapper、TypeHandler、字典和参数调用。
- 项目登记的增量 SQL 目录和已有迁移。
- 项目明确规定的数据库、schema、版本、命名、时间、状态和审计约定。

契约缺少表身份、关系、唯一性、删除或迁移结论时，先回到 `database-design`；不在编码阶段补做建模决定。不增加当前项目没有的隔离字段，也不把其他框架的可选隔离模型带进本项目。

## 表与字段

- 按已批准契约落表；需要调整表边界、宽表/JSONB 选择、关系、唯一性或删除策略时，回到 `database-design`。
- 表名、列名、约束和索引使用项目已有命名约定；PostgreSQL 默认小写 `snake_case`，不加双引号。
- 每张业务表有稳定主键；雪花 ID 使用项目既有 `bigint` / `Long` 契约，前端 ID 保持 `string | number`。
- 金额使用明确精度的 `numeric` / `decimal`，不用浮点。字符串长度按真实业务约束，不统一 `varchar(255)`。
- 状态、标志、时间和审计列沿用项目已验证的类型和时区约定；同一业务域不混用字符串、`char(1)` 和布尔表达。
- 新表和新增字段写数据库注释，术语与页面、字典和 Java 字段一致。`Entity` 的 JavaDoc 不能代替 `obj_description` / `col_description`。
- 非空、默认值、唯一和检查约束按已批准契约落 DDL；新增必填列先设计已有数据补值，不直接加无默认值的 `NOT NULL`。

## 字段链路

新增或修改字段至少核对实际受影响项：

```text
DDL / 增量 SQL
  -> Entity（类型、@TableField、逻辑删除/版本/自动填充）
  -> BO（新增/编辑分组校验）
  -> VO（列表、详情、Excel、翻译、脱敏）
  -> Mapper（查询条件、排序和数据权限）
  -> TS（VO/Form/Query）
  -> 页面（搜索、列、表单、状态和错误反馈）
```

无页面、导入导出或后台任务时不制造无关链路。缺少任何实际需要的一环，都可能出现“库里有值、接口没有、页面不显示”。

### Entity 与 JSONB

- `@TableName` 绑定真实表；`@TableId` 策略与 DDL 一致；逻辑删除、乐观锁和自动填充按当前模块核对。
- 普通 `JacksonTypeHandler` 不能证明 PostgreSQL `jsonb` JDBC 绑定正确。优先复用项目已有的 JSONB-aware TypeHandler，核对 `@TableName(autoResultMap = true)`、`@TableField`、Entity/BO/VO 类型和 Wrapper 写入链路。
- 项目没有合适处理器时，按 PostgreSQL JDBC 的 `Types.OTHER` / `PGobject` 方式最小适配，不重复造多个处理器。
- 明确未传、SQL NULL、JSON null、空对象和删除属性的差异；整文档替换或局部更新按已确认语义实现。
- 可空字段更新要清空时显式 `.set(field, null)`，不依赖全局更新策略。

## 字典、参数、菜单和权限

- 有限枚举、状态和类型复用 `sys_dict_type` + `sys_dict_data`；运行期开关、阈值和周期复用 `sys_config`。先查已有类型/键，避免重复建字典和参数。
- 字典只提供值和展示，不替代 Service 的合法状态迁移校验；参数不承载业务记录、流水或历史。
- 菜单 SQL 使用项目已有约定和幂等写法；菜单 `component` 与 `dynamicPage.tsx` 注册键一致。
- 权限字符在菜单/按钮、后端 `@SaCheckPermission` 和前端 `hasPermi` 三处一致。
- 数据权限由后端实际查询和写入范围保证；列表、详情、更新、删除、批量、导出和关联记录逐项核对，不靠隐藏菜单或前端过滤。
- `@Log` 是用户操作日志，不等同于业务状态历史、字段前后值或长期合规审计。

## SQL 与迁移

- 框架初始化、框架升级和业务增量分开；业务增量放项目登记目录，不混入框架升级脚本。
- 生产变更使用增量脚本，不重跑全量初始化。脚本可重复执行，或写清幂等条件与重复执行行为。
- PostgreSQL 没有 `DELETE IF EXISTS`；按业务选条件 `INSERT` / `UPDATE` / `DELETE` 或 `ON CONFLICT`。先删再插可能破坏引用、授权和审计，不作为通用模板。
- DDL 落契约中的主键、非空、默认值、注释、索引和约束；不在本文件重新论证索引策略。

## 完成条件

- [ ] 落表决定可追溯到已批准的 Data Model Contract；模型变化没有在编码阶段擅自决定。
- [ ] 表、字段、约束、索引、字典、参数与业务身份和真实查询一致。
- [ ] DDL、迁移、Entity/BO/VO、Mapper、TS 和页面链路已核对本次涉及项。
- [ ] 菜单、路由、权限字符和后端数据范围一致。
