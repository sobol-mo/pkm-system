Purpose

Use layered traversal in concept-graph design so retrieval can expand context gradually instead of loading a flat web.

Core rule

Do not connect a parent concept directly to every descendant when an intermediate organizing node already exists.

Preferred shape

- root concept -> taxonomy / collection / framework-group node
- taxonomy node -> member concepts
- framework-group / technique-group node -> concrete frameworks or techniques
- leaf node -> parent + only semantically necessary cross-domain links
- source page -> top-layer extracted nodes, not the whole descendant fan-out of each branch

For hierarchy-first or teaching-first graph views, sibling-to-sibling links inside one taxonomy level are off by default.
Keep the comparison in prose unless the graph edge is genuinely necessary for retrieval.

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

4. Sibling mesh inside one taxonomy level
If clear/complicated/complex/chaotic all point to each other, the branch stops reading like a tree and starts reading like a net. For hierarchy-first teaching graphs, route all of them through the taxonomy parent instead.

5. Source fan-out across a whole branch
If a source points to an organizing node and also to every leaf underneath it, the branch depth is visually flattened. Prefer source -> branch node, then branch node -> leaves.

Recommended decision test

Before adding a direct edge, ask:
1. Is this node the direct parent, or is there already an intermediate organizing node?
2. Is the target a member of a taxonomy, or a tool for working with that taxonomy?
3. If this direct edge is removed, can the concept still be reached naturally in 1-2 hops?
4. Would adding this edge improve retrieval, or just make the map denser?
5. Is this edge turning same-level siblings into a mesh when the branch is meant to read as a hierarchy?

If the answer to 4 is "just denser" or to 5 is "yes", do not add the edge.

External alignment noted in session

- Concept-map practice favors top-down movement from general to specific, with cross-links added only when semantically meaningful.
- Ontology/taxonomy practice treats taxonomy as classification backbone; richer methods and relations are layered around it, not inserted into it as members.

Operational default for PKM ingest

When a source contains a mind map, staged model, or conceptual architecture:
- first identify the organizing node types
- separate taxonomy nodes from framework nodes
- separate framework nodes from technique nodes
- add leaf links only under the appropriate parent node
- keep same-level taxonomy members connected through the parent by default
- let source pages point to branch entry nodes instead of duplicating every descendant link
- add cross-links sparingly and explicitly justify them
