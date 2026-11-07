# plus-ui 现有组件与 hooks 使用规范

本文件按“场景 → 入口 → 用法 → 边界”记录 plus-ui 现有能力。新增页面前先找这里或同模块兄弟页面，不要另造平行组件。

## 1. 页面外壳

| 结构 | 现有类或组件 | 用法 |
|---|---|---|
| 页面容器 | `.p-2.app-container` | 纵向 flex、12px gap；不要再套一层大卡片 |
| 筛选卡片 | `.search-wrap` + `.search-panel` | 可配 `is-collapsed` 和 `.search-panel-toggle` |
| 表格卡片 | `.table-panel` | 承载工具栏、表格、分页 |
| 工具栏 | `.toolbar-shell`、`.table-heading`、`.toolbar-actions` | `toolbar-actions` 保持单行，必要时内部横向滚动 |
| 表格 | `.data-table` | 行操作 `is-link` 按钮已有统一 28–32px 规格 |
| 分页 | `<pagination>` | 全局注册的 `Pagination` 组件 |

标准顺序：

```text
p-2 app-container
  search-wrap / search-panel
  table-panel
    toolbar-shell
    el-table.data-table
    pagination
  el-dialog / el-drawer
```

## 2. 基础组件

| 组件 | 路径 | 关键 props / 事件 | 边界 |
|---|---|---|---|
| `Pagination` | `components/Pagination/index.vue` | `total`、`page`、`limit`、`pageSizes`、`layout`、`hidden`、`autoScroll`、`background`、`@pagination` | 用 `v-model:page`、`v-model:limit`；`autoScroll` 默认开启；`float` 已不控制布局；不要手写第二套分页 |
| `RightToolbar` | `components/RightToolbar/index.vue` | `showSearch`、`columns`、`search`、`storageKey`、`@queryTable` | 列显隐需要稳定的列 `key`；刷新事件接列表查询 |
| `DictTag` | `components/DictTag/index.vue` | `options`、`value`、`showValue`、`separator` | 先通过 `useDict` 取字典；未知值按现有回显策略处理 |
| `TreePanel` | `components/TreePanel/index.vue` | `title`、`data`、`nodeKey`、`treeProps`、`collapsed`、`contentSpan`、`@node-click` | 基于 `el-tree-v2`；由父页面监听折叠状态并调整内容列宽，组件不自动让宽 |
| `UserSelect` | `components/UserSelect/index.vue` | `modelValue`、`multiple`、`data`/`userIds`、`@confirmCallBack`；暴露 `open()`、`close()` | 通过 ref 调用 `open()`；内部使用 `vxe-table` 和系统用户 API；不要复制选择器 |
| `RoleSelect` | `components/RoleSelect/index.vue` | `modelValue`、`multiple`、`data`、`@confirmCallBack`；暴露 `open()`、`close()` | 通过 ref 调用 `open()`；角色数据走系统 API |
| `FileUpload` | `components/FileUpload/index.vue` | `modelValue`、`limit`、`fileSize`、`fileType`、`disabled`、`ossExt` | 值是逗号分隔的 `ossId`；上传接口是 `/resource/oss/upload` |
| `ImageUpload` | `components/ImageUpload/index.vue` | `modelValue`、`limit`、`fileSize`、`fileType`、`compressSupport`、`deleteOnRemove` | 值是 `ossId` 串；`deleteOnRemove=true`（默认）时删除会调用 `delOss` |
| `ImagePreview` | `components/ImagePreview/index.vue` | `src`、`width`、`height` | 多图用逗号分隔；只用于预览 |
| `Editor` | `components/Editor/index.vue` | `modelValue`、`height`、`minHeight`、`readOnly`、`type`、`fileSize`、`videoSize` | `url` 模式存储 `oss://<ossId>`，展示前需解析 |
| `IconSelect` | `components/IconSelect/index.vue` | 由菜单/图标场景复用 | 不要另造图标选择器 |

## 3. hooks

| hook | 路径 | 返回/作用 | 用法 |
|---|---|---|---|
| `useLoading` | `hooks/async/useLoading.ts` | `loading`、`setLoading`、`withLoading` | 列表和详情用 `withLoading` 包住异步调用 |
| `useDialogState` | `hooks/dialog/useDialogState.ts` | `dialog`、`openDialog`、`closeDialog`、`toggleDialog`、`setTitle` | 只管理弹窗显隐和标题 |
| `useFormDialog` | `hooks/dialog/useFormDialog.ts` | `openDialog` 重置表单，`showDialog` 保留回填 | 新增用 `openDialog`；编辑先拉详情、`Object.assign(form, data)`，再 `showDialog` |
| `useSearchToggle` | `hooks/form/useSearchToggle.ts` | `showSearch`、`toggleSearch`、`setShowSearch` | 配 `RightToolbar` 或筛选区折叠 |
| `useSearchReset` | `hooks/form/useSearchReset.ts` | `resetQuery` | 重置表单、页码；通过 `afterReset` 重新查询 |
| `useDateRangeQuery` | `hooks/form/useDateRangeQuery.ts` | `dateRange`、`applyDateRange`、`resetDateRange` | 将范围写入 `params.beginXxx/endXxx`；重置时同时清空 |
| `useTableSelection` | `hooks/table/useTableSelection.ts` | `ids`、`selectedRows`、`single`、`multiple`、`handleSelectionChange`、`clearSelection` | `single` 表示“不是恰好一条”，`multiple` 表示“零条”；按钮禁用直接用它 |
| `useTableSortQuery` | `hooks/table/useTableSortQuery.ts` | `handleSortChange`、`resetSort` | 把 `prop/order` 写入 `orderByColumn/isAsc`，再查询 |
| `useFullHeightTable` | `hooks/table/useFullHeightTable.ts` | 自动调整 `.table-panel .data-table` 高度 | 由 `AppMain.vue` 全局启用，业务页不要重复调用；独立表格可设 `data-full-height-table="false"` |
| `useTreeCollapsed` | `hooks/tree/useTreeCollapsed.ts` | `treeCollapsed`、`toggleCollapsed`、`setCollapsed` | 左右分栏树折叠 |
| `useTreeTableExpand` | `hooks/tree/useTreeTableExpand.ts` | `isExpandAll`、`setExpandAll`、`handleToggleExpandAll` | 树表展开/折叠；依赖 `treeTableRef` 和树数据 |

## 4. 其它现有入口

| 场景 | 入口 |
|---|---|
| 字典 | `utils/dict.ts` 的 `useDict`；Pinia `store/modules/dict.ts` |
| 权限字符 | `directive/permission/index.ts` 的 `v-hasPermi`；`utils/permission.ts` 的 `checkPermi` |
| 角色 | `v-hasRoles`；`utils/permission.ts` 的 `checkRole` |
| 消息、确认、加载遮罩 | `plugins/modal.ts` |
| 下载 | `utils/request.ts` 的 `download`；`plugins/download.ts` 的 `oss/zip` |
| 文件保存 | `utils/save.ts` 的 `saveBlob` |
| 树构造 | `utils/ruoyi.ts` 的 `handleTree` |
| 日期范围 | `utils/ruoyi.ts` 的 `addDateRange` |
| 时间格式 | `utils/ruoyi.ts` 的 `parseTime` |
| OSS 内容解析 | `utils/ossContent.ts` 的 `resolveOssContent` |
| 请求返回类型 | `utils/api-types.ts` 的 `AxiosPromise` |
| 分页返回类型 | `api/types.ts` 的 `PageResult<T>` |

## 5. 组合方式

### 普通 CRUD

```text
useLoading
useSearchToggle + RightToolbar
useSearchReset
useTableSelection
useFormDialog
useDict / DictTag
v-hasPermi
```

### 树表

```text
普通 CRUD 组合
+ useTreeTableExpand
+ handleTree
+ el-tree-select
```

### 左树右表

```text
TreePanel / useTreeCollapsed
+ 右侧普通 CRUD 组合
```

### 选择器与附件

```text
UserSelect / RoleSelect
FileUpload / ImageUpload / Editor
```

## 6. 禁止事项

- 不复制 `Pagination`、`RightToolbar`、`DictTag` 或选择器到业务目录。
- 不手写第二套按钮禁用规则；用 `single/multiple` 的现有语义。
- 不在页面里重复请求字典；`useDict` 已带 Pinia 缓存和并发合并。
- 不把 `v-hasPermi` 当作数据权限；接口和 Service 仍要校验。`v-hasPermi` 在挂载时移除无权元素，权限变化不会自动恢复；动态权限用 `checkPermi` + `v-if`。
- 不用 `vxe-table` 替换普通 `el-table`；现有 `vxe-table` 只在选择器等既有场景使用。
- 不把上传文件二进制或临时 URL 存业务表；优先保存 `ossId`。
- 不修改共享组件只为单页样式；页面样式加 `scoped`，优先复用现有类。
- `Breadcrumb`、`Screenfull`、`SizeSelect`、`LangSelect`、`TopNav` 属于布局壳组件，业务页只复用，不复制重建。
