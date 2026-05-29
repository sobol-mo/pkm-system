#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
from pathlib import Path


TYPE_MAP = {
    "concepts": "concept",
    "implementations": "implementation",
    "people": "person",
    "quotes": "quote",
    "thoughts": "thought",
    "sources": "source",
    "analyses": "analysis",
}

SPECIAL_TYPES = {
    "index.md": "index",
    "overview.md": "overview",
    "glossary.md": "glossary",
    "log.md": "log",
    "connection-map.md": "connection-map",
    "schema.md": "schema",
}

SKIP = {"README.md"}


def resolve_vault_root(cli_value: str | None) -> Path:
    if cli_value:
        return Path(cli_value).expanduser().resolve()

    env_value = os.environ.get("PKM_VAULT_PATH") or os.environ.get("OBSIDIAN_VAULT_PATH")
    if env_value:
        return Path(env_value).expanduser().resolve()

    return Path.home().joinpath("KnowledgeVault").resolve()


def iter_md_files(vault_root: Path):
    for path in sorted(vault_root.rglob("*.md")):
        if not path.is_file() or path.name in SKIP:
            continue
        yield path


def get_type(filepath: Path, vault_root: Path) -> str:
    rel = filepath.relative_to(vault_root)
    if rel.name in SPECIAL_TYPES:
        return SPECIAL_TYPES[rel.name]
    if rel.parts:
        return TYPE_MAP.get(rel.parts[0], "unknown")
    return "unknown"


def extract_title(content: str) -> str:
    match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "Untitled"


def extract_date(content: str) -> str:
    match = re.search(r"(?:Added|Date|created|Created)[_:]\s*(\d{4}-\d{2}-\d{2})", content)
    if match:
        return match.group(1)
    return "2026-04-14"


def main() -> int:
    parser = argparse.ArgumentParser(description="Add missing frontmatter to KnowledgeVault markdown pages.")
    parser.add_argument("vault_root", nargs="?", help="Canonical vault root. Defaults to PKM_VAULT_PATH, then OBSIDIAN_VAULT_PATH, then ~/KnowledgeVault")
    args = parser.parse_args()

    vault_root = resolve_vault_root(args.vault_root)
    count = 0

    for fpath in iter_md_files(vault_root):
        content = fpath.read_text(encoding="utf-8")
        if content.startswith("---"):
            continue

        page_type = get_type(fpath, vault_root)
        title = extract_title(content)
        created = extract_date(content)

        frontmatter = f"""---
title: \"{title}\"
type: {page_type}
created: {created}
updated: 2026-04-14
sources: []
tags: []
---

"""

        fpath.write_text(frontmatter + content, encoding="utf-8")
        count += 1
        print(f"  {fpath.relative_to(vault_root)} ({page_type})")

    print(f"\nVault root: {vault_root}")
    print(f"Total: {count} pages updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
