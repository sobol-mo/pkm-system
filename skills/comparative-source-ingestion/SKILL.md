---
name: comparative-source-ingestion
description: Add an external implementation, repo, framework, or methodology into the PKM as a source plus comparative analysis against the local architecture.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [pkm, ingest, comparison, architecture, repo-analysis]
    related_skills: [pkm, pkm-ingest, pkm-query, obsidian]
---

Comparative source ingestion

Overview

Use this when the user does not just want a source stored, but wants an external system understood in relation to our current system.
Typical triggers:
- add this repo/framework/article to the knowledge base
- compare this approach to ours
- what should we borrow from this system
- how does this implementation differ from our architecture

This skill is for comparative ingestion of external systems into a PKM or wiki.
It is not for ordinary single-page note capture.

When to use

Use when:
- the source is an implementation, repo, framework, methodology, or architecture pattern
- the user wants both preservation and comparison
- the output should become reusable knowledge, not just a chat answer

Do not use when:
- the user only wants a summary with no vault update
- the source is a simple quote or short article with no architectural comparison value

Minimum artifact set

1. raw capture
Preserve the fetch method and concrete evidence inspected.
For repos, capture README claims, observed file layout, key scripts, and any verification run.

2. source page
Summarize why the external system matters.
State boundaries clearly: what it is for and what it is not for.

3. implementation page
Represent the external system as an implementation, not only as a source.
Record what it instantiates, complements, or does not replace.

4. analysis page
If the user asks how it differs from our approach, create a dedicated comparative analysis page.
Do not scatter the comparison across raw/source/implementation pages only.

Recommended comparison axes

- core abstraction: ontology, schema, graph, memory layer, workflow engine, retrieval layer, etc.
- primary value: semantics, hygiene, retrieval, orchestration, automation, governance
- epistemic model: raw, curated, compiled layers
- maintenance model: health checks, dedup, repair, decay, cron upkeep
- portability: model-agnostic storage, runtime compatibility, protocol boundaries
- worldview specificity vs generic applicability
- deterministic scripts vs LLM-driven workflows

Workflow

1. Inspect the source directly.
2. Record concrete evidence, not just claims.
3. Identify whether it should exist in the PKM as source only or also as implementation.
4. If comparison is requested, create a dedicated analysis page.
5. Update retrieval surfaces so the new knowledge is easy to find later.
6. If the source exposes tests or deterministic verification commands, run at least one real verification step and record the result.

Verification rule

Never rely only on README positioning when the source offers a runnable verification path.
Prefer at least one real command with concrete output: tests, health command, CLI help, or script execution.
Record the result in the raw capture and summarize it in the source or implementation page.

Indexing rule

For comparative implementation ingests, update:
- index
- log
- connection-map
- glossary only if a genuinely reusable term enters the shared vocabulary

Common pitfalls

1. Creating only a source page for something that is clearly also an implementation.
2. Giving comparison only in chat and not saving it as an analysis page.
3. Repeating README marketing language without direct inspection.
4. Forgetting to capture what is borrowable versus what should not be copied.
5. Treating operational vault-governance tools as if they automatically replace semantic ontology systems.

Support files

- references/comparative-implementation-ingest.md — compact checklist and comparison axes for repo/framework ingest tasks

Verification checklist

- raw capture created with evidence and fetch method
- source page created or updated
- implementation page created when the source is an actual system
- analysis page created when comparison was requested
- at least one real verification step recorded when available
- index, log, and connection-map updated
- borrow vs do-not-copy distinction made explicit
