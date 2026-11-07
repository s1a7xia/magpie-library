# Standards Gate — Detailed Rules

This is the detailed version of the gate summarized in [entry-protocol.md](../entry-protocol.md#standards-gate). Read it when a task changes code, approves compliance, or needs a completion verdict; read-only diagnosis may use the compact gate.

## Required context before affected work

Once a standard/profile applies, successfully read its configuration, entry point and relevant original rules before changing affected code or approving its compliance. Record their actual paths in the task evidence.

A missing/unreadable file, an unresolved reference or a missing original is a blocked prerequisite: stop affected code changes and compliance approval, identify what could not be read, and restore it within the authorized scope when possible. Read-only diagnosis and unrelated work may continue. A prior session's summary does not satisfy this gate.

## Verification authorization before completion

Checks are required only when the current request, the project's explicitly adopted standards, or this stage's explicitly authorized verification calls for them. Derive the scope from the active stage, applicable standards and actual project build configuration.

When checks are authorized, a code task is complete, verified, or eligible for a `Done` transition only after they pass against its final changes. Preserve command, working directory, exit status and relevant output as evidence. When no check is authorized, complete the implementation with the diff reviewed, label it unverified, and do not claim test, acceptance, or runtime success.

When an authorized check fails, repair and rerun it within scope. When it cannot run, report the affected task as blocked/unverified. Existing merge/release criteria still apply after authorized checks pass.

## Stage boundaries

Planning does not require compiling prospective code. A read-only review may use current, verifiable build/test evidence for the change under review instead of rerunning unchanged checks solely because a review was requested.

An intermediate phase that is not the delivered result (planning notes, a spike, a probe) is not a completed implementation; apply the delivery checks once the real change exists. Mark a check not applicable only with an explicit stage/scope reason. A missing dependency, failed command or unread standard is not a not-applicable reason. A review may report findings with verification gaps, but must withhold an unqualified pass when required evidence is missing or stale.

## Design and compliance constraints

Apply design constraints during think/grill, carry agreed contracts into story acceptance criteria, use implementation conventions during implement/debug, and check violations during review.

Explicit project decisions/exceptions take precedence over generic defaults; cite their source and scope rather than inventing a waiver. Where documented API usage conflicts with the checkout, expose the mismatch and inspect source before writing code.
