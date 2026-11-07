# Filing Consistency

While scanning domain docs, flag misplaced files so drift surfaces early. Report findings as a note; do **not** auto-fix by moving or renaming files. Moving files is a destructive operation and needs explicit authorization.

## Checks

- **PRD outside `docs/prd/`**: `docs/adr/PRD-*.md`, `docs/prd-*.md` in the docs root, or `PRD-*.md` at repo root.
- **Prefix mismatch**: ADR files carrying a `PRD-` prefix, or PRD files carrying no `PRD-` prefix.
- **Research outside `docs/research/`**: `<stack>-<topic>-<major>.md` at repo root or under `docs/` elsewhere.
- **Number collisions**: two ADRs sharing the same `NNNN`, or two PRDs sharing the same `PRD-NNNN`. This is common when multiple sessions run concurrently.
- **Research record collisions**: two records sharing the same `<stack>-<topic>-<major>` filename (see the `/research` dedup step).

## Reporting

Use a short note in the skill output:

> Filing inconsistency found: `<file>` appears misplaced / `<NNNN>` is used by two files. Want me to relocate?

Do not silently move or renumber. If the user approves a correction, preserve links and update references in the same change.
