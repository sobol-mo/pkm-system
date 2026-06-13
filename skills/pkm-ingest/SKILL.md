---
name: pkm-ingest
description: Use when adding a new source, thought, quote, forward, or document into a PKM wiki with raw and curated layers.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [pkm, ingest, wiki, digital-mind, ontology]
    related_skills: [pkm, multimodal-source-ingest, pkm-query, pkm-lint, obsidian]
---

# PKM Ingest

## Overview

Generic ingest contract for PKM repositories that separate raw capture from curated wiki state.
Use this for ordinary text sources and as the base contract for multimodal ingest.

For this project's current migration state, the canonical write target is the resolved `KnowledgeVault` path. Repo-local `raw/` and `wiki/` inside the project clone are legacy mirrors/reference state and should not be used as the default destination for new canonical ingest.

## When to Use

Use this skill when:
- the user sends a source, link, forward, quote, note, or text to preserve in PKM
- a raw capture and corresponding curated source page must be created or updated
- the wiki graph needs new concepts, people, implementations, thoughts, quotes, or analyses derived from a source

Prefer multimodal-source-ingest as a companion when screenshots, infographics, or image-only details carry meaning.

## Inputs and Outputs

Inputs:
- URL, pasted text, forwarded content, file, quote, thought, or voice-derived transcript
- optional framing from the user explaining why it matters

Outputs:
- one raw capture in `raw/` under the resolved canonical vault path
- one curated source page in `sources/` under the resolved canonical vault path when the vault uses that split
- updates to existing or new curated pages as needed
- updates to `index.md`, `glossary.md`, `connection-map.md`, and `log.md` when relevant
- confirmation with commit hash if the repo is git-backed and a commit is in scope

## Base Workflow

1. Read the source fully.
2. Decide whether it is a source, quote, thought, analysis seed, or mixed artifact.
3. Save the fidelity layer in `raw/` under the resolved canonical vault path.
4. Identify reusable entities and likely target pages.
5. Create or update curated wiki pages.
6. Add typed relations.
7. Add human-navigable links between raw and curated layers.
8. Update global wiki surfaces that help retrieval.
9. Verify links and changed pages.
10. Commit and push when the project workflow expects it.

## Automation Boundary for Curated Thought Ingest

Automate only the deterministic routine.
Semantic preparation stays with intelligence: interpretation, note shaping, conservative attribution decisions, and linking choices are not the part to force into a brittle script.

For curated thought ingest, the intended split is:
- AI prepares the curated payload or edit decision
- deterministic automation applies the repeatable vault side effects

Do not report success until the production vault contains the note and the expected registry files were updated and verified.
When reporting completion, say explicitly whether the run was end-to-end automated or semi-automated with AI-prepared payload plus script-applied updates.

### Concrete implementation

The deterministic automation lives in the project's shared script at `scripts/knowledgevault_automation.py` (resolved from the pkm-system project root, accessible from this skill as `../scripts/knowledgevault_automation.py`).

Available subcommands:

- **`curate-thought`** — creates/updates a thought page + index + connection-map + log from a JSON payload. Used after AI prepares the payload file.
  Usage: `python3 ../scripts/knowledgevault_automation.py curate-thought <payload.json> [--vault-root <path>]`
- **`capture-thought`** — appends a raw thought to PKM-idea.md (quick capture without curation).
  Usage: `python3 ../scripts/knowledgevault_automation.py capture-thought --text "..." --author "..." --user-request "..."`
- **`run-fixture`** — runs a fixture through the real automation entrypoint (testing).
  Usage: `python3 ../scripts/knowledgevault_automation.py run-fixture <fixture.json>`

All three respect `PKM_VAULT_PATH` env var, then `OBSIDIAN_VAULT_PATH`, then default to `~/KnowledgeVault`.

## Raw Layer Rules

Raw is the capture layer.
Keep original content, source metadata, context, and any extraction notes needed for future verification.
Do not silently rewrite the source into a cleaner narrative and call that raw.
If the project treats raw as immutable after creation, preserve that rule.
Do not default to writing new canonical raw captures into repo-local `PKM/raw/` after vault cutover.

Publication date is a first-class metadata field for this project.
When ingesting a source, always try to establish the original publication date of the source itself, not just the date it was found, forwarded, or saved into the vault.
If the publication date cannot be verified, say so explicitly in both the raw note and the curated source page rather than leaving the reader to assume recency.
For fast-moving AI topics, treat publication date as part of the meaning of the source, not as optional bibliography fluff.

For direct-input quote ingests, treat author attribution separately from publication date.
If the quote arrives as pasted text or user attribution without primary-source verification, preserve the quote exactly as submitted but mark the attribution as not independently verified in both raw and curated layers.
Do not silently upgrade user-supplied attribution into a verified historical fact.

### Raw File Frontmatter Convention

Every new raw file MUST follow this shape:

```yaml
---
title: "Descriptive Title"
type: raw
created: YYYY-MM-DD
updated: YYYY-MM-DD
source_kind: youtube-video | pasted-post | arxiv-paper | forwarded-text | ...
url: https://...
author: name or "unidentified"
publication_date: YYYY-MM-DD or "unverified"
curated_page: ../sources/source-slug.md
tags: [raw, topic1, topic2]
---
```

Rules:
- `curated_page` is REQUIRED — it creates the bidirectional raw↔source link that the vault's link contract depends on
- `source_kind` describes the type of source (not `source_type`, which conflicts with `type` in the schema)
- `tags` includes `raw` as the first tag plus topic tags
- After creating a raw file, run `check_vault_health.py` to verify links resolve


## Curated Page Frontmatter Convention

Every new concept page MUST use this frontmatter shape:

```yaml
---
title: "Page Title in English"
type: concept
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - sources/source-slug.md
tags: [tag1, tag2, tag3]
---
```

Rules:
- **Language**: English only for all vault content (concepts, sources, quotes, thoughts, analyses), regardless of chat language or source language.
- **Frontmatter**: use `tags:` (lowercase kebab-case), not `relations:` or `related_to:`. Tags are the cross-cutting organization mechanism that compensates for folder-by-type limitations.
- **`## Relations` section**: every curated page MUST have a `## Relations` section at the bottom with clickable markdown links to related pages. Do NOT use `## Related` — the health checker expects `## Relations`.
- **sources**: bare source page IDs in frontmatter (no `$` prefix).
- After creating or updating curated pages, run the vault health checker to catch frontmatter, language, `## Relations`, and link violations automatically:
  ```bash
  python3 /home/hermes/.hermes/agents-projects/pkm-system/skills/schema-driven-vault-maintenance/scripts/check_vault_health.py ~/KnowledgeVault
  ```

## Curated Layer Rules

Update existing pages before creating new ones.
Create new concept pages only for stable reusable concepts, not every phrase in a source.
When the source mainly adds evidence or nuance to an existing page, enrich the existing page instead of spawning a duplicate node.
Do not default to writing new canonical curated pages into repo-local `PKM/wiki/` after vault cutover.

## Required Global Updates

Check whether the ingest should update:
- `index.md`
- `glossary.md`
- `connection-map.md`
- `log.md`
- `overview.md` if the big picture changed materially

## Log Ordering Rule

In this vault, `log.md` is newest-first.
When adding a new ingest or refinement record:
- insert the new block directly under the file intro, not at the bottom
- preserve older entries below in descending recency order
- if an automation path writes to `log.md`, verify that it prepends rather than appends
- if you notice mixed ordering from previous runs, fix the ordering before finishing the task instead of leaving the log half-reversed

## Source Refinement Pattern

When a source was already ingested and the user later sends one more quote, correction, framing note, or interpretive nuance:

1. Update the existing raw capture with the new quote or evidence excerpt, preserving whether it came from transcript text, user framing, or direct verification.
2. Update the existing curated source page rather than creating a second source note.
3. If the new material changes the reusable idea layer, enrich the existing concept page that carries that argument instead of spawning a narrow new concept.
4. Add a short refinement entry near the top of `log.md` so later retrieval shows that the source was materially enriched after the first ingest.
5. Keep `log.md` newest-first: fresh entries go directly under the file intro, older entries stay below in descending recency order.
6. Keep epistemic status explicit: quote text, user-supplied context, and independently verified metadata should remain distinguishable.

Typical case: a user remembers an important quote from a previously ingested video and wants the anti-panic framing, example profession, or argumentative role preserved.

## Architecture-post ingest pattern

When the source is a product announcement, release post, vendor architecture summary, or promo image describing a technical system:

1. Treat the post as a real source, not as mere marketing noise, when it contains reusable architecture claims.
2. If the user highlights one specific term or mechanism they want clarified, preserve that framing in the raw note and use it to guide extraction.
3. When the artifact describes an actual platform or system, create both:
   - a source page for the post itself
   - an implementation page for the platform/system
4. If the highlighted mechanism is reusable beyond the source, also create or update a concept page for that term.
5. If a companion image contains labeled architecture blocks, extract only the technically relevant labels and preserve them as image-derived evidence instead of paraphrasing the whole poster.
6. Keep interpretation conservative: distinguish what the source explicitly claims from what we infer about purpose or design intent.
7. For sandboxing or security-adjacent claims, phrase conclusions as likely runtime-isolation / blast-radius control unless the source explicitly proves stronger guarantees.

Typical example:
- user forwards a platform announcement and asks whether `micro-VM` means a secure sandbox
- ingest should preserve the exact phrase in raw
- create source + implementation + concept pages
- answer that the sandbox interpretation is directionally correct, but broader than malware defense alone unless the source provides deeper runtime details

## Cross-source Linking Pattern

When the user asks to link two already-related artifacts such as video ↔ book, interview ↔ article, or talk ↔ paper:

1. Do not just patch one sentence into an existing page if one side of the relation is not yet represented as a source.
2. Create the missing minimal raw/source pair for the newly referenced artifact when needed.
3. Add bidirectional `related_source` links so the relationship is traversable from either page.
4. Update `index.md`, `connection-map.md`, and `log.md` so the new relation is visible in global retrieval surfaces.
5. Preserve epistemic status explicitly:
   - if the user identifies the relation and the source evidence fully confirms it, state it directly
   - if transcript or source evidence supports the relation only partially, write that clearly instead of overstating certainty
6. For videos, distinguish between metadata verified directly (title, channel, canonical URL) and claims supported only by transcript snippets or user framing.

## Link Contract

For vaults with `raw/` and `sources/` split:
- source page links to raw capture
- raw capture links back to source page
- relative paths must be verified from the real file location
- if assets are stored in `assets/raw/`, source pages link there explicitly

Run the deterministic checker from multimodal-source-ingest when the active vault still uses the legacy raw/source relative-link pattern and deterministic verification is available.

## Entity Routing

Folders encode ENTITY TYPE (what a page IS), not TOPIC (what it's ABOUT). This is a deliberate design decision that prevents the multiple-belonging problem — one concept belongs to exactly one entity type, but can link to any number of topics.

| Folder | Entity Type | Goes here when... | NOT here when... |
|--------|-------------|-------------------|------------------|
| `concepts/` | Idea, definition, principle, pattern | A stable reusable idea with definition and relations | It's a specific person's implementation (→ implementations/) |
| `people/` | Person, author, thinker | Someone whose ideas, quotes, or work connects to the Digital Mind | The content is purely about their tool (→ implementations/) |
| `implementations/` | Tool, system, project, codebase | A specific working system or product that instantiates a concept | The content is just an idea about how something could work (→ concepts/) |
| `quotes/` | Verbatim quote | A quotable formulation that Maxim endorses as personality signal | A paraphrased observation (→ thoughts/ or enrich existing concept) |
| `thoughts/` | Maxim's own dated reflection | A first-person insight, opinion, or synthesis by Maxim | A third-party source (→ sources/ + concepts/) |

For quote-anthology ingests, do not store the quote as an isolated fragment.
If the user explicitly says a quote reflects their worldview or that they endorse it, preserve three layers together:
- the quote page in `quotes/`
- the author page in `people/` if the person matters and is not already present
- at least one concept/value/principle page capturing what the quote expresses

Also encode the user's stance explicitly:
- quote `--endorsed_by-->` the user's person node
- quote `--expresses-->` the relevant concept pages
- when justified, the user's person page should carry a worldview relation such as `--values-->` to the concept with temporal scope

This turns a saved quote into a retrievable worldview signal rather than a disconnected citation.
| `analyses/` | Comparative or synthetic study | A comparison of approaches, design decisions, or publication directions | Raw findings from a single source (→ sources/ + concepts/) |
| `sources/` | Curated summary of an external document | A complex source with multiple ideas extracted across several pages | A single idea already captured in a concept page |

### Thought-note rules

Thoughts belong in `thoughts/YYYY-MM-DD-slug.md`.
If a quote appears inside a thought but attribution is not verified, keep it inside the thought note instead of creating a standalone quote note.
Only create a separate quote note when attribution and source are verified enough for the vault's quote conventions.

### The Principle: Type over Topic

`concepts/agent-memory.md` lives in `concepts/` because it IS a concept — not because it's "about AI" (topic). The topic emerges from its links to other pages (execution-loop, digital-mind, mempalace), not from folder placement. This is the wiki's concrete implementation of the Linking Over Categorizing principle.

If you're unsure whether something belongs in `concepts/` vs `implementations/` vs `people/`, ask: "What IS this entity?" — not "What is it about?"

## Guardrails

- If the source contradicts existing wiki content, flag it before resolving.
- If entity extraction is unclear, ask the user what should be preserved rather than inventing ontology.
- If a fetch fails, retry once before falling back to asking for pasted content.
- For commerce and marketplace URLs, normalize to a canonical clean URL before storing it in curated notes. Strip affiliate/tracking query parameters from the primary `url` field, and keep the originally submitted URL only in raw capture when provenance matters.
- If the canonical page is bot-guarded but a readable text-access proxy or mirror is used for verification, record that explicitly in raw notes as a verification method and limitation. Do not pretend the direct page fetch worked if it actually returned captcha/interstitial content.
- If the accessible preview is image-based rather than text-based, extract evidence from the preview images and preserve the access path. Typical pattern: clean product page URL -> text proxy or mobile page -> sample/preview reader -> preview image URLs -> OCR -> raw evidence block + curated summary + explicit limitations.
- For partial-access books and commercial sources, distinguish verified preview-derived contents from unverified full-book claims. Label them as sample-derived or preview-derived, not as the complete table of contents unless fully verified.
- Do not run plain git commit when the project provides a helper with explicit authorship conventions.

## Support Files

- references/commerce-sample-ocr.md — fallback pattern for bot-guarded commercial/book pages where useful content is only visible in preview images.
- references/thought-ingest-verification-checklist.md — deterministic side-effect checks for curated thought ingest into the production vault.

## Common Pitfalls

1. Creating too many tiny concept pages from one source.
2. Forgetting to update index/log/glossary after page changes.
3. Treating curated interpretation as if it were raw capture.
4. Using broken relative links between raw and source pages.
5. **Confusing entity type with topic.** If you find yourself thinking "this concept is about AI, so it should go in an AI folder" — stop. It goes in `concepts/` because it IS a concept. The topic emerges from links, not folder hierarchy. The type-based system prevents the multiple-belonging problem that plagues topic-based trees.
6. **Creating pages without checking existing conventions.** Before writing any new vault page, the deterministic health checker must be consulted — either by running `check_vault_health.py` on the existing vault to see the expected frontmatter shape in action (via sample issues), or by inspecting a recent page of the same type. Creating pages blind leads to frontmatter drift, language violations, missing `## Relations` sections, and non-clickable `relations:` fields that duplicate the link section. The checker catches these automatically, so the fix is to run it pre-ingest for orientation and post-ingest for validation.
7. **Using `## Related` instead of `## Relations`.** The vault convention and health checker both expect `## Relations`. Using `## Related` causes the page to be flagged as missing its Relations section.

## Verification Checklist

- [ ] Raw capture saved with enough fidelity to re-check the source later
- [ ] Curated page explains why the source matters
- [ ] Existing pages were preferred over duplicates
- [ ] Global retrieval surfaces updated where needed
- [ ] Raw/source links verified (bidirectional `curated_page` ↔ relative link)
- [ ] `check_vault_health.py` run post-ingest — no new issues from this ingest
- [ ] Commit helper used when commit was required

For curated thoughts, also verify:
- [ ] The real file exists at `thoughts/YYYY-MM-DD-slug.md` in the canonical vault
- [ ] The note preserves the user-provided thought unless rewriting was requested
- [ ] `index.md`, `connection-map.md`, and `log.md` were updated when expected
- [ ] The user-facing report includes exact created and updated paths
