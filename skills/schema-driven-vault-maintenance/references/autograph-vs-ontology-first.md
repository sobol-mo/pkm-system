Source pattern captured from session:

External source
- Repo: https://github.com/smixs/autograph
- Useful idea: schema-driven operational governance for markdown vaults

What transferred well
- machine-readable operational schema
- deterministic health checker
- health score with explicit penalty weights
- JSON report output for automation
- safe repair of resolvable broken relative links

What should not be copied blindly into ontology-first vaults
- generic node taxonomy as the primary meaning system
- folder/status/type enforcement replacing semantic modeling
- auto-generated placeholder notes to satisfy validators

Recommended synthesis for ontology-first vaults
- semantic schema remains authoritative
- operational schema lives as a separate guardrail layer
- raw capture areas may remain tolerant to missing frontmatter
- curated areas are validated strictly
- only mechanically provable fixes are automated

Concrete implementation pattern from session
- operational-schema.json defines ignored dirs, curated folders, required fields, special root files, weights
- check_vault_health.py scans frontmatter, required fields, folder/type alignment, required sections, and relative links
- checker emits JSON for cron or maintenance tooling
- after safe auto-repair, rerun checker and compare score delta

Decision rule for remaining broken links
If a link target does not exist, do not create a stub automatically. Escalate to semantic review: create a real note, retarget the link, or delete it.
