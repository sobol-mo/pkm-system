#!/usr/bin/env python3
"""Determine if the PKM skill bridge has drifted.

Checks whether ~/.hermes/skills/note-taking/ contains any real
(non-symlink) directories that look like PKM skills not owned by
the pkm-system project.

Exit codes:
  0 = clean (no drift) or drift alert emitted successfully
  82 = error (can't read paths)
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

BRIDGE = Path.home() / ".hermes" / "skills" / "note-taking"
PROJECT_SKILLS = (
    Path.home()
    / ".hermes"
    / "agents-projects"
    / "pkm-system"
    / "skills"
)


def resolve_symlink_target(p: Path) -> Path | None:
    try:
        return p.resolve() if p.is_symlink() else None
    except OSError:
        return None


def main() -> int:
    if not BRIDGE.is_dir():
        print(f"SKIP: {BRIDGE} does not exist")
        return 0

    if not PROJECT_SKILLS.is_dir():
        print(f"ERROR: project skills dir {PROJECT_SKILLS} not found")
        return 82

    project_skill_names: set[str] = set()
    for child in PROJECT_SKILLS.iterdir():
        if child.is_dir():
            project_skill_names.add(child.name)

    drifted: list[str] = []

    for child in sorted(BRIDGE.iterdir()):
        if child.name == "DESCRIPTION.md":
            continue
        if not child.is_dir():
            continue  # not a skill directory, skip
        if child.is_symlink():
            target = resolve_symlink_target(child)
            if target and target.parent == PROJECT_SKILLS and target.name in project_skill_names:
                continue  # valid bridge symlink
            drifted.append(f"{child.name} (symlink target not in project skills)")
        else:
            # real directory not a symlink — potential drift
            if child.name in project_skill_names:
                drifted.append(f"{child.name} (real dir, project has matching skill)")
            else:
                drifted.append(f"{child.name} (real dir, no matching project skill)")

    if not drifted:
        return 0

    print(f"DRIFT: {len(drifted)} item(s) outside pkm-system project")
    for item in drifted:
        print(f"  {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
