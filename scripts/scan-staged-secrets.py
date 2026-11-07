"""Fail a local delivery check when staged text contains high-confidence secrets.

This intentionally has a small pattern set. It is a guard against obvious
accidental commits, not a replacement for a secret-management system.
"""

from __future__ import annotations

import re
import subprocess
import sys


PATTERNS = (
    ("private key", re.compile(r"-----BEGIN(?: [A-Z0-9]+)? PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"\b(?:ghp|gho|ghu|ghs)_[A-Za-z0-9]{20,}\b")),
    ("GitHub fine-grained token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b")),
    ("GitLab token", re.compile(r"\bglpat-[A-Za-z0-9_-]{20,}\b")),
    ("Slack token", re.compile(r"\bxox(?:b|p|a|r|s)-[A-Za-z0-9-]{20,}\b")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("Telegram bot token", re.compile(r"\b\d{8,12}:[A-Za-z0-9_-]{30,}\b")),
    (
        "credentialed connection string",
        re.compile(r"\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis)://[^/\s:@]+:[^@\s]+@"),
    ),
)


def staged_diff() -> tuple[int, str]:
    completed = subprocess.run(
        ["git", "diff", "--cached", "--no-ext-diff", "--unified=0"],
        capture_output=True,
        check=False,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if completed.returncode != 0:
        print("Unable to read staged Git diff; secret scan was not completed.", file=sys.stderr)
        return completed.returncode, ""
    return 0, completed.stdout


def main() -> int:
    status, diff = staged_diff()
    if status:
        return status
    if not diff:
        return 0

    findings: list[str] = []
    for line_number, line in enumerate(diff.splitlines(), start=1):
        if not line.startswith("+") or line.startswith("+++"):
            continue
        for label, pattern in PATTERNS:
            if pattern.search(line):
                findings.append(f"{label} in staged addition near diff line {line_number}")
                break

    if not findings:
        return 0

    print("Potential secrets found in staged changes. Commit stopped:", file=sys.stderr)
    for finding in findings:
        print(f"- {finding}", file=sys.stderr)
    print(
        "Remove, rotate, or move the credential to an approved secret store; "
        "do not paste it into the report.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
