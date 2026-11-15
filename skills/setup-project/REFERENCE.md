# Setup Project: Detailed Reference




## Contents

- [Re-run Checklist](#re-run-checklist)
- [Re-run Behavior](#re-run-behavior)
- [Migration (Structural Changes)](#migration-structural-changes)
- [Conformance Sweep (Re-run Only)](#conformance-sweep-re-run-only)
- [Traceability](#traceability)
- [Step 1: Explore](#step-1-explore)
- [Step 2: Detect Project Structure](#step-2-detect-project-structure)
- [Step 3: Present Findings](#step-3-present-findings)
- [Step 4: Ask for Overrides](#step-4-ask-for-overrides)
- [Step 5: Confirm](#step-5-confirm)
- [Step 6: Write](#step-6-write)
- [Step 7: Done](#step-7-done)
- [Seed Templates](#seed-templates)

---

## Re-run Checklist

When `docs/agents/` already exists and the user explicitly asks to update project configuration, check only the config files relevant to that request:

| Config file | Detection check | Drift signal | Action |
|---|---|---|---|
| `issue-tracker.md` (only if present) | Does the configured tracker still match how this project actually tracks work? | Tracker changed or was abandoned | Present change, confirm, rewrite or remove with authorization |
| `triage-labels.md` (only if present) | Check only the labels relevant to the requested tracker update | Labels renamed, added, or deprecated | Present change, confirm, rewrite `triage-labels.md` |
| `domain.md` | Does `CONTEXT-MAP.md` exist now when it didn't before? Were domain dirs (`docs/prd/`, `docs/adr/`, `docs/research/`) reorganized? | Context layout changed (single↔multi), dirs moved | Present change, confirm, rewrite `domain.md` |
| `language.md` | Read the existing value only when language is in scope | Language preference changed | Confirm, rewrite `language.md`; report affected docs without auto-rewriting them |
| **doc content** | When the requested change affects existing docs, scan only those record types | Config changed (language, naming, FORMAT) | Report affected files; change them only when cleanup is authorized |
| `repo-map.md` (if exists) | Has the project structure changed? (Workspace files added/removed? User mentions sibling repos?) | Package count changed, repos added/removed, project type (single↔mono↔multi) changed | Present diff, confirm, rewrite `repo-map.md`. If project type changed → trigger **Migration** path below |
| (no `repo-map.md` yet) | Detect new multi-repo or monorepo signals: workspace files, user mentions sibling repos, subproject dirs | New structure signals found | Ask if project structure changed, create `repo-map.md` if needed |
| AGENTS.md/CLAUDE.md `## Agent skills` block | Only if the requested configuration touches this block: are its recorded project facts still accurate? | Structure, language, or configured-record paths changed | Present the affected section and update it in place with confirmation |
| AGENTS.md/CLAUDE.md `## Engineering principles` section | Only if principles are in scope: check them against the current stack and real commands | Stack or verification commands changed | Present the diff and update the section only when requested |

**If no drift detected in any section**, tell the user: "All config is current — no changes needed." and stop.

## Re-run Behavior

When re-running, follow this sequence:

1. **Read the affected config** — load only the `docs/agents/*.md` files relevant to the requested change
2. **Run the relevant Re-run Checklist rows** — do not expand into an unrelated project audit
3. **Present diff** — show what changed vs what stayed the same. Only ask about changed sections.
4. **Update selectively** — rewrite only files that need changes. Leave untouched files alone.

If the user says "update repo map" or "switch issue tracker", keep the change to that configuration area.

## Migration (Structural Changes)

When the repo's structure has changed significantly since the last setup-project run, additional migration actions are needed beyond the normal re-run update.

| Previous state | Current state | Migration actions |
|---|---|---|
| **Single repo** | **Monorepo** (workspace files detected) | Add per-package `docs/agents/` dirs for packages with their own domain scope. Update `domain.md` to mention multi-context option. If `CONTEXT-MAP.md` was created, reference it in `domain.md`. |
| **Single repo** | **Multi-repo** (user mentions sibling repos) | Create `repo-map.md` listing all repos. Add tracker ownership only if the project uses Issues. |
| **Monorepo** | **Single repo** (workspace removed) | Remove per-package `docs/agents/` dirs (**ask first** — destructive). Simplify `domain.md` back to single-context. If `CONTEXT-MAP.md` was removed, remove references to it. |
| **Multi-repo** | **Single repo** | Remove `repo-map.md` (**ask first** — destructive). Remove tracker ownership only if it is no longer valid. |
| **Monorepo** | **Multi-repo** (packages split into separate repos) | Move per-package config to the new repos (`repo-map.md` + per-repo `docs/agents/`). Ask: "Which repo gets the shared domain docs?" |
| Any structure | **Reorganized domain dirs** (e.g. `docs/prd/` renamed or split across contexts) | Update `domain.md` with new paths. Check if old paths have stale files and ask about cleanup. |

**Rule:** Migration implies rewriting more files than a normal re-run. Always present the full diff of what will be created, rewritten, and removed. Get explicit approval before removing any files (anti-pattern #16).

## Conformance Sweep (Re-run Only)

Only when the requested configuration changes an existing document rule, sweep the affected records for drift against that rule.

### Naming Audit

Check each file's name against the convention defined in the relevant FORMAT spec:

| Directory | Expected pattern | Example |
|-----------|-----------------|---------|
| `docs/prd/` | `PRD-NNNN-<title>.md` | `PRD-0001-user-subscription.md` |
| `docs/adr/` | `<NNNN>-<title>.md` (no `ADR-` prefix) | `0001-event-sourced-orders.md` |
| `docs/research/` | `<stack>-<topic>-<major>.md` | `react-concurrent-rendering-18.md` |

For each mismatch: report `<file> does not match convention — expected <pattern>`. Renaming is a destructive op: list every violating file individually, then request one explicit authorization covering exactly that listed set (anti-pattern #16 — this is same-shape op authorization, not interview questioning; it does not relax the one-decision-per-message rule for actual decisions).

### Language Audit

When documentation language is explicitly in scope, read `docs/agents/language.md` and scan only the affected files:

- If detected language differs from setting → flag the file
- Do NOT auto-translate; report the file as needing an authorized content update
- Report: `"<file> is in <detected>, but language.md requires <expected>. Update that file only when translation is within the current authorization."`

### Format Audit

Compare each file's section headers against its FORMAT spec:

| Type | Required sections |
|------|------------------|
| PRD | `# Title`, `## Goal`, `## Requirements`, `## Acceptance Criteria`, `## Out of Scope`, `## Traceability` |
| ADR | `# Title`, `## Status`, `## Context`, `## Decision`, `## Consequences` |
| Research | `# Title`, `## TL;DR`, `## Question`, `## Approach`, `## Findings`, `## Verdict`, `## Boundary Conditions`, `## Sources` |

Report missing or extra sections. Do NOT auto-add placeholder sections.

### Metadata Consistency

Check PRD `## Traceability` fields against lifecycle:
- `Sliced into` exists but child issues list empty?
- `Status` says `Grilled` but `Grilled by` empty?
- Child Issue referenced but `## Issue` field missing?
- `Status` says `Done` but not all child issues `— Done`?

Informational only — report, don't auto-fix.

### Action Rules

| Category | Action |
|----------|--------|
| **Naming** | List each misnamed file; one explicit authorization for the listed renames only (destructive-op rule #16). |
| **Language** | Flag only; never auto-translate without authorization. |
| **Format** | Report deviations only. Never auto-add empty sections. |
| **Metadata** | Report inconsistencies only. Never auto-fix. |

## Traceability

This skill does not create or modify PRDs, so it does not fill any PRD `## Traceability` field. Instead, its outputs form the **config layer** of the project's traceability chain:

```
setup-project (config layer)
    ↓ docs/agents/*.md are read by the Entry Protocol
    ↓
dev-workflow / think / research / grill / story / implement / review / debug / setup-project
    ↓ each fills its own PRD Traceability fields
```

Consumer skills reference these config files via the [Skill Entry Protocol](../rules/entry-protocol.md), which reads `docs/agents/` at startup. Without this setup, consumer skills degrade to guesses and defaults (entry protocol "If missing" paths).

When the project structure changes, re-running the `setup-project` stage updates the config layer so downstream stages continue to read correct paths.

## Step 1: Explore

Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- `git remote -v` — is this a GitHub repo? GitLab? No remote?
- `AGENTS.md` and `CLAUDE.md` at the repo root — does either exist? Is there already an `## Agent skills` section in either?
- `CONTEXT.md` and `CONTEXT-MAP.md` at the repo root
- `docs/adr/` and `docs/prd/` directories
- `docs/agents/` — does this skill's prior output already exist?
- `.scratch/` — sign that a local-markdown issue tracker convention is already in use

**Monorepo detection (Step 2):**
- `package.json` with `"workspaces"` field (npm/yarn)
- `pnpm-workspace.yaml` — pnpm workspaces
- `lerna.json` — Lerna monorepo
- `Cargo.toml` with `[workspace]` — Rust monorepo
- `go.work` or `go.mod` with workspace — Go workspace
- `pyproject.toml` with `[tool.poe.tasks]` or similar — Python workspace
- `build.gradle.kts` or `settings.gradle.kts` — Gradle multi-project
- `pom.xml` with `<modules>` — Maven multi-module
- `subprojects/` or `packages/` or `apps/` or `libs/` directory patterns
- `docs/adr/` inside subdirectories — sign of per-package architecture tracking

**Stack detection (feeds the engineering-principles tailoring, Section E):**

- Frontend: framework deps in `package.json` (react/vue/svelte/next/…), `src/components|app|pages` directories
- Backend: server entrypoints, `api/`/`server/` directories, backend framework deps
- Database: ORM config (drizzle/prisma/knex/typeorm/…), `migrations/` directories, schema files
- Multi-tenant signals: auth middleware, tenant/org IDs in schemas, "multi-tenant" in the README
- Verification commands: package.json `scripts`, Makefile, justfile, CI workflows — candidates for the change quick reference

## Step 2: Detect Project Structure

Based on your exploration, classify the project:

| Signal | Classification |
|---|---|
| No workspace files, no subproject dirs | **Single repo** |
| Workspace files found (see Step 1), multiple packages/apps/libs | **Monorepo** |
| User mentions related repos or sibling repos exist outside this clone | **Multi-repo** |
| Both workspace files AND related repos | **Monorepo + Multi-repo** |

Ask the user to confirm the detection. If unsure, ask: "Is this a single project, a monorepo with multiple packages, or part of a multi-repo setup?"

### Multi-repo: Collect Repo Information

If multi-repo, collect the repos one at a time — one repo per message, each field derived from prior answers where possible (git remotes often already name the repos and URLs; read those first, don't ask). Per repo:
- **Repo name/slug** — e.g., `backend`, `frontend`, `shared`
- **Remote URL** — so skills can reference it
- **Domain role** — what the repo does (API server, web app, shared library, infrastructure)
- **Issue tracker** — optional; if Issues are used, which repo owns them?

Record this as `docs/agents/repo-map.md` (see seed template below).

## Step 3: Present Findings

Summarise what's present and what's missing. Show the detected defaults:

- **Project structure**: single repo / monorepo / multi-repo
- **Issue tracker**: optional. Detect GitHub/GitLab only as a candidate; do not enable Issue creation merely because a remote exists.
- **Triage labels**: defaults (needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix)
- **Domain docs**: single-context (one CONTEXT.md + docs/adr/ at root) or multi-context (CONTEXT-MAP.md exists)
- **Documentation language**: undetected by default — present as "please choose" (see Section D). If existing PRDs/ADRs/CONTEXT.md are consistently in one language, offer that as the recommended default.
- **Engineering principles**: detected stack scope (fullstack / backend-only / frontend-only; multi-tenant yes/no) and candidate quick-reference commands, from the Step 1 stack detection (see Section E)

## Step 4: Ask for Overrides

Present the detected configuration. Ask the user: "Does this look right? Anything to change?"

If the user wants to change something, walk through that section **one at a time**:

### Section A — Issue Tracker

> The "issue tracker" is optional. Configure it only if this project actually uses Issues and the user wants AI work items published there.

Options:
- **GitHub** — issues live in the repo's GitHub Issues (uses the `gh` CLI)
- **GitLab** — issues live in the repo's GitLab Issues (uses the `glab` CLI)
- **Local markdown** — issues live as files under `.scratch/<feature>/` in this repo (good for solo projects or repos without a remote)
- **Other** (Jira, Linear, etc.) — ask the user to describe the workflow in one paragraph; the skill will record it as freeform prose

For **multi-repo**: ask which repo owns the primary issue tracker. The other repos' `issue-tracker.md` can point to the primary repo's tracker.

### Section B — Triage Label Vocabulary

> When issues are created or managed, they carry triage labels. The five canonical roles:

- `needs-triage` — maintainer needs to evaluate
- `needs-info` — waiting on reporter
- `ready-for-agent` — fully specified, AFK-ready (an agent can pick it up with no human context)
- `ready-for-human` — needs human implementation
- `wontfix` — will not be actioned

Ask the user if they want to override any of the default label strings. If their issue tracker has no existing labels, the defaults are fine.

### Section C — Domain Docs

> Relevant skills may read `CONTEXT.md`, ADRs, and PRDs when those documents exist. This section records non-default paths; missing documents do not require setup.

Options:
- **Single-context** — one `CONTEXT.md` + `docs/adr/` + `docs/prd/` at the repo root. Most repos are this.
- **Multi-context** — `CONTEXT-MAP.md` at the root pointing to per-context `CONTEXT.md` files (typically a monorepo). PRDs and ADRs may be per-context or shared.

For **multi-repo**: the domain docs may be split across repos. The `repo-map.md` records which repo owns which docs. Consumer skills check the map first.

### Section D — Documentation Language

> Skills produce a lot of human-facing text: PRDs, ADRs, `CONTEXT.md`, issue bodies and titles, review reports, comments. Writing all of it in one consistent language keeps the docs readable for the whole team — regardless of which member (or agent session) triggered the skill. Without this config, each skill falls back to "follow the user's input language", which drifts whenever a different member runs a skill.

Options:
- **English** — all human-facing output is written in English.
- **Chinese (中文)** — all human-facing output is written in Chinese.
- **Other** — name the language (e.g. 日本語, Deutsch); skills write output in it.

This is a **single language for the whole project** — it applies uniformly to PRDs, ADRs, `CONTEXT.md`, Issues, and comments. It is recorded in `docs/agents/language.md`, and every consumer skill reads it via the Skill Entry Protocol. Code, identifiers, and CLI commands are never affected — only prose.

**Detection heuristic (Step 3):** there is nothing in the repo that reliably reveals the team's preferred doc language, so do **not** guess. Surface this section as "undetected — please choose" and let the user pick. If `CONTEXT.md` or existing PRDs already exist and are consistently in one language, offer that as the recommended default.

**Common pitfall:** the user typing the command is not necessarily the audience. A Chinese-speaking developer may still want English docs for an international team. Ask which language the *team* reads, not which language the conversation is in.

### Section E — Engineering Principles

> The `## Engineering principles` section in AGENTS.md/CLAUDE.md tells every agent session and contributor how this repo expects engineering work done — design-first planning, module quality, boundaries, security, concurrency, UX, reuse, maintainability, reversibility — and which commands verify each kind of change before committing. It is generated from [templates/engineering-principles.md](templates/engineering-principles.md), tailored to this repo.

Present the detected tailoring as a draft; the user confirms or edits:

- **Scope** — which conditional blocks apply (<Multi-tenant>, <Backend>, <Frontend>), from Step 1 stack detection
- **File-size bound** — principle 2's line limit (suggest 500 when the repo shows no other convention)
- **Dependency-check locations** — principle 7's where-to-check-first paths (from workspace detection)
- **Change quick reference** — baseline and per-change-type commands, filled from package.json scripts / Makefile / CI config. Never invent commands; a row with no real command is dropped, not guessed.
- **Language** — the section is rendered in the Section D language (headings and prose translated; commands, paths, and identifiers stay as-is)

If the file already carries a hand-written `## Engineering principles` (or equivalent) section, ask: adopt as-is (setup stops managing it), merge, or replace. Never overwrite it silently.

## Step 5: Confirm

Show the user a draft of all files to be written. Let them edit before writing. The draft includes the tailored `## Engineering principles` section — confirm its scope, placeholder fills, and quick-reference commands before writing.

## Step 6: Write

**Pick the file to edit:**

- If `CLAUDE.md` exists, edit it.
- Else if `AGENTS.md` exists, edit it.
- If neither exists, ask the user which one to create — don't pick for them.

Never create `AGENTS.md` when `CLAUDE.md` already exists (or vice versa) — always edit the one that's already there.

If an `## Agent skills` block already exists in the chosen file, update its contents in-place rather than appending a duplicate. Don't overwrite user edits to the surrounding sections.

**The `## Agent skills` block** (single-repo / monorepo baseline; multi-repo adds the Repo map section):

The block opens with a fixed **Working principles** section — the first-principles reasoning prompt below, copied **verbatim** into every repo. It is not customised per project and has no `docs/agents/` config file: it lives in AGENTS.md/CLAUDE.md itself so every agent session reads it at startup, before any skill runs. All other sections are one-line summaries pointing at `docs/agents/` config files.

```markdown
## Agent skills

### Working principles

Apply first-principles reasoning to engineering work. Establish WHAT before determining HOW. Verify material facts before relying on them: inspect the actual code and relevant files, run the relevant commands or tests, and do not infer behavior beyond the available evidence. When verification is impossible, state the gap explicitly as an assumption; treat unstated goals and constraints the same way. Analogy is not evidence. Decompose a problem only until further decomposition can no longer change the next action. Trace every material conclusion to a fact, constraint, goal, or explicit assumption. Prefer the simplest solution that satisfies all real constraints and can be verified. Treat existing code and conventions as evidence about the system, not as unquestionable authority: understand why an existing solution works before extending, replacing, or reusing it; follow established conventions by default, and deviate only with a stated reason.

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout — "single-context" or "multi-context"]. See `docs/agents/domain.md`.

### Documentation language

[one-line summary — e.g. "all docs in English"]. See `docs/agents/language.md`.

<!-- Multi-repo only: include this section -->
### Repo map

[one-line summary of multi-repo structure]. See `docs/agents/repo-map.md`.
```

Then write the docs files using the seed templates in [templates/](templates/).

**The `## Engineering principles` section** — written into the same file, immediately after the `## Agent skills` block, from [templates/engineering-principles.md](templates/engineering-principles.md). Apply the Section E tailoring: drop inapplicable conditional blocks, fill placeholders from detected evidence, render in the Section D language. If the section already exists, update it in-place — never append a duplicate. If the user chose "adopt as-is" in Section E, skip writing it.

### Monorepo: Per-Package Config

For each detected package with its own domain scope, create `docs/agents/` inside that package as well, but with a simpler config:

```markdown
# Domain Docs (package: <pkg-name>)

This package's domain docs:
- **`CONTEXT.md`** at the package root (falls back to repo root if missing)
- **`docs/adr/`** at the package root (falls back to repo root if missing)

For shared conventions (including documentation language), see repo root `docs/agents/`.
```

**On re-run:** check that per-package `docs/agents/` dirs are still in sync with the current package structure. If packages were added, create new per-package configs. If packages were removed/renamed, update or remove the corresponding per-package configs (**ask first** before removing — destructive).

## Step 7: Done

Tell the user which requested configuration is now in place and which files were written. Mention that they can edit those files directly later; do not prescribe a setup refresh schedule. Re-run this skill only when the user explicitly requests a configuration update.

---

## Seed Templates

Each generated file is seeded from a template, customised based on the user's choices in Step 3-4. The templates live as separate files so they can be maintained independently and read on demand:

| Output file | Seed template | When used |
|---|---|---|
| `## Engineering principles` | [templates/engineering-principles.md](templates/engineering-principles.md) | Only when project principles are explicitly requested; skip when the project keeps its own section |
| `docs/agents/issue-tracker.md` | [templates/issue-tracker-github.md](templates/issue-tracker-github.md) | Only when the project actually uses GitHub Issues and tracker configuration is requested |
| | [templates/issue-tracker-gitlab.md](templates/issue-tracker-gitlab.md) | Only when the project actually uses GitLab Issues and tracker configuration is requested |
| | [templates/issue-tracker-local.md](templates/issue-tracker-local.md) | Only when the project uses local markdown issues and requests tracker configuration |
| `docs/agents/triage-labels.md` | [templates/triage-labels.md](templates/triage-labels.md) | Only after tracker configuration was explicitly requested |
| `docs/agents/domain.md` | [templates/domain.md](templates/domain.md) | Only when domain-document paths need configuration; include only the record types the project actually uses |
| `docs/agents/language.md` | [templates/language.md](templates/language.md) | Only when the team wants a fixed documentation language |
| `docs/agents/repo-map.md` | [templates/repo-map.md](templates/repo-map.md) | Multi-repo only, and only when requested |

Read the relevant template file, apply the user's Step 4 overrides, and write the customised result to the target path.
