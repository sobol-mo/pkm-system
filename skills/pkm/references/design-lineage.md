PKM design lineage

Purpose
Concise provenance note for why the PKM/Digital Mind workflow looks the way it does.
Use when a future session asks where the raw/wiki/schema pattern came from, what was copied by design, and what was only a comparative influence.

Primary lineage
- Conceptual origin: Andrej Karpathy's llm-wiki idea file (gist), especially the raw sources -> wiki -> schema split and the ingest/query/lint operating loop.
- Working reference implementation actually used during restructuring: balukosuri/llm-wiki-karpathy.
- This repo supplied the practical shape of the wiki layer: raw/, wiki/, CLAUDE.md-style schema, index/glossary/log, and page-type workflow.

Important non-origin references
- myPKA is not the foundation. It is a comparative reference only.
- MemPalace and GBrain are architectural influences in adjacent areas, especially memory and operational patterns, but not the primary source of the wiki schema.

Design takeaway
When reasoning about "why this PKM is shaped this way", start from:
1. Karpathy gist for the concept
2. llm-wiki-karpathy repo for the practical workflow shape
3. only then compare against myPKA / MemPalace / GBrain for secondary ideas

Migration note
The active workflow skills now live under note-taking/: pkm, pkm-ingest, pkm-query, pkm-lint, with multimodal-source-ingest as a specialist overlay.
Legacy oc-skills/pkm remains only as a deprecated breadcrumb layer during migration.