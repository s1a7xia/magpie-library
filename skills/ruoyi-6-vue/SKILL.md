---
name: ruoyi-6-vue
description: "RuoYi-Vue-Plus 6.0.0 + Vue 3 开发配置：按任务只加载后端、前端、数据库、页面设计和官方文档地图，提供 6.0.0 源码约束、复用检查与验证门禁。用于已确认的 RuoYi 6.0.0 Vue 项目；也是全局默认技术 profile。触发：ruoyi-6-vue、RuoYi-Vue-Plus 6.0.0、若依Plus、plus-ui、Vue 页面、Java 业务代码、SQL。"
---

# RuoYi 6.0 Vue Development Profile

这是 **RuoYi-Vue-Plus 6.0.0 + Vue** 的单一技术入口，不按后端、前端、数据库拆成多个技能。先读 [common.md](references/common.md)，再只加载当前任务真正涉及的领域参考。

## 事实优先级

1. 当前项目自己的 `AGENTS.md`、`docs/agents/coding-standards.md` 和真实源码。
2. 本技能中以 6.0.0 源码核对过的约束。
3. [官方文档地图](references/docs-map.md) 指向的 RuoYi-Plus 文档站；该站正文默认以 3.5.x 为主线，不能替代 6.0.0 源码事实。
4. 通用 Spring Boot、MyBatis-Plus、Vue、Element Plus 习惯。

发生冲突时，以目标工程当前版本的源码、生成器模板和邻近业务实现为准。不要用示例路径、旧版 API 或文档站版本号猜目标工程。

## Load Map

| 任务范围 | 必读 | 按需追加 |
|---|---|---|
| 任何 RuoYi 6.0.0 业务改动 | [common.md](references/common.md) | — |
| Java / Spring Boot / MyBatis-Plus / Sa-Token | common | [backend.md](references/backend.md) |
| plus-ui Vue 3 / TypeScript / Element Plus | common | [frontend.md](references/frontend.md) |
| 表结构 / SQL / 字典 / 参数 / 菜单 | common | [database.md](references/database.md) |
| 可见页面、布局、样式、仪表盘 | common + frontend（改 Vue 时） | [ui-design.md](references/ui-design.md) |
| 需要查官方规范或功能说明 | common | [docs-map.md](references/docs-map.md) |
| 前后端或全栈切片 | common | 对应领域文件全部加载 |

页面可见改动还要按 `frontend-design` 的方法设计；`ui-design.md` 负责把 RuoYi 业务页收敛到既有产品边界。视觉结论只能来自渲染页面，按 `page-acceptance` 验收。

## Process

1. **定位版本与边界**：读取目标工程的 `pom.xml`、模块 POM、`package.json`/锁文件和现有目录；确认当前模块、构建命令与实际前端位置。6.0.0 后端常见基线是 Java 21、Spring Boot 4.1.1、MyBatis-Plus 3.5.17、Sa-Token 1.46.0，但以目标工程实际版本为准。前端可能是独立的 `plus-ui` 6.X-Vue 仓库，不假设它在后端仓库里。
2. **加载最小参考集**：按 Load Map 只读本次范围。跨模块改动再追加对应文件，不预读全部。
3. **先看真实实现**：修改现有模块前读目标 Controller/Service/Mapper、Vue 页面/API/hooks；新增标准 CRUD 前读生成器 `fm/` 模板和 demo。数据库改动先看现有表、字典、参数和脚本方言。
4. **做复用检查**：按 [common.md 的复用检查](references/common.md#repository-reuse-check) 搜索并读取候选实现、调用方和行为差异；确认现有能力不满足后才新增。跨模块调用优先 `ruoyi-api` 的接口与 DTO。
5. **实现与验证**：只做已确认范围；修改 Entity/BO/VO 映射后执行实际 Maven 编译以触发 MapStruct。前端按项目脚本构建或类型检查。通过 [Standards Gate](../rules/entry-protocol.md#standards-gate) 后才算完成当前阶段；页面行为与外观另走页面验收。

## Stage Integration

| 当前阶段 | 本配置提供 |
|---|---|
| think / grill | 框架复用、字段落列与 JSON、归属与审计、权限、可空更新、唯一性和状态流转；不打破单问题访谈节奏 |
| story | 把 DDL、Entity/BO/VO、API、权限、页面交互和验证写进现有 Issue 范围与验收标准 |
| implement | 读真实模板与邻近实现，按切片编码；映射变更后编译；保留工作流的门禁 |
| page-acceptance | 按 [page-acceptance](../page-acceptance/SKILL.md) 走真实 Vue 页面；具体浏览器命令见 [RuoYi 页面验收速查](../page-acceptance/references/ruoyi-6-vue-browser.md) |
| debug | 结合缺陷证据检查对应层级；先复现和定位，再改动 |
| review | Test 视角看可观察契约，Code 视角看框架/映射/前端约定，Impact 视角看权限、后台身份、脚本和跨模块影响 |

## Gotchas

| 现象 | 规则 |
|---|---|
| 把原版 RuoYi 写法混进 Plus | 禁止 `SecurityUtils`、`@PreAuthorize`、`AjaxResult`、`TableDataInfo`、`BeanUtils.copyProperties`；以目标源码的 Plus 接口为准 |
| 把 6.0.0 与 6.X-Vue 的版本号硬绑 | 后端 revision 与前端 `package.json` 可能不同；分别读取各自仓库和锁文件 |
| 每个配置都新建表 | 先查 `sys_config`、`sys_dict_*`、`sys_oss` 与现有业务表；配置、枚举和业务记录分开判断 |
| 已有工具被新 helper 覆盖 | 执行复用检查；写出选中的现有方法，或说明新增实现的具体缺口 |
| 后台任务直接取登录人 | 明确任务身份、归属和数据范围；`DataPermissionHelper.ignore` 只在有理由的范围内使用 |
| 只编译就宣称页面完成 | 编译只证明代码可构建；可见页面必须实际渲染验收 |
| 单领域任务加载全部参考 | 按 Load Map 加载；不要把“相关”理解成“全部” |

## Output

```text
Profile: ruoyi-6-vue — <scope; observed backend/frontend versions>
Loaded: common + <domain references>
Source/template evidence: <paths read>
Reuse evidence: <searched scope; reused path#method or concrete gap>
Applicable checks: <passed / findings / not applicable>
Page evidence: <rendered check or not applicable / not run>
Unfinished: <none / failed or blocked checks and next action>
```
