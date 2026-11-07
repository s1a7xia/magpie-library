# Implement: Detailed Reference

## Step 1: Entry Protocol Detail

Apply the [Skill Entry Protocol](../rules/entry-protocol.md) to read config and domain context.

### Context Checklist

- [ ] `docs/agents/domain.md` — actual paths for CONTEXT.md, PRDs, ADRs
- [ ] `docs/agents/repo-map.md` — multi-repo structure
- [ ] `docs/agents/issue-tracker.md` — tracker type and CLI conventions
- [ ] `docs/agents/triage-labels.md` — label vocabulary
- [ ] `docs/agents/language.md` — human-facing output language
- [ ] `docs/agents/coding-standards.md`, selected profile and original rules — apply the [Standards Gate](../rules/entry-protocol.md#standards-gate) for loading and completion evidence
- [ ] `CONTEXT.md` — domain glossary
- [ ] `docs/prd/PRD-NNNN-<title>.md` — product requirements (the PRD)
- [ ] `docs/adr/*.md` — architecture decision records
- [ ] `docs/research/INDEX.md` — research knowledge base

### Upstream Quality Check

Check the PRD's `## Traceability` section for each of these signals and note them in the output:

| Signal | Meaning | Note |
|--------|---------|------|
| PRD is not `Status: Grilled` or newer | Requirements are not frozen | Stop; return to `think` → `grill` |
| `Open Questions` or `TODO` markers remain | Decisions unresolved | Stop; return to `grill` |
| `Grilled by` field empty | Plan not validated against domain model | Stop; return to `grill` |

### Filing-Consistency Check

While scanning domain docs, flag (report, do not auto-fix):

- PRD content outside `docs/prd/`
- ADR files with `PRD-` prefix or PRD files without `PRD-` prefix
- Research records outside `docs/research/`
- Number collisions (two PRDs sharing the same NNNN, two ADRs sharing the same NNNN)
- Research record collisions (same `<stack>-<topic>-<major>` filename)

## Step 2: Work Inventory

### Determine Work Items

Work items come from the approved slice list. Do not create a second work breakdown here:

1. **Issues from `/story`** — read the `## Sliced into` list in the PRD. Each issue is a seam. Read each issue's body for its Acceptance Criteria and blocked-by relationships.
2. **No slice list** — stop and return to `/story`. A PRD alone is a frozen baseline, not an implementation batch.
3. **No PRD** — a small, clear change is handled by direct implementation; a larger request returns to `think` → `grill`.

### Dependency Ordering

Check each issue for `Blocked by` references in its body. Implement non-blocked items first, then their dependents. If no explicit dependencies exist, implement in the order listed in `## Sliced into`.

### Coverage Pre-check

Read every slice's `Covers` field and compare it with the PRD's numbered `Requirements` (`R#`) and `Acceptance Criteria` (`AC#`). Every PRD acceptance criterion must be assigned to at least one slice before coding starts. If a criterion is unassigned, stop and return to `story`; if the PRD has no stable IDs, treat coverage as unverifiable and return to `story`/`grill` to label it. Do not add a new requirement or silently widen a slice. Record `Coverage: <assigned>/<total>` in the batch evidence.

### PRD Status Update

Update the PRD status line from:
```
> **Status**: Sliced | **PRD**: PRD-NNNN | **Created**: YYYY-MM-DD | **Last updated**: YYYY-MM-DD
```
to:
```
> **Status**: In Progress | **PRD**: PRD-NNNN | **Created**: YYYY-MM-DD | **Last updated**: YYYY-MM-DD
```

Also set `Last updated` to today's date.

## Step 3: Implement Each Seam

### 3a. Direct Implementation

Implement each item directly. Read the seam's acceptance criteria first and confirm they are clear;
the project is documentation-driven, so the PRD or issue body is the contract.

1. **Understand the behavior** — read the issue body or PRD acceptance criteria
2. **Implement** — write the minimal code that satisfies the acceptance criteria
3. **Apply engineering principles design-time** — there is no separate Refactor phase behind this path. Consult [../rules/engineering-principles.md](../rules/engineering-principles.md) while writing; its Consumer & Ownership Map lists this path against every principle, in design-time terms. Read each entry's *When NOT to apply* before restructuring anything — the counter-indications are what keep this from becoming speculative abstraction.
4. **Run the required compile check** — compile the affected side with the project's real build command and make it pass; otherwise record the slice as unverified
5. **Tests** — write or run tests only when the current request explicitly asks for test work

### 3b. Compilation

After each item is implemented:

1. Take the actual backend/frontend compile commands and working directories from the project config, build files or verified run instructions.
2. Run only the affected side: backend for backend changes, frontend for frontend changes, both when both changed.
3. If it fails, read the error output, fix the cause and re-run. Do not substitute a separate typechecker, lint run or full test suite for the required compile check.

If no real compile command can be found, mark the slice unverified and name the missing command; do not invent one.

### 3c. Testing Boundary

Compilation is the normal slice gate. Do not run tests unless the current request explicitly asks for test work. Page testing is a separate stage in `page-acceptance`, started by the user after the batch is pushed.

When tests are explicitly requested, run only the requested minimal target and report its actual output. When they are not requested, record `not run — outside current request`; never imply that compilation proves runtime behavior.

### 3d. Committing

Commit each slice separately with a descriptive message, then push it to the existing upstream on the current branch. Never create a feature branch for one requirement.

```
[PRD-NNNN] <seam title> — <summary>

Implemented <what>.
<additional context if needed>
```

- Reference the issue number in the commit message body
- Commit only the changes related to this item
- Do not commit changes that belong to a different work item — **minimal change per commit** (anti-pattern #5)
- If the working tree has pre-existing dirty state unrelated to this session, warn the user before committing
- Include the slice's PRD status in the same commit. Update `project-state.md` and `verification.md` once at batch close-out; the verification entry carries the actual compile result for each slice in that batch.
- After pushing, verify the remote reference; if the push fails, report the slice as committed but not pushed

**Commit message examples:**
```
[PRD-0003] User subscription data model — schema + CRUD API

Implemented subscription schema, repository, and CRUD API.
Closes #42
```

```
[PRD-0003] Subscription management UI — view/cancel/upgrade

Implemented subscription management page with view, cancel, and upgrade flows.
Page testing remains a separate stage.
Closes #43
```

### Slice Status Update

After each item is committed and pushed, update the PRD's `## Sliced into` list. Change the relevant slice's status from `— In Progress` or no marker to `— Dev Complete`:

```
- #<issue-1> — [PRD-NNNN] <slice title> (AFK) — covers: R1, AC1 — Dev Complete
```

`Dev Complete` means code is implemented, compiled, committed and pushed. It does not mean accepted or done: page testing and review are separate stages.

## Step 4: Batch Close-out

After all items in the batch are implemented and pushed:

1. Compile the affected sides once more and record the commands and results, retaining each slice's compile command/result in the batch evidence.
2. Run the coverage gate: every PRD requirement and acceptance criterion maps through `Covers` to a slice that is `Dev Complete`. Report `Coverage: <n>/<n>` and name every gap.
3. If a PRD criterion has no slice, keep the PRD `In Progress` and return to `story` for a new slice (with a PRD Change Log entry when scope changed). If the slice exists but the code does not satisfy it, fix that slice and recompile.
4. Update `project-state.md` once with the batch objective, completed slices and next step; update `verification.md` once with the actual per-slice compile results and any gaps.
5. List every slice with its commit hash, push state and `Dev Complete` or unverified status.
6. Set the PRD status to `Dev Complete` only when every slice is implemented, compiled, pushed and its `Covers` criteria are accounted for; otherwise keep `In Progress` and name the blockers.
7. Do not open a browser, run page acceptance, run a full review or mark the PRD `Done`.

## Step 5: Hand Off to Page Testing

Present the batch state to the user:

```
All <N> work items implemented; compile checks, commits and pushes completed.
Compile: PASS | FAIL | NOT RUN (reason)
Coverage: <n>/<n> PRD acceptance criteria assigned; gaps: <none | IDs>

Next: Start page testing for <routes/pages>. Page acceptance is a separate, user-initiated stage.
```

Do not auto-run page testing or `/review`. Wait for the user to start page acceptance; after it passes, the user decides whether to run a full review.

## Step 6: Output

Produce the output template from SKILL.md, filling in:
- Each work item with its implementation method and commit hash
- PRD reference and current status
- Compile result and any unverified slices
- Next step to user-initiated `page-acceptance`

## Recovery Procedures

### Compile Regression

If a change for item B breaks compilation for previously implemented item A:

1. The dependency ordering was wrong — item B should have been implemented after A
2. Fix item B's implementation to not break A
3. Recompile both A and B before proceeding

### Dirty Working Tree

If the working tree has uncommitted changes before starting:

1. Warn the user: "Working tree has uncommitted changes from outside this session."
2. Stop the affected slice when the changes cannot be separated safely. Do not stash, revert, or include unrelated changes in implement commits.
3. Resume only after the user resolves or explicitly assigns those changes.

### Compile Command Not Found

If no real compile command can be found:

1. Mark the affected slices unverified
2. Record the missing command and the evidence gap in `verification.md`
3. Do not invent a command or claim the slice compiled
