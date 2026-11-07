# RuoYi-Vue-Plus 6.0 CRUD 落地规范

用于新增或修改普通单表、树表 CRUD。本项目没有代码生成器操作环节；`ruoyi-gen` 的 FreeMarker 模板只作为结构清单，最终代码由 AI 参考同模块真实实现直接编写。

## 1. 先定字段契约

写代码前逐字段确认：

| 项目 | 必须说明 |
|---|---|
| 标识 | 表名、模块名、业务名、类名、权限前缀 |
| 类型 | 数据库类型、Java 类型、TypeScript 类型、是否大整数 |
| 查询 | 是否出现在搜索区、查询方式（EQ/LIKE/BETWEEN 等） |
| 录入 | 新增/编辑是否出现、校验分组、必填、长度、格式 |
| 列表 | 是否展示、字典、状态、排序、脱敏、翻译 |
| 能力 | 是否需要导出、状态切换、树结构、上传、导入 |

字段契约不清时先补齐，不边写边猜。数据库字段、Entity/BO/VO、前端类型和页面标签使用同一业务术语。

## 2. 标准文件链

```text
后端模块
├─ controller/XxxController.java
├─ domain/Xxx.java
├─ domain/bo/XxxBo.java
├─ domain/vo/XxxVo.java
├─ mapper/XxxMapper.java
└─ service/{IXxxService.java,impl/XxxServiceImpl.java}

plus-ui
├─ api/<module>/<business>/index.ts
├─ api/<module>/<business>/types.ts
└─ views/<module>/<business>/index.vue
```

- 普通 CRUD 使用分页 `PageResult`；树表列表使用 `List<Vo>` 并在前端构建树。
- 不新增 DAO 层；`ServiceImpl` 直接依赖 Mapper。
- 先写 `types.ts` 与 `api/index.ts`，再写页面；后端字段和前端类型同步落地。

## 3. 对象与查询

- Entity 继承模块现有 `BaseEntity`，按需加 `@TableName`、`@TableId`、`@TableLogic`、`@Version`。
- BO 使用 `@AutoMapper(target = Entity.class, reverseConvertGenerate = false)`；新增/修改字段用 `AddGroup` / `EditGroup`。
- VO 使用 `@AutoMapper(target = Entity.class)`；导出字段用现有 Fesod 注解，展示名称用 `@Translation`。
- 查询条件集中在 `buildQueryWrapper`；可选条件先判空，模糊查询只用于明确允许的字段。
- 分页使用 `pageQuery.build()` 和 `selectVoPage`，结果用 `PageResult.build(records, total)`。

## 4. 普通 CRUD 顺序

1. 建表/增量 SQL，补字典、参数、菜单和按钮权限。
2. 写 Entity、BO、VO、Mapper、Service 接口与实现。
3. 写 Controller：列表、详情、新增、修改、删除；按需加导出、导入、状态、排序。
4. 写前端 `types.ts`、`api/index.ts`。
5. 写页面：搜索、工具栏、表格、分页、弹窗表单、权限按钮。
6. 编译后端、构建前端；页面验收另行发起。

## 5. 树表 CRUD

- Entity 增加 `parentId`；VO 增加 `children`，前端用现有 `handleTree`/`TreePanel` 构建树。
- 列表使用 `row-key="id"`、`:tree-props="{ children: 'children', hasChildren: 'hasChildren' }"`。
- 新增子节点时设置父级；编辑时禁止选择自身或后代作为父级。
- 删除前检查子节点、关联数据和业务状态；不要只依赖前端确认框。
- 树的展开、搜索、空节点和加载态沿用现有 demo，不另造树组件。

## 6. 菜单、字典与权限

- 菜单和按钮权限写入可执行 SQL：`sys_menu` 的 `perms` 与 Controller 的 `@SaCheckPermission`、前端 `v-hasPermi` 三处一致。
- 字典类型和字典值写入 `sys_dict_type` / `sys_dict_data`；前后端使用同一 `dict_value`。
- 可变阈值、开关、周期优先 `sys_config`；不要为配置建业务表。
- 新菜单要确认父级、路由名、组件路径、排序、可见性和缓存策略；路由名由后端 `routeName + menuId` 生成，不要手工假设组件名必须等于完整路由名。

## 7. 页面实现要点

- 页面壳复用 `app-container`、`search-panel`、`table-panel`、`toolbar-shell`、`right-toolbar`。
- 搜索区使用 `el-form` + `queryParams`；查询重置用 `useSearchReset`。
- 表格使用 `el-table` + `pagination`；选择用 `useTableSelection`；加载态用 `useLoading`。
- 弹窗使用 `useFormDialog`：新增 `openDialog` 会重置，编辑先拉详情再 `showDialog`。
- 字典用 `useDict` / `DictTag`；权限用 `v-hasPermi` 或 `checkPermi`。
- 状态列用语义化 `el-tag` 或字典标签；不要自造一套颜色含义。

## 8. 检查清单

- [ ] 表、Entity、BO、VO、前端类型、字典值和页面标签一致。
- [ ] 普通表使用分页，树表返回列表并由前端建树。
- [ ] 查询条件有空值保护，空 ID 集合不会退化成全表查询。
- [ ] 新增/修改分组校验、唯一性、事务和并发处理明确。
- [ ] 菜单权限、按钮权限、接口权限、数据范围四处对齐。
- [ ] 编辑能正确回显；提交失败保留输入并恢复 loading。
- [ ] 删除有二次确认和后端业务校验；测试数据可清理。
- [ ] 页面可见改动在 `page-acceptance` 阶段做真实浏览器验收。
