# Skill Entry Protocol

Shared bootstrap sequence for all skills. Each skill references this protocol instead of repeating the full instructions.

## Purpose

Every skill needs to locate domain docs, identify multi-repo scope, and check for upstream artifacts before starting work. This protocol standardizes that bootstrap — it operationalizes [anti-patterns.md #1](anti-patterns.md) (act before reading) as a shared sequence. It ensures skills can run **standalone** (graceful degradation when prerequisites are missing) and **composable** (correctly reads prior skill outputs when chained).

## Protocol

When entering any skill, perform this read sequence **before** starting skill-specific work:

### Step 1: Read Project Config

Read config files under `docs/agents/` (created by `setup-project`). If the directory doesn't exist, skip to defaults.

When the task involves both Codex and dsh, read `docs/agents/ai-collaboration.md` if present and apply the shared [ai-collaboration skill](../ai-collaboration/SKILL.md). The project file supplies the canonical remote/tracker and any confirmed project-specific role refinements.

| File | What it tells you | If missing |
|------|-------------------|------------|
| `docs/agents/domain.md` | Actual paths for CONTEXT.md, PRDs, ADRs (may differ from defaults in multi-repo/monorepo) | Use default paths (Step 3) |
| `docs/agents/repo-map.md` | Multi-repo structure — which repos exist, which owns the issue tracker | Treat as single-repo |
| `docs/agents/issue-tracker.md` | Issue tracker type and CLI conventions | Ask user which tracker they use |
| `docs/agents/ai-collaboration.md` | Multi-agent role ownership, handoff channel, and write boundaries | Use the shared role defaults in `ai-collaboration` when multiple agents collaborate |
| `docs/agents/triage-labels.md` | Label vocabulary mapping | Use canonical defaults |
| `docs/agents/language.md` | Language consumer skills should write human-facing output in (PRDs, ADRs, CONTEXT, Issues, comments) | Fall back to the user's input language; ask when unsure |
| `docs/agents/coding-standards.md` | Applicable coding conventions, technical profile, source paths, and verification commands | Follow existing project instructions/style; do not assume a framework profile |
| `docs/agents/project-state.md` | Current objective, active work, blockers, next step, and default delivery profile | Treat the current request as the only task context; do not create a state file implicitly |
| `docs/agents/project-decisions.md` | Confirmed cross-task decisions, their scope, and superseded choices | Use current code and user instructions when no matching decision exists |
| `docs/agents/verification.md` | Reusable verification evidence and known gaps | Do not treat old evidence as proof for changed code |

### Step 1a: Apply Project Standards and Tracker Conventions

**Coding standards.** If configured, read the maintained standards and the named technical profile's `SKILL.md` from the installed skills directory, then its task-relevant original references. Apply only to its declared repository/module/file scope. If no profile is configured, use one only when the actual project or explicit task establishes its applicability. A profile is supplementary context: it does not restart this protocol, authorize code during planning, replace artifact formats, skip workflow gates, or auto-chain skills.

#### Standards Gate

**Required context before affected work.** Once a standard/profile applies, successfully read its configuration, entry point and relevant original rules before changing affected code or approving its compliance. Record their actual paths in the task evidence. A missing/unreadable file, an unresolved reference or a missing original is a blocked prerequisite: stop affected code changes and compliance approval, identify what could not be read, and restore it within the authorized scope when possible. Read-only diagnosis and unrelated work may continue; a prior session's summary does not satisfy this gate.

**Verification authorization before completion.** Checks are required only when the current request, the project's explicitly adopted delivery profile, or this stage's explicitly authorized verification calls for them. Derive the scope from the active stage, applicable standards and actual project build configuration. When checks are authorized, a code task is complete, verified, or eligible for a `Done` transition only after they pass against its final changes; preserve command, working directory, exit status and relevant output as evidence. When no check is authorized, complete the implementation with the diff reviewed, label it unverified, and do not claim test, acceptance, or runtime success. When an authorized check fails, repair and rerun it within scope; when it cannot run, report the affected task as blocked/unverified. Existing merge/release criteria still apply after authorized checks pass.

**Stage boundaries.** Planning does not require compiling prospective code. A read-only review may use current, verifiable build/test evidence for the change under review instead of rerunning unchanged checks solely because a review was requested. An intermediate phase that is not the delivered result (planning notes, a spike, a probe) is not a completed implementation; apply the delivery checks once the real change exists. Mark a check not applicable only with an explicit stage/scope reason. A missing dependency, failed command or unread standard is not a not-applicable reason. A review may report findings with verification gaps, but must withhold an unqualified pass when required evidence is missing or stale.

Apply design constraints during think/grill, carry agreed contracts into story acceptance criteria, use implementation conventions during implement/debug, and check violations during review. Explicit project decisions/exceptions take precedence over generic defaults; cite their source and scope rather than inventing a waiver. Where documented API usage conflicts with the checkout, expose the mismatch and inspect source before writing code.

#### Tracker Conventions

All issue/PR/release examples in consumer skills are illustrative. Select operations from `docs/agents/issue-tracker.md` before executing them; never send a Gitee target to `gh` or `glab`.

**Use one collaboration workflow across GitHub, GitLab, Gitee, and local trackers.** Resolve the repository and configured tracker first. When a task starts from an Issue, read that Issue, its relevant comments and labels, and use its acceptance criteria as the work input. Keep the shared Story Format, planning/implementation/review stages, local Git workflow, and user-facing progress/reporting consistent across providers. Only the transport adapter changes: CLI, MCP, OpenAPI, or local files. For work that starts from a direct user request, do not force an Issue/PRD workflow unless the task calls for planning or tracking.

Preserve the tracker's returned identifiers and URLs (Gitee Issue numbers are case-sensitive strings), and verify remote writes before updating local traceability. Missing authentication is an unpublished-work gap, not permission to switch trackers. With no `.git` directory (for example a downloaded ZIP), do not infer a remote from an upstream README; retain configured tracker facts and report unavailable Git operations.

### Project State and Delivery Profile

Treat `project-state.md` as a concise operational handoff, not a replacement for requirements or source inspection. Read only the sections relevant to the current task. Its default delivery profile is effective only when the project `AGENTS.md`/`CLAUDE.md` explicitly adopts it; otherwise the global default remains change-only. The order of precedence is: current request, applicable project instructions, then the state file.

`project-decisions.md` records durable, confirmed choices. Do not turn a transient implementation detail, an unverified hypothesis, or a chat preference into a decision. `verification.md` must identify the version or commit, command/path, result, date, and whether the evidence came from the agent or the user. A changed file, environment, dependency, or requirement can invalidate old evidence.

### Step 2: Identify Multi-Repo Scope

If `repo-map.md` exists, identify which repos are involved in the current task. Cross-repo tasks require reading domain docs from all relevant repos.

If `repo-map.md` is missing, treat the current repo as the only repo. If the task mentions files or modules outside this repo, ask the user.

### Step 3: Read Domain Context

Read domain docs at the paths discovered in Step 1 (or defaults if config missing):

| Document | Default path | Purpose |
|----------|-------------|---------|
| CONTEXT.md | `CONTEXT.md` at repo root; if a root `CONTEXT-MAP.md` exists (multi-context repo), the per-context `CONTEXT.md` files it points to | Domain glossary — terminology, concepts, relationships |
| PRDs | `docs/prd/PRD-NNNN-<title>.md` | Product requirements — what to build, acceptance criteria |
| ADRs | `docs/adr/*.md` | Architecture Decision Records — past technical decisions |
| Research INDEX | `docs/research/INDEX.md` | Searchable index of persisted technical research records (stack × topic × major). Query before re-searching; see `/research` skill |
| Audit records | `docs/audits/*.md` | Dated architecture and anti-pattern audit records. Read the most recent before proposing structural changes — it records which judgments were already made and why |

**If any document is missing, proceed without it.** Missing context reduces precision but does not block execution. State what's missing so the user knows the limitation.

**Filing-consistency check.** While scanning for these docs, also flag misplaced files so the drift surfaces early. Report (do not auto-fix — moving files is a destructive op needing explicit authorization):

- PRD content found **outside** `docs/prd/` — e.g. `docs/adr/PRD-*.md`, `docs/prd-*.md` in the docs root, or `PRD-*.md` at repo root.
- ADR files carrying a `PRD-` prefix, or PRD files carrying no `PRD-` prefix.
- Research records found **outside** `docs/research/` — e.g. `<stack>-<topic>-<major>.md` at repo root or under `docs/`.
- **Number collisions** — two ADRs sharing the same `NNNN`, or two PRDs sharing the same `PRD-NNNN` (common when multiple sessions run concurrently). Scan the directory and report any duplicate numbers before creating a new file.
- **Research record collisions** — two records sharing the same `<stack>-<topic>-<major>` filename (a `/research` duplicate; see `/research` Step 2 dedup).

Report findings as a note in the skill output: *"Filing inconsistency found: <file> appears misplaced / <NNNN> is used by two files. Want me to relocate?"* Do not silently move or renumber.

### Step 3a: PRD Conflict Check (only for PRD-creating skills)

Applies **only** to skills about to create a new PRD file (`/think` Step 2, `/story` Step 3). Skills that only read an existing PRD — and all non-PRD skills (`debug`, `review`, etc.) — skip this entirely.

The full procedure lives with the primary PRD-creator: see [think/REFERENCE.md §PRD Conflict Check](../think/REFERENCE.md#prd-conflict-check-before-assigning-nnnn). It is owned there rather than in this shared protocol so that non-PRD skills don't carry PRD-management ceremony they never use. `/story` follows the same procedure when it creates a minimal PRD.

### Step 4: Check Upstream Artifacts (Composability)

If the skill consumes another skill's output, verify upstream quality:

| Signal | Meaning | Action |
|--------|---------|--------|
| PRD Traceability shows `Created by: /story (minimal PRD)` | Requirements may not be decision-complete — no `/think` session | Confirm acceptance criteria with user before proceeding |
| PRD has `Open Questions` or `TODO` markers | `/grill` may not have resolved all decisions | Note: "PRD has unresolved items" — proceed but flag uncertainty |
| PRD `Grilled by` field is empty | Plan not validated against domain model | Proceed but note plan is unvalidated |

These are notes, not blockers. Record them in the skill's output.

## Standalone vs Composable

**Standalone (no prior skill ran):** The skill works with whatever context exists. If no PRD, no CONTEXT.md, no ADRs — the skill derives what it can from the codebase and user input. It does not refuse to start.

**Composable (prior skills ran):** The skill reads prior outputs via the Traceability chain in PRD files. Each PRD's `## Traceability` section records which skills touched it, enabling the current skill to verify completeness.

## Reference

Skills should reference this protocol as:
```
Apply the [Skill Entry Protocol](../rules/entry-protocol.md) before proceeding.
```
