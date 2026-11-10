# Skill Entry Protocol

Shared bootstrap for all skills. Read only what the current task needs; do not load every referenced file.

Stage entry, required artifacts, stop conditions and failure routing are defined once in [workflow-contract.md](workflow-contract.md); follow it without copying the stage table into each skill.

## Protocol

### Step 1: Read Project Config

Read `docs/agents/` when present. Missing files degrade to defaults; do not create them implicitly.

| File | Use | If missing |
|---|---|---|
| `domain.md` | Paths for CONTEXT, PRDs, ADRs, research | Use defaults in Step 3 |
| `repo-map.md` | Multi-repo structure and tracker owner | Treat as single-repo |
| `issue-tracker.md` | Tracker type and adapter | Ask which tracker; do not guess |
| `triage-labels.md` | Label vocabulary | Use canonical defaults |
| `language.md` | Human-facing output language | Use the user's input language; ask when unsure |
| `coding-standards.md` | Conventions, profile, source paths, verification | Use global `ruoyi6` unless the user or project explicitly selects another profile or `none` |
| `project-state.md` | Objective, stage dashboard, blockers, next step, compile/run commands and ports | Use the current request only; do not create implicitly |
| `project-decisions.md` | Durable confirmed decisions and scope | Use current code and user instructions |
| `verification.md` | Versioned evidence and known gaps | Do not treat old evidence as proof for changed code |

### Step 1a: Apply Standards

Resolve the profile in this order: current user instruction, explicit project `coding-standards.md` or `AGENTS.md` selection (including `Technical profile: none`), then the global `ruoyi6` default. A project-level `none` is an explicit opt-out, not a missing value. Do not probe framework signatures to override a selected profile.

Read the selected profile's `SKILL.md` and its task-relevant original rules from the installed skills directory; apply only to its declared repository/module/file scope. A profile is supplementary: it does not restart this protocol, authorize code during planning, replace artifact formats, skip workflow gates, or auto-chain skills.

For a RuoYi-Vue-Plus 6.x + React project whose profile is `ruoyi6`, load it for any code or contract change to backend Java, PostgreSQL/SQL, React pages, API/types, permissions or field contracts — including direct implementation, `debug` and `review`, not only `implement`. Pure documentation, read-only planning or diagnosis that changes no RuoYi code may skip loading it. If the project explicitly selects `Technical profile: none`, do not load it.

#### Standards Gate

- **Before affected work:** read the applicable standards/profile entry point and relevant originals; record their actual paths. A missing/unreadable required rule blocks affected code and compliance approval; read-only diagnosis may continue. A prior session's summary is not evidence.
- **Verification:** only checks authorized by the current request, project standards, or active stage. Authorized checks must pass on final changes with command, working directory, exit status and relevant output. If none are authorized, review the diff, label the work unverified, and never claim test, acceptance or runtime success. A failed authorized check is unresolved, not waived.
- **Stage boundaries:** planning does not compile prospective code; a read-only review may use current verifiable evidence instead of rerunning unchanged checks; an intermediate phase (notes, spike, probe) is not a delivered implementation. A check is N/A only with an explicit stage/scope reason.
- **Design and compliance:** apply constraints in think/grill, carry contracts into story acceptance criteria, use conventions in implement/debug, and check violations in review. Explicit project decisions/exceptions win with cited scope.
- **Extended rules:** [standards-gate-details.md](references/standards-gate-details.md).

#### Tracker Conventions

Use one collaboration workflow across GitHub, GitLab, Gitee and local trackers; only the transport adapter changes. Resolve the repository and `docs/agents/issue-tracker.md` first. From an Issue, read it and its comments/labels and use its acceptance criteria; a direct request does not force an Issue/PRD. Preserve returned identifiers/URLs; verify remote writes before updating local traceability; missing auth is an unpublished-work gap, not permission to switch trackers. Local Markdown tracking is the default; when a remote tracker is configured, use the platform MCP or CLI directly and keep remote writes explicitly authorized.

### Project State

`project-state.md` is an operational handoff, not requirements. Read only relevant sections; PRD `Status` and `Sliced into` remain the requirement source. Precedence: current request > project instructions > state file. Do not turn transient notes or hypotheses into decisions. Verification needs version/commit, command/path, result, date, and agent/user source. The file is created and refreshed by `setup-project`; maintain it only at the stage transitions defined in the global instructions.

### Step 2: Multi-Repo Scope

If `repo-map.md` exists, identify which repos are involved and read each repo's domain docs. If missing, treat the current repo as single; ask only when the task names files or modules outside it.

### Step 3: Read Domain Context

Read domain docs at the configured paths (defaults):

| Document | Default | Purpose |
|---|---|---|
| CONTEXT.md | Root `CONTEXT.md`; if `CONTEXT-MAP.md` exists, the per-context files it points to | Domain glossary, terms, relationships |
| PRDs | `docs/prd/PRD-NNNN-<title>.md` | Requirements and acceptance criteria |
| ADRs | `docs/adr/*.md` | Architecture decisions |
| Research INDEX | `docs/research/INDEX.md` | Reusable research records; query before re-searching |
| Audit records | `docs/audits/*.md` | Recent architecture/anti-pattern audits; read before structural changes |

If a document is missing, proceed without it and state the limitation.

**Filing consistency:** flag misplaced PRD/ADR/research files and duplicate numbering/collisions; report them, do not auto-move. Full checks and reporting format: [filing-consistency.md](references/filing-consistency.md).

### Step 3a: PRD Conflict Check

Only `/think` before creating a new PRD. `/story` and all non-PRD skills skip this step. Procedure: [think/REFERENCE.md §PRD Conflict Check](../think/REFERENCE.md#prd-conflict-check-before-assigning-nnnn).

### Step 4: Check Upstream Artifacts

If consuming another skill's output, verify:

| Signal | Action |
|---|---|
| Legacy minimal PRD from `/story` | Do not implement; recreate through `think` → `grill` |
| `Open Questions`, `[TEMPORARY]` or PRD-level unresolved `TODO` (including `TODO(prd-NNNN)`) | Upstream baseline decision unresolved; read-only planning may note. Block affected implementation/acceptance and report that the user must complete upstream `grill`; do not auto-invoke it |
| Empty `Grilled by` | Same: upstream baseline not validated; block affected coding/acceptance and report the gap; do not auto-invoke `grill` |
| `TODO(待确认)` implementation note | Non-blocking confirmation, not a baseline gap. It never masks incomplete API, page, data, validation or feedback; continue the current slice when the recommended default is fully implemented |

Record these in the skill output. Baseline gaps block coding and acceptance claims; a fully implemented `TODO(待确认)` does not block testing or `Dev Complete`, but must be reported and carried into the PRD/project state.

## Standalone vs Composable

**Standalone:** use whatever context exists. Missing PRD, CONTEXT or ADRs reduces precision but does not block work; state the missing evidence.

**Composable:** read prior outputs through the PRD `## Traceability` chain and verify completeness before relying on them.

## Reference

Skills should reference this protocol as:

```text
Apply the [Skill Entry Protocol](../rules/entry-protocol.md) before proceeding.
```
