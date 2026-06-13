Schema authority boundary for PKM systems

Problem pattern
A PKM system drifts when ontology philosophy is split across multiple writable places:
- vault-local schema.md
- ingest skill instructions
- project requirements/domain docs

This causes meaning drift. The agent starts treating an operational skill as a second schema authority.

Correct boundary
- Canonical semantic schema belongs to the PKM system layer, not the knowledge-state vault.
- Best canonical home: project Requirements layer when the schema defines philosophy, entity types, relation types, temporal conventions, page rules, and link policy.
- Skills are operational consumers of the schema. They may summarize execution consequences, but must defer to the schema for meaning.
- A vault-local schema.md may exist only as a compatibility bridge or pointer for old links and legacy habits. It is not canonical.

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
4. Convert vault-local schema.md into a clearly marked non-canonical bridge if old links still depend on it.
5. Keep the bridge checker-friendly until it can be removed cleanly.

Why this matters
Schema is philosophy and meaning contract.
Skill is procedure.
Mixing them creates semantic drift and eventually contradictory agent behavior.
