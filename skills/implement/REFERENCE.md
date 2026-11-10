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
| PRD is not `Status: Grilled` or newer | Requirements are not frozen | Stop; report that the upstream baseline is unresolved and the user must complete the required stage; do not invoke `grill` here |
| `Open Questions`, `[TEMPORARY]` or `TODO(prd-NNNN)` remains | Baseline decisions unresolved | Stop; report the upstream baseline gap; do not invoke `grill` here |
| `Grilled by` field empty | Plan not validated against domain model | Stop; report the upstream baseline gap; do not invoke `grill` here |

`TODO(待确认)` is an implementation note, not a baseline marker. It does not block a slice when the recommended default is fully implemented and the note records only the remaining confirmation; it cannot hide missing API, page, data, validation or feedback.

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
2. **No slice list** — stop and report that `/story` must produce the approved slices. A PRD alone is a frozen baseline, not an implementation batch.
3. **No PRD** — a small, clear change is handled by direct implementation; a larger request needs a user-initiated upstream stage before implementation.

### Dependency Ordering

Check each issue for `Blocked by` references in its body. Implement non-blocked items first, then their dependents. If no explicit dependencies exist, implement in the order listed in `## Sliced into`.

### Coverage Pre-check

Read every slice's `Covers` field and compare it with the PRD's numbered `Requirements` (`R#`) and `Acceptance Criteria` (`AC#`). Every PRD acceptance criterion must be assigned to at least one slice before coding starts. If a criterion is unassigned, stop and report that `story` must assign it; if the PRD has no stable IDs, report the baseline defect as unresolved and do not implement it. Do not add a new requirement or silently widen a slice. Record `Coverage: <assigned>/<total>` in the batch evidence.

### Novel-Business Research Gate

Run this gate before Step 3 when a slice introduces business behavior that looks unfamiliar. The business baseline must already be settled; research resolves only technical implementation uncertainty. All conditions must hold:

1. The scenario is genuinely new to the current product, not merely a new field, page or endpoint on an existing pattern.
2. Current project implementations and `ruoyi6`'s capability map, references and templates do not cover it.
3. `docs/research/INDEX.md` has no applicable record.
4. Choosing a technical implementation without external evidence would require inventing an architecture or mechanism, not a business rule.

If any condition fails, continue with local evidence and do not invoke `research`.

If a previously unknown, non-blocking business rule, state semantic, permission boundary or acceptance criterion emerges during implementation, do not search for an external pattern to decide it and do not route to `grill`. Implement the safest/recommended default end-to-end and record a standard `TODO(待确认)` (defined in [ruoyi6 templates](../ruoyi6/references/templates.md#todo-待确认记录)) with what remains to confirm, the current behavior, whether later adjustment is expected and the confirmation owner. If the PRD already exposes it as an unresolved baseline decision, apply the Upstream Quality Check and stop before coding. Stop only the affected action/slice when no safe default exists because the choice involves an irreversible data change, unresolved permission scope or security risk; report it and do not invoke `grill`.

When the gate passes:

1. Define one bounded, answerable implementation question.
2. Run the `research` skill with live authoritative sources, preferring `magpie-web-search` and then `context7`.
3. Reuse an existing record on an INDEX hit; otherwise persist the reusable verdict under `docs/research/`.
4. Apply the verdict inside the current slice and cite the record or source in the PRD's `Research References` when it changes the implementation decision.
5. Return to Step 3 without starting another workflow stage.

Do not use this gate for ordinary CRUD, capabilities already provided by the framework, dependency/version confirmation, debugging, or facts obtainable from current code. If research contradicts the frozen baseline, stop the affected slice and report that the user must decide on upstream correction; do not invoke or return to `think`/`grill` automatically.

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

When the implementation exposes a non-blocking business detail that is not settled in the frozen PRD, complete the recommended default across API, page, data and feedback first, then add the standard `TODO(待确认)` with the expected later adjustment. Do not leave a placeholder, empty action or skipped validation. The TODO is recorded in the slice's PRD or `project-state.md` at batch close-out.

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

`Dev Complete` means code is implemented, compiled, committed and pushed. A remaining `TODO(待确认)` does not prevent `Dev Complete` when the default behavior is complete and testable; it records a future business confirmation, not a missing implementation. It does not mean accepted or done: the first full-scope page acceptance and the later review are separate user-initiated stages.

## Step 4: Batch Close-out

After all items in the batch are implemented and pushed:

1. Retain each slice's compile command/result. Reuse the latest successful check if it covers final code, dependencies and build configuration; only recompile sides whose relevant inputs changed afterwards.
2. Run the coverage gate: every PRD requirement and acceptance criterion maps through `Covers` to a slice that is `Dev Complete`. Report `Coverage: <n>/<n>` and name every gap.
3. If a PRD criterion has no slice, keep the PRD `In Progress` and report that `/story` must add a new slice (with a PRD Change Log entry when scope changed). If the slice exists but the code does not satisfy it, fix that slice and recompile.
4. Update `project-state.md` once with the batch objective, completed slices, page-acceptance requirement (`REQUIRED` or `N/A — <reason>`), next step and a TODO summary (what remains to confirm, the current default, whether later adjustment is expected and the owner); write the same summary into the PRD when a PRD exists. Update `verification.md` once with the actual per-slice compile results and any gaps.
5. Record the batch base (HEAD before the first slice), final implementation head and each slice commit hash, push state and status in the existing batch evidence. Interleaved unrelated commits must be excluded from the review scope using the slice commit list.
6. Set the PRD status to `Dev Complete` only when every slice is implemented, compiled, pushed and its `Covers` criteria are accounted for; a fully implemented `TODO(待确认)` does not block this status. Otherwise keep `In Progress` and name the blockers.
7. Do not open a browser, run page acceptance, run a full review or mark the PRD `Done`.
8. Classify the batch's observable impact. A batch with rendered, interactive, displayed-data, permission-outcome or visual changes requires the first full-scope page acceptance before review. A batch with only backend internals, background jobs, SQL, logs, configuration or other non-page-observable changes records `Page acceptance: N/A — <reason>` and hands off directly to user-initiated review.

## Step 5: Hand Off to the Next Gate

Present the batch state to the user:

```
All <N> work items implemented; compile checks, commits and pushes completed.
Compile: PASS | FAIL | NOT RUN (reason)
Coverage: <n>/<n> PRD acceptance criteria assigned; gaps: <none | IDs>
TODO(待确认): <none | items with current default, later-adjustment expectation and owner>
Page acceptance: REQUIRED | N/A — <reason>

Next: <Start the first full-scope page acceptance for <routes/pages>; after it passes, the user may explicitly start /review. | Start /review; this batch has no page-observable impact.>
```

Do not auto-run page testing or `/review`. For a page-observable batch, wait for the user to start the first full-scope page acceptance; after it passes, the user decides whether to run a full review. For a non-UI batch, wait for the user to start `/review`.

## Step 6: Output

Produce the output template from SKILL.md, filling in:
- Each work item with its implementation method and commit hash
- PRD reference and current status
- Compile result and any unverified slices
- Next gate: user-initiated `page-acceptance` for page-observable work, otherwise user-initiated `review` with `Page acceptance: N/A`

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
