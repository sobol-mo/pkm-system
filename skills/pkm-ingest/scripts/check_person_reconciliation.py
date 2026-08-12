#!/usr/bin/env python3
"""Fail-closed validation for people mentioned during a source ingest."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ALLOWED_ROLES = {
    "speaker",
    "explicitly-mentioned",
    "attributed-researcher",
    "attribution-correction",
}
ALLOWED_RESOLUTIONS = {"existing", "created", "deferred"}
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def load_manifest(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("manifest must be a JSON object")
    return data


def validate_manifest(manifest: dict, vault_root: Path, source_page: Path) -> list[str]:
    errors: list[str] = []
    people = manifest.get("people")
    if not isinstance(people, list) or not people:
        return ["people must be a non-empty list"]

    source_text = source_page.read_text(encoding="utf-8") if source_page.exists() else ""
    if not source_page.exists():
        errors.append(f"source page does not exist: {source_page}")

    seen_names: set[str] = set()
    seen_paths: set[str] = set()
    for index, person in enumerate(people):
        prefix = f"people[{index}]"
        if not isinstance(person, dict):
            errors.append(f"{prefix} must be an object")
            continue

        name = person.get("name")
        role = person.get("role")
        resolution = person.get("resolution")
        page = person.get("page")
        evidence = person.get("evidence")

        if not isinstance(name, str) or not name.strip():
            errors.append(f"{prefix}.name must be non-empty")
        elif name.casefold() in seen_names:
            errors.append(f"duplicate person name: {name}")
        else:
            seen_names.add(name.casefold())

        if role not in ALLOWED_ROLES:
            errors.append(f"{prefix}.role is invalid: {role!r}")
        if resolution not in ALLOWED_RESOLUTIONS:
            errors.append(f"{prefix}.resolution is invalid: {resolution!r}")
        if not isinstance(evidence, str) or not evidence.strip():
            errors.append(f"{prefix}.evidence must identify a timestamp or correction source")

        if resolution == "deferred":
            reason = person.get("defer_reason")
            if not isinstance(reason, str) or not reason.strip():
                errors.append(f"{prefix}.defer_reason is required for deferred people")
            continue

        if not isinstance(page, str) or not page.startswith("people/") or not page.endswith(".md"):
            errors.append(f"{prefix}.page must be a people/*.md path")
            continue
        if page in seen_paths:
            errors.append(f"duplicate person page: {page}")
        seen_paths.add(page)

        page_path = vault_root / page
        if not page_path.is_file():
            errors.append(f"missing person page: {page}")
            continue
        page_text = page_path.read_text(encoding="utf-8")
        if "type: person" not in page_text:
            errors.append(f"person page has no type: person: {page}")
        if "## Relations" not in page_text:
            errors.append(f"person page has no Relations section: {page}")

        relative_target = Path(page).relative_to("people")
        expected_from_source = f"../people/{relative_target.as_posix()}"
        if expected_from_source not in source_text:
            errors.append(f"source page does not link person: {page}")

    declared_count = manifest.get("declared_person_count")
    if declared_count != len(people):
        errors.append(
            f"declared_person_count {declared_count!r} does not match people count {len(people)}"
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--vault-root", type=Path, required=True)
    parser.add_argument("--source-page", type=Path, required=True)
    args = parser.parse_args()

    try:
        manifest = load_manifest(args.manifest)
        errors = validate_manifest(manifest, args.vault_root, args.source_page)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, ensure_ascii=False))
        return 2

    print(
        json.dumps(
            {
                "ok": not errors,
                "declared_person_count": manifest.get("declared_person_count"),
                "errors": errors,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
