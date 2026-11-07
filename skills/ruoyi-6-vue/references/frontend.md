# Frontend Reference — plus-ui 6.1.0

用于 `codex/p0-integration` 中 `plus-ui` 6.1.0 的 **Vue 3 / TypeScript / Element Plus** 页面、API 与样式。先读 [common.md](common.md) 的流程、复用检查和交付门禁；涉及 `utils/request`、路由、Pinia、layout、hooks 或全局组件时，先读 [frontend-shell.md](frontend-shell.md)；出现可见页面改动时再读 [ui-design.md](ui-design.md)。

## 版本与目录

- 本地基线的 `plus-ui/package.json` 是 6.1.0，依赖为 Vue 3.5.44、Element Plus 2.14.7、Vite 8.3.5、pnpm 10.34.5；不要据此反推后端版本。
- 先读目标工程的 `package.json`、锁文件、`vite.config` 和现有页面，再决定命令。`codex/p0-integration` 的前端在同仓 `plus-ui/`。
- API、类型和页面分开：`src/api/<module>/<business>/{index.ts,types.ts}` 与 `src/views/<module>/<business>/index.vue`。请求返回值、动态路由、页面缓存和全局 store 的实际链路见 [frontend-shell.md](frontend-shell.md)。
- 页面使用 `<script setup name="Xxx" lang="ts">`；组件 `name` 与菜单路由 `name` 保持一致，否则 keep-alive 缓存会失效。
- 修改前读同模块的两三个兄弟页面、现有 API 和 hooks，沿用页面壳、表格、表单、弹窗和主题 token；不要为单页另造一套组件体系。

## API 与类型

- 请求统一走 `@/utils/request`；`AxiosPromise` 从 `@/utils/api-types` 引入，`PageResult` 从 `@/api/types` 引入。拦截器解析后读取 `res.data`；分页再读 `res.data.rows`/`res.data.total`，树表读取 `res.data` 数组。
- VO、Form、Query 按职责定义，不把页面表单和列表返回混成一个万能类型。主键及关联 ID 使用 `string | number`，并核对实际 JSON 序列化：联合类型无法挽回已经被 JSON number 舍入的雪花 ID。
- 日期、状态、字典值和可空字段与后端契约一致；查询走 `params`，请求体走 `data`，下载复用现有请求工具。
- 不绕过 Axios 拦截器直接请求后端；鉴权、RSA/AES 加解密、错误提示和参数序列化由现有请求链处理。

## 页面交互

优先复用 6.X-Vue 已有 hooks，不复制一套局部实现；完整入口和标准 CRUD 骨架见 [frontend-shell.md](frontend-shell.md)。

| 能力 | 现有入口 |
|---|---|
| 加载态 | `@/hooks/async/useLoading` |
| 表单弹窗生命周期 | `@/hooks/dialog/useFormDialog`、`useDialogState` |
| 搜索重置/折叠 | `@/hooks/form/useSearchReset`、`useSearchToggle` |
| 表格选择 | `@/hooks/table/useTableSelection` |
| 树折叠/树表展开 | `@/hooks/tree/useTreeCollapsed`、`useTreeTableExpand` |
| 日期范围查询 | `@/hooks/form/useDateRangeQuery` |

- `openDialog` 会重置表单，编辑回填后使用 `showDialog`；具体签名以目标版本 hooks 为准。
- 表单提交保留校验、按钮 loading 和失败恢复；请求失败时保留用户输入并恢复加载状态，状态开关失败时回滚。
- 字典使用 `@/utils/dict` 的 `useDict` / `DictTag`，按钮权限使用 `v-hasPermi` 或 `checkPermi`。视觉调整不得隐藏、伪造或绕过权限控制。
- 保留已有复杂交互：树筛选、列显隐、导入导出、分页、抽屉、选择弹窗、授权和批量操作。美化只改善层级、间距、状态与信息表达。
- 单页样式限定在本页作用域，不覆盖全局主题；需要主题调整时改 token，不在组件里散落硬编码色值。

## 页面设计

- 业务 CRUD 页按 `frontend-design` 的 Enhance 模式处理：Element Plus 和若依内置组件就是设计系统，重点做信息层级、密度、语义状态和空/错/无权限状态。
- 登录页、工作台、态势大屏和独立展示页可按 Design 模式完整设计；进入 RuoYi 业务页后仍要服从 [ui-design.md](ui-design.md) 的组件与交互边界。
- 不把“好看”作为唯一验收条件。视觉改动要有渲染截图，并按 [page-acceptance](../../page-acceptance/SKILL.md) 检查主路径和一个边界。

## 构建与检查

- 从实际 `package.json`、锁文件和 CI 读取包管理器与脚本；官方 6.X-Vue 使用 pnpm，但不要把它当成所有项目的固定事实。
- 至少执行项目已有的前端构建或类型检查；只在用户要求时运行额外 lint/test，不自行扩展测试范围。
- 编译、类型检查通过不等于页面验收通过。页面可见改动在真实浏览器验收前，只能标记为“开发完成、未验收”。

## 非 Vue 工程

如果目标工程不是 Vue/Element Plus，停止使用本文件的前端细节，改读项目的 `docs/agents/coding-standards.md` 和实际前端工程。`ruoyi-6-vue` 不覆盖 React 分支，也不把 React 写法混入 Vue 页面。
