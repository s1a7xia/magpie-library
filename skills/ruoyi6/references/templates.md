# 代码模板

以下模板摘自作者自带的 `ruoyi-demo`（`TestDemo*`），是标准单表形态的骨架参考，不是所有业务的固定答案。字段、契约、权限和流程按当前需求确定；业务形态不标准时，先用 [author-patterns.md](author-patterns.md) 定位作者对应实现，再取最小充分结构。这是后端代码骨架的唯一来源，`backend.md` 只讲规则和选型。默认骨架是不启用数据权限的普通单表；数据权限按“可选片段”追加。片段省略 import，按目标模块现有风格补齐，不要机械复制无法解析的符号。

## Controller

```java
@Validated
@RequiredArgsConstructor
@RestController
@RequestMapping("/<module>/<business>")
public class XxxController extends BaseController {

    private final IXxxService xxxService;

    /**
     * 查询Xxx列表
     */
    @SaCheckPermission("<module>:<business>:list")
    @GetMapping("/list")
    public R<PageResult<XxxVo>> list(@Validated(QueryGroup.class) XxxBo bo, PageQuery pageQuery) {
        return R.ok(xxxService.queryPageList(bo, pageQuery));
    }

    /**
     * 获取Xxx详细信息
     *
     * @param id 主键
     */
    @SaCheckPermission("<module>:<business>:query")
    @GetMapping("/{id}")
    public R<XxxVo> getInfo(@NotNull(message = "主键不能为空")
                            @PathVariable("id") Long id) {
        return R.ok(xxxService.queryById(id));
    }

    /**
     * 新增Xxx
     */
    @SaCheckPermission("<module>:<business>:add")
    @Log(title = "Xxx", businessType = BusinessType.INSERT)
    @RepeatSubmit(interval = 2, timeUnit = TimeUnit.SECONDS, message = "{repeat.submit.message}")
    @PostMapping()
    public R<Void> add(@Validated(AddGroup.class) @RequestBody XxxBo bo) {
        return toAjax(xxxService.insertByBo(bo));
    }

    /**
     * 修改Xxx
     */
    @SaCheckPermission("<module>:<business>:edit")
    @Log(title = "Xxx", businessType = BusinessType.UPDATE)
    @RepeatSubmit
    @PutMapping()
    public R<Void> edit(@Validated(EditGroup.class) @RequestBody XxxBo bo) {
        return toAjax(xxxService.updateByBo(bo));
    }

    /**
     * 删除Xxx
     *
     * @param ids 主键串
     */
    @SaCheckPermission("<module>:<business>:remove")
    @Log(title = "Xxx", businessType = BusinessType.DELETE)
    @DeleteMapping("/{ids}")
    public R<Void> remove(@NotEmpty(message = "主键不能为空")
                          @PathVariable Long[] ids) {
        return toAjax(xxxService.deleteWithValidByIds(Arrays.asList(ids), true));
    }

    /**
     * 导出Xxx列表
     */
    @SaCheckPermission("<module>:<business>:export")
    @Log(title = "Xxx", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(@Validated(QueryGroup.class) XxxBo bo, HttpServletResponse response) {
        List<XxxVo> list = xxxService.queryList(bo);
        ExcelBuilder.of(list, XxxVo.class).sheetName("Xxx").toResponse(response);
    }

}
```

## Service 接口

```java
public interface IXxxService {

    XxxVo queryById(Long id);

    PageResult<XxxVo> queryPageList(XxxBo bo, PageQuery pageQuery);

    List<XxxVo> queryList(XxxBo bo);

    Boolean insertByBo(XxxBo bo);

    Boolean updateByBo(XxxBo bo);

    Boolean deleteWithValidByIds(Collection<Long> ids, Boolean isValid);

}
```

## Service 实现

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
        // 示例为默认 10、上限 100；沿用项目已有分页约定时替换这两个值。
        int size = pageQuery.getPageSize() == null ? 10 : pageQuery.getPageSize();
        if (size < 1 || size > 100) {
            throw new ServiceException("分页大小须在1到100之间");
        }
        pageQuery.setPageSize(size);
        // 最小模板只按 ID 排序；需要交互排序时先校验业务列白名单。
        pageQuery.setOrderByColumn(null);
        pageQuery.setIsAsc(null);
        LambdaQueryWrapper<Xxx> lqw = buildQueryWrapper(bo);
        Page<XxxVo> result = xxxMapper.selectVoPage(pageQuery.build(), lqw);
        return PageResult.build(result.getRecords(), result.getTotal());
    }

    @Override
    public List<XxxVo> queryList(XxxBo bo) {
        return xxxMapper.selectVoList(buildQueryWrapper(bo));
    }

    private LambdaQueryWrapper<Xxx> buildQueryWrapper(XxxBo bo) {
        return QueryBuilder.lambda(Xxx.class)
            .likeIfText(Xxx::getName, bo.getName())
            .orderByAsc(Xxx::getId)
            .build();
    }

    @Override
    public Boolean insertByBo(XxxBo bo) {
        Xxx add = MapstructUtils.convert(bo, Xxx.class);
        validEntityBeforeSave(add);
        boolean flag = xxxMapper.insert(add) > 0;
        if (flag) {
            bo.setId(add.getId());
        }
        return flag;
    }

    @Override
    public Boolean updateByBo(XxxBo bo) {
        Xxx update = MapstructUtils.convert(bo, Xxx.class);
        validEntityBeforeSave(update);
        return xxxMapper.updateById(update) > 0;
    }

    private void validEntityBeforeSave(Xxx entity) {
        // 按业务补齐规则；若无额外规则可移除此方法与调用，不把空方法当作已校验。
        // 唯一性等未定口径按本文 TODO 规则处理，不从 name 字段自动推断唯一键。
    }

    @Override
    public Boolean deleteWithValidByIds(Collection<Long> ids, Boolean isValid) {
        if (CollUtil.isEmpty(ids)) {
            return false;
        }
        if (isValid) {
            List<Xxx> list = xxxMapper.selectByIds(ids);
            if (list.size() != ids.size()) {
                throw new ServiceException("您没有删除权限!");
            }
        }
        return xxxMapper.deleteByIds(ids) > 0;
    }

}
```

## Entity

```java
@Data
@EqualsAndHashCode(callSuper = true)
@TableName("xxx")
public class Xxx extends BaseEntity {

    @Serial
    private static final long serialVersionUID = 1L;

    /**
     * 主键
     */
    @TableId(value = "id")
    private Long id;

    /**
     * 名称
     */
    private String name;

}
```

## BO

```java
@Data
@AutoMapper(target = Xxx.class, reverseConvertGenerate = false)
public class XxxBo implements Serializable {

    @Serial
    private static final long serialVersionUID = 1L;

    /**
     * 主键
     */
    @NotNull(message = "主键不能为空", groups = {EditGroup.class})
    private Long id;

    /**
     * 名称
     */
    @NotBlank(message = "名称不能为空", groups = {AddGroup.class, EditGroup.class})
    private String name;

}
```

## VO

```java
@Data
@ExcelIgnoreUnannotated
@AutoMapper(target = Xxx.class)
public class XxxVo implements Serializable {

    @Serial
    private static final long serialVersionUID = 1L;

    /**
     * 主键
     */
    @ExcelProperty(value = "主键")
    private Long id;

    /**
     * 名称
     */
    @ExcelProperty(value = "名称")
    private String name;

}
```

## Mapper

```java
public interface XxxMapper extends BaseMapperPlus<Xxx, XxxVo> {
}
```

### 可选：数据权限片段

只有业务实体确实有部门、用户或其他归属列，且需求要求按数据范围隔离时才追加。列名必须是真实字段或查询别名；覆盖范围至少包括分页、列表、按 ID 查询、批量查询、更新和删除。删除优先沿用作者模式：先通过带 `@DataPermission` 的查询校验本次 ID 是否都在当前数据范围内，再调用 Mapper 删除；不在 Mapper 上直接重写 `deleteByIds`：

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

    @Override
    @DataPermission({
        @DataColumn(key = "deptName", value = "dept_id"),
        @DataColumn(key = "userName", value = "user_id")
    })
    default XxxVo selectVoById(Serializable id) {
        return selectVoById(id, this.currentVoClass());
    }

    @Override
    @DataPermission({
        @DataColumn(key = "deptName", value = "dept_id"),
        @DataColumn(key = "userName", value = "user_id")
    })
    default List<XxxVo> selectVoList(Wrapper<Xxx> wrapper) {
        return selectVoList(wrapper, this.currentVoClass());
    }

    @Override
    @DataPermission(value = {
        @DataColumn(key = "deptName", value = "dept_id"),
        @DataColumn(key = "userName", value = "user_id")
    }, joinStr = "AND")
    List<Xxx> selectByIds(@Param(Constants.COLL) Collection<? extends Serializable> idList);

    @Override
    @DataPermission({
        @DataColumn(key = "deptName", value = "dept_id"),
        @DataColumn(key = "userName", value = "user_id")
    })
    int updateById(@Param(Constants.ENTITY) Xxx entity);
}
```

`Xxx` 必须有 `deptId`、`userId`（或当前业务真实归属列），Mapper 片段中的列名必须同步替换。服务层按现有作者写法调用这些 Mapper 方法，不要只在列表接口加数据权限。删除时先调用带数据权限的 `selectByIds`/`selectVoById` 校验范围，再执行 `deleteByIds`；如果业务还要求删除前的引用检查，继续放在同一个 Service 事务中。

启用数据权限后，范围校验不能由可选的 `isValid=false` 跳过；该参数只控制额外业务检查。归属可并发变化时，另确认删除时的数据范围约束或锁策略，先查后删本身不保证范围不会变化。

## 使用说明

最小模板只包含 `id`、`name` 及 Entity 的基类审计字段，与前端单表模板对齐；删除默认是物理删除，仅在业务允许时使用。导出接口与 Excel 注解不需要时一起移除。业务校验注释是编写位置提示，不代表已实现业务规则。

| 按需能力 | 必须一起补齐的契约 |
|---|---|
| 排序 | DDL、Entity/BO/VO、前端类型/表单/展示和查询排序规则 |
| 乐观锁 | DDL 默认值、Entity `@Version`、编辑 BO 必填版本、详情 VO、前端类型及隐藏版本字段；编辑提交原版本，更新失败给冲突提示 |
| 创建人翻译 | VO 同时包含来源 `createBy` 和展示 `createByName`，再配置 `@Translation(mapper = "createBy")`；确认查询/映射有来源值，前端按需声明展示字段 |
| 逻辑删除 | DDL 删除标记、Entity `@TableLogic`、实际配置值及唯一索引重建语义 |

- 这套模板来自作者 `TestDemo*`，标准单表沿用同一分层和命名；有主从、状态、导入、异步、外部接入等额外形态时，按其最小充分结构扩展，不为套模板删减业务契约。
- 上面的 `QueryBuilder` 写法演示条件辅助方法；若目标模块已有 `Wrappers.lambdaQuery()` 风格，保持现状，不整体重写。引用时按现有 import 补齐 `QueryBuilder`、`CollUtil` 和实体类型。
- 默认 Mapper 不包含 `@DataPermission`；只有存在真实归属列且需求要求隔离时，再追加“可选：数据权限片段”，并同步实体字段和列名。
- 需要自定义分页时，在 Mapper 加方法并照 `customPageList` 的样子带 `@DataPermission`。
- 以上是骨架；字段、字典、状态、权限前缀按实际需求替换。

## 可选导入

用 `ExcelBuilder.read(..., XxxImportVo.class)` 解析并校验独立 ImportVo，把行数据交给业务 Service 的导入方法。不要在 Controller 转 Entity 后调用无业务约束的 `saveBatch`。

Service 先批量核对文件内重复、库内冲突、关联和归属，再复用普通写入的业务规则并批量持久化。全量成功模式用事务并在校验或持久化失败时抛异常；部分成功模式返回成功/失败行和原因，不能混用全量回滚语义。新增对应 Service 契约和结果 VO，Controller 返回实际导入结果；`excelResult.getAnalysis()` 只描述解析结果。

写法入口见 [backend.md](backend.md#excel-选择) 和 [author-patterns.md](author-patterns.md)，实际批大小与失败策略按业务确定。

## TODO 待确认记录

业务口径没定时，先按当前业务推荐做法完成可运行实现，再用固定格式留下 TODO，保证功能完整、其它功能可测：

```java
// TODO(待确认): <具体业务口径>
// 当前推荐实现: <已实现的行为及业务依据，包含相关校验、约束和页面反馈>
// 后续调整: <业务确认后是否需要调整；需要时调整哪些行为；当前不阻断>
// 确认人: <业务方 / 产品>
```

规则：

- 占位后必须保证能编译、能启动、页面能打开、不阻断其它功能。
- TODO 不是“暂不实现”的许可。能按当前业务判断的默认行为要先实现，再记录待确认点；不得写“先允许重复”“先不校验”“前端不提示”这类绕过业务约束的占位。
- 推荐规则不能覆盖已确认契约。若推荐规则要求唯一性，应同时实现适当的数据库唯一约束与冲突反馈；普通索引和先查后写不能保证并发唯一性。唯一字段组合从业务语义推导，不把名称或部门当通用唯一键。编写迁移脚本与执行数据库变更的授权分开。
- 不能用于掩盖未实现；接口没写、页面没做、数据没接不算 TODO。
- `TODO(待确认)` 是后续业务确认项，不是 `grill` 入口，也不阻断已验证的默认实现进入 `Dev Complete` 或页面验收；若后续确认需要调整，通过 PRD 的 Change Log 和正常修改流程处理。
- 交付时汇总 TODO 清单，写入 `docs/agents/project-state.md` 或 PRD。
