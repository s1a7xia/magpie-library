# Sub-Agent Runtime Semantics

Optional rules for work the user explicitly authorizes to be delegated.

## The Rule

- The main agent completes ordinary work. Risk, complexity, or the availability of another model does not by itself authorize delegation.
- Delegation requires an explicit user request or an already-recorded project authorization for that class of work.
- A delegated context reads the current facts it needs from disk rather than relying on the main agent's summary alone.
- Delegated investigation and review are read-only by default. They inherit only the test, database, Git, and external-write permissions explicitly included in the current task.
- Do not assume parallel execution, a fixed number of reviewers, or a multi-agent pipeline. Use the host's available collaboration mechanism only when useful; otherwise the main agent performs the work.
- The main agent verifies and reconciles delegated findings, and remains the single product writer unless the user assigns another writer explicitly.

## Reference

Skills may link to this file as:

```
See [Sub-Agent Runtime Semantics](../rules/sub-agent-runtime.md) — delegation is optional and requires explicit authorization.
```
