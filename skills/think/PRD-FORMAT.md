# PRD Format

## 用途

PRD 文件格式模板。仅当项目已经使用 PRD，或用户明确要求创建 PRD 时使用；普通任务可以直接用对话、现有规格或项目文档承接。

## 文件位置

`docs/prd/PRD-NNNN-<title>.md`

**归档规则（强制）**:

- **只放在 `docs/prd/`**：PRD 文件只属于 `docs/prd/`。**绝不放在仓库根、`docs/` 根、或 `docs/adr/`**。
- **PRD ≠ ADR**：PRD 记录"要做什么（what + why）"，ADR 记录"难逆转的技术决策"。两者的目录和编号空间相互独立（`PRD-0011` 与 ADR 的 `0011` 靠目录和前缀区分，天然不冲突）。ADR 的归档见 [ADR-FORMAT](../grill/ADR-FORMAT.md)。
- **命名前缀固定为 `PRD-`**：文件名必须以 `PRD-NNNN-` 开头，**不要写成 `prd-NNNN-`（小写）或无前缀**。

**命名规则**:

- **NNNN**：四位零填充序号（0000-9999）。由需求阶段（`think`）决定创建 PRD 时自动分配：扫描 `docs/prd/` 下现有 `PRD-NNNN-*.md` 文件，取最大序号 +1。首次创建从 `0000` 开始。**分配前先确认该号未被占用**——多个会话并发时，扫描后、写入前可能有别的会话抢占了同号，此时取下一个可用号而非覆盖。
- **创建前去重**：分配编号前先做 PRD 冲突检查（按 title slug 与 `## Goal` 比对现有 PRD），发现疑似重复时询问用户。完整流程见 [think/REFERENCE.md §PRD Conflict Check](REFERENCE.md#prd-conflict-check-before-assigning-nnnn)。
- **title**：语义标题，使用 kebab-case（小写字母 + 连字符）。简明描述 PRD 主题，与 `# <Feature Name>` 标题对应。
- 示例：`PRD-0000-agent-runtime-evolution.md`、`PRD-0005-minio-storage-switch.md`

**文档语言**: 项目已配置 `docs/agents/language.md` 时遵循它；未配置时跟随用户当前语言，不因缺少该文件中断任务。详见 [Skill Entry Protocol](../rules/entry-protocol.md)。

**为什么用编号**:
- 稳定短引用：Issue、commit、对话中 `PRD-0005` 比 `minio-storage-switch.md` 精确且不受改名影响
- 创建顺序可见：编号反映 PRD 创建的先后关系
- 状态追踪：结合 `## Status` 字段可快速建立实现全景表

## PRD 生命周期状态

PRD 在其生命周期内经历以下状态，每个状态的进入由可验证证据驱动：

```
Draft → Grilled → Sliced → In Progress → Done
  └─────────────────────────────────→ Deprecated
```

| 状态 | 进入条件 | 设置者 |
|------|---------|--------|
| **Draft** | PRD 文件创建，`Open Questions` 尚未全部解决 | 需求阶段（`think`） |
| **Grilled** | 当前交付所需的决策已解决，术语和影响已确认 | 设计验证（可选） |
| **Sliced** | 已记录独立交付切片；Issue 不是必需产物 | 任务拆解（可选） |
| **In Progress** | 至少一个切片进入实现 | 实现阶段 |
| **Done** | 所有 Acceptance Criteria 有按授权取得的证据；未验证项已明确说明 | 实现收口或人工确认 |
| **Deprecated** | PRD 被放弃或替代（从任意前置状态可达） | 人工标记 |

**状态与代码的关系**: `Done` 以实际实现和当前授权范围内取得的证据为准，不依赖 Issue 关闭状态或口头确认：
- 用户可观察的验收项有对应证据；未授权或环境不可用时单列未验证边界
- 当前请求涉及测试、构建或运行验收时，记录实际执行的检查及结果
- 允许保留的待确认项必须写明当前实现和调整条件，不能用 TODO 掩盖缺失能力

**Status 字段格式**（放在 PRD 模板中 `# <Feature Name>` 之后的第一行）:

```markdown
> **Status**: Draft | **PRD**: PRD-NNNN | **Created**: YYYY-MM-DD | **Last updated**: YYYY-MM-DD
```

## 模板

```markdown
# <Feature Name>

> **Status**: Draft | **PRD**: PRD-NNNN | **Created**: YYYY-MM-DD | **Last updated**: YYYY-MM-DD

## Goal

<why + what in one paragraph>

## What I already know

* <facts from user message>
* <facts discovered from repo/docs>

## Assumptions (temporary)

* <assumptions to validate>

## Open Questions

* <ONLY Blocking / Preference questions; keep list short>

## Requirements

* <requirement 1>
* <requirement 2>

## Acceptance Criteria

* [ ] <testable criterion 1>
* [ ] <testable criterion 2>
* [ ] <testable criterion 3>

## Definition of Done

* Acceptance criteria met, or each remaining gap explicitly marked unverified
* Checks required by the current request executed and recorded
* Affected existing docs updated when behavior changes
* Rollout/rollback considered only for the risks actually in scope

## Out of Scope

* <what we will not do in this task>

## Technical Approach

<key design + decisions>

## Research References

* [research topic](docs/research/<stack>-<topic>-<major>.md) — <one-line takeaway>

**填充规则**：当本 PRD 的技术方案引用了调研阶段产出的研究记录时，在此列出。每条格式：`[主题](docs/research/<stack>-<topic>-<major>.md) — 一句话结论`。

- 引用项目实际维护的 `docs/research/*.md` 记录（权威信源、版本化、不可变）。
- 不要在此放临时搜索结果或非权威信源链接——那些属于 `## Technical Notes`。
- 若本 PRD 的决策被采纳并升格为 ADR，ADR 的 `## References` 也会引用同一研究记录（research 是证据层，PRD/ADR 是决策层，引用不复制）。

## Feasible Approaches

**Approach A: <name>** (Recommended)

* How it works:
* Pros:
* Cons:

**Approach B: <name>**

* How it works:
* Pros:
* Cons:

## Decision (ADR-lite)

**Context**: Why this decision was needed
**Decision**: Which approach was chosen
**Consequences**: Trade-offs, risks, potential future improvements

## Implementation Plan (small PRs)

* PR1: <scaffolding + minimal plumbing>
* PR2: <core behavior>
* PR3: <edge cases + docs + cleanup when required>

## Technical Notes

* <files inspected, constraints, links, references>
* <research notes summary if applicable>

## Traceability

- **Created by**: requirement/design stage (or task slicing for a minimal PRD)
- **Prototyped by**: <authorized prototype or experiment> (<YYYY-MM-DD>) — if evidence adjudicated a design option — <divergence> → <selected X / eliminated Y, because <evidence>>
- **Grilled by**: design validation (optional; completed <YYYY-MM-DD>) — <summary: terms sharpened, assumptions resolved, records created>
- **Sliced by**: task slicing (optional; completed <YYYY-MM-DD>) — slices recorded below
- **Sliced into**:
  - #<issue-1> — [PRD-NNNN] <slice title> (AFK) — Done
  - #<issue-2> — [PRD-NNNN] <slice title> (HITL, blocked by #<issue-1>) — In Progress
  - #<issue-3> — [PRD-NNNN] <slice title> (AFK)
- **Implemented by**: implementation stage (optional Issue reference)
- **Debugged by**: debug stage (if a bug fix touched this feature) — <bug summary + root cause>
- **Arch reviewed by**: <review or decision record> (if architecture review performed) — <finding summary>
- **Reviewed by**: review stage (optional PR reference)
- **New terms**: <domain terms found during review, for CONTEXT.md>
- **New decisions**: <decisions made during implementation, for ADR>

## Issue

#<issue-number>（父 Issue，如有）
```

## 字段说明

| 字段 | 说明 |
|------|------|
| Status | PRD 生命周期状态（Draft / Grilled / Sliced / In Progress / Done / Deprecated） |
| PRD | PRD 编号（四位零填充，如 PRD-0000） |
| Goal | 一句话描述为什么和做什么 |
| What I already know | 已知事实（来自用户和代码库） |
| Assumptions | 需要验证的临时假设 |
| Open Questions | 仅阻塞/偏好问题 |
| Requirements | 功能需求列表 |
| Acceptance Criteria | 可测试的验收标准 |
| Definition of Done | 完成定义（团队质量标准） |
| Out of Scope | 明确不做的事情 |
| Technical Approach | 技术方案和关键决策 |
| Research References | 项目研究记录引用（`docs/research/*.md`，含一句话结论；临时搜索结果放 Technical Notes） |
| Feasible Approaches | 可行方法（2-3个选项）|
| Decision (ADR-lite) | 决策记录（轻量级ADR）|
| Implementation Plan | 实施计划（拆分成小PR）|
| Technical Notes | 技术笔记 |
| Traceability | 全链路追踪（各 skill 阶段自动填充）|
| Issue | 对应的 Issue 编号 |
| Sliced into | 已批准切片列表；如发布 Issue，可记录编号，否则直接记录切片标题和依赖 |
