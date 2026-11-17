# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root — domain glossary (core concepts, terminology, relationships)
- **`CONTEXT-MAP.md`** at the root if it exists — it points at one `CONTEXT.md` per context. Read each one relevant to the topic.
- **`docs/prd/`** — product requirements documents. Skills such as `review` read these for planned features and acceptance criteria.
- **`docs/adr/`** — architecture decision records. Read ADRs that touch the area you're about to work in. In multi-context repos, also check `src/<context>/docs/adr/` for context-scoped decisions.
- **`docs/research/INDEX.md`** — optional searchable index of persisted technical research records (stack × topic × major). The `think` stage checks it when it exists before re-searching; the `research` stage creates records here only when durable reuse is warranted.
- **Existing status record, otherwise `docs/project-state.md`** — optional live task state for large, multi-session, or multi-stage work. Reuse the existing record and fill its actual path here; reconcile code claims with Git before relying on them. Do not duplicate the task list.

If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The producer stages (`grill` for CONTEXT.md and ADRs, `think` or `story` for PRDs) create them lazily.

## What to do if files are missing

If `CONTEXT.md` doesn't exist yet, consumer stages should proceed without it. The first run of the `grill` stage will create it lazily. Do not create an empty `CONTEXT.md` during setup — an empty file is noise.

Same for `docs/prd/`, `docs/adr/`, `docs/research/`, and `docs/project-state.md` — create them only when there's actual content to write. A missing status document is not a setup defect; create it only for work that genuinely needs durable tracking.

## File structure

Single-context repo (most repos):

```
/
├── CONTEXT.md
├── docs/
│   ├── prd/
│   │   ├── PRD-0001-user-subscription.md
│   │   └── PRD-0002-payment-integration.md
│   ├── adr/
│   │   ├── 0001-event-sourced-orders.md
│   │   └── 0002-postgres-for-write-model.md
│   └── research/
│       ├── INDEX.md
│       ├── react-concurrent-rendering-18.md
│       └── postgres-index-strategy-15.md
└── src/
```

**File naming conventions** (producer skills define these; consumer skills read them):

- PRD: `PRD-NNNN-<title>.md` — see the dev-workflow `think` stage's `PRD-FORMAT.md`
- ADR: `<NNNN>-<title>.md` (no `ADR-` prefix) — see the dev-workflow `grill` stage's `ADR-FORMAT.md`
- Research: `<stack>-<topic>-<major>.md` — see the dev-workflow `research` stage's `RESEARCH-FORMAT.md`

Multi-context repo (presence of `CONTEXT-MAP.md` at the root):

```
/
├── CONTEXT-MAP.md
├── docs/
│   ├── prd/                           ← shared PRDs
│   └── adr/                           ← system-wide decisions
└── src/
    ├── ordering/
    │   ├── CONTEXT.md
    │   └── docs/adr/                  ← context-specific decisions
    └── billing/
        ├── CONTEXT.md
        └── docs/adr/
```

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal — either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for the `grill` stage).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0007 (event-sourced orders) — but worth reopening because…_
