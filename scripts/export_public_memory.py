"""Export the reviewed public subset of Magpie structured memory.

The running memory store contains local paths and operational metadata. This
script copies only Markdown memory bodies with a whitelist of durable metadata
fields, so the public mirror never depends on hand-editing the live store.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


MEMORY = Path.home() / ".config" / "magpie" / "memory"
PUBLIC_FIELDS = (
    "kind",
    "scope",
    "status",
    "origin",
    "tags",
    "why",
    "created",
    "updated",
    "edited",
)


def split_frontmatter(text: str) -> tuple[str, str]:
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z", text, re.S)
    if not match:
        raise ValueError("memory file has no YAML frontmatter")
    return match.group(1), match.group(2).lstrip()


def top_level_yaml(frontmatter: str) -> dict[str, list[str]]:
    fields: dict[str, list[str]] = {}
    current: str | None = None
    for line in frontmatter.splitlines():
        top = re.match(r"^([A-Za-z_][\w-]*):(?:\s*(.*))?$", line)
        if top:
            current = top.group(1)
            fields[current] = [top.group(2).rstrip()]
            continue
        if current and (line.startswith("  ") or line.startswith("- ")):
            fields[current].append(line.rstrip())
        else:
            current = None
    return fields


def public_scope(source: Path) -> str:
    """Use the transport-neutral scope published by the public mirror."""
    try:
        index = json.loads((MEMORY / "index.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return "global"
    item = index.get("files", {}).get(source.name, {}).get("memory", {})
    return "global" if item.get("scope") == "agent:codex" else item.get("scope", "global")


def export_file(source: Path) -> str:
    frontmatter, body = split_frontmatter(source.read_text(encoding="utf-8"))
    fields = top_level_yaml(frontmatter)
    missing = [name for name in ("kind", "scope", "status") if name not in fields]
    if missing:
        raise ValueError(f"{source.name}: missing {', '.join(missing)}")
    output = ["---"]
    for name in PUBLIC_FIELDS:
        values = ["global"] if name == "scope" else fields.get(name)
        if not values:
            continue
        output.append(f"{name}: {values[0]}" if values[0] else f"{name}:")
        output.extend(values[1:])
    output.extend(
        [
            "sources:",
            "  - agent: codex",
            f'    at: "{fields.get("created", [""])[0].strip(chr(34))}"',
        ]
    )
    output.extend(["---", "", body.rstrip(), ""])
    return "\n".join(output)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out",
        type=Path,
        default=MEMORY.parent / "library" / "memory",
        help="output directory for the public memory mirror",
    )
    args = parser.parse_args()
    files = sorted(MEMORY.glob("*.md"))
    if not files:
        raise SystemExit(f"no memory files found in {MEMORY}")
    args.out.mkdir(parents=True, exist_ok=True)
    for source in files:
        target = args.out / source.name
        target.write_text(export_file(source), encoding="utf-8")
        print(f"wrote {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
