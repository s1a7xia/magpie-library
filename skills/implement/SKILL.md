---
name: implement
description: "Orchestrate a batch of already-approved slices from /story: load the RuoYi 6.1 Vue profile and frontend-design, implement, compile, commit/push each slice, then stop for user page testing. Use only on explicit /implement; do not trigger from ordinary 实现/开发."
---

# Implement: Workflow Orchestration

检查范围以全局协作指令和项目配置为准：默认只编译受影响的一侧，跳过测试；页面验收不在本流程。授权、证据和失败处理见 [Skill Entry Protocol](../rules/entry-protocol.md)。

🥷 Implement from PRD or issues — orchestrate authorized implementation, checks, review, and commits.

Sequences one batch of pre-agreed vertical slices: load the framework profile and design standards, implement each slice, compile the affected side, commit and push that slice, then stop for the user's page testing. Page acceptance and full review are separate, user-initiated stages.

## Outcome Contract

- **Outcome**: All approved slices in the PRD's `Sliced into` list are implemented, compile-checked, committed, and pushed, with every acceptance criterion covered. Page testing and review remain separate user-initiated stages.
- **Done when**: Each slice is complete against its acceptance criteria, the affected side compiles, the slice is committed and pushed, every PRD acceptance criterion is covered by a `Dev Complete` slice, and the PRD records `Dev Complete`. Unverified, blocked, or uncovered slices are named rather than marked complete.
- **Evidence**: Compile commands, working directories, exit status and results; diff review; commit hashes and push state; PRD and project-state updates.
- **Output**: Summary of implemented slices, compile evidence, commits and pushes, unverified items, and the explicit handoff to user-initiated page testing.

## Process Summary

**Step 0 — Quick assessment.** If the work is trivial (single file, one obvious change), recommend direct implementation and stop — this skill is unnecessary overhead.

**Step 1 — Entry Protocol.** Apply the [Skill Entry Protocol](../rules/entry-protocol.md). Read project config (`docs/agents/`), domain docs (CONTEXT.md, ADRs, research INDEX), and the input work items (PRD or Issues from `/story`). Require a frozen, consistent baseline: `Status: Sliced`, `In Progress`, or `Dev Complete`, no open questions/TODOs, and a filled `Grilled by`. If not, stop before coding and return to `think` → `grill` or `/story` as appropriate.

**Step 2 — Work Inventory and profile loading.** List the approved slices and sort them by `blocked-by`. Before writing code, verify every PRD acceptance criterion is assigned through a slice `Covers` field; an unassigned criterion stops the batch and returns to `story`. Update PRD Status from `Sliced` to `In Progress`; set the project dashboard's `Development` row to `In Progress` when it exists. Resolve and load the technical profile once per batch per [entry protocol](../rules/entry-protocol.md); the default is [ruoyi-6-vue](../ruoyi-6-vue/SKILL.md). Load [frontend-design](../frontend-design/SKILL.md) when the batch changes frontend view files.
- If Issues from `/story` exist — each issue is a seam
- If only a PRD exists — stop and run `/story` first; do not invent slices inside `implement`
- Sort by dependency order (blocked-by relationships from `/story`)
- Update PRD Status from `Sliced` to `In Progress` in the PRD's status line

**Step 3 — Implement each slice.** For each work item in dependency order:

1. **Read the slice's acceptance criteria** — from the PRD or the issue it came from; confirm they are clear before writing code.
2. **Implement directly** — write the smallest change that satisfies them; apply [engineering principles](../rules/engineering-principles.md) design-time, the loaded framework profile, and `frontend-design` for view changes. Write tests only when the current request explicitly asks for test work.
3. **Self-check** — compile the affected frontend/backend. For UI slices this is a compile check only; do not open a browser. Record what was checked.
4. **Commit and push this slice** — commit with `[PRD-NNNN] <slice name> — <summary>` and push to the existing upstream on the same branch. Never create a feature branch. If a check fails, fix it or mark the slice unverified before moving on.
5. **Sync slice status** — update the slice status in the PRD `Sliced into` list in the same commit. Do not rewrite `project-state.md` or append a separate `verification.md` entry for every slice.

Mark the slice `Dev Complete`, never `Done` — `Done` requires page testing.

**Step 4 — Batch close-out.** After every slice is implemented and pushed, compile the affected sides once more. Run the **coverage gate**: every PRD requirement and acceptance criterion must map through `Covers` to a slice that is `Dev Complete`; an uncovered criterion keeps the batch `In Progress`. A missing slice returns to `story`; a code gap is fixed inside its existing slice. Then update `project-state.md` once with `Development` set to `Passed` (or `In Progress` with gaps) and `verification.md` once with the actual per-slice compile commands/results and any gaps. List slices with their commit hashes, slices marked `Dev Complete`, and anything blocked or unverified. Do not run page acceptance, do not run full review, do not mark the PRD `Done`.

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
| The framework profile or design standards were skipped | Step 2: resolve the project profile first (global `ruoyi-6-vue` only when none is configured) and load `frontend-design` when views change, once per batch |
| Work items had hidden dependencies | Step 2: read `blocked-by` from `/story`; implement in dependency order and skip blocked slices |
| A slice list missed a PRD acceptance criterion | Step 2 / Step 4: stop before coding or close-out; return to `story` instead of adding scope silently |
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
**Coverage:** <n>/<n> PRD acceptance criteria assigned; <gaps or none>
**Page testing:** not run — user-initiated stage
**PRD status:** Dev Complete | In Progress (gaps: <none | IDs>)

**Next:** Start page testing for <routes/pages>; after it passes, run /review if wanted.
```
