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
- **Done when**: The in-scope code fix is complete, final diff is checked, task-owned instrumentation is removed, and actual verification or its absence is recorded; runtime recovery is claimed only with observed evidence
- **Evidence**: Exact logs/code explaining the mechanism; runtime reproduction and regression results only when authorized and actually observed
- **Output**: Root cause, fix, confirmation, test location, regression guard

## Process Summary

**Stage 0 (Context Setup)**: Apply the [Skill Entry Protocol](../rules/entry-protocol.md) and its [Standards Gate](../rules/entry-protocol.md#standards-gate) for applicable coding rules and verification. Resolve the selected profile through that protocol, honoring explicit `none`; load `ruoyi6` only for an applicable RuoYi scope. It also locates domain docs; domain vocabulary helps form accurate hypotheses.

**Stage 1 (Quick Locate)**: Root cause analysis — form 1-2 hypotheses, validate, output one-sentence root cause. If quick validation fails (hypotheses refuted or none explains all symptoms), escalate to Stage 2.

**Stage 2 (Systematic Fix)**: 6-phase loop
- Phase 1: Build feedback loop — select the smallest useful signal; run only authorized reproduction
- Phase 2: Reproduce — confirm symptoms from available evidence; distinguish static inference, user reports and agent runtime observations
- Phase 3: Hypothesize — rank a few falsifiable predictions proportional to the uncertainty
- Phase 4: Instrument — add minimal probes only if necessary and authorized; protect secrets
- Phase 5: Fix + regression guard — write/update a test only with explicit test-authoring authorization and a correct seam; otherwise record the unverified regression gap
- Phase 6: Cleanup + retrospective — remove only task-owned probes/artifacts, document actual evidence

See [REFERENCE.md](REFERENCE.md) for detailed phases, optional modes (bisect, scope scan), and quality gates.

## Optional Modes

**Bisect mode**: Consider for a known regression interval; actual bisect/check execution requires authorization and an isolated worktree (see reference).

**Scope scan mode**: Read related callers after the root fix; broaden only for the requested same-class scope, report unrelated findings without fixing.

## Gotchas

| What happened | Rule |
|---|---|
| Fix client pane instead of local pane | Trace execution path before touching files |
| Say "try again" or "I'm confident" | Tie the hypothesis to exact logs/code; run probes only when necessary and authorized |
| Instrumentation only to stdout, lost after loop | When authorized probes need persistence, use a task-owned redacted log with sequence/time; do not require instrumentation for already-sufficient evidence |
| Can't reproduce autonomously, skip repro | Continue static diagnosis where possible; ask only for evidence that materially blocks the fix, label runtime unverified |
| MCP not loading, switch tools instead of diagnose | Check server status, API key, config first |
| Compile passes but UI looks wrong | Report static/compile limits; suggest manual page acceptance, never auto-launch it |
| Fix one instance, ignore siblings | Inspect directly affected callers; report unrelated instances, do not expand repair scope |
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

**Regression guard:** Only an explicit request to write/modify tests authorizes a new regression test. A run-tests request permits existing tests only; profile suggestions do not grant permission. Otherwise report the missing guard; do not claim verification.

**PRD Traceability:** If PRD exists, fill `Debugged by` in its `## Traceability`:
```markdown
- **Debugged by**: `/debug` (<YYYY-MM-DD>) — <one-line root cause + fix summary>
```

## 验收交接

按 [生命周期规则](../think/PRD-FORMAT.md#prd-生命周期状态)，修复改变已验收行为时，受影响的 `Accepted` / `Done` 切片退回 `Dev Complete`，记录原因和待复测路径；已知代码错误或行为未实现则保持 `In Progress`，未获授权运行构建另记未验证。相关父 PRD 同步退回，其他切片不受影响。标明旧验收及 review 结论的失效范围，保留历史证据。

正常顺序：implement → 用户手动 review（内部 debug 修复后继续本轮审查）→ 用户手动完整范围 page-acceptance → Done。非 UI 范围页面验收记 N/A。debug 返回调用它的当前阶段，不自动启动新 review 或页面验收；验收中涉及权限、事务、数据模型或复杂状态的实质修复后，提示用户发起针对性 review，普通样式/反馈修正局部复验即可。

`debug` 不默认构建、打包、重启或重建开发环境。确需运行验证时按项目实际模式与当前授权协调环境所有者；不假定 SQL 永不需要重载或项目不能使用容器。

## Next step

If this debug was entered from `page-acceptance` or `review`, return to that calling flow and follow its re-test/review handoff. For a standalone fix:

- If the fix changes page-observable behavior, interaction, displayed data, permission outcome or visual result, recommend user-initiated `/review` first, then user-initiated full-declared-scope `/page-acceptance`; reuse still-valid evidence for unaffected paths.
- Only after confirming no page-observable impact through the relevant consumers, record `Page acceptance: N/A — <reason>` and recommend user-initiated `/review` directly. SQL or configuration alone does not imply N/A; classify by [observable impact](../rules/workflow-contract.md#4-验收门槛与回流).
- A simple Direct fix may stop after diff/code checks without a full review; record any unrun checks rather than requiring compile/regression execution. Never start page acceptance or review automatically.

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
