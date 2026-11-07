# Soybean Admin / Naive UI 可选前端参考

仅在目标项目**实际采用** `ruoyi-plus-soybean` 或同类的 `Vue 3 + Soybean Admin + Naive UI` 前端时加载。它不是官方 `plus-ui` 的替代品，也不改变本技能默认的 Element Plus 约束。

## 已核实的差异

- 参考仓库 `m-xlsea/ruoyi-plus-soybean` 默认分支为 `master`，`package.json` 名称是 `ruoyi-vue-plus`，版本 `2.2.0`。
- 前端核心是 Vue 3.5、TypeScript、Vite、Naive UI、UnoCSS、Pinia 和 Soybean Admin 的 monorepo 包；不是 Element Plus。
- 它复用 RuoYi-Vue-Plus 后端能力，但页面、权限 hook、请求层和组件体系是另一套实现。不能把它的 `NDataTable`、`NDrawer` 或 service 代码直接复制进 plus-ui。
- 目录包含 `src/views`、`src/service`、`src/theme`、`src/layouts`、`src/components` 和 `packages/`；具体页面结构以目标项目版本为准。

## 可以借鉴什么

只在“项目本来就用 Soybean”时借鉴其信息组织和交互：

- 列表页把搜索、表格操作、列设置和分页拆成独立区域，减少单文件复杂度。
- 新增/编辑使用抽屉承载中等复杂度表单；表单校验、提交 loading、关闭和刷新行为分明。
- 表格状态使用语义标签，行操作用图标按钮并保留权限判断；搜索和重置只保留一组。
- 主题集中放在 `src/theme`，页面不散落硬编码颜色；深色模式与组件主题一起验证。
- 主页可参考其 KPI/图表的信息层级，但业务数据、权限和空状态仍由本项目提供。

## 不能做什么

- 不把现有 plus-ui 页面整体改写成 Naive UI；那是一次前端栈迁移，不是页面美化。
- 不混用 Element Plus 与 Naive UI 的全局样式、弹窗、表单和消息系统。
- 不照搬参考仓库的登录、RSA/AES、Sa-Token、菜单或接口封装；先核对目标后端的实际契约。
- 不因参考仓库好看就替换现有设计系统。只借鉴布局、信息密度和状态表达，组件与交互仍服从当前项目。

## 判断是否采用

如果只是现有 RuoYi 项目的业务页美化，继续使用 [frontend.md](frontend.md) 和 [ui-design.md](ui-design.md)。只有在新项目明确选择 Soybean 前端，或现有项目已经完成该前端栈迁移时，才把本文件作为补充参考，并单独建立该前端的构建、鉴权和页面验收事实。

参考：<https://github.com/m-xlsea/ruoyi-plus-soybean>
