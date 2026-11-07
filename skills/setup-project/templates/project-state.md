# Project State

## Compile checks

默认只编译受影响的前后端，不选择交付档位。记录实际命令和工作目录；没有的命令标为待确认。

- Backend: <actual compile command and directory, or not applicable>
- Frontend: <actual build command and directory, or not applicable>
- 不自动运行测试、lint 或独立类型检查；UI 可见改动仍按 `page-acceptance` 走页面验收；构建内置编译检查保留。

## Workflow status

> 当前批次总览，只在阶段转换时更新。PRD 的 `Status` 与 `Sliced into` 才是需求状态源；这里不复制需求或验收标准。多个并行 PRD 时每个 PRD 一张表。

### PRD-NNNN <title>

| Stage | Status | Evidence / next |
|---|---|---|
| Baseline | Pending | <PRD path; Grilled or reason> |
| Slices | Pending | <slice count; uncovered criteria or none> |
| Development | Pending | <batch state; compile evidence> |
| Page acceptance | Pending | <routes; accepted / blocked / not started> |
| Review | Pending | <requested / passed / not requested> |
| Close-out | Pending | <remaining docs, commit or release action> |

**Status values:** `Pending`, `In Progress`, `Passed`, `Blocked`, `N/A`.

## Current objective

<one sentence, or "Project setup complete; no active delivery task.">

## Active work

- <task or Issue identifier>: <state>

## Blockers / risks

- <only material current blockers, or "None recorded.">

## Next step

<one concrete action>

## Updated

<YYYY-MM-DD — source: agent or user>
