# 代码模板

以下模板摘自作者自带的 `ruoyi-demo`（`TestDemo*`），是标准单表形态的骨架参考，不是所有业务的固定答案。字段、契约、权限和流程按当前需求确定；业务形态不标准时，先用 [author-patterns.md](author-patterns.md) 定位作者对应实现，再取最小充分结构。这是后端代码骨架的唯一来源，`backend.md` 只讲规则和选型。片段省略 import，按目标模块现有风格补齐，不要机械复制无法解析的符号。

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
    public void export(@Validated XxxBo bo, HttpServletResponse response) {
        List<XxxVo> list = xxxService.queryList(bo);
        ExcelBuilder.of(list, XxxVo.class).sheetName("Xxx").toResponse(response);
    }

    /**
     * 导入Xxx
     *
     * @param file 导入文件
     */
    @Log(title = "Xxx", businessType = BusinessType.IMPORT)
    @SaCheckPermission("<module>:<business>:import")
    @PostMapping(value = "/importData", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public R<Void> importData(@RequestPart("file") MultipartFile file) throws Exception {
        ExcelResult<XxxImportVo> excelResult = ExcelBuilder.read(file.getInputStream(), XxxImportVo.class)
            .validate(true)
            .doRead();
        List<Xxx> list = MapstructUtils.convert(excelResult.getList(), Xxx.class);
        xxxService.saveBatch(list);
        // 作者写法：R.ok 的单参数重载把字符串作为提示消息，业务数据为空。
        // 若要把分析结果返回给页面，声明 R<String> 并使用 R.ok(msg, data) 或 R.data(data)。
        return R.ok(excelResult.getAnalysis());
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

    Boolean saveBatch(List<Xxx> list);
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
            .eqIfPresent(Xxx::getDeptId, bo.getDeptId())
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
        // TODO(待确认): 唯一键未定，暂不做重复校验
        // 临时做法: 先允许重复写入，前端不提示
        // 确认人: 业务方 / 产品
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

    @Override
    public Boolean saveBatch(List<Xxx> list) {
        return xxxMapper.insertBatch(list);
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

    /**
     * 排序号
     */
    @OrderBy(asc = false, sort = 1)
    private Integer orderNum;

    /**
     * 版本
     */
    @Version
    private Long version;

    /**
     * 删除标志
     */
    @TableLogic
    private Long delFlag;
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

    /**
     * 版本
     */
    private Long version;
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

    /**
     * 创建时间
     */
    @ExcelRequired
    @DateTimeFormat("yyyy-MM-dd HH:mm:ss")
    @ExcelProperty(value = "创建时间")
    private LocalDateTime createTime;

    /**
     * 创建人账号
     */
    @Translation(type = TransConstant.USER_ID_TO_NAME, mapper = "createBy")
    @ExcelProperty(value = "创建人账号")
    private String createByName;

    /**
     * 版本
     */
    private Long version;
}
```

## Mapper

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

## 使用说明

- 这套模板来自作者 `TestDemo*`，标准单表沿用同一分层和命名；有主从、状态、导入、异步、外部接入等额外形态时，按其最小充分结构扩展，不为套模板删减业务契约。
- 上面的 `QueryBuilder` 写法演示条件辅助方法；若目标模块已有 `Wrappers.lambdaQuery()` 风格，保持现状，不整体重写。引用时按现有 import 补齐 `QueryBuilder`、`CollUtil` 和实体类型。
- 不需要数据权限的表，去掉 Mapper 上的 `@DataPermission` 重写即可，其余保持。
- 需要自定义分页时，在 Mapper 加方法并照 `customPageList` 的样子带 `@DataPermission`。
- 以上是骨架；字段、字典、状态、权限前缀按实际需求替换。

## TODO 占位

业务口径没定时，用固定格式留下 TODO，保证功能能跑通、其它功能可测：

```java
// TODO(待确认): <什么没定>
// 临时做法: <现在的默认行为>
// 确认人: <业务方 / 产品 / 谁>
```

```ts
// TODO(待确认): <什么没定>
// 临时做法: <现在的默认行为>
// 确认人: <业务方 / 产品 / 谁>
```

规则：

- 占位后必须保证能编译、能启动、页面能打开、不阻断其它功能。
- 不能用于掩盖未实现；接口没写、页面没做、数据没接不算 TODO。
- 交付时汇总 TODO 清单，写入 `docs/agents/project-state.md` 或 PRD。
