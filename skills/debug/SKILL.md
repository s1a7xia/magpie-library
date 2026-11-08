---
name: debug
description: "Root cause analysis and systematic fix. Quick root cause location, then 6-phase systematic loop for bug fixes. Use when errors, crashes, regressions, test failures, anomalous behavior, or the user says 'used to work'. Trigger words: debug, 排查, 报错, 崩溃, 不工作, regression, 以前是好的, broken after update."
---

# Debug: Root Cause Analysis and Systematic Fix

🥷 Find root cause before fixing.

This skill restores intended behavior; it does not redesign the UI. Do not load `frontend-design` or add visual polish during debugging. If the requested outcome is a visual redesign rather than a defect fix, stop and treat it as a separate explicit design task.

> **Terminology note:** debug uses **Stage** (macro: Stage 0 context / Stage 1 quick-locate / Stage 2 systematic-fix) and **Phase** (micro: the 6-phase loop inside Stage 2) deliberately, to distinguish quick-locate from systematic-fix. Other skills use **Step**. This is an intentional divergence, not drift.

## Outcome Contract

- **Outcome**: Bug fixed with a regression guard when authorized, root cause documented, debug artifacts cleaned
- **Done when**: Bug no longer reproduces, the authorized regression test and reproduction check pass or their absence is recorded, instrumentation removed, root cause in commit/PR message when a commit is authorized
- **Evidence**: Reproduction loop passes; when tests are authorized, the regression test fails on old code and passes on new
- **Output**: Root cause, fix, confirmation, test location, regression guard

## Process Summary

**Stage 0 (Context Setup)**: Apply the [Skill Entry Protocol](../rules/entry-protocol.md) and its [Standards Gate](../rules/entry-protocol.md#standards-gate) for applicable coding rules and verification. It also locates domain docs; domain vocabulary helps form accurate hypotheses.

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
| Fix needs >5 files | Pause and confirm scope with user |

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

Next: Run `/review` for non-trivial fixes. For simple fixes with clear regression tests, review is optional.

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
