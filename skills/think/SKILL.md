---
name: think
description: "Clarify requirements and converge on a decision-complete plan. Use when requirements are unclear, multiple implementation paths exist, or a feature or architecture decision needs design. Do not require or automatically create a PRD; persist only in an existing project record or when the user asks for one. Trigger words: brainstorm, 构思, plan, how should I, design approach, feasibility, 技术方案."
---

# Think: Brainstorm and Solution Convergence

🥷 Think before you code.

Transform rough ideas into decision-complete plans. Ask one question at a time, each with your recommended answer. Do not write code, generate scaffolds, or write pseudocode until the user explicitly starts an implementation workflow.

If a question can be answered by exploring the codebase or a quick research pass, do that instead of asking.

## Outcome Contract

- **Outcome**: A decision-complete plan that the current task can implement, optionally persisted in an existing project doc or a PRD
- **Done when**: The user approves the plan, or the current request explicitly asks only for analysis
- **Evidence**: The decisions and acceptance criteria in the conversation, an existing project document, or an approved PRD
- **Output**: Approved design summary; persistence and any next stage are optional

## Core Principles

1. **Task-first** — capture the idea immediately
2. **Action-before-asking** — derive from codebase/docs before asking. Apply the [Skill Entry Protocol](../rules/entry-protocol.md)
3. **Ask only outcome-changing decisions** — derive blocking facts from code or docs first. For a large ambiguous design, work one decision at a time with a recommended answer and let each answer reshape the next question; for ordinary focused work, resolve independent low-risk defaults and report them. Never attach an unrelated rider.
4. **Prefer concrete options** — present 2-3 viable approaches with trade-offs; never silently assume a single path (anti-pattern #28)
5. **Research-first** — query INDEX before proposing; study authoritative sources
6. **Diverge → Converge** — expand on edges, then converge to MVP

## Process Summary

**Step 0 — Quick assessment.** If the request is trivial (typo, single-line fix, one obvious approach), skip this skill and implement directly. Do not create a PRD.

**Step 1 — Auto-collect context.** Explore the codebase (affected modules, existing patterns, constraints) and docs (relevant requirements, README, ADRs) before asking anything. Write findings into the active plan record only if one is in use; otherwise keep them in the working summary.

**Step 2 — Decide whether a durable document is needed.** Reuse an existing project PRD or specification when one already owns this topic. Only ask about creating a new PRD when the task is large or cross-iteration enough that conversation alone would lose decisions. Never create one automatically. If the user declines, work conversationally and produce a summary at the end. When creating a new PRD: run the **PRD Conflict Check** (see REFERENCE.md §PRD Conflict Check) — compare the topic against existing PRDs by title slug and Goal; if a candidate collides, ask whether to resume it (reuse its NNNN) or create a new one with a distinct title. Only then assign next NNNN (max + 1, starting from 0000).

**Step 3 — Classify complexity.** Simple / Moderate / Complex (see REFERENCE.md). Depth of brainstorming scales with complexity.

**Step 4 — Gate your questions.** Only ask **Blocking** (can't continue without input) or **Preference** (multiple valid choices) questions. Derivable questions → inspect the code/research instead. Meta questions ("should I search?") → never ask, just act. If the user packs multiple requests, enumerate and address each one (anti-pattern #20).

**Step 5 — Research-first for technical choices.** When choosing an approach/library/framework:

1. **Check an existing research INDEX.** If `docs/research/INDEX.md` exists, look for matching stack + topic + major records:
   - **Hit (verified)** → read TL;DR only; reuse verdict. Don't read full record by default.
   - **Hit (stale)** → read the full record's `## Boundary Conditions` to decide if the old conclusion applies. If the current request needs new-major evidence, research it then.
   - **Hit but decision depends on implementation detail** → read full record's Findings/Code Snippet even if verified.
   - **Miss** → research inline with authoritative sources; persist a research record only when the conclusion is reusable or the current task asks for it.
2. **Only on a miss**, research 2-4 comparable patterns against **authoritative sources** (official docs/source/spec), map to codebase constraints, present 2-3 options with trade-offs, ask one preference question.
3. Cite reused research records in the active plan record's `## Research References` when that record exists; otherwise summarize the reuse in the conversation.

**Step 6 — Expansion scan (diverge).** Proactively raise 1-2 points each on future evolution, related scenarios, and failure/edge cases before converging. **Scale to complexity** (Step 3): Simple tasks skip this step; Moderate does failure/edge only; Complex does all three. Let the user pick what enters the MVP vs `Out of Scope`.

**Step 7 — Converge.** Ask only outcome-changing questions that cannot be derived. For a large ambiguous design, use one question at a time with a recommended answer; for ordinary focused work, resolve safe independent defaults and report them. Update the plan record only if one is in use. Continue until every decision affecting the current deliverable is resolved.

**Step 8 — Propose approaches + record decision.** When requirements are clear, present 2-3 approaches (if not already done via research), ask preference, and record the result in the active plan record's `Decision (ADR-lite)` section when one is in use; otherwise keep the decision in the approved design summary. If the options cannot be separated by reasoning or trade-offs alone, state what the smallest authorized prototype would test; create or run it only if the current request authorizes implementation and execution. Record the evidence in the decision.

**Step 9 — Submit plan for approval.** Present the complete requirements (Goal, Requirements, Acceptance Criteria, Definition of Done, Out of Scope, Technical Approach, implementation slices). The approval submission asks exactly one thing — approval. Optional process choices do not need to be settled before ordinary work. After approval, persist or finalize the plan if the task uses a document, then either continue within the authorized workflow or stop for review.

**Step 10 — Finalize the plan record.** After plan approval:
1. If an existing PRD or project specification is being used, finalize its requirements, acceptance criteria, traceability, and status. Do not create one merely to complete this stage.
2. If the project already has an issue tracker and the current request authorizes writing to it, create or update the relevant Issue; otherwise use the existing record or conversation and do not ask for a tracker.
3. Record new domain terms in the active plan record or approved summary; update a project glossary only when the project already maintains one.
4. Output the approved design summary. Do not require a review stage or issue creation to proceed.

See [REFERENCE.md](REFERENCE.md) for complexity classification detail, question-gate rules, and worked message formats. The PRD template and field rules live in [PRD-FORMAT.md](PRD-FORMAT.md) — that file is the single source.

## Gotchas

| What happened | Rule |
|---|---|
| Created a PRD nobody needed | Step 2: persist only when the task benefits from a durable record |
| Asked user about code/context that could be derived | Step 1: auto-collect context first |
| Had user choose approach before presenting options | Step 5: research-first for technical choices |
| Re-searched a topic a prior task already captured | Step 5: when `docs/research/INDEX.md` exists, query it first; reuse the TL;DR on a hit |
| Cited a blog/tutorial as the basis for a technical choice | Step 5: research against authoritative sources (official docs/source/spec) only |
| Asked meta questions like "should I search?" | Step 4: never ask; inspect the code or research |
| Drifted without updating an active plan record | Update only a record that is actually in use |
| Attached an unrelated rider sub-ask to a question | Keep one coherent decision per question |
| Stayed on initial request without considering edges | Step 6: expansion scan before converging |
| Domain terms introduced but lost after planning | Step 10: record them in the active plan record or approved summary; update a maintained glossary only when one exists |
| Same topic got two PRDs (e.g. PRD-0001 + PRD-0002) | Step 2: run PRD Conflict Check (REFERENCE.md) before assigning NNNN |
| Asked for or invented an Issue tracker when the project has none | Step 10: Issues are optional; use existing docs or conversation unless the project already has a tracker and the current request authorizes writing |

## Output

When the plan is approved, output:

```
Plan approved.

**Approved design summary:**
- **Building**: What this is (1 paragraph)
- **Not building**: Explicit exclusion list
- **Approach**: Chosen option + rationale
- **Key decisions**: 3-5 items with rationale
- **Unknowns**: Only explicitly deferred items with reason and owner
- **Record**: existing doc / PRD path / conversation only
```

Stop after output when the user asked only for requirements or design. Continue only when the current request authorizes implementation.
