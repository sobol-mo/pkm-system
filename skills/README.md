# PKM Skills

This directory is the source of truth for the Digital Mind project skill set.

These skills are stored here so agents working directly in the project clone can load, inspect, edit, and reuse the same operational logic as the VPS Hermes runtime.

## Current Skill Set

| Skill | Purpose |
|-------|---------|
| `pkm/` | Router for PKM tasks |
| `pkm-ingest/` | Ingest raw sources into curated wiki pages |
| `pkm-query/` | Answer questions from curated wiki content |
| `pkm-lint/` | Check contradictions, stale claims, orphans, and schema consistency |
| `multimodal-source-ingest/` | Overlay for image/audio/video source ingestion |
| `pkm-system-boundaries/` | Boundary decisions between system artifacts and PKM knowledge state |
| `obsidian/` | Low-level vault filesystem operations used by PKM workflows |

## Source-of-Truth Rule

Edit these skills here first.

Runtime paths under `~/.hermes/skills/` are compatibility consumers, not canonical sources.

## Runtime Bridge Model

On the VPS Hermes runtime, the legacy paths under `~/.hermes/skills/note-taking/` are symlink bridges pointing back to these project-owned directories.

That keeps existing Hermes skill names and routing stable without duplicating files.

## Other Agent Consumption Model

Agents that operate directly on this project should treat this `skills/` directory as the canonical skill root.

If a Hermes-based agent needs these skills outside the VPS bridge layout, point its `skills.external_dirs` to this directory or create local compatibility links that resolve back here.

The goal is that project agents and Hermes runtime agents consume the same files, not copies.
