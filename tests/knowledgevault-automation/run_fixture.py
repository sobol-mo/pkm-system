#!/usr/bin/env python3
import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
FIXTURES_DIR = SCRIPT_DIR / "fixtures"
MANIFESTS_DIR = SCRIPT_DIR / "manifests"
DEFAULT_RUNS_DIR = Path("/home/hermes/temp/knowledgevault-automation-runs")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def snapshot_tree(root: Path) -> dict[str, dict[str, str]]:
    snapshot: dict[str, dict[str, str]] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            rel = path.relative_to(root).as_posix()
            text = read_text(path)
            snapshot[rel] = {
                "sha256": sha256_text(text),
                "content": text,
            }
    return snapshot


def ensure_seed_vault(workspace: Path) -> None:
    workspace.mkdir(parents=True, exist_ok=True)
    seed_files = {
        "PKM-idea.md": "# PKM Idea Inbox\n\n",
        "index.md": "# Index\n\n",
        "connection-map.md": "# Connection Map\n\n",
        "log.md": "# Log\n\n",
    }
    for relative_path, content in seed_files.items():
        path = workspace / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def append_thought_capture(workspace: Path, fixture: dict) -> dict:
    payload = fixture["input_payload"]
    author = payload["author"]
    text = payload["text"]
    destination = workspace / "PKM-idea.md"
    before = read_text(destination)
    entry = f"## Captured Thought\n\n- Author: {author}\n- Channel: {fixture.get('channel', 'unknown')}\n- Request: {fixture['user_request']}\n- Text: {text}\n\n"
    destination.write_text(before + entry, encoding="utf-8")
    return {
        "destination": "PKM-idea.md",
        "preserved_text": text,
        "entry": entry,
    }


def apply_fixture(workspace: Path, fixture: dict) -> dict:
    fixture_name = fixture["fixture_name"]
    workflow_class = fixture["workflow_class"]
    automation_mode = fixture["automation_mode"]

    if fixture_name == "thought-simple" and workflow_class == "thought" and automation_mode == "capture_only":
        return {
            "implementation": "deterministic_stub",
            "action": "append_to_pkm_idea",
            "details": append_thought_capture(workspace, fixture),
        }

    raise ValueError(
        f"Unsupported fixture: fixture_name={fixture_name!r}, workflow_class={workflow_class!r}, automation_mode={automation_mode!r}"
    )


def classify_diff(before: dict, after: dict) -> dict[str, list[str]]:
    before_paths = set(before)
    after_paths = set(after)
    created = sorted(after_paths - before_paths)
    removed = sorted(before_paths - after_paths)
    common = before_paths & after_paths
    modified = sorted(path for path in common if before[path]["sha256"] != after[path]["sha256"])
    untouched = sorted(path for path in common if before[path]["sha256"] == after[path]["sha256"])
    return {
        "created_files": created,
        "removed_files": removed,
        "modified_files": modified,
        "untouched_files": untouched,
    }


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a deterministic KnowledgeVault automation fixture in an isolated temp vault.")
    parser.add_argument("fixture_name", help="Fixture name under tests/knowledgevault-automation/fixtures/")
    parser.add_argument("--runs-dir", default=str(DEFAULT_RUNS_DIR), help="Directory where run artifacts are stored")
    parser.add_argument("--run-id", default=None, help="Optional stable run id to control the output directory name")
    parser.add_argument("--clean", action="store_true", help="Delete any existing output directory for this run id before execution")
    args = parser.parse_args()

    fixture_path = FIXTURES_DIR / args.fixture_name / "input.json"
    manifest_path = MANIFESTS_DIR / f"{args.fixture_name}.json"
    if not fixture_path.exists():
        raise SystemExit(f"Fixture not found: {fixture_path}")
    if not manifest_path.exists():
        raise SystemExit(f"Manifest not found: {manifest_path}")

    fixture = load_json(fixture_path)
    manifest = load_json(manifest_path)

    run_id = args.run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    runs_dir = Path(args.runs_dir).resolve()
    run_dir = runs_dir / f"{args.fixture_name}-{run_id}"
    workspace = run_dir / "workspace"

    if args.clean and run_dir.exists():
        shutil.rmtree(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)

    ensure_seed_vault(workspace)
    before = snapshot_tree(workspace)
    execution = apply_fixture(workspace, fixture)
    after = snapshot_tree(workspace)
    diff = classify_diff(before, after)

    result = {
        "fixture_name": args.fixture_name,
        "run_id": run_id,
        "run_dir": str(run_dir),
        "workspace": str(workspace),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "fixture_path": str(fixture_path),
        "manifest_path": str(manifest_path),
        "implementation": execution,
        "expected_contract_summary": {
            "expected_created_files": manifest.get("expected_created_files", []),
            "expected_modified_files": manifest.get("expected_modified_files", []),
            "expected_untouched_files": manifest.get("expected_untouched_files", []),
        },
        "before": before,
        "after": after,
        "diff": diff,
    }

    result_path = run_dir / "result.json"
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "fixture_name": args.fixture_name,
        "run_id": run_id,
        "run_dir": str(run_dir),
        "workspace": str(workspace),
        "result_path": str(result_path),
        "diff": diff,
        "implementation": execution,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
