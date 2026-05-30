---
name: schema-driven-vault-maintenance
description: Add an operational governance layer to a PKM/wiki vault using deterministic schema checks, health scoring, and safe structural repair without replacing the vault's semantic ontology.
triggers:
  - schema-driven vault maintenance
  - vault health checker
  - broken markdown links in knowledge base
  - PKM operational schema
  - knowledge vault governance
---
Use when a user wants to improve a PKM/wiki/knowledge-vault structurally, especially after showing an external repo or framework and asking what to adopt.

Core rule
Keep semantic ontology and operational governance as separate layers. Do not replace a worldview-driven or ontology-first schema with a generic card taxonomy just because the source system uses one.

What to extract from an external system
Extract transferable operational mechanisms, not foreign meaning systems.
Good candidates:
- deterministic health checks
- machine-readable operational schema
- safe auto-repair for mechanically verifiable issues
- JSON outputs for automation
- freshness/decay signals
- MOC or index regeneration when explicitly useful

Do not import blindly:
- generic type/status taxonomies that flatten the user's ontology
- folder rules that become the meaning system
- auto-creation of placeholder notes just to satisfy validation

Recommended workflow
1. Inspect the target vault's existing semantic schema first. Treat that as authoritative.
2. Inspect the external source and identify only the operational patterns worth borrowing.
3. Before writing files, classify each artifact as knowledge-state content or system-layer implementation.
4. Design a separate operational schema file that complements the semantic schema.
5. Implement deterministic local scripts for checks. Prefer Python and JSON output.
6. Store reusable skills, scripts, and schemas in the owning PKM system project skill tree, not inside the live knowledge vault.
7. Allow legacy tolerance where the corpus justifies it, especially raw capture folders.
8. Auto-repair only when the fix is mechanically provable, for example broken relative links whose correct existing target can be resolved unambiguously.
9. Re-run the checker after changes and report the real delta in score and issue counts.
10. Record the improvement in the vault's own log/changelog if it has one.

Operational schema design guidance
Include:
- ignored directories
- special root files
- curated folder to expected type mapping
- required frontmatter fields by type
- scoring weights by issue class
- optional decay/freshness settings

Health scoring guidance
Use a simple additive penalty model with explicit weights. Weight semantic-structure violations higher than cosmetic metadata gaps. Broken links can be numerous, so keep their per-item penalty lower than type mismatches.

Safe repair rules
Safe to auto-fix:
- path rewrites when the replacement target exists on disk
- legacy path normalization, for example stripping stale `../wiki/` prefixes when the same target exists directly under the canonical vault
- adding missing structural sections when the required content can be inferred confidently
- filling missing frontmatter fields from existing page evidence, for example H1 title, folder-to-type mapping, filename date prefixes, or linked raw-capture metadata
Not safe to auto-fix without review:
- creating missing target notes just to remove link errors
- inventing metadata values with no evidence
- changing ontology or note type assignments to fit the checker

Practical repair order
1. Re-run the checker and classify issues into deterministic versus semantic.
2. Clear metadata debt first: missing frontmatter, missing required fields, missing `## Relations`.
3. Normalize mechanically stale links next, especially legacy repository-era prefixes like `../wiki/`.
4. Re-run the checker immediately after the mechanical pass.
5. Treat the remaining broken links as semantic backlog unless the correct target exists unambiguously.

Frontmatter completion guidance
- Prefer values derivable from the file itself: H1 for `title`, folder mapping for `type`, filename date prefix for `created`/`updated` when no better source exists.
- For `source` pages, look to the linked raw capture first for `author`, `url`, and `date`.
- If authorship is genuinely unavailable but the page still needs a value for schema completeness, use a neutral provenance marker such as `forwarded note` rather than inventing a person.
- Keep list-valued fields in a checker-friendly form that the local validator actually parses consistently.

Important pitfall
When the user says add an external repo to the knowledge base as a source and compare it with our approach, do two outputs, not one:
1. ingest the external source into the vault as a reusable reference
2. produce an explicit difference analysis between imported operational ideas and the local semantic model

Boundary pitfall
Do not let a vault-scoped task trick you into storing reusable maintenance implementation inside the vault itself.
`<vault>/skills/` is knowledge-state contamination when the artifact is actually a PKM system skill, script, or operational schema.
Those artifacts belong in the owning project skill tree, with the vault only consuming their outputs.

Preferred artifact layout
Place reusable scripts with the owning project skill, not inside the live knowledge vault and not as random standalone scripts. Keep the PKM system project directory as the source of truth.

What this skill package owns
- references/autograph-vs-ontology-first.md
- references/operational-schema.json
- scripts/check_vault_health.py

KnowledgeVault run examples
- python3 /home/hermes/.hermes/agents-projects/pkm-system/skills/schema-driven-vault-maintenance/scripts/check_vault_health.py /home/hermes/KnowledgeVault
- python3 /home/hermes/.hermes/agents-projects/pkm-system/skills/schema-driven-vault-maintenance/scripts/check_vault_health.py /home/hermes/KnowledgeVault --json
- python3 /home/hermes/.hermes/agents-projects/pkm-system/skills/schema-driven-vault-maintenance/scripts/check_vault_health.py /home/hermes/KnowledgeVault --write-json /home/hermes/KnowledgeVault/.health/latest.json

Verification standard
The deliverable is not the script alone. Run it on the real vault, capture the actual score and issue counts, and save a machine-readable report when automation is part of the goal.
