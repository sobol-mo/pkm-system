---
name: schema-driven-vault-maintenance
description: Add an operational governance layer to a PKM/wiki vault using deterministic schema checks, health scoring, and safe structural repair without replacing the vault's semantic ontology.
triggers:
  - schema-driven vault maintenance
  - vault health checker
  - broken markdown links in knowledge base
  - PKM operational schema
  - knowledge vault governance
  - vault gap analysis
  - missing concept recovery from backlinks
  - reconstruct vault pages from source evidence
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
5. Before building new automation, define the acceptance harness first: fixtures, manifest/oracle format, deterministic checker output, and pass/fail gates.
6. Implement deterministic local scripts for checks. Prefer Python and JSON output.
7. Store reusable skills, scripts, and schemas in the owning PKM system project skill tree, not inside the live knowledge vault.
8. Allow legacy tolerance where the corpus justifies it, especially raw capture folders.
9. Auto-repair only when the fix is mechanically provable, for example broken relative links whose correct existing target can be resolved unambiguously.
10. Re-run the checker after changes and report the real delta in score and issue counts.
11. Record the improvement in the vault's own log/changelog if it has one.

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
5. For missing target pages that are concepts, people, or other curated entities: try source-evidence recovery (see below) before relegating to semantic backlog.
6. Re-run the checker again after the recovery pass.
7. Treat the remaining broken links as semantic backlog only when there is no existing source evidence to reconstruct from.

Missing target page recovery from source evidence
When a health report shows broken links pointing to pages that do not exist, the cause is often a concept that was referenced during source-ingest but never created. These pages can be recovered rather than left as permanent backlog.

Method (validated with Maxim on Digital Mind vault):
1. Identify which source(s) and backlinks reference the missing target. Read the page(s) that contain the broken link.
2. Find the original source material — the raw capture or source page that was being processed when the concept was first referenced.
3. Understand what the source material actually says about the missing topic. The source almost always contains the answer.
4. Reconstruct the concept page from the source evidence: extract the key ideas, frame them in the vault's ontology, and link back to the source in Relations.
5. Fix the broken links in all referring pages (remove stale TODO markers, normalize relative paths).
6. Run the checker to confirm the links resolved and the new page meets frontmatter/Relations requirements.

Recover vs when to leave as backlog:
- Recover: the concept was referenced from a source that exists in the vault. The source provides definitional content (examples: a video transcript that discusses "AI-native Architecture", a thought note that requires "Structured Knowledge Ingestion").
- Recover: the missing target is a known entity widely referenced across multiple pages (example: "Philip Kotler" is obviously a person page that should exist).
- Leave as backlog: there is no source evidence in the vault and the concept is unknown or speculative.
- Leave as backlog: the link points to a boundary/system artifact outside the vault scope (example: references to PKM-idea.md from inside the vault — those are setup layer references, not knowledge state).

Pitfall: Do not auto-create placeholder pages to remove link errors. Each recovered page must carry real content grounded in the source material. An empty page with a fixed link is worse than a broken link — it creates a false signal that the concept is covered.

Recovery technique: backlink-first discovery
Start from the health report broken-link sample. For each missing target, find all referring pages. Read those pages to understand what context expected the target. Then trace to the original source material — often a raw capture or source page whose "Wiki Links" section created the reference. The missing concept was referenced during source-ingest; the source IS the evidence to reconstruct from.

After each recovery pass, update the vault log and re-run the health checker. Report the score as a sequence (example: 42 -> 36 -> 35 -> 20 over 4 passes) so the user sees compounding progress.

Recovery patterns that emerged in practice:
- Raw files often link to concepts/xxx.md WITHOUT the ../ prefix. Creating the concept alone does not fix the link — both actions needed: create page AND normalize path to ../concepts/xxx.md.
- Concepts/ pages linking to concepts/xxx.md are double-nested (from concepts/, the correct path is xxx.md). Fix the path when creating the page.
- The recurring origin pattern: a video or book raw capture lists Wiki Links -> --discusses--> [Concept Name](concepts/xxx.md) — this is the moment a missing concept was born. The raw capture IS the evidence.
- After creating the page and fixing all links, remove stale TODO markers like "[TODO: create if needed]" from referring pages.

Pitfall: When patching Relations links, preserve the list format (leading "- " prefix). A patch that drops the prefix is a silent format error. Read back each patched file to catch this.

Pitfall: Self-inflicted broken links from new pages
Creating pages from source evidence introduces its own broken links — each new page's Relations section references other concepts/people that may also be missing. After creating all pages, always re-run the checker and fix the newly-created broken links in a second pass. This is normal and expected; plan for it in batch recovery. Example: 26 pages created -> checker showed 10 new broken links from those pages' own Relations -> fixed in a second pass.

Alias/redirect pages for duplicate concept references
When a source file references a concept by a name or spelling that differs from the existing canonical page filename, create a minimal alias page rather than fixing the source reference:
- Frontmatter with title and tags
- A short note pointing to the canonical page
- Relations: --redirects_to--> [Canonical Name](canonical-page.md)
- Example: n8n-orchestration.md -> n8n-orchestration-for-ai.md
Do NOT create aliases for typos or genuinely distinct concepts - only for known canonical equivalents.

Log update pattern after recovery
After a recovery pass, update the vault's log.md with a structured entry including:
- Score sequence (before -> after)
- Count of pages created by category
- Number of path fixes, boundary redirects, TODO marker cleanups
- The final health state so future sessions can orient from the log alone

Batch creation technique for 10+ missing pages
When the checker reports many missing targets (20+), batch-create them rather than one at a time:
1. Read all referring source files to gather evidence for every target.
2. Group targets by source (e.g. all Next Move Engine sub-components from one source).
3. Use execute_code to write all pages from a single code block - one write_file call per page.
4. After creation, re-run the checker to surface self-inflicted broken links.
5. Fix self-inflicted links (remove non-existent Relations references).
6. Re-run checker to confirm zero broken links before updating the log.
This avoids token waste from 20+ sequential tool calls and gives a clean before/after delta.

Boundary/system link resolution
When the health report flags broken links to files that live outside the vault (for example, PKM-idea.md in the PKM system project repo), do not create those files inside the vault. Instead:
1. Create (or use an existing) implementations/ page about the external system, explaining it as a setup artifact (example: implementations/pkm-system.md documents the PKM System project and explains that PKM-idea.md is its origin document).
2. Re-point all vault-internal references from the external path to the new implementations/ page.
3. Verify with the user: "We have an implementations/ page about Project X — redirect broken links there instead of crossing the boundary?"
This preserves the system/state separation enforced by the vault's architecture.

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
- references/automation-test-strategy.md
- references/operational-schema.json
- scripts/check_vault_health.py

KnowledgeVault run examples
- python3 /home/hermes/.hermes/agents-projects/pkm-system/skills/schema-driven-vault-maintenance/scripts/check_vault_health.py /home/hermes/KnowledgeVault
- python3 /home/hermes/.hermes/agents-projects/pkm-system/skills/schema-driven-vault-maintenance/scripts/check_vault_health.py /home/hermes/KnowledgeVault --json
- python3 /home/hermes/.hermes/agents-projects/pkm-system/skills/schema-driven-vault-maintenance/scripts/check_vault_health.py /home/hermes/KnowledgeVault --write-json /home/hermes/KnowledgeVault/.health/latest.json

Verification standard
The deliverable is not the script alone. Run it on the real vault, capture the actual score and issue counts, and save a machine-readable report when automation is part of the goal.
