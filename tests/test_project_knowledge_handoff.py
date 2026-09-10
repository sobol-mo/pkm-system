import importlib.util
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "project-knowledge-handoff"
SCRIPT_PATH = SKILL_ROOT / "scripts" / "validate_contracts.py"
HEALTH_CHECKER_PATH = (
    ROOT
    / "skills"
    / "schema-driven-vault-maintenance"
    / "scripts"
    / "check_vault_health.py"
)
FIXTURE_ROOT = SKILL_ROOT / "fixtures"
OPERATIONAL_SCHEMA = (
    ROOT
    / "skills"
    / "schema-driven-vault-maintenance"
    / "references"
    / "operational-schema.json"
)


def load_module():
    spec = importlib.util.spec_from_file_location("validate_contracts", SCRIPT_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_health_checker():
    spec = importlib.util.spec_from_file_location("check_vault_health", HEALTH_CHECKER_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_fixture(group: str, name: str):
    return json.loads((FIXTURE_ROOT / group / name).read_text(encoding="utf-8"))


def test_valid_handoff_fixture_passes():
    module = load_module()

    errors = module.validate_document(load_fixture("positive", "course-concepts-handoff.json"))

    assert errors == []


def test_valid_result_fixture_passes():
    module = load_module()

    errors = module.validate_document(load_fixture("positive", "handoff-result.json"))

    assert errors == []


def test_invalid_digest_fixture_fails_with_stable_error():
    module = load_module()

    errors = module.validate_document(load_fixture("negative", "handoff-invalid-digest.json"))

    assert any("payload_references/0/digest/value" in error for error in errors)


def test_course_profile_rejects_unknown_payload_reference():
    module = load_module()

    errors = module.validate_document(
        load_fixture("negative", "course-concepts-missing-reference.json")
    )

    assert "payload_profile.data.approved_concept_artifact_ref does not name a payload reference" in errors


def test_result_rejects_non_relative_read_back_path():
    module = load_module()

    errors = module.validate_document(load_fixture("negative", "result-absolute-read-back-path.json"))

    assert any("read_back_paths/0" in error for error in errors)


def test_result_rejects_parent_traversal_read_back_path():
    module = load_module()

    errors = module.validate_document(load_fixture("negative", "result-parent-traversal-path.json"))

    assert any("read_back_paths/0" in error for error in errors)


def test_course_profile_requires_explicit_identifier_selection():
    module = load_module()

    errors = module.validate_document(load_fixture("negative", "course-concepts-bounded-selection.json"))

    assert "payload_profile: course-concepts.v1 requires included_identifiers" in errors


def test_course_profile_selection_must_match_envelope_selection():
    module = load_module()

    errors = module.validate_document(load_fixture("negative", "course-concepts-selection-mismatch.json"))

    assert "payload_profile.data.included_concept_ids must exactly match included_identifiers" in errors


def test_fixture_suite_has_only_expected_outcomes():
    module = load_module()

    report = module.validate_fixture_tree(FIXTURE_ROOT)

    assert report["positive"] >= 2
    assert report["negative"] >= 2
    assert report["unexpected_passes"] == []
    assert report["unexpected_failures"] == {}


def test_operational_schema_supports_project_pages():
    schema = json.loads(OPERATIONAL_SCHEMA.read_text(encoding="utf-8"))

    assert schema["curated_folders"]["projects"] == "project"
    assert "projects" in schema["relations_required_in"]
    assert schema["required_frontmatter_fields"]["project"] == [
        "title",
        "type",
        "created",
        "updated",
        "sources",
        "tags",
        "project_id",
        "authority_refs",
    ]


def test_health_checker_recognizes_project_authority_refs_list():
    module = load_health_checker()
    frontmatter, _ = module.parse_frontmatter(
        "---\n"
        "title: Example\n"
        "type: project\n"
        "authority_refs:\n"
        "  - project-catalog.v1#example\n"
        "---\n\n"
        "## Relations\n"
    )

    assert frontmatter is not None
    assert frontmatter["authority_refs"] == ["project-catalog.v1#example"]


def test_health_checker_reports_missing_project_identity_fields(tmp_path):
    project = tmp_path / "projects" / "example.md"
    project.parent.mkdir()
    project.write_text(
        "---\n"
        "title: Example\n"
        "type: project\n"
        "created: 2026-09-10\n"
        "updated: 2026-09-10\n"
        "sources: []\n"
        "tags: []\n"
        "---\n\n"
        "## Relations\n",
        encoding="utf-8",
    )

    completed = subprocess.run(
        [sys.executable, str(HEALTH_CHECKER_PATH), str(tmp_path), "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    report = json.loads(completed.stdout)

    assert report["counts"]["curated_missing_required_fields"] == 1
    assert report["samples"]["curated_missing_required_fields"] == [
        {"file": "projects/example.md", "missing": ["project_id", "authority_refs"]}
    ]
