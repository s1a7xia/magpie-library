"""Compare the public GitHub mirror against the live local sources.

Checks file names and SHA-256 content for the instruction, local skill, memory,
configuration and plugin trees. It is read-only and does not contact GitHub.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def files(root: Path) -> dict[str, str]:
    result = {}
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix()
        result[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def compare(label: str, source: Path, target: Path) -> list[str]:
    source_files = files(source)
    target_files = files(target)
    missing = sorted(set(source_files) - set(target_files))
    extra = sorted(set(target_files) - set(source_files))
    changed = sorted(
        name
        for name in set(source_files) & set(target_files)
        if source_files[name] != target_files[name]
    )
    print(
        f"{label}: source={len(source_files)} target={len(target_files)} "
        f"missing={len(missing)} extra={len(extra)} changed={len(changed)}"
    )
    problems = []
    for kind, names in (("missing", missing), ("extra", extra), ("changed", changed)):
        for name in names:
            problems.append(f"{label} {kind}: {name}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mirror", type=Path)
    args = parser.parse_args()
    mirror = args.mirror.resolve()
    library = (Path.home() / ".config" / "magpie" / "library").resolve()
    problems = []
    for name in (
        "skills",
        "memory",
        "config",
        "scripts",
        "instructions",
    ):
        problems.extend(compare(name, library / name, mirror / name))
    for name in (
        "README.md",
        "USAGE.md",
        "SKILLS-DECISION.md",
        "DESIGN.md",
        "DEPENDENCIES.md",
        "ENVIRONMENT.md",
        "THIRD-PARTY.md",
        "instructions.md",
    ):
        source = library / name
        target = mirror / name
        if not target.is_file():
            problems.append(f"document missing: {name}")
        elif hashlib.sha256(source.read_bytes()).digest() != hashlib.sha256(
            target.read_bytes()
        ).digest():
            problems.append(f"document differs: {name}")
        else:
            print(f"document matches: {name}")
    if problems:
        print("\nDifferences:")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print("\nPublic mirror matches the selected local sources.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
