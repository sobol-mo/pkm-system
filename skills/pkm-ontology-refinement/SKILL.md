---
name: pkm-ontology-refinement
description: Use when PKM needs a sparse spine for a buried contrast.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [pkm, ontology, graph, digital-mind, refinement]
    related_skills: [pkm-ingest, pkm-lint, schema-driven-vault-maintenance, pkm-query]
---

# PKM Ontology Refinement

## When to use

- Maxim says a concept is buried in prose, the graph does not teach a distinction, or neighbors are missing for an existing page
- A refinement is needed without a full new source ingest
- Hierarchy or contrast cleanup on a small branch (not bulk vault maintenance — that is schema-driven-vault-maintenance)

Load companion `pkm-ingest` for vault path conventions, frontmatter, health checker, and global surfaces. This skill owns the **sparse teaching-spine** procedure and pitfalls.

Canonical ontology meaning still lives in the vault project `Requirements/05-knowledge-graph-schema.md`. Do not invent relation types here.

## Default outcome shape

**Narrow spine + verification**, not a dense neighborhood map.

User-facing report (Telegram-friendly):
1. One-sentence teaching failure fixed
2. Text spine (nodes + typed edges)
3. Created / rewritten / tightened pages
4. Relation types used (must be schema-existing only)
5. Broken-link count on touched pages

## Procedure

1. **Name the teaching failure** in one sentence: what question the graph cannot answer now.
2. **Search existing pages** by name, alias, slug before proposing new nodes.
3. **Draft a spine** of 2–5 nodes and edges that make the contrast traversable.
   - Prefer: `opposed_to` for definitional contrasts; `narrower_than` / `broader_than` for layer/class hierarchy; `related_concept` only when hierarchy or opposition is wrong.
   - Source/evidence links: `source`, `about`, `analyzes` as appropriate.
   - **Forbidden:** inventing a new relation type for one fix; defaulting every neighbor to `related_concept`.
4. **Separate layers** when ordinary language, technical class, and clinical/diagnostic categories are mixed:
   - phenomenon ≠ class ≠ diagnosis
   - affect ≠ emotion ≠ disorder
   - Do not rename a phenomenon page into a class/diagnosis page to "simplify".
5. **Reuse first:** rewrite the page that was doing double duty; tighten specialized pages that already exist; create only missing spine nodes.
6. **Promotion gate:** Title-Case or glossary-like terms that only explain the definition stay prose unless Maxim approves promotion. After approval, create spine nodes only — not every word in the definition.
7. **Write pages** in English vault style: frontmatter, body contrast table when useful, `## Relations` with clickable links, explicit "kept as prose" when a known vault concept is mentioned but not edged.
8. **Global surfaces:** `index.md`, `glossary.md`, `connection-map.md`, `log.md` (newest-first). Match adjacent `index.md` row pipe style; patch `connection-map.md` with unique surrounding context.
9. **Verify:** run vault health checker on the vault; zero new broken links from this spine; no new relation-type invention.
10. **Report** the spine, not a tour of every file touched.

## Decision tests before adding an edge

1. Does this edge teach the named contrast, or only densify the map?
2. Is there already an intermediate parent that should carry the hop?
3. Would `opposed_to` or hierarchy state the relation more clearly than `related_concept`?
4. Are the two ends the same ontological layer (both phenomena, both classes)? If not, use hierarchy or keep separate with a single typed link — do not merge pages.
5. If the justification sentence is longer than the relation name, ask Maxim or leave unlinked prose.

## Worked spine pattern (contrast + layer)

```text
PhenomenonA  --opposed_to-->  PhenomenonB
PhenomenonB  --related_concept-->  ClassB   # only if class is genuinely separate
ParentLayer  --broader_than-->  PhenomenonA / PhenomenonB
```

Anti-pattern:
```text
A --related_concept--> B --related_concept--> C --related_concept--> D
# mesh; graph does not teach which contrast matters
```

## Pitfalls

- **Mesh over spine.** Linking every neighbor with `related_concept` fails the teaching goal; prefer one opposition or parent chain.
- **Layer collapse.** Rewriting a phenomenon into its clinical/class page destroys retrieval of ordinary language.
- **New relation types.** Schema catalog only; one-off labels are ontology drift.
- **Promotion without ask.** Definitional vocabulary is not automatically a page; operator authorizes new identities.
- **Skipping health check.** New `## Relations` paths are a common self-inflicted broken-link source — run the checker before claiming done.
- **index/connection-map blind patches.** Read the target region first; short unique strings often match multiple sections.
- **Duplicate of bulk recovery.** Missing-page archaeology from health reports belongs to schema-driven-vault-maintenance; this skill is contrast/spine surgery.

## Support

- references/teaching-spine-examples.md — compact good/bad edge patterns
