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


def is_backup(path: Path) -> bool:
    return path.name.endswith((".bak", "~"))


def skill_files(root: Path) -> list[Path]:
    return [
        item
        for item in root.rglob("*")
        if item.is_file()
        and not is_backup(item)
        and not any(part in {".git", "node_modules", "__pycache__"} for part in item.parts)
    ]


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.startswith((" ", "\t")):
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip("\"'")
    return fields


def markdown_links(text: str) -> list[str]:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`]*`", "", text)
    return [
        match.group(1).strip()
        for match in re.finditer(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", text)
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
        match = re.search(re.escape(BEGIN) + r"[^\r\n]*-->\r?\n(.*?)" + re.escape(END), agents_text, re.S)
        if not match:
            errors.append("~/.codex/AGENTS.md has no Magpie instruction block")
        else:
            body = match.group(1).strip()
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

        skill_dirs = {
            item.name
            for item in source_skills.iterdir()
            if item.is_dir() and (item / "SKILL.md").is_file()
        }
        declared_names = [
            item.get("name") for item in data.get("skills", []) if item.get("name")
        ]
        declared = set(declared_names)
        if len(declared_names) != len(declared):
            errors.append("library.json contains duplicate skill names")
        if skill_dirs != declared:
            errors.append(
                "library.json skill list differs from skills/ directories: "
                f"missing={sorted(skill_dirs - declared)}, extra={sorted(declared - skill_dirs)}"
            )
        else:
            checks.append(f"library.json lists all {len(skill_dirs)} skills")

        backups = [
            item for item in source_skills.rglob("*") if item.is_file() and is_backup(item)
        ]
        if backups:
            warnings.append(
                f"backup files remain under skills/ ({len(backups)}); move them out before sync"
            )

        external = {
            item.get("name")
            for item in data.get("skills", [])
            if item.get("name") and item.get("source")
        }
        seen_names: set[str] = set()
        malformed: list[str] = []
        long_descriptions: list[str] = []
        link_errors: list[str] = []
        link_count = 0
        for skill_dir in sorted(source_skills.iterdir()):
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.is_file():
                continue
            text = skill_md.read_text(encoding="utf-8")
            fields = frontmatter(text)
            name = fields.get("name", "")
            description = fields.get("description", "")
            if name != skill_dir.name:
                malformed.append(f"{skill_dir.name}: name is {name!r}")
            if not description:
                malformed.append(f"{skill_dir.name}: missing description")
            elif skill_dir.name not in external and len(description) > 800:
                long_descriptions.append(f"{skill_dir.name}: {len(description)} chars")
            if name in seen_names:
                malformed.append(f"{skill_dir.name}: duplicate name {name!r}")
            seen_names.add(name)

        for markdown in sorted(source_skills.rglob("*.md")):
            rel = markdown.relative_to(source_skills).as_posix()
            for target in markdown_links(markdown.read_text(encoding="utf-8")):
                if target.startswith(("http://", "https://", "#", "mailto:", "codex:", "file:")):
                    continue
                if any(char in target for char in "<>{}"):
                    continue
                if target in {"URL", "direct-URL"} or target.startswith("/") or re.match(
                    r"^[A-Za-z]:", target
                ):
                    continue
                target_path = target.split("#", 1)[0]
                if not target_path:
                    continue
                link_count += 1
                if not (markdown.parent / target_path).exists():
                    link_errors.append(f"{rel} -> {target}")

        if malformed:
            errors.extend(f"skill frontmatter: {item}" for item in malformed)
        else:
            checks.append("skill frontmatter names match directories")
        if long_descriptions:
            warnings.append(
                "skill descriptions above 800 chars: " + ", ".join(long_descriptions)
            )
        if link_errors:
            errors.extend(f"broken relative link: {item}" for item in link_errors)
        else:
            checks.append(f"relative links resolve ({link_count} checked)")

        inline_credentials = []
        for server in data.get("mcp", []):
            headers = server.get("headers", {})
            if not isinstance(headers, dict):
                continue
            for key, value in headers.items():
                if (
                    key.lower() == "authorization"
                    and isinstance(value, str)
                    and "{{" not in value
                    and re.search(r"\bBearer\s+[A-Za-z0-9._-]{20,}", value)
                ):
                    inline_credentials.append(server.get("name", "<unnamed>"))
        if inline_credentials:
            warnings.append(
                "MCP headers contain inline credentials (move to Magpie placeholders): "
                + ", ".join(sorted(set(inline_credentials)))
            )

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
