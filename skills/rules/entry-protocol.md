# Skill Entry Protocol

Optional context discovery shared by engineering skills. Each skill references this protocol instead of repeating the full instructions.

## Purpose

Read the smallest set of project facts needed for the current task. This protocol prevents acting before reading relevant evidence, while avoiding a mandatory full-project preload. It ensures skills can run **standalone** when optional docs are missing and **composable** when relevant prior outputs exist.

## Protocol

Use this sequence selectively before skill-specific work. Read only files relevant to the current request; do not scan the whole repository or every document directory by default.

### Step 1: Read Project Config

Read config files under `docs/agents/` only when they exist and affect the current task. A missing directory is a valid standalone setup, not a reason to initialize the project.

| File | What it tells you | If missing |
|------|-------------------|------------|
| `docs/agents/domain.md` | Actual paths for CONTEXT.md, PRDs, ADRs (may differ from defaults in multi-repo/monorepo) | Use default paths (Step 3) |
| `docs/agents/repo-map.md` | Multi-repo structure — which repos exist, which owns the issue tracker | Treat as single-repo |
| `docs/agents/issue-tracker.md` | Optional issue tracker type and CLI conventions | No tracker: use existing project docs or the current conversation; do not ask or initialize one |
| `docs/agents/triage-labels.md` | Label vocabulary mapping | Use canonical defaults |
| `docs/agents/language.md` | Language consumer skills should write human-facing output in (PRDs, ADRs, CONTEXT, Issues, comments) | Follow the user's current language; ask only when the audience materially matters |


### Step 2: Identify Multi-Repo Scope

If `repo-map.md` exists and the current task crosses repository boundaries, identify the repositories actually involved and read only their relevant docs.

If `repo-map.md` is missing, treat the current repo as the only repo. Investigate an explicitly mentioned external path when it is readable; ask only if the missing repository changes the task outcome.

### Step 3: Read Domain Context

Read only domain docs that can affect the current task:

| Document | Default path | Purpose |
|----------|-------------|---------|
| CONTEXT.md | `CONTEXT.md` at repo root; if a root `CONTEXT-MAP.md` exists (multi-context repo), the per-context `CONTEXT.md` files it points to | Domain glossary — terminology, concepts, relationships |
| PRDs | `docs/prd/PRD-NNNN-<title>.md` | Product requirements — what to build, acceptance criteria |
| ADRs | `docs/adr/*.md` | Architecture Decision Records — past technical decisions |
| Research INDEX | `docs/research/INDEX.md` | Optional index of persisted technical research records (stack × topic × major). Check it when it exists and the current decision depends on prior research |
| Audit records | `docs/audits/*.md` | Dated architecture and anti-pattern audit records. Read the most recent before proposing structural changes — it records which judgments were already made and why |
| Project state | Existing project status record; otherwise `docs/project-state.md` | Current stage, task statuses, next action, remaining work, risks, blockers, and acceptance evidence. Use the project instructions for a non-default path; follow Project State Maintenance below |

**If any document is missing, proceed without it.** Do not create blank docs, initialize `docs/agents/`, or suggest setup merely because a document is absent. Mention a concrete evidence gap only when it affects the current conclusion.

**Filing-consistency check.** When a relevant documentation directory is already being read, flag clearly misplaced files that affect this task. Do not scan unrelated directories. Report the issue; moving or renaming files requires explicit authorization.

- PRD content found **outside** `docs/prd/` — e.g. `docs/adr/PRD-*.md`, `docs/prd-*.md` in the docs root, or `PRD-*.md` at repo root.
- ADR files carrying a `PRD-` prefix, or PRD files carrying no `PRD-` prefix.
- Research records found **outside** `docs/research/` — e.g. `<stack>-<topic>-<major>.md` at repo root or under `docs/`.
- **Number collisions** — two ADRs sharing the same `NNNN`, or two PRDs sharing the same `PRD-NNNN` (common when multiple sessions run concurrently). Scan the directory and report any duplicate numbers before creating a new file.
- **Research record collisions** — two records sharing the same `<stack>-<topic>-<major>` filename. Report a duplicate before creating another record.

Report findings as a note in the skill output: *"Filing inconsistency found: <file> appears misplaced / <NNNN> is used by two files. Want me to relocate?"* Do not silently move or renumber.

### Step 3a: PRD Conflict Check (only before creating a PRD)

Applies **only** when the current task has already chosen to create a new PRD file. Skills that read an existing PRD, work conversationally, or do not use a PRD skip this entirely.

The full procedure lives with the primary PRD-creator: see [think/REFERENCE.md §PRD Conflict Check](../think/REFERENCE.md#prd-conflict-check-before-assigning-nnnn). It is owned there rather than in this shared protocol so that non-PRD stages don't carry PRD-management ceremony they never use. The `story` stage follows the same procedure when it creates a minimal PRD.

### Step 4: Check Relevant Upstream Artifacts

If the current task consumes a PRD or another persisted artifact, verify only the fields that affect the next action:

| Signal | Meaning | Action |
|--------|---------|--------|
| PRD Traceability shows a minimal PRD created during slicing | Requirements may not be decision-complete | Confirm the acceptance criteria needed for the current task |
| PRD has `Open Questions` or `TODO` markers | Some decisions remain unresolved | Resolve only those that affect the current action; otherwise note the uncertainty |
| PRD has no validation record | Design may not have been separately challenged | Proceed; validation is optional unless the current task needs it |

These are notes, not blockers and not a reason to initialize missing process artifacts.

## Project State Maintenance

For large, multi-session, or multi-stage projects, reuse one current-state record (existing status doc or task board; otherwise `docs/project-state.md`). A non-default path may be recorded in existing project instructions; no separate path-config file is needed.

- Before work, read the current summary and relevant requirements; reconcile code claims with the branch, working-tree diff, and relevant commits. Do not scan all history. Git proves code changes, not business acceptance; if Git is unavailable, state the evidence gap rather than initializing a repository.
- Keep the current iteration, objective, next action, risks, blockers, and acceptance evidence. Use one task list with stable IDs and statuses, or link the existing task source instead of duplicating it. Separate iteration remaining work from known project backlog; mark unsliced scope as unknown, not a completion percentage.
- After a slice, scope change, blocker, or acceptance decision, and before session handoff, update only facts changed by the authorized task. Pure questions and read-only reviews do not authorize document edits. No changed facts means no ceremonial update.
- Distinguish implementation complete, unverified, failed verification, passed verification, and business acceptance. Record actual evidence or the unverified boundary; a commit does not imply acceptance.
- Keep the summary short. Do not copy whole PRDs, diffs, or task lists into it, or mutable status into AGENTS.md. Missing documents do not trigger setup; create them only within requested initialization or documentation work. Never create them for a small change merely to satisfy process.
- These rules do not authorize tests, commits, pushes, or deployment. When a commit is authorized, include the related status update within its scope. Setup only initializes records; the task's executing agent maintains them, not a background service.

## Standalone vs Composable

**Standalone (no prior artifact):** The skill works with the codebase, the current request, and any relevant existing docs. The absence of a PRD, tracker, `CONTEXT.md`, or ADR does not block ordinary work.

**Composable (relevant artifact exists):** The skill reads only the traceability or decision fields needed to understand the current slice. It does not require the full historical chain.

## Reference

Skills should reference this protocol as:
```
Apply the [Skill Entry Protocol](../rules/entry-protocol.md) before proceeding.
```
