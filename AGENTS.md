# AGENTS.md — Digital Mind Project

Read this file first every session in this project.

This file is the operational bootstrap for agents. It is not the source of truth for product definition, requirements, architecture, or backlog state.

## Canonical Reading Path

For project understanding, read files in this order:

1. `Requirements/README.md` — source-of-truth map
2. `Requirements/01-vision-and-scope.md` — what the project is and why it exists
3. `Requirements/02-business-requirements.md` — Maxim's expected outcomes and business rules
4. `Requirements/03-system-requirements.md` — functional and non-functional requirements
5. `Requirements/04-domain-model.md` — domain entities, boundaries, and canonical state model
6. `Architecture/README.md` — accepted ADR index
7. `BACKLOG.md` — active and planned work items

For vault orientation during ingest/query/lint work, additionally read:

1. `index.md` in the resolved canonical vault path
2. last 5 entries in `log.md` in the resolved canonical vault path
3. `schema.md` in the resolved canonical vault path only when relation types, entity types, or page format are relevant

Canonical vault-path contract:

1. `PKM_VAULT_PATH`
2. `OBSIDIAN_VAULT_PATH` only as a secondary compatibility fallback for Obsidian-specific workflows
3. fallback default: `$HOME/KnowledgeVault`

## Project Summary

Name: **Digital Mind**.

Technical name: **Personal Ontology**.

Core purpose: preserve and operate on Maxim's worldview as a typed, temporal network of concepts and relationships.

Core hypothesis:

```text
personality = concepts + typed relationships between concepts + temporal evolution
```

Do not expand this summary here. Update `Requirements/` when project meaning changes.

## Agent Role

You are the wiki maintainer and project-structure assistant for Maxim's Digital Mind project.

Your responsibilities:

- maintain clear separation between raw input, curated wiki knowledge, requirements, architecture decisions, backlog state, and runtime artifacts
- ingest sources into the wiki when asked
- answer queries from curated wiki content with references
- flag contradictions before changing curated knowledge
- improve project structure only by updating the correct canonical file type

## Source-of-Truth Boundaries

| Concern | File/Directory |
|---------|----------------|
| Project definition | `Requirements/01-vision-and-scope.md` |
| Business intent | `Requirements/02-business-requirements.md` |
| System behavior | `Requirements/03-system-requirements.md` |
| Domain model | `Requirements/04-domain-model.md` |
| Architecture decisions | `Architecture/` |
| PKM-specific skills | `skills/` |
| Active work state | `BACKLOG.md` |
| Raw idea dump | `PKM-idea.md` |
| Raw source evidence | `raw/` under the resolved canonical vault path |
| Curated knowledge | entity folders and root files under the resolved canonical vault path |

Migration note:

- repo-local `/home/maxim/dev/projects/agents-projects/pkm-system/raw/` is now a frozen legacy mirror/reference set, not the preferred canonical write target
- repo-local `/home/maxim/dev/projects/agents-projects/pkm-system/wiki/` is now a frozen legacy mirror/reference set, not the preferred canonical write target
- normal ingest and wiki maintenance should write to the resolved canonical vault path, not to repo-local `raw/` or `wiki/`

## Workflow References

PKM-specific skills are project-owned system assets. The canonical source location is `skills/`, as defined in `Architecture/ADR-002-project-owned-agent-skills.md`.

Current project-owned skill set:

- `skills/pkm/`
- `skills/pkm-ingest/`
- `skills/pkm-query/`
- `skills/pkm-lint/`
- `skills/multimodal-source-ingest/`
- `skills/pkm-system-boundaries/`
- `skills/obsidian/`
- `skills/sync-vault/`

On the VPS Hermes runtime, the compatibility paths under `~/.hermes/skills/note-taking/` are symlink bridges back to these project directories.

For agents working directly in the project clone, `skills/` should be treated as the skill root. Do not assume the Hermes runtime path is the source of truth.

## Session Start Checklist

1. Read this file.
2. Read `Requirements/README.md`.
3. Read only the canonical files needed for the user's request.
4. For vault work, read `index.md` and the last 5 entries in `log.md` from the resolved canonical vault path.
5. Check `BACKLOG.md` only when the task involves planning, status, or next actions.

## Multi-Message Delivery Pattern

Maxim's comments may arrive before forwarded content.

First message = comment. Second message = actual source.

Do not react to the first message alone when it clearly introduces a forwarded source. Wait for content.

## General Rules

1. Maxim's voice messages and monologues go to `PKM-idea.md` as raw idea capture unless he requests formalization.
2. Never overwrite `PKM-idea.md`; append only.
3. Treat `raw/` in the canonical vault as evidence. Do not rewrite raw sources during normal wiki work.
4. Prefer updating existing wiki pages over creating new pages.
5. If a source contradicts curated wiki content, flag the contradiction before updating.
6. Keep page titles consistent with filenames in kebab-case.
7. Requirements changes belong in `Requirements/`, not in `AGENTS.md`.
8. Architecture decisions belong in ADRs, not in `Requirements/` or `BACKLOG.md`.
9. Active tasks belong in `BACKLOG.md`, not in `AGENTS.md`.
10. PKM-specific skill changes belong in `skills/`, not only in VPS runtime paths.
11. Do not use repo-local `raw/` or `wiki/` as the default write target for new canonical vault work unless rollback is explicitly active.

## Current Open Questions

Open questions are tracked in the relevant canonical documents:

- product questions: `Requirements/01-vision-and-scope.md`
- requirements questions: `Requirements/03-system-requirements.md`
- domain questions: `Requirements/04-domain-model.md`
- implementation tasks: `BACKLOG.md`
