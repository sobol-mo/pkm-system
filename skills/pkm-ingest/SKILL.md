---
name: pkm-ingest
description: Use when adding a new source, thought, quote, forward, or document into a PKM wiki with raw and curated layers.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [pkm, ingest, wiki, digital-mind, ontology]
    related_skills: [pkm, multimodal-source-ingest, pkm-query, pkm-lint, obsidian]
---

# PKM Ingest

## Overview

Generic ingest contract for PKM repositories that separate raw capture from curated wiki state.
Use this for ordinary text sources and as the base contract for multimodal ingest.

For this project's current migration state, the canonical write target is the resolved `KnowledgeVault` path. Repo-local `raw/` and `wiki/` inside the project clone are legacy mirrors/reference state and should not be used as the default destination for new canonical ingest.

## When to Use

Use this skill when:
- the user sends a source, link, forward, quote, note, or text to preserve in PKM
- a raw capture and corresponding curated source page must be created or updated
- the wiki graph needs new concepts, people, implementations, thoughts, quotes, or analyses derived from a source

Prefer multimodal-source-ingest as a companion when screenshots, infographics, or image-only details carry meaning.

## Inputs and Outputs

Inputs:
- URL, pasted text, forwarded content, file, quote, thought, or voice-derived transcript
- optional framing from the user explaining why it matters

Outputs:
- one raw capture in `raw/` under the resolved canonical vault path
- one curated source page in `sources/` under the resolved canonical vault path when the vault uses that split
- updates to existing or new curated pages as needed
- updates to `index.md`, `glossary.md`, `connection-map.md`, and `log.md` when relevant
- confirmation with commit hash if the repo is git-backed and a commit is in scope

## Base Workflow

1. Read the source fully.
2. Decide whether it is a source, quote, thought, analysis seed, or mixed artifact.
3. Save the fidelity layer in `raw/` under the resolved canonical vault path.
4. Identify reusable entities and likely target pages.
5. Create or update curated wiki pages.
6. Add typed relations.
7. Add human-navigable links between raw and curated layers.
8. Update global wiki surfaces that help retrieval.
9. Verify links and changed pages.
10. Commit and push when the project workflow expects it.

## Raw Layer Rules

Raw is the capture layer.
Keep original content, source metadata, context, and any extraction notes needed for future verification.
Do not silently rewrite the source into a cleaner narrative and call that raw.
If the project treats raw as immutable after creation, preserve that rule.
Do not default to writing new canonical raw captures into repo-local `PKM/raw/` after vault cutover.

## Curated Layer Rules

Update existing pages before creating new ones.
Create new concept pages only for stable reusable concepts, not every phrase in a source.
When the source mainly adds evidence or nuance to an existing page, enrich the existing page instead of spawning a duplicate node.
Do not default to writing new canonical curated pages into repo-local `PKM/wiki/` after vault cutover.

## Required Global Updates

Check whether the ingest should update:
- `index.md`
- `glossary.md`
- `connection-map.md`
- `log.md`
- `overview.md` if the big picture changed materially

## Link Contract

For vaults with `raw/` and `sources/` split:
- source page links to raw capture
- raw capture links back to source page
- relative paths must be verified from the real file location
- if assets are stored in `assets/raw/`, source pages link there explicitly

Run the deterministic checker from multimodal-source-ingest when the active vault still uses the legacy raw/source relative-link pattern and deterministic verification is available.

## Entity Routing

Folders encode ENTITY TYPE (what a page IS), not TOPIC (what it's ABOUT). This is a deliberate design decision that prevents the multiple-belonging problem — one concept belongs to exactly one entity type, but can link to any number of topics.

| Folder | Entity Type | Goes here when... | NOT here when... |
|--------|-------------|-------------------|------------------|
| `concepts/` | Idea, definition, principle, pattern | A stable reusable idea with definition and relations | It's a specific person's implementation (→ implementations/) |
| `people/` | Person, author, thinker | Someone whose ideas, quotes, or work connects to the Digital Mind | The content is purely about their tool (→ implementations/) |
| `implementations/` | Tool, system, project, codebase | A specific working system or product that instantiates a concept | The content is just an idea about how something could work (→ concepts/) |
| `quotes/` | Verbatim quote | A quotable formulation that Maxim endorses as personality signal | A paraphrased observation (→ thoughts/ or enrich existing concept) |
| `thoughts/` | Maxim's own dated reflection | A first-person insight, opinion, or synthesis by Maxim | A third-party source (→ sources/ + concepts/) |
| `analyses/` | Comparative or synthetic study | A comparison of approaches, design decisions, or publication directions | Raw findings from a single source (→ sources/ + concepts/) |
| `sources/` | Curated summary of an external document | A complex source with multiple ideas extracted across several pages | A single idea already captured in a concept page |

### The Principle: Type over Topic

`concepts/agent-memory.md` lives in `concepts/` because it IS a concept — not because it's "about AI" (topic). The topic emerges from its links to other pages (execution-loop, digital-mind, mempalace), not from folder placement. This is the wiki's concrete implementation of the Linking Over Categorizing principle.

If you're unsure whether something belongs in `concepts/` vs `implementations/` vs `people/`, ask: "What IS this entity?" — not "What is it about?"

## Guardrails

- If the source contradicts existing wiki content, flag it before resolving.
- If entity extraction is unclear, ask the user what should be preserved rather than inventing ontology.
- If a fetch fails, retry once before falling back to asking for pasted content.
- Do not run plain git commit when the project provides a helper with explicit authorship conventions.

## Common Pitfalls

1. Creating too many tiny concept pages from one source.
2. Forgetting to update index/log/glossary after page changes.
3. Treating curated interpretation as if it were raw capture.
4. Using broken relative links between raw and source pages.
5. **Confusing entity type with topic.** If you find yourself thinking "this concept is about AI, so it should go in an AI folder" — stop. It goes in `concepts/` because it IS a concept. The topic emerges from links, not folder hierarchy. The type-based system prevents the multiple-belonging problem that plagues topic-based trees.

## Verification Checklist

- [ ] Raw capture saved with enough fidelity to re-check the source later
- [ ] Curated page explains why the source matters
- [ ] Existing pages were preferred over duplicates
- [ ] Global retrieval surfaces updated where needed
- [ ] Raw/source links verified
- [ ] Commit helper used when commit was required
