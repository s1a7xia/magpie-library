---
name: scm-collaboration
description: 以统一流程协作 GitHub、GitLab、Gitee 或本地任务跟踪：识别当前仓库与平台适配器，关联需求、分支、提交、验证证据和 Issue/PR/MR。仅在需要读写远端任务单或合并请求时触发；本地提交与推送走常规 Git 流程，不经过本技能。不假设远程写入已授权或平台 API 已接通。
---

# SCM Collaboration

**Trigger boundary.** This skill handles the remote task layer: creating or reading Issues, opening PR/MR, syncing status, linking commits to work items. Local commits and pushes on an existing branch do not go through it — those follow the normal Git workflow in `engineering-workflow`.

Keep one collaboration flow across code-hosting platforms. Git operations and
task semantics are shared; only the remote transport is platform-specific.

```text
requirement / issue
  → acceptance criteria
  → local branch and scoped changes
  → verification evidence
  → local commit
  → authorized issue / PR / MR update
  → project state
```

## Resolve the Actual Adapter

1. Read applicable `AGENTS.md`/`CLAUDE.md` and
   `docs/agents/issue-tracker.md` when present.
2. When the task crosses Codex and dsh, also read
   `docs/agents/ai-collaboration.md` and follow the configured role/write
   boundaries.
3. Inspect `git remote -v`; select the configured remote rather than guessing
   from repository names or mirrors.
4. Treat GitHub, GitLab, Gitee, and local Markdown as transport adapters:
   preserve their identifiers and URLs exactly, especially Gitee Issue numbers.
5. Before any remote write, read the current Issue/PR/MR or repository and
   verify access. A connected MCP, installed CLI, or saved credential is not
   authorization to write.

If the configured platform lacks an authenticated adapter, continue with local
Git work when authorized and report the remote publication as pending. Do not
silently change the tracker.

## Shared Work Contract

When work starts from an Issue, use its current description, comments, labels,
and acceptance criteria as task input. When work starts from a direct request,
do not force an Issue unless the user wants tracking.

For every tracked change, keep these facts aligned:

- requirement or ticket identifier;
- affected repository and branch;
- local commit(s);
- checks actually run and their results;
- remote status only after the remote action succeeds.

Record these in existing project context files only when the project uses them.
Never claim a PR/MR was created, commented on, or merged based on a local
commit alone.

## Adapter Boundaries

Current adapters in this library (verified 2026-11-06):

| Platform | Read/write path |
|---|---|
| GitHub | GitHub MCP (`github`) exposed through the Magpie hub; `gh` as fallback. |
| Gitee | Official Gitee MCP (`gitee`, `https://api.gitee.com/mcp`, bearer token held by Magpie). Fallback: Gitee OpenAPI v5 with `GITEE_ACCESS_TOKEN` from the environment. |
| GitLab | `glab` CLI (`C:\Users\s1a71\AppData\Local\Programs\glab\glab.exe`, on PATH). Not an MCP on purpose: `glab mcp serve` exposes ~220 tools and 360k characters of schemas, which crowds out the rest of the context. |
| Local | Use the repository's configured Markdown tracker; no remote status is implied. |

All three remote adapters share one task flow; only the transport differs.
`gh` is not a GitLab adapter and `glab` is not a Gitee adapter.

Before the first GitLab operation on a host, confirm `glab auth status` succeeds
for that host. If it does not, run `glab auth login --hostname <host>` once and
retry; a pending sign-in is a blocker to remote actions, not to local Git work.
Pass long bodies from a UTF-8 file or stdin, never through shell interpolation.

Local Git remains the common layer. `git status`, diff, branches and commits
can be handled uniformly, but push, Issue, PR/MR, comments, labels and merge
actions stay explicitly authorized remote operations.

## Inbox Requirement Publishing

For a registered project with a normal feature branch and existing upstream,
`scripts/publish-wechat-requirement.ps1` takes a draft directory containing
`需求.md` and optional `assets/`, then publishes one WeChat requirement through
`scripts/publish-inbox.ps1` without touching other worktree or staged changes.
The low-level publisher creates
`docs/inbox/<REQ-YYYYMMDD-NNN>/需求.md`, copies received attachments under
`assets/`, rejects credential-like content and sensitive filenames, stages only
that requirement directory, scans the staged diff, commits with
`git commit --only`, pushes the current upstream, and verifies HEAD equals
`@{u}`.

`scripts/publish-wechat-research.ps1` uses the same publisher with
`-Kind research` for a bounded WeChat `调研：` brief. It creates
`docs/research/inbox/<RES-YYYYMMDD-NNN>/调研简报.md` plus optional `assets/`,
and applies the same branch, upstream, isolation, sensitive-content, commit, and
push checks. This inbox is unverified input for Codex; it is not a formal
`docs/research/<stack>-<topic>-<major>.md` record and never updates INDEX.

After a successful publish the wrapper removes the local draft unless
`-KeepDraft` is set. A failed publish preserves the draft for correction.
If `push` fails after the commit, the publisher returns `Status=COMMITTED`
with `Push=FAILED` and keeps the draft; that is "committed, not pushed", never
"remote visible". Re-running after the remote recovers pushes the pending
requirement commits. `-NoPush` returns `Push=NOT_PUSHED` and also keeps the draft.

It refuses detached HEAD, default/protected branches, missing upstream, an
incomplete remote configuration, a branch behind its upstream, and unpushed
commits that touch anything outside the selected publishing root
(`docs/inbox/` or `docs/research/inbox/`), so business commits are never pushed
together with an inbox item; a retry can still push an earlier inbox commit
whose push failed. It also refuses symlinked or duplicate attachments and a
repository root mismatch. It does not fetch/rebase, modify business files,
write project status, or create Issues. If the project is not registered or
the branch/upstream is unsuitable, keep an explicit local draft and report it
as not published; never bypass the script with whole-repository staging.
