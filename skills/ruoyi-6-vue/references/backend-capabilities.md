# RuoYi-Vue-Plus 6.0 后端公共能力使用规范

本文件记录业务开发最常用、最容易重复造轮子的后端能力。写代码前先按此表查现有实现。

## 1. 响应、分页与异常

| 能力 | 入口 | 用法 |
|---|---|---|
| 统一响应 | `org.dromara.common.core.domain.R` | Controller 返回 `R.ok(data)` 或 `toAjax(...)` |
| 分页结果 | `org.dromara.common.core.domain.PageResult` | `total` + `rows`；Service 返回它，Controller 再包 `R` |
| 分页参数 | `org.dromara.common.mybatis.core.page.PageQuery` | `pageQuery.build()`；排序字段会经过 `SqlUtil.escapeOrderBySql`；`pageSize` 未传时默认接近全量，业务列表必须给出有效默认值和上限 |
| 业务异常 | `org.dromara.common.core.exception.ServiceException` | 业务阻断直接抛出；全局异常处理统一转响应 |
| 分组校验 | `AddGroup`、`EditGroup`、`QueryGroup` | Controller 用 `@Validated(XxxGroup.class)`；非 Controller 用 `ValidatorUtils` |

## 2. Entity、BO、VO

| 类型 | 约定 |
|---|---|
| Entity | 继承 `BaseEntity`；`@TableId`；按需 `@TableLogic`、`@Version`、`@OrderBy`、`@TableField` |
| BO | 实现 `Serializable`；`@AutoMapper(target = Entity.class, reverseConvertGenerate = false)`；分组校验 |
| VO | 实现 `Serializable`；`@AutoMapper(target = Entity.class)`；Excel、`@Translation`、`@Sensitive` 注解按需添加 |

固定基类 `BaseEntity` 的审计字段：`createDept`、`createBy`、`createTime`、`updateBy`、`updateTime`。不要重复声明，也不要假设它包含 `status`、`delFlag`、`version`。

JSON 字段：

```java
@TableName(value = "biz_xxx", autoResultMap = true)
public class BizXxx extends BaseEntity {
    @TableField(typeHandler = JacksonTypeHandler.class)
    private List<BizItem> items;
}
```

Entity、BO、VO 对同一 JSON 字段使用同构类型；不要一层对象、一层字符串。

## 3. Mapper 与查询

| 需求 | 入口 |
|---|---|
| 简单 CRUD | `BaseMapperPlus<Entity, Vo>` |
| 按 ID 查 VO | `selectVoById` |
| 按 ID 集合查 VO | `selectVoByIds` |
| 条件列表 | `selectVoList(wrapper)` |
| 分页 | `selectVoPage(pageQuery.build(), wrapper)` |
| 批量插入/更新 | `insertBatch`、`updateBatchById`、`insertOrUpdateBatch` |
| Lambda 条件 | `LambdaQueryWrapper` / `Wrappers.lambdaQuery()` |
| 项目查询构造器 | `QueryBuilder.lambda(Entity.class)`，支持可选条件、聚合、子查询 |
| 联表 | `QueryBuilder.lambdaJoin(...)` 或现有 MPJ/XML |

规则：

- 查询条件集中在 `buildQueryWrapper`。
- 空 ID 集合直接返回空结果，禁止退化成全表查询。
- 分页必须在数据库完成。控制器或前端必须保证 `pageSize` 有有限默认值，并对上限做校验；不能依赖未传参时的全量默认值。
- 可空字段显式清空用 `.set(...)`，不要依赖 `NOT_NULL` 更新策略。
- 数据权限注解放在真正执行的 Mapper 方法上，列名与 SQL 别名一致。

## 4. 权限、身份与数据范围

| 能力 | 入口 |
|---|---|
| 接口权限 | `@SaCheckPermission("{module}:{business}:{action}")` |
| 当前登录人 | `LoginHelper` |
| 数据权限 | `@DataPermission({@DataColumn(...)})` |
| 忽略数据权限 | `DataPermissionHelper.ignore(...)` |
| 数据范围模板 | `DataScopeType` |
| 字段脱敏 | `@Sensitive` |
| 字段翻译 | `@Translation` |

功能权限和数据权限是两层。列表、详情、导出、批量写、关联选择都要遵守数据范围；后台任务和异步线程没有登录态，必须显式确定身份。

## 5. 日志、幂等与限流

| 能力 | 注解/入口 | 默认值与边界 |
|---|---|---|
| 操作日志 | `@Log(title, businessType, excludeParamNames, isSaveRequestData, isSaveResponseData)` | 写、导入、导出等关键动作使用；敏感参数排除 |
| 防重复提交 | `@RepeatSubmit(interval, timeUnit, message)` | 默认 5000ms；只用于有重复提交风险的 POST/PUT |
| 限流 | `@RateLimiter(key, time, count, limitType, timeout)` | 默认 60 秒 100 次；按接口/用户/IP 设计 key |
| 分布式锁 | `@Lock4j(keys = {...})` | 锁范围小，不在锁内做远程调用和长事务 |

## 6. 缓存与队列

| 能力 | 入口 |
|---|---|
| Spring Cache | `CacheUtils` |
| Redis 通用操作 | `RedisUtils` |
| 队列 | `QueueUtils` |
| 序列号 | `SequenceUtils` |
| 缓存键 | `CacheNames`、`GlobalConstants` |

缓存要明确 TTL、失效点和数据库提交顺序；不在缓存里放令牌、密码或大对象。实时通知优先 `ruoyi-common-push`，重要消息要落业务记录，不能只依赖内存队列。

## 7. Excel

| 需求 | 入口 |
|---|---|
| 导出 | `ExcelBuilder.of(list, ExportVo.class).sheetName(...).toResponse(response)` |
| 导入 | `ExcelBuilder.read(inputStream, ImportVo.class).validate(true).doRead()` |
| 空模板导出 | `ExcelBuilder.of(new ArrayList<>(), ImportVo.class)` |
| 已有 Excel 模板填充 | `ExcelBuilder.template("excel/模板.xlsx").data(list).toResponse(response)` |
| 结果 | `ExcelResult`、`DefaultExcelListener` |
| 字典转换 | `ExcelDictConvert`、`ExcelEnumConvert` |
| 大整数 | `ExcelBigNumberConvert` |

导入导出使用专用 VO，导出查询条件和数据权限与列表同源，失败行要能反馈。

## 8. 文件与 OSS

系统入口：`SysOssController`、`ISysOssService`、`sys_oss`。

实际接口：

```text
POST   /resource/oss/upload
GET    /resource/oss/list
GET    /resource/oss/listByIds/{ossIds}
GET    /resource/oss/download/{ossId}
GET    /resource/oss/local
DELETE /resource/oss/{ossIds}
```

`/local` 需要 `key` 和 `token` 参数，按服务端生成的本地访问地址使用，不当作公开静态文件路径。业务表保存 `ossId` 或业务附件关联；不要另建文件表。删除记录前明确附件保留、软删和共享引用。

## 9. 加解密

| 能力 | 入口 |
|---|---|
| API 响应加密 | `@ApiEncrypt(response = true)` |
| 字段落库加密 | `@EncryptField` |
| 请求解密 | `CryptoFilter`、`DecryptRequestBodyWrapper` |
| 字段加解密拦截 | `MybatisEncryptInterceptor`、`MybatisDecryptInterceptor` |

传输加密成立条件：前端 `VITE_APP_ENCRYPT === 'true'`、请求头 `isEncrypt === 'true'`、方法为 POST/PUT；后端还要开启 `api-decrypt.enabled`。不是全站默认加密。

## 10. 复用检查

新增公共工具、Service 或注解前，至少检查：

1. `ruoyi-common-core/src/main/java/org/dromara/common/core/utils/`
2. `ruoyi-common-*/src/main/java/org/dromara/common/`
3. 所属业务模块的同名/近义 Service
4. `ruoyi-api` 是否已有跨模块契约
5. 前端 `utils/`、`hooks/`、`components/` 是否已有等价能力

输出时写出选中的 `path#method`，或说明具体缺口；不要只说“已检查”。
