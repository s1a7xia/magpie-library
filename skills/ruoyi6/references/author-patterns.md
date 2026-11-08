# 作者实现与业务场景映射

本文件只用来解决一个问题：业务需求出现后，先看作者在真实框架代码里如何表达同一类能力，再从最小实现开始写。

这里列的是**文件入口和可借鉴的决策**，不是整页复制清单。只从 `ruoyi-system`、`ruoyi-demo`、`ruoyi-common-*` 和 `ruoyi-api` 取样；业务模块只用于核实字段、权限和集成事实，不作为实现范本。

## 先判业务，再看入口

| 业务问题 | 作者入口 | 先学什么 |
|---|---|---|
| 普通单表 CRUD、分页、详情、增删改 | `TestDemoController`、`TestDemoServiceImpl`、`TestDemoMapper`、`TestDemoBo`、`TestDemoVo` | BO 接请求、VO 出响应、Service 转 Entity、Mapper 做分页和数据权限 |
| 树形分类、父子节点、展开折叠 | `TestTreeController`、`TestTreeServiceImpl`、`pages/demo/tree/index.tsx`、`useTreeTableExpand`、`handleTree` | 列表返回平铺数据，前端建树；父子约束在 Service 校验 |
| 动态参数、开关、阈值 | `SysConfigController`、`ISysConfigService` | 参数是运行期可调整配置，不另建业务表；缓存刷新走现有入口 |
| 有限枚举、状态展示 | `SysDictDataController`、`SysDictTypeController` | 字典类型和数据分开维护，页面用 `DictTag`，不要硬编码中文 |
| 用户、部门、角色、岗位、文件 | `SysUserController`、`SysDeptController`、`SysRoleController`、`SysPostController`、`SysOssController` | 先查系统模块的现有页面、组件和 API，不另造选择器、上传器或平行查询表 |
| Excel 导入 | `TestDemoController.importData`、`TestDemoImportVo`、`TestExcelController.importWithOptions`、`DefaultExcelListener` | 导入用独立 ImportVo，先校验再转换，错误结果反馈给用户 |
| Excel 导出、模板、多 sheet | `TestExcelController`、`ExportExcelServiceImpl`、`ExportDemoVo` | 复用 `ExcelBuilder`，按导出规模决定普通导出还是自定义 writer |
| 数据权限 | `TestDemoMapper`、系统模块的 `@DataPermission` | 注解主要在 Mapper；列表、详情、更新、删除都覆盖，列名和表别名一致 |
| 防重复提交 | 作者 Controller 的 `@RepeatSubmit` | 短时防重只解决重复点击；业务唯一性和长期幂等另用约束或幂等表 |
| 操作日志 | 作者 Controller 的 `@Log` + `BusinessType` | 记录用户操作；不等于业务状态历史、版本比较或合规留痕 |
| 事务边界、批量写 | 系统模块 Service 的事务边界、`TestBatchController` 的批量入口 | 单表单次写不必机械加事务；多表写入在 Service 公共方法上界定边界，批量写入先确认数据量和失败策略 |
| 分布式锁、限流 | `RedisLockController`、`RedisRateLimiterController` | 只在真实并发或滥用风险出现时引入；锁和限流粒度尽量小 |
| 异步、队列 | `PriorityQueueController` 及现有消息、任务入口 | 先判断同步是否足够；需要异步时再选队列、任务或消息，不预设 MQ |
| 敏感字段 | `TestSensitiveController`、返回对象/VO 字段上的 `@Sensitive` | 脱敏在响应出口做，不把前端隐藏当作安全边界 |
| 字段存储加密 | `TestEncryptController`、`TestDemoEncrypt`、`@EncryptField` | 加密落库字段；与展示脱敏、传输加密不是同一件事 |
| 接口传输加密 | `SysUserController`、`SysProfileController` 的 `@ApiEncrypt` | 保护请求体传输；前端配合 `isEncrypt: 'true'`，不能替代存储加密 |
| 国际化、接口文档 | `TestI18nController`、Controller JavaDoc | 接口文档来自 JavaDoc，不重复写 `@Tag` / `@Operation` |
| 搜索、消息、MQTT、工作流、AI | 对应 `ruoyi-modules/ruoyi-*`、`ruoyi-common-*` 和 `ruoyi-api` | 只有需求确实涉及才读现有调用链，不把可选能力变成业务模块前置依赖 |

## 按业务形态组合

**普通单表**：先用 `TestDemo*` 的 Controller、Service、Mapper、BO、VO 和 `pages/demo/demo/index.tsx` 页面壳；字段和校验按 BO 契约替换。不要因为 demo 有部门、用户字段就把它们带进新业务。

**主从记录**：主表承载主体，子表承载可重复明细或独立生命周期。作者没有现成的主从示例，不要从业务模块找一个“像主从”的实现当规范；按 `TestDemo*` 的 Service/Mapper 结构扩展，子表查询和写入放在同一业务 Service 的事务边界内，并参照系统模块的权限、删除和事务处理。

**状态流转**：状态变更写法参照 `ruoyi-system` 的 `changeStatus` 端点；状态值放字典，状态迁移校验放 Service，Controller 只接请求和执行权限检查。状态历史是业务需求，`@Log` 不能替代它。

**导入批处理**：用独立 ImportVo、`ExcelBuilder.read`、校验和错误反馈；批量写入注意数据量、事务、重复导入和部分失败策略。不要直接复用 Entity 当导入对象。

**文件、图片、富文本**：先查 `FileUpload`、`ImageUpload`、`RichTextEditor` 和 OSS API，表单保存 `ossId` 或 `oss://<ossId>`，不要自建上传接口或保存临时 URL。

**外部接入、异步、审批**：先找 `ruoyi-api` 或作者模块入口，确认进程内 Bean、独立服务、消息或 HTTP 的边界；业务模块只用来核实已有字段和集成事实。只有当前验收标准需要时才引入。外部副作用不塞进长事务，失败要有明确反馈或补偿记录。

## 取样后的判断

选中作者实现后，不要照着类名整段复制。至少确认：

- 当前需求是否真的需要这个机制；不需要就不引入。
- 权限、数据范围、事务、异常和返回结构是否与业务契约一致。
- 字段是否来自当前 BO/VO，而不是 demo 示例字段。
- 复用的是框架能力，还是仅复制了一个碰巧相似的业务实现。
- 新增抽象是否有当前真实调用方；只有一个业务使用时留在业务模块。

作者的写法是起点，不是替代业务判断的模板。业务契约优先于 demo 字段，框架公共能力优先于自造实现。
