import importlib.util
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_pkm_drift.py"


def load_module():
    spec = importlib.util.spec_from_file_location("check_pkm_drift", SCRIPT_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_resolve_project_skills_prefers_env_binding(tmp_path, monkeypatch):
    module = load_module()
    root = tmp_path / "custom-pkm-system"
    skills = root / "skills"
    skills.mkdir(parents=True)

    monkeypatch.setenv("PKM_SYSTEM_PATH", str(root))

    assert module.resolve_project_skills() == skills


def test_resolve_project_skills_defaults_to_script_checkout(monkeypatch):
    module = load_module()

    monkeypatch.delenv("PKM_SYSTEM_PATH", raising=False)
    monkeypatch.delenv("PKM_PROJECT_ROOT", raising=False)

    assert module.resolve_project_skills() == SCRIPT_PATH.resolve().parents[1] / "skills"
