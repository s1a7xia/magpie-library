# Research INDEX Format

## 用途

研究知识库的可选索引与入口文件。位于 `docs/research/INDEX.md`。已有索引时先查匹配记录并复用 TL;DR；只有当结论需要跨任务复用或用户要求时，才持久化新记录并更新索引。

## 文件位置

`docs/research/INDEX.md`

**Lazy creation**: created only when the first durable research record is requested or justified; never scaffolded as an empty file.

## 双视图结构

INDEX provides two views over **the same set of records**, serving two query types:

1. **By Stack** — grouped per stack; answers "what research exists for this stack". One row per record.
2. **By Topic** — cross-stack comparison; answers "how does this topic behave across different stacks". Multiple stacks of the same topic listed side by side.

Both views point to the same `<stack>-<topic>-<major>.md` files; content is not duplicated.

## 模板

```markdown
# Research Index

> Entry point for every research record. Query here first; reuse the TL;DR on a hit, start new research only on a miss.
> Status values: verified (validated) | stale (current project major is higher; suggest re-research) | deprecated (abandoned).

## By Stack

### react

| Topic | Major | Version | Verdict | File | Status |
|---|---|---|---|---|---|
| concurrent-rendering | 18 | react@18.2.0 | useTransition is enough; do not build a custom scheduler | [react-concurrent-rendering-18.md](react-concurrent-rendering-18.md) | verified |
| suspense-data-fetching | 18 | react@18.2.0 → 19 | Many edge cases; consider wrapping with React Query | [react-suspense-data-fetching-18.md](react-suspense-data-fetching-18.md) | stale |

### postgres

| Topic | Major | Version | Verdict | File | Status |
|---|---|---|---|---|---|
| index-strategy | 15 | postgres@15.4 | Partial indexes + BRIN save 60% space vs B-tree | [postgres-index-strategy-15.md](postgres-index-strategy-15.md) | verified |

## By Topic

> Cross-stack comparison of the same topic. Single-stack topics are kept too (listed when ≥1), so a future new stack immediately sees the existing baseline.

| Topic | Stacks | See |
|---|---|---|
| concurrent-rendering | react@18 | [react-concurrent-rendering-18.md](react-concurrent-rendering-18.md) |
| data-fetching | react@18 | [react-suspense-data-fetching-18.md](react-suspense-data-fetching-18.md) |
| index-strategy | postgres@15 | [postgres-index-strategy-15.md](postgres-index-strategy-15.md) |
```

## 字段说明

| Field | Description |
|---|---|
| Topic | Research slug (kebab-case), without the stack prefix |
| Major | Major version number, matching the filename suffix |
| Version | Version column. **verified/deprecated rows**: a single studied version (e.g. `react@18.2.0`). **stale rows**: `studied-version → current-major` (e.g. `react@18.2.0 → 19`), showing version drift at a glance |
| Verdict | A one-line conclusion; a further distillation of the record file's TL;DR |
| File | Relative link to the record file |
| Status | **Fixed plain-text enum**: `verified \| stale \| deprecated`. **Carries no data, no emoji** (mirrors PRD's `Status: Draft` and ADR's `Status: Accepted` conventions) |

## Status 字段规则（强制）

**The Status column is always a pure enum token and carries no data.** All version information belongs in the Version column.

| Status | When set | Set by |
|---|---|---|
| `verified` | When a durable research record is written | `research` stage |
| `stale` | When a loaded stage reading the index finds the project's relevant major is higher than the record's major | The stage using the index — collaborative marking |
| `deprecated` | When the conclusion is overturned or the stack is abandoned | Explicit human marking |

### Full format of a stale row

When a row is marked stale, **edit both fields** (never embed data in Status):

- `Status` column → `stale` (pure token, no data)
- `Version` column → change from a single value to `studied-version → current-major`

Example:
```
| suspense-data-fetching | 18 | react@18.2.0 → 19 | Many edge cases... | react-suspense-data-fetching-18.md | stale |
```

The re-research hint is written at the end of the verdict or in a note below the table: `→ re-research react suspense-data-fetching-19 when requested`. **Do not auto-trigger re-research.**

## By Topic 视图规则

- **Single-stack topics are listed too** (listed when ≥1 stack has researched it). Value: when a future new stack researches the same topic, the existing baseline is immediately visible.
- **Topics with 0 stacks researched do not appear** (no record to index).
- `Stacks` column format: `<stack>@<major>`, multiple stacks space-separated: `react@18 vue3@3`.

## 更新规则

1. **Immediate update** — the `research` stage updates both INDEX views when it produces a new durable record.
2. **Collaborative stale marking** — a stage already reading the index can mark a relevant stale row when it detects a version mismatch.
3. **Do not delete stale rows** — stale records have historical value (immutability principle, ADR-0004); keep and mark them.
4. **Re-research produces a new row** — when the current request asks for research on a new major, create a new record file and row; keep the old stale row.

## 反模式

| Anti-pattern | Correct approach |
|---|---|
| Status column carries data (e.g. `stale (v19)`) | Status is a pure enum; version info belongs in the Version column |
| Using emoji for status (check/warning/cross symbols) | Plain-text enum (verified/stale/deprecated), mirroring PRD/ADR conventions |
| Deleting the old record on a stale row | Keep and mark stale (immutability, ADR-0004) |
| By Topic lists only topics with ≥2 stacks | Single-stack topics are listed too, preserving the comparison baseline |
| INDEX scaffolded empty ahead of time | Created only when the first record is produced |
