# Preconditions for thought-simple

Vault mode:
- isolated temp vault or seeded temp workspace

Assumptions:
- `PKM-idea.md` exists in the system project area and is append-only
- no external source URL is present
- no new curated thought page is required for this MVP fixture

Must already exist:
- `PKM-idea.md`

Must not be required:
- `sources/` page creation
- `raw/` source capture creation for an external document
- `people/` page creation for Maxim

Expected raw destination:
- append to `PKM-idea.md`

Reason:
- this fixture tests the most conservative baseline behavior for thought capture before any ontology expansion or curation logic is added
