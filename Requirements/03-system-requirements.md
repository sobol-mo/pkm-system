# System Requirements

Status: Baseline draft
Last updated: 2026-05-28

## Requirement Language

- **Must** means required for the baseline architecture.
- **Should** means expected unless a later ADR supersedes it.
- **May** means optional or future-facing.

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-01 | The system must capture raw inputs from Maxim and external sources without treating them as curated truth. | Must |
| FR-02 | The system must maintain curated wiki pages for concepts, people, quotes, thoughts, sources, analyses, and implementations. | Must |
| FR-03 | The system must represent typed relations between knowledge objects. | Must |
| FR-04 | The system must support worldview relations such as `sufficient_for`, `instrument_for`, `necessary_for`, `values`, `believes_that`, `supports`, and `contradicts`. | Must |
| FR-05 | The system must support temporal scope for beliefs, values, and other worldview relations that can change over time. | Must |
| FR-06 | The system must support quote ingestion as a first-class workflow: quote text, author, expressed concepts, and Maxim endorsement. | Must |
| FR-07 | The system must support thought ingestion as a first-class workflow: original thought, extracted concepts, and relations. | Must |
| FR-08 | The system must support source ingestion: raw source, curated source summary, extracted entities, and updated relation graph. | Must |
| FR-09 | The system must support query workflows that answer from curated wiki content with references to source pages. | Must |
| FR-10 | The system must support lint workflows for contradictions, stale claims, missing cross-links, orphan pages, and schema inconsistencies. | Should |
| FR-11 | The system must support rebuilding derived runtime artifacts from canonical markdown files. | Must |
| FR-12 | The system should support exporting the vault for legacy use. | Should |
| FR-13 | The system should support Telegram/OpenClaw-based capture and interaction. | Should |
| FR-14 | The system may support graph database or vector search backends as derived indexes. | May |
| FR-15 | The system must provide project-owned PKM skills for ingest, query, lint, and related wiki maintenance workflows. | Must |
| FR-16 | The system must allow those skills to be used from both VPS production agents and localhost development agents. | Must |
| FR-17 | The system must support storing role, process, artifact, goal, constraint, and evaluation knowledge for agent onboarding and operation. | Must |
| FR-18 | The system should support agent onboarding workflows that assemble role-relevant context from curated knowledge. | Should |
| FR-19 | The system should support goal-oriented agent work by exposing objectives, constraints, and success criteria as structured knowledge. | Should |

## Non-Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| NFR-01 | Canonical knowledge must be stored in human-readable markdown files. | Must |
| NFR-02 | The system must remain portable across LLM providers, databases, and note-taking tools. | Must |
| NFR-03 | Databases, embeddings, vector indexes, and compiled graphs must be rebuildable from canonical files. | Must |
| NFR-04 | The system must preserve raw evidence separately from curated interpretation. | Must |
| NFR-05 | The vault must be recoverable and transferable as a folder/archive. | Must |
| NFR-06 | Session startup for an agent must be deterministic and based on a small set of canonical files. | Must |
| NFR-07 | The system should minimize routine context loading to avoid token waste. | Should |
| NFR-08 | The system should support bilingual or multilingual inputs without forcing early translation decisions. | Should |
| NFR-09 | The system should be usable by Maxim without requiring manual database operations. | Should |
| NFR-10 | The system should preserve auditability of important decisions through ADRs and requirements documents. | Should |
| NFR-11 | PKM-specific operational skills must be versioned, reviewable, and reproducible outside any single agent runtime. | Must |
| NFR-12 | Runtime-specific paths on the VPS or localhost must not be the only source of skill behavior. | Must |
| NFR-13 | Agent behavior should depend on durable curated knowledge rather than fragile prompt-only context. | Should |

## Data Requirements

| ID | Requirement |
|----|-------------|
| DR-01 | Every curated page must have a stable filename and title. |
| DR-02 | Every curated page should include frontmatter with type, created date, updated date, sources, and tags. |
| DR-03 | Every worldview claim should be traceable to raw input, source, or explicit Maxim decision. |
| DR-04 | Every temporal worldview relation should preserve old states instead of overwriting them. |
| DR-05 | Raw captures must remain immutable after processing, except for explicit correction of capture errors. |
| DR-06 | Role, process, artifact, goal, constraint, and evaluation knowledge should be represented as first-class curated objects or clearly tagged concepts. |

## Interface Requirements

| ID | Requirement |
|----|-------------|
| IR-01 | The primary human interaction channel should support natural-language capture. |
| IR-02 | The system should expose a workflow for agent-assisted ingest, query, lint, rebuild, and export. |
| IR-03 | The system should remain usable through files even if Telegram, OpenClaw, or a database is unavailable. |
| IR-04 | Localhost agents should be able to discover and use project PKM skills from the project tree. |
| IR-05 | VPS agents should use the same project-owned skill definitions, either directly or through deployment/sync from the project tree. |
| IR-06 | Agent-facing workflows should be able to retrieve role-specific onboarding context from the knowledge base. |

## Requirements Resolved By ADR-001

ADR-001 currently resolves these design questions:

- folder organization is type-based, not domain-based
- canonical vault and system configuration have different lifecycles
- markdown files are canonical
- databases and indexes are compiled artifacts
- runtime artifacts are not versioned

## Open Requirements Questions

- What is the smallest ontology that makes the first MVP useful?
- What review states are needed between raw capture and Maxim-endorsed knowledge?
- How should bilingual concept naming work?
- Which exact sync/backup mechanism protects the canonical vault?
- What should be exported for the legacy audience first?
- What exact mechanism should deploy project-owned skills into the VPS agent runtime?
- Which entity model should represent agent roles, processes, goals, constraints, and evaluation criteria?
