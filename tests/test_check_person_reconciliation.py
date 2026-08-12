import importlib.util
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "pkm-ingest"
    / "scripts"
    / "check_person_reconciliation.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("check_person_reconciliation", SCRIPT_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def make_person(vault, slug="author"):
    people = vault / "people"
    people.mkdir(parents=True)
    page = people / f"{slug}.md"
    page.write_text(
        "---\ntitle: Author\ntype: person\n---\n\n# Author\n\n## Relations\n",
        encoding="utf-8",
    )
    return page


def test_valid_manifest_requires_page_and_source_link(tmp_path):
    module = load_module()
    vault = tmp_path / "vault"
    make_person(vault)
    source = vault / "sources" / "lecture.md"
    source.parent.mkdir()
    source.write_text(
        "# Lecture\n\n## Relations\n\n- --authored_by--> [Author](../people/author.md)\n",
        encoding="utf-8",
    )
    manifest = {
        "declared_person_count": 1,
        "people": [
            {
                "name": "Author",
                "role": "speaker",
                "resolution": "created",
                "page": "people/author.md",
                "evidence": "00:01",
            }
        ],
    }

    assert module.validate_manifest(manifest, vault, source) == []


def test_missing_person_page_fails(tmp_path):
    module = load_module()
    vault = tmp_path / "vault"
    source = vault / "sources" / "lecture.md"
    source.parent.mkdir(parents=True)
    source.write_text("# Lecture\n", encoding="utf-8")
    manifest = {
        "declared_person_count": 1,
        "people": [
            {
                "name": "Missing",
                "role": "explicitly-mentioned",
                "resolution": "created",
                "page": "people/missing.md",
                "evidence": "03:14",
            }
        ],
    }

    errors = module.validate_manifest(manifest, vault, source)
    assert "missing person page: people/missing.md" in errors


def test_deferred_person_requires_reason(tmp_path):
    module = load_module()
    vault = tmp_path / "vault"
    source = vault / "sources" / "lecture.md"
    source.parent.mkdir(parents=True)
    source.write_text("# Lecture\n", encoding="utf-8")
    manifest = {
        "declared_person_count": 1,
        "people": [
            {
                "name": "Ambiguous Name",
                "role": "explicitly-mentioned",
                "resolution": "deferred",
                "evidence": "damaged ASR at 10:00",
            }
        ],
    }

    errors = module.validate_manifest(manifest, vault, source)
    assert "people[0].defer_reason is required for deferred people" in errors
