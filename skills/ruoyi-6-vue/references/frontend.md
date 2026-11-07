# plus-ui 6.0 前端开发规范

用于 `61b9ee20c3452febe1d03c6e013c0b4de11237f1` 中 `plus-ui` 6.0.0 的 Vue 3 + TypeScript + Element Plus 页面、API 与样式。请求、路由、Pinia 和布局链路读 [frontend-shell.md](frontend-shell.md)；接口契约读 [api-contract.md](api-contract.md)；视觉边界读 [ui-design.md](ui-design.md)。

## 1. 目录与文件

```text
plus-ui/src/
├─ api/<module>/<business>/{index.ts,types.ts}
├─ views/<module>/<business>/index.vue
├─ hooks/{async,dialog,form,table,tree}/
├─ components/
├─ store/modules/
├─ utils/
└─ assets/styles/
```

- 页面入口固定 `views/<module>/<business>/index.vue`；复杂页面可拆同目录子组件。
- API 与类型分文件：`index.ts` 只放请求函数，`types.ts` 放 `VO` / `Form` / `Query`。
- 单页临时状态留在页面；跨页面共享状态才进 Pinia store。
- 修改前读同模块两三个兄弟页面和现有 hooks，沿用页面壳、表格、弹窗、工具栏和主题 token。
- 不为单页新建第二套请求层、表格组件、弹窗组件或主题系统。

## 2. 组件写法

- 页面使用 `<script setup name="Xxx" lang="ts">`；业务组件使用大驼峰文件名与组件名。
- 组件 `name` 用于 keep-alive 和标签页。菜单路由名由后端 `routeName + menuId` 生成，页面加载器再用路由名包装组件；不要手工假设组件名必须等于完整路由名。
- Props 用 TypeScript 接口 + `withDefaults(defineProps<Props>())`；事件用 `defineEmits<{...}>()`。
- 模板保持语义结构，避免无意义深层嵌套；列表渲染使用稳定业务主键作为 `key`。
- 组件职责单一；复杂查询、弹窗生命周期、选择逻辑优先抽到现有 hooks 或本页 composable，不复制到多个页面。

## 3. TypeScript 与类型

- 开启严格类型；不使用 `any` 掩盖后端字段不一致，确需临时断言时说明原因。
- `VO` 表示列表/详情返回；`Form` 表示新增/编辑请求；`Query` 继承 `PageQuery`。
- 主键和关联 ID 使用 `string | number`；雪花 ID 可能已被 JSON number 舍入，不能靠前端联合类型补救。
- 可选字段与后端可空性一致；日期、状态、字典值使用统一类型，不把 `null`、`undefined`、空字符串混用。
- 类型文件只放类型；纯类型导入使用 `import type`。

## 4. API 与数据流

- 请求统一走 `@/utils/request` 的 `request`；返回类型 `AxiosPromise<T>`。
- 分页读取 `res.data.rows`、`res.data.total`；树表读取 `res.data` 数组。
- 查询用 `params`，新增/修改用 `data`，下载复用 `download` 或现有下载入口。
- 请求失败由拦截器统一提示；页面只在需要补充业务上下文时处理错误，不重复弹同一错误。
- 表单提交保留校验、按钮 loading 和失败恢复；编辑必须先拉详情，再回填表单。
- 状态切换失败要回滚界面状态；删除后刷新列表并清理选中项。

## 5. 页面交互与 hooks

| 场景 | 优先入口 |
|---|---|
| 加载态 | `@/hooks/async/useLoading` |
| 表单弹窗 | `@/hooks/dialog/useFormDialog`、`useDialogState` |
| 搜索重置/折叠 | `@/hooks/form/useSearchReset`、`useSearchToggle` |
| 日期范围 | `@/hooks/form/useDateRangeQuery` |
| 表格多选 | `@/hooks/table/useTableSelection` |
| 表格排序/全高 | `@/hooks/table/useTableSortQuery`、`useFullHeightTable` |
| 树展开/折叠 | `@/hooks/tree/useTreeCollapsed`、`useTreeTableExpand` |
| 字典 | `useDict`、`DictTag` |
| 权限 | `v-hasPermi`、`checkPermi` |

- `useFormDialog.openDialog` 会重置表单；编辑回填后用 `showDialog`。
- `useSearchReset` 负责重置查询表单和页码；重置后要重新查询。
- `useTableSelection` 输出 `ids`、`single`、`multiple` 和选择回调；不要手写另一套禁用逻辑。
- `v-hasPermi` 对延迟渲染节点可能失效，此类场景用 `checkPermi` + `v-if`。
- 字典缓存由 `useDict` 和 Pinia dict store 管理；页面不重复请求同一字典。

## 6. 状态与全局链路

- `user`、`permission`、`dict`、`tagsView`、`app`、`settings`、`branding`、`notice` 等 store 已有明确职责；新增全局状态前先确认现有 store 不能承载。
- 动态路由、401、登录、标签页和菜单加载由 `permission.ts`、`request.ts` 和 permission store 统一处理；页面不复制这些逻辑。
- 页面缓存依赖组件名和 tagsView 的 cachedViews；修改路由名或组件 name 时检查 keep-alive。
- 不在页面里直接读写 token 或清登录态；统一走现有 auth/store/request 链路。

## 7. 样式与设计边界

- 业务 CRUD 页按 `frontend-design` 的 Enhance 模式处理，Element Plus 与若依内置组件就是设计系统。
- 复用 `app-container`、`search-panel`、`table-panel`、`toolbar-shell`、`toolbar-actions`、`panel-kicker`、`data-table` 等现有样式。
- 状态用语义化 `el-tag` 或 `DictTag`：成功、警告、危险、信息各有固定含义；不把所有状态染成 primary。
- 单页样式加 `scoped`；主题色改 token，不在组件里散落硬编码色值。
- 禁止无意义侧边粗色条、渐变标题、毛玻璃堆叠、卡片套卡片和装饰性 KPI。
- 不为了视觉效果替换 `el-table`、`el-form`、`el-dialog`、`el-pagination`、`dict-tag`、`right-toolbar` 等核心组件。

## 8. 构建与验收

- 从实际 `package.json` 和锁文件确认包管理器与脚本。固定基线 6.0.0 使用 pnpm，脚本包括 `pnpm dev`、`pnpm build`、`pnpm lint`、`pnpm fmt`。
- 修改前端后至少执行项目已有的实际构建；独立类型检查不替代构建。只在用户要求时运行额外 lint/test。
- 修改路由、组件 name、请求封装、全局 store 或布局时，检查所有受影响页面。
- 构建通过不等于页面可用或好看；开发阶段只做静态核对，不启动浏览器。可见页面由用户主动发起 `page-acceptance`，在真实浏览器验收并保留截图证据。

## 9. 检查清单

- [ ] API、类型、页面位置符合现有目录，未绕过统一请求层。
- [ ] `VO` / `Form` / `Query` 分开，主键和关联 ID 保持精度。
- [ ] 复用现有 hooks、字典、权限、分页、工具栏和页面壳。
- [ ] 表单校验、loading、失败恢复、编辑回显和删除刷新完整。
- [ ] 业务页保留 Element Plus 和若依核心组件，权限未被视觉改动绕过。
- [ ] 无横向溢出、按钮折行、层级遮挡和深色模式对比度问题。
- [ ] 已执行实际前端构建；页面验收状态单独记录。
