PKM vault vs UserData vs derived machine state

Use this reference when a PKM project has outgrown its original repo boundary and now mixes human knowledge, project setup, and machine indexing.

Core distinction
- setup/meta: repo-managed system artifacts such as AGENTS/CLAUDE docs, backlog, ADRs, scripts, schemas, workflows
- canonical PKM vault: human-facing notes and sources that must sync across devices and remain pleasant to browse/edit in Obsidian-class tools
- derived machine state: LightRAG, Chroma, SQLite graph stores, embeddings, caches, compiled indexes, and other rebuildable artifacts

Decision rules
- If a file exists mainly to explain or operate the system, it belongs to setup/meta.
- If a file is part of the evolving knowledge corpus the human reads and edits, it belongs to the canonical vault.
- If an artifact can be regenerated from the canonical vault and mainly serves retrieval/runtime performance, it belongs to derived machine state.

Operational rule
Do not place the canonical PKM vault into generic server-only UserData merely because both are non-versioned. Their lifecycle differs:
- UserData: server-first, backup-oriented, agent-operational
- PKM vault: human-facing, cross-device, sync-oriented

Naming rule
If Digital Mind is only one domain, do not let it name the whole container. Prefer a broader container such as PKM or Knowledge Vault, with Digital Mind as one domain inside it.

Default target layout
- repo or system project: setup/meta only
- synced vault: inbox, sources, domain notes, idea dumps, curated notes
- server runtime: derived indexes and retrieval stores

Sync/backups
- Sync and backup are different contracts.
- The vault needs cross-device sync, including mobile.
- The vault also needs backup/retention, but backup should not be inferred from the sync method.
- Derived machine state usually needs backup only if rebuild cost is high; otherwise rebuildability is enough.
