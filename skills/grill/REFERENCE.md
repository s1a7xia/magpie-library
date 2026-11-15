# Grill: Detailed Reference

## File Layout

When the project already uses domain docs, grill can update the relevant ones. Their location depends on the repo shape; a project without them can still validate a plan conversationally.

**Single context (most repos):**

```
/
├── CONTEXT.md
├── docs/
│   ├── adr/
│   │   ├── 0001-event-sourced-orders.md
│   │   └── 0002-postgres-for-write-model.md
│   └── prd/
│       └── PRD-NNNN-<title>.md
└── src/
```

**Multi-context** — a root `CONTEXT-MAP.md` marks the repo as having several bounded contexts, each with its own glossary and ADRs:

```
/
├── CONTEXT-MAP.md
├── docs/adr/                 ← system-wide decisions
└── src/
    ├── ordering/
    │   ├── CONTEXT.md
    │   └── docs/adr/         ← context-specific decisions
    └── billing/
        ├── CONTEXT.md
        └── docs/adr/
```

Create or update these files only when the project has chosen to use that record and the current task includes it. Do not initialize a glossary or ADR directory merely because a decision was made. If a record is in use and a file is missing, use [CONTEXT-FORMAT.md](CONTEXT-FORMAT.md) or [ADR-FORMAT.md](ADR-FORMAT.md) as the format source.

## Requirement vs Validation Boundary

Requirement convergence discovers *what to build* and produces a plan. Validation challenges *how well that plan holds up* and sharpens the relevant decisions, glossary, and architecture records.

**Return to requirement convergence** when:
- The goal statement itself needs to change (not just individual requirements)
- A fundamental technical approach needs re-evaluation (not just refinement)
- New requirements introduce an entirely new domain area outside original scope
- The PRD's Decision (ADR-lite) is invalidated by new information
- The PRD was created minimally during slicing (no requirement-stage `think` pass) and major design questions surface

**Proceed with work slicing or implementation** when only terminology was sharpened, scope confirmed, or approach validated with refinements. Slicing is optional unless the work needs it.

Small clarifications can be resolved inline. Major scope changes deserve a proper think session.

## What to Challenge

Read the available requirements or plan with hostile eyes. Pull out every open decision across these categories that can affect the current deliverable:

| Category | What to look for |
|---|---|
| **Open Questions** | Items explicitly unresolved in the plan |
| **Assumptions** | Things the plan assumes but hasn't validated |
| **Vague terms** | Words that could mean different things to different people |
| **Scope boundaries** | Why something is in vs out of scope — and is "out" really "deferred"? |
| **Technical approach** | Is the chosen approach sound? Were alternatives considered? |
| **Edge cases** | What happens when things go wrong (mid-billing cancellation, partial failure, concurrency)? |
| **Glossary conflicts** | Terms that clash with a glossary the project actually maintains |
| **Code contradictions** | Stated behavior that doesn't match what the code does |
| **Recorded decisions** | Decisions already captured in the plan — evaluate whether the project's existing ADR mechanism warrants a formal record |

## Challenge Patterns

For each item, lead with your recommended answer, then ask. A few patterns:

- **Terminology conflict** — *"Your glossary defines 'cancellation' as X, but the PRD seems to mean Y — which is it?"*
- **Fuzzy language** — *"The PRD says 'account' — do you mean Customer or User? Those are different."* Propose a precise canonical term.
- **Scope boundary** — *"You've excluded batch operations — genuinely not needed, or deferred? If deferred, note the extension point."*
- **Edge case** — *"What happens when a customer cancels mid-billing cycle? Prorate / full refund / no refund?"*
- **Code cross-check** — *"The PRD says partial cancellation is possible, but the code cancels entire Orders — which is the target state?"* Verify by reading the code, don't just ask.

## Question Pacing

Ask only decisions that cannot be derived from code, documents, or safe reversible defaults. For a large ambiguous plan, walk the decision tree one question at a time with a recommended answer. For ordinary focused work, resolve independent low-risk defaults and report them; do not create a mandatory interview.

1. **Pick the highest-value unresolved node** and ask it as a single question, with your recommended answer.
2. **Wait for the answer.** The answer resolves that node and changes the tree: it may open child questions (the answer's consequences), close a branch (settled for good), or contradict the PRD (new unresolved node).
3. **Recompute, then pick the next question.** The next question must be *derived from the answer just given* — ask what the answer newly makes askable or newly puts in doubt. If you already knew what question N+1 would be before hearing answer N, you are working a list, not a tree.
4. **Terminate on tree exhaustion**, not on list exhaustion: every Open Question resolved, every Assumption validated or converted, every term settled, every scope boundary confirmed, every code cross-check done. When no unresolved node remains, declare completion — do not pad with redundant confirmations.

A question whose prerequisite decision is still open is **not askable yet** — asking it now means guessing at the prerequisite's answer. Keep it in the tree; it usually becomes askable (or disappears) after the next answer.

For a multi-session or high-impact design, use one question block per message:

```
❓ **Q — <question title>**: <body; multiple choices if applicable>

➡️ <your recommended answer>
```

## Exhaustiveness Gate

Before declaring complete, verify every box that applies to the current deliverable:

- [ ] Every open question that can change the deliverable has a resolution or an explicit deferral
- [ ] Every Assumption validated or converted to a requirement
- [ ] Every term conflict that affects implementation addressed
- [ ] Every scope boundary confirmed (why is X out of scope?)
- [ ] Code cross-check completed for all stated behaviors

If any box is unchecked, keep going.

## Optional Requirement Record Update

If a PRD or equivalent requirement record is already in use, record the validation there:

```markdown
- **Grilled by**: design-validation stage (`grill`, completed <YYYY-MM-DD>) — <summary: terms sharpened, assumptions resolved, ADRs created>
```

## Existing Tracker Record

Issues are optional. If the PRD already references an Issue and the current request authorizes tracker writes, update that Issue with approved scope changes. If there is no tracker or no referenced Issue, continue with the PRD or conversation; do not create a parent Issue and do not warn about its absence.

## Worked Example

```
User: validate the "user subscription" plan (worked example where the project already uses a PRD)

Agent: [reads docs/prd/PRD-0003-subscription.md and CONTEXT.md]

I've reviewed the PRD and found 6 items to resolve:

1. "Subscription" — not in CONTEXT.md, used ambiguously
2. Assumption: "payment is immediate" — not validated
3. Open Question: cancellation policy
4. Scope: "upgrade/downgrade" excluded without reason
5. Technical: Stripe vs custom payment — no decision recorded
6. Code: existing User model has no payment fields — migration unclear

#2 and #6 are code questions — I check those myself before asking
anything. [grep: payment, stripe, gateway] → found src/payment/ with
custom gateway, no Stripe; payment is async (assumption #2 disproved —
PRD updated to match). #6: User model has no payment fields →
migration cost is the hinge for #5, so #5 is not askable until the
cancellation/scope answers land.

Highest-value unresolved node right now is the terminology — it shapes
how every later question reads. So, one question:

❓ **Q1 — "Subscription"**: your PRD uses it for both the act and the
entity. I recommend: **Subscription** — a Customer's active paid access
agreement with a lifecycle (created → trial → active → past_due →
cancelled).

➡️ Adopt this definition.

User: Good, and make sure "trial" is one of the states.

Agent: [updates CONTEXT.md now: Subscription includes trial state]
The answer settles the term and opens a child I couldn't ask before:
with a trial state in the lifecycle, money can change hands mid-cycle.

❓ **Q2 — Cancellation policy**: when a paying customer cancels, recommend
End-of-period (simpler, less refund logic). Alternatives: immediate +
prorate, immediate + no refund.

➡️ End-of-period.

User: End-of-period.

Agent: [Q2 meets all 3 ADR conditions — hard to reverse ✓, surprising
without context ✓, real trade-off ✓ — creates docs/adr/0003-
cancellation-eop.md inline] That decision closes the refund branch,
which makes the payment-gateway question answerable: the codebase
already runs a custom gateway in src/payment/.

❓ **Q3 — Stripe vs custom gateway**: recommend keeping the custom
gateway; add a Stripe adapter only if webhook events are needed.

➡️ Keep the custom gateway.

User: Keep custom.

Agent: [PRD updated] Last unresolved node is the scope boundary:

❓ **Q4 — "Upgrade/downgrade" excluded**: genuinely not needed, or
deferred? If deferred, I'll note the extension point in the PRD.

➡️ Deferred.

User: Deferred.

Agent: All 6 resolved — tree exhausted. Exhaustiveness check: ✓ Open
Questions, ✓ Assumptions, ✓ Terms, ✓ Scope, ✓ Code.

Updated files:
- docs/prd/PRD-0003-subscription.md — updated (Status → Grilled)
- CONTEXT.md — 3 new terms, 1 sharpened
- docs/adr/0003-cancellation-eop.md — created

Next: slice or implement the approved plan when the current request authorizes it. In a conversational plan, the validated decision summary is enough.
```

Note the shape: extract all items up front; answer code questions yourself before asking anything; then **one question per message**, each next question derived from the answer just given (the trial-state answer opened the cancellation question; the cancellation answer unblocked the gateway question); hold questions whose prerequisites are still open until an answer unlocks them; update CONTEXT.md / create the ADR inline the moment each decision lands — never in a batch at the end.
