# ADR-004: Graph-Construction-Oriented Ingest

**Date:** 2026-06-13
**Status:** Accepted

## Context

Digital Mind is not just a note archive.
Its purpose is to preserve and operate on Maxim's worldview as a typed knowledge graph.

In practice, source ingest can drift toward a summary-oriented pattern:

- capture the raw source
- create a source page
- extract a few obvious concepts
- leave the rest of the source's internal structure buried inside prose

This is acceptable for archival capture, but insufficient for a system whose value depends on reusable graph structure.
A clean summary does not guarantee that the source has been integrated into the knowledge graph.

The problem becomes visible with structurally rich sources.
A source may contain:

- concepts
- frameworks
- techniques
- taxonomic groupings
- contrasts between neighboring concepts
- organizing nodes that exist to structure other entities

If ingest treats all extracted entities as ordinary concepts, or reduces the source to a summary, the system loses reusable structure.
The source remains readable, but knowledge that should become graph-native stays trapped inside the source page.

A second problem appears at the ontology boundary.
Not every graph node is a concept.
Some nodes are valuable precisely because they organize, diagnose, or connect other nodes.
Without this distinction, agents either under-extract structure or force everything into the concept bucket.

## Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **A: Summary-oriented ingest** | Fast; low cognitive overhead; easy to automate | Preserves content but not structure; weak graph growth; reusable distinctions stay buried in prose |
| **B: Full ontology expansion for every source** | Maximally expressive; strong graph coverage | Too expensive; turns ordinary ingest into research; causes node explosion |
| **C: Graph-construction-oriented ingest with depth levels** | Preserves graph value while controlling effort; supports progressive enrichment; matches source importance | Requires judgment; adds a new ingest decision and ontology discipline |

## Decision

The system adopts **graph-construction-oriented ingest**.

Ingest is not defined as "create a summary and a few notes."
It is defined as the process of moving source knowledge into the graph as reusable first-class entities and explicit relations.

### 1. Unit of preservation

The unit of preservation is not only the concept.
It is any **graph-worthy entity** that should live independently in the knowledge graph.

Allowed graph-worthy entity classes include:

- concept
- framework node
- taxonomy or collection node
- technique node
- relation hub

This means:

- every concept can be a graph node
- not every graph node must be a concept
- some nodes are organizational rather than purely conceptual

Examples:

- `complex systems` is a concept
- `DART framework` may be represented as a framework node
- `techniques of systems thinking` may be represented as a taxonomy or collection node
- `getting on the platform` may be represented as a technique node

### 2. Minimum ingest rule

Every ingest must produce at least a **minimal graph-useful result**.

A source that enters the vault only as raw text plus a source summary is archived, but not yet properly integrated into the knowledge graph.

At minimum, ingest must extract:

- a small set of reusable graph-worthy entities
- the most important explicit relations needed for later retrieval and reuse

### 3. Progressive enrichment

The system rejects the false binary between:

- shallow archival capture
- full ontology decomposition for every source

Instead, ingest uses three depth levels.

#### Level 1 — source capture

Use when the goal is to preserve the source quickly without deep decomposition yet.
Still required:

- raw capture
- source page
- 2 to 5 important graph-worthy entities
- the key explicit relations needed for later rediscovery

#### Level 2 — structured extraction

Use when the source contains several reusable ideas and a meaningful internal structure.
Expected output:

- main concepts
- major frameworks, techniques, or taxonomy nodes
- the key contrasts and relations between them

#### Level 3 — ontology expansion

Use when the source is highly structured, strategically important, or clearly presents a conceptual map.
Expected output:

- recovery of the source's conceptual architecture
- separation of concepts from organizing nodes
- preservation of contrasts, taxonomies, frameworks, and relation hubs as first-class graph entities where justified
- avoidance of flattening a mind map into a single summary page

### 4. Selection heuristics for Level 3

Prefer Level 3 when one or more of the following is true:

- the author presents an explicit map, staged model, taxonomy, or framework
- the source's value depends on distinctions between neighboring concepts
- Maxim explicitly signals that the source matters for graph-building or ontology
- later retrieval would be materially degraded if the structure stayed buried inside prose

### 5. Operational interpretation

For this system, ingest quality is judged not only by factual correctness and schema compliance, but also by whether reusable structure was preserved as graph-native entities and relations.

A technically valid ingest may still be semantically incomplete if:

- it produces only summary text
- it collapses multiple distinct entities into one page
- it omits obvious framework or taxonomy nodes from a structurally rich source
- it forces organizational nodes to masquerade as concepts

## Consequences

### Positive

- The vault grows as a reusable knowledge graph rather than as a pile of source summaries.
- Structurally rich sources contribute their internal maps, not only their surface content.
- Agents gain a clearer ontology for deciding what should become a first-class node.
- Progressive enrichment controls effort without sacrificing graph quality.

### Neutral

- Ingest now requires an explicit depth decision.
- Some nodes will exist primarily for organization rather than as standalone philosophical concepts.

### Negative

- Level 3 ingest is more cognitively expensive than summary-oriented ingest.
- Poor judgment can still create node explosion if structure is extracted without discipline.
- Agents need better ontology sensitivity, not just formatting compliance.

## Implementation Notes

- `Requirements/04-domain-model.md` defines the distinction between concept and graph node.
- `skills/pkm-ingest/SKILL.md` carries the operational ingest rules and the Level 1/2/3 workflow.
- Health checks and schema validation remain necessary but are not sufficient; they prevent structural drift in format, not loss of ontology during extraction.
- Future automation may assist with candidate-entity extraction, but final ontology judgment remains an intelligent task rather than a purely deterministic one.

## Decision Log

| Date | Decision | Context |
|------|----------|---------|
| 2026-06-13 | Adopt graph-construction-oriented ingest | Session analyzing why a systems-thinking video ingest preserved some concepts but failed to preserve enough of the source's conceptual map |
| 2026-06-13 | Distinguish concept from graph node | Needed to allow framework/taxonomy/technique nodes without forcing all entities into the concept bucket |
| 2026-06-13 | Introduce Level 1/2/3 ingest depth | Needed to avoid the false binary between shallow archive capture and full ontology research |

## References

- `../Requirements/04-domain-model.md`
- `../skills/pkm-ingest/SKILL.md`
- `ADR-001-folder-organization-and-system-state-separation.md`
