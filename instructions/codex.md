## 通用技能触发

- RuoYi-Vue-Plus 项目在形成规格前需要核对框架/相邻模块的复用能力或技术落点时，读取 `ruoyi6` 做只读预检；修改 `ruoyi-modules/ruoyi-*` 后端，或 `plus-ui-React/src` 对应页面、API、类型、路由、菜单、组件前，必须先读取 `ruoyi6` 的 `SKILL.md`。
- 涉及持久化对象、表、字段语义、归属、关系、状态、唯一性、生命周期、删除/历史、JSONB 或迁移时，先读取 `database-design` 的 `SKILL.md`。
- 单会话内存在会改变结果的真实歧义时，先读取 `grill-with-docs` 的 `SKILL.md`；目标和验收已明确则直接推进。
