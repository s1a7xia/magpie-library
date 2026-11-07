---
name: project-context
description: 维护跨会话的项目状态、已确认决策、编译及其他明确要求的验证证据。用于初始化项目协作上下文、继续旧任务、交接或用户要求让 AI 记住项目；不替代业务需求、代码阅读或原始会话历史。
---

# Project Context

Use a small, Git-tracked operational context for a project. Its purpose is to
make a later session recover the current facts without turning chat history
into an uncurated knowledge base.

## Read Before Work

At the repository root, inspect these files when they exist:

| File | Read it for | Do not use it for |
|---|---|---|
| `docs/agents/project-state.md` | active objective, current work, blockers, next step, compile commands and scope | permanent architectural rationale |
| `docs/agents/project-decisions.md` | confirmed cross-task decisions and their scope | transient implementation notes or unresolved options |
| `docs/agents/verification.md` | versioned validation evidence and known gaps | proof that later changes still pass |

Current user instructions and applicable `AGENTS.md`/`CLAUDE.md` override these
files. Inspect current code and Git state before trusting a recorded fact.

## Create or Refresh Context

Create the files only when the user asks to initialize/configure a project,
make the project reusable, or explicitly requests project memory. Use
`setup-project` for that broader setup; do not create documentation merely
because a small implementation task started.

Use the templates in [references/templates.md](references/templates.md).
默认检查方式：默认只检查本次改动涉及的前后端能否编译，不再选择交付档位或重复询问验证授权。前后端均有改动时分别编译；仅改一端时只编译该端，纯文档或不影响编译的配置改动只核对差异。复用项目已有编译/构建命令，跳过测试，不独立运行 lint、类型检查、自动化测试或页面快检；已有构建命令内置的编译类型检查可保留。用户明确要求额外检查或暂不编译时按当次要求执行。编译失败或环境缺失时如实报告，不把编译通过等同于功能验收。

## Keep It Useful

- Update `project-state.md` after a material task only when the files already
  exist or the user requested project context. Keep it short: current goal,
  completed work, active blockers, and one concrete next step.
- Add a decision only when it is confirmed, affects future tasks, and has a
  stated scope. Mark replaced choices as superseded rather than silently
  deleting their rationale.
- Record verification only with a version/commit or change scope, command or
  path, result, date, and source (`agent` or `user`). Record failures and
  unverified gaps honestly.
- Never place secrets, tokens, complete authentication headers, personal data,
  raw production exports, or large logs in these files.
- Do not duplicate requirements, ADRs, PRDs, or source documentation. Link to
  them when they are the source of truth.

## Handoff

For a handoff, update the state first, then report the same facts in a compact
form: active task, changed scope, evidence, blockers, and next step. A handoff
does not authorize a remote write, deployment, or database mutation.
