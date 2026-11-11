---
name: page-acceptance
description: "Test a rendered change in the real UI: render, visual finish, interaction, data round-trip, permission, console/network. Use when the user says 页面测试、页面验收、UI 走查、走一遍页面，或明确针对页面的功能自测/冒烟测试；不用于纯后端测试. Separate from implement; compile and code review do not substitute."
---

# Page Acceptance

本阶段只能由用户单独明确发起；端到端开发授权、上一阶段完成或工作流自动续接都不能启动本阶段。

🥷 A rendered surface is its own artifact. Compilation proves syntax; this proves the page. Run it as a separate stage after development, never as an automatic step inside implementation.

# Outcome Contract

- **Outcome**: A verdict on the changed surface, backed by what was observed in a real browser.
- **Done when**: The declared scope has been exercised end to end through the UI, console and network were checked, failures were either fixed and re-run or reported as failures, anything not exercised is named, and the verdict has been written back to the project record.
- **Evidence**: URL, browser tool, step sequence, observable result per step, screenshots for visual claims, console/network findings, and the data touched.
- **Output**: Layer-by-layer verdict — render, interaction, data, permission — plus scope and untested items.

## When this stage runs

- **Started by the user.** 默认在完整 review（含修复）后，用户单独发起完整声明范围的页面验收；不自动运行。视觉探索可提前，但不能据此跳过正式范围验收。
- **Only for page-observable behavior.** This stage is required when a change affects rendering, interaction, displayed data, permission outcome or visual result. A backend-only change to internal logic, background jobs, SQL, logs or configuration records `Page acceptance: N/A — <reason>` and goes to review with applicable existing evidence; do not manufacture a browser pass for it. A mixed batch applies the gate only to its page-observable scope.
- **Unattended runs skip it.** A goal running without the user does not open a browser, does not need a login session or captcha. It stops with the slices marked `Dev Complete` and says page testing is pending.
- **Fixes are re-tested narrowly.** 首次覆盖完整声明页面范围；失败时 debug 后只复验受影响路径。最多三轮，仍失败则报告，不伪造通过。
- 阶段顺序与证据回流见 [共享契约](../rules/workflow-contract.md#4-验收门槛与回流)：默认先手动 review，再手动页面验收；首次覆盖完整声明范围，不自动启动下一阶段。


For RuoYi-Vue-Plus 6.x + React, use [the RuoYi browser quick reference](references/ruoyi6-browser.md) for session reuse, snapshot refresh, the five-step CRUD smoke path, and the error loop. Read [REFERENCE.md](REFERENCE.md) only when the page needs detailed evidence templates, multi-role/permission testing, or a failure-classification workflow beyond this file.

## Environment contract

Page acceptance drives an environment that is already running; it is not a build or deployment step.

- Acceptance never packages or rebuilds: no `mvn package` round per fix, no container rebuild, no deploying just to look at a page. It connects to the environment the project already runs.
- Use the project's actual registered environment and process/container mode. Do not impose another run mode or add dependencies for acceptance.
- If the frontend or backend is not reachable, report the check as `blocked`, name the missing service, and ask the user to start it or run the project's registered command once. Do not improvise a different run mode.
- Frontend-only changes use the dev server's HMR or a page reload. Java, backend configuration or mapper changes may need **one** reload of the already-running development process; SQL changes may need cache/config refresh depending on the actual application; do not assume no reload is ever needed. Schema/data writes require their own authorization.
- In a review round, finish the behavior-affecting fixes first, reload once, then leave the handoff for manual acceptance; first acceptance still covers the full declared scope, later re-tests may reuse valid unaffected evidence. Do not reload or restart once per fix, and do not have `debug` package or restart the service.
- Do not add `spring-boot-devtools` or another hot-reload dependency just for acceptance; it changes the project's runtime and is a separate decision.
- Restarting the backend is the environment owner's action, not part of acceptance. Do not build, package, start containers or create process-management wrappers during acceptance. Ask the user to stop the already-running process and start it again with the project's registered command once; if it is not reachable, report `blocked`.

## Step 0 — Declare the scope

Write down, before touching the browser:

- **Target**: environment, base URL, entry route.
- **Account**: which role; where the credential comes from.
- **Path**: one main path plus one meaningful boundary (empty state, validation failure, denied permission, long content, pagination edge).
- **Data boundary**: default read-only; create/update/delete only when the user has explicitly authorized the target environment and disposable test-data scope. Page-acceptance invocation alone does not authorize writing business/production records.

Take target, commands and account from the project's configured standards, `AGENTS.md`, or verified run instructions. Do not guess ports, do not invent credentials, and do not copy a credential into a report, commit, screenshot or log. If a required piece is missing, report it as a blocked check instead of improvising.

## Step 1 — Establish a session

Use the browser capability this environment actually provides, in this order:

1. The user/project-selected tool or existing host browser capability and authenticated session.
2. An installed automation CLI when appropriate and no selected tool/session would be displaced; no install required just for this stage.

Reuse a running session and its saved auth state before logging in again. Keep one session per task; do not let two operators drive the same browser.

## Step 2 — Check the surface is healthy

Load the entry route, then confirm the page rendered before judging the feature:

- Interactive elements present and named as expected.
- No framework error overlay, blank area, or stuck spinner.
- Console free of errors; network free of 401/403/500 on the requests this page needs.

Record what you saw. A failed request that predates your change is still worth naming, but separate it from the change under test.

### Visual layer (when the change is visual)

For a new or restyled page, a layout change, or any claim about "looks better", check the rendered pixels against the project's UI standard and the craft floor:

- No unintended horizontal overflow at a narrow viewport.
- Button labels stay on one line.
- Dark-mode text, secondary text, borders and disabled states remain legible.
- Dialogs, dropdowns, date pickers, tooltips and drawers have no z-index collision.
- For an ordinary RuoYi business page, verify the default baseline was implemented during development: clear hierarchy, spacing, semantic status colours, loading/empty/error states, table/form alignment and no accidental overflow. `frontend-design` is not required for this baseline and cannot excuse skipping it.

If the project has a UI standard (for RuoYi-Vue-Plus: [前端规范和样式边界](../ruoyi6/references/frontend.md#样式与设计)), use it as the acceptance reference. If the change is a deliberate design direction, compare the screenshot with the stated intent rather than with personal taste. Keep at least one screenshot for every visual claim.

## Step 3 — Walk the main path

Drive the change the way a user would, through the rendered controls only.

Only with explicit disposable-data write authorization, close a create/read/update/delete loop in this order and stop at a failure instead of pushing on:

1. **Create** — open the form, fill required fields with an identifiable marker, submit, confirm the dialog closes and the new row is visible.
2. **Read** — search for that marker, confirm filtering is correct, then reset.
3. **Update** — open the existing record, confirm fields populate from stored values (not defaults), change one field, confirm the list reflects it.
4. **Delete** — delete the marker record, confirm the confirmation step, confirm it is gone.

Clean up only the authorized records this task created, even on partial failure; never delete existing data. Without data-write authorization exercise read-only paths and report CRUD unverified; ask only if that missing scope is necessary for the requested verdict.

## Step 4 — Probe the boundary

One boundary, chosen for the change: empty state, required-field or format validation, permission-denied control for a lower-privilege role, pagination past the last page, or a long/unicode value. State which boundary you chose and why.

## Step 5 — Close the loop on failures

When something fails, do not retry blindly:

1. Read the console error and the failing request (status, payload, response).
2. Locate the cause in the code path — field name or type mismatch, missing dictionary value, permission string, mapping error, missing null handling.
3. Fix the root cause inside the authorized scope.
4. Reload, re-run from the failed step, and continue.

Allow at most three evidence-driven repair/retest rounds, then report remaining blockers; do not loop indefinitely or retry unchanged conditions. Never weaken the check to make it pass.

## Step 6 — Report

Report each layer separately and never merge them into a single "done":

| Layer | Meaning |
|---|---|
| Render | Page, table, form, states draw correctly |
| Visual | Layout, spacing, color, overflow, contrast and layer order match the project standard |
| Interaction | Controls respond; dialogs, dropdowns and pagination behave |
| Data | Values round-trip correctly through create/read/update/delete |
| Permission | Controls and requests match the role under test |

Name the untested items. A passing main path does not imply passing boundaries, other roles, or other pages. A functional pass does not imply a visual pass; report them separately.

## Step 7 — Write the verdict back

Persist the result in the same turn; a browser-only report leaves the project status stale.

- **`accepted`** — 将实际覆盖范围写为 `Accepted`；有效 review 已覆盖最终实现且收尾完成时，可在同次写回 `Done`。记录代码版本、角色、URL、完整范围、边界、控制台/网络和证据，不自动关闭远端 Issue。
- **`accepted with caveats`** — keep the tested scope at `Accepted` only when the caveats are outside its acceptance criteria. Record each unexercised role, boundary or page as an explicit remaining gap; otherwise keep it at `Dev Complete`.
- **`not accepted` or `blocked`** — use `In Progress` for a known unresolved code defect/missing behavior; use `Dev Complete` for complete implementation with an environment/evidence blocker. Record the failing step, symptom and evidence. A confirmed in-scope defect enters `debug` as part of this acceptance pass; after the fix, re-test only the affected path and return to this verdict step. Resume any untested portion of the original declared scope after repair; narrow re-testing alone is sufficient only when all other scope has valid existing evidence. Substantial permission/transaction/model/state fixes invalidate affected review evidence and require a user-initiated targeted review.
- **No PRD or slice exists** — still write the evidence to `docs/agents/verification.md` when that file is configured; otherwise report it and name the missing record instead of inventing a status.

When `docs/agents/project-state.md` exists, update its **Workflow status → Page acceptance** row in the same turn: `Passed`, `Blocked`, or `In Progress`, with the tested routes and a one-line next step. When acceptance completes `Done`, also set `Review` to `Passed` only if the review record says so, and set `Close-out` to `Passed` only if every configured closure gate is actually satisfied; remaining required actions keep close-out pending. Do not rewrite the rest of the dashboard.

After a defect fix passes re-testing, record the new tested code version and affected paths, superseding the invalidated verdict while preserving its history. Follow the [lifecycle rules](../think/PRD-FORMAT.md#prd-生命周期状态); unrelated valid evidence remains applicable. Recompute the parent PRD status from all slices; one passing slice cannot accept the whole batch.

Commit and push verdict updates only under current user/project Git authorization; preserve changes and report Git state otherwise. If the evidence belongs to a batch already pushed, use one documentation commit for this testing round; do not rewrite history or create a feature branch.

## Hard rules

- **Trigger through the UI.** The frontend request layer, auth flow and encryption are part of what is being verified; bypassing them with direct API calls tests a different system. Skip UI only when the project explicitly authorizes interface-level checks, and say which layer was then left unverified.
- **Snapshot, then act, then snapshot again.** Element references go stale after navigation, dialog open/close, dropdown expansion, and table refresh. Re-read the interactive elements after any of these.
- **Never dump a full component-tree DOM.** Component libraries nest deeply and the dump destroys the working context. Read the compact interactive-element list instead.
- **Judge visuals from pixels, not source.** Any claim about layout, spacing, color or polish needs a rendered screenshot.
- **A functional pass is not a visual pass.** When the change is visible, record the visual layer separately; "works" and "looks right" are different claims.
- **Keep the scope.** Do not turn one page check into a full regression sweep.

## Gotchas

| What happened | Rule |
|---|---|
| Compilation passed, so the page was declared fine | Run this skill; state the runtime layer separately (anti-pattern #17) |
| Old element reference used after a dialog opened | Re-read interactive elements after every DOM change |
| Full HTML pulled to "understand" the page | Interactive-element snapshot only |
| Direct API call used to prove the feature | Drive the UI; the request layer is under test |
| Test record left behind | Use an identifiable marker and delete it, or report the leftover |
| Feature "works" but looks broken | Screenshot and check layout, spacing, overflow, alignment; an ordinary business page must already carry the RuoYi frontend baseline, not wait for `frontend-design` |
| Only the happy path run | Add one boundary chosen for this change |
| Second page silently assumed fine | Every claim names which page and role it covers |

## Output

```
Page acceptance — <page / feature> [<environment>]
Scope:      <main path> + <boundary>
Account:    <role>              Data: <read-only | created and cleaned up | leftover: ...>

Render:      pass | fail | not checked — <what was seen>
Visual:      pass | fail | not checked — <overflow, button wrap, contrast, z-index, screenshot>
Interaction: pass | fail | not checked — <steps and results>
Data:        pass | fail | not checked — <round-trip evidence>
Permission:  pass | fail | not checked — <role and control/request behavior>
Console/Net: <errors, 4xx/5xx, or clean>
Evidence:    <screenshot paths, request observations>

Failures:    <fixed and re-run: step, cause, fix> or <open: step, symptom, blocker>
Debug:       <entered for confirmed in-scope defects | not needed>
Next:        <Done with valid review and acceptance | user-initiated targeted /review after substantial fix | finish local debug/retest | resolve blocker>
Not run:     <items outside the declared scope>
Verdict:     accepted | accepted with caveats | not accepted | blocked
```

When a boundary or role could not be exercised, the verdict is `accepted with caveats` or `blocked`, never a bare pass.
