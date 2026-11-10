# PRD Format

## 用途

PRD 文件格式模板。由 `think` 或 `story`（无 PRD 时）生成和维护。

## 文件位置

`docs/prd/PRD-NNNN-<title>.md`

**归档规则（强制）**:

- **只放在 `docs/prd/`**：PRD 文件只属于 `docs/prd/`。**绝不放在仓库根、`docs/` 根、或 `docs/adr/`**。
- **PRD ≠ ADR**：PRD 记录"要做什么（what + why）"，ADR 记录"难逆转的技术决策"。两者的目录和编号空间相互独立（`PRD-0011` 与 ADR 的 `0011` 靠目录和前缀区分，天然不冲突）。ADR 的归档见 [ADR-FORMAT](../grill/ADR-FORMAT.md)。
- **命名前缀固定为 `PRD-`**：文件名必须以 `PRD-NNNN-` 开头，**不要写成 `prd-NNNN-`（小写）或无前缀**。

**命名规则**:

- **NNNN**：四位零填充序号（0000-9999）。由 `/think` 创建时自动分配：扫描 `docs/prd/` 下现有 `PRD-NNNN-*.md` 文件，取最大序号 +1。首次创建从 `0000` 开始。**分配前先确认该号未被占用**——多个会话并发时，扫描后、写入前可能有别的会话抢占了同号，此时取下一个可用号而非覆盖。
- **创建前去重**：分配编号前先做 PRD 冲突检查（按 title slug 与 `## Goal` 比对现有 PRD），发现疑似重复时询问用户。完整流程见 [think/REFERENCE.md §PRD Conflict Check](REFERENCE.md#prd-conflict-check-before-assigning-nnnn)。
- **title**：语义标题，使用 kebab-case（小写字母 + 连字符）。简明描述 PRD 主题，与 `# <Feature Name>` 标题对应。
- 示例：`PRD-0000-agent-runtime-evolution.md`、`PRD-0005-minio-storage-switch.md`

**文档语言**: 跟随项目配置 `docs/agents/language.md`（由 `/setup-project` 写入）。若未配置，回退到用户输入语言并询问团队偏好。详见 [Skill Entry Protocol](../rules/entry-protocol.md)。

**为什么用编号**:
- 稳定短引用：Issue、commit、对话中 `PRD-0005` 比 `minio-storage-switch.md` 精确且不受改名影响
- 创建顺序可见：编号反映 PRD 创建的先后关系
- 状态追踪：结合 `## Status` 字段可快速建立实现全景表

## PRD 生命周期状态

> 此表是 PRD 与切片生命周期的唯一来源；`story`、`implement`、`page-acceptance`、`review` 引用这里，不复制完整状态定义。

PRD 在其生命周期内经历以下状态，每个状态的进入由可验证证据驱动：

```
Draft → Grilled → Sliced → In Progress → Dev Complete → Accepted → Done
  └─────────────────────────────────→ Deprecated
```

| 状态 | 进入条件 | 设置者 |
|------|---------|--------|
| **Draft** | PRD 文件创建，`Open Questions` 尚未全部解决 | `/think` |
| **Grilled** | 所有 Open Questions 已解决，Assumptions 已验证，Exhaustiveness Gate 通过；或冻结后目标/范围不变、`Change Log` 已登记、需补拆新增或变更的 `R#` / `AC#` | `/grill`；增量变更由 `/grill` 或用户显式改回 |
| **Sliced** | PRD 已拆分为 Issues，Traceability 的 `Sliced into` 列表已填充 | `/story` |
| **In Progress** | 至少一个 Child Issue 开始实现 | 实现工作流首次执行 |
| **Dev Complete** | 所有切片代码写完、编译通过、已提交推送，但**未做页面测试** | `implement` 批次结束 |
| **Accepted** | 用户发起的页面测试通过，确认缺陷已修复并复测，验收证据已落盘 | `page-acceptance` 通过 |
| **Done** | 当前行为已有有效 `Accepted` 证据，用户显式发起的完整 review 通过，项目收尾条件满足 | `/review`；若有行为修复，则在修复点 `page-acceptance` 通过后写回 |
| **Deprecated** | PRD 被放弃或替代（从任意前置状态可达） | 人工标记 |

**状态与代码的关系**: `Done` 判定以代码和验收证据为准——不依赖 Issue 关闭状态或口头确认，而是验证：
- 对应功能代码已按当前同一分支的提交与推送约定完成；不要求另建分支或远端 Issue
- 声明的页面测试范围已通过，Acceptance Criteria 已按实际验证结果勾选（用户明确要求但未运行的测试必须标为未验证，不能写成通过）
- 无 `[TEMPORARY]` / `TODO(prd-NNNN)` 残留标记

**验收与修复回流**：证据记录被验证的代码版本、范围与环境。后续实现或 debug 改变已验收行为时，受影响切片从 `Accepted` / `Done` 退回 `Dev Complete`（编译未通过则为 `In Progress`），标明旧验收及 review 结论失效范围与待复测路径；父 PRD 同步退回，未受影响切片保留状态。仅文档提交或不影响已验证行为的无关改动，不因 HEAD 改变而要求重测。

标准顺序是 `implement → 首次全范围 page-acceptance → review（内嵌 debug）→ 修复点 page-acceptance → Done`。review 开始前必须有首次页面验收；不能用修复点验收替代首次验收。review 一轮内完成发现、修复和剩余范围检查，整轮结束后才由用户发起修复点验收，只覆盖修复点及连带路径。修复改变已验收行为时，旧验收先失效并退回 `Dev Complete`；修复点验收通过后恢复 `Accepted`，本轮 review 已覆盖最终代码即可恢复 `Done`。若整轮 review 没有修复，首次验收继续有效。验收证据保留历史并标注被哪次验证替代，不伪称旧代码上的检查覆盖新行为。

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

## Domain Terms (draft — for /grill to refine)

> 可选章节。仅当头脑风暴中出现了新领域概念时由 `/think` Step 10b 追加。这些是**草稿**术语，`/grill` 负责把它们推进 `CONTEXT.md` 或标记冲突；`/think` 不直接写 `CONTEXT.md`。没有新术语时整节省略。

| Term | Working Definition | Status |
|------|--------------------|--------|
| <term> | <one-sentence working definition> | new / needs sharpening / conflicts with existing |

## Requirements

* R1 — <requirement 1>
* R2 — <requirement 2>

## Acceptance Criteria

* [ ] AC1 — <testable criterion 1>
* [ ] AC2 — <testable criterion 2>
* [ ] AC3 — <testable criterion 3>

需求与验收标准使用稳定 ID（`R1`、`AC1`），供 `story` 的 `Covers` 和 `implement` 的覆盖门引用。基线冻结后不得重新编号；旧 PRD 缺少 ID 时，在 `## Change Log` 记一行“仅补充编号”，再补齐。

## Definition of Done

* 声明的验收标准已在约定范围内验证通过，未验证项已列明
* 每条需求至少有一条可观察的验收标准；切片后每条验收标准都有明确切片承接
* 受影响的前后端编译通过；用户明确要求的其他检查通过
* 行为变化涉及的文档已同步
* 有风险时已说明上线与回退方式

## Change Log

Baseline changes after `Grilled` go here — one row per change. Additive changes (a new field, an extra validation, an added state) keep the baseline valid: set the PRD back to `Grilled`, mark affected slices `Dev Complete`, invalidate their old acceptance evidence, then re-run `story` for the new or changed `R#` / `AC#`; unaffected slices keep their state and evidence. If the goal or scope itself changes materially, set the PRD back to `Draft` and re-run `think` → `grill`.

| Date | Change | Why / who asked | Affected slices |
|---|---|---|---|
| <YYYY-MM-DD> | <what changed> | <business reason, requester> | <#issue or none> |

## Out of Scope

* <what we will not do in this task>

## Technical Approach

<key design + decisions>

## Research References

* [research topic](docs/research/<stack>-<topic>-<major>.md) — <one-line takeaway>

**填充规则**：当本 PRD 的技术方案引用了 `/research` skill 产出的研究记录时，在此列出。每条格式：`[主题](docs/research/<stack>-<topic>-<major>.md) — 一句话结论`。

- 仅引用 `/research` 产出的 `docs/research/*.md` 记录（权威信源、版本化、不可变）。
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

* PR1: <scaffolding + tests + minimal plumbing>
* PR2: <core behavior>
* PR3: <edge cases + docs + cleanup>

## Technical Notes

* <files inspected, constraints, links, references>
* <research notes summary if applicable>

## Traceability

- **Created by**: `/think`
- **Prototyped by**: minimal experiment (<YYYY-MM-DD>) — if a demo adjudicated a design option — <divergence> → <selected X / eliminated Y, because <evidence>>
- **Grilled by**: `/grill` (completed <YYYY-MM-DD>) — <summary: terms sharpened, assumptions resolved, ADRs created>
- **Sliced by**: `/story` (completed <YYYY-MM-DD>) — child issues listed under `Sliced into` below
- **Sliced into**:
  - #<issue-1> — [PRD-NNNN] <slice title> (AFK) — covers: R1, AC1 — Dev Complete
  - #<issue-2> — [PRD-NNNN] <slice title> (HITL, blocked by #<issue-1>) — covers: R2, AC2 — In Progress
  - #<issue-3> — [PRD-NNNN] <slice title> (AFK) — covers: R3, AC3
- **Implemented by**: implementation workflow (Issue reference)
- **Accepted by**: `/page-acceptance` (<YYYY-MM-DD>) — <pages/routes and evidence location>
- **Debugged by**: `/debug` (if bug fix touched this feature) — <bug summary + root cause>
- **Arch reviewed by**: separate architecture review (if performed) — <finding summary>
- **Reviewed by**: `/review` (PR reference)
- **New terms**: <domain terms found during review, for CONTEXT.md>
- **New decisions**: <decisions made during implementation, for ADR>

## Issue

#<issue-number>（父 Issue，如有）
```

## 字段说明

| 字段 | 说明 |
|------|------|
| Status | PRD 生命周期状态（Draft / Grilled / Sliced / In Progress / Dev Complete / Accepted / Done / Deprecated） |
| PRD | PRD 编号（四位零填充，如 PRD-0000） |
| Goal | 一句话描述为什么和做什么 |
| What I already know | 已知事实（来自用户和代码库） |
| Assumptions | 需要验证的临时假设 |
| Open Questions | 仅阻塞/偏好问题 |
| Domain Terms (draft) | 头脑风暴中新增的草稿术语（Term / Working Definition / Status）；由 `/think` Step 10b 追加，交 `/grill` 推进到 `CONTEXT.md`；可选章节 |
| Requirements | 功能需求列表，使用稳定 ID（`R1`、`R2`）|
| Acceptance Criteria | 可测试的验收标准，使用稳定 ID（`AC1`、`AC2`）|
| Definition of Done | 完成定义（团队质量标准） |
| Out of Scope | 明确不做的事情 |
| Technical Approach | 技术方案和关键决策 |
| Research References | 研究记录引用（仅 `/research` 产出的 `docs/research/*.md`，含一句话结论；临时搜索结果放 Technical Notes） |
| Feasible Approaches | 可行方法（2-3个选项）|
| Decision (ADR-lite) | 决策记录（轻量级ADR）|
| Implementation Plan | 实施计划（拆分成小PR）|
| Technical Notes | 技术笔记 |
| Traceability | 全链路追踪（各 skill 阶段自动填充）|
| Issue | 对应的 Issue 编号 |
| Sliced into | 子 Issues 列表，Traceability 的一环（由 /story 自动填写，格式：`#<number> — <title> (type) — covers: R#, AC# — status`；PRD 无独立 "Child Issues" 字段）|
