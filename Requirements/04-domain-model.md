# Domain Model

Status: Baseline draft
Last updated: 2026-05-28

## Purpose

This document defines the conceptual model of Digital Mind before implementation details.

It answers: what kinds of things exist in the system, what relationships matter, and what is canonical versus derived.

## Core Model

Digital Mind models Maxim's worldview as a typed, temporal knowledge network.

```text
Raw Input -> Curated Knowledge Object -> Typed Relations -> Derived Runtime Views
```

The canonical record is the curated markdown vault. Databases and indexes are compiled from it.

## Core Entities

| Entity | Meaning | Canonical Location |
|--------|---------|--------------------|
| Raw Input | Unprocessed source material: forwarded text, transcript, note, article, quote, file | `raw/` now; future canonical vault `raw/` |
| Concept | Idea, definition, value, belief, event, principle, or technical term | `wiki/concepts/` now; future vault `concepts/` |
| Quote | Exact formulation endorsed or analyzed by Maxim | `wiki/quotes/` now; future vault `quotes/` |
| Thought | Maxim's dated reflection with original wording and extracted concepts | `wiki/thoughts/` now; future vault `thoughts/` |
| Source | Curated summary of an external or internal source | `wiki/sources/` now; future vault `sources/` |
| Person | Person relevant to the ontology, source network, or influence map | `wiki/people/` now; future vault `people/` |
| Implementation | Tool, system, project, or reference implementation | `wiki/implementations/` now; future vault `implementations/` |
| Analysis | Synthesis, comparison, gap analysis, design note, or research output | `wiki/analyses/` now; future vault `analyses/` |
| Relation | Typed edge connecting two entities | Stored inside page relation sections |
| Skill | Agent-executable workflow instructions for maintaining or operating the wiki | `skills/` in the project system layer |
| Automation Script | Reusable executable support for skills or runtime maintenance | `scripts/` or future `automation/` in the project system layer |
| Role | Expected function of a human or agent collaborator | Concept tagged `role` now; may become separate type later |
| Process | Repeatable workflow or operating procedure | Concept tagged `process` or `sop` now; may become separate type later |
| Artifact | Work product, document, code asset, schema, or deliverable used by a project | Concept tagged `artifact` now; may become separate type later |
| Goal | Desired outcome used to guide agent or project work | Concept tagged `goal` now; may become separate type later |
| Constraint | Limitation or rule that shapes acceptable agent/project behavior | Concept tagged `constraint` now; may become separate type later |
| Evaluation Criterion | Condition used to judge agent or project performance | Concept tagged `evaluation` now; may become separate type later |
| Runtime Artifact | Vector index, graph DB, compiled graph, export | Derived; not canonical |

## Important Distinctions

### Concept vs Graph Node

A concept is a knowledge-bearing entity.
A graph node is any entity that is useful as a first-class object in the knowledge graph.

Therefore:

- every concept can be represented as a graph node
- not every graph node must be a concept
- some nodes exist primarily to organize, collect, diagnose, or structure other nodes

Typical non-concept but graph-worthy node classes include:

- framework node
- taxonomy node
- technique node
- relation hub
- map-of-content or collection node

Examples:

- `complex systems` is a concept
- `DART framework` may be treated as a framework node
- `techniques of systems thinking` may be treated as a taxonomy/collection node
- `getting on the platform` may be treated as a technique node

This distinction matters operationally.
The goal of ingest is not only to summarize source content, but to preserve reusable graph structure.
If a source contains meaningful structure, the system should preserve that structure as explicit graph entities and relations rather than burying it inside prose.

### Raw vs Curated

Raw input records what was received.

Curated knowledge records what has been extracted, structured, summarized, or reviewed.

Raw input is evidence. Curated knowledge is interpretation.

### Mentioned vs Endorsed

A concept or quote appearing in a source does not mean Maxim endorses it.

Endorsement must be explicit through a relation such as:

```text
[quote] --endorsed_by--> [Maxim] (from: YYYY-MM-DD)
[Maxim] --believes_that--> [claim] (from: YYYY-MM-DD)
```

### Project System vs Knowledge Vault

The project system defines how the vault is maintained.

The knowledge vault stores the worldview and knowledge state.

ADR-001 defines the intended separation:

- system: configuration, requirements, ADRs, scripts, schemas, automation
- canonical vault: raw and curated knowledge files
- runtime: derived indexes, graph databases, exports

PKM-specific skills belong to the system layer because they define how agents operate on the vault. They are not vault content and should not exist only as hidden VPS runtime state.

### Unified Knowledge Field vs Note Collection

Digital Mind is not only a collection of notes. It is intended to be a unified knowledge field for Maxim's projects and agents.

This means the vault must be able to represent:

- what Maxim knows and believes
- what projects exist and why
- what roles agents or humans can perform
- what processes and artifacts guide work
- what goals, constraints, and evaluation criteria define successful work

Agents should be onboarded from this structured context rather than only from task-specific prompts.

## Relation Classes

The detailed canonical relation and page schema lives in `Requirements/05-knowledge-graph-schema.md`.

This domain-model file keeps only the class-level interpretation needed to explain the model shape.

At the domain-model level, relations fall into these classes:

| Class | Purpose | Examples |
|-------|---------|----------|
| Structural | Define taxonomy or implementation relationships | `instance_of`, `broader_than`, `narrower_than` |
| Attribution | Connect claims to sources or creators | `authored_by`, `source`, `originated_from` |
| Expression | Connect quotes and thoughts to concepts | `expresses`, `expressed_in`, `endorsed_by` |
| Worldview | Capture Maxim's subjective conceptual model | `values`, `believes_that`, `sufficient_for`, `instrument_for` |
| Logical/Semantic | Capture reasoning relationships | `supports`, `contradicts`, `implies`, `opposed_to` |
| Operational | Connect workflows, SOPs, tools, and implementations | `uses_pattern`, `implemented_by`, `enables` |
| Agent Management | Connect roles, goals, processes, artifacts, and evaluation criteria | `responsible_for`, `requires_context`, `evaluated_by`, `constrained_by` |

## Temporal Model

Worldview relations can change over time. The system must preserve this change rather than overwrite it.

Example:

```text
[money] --sufficient_for--> [happiness] (from: 2010-01-01, until: 2020-06-15)
[money] --instrument_for--> [happiness] (from: 2020-06-15)
```

Temporal scope is required for claims about Maxim's beliefs, values, and interpretations when the claim may evolve.

## Progressive Enrichment and Ingest Depth

Ingest is not binary.
A source does not need either zero extraction or full ontology expansion.
The system supports progressive enrichment, where a source may enter the vault at different depths and be enriched later.

Default depth model:

- Level 1 — source capture
  - preserve raw capture and curated source page
  - extract a minimal graph-worthy set of entities and relations
  - enough to ensure the source is not trapped as dead text
- Level 2 — structured extraction
  - extract the main concepts, frameworks, techniques, and key relations
  - preserve the source's major internal structure in graph form
- Level 3 — ontology expansion
  - perform deep decomposition when the source is itself strongly structured or strategically important
  - recover the source's internal map where useful: concepts, graph-organizing nodes, relation hubs, contrasts, taxonomies, and frameworks

Operational rule:
Every ingest must produce at least a minimal graph-useful result.
A source that enters the system without any extracted reusable entities is archived, but not yet integrated into the knowledge graph.

Selection rule:
Choose deeper extraction when the source already presents a strong conceptual architecture, when Maxim explicitly flags it as structurally important, or when later reuse depends on preserving distinctions between neighboring entities.

## Canonical State Boundaries

| Layer | Canonical? | Purpose |
|-------|------------|---------|
| `PKM-idea.md` | No | Historical idea dump and raw monologue capture |
| `raw/` | Evidence only | Immutable raw sources and captures |
| `Requirements/` | Yes, for project definition | Vision, business requirements, system requirements, domain model, graph schema |
| `Architecture/` | Yes, for accepted architecture decisions | ADRs and architecture rationale |
| `skills/` | Yes, for PKM-specific agent workflows | Project-owned skills usable from VPS and localhost |
| `scripts/` | Yes, for reusable support automation | Project-owned scripts, not runtime state |
| `wiki/` | Yes, for curated knowledge until vault migration | Curated personal ontology content |
| Legacy schema-file paths | No | Deprecated; use `Requirements/05-knowledge-graph-schema.md` directly |
| `BACKLOG.md` | Yes, for active work state only | Actionable tasks and status |
| `AGENTS.md` | Yes, for operation only | Session bootstrap and agent behavior |
| Derived databases/indexes | No | Fast query/search/runtime support |

## Current Domain Decisions

- Digital Mind is broader than standard PKM because it models worldview, not only stored information.
- The relation type is as important as the connected concepts.
- Quotes are first-class personality nodes when Maxim endorses them.
- Technical knowledge and worldview are not cleanly separable for Maxim, so the design supports both.
- Markdown files are canonical; databases are compiled.
- Folder organization is by entity type, not by domain topic.
- PKM-specific skills are project system assets and should be versioned with the project, then deployed or synced to agent runtimes as needed.
- Digital Mind is a unified knowledge field for both worldview preservation and deep agent context.
- Agents should be managed through roles, goals, constraints, and evaluation criteria, not only through prompts.

## Open Domain Questions

- What review state separates AI-extracted relations from Maxim-endorsed relations?
- Should `Belief`, `Value`, and `Event` remain tagged concepts or become separate entity folders later?
- What is the exact bilingual naming convention for concepts?
- Should `Maxim` be modeled as a person page, a special subject, or both?
- What is the exact deployment/sync mechanism for making project-owned skills available to the VPS agent runtime?
- Should `Role`, `Process`, `Artifact`, `Goal`, `Constraint`, and `Evaluation Criterion` remain tagged concepts or become separate entity types?
- Which relation types are needed for agent onboarding and evaluation?
