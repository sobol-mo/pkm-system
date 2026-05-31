#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def iter_md_files(path: Path):
    return sorted(p for p in path.rglob("*.md") if p.is_file())


def extract_links(text: str):
    return [m.group(1).strip() for m in MD_LINK_RE.finditer(text)]


def is_external(target: str) -> bool:
    return target.startswith(("http://", "https://", "mailto:", "#", "data:"))


def resolve_target(base: Path, target: str) -> Path:
    clean = target.split("#", 1)[0].split("?", 1)[0]
    return (base.parent / clean).resolve()


def resolve_root(cli_value: str | None) -> Path:
    if cli_value:
        return Path(cli_value).expanduser().resolve()
    env_value = os.environ.get("PKM_VAULT_PATH") or os.environ.get("OBSIDIAN_VAULT_PATH")
    if env_value:
        return Path(env_value).expanduser().resolve()
    return Path.home().joinpath("KnowledgeVault").resolve()


def detect_layout(root: Path) -> str:
    if (root / "sources").is_dir() and (root / "raw").is_dir():
        return "vault"
    if (root / "wiki" / "sources").is_dir() and (root / "raw").is_dir():
        return "legacy-repo"
    raise ValueError(f"Cannot detect PKM link layout under {root}")


def layout_paths(root: Path, layout: str):
    if layout == "vault":
        return root / "sources", root / "raw", root / "assets" / "raw"
    return root / "wiki" / "sources", root / "raw", root / "raw" / "assets"


def expected_source_to_raw(layout: str) -> str:
    return "../raw/" if layout == "vault" else "../../raw/"


def expected_source_to_assets(layout: str) -> str:
    return "../assets/raw/" if layout == "vault" else "../../raw/assets/"


def expected_raw_to_sources(layout: str) -> str:
    return "../sources/" if layout == "vault" else "../wiki/sources/"


def rel_for_report(path: Path, root: Path) -> Path:
    try:
        return path.relative_to(root)
    except ValueError:
        return path


def check(root: Path, layout: str):
    issues: list[str] = []
    source_root, raw_root, _ = layout_paths(root, layout)
    source_to_raw = expected_source_to_raw(layout)
    source_to_assets = expected_source_to_assets(layout)
    raw_to_sources = expected_raw_to_sources(layout)

    for path in iter_md_files(source_root):
        text = path.read_text(encoding="utf-8")
        rel = rel_for_report(path, root)

        if layout == "legacy-repo":
            if "(../raw/" in text:
                issues.append(f"BAD_PATH {rel}: uses ../raw/ from wiki/sources; expected ../../raw/")
            if "(../raw/assets/" in text:
                issues.append(f"BAD_PATH {rel}: uses ../raw/assets/ from wiki/sources; expected ../../raw/assets/")
        else:
            if "(../../raw/" in text:
                issues.append(f"BAD_PATH {rel}: uses ../../raw/ from sources/; expected ../raw/")
            if "(../../raw/assets/" in text:
                issues.append(f"BAD_PATH {rel}: uses ../../raw/assets/ from sources/; expected ../assets/raw/")

        for target in extract_links(text):
            if is_external(target):
                continue
            if target.startswith(source_to_raw) or target.startswith(source_to_assets):
                resolved = resolve_target(path, target)
                if not resolved.exists():
                    issues.append(f"MISSING_TARGET {rel}: {target} -> {resolved}")

    for path in iter_md_files(raw_root):
        text = path.read_text(encoding="utf-8")
        rel = rel_for_report(path, root)
        if layout == "vault" and "(assets/" in text:
            issues.append(f"BAD_PATH {rel}: uses assets/ from raw/; expected ../assets/raw/")

        for target in extract_links(text):
            if is_external(target):
                continue
            if layout == "vault" and target.startswith("assets/"):
                resolved = resolve_target(path, target)
                issues.append(f"BAD_PATH {rel}: uses {target}; expected ../assets/raw/{Path(target).name}")
                if not resolved.exists():
                    issues.append(f"MISSING_TARGET {rel}: {target} -> {resolved}")
                continue
            if target.startswith(raw_to_sources) or target.startswith("../wiki/sources/") or target.startswith("../sources/") or (layout == "vault" and target.startswith("../assets/raw/")):
                resolved = resolve_target(path, target)
                if not resolved.exists():
                    issues.append(f"MISSING_TARGET {rel}: {target} -> {resolved}")

    return issues


def fix(root: Path, layout: str):
    changed: list[Path] = []
    source_root, raw_root, _ = layout_paths(root, layout)

    for path in iter_md_files(source_root):
        text = path.read_text(encoding="utf-8")
        new_text = text
        if layout == "legacy-repo":
            new_text = new_text.replace("(../raw/assets/", "(../../raw/assets/")
            new_text = new_text.replace("(../raw/", "(../../raw/")
        else:
            new_text = new_text.replace("(../../raw/assets/", "(../assets/raw/")
            new_text = new_text.replace("(../../raw/", "(../raw/")
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed.append(path)

    if layout == "vault":
        for path in iter_md_files(raw_root):
            text = path.read_text(encoding="utf-8")
            new_text = text.replace("(../wiki/sources/", "(../sources/")
            new_text = new_text.replace("(assets/", "(../assets/raw/")
            if new_text != text:
                path.write_text(new_text, encoding="utf-8")
                changed.append(path)

    return sorted(set(changed))


def main() -> int:
    parser = argparse.ArgumentParser(description="Check/fix PKM raw<->source relative link conventions.")
    parser.add_argument("root", nargs="?", help="Canonical vault root or legacy PKM repo root")
    parser.add_argument("--fix", action="store_true", help="rewrite known bad raw/source relative paths for the detected layout")
    args = parser.parse_args()

    root = resolve_root(args.root)
    layout = detect_layout(root)

    if args.fix:
        changed = fix(root, layout)
        for path in changed:
            print(f"FIXED {rel_for_report(path, root)}")

    issues = check(root, layout)
    if issues:
        print(f"LAYOUT {layout}")
        for issue in issues:
            print(issue)
        return 1

    print(f"OK: raw/source links passed ({layout})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
