# Thought-Only Ingest Pattern

When the user shares personal practical knowledge (not an external source, no URL, no forwarded content),
this is a thought-only ingest — skip the raw/ and source/ layers entirely.

## Distinction from full source ingest

| Layer | Full source ingest | Thought-only ingest |
|-------|-------------------|-------------------|
| raw/ | Create raw capture | SKIP |
| sources/ | Create curated source page | SKIP |
| concepts/ | Create/enrich concept pages | Create concept page for the reusable idea |
| thoughts/ | Optional (if user reflects) | REQUIRED — dated thought note |
| index.md | Update Concepts, Sources, etc. | Update Concepts + Thoughts sections |
| connection-map.md | Add source + concept links | Add thought → concept link only |
| log.md | Prepend entry | Prepend entry |

## When to use

- User states a fact they know and want preserved: "есть специи которые помогают..."
- User shares a technique, recipe, or practical method from personal experience
- User reflects on an observation that has reusable knowledge content
- No external source is involved — this is the user's own knowledge

## Workflow

1. Ask clarifying questions if the knowledge is incomplete (e.g., which specific spices?)
2. Create concept page in `concepts/` with:
   - English content (per vault language rule)
   - `--about-->` link to the thought page in Relations
   - appropriate tags (domain-specific, not generic)
3. Create thought page in `thoughts/YYYY-MM-DD-slug.md` with:
   - English content (per vault language rule)
   - `--about-->` link to the concept page in Relations
   - `author: Maxim Sobol` in frontmatter
   - tags including `thought` plus domain tags
4. Update `index.md`:
   - Add concept row to Concepts table (with matching pipe prefix)
   - Add thought row to Thoughts section
5. Update `connection-map.md`: add `thought → concept` link at the bottom
6. Update `log.md`: prepend entry (newest-first)
7. Run `check_vault_health.py` to verify no new issues

## Relation types

- Thought → Concept: `--about-->` (canonical, per schema)
- Concept → Thought: `--about-->` (bidirectional)
- Do NOT use `--connects_to-->` or `--expresses-->` for thought→concept; `--about-->` is the standard type for thoughts

## Pitfalls

- Do NOT create a raw/ or sources/ page when there is no external source
- Do NOT use `--connects_to-->` — the schema defines `--about-->` as the canonical relation for thoughts
- Do NOT forget to update connection-map.md — it's easy to overlook when no source pages are involved
- When the thought content is originally in Russian, the vault page must still be in English per the vault language rule; preserve the user's meaning, not the literal wording
