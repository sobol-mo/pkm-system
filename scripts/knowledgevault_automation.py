#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class CaptureRequest:
    workflow_class: str
    automation_mode: str
    user_request: str
    text: str
    author: str
    language: str
    channel: str = "unknown"


@dataclass
class CaptureResult:
    implementation: str
    workflow_class: str
    automation_mode: str
    action: str
    destination: str
    preserved_text: str
    author: str
    channel: str
    entry: str


class UnsupportedWorkflowError(ValueError):
    pass


class ValidationError(ValueError):
    pass


def resolve_vault_root(cli_value: str | None) -> Path:
    if cli_value:
        return Path(cli_value).expanduser().resolve()

    env_value = os.environ.get("PKM_VAULT_PATH") or os.environ.get("OBSIDIAN_VAULT_PATH")
    if env_value:
        return Path(env_value).expanduser().resolve()

    return Path.home().joinpath("KnowledgeVault").resolve()


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_text(path: Path, content: str) -> None:
    ensure_parent(path)
    path.write_text(content, encoding="utf-8")


def normalize_append_only_markdown(text: str) -> str:
    stripped = text.rstrip()
    return stripped + "\n\n" if stripped else ""


def append_unique_line(path: Path, line: str) -> bool:
    content = read_text(path)
    if line in content:
        return False
    updated = normalize_append_only_markdown(content) + line + "\n"
    write_text(path, updated)
    return True


def append_block(path: Path, block: str) -> None:
    content = read_text(path)
    updated = normalize_append_only_markdown(content) + block.rstrip() + "\n"
    write_text(path, updated)


def prepend_log_block(path: Path, block: str) -> None:
    content = read_text(path)
    stripped = content.strip()
    if not stripped:
        write_text(path, block.rstrip() + "\n")
        return

    parts = content.split("---\n", 2)
    if len(parts) == 3 and content.startswith("---\n"):
        frontmatter = "---\n" + parts[1] + "---\n"
        body = parts[2].lstrip("\n")
    else:
        frontmatter = ""
        body = content.lstrip("\n")

    header, separator, remainder = body.partition("\n---\n\n")
    if separator:
        updated_body = header.rstrip() + "\n\n---\n\n" + block.rstrip() + "\n\n" + remainder.lstrip("\n")
    else:
        updated_body = body.rstrip() + "\n\n" + block.rstrip() + "\n"

    updated = frontmatter + "\n" + updated_body.lstrip("\n") if frontmatter else updated_body
    write_text(path, updated)


def append_to_pkm_idea(vault_root: Path, request: CaptureRequest) -> CaptureResult:
    destination = vault_root / "PKM-idea.md"
    ensure_parent(destination)

    if destination.exists():
        existing = normalize_append_only_markdown(read_text(destination))
    else:
        existing = "# PKM Idea Inbox\n\n"

    entry = (
        "## Captured Thought\n\n"
        f"- Author: {request.author}\n"
        f"- Channel: {request.channel}\n"
        f"- Language: {request.language}\n"
        f"- Request: {request.user_request}\n"
        f"- Text: {request.text}\n"
    )
    destination.write_text(existing + entry + "\n", encoding="utf-8")

    return CaptureResult(
        implementation="knowledgevault_automation",
        workflow_class=request.workflow_class,
        automation_mode=request.automation_mode,
        action="append_to_pkm_idea",
        destination="PKM-idea.md",
        preserved_text=request.text,
        author=request.author,
        channel=request.channel,
        entry=entry,
    )


def validate_capture_request(request: CaptureRequest) -> None:
    if not request.text.strip():
        raise ValidationError("Thought text must be non-empty")
    if not request.author.strip():
        raise ValidationError("Author must be non-empty")
    if request.workflow_class != "thought":
        raise UnsupportedWorkflowError(f"Unsupported workflow_class: {request.workflow_class}")
    if request.automation_mode != "capture_only":
        raise UnsupportedWorkflowError(f"Unsupported automation_mode for thought capture: {request.automation_mode}")


def build_capture_request_from_fixture(fixture: dict) -> CaptureRequest:
    payload = fixture.get("input_payload", {})
    return CaptureRequest(
        workflow_class=fixture["workflow_class"],
        automation_mode=fixture["automation_mode"],
        user_request=fixture["user_request"],
        text=payload["text"],
        author=payload["author"],
        language=payload.get("language", "unknown"),
        channel=fixture.get("channel", "unknown"),
    )


def build_capture_request_from_args(args: argparse.Namespace) -> CaptureRequest:
    return CaptureRequest(
        workflow_class=args.workflow_class,
        automation_mode=args.automation_mode,
        user_request=args.user_request,
        text=args.text,
        author=args.author,
        language=args.language,
        channel=args.channel,
    )


def run_capture(vault_root: Path, request: CaptureRequest) -> CaptureResult:
    validate_capture_request(request)
    return append_to_pkm_idea(vault_root, request)


def render_relations(relations: list[dict[str, str]]) -> str:
    if not relations:
        return "## Relations\n\n"
    lines = ["## Relations", ""]
    for relation in relations:
        lines.append(f"{relation['predicate']} [{relation['label']}]({relation['path']})")
    lines.append("")
    return "\n".join(lines)


def render_sections(sections: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for section in sections:
        parts.append(f"## {section['heading']}")
        parts.append("")
        body = section["body"]
        if isinstance(body, list):
            for item in body:
                parts.append(f"- {item}")
        else:
            parts.append(str(body).rstrip())
        parts.append("")
    return "\n".join(parts).rstrip() + "\n\n"


def render_thought_page(payload: dict[str, Any]) -> str:
    tags = payload.get("tags", [])
    tags_literal = json.dumps(tags, ensure_ascii=False)
    frontmatter = (
        "---\n"
        f"title: \"{payload['title']}\"\n"
        "type: thought\n"
        f"created: {payload['created']}\n"
        f"updated: {payload.get('updated', payload['created'])}\n"
        f"author: {payload.get('author', 'Maxim Sobol')}\n"
        f"source: {payload.get('source', 'Telegram message')}\n"
        f"tags: {tags_literal}\n"
        "---\n\n"
        f"# {payload['title']}\n\n"
    )
    original = "## Исходная мысль\n\n" + payload["original_thought"].rstrip() + "\n\n"
    sections = render_sections(payload.get("sections", []))
    relations = render_relations(payload.get("relations", []))
    return frontmatter + original + sections + relations


def update_index_for_thought(vault_root: Path, payload: dict[str, Any]) -> bool:
    index_path = vault_root / "index.md"
    line = f"| [{payload['slug']}](thoughts/{payload['slug']}.md) | {payload['index_summary']} |"
    return append_unique_line(index_path, line)


def update_connection_map_for_thought(vault_root: Path, payload: dict[str, Any]) -> bool:
    connection_map_path = vault_root / "connection-map.md"
    line = payload.get("connection_entry", "")
    if not line:
        return False
    return append_unique_line(connection_map_path, line)


def append_log_for_thought(vault_root: Path, payload: dict[str, Any]) -> None:
    log_path = vault_root / "log.md"
    log_payload = payload["log"]
    block_lines = [
        f"## {log_payload['date']} | {log_payload['kind']} | {log_payload['title']}",
        "",
        f"Source: {log_payload['source']}",
        "Publication date of the original source: not applicable — Maxim direct input",
        "Pages created:",
    ]
    for item in log_payload.get("pages_created", []):
        block_lines.append(f"  - {item}")
    block_lines.append("Pages updated:")
    for item in log_payload.get("pages_updated", []):
        block_lines.append(f"  - {item}")
    block_lines.append("Key additions:")
    for item in log_payload.get("key_additions", []):
        block_lines.append(f"  - {item}")
    block_lines.append("")
    block_lines.append("---")
    prepend_log_block(log_path, "\n".join(block_lines))


def validate_curated_thought_payload(payload: dict[str, Any]) -> None:
    required = [
        "slug",
        "title",
        "created",
        "original_thought",
        "sections",
        "relations",
        "index_summary",
        "connection_entry",
        "log",
    ]
    missing = [field for field in required if field not in payload]
    if missing:
        raise ValidationError(f"Curated thought payload missing required fields: {missing}")


def curate_thought(vault_root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    validate_curated_thought_payload(payload)
    thought_path = vault_root / "thoughts" / f"{payload['slug']}.md"
    page_content = render_thought_page(payload)
    write_text(thought_path, page_content)
    index_changed = update_index_for_thought(vault_root, payload)
    connection_changed = update_connection_map_for_thought(vault_root, payload)
    append_log_for_thought(vault_root, payload)
    return {
        "implementation": "knowledgevault_automation",
        "action": "curate_thought",
        "thought_path": str(thought_path),
        "index_changed": index_changed,
        "connection_map_changed": connection_changed,
        "log_appended": True,
    }


def cmd_capture(args: argparse.Namespace) -> int:
    vault_root = resolve_vault_root(args.vault_root)
    request = build_capture_request_from_args(args)
    result = run_capture(vault_root, request)
    print(json.dumps({"vault_root": str(vault_root), "result": asdict(result)}, ensure_ascii=False, indent=2))
    return 0


def cmd_curate_thought(args: argparse.Namespace) -> int:
    vault_root = resolve_vault_root(args.vault_root)
    payload_path = Path(args.payload).expanduser().resolve()
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    result = curate_thought(vault_root, payload)
    print(json.dumps({"vault_root": str(vault_root), "payload_path": str(payload_path), "result": result}, ensure_ascii=False, indent=2))
    return 0


def cmd_run_fixture(args: argparse.Namespace) -> int:
    vault_root = resolve_vault_root(args.vault_root)
    fixture_path = Path(args.fixture).expanduser().resolve()
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    request = build_capture_request_from_fixture(fixture)
    result = run_capture(vault_root, request)
    print(json.dumps({
        "fixture_path": str(fixture_path),
        "vault_root": str(vault_root),
        "result": asdict(result),
    }, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="KnowledgeVault automation entrypoint")
    subparsers = parser.add_subparsers(dest="command", required=True)

    capture = subparsers.add_parser("capture-thought", help="Capture a Maxim-originated thought into PKM-idea.md")
    capture.add_argument("--vault-root", help="Canonical vault root. Defaults to PKM_VAULT_PATH, then OBSIDIAN_VAULT_PATH, then ~/KnowledgeVault")
    capture.add_argument("--workflow-class", default="thought")
    capture.add_argument("--automation-mode", default="capture_only")
    capture.add_argument("--user-request", required=True)
    capture.add_argument("--text", required=True)
    capture.add_argument("--author", required=True)
    capture.add_argument("--language", default="unknown")
    capture.add_argument("--channel", default="unknown")
    capture.set_defaults(func=cmd_capture)

    curate = subparsers.add_parser("curate-thought", help="Create or update a curated thought page plus index/log/connection-map entries from a JSON payload")
    curate.add_argument("payload", help="Path to curated thought JSON payload")
    curate.add_argument("--vault-root", help="Canonical vault root. Defaults to PKM_VAULT_PATH, then OBSIDIAN_VAULT_PATH, then ~/KnowledgeVault")
    curate.set_defaults(func=cmd_curate_thought)

    run_fixture = subparsers.add_parser("run-fixture", help="Run a fixture input through the real automation entrypoint")
    run_fixture.add_argument("fixture", help="Path to fixture input.json")
    run_fixture.add_argument("--vault-root", help="Canonical vault root. Defaults to PKM_VAULT_PATH, then OBSIDIAN_VAULT_PATH, then ~/KnowledgeVault")
    run_fixture.set_defaults(func=cmd_run_fixture)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
