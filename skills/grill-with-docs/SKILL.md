---
name: grill-with-docs
description: Stress-test a plan or design through focused question rounds, recording durable decisions as ADRs and domain terms as they are resolved. Use before implementation when scope or design boundaries are still uncertain.
---

Run the methods in `grilling` and `domain-modeling` together:

- `grilling` drives the decision tree and asks one frontier round at a time.
- `domain-modeling` records a durable term or decision when it is actually settled.
- When the frontier reaches persisted business objects, ownership, identity, uniqueness, state, lifecycle, deletion/history, table relationships, or JSONB modeling, load `database-design` in that round and settle the data contract before the spec. Design-stage table approval is not execution approval.

Use the installed skill files directly; Codex has no separate "Skill tool". Keep fact-finding read-only and in the main context unless the user explicitly authorizes delegation.
