---
name: page-acceptance
description: "Test a rendered change in the real UI: render, visual finish, interaction, data round-trip, permission, console/network. Use when the user says 页面测试、页面验收、功能自测、冒烟测试、UI 走查、走一遍页面. Separate from implement; compile and code review do not substitute."
---

# Page Acceptance

🥷 A rendered surface is its own artifact. Compilation proves syntax; this proves the page. Run it as a separate stage after development, never as an automatic step inside implementation.

# Outcome Contract

- **Outcome**: A verdict on the changed surface, backed by what was observed in a real browser.
- **Done when**: The declared scope has been exercised end to end through the UI, console and network were checked, failures were either fixed and re-run or reported as failures, anything not exercised is named, and the verdict has been written back to the project record.
- **Evidence**: URL, browser tool, step sequence, observable result per step, screenshots for visual claims, console/network findings, and the data touched.
- **Output**: Layer-by-layer verdict — render, interaction, data, permission — plus scope and untested items.

## When this stage runs

- **Started by the user, after development.** A batch of slices is finished and pushed; the user says "开始页面测试" or names the pages. The normal sequence is `implement → first full-scope acceptance → review → repair-scope acceptance → Done`. Do not start on your own, and never inside `implement`.
- **Only for page-observable behavior.** This stage is required when a change affects rendering, interaction, displayed data, permission outcome or visual result. A backend-only change to internal logic, background jobs, SQL, logs or configuration records `Page acceptance: N/A — <reason>` and goes to review with compile evidence; do not manufacture a browser pass for it. A mixed batch applies the gate only to its page-observable scope.
- **Unattended runs skip it.** A goal running without the user does not open a browser, does not need a login session or captcha. It stops with the slices marked `Dev Complete` and says page testing is pending.
- **Fixes are re-tested narrowly.** There are two distinct passes: the first acceptance covers the declared full page scope after development; the second runs after a full review has changed code, and covers only the repaired points and their connected paths. Do not replace the first pass with a repair-only pass. Three rounds of verify → fix → re-test is the ceiling; past that, stop and report what still fails.
- **Passing a first full-scope pass produces `Accepted`.** An implemented-but-untested change stays `Dev Complete`. `Accepted` means the declared page scope passed; `Done` still requires the project's close-out conditions, including a passing user-initiated full review. Without it, remain `Accepted`. After a first-pass acceptance, the next stage is review.
- **A post-review repair pass completes close-out only when review already covered the final code.** That pass covers only the repaired points and connected paths. If review stayed open and has not inspected the final code, record `Accepted` and return to review. If review already completed over the final code and this pass reveals no remaining defect, write `Done` and update close-out; do not require a second full review. Not every review fix needs a new browser pass: if the fix changes no page-observable behavior, interaction, data feedback, permission outcome or visual result, the original acceptance evidence remains valid.

For RuoYi-Vue-Plus 6.x + React, use [the RuoYi browser quick reference](references/ruoyi6-browser.md) for session reuse, snapshot refresh, the five-step CRUD smoke path, and the error loop. Read [REFERENCE.md](REFERENCE.md) only when the page needs detailed evidence templates, multi-role/permission testing, or a failure-classification workflow beyond this file.

## Environment contract

Page acceptance drives an environment that is already running; it is not a build or deployment step.

- Acceptance never packages or rebuilds: no `mvn package` round per fix, no container rebuild, no deploying just to look at a page. It connects to the environment the project already runs.
- The run mode is the project's registered command. A locally launched application process is the norm: use the command recorded in the project's standards, such as `java -jar` for a packaged backend and the project's frontend dev script. Keep the app out of a container locally so code and config stay directly editable; reserve containers for deployment-shaped environments.
- If the frontend or backend is not reachable, report the check as `blocked`, name the missing service, and ask the user to start it or run the project's registered command once. Do not improvise a different run mode.
- Frontend-only changes use the dev server's HMR or a page reload. Java, backend configuration or mapper changes may need **one** reload of the already-running development process; SQL-only changes need none.
- In a review round, finish the behavior-affecting fixes first, reload once, then run one repair-scope acceptance. Do not reload or restart once per fix, and do not have `debug` package or restart the service.
- Do not add `spring-boot-devtools` or another hot-reload dependency just for acceptance; it changes the project's runtime and is a separate decision.
- Restarting the backend is the environment owner's action, not part of acceptance. Do not build, package, start containers or create process-management wrappers during acceptance. Ask the user to stop the already-running process and start it again with the project's registered command once; if it is not reachable, report `blocked`.

## Step 0 — Declare the scope

Write down, before touching the browser:

- **Target**: environment, base URL, entry route.
- **Account**: which role; where the credential comes from.
- **Path**: one main path plus one meaningful boundary (empty state, validation failure, denied permission, long content, pagination edge).
- **Data boundary**: read-only, or may create/update/delete identifiable test records.

Take target, commands and account from the project's configured standards, `AGENTS.md`, or verified run instructions. Do not guess ports, do not invent credentials, and do not copy a credential into a report, commit, screenshot or log. If a required piece is missing, report it as a blocked check instead of improvising.

## Step 1 — Establish a session

Use the browser capability this environment actually provides, in this order:

1. A browser automation CLI already installed and usable.
2. The built-in browser or computer-use tooling of the current agent.

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

For a create/read/update/delete surface, close the loop in this order and stop at a failure instead of pushing on:

1. **Create** — open the form, fill required fields with an identifiable marker, submit, confirm the dialog closes and the new row is visible.
2. **Read** — search for that marker, confirm filtering is correct, then reset.
3. **Update** — open the existing record, confirm fields populate from stored values (not defaults), change one field, confirm the list reflects it.
4. **Delete** — delete the marker record, confirm the confirmation step, confirm it is gone.

Clean up test data even when the run fails partway, and say so if cleanup was impossible.

## Step 4 — Probe the boundary

One boundary, chosen for the change: empty state, required-field or format validation, permission-denied control for a lower-privilege role, pagination past the last page, or a long/unicode value. State which boundary you chose and why.

## Step 5 — Close the loop on failures

When something fails, do not retry blindly:

1. Read the console error and the failing request (status, payload, response).
2. Locate the cause in the code path — field name or type mismatch, missing dictionary value, permission string, mapping error, missing null handling.
3. Fix the root cause inside the authorized scope.
4. Reload, re-run from the failed step, and continue.

Repeat until the declared scope passes, or report the specific blocker. Never weaken the check to make it pass.

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

- **`accepted`** — a first full-scope pass sets the tested PRD or slice from `Dev Complete` to `Accepted`. A post-review repair pass whose completed review already covered the final code sets the affected slice and parent PRD to `Done`; otherwise it leaves them at `Accepted` for review to finish. Tick only the acceptance criteria actually exercised. On the first pass, record the full declared page scope. On a repair pass, record the invalidated scope and repaired points. Append the verified implementation commit (and any relevant uncommitted changes), URL/route, account role, main path, boundary, console/network result, evidence paths and date to `docs/agents/verification.md`, marked as verified by the agent. Do not close Issues without separate authorization.
- **`accepted with caveats`** — keep the tested scope at `Accepted` only when the caveats are outside its acceptance criteria. Record each unexercised role, boundary or page as an explicit remaining gap; otherwise keep it at `Dev Complete`.
- **`not accepted` or `blocked`** — keep the status at `Dev Complete`. Record the failing step, symptom and evidence. A confirmed in-scope defect enters `debug` as part of this acceptance pass; after the fix, re-test only the affected path and return to this verdict step. If the failure is found in the second post-review pass, return to the same repair-scope loop; do not restart the full page scope.
- **No PRD or slice exists** — still write the evidence to `docs/agents/verification.md` when that file is configured; otherwise report it and name the missing record instead of inventing a status.

When `docs/agents/project-state.md` exists, update its **Workflow status → Page acceptance** row in the same turn: `Passed`, `Blocked`, or `In Progress`, with the tested routes and a one-line next step. When a repair pass completes `Done`, also set `Review` to `Passed` only if the review record says so, and set `Close-out` to `Passed` with the remaining release action, if any. Do not rewrite the rest of the dashboard.

After a defect fix passes re-testing, record the new tested code version and affected paths, superseding the invalidated verdict while preserving its history. Follow the [lifecycle rules](../think/PRD-FORMAT.md#prd-生命周期状态); unrelated valid evidence remains applicable. Recompute the parent PRD status from all slices; one passing slice cannot accept the whole batch.

Commit and push the verdict update with the affected slice's repository state. If the evidence belongs to a batch already pushed, use one documentation commit for this testing round; do not rewrite history or create a feature branch.

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
Next:        <First pass accepted -> user-initiated /review | repair pass accepted and review covered final code -> status written back to Done | repair pass accepted but review must still inspect final code -> /review | review fix changed no page-observable behavior -> original acceptance remains valid | finish current debug retest | resolve blocker>
Not run:     <items outside the declared scope>
Verdict:     accepted | accepted with caveats | not accepted | blocked
```

When a boundary or role could not be exercised, the verdict is `accepted with caveats` or `blocked`, never a bare pass.
