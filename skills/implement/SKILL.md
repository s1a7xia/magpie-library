---
name: implement
description: "Orchestrate a batch of already-approved slices from /story: load the RuoYi 6.x React profile and its frontend baseline, implement, compile, commit/push each slice, then stop for user page testing. Use only on explicit /implement; do not trigger from ordinary 实现/开发."
---

# Implement: Workflow Orchestration

检查范围以全局协作指令和项目配置为准：默认只编译受影响的一侧，跳过测试；页面验收不在本流程。授权、证据和失败处理见 [Skill Entry Protocol](../rules/entry-protocol.md)。

🥷 Implement from PRD or issues — orchestrate authorized implementation, checks, commits and pushes.

Sequences one batch of pre-agreed vertical slices: load the framework profile and design standards, implement each slice, compile the affected side, commit and push that slice, then stop for the user's page testing. Page acceptance and full review are separate, user-initiated stages.

## Outcome Contract

- **Outcome**: All approved slices in the PRD's `Sliced into` list are implemented, compile-checked, committed, and pushed, with every acceptance criterion covered. Page testing and review remain separate user-initiated stages.
- **Done when**: Each slice is complete against its acceptance criteria, the affected side compiles, the slice is committed and pushed, every PRD acceptance criterion is covered by a `Dev Complete` slice, and the PRD records `Dev Complete`. Unverified, blocked, or uncovered slices are named rather than marked complete.
- **Evidence**: Compile commands, working directories, exit status and results; diff review; commit hashes and push state; PRD and project-state updates.
- **Output**: Summary of implemented slices, compile evidence, commits and pushes, unverified items, and the explicit handoff to user-initiated page testing.

## Process Summary

**Step 0 — Quick assessment.** If the work is trivial (single file, one obvious change), recommend direct implementation and stop — this skill is unnecessary overhead.

**Step 1 — Entry Protocol.** Apply the [Skill Entry Protocol](../rules/entry-protocol.md). Require a consistent baseline (`Status: Sliced`, `In Progress` or `Dev Complete`) with no open questions/TODOs and a filled `Grilled by`; otherwise return to `think` → `grill` or `/story`.

**Step 2 — Work Inventory.** List the approved slices and sort them by `blocked-by`. Verify every PRD acceptance criterion is assigned through `Covers`; an unassigned criterion stops the batch and returns to `story`. Set the PRD to `In Progress`. Resolve the technical profile once per batch per the [entry protocol](../rules/entry-protocol.md); default to [ruoyi6](../ruoyi6/SKILL.md), including its frontend baseline for page or style changes. Layer [frontend-design](../frontend-design/SKILL.md) on top only for an explicit beautification, deep-design or full-redesign request.
- If Issues from `/story` exist — each issue is a seam
- If only a PRD exists — stop and run `/story` first; do not invent slices inside `implement`
- Sort by dependency order (blocked-by relationships from `/story`)
- Update PRD Status from `Sliced` to `In Progress` in the PRD's status line

**Step 3 — Implement each slice.** In dependency order:

1. Read the slice's acceptance criteria and mark it `In Progress`.
2. Make the smallest change that satisfies them, applying the engineering principles and loaded profile. Write tests only when explicitly requested.
3. Compile only the affected side, then commit and push the slice on the current branch.
4. In the same commit, mark the slice `Dev Complete`; do not update `project-state.md` or `verification.md` per slice.

Mark the slice `Dev Complete`, never `Done` — `Done` requires page testing.

**Blocked slice.** Leave it `In Progress`, report why, and continue with unblocked slices.

**Step 4 — Batch close-out.** Compile the affected sides once more, run the coverage gate, then update `project-state.md` and `verification.md` once. A missing slice returns to `story`; a code gap stays inside its existing slice. Do not run page acceptance or full review, and do not mark the PRD `Done`.

**Step 5 — Hand off to the user's testing stage.** Tell the user the batch is ready for page testing and name the pages/routes affected. Page acceptance is user-initiated: wait for the explicit request before touching a browser. After page testing passes, the user decides whether to run `/review`.

**Step 6 — Output.** Report slices, commits/pushes, compile evidence, unverified items and the page-testing handoff.

See [REFERENCE.md](REFERENCE.md) for detailed step instructions, implementation guidelines, and recovery procedures.

## Gotchas

| What happened | Rule |
|---|---|
| A slice started before its acceptance criteria were clear | Step 3.1: read and confirm the acceptance criteria first |
| Page acceptance was run inside implement | Step 3 / Step 4: slice self-check is compile + diff only; page testing is a separate user-initiated stage |
| Slices were batched into one commit | Step 3: one commit and push per slice, message `[PRD-NNNN] <slice name> — <summary>` |
| A feature branch was created | Step 3: commit on the current branch only |
| The framework profile or frontend baseline was skipped | Step 2: resolve the project profile first (global `ruoyi6` only when none is configured); use its frontend baseline once per batch. Add `frontend-design` on top only for an explicit beautification or deep-design request |
| Work items had hidden dependencies | Step 2: read `blocked-by` from `/story`; implement in dependency order and skip blocked slices |
| A slice list missed a PRD acceptance criterion | Step 2 / Step 4: stop before coding or close-out; return to `story` instead of adding scope silently |
| PRD was marked Done after implementation | Step 3 / Step 4: mark `Dev Complete` only; `Done` requires page testing to pass |
| Unattended run tried to open a browser | Step 3: no browser, no login state, no captcha in unattended mode — mark the slice unverified and continue |
| The PRD slice still looked unstarted while code was in flight | Step 3: set the PRD slice to `— In Progress` before coding |
| A blocked slice was marked complete | Blocked slice rule: leave the PRD slice `In Progress` and report the blocker |
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
