---
name: grill
description: "Challenge plans by extracting every open decision from the PRD and resolving them one by one — skip none. Use only when the user explicitly asks to grill, challenge, stress-test, or deeply validate a plan or design. Do not trigger for an ordinary implementation request or a code review."
---

# Grill: Challenge Plans and Update Domain Knowledge

🥷 Challenge the plan before coding.

Interview me relentlessly about every aspect of this plan until we reach shared understanding — every branch of the design tree. For each question, provide your recommended answer.

Finding facts is your job, never the user's: if the codebase can answer it, look it up instead of asking. Only decisions reach the user.

Ask **exactly one question per message, always** — never a batch, never a pre-computed list, no piggyback riders (anti-patterns #3, #4). The next question is derived from the user's last answer; keep asking until the decision tree is **exhausted** — every branch walked to a settled decision. Tree-walk mechanics and the message template: [REFERENCE.md §Question Pacing](REFERENCE.md).

## Outcome Contract

- **Outcome**: A frozen business baseline — the PRD with every open decision resolved — plus a rendered baseline page for human review
- **Done when**: Every open decision resolved, terminology consistent with `CONTEXT.md`, ADRs created where the 3 conditions are met, PRD `Status: Grilled`, and `docs/baseline/PRD-NNNN-<slug>.html` rendered from the final PRD
- **Evidence**: Updated `docs/prd/PRD-NNNN-<title>.md` (status → Grilled), updated `CONTEXT.md`, created `docs/adr/<NNNN>-*.md` (where warranted), baseline page path
- **Output**: Baseline page for the user to confirm, parent Issue synced (if created by `/think`), next step to `/story`

## Before You Start

Apply the [Skill Entry Protocol](../rules/entry-protocol.md) — it locates the PRD and `CONTEXT.md` and checks upstream artifacts. If no PRD exists or it's too thin, suggest `/think` first — don't grill vapor.

## The Work

1. **Extract everything unresolved.** Read the PRD with hostile eyes: Open Questions, unvalidated Assumptions, the `## Domain Terms (draft)` section `/think` left behind, vague terms, unexplained scope boundaries, shaky technical approach, edge cases, conflicts with `CONTEXT.md`. Skip none.
2. **Work the checklist one question at a time.** Pick the highest-value unresolved item, ask it as a single question with your recommended answer, and wait. After the answer lands, update the tree — resolved items close, new findings may open children — and pick the next question from what the answer just made askable (see [REFERENCE.md §Question Pacing](REFERENCE.md)).
3. **Resolve as you go, not in a batch at the end.** Update files inline:
   - **Terminology resolved** → update `CONTEXT.md` now (glossary only, no implementation details).
   - **Significant decision** → offer an ADR when the three conditions in [ADR-FORMAT.md §创建条件](ADR-FORMAT.md) are all met (hard to reverse, surprising without context, result of a real trade-off — full definitions live there, single source). Otherwise skip. **Decide eligibility once, the moment the decision lands**: either create the ADR inline, or record "no ADR — <which condition failed>" in the PRD. Never re-adjudicate a decision's ADR eligibility at completion — a flip between "declined inline" and "created at wrap-up" means the inline judgment was never made.
   - **Code can answer it** → grep/read the code instead of asking the user.
   - **Only running a demo can answer it** (options that reasoning and reading can't separate — which is faster, does the model hold up, what should it look like) → park the item and propose a minimal experiment; if a prototype skill is installed, it may be used. Fold the verdict back as an ADR / PRD update and resume the checklist.
4. **Run the exhaustiveness gate** before declaring complete: Open Questions, Assumptions, terms, scope, code cross-check — all resolved.
5. **Fill the PRD `## Traceability` `Grilled by` field** so downstream skills know the plan was validated.
6. **Sync the parent Issue (if it exists).** Update its body to reflect scope changes (sharpened terms, confirmed boundaries, new ADRs). Do **not** change title or close it. If the `## Issue` field is empty, check the PRD's `Created by` field — if `/story`, skip (expected); if `/think`, warn the user that the parent Issue was not created (see REFERENCE.md for exact message).
7. **Freeze the baseline.** Set `Status: Grilled`. From here the requirements are a contract — see [Freezing the Baseline](#freezing-the-baseline).
8. **Render the baseline page.** Use `answer-me-with-html` to write `docs/baseline/PRD-NNNN-<slug>.html` from the frozen PRD, then report its path so the user can confirm the whole scope in one view.

## What Goes Where

| Situation | Action |
|---|---|
| Goal statement itself needs to change, or fundamental approach invalidated | Send back to `/think` — too big for grill |
| Only terminology sharpened, scope confirmed, approach validated with refinements | Proceed to `/story` |

For the challenge types (terminology conflict, fuzzy language, scope boundary, edge case, code cross-check), the file layout (single vs multi-context via `CONTEXT-MAP.md`), and a worked example, see [REFERENCE.md](REFERENCE.md).

## Freezing the Baseline

Reaching `Status: Grilled` **freezes the baseline**. From that moment the PRD's Goal, Requirements, Acceptance Criteria and Out of Scope are a contract: `story` and `implement` read it, they never edit it.

**Changes after freezing go through the PRD, not around it.** Record every change in a `## Change Log` table — one row per change: `date | what changed | why and who asked | affected slices`. Keep `Status: Grilled` for additive changes (new field, extra validation, an added state). If the goal itself or the scope changes materially, send the PRD back to `Draft` and re-run `think` → `grill`.

**Render the baseline page as part of finishing.** After the PRD reaches `Grilled`, use [answer-me-with-html](../answer-me-with-html/SKILL.md) to render `docs/baseline/PRD-NNNN-<slug>.html` from the PRD: goal, in scope, out of scope, key decisions with their ADRs, and any assumption that stayed unresolved. Render it before reporting completion — the user should open one page and answer "is this what we agreed?".

**The page is a view, never the source.** The PRD is authoritative. If the page and the PRD disagree, the PRD wins and the page is re-rendered. Re-render after any `## Change Log` entry so the page date matches the PRD's `Last updated`. Commit the page with the documentation; it is a delivery artifact, not a throwaway render.

## Gotchas

| What happened | Rule |
|---|---|
| Skipped an unresolved assumption | Extract every open item first, then resolve each |
| Updated CONTEXT.md in a batch at the end | Update inline, the moment each term resolves |
| Created an ADR for a trivial decision | Only when all 3 conditions met |
| ADR flipped at completion (declined inline, created at wrap-up — or vice versa) | Decide ADR eligibility once, inline, when the decision lands; record the failed condition when declining |
| CONTEXT.md gained implementation details | It is a glossary, nothing more |
| Asked the user something the code could answer | Explore the codebase instead |
| Skipped the PRD's `## Domain Terms (draft)` section | It is `/think`'s explicit handoff; promote each row to `CONTEXT.md` (or resolve the flagged conflict), then drop the section |
| Batched questions into one message, or worked a pre-computed list | One question per message, always — the next question is derived from the last answer (anti-patterns #3, #4; see Question Pacing) |
| Forced a decision that reasoning couldn't settle | Park the item and propose a minimal experiment — a demo may settle it; fold the verdict back as an ADR |
| PRD not updated after interview | Update `docs/prd/PRD-NNNN-<title>.md` and set `Status` to `Grilled` before declaring complete |
| Declared complete without the exhaustiveness gate | Run the 5-point gate first |
| Parent Issue body stale after grill changed scope | Sync the parent Issue (if `## Issue` field present) — reflect sharpened terms, scope, ADRs; don't change title or close |

## Output

```
Grill complete — baseline frozen.

Resolved <N> items:
- <term>: <resolution>
- <assumption>: <validated/converted>
- <decision>: <ADR created | recorded in PRD>

Updated:
- docs/prd/PRD-NNNN-<title>.md — Status → Grilled
- CONTEXT.md — <count> terms sharpened/added
- docs/adr/<NNNN>-<title>.md — created (if any)
- docs/baseline/PRD-NNNN-<slug>.html — rendered from the frozen PRD

Exhaustiveness gate: passed
Parent Issue: #<num> synced | skipped (none)

Baseline page: <absolute path>
Next: Confirm the page; then /story to slice the frozen baseline.
```
