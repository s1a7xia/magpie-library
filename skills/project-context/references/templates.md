# Project Context Templates

Use these as concise starting points. Delete sections that do not apply; do
not leave placeholder values in a real project.

## `docs/agents/project-state.md`

```markdown
# Project State

## Compile checks

默认只编译受影响的前后端，不选择交付档位。记录实际命令和工作目录；没有的命令标为待确认。

- Backend: <actual compile command and directory, or not applicable>
- Frontend: <actual build command and directory, or not applicable>
- 不自动运行测试、lint、独立类型检查或页面快检；构建内置编译检查保留。

## Current objective

<one sentence>

## Active work

- <task or issue identifier>: <state>

## Blockers / risks

- <only current, material blockers>

## Next step

<one concrete next action>

## Updated

<YYYY-MM-DD — source: agent or user>
```

## `docs/agents/project-decisions.md`

```markdown
# Project Decisions

## Active decisions

### <short decision title>

- **Decision:** <what is settled>
- **Scope:** <modules / dates / users affected>
- **Why:** <concise rationale and source>
- **Recorded:** <YYYY-MM-DD>

## Superseded decisions

### <old decision title>

- **Replaced by:** <link or decision title>
- **Why changed:** <concise reason>
```

## `docs/agents/verification.md`

```markdown
# Verification Evidence

## Latest evidence

### <task or change title>

- **Change scope / commit:** <commit, branch, or precise changed area>
- **Date:** <YYYY-MM-DD>
- **Source:** agent | user
- **Checks:** <command, page path, API call, or inspection performed>
- **Result:** passed | failed | blocked | not run
- **Notes:** <only material limitation or evidence>

## Known gaps

- <what is still unverified and why>
```
