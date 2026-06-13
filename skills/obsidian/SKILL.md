---
name: obsidian
description: Read, search, create, and edit notes in the Obsidian vault.
platforms: [linux, macos, windows]
---

# Obsidian Vault

Use this skill for filesystem-first Obsidian vault work: reading notes, listing notes, searching note files, creating notes, appending content, and adding wikilinks.

## Vault path

Use a known or resolved vault path before calling file tools.

The documented vault-path convention is:

1. `PKM_VAULT_PATH`
2. `OBSIDIAN_VAULT_PATH` as a secondary compatibility fallback for Obsidian-specific workflows
3. fallback default: `~/KnowledgeVault`

File tools do not expand shell variables. Do not pass paths containing `$PKM_VAULT_PATH` or `$OBSIDIAN_VAULT_PATH` to file tools; resolve the vault path first and pass a concrete absolute path. Vault paths may contain spaces, which is another reason to prefer file tools over shell commands.

If the vault path is unknown, `terminal` is acceptable for resolving `PKM_VAULT_PATH`, then `OBSIDIAN_VAULT_PATH`, or checking whether the fallback path exists. Once the path is known, switch back to file tools.

## Read a note

Use `read_file` with the resolved absolute path to the note. Prefer this over `cat` because it provides line numbers and pagination.

## List notes

Use `search_files` with `target: "files"` and the resolved vault path. Prefer this over `find` or `ls`.

- To list all markdown notes, use `pattern: "*.md"` under the vault path.
- To list a subfolder, search under that subfolder's absolute path.

## Search

Use `search_files` for both filename and content searches. Prefer this over `grep`, `find`, or `ls`.

- For filenames, use `search_files` with `target: "files"` and a filename `pattern`.
- For note contents, use `search_files` with `target: "content"`, the content regex as `pattern`, and `file_glob: "*.md"` when you want to restrict matches to markdown notes.

## Create a note

Use `write_file` with the resolved absolute path and the full markdown content. Prefer this over shell heredocs or `echo` because it avoids shell quoting issues and returns structured results.

### YAML frontmatter for Obsidian properties

If a note uses frontmatter, it must be valid YAML or Obsidian will show the block as plain text instead of properties.

Rules:
- Wrap string values in quotes when they contain `:` or other YAML-sensitive characters. Example: `title: "AI Agents: The Illustrated Guidebook"`.
- If Obsidian stops recognizing `url`, `tags`, or other properties, suspect broken frontmatter first, not an Obsidian indexing issue.
- For notes created by ingestion workflows, prefer a quick YAML parse validation when the frontmatter was assembled manually or from extracted source text.

## Append to a note

Prefer a native file-tool workflow when it is not awkward:

- Read the target note with `read_file`.
- Use `patch` for an anchored append when there is stable context, such as adding a section after an existing heading or appending before a known trailing block.
- Use `write_file` when rewriting the whole note is clearer than constructing a fragile patch.

For an anchored append with `patch`, replace the anchor with the anchor plus the new content.

For a simple append with no stable context, `terminal` is acceptable if it is the clearest safe option.

## Targeted edits

Use `patch` for focused note changes when the current content gives you stable context. Prefer this over shell text rewriting.

## Graph-view hygiene for teaching and ontology work

When a vault is meant to be shown visually in Obsidian, separate navigation artifacts from ontology nodes.

Default rule:
- `index.md` and `glossary.md` are navigation aids, not semantic hubs
- avoid turning them into the largest graph nodes by linking them to everything unless that is explicitly desired
- prefer middle-layer organizing notes such as taxonomy nodes, technique buckets, framework buckets, or obstacle buckets
- build graph traversal as general -> intermediate -> specific rather than root -> every leaf

If the user wants these files hidden permanently from Graph View, use Obsidian Settings -> Files & Links -> Excluded files and add the concrete vault-relative file or folder paths.

For whole folders, prefer plain paths such as `raw/` or `assets/raw/` rather than regex-style anchors.
For one graph session only, prefer Graph View filter queries such as `-path:"raw/"` or `-path:"assets/raw/"`.

This is a display-layer solution only. Structural cleanup still belongs in the vault graph itself.

## Wikilinks

Obsidian links notes with `[[Note Name]]` syntax. When creating notes, use these to link related content.
