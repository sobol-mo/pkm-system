#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, str]:
    if not text.startswith("---\n"):
        return None, text
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return None, text
    fm_text = parts[1]
    body = parts[2]
    fm: dict[str, str] = {}
    for raw_line in fm_text.splitlines():
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        fm[key.strip()] = value.strip()
    return fm, body


def iter_markdown(vault_root: Path, ignore_dirs: set[str]):
    for path in vault_root.rglob("*.md"):
        rel = path.relative_to(vault_root)
        if any(part in ignore_dirs for part in rel.parts):
            continue
        yield path, rel


def required_fields_for(doc_type: str, schema: dict[str, Any]) -> list[str]:
    specific = schema["required_frontmatter_fields"].get(doc_type)
    if specific:
        return specific
    return schema["required_frontmatter_fields"]["default"]


def score_report(report: dict[str, Any], schema: dict[str, Any]) -> int:
    weights = schema["score_weights"]
    curated = max(1, report["summary"]["curated_files"])
    penalties = 0.0
    penalties += weights["missing_frontmatter"] * min(1.0, report["counts"]["curated_missing_frontmatter"] / curated)
    penalties += weights["missing_required_fields"] * min(1.0, report["counts"]["curated_missing_required_fields"] / curated)
    penalties += weights["type_mismatch"] * min(1.0, report["counts"]["type_mismatch"] / curated)
    penalties += weights["missing_relations"] * min(1.0, report["counts"]["missing_relations"] / curated)
    penalties += weights["broken_relative_links"] * min(1.0, report["counts"]["broken_relative_links"] / curated)
    return max(0, round(100 - penalties))


def sample(items: list[Any], limit: int) -> list[Any]:
    return items[:limit]


def default_schema_path() -> Path:
    return Path(__file__).resolve().parent.parent / "references" / "operational-schema.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Operational health check for KnowledgeVault")
    parser.add_argument("vault", type=Path, help="Path to vault root")
    parser.add_argument("--schema", type=Path, default=None, help="Path to operational schema JSON")
    parser.add_argument("--json", action="store_true", help="Print full JSON report")
    parser.add_argument("--write-json", type=Path, default=None, help="Write full JSON report to path")
    args = parser.parse_args()

    vault_root = args.vault.resolve()
    schema_path = (args.schema or default_schema_path()).resolve()
    schema = load_json(schema_path)
    ignore_dirs = set(schema.get("ignore_dirs", []))
    curated_folders = schema["curated_folders"]
    special_root_files = schema["special_root_files"]
    relations_required_in = set(schema.get("relations_required_in", []))
    sample_limit = int(schema.get("report_samples_per_category", 20))

    issues: dict[str, list[Any]] = {
        "curated_missing_frontmatter": [],
        "legacy_raw_missing_frontmatter": [],
        "curated_missing_required_fields": [],
        "type_mismatch": [],
        "missing_relations": [],
        "broken_relative_links": [],
    }

    summary = {
        "total_markdown_files": 0,
        "curated_files": 0,
        "raw_files": 0,
        "root_files": 0,
        "by_topdir": {},
    }

    for path, rel in iter_markdown(vault_root, ignore_dirs):
        summary["total_markdown_files"] += 1
        top = rel.parts[0] if len(rel.parts) > 1 else "(root)"
        summary["by_topdir"][top] = summary["by_topdir"].get(top, 0) + 1

        text = path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)

        is_root = len(rel.parts) == 1
        is_raw = top == "raw"
        is_curated = top in curated_folders

        if is_root:
            summary["root_files"] += 1
        elif is_raw:
            summary["raw_files"] += 1
        elif is_curated:
            summary["curated_files"] += 1

        expected_type = None
        doc_type_for_rules = None
        if is_curated:
            expected_type = curated_folders[top]
            doc_type_for_rules = expected_type
        elif is_root and rel.name in special_root_files:
            expected_type = special_root_files[rel.name]
            doc_type_for_rules = expected_type

        if fm is None:
            if is_curated or (is_root and rel.name in special_root_files):
                issues["curated_missing_frontmatter"].append(str(rel))
            elif is_raw:
                issues["legacy_raw_missing_frontmatter"].append(str(rel))
            continue

        if doc_type_for_rules:
            required = required_fields_for(doc_type_for_rules, schema)
            missing = [field for field in required if not fm.get(field)]
            if missing:
                issues["curated_missing_required_fields"].append({"file": str(rel), "missing": missing})
            if expected_type and fm.get("type") != expected_type:
                issues["type_mismatch"].append({"file": str(rel), "expected": expected_type, "actual": fm.get("type")})

        if is_curated and top in relations_required_in and "## Relations" not in body:
            issues["missing_relations"].append(str(rel))

        for match in MD_LINK_RE.finditer(body):
            target = match.group(1).strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            target_path = (path.parent / target).resolve()
            if not target_path.exists():
                issues["broken_relative_links"].append({"file": str(rel), "target": target})

    counts = {name: len(items) for name, items in issues.items()}
    report = {
        "vault": str(vault_root),
        "schema": str(schema_path),
        "summary": summary,
        "counts": counts,
        "health_score": 0,
        "samples": {name: sample(items, sample_limit) for name, items in issues.items()},
    }
    report["health_score"] = score_report(report, schema)

    if args.write_json:
        args.write_json.parent.mkdir(parents=True, exist_ok=True)
        args.write_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    print(f"Vault: {report['vault']}")
    print(f"Operational schema: {report['schema']}")
    print(f"Health score: {report['health_score']}/100")
    print("")
    print("Summary:")
    print(f"  total markdown files: {summary['total_markdown_files']}")
    print(f"  curated files: {summary['curated_files']}")
    print(f"  raw files: {summary['raw_files']}")
    print(f"  root files: {summary['root_files']}")
    print("")
    print("Issues:")
    for key, label in [
        ("curated_missing_frontmatter", "curated files missing frontmatter"),
        ("curated_missing_required_fields", "curated files missing required fields"),
        ("type_mismatch", "folder/type mismatches"),
        ("missing_relations", "curated files missing Relations section"),
        ("broken_relative_links", "broken relative markdown links"),
        ("legacy_raw_missing_frontmatter", "legacy raw files missing frontmatter"),
    ]:
        print(f"  {label}: {counts[key]}")

    print("")
    print("Samples:")
    for key in [
        "curated_missing_frontmatter",
        "curated_missing_required_fields",
        "type_mismatch",
        "missing_relations",
        "broken_relative_links",
    ]:
        if not report["samples"][key]:
            continue
        print(f"  {key}:")
        for item in report["samples"][key][:5]:
            print(f"    - {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
