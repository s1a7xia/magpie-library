"""Build the public, credential-free Magpie configuration snapshot.

Reads the local Magpie library and emits only the fields that are safe for the
public configuration mirror. It never copies MCP headers, environment values,
DSN credentials, login state, or sync configuration.
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path


MAGPIE_HOME = Path.home() / ".config" / "magpie"
LIBRARY = MAGPIE_HOME / "library"
OUT = LIBRARY / "config" / "environment.snapshot.json"


def main() -> int:
    data = json.loads((MAGPIE_HOME / "library.json").read_text(encoding="utf-8"))
    mcp = []
    for server in data.get("mcp", []):
        name = server.get("name")
        item = {
            "name": name,
            "transport": server.get("transport"),
            "agents": server.get("agents", []),
        }
        if server.get("url"):
            item["url"] = server["url"]
        command = server.get("command")
        if command:
            item["command"] = Path(command).name
        args = server.get("args")
        if isinstance(args, list):
            # stdio servers are often `npx -y <package>` or `<magpie> mcp <mode>`.
            # Keep the package/subcommand, but never copy a DSN, token or path.
            safe_args = [
                arg
                for arg in args
                if isinstance(arg, str) and not arg.startswith(("-", "/", "\\"))
            ]
            if name == "dbhub":
                item["args"] = ["@bytebase/dbhub", "--transport", "stdio"]
            elif safe_args:
                item["args"] = safe_args
        mcp.append(item)

    snapshot = {
        "recordedDate": date.today().isoformat(),
        "source": "local Magpie library; config registration is not connectivity verification",
        "instructionsAgents": data.get("instructions", {}).get("agents", []),
        "sharedSkills": bool(data.get("sharedSkills", False)),
        "mcpHub": bool(data.get("mcpHub", False)),
        "skillRouter": bool(data.get("skillRouter", False)),
        "skills": [
            {
                "name": item.get("name"),
                "agents": item.get("agents", []),
                "route": item.get("router", "routed" if data.get("skillRouter") else "direct"),
            }
            for item in data.get("skills", [])
        ],
        "mcp": mcp,
    }
    OUT.write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
