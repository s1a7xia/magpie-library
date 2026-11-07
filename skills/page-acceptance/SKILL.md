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

- **Started by the user, after development.** A batch of slices is finished and pushed; the user says "开始页面测试" or names the pages. Do not start on your own, and never inside `implement`.
- **Unattended runs skip it.** A goal running without the user does not open a browser, does not need a login session or captcha. It stops with the slices marked `Dev Complete` and says page testing is pending.
- **Fixes are re-tested narrowly.** When a defect is fixed, re-run only the affected page and path — not the whole batch. Three rounds of verify → fix → re-test is the ceiling; past that, stop and report what still fails.
- **Passing this stage produces `Accepted`.** An implemented-but-untested change stays `Dev Complete`. `Accepted` means the declared page scope passed; `Done` still requires the project's close-out conditions, including a passing full review when one was requested.

For RuoYi-Vue-Plus 6.0.0 + Vue, use [the RuoYi browser quick reference](references/ruoyi-6-vue-browser.md) for session reuse, snapshot refresh, the five-step CRUD smoke path, and the error loop.

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

If the project has a UI standard (for RuoYi-Vue-Plus: [RuoYi UI 规范](../ruoyi-6-vue/references/ui-design.md)), use it as the acceptance reference. If the change is a deliberate design direction, compare the screenshot with the stated intent rather than with personal taste. Keep at least one screenshot for every visual claim.

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

- **`accepted`** — set the tested PRD or slice from `Dev Complete` to `Accepted`. Tick only the acceptance criteria actually exercised. Append the URL/route, account role, main path, boundary, console/network result, evidence paths and date to `docs/agents/verification.md`, marked as verified by the agent. Do not mark `Done` and do not close Issues without separate authorization.
- **`accepted with caveats`** — keep the tested scope at `Accepted` only when the caveats are outside its acceptance criteria. Record each unexercised role, boundary or page as an explicit remaining gap; otherwise keep it at `Dev Complete`.
- **`not accepted` or `blocked`** — keep the status at `Dev Complete`. Record the failing step, symptom and evidence. Enter `debug` for the confirmed defect, then re-test only the affected path.
- **No PRD or slice exists** — still write the evidence to `docs/agents/verification.md` when that file is configured; otherwise report it and name the missing record instead of inventing a status.

When `docs/agents/project-state.md` exists, update its **Workflow status → Page acceptance** row in the same turn: `Passed`, `Blocked`, or `In Progress`, with the tested routes and a one-line next step. Do not rewrite the rest of the dashboard.

After a defect fix passes re-testing, update the same verdict record — do not append a contradictory second "accepted" entry.

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
| Feature "works" but looks broken | Screenshot and check layout, spacing, overflow, alignment |
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
Not run:     <items outside the declared scope>
Verdict:     accepted | accepted with caveats | not accepted | blocked
```

When a boundary or role could not be exercised, the verdict is `accepted with caveats` or `blocked`, never a bare pass.
