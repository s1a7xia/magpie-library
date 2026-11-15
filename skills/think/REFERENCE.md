# Think: Detailed Reference




## Contents

- [Step 0: Quick Assessment](#step-0-quick-assessment)
- [Step 1: Auto-Context Collection](#step-1-auto-context-collection)
- [Step 2: Decide Whether to Create a PRD](#step-2-decide-whether-to-create-a-prd)
- [Step 3: Classify Complexity](#step-3-classify-complexity)
- [Step 4: Question Gates (Only Ask High-Value Questions)](#step-4-question-gates-only-ask-high-value-questions)
- [Step 5: Research-First Mode (Technical Choices)](#step-5-research-first-mode-technical-choices)
- [Step 6: Expansion Scan (DIVERGE)](#step-6-expansion-scan-diverge)
- [Step 7: Converge](#step-7-converge)
- [Step 8: Propose Approaches + Record Decision](#step-8-propose-approaches-record-decision)
- [Step 9: Submit Plan for Approval](#step-9-submit-plan-for-approval)
- [Step 10: Optional Issue Sync and Finalize Plan Record](#step-10-optional-issue-sync-and-finalize-plan-record)
- [Complexity Classification Detail](#complexity-classification-detail)

---

## Step 0: Quick Assessment

Before doing anything, assess complexity from the user's request:

- If the request is obviously **Trivial** (single-line fix, typo, obvious change with one clear approach): skip this stage and implement directly. No PRD file is created.
- For all other complexity levels: proceed to Step 1.

This avoids wasting time on requests that don't need brainstorming.

## Step 1: Auto-Context Collection

Before asking "what does the code look like?", collect context yourself:

**Codebase Checklist:**
- Identify likely affected modules/files
- Find existing patterns (similar features, conventions, error handling style)
- Check configs, scripts, existing command definitions
- Note constraints (runtime, dependency policies, build tools)

**Docs Checklist:**
- Find existing PRD/spec/templates
- Find command usage examples, README, ADRs (if any)

Write findings to the active plan record only if one is in use:
- Add to `What I already know`
- Add constraints/links to `Technical Notes`

Otherwise keep the same information in the working summary. Do not create a record just to hold context.

## Step 2: Decide Whether to Create a PRD

After auto-context collection (Step 1), reuse an existing project requirement document when it owns this topic. A new PRD is optional and is most useful when decisions must survive across iterations or sessions. **Do not create one automatically.**

If a new PRD would materially help, ask once whether to persist the plan at `docs/prd/PRD-NNNN-<title>.md`. If the user declines, or the task is small, work conversationally and provide a design summary.

**If Yes:** first run the [PRD Conflict Check](#prd-conflict-check-before-assigning-nnnn) (below) to catch topic collisions against existing `PRD-NNNN-*.md` (resume vs create-new). Only after the check passes, scan `docs/prd/` for existing `PRD-NNNN-*.md` files, assign the next NNNN (max + 1, starting from 0000), and create the PRD at `docs/prd/PRD-NNNN-<title>.md`.

**If No:** skip PRD creation. Follow the same convergence process, but keep notes in the conversation and produce a design summary at the end.

**PRD Location:** `docs/prd/PRD-NNNN-<title>.md`

If creating, use the template and field rules in [PRD-FORMAT.md](PRD-FORMAT.md) — that file is the single source for the template and every field rule.

### PRD Conflict Check (before assigning NNNN)

> This check lives here (the primary PRD-creator skill) rather than in the shared Entry Protocol, because only the requirement (`think`) and slicing (`story`) stages that create a PRD need it — every other stage that "applies the Entry Protocol" would otherwise carry PRD-management ceremony it never uses. The `story` stage references the same procedure defined here.

Applies when about to **create** a new PRD file. Skills that only **read** an existing PRD skip this check.

Different sessions do not share memory, so a later session has no way to know an earlier one already started a PRD on the same topic — it would silently auto-assign the next NNNN and write a duplicate file. This check prevents that.

**Before assigning a new NNNN, scan `docs/prd/` and compare against the new topic:**

1. List existing `PRD-NNNN-*.md` files.
2. For each, compare to the topic being created:
   - **Title slug match** — the kebab-case title in the filename equals the new topic's intended slug (e.g. two `*-block-ui.md`). This is the strongest signal.
   - **Header/Goal similarity** — the PRD's `# <Feature Name>` line or `## Goal` first paragraph names the same subject as the new request.
3. A match on either is a candidate collision.

**If a candidate is found, ask one question (Preference type, with a recommended answer):**

```
Found a possible existing PRD on this topic:
- PRD-0001-block-ui.md — <one-line Goal summary>

Is this the same design, or a different topic?
1. Resume PRD-0001 (Recommended) — reuse its number, continue editing it
2. New PRD — different topic, create with a distinct title
```

- **Resume** → reuse that NNNN, load and continue editing the existing file. Do not create a new file.
- **New PRD** → assign next NNNN (max + 1) and create a new file with a clearly distinct title.

**If no candidate is found** → proceed to assign next NNNN (max + 1) as before.

This check is non-blocking: it never silently merges or silently duplicates. When in doubt, it asks. The intent is to surface the collision, not to make a perfect semantic match — a cheap one-time confirmation is preferable to a stray duplicate PRD.

## Step 3: Classify Complexity

Determine depth of brainstorming for Simple/Moderate/Complex tasks:

| Complexity | Criteria | Behavior |
|---|---|---|
| **Simple** | Clear goal, 1-2 files, clear scope | Ask 1 confirmation question, then finalize a lightweight PRD or implement directly when the change is already clear |
| **Moderate** | Multiple files, some ambiguity | Light brainstorming — resolve only MVP-critical blocking/preference nodes, however many (or few) that turns out to be |
| **Complex** | Unclear goal, architecture choices, multiple approaches | Full brainstorming |

## Step 4: Question Gates (Only Ask High-Value Questions)

Before asking any question, run these gates:

**Gate A — Can I derive this without user?**

If answer obtainable via:
- Codebase inspection (code/configs)
- Docs/specs/conventions
- Quick market/OSS research

→ **Don't ask.** Fetch it and summarize it in the active plan record or working summary. Only when the evidence genuinely doesn't exist in the repo (e.g. no content files to sample) may you ask — as its own single question with your best inference as the recommended answer.

**Gate B — Is this a meta/lazy question?**

Examples:
- "Should I search?"
- "Can you paste code so I can continue?"
- "What does the code look like?" (when codebase is available)

→ **Don't ask.** Take action.

**Gate C — What type of question is this?**

- **Blocking**: Cannot continue without user input
- **Preference**: Multiple valid choices, depends on product/UX/risk preference
- **Derivable**: Should be answered by inspection/research

→ Only ask **Blocking** or **Preference**.

## Step 5: Research-First Mode (Technical Choices)

**Triggers (any one → research first):**
- Task involves choosing approach, library, protocol, framework, template system, plugin mechanism, or CLI UX convention
- User asks "best practice", "how do others do this", "recommended"
- User cannot reasonably enumerate options

**Gate — query an existing `docs/research/INDEX.md`.** If the file exists, check it before repeating research. The full hit (verified/stale/implementation-detail) / miss decision table lives in [SKILL.md Step 5](SKILL.md) — it is authoritative. On a verified hit, reuse the TL;DR and skip the research steps below entirely; on a stale hit, check the record's Boundary Conditions first. Do not create an INDEX merely to perform this check. The steps below run **only on a miss** (or a stale record whose conclusion no longer applies):

**Research Steps (only on an INDEX miss):**
1. Identify 2-4 comparable tools/patterns
2. Summarize common conventions and why they exist
3. Map conventions to our codebase constraints
4. Write to the active plan record's `Research References` section when one exists; otherwise keep the citations in the working summary

If the resulting conclusion is reusable beyond the current task, suggest persisting it as an immutable research record before committing to the approach.

Then present **2-3 viable approaches** in the active plan record when one is in use, or in the working summary otherwise. When using a PRD, fill the `## Research References` and `## Feasible Approaches` sections per [PRD-FORMAT.md](PRD-FORMAT.md).

Then ask **one** preference question:
- "Which approach do you prefer: A / B / C (or other)?"

## Step 6: Expansion Scan (DIVERGE)

Once you can summarize the goal, proactively expand your thinking before converging. **Scale to complexity** (from Step 3):

- **Simple** — skip this step entirely. Simple tasks have a clear goal and 1-2 files; forcing future-evolution/related-scenario divergence on them is over-ceremony. Go straight to Step 7.
- **Moderate** — do only category 3 (Failure & edge cases), raised as a single question.
- **Complex** — do all three categories below, 1-2 points each.

**Expansion Categories (1-2 points each):**

1. **Future evolution**
   - What might this feature become in 1-3 months?
   - Which extension points are worth preserving now?

2. **Related scenarios**
   - Related commands/workflows this should align with?
   - Parity expectations (create vs update, import vs export)?

3. **Failure & edge cases**
   - Conflicts, offline/network failures, retry, idempotency, compatibility, rollback
   - Input validation, security boundaries, permission checks

**Expansion message template (to user):**

```markdown
I understand you want to implement: <current goal>.

Before deep design, let me quickly diverge on three categories (avoid rework later):

1. Future evolution: <1-2 points>
2. Related scenarios: <1-2 points>
3. Failure/edge cases: <1-2 points>

Which do you want in this MVP (or none)?

1. Current requirements only (minimum viable)
2. Add <X> (reserve for future expansion)
3. Add <Y> (improve robustness/consistency)
4. Other: describe your preference
```

Then update the active plan record when one is in use (otherwise keep the same decisions in the working summary):
- What goes in MVP → `Requirements`
- What's excluded → `Out of Scope`

## Step 7: Converge

**Rules:**
- Ask only decisions that cannot be derived from code, docs, or safe reversible conventions. For a large ambiguous design, work one decision at a time with a recommended answer; for ordinary focused work, resolve independent low-risk defaults and report them together.
- Never attach an unrelated second decision as a rider to the main question.
- In a large design, derive the next question from the last answer when it changes the remaining branches. Do not turn repeatable work into an interview merely to follow tree mechanics.
- Terminate when every blocking or preference node that affects the current deliverable is resolved.
- Use multiple choice for preference questions
- After each user answer:
  - Immediately update the active plan record if one is in use; otherwise keep the answer in the working summary
  - Move answered items from `Open Questions` to `Requirements`
  - Update `Acceptance Criteria` with testable checkboxes
  - Clarify `Out of Scope`

**Question priority (recommended):**
1. MVP scope boundaries (what's in/out)
2. Preference decisions (after presenting specific options)
3. Failure/edge behavior (only for MVP-critical paths)
4. Success metrics & acceptance criteria (what proves it works)

**Preference question format (multiple choice):**

```markdown
For <topic>, which approach do you prefer?

1. **Option A** — <implication + trade-off>
2. **Option B** — <implication + trade-off>
3. **Option C** — <implication + trade-off>
4. **Other** — describe your preference
```

## Step 8: Propose Approaches + Record Decision

When requirements are clear enough, propose 2-3 approaches (if not already done via research-first):

```markdown
Based on current information, here are 2-3 viable approaches:

**Approach A: <name>** (Recommended)
- How:
- Pros:
- Cons:

**Approach B: <name>**
- How:
- Pros:
- Cons:

Which direction do you prefer?
```

Record the result in the active plan record's `## Decision (ADR-lite)` section when one exists, using the field shape defined in [PRD-FORMAT.md](PRD-FORMAT.md) (Context / Decision / Consequences). Otherwise keep the same Context / Decision / Consequences summary in the approved design.

## Step 9: Submit Plan for Approval

When open questions are resolved, confirm the complete requirements with a structured summary. If the current task only asked for requirements or design, stop after approval; if it authorizes implementation, continue under that authorization. Persisting a PRD or creating an Issue remains optional.

**Approval format:**

```markdown
Here is my understanding of complete requirements:

**Goal**: <one sentence>

**Requirements**:
* ...

**Acceptance Criteria**:
* [ ] ...
* [ ] ...

**Definition of Done**:
* ...

**Out of Scope**:
* ...

**Technical Approach**:
<brief summary + key decisions>

**Implementation Plan (small PRs)**:
* PR1: <scaffolding + minimal pipeline>
* PR2: <core behavior>
* PR3: <edge cases + docs + cleanup>

Does this look correct? If confirmed, I will continue within the current authorization and persist only the records this project actually uses.
```

## Step 10: Optional Issue Sync and Finalize Plan Record

After the user confirms the plan in Step 9, update the optional plan record and report the approved design. Do not create external artifacts merely to complete a stage.

### 10a: Optional Issue Synchronization

An Issue is an optional external artifact, not a required part of planning. Create or update one only when the project already has a tracker configuration and the current request authorizes writing to it. Otherwise leave the PRD or conversation as the source of truth; do not ask which tracker to use and do not create a local substitute.

If a PRD exists and its `## Issue` field already references an Issue, keep it accurate when the authorized task changes the tracked scope. Never invent a parent Issue merely to make downstream stages work.

### 10b: Record Domain Terms

If new domain concepts emerged during brainstorming (a named concept, an agreed working definition for an ambiguous term, or an entity/relationship not yet represented in the project's glossary), capture them in the active plan record or approved design summary. These are **draft** terms; promote them into a maintained project glossary only when the project already uses one and the current task includes that record.

Add a `## Domain Terms` section to the PRD or approved design summary:

```markdown
## Domain Terms (draft — refine if design validation is needed)

| Term | Working Definition | Status |
|------|--------------------|--------|
| <term> | <one-sentence working definition> | new / needs sharpening / conflicts with existing |
```

Keep this lightweight — record only genuinely new or ambiguous terms (don't duplicate an existing glossary), flag conflicts explicitly, and 3-7 terms is typical. If you have notably more, the scope may be too broad.

### 10c: Output Approved Plan

After the optional record updates, output the approved plan:

```markdown
Plan approved.

**Approved design summary:**
- **Building**: What this is (1 paragraph)
- **Not building**: Explicit exclusion list
- **Approach**: Chosen option + rationale
- **Key decisions**: 3-5 items with rationale
- **Unknowns**: Only explicitly deferred items with reason and owner
- **Record**: existing doc / optional PRD path / conversation only
```

## Complexity Classification Detail

### Trivial

**Criteria:**
- Single-line fix
- Typo correction
- Obvious change with one clear approach

**Behavior:**
- Skip brainstorming entirely
- State that requirement convergence is unnecessary for this request
- Recommend direct implementation outside this skill

**Example:** "Fix typo in error message"

### Simple

**Criteria:**
- Clear goal
- 1-2 files affected
- Clear scope, no ambiguity

**Behavior:**
- Ask 1 confirmation question if needed
- Finalize a lightweight plan record only when the project uses one, or implement directly when the change is already clear
- Do not write code inside the requirement stage

**Example:** "Add retry to this API call"

### Moderate

**Criteria:**
- Multiple files
- Some ambiguity
- Clear goal but multiple paths

**Behavior:**
- Light brainstorming
- resolve only MVP-critical blocking/preference nodes — the tree decides the count, not a quota

**Example:** "Add user preferences page"

### Complex

**Criteria:**
- Unclear goal
- Architecture choices required
- Multiple valid approaches
- Significant implementation effort

**Behavior:**
- Full brainstorming process
- All steps apply
- Research-first for technical choices

**Example:** "Design multi-tenant authentication system"
