---
name: to-spec
description: "Turn the current conversation into a project spec: no interview, just synthesis of what has already been agreed. Use when a design is settled enough to record before task slicing."
---

This skill takes the current conversation context and codebase understanding and produces a spec. Do NOT interview the user; just synthesize what you already know.

The issue tracker and project state path should have been provided by the project's `AGENTS.md`. If not, use `setup-matt-pocock-skills`.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching.

2. Identify the seams through which this feature will be verified. Prefer existing seams over new ones and use the highest practical seam. Testing is optional: include test seams only when the user explicitly requested tests. Without that request, describe observable acceptance evidence instead.

Check with the user that these seams match their expectations.

3. Before writing a spec that persists business data, settle the data contract with `database-design`: reuse conclusion, persisted object and row identity, ownership, relationships, state/lifecycle, uniqueness, deletion/history, query/index basis, and migration. A settled contract is not approval to create tables or run DDL.

4. Write the spec using the template below, then publish it to the project issue tracker. On a local Markdown tracker, use `Status: ready`. Do not apply a triage label.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

This list of user stories should be extremely extensive and cover all aspects of the feature.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Data contract: reuse conclusion, persisted objects and row identity, relationships, state/lifecycle, uniqueness, deletion/history, query/index basis, and migration intent
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.

## Verification Decisions

How the accepted behavior will be observed. Include tests only when the user explicitly authorized them; otherwise record the smallest usable acceptance evidence and any verification limits.

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>
