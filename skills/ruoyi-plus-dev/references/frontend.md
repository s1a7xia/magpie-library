# Frontend Reference

用于 plus-ui 的 Vue 3 / TS / Element Plus 与 React / Ant Design Pro 页面和 API。先读 [common.md](common.md) 的流程、复用检查和交付门禁；出现可见页面改动时再读 [ui-design.md](ui-design.md)。先看目标项目的 `gen_table.frontend_type`、`fm/<frontendType>/` 模板和现有页面，不要把两套组件体系混用。

## 目录与组件契约

- API、类型和页面分开：`src/api/<module>/<business>/{index.ts,types.ts}` 与 `src/views/<module>/<business>/index.vue`。
- 页面使用 `<script setup name="Xxx" lang="ts">`；组件 `name` 与菜单路由 `name` 保持一致，否则 keep-alive 缓存会失效。
- 修改前读同模块的两三个兄弟页面、现有 API 和 hooks，沿用页面壳、表格、表单、弹窗和主题 token；不要为单页另造一套组件体系。

## API 与类型

- 请求统一走 `@/utils/request`；`AxiosPromise` 从 `@/utils/api-types` 引入，`PageResult` 从 `@/api/types` 引入。分页读取 `res.data.rows`/`res.data.total`，树表读取 `res.data` 数组。
- VO、Form、Query 按职责定义，不把页面表单和列表返回混成一个万能类型。主键及关联 ID 使用 `string | number`，并核对实际 JSON 序列化：联合类型无法挽回已经被 JSON number 舍入的雪花 ID。
- 日期、状态、字典值和可空字段与后端契约一致；查询走 `params`，请求体走 `data`，下载复用现有请求工具。
- 不绕过 Axios 拦截器直接请求后端；鉴权、RSA/AES 加解密、错误提示和参数序列化由现有请求链处理。

## 页面交互

- 复用 `useLoading`、`useFormDialog`、`useSearchReset`、`useSearchToggle`、`useTableSelection` 等现有 hooks。`openDialog` 会重置表单，编辑回填后使用 `showDialog`。
- 表单提交保留校验、按钮 loading 和失败恢复；请求失败时保留用户输入并恢复加载状态，状态开关失败时回滚。
- 字典使用 `useDict` / `DictTag`，按钮权限使用 `v-hasPermi` 或 `checkPermi`。视觉调整不得隐藏、伪造或绕过权限控制。
- 保留已有复杂交互：树筛选、列显隐、导入导出、分页、抽屉、选择弹窗、授权和批量操作。美化只改善层级、间距、状态与信息表达。
- 单页样式限定在本页作用域，不覆盖全局主题；需要主题调整时改 token，不在组件里散落硬编码色值。

## 页面设计

- 业务 CRUD 页按 `frontend-design` 的 Enhance 模式处理：Element Plus 和若依内置组件就是设计系统，重点做信息层级、密度、语义状态和空/错/无权限状态。
- 登录页、工作台、态势大屏和独立展示页可按 Design 模式完整设计；进入 RuoYi 业务页后仍要服从 [ui-design.md](ui-design.md) 的组件与交互边界。
- 不把“好看”作为唯一验收条件。视觉改动要有渲染截图，并按 [page-acceptance](../../page-acceptance/SKILL.md) 检查主路径和一个边界。

## React 分支

- 仅当目标工程的 `frontendType=react` 或现有前端确为 React 时使用；模板与现成页面优先于通用习惯。
- 请求从 `@/api/request` 引入，类型使用 `R`/`PageResult`；列表页沿用 `PageContainer`、`ProTable`、`ModalForm`、`ActionType`。
- 权限用 `useUserStore` 的 `userInfo` 与 `hasPermi`；表格选择、字典、日期范围、导出分别沿用 `useTableSelection`、`useDict`/`dictOptions`、`useDateRangeQuery`、`useTableExport`。
- 文件、图片和富文本沿用 React 工程已有的 `FileUpload`、`ImageUpload`、`ImagePreview`、`RichTextEditor`；不要把 Vue 的 `v-hasPermi`、Element Plus 或 Pinia 写法带进来。

## 构建与检查

- 从实际 `package.json`、锁文件和 CI 读取包管理器与脚本；官方 plus-ui 6.1 使用 pnpm，但不要把它当成所有项目的固定事实。
- 至少执行项目已有的前端构建或类型检查；只在用户要求时运行额外 lint/test，不自行扩展测试范围。
- 编译、类型检查通过不等于页面验收通过。页面可见改动在真实浏览器验收前，只能标记为“开发完成、未验收”。
