# 后端开发规范

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
- 简单条件用 `LambdaQueryWrapper` 或 `QueryBuilder`；复杂联表再沿用 MPJ/XML。
- 查询条件集中在 `buildQueryWrapper`；可选条件先判空。
- 空 ID 集合直接返回空结果，禁止生成无条件全表查询。
- 分页在数据库完成；关联展示批量查询或 `@Translation`，避免 N+1。

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
- 写公共工具或 Service 前，先查 `ruoyi-common-core`、相关 `ruoyi-common-*`、所属模块 Service 和 `ruoyi-api`。
- 公共方法只放稳定、跨模块能力；单模块业务规则留在业务模块。

## 常见错误

| 写法 | 问题 | 正确做法 |
|---|---|---|
| Controller 注入 Mapper 并直接查询 | 绕过业务校验、事务和数据权限 | Controller 只调 Service |
| Service 返回 `R<T>` | 响应层泄漏到业务层 | 返回 `PageResult`、`VO`、`List` 或 `Boolean` |
| 新增 `XxxDao` | 与当前分层重复 | 沿用 `BaseMapperPlus` |
| 只加 `@SaCheckPermission` 不加菜单权限 | 菜单可见但接口或按钮不一致 | 同步 `sys_menu.perms` 和前端 `v-hasPermi` |
| 分页不传 `pageSize` | `PageQuery` 默认接近全量 | 列表接口和页面设置有限默认值 |

## 常用能力

| 能力 | 入口 |
|---|---|
| 响应、分页、异常 | `R`、`PageResult`、`ServiceException` |
| 分组校验 | `AddGroup`、`EditGroup`、`QueryGroup`、`ValidatorUtils` |
| 数据访问 | `BaseEntity`、`BaseMapperPlus`、`PageQuery`、`QueryBuilder` |
| 权限与身份 | `@SaCheckPermission`、`@DataPermission`、`LoginHelper` |
| 日志、幂等、限流 | `@Log`、`@RepeatSubmit`、`@RateLimiter` |
| 缓存与锁 | `CacheUtils`、`RedisUtils`、`@Lock4j` |
| Excel | `ExcelBuilder`、`ExcelResult`、Fesod 注解 |
| 文件 | `/resource/oss/upload`、`sys_oss`、`OssClient` |
| 加解密 | `@ApiEncrypt`、`@EncryptField`、`CryptoFilter` |

加密不是全站默认：前端 `VITE_APP_ENCRYPT=true`、请求头 `isEncrypt=true`、方法为 POST/PUT，后端 `api-decrypt.enabled=true` 同时成立才处理请求解密。

## 检查

- [ ] 没有 DAO 层，Controller 不直接调 Mapper，Service 不返回 `R`。
- [ ] Entity/BO/VO、查询、分页、空集合和映射正确。
- [ ] 权限字符、数据范围、日志、幂等和事务按需完整。
- [ ] 鉴权、响应、转换使用现有封装；公共能力没有重复实现。
