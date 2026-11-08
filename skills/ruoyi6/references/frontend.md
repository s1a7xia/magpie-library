# React 前端开发规范

## 写页面前

先按 `SKILL.md` 的任务判型、业务判型、复用扫描和契约门确认范围，再决定组件和文件。作者 `ruoyi-demo` React 页面、`plus-ui-React` 公共组件/hooks 和生成模板是实现写法参考；目标业务页面只用于确认业务字段、权限、路由和集成约束，不作为质量范本。

前端重点检查：

1. 是否已有同一业务领域的页面壳、查询区、表格、详情抽屉或弹窗。
2. `src/components/common` 是否已有字典、行操作、树、选择器、上传、富文本、预览等组件。
3. `src/hooks` 是否已有表格选择、导出、滚动、日期范围、字典、树展开等行为封装。
4. 请求、鉴权、权限、字典、主题、日期和下载是否必须走 `src/api/request.ts`、`src/utils/*`。
5. 页面需要的状态、文件和接口是否已经由后端或公共模块提供。

取样顺序固定为：`src/pages/demo` 作者示例 -> `components/common` / `hooks` / `utils` -> `plus-ui-React/gen` 模板 -> 通用 React / Ant Design 习惯。目标目录页面用于读取业务约束，不作为编码模式依据。模板是标准骨架，不是最终答案。

## 工程事实

| 项 | 当前约定 |
|---|---|
| 框架 | React 19 + TypeScript + Umi Max |
| UI | Ant Design 6 + Ant Design ProComponents |
| 请求 | axios 封装在 `src/api/request.ts` |
| 数据请求 | TanStack Query、ahooks |
| 状态 | Zustand，读取必须使用 selector |
| 样式 | LESS，`src/assets/styles/` |
| 包管理 | pnpm |

版本和脚本从当前 `plus-ui-React/package.json` 读取：`dev`、`build:dev`、`build:prod`、`lint`、`fmt`。不用记忆中的旧前端写法覆盖当前源码。

## 选择页面形态

| 页面用途 | 最小实现 |
|---|---|
| 单表列表 | `PageContainer` + `ProTable` + `ModalForm` |
| 树形分类 | 树表或左树右表；节点移动、删除和展开规则与后端一致 |
| 主从记录 | 主记录页面 + 明细区/子页面；重复明细或关系约束需要单独表达时建子表 |
| 状态流转 | `Tag`/`DictTag` + 合法操作按钮 + 二次确认 + 失败提示 |
| 审批业务 | 复用 `src/components/workflow/*`，查询当前任务和业务状态，不另做审批交互 |
| 只读报表 | 查询条件 + 图表/表格 + 导出；不显示无意义的增删改按钮 |
| 详情页/抽屉 | `Drawer` + `ProDescriptions`；长字段分组，不堆满屏表单项 |
| 导入/批处理 | 模板下载、文件校验、错误行反馈、结果汇总和刷新 |

按钮、状态和操作是否出现由权限和业务状态共同决定。不要只按页面布局硬编码，也不要把所有操作都堆在工具栏。

## 文件与路由

```text
plus-ui-React/src/
├─ api/<module>/<business>/index.ts
├─ api/<module>/<business>/types.ts
├─ pages/<module>/<business>/index.tsx
├─ pages/dynamicPage.tsx
├─ components/common/
├─ hooks/
├─ stores/
├─ layouts/
└─ utils/
```

- 页面入口固定 `index.tsx`；复杂页面可拆同目录子组件。
- `types.ts` 放 `VO`、`Form`、`Query`；`index.ts` 只放请求函数。
- `VO` 字段必填、`Form extends BaseEntity` 且字段全部可选、`Query extends PageQuery` 且条件可选；字段名与后端 BO/VO 完全一致。
- 单页状态留在页面，跨页面状态才进 Zustand。
- 同模块兄弟页面只用于读字段、路由、权限和已有集成约束；写法仍从作者 demo、公共组件/hooks 和模板取样。

### 动态路由门

业务路由来自后端菜单，`src/pages/dynamicPage.tsx` 用 `migratedPages` 把菜单 `component` 映射到 React 页面。新页面只创建 TSX 不够：

1. 在后端菜单中保留 `component`（通常是 `@/views/<module>/<business>/index`）。
2. 在 `dynamicPage.tsx` import 新页面，并登记对应键，例如 `module/business/index`。
3. 若页面遵循稳定路径前缀，可评估 `migratedPathPrefixes`，但新业务默认用显式键，避免误匹配。
4. 未登记会进入页面占位提示，即使 TSX 本身构建通过。

`normalizeComponentKey` 会规范菜单 `component` 键。后端菜单格式以现有归一化规则为准，不为了前端改动菜单契约。

## 页面骨架

```text
PageContainer
  ProTable
    search / columns / toolbar / rowSelection / pagination
  ModalForm
  Drawer + ProDescriptions（按需）
```

- 页面用函数组件，默认导出页面组件。
- `ProTable` 的 `rowKey` 用稳定业务主键；`scroll` 复用 `useTableScroll`。
- 查询参数从 ProTable `params` 经 `toPageQuery` 转换，分页结果为 `toTableData(res)`。
- 表格操作列用 `valueType: 'option'` + `RowActions`。
- 列表 `request` 内不要直接拼第二套分页或错误处理逻辑。

## API 与类型

- 请求统一 `import request from '@/api/request'`；导出函数返回 `Promise<R<T>>`。
- 分页读 `res.data.rows`、`res.data.total`；树表读 `res.data` 数组。
- 查询用 `params`，新增/修改用 `data`；下载复用 `@/utils/download` 或 `useTableExport`。
- `R`、`PageResult`、`PageQuery`、`BaseEntity` 来自 `@/api/types`。
- 主键和关联 ID 用 `string | number`。
- 不使用 `any` 掩盖字段不一致；纯类型导入用 `import type`。
- 不使用 `AxiosPromise`，不从 `axios` 导出响应类型；`request` 已直接返回响应体。
- 日期范围保留 `Query.params`；列表页 `Query` 继承 `PageQuery`，树表 `Query` 不继承。
- API 函数优先跟随 `plus-ui-React/gen/api.ts.ftl` 的命名和 `export function` 形式；相邻模块已统一另一风格时保持该模块风格。

### API 模板

```ts
import type { PageResult, R } from '@/api/types';
import request from '@/api/request';
import type { XxxForm, XxxQuery, XxxVO } from './types';

export function listXxx(query?: XxxQuery) {
  return request<R<PageResult<XxxVO>>>({
    url: '/<module>/<business>/list',
    method: 'get',
    params: query
  });
}

export function getXxx(id: string | number) {
  return request<R<XxxVO>>({
    url: `/<module>/<business>/${id}`,
    method: 'get'
  });
}

export function addXxx(data: XxxForm) {
  return request<R>({
    url: '/<module>/<business>',
    method: 'post',
    data
  });
}

export function updateXxx(data: XxxForm) {
  return request<R>({
    url: '/<module>/<business>',
    method: 'put',
    data
  });
}

export function delXxx(id: string | number | Array<string | number>) {
  return request<R>({
    url: `/<module>/<business>/${id}`,
    method: 'delete'
  });
}
```

`types.ts` 至少分开 `XxxVO`、`XxxForm`、`XxxQuery`；字段名与 BO/VO 完全一致，主键、关联 ID 和雪花 ID 不使用单 `number` 类型。

## 页面行为

- 新增：`form.resetFields()` → `setFieldsValue(defaultForm)` → 打开 `ModalForm`。
- 编辑：先 `getXxx(id)`，再 `resetFields()` + `setFieldsValue(res.data)` 回显；不要用列表行暗中替代详情契约。
- 提交成功后关闭弹窗并 `actionRef.current?.reload()`；失败保留输入并让 `ModalForm` 恢复提交状态。
- 删除先确认，再清选中项并 `reloadAndRest`。
- 状态切换失败要回滚界面状态；使用 `confirmAction` 或 `Popconfirm`。
- 权限用 `const userInfo = useUserStore(state => state.userInfo)` + `hasPermi(userInfo, ['module:business:action'])`；不要另造页面级权限判断。
- 页面至少处理 loading、空结果、请求失败、无权限和提交失败；不能只覆盖成功路径。
- 表单字段、列表字段和查询字段从同一份契约派生；不要在不同组件里各自硬编码标签和枚举。
- 树表使用 `handleTree`、`useTreeTableExpand`、`ProTable` 的 `expandable` 和 `ProFormTreeSelect`；新增子节点时从当前行带入父 ID。
- 修改已有复杂页面时保留树筛选、导入、导出、详情抽屉、分配页面和路由跳转，只增量修改本需求范围内的交互。

### 请求头开关

| Header | 作用 | 什么时候用 |
|---|---|---|
| `isToken: false` | 本次请求不携带 Token | 登录、验证码等公开接口 |
| `repeatSubmit: false` | 关闭 POST/PUT 前端短时防重 | 明确允许连续提交的接口；后端 `@RepeatSubmit` 仍独立生效 |
| `isEncrypt: 'true'` | 开启 POST/PUT 请求体加密 | 后端标注 `@ApiEncrypt` 且环境开启加密的敏感接口 |

本地 `request.ts` 同时接受布尔 `true` 和字符串 `'true'`；新代码沿用同模块现有写法。非 Axios 上传、富文本等请求需要公共头时复用 `globalHeaders()`。

## 现有 hooks

| 场景 | 入口 |
|---|---|
| 表格选择 | `hooks/useTableSelection`：`ids`、`selectedOne`、`single`、`multiple`、`handleSelectionChange`、`clearSelection` |
| 表格导出 | `hooks/useTableExport`：`updateExportParams`、`exportFile` |
| 表格滚动 | `hooks/useTableScroll`：`tableScroll` |
| 日期范围 | `hooks/useDateRangeQuery`：`dateRange`、`applyDateRange`、`resetDateRange` |
| 搜索重置 | `hooks/useSearchReset` |
| 字典 | `hooks/useDict` |
| 树展开 | `hooks/useTreeTableExpand`：`expandAll`、`expandedRowKeys`、`onExpandedRowsChange`、`syncExpandedRows`、`toggleExpandAll` |
| 异步 loading | `ahooks` 的 `useBoolean`、`useRequest`，或现有 `useLoading` |

- 新增 hook 前先确认现有 hook 不能被组合或薄包装解决。
- hook 只承载页面行为，不塞业务协议和全局状态。
- Zustand store 必须用 selector 读取，例如 `useUserStore(state => state.userInfo)`。

## 现有组件与工具

| 场景 | 组件 / 工具 |
|---|---|
| 页面标题与操作区 | ProComponents `PageContainer` |
| 列表与分页 | ProComponents `ProTable` |
| 弹窗表单 | ProComponents `ModalForm`、`ProForm*` |
| 行操作 | `components/common/RowActions` |
| 字典 | `components/common/DictTag` + `useDict` + `dictOptions` |
| 左树 | `components/common/TreePanel` |
| 用户选择 | `components/common/UserSelect` |
| 文件、图片、预览 | `components/common/FileUpload`、`ImageUpload`、`ImagePreview` |
| 富文本、图标 | `components/common/RichTextEditor`、`IconSelect` |
| 审批交互 | `components/workflow/*` |
| 详情面板 | antd `Drawer` + ProComponents `ProDescriptions` |
| 下载 | `@/utils/download` 的 `download` / `saveBlob` / `saveValidatedBlob` |
| 确认框 | `@/utils/modal` 的 `confirmAction`、`confirmTitle`、`confirmTitleSafe` |
| 权限 | `@/utils/permission` 的 `hasPermi`、`hasRole` |
| 查询、树、日期 | `@/utils/ruoyi` 的 `toPageQuery`、`toTableData`、`handleTree`、`filterTree`、`addDateRange`、`withTableSort` |
| 字典选项 | `@/utils/dict` 的 `dictOptions` |

上传值保存 `ossId`，不保存二进制或临时 URL。富文本的 OSS 约定以 `RichTextEditor` 和现有页面为准。不要复制分页、工具栏、字典、选择器或上传组件。

## 复用边界

- 请求统一走 `@/api/request`；鉴权走 `@/utils/auth`；权限判断走 `@/utils/permission`；字典走 `useDict` / `DictTag` / `dictOptions`；下载复用现有工具。
- 页面需要的用户、部门、角色、岗位、文件、流程、消息能力，先查现有组件和 API；不要新建平行选择器、上传器或请求封装。
- 同一业务领域已有页面壳时，优先扩展查询、列、操作和详情；不要另起一套风格和交互。
- 新增全局组件前确认至少有两个真实调用方；单页专用结构留在页面或同目录子组件。
- 现有业务页面的代码质量不作为规范依据。可以读它确认字段、接口和权限，但不能复制其重复请求、散落常量或无边界的状态处理。

## 样式与设计

- 业务页保留 ProComponents/Ant Design 核心组件：`PageContainer`、`ProTable`、`ModalForm`、`Drawer`、`Pagination`/ProTable 分页、`DictTag`、`RowActions`。
- 复用现有页面壳和类：`tree-table-page`、`table-panel`、`page-surface`，以及 `src/assets/styles/` 的 token。
- 颜色优先用 `--app-*` 主题变量；不散落硬编码色值。
- 单页样式放页面局部 LESS 或现有模块样式文件，不覆盖 Ant Design 类名。
- 状态用语义化 `Tag` 或 `DictTag`：成功、警告、危险、信息含义固定。
- 禁止无意义侧边粗色条、渐变标题、毛玻璃堆叠、卡片套卡片。
- 保证无横向溢出、按钮不折行、弹窗与下拉层级正常、深色模式文字可读。

`frontend-design` 负责设计方法和 craft floor，本文件负责收敛当前组件与样式边界。

## 图表

项目已装 `echarts` 和 `echarts-for-react`，报表和大屏直接复用，不要再引入别的图表库，也不要在多个页面各写一份初始化逻辑。

- 至少处理实例创建、`setOption`、容器 resize 和卸载 dispose。
- 数据变化后更新现有实例，不在渲染期反复重建。
- 图表要有可读的 `aria`/文本替代，并把关键数据以可访问形式同时列出。
- 需要下钻时用组件事件把选中项交给父页面，不在图表组件内部直接跳路由。
- 多页面复用同一类图表时抽成组件；单页一次性图表留在页面同目录。

图表实现以当前 `plus-ui-React` 的公共封装和作者示例为准。

## 构建与验收

- 使用项目登记的 pnpm 脚本：`pnpm dev`、`pnpm build:dev`、`pnpm build:prod`、`pnpm lint`、`pnpm fmt`。
- 修改前端后至少执行实际构建；独立类型检查不替代构建。
- 修改路由、`dynamicPage.tsx`、请求封装、全局 store 或布局时检查所有受影响页面。
- 开发阶段只做代码和构建检查；页面可见改动由用户发起 `page-acceptance` 在真实浏览器验收。

## 常见错误

| 写法 | 问题 | 正确做法 |
|---|---|---|
| `import { request } from '@/utils/request'` | 路径和导出都不对 | `import request from '@/api/request'` |
| 使用 `AxiosPromise<T>` | React 工程请求层直接返回 `R<T>` | `request<R<T>>`，函数返回 `Promise<R<T>>` |
| 页面直接拼 `fetch`/`axios` | 绕过鉴权、加解密、错误提示 | 统一走 `@/api/request` |
| 新建页面但没登记 `dynamicPage.tsx` | 菜单进入页面占位提示 | 在 `migratedPages` 登记键 |
| 主键声明为 `number` | 雪花 ID 可能丢精度 | `string \| number` |
| 只加前端 `hasPermi` | 绕过接口调用仍可能成功 | 后端 `@SaCheckPermission` 必须同步 |
| 每个页面复制分页、树、上传组件 | 样式和行为漂移 | 复用 `components/common` 和 `hooks` |
| 复制已有业务页面整套逻辑 | 把历史问题扩散到新模块 | 只读集成约束，基础行为取框架组件和 hooks |
| 新增第二套请求/权限/字典封装 | 绕过加解密、错误提示和统一权限 | 使用现有 `api/request`、`utils`、`useDict`、`DictTag` |
| 报表页硬加增删改按钮 | 与只读业务不匹配 | 按业务形态决定操作，不套完整 CRUD |
| 删除日期范围 `params` | 后端 `betweenParams` 收不到 begin/end | 保留 `Query.params` 和 `useDateRangeQuery` |

## 检查

- [ ] API、类型、页面位置正确，没有绕过统一请求层。
- [ ] `VO` / `Form` / `Query` 分开，ID 精度保留。
- [ ] 已选择最小页面形态，并扫描现有 hooks、组件、字典、权限和页面壳。
- [ ] 没有复制业务模块，也没有新增第二套请求、权限、字典、分页或上传实现。
- [ ] 新页面已登记 `dynamicPage.tsx`，菜单 `component` 和权限字符一致。
- [ ] 表单校验、loading、失败恢复、编辑回显、删除刷新完整。
- [ ] 构建通过；页面未验收时明确标注。
- [ ] 业务未定的交互用 TODO 占位且页面可正常打开，没有留空白按钮或半截功能；TODO 已写明原因和确认人。
