---
name: pkm-ingest-crosslinking
description: Systematic cross-referencing of new PKM entities against the existing vault during source ingestion. Date verification and vault entity lookup before creating pages or adding relations.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [pkm, ingest, cross-linking, vault]
    related_skills: [pkm-ingest, pkm, pkm-lint]
---

# PKM Ingest — Cross-Referencing with Existing Vault

## Overview

A companion workflow to pkm-ingest that addresses the systematic gap: when a new source references entities (people, concepts, quotes, frameworks), the agent must proactively check which of those entities ALREADY exist in the vault and add cross-links — before creating new pages and before finalizing the ingest.

The failure mode is a fragmented graph: the Stoicism video mentions Mark Twain, but the vault's existing Mark Twain quote page is never connected because the ingest workflow lacks a search-the-vault step.

## When to enable

Use this alongside pkm-ingest for any Level 2+ ingest. Always-on for this vault: every new source may reference existing vault entities silently.

## Workflow step (insert between Base Workflow steps 4 and 5 of pkm-ingest)

After saving the raw capture and before creating curated pages:

1. **Extract all graph-worthy candidates from the source** — people quoted or referenced, concepts named, frameworks invoked, techniques described, quotes attributed, cases/examples, and meta-principles implied by the source's practical argument.
2. **Do a second-pass ontology coverage audit for Level 2+ sources** — ask what useful philosophical concepts, life-improvement tools, techniques, cases, and relation hubs are still buried in the prose after the obvious named frameworks were extracted. Summary-driven extraction is not enough for this vault.
3. **For each candidate, search the vault** — use `search_files` on the vault for the entity name, aliases, person name, concept title, quote snippet, and distinctive case/example text. Also check `index.md` and `connection-map.md` for existing pages by scanning the entity's canonical form.
4. **Build a cross-reference list**: for each match found, add a typed relation from the new source page and from the new concept page to the existing entity.
   - People referenced → `--referenced_person--> [Name](people/name.md)` on the source page
   - Concepts named → `--related_concept--> [Concept](concepts/concept.md)` on the new concept page
   - Quotes attributed → `--referenced_quote--> [Quote](quotes/quote.md)` on the source page
4. **If an existing page matches an ONTOLOGY entity** (person, quote, concept), prefer linking to it over re-creating the entity. Do NOT create a duplicate person page or quote page. 
5. **Only create new pages** for entities that have NO existing vault representation.
6. **Definitional closure on our prose, not only on the source.** After the curated page is drafted, extract the terms *we used to explain the node*. Search the vault for those terms too. If they do not exist and they are graph-worthy, create them in the same ingest. Source-entity extraction is not enough: a page can mention only DocLang in the source title while its body teaches via OTSL and DocTags.

## Pitfalls

1. **Assuming all references are new.** In this vault, many philosophers, authors, and concepts already have pages. Always search before creating.
2. **Extracting only named frameworks.** A source can contain valuable ontology that is not presented as a capitalized term: practical techniques, self-audit questions, cases, physiological mechanisms, and meta-principles. For philosophy, psychology, and quality-of-life sources, run a second-pass audit for what should become reusable graph nodes.
3. **Skipping people.** People are the most commonly missed cross-reference — the source names a thinker (e.g. "as Marcus Aurelius said") and the thinker has a vault page, but no link is added.
4. **Date blindness.** Always run `date` at the start of the ingest session. DO NOT reuse dates from conversation context or session summaries — they may be stale. A stale date means every new page carries the wrong creation timestamp.
5. **Partial name matching.** "Mark Twain" and "Samuel Clemens" are the same person. When a source uses a nickname/alias, search both the common name and the formal name.
6. **Closing the source vocabulary but not the describing vocabulary.** Neighbor concepts used in our definition remain unlinked jargon. Treat that as an incomplete ingest.

## References

- `references/second-pass-ontology-audit.md` — session-derived pattern for auditing missed concepts, techniques, people, quotes, cases, and meta-principles after a shallow first-pass extraction.

## Verification

- [ ] `date` was called at session start, and every created page uses the real date
- [ ] All graph-worthy candidates from the source were checked against `index.md` / `connection-map.md`
- [ ] A second-pass ontology audit was done for Level 2+ sources: missed techniques, cases, meta-principles, people, quotes, and practical life tools
- [ ] Every existing match received a typed cross-link relation
- [ ] No duplicate pages were created for entities that already exist in the vault
- [ ] Definitional terms on new curated pages were searched, then linked or created
- [ ] `check_vault_health.py` run post-ingest confirms no new issues
