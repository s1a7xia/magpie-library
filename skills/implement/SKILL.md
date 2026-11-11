---
name: implement
description: "Implement an approved /story batch from remote Issues or stable local Markdown slices. Use only for explicit /implement; ordinary small implementation requests use Direct. Resolve the project profile, preserve the baseline, and record implementation, authorized checks and Git separately."
---

# Implement

推进已批准的纵向切片，不重新拆需求。先按 [入口协议](../rules/entry-protocol.md) 加载当前项目所需配置与技术 profile；`none` 明确禁止套用默认框架。小而明确的普通任务走 Direct，不为其建立 PRD。

## 输入门

- 显式 `/implement` 需要已冻结且已批准拆分的基线：PRD 为 `Sliced`、`In Progress` 或待补齐的 `Dev Complete`，`Grilled by` 有有效记录。
- 远端 Issue **或本地稳定 slice ID** 都是合法切片。每片具备验收标准、`Covers: R#/AC#` 与 `blocked-by`，完整映射需求。只有无切片列表的 PRD 才提示用户先 `/story`。
- 判断实际未决业务/模型选择，不用 `TODO`、`?` 或标题关键词机械阻塞；空/已解决 Open Questions、示例和 SQL 参数不算未决。基线仍有真实阻塞时停受影响片，不自动启动上游阶段。
- 涉及表、关系、唯一性、生命周期、索引或迁移：先按项目指定的数据库入口核对模型与当前 schema；未配置才用 [database-design](../database-design/SKILL.md)。RuoYi 落表规则见 [数据库参考](../ruoyi6/references/database.md)。读取模型不授权执行 SQL。

## 执行

1. 记录保护基线、批次 base 和切片清单，按依赖排序；已有混杂改动不碰。切片开始时写 `In Progress`。
2. 先读当前作者源码、能力地图、真实签名和使用方，复用实际能力，不整体复制业务模块。只按当前 profile 加载对应参考；RuoYi 页面采用 frontend 基线，`frontend-design` 只在用户明确要求美化/深度设计时叠加。
3. 最小充分实现验收标准。新发现的非阻塞业务细节采用安全推荐默认，完整实现 API/页面/数据/校验/反馈，并用 `TODO(待确认)` 记待确认事项、当前行为、后续调整与确认人；不能拿 TODO 代替功能。不可逆数据、权限或安全选择无安全默认时仅停受影响动作。
4. 核对 diff、字段/调用链与覆盖；按当前请求授权执行最小检查，未授权不运行测试/lint/类型检查/构建/浏览器。记录 `not run`，不把它当实现缺失，也不宣称运行通过。实现完整可写 `Dev Complete`；已知代码缺陷或缺行为仍为 `In Progress`。
5. 提交和推送按当前用户/项目明确授权，精确处理本片及对应状态，不碰旧暂存/脏改；无授权或非 Git 目录不阻断本地实现。记录提交/推送状态，不以 Git 成功代替实现或验证。
6. 批次结束核对每条 R#/AC# 的实现归属，更新适用 PRD、`project-state.md` 和 `verification.md` 一次；记录切片提交、batch base/final head、实际检查、TODO 和缺口。不创建缺乏依据的模板。

### 本地证据边界

本阶段只读本地代码/schema/项目文档、当前 profile 与 `docs/research/`；不自动联网调研。缺外部权威事实时停受影响片，明确问题并报告 `Next: /research`。本地事实推翻冻结基线则交用户裁决，不自动进入 think/grill，也不猜测绕过。

## 交付与停止

报告切片实现/覆盖、实际检查或未验证项、Git 状态、业务待确认与阻塞。手动门和回流只按 [共享契约](../rules/workflow-contract.md#4-验收门槛与回流)：先建议用户手动 `/review`，有页面影响再手动完整范围 `/page-acceptance`；非 UI 记 N/A。不自动启动任一阶段，不在 implement 写 `Done`。

恢复与记账细节按需读 [REFERENCE.md](REFERENCE.md)。
