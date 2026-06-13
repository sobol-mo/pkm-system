Purpose

Use layered traversal in concept-graph design so retrieval can expand context gradually instead of loading a flat web.

Core rule

Do not connect a parent concept directly to every descendant when an intermediate organizing node already exists.

Preferred shape

- root concept -> taxonomy / collection / framework-group node
- taxonomy node -> member concepts
- framework-group / technique-group node -> concrete frameworks or techniques
- leaf node -> parent + only semantically necessary sibling or cross-domain links

Structural-role separation

Keep these roles distinct:
- taxonomy spine: classification hierarchy only
- framework: diagnostic or operational method
- technique node: practical move or reusable maneuver
- supporting concept: peer idea that is not a child in the taxonomy
- cross-link: non-hierarchical relation justified by real semantic dependence

Anti-patterns

1. Parent -> all descendants fan-out
This creates a retrieval web instead of layered context expansion.

2. Mixing taxonomy with framework
If a taxonomy page contains both class members and operational methods, the graph is conflating classification with usage.
Example: a node like four-system-types should contain the four types only; a diagnostic framework like DART may point to that taxonomy but is not part of the taxonomy.

3. "Related to" as default glue
Prefer typed structural relations over generic relatedness whenever the role is clear.

Recommended decision test

Before adding a direct edge, ask:
1. Is this node the direct parent, or is there already an intermediate organizing node?
2. Is the target a member of a taxonomy, or a tool for working with that taxonomy?
3. If this direct edge is removed, can the concept still be reached naturally in 1-2 hops?
4. Would adding this edge improve retrieval, or just make the map denser?

If the answer to 4 is "just denser", do not add the edge.

External alignment noted in session

- Concept-map practice favors top-down movement from general to specific, with cross-links added only when semantically meaningful.
- Ontology/taxonomy practice treats taxonomy as classification backbone; richer methods and relations are layered around it, not inserted into it as members.

Operational default for PKM ingest

When a source contains a mind map, staged model, or conceptual architecture:
- first identify the organizing node types
- separate taxonomy nodes from framework nodes
- separate framework nodes from technique nodes
- add leaf links only under the appropriate parent node
- add cross-links sparingly and explicitly justify them
