---
name: to-spec
description: 把当前对话中已经确认的内容合成为可验收 spec；不做访谈。默认保存为项目内 Markdown，只有明确授权时才发布到外部 issue tracker。
---

# To Spec

使用当前 conversation context 和 codebase understanding 产出 spec。**不要**访谈用户，只综合已经知道的内容；未知或未决定项必须明确标出，不能补写成已确认事实。

Issue tracker 若已配置，按其约定保存。**没有明确外部写入授权时，默认写到项目内本地文件**，例如 `.scratch/<feature-slug>/spec.md`；不要自行调用 `gh issue create`、`glab issue create`、添加标签或在外部 tracker 上评论。需要外部发布时，先把拟发布内容给用户确认。

## 流程

1. 如果还没有探索 repo，先探索它以理解 codebase 当前状态。spec 始终使用项目 domain glossary vocabulary，并遵守相关 ADRs。
2. 草拟准备使用或新增的 seams，优先复用高层现有 seam；seam 越少越好。若需求含持久化对象、字段语义、身份/归属、状态、唯一性、删除/历史或 JSONB，先确认 `database-design` 的结论。
3. 写明用户可观察的验收方式、范围外事项、未决项和需要单独授权的动作。不要把未运行的测试或未检查的页面写成已验证。
4. 使用下面模板写 spec。默认保存到项目内并报告路径；只有用户明确要求发布到外部 tracker，才按已配置方式发布并应用对应标签。

<spec-template>

## Problem Statement

用户正在面对的问题，从用户视角描述。

## Solution

问题的解决方案，从用户视角描述。

## User Stories

一份完整的编号 user stories 列表。每条使用以下格式：

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

覆盖 feature 的所有方面，包括失败路径和权限边界。

## Implementation Decisions

已作出的 implementation decisions：

- 将 build/modify 的 modules
- 将 modify 的 module interfaces
- 来自 developer 的技术澄清
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

不要包含容易过时的具体 file paths 或大段 code。例外：如果 prototype 产出的 snippet 比 prose 更精确地编码了某个决策（state machine、reducer、schema、type shape），可以内联决策密集部分并注明来自 prototype。

## Testing Decisions

已作出的 testing decisions：

- 什么是好测试：只验证 external behavior，不测试 implementation details
- 哪些 modules 会被测试
- 测试的 prior art（codebase 中类似类型的 tests）
- 当前任务是否已经明确授权测试；未授权时写明“待授权”，不要自动执行

## Out of Scope

本 spec 明确不做的事项。

## Further Notes

风险、开放问题、依赖和需要单独授权的动作。

</spec-template>

## 输出

报告 spec 路径，并给出 3–5 条摘要：目标、关键决策、验收证据、未决项、下一步。若存在阻塞性未知，停止在 spec，不进入实现。
