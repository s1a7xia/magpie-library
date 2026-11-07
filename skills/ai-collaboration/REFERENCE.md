# Collaboration Reference

## Operational Boundaries

- Git and the configured Issue/PR/MR provide shared traceability; chat history is not the project record.
- A pushed commit, remote issue update, CI result, or test result is reported only after direct confirmation.
- All automated verification and browser/page testing are performed by Codex. dsh does not test or report test results as its own.
- dsh captures requirements and identifies the project's agreed inbox. It does not claim a remote or local write succeeded without direct confirmation.
- For status replies, use project-state and accessible Issue/PR/Git evidence; keep the response short and mobile-readable. Never infer current progress from chat history alone.
- WeChat intent routing and research rules live only in `~/.dsh/im/AGENTS.md` and `REPORTER.md`; this file does not restate them. A brief is unverified input for Codex, not a formal research record.
- If a task requires dsh to modify code or commit, ask the user to explicitly change the role boundary for that task; no default overlap.
