---
name: setup-project
description: "仅在用户明确要求初始化或调整项目级 AI 工程约定时，生成或更新 docs/agents 配置、可选 Issue tracker 约定、领域文档路径和工程原则。普通开发不需要先运行；缺少 docs/agents、tracker 或 PRD 不触发本技能。"
---

# Setup Project

🥷 Configure the repo so skills know where to read and write.

Create or update optional project-level configuration when the user explicitly asks for it:

- **Working principles** — a fixed first-principles reasoning prompt written verbatim into the `## Agent skills` rules block, so every agent session in the repo reasons from evidence
- **Engineering principles** — a stack-tailored `## Engineering principles` section in AGENTS.md/CLAUDE.md (design-first planning, module quality, boundaries, security, concurrency, UX, reuse, maintainability, reversibility) plus a change quick-reference mapping each kind of change to its verification commands
- **Project structure** — single repo, monorepo (multiple packages in one repo), or multi-repo (multiple related repos)
- **Issue tracker** — optional; where issues live if the project actually uses them (GitHub, GitLab, local markdown, or other)
- **Triage labels** — the strings used for the five canonical triage roles
- **Domain docs** — where `CONTEXT.md`, ADRs, PRDs, and the research index live; how consumer skills find them across repos
- **Documentation language** — the language skills should write human-facing output in (PRDs, ADRs, CONTEXT, Issues, comments), so output is readable for the team regardless of who triggers the skill

This is a prompt-driven skill, not a deterministic script. Explore only the repository facts relevant to the requested setup, present what you found, confirm, then write.

**Can be re-run.** If `docs/agents/` already exists, read the relevant current config first, detect what changed since last setup, present only sections that need updating, and rewrite affected files.

## Relationship to the Entry Protocol

This skill creates optional configuration that the [Skill Entry Protocol](../rules/entry-protocol.md) may read. Without it, consumer skills use relevant repository facts, existing docs, and reasonable defaults; missing configuration is not a defect.

| Config file | Entry Protocol Step | What it tells the consumer skill |
|---|---|---|
| `docs/agents/domain.md` | Step 1 | Actual paths for CONTEXT.md, PRDs, ADRs, and `docs/research/INDEX.md` |
| `docs/agents/issue-tracker.md` | Step 1 | Issue tracker type and CLI conventions |
| `docs/agents/triage-labels.md` | Step 1 | Label vocabulary mapping for the five canonical triage roles |
| `docs/agents/language.md` | Step 1 | Language for all human-facing prose (PRDs, ADRs, CONTEXT, Issues, comments) |
| `docs/agents/repo-map.md` | Step 2 (if exists) | Multi-repo structure — which repos exist, which owns the primary issue tracker |

This is not a normal development stage. Consumer skills remain usable without it; setup only improves explicit project conventions when those conventions are worth persisting.

## Outcome Contract

- **Outcome**: The project configuration the user explicitly requested — relevant `docs/agents/*.md` files and/or a tailored `## Agent skills` / `## Engineering principles` section. Tracker, triage, domain docs, and language files are created only when the project actually uses them. On re-run: conformance findings limited to the configuration being updated.
- **Done when**: User confirms the requested configuration, selected files are written, and AGENTS.md/CLAUDE.md is updated only when requested
- **Evidence**: The explicitly requested config files and/or principles updates; no placeholder tracker or domain files merely to complete setup
- **Output**: Summary of configuration, next step to use engineering skills

## Process Summary

**Step 1: Explore** — detect current repo state (remote, AGENTS.md, existing docs/agents/, workspace/monorepo structure) and stack signals for the principles tailoring (frontend/backend/DB, multi-tenant, verification scripts). If `docs/agents/` exists, read all current config files to understand existing setup.

**Step 2: Detect project structure** — single repo, monorepo, or multi-repo. Ask the user if detection is uncertain or if there are related repos not visible in this clone. If config already exists, compare detected structure against `repo-map.md` to find what changed.

**Step 3: Present findings** — show detected defaults (project structure, issue tracker, triage labels, domain layout, documentation language). If updating, show a diff of what changed vs current config.

**Step 4: Ask for overrides** — present only the configuration sections the user asked to create or change. Ask one section at a time. A tracker and triage labels are included only when the project actually uses Issues.

**Step 4a (Re-run only, affected records)** — Only when the requested config change affects existing records, inspect those records for relevant naming, language, format, or metadata drift. Report findings; rename or rewrite only with authorization. See [REFERENCE.md](REFERENCE.md) Conformance Sweep.

**Step 5: Confirm** — show the complete draft of all files to be written (AGENTS.md block + each `docs/agents/` file). If updating, show only files that changed.

**Step 6: Write** — write the `docs/agents/*.md` config files first, the AGENTS.md/CLAUDE.md sections last (an abort mid-way then leaves at most an unchanged AGENTS.md, never a block pointing at missing files): the `## Agent skills` block, then the tailored `## Engineering principles` section after it (see [REFERENCE.md](REFERENCE.md) Step 6). When writing `domain.md`, scan `docs/prd/`, `docs/adr/`, `docs/research/` first and use actual filenames in the file tree, not template placeholders (see REFERENCE.md domain.md template note). Update in-place, never append duplicates.

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
| Created AGENTS.md when CLAUDE.md (or neither) exists | Step 6: Edit the file that exists; don't silently default to AGENTS.md |
| Duplicated existing `## Agent skills` block | Step 6: Update in-place, don't append |
| Paraphrased or dropped the Working principles prompt | Step 6: Copy it verbatim — fixed text, not a per-repo template |
| Template principles copied wholesale into a single-stack repo | Step 4E: tailor to the detected stack — drop <Backend>/<Frontend>/<Multi-tenant> blocks that don't apply, confirm scope with the user |
| Quick-reference commands invented instead of read from the repo | Step 4E: fill from package.json scripts / Makefile / CI config; drop rows with no real command |
| Overwrote the user's hand-written principles section | Step 4E: if an `## Engineering principles` section already exists, ask adopt/merge/replace — never silently overwrite |
| Wrote files without user confirmation | Step 5: Show full draft before writing |
| Re-run: overwrote unchanged sections / missed drift | Step 1-2: Read existing config, compare structure against `repo-map.md`, only update what changed |
| Re-run: language change undetected / per-package out of sync | Step 4D / Step 6: Compare existing config against current state on re-run |
| Re-run: domain.md shows template examples, not actual files | Step 6: scan `docs/prd/` `docs/adr/` `docs/research/` for real filenames before writing domain.md |
| Re-run: renamed PRDs not updated in referencing files | After renaming, scan `docs/adr/` and `CONTEXT.md` for references to old name; suggest update |
| Re-run: language change didn't reach existing docs | Language Audit: flag files in wrong language — don't auto-translate |
| Re-run: format drift not detected | Format Audit: compare each file's section structure against its FORMAT spec |
| Migration: orphaned files after structure change (e.g. single→monorepo) | Step 2: Detect drift, present migration path, clean up with confirmation |

## Output

**Requested configuration:**
```
Setup complete.

Configuration:
- Project structure: <single / monorepo / multi-repo>
- Issue tracker: <configured, or omitted when the project does not use one>
- Domain docs: <configured paths, or omitted when not requested>
- Documentation language: <configured, or follow the user's current language>

Updated files:
- <only files actually requested and written>

Skills now configured: dev-workflow plus only the project-specific skills this setup actually needs

Next: continue normal development. `dev-workflow` routes stages internally; do not require manual stage commands.
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
- ⚠️ Language: 1 file in wrong language (manual update)
- ✅ Format: all files comply

Done with 1 finding, 0 fixed (manual update).

Next: Update any affected existing documents within the authorized scope.
```
