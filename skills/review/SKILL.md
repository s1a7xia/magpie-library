---
name: review
description: "Three-perspective code review performed by the main agent. Use only for an explicit full review: 完整审查, 三视角审查, 发布前完整把关, or a direct /review invocation. Ordinary 审查一下/check/验收 is a main-agent light review and must not start this flow."
---

# Review: Three-Perspective Review

🥷 Complete all finish work before merge or release.

Performs three independent review perspectives — Test Review, Code Review, Impact Review — by re-reading all shared context from disk for each perspective. Merges the results into a single comprehensive review. Issue sync and release follow-through require current-turn explicit authorization.

## Outcome Contract

- **Outcome**: Merged three-perspective review report — test quality, implementation quality, and impact analysis — with contradictions highlighted for human adjudication
- **Done when**: All three perspective reports produced, merged report presented, local file updates completed or listed as follow-up, remote actions completed only if explicitly authorized
- **Evidence**: Authorized test/lint/typecheck/build output, code diff analysis, updated files
- **Output**: Structured merged report with per-perspective sections, contradiction block (if any), and unified recommendation

## Prerequisites

- Code is complete (by `implement` or directly)
- Reviewable changes exist — uncommitted (staged or unstaged) **or** already committed on the current branch (e.g., per-seam commits from `/implement`)

## Process Summary

**Step 1 — Collect context**: Apply the [Skill Entry Protocol](../rules/entry-protocol.md). Read the diff — staged + unstaged if the working tree is dirty, otherwise the branch range since the default branch (or the PR diff) when the work is already committed (see [REFERENCE.md Chapter 1](REFERENCE.md)). Read README, package.json, Makefile, CI configs. If the diff contains an Issue reference, read the PRD path from the Issue body's `Meta → PRD` field and load it. Gather available shared context paths (PRD, Story, Issues, CONTEXT.md, ADRs). **PRD quality check:** if PRD Traceability shows `Created by: /story (minimal PRD)`, note that requirements may not be decision-complete — review acceptance criteria coverage with extra care.

**Step 2 — Produce three review perspectives**: Re-read the shared context from disk and complete Test Review, Code Review and Impact Review in sequence. Do not reuse another perspective's cached conclusions.

**Step 3 — Merge reports**: Concatenate the three reports. Do not auto-resolve contradictions — flag them explicitly for human adjudication. See [Report Merge Rules](#report-merge-rules).

**Step 4 — Present merged report**: Show the full merged report to the user with per-perspective sections, verification status, contradiction block, and unified recommendation.

**Step 5 — Authorization gate**: Present the report and ask **one** question — approve the recommendation, or request changes. Merge/release and other actions are not part of the approval: they are requested (and authorized) separately per Chapter 6. Local doc updates are allowed when necessary; remote actions require current-turn explicit authorization.

**Step 6 — Execute authorized actions**: Perform only actions the user explicitly requested in the current turn — local file updates, issue sync, release follow-through. A passing review does not bypass page acceptance: a slice that has not passed the user-initiated `page-acceptance` stays `Dev Complete`. A slice already `Accepted` may be marked `— Done` after review passes. Set the PRD to `Done` only when every slice is `— Done` and the project's other close-out conditions hold. See [Authorization Boundaries](#authorization-boundaries).

See [REFERENCE.md](REFERENCE.md) for detailed checklists and report templates.

## Three Review Perspectives

Each perspective is completed independently, re-reading all shared context from disk (PRD, Story, Issues, CONTEXT.md, ADRs, diff). Do not let one perspective's conclusion substitute for another's evidence.

| Perspective | Focus Area |
|---|---|
| **Test Review** | Test quality, boundary coverage, test design reasonableness, naming, isolation, mock usage |
| **Code Review** | Implementation quality, security, performance, code conventions, error handling, readability, engineering principles local to the diff ([rules/engineering-principles.md](../rules/engineering-principles.md)) |
| **Impact Review** | Change scope, regression risk, compatibility, architecture health (local to this change), principles with cross-module consequence (DIP, OCP, new coupling), tech debt introduced, release strategy (feature flags, canary, rollback plan). Records global architecture concerns for a separate review |

### Perspective Independence

Each perspective is independent: re-read shared context from disk and do not reuse cached conclusions. See the common checklist in [REFERENCE.md](REFERENCE.md), plus each chapter's perspective-specific addition.

## Report Merge Rules

Present the three perspective reports as distinct sections. If two or more reach conflicting conclusions on the same item, extract them into a `Contradictions` block — present both sides, **never auto-resolve** (the human adjudicates). Derive a single recommendation; if perspectives disagree, the recommendation is "Request Changes" and the disagreement goes in Contradictions. See [REFERENCE.md Chapter 5](REFERENCE.md) for the merge steps, contradiction format, and merged-report template.

## Authorization Boundaries

Default review is local inspection only. Local doc/PRD/CONTEXT/ADR updates are allowed **only when the review verified the underlying change**. Issue close/status/label changes and all release actions require explicit user authorization **in the current turn**. See [REFERENCE.md Chapter 6](REFERENCE.md) for the full boundary table.

## Hard Rules

- **Security first**: Block immediately on any security issue. The Code Review perspective runs the full Security Checklist in REFERENCE.md before approving any diff. Security-sensitive changes must include rollback path, audit trail, and regression test (anti-pattern #18).
- **Test coverage**: New code should have tests whenever the project profile or current request authorizes writing or running tests; otherwise record the gap as a risk. Review never writes tests on its own.
- **Evidence first**: Every conclusion needs evidence. Run only authorized checks and never claim one passed without running it (anti-pattern #6). An unauthorized check is reported as not run.
- **Verify the artifact, not just the source**: "tests pass, code looks right" is not done. Report each layer's status separately — source tests, build/package, CI, runtime — a missing layer is an explicit gap, not passing evidence (anti-pattern #17).
- **Missing dependency**: a skill this review names but that is not installed is not an implicit dependency. Complete the review with the steps here and record the uncovered capability instead of stalling, inventing a result, or asking for a skill the project never had.

## Integration Review

When all vertical slices of a PRD are complete, perform extra checks beyond single-slice review (cross-slice data flow, shared state consistency, full PRD acceptance criteria coverage, integration test coverage, dependency order). See [REFERENCE.md](REFERENCE.md) for details. State explicitly: "Integration Review — checking <N> slices for PRD <name>."

## Gotchas

| What happened | Rule |
|---|---|
| Perspective reused cached context | Independence rule: re-read all shared context from disk for each perspective |
| Contradictions silently resolved in merge | Report Merge Rules: extract to Contradictions block, present both sides |
| Said "should work" without verification | Hard Rules: run verification commands |
| Assumed project commands | Step 1: extract from config |
| Didn't check security issues | Hard Rules: Security first — Code Review perspective runs Security Checklist |
| Impact Review drifts into global architecture review | Impact Review scope: local impact only. Record global concerns for a separate architecture review |
| PRD not updated after review | Step 6: update local files when authorized |
| Issues closed without authorization | Authorization Boundaries: close/status/label requires current-turn authorization |
| Perspective skipped re-reading shared context | Independence rule: never cache file reads from another perspective |
| Principle violation reported as a blocker, or with no stated consequence | Ch3 Engineering Principles gates: name the concrete consequence or drop the finding; severity defaults to `minor`, and a principle tag never creates a blocker |

## Output

```
Review complete.

── Test Review ──      <Test Review report>
── Code Review ──      <Code Review report>
── Impact Review ──    <Impact Review report>
── Contradictions ──   <both sides, or "No contradictions">
── Verification ──     Tests / Lint / Typecheck / Build: <pass/fail>
── Findings ──         new terms, new decisions, updated files, synced issues
Recommendation: Approve / Request Changes / Comments

Next: User decides — merge/release, or fix issues and re-review.
```

The full merged-report template (with all fields and next-step branches) is in [REFERENCE.md Chapter 5](REFERENCE.md).
