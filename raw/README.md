# MOVED

This legacy repo-local `raw/` path has been decommissioned.

Canonical raw source evidence now lives in:

- `Dev`: `/home/maxim/KnowledgeVault/raw/`
- `Prod`: `/home/hermes/KnowledgeVault/raw/`

Canonical vault-path contract:

1. `PKM_VAULT_PATH`
2. `OBSIDIAN_VAULT_PATH` only as a secondary compatibility fallback
3. fallback default: `$HOME/KnowledgeVault`

Do not write new canonical raw captures into this repo-local directory.
Use the resolved canonical vault path instead.
