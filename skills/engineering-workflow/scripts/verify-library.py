"""Read-only health check for the Magpie engineering library.

Checks the library definition, generated Codex instructions, and skill copies.
It never edits files, runs agents, or tests MCP connectivity. Exit code 0
means no structural errors were found.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


MAGPIE_HOME = Path.home() / ".config" / "magpie"
LIBRARY = MAGPIE_HOME / "library"
CODEX_HOME = Path.home() / ".codex"
BEGIN = "<!-- magpie:begin"
END = "<!-- magpie:end -->"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def skill_files(root: Path) -> list[Path]:
    return [
        item
        for item in root.rglob("*")
        if item.is_file()
        and not any(part in {".git", "node_modules", "__pycache__"} for part in item.parts)
    ]


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    checks: list[str] = []

    library_json = MAGPIE_HOME / "library.json"
    if not library_json.is_file():
        print("ERROR library.json not found")
        return 1
    try:
        data = json.loads(library_json.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"ERROR library.json is not valid JSON: {exc}")
        return 1
    checks.append("library.json parses")

    for key in ("skills", "mcp"):
        value = data.get(key, [])
        if not isinstance(value, list) or not value:
            errors.append(f"library.json: {key} is missing or empty")
    checks.append("library.json has skills and MCP")

    applied = data.get("applied", {}).get("codex", {})
    if not applied.get("instructions"):
        warnings.append("Codex instructions are not marked applied")

    library_instructions = LIBRARY / "instructions.md"
    agents_md = CODEX_HOME / "AGENTS.md"
    if not library_instructions.is_file():
        errors.append("library/instructions.md is missing")
    elif not agents_md.is_file():
        errors.append("~/.codex/AGENTS.md is missing")
    else:
        library_text = library_instructions.read_text(encoding="utf-8").strip()
        agents_text = agents_md.read_text(encoding="utf-8")
        match = re.search(re.escape(BEGIN) + r".*?" + re.escape(END), agents_text, re.S)
        if not match:
            errors.append("~/.codex/AGENTS.md has no Magpie instruction block")
        else:
            block = match.group(0)
            body = block[block.find("# 通用协作约定"):]
            body = body[: body.rfind(END)].strip()
            digest = hashlib.sha256(body.encode("utf-8")).hexdigest()[:16]
            if body != library_text:
                errors.append("Codex instructions differ from library/instructions.md")
            elif applied.get("instrHash") and applied["instrHash"] != digest:
                errors.append("applied.instrHash does not match the instruction body")
            else:
                checks.append(f"instructions synced (hash {digest})")

    source_skills = LIBRARY / "skills"
    if not source_skills.is_dir():
        errors.append("library/skills is missing")
    else:
        # Skills land where the library is configured to put them: ~/.agents/skills
        # when shared, otherwise each agent's own skills directory (Codex checked here).
        if data.get("sharedSkills"):
            target_skills = Path.home() / ".agents" / "skills"
            target_label = "~/.agents/skills (shared)"
        else:
            target_skills = CODEX_HOME / "skills"
            target_label = "~/.codex/skills"
        if not target_skills.is_dir():
            errors.append(f"{target_label} is missing")
        else:
            missing = 0
            changed = 0
            for source in skill_files(source_skills):
                target = target_skills / source.relative_to(source_skills)
                if not target.is_file():
                    missing += 1
                elif sha256(source) != sha256(target):
                    changed += 1
            if missing or changed:
                errors.append(
                    f"skill copies differ in {target_label}: {missing} missing, {changed} changed"
                )
            else:
                checks.append(f"all skill copies match the library in {target_label}")

    print("Magpie library health check")
    print("=" * 32)
    for item in checks:
        print(f"OK   {item}")
    for item in warnings:
        print(f"WARN {item}")
    for item in errors:
        print(f"FAIL {item}")
    print()
    print(f"{len(checks)} checks passed, {len(warnings)} warnings, {len(errors)} errors")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
