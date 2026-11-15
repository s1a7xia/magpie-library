---
name: grill
description: "Challenge and validate a requirement set or design plan, resolving the decisions that can change the result. Use when a plan needs a rigorous design check, terminology sharpening, edge-case confirmation, or trade-off validation. Work conversationally; maintain PRD, CONTEXT, or ADR records only when the project already uses them and the current task includes that record. Trigger words: challenge, 细化和验证, deep dive, question the plan, grill, validate plan, 这个方案行不行, 审查设计, find holes, stress test."
---

# Grill: Challenge Plans and Update Domain Knowledge

🥷 Challenge the plan before coding.

Challenge the plan until the decisions that affect the current deliverable are resolved. For each question, provide your recommended answer.

Finding facts is your job, never the user's: if the codebase or existing evidence can answer it, look it up instead of asking. Only decisions reach the user.

Ask only decisions that cannot be derived. For a large ambiguous plan, ask one decision at a time with a recommended answer and let each answer reshape the next question. For ordinary focused changes, resolve safe independent defaults and report them; do not manufacture an interview. Never attach an unrelated rider. Details: [REFERENCE.md §Question Pacing](REFERENCE.md).

## Outcome Contract

- **Outcome**: A validated plan or decision set that can be implemented, with affected terminology and trade-offs made explicit
- **Done when**: Every decision that can change the current deliverable is resolved or explicitly deferred with its impact
- **Evidence**: The validated decisions in the conversation, an existing project record, or an optional PRD/ADR when one is actually in use
- **Output**: Validated decisions and, only when an existing artifact is in scope, its synchronized record

## Before You Start

Apply the [Skill Entry Protocol](../rules/entry-protocol.md) selectively. Use an existing PRD, specification, or design summary when present; do not require one. If the available requirements are too thin to challenge, return to requirement clarification instead of inventing missing context.

## The Work

1. **Extract every unresolved decision that matters.** Read the available requirements or plan with hostile eyes: open questions, unvalidated assumptions, vague terms, unexplained scope boundaries, shaky technical approach, edge cases, and conflicts with an existing glossary. Do not invent missing requirements merely to fill a checklist.
2. **Work the checklist one question at a time.** Pick the highest-value unresolved item, ask it as a single question with your recommended answer, and wait. After the answer lands, update the tree — resolved items close, new findings may open children — and pick the next question from what the answer just made askable (see [REFERENCE.md §Question Pacing](REFERENCE.md)).
3. **Resolve as you go, not in a batch at the end.** Update files inline:
   - **Terminology resolved** → update a maintained project glossary now (glossary only, no implementation details); otherwise keep the definition in the validated decisions.
   - **Significant decision** → when the project already keeps ADRs, offer one if the three conditions in [ADR-FORMAT.md §创建条件](ADR-FORMAT.md) are all met. Otherwise record the decision and trade-off in the active plan record or validated summary, without creating project scaffolding.
   - **Code can answer it** → grep/read the code instead of asking the user.
   - **Only running a demo can answer it** (options that reasoning and reading can't separate — which is faster, does the model hold up, what should it look like) → park the item and state the smallest authorized prototype that would settle it; fold resulting evidence into the ADR / PRD before resuming.
4. **Run the exhaustiveness gate** before declaring complete: Open Questions, Assumptions, terms, scope, code cross-check — all resolved.
5. **Record validation in the artifact actually in use.** If a PRD or equivalent project record is in scope, fill its validation field. Otherwise the validated decision summary is sufficient.
6. **Update an existing tracked record only if relevant and authorized.** If the PRD already references an Issue and the current request authorizes tracker writes, synchronize its body with approved scope changes. A missing tracker or parent Issue is not an error; do not create or ask for one.

## What Goes Where

| Situation | Action |
|---|---|
| Goal statement itself needs to change, or fundamental approach invalidated | Return to requirement and solution convergence |
| Only terminology sharpened, scope confirmed, approach validated with refinements | The plan is ready for authorized implementation or optional work slicing |

For the challenge types (terminology conflict, fuzzy language, scope boundary, edge case, code cross-check), the file layout (single vs multi-context via `CONTEXT-MAP.md`), and a worked example, see [REFERENCE.md](REFERENCE.md).

## Gotchas

| What happened | Rule |
|---|---|
| Skipped an unresolved assumption | Extract every open item first, then resolve each |
| Updated CONTEXT.md in a batch at the end | Update inline, the moment each term resolves |
| Created an ADR for a trivial decision | Only when all 3 conditions met |
| ADR flipped at completion (declined inline, created at wrap-up — or vice versa) | Decide ADR eligibility once, inline, when the decision lands; record the failed condition when declining |
| CONTEXT.md gained implementation details | It is a glossary, nothing more |
| Asked the user something the code could answer | Explore the codebase instead |
| Shaped ordinary work into a long interview | Ask only outcome-changing decisions; resolve safe defaults yourself |
| Forced a decision that reasoning couldn't settle | Park the item and state the smallest authorized prototype that would settle it; fold the result into an ADR before resuming |
| Existing requirement record not updated after validation | Update the record actually in use; do not create a PRD to satisfy the stage |
| Declared complete with unresolved decisions that change the result | Confirm every relevant open question, assumption, scope boundary, and code claim is resolved or explicitly deferred |
| Parent Issue body stale after grill changed scope | Only when an existing tracker record is in scope and authorized: sync the referenced Issue; never create one to satisfy the process |

## Output

```
Grill complete.

Resolved <N> decisions:
- <term>: <resolution>
- <assumption>: <validated/converted>
- <decision>: <recorded in active plan/ADR | kept in validated summary>

Updated:
- existing requirement record — updated (if one was in use)
- maintained glossary — <count> terms sharpened/added (if one was in use)
- ADR record — created (only when the project already uses ADRs and warranted)

Decision check: complete for the current deliverable
Tracked record: #<num> synced | not used
```
