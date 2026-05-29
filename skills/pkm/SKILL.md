---
name: pkm
description: Use when working in a PKM or Digital Mind context. Route between ingest, query, lint, and boundary decisions; load project context before acting.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [pkm, digital-mind, routing, orchestration, wiki]
    related_skills: [pkm-ingest, pkm-query, pkm-lint, multimodal-source-ingest, pkm-system-boundaries, obsidian]
---

# PKM

## Overview

Front door for PKM and Digital Mind work.
Use this skill to decide whether the request is ingest, query, lint, or architecture-boundary work, and to force the minimum project-context read before acting.

## When to Use

Use this skill when:
- the user asks about the PKM, wiki, Digital Mind, personal ontology, or source ingestion
- a message lands in the PKM workstream and you need to choose the right sub-workflow
- the request could be query, ingest, lint, or system-boundary work

Do not use this skill when:
- the task is general file editing outside PKM context
- the user asks only about Hermes Agent configuration with no PKM angle

## Session Start Checklist

Before acting in a PKM project, read:
1. project AGENTS.md
2. `index.md` from the resolved canonical vault path
3. last recent entries in `log.md` from the resolved canonical vault path
4. BACKLOG.md

If already read in the current turn, do not repeat.

## Routing Rules

- New source, link, forward, quote, screenshot, attachment, "ingest", "добавь в wiki" -> pkm-ingest
- Multimodal source where meaning lives in screenshots, slides, or infographics -> multimodal-source-ingest plus pkm-ingest contract
- "Что мы знаем", "расскажи про", retrieval from existing wiki -> pkm-query
- "Проверь wiki", "lint", consistency audit, orphan-page detection -> pkm-lint
- Questions about repo shape, git vs state, system vs content boundaries -> pkm-system-boundaries
- Low-level vault operations -> obsidian

## Multi-message Pattern

In this PKM workflow, user commentary may arrive before the actual forwarded source.
Treat the first message as context and wait for the actual source content if it is clearly still coming in the same turn.
Do not ingest commentary alone unless the user explicitly says the comment itself is the source.

## Decision Notes

- Prefer existing pages over near-duplicates.
- Treat raw capture and curated vault knowledge as different layers.
- If the task is both generic ingest and multimodal ingest, pkm-ingest provides the base contract and multimodal-source-ingest adds image-specific handling.
- If a session asks about why the PKM/wiki/vault is shaped this way by design, consult references/design-lineage.md first.
- Native note-taking skills are now the active PKM workflow surface; legacy oc-skills/pkm should be treated as deprecated breadcrumbs, not the primary operating layer.

## Support Files

- references/design-lineage.md — provenance note for the PKM architecture: Karpathy gist as conceptual origin, llm-wiki-karpathy as the working reference implementation, myPKA as comparative but not foundational.
- references/folder-philosophy.md — why the wiki uses type-based folders (not topic-based), how MOC complements the system, and the dual navigation model for agents and users.

## Common Pitfalls

1. Starting edits before reading project context.
2. Treating a query as an ingest and creating new pages without need.
3. Forgetting that multimodal posts need image-derived content preserved.
4. Mixing PKM system-architecture work with knowledge-state work.

## Verification Checklist

- [ ] Correct sub-skill selected
- [ ] AGENTS/index/log/BACKLOG checked when entering PKM context
- [ ] Raw vs wiki vs system-boundary distinction kept explicit
- [ ] No unnecessary new pages created during query-only work
