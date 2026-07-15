---
name: source-ingestion-integrity
description: Use when ingesting external sources into a PKM/wiki where raw evidence, entity extraction, existing-entity reconciliation, and graph links must be reliable.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [pkm, ingest, source-integrity, evidence, entity-reconciliation, digital-mind]
    related_skills: [pkm, pkm-ingest, pkm-query, pkm-lint]
---

# Source Ingestion Integrity

## Purpose

This skill is a quality gate for PKM source ingestion.
Use it alongside the main PKM ingest workflow when a source must become trustworthy graph knowledge, not just a summary.

The core contract:
raw evidence first, curated interpretation second, graph integration third.
Never invert that order.

## When to Use

Use this skill when:
- ingesting YouTube videos, transcripts, articles, PDFs, books, talks, forwards, or long source text
- the user asks to extract concepts, people, techniques, quotes, or relationships from a source
- the source should be connected to existing PKM pages
- the user expresses concern about missing links, duplicate pages, incomplete raw evidence, or shallow summary
- a specialized ingestion agent is being designed or evaluated

## Required Workflow

1. Establish today's real date with `date` before writing metadata.
2. Capture the raw evidence layer before creating curated pages.
3. Verify that raw means raw:
   - transcript raw contains full transcript text
   - article raw contains extracted article text or clear access limitations
   - PDF raw links to the preserved source file and extracted text when available
   - summary-only files are labeled as derived summaries, not raw transcript/article evidence
4. Extract candidate entities:
   - people
   - quoted authors
   - quoted phrases
   - concepts
   - techniques
   - frameworks
   - implementations/tools/systems
   - publications/sources
5. Reconcile every candidate against the existing vault before creating pages.
6. Classify candidates:
   - exact match: link existing page immediately
   - near match: inspect and ask if identity is uncertain
   - new entity: create only after exact/near matches are ruled out
7. Build relations in two layers:
   - source-internal relations between extracted entities
   - vault-crosslinks to existing entities
8. Update global retrieval surfaces: index, connection-map, log, and any relevant MOC/overview.
9. Run the vault health checker.
10. Report honestly: what was captured, what was inferred, what is incomplete, and what remains blocked.

## Transcript Evidence Rule

A file named transcript must contain the full transcript text.
If only a summary was saved, this is an ingestion failure, not a valid raw capture.

If transcript capture fails or cannot be re-run:
- mark the raw file as INCOMPLETE RAW CAPTURE
- explain what is missing
- remove or correct any log/source wording that says full transcript was ingested
- do not claim source-grounded completeness
- ask for fresh cookies or pasted transcript if needed

## Ontology Coverage Audit

For sources that teach a philosophy, life-improvement method, technical framework, or practical system, do a second-pass coverage audit after the first extraction.
The question is not only "what named entities were extracted?" but also "what reusable concepts, techniques, cases, meta-principles, and life tools are still buried in the source?"

Classify missed candidates as:
- standalone concepts: reusable philosophical, psychological, or technical ideas
- technique nodes: repeatable practices such as strategic silence, delay rules, reframing, breathing, or self-review
- person/quote/case nodes: thinkers, attributed quotes, examples, case studies, historical anecdotes
- relation hubs: organizing ideas that connect multiple techniques or concepts
- non-promoted mentions: mentioned in source but not important enough for a page; still record when useful

For each candidate, decide:
- create page now
- enrich existing page
- leave as source-page bullet only
- ask Maxim because ontology value is unclear

A good audit explicitly reports what was extracted, what was missed, and what should be promoted next.
This prevents summary-driven extraction where only the big named frameworks are captured while the practical ontology remains trapped in prose.

## Existing Entity Reconciliation Pass

This pass is mandatory.
Do not skip it because the source is long or because new pages were already created.

For each extracted entity:
- search by exact name
- search by common aliases
- search by slug-like filename
- search distinctive quote text
- inspect existing pages before deciding to create a new one

Conservatism about semantic cross-links does not apply to identity reconciliation.
If a source explicitly mentions Mark Twain and `people/mark-twain.md` exists, link Mark Twain.
If a source uses a known quote and the quote page exists, link the quote.
If a source uses an existing concept with the same meaning, update/link the existing concept rather than leaving a plain-text mention.

## Pitfalls

- Do not call a summary a transcript.
- Do not let extracted people remain plain prose when person pages already exist.
- Do not create duplicate person/concept pages before searching the vault.
- Do not claim full source ingest when access failed or cookies expired.
- Do not trust model confidence on entity identity without vault lookup.
- Do not treat health score alone as proof of semantic correctness; health checks catch schema/link issues, not missed conceptual links.

## Specialist Agent Boundary

For complex ontology-building, prefer a dedicated ingestion specialist agent over a generic assistant.
The specialist should optimize for:
- evidence preservation
- entity extraction
- entity reconciliation
- graph linking
- auditability
- explicit incompleteness reporting

Generic assistants tend to summarize; ingestion specialists must preserve and reconcile.

## Verification Checklist

- [ ] Current date checked with `date`
- [ ] Raw evidence is complete, or incompleteness is explicit
- [ ] Raw/source bidirectional links exist
- [ ] Candidate entities were listed and reconciled against existing vault pages
- [ ] Exact matches were linked immediately
- [ ] Near matches were inspected or escalated
- [ ] New pages are not duplicates
- [ ] Relations include both source-internal links and existing-vault links
- [ ] Index, connection-map, and log were updated
- [ ] Log does not overclaim capture completeness
- [ ] Health checker was run
- [ ] Final report states blockers and limitations clearly

## References

- references/source-evidence-integrity.md — session-derived failure pattern and audit checklist for incomplete transcript/raw capture problems.
- references/ontology-coverage-audit.md — second-pass audit pattern for finding concepts, techniques, people, quotes, cases, and meta-principles missed by summary-driven extraction.
