When ingesting an external repo or method into KnowledgeVault, treat it as a comparative source rather than a candidate replacement for the whole vault architecture.

Workflow
1. Capture the external artifact as a source with stable identifiers: repo URL, author/org, date accessed, short scope statement.
2. Extract the reusable idea, not the product taxonomy. For Autograph-like systems, the reusable layer is operational governance: schema-as-code, deterministic health checks, link hygiene, maintenance guardrails, decay/resurfacing policy.
3. Compare against our canonical architecture explicitly:
   - our semantic core stays ontology-first
   - schema.md remains the worldview/meaning contract
   - operational-schema.json is an additional machine-checkable guardrail, not a replacement for ontology
4. Preserve system boundaries:
   - KnowledgeVault is knowledge state
   - reusable maintenance logic, scripts, and skills live in the PKM System project skill tree
   - runtime bridge directories are not source of truth
5. Materialize the ingest in the vault with at least:
   - source note for the external artifact
   - analysis note describing deltas vs our approach
   - implementation note only when the external artifact also changes how our system is operated
   - connection-map and log updates when the new source affects core architecture understanding
6. Treat raw legacy pages with tolerance. Report them separately from curated notes in health scoring.
7. Only auto-repair links when the target exists and the fix is path-only. Missing target pages stay as backlog or deliberate gaps; do not invent pages just to satisfy the checker.

Autograph-specific conclusion
- Do not import Autograph's vault taxonomy as the new organizing principle.
- Reuse its operational discipline around explicit rules, validation, and hygiene.
- Keep ontology-first meaning-making as the primary layer in Digital Mind / KnowledgeVault.

Common pitfalls
- Mixing knowledge-state files with reusable system-layer skills or scripts.
- Replacing the semantic architecture with a generic folder/schema regime from an external vault.
- Scoring legacy raw captures by curated standards without tolerance.
- Treating setup/system artifacts like PKM-idea.md as ordinary vault-state pages.
