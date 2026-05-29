---
name: pkm-query
description: Use when answering from an existing PKM wiki. Retrieve from curated pages first, fall back to raw only when the wiki is insufficient.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [pkm, query, retrieval, synthesis, wiki]
    related_skills: [pkm, pkm-ingest, pkm-lint, obsidian, pkm-system-boundaries]
---

# PKM Query

## Overview

Use the wiki as compiled knowledge, not as a folder of files to paraphrase blindly.
Query work means retrieving from existing PKM pages, synthesizing a direct answer, and citing the consulted pages.

For this project's current migration state, the canonical read surface is the resolved `KnowledgeVault` path. Repo-local `PKM/wiki/` is a legacy mirror/reference surface and should not be the preferred source when the canonical vault is available.

## When to Use

Use this skill when:
- the user asks what the PKM says about a concept, person, source, or pattern
- the request is explanatory or comparative rather than an ingest request
- you need to tell whether the answer already exists in wiki form or only in raw captures

## Retrieval Order

1. Start from `index.md` in the resolved canonical vault path to orient.
2. Read the most relevant curated pages.
3. Synthesize the answer from curated pages.
4. Fall back to raw only if the wiki does not answer the question well enough.
5. If the answer is valuable as a durable artifact, offer to save it as an analysis page.

## Output Rules

- Start with the direct answer.
- Then provide compact supporting synthesis.
- Cite specific wiki files.
- If there is no answer in wiki, say so explicitly.
- If raw likely contains the missing answer, say that it exists only in raw and suggest ingest or promotion.

## Contradictions

If multiple pages conflict:
- present the conflict explicitly
- cite the conflicting pages
- do not silently choose one version

## Ambiguity Handling

If the query could refer to several nodes, list the candidate matches and ask which one the user means.
Only ask when ambiguity is real; otherwise answer directly.

## Optional Analysis Capture

When the synthesis itself is valuable beyond the chat:
- ask whether to save it as `analyses/` in the canonical vault
- if yes, create the page and append to the project log if that workflow is active

## Common Pitfalls

1. Jumping to raw files before reading curated pages.
2. Answering from memory without citations.
3. Inventing certainty when the wiki is incomplete.
4. Resolving contradictions silently.

## Verification Checklist

- [ ] Relevant wiki pages were read first
- [ ] Direct answer came before detail
- [ ] Citations point to specific pages
- [ ] Raw fallback used only when needed
- [ ] Contradictions or gaps were stated explicitly
