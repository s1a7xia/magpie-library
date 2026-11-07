---
name: story
description: "Break a frozen, grilled PRD into executable vertical-slice Issues. Use only when the user explicitly asks to split a plan into tasks or Issues. Requires Status: Grilled; no shortcut around think/grill."
---

# Story: Break Plan Into Issues

🥷 Vertical slices, each issue is end-to-end.

Break a frozen, grilled baseline into independently actionable issues using vertical slices (tracer bullets). The PRD is the contract; this skill reads it and never rewrites its requirements.

## Outcome Contract

- **Outcome**: Set of Issues, each executable independently, covering the full plan
- **Done when**: All issues created with dependencies mapped; PRD created or updated with child issues
- **Evidence**: Created Issues with proper acceptance criteria, PRD (created or updated) with child issue links
- **Output**: Issue count list, PRD created/updated, next step to a user-invoked implement workflow or direct implementation

## Prerequisites

- **A frozen baseline is mandatory.** The input PRD must exist at `docs/prd/PRD-NNNN-<title>.md` with `Status: Grilled`. If there is no PRD, or its status is `Draft`, stop and tell the user to run `think` → `grill` first (grill runs automatically after think). There is no "minimal PRD" shortcut here: a baseline that was never grilled is not a baseline.
- Apply the [Skill Entry Protocol](../rules/entry-protocol.md) to locate domain docs and issue tracker config
- `docs/agents/issue-tracker.md` — read for issue creation convention; missing config means local-only output, not a guess at a tracker
- `docs/agents/triage-labels.md` — read for label mapping

## Baseline Consistency Gate

Before drafting slices, audit the frozen PRD read-only. Do not repair requirements silently in this skill.

| Check | Pass condition |
|---|---|
| Frozen | `Status: Grilled`; `Grilled by` filled |
| Resolved | No `Open Questions`, `TODO`, `?` markers, or unvalidated assumptions |
| Traceable | Requirements and criteria carry stable `R#` / `AC#` IDs; every requirement has at least one observable criterion; every criterion traces to a requirement or is explicitly marked non-functional |
| Consistent | Criteria do not contradict each other or `Out of Scope`; terminology matches `CONTEXT.md` |
| Sliceable | Dependencies can be ordered without a cycle |

If any check fails, stop before creating issues, name the offending sections or IDs, and route back to `grill` (or `think` when the goal itself changed). Slicing an inconsistent baseline only distributes the defect across tickets.

## Process Summary

**Step 0**: Read project configuration — apply the [Skill Entry Protocol](../rules/entry-protocol.md); read `docs/agents/issue-tracker.md` and `triage-labels.md`.

**Step 1**: Verify the baseline. Locate the PRD, confirm `Status: Grilled`, and run the **Baseline Consistency Gate**. Anything else stops here with the instruction to run `think` → `grill` first.

**Step 2**: Read the frozen baseline. Extract Goal, Requirements, Acceptance Criteria and Out of Scope. Do not add, soften or reinterpret requirements.

**Step 3**: Explore the codebase as needed to size the slices — current modules, existing patterns, ADRs, domain glossary.

**Step 4**: Draft vertical slices. Each slice is a thin path through every affected layer and can land verified on its own. Give every slice a `Covers` field naming the PRD requirements and acceptance criteria it closes.

**Step 5**: Record dependencies explicitly. Every slice carries `blocked-by` (or `none`). This is not optional: `implement` uses it to skip blocked work in unattended runs. Complete the coverage map: every PRD acceptance criterion is assigned to exactly one slice, or shared with a stated reason.

**Step 6**: Assemble the complete local slice list, including `Covers`, dependencies and coverage totals. Do not publish it yet; it must be complete before any remote write.

**Step 7**: Present the slice list and ask one approval question. Show title, type (HITL/AFK), `blocked-by`, `Covers`, and the acceptance criteria each slice closes. Include `Coverage: <n>/<n> PRD acceptance criteria assigned`; do not ask for approval while a criterion is unassigned.

**Step 8**: After approval, write the approved list to the PRD `## Traceability` `Sliced into` field with stable local slice IDs and set `Status: Sliced`. Local Markdown is the default; stop after the local write and say so. If a remote tracker is configured and the user asked to publish, create the child Issues in dependency order using the platform MCP or CLI, then replace local IDs with the returned identifiers. A remote failure leaves the local list intact; report it and let the user retry.

**Step 9**: If a remote parent Issue exists, update it with the child list. Do not change its title or close it. If `docs/agents/project-state.md` exists, set its `Workflow status → Slices` to `Passed` and `Development` to `Pending`, with the slice count and coverage total.

**Step 10**: Stop. Output the slice list and ask whether to start a batch with `implement`. Do not start implementation on your own.

**Slice Types:**
- **HITL**: Human-in-the-loop — requires human judgment (architecture, design, UX). Agent pauses at decision points for input.
- **AFK**: Away-from-keyboard — implementable end-to-end without human interaction.

See [STORY-FORMAT.md](STORY-FORMAT.md) for the issue title/body template (single source) and [REFERENCE.md](REFERENCE.md) for slicing detail and examples.

## Gotchas

| What happened | Rule |
|---|---|
| Slicing started without a grilled PRD | Step 1: require `Status: Grilled`; no minimal-PRD shortcut — send the user to `think` → `grill` |
| Requirements were rewritten while slicing | Step 2: the PRD is the contract; changes go through the PRD `## Change Log`, not through this skill |
| Horizontal slicing (all schema, then all API) | Use vertical slices through all layers |
| Slices too thick | Prefer many thin slices over few thick ones |
| A PRD requirement had no accepting slice | Baseline Consistency Gate / Step 5: assign every acceptance criterion to a slice before approval |
| A slice had no `blocked-by` | Step 5: every slice states its blockers or `none`; `implement` needs this to skip blocked work |
| Remote Issue creation started before the local list was complete | Step 6 then Step 8: finish and confirm the local list first; publish only when a tracker is configured and the user asked |
| A remote failure lost the slice plan | Step 8: the local list survives; report and retry, never rebuild from memory |
| Implementation started automatically after slicing | Step 10: stop and ask; `implement` is user-invoked |
| PRD or parent issue left stale | Step 6/9: update `Sliced into` and sync the parent Issue |
| Forced a wide refactor (rename shared column, retype shared symbol) into tracer bullets | Vertical Slice Rules: slice it expand → migrate batches → contract |

## Vertical Slice Rules

- Each slice traces one narrow but **complete** path through every layer
- Completed slice is demonstrable or verifiable on its own
- Prefer many thin slices over few thick ones
- Avoid file paths or code snippets — they become stale

**Wide refactors are the exception.** A wide refactor is one mechanical change (rename a shared column, retype a shared symbol) whose blast radius spans the whole codebase — no vertical slice can land green on its own. Don't force it into tracer bullets; slice it as **expand → migrate → contract**: (1) one ticket adds the new form beside the old so nothing breaks; (2) migration tickets move call sites in batches sized by blast radius (per package/directory), each batch keeping the suite green because the old form still exists, each blocked by the expand; (3) one contract ticket deletes the old form, blocked by every migrate batch. See [REFERENCE.md](REFERENCE.md) for the sequence diagram.

## Output

```
Story complete — PRD-NNNN <title> (baseline: Grilled → Sliced)

**Slices (local list, source of truth):**
* #<n> <slice name> — AFK — blocked-by: none — covers: R1, AC1
* #<n> <slice name> — AFK — blocked-by: #<n> — covers: R2, AC2-AC3
* #<n> <slice name> — HITL — blocked-by: #<n> — covers: R3, AC4

**Coverage:** <n>/<n> PRD acceptance criteria assigned

**Tracker:** <created N issues in order | local only (default) | failed: <reason>, local list intact>
**Updated:** docs/prd/PRD-NNNN-<title>.md — `Sliced into` filled, Status → Sliced

**Next:** Start a batch with `implement` for these slices? Implementation stops after each batch for page testing.
```
