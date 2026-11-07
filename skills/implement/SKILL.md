---
name: implement
description: "Use only when the user explicitly invokes implement for a PRD or set of issues. It orchestrates per-seam implementation, authorized verification, review recommendation, and commits. Do not trigger from words like 实现/开发/开始写代码; the main agent handles those directly under the shared compile-only default."
---

# Implement: Workflow Orchestration

当前资源库检查规则优先：默认只检查本次改动涉及的前后端能否编译，不再选择交付档位或重复询问验证授权。前后端均有改动时分别编译；仅改一端时只编译该端，纯文档或不影响编译的配置改动只核对差异。复用项目已有编译/构建命令，跳过测试，不独立运行 lint、类型检查或自动化测试；UI 可见改动另按 `page-acceptance` 走页面验收（见 Step 3.5）；已有构建命令内置的编译类型检查可保留。用户明确要求额外检查或暂不编译时按当次要求执行。编译失败或环境缺失时如实报告，不把编译通过等同于功能验收。测试编写、独立类型检查或全量测试步骤只有用户明确要求时才执行；不再要求选择项目交付档位。


🥷 Implement from PRD or issues — orchestrate authorized implementation, checks, review, and commits.

Sequences the implementation pipeline for a set of pre-agreed vertical slices: implement each seam directly, compile affected sides by default; run extra checks only when explicitly requested, recommend review, and commit per completed item when local commit authorization applies.

## Outcome Contract

- **Outcome**: All items from the PRD's acceptance criteria or child issues are implemented, with authorized checks and review handled under the current request.
- **Done when**: Each seam is complete against its acceptance criteria, authorized checks pass, review is recommended, and authorized commits exist.
- **Evidence**: Authorized typecheck/test results, diff analysis, review outcome or explicitly deferred review, and commit hashes when committed.
- **Output**: Summary of implemented items, authorized checks actually run, commits or uncommitted reason, next step.

## Process Summary

**Step 0 — Quick assessment.** If the work is trivial (single file, one obvious change), recommend direct implementation and stop — this skill is unnecessary overhead.

**Step 1 — Entry Protocol.** Apply the [Skill Entry Protocol](../rules/entry-protocol.md). Read project config (`docs/agents/`), domain docs (CONTEXT.md, ADRs, research INDEX), and the input work items (PRD or Issues from `/story`). Check upstream quality: if PRD Traceability shows `Created by: /story (minimal PRD)`, note that requirements may not be decision-complete; if `Grilled by` is empty, note the plan is unvalidated.

**Step 2 — Work Inventory.** List all items to implement:
- If Issues from `/story` exist — each issue is a seam
- If only a PRD — extract Acceptance Criteria as work items
- Sort by dependency order (blocked-by relationships from `/story`)
- Update PRD Status from `Sliced` to `In Progress` in the PRD's status line

**Step 3 — Implement each seam.** For each work item in dependency order:

1. **Read the seam's acceptance criteria** — from the PRD or the issue it came from; confirm they are clear before writing code.
2. **Implement directly** — write the smallest change that satisfies them; apply [engineering principles](../rules/engineering-principles.md) design-time. Write tests only when the current request explicitly asks for test work.
3. **Typecheck** — compile the affected frontend/backend; run a separate typechecker only when explicitly requested. If it fails, fix before proceeding.
4. **Check** — run authorized checks for this item / changed files. Record checks not authorized as not run.
5. **Page acceptance** — when this item changes something visible in the UI, run [page-acceptance](../page-acceptance/SKILL.md) for the main path and one boundary; report the runtime layer separately from compilation. Skip it for non-UI changes and say so.
6. **Commit** — commit with a descriptive message referencing the issue (format: `[PRD-NNNN] <seam description> — <summary>`) only when local commit authorization applies; otherwise leave the changes and report why.

Update the issue's status in the PRD's `Sliced into` list to `— Done`.

**Step 4 — Authorized full check.** After all items are implemented, compile affected sides; run the full suite or other extra checks only when explicitly requested. If an authorized check fails, return to the affected item and fix. Record unauthorized or unavailable checks as not run.

**Step 5 — Recommend /review.** Present the completed changes and instruct: "Next: Run `/review` to review all changes before merge."

**Step 6 — Output.** Produce summary of implemented items, commits made or omitted, and the checks actually run.

See [REFERENCE.md](REFERENCE.md) for detailed step instructions, implementation guidelines, and recovery procedures.

## Gotchas

| What happened | Rule |
|---|---|
| A seam started before its acceptance criteria were clear | Step 3.1: read and confirm the acceptance criteria first |
| Checks were batched until after every seam | Step 3.4: run the authorized checks per item, not once at the end |
| Typechecker not configured for the project | Step 3.3: detect typechecker from project config (tsconfig, pyproject.toml, etc.); if none, skip and note the gap |
| Work items had hidden dependency on incomplete items | Step 2: read blocked-by relationships from `/story` issues; implement in dependency order |
| Commit conflicts with uncommitted work not from this session | Step 3.6: warn user about existing dirty state; ask how to handle before committing |
| PRD Traceability shows ungrilled or unsliced state | Step 1: flag the gap in output but proceed — implement is not blocked by missing upstream steps |
| UI change compiled but was never opened | Step 6: run `page-acceptance`; compilation is not evidence about a rendered page (anti-pattern #17) |
| User expected /review to run automatically | Step 5: recommend the review skill; do not auto-run it |

## Output

```
Implement complete.

**Work items:**
* <issue-#N / PRD acceptance criterion> — direct — commit <hash or uncommitted reason>
* <issue-#M / PRD acceptance criterion> — direct — commit <hash>

**PRD**: PRD-NNNN — Status: In Progress

**Checks**: <pass / N failures / not run with reason>

**Next**: Run /review to review all changes before merge.
```
