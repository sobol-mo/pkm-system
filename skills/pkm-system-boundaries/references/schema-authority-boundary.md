Schema authority boundary for PKM systems

Problem pattern
A PKM system drifts when ontology philosophy is split across multiple writable places:
- legacy schema-file paths outside `Requirements/05-knowledge-graph-schema.md`
- ingest skill instructions
- project requirements/domain docs

This causes meaning drift. The agent starts treating an operational skill as a second schema authority.

Correct boundary
- Canonical semantic schema belongs to the PKM system layer, not the knowledge-state vault.
- Best canonical home: project Requirements layer when the schema defines philosophy, entity types, relation types, temporal conventions, page rules, and link policy.
- Skills are operational consumers of the schema. They may summarize execution consequences, but must defer to the schema for meaning.
- Legacy schema-file paths are deprecated. Agents should point directly to `Requirements/05-knowledge-graph-schema.md`.

Recommended split
- Requirements/: canonical meaning contract
- skills/: operational workflows that apply the contract
- vault/: changing knowledge-state content

Operational rule
When a skill and schema both contain ontology semantics, reduce the skill to:
- a short pointer to the canonical schema
- only the task-specific operational reminders needed during execution

Do not maintain parallel full definitions of:
- entity types
- relation meanings
- temporal rules
- link policy
- page-format philosophy

Migration pattern
1. Create canonical schema in the project system layer.
2. Repoint AGENTS/requirements/backlog/architecture docs to that schema.
3. Patch ingest skills to defer to the schema instead of restating it fully.
4. Remove legacy schema-file path references and point old guidance directly at `Requirements/05-knowledge-graph-schema.md`.
5. Verify operational docs and tooling no longer expect a vault-local schema file.

Why this matters
Schema is philosophy and meaning contract.
Skill is procedure.
Mixing them creates semantic drift and eventually contradictory agent behavior.
