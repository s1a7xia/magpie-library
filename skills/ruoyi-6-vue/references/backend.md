# 后端开发规范

## 写业务前

先按 `SKILL.md` 的业务判型、复用扫描和业务契约门确认范围，再决定文件。后端重点检查：

1. 现有表、字典、参数、菜单是否已经覆盖数据。
2. `ruoyi-api` 是否已有跨模块查询、消息、配置、文件或工作流接口。
3. `ruoyi-common-*` 是否已有校验、转换、查询、分页、Excel、缓存、锁、加解密等能力。
4. `ruoyi-system` 和 `ruoyi-demo` 是否已有同类系统能力或框架示例。
5. 当前业务模块是否只是需要新增字段、状态或接口，而不是新增一整套模块。

找到可复用能力后，确认方法语义、权限、事务和异常行为再使用。不要仅因为类名相似就复用，也不要为了少改现有代码而复制一份。

取样顺序固定为：目标模块最近似实现 -> 公共基础模块约定 -> 后端生成模板 -> 通用 Spring / MyBatis-Plus 习惯。模板位于 `ruoyi-modules/ruoyi-gen/src/main/resources/fm/java/` 和 `fm/xml/`；它是骨架，不是目标模块的事实源。

## 分层

```text
XxxController
  -> IXxxService
  -> XxxServiceImpl
  -> XxxMapper extends BaseMapperPlus<Xxx, XxxVo>
```

- Controller 只做参数、校验、权限、日志、响应。
- Service 做业务校验、编排、事务、缓存和并发。
- 不新增 DAO/Repository 层。
- 跨模块调用走 `ruoyi-api`，不注入其他模块的 ServiceImpl、Mapper 或 Entity。
- 标准新增可对齐生成器的 `queryById`、`queryPageList`、`queryList`、`insertByBo`、`updateByBo`、`deleteWithValidByIds`，再补目标模块已有的数据权限、联表、缓存、导入导出和删除校验。

## 复用边界

### 跨模块 API

以下是 6.x 框架提供的稳定跨模块入口；调用前仍要读当前 checkout 的接口定义，确认实际方法和 DTO。

| 领域 | 入口 | 典型用途 |
|---|---|---|
| 用户 | `ruoyi-api/.../system/api/UserService` | 按 ID 取用户、批量取昵称、按角色/部门/岗位取用户 |
| 部门 | `DeptService` | 部门名称、负责人、部门列表 |
| 角色 | `RoleService` | 批量角色名称 |
| 岗位 | `PostService` | 批量岗位名称 |
| 消息 | `MessageService` | `sendMessage` 实时推送；`publishMessage` / `publishAll` 可落库供消息盒子 |
| 消息 | `MessageService` | 单用户、多用户和广播消息 |
| 文件 | `OssService` | 按 OSS ID 取地址或文件信息 |
| 工作流 | `WorkflowService`、`WorkflowTaskQueryService` | 发起、办理、撤回、驳回、状态和流程变量 |

业务模块只能依赖接口，不依赖实现类。需要新增跨模块能力时，先判断现有接口能否扩展；不要为了一个调用方复制系统模块的 Entity、Mapper 或 ServiceImpl。

### 公共技术与系统能力

| 需求 | 先看 |
|---|---|
| 响应、分页、异常、校验 | `ruoyi-common-core` 的 `R`、`PageResult`、`ServiceException`、`ValidatorUtils` |
| 数据访问 | `ruoyi-common-mybatis` 的 `BaseEntity`、`BaseMapperPlus`、`PageQuery`、`QueryBuilder` |
| 对象转换 | `MapstructUtils`；树结构用 `TreeBuildUtils` |
| 登录身份与权限 | `LoginHelper`、`@SaCheckPermission`、`@DataPermission` |
| 缓存、队列、锁 | `ruoyi-common-redis` 的 `CacheUtils`、`RedisUtils`、`QueueUtils` |
| Excel、文件、加解密 | `ruoyi-common-excel`、`ruoyi-common-oss`、`ruoyi-common-encrypt` |
| 翻译、脱敏 | `ruoyi-common-translation`、`ruoyi-common-sensitive` |
| 消息、邮件、短信、社交、MQTT | 对应 `ruoyi-common-*` 现有客户端和配置 |
| 定时任务、工作流、AI、搜索 | 对应 `ruoyi-modules/ruoyi-*` 现有 Bean 和调用链 |

需要字符串、集合、对象、JSON、日期、树、文件、IP 或 SQL 工具时，先读 [utils.md](utils.md)，再按当前源码核对方法签名；不要另写一套。

公共工具只放稳定、跨模块复用且无业务归属的能力。只服务一个业务的规则留在该业务 Service；不要为了“以后可能复用”把它提升为通用层。

### 公共基础模块改动

修改 `ruoyi-common-*` 或供多个模块使用的公共 API 时，先搜索接口、实现类和全部调用点，默认保持公开方法签名、泛型、返回值和异常语义兼容。新增能力优先扩展已有入口或薄包装，确实需要改签名时同步所有调用方并重新编译受影响模块；只改注释或文档时，不重排 import、不格式化整个文件、不改代码逻辑。

### 业务模块不是模板

- `ruoyi-demo` 是框架示例，可复制文件结构和调用骨架。
- `ruoyi-system` 是系统能力来源，可调用 `ruoyi-api` 暴露的接口。
- 目标项目的其它业务模块只用于了解已有字段、权限和集成约束，不复制其分层、命名、工具类、请求封装或页面组件。
- 如果当前业务模块已有用户选择、状态、文件或消息实现，先确认能否扩展现有接口；不能复用才补最小缺口。

## 最小完整落点

新增一个普通单表业务时，按以下文件闭环，不要只写 Controller：

```text
ruoyi-modules/ruoyi-<module>/src/main/java/.../
├─ controller/XxxController.java
├─ service/IXxxService.java
├─ service/impl/XxxServiceImpl.java
├─ mapper/XxxMapper.java
├─ domain/Xxx.java
├─ domain/bo/XxxBo.java
└─ domain/vo/XxxVo.java

plus-ui/src/
├─ api/<module>/<business>/types.ts
├─ api/<module>/<business>/index.ts
└─ views/<module>/<business>/index.vue
```

字段、查询条件、导入导出和权限至少同时出现在上述链路中。先读 `TestDemo*` 的完整实现，再按业务命名替换。

## Controller 模板

```java
@Validated
@RequiredArgsConstructor
@RestController
@RequestMapping("/<module>/<business>")
public class XxxController extends BaseController {

    private final IXxxService xxxService;

    @SaCheckPermission("<module>:<business>:list")
    @GetMapping("/list")
    public R<PageResult<XxxVo>> list(@Validated(QueryGroup.class) XxxBo bo, PageQuery pageQuery) {
        return R.ok(xxxService.queryPageList(bo, pageQuery));
    }

    @SaCheckPermission("<module>:<business>:query")
    @GetMapping("/{id}")
    public R<XxxVo> getInfo(@NotNull @PathVariable Long id) {
        return R.ok(xxxService.queryById(id));
    }

    @SaCheckPermission("<module>:<business>:add")
    @Log(title = "<业务名>", businessType = BusinessType.INSERT)
    @RepeatSubmit
    @PostMapping
    public R<Void> add(@Validated(AddGroup.class) @RequestBody XxxBo bo) {
        return toAjax(xxxService.insertByBo(bo));
    }

    @SaCheckPermission("<module>:<business>:edit")
    @Log(title = "<业务名>", businessType = BusinessType.UPDATE)
    @RepeatSubmit
    @PutMapping
    public R<Void> edit(@Validated(EditGroup.class) @RequestBody XxxBo bo) {
        return toAjax(xxxService.updateByBo(bo));
    }

    @SaCheckPermission("<module>:<business>:remove")
    @Log(title = "<业务名>", businessType = BusinessType.DELETE)
    @DeleteMapping("/{ids}")
    public R<Void> remove(@NotEmpty @PathVariable Long[] ids) {
        return toAjax(xxxService.deleteWithValidByIds(Arrays.asList(ids), true));
    }
}
```

导入、导出、状态变更和排序按现有同类接口追加，不把文件流塞进普通 JSON 响应。

## 命名

```text
XxxController
IXxxService
XxxServiceImpl
XxxMapper
Xxx
XxxBo
XxxVo
```

Controller 方法沿用 `list`、`getInfo`、`add`、`edit`、`remove`、`export`、`importData`、`changeStatus`、`updateSort`。Service 沿用 `queryById`、`queryPageList`、`queryList`、`insertByBo`、`updateByBo`、`deleteWithValidByIds`。

## Entity / BO / VO

- Entity 继承 `BaseEntity`。基类只有 `createDept`、`createBy`、`createTime`、`updateBy`、`updateTime`。
- 主键用 `@TableId`；逻辑删除、乐观锁、排序分别按需用 `@TableLogic`、`@Version`、`@OrderBy`。
- JSON 字段用 `@TableName(autoResultMap = true)` + `@TableField(typeHandler = JacksonTypeHandler.class)`，Entity/BO/VO 类型同构。
- BO 用 `@AutoMapper(target = Xxx.class, reverseConvertGenerate = false)`；新增/修改用 `AddGroup` / `EditGroup`。
- VO 用 `@AutoMapper(target = Xxx.class)`；导出、翻译、脱敏按需加现有注解。
- 修改映射后实际编译，让 MapStruct 生成实现。

## Service 与 Mapper 模板

```java
@RequiredArgsConstructor
@Service
public class XxxServiceImpl implements IXxxService {

    private final XxxMapper xxxMapper;

    @Override
    public XxxVo queryById(Long id) {
        return xxxMapper.selectVoById(id);
    }

    @Override
    public PageResult<XxxVo> queryPageList(XxxBo bo, PageQuery pageQuery) {
        Page<XxxVo> page = xxxMapper.selectVoPage(pageQuery.build(), buildQueryWrapper(bo));
        return PageResult.build(page.getRecords(), page.getTotal());
    }

    @Override
    public Boolean insertByBo(XxxBo bo) {
        Xxx entity = MapstructUtils.convert(bo, Xxx.class);
        validEntityBeforeSave(entity);
        return xxxMapper.insert(entity) > 0;
    }

    @Override
    public Boolean updateByBo(XxxBo bo) {
        Xxx entity = MapstructUtils.convert(bo, Xxx.class);
        validEntityBeforeSave(entity);
        return xxxMapper.updateById(entity) > 0;
    }

    private LambdaQueryWrapper<Xxx> buildQueryWrapper(XxxBo bo) {
        LambdaQueryWrapper<Xxx> lqw = Wrappers.lambdaQuery();
        lqw.like(StringUtils.isNotBlank(bo.getName()), Xxx::getName, bo.getName());
        return lqw;
    }
}
```

Mapper 继承 `BaseMapperPlus<Xxx, XxxVo>`；需要行级隔离时沿用 `@DataPermission`，列名必须与表字段和查询别名一致：

```java
public interface XxxMapper extends BaseMapperPlus<Xxx, XxxVo> {
    @Override
    @DataPermission({
        @DataColumn(key = "deptName", value = "dept_id"),
        @DataColumn(key = "userName", value = "user_id")
    })
    default <P extends IPage<XxxVo>> P selectVoPage(IPage<Xxx> page, Wrapper<Xxx> wrapper) {
        return selectVoPage(page, wrapper, this.currentVoClass());
    }
}
```

## Controller 与接口

标准路径为 `/{module}/{business}`，权限字符为 `{module}:{business}:{action}`。

```text
GET    /list                 R<PageResult<Vo>>
GET    /{id}                 R<Vo>
POST   /                     R<Void>
PUT    /                     R<Void>
DELETE /{ids}                R<Void>
POST   /export               文件流
POST   /importData           R<Void>
PUT    /changeStatus         R<Void>
PUT    /updateSort            R<Void>
```

- 普通单表列表：`list(@Validated(QueryGroup.class) XxxBo bo, PageQuery pageQuery)`。
- 树表列表：`R<List<XxxVo>> list(XxxBo bo)`，前端建树。
- 新增用 `AddGroup`，修改用 `EditGroup`，路径批量 ID 用 `@NotEmpty`。
- 新增/修改/删除用 `toAjax(...)`；业务失败抛 `ServiceException`。
- 写操作加 `@Log`；有重复提交风险的 POST/PUT 按需加 `@RepeatSubmit`。
- 普通表导出常用 `POST /export`，树表常用 `GET /export`；按同模块现有接口写。

分页使用 `PageQuery.build()`，但 `PageQuery` 未传 `pageSize` 时默认接近全量。业务列表必须给出有限默认值并校验上限，不能直接依赖这个默认值。

## 查询与 Mapper

- 继承 `BaseMapperPlus<Xxx, XxxVo>`，优先用 `selectVoById`、`selectVoByIds`、`selectVoList`、`selectVoPage`。
- 简单条件用 `LambdaQueryWrapper` 或 `QueryBuilder`；需要链式查询和更新时，先识别本地增强入口：
  - `mapper.lambda()`：`eqIfText`、`likeIfText`、`betweenParams`、`inIfNotEmpty`、`voOne`、`voList`、`voPage`、`update`、`deleteCount`。
  - `QueryBuilder.lambda(Entity.class)`：适合 Service 内构造可复用 Wrapper，最后 `.build()`。
  - `QueryBuilder.lambdaJoin("u", Entity.class)`：多表联查、`selectAs`、`leftJoin`、别名条件、`list`/`page`/`count`。
- 查询条件集中在 `buildQueryWrapper`；可选条件先判空。
- 老模块已有 `Wrappers.lambdaQuery()` 或显式 `StringUtils.isNotBlank(...)` 时可增量保持，不与新写法混改。
- 空 ID 集合直接返回空结果，禁止生成无条件全表查询。
- 分页在数据库完成；关联展示批量查询或 `@Translation`，避免 N+1。
- `PageQuery` 支持 `orderByColumn`、`isAsc` 的多字段排序，前端 `ascending` / `descending` 会自动转成 `asc` / `desc`；排序字段仍要防止任意列注入。

### 数据权限

- `@DataPermission` 主要标在 Mapper 层；列表、详情、更新、删除都要覆盖，不能只给列表加。
- 方法级注解优先于类级；XML / MPJ 联表使用表别名时，`@DataColumn` 的 `value` 必须写 `别名.列名`。
- 需要临时绕过时，`DataPermissionHelper.ignore(...)` 或 `@InterceptorIgnore(dataPermission = "true")` 只包最小范围，并说明原因。
- 功能权限只控制“能否调用”，数据权限控制“能看到/操作哪些数据”，两者不能互相替代。

## Service、事务与并发

- Service 返回领域结果、`PageResult`、`List` 或 `Boolean`，不返回 `R<T>`。
- 多表写入在公共方法上用 `@Transactional(rollbackFor = Exception.class)`；单表简单写入不机械加事务。
- 唯一性优先数据库唯一约束；并发更新用 `@Version`、条件更新或现有锁，并检查影响行数。
- 当前用户、部门、账号用 `LoginHelper`；后台任务和异步线程显式确定身份，不强依赖登录态。
- 可空字段要清空时用 `.set(..., null)`，不依赖 `NOT_NULL` 更新策略。
- `DataPermissionHelper.ignore` 只包最小范围并写明原因。
- 批量写入和删除要检查影响行数；空 ID 集合直接返回，不生成无条件 SQL。

## 权限与复用

- 功能权限只控制能否调用；数据范围由 `@DataPermission` / `DataScopeType` 控制。
- 字段脱敏在 VO 或序列化出口做，不在前端隐藏替代。
- `@Sensitive` 标在返回 VO，不标 Entity；它只影响序列化响应，不改变数据库值。需要查看完整值时使用受控接口，不取消整个 VO 的脱敏。
- 用户、部门、字典、OSS 等展示字段优先用 `@Translation`；大列表、导出和远程翻译使用批量能力或缓存，避免 N+1。
- 写公共工具或 Service 前，先查 `ruoyi-common-core`、相关 `ruoyi-common-*`、所属模块 Service 和 `ruoyi-api`。
- 公共方法只放稳定、跨模块能力；单模块业务规则留在业务模块。
- 用户、部门、角色、岗位、字典、参数、文件、消息、工作流都有现有入口时，不得另建同名查询表或平行 Service。
- 外部接入、批处理或状态流转逻辑留在业务 Service 或适配器，不塞进 Controller、Entity 或前端。

## 注释与公共 API

- 新增或修改类、接口、BO/VO 字段、Mapper 默认方法和 Service/Controller 的公共方法时，按同包现有风格补简短 JavaDoc，说明做什么和关键参数语义；不复述显而易见的实现，不给 `void` 写 `@return`。
- 私有方法只在业务规则、算法或字段映射不直观时加注释；覆写框架方法且语义已明确时，不强行重复注释。
- 只补注释时不改实现、不重排 import、不格式化整个文件；公共 API 改动优先保证调用方兼容，确有签名变化时同步所有调用点并编译受影响模块。

## 常见错误

| 写法 | 问题 | 正确做法 |
|---|---|---|
| Controller 注入 Mapper 并直接查询 | 绕过业务校验、事务和数据权限 | Controller 只调 Service |
| Service 返回 `R<T>` | 响应层泄漏到业务层 | 返回 `PageResult`、`VO`、`List` 或 `Boolean` |
| 新增 `XxxDao` | 与当前分层重复 | 沿用 `BaseMapperPlus` |
| 公共 API 直接改签名 | 其它模块编译或运行行为被破坏 | 先查全部调用点；优先扩展，不改已发布签名 |
| 只补注释却重排全文件 | diff 噪声掩盖真实改动 | 不做无关格式化，只改注释 |
| 只加 `@SaCheckPermission` 不加菜单权限 | 菜单可见但接口或按钮不一致 | 同步 `sys_menu.perms` 和前端 `v-hasPermi` |
| 分页不传 `pageSize` | `PageQuery.DEFAULT_PAGE_SIZE` 为 `Integer.MAX_VALUE` | 列表接口和页面显式设置有限默认值并校验上限 |
| 复制其它业务模块的 Service/Mapper | 形成第二套用户、权限或文件实现 | 先查 `ruoyi-api` 和现有公共能力，必要时扩展现有接口 |
| 为单模块需求新增通用工具 | 公共层膨胀，调用方难收敛 | 留在业务模块；稳定跨模块后再提升 |

## 常用能力

| 能力 | 入口 |
|---|---|
| 响应、分页、异常 | `R`、`PageResult`、`ServiceException` |
| 分组校验 | `AddGroup`、`EditGroup`、`QueryGroup`、`ValidatorUtils` |
| 数据访问 | `BaseEntity`、`BaseMapperPlus`、`PageQuery`、`QueryBuilder` |
| 权限与身份 | `@SaCheckPermission`、`@DataPermission`、`LoginHelper` |
| 日志、幂等、限流 | `@Log`、`@RepeatSubmit`、`@RateLimiter` |
| 缓存与锁 | 通用 Redis 读写用 `RedisUtils`；与 `@Cacheable`/`@CacheEvict` 联动用 `CacheUtils`；锁用 `@Lock4j` |
| Excel | `ExcelBuilder`、`ExcelResult`、Fesod 注解、`DefaultExcelListener` |
| 文件 | `/resource/oss/upload`、`sys_oss`、`OssClient` |
| 加解密 | `@ApiEncrypt`、`@EncryptField`、`CryptoFilter` |
| 翻译、脱敏 | `@Translation`、`TransConstant`、`@Sensitive`、`SensitiveStrategy` |
| 消息 | `MessageService.sendMessage` 只实时推送；消息盒子用 `publishMessage` / `publishAll`（符合消息/通知类型时落库再推送）；低层实时推送用 `PushHelper`，不负责持久化 |

加密不是全站默认：前端 `VITE_APP_ENCRYPT=true`、请求头 `isEncrypt: 'true'`（`request.ts` 按字符串判断）、方法为 POST/PUT，后端 `api-decrypt.enabled=true` 同时成立才处理请求解密。现有 `login.ts` / `system/user` 中可能使用布尔 `true`，以当前拦截器实现和实际请求结果为准，不能只凭旧示例。

### 缓存选择

- 通用 Redis 读写：`RedisUtils`。
- 需要和 Spring Cache、`@Cacheable`、`@CacheEvict` 使用同一套缓存管理：`CacheUtils`。
- 缓存名使用 `CacheNames`，格式为 `cacheNames#ttl#maxIdleTime#maxSize#local`；同一个缓存名不要在不同位置使用不同参数。
- 写操作命中已有缓存模块时，同步处理失效，不能只改数据库。

### Excel 选择

- 导入使用独立 `ImportVo`，不复用数据库 Entity；建议 `@ExcelIgnoreUnannotated`、`ExcelDictConvert` / `ExcelEnumConvert`、Validator 校验。
- 默认 `failFast=true`；需要收集全部错误行时用 `.failFast(false)` 和自定义 `ExcelListener` / `DefaultExcelListener`。
- 导出按需使用 `@CellMerge`、`@ExcelRequired`、`@ExcelNotation`、`DropDownOptions`、`.merge()`、`.options(...)`、`.zip(...)`、模板导出和 `ExcelBuilder.writer()` 多 sheet。
- 本地示例优先读 `TestExcelController`、`ExportExcelServiceImpl`、`ExportDemoListener`、`TestDemoImportVo`，不要复制整篇 Fesod 文档。

### 接口放行与国际化

- 单个接口放行优先 `@SaIgnore`，不要为一个接口扩大 `security.excludes`；放行接口不能依赖登录用户上下文。
- 前端已有 `zh_CN`、`en_US`，请求头使用 `Content-Language`；后端可用 `MessageUtils.message("code")`，校验消息可用 `{code}`。

## 检查

- [ ] 没有 DAO 层，Controller 不直接调 Mapper，Service 不返回 `R`。
- [ ] Entity/BO/VO、查询、分页、空集合和映射正确。
- [ ] 权限字符、数据范围、日志、幂等和事务按需完整。
- [ ] 已检查 `ruoyi-api`、`ruoyi-common-*`、`ruoyi-system` 和框架示例，列出实际复用入口。
- [ ] 鉴权、响应、转换使用现有封装；没有复制业务模块或另造第二套公共能力。
