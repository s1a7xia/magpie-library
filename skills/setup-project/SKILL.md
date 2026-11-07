---
name: setup-project
description: "Initialize or reconfigure a repository's engineering setup: issue tracker, project state, compile commands, domain docs, principles, coding profile, and optional WeChat entry. Use when the user says 按通用资源库配置这个项目 or asks to refresh project collaboration. Not required for every task."
---

# Setup Project

Scaffold the per-repo configuration that the engineering skills assume:

- **Project standards** — project-specific conventions and a stack-tailored engineering quick reference written into `docs/agents/coding-standards.md`. Global working principles and workflow rules stay in the Magpie global instructions and are not copied per repo.
- **Project structure** — single repo, monorepo (multiple packages in one repo), or multi-repo (multiple related repos)
- **Issue tracker** — where issues live (GitHub, GitLab, Gitee via official MCP/OpenAPI, local markdown, or other)
- **Triage labels** — the strings used for the five canonical triage roles
- **Domain docs** — where `CONTEXT.md`, ADRs, PRDs, and the research index live; how consumer skills find them across repos
- **Documentation language** — the language skills should write human-facing output in (PRDs, ADRs, CONTEXT, Issues, comments), so output is readable for the team regardless of who triggers the skill
- **Coding standards** — project conventions and a technical profile. The global default is `ruoyi-plus-dev`; do not probe framework signatures or ask whether the project is RuoYi. Register the selected profile in project config. If the user identifies the project as non-RuoYi, record `Technical profile: none` (or the user-named alternative) and the reason as an explicit project override so later sessions do not fall back to the global default. A different installed profile is used only when the user names it.
- **Project handoff** — concise current state, durable decisions, versioned verification evidence, and affected-side compile commands
- **Agent collaboration** — when multiple agents share a project, define role ownership and handoff in `docs/agents/ai-collaboration.md`
- **WeChat entry (optional)** — when the project wants the WeChat assistant entry, keep the WeChat sections in `docs/agents/ai-collaboration.md` and output a ready-to-paste registry entry for the user. The machine-level index (`~/.dsh/im/PROJECTS.md`) is maintained by the user, never written by this skill. Without it the project runs standalone.

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write. It is required for project initialization or reconfiguration, not a gate before ordinary implementation tasks.

**Can be re-run.** If `docs/agents/` already exists, read current config first, detect what changed since last setup, present only the sections that need updating, and rewrite affected files. The user can also use this to switch issue trackers, add/remove repos from the map, or reorganize domain docs.

## Global-first default

The shared Magpie instructions are the single source for working principles, workflow routing, compile policy, page-acceptance timing, and Git rules. Project setup must not duplicate them.

- **Default: do not create or modify `AGENTS.md` / `CLAUDE.md`.** All project-specific facts go into `docs/agents/`.
- If the project already has `AGENTS.md` or `CLAUDE.md`, only update the file that exists and only with project-specific facts or a short pointer to `docs/agents/`.
- If the user explicitly asks for a project-level rules file, write a short pointer block; never copy the global Working principles, engineering workflow, compile policy, page-acceptance policy, or commit policy into it.
- Project-specific engineering principles (file-size bounds, dependency-check paths, per-change verification commands) live in `docs/agents/coding-standards.md`.

## Relationship to the Entry Protocol

This skill creates the configuration that the [Skill Entry Protocol](../rules/entry-protocol.md) reads at the start of every consumer skill. Without this setup, consumer skills fall back to default paths and guesses.

| Config file | Entry Protocol Step | What it tells the consumer skill |
|---|---|---|
| `docs/agents/domain.md` | Step 1 | Actual paths for CONTEXT.md, PRDs, ADRs, and `docs/research/INDEX.md` |
| `docs/agents/issue-tracker.md` | Step 1 | Issue tracker type and CLI conventions |
| `docs/agents/ai-collaboration.md` | Step 1 | Multi-agent role ownership, handoff, and write boundaries |
| `docs/agents/triage-labels.md` | Step 1 | Label vocabulary mapping for the five canonical triage roles |
| `docs/agents/language.md` | Step 1 | Language for all human-facing prose (PRDs, ADRs, CONTEXT, Issues, comments) |
| `docs/agents/coding-standards.md` | Step 1a (if configured) | Scoped conventions, technical profile, source evidence, and verification commands |
| `docs/agents/repo-map.md` | Step 2 (if exists) | Multi-repo structure — which repos exist, which owns the primary issue tracker |
| `docs/agents/project-state.md` | Step 1 | Current objective, workflow-stage dashboard, blockers, next step, and actual backend/frontend compile commands |
| `docs/agents/project-decisions.md` | Step 1 | Durable confirmed choices and their scope |
| `docs/agents/verification.md` | Step 1 | Versioned verification evidence and known gaps |

This is not a consumer skill — it is the **foundation** that consumer skills depend on. The Entry Protocol's "If missing" degradation paths ensure skills still work without setup-project, but with reduced precision.

## Outcome Contract

- **Outcome**: `docs/agents/` directory with issue-tracker, triage-labels, domain docs, documentation language, project-state, project-decisions, verification, optional multi-agent collaboration contract, optional coding-standards registration, and (for multi-repo) repo-map. `AGENTS.md`/`CLAUDE.md` is updated only when it already exists or the user explicitly asks; it carries a short project-specific pointer, not a copy of the global workflow. On re-run: conformance sweep results — naming, language, and format audit of existing doc files.
- **Done when**: User confirms configuration, all required files written, and the AGENTS.md/CLAUDE.md decision is recorded (updated only when applicable)
- **Evidence**: `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, `docs/agents/domain.md`, `docs/agents/language.md`, `docs/agents/project-state.md`, `docs/agents/project-decisions.md`, `docs/agents/verification.md`; `coding-standards.md` when configured; `docs/agents/repo-map.md` (multi-repo only); project-specific engineering quick-reference present in `coding-standards.md`
- **Output**: Summary of configuration, next step to use engineering skills

## Process Summary

**Step 1: Explore** — detect current repo state (remote, existing AGENTS.md/CLAUDE.md, existing docs/agents/, workspace/monorepo structure) and stack signals for the principles tailoring (frontend/backend/DB, multi-tenant, verification scripts). If `docs/agents/` exists, read all current config files to understand existing setup. If neither AGENTS.md nor CLAUDE.md exists, do not create one by default.

**Step 2: Detect project structure** — single repo, monorepo, or multi-repo. Ask the user if detection is uncertain or if there are related repos not visible in this clone. If config already exists, compare detected structure against `repo-map.md` to find what changed.

**Step 3: Present findings** — show detected defaults (project structure, issue tracker, triage labels, domain layout, documentation language, coding standards and any technical profile, project handoff and compile commands). If updating, show a diff of what changed vs current config.

**Step 4: Ask for overrides** — present the full detected configuration as a draft; ask if anything needs changing. If the user wants to change something, walk through that section one at a time. Sections: A (Issue Tracker), B (Triage Labels), C (Domain Docs), D (Documentation Language), E (Project Engineering Principles — scope, line bound, dependency paths, quick-reference commands; written into `docs/agents/coding-standards.md`), F (Coding Standards — project setting overrides the global `ruoyi-plus-dev` default; do not probe framework signatures or ask whether the project is RuoYi; if the user identifies a non-RuoYi project, record `none` or the named alternative explicitly with its reason), G (Project Handoff and Compile Commands), H (WeChat Entry — optional, default off), I (Project AGENTS.md/CLAUDE.md — default skip; update only if the file exists or the user explicitly asks). For G, record actual backend/frontend compile commands and working directories. Default to compiling only affected sides, skipping tests; do not ask the user to select delivery profiles or approve routine compilation. Do not independently run lint, type checks, tests or browser checks unless explicitly requested; preserve compilation checks built into the existing build command. If everything looks good, proceed.

**Step 4a (Re-run only): Conformance sweep** — After config overrides are confirmed, scan `docs/prd/`, `docs/adr/`, `docs/research/` for files that don't match the new settings. Group findings by naming, language, format, and metadata. For naming violations suggest rename; for language flag and suggest manual translation or an installed writing skill; for format/metadata report only. Confirm with user before acting. See [REFERENCE.md](REFERENCE.md) Conformance Sweep.

**Step 5: Confirm** — show the complete draft of all files to be written (each `docs/agents/` file, plus the optional AGENTS.md/CLAUDE.md pointer only when applicable). If updating, show only files that changed.

**Step 6: Write** — write the `docs/agents/*.md` config files first. Update `AGENTS.md`/`CLAUDE.md` last, and only when it already exists or the user explicitly asked for it; a project-level file gets a short pointer to `docs/agents/`, not a copy of global rules. Write the project-specific engineering quick-reference into `docs/agents/coding-standards.md` (see [REFERENCE.md](REFERENCE.md) Step 6). When multiple agents are used, include `ai-collaboration.md` from its template and fill in the actual agent roles, tracker, and handoff path. If the project opted into the WeChat entry (Section H), keep the WeChat sections in that file, fill the project facts, and print the registry entry block for the user to paste into `~/.dsh/im/PROJECTS.md`; if not, drop those sections so the project runs standalone. When writing `domain.md`, scan `docs/prd/`, `docs/adr/`, `docs/research/` first and use actual filenames in the file tree, not template placeholders (see REFERENCE.md domain.md template note). Always write `project-state.md`, `project-decisions.md` and `verification.md` from actual confirmed project facts; never leave example placeholders (an empty decisions or verification section reads as "none recorded", not as a blank template) and never record unverified claims as current facts. For `project-state.md`, replace `<PRD-NNNN>` with the active PRD or `No active PRD`; when there is no active batch, mark the remaining stage rows `N/A` rather than leaving template text. Record actual compile commands in `project-state.md`; no delivery-profile selection is needed. Update in-place, never append duplicates.

**Step 7: Done** — list skills now configured, suggest next step

See [REFERENCE.md](REFERENCE.md) for seed templates and detailed steps.

## Gotchas

| What happened | Rule |
|---|---|
| Assumed GitHub without checking remote | Step 1: Run `git remote -v` first |
| Missed monorepo/multi-repo structure | Step 2: Check for workspace files, subprojects, sibling repos |
| Monorepo: only configured root, missed packages | Step 6: Create per-package `docs/agents/` dirs in monorepo |
| Multi-repo: no coordination between repos | Step 6: Create `repo-map.md` linking repos to skill domains |
| Asked all decisions at once | Step 3-4: present detected defaults first, then ask for overrides one section at a time |
| Created AGENTS.md when neither file existed | Global-first default / Step 6: skip it; project facts belong in `docs/agents/` |
| Copied global workflow or Working principles into a project file | Global-first default: keep the global instructions as the single source; write only project-specific facts or a short pointer |
| Duplicated an existing `## Agent skills` block | Step 6: update the existing pointer in place, don't append |
| Template principles copied wholesale into a single-stack repo | Step 4E: tailor to the detected stack — drop <Backend>/<Frontend>/<Multi-tenant> blocks that don't apply, confirm scope with the user |
| Quick-reference commands invented instead of read from the repo | Step 4E: fill from package.json scripts / Makefile / CI config; drop rows with no real command |
| Gitee remote treated as GitHub / GitLab | Use the Gitee template and connected MCP or OpenAPI; preserve string Issue numbers |
| Standards not re-read before each check | Entry Protocol Step 1a: reload the selected profile and scoped standards before a compliance verdict |
| Profile selected by probing framework signatures | Section F: default to `ruoyi-plus-dev`; do not probe signatures or ask whether the project is RuoYi. Record a user-confirmed non-RuoYi choice as an explicit project override (`none` or a named profile) |
| Confirmed profile registered as a bare name only | Section F: also carry the profile's hard constraints into the project config so they are visible without loading the profile |
| Overwrote the user's hand-written principles section | Step 4E: if a project-specific principles section already exists, ask adopt/merge/replace — never silently overwrite |
| Wrote files without user confirmation | Step 5: Show full draft before writing |
| Re-run: overwrote unchanged sections / missed drift | Step 1-2: Read existing config, compare structure against `repo-map.md`, only update what changed |
| Re-run: language change undetected / per-package out of sync | Step 4D / Step 6: Compare existing config against current state on re-run |
| Re-run: domain.md shows template examples, not actual files | Step 6: scan `docs/prd/` `docs/adr/` `docs/research/` for real filenames before writing domain.md |
| Re-run: renamed PRDs not updated in referencing files | After renaming, scan `docs/adr/` and `CONTEXT.md` for references to old name; suggest update |
| Re-run: language change didn't reach existing docs | Language Audit: flag files in wrong language; recommend manual translation or an installed writing skill — don't auto-translate |
| Re-run: format drift not detected | Format Audit: compare each file's section structure against its FORMAT spec |
| Migration: orphaned files after structure change (e.g. single→monorepo) | Step 2: Detect drift, present migration path, clean up with confirmation |
| Wrote the machine-level WeChat index from a project skill | Step 6 / Section H: output the registry entry for the user to paste; `~/.dsh/im/PROJECTS.md` is global and out of a per-repo skill's scope |
| WeChat sections written into projects that do not use the entry | Section H defaults off — drop the WeChat sections so the project runs standalone |

## Output

**First run:**
```
Setup complete.

Configuration:
- Project structure: <single / monorepo / multi-repo>
- Issue tracker: <GitHub / GitLab / Gitee / Local / Other>
- Coding standards: <existing conventions / selected profile / none>
- Triage labels: <defaults / customised>
- Domain docs: <single-context / multi-context>
- Documentation language: <English / Chinese / Other>
- WeChat entry: <on — registry entry printed for ~/.dsh/im/PROJECTS.md / off (standalone)>

Updated files:
- AGENTS.md/CLAUDE.md — not created by default; if the file already existed or was requested, updated with a short ## Project context pointer
- docs/agents/issue-tracker.md — created
- docs/agents/triage-labels.md — created
- docs/agents/domain.md — created
- docs/agents/language.md — created
- docs/agents/coding-standards.md — created/updated (project principles and verification quick reference)
- docs/agents/repo-map.md — created (multi-repo only)
- docs/agents/ai-collaboration.md — created/updated (WeChat sections only when the entry is on)
- docs/agents/project-state.md — created (current objective, workflow-stage dashboard, blockers, next step, compile commands)
- docs/agents/project-decisions.md — created (or "no decisions recorded yet")
- docs/agents/verification.md — created (or "no verification recorded yet")

Skills now configured: setup-project, think, research, grill, story, implement, page-acceptance, review, debug, project-context, scm-collaboration, frontend-design, ruoyi-plus-dev, rules, engineering-workflow

Next: Start using skills. Run /think to brainstorm a feature, /research for technical investigation, or /debug to investigate a bug.
```

**Re-run (config update):**
```
Config updated.

Changes:
- <what changed, e.g., "Switched issue tracker from GitHub to GitLab">
- <what changed, e.g., "Language changed from Chinese to English">

Updated files:
- docs/agents/<file>.md — updated (changed: <sections>)
- <... other files ...>

Conformance sweep:
- ✅ Naming: all files conform
- ⚠️ Language: 1 file in wrong language (manual translation or installed writing skill)
- ✅ Format: all files comply

Done with 1 finding, 0 fixed (requires manual translation or an installed writing skill).

Next: Re-run affected skills if config change affects their behavior (e.g., after language change, update flagged docs with an installed writing skill).
```
