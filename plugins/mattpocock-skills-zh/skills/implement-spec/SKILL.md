---
name: implement-spec
description: 在已授权时按 spec 和 tickets 的 task graph 实现整个功能；由实现者子代理在隔离 worktree 中并行推进。适用于用户要求实现一份已拆票的 spec。
disable-model-invocation: true
---

# 实现 Spec

你已拿到一份 spec，以及与之关联的 tickets。Tickets 是一个带 blocking edges 的 **task graph**，不是线性步骤清单；始终应从 blockers 已完成的 **frontier** 中领取工作。

Issue tracker 若未配置，提示用户显式运行 `setup-matt-pocock-skills` 技能。**没有明确授权时，不得创建或修改外部 Issue、PR 或 push；技能定义内的隔离 worktree、任务分支、本地提交和 integration branch 合并除外。**

## 授权等级

先根据当前任务确定执行模式，不要默认升级：

本技能被调用时默认采用 C（子代理编排）；只有用户明确要求串行、禁止子代理，或宿主无法启动子代理时，才使用 B 或降级模式。

### A. 未调用本技能：当前会话、单写入者

- 在当前工作区按 task graph 顺序实现；一次只处理一个可领取的 ticket 或最小充分切片。
- 按项目规范复用现有能力，写清每项的验收证据。
- 测试、提交、PR 仍按当前任务另行授权；未要求测试就只做实现和静态核对。
- 所有 ticket 完成后，仅在用户明确要求审查时调用 `code-review`。

### B. 用户明确要求串行：单写入者分支

只有用户明确要求使用 integration branch / worktree、但同时要求不使用子代理时：

- 在项目当前 Git 约定下创建或使用 integration branch；
- 从一个 ticket 开始，完成、核对、纳入 integration branch，再处理下一个；
- 不擅自清理用户已有 worktree、分支或未提交改动。

### C. 技能授权：子代理并行编排

用户显式调用或要求 `implement-spec` 实现已拆票的 spec 时，即授权本技能启动以下实现编排，无需再次确认子代理。该授权覆盖本技能完成当前 spec 所需的隔离 worktree、任务分支、本地提交和合并到 integration branch；push、PR、Issue 写入、测试和发布仍按当前任务另行授权。

1. 阅读 spec 和 tickets，确认依赖图、共享接口和合并顺序。
2. 可选地启动 exploration subagent，把相关代码或外部文档的 Markdown notes 存到所有实现者都能访问的 repo 外目录；不要让它直接改产品代码。
3. 每个 implementer subagent 使用独立 worktree 和 branch；启动前确认基点是 integration branch，结束时把 integration branch 的最新提交合并进自己的分支。
4. 每个 implementer 只实现一个 ticket，按项目规范和当前已授权范围实现；本插件未提供 `tdd`，若任务要求 TDD，应按项目既有测试规范手工采用 red-green-refactor，不声称调用不存在的技能。
5. 使用 merger subagent 依次把完成项合并到 integration branch；每次合并后重新计算 frontier，只对有独立可领取 ticket 的工作启动更多实现者。
6. 所有 tickets 完成后，仅在用户明确要求审查时，在 integration branch 上调用 `code-review`。审查发现只在当前实现授权范围内修复。
7. 清理本任务创建且已确认归属的 worktree；不触碰其他 worktree、分支或用户改动。

## 共同步骤

1. 先读 spec、tickets、项目 `AGENTS.md`、术语表、ADR、状态文档和相关代码；用 context pointers 指向这些事实，不重复粘贴。
2. 确认每个 ticket 的目标、验收、数据/API/权限影响和 blocking edges；发现规格缺口时停止扩大实现，先记录并解决会影响正确性的决策。
3. 在项目中实现 tracer-bullet 纵向切片；优先复用现有 seam、模块、组件和测试入口。
4. 每完成一项就核对 diff、调用链、受影响文档和验收证据；不把未运行的验证写成已通过。
5. 按 issue tracker 的工作方式收尾；没有 tracker 或没有外部写入授权时，只报告本地完成状态和下一步。
6. 最终报告：已交付行为、tickets 状态、实际验证证据、未验证边界、剩余风险，以及需要用户授权的外部动作。

