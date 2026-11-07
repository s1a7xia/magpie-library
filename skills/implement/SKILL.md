---
name: implement
description: "Use only when the user explicitly invokes implement for a PRD or set of issues. It orchestrates per-slice implementation in one batch: load the framework profile and frontend-design, implement each slice, compile, commit and push each slice, then stop for the user's page testing. Do not trigger from words like 实现/开发/开始写代码; the main agent handles those directly."
---

# Implement: Workflow Orchestration

当前资源库检查规则优先：默认只检查本次改动涉及的前后端能否编译。前后端均有改动时分别编译；仅改一端时只编译该端；纯文档或不影响编译的配置改动只核对差异。复用项目已有编译/构建命令，跳过测试，不独立运行 lint、类型检查或自动化测试；已有构建命令内置的编译类型检查可保留。**页面测试不属于本流程**：切片自检只做编译与 diff 核对，整批完成后由用户主动发起 `page-acceptance`。测试编写、独立类型检查或全量测试步骤只有用户明确要求时才执行。

🥷 Implement from PRD or issues — orchestrate authorized implementation, checks, review, and commits.

Sequences one batch of pre-agreed vertical slices: load the framework profile and design standards, implement each slice, compile the affected side, commit and push that slice, then stop for the user's page testing. Page acceptance and full review are separate, user-initiated stages.

## Outcome Contract

- **Outcome**: All items from the PRD's acceptance criteria or child issues are implemented, compile-checked, committed, and pushed. Page testing and review remain separate user-initiated stages.
- **Done when**: Each slice is complete against its acceptance criteria, the affected side compiles, the slice is committed and pushed, and the PRD records `Dev Complete`. Unverified or blocked slices are named rather than marked complete.
- **Evidence**: Compile commands, working directories, exit status and results; diff review; commit hashes and push state; PRD and project-state updates.
- **Output**: Summary of implemented slices, compile evidence, commits and pushes, unverified items, and the explicit handoff to user-initiated page testing.

## Process Summary

**Step 0 — Quick assessment.** If the work is trivial (single file, one obvious change), recommend direct implementation and stop — this skill is unnecessary overhead.

**Step 1 — Entry Protocol.** Apply the [Skill Entry Protocol](../rules/entry-protocol.md). Read project config (`docs/agents/`), domain docs (CONTEXT.md, ADRs, research INDEX), and the input work items (PRD or Issues from `/story`). Check upstream quality: if PRD Traceability shows `Created by: /story (minimal PRD)`, note that requirements may not be decision-complete; if `Grilled by` is empty, note the plan is unvalidated.

**Step 2 — Work Inventory and profile loading.** List all items to implement: Issues from `/story` are the seams (each carries its `blocked-by` relations). Sort by dependency order. Update PRD Status from `Sliced` to `In Progress`. Then load, once per batch (not per slice): [ruoyi-plus-dev](../ruoyi-plus-dev/SKILL.md) — this project defaults to RuoYi-Vue-Plus工艺; if the user says it is not a RuoYi project, skip it. Load [frontend-design](../frontend-design/SKILL.md) when the batch touches frontend view files (`.vue`, `.tsx`, `.css`, `.scss`, components, layout, styles); skip it for pure backend or data-layer-only work.
- If Issues from `/story` exist — each issue is a seam
- If only a PRD — extract Acceptance Criteria as work items
- Sort by dependency order (blocked-by relationships from `/story`)
- Update PRD Status from `Sliced` to `In Progress` in the PRD's status line

**Step 3 — Implement each slice.** For each work item in dependency order:

1. **Read the slice's acceptance criteria** — from the PRD or the issue it came from; confirm they are clear before writing code.
2. **Implement directly** — write the smallest change that satisfies them; apply [engineering principles](../rules/engineering-principles.md) design-time, the loaded framework profile, and `frontend-design` for view changes. Write tests only when the current request explicitly asks for test work.
3. **Self-check** — compile the affected frontend/backend. For UI slices this is a compile check only; do not open a browser. Record what was checked.
4. **Commit and push this slice** — commit with `[PRD-NNNN] <slice name> — <summary>` and push to the existing upstream on the same branch. Never create a feature branch. If a check fails, fix it or mark the slice unverified before moving on.
5. **Sync documents** — update the slice status in the PRD `Sliced into` list and the affected parts of `project-state.md` / `verification.md` in the same commit.

Mark the slice `Dev Complete`, never `Done` — `Done` requires page testing.

**Step 4 — Batch close-out.** After every slice is implemented and pushed, compile the affected sides once more and list: slices pushed with their commit hashes, slices marked `Dev Complete`, and anything blocked or unverified. Do not run page acceptance, do not run full review, do not mark the PRD `Done`.

**Step 5 — Hand off to the user's testing stage.** Tell the user the batch is ready for page testing and name the pages/routes affected. Page acceptance is user-initiated: wait for the explicit request before touching a browser. After page testing passes, the user decides whether to run `/review`.

**Step 6 — Output.** Produce the batch summary: slices implemented, commits and pushes actually made, compile results, slices marked unverified, and the explicit next step (page testing by the user).

See [REFERENCE.md](REFERENCE.md) for detailed step instructions, implementation guidelines, and recovery procedures.

## Gotchas

| What happened | Rule |
|---|---|
| A slice started before its acceptance criteria were clear | Step 3.1: read and confirm the acceptance criteria first |
| Page acceptance was run inside implement | Step 3.3 / Step 4: slice self-check is compile + diff only; page testing is a separate user-initiated stage |
| Slices were batched into one commit | Step 3.4: one commit and push per slice, message `[PRD-NNNN] <slice name> — <summary>` |
| A feature branch was created | Step 3.4: one branch per requirement is not allowed here — commit on the current branch only |
| The framework profile or design standards were skipped | Step 2: load `ruoyi-plus-dev` (default for this library) and `frontend-design` (when views change) once per batch |
| Work items had hidden dependencies | Step 2: read `blocked-by` from `/story`; implement in dependency order and skip blocked slices |
| PRD was marked Done after implementation | Step 3 / Step 4: mark `Dev Complete` only; `Done` requires page testing to pass |
| Unattended run tried to open a browser | Step 3.3: no browser, no login state, no captcha in unattended mode — mark the slice unverified and continue |
| User expected /review to run automatically | Step 5: review is explicitly user-invoked and runs after page testing |

## Output

```
Implement batch complete — PRD-NNNN <title>

**Slices:**
* #<n> <slice name> — Dev Complete — commit <hash> — pushed
* #<n> <slice name> — Dev Complete — commit <hash> — pushed
* #<n> <slice name> — unverified (<reason>) — commit <hash>

**Compile:** <side> pass | fail (<reason>)
**Page testing:** not run — user-initiated stage
**PRD status:** In Progress (slice statuses Dev Complete)

**Next:** Start page testing for <routes/pages>; after it passes, run /review if wanted.
```
