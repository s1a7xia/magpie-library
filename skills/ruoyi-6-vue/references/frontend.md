# 前端开发规范

## 写页面前

先按 `SKILL.md` 的业务判型、复用扫描和契约门确认页面形态，再决定组件和文件。前端重点检查：

1. 是否已有同一业务领域的页面壳、查询区、表格、详情抽屉或弹窗。
2. `components/` 是否已有分页、工具栏、字典、选择器、上传、流程、空状态等组件。
3. `hooks/` 是否已有 loading、搜索、弹窗、表格选择、排序、树折叠等行为封装。
4. 请求、鉴权、权限、字典、主题、日期和下载是否必须走 `utils/`。
5. 页面需要的状态、文件和接口是否已经由后端或公共模块提供。

页面实现不是把现有业务页面整页复制后改名。已有业务页面只帮助理解交互和集成约束；基础行为以 `components/`、`hooks/`、`utils/` 和框架 demo 为准。

## 选择页面形态

| 页面用途 | 最小实现 |
|---|---|
| 单表列表 | 查询区 + 表格 + 分页 + 新增/编辑弹窗 |
| 树形分类 | 树表或左树右表；节点移动、删除和展开规则与后端一致 |
| 主从记录 | 主记录页面 + 明细区/子页面；明细查询边界独立时才拆 |
| 状态流转 | 状态标签 + 合法操作按钮 + 二次确认 + 失败提示 |
| 审批业务 | 复用 `Process/*` 组件，查询当前任务和业务状态，不另做审批交互 |
| 只读报表 | 查询条件 + 图表/表格 + 导出；不显示无意义的增删改按钮 |
| 详情页/抽屉 | 复用现有页面壳和排版；长字段分组，不堆满屏表单项 |
| 导入/批处理 | 模板下载、文件校验、错误行反馈、结果汇总和刷新 |

按钮、状态和操作是否出现由权限和业务状态共同决定。不要只按页面布局硬编码，也不要把所有操作都堆在工具栏。

## 文件

```text
plus-ui/src/
├─ api/<module>/<business>/index.ts
├─ api/<module>/<business>/types.ts
├─ views/<module>/<business>/index.vue
├─ hooks/
├─ components/
├─ store/modules/
└─ utils/
```

- 页面入口固定 `index.vue`；复杂页面可拆同目录子组件。
- `types.ts` 放 `VO`、`Form`、`Query`；`index.ts` 只放请求函数。
- 单页状态留在页面，跨页面状态才进 Pinia。
- 先读同模块两三个兄弟页面了解现有交互，再从 `components/`、`hooks/`、`utils/` 选通用能力；不要复制业务页面的实现。

## 页面骨架

```text
p-2 app-container
  search-wrap / search-panel
  table-panel
    toolbar-shell
    el-table.data-table
    pagination
  el-dialog / el-drawer
```

- 页面用 `<script setup name="Xxx" lang="ts">`。
- 组件 `name` 用于 keep-alive；菜单路由名由后端 `routeName + menuId` 生成，两者不要求相等。
- Props 用 `withDefaults(defineProps<Props>())`，事件用 `defineEmits`。
- 列表 `key` 用稳定业务主键。

## API 与类型

- 请求统一 `import request from '@/utils/request'`，返回 `AxiosPromise<T>`。
- 分页读 `res.data.rows`、`res.data.total`；树表读 `res.data` 数组。
- 查询用 `params`，新增/修改用 `data`；下载复用现有 `download`。
- `VO` 表示返回，`Form` 表示提交，`Query` 继承分页查询。
- 主键和关联 ID 用 `string | number`。
- 不使用 `any` 掩盖字段不一致；纯类型导入用 `import type`。

### API 模板

```ts
import request from '@/utils/request';
import type { AxiosPromise } from '@/utils/api-types';
import type { PageResult } from '@/api/types';
import type { XxxForm, XxxQuery, XxxVo } from './types';

const base = '/<module>/<business>';

export const listXxx = (query?: XxxQuery): AxiosPromise<PageResult<XxxVo>> =>
  request({ url: base + '/list', method: 'get', params: query });

export const getXxx = (id: string | number): AxiosPromise<XxxVo> =>
  request({ url: base + '/' + id, method: 'get' });

export const addXxx = (data: XxxForm) =>
  request({ url: base, method: 'post', data });

export const updateXxx = (data: XxxForm) =>
  request({ url: base, method: 'put', data });

export const delXxx = (id: string | number | Array<string | number>) =>
  request({ url: base + '/' + id, method: 'delete' });
```

`types.ts` 至少分开 `XxxVo`、`XxxForm`、`XxxQuery`；字段名与 BO/VO 完全一致，主键、关联 ID 和雪花 ID 不使用 `number` 单类型。

## 页面行为

- 编辑先拉详情，`Object.assign(form, data)` 后 `showDialog`；新增用 `openDialog`。
- 提交成功后关闭弹窗并刷新；失败保留输入、恢复 loading。
- 删除先确认，再清选中项并刷新。
- 状态切换失败要回滚界面状态。
- 权限用 `v-hasPermi`；延迟渲染节点用 `checkPermi` + `v-if`。
- `v-hasPermi` 只移除无权 DOM，不替代后端接口权限和数据权限。
- 页面至少处理 loading、空结果、请求失败、无权限和提交失败；不能只覆盖成功路径。
- 删除、批量操作、状态变更和导入都要有明确的确认、结果反馈和刷新策略。
- 表单字段、列表字段和查询字段从同一份契约派生；不要在不同组件里各自硬编码标签和枚举。

### 页面最小骨架

业务列表页沿用本地 `views/demo/demo/index.vue` 的页面壳，核心组合如下：

```vue
<template>
  <div class="p-2 app-container">
    <el-card class="search-panel">
      <el-form ref="queryFormRef" :model="queryParams" :inline="true">
        <el-form-item label="名称" prop="name">
          <el-input v-model="queryParams.name" clearable @keyup.enter="handleQuery" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleQuery">搜索</el-button>
          <el-button @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-panel">
      <template #header>
        <div class="toolbar-shell">
          <el-button v-hasPermi="['<module>:<business>:add']" type="primary" @click="handleAdd">新增</el-button>
          <right-toolbar v-model:show-search="showSearch" :search="false" @query-table="getList" />
        </div>
      </template>
      <el-table v-loading="loading" class="data-table" :data="xxxList">
        <el-table-column label="名称" prop="name" />
      </el-table>
      <pagination
        v-show="total > 0"
        v-model:page="queryParams.pageNum"
        v-model:limit="queryParams.pageSize"
        :total="total"
        @pagination="getList"
      />
    </el-card>
  </div>
</template>
```

脚本侧优先复用 `useLoading`、`useFormDialog`、`useSearchReset`、`useSearchToggle`、`useTableSelection`；编辑用 `getXxx(id)` 回填后 `showDialog`，新增用 `openDialog`。

## 现有 hooks

| 场景 | 入口 |
|---|---|
| 加载态 | `hooks/async/useLoading` |
| 弹窗 | `hooks/dialog/useDialogState`、`useFormDialog` |
| 搜索折叠、重置、日期范围 | `hooks/form/useSearchToggle`、`useSearchReset`、`useDateRangeQuery` |
| 表格选择、排序、满高 | `hooks/table/useTableSelection`、`useTableSortQuery`、`useFullHeightTable` |
| 树折叠、树表展开 | `hooks/tree/useTreeCollapsed`、`useTreeTableExpand` |

- `useFormDialog.openDialog` 会重置表单；编辑回填后用 `showDialog`。
- `useSearchReset` 负责清空查询和页码，重置后重新查询。
- `useTableSelection` 的 `single` 表示“不是恰好一条”，`multiple` 表示“零条”。
- `useFullHeightTable` 由 `AppMain.vue` 全局启用，业务页不要重复调用。

## 现有组件

| 场景 | 组件 |
|---|---|
| 分页 | `Pagination`：`v-model:page`、`v-model:limit`、`total` |
| 列显隐、刷新 | `RightToolbar`：`showSearch`、`columns`、`@queryTable` |
| 字典 | `DictTag`，配合 `useDict` |
| 空状态、状态页签 | `EmptyState`、`StatusTabs` |
| 页面标题与操作区 | `PageHeader` |
| 左树 | `TreePanel`，折叠时由父页面调整右侧列宽 |
| 用户、角色 | `UserSelect`、`RoleSelect`，通过 ref 调 `open()` |
| 文件、图片、预览 | `FileUpload`、`ImageUpload`、`ImagePreview` |
| 富文本、图标 | `Editor`、`IconSelect` |
| 审批交互 | `Process/` 下的提交、审批按钮、流程图和审批记录组件 |

上传值保存 `ossId`，不保存二进制或临时 URL。`Editor` 的 `url` 模式保存 `oss://<ossId>`。不要复制分页、工具栏、字典、选择器或上传组件。

## 复用边界

- 请求统一走 `@/utils/request`；鉴权走 `@/utils/auth`；权限判断走 `@/utils/permission`；字典走 `useDict` / `DictTag`；下载复用现有工具。
- 页面需要的用户、角色、部门、岗位、文件、流程、消息能力，先查现有组件和 API；不要新建平行选择器、上传器或请求封装。
- 同一业务领域已有页面壳时，优先扩展查询、列、操作和详情；不要另起一套风格和交互。
- 新增 hook 前先确认现有 hook 不能被组合或薄包装解决；hook 只承载页面行为，不塞业务协议和全局状态。
- 新增全局组件前确认至少有两个真实调用方；单页专用结构留在页面或同目录子组件。
- 现有业务页面的代码质量不作为规范依据。可以读它确认字段、接口和权限，但不能复制其重复请求、散落常量或无边界的状态处理。

## 样式与设计

- 业务页保留 `el-table`、`el-form`、`el-dialog`、`el-pagination`、`dict-tag`、`right-toolbar`。
- 复用 `app-container`、`search-panel`、`table-panel`、`toolbar-shell`、`toolbar-actions`、`panel-kicker`、`data-table`。
- 状态用语义化 `el-tag` 或 `DictTag`：成功、警告、危险、信息含义固定。
- 单页样式加 `scoped`；颜色用现有主题 token，不散落硬编码色值。
- 禁止无意义侧边粗色条、渐变标题、毛玻璃堆叠、卡片套卡片。
- 保证无横向溢出、按钮不折行、弹窗与下拉层级正常、深色模式文字可读。

## 构建与验收

- 使用项目登记的 pnpm 脚本：`pnpm dev`、`pnpm build:dev`、`pnpm build:prod`、`pnpm lint`、`pnpm fmt`。
- 修改前端后至少执行实际构建；独立类型检查不替代构建。
- 修改路由、组件 name、请求封装、全局 store 或布局时检查所有受影响页面。
- 开发阶段只做代码和构建检查；页面可见改动由用户发起 `page-acceptance` 在真实浏览器验收。

## 常见错误

| 写法 | 问题 | 正确做法 |
|---|---|---|
| `import { request } from '@/utils/request'` | 本地实际是默认导出，构建会报错 | `import request from '@/utils/request'` |
| 页面直接拼 `fetch`/`axios` | 绕过鉴权、加解密、错误提示 | 统一走 `@/utils/request` |
| 主键声明为 `number` | 雪花 ID 可能丢精度 | `string \| number` |
| 只加前端 `v-hasPermi` | 绕过接口调用仍可能成功 | 后端 `@SaCheckPermission` 必须同步 |
| 每个页面复制分页、工具栏、上传组件 | 样式和行为漂移 | 复用 `components/` 和 `hooks/` |
| 复制已有业务页面整套逻辑 | 把历史问题扩散到新模块 | 只读集成约束，基础行为取框架组件和 hooks |
| 新增第二套请求/权限/字典封装 | 绕过加解密、错误提示和统一权限 | 使用现有 `utils/`、`useDict`、`DictTag` |
| 报表页硬加增删改按钮 | 与只读业务不匹配 | 按业务形态决定操作，不套完整 CRUD |

## 检查

- [ ] API、类型、页面位置正确，没有绕过统一请求层。
- [ ] `VO` / `Form` / `Query` 分开，ID 精度保留。
- [ ] 已选择最小页面形态，并扫描现有 hooks、组件、字典、权限和页面壳。
- [ ] 没有复制业务模块，也没有新增第二套请求、权限、字典、分页或上传实现。
- [ ] 表单校验、loading、失败恢复、编辑回显、删除刷新完整。
- [ ] 构建通过；页面未验收时明确标注。
