# Knowledge Graph Schema

Status: Canonical
Last updated: 2026-06-13

## Purpose

This document is the canonical schema and meaning contract for Digital Mind.

It defines:
- entity types
- relation types
- temporal conventions
- page format
- link policy

This file belongs to the PKM system layer, not to the knowledge-state vault.
Skills must follow this schema.
They must not become a second competing source of truth for ontology meaning.

## Boundary Rule

Separate:
- schema philosophy and semantic rules
- operational workflows that apply those rules
- changing knowledge-state content

Therefore:
- canonical schema lives in `Requirements/`
- agent procedures live in `skills/`
- curated knowledge lives in the canonical vault

Legacy schema-file paths are deprecated.
Resolve schema meaning only from `Requirements/05-knowledge-graph-schema.md`.

## Core Principle

Digital Mind is a typed, temporal knowledge graph expressed in markdown.

```text
entity + typed relations + temporal scope = meaning that agents can traverse
```

The relation type is part of the knowledge, not decorative metadata.

## Entity Types

Entity folders encode what a page IS, not what it is ABOUT.

| Type | Canonical Location | Meaning |
|------|--------------------|---------|
| Concept | `concepts/` | Idea, principle, belief, value, pattern, definition, event, technical term |
| Implementation | `implementations/` | Tool, system, project, or concrete implementation |
| Person | `people/` | Person relevant to the ontology, source network, or influence map |
| Quote | `quotes/` | Verbatim quote preserved as a first-class object |
| Thought | `thoughts/` | Maxim's dated reflection |
| Source | `sources/` | Curated summary of an external or internal source |
| Analysis | `analyses/` | Comparative or synthetic study |
| Raw | `raw/` | Evidence and source capture, not curated knowledge |

### Graph node vs concept

A concept is a knowledge-bearing entity.
A graph node is any entity useful as a first-class object in the graph.

Therefore:
- every concept can be a graph node
- not every graph node must be a concept

Graph-worthy non-concept node classes include:
- taxonomy node
- framework node
- technique node
- relation hub
- map-of-content or collection node

Do not force every graph-worthy entity to masquerade as a concept.

## Relation Format

Use typed links in the `## Relations` section.

Format:

```text
- --type--> [target](relative-path.md)
- --type--> [target](relative-path.md) (from: YYYY-MM-DD)
- --type--> [target](relative-path.md) (from: YYYY-MM-DD, until: YYYY-MM-DD)
```

Keep relation names lowercase, underscored, and descriptive.
Prefer existing relation types before inventing new ones.

## Relation Classes

| Class | Purpose | Examples |
|------|---------|----------|
| Structural | hierarchy, part-whole, implementation, organization | `instance_of`, `broader_than`, `narrower_than`, `implemented_by` |
| Attribution | connect claims to sources or creators | `authored_by`, `source`, `originated_from` |
| Expression | connect quotes/thoughts to concepts | `expresses`, `expressed_in`, `endorsed_by` |
| Worldview | capture Maxim's subjective model | `values`, `believes_that`, `sufficient_for`, `instrument_for` |
| Logical/Semantic | reasoning relationships | `supports`, `contradicts`, `implies`, `opposed_to` |
| Operational | workflows, tools, and support structure | `uses_pattern`, `uses_protocol`, `enables` |

## Standard Relation Types

### Structural Relations

Structural relations carry the semantic backbone of the graph.
Use them for hierarchy, part-whole, implementation, support, contrast, and other meaning-bearing links.
Do not replace these relations with tags.

| Type | Meaning |
|------|---------|
| `--instance_of-->` | X is an implementation or instance of Y |
| `--broader_than-->` | X is broader than Y |
| `--narrower_than-->` | X is narrower than Y |
| `--related_concept-->` | Conceptual similarity or close neighboring meaning |
| `--enables-->` | X enables Y |
| `--solves-->` | X solves problem Y |
| `--uses_pattern-->` | X uses pattern Y |
| `--uses_protocol-->` | X uses protocol Y |
| `--implemented_by-->` | Concept or pattern implemented by Y |
| `--authored_by-->` | Created by person Y |
| `--originated_from-->` | X originated from Y |
| `--evolved_from-->` | X evolved from Y |
| `--complementary_to-->` | X complements Y |
| `--demonstrates-->` | X demonstrates Y |
| `--co_created_with-->` | Person co-created with Y |
| `--about-->` | Thought or analysis is about Y |

### Expression Relations

| Type | Meaning |
|------|---------|
| `--expresses-->` | Quote or artifact expresses concept Y |
| `--expressed_in-->` | Concept expressed in Y |
| `--endorsed_by-->` | Endorsed by person Y |

### Worldview Relations

Worldview relations describe Maxim's subjective belief structure.
Use temporal scope when the belief, value, or interpretation may evolve.

| Type | Meaning |
|------|---------|
| `--sufficient_for-->` | X is sufficient for Y |
| `--instrument_for-->` | X is a means to achieve Y |
| `--necessary_for-->` | X is necessary for Y |
| `--values-->` | Subject values Y |
| `--believes_that-->` | Subject believes proposition Y |
| `--contradicts-->` | X contradicts Y |
| `--supports-->` | X supports or justifies Y |
| `--opposed_to-->` | X is opposed to Y |
| `--implies-->` | X implies Y |
| `--exemplifies-->` | X is an example of Y |

### Source Attribution

| Type | Meaning |
|------|---------|
| `--source-->` | Claim or page is grounded in source Y |

## Temporal Scope

Temporal scope is optional for stable structural or historical facts.
Temporal scope is required when the relation captures a worldview claim that may change over time.

Format:

```text
(from: YYYY-MM-DD)
(from: YYYY-MM-DD, until: YYYY-MM-DD)
```

Use temporal scope for:
- `values`
- `believes_that`
- `sufficient_for`
- `instrument_for`
- other time-bound interpretive claims

Do not use temporal scope for:
- `authored_by`
- `originated_from`
- `instance_of`
- other definitionally stable structural facts

## Page Format

Canonical curated-page frontmatter:

```yaml
---
title: "Page Title"
type: concept | implementation | person | quote | thought | source | analysis
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [raw-or-source-identifiers]
tags: [tags]
---
```

Canonical curated-page body shape:
1. one-line summary
2. structured content
3. `## Relations` section with typed links

Raw pages preserve source fidelity and evidence.
They are not rewritten as curated interpretation.

## Link Policy

### 1. Default traversal is layered

Represent knowledge from general to specific.
Prefer:
- parent node -> immediate organizing node
- organizing node -> direct members
- leaf node -> parent plus only semantically necessary sibling or cross-domain links

Do not default to parent -> every descendant.
If an intermediate taxonomy, framework, or collection node already exists, route traversal through it.

### 2. Keep structural roles separate

Do not mix these roles in one node:
- taxonomy node = classification spine
- framework node = diagnostic or operating method
- technique node = concrete maneuver
- source/index/glossary node = retrieval surface, not semantic concept container

A framework may point to a taxonomy.
That does not make it a member of the taxonomy.

### 3. Tags are facets, not semantic edges

Use tags for:
- topic grouping
- retrieval filters
- page subtyping within one folder
- lightweight thematic clustering

Do not use tags as a substitute for relations such as:
- broader/narrower structure
- part-whole structure
- framework-for
- source attribution
- support/contrast/implication

If the relationship changes the meaning of traversal, represent it as a typed relation.

### 4. Cross-links must earn their place

Cross-links are allowed, but they should be sparse and explicit.
Add them when they:
- connect otherwise separate branches
- support an important comparison or contrast
- materially improve retrieval

Avoid all-to-all dense linking between neighboring pages from the same source.

### 5. Retrieval surfaces are not graph hubs

`index.md`, `glossary.md`, and similar overview files are retrieval surfaces.
They help humans and agents find pages.
They are not part of the semantic graph and should not be treated as ontology hubs that justify extra concept-to-concept links.

## Operational Implication for Skills

Skills such as `pkm-ingest` may summarize the operational consequences of this schema.
They must not silently redefine:
- entity types
- relation meanings
- page format
- temporal rules
- link policy

When a conflict appears, this schema wins.

## Change Policy

Update this file when the meaning contract of the system changes.
Do not use a skill file as the canonical place for ontology philosophy.
Do not store canonical schema meaning inside the vault state.
