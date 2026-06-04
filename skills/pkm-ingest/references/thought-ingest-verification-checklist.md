Thought ingest verification checklist

Use this after any automated or manual KnowledgeVault thought ingest.

Required outcomes
- A real file exists at thoughts/YYYY-MM-DD-slug.md in the production vault.
- The note body preserves the user-provided thought unless rewriting was requested.
- The vault registries expected by this vault were updated, typically index.md, connection-map.md, and log.md.
- The user-facing report includes exact created and updated paths.

Decision rule for quotes
- Verified attribution and source: standalone quote note may be created if the vault schema supports it.
- Unverified attribution or source: keep the quote inline inside the thought note and say that quote-note creation was intentionally skipped.

Red flags
- Only a route, stub, plan, or setup artifact was changed.
- The assistant says the tool is ready but cannot name the final note path.
- The assistant reports success without checking index/log side effects.

Minimal completion statement
Created: <thought path>
Updated: <index path>
Updated: <connection-map path>
Updated: <log path>
Quote handling: inline only or separate quote note, with reason.
