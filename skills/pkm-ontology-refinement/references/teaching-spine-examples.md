# Teaching-spine examples (illustrative)

Not a second ontology. Canonical relation catalog is the vault schema.

## Good: opposition + layer separation

Teaching failure: graph cannot answer present affect vs anticipatory emotion vs clinical class.

```text
Fear (affect, present threat)
  --opposed_to-->
Anxiety (emotion, anticipation)
  --related_concept-->
Anxiety Disorder (clinical class)

affect-and-affective-trace --broader_than--> Fear
Anxiety --broader_than--> specialized anticipatory facets (optional)
```

Edges used: opposed_to, broader_than / narrower_than, at most one related_concept to the class node.
Do not merge Fear into Anxiety Disorder.

## Good: hierarchy without sibling mesh

```text
taxonomy-parent --broader_than--> member-a
taxonomy-parent --broader_than--> member-b
# contrast between members stays in prose on the parent or members
```

## Bad: related_concept mesh

```text
A --related_concept--> B
B --related_concept--> C
C --related_concept--> A
A --related_concept--> D
```

Dense, non-teaching. Replace with one spine that answers the user question.

## Bad: inventing edge labels

```text
A --diagnostically_shadowed_by--> B
```

If the schema has no such type, encode in prose or use the nearest existing type after asking.

## Report stub

- Failure fixed: ...
- Spine: ...
- New / rewritten / tightened: ...
- Types used: ...
- Health: N broken links on touched pages
