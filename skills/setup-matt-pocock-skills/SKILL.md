---
name: setup-matt-pocock-skills
description: "Initialize a Codex project once: configure its issue tracker, domain docs, AGENTS.md entry, and project state document when needed. Use only when the user explicitly asks to initialize or configure a project."
---

# Setup Matt Pocock's Skills

Scaffold the per-repo configuration that the Codex engineering skills assume:

- **Issue tracker**: where issues live (local markdown by default; GitHub and GitLab are available when the project already uses them)
- **Project state**: the single current-state document used to resume work across sessions
- **Domain docs**: where `GLOSSARY.md` and ADRs live, and the consumer rules for reading them

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

## Process

### 1. Explore

Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- `git remote -v` and `.git/config`: is this a GitHub repo? Which one?
- `AGENTS.md` at the repo root: does it exist? Is there already an `## Agent skills` section?
- `GLOSSARY.md` and `GLOSSARY-MAP.md` at the repo root, and the legacy `CONTEXT.md` / `CONTEXT-MAP.md`. If a legacy file exists, offer to `git mv` it to its `GLOSSARY` name and rewrite those names in `docs/agents/domain.md`.
- `docs/adr/` and any `src/*/docs/adr/` directories
- `docs/agents/`: does this skill's prior output already exist?
- Existing project state documents: check `docs/project-state.md`, `docs/status.md`, `docs/progress.md`, a project task board, or a path already named in `AGENTS.md`. Reuse what exists rather than creating a second status source.
- `.scratch/`: a sign that a local-markdown issue tracker convention is already in use
- Monorepo signals: a `pnpm-workspace.yaml`, a `workspaces` field in `package.json`, or a populated `packages/*` with its own `src/`. These are present only in a genuinely large multi-package repo; their absence means single-context, which is almost every repo.

### 2. Present findings and ask

Summarise what's present and what's missing. Then take the sections in order. One section, one answer, then the next.

Lead each section with the recommended answer so the user can accept it in a word. Give a one-line explainer only when the choice genuinely branches; skip the section entirely when exploration already settled it (Section B when there's no monorepo).

**Section A: Issue tracker.**

> Explainer: The "issue tracker" is where specs and implementation tickets live for this repo. `to-spec` and `to-tickets` read from and write to it. Pick the place you actually track work for this repo.

Default posture: use **Local markdown** for Codex-led projects unless the repository already uses GitHub or GitLab issues. This keeps specification and task state inside the project and removes an external dependency from the normal development loop.

- **GitHub**: issues live in the repo's GitHub Issues (uses the `gh` CLI)
- **GitLab**: issues live in the repo's GitLab Issues (uses the [`glab`](https://gitlab.com/gitlab-org/cli) CLI)
- **Local markdown**: issues live as files under `.scratch/<feature>/` in this repo (good for solo projects or repos without a remote)
- **Other** (Jira, Linear, etc.): ask the user to describe the workflow in one paragraph; the skill will record it as freeform prose

Record the choice in `docs/agents/issue-tracker.md`. Do not create triage labels or ask about a triage vocabulary: the `triage` skill is not part of this Codex setup.

A GitHub or GitLab tracker needs a reachable repo. When the user picks one and no `git remote` points at that host, get the repo URL from them and wire it up (`git init` if needed, `git remote add origin <url>`) before going further. Done when `gh repo view` / `glab repo view` prints the project from inside this directory; if it can't, stop and tell the user what's missing.

**Section B: Domain docs.** Default to **single-context** (one `GLOSSARY.md` + `docs/adr/` at the repo root). This fits almost every repo; write it without asking.

Offer **multi-context** (a root `GLOSSARY-MAP.md` pointing to per-context `GLOSSARY.md` files) only when exploration found monorepo signals. Then confirm which layout they want.

**Section C: Project state.** Reuse an existing status source when one was found. Otherwise create `docs/project-state.md` from [templates/project-state-document.md](./templates/project-state-document.md) when the project is large, multi-phase, or expected to span multiple sessions. Skip it for a small one-session project. This document is the task-state source for continuing work; Git remains the code-state source.

Do not create a second state document when a project task board, PRD status section, or other current-state file already exists. Record the chosen path in `AGENTS.md`.

### 3. Confirm and edit

Show the user a draft of:

- The `## Agent skills` block to add to `AGENTS.md` (see step 4)
- The contents of `docs/agents/issue-tracker.md`, `docs/agents/domain.md`, and, when Section C applies, the project state document (or the reused state path)

Let them edit before writing.

### 4. Write

**Pick the file to edit:**

- Always use the repository-root `AGENTS.md`.
- If it does not exist, create it.
- Never put Codex engineering configuration in `CLAUDE.md`.

If an `## Agent skills` block already exists in the chosen file, update its contents in-place rather than appending a duplicate. Don't overwrite user edits to the surrounding sections.

The block:

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Domain docs

[one-line summary of layout: "single-context" or "multi-context"]. See `docs/agents/domain.md`.

### Project state

[path to the current-state document, only when Section C applies; otherwise omit this section]. Update it when the current phase, completed work, next action, remaining work, blockers, or acceptance state changes.
```

Then write the docs files using the seed templates in this skill folder as a starting point:

- [issue-tracker-github.md](./issue-tracker-github.md): GitHub issue tracker
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md): GitLab issue tracker
- [issue-tracker-local.md](./issue-tracker-local.md): local-markdown issue tracker
- [domain.md](./domain.md): domain doc consumer rules + layout
- [templates/project-state-document.md](./templates/project-state-document.md): current project state

For "other" issue trackers, write `docs/agents/issue-tracker.md` from scratch using the user's description.

The original `triage-labels.md` is not installed into a project because this Codex setup has no `triage` skill. Local ticket state uses the four values documented in `issue-tracker-local.md`.

### 5. Done

Tell the user the setup is complete and which engineering skills will now read from these files. Mention they can edit `docs/agents/*.md` and the project state document directly later; re-running this skill is only necessary if they want to switch issue trackers or restart from scratch.
