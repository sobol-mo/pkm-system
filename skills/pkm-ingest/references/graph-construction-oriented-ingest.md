Graph-construction-oriented ingest

Purpose
Use this reference when a source is structurally rich and should be preserved as graph structure, not only as a summary.

Core distinction
- concept = knowledge-bearing entity
- graph node = any first-class reusable entity in the graph
- not every graph node must be a concept

Allowed graph-worthy node classes
- concept
- framework node
- taxonomy or collection node
- technique node
- relation hub

Progressive enrichment levels
- Level 1: source capture
  - raw capture
  - source page
  - 2 to 5 graph-worthy entities
  - key explicit relations
- Level 2: structured extraction
  - main concepts
  - major frameworks, techniques, or taxonomy nodes
  - key contrasts and relations
- Level 3: ontology expansion
  - recover the source's conceptual architecture
  - separate concepts from organizing nodes
  - preserve taxonomies, frameworks, contrasts, and relation hubs as first-class entities where justified

When to choose Level 3
- the author presents an explicit map, taxonomy, framework, or staged model
- the source's value lies in distinctions between neighboring concepts
- Maxim explicitly signals graph-building or ontology value
- later retrieval would be degraded if structure stayed buried in prose

Worked example: systems-thinking video
Recommended extracted nodes:
- systems-thinking
- four-system-types
- clear-systems
- complicated-systems
- complex-systems
- chaotic-systems
- dart-framework
- techniques-of-systems-thinking
- getting-on-the-platform
- cobra-effect
- delayed-feedback-loops
- false-binary

Normalization lesson
Do not flatten a mind map into one source page plus one concept page.
Preserve the author's conceptual architecture when it is already present in the source.

Quality test
A technically valid ingest may still be semantically incomplete if:
- it produces only summary text
- it omits obvious framework or taxonomy nodes
- it collapses multiple distinct entities into one page
- it forces organizational nodes to masquerade as concepts
