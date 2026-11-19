---
name: ruoyi6
description: "RuoYi-Vue-Plus 6.x + plus-ui-React 业务模块的复用预检、实现和审查。预检/审查默认只读；只在明确要求实现或修复时修改文件。"
---

# RuoYi-Vue-Plus 编码约束

把任务正确落入当前 RuoYi checkout。技术事实以源码为准，不凭记忆使用版本、类名或方法签名。

## 选择参考

| 当前工作 | 读取 |
|---|---|
| 后端分层、接口、权限、事务、异常、导入导出、能力入口 | [backend.md](references/backend.md) |
| React 页面、API、类型、菜单路由、组件与交互 | [frontend.md](references/frontend.md) |
| 公共工具、转换、查询、文件、日期和通用能力 | [utils.md](references/utils.md) |
| 已确认契约在当前代码和 RuoYi/PostgreSQL 中的字段、字典/参数、菜单权限和增量脚本落点 | [database.md](references/database.md) |
| 业务场景对应的作者示例；新模块标准代码骨架 | [author-patterns.md](references/author-patterns.md)、[templates.md](references/templates.md) |
| 邮件、短信、消息推送、MQTT、缓存/队列、任务、工作流、OSS、AI、搜索和翻译等可选能力 | [capabilities.md](references/capabilities.md) |

只读当前切片实际涉及的 reference。

## 使用边界

- 普通单表、已有模块的小范围增量，按当前入口直接实现；出现主从、状态流转、导入批处理、异步、外部接入、数据隔离或可选能力时，再读对应 reference，不把所有流程套在每个切片上。
- 复用预检和审查默认只读；只有用户明确要求实现、修复或调整代码时才修改文件。
- 模板和作者示例提供骨架与场景，不替代当前业务契约；不要为套模板删减字段、校验、权限或失败路径。

## 编码约束

- 新模块按“项目契约 → `ruoyi-common-*` / `ruoyi-api` / `ruoyi-system` → 生成器骨架 → `ruoyi-demo` 场景”确定实现；已有模块按“项目契约 → 该模块现有分层、命名和集成契约 → 公共封装 → 生成器 / demo”增量修改。生成器是默认骨架，不覆盖当前公共封装和已确认的存量契约。
- 优先复用作者维护的 `ruoyi-system`、`ruoyi-demo`、`ruoyi-common-*`、`ruoyi-api`、公共组件和 hooks；不复制相邻业务模块，不另建请求、权限、字典、分页、上传或流程实现。
- 已有模块只延续其稳定风格，不复制其中已知重复的请求、权限、字典、分页、上传或错误处理；本切片涉及冲突时，以项目契约和当前公共封装为准。
- 遵循已确认的业务对象、归属、状态、权限、唯一性和删除规则；实现中发现契约冲突时，不自行改业务口径。
- 实现只覆盖当前切片需要的事务、幂等、并发、缓存、异步和异常路径，不预埋通用框架。
- 工具类优先使用 `org.dromara.common.core.utils` 及对应 `ruoyi-common-*` 封装；Service 业务失败抛 `ServiceException`；项目没有对应能力时再使用既有依赖。
- 后端功能权限与数据权限分开，菜单/按钮隐藏不替代后端鉴权。数据权限至少覆盖列表、详情、更新、删除、导出和关联记录。
- 字典只承载有限枚举，参数只承载运行期配置；业务身份、归属、唯一键、状态和常用查询字段落真实列。
- 涉及持久化时读取 [database.md](references/database.md)。数据模型尚未确定时先由 `database-design` 形成契约，本技能只承接已确认模型在 RuoYi/PostgreSQL 中的字段链路和迁移落点。
- 修改公共 API 或 `ruoyi-common-*` 时，先核对接口、实现和调用点；优先扩展已有入口，保持公开签名、泛型、返回值和异常语义兼容。

## 前后端与路由契约

创建或修改业务页面时，至少核对本次涉及项：

- 后端 Controller/Service/Mapper、请求 BO、响应 VO 与前端 `types.ts` 的字段、可空性和 ID 精度一致。
- API 路径、HTTP 方法、分页结构和前端请求函数一致。
- 菜单 `component`、`dynamicPage.tsx` 注册键、页面路径和权限字符一致；不发布没有实现入口的空菜单。
- 权限字符在菜单/按钮、后端注解和前端 `hasPermi` 三处一致。
- 列表、详情、写入、批量、导出和关联对象使用与业务契约一致的数据范围。

## 完成条件

- [ ] 已按新模块骨架、已有模块风格或实际复用入口说明实现依据；没有可复用入口时说明了新建理由。
- [ ] 没有复制相邻模块或发明平行基础设施。
- [ ] 本次涉及的接口、类型、页面、菜单、路由、权限、字典和数据链路已贯通。
- [ ] 本次涉及的查询范围、事务、异常、唯一性和状态规则已落实。
