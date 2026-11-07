# Project Context Templates

The three state-file templates are maintained in **one** place — the `setup-project` skill's template directory — so they cannot drift into two copies. Read them there:

| Output file | Template |
|---|---|
| `docs/agents/project-state.md` | [../../setup-project/templates/project-state.md](../../setup-project/templates/project-state.md) |
| `docs/agents/project-decisions.md` | [../../setup-project/templates/project-decisions.md](../../setup-project/templates/project-decisions.md) |
| `docs/agents/verification.md` | [../../setup-project/templates/verification.md](../../setup-project/templates/verification.md) |

`setup-project` creates these files at initialization from confirmed project facts; this skill (`project-context`) maintains them afterwards. Do not leave placeholder values in a real project: an empty decisions or verification section reads as "none recorded", not as a blank template.
