---
name: implement
description: "Orchestrate a batch of already-approved slices from /story: load the RuoYi 6.x React profile and its frontend baseline, implement, compile, commit/push each slice, then hand off to user-initiated page testing when behavior is page-observable or directly to review when it is not. Use only on explicit /implement; do not trigger from ordinary 实现/开发."
---

# Implement: Workflow Orchestration

检查范围以全局协作指令和项目配置为准：默认只编译受影响的一侧，跳过测试；页面验收不在本流程。授权、证据和失败处理见 [Skill Entry Protocol](../rules/entry-protocol.md)。

🥷 Implement from PRD or issues — orchestrate authorized implementation, checks, commits and pushes.

Sequences one batch of pre-agreed vertical slices: load the framework profile and design standards, implement each slice, compile the affected side, commit and push that slice, then stop for the correct user-initiated next gate. Page acceptance applies to page-observable behavior; full review remains a separate user-initiated stage.

## Outcome Contract

- **Outcome**: All approved slices in the PRD's `Sliced into` list are implemented, compile-checked, committed, and pushed, with every acceptance criterion covered. The first full-scope page acceptance and the later full review are separate user-initiated stages. A review repair pass gets a narrow repair-scope acceptance only when the repair is page-observable.
- **Done when**: Each slice is complete against its acceptance criteria, the affected side compiles, the slice is committed and pushed, every PRD acceptance criterion is covered by a `Dev Complete` slice, and the PRD records `Dev Complete`. Unverified, blocked, or uncovered slices are named rather than marked complete.
- **Evidence**: Compile commands, working directories, exit status and results; diff review; commit hashes and push state; PRD and project-state updates; any novel-scenario research record or cited verdict.
- **Output**: Summary of implemented slices, compile evidence, commits and pushes, unverified items, and the explicit handoff to user-initiated page testing.

## Process Summary

**Step 0 — Route check.** This skill handles approved slices only. Direct low-risk work is handled by the main agent under the global Direct path and never enters `implement`. If no approved, sliced baseline exists, stop and report that the user must complete `/story`; if the baseline is unresolved, stop and report the upstream gap. Do not dismiss an explicit `/implement` invocation merely because the requested slice looks small.

**Step 1 — Entry Protocol.** Apply the [Skill Entry Protocol](../rules/entry-protocol.md). Require a frozen baseline (`Status: Sliced`, `In Progress` or `Dev Complete`) with no unresolved PRD-level questions, no empty `Grilled by`, and no `[TEMPORARY]` or `TODO(prd-NNNN)` markers. A pre-existing implementation `TODO(待确认)` does not block the slice when the behavior is fully implemented and the TODO only records a non-blocking confirmation. If the baseline itself is unresolved, stop and report that the user must complete the upstream work; do not invoke `grill` from this stage.

**Step 2 — Work Inventory.** Record the starting HEAD as the batch base, then list the approved slices and sort them by `blocked-by`. Verify every PRD acceptance criterion is assigned through `Covers`; an unassigned criterion stops the batch and reports that `/story` must assign it. Set the PRD to `In Progress`. Resolve the technical profile once per batch per the [entry protocol](../rules/entry-protocol.md); default to [ruoyi6](../ruoyi6/SKILL.md), including its frontend baseline for page or style changes. In a RuoYi project, load `ruoyi6` for every slice that changes backend Java, PostgreSQL/SQL, React UI, API/types, permissions or field contracts, not only for page work. Layer [frontend-design](../frontend-design/SKILL.md) on top only for an explicit beautification, deep-design or full-redesign request.
- If Issues from `/story` exist — each issue is a seam
- If only a PRD exists — stop and report that `/story` must run first; do not invent slices inside `implement`
- Sort by dependency order (blocked-by relationships from `/story`)
- Update PRD Status from `Sliced` to `In Progress` in the PRD's status line

**Step 2A — Novel-business research gate.** Before coding a slice, scan the design, current project implementations, `ruoyi6` capability map/references, and `docs/research/INDEX.md`. Trigger `research` automatically only when the business baseline is settled, the gap is technical implementation uncertainty, and all four local sources miss.

- Ask one bounded implementation question; use live authoritative sources, starting with `magpie-web-search` and then `context7` when needed.
- Reuse an existing research record when it covers the question; persist a new reusable verdict only on a miss.
- Return the verdict to the current slice and continue. Do not auto-enter `think` or `grill`.
- If the missing input is a newly discovered, non-blocking business rule, state semantic, permission boundary or acceptance criterion, do not stop the slice and do not route to `grill`: implement the safest/recommended default end-to-end and record a standard `TODO(待确认)` with what remains to confirm, the current behavior, whether later adjustment is expected and the confirmation owner. If the uncertainty is already a PRD-level unresolved decision, use Step 1 instead. Stop only when the implementation choice cannot use a safe default because it involves an irreversible data change, unresolved permission scope or security risk; report that the user must handle the upstream decision.
- If the evidence invalidates the frozen baseline, stop the affected slice and report that the user must decide on upstream correction (`think`/`grill`); do not invoke or return to those skills automatically.
- Do not trigger for ordinary CRUD, framework-provided capabilities, generic version confirmation, debugging, or a problem answerable by reading the project.

**Step 3 — Implement each slice.** In dependency order:

1. Read the slice's acceptance criteria and mark it `In Progress`.
2. Make the smallest change that satisfies them, applying the engineering principles and loaded profile. If a non-blocking business detail is newly discovered, implement the safest/recommended default across API, UI, data and feedback, then record a standard `TODO(待确认)` with the current behavior, whether later adjustment is expected and the confirmation owner. A TODO never substitutes for required behavior.
3. Compile only the affected side, then commit and push the slice on the current branch.
4. In the same commit, mark the slice `Dev Complete`; do not update `project-state.md` or `verification.md` per slice.

Mark the slice `Dev Complete`, never `Done` inside `implement`. Page-observable work needs page acceptance before review can close it; a non-page-observable batch can close through review with `Page acceptance: N/A`.

**Blocked slice.** Leave it `In Progress`, report why, and continue with unblocked slices.

**Step 4 — Batch close-out.** Reuse the latest successful compile evidence when it covers the final affected code, dependencies and build configuration; recompile only affected inputs changed since that check. Run the coverage gate, then update `project-state.md` and `verification.md` once. A missing slice is reported for `/story`; a code gap stays inside its existing slice. When the batch closes, write the consolidated `TODO(待确认)` summary (remaining confirmation, current default, whether later adjustment is expected and the owner) in both `project-state.md` and the PRD. Do not run page acceptance or full review, and do not mark the PRD `Done`.

**Step 5 — Hand off to the correct next gate.** Determine whether this batch has a page-observable impact: changed rendering, interaction, displayed data, permission outcome or visual result.

- If yes, name the affected pages/routes and hand off to the user-initiated first full-scope `/page-acceptance`. After it passes, stop and recommend `/review`; never start either stage automatically.
- If no, record `Page acceptance: N/A — <reason>` in the batch evidence and `project-state.md`, then recommend the user-initiated `/review` directly. Backend-only behavior, SQL, internal logic, logs and configuration still need their affected-side compile and review evidence; they do not need a browser pass merely to satisfy the workflow.

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
| A slice list missed a PRD acceptance criterion | Step 2 / Step 4: stop before coding or close-out; report that `/story` must assign it instead of adding scope silently |
| PRD was marked Done after implementation | Step 3 / Step 4: mark `Dev Complete` only; UI work needs page acceptance, while a non-UI batch closes only through review with `Page acceptance: N/A` |
| Unattended run tried to open a browser | Step 3: no browser, no login state, no captcha in unattended mode — mark the slice unverified and continue |
| The PRD slice still looked unstarted while code was in flight | Step 3: set the PRD slice to `— In Progress` before coding |
| A blocked slice was marked complete | Blocked slice rule: leave the PRD slice `In Progress` and report the blocker |
| User expected /review to run automatically | Step 5: hand off only; review is explicitly user-invoked afterwards |
| A backend-only batch was sent to page acceptance | Step 5: page acceptance is required for page-observable behavior; record `N/A` for non-UI changes and hand off to review |
| Research was launched for an ordinary feature | Step 2A: research only a genuinely novel business scenario that project code, `ruoyi6` and existing research cannot answer |
| Research was used to invent a business rule | Step 2A: implement the safest/recommended default end-to-end and record `TODO(待确认)`; do not route to `grill` |
| A business ambiguity stopped a whole slice | Step 2A: only irreversible data, permission-expansion or security choices with no safe default stop the affected action/slice; otherwise keep the feature complete and record the TODO |
| A TODO was used as a substitute for required work | Step 2A / Step 3: TODO records a non-blocking confirmation only; missing API, page, data, validation or feedback leaves the slice blocked |
| Research contradicted the frozen baseline | Step 2A: stop the affected slice and report that the user must decide on correction; do not auto-enter `think`/`grill` |

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

**Next (user-initiated):** <first full-scope `/page-acceptance` for <routes/pages>, then `/review` | `/review` with `Page acceptance: N/A — <reason>`>
```
