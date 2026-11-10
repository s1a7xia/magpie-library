---
name: debug
description: "Root cause analysis and systematic fix. Quick root cause location, then 6-phase systematic loop for bug fixes. Use when errors, crashes, regressions, test failures, anomalous behavior, or the user says 'used to work'. Trigger words: debug, 排查, 报错, 崩溃, 不工作, regression, 以前是好的, broken after update."
---

# Debug: Root Cause Analysis and Systematic Fix

🥷 Find root cause before fixing.

This skill restores intended behavior; it does not redesign the UI. Do not load `frontend-design` or add visual polish during debugging. If the requested outcome is a visual redesign rather than a defect fix, stop and treat it as a separate explicit design task.

Do not auto-trigger `research` from debugging. Diagnose from runtime evidence, project code and existing docs first; if external authoritative research is genuinely required, state that and wait for an explicit `/research` request.

> **Terminology note:** debug uses **Stage** (macro: Stage 0 context / Stage 1 quick-locate / Stage 2 systematic-fix) and **Phase** (micro: the 6-phase loop inside Stage 2) deliberately, to distinguish quick-locate from systematic-fix. Other skills use **Step**. This is an intentional divergence, not drift.

## Outcome Contract

- **Outcome**: Bug fixed with a regression guard when authorized, root cause documented, debug artifacts cleaned
- **Done when**: Bug no longer reproduces, the authorized regression test and reproduction check pass or their absence is recorded, instrumentation removed, root cause in commit/PR message when a commit is authorized
- **Evidence**: Reproduction loop passes; when tests are authorized, the regression test fails on old code and passes on new
- **Output**: Root cause, fix, confirmation, test location, regression guard

## Process Summary

**Stage 0 (Context Setup)**: Apply the [Skill Entry Protocol](../rules/entry-protocol.md) and its [Standards Gate](../rules/entry-protocol.md#standards-gate) for applicable coding rules and verification. When the fix changes RuoYi-Vue-Plus 6.x + React backend Java, PostgreSQL/SQL, React UI, API/types, permissions or field contracts, load `ruoyi6` before touching the code; do not wait for the Entry Protocol to infer it. It also locates domain docs; domain vocabulary helps form accurate hypotheses.

**Stage 1 (Quick Locate)**: Root cause analysis — form 1-2 hypotheses, validate, output one-sentence root cause. If quick validation fails (hypotheses refuted or none explains all symptoms), escalate to Stage 2.

**Stage 2 (Systematic Fix)**: 6-phase loop
- Phase 1: Build feedback loop — construct deterministic repro (the critical skill)
- Phase 2: Reproduce — run loop, confirm bug appears (or output a HITL repro guide when the loop can't run autonomously)
- Phase 3: Hypothesize — generate 3-5 ranked falsifiable predictions
- Phase 4: Instrument — add targeted logging with persistence + ordering for each prediction
- Phase 5: Fix + regression guard — write or update a test first when authorized and a correct seam exists; otherwise record the unverified regression gap
- Phase 6: Cleanup + retrospective — remove debug logs + `DEBUG/` artifacts, document proof

See [REFERENCE.md](REFERENCE.md) for detailed phases, optional modes (bisect, scope scan), and quality gates.

## Optional Modes

**Bisect mode**: Triggered by "used to work", "broke after update", or user recalls specific good commit/version

**Scope scan mode**: Triggered after root fix, before declaring done, or user says "check similar areas"

## Gotchas

| What happened | Rule |
|---|---|
| Fix client pane instead of local pane | Trace execution path before touching files |
| Say "try again" or "I'm confident" | Write hypothesis; run instrumentation to prove (anti-pattern #32 — fix without instrumentation) |
| Instrumentation only to stdout, lost after loop | Persist probes to `DEBUG/<session>-<n>.log` with sequence+timestamp so evidence survives and ordering is analysable (race bugs) |
| Can't reproduce autonomously, skip repro | Stop and output a HITL repro guide; wait for the user's report before hypothesizing |
| MCP not loading, switch tools instead of diagnose | Check server status, API key, config first |
| Compile passes but UI looks wrong | Move up Runtime Evidence Ladder, verify rendered surface |
| Fix one instance, ignore siblings | After fix, grep pattern and fix or report each instance (anti-pattern #21) |
| Fix expands beyond authorized behavior or data scope | Pause only the affected work and identify the additional decision; file count alone is not a permission gate |

## Output (Success)

```
Root cause:    [what broke, file:line]
Fix:           [what changed, file:line]
Confirmation:  [evidence fix works or test]
Test:          [pass/fail count, regression test location]
Regression:    [test file:line] or [none, reason]
Status:        resolved | resolved with caveats | blocked
```

**Regression guard:** When the project profile or current request authorizes test work, a recurrence fix is not complete until a regression test exists (fails on old, passes on new) in the project suite. Otherwise report the missing guard; do not claim verification.

**PRD Traceability:** If PRD exists, fill `Debugged by` in its `## Traceability`:
```markdown
- **Debugged by**: `/debug` (<YYYY-MM-DD>) — <one-line root cause + fix summary>
```

## 验收交接

按 [生命周期规则](../think/PRD-FORMAT.md#prd-生命周期状态)，修复改变已验收行为时，受影响的 `Accepted` / `Done` 切片退回 `Dev Complete`，记录原因和待复测路径；尚未编译通过则保持 `In Progress`。相关父 PRD 同步退回，其他切片不受影响。标明旧验收及 review 结论的失效范围，保留历史证据。

有页面可观察行为时，正常顺序是：`implement → 首次全范围 page-acceptance → review → debug（review 内） → 修复点 page-acceptance（仅行为变化时） → Done`。纯后端、SQL、内部逻辑、日志或配置批次记录 `Page acceptance: N/A`，直接进入 review，review 通过后可从 `Dev Complete` 写 `Done`。由首次页面验收触发时，修复后回到本次验收继续局部复测，不要求用户重新进入验收。由 review 触发时，修复完成后返回同一轮 review，继续检查剩余角度和范围；整轮 review 结束后，只有修复改变了页面可观察行为、交互、数据反馈、权限表现或视觉结果时，才提示用户发起一次 `/page-acceptance` 验证修复点及连带路径；纯内部修复保留原验收证据并说明覆盖边界。通过后恢复 `Accepted`，本轮 review 已覆盖最终代码即可 `Done`。其他情况下等待用户主动发起页面验收。不自行启动新的页面阶段或完整 review。

`debug` 不负责打包，也不负责重建开发环境。前端修复靠刷新；Java/配置修复由环境所有者重载一次已运行的开发进程（本地直接跑，Docker 留给部署）；同一轮 review 的多个行为修复合并后只重载和复测一次。

## Next step

If this debug was entered from `page-acceptance` or `review`, return to that calling flow and follow its re-test/review handoff. For a standalone fix:

- If the fix changes page-observable behavior, interaction, displayed data, permission outcome or visual result, recommend the user-initiated `/page-acceptance` first; after it passes, recommend `/review`.
- If the fix changes only backend internals, SQL, logs, configuration or other non-page-observable behavior, record `Page acceptance: N/A — <reason>` and recommend the user-initiated `/review` directly.
- A simple fix with clear compile and regression evidence may stop without review when the user does not ask for it. Never start page acceptance or review automatically.

## Output (Handoff — after 3 falsified hypotheses in Stage 2)

Emitted from Stage 2 Phase 4 when 3 hypotheses have been falsified without identifying the cause (see REFERENCE.md §Phase 4).

```
Symptom: [original error]

Tested hypotheses:
1. [h1] → [test] → [result]
2. [h2] → [test] → [result]
3. [h3] → [test] → [result]

Evidence: [logs, stack traces, repro steps, environment]
Excluded: [ruled out root causes]
Unknown:  [what remains unclear]

Suggested next: [next direction, tools needed, context required]
Status: blocked
```

Share this handoff with a fresh agent session, or provide additional info and re-run /debug.
