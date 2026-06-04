#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
MANIFESTS_DIR = SCRIPT_DIR / "manifests"


class CheckFailure(Exception):
    pass


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def relative_file_set(paths: list[str]) -> set[str]:
    return {Path(path).as_posix() for path in paths}


def parse_frontmatter(text: str) -> set[str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return set()
    fields: set[str] = set()
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            fields.add(line.split(":", 1)[0].strip())
    return fields


def get_after_content(result: dict, relative_path: str) -> str:
    after = result["after"]
    if relative_path not in after:
        raise CheckFailure(f"Missing file in after-snapshot: {relative_path}")
    return after[relative_path]["content"]


def validate_manifest_shape(manifest: dict) -> list[str]:
    required = [
        "fixture_name",
        "workflow_class",
        "automation_mode",
        "expected_created_files",
        "expected_modified_files",
        "expected_untouched_files",
        "required_frontmatter",
        "required_relations",
        "surface_expectations",
        "prohibited_outcomes",
        "pass_criteria",
    ]
    failures = []
    for field in required:
        if field not in manifest:
            failures.append(f"Manifest missing required field: {field}")
    return failures


def check_expected_file_sets(manifest: dict, result: dict) -> list[str]:
    failures = []
    diff = result["diff"]
    actual_created = relative_file_set(diff["created_files"])
    actual_modified = relative_file_set(diff["modified_files"])
    actual_untouched = relative_file_set(diff["untouched_files"])

    expected_created = relative_file_set(manifest["expected_created_files"])
    expected_modified = relative_file_set(manifest["expected_modified_files"])
    expected_untouched = relative_file_set(manifest["expected_untouched_files"])

    if actual_created != expected_created:
        failures.append(f"Created files mismatch: expected {sorted(expected_created)}, got {sorted(actual_created)}")
    if actual_modified != expected_modified:
        failures.append(f"Modified files mismatch: expected {sorted(expected_modified)}, got {sorted(actual_modified)}")
    if not expected_untouched.issubset(actual_untouched):
        missing = sorted(expected_untouched - actual_untouched)
        failures.append(f"Expected untouched files changed unexpectedly: {missing}")
    if diff.get("removed_files"):
        failures.append(f"Files were removed unexpectedly: {diff['removed_files']}")
    return failures


def check_frontmatter(manifest: dict, result: dict) -> list[str]:
    failures = []
    for relative_path, rules in manifest["required_frontmatter"].items():
        text = get_after_content(result, relative_path)
        fields = parse_frontmatter(text)
        required_fields = set(rules.get("required_fields", []))
        forbidden_fields = set(rules.get("forbidden_fields", []))
        missing = sorted(required_fields - fields)
        present_forbidden = sorted(forbidden_fields & fields)
        if missing:
            failures.append(f"Missing frontmatter fields in {relative_path}: {missing}")
        if present_forbidden:
            failures.append(f"Forbidden frontmatter fields present in {relative_path}: {present_forbidden}")
    return failures


def check_relations(manifest: dict, result: dict) -> list[str]:
    failures = []
    for rule in manifest["required_relations"]:
        text = get_after_content(result, rule["path"])
        for needle in rule["must_contain"]:
            if needle not in text:
                failures.append(f"Required relation text missing in {rule['path']}: {needle}")
    return failures


def check_surface_expectations(manifest: dict, result: dict) -> list[str]:
    failures = []
    modified = relative_file_set(result["diff"]["modified_files"])
    mapping = {
        "index": "index.md",
        "connection_map": "connection-map.md",
        "log": "log.md",
    }
    for surface_key, relative_path in mapping.items():
        expectation = manifest["surface_expectations"][surface_key]
        changed = relative_path in modified
        if expectation == "must_change" and not changed:
            failures.append(f"Surface file did not change as required: {relative_path}")
        if expectation == "must_not_change" and changed:
            failures.append(f"Surface file changed but must not change: {relative_path}")
    return failures


def check_thought_simple_specifics(manifest: dict, result: dict, fixture: dict) -> list[str]:
    failures = []
    if manifest["fixture_name"] != "thought-simple":
        return failures

    thought_text = fixture["input_payload"]["text"]
    pkm_idea = get_after_content(result, "PKM-idea.md")

    if thought_text not in pkm_idea:
        failures.append("Original thought text does not appear in PKM-idea.md")

    created_or_modified = relative_file_set(result["diff"]["created_files"] + result["diff"]["modified_files"])
    forbidden_prefixes = ("sources/", "raw/", "people/", "concepts/")
    unexpected_entities = sorted(path for path in created_or_modified if path.startswith(forbidden_prefixes))
    if unexpected_entities:
        failures.append(f"Curated entity files changed unexpectedly: {unexpected_entities}")

    if re.search(r"https?://", pkm_idea):
        failures.append("PKM-idea.md contains an invented URL for thought-simple")

    if "publication date" in pkm_idea.lower() or "дата публикации" in pkm_idea.lower():
        failures.append("PKM-idea.md contains publication-date language for thought-simple")

    exact_text_label = f"- Text: {thought_text}"
    if exact_text_label not in pkm_idea:
        failures.append("Thought text was not preserved verbatim under the expected capture label")

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a KnowledgeVault fixture run against its manifest.")
    parser.add_argument("fixture_name", help="Fixture name")
    parser.add_argument("run_dir", help="Run directory produced by run_fixture.py")
    args = parser.parse_args()

    manifest_path = MANIFESTS_DIR / f"{args.fixture_name}.json"
    fixture_path = SCRIPT_DIR / "fixtures" / args.fixture_name / "input.json"
    result_path = Path(args.run_dir).resolve() / "result.json"

    if not manifest_path.exists():
        raise SystemExit(f"Manifest not found: {manifest_path}")
    if not fixture_path.exists():
        raise SystemExit(f"Fixture not found: {fixture_path}")
    if not result_path.exists():
        raise SystemExit(f"Run result not found: {result_path}")

    manifest = load_json(manifest_path)
    fixture = load_json(fixture_path)
    result = load_json(result_path)

    failures = []
    failures.extend(validate_manifest_shape(manifest))
    failures.extend(check_expected_file_sets(manifest, result))
    failures.extend(check_frontmatter(manifest, result))
    failures.extend(check_relations(manifest, result))
    failures.extend(check_surface_expectations(manifest, result))
    failures.extend(check_thought_simple_specifics(manifest, result, fixture))

    output = {
        "fixture_name": args.fixture_name,
        "run_dir": str(Path(args.run_dir).resolve()),
        "result_path": str(result_path),
        "passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
        "checked_pass_criteria": manifest["pass_criteria"],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
