#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

SKILL_ROOT = Path(__file__).resolve().parent.parent
CONTRACT_ROOT = SKILL_ROOT / "references" / "contracts"
DEFAULT_FIXTURE_ROOT = SKILL_ROOT / "fixtures"

SCHEMA_PATHS = {
    "pkm-knowledge-handoff.v1": CONTRACT_ROOT / "pkm-knowledge-handoff.v1.schema.json",
    "course-concepts.v1": CONTRACT_ROOT / "course-concepts.v1.schema.json",
    "pkm-knowledge-handoff-result.v1": CONTRACT_ROOT / "pkm-knowledge-handoff-result.v1.schema.json",
}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: root must be a JSON object")
    return value


def format_error(error: Any) -> str:
    path = "/".join(str(part) for part in error.absolute_path)
    return f"{path or '<root>'}: {error.message}"


def schema_errors(document: dict[str, Any], schema_version: str) -> list[str]:
    schema_path = SCHEMA_PATHS.get(schema_version)
    if schema_path is None:
        return [f"schema_version: unsupported contract {schema_version!r}"]
    validator = Draft202012Validator(load_json(schema_path), format_checker=FormatChecker())
    return [
        format_error(error)
        for error in sorted(
            validator.iter_errors(document),
            key=lambda item: (tuple(str(part) for part in item.absolute_path), item.message),
        )
    ]


def handoff_semantic_errors(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    references = document.get("payload_references")
    if not isinstance(references, list):
        return errors

    reference_ids = [item.get("reference_id") for item in references if isinstance(item, dict)]
    known_reference_ids = {item for item in reference_ids if isinstance(item, str)}
    if len(known_reference_ids) != len(reference_ids):
        errors.append("payload_references: reference_id values must be unique strings")

    payload_profile = document.get("payload_profile")
    if not isinstance(payload_profile, dict):
        return errors
    profile_version = payload_profile.get("schema_version")
    if not isinstance(profile_version, str):
        return errors

    errors.extend(schema_errors(payload_profile, profile_version))

    if profile_version == "course-concepts.v1":
        data = payload_profile.get("data")
        if isinstance(data, dict):
            if "included_identifiers" not in document:
                errors.append("payload_profile: course-concepts.v1 requires included_identifiers")
            for field in ("approved_concept_artifact_ref", "terminology_registry_ref"):
                value = data.get(field)
                if isinstance(value, str) and value not in known_reference_ids:
                    errors.append(f"payload_profile.data.{field} does not name a payload reference")
            selected = document.get("included_identifiers")
            profile_ids = data.get("included_concept_ids")
            if isinstance(selected, list) and isinstance(profile_ids, list) and selected != profile_ids:
                errors.append("payload_profile.data.included_concept_ids must exactly match included_identifiers")
    return errors


def validate_document(document: dict[str, Any]) -> list[str]:
    schema_version = document.get("schema_version")
    if not isinstance(schema_version, str):
        return ["schema_version: required string"]

    errors = schema_errors(document, schema_version)
    if schema_version == "pkm-knowledge-handoff.v1":
        errors.extend(handoff_semantic_errors(document))
    return sorted(set(errors))


def validate_fixture_tree(fixture_root: Path = DEFAULT_FIXTURE_ROOT) -> dict[str, Any]:
    report: dict[str, Any] = {
        "positive": 0,
        "negative": 0,
        "unexpected_passes": [],
        "unexpected_failures": {},
    }
    for expected in ("positive", "negative"):
        for path in sorted((fixture_root / expected).glob("*.json")):
            report[expected] += 1
            errors = validate_document(load_json(path))
            relative = str(path.relative_to(fixture_root))
            if expected == "positive" and errors:
                report["unexpected_failures"][relative] = errors
            elif expected == "negative" and not errors:
                report["unexpected_passes"].append(relative)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate PKM knowledge handoff contracts")
    parser.add_argument("documents", nargs="*", type=Path, help="JSON envelope or result documents")
    parser.add_argument("--fixtures", action="store_true", help="Validate bundled positive and negative fixtures")
    args = parser.parse_args()

    if args.fixtures:
        report = validate_fixture_tree()
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1 if report["unexpected_passes"] or report["unexpected_failures"] else 0

    if not args.documents:
        parser.error("provide at least one document or --fixtures")

    failed = False
    for path in args.documents:
        try:
            errors = validate_document(load_json(path))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors = [str(exc)]
        if errors:
            failed = True
            print(f"FAIL {path}")
            for error in errors:
                print(f"  {error}")
        else:
            print(f"PASS {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
