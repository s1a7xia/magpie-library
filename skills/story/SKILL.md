---
name: story
description: "把已确认方案拆成可独立交付的纵向切片。默认用现有需求文档或对话承接，仅在项目已有 Issue tracker 且当前请求授权时才发布 Issue。用于任务拆解、依赖排序和迭代切片，不用于需求澄清或普通实现。"
---

# Story: Break a Plan Into Deliverable Slices

🥷 Vertical slices, each slice is demonstrable end-to-end.

Break a plan into independently actionable vertical slices (tracer bullets). Accepts an existing PRD or a direct feature description. Publishing the slices as Issues is optional.

## Outcome Contract

- **Outcome**: Ordered slices, each independently executable and demonstrable, covering the current plan
- **Done when**: Dependencies and acceptance criteria are clear and the user approves the breakdown
- **Evidence**: The approved slice list in the conversation or an existing project record; Issues only when an authorized tracker exists
- **Output**: Slice list, dependencies, and the chosen record location

## Prerequisites

- **Input**: an existing PRD at `docs/prd/PRD-NNNN-<title>.md`, or a direct feature description from the user
- Apply the [Skill Entry Protocol](../rules/entry-protocol.md) selectively to locate relevant requirements and decisions
- If, and only if, the project has an existing tracker and the current task will publish Issues, read its convention and label mapping
- Missing tracker config is normal: keep the approved slices in the existing project docs or conversation; do not create tracker config or run setup

## Process Summary

**Step 0**: Read the relevant project context. Tracker configuration is needed only when the current task will actually publish Issues.

**Step 1**: Determine input source — locate existing PRD, or capture feature description from user

**Step 2**: Extract requirements — from PRD or from user description + codebase exploration

**Step 3**: Use the source of truth that already exists. Reuse an existing PRD or project specification when present; do not create a PRD solely to hold a slice list.

**Step 4**: Explore codebase (optional) — understand current state, use domain glossary, respect ADRs

**Step 5**: Draft vertical slices — each is a thin vertical slice through the layers it actually changes; tests are included only when the current request requires them

**Step 6**: Present to user — show title, type (HITL/AFK), blocked-by, user stories; self-check granularity/dependencies first, then ask one approval question

**Step 7**: Unless an existing tracker is explicitly in scope, keep the approved slices in the source document or conversation. If publishing is authorized, create Issues in dependency order using the project's convention.

**Step 8**: If a PRD or project record is in use, record the approved slices and dependencies there. Do not force a PRD lifecycle label when the project does not use one.

**Step 9**: If an existing parent Issue is in scope and tracker writes are authorized, synchronize it. Otherwise skip without warning.

**Slice Types:**
- **HITL**: Human-in-the-loop — requires human judgment (architecture, design, UX). Agent pauses at decision points for input.
- **AFK**: Away-from-keyboard — implementable end-to-end without human interaction.

See [STORY-FORMAT.md](STORY-FORMAT.md) for the issue title/body template (single source) and [REFERENCE.md](REFERENCE.md) for input handling, slicing detail, and examples.

## Gotchas

| What happened | Rule |
|---|---|
| Horizontal slicing (all schema, then all API) | Use thin vertical slices through the layers the behavior needs |
| Slices too thick | Prefer many thin slices over few thick ones |
| Dependencies wrong | Order the slices blockers first, whether or not Issues are published |
| PRD or parent Issue not updated | Update only a record that already exists and is in the authorized scope |
| Input too vague for slicing | Return to requirement clarification; do not invent requirements or run a full brainstorming session here |
| Forced a wide refactor (rename shared column, retype shared symbol) into tracer bullets | Vertical Slice Rules: slice it expand → migrate batches → contract; a slice that can't land green alone isn't a slice |
| Same topic got two PRDs (e.g. PRD-0001 + PRD-0002) | Only when the user explicitly requests a new PRD: run the PRD Conflict Check in think/REFERENCE.md before creating |

## Vertical Slice Rules

- Each slice traces one narrow but **complete** path through every layer
- Completed slice is demonstrable or verifiable on its own
- Prefer many thin slices over few thick ones
- Avoid file paths or code snippets — they become stale

**Wide refactors are the exception.** A wide refactor is one mechanical change (rename a shared column, retype a shared symbol) whose blast radius spans the whole codebase — no vertical slice can land green on its own. Don't force it into tracer bullets; slice it as **expand → migrate → contract**: (1) one ticket adds the new form beside the old so nothing breaks; (2) migration tickets move call sites in batches sized by blast radius (per package/directory), each batch keeping the suite green because the old form still exists, each blocked by the expand; (3) one contract ticket deletes the old form, blocked by every migrate batch. See [REFERENCE.md](REFERENCE.md) for the sequence diagram.

## Output

```
Story complete.

Approved slices:
* 1 — <title> (AFK)
* 2 — <title> (HITL, blocked by 1)

Record:
- existing doc / PRD path / conversation

Next: implement the agreed slices when the current request authorizes implementation.
```

## Example

```
Requirement record: User subscription (optional PRD-0003-subscription)

Proposed:
1. Create subscription data model (AFK) — schema + API
2. Payment flow integration (AFK, blocked by #1) — gateway + webhooks
3. Management UI (HITL, blocked by #2) — design review + components

User: granularity looks right, proceed → [keep the approved slices in the plan record; publish Issues only if already authorized]
```
