#!/usr/bin/env python3
"""Read-only gate for database work.

This script does not design a schema. It checks that a task record has the
minimum data-model admission fields before DDL is written. It never connects to
a database and never modifies files.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED = (
    ("复用结论", r"复用(结论|判断|扫描)|reuse(?:d)?\b"),
    ("表角色", r"表角色|核心实体|明细/关系|来源原始事实|规范化结果|派生统计|流程/任务|历史/审计|临时请求"),
    ("业务身份", r"业务身份|一行代表|唯一识别|primary identity"),
    ("生命周期", r"生命周期|终态|保留期限|归档|注销"),
    ("删除语义", r"删除语义|物理删除|逻辑删除|级联|置空|禁止删除"),
    ("不变量", r"不变量|invariant|业务规则"),
    ("唯一性", r"唯一(键|约束)|unique\s*(key|constraint)"),
    ("迁移", r"迁移|migration|增量脚本"),
    ("回滚", r"回滚|rollback|补偿"),
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, help="PRD, slice note, or contract file")
    args = parser.parse_args()

    if not args.path.is_file():
        print(f"BLOCK missing contract file: {args.path}")
        return 2

    try:
        text = args.path.read_text(encoding="utf-8")
    except UnicodeError:
        text = args.path.read_text(encoding="utf-8-sig")

    missing = [label for label, pattern in REQUIRED if not re.search(pattern, text, re.I)]
    if missing:
        print("BLOCK data-model contract is incomplete")
        for label in missing:
            print(f"- missing: {label}")
        print("Write the missing decisions before DDL; do not create tables first.")
        return 1

    print("PASS data-model admission fields present")
    print("Note: field presence is not proof of correctness; review the decisions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
