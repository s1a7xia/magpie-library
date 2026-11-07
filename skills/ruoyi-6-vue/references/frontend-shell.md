# plus-ui 6.1.0 Frontend Shell

用于理解 `plus-ui` 的请求、鉴权、动态路由、状态、布局与页面骨架。它解决“代码应该接在哪”，具体业务交互仍读 [frontend.md](frontend.md)，视觉边界读 [ui-design.md](ui-design.md)。

## 1. 启动链路

```text
main.ts
  -> 注册 Element Plus / Vxe / 指令 / 插件 / i18n / Pinia / Router
  -> 先加载品牌配置
  -> mount #app
permission.ts
  -> 是否有 token
  -> 拉取 getInfo()：roles、permissions、用户资料
  -> permissionStore.generateRoutes()
  -> router.addRoute() 动态挂载菜单路由
```

- 路由来自后端 `/system/menu/getRouters`，`Layout`、`ParentView`、`InnerLink` 是特殊组件标识；业务页面按 `views/**/*.vue` 的路径被解析。
- 页面组件的 `name` 必须与菜单路由 `name` 一致，否则 `keep-alive` 缓存、标签页和动态组件行为会异常。
- 无 token 时跳登录；登录态失效由 `request.ts` 的 401 分支统一处理。不要在页面里重复写跳登录或清 token。
- 强制改密由后端 `PASSWORD_CHANGE_REQUIRED` 与 `mustChangePassword` 驱动，只有允许的路径可访问；新增拦截逻辑前先读 `permission.ts` 和 `request.ts`。

## 2. 请求与返回类型

- 所有 API 从 `@/utils/request` 导入 `request`，保留拦截器提供的 token、`clientid`、`Content-Language`、重复提交、RSA/AES 和错误提示。
- 请求函数返回类型使用 `AxiosPromise<T>`（来自 `@/utils/api-types`）；拦截器 resolve 的是若依风格 `{ code, msg, data }`，所以页面读取 `res.data`。
- 分页返回类型是 `PageResult<T>`（来自 `@/api/types`）：`res.data.rows`、`res.data.total`。树表列表通常直接返回 `VO[]`。
- 查询使用 `params`，新增修改使用 `data`；下载走 `download` 或现有下载入口，不手工拼裸链接绕过鉴权。
- `isEncrypt`、`isToken`、`repeatSubmit` 是项目已有请求头开关；只在确有对应契约时使用，不要自创请求头协议。

## 3. API 与页面位置

```text
src/api/<module>/<business>/index.ts     请求函数
src/api/<module>/<business>/types.ts     VO / Form / Query 类型
src/views/<module>/<business>/index.vue  页面
```

- API 函数保持薄：拼 URL、method、params/data 和返回类型；业务编排留在页面或 hook。
- `VO`、`Form`、`Query` 分开定义；主键和外部关联 ID 用 `string | number`，分页查询继承 `PageQuery`。
- 页面使用 `<script setup name="Xxx" lang="ts">`；组件名与菜单路由一致。
- 类型里的日期、状态、字典值、可空字段必须与后端 VO/BO 对齐；不要用 `any` 掩盖契约不一致。

## 4. 现有 hooks 与组件

写页面前先读对应实现和两三个兄弟页面，优先组合而不是复制：

| 能力 | 现有入口 |
|---|---|
| 异步加载态 | `@/hooks/async/useLoading` |
| 表单弹窗生命周期 | `@/hooks/dialog/useFormDialog`、`useDialogState` |
| 搜索重置/折叠 | `@/hooks/form/useSearchReset`、`useSearchToggle` |
| 日期范围查询 | `@/hooks/form/useDateRangeQuery` |
| 表格选择 | `@/hooks/table/useTableSelection` |
| 表格排序/全高 | `@/hooks/table/useTableSortQuery`、`useFullHeightTable` |
| 树折叠/树表展开 | `@/hooks/tree/useTreeCollapsed`、`useTreeTableExpand` |
| 字典 | `useDict`（`@/utils/dict`）、`DictTag` |
| 权限 | `v-hasPermi` 指令、`checkPermi` |
| 分页、页面壳、工具栏 | `pagination`、`right-toolbar`、现有 page-shell / search-panel / table-toolbar 样式 |

- `useFormDialog.openDialog` 会重置表单，编辑回填后用 `showDialog`；具体签名以当前版本源码为准。
- 字典缓存由 Pinia `dict` store 管理，`useDict` 负责并发请求合并；不要在页面重复实现字典请求。
- `v-hasPermi` 对 `el-dropdown-item` 等延迟渲染节点可能失效，改用 `checkPermi` + `v-if` 的现有做法。
- 选择行的 `single`/`multiple` 语义来自 `useTableSelection`，不要手写一套不一致的禁用逻辑。

## 5. 标准 CRUD 页面骨架

页面（包括标准 CRUD）由 AI 直接编写；本项目没有代码生成器或模板脚手架环节。页面结构按现有 demo 与业务页组合：

新增标准 CRUD 时，可先按 [common.md 的 CRUD Fast Path](common.md#新增-crud-的最快路径) 读 `ruoyi-gen/.../fm/vue/` 的 `api.ts.ftl`、`types.ts.ftl`、`index.vue.ftl` 或 `index-tree.vue.ftl`，作为完整交互分支的清单；按字段契约裁剪后直接写目标页面。模板与真实业务页冲突时，以真实业务页为准。

```text
搜索卡片（el-form + queryParams）
表格卡片
  toolbar（新增/修改/删除/导出 + right-toolbar）
  el-table（selection、字典/状态列、行操作）
  pagination
el-dialog / el-drawer（form + rules + submit loading）
```

推荐实现顺序：

1. 先写 `types.ts` 与 `api/index.ts`，对齐后端 URL、分页和字段。
2. 页面用 `useLoading`、`useSearchToggle`、`useTableSelection`、`useFormDialog`、`useSearchReset` 搭骨架。
3. 查询、重置、新增、编辑回填、提交、删除、导出按现有 demo 的调用顺序实现；编辑必须先拉详情再 `Object.assign` 回填。
4. 状态列用 `DictTag` 或语义化 `el-tag`；权限按钮和行操作不遗漏 `v-hasPermi`。
5. 最后按 [ui-design.md](ui-design.md) 调整信息层级与间距，不改变组件和交互契约。

## 6. 布局与全局状态

- 布局由 `src/layout/index.vue` 组织侧栏、Navbar、TagsView、AppMain、设置面板；业务页只渲染在 AppMain 的 router-view 内。
- `AppMain` 使用 `keep-alive :include="tagsViewStore.cachedViews"`，页面缓存依赖组件名；不随意改路由名或组件 name。
- Pinia 已有 `user`、`permission`、`dict`、`tagsView`、`app`、`settings`、`branding`、`notice` 等 store。新增全局状态前先确认现有 store 不能承载；单页临时状态留在页面。
- 路由守卫、401、登录、强制改密、标签页和菜单加载是框架链路；页面级改动不要复制或绕过这些机制。

## 7. 构建与检查

- 先读目标 `package.json`。本地 6.1.0 脚本包括 `pnpm dev`、`pnpm build`、`pnpm lint`；是否运行 lint/typecheck 以项目要求和本次范围为准。
- 修改路由、组件 `name`、请求封装、全局 store、布局时，检查影响的所有页面，不只检查当前页。
- 构建通过不等于页面可用；可见页面必须在真实浏览器按 `page-acceptance` 验收。

## 8. 反模式

- 在页面里直接用 Axios/fetch，绕过 token、加密、错误处理和重复提交保护。
- 把 `R<T>` 当成页面直接数据，忘记读取 `res.data`；或把分页 `rows/total` 写成数组。
- 为单页复制 `useFormDialog`、`useTableSelection`、字典缓存或权限判断。
- 组件 `name` 与菜单路由 `name` 不一致，导致 keep-alive 和标签页失效。
- 业务页复制全局布局或另造主题层；先复用 `layout`、页面壳和主题 token。
- 用前端隐藏代替后端脱敏、权限或数据范围控制。
