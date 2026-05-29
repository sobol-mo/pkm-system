# ADR-001: Folder Organization and System/State Separation

**Date:** 2026-05-27
**Status:** Accepted

## Context

The PKM project has grown from a personal ontology experiment into both a knowledge vault and a system for maintaining it. Two tensions emerged:

1. **Folder categorization vs linking.** Deep domain-based folder trees (AI/, philosophy/, uni/, devops/) create conflicts — a concept like agent-memory belongs in multiple domains. Pure flat structure (all notes in one folder) makes browsing impossible beyond ~100 files.

2. **System state vs content state.** Configuration (schema, automation, ADRs) and content (notes, concepts, sources) were interleaved in the same project. Changes to architecture and changes to knowledge lived in the same git history.

## Options Considered

### For folder organization

| Option | Pros | Cons |
|--------|------|------|
| **A: Domain-based folders** (AI/, philosophy/, uni/) | Intuitive browsing by topic | Multiple parents; hard boundaries; reorganizations are painful |
| **B: Flat single folder** | No categorization conflicts | Browsing impossible at scale; no navigation affordance |
| **C: Type-based folders** (concepts/, people/, quotes/, sources/) | No "multiple parent" problem — a note knows what it IS | Domain browsing must happen via links, not folders |
| **D: Type-based + MOC as separate layer** | Clean separation of entity type from navigation | Adds a new entity type to maintain; existing hub pages already serve this function |

### For system/state separation

| Option | Pros | Cons |
|--------|------|------|
| **A: Monorepo** (all in one repo) | Simple; single commit history | Config changes mixed with content changes; hard to reuse automation across vaults |
| **B: Three-way split** (system repo + canonical vault + derived runtime) | Clean boundaries; each has its own lifecycle and sync strategy | More repos to manage; migration cost |
| **C: Two-way split** (system + vault in same repo, runtime derived) | Pragmatic; system and vault versioned together, runtime ephemeral | System and content still share git history |

## Decision

### 1. Type-based folders, no domain folders

Wiki content is organized by **entity type**, not by topic:

```
wiki/
  concepts/        ← definitions, ideas, principles
  people/          ← persons in the ontology
  quotes/          ← quotes endorsed by Maxim
  thoughts/        ← Maxim's dated reflections
  sources/         ← curated source summaries
  analyses/        ← synthesis and comparisons
  implementations/ ← tools and systems
  mocs/            ← (reserved, not required as active layer)
```

- Domain relationships (what a concept is "about") are expressed **exclusively through typed relations and tags**
- No AI/, philosophy/, uni/, or devops/ folders will be created
- Hub pages (e.g. agentic-ai-system.md) with dense relation lists serve as de facto Maps of Content
- MOC is a useful conceptual understanding but NOT a required entity type — adding it as a separate layer would introduce complexity without solving a real problem
- `index.md` and `connection-map.md` provide entry points without domain folders

### 2. Three-way split: system, canonical vault, derived runtime

The project separates into three scopes with distinct lifecycles:

**A. System** — `~/.hermes/agents-projects/pkm-system/`

```
pkm-system/
  AGENTS.md         ← agent operational context
  BACKLOG.md        ← active and planned work
  Architecture/     ← ADRs and design docs
  adr/              ← individual ADR files (alias for clarity)
  scripts/          ← reusable automation
  schema/           ← entity types, relation types, page templates
  automation/
    ingest/         ← Telegram → vault pipeline
    export/         ← vault → publication format
    rebuild/        ← vault → derived runtime
  templates/        ← note templates for each entity type
```

System IS versioned (git, monorepo `agents-projects`). System IS human-reviewed. Commits are meaningful — they change how the vault is managed, not what the vault contains.

**B. Canonical vault** — external synced folder `KnowledgeVault/`

```
KnowledgeVault/
  inbox/            ← raw capture, everything lands here from Telegram
  raw/              ← immutable source captures (from inbox after processing)
  concepts/         ← definitions, ideas, principles
  people/           ← persons in the ontology
  quotes/           ← quotes endorsed by Maxim
  thoughts/         ← Maxim's dated reflections
  sources/          ← curated source summaries
  analyses/         ← synthesis and comparisons
  implementations/  ← tools and systems
  daily/            ← dated journal entries
  mocs/             ← (reserved, not required as active layer)
  assets/           ← images, attachments referenced by notes
  index.md          ← master catalog of all pages
  overview.md       ← project-level description
  glossary.md       ← term definitions
  connection-map.md ← exhaustive relation graph
  log.md            ← chronological ingest record
  schema.md         ← reference copy (generated from system/schema/)
```

Vault IS sync-first (Obsidian). Vault IS NOT a git project. Vault IS the canonical truth — losing system is inconvenient, losing vault is catastrophic.

Note: the type-based folder structure from section 1 applies to vault content. No domain-based folders.

Vault identity: external synced folder named `KnowledgeVault`.

Default path convention:

- `Dev`: `/home/maxim/KnowledgeVault`
- `Prod`: `/home/hermes/KnowledgeVault`

The canonical vault is defined by identity and contract, not by one universal absolute path.
Concrete absolute path is an environment binding resolved by configuration.

Production note: the VPS may act as the primary runtime host for rebuild/index operations, but it must not be treated as the only architectural path assumption for the vault.

**C. Derived runtime (NOT in repo)**

```
~/.knowledge-runtime/
  vector-index/     ← embeddings from vault (e.g. LightRAG)
  compiled-graph/   ← aggregated graph for fast queries (e.g. Neo4j)
  export/           ← one-shot publication exports
```

Runtime IS ephemeral. Runtime IS regenerated from vault. Runtime IS NOT committed or synced.

### 3. Files are canonical, databases are compiled

A critical architectural principle derived from the Karpathy three-layer pattern and the long-term technology outlook (LightRAG, Neo4j, vector databases):

- **Markdown files in the canonical `KnowledgeVault/` are the source of truth.** They are human-readable, portable, versionable, and format-agnostic.
- **Any database (graph DB, vector index, relational store) is a compiled artifact.** It is built from files, can be rebuilt from files, and should never be treated as the primary record.

This ensures portability independent of specific database technology:
- Moving the vault: sync or copy `KnowledgeVault/` to the new environment path → run `rebuild` → all databases are restored
- Losing a database: run `rebuild` — markdown files contain all relations and content
- Changing database technology: write a new `rebuild` target; the source (markdown files) doesn't change
- Heir transfer: hand over the `KnowledgeVault/` folder (or a compressed archive) — no database dependency

## System-vault interface

The system operates on the vault via scripts in `automation/`:

| Operation | Source | Target | Trigger |
|-----------|--------|--------|---------|
| Ingest | Telegram / inbox | raw/ + wiki/ | On new source arrival |
| Compile | raw/ + wiki/ | wiki/ (curation) | After ingest |
| Lint | wiki/ | wiki/ (corrections) | On demand |
| Rebuild | vault/ | runtime/ | On demand or cron |
| Export | vault/ | export/ | On demand |

## Rationale

### For type-based folders

- Entity type is **stable and non-overlapping** — a note always knows what it is (concept, person, quote).
- Domain is **fluid and multi-dimensional** — one concept connects to many domains. Relations handle this naturally.
- The current wiki already follows this pattern and works. This ADR formalizes what was already discovered through practice.
- No migration needed — the existing structure is already type-based.

### For system/state separation

- System and canonical vault have **different lifecycles**: system evolves by human architectural decision, vault evolves by ingestion.
- System and vault have **different git strategies**: system is versioned with meaningful commits, vault is sync-first without git history pollution.
- Vault IS NOT a git project because:
  - Git tracks changes, not state — but the vault IS the state, not a record of changes.
  - Committing every ingest floods history with automated content — meaningful history is in system commits.
  - Sync (Obsidian, Dropbox, Syncthing) is the right tool for vault distribution, not git.
- A production VPS may be **more reliable than a local HDD** as a runtime/backup host, but the canonical vault still needs a cross-environment sync contract and must not be reduced to a VPS-only location assumption.
- **Files > databases** for portability: markdown is a universal format with no vendor lock-in. A folder can be copied, archived, or transferred to an heir regardless of what database technology was in use.
- Runtime is derived from vault and is trivially reproducible — losing runtime is a rebuild, losing vault is a disaster.
- Migration cost from current state (PKM/ has raw/ + wiki/) is accepted: vault content moves to the external `KnowledgeVault/`, system retains only config, schema, automation.

## Consequences

### Positive
- No more "which folder does this go in" ambiguity
- Domain browsing through relations is richer than folder browsing (multi-dimensional)
- Clean separation of concerns between content and automation
- Runtime state can be aggressively regenerated without versioning concerns

### Neutral
- Domain-based browsing requires `connection-map.md` or tags instead of folder navigation — a conceptual shift for anyone accustomed to tree structures

### Negative
- Migration cost: current raw/ + wiki/ must move from PKM/ to `KnowledgeVault/`; system automation must be updated to target the configured vault path
- Two locations to maintain instead of one; vault requires a sync mechanism independent of git

## Decision Log

| Date | Decision | Context |
|------|----------|---------|
| 2026-05-27 | Type-based folders for wiki content | Session discussion on folder vs linking |
| 2026-05-27 | No MOC as separate entity type | MOC useful as concept, not required as layer |
| 2026-05-27 | Three-way split (system + canonical vault + derived runtime) | Vault is sync-first, not git; system is versioned with meaningful commits |
| 2026-05-27 | Vault uses `KnowledgeVault` as canonical identity | External synced vault; concrete path resolved per environment |
| 2026-05-27 | Files are canonical, databases are compiled | Markdown = portable source of truth; any DB is rebuildable from files |

## References

- wiki/concepts/linking-over-categorizing.md — Zettelkasten principle
- wiki/concepts/map-of-content.md — MOC as concept (ingested 2026-05-27)
- wiki/connection-map.md — current cluster map
- wiki/schema.md — entity types and relation types
- ADR-003: cross-environment vault deployment and sync
