---
name: multimodal-source-ingest
description: Ingest multimodal sources into a PKM/wiki system, especially posts or articles with attached screenshots, infographics, slides, or image-only details that must be preserved.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [pkm, ingest, multimodal, wiki, infographic]
    related_skills: [pkm, pkm-ingest, pkm-query, pkm-lint, pkm-system-boundaries, obsidian]
---

Use this when a source is not just text: social posts with attached images, screenshots of threads, infographics, slide snapshots, or documents where part of the meaning lives in the image.

This skill is a specialist companion to pkm-ingest, not a replacement for the generic PKM ingest contract.

Core rule

Treat the source as a multimodal artifact, not as a text post plus optional image. If the image contains examples, labels, taxonomy, caveats, or other content missing from the text, ingest that material explicitly.

What to preserve

- source metadata: author, platform, date, link, title if any
- raw text from the post/article/document
- image-only content: examples, labels, captions, diagrams, lists, footnotes, callouts
- why the source matters: terminology, taxonomy, checklist, decision frame, historical context, or worldview relevance
- links to existing concepts instead of duplicating nearby nodes

Recommended workflow

1. Identify the unit of ingest.
Decide whether the source should be modeled as one multimodal source or multiple separate sources. Default to one source page when text and image are clearly one publication.

2. Extract both channels.
Capture the text content and inspect attached images separately. Do not assume the text preview already contains the image information.

For Telegram or similar social-post ingests, prefer a layered extraction path:
- fetch the public post text from the web view or embed view first so the raw note preserves the exact post framing
- treat attached images as a second channel and run OCR when the useful content is a cover, table of contents, diagram, or workflow screenshot
- if the post points to an attachment in comments or a secondary location, save the public pointer even when the file itself is not yet directly retrievable
- record the attachment state precisely: captured file vs public pointer only vs unverifiable mention

3. Classify the source value.
Decide what the source is useful for in the knowledge system:
- terminology reference
- conceptual map
- checklist or gap-analysis scaffold
- evidence for a claim
- historical/political/ethical framing

4. Write a raw note that keeps fidelity.
Preserve the original structure and note which items came only from the image.

5. Update wiki pages.
Create or update:
- a source page
- person/entity pages if the author matters
- concept pages for new stable concepts
- bridge links into nearby existing concepts

For PKM projects with raw/ plus wiki/sources/ split:
- raw is the fidelity layer: original capture, extracted text, image-only details, source URL, and attached assets
- wiki/source is the curated layer: why the source matters, how it connects into the graph, and the stable retrieval surface
- link them both ways
  - source page should link to the raw capture
  - raw note should link back to the source page
- verify relative paths from the file's real location, not from the conceptual layer name
  - from wiki/sources/<note>.md to raw/<note>.md the relative link is ../../raw/<note>.md
  - from raw/<note>.md back to wiki/sources/<note>.md the relative link is ../wiki/sources/<note>.md
  - from wiki/sources/<note>.md to raw/assets/<file> the relative link is ../../raw/assets/<file>
- if the source includes an infographic, screenshot, or slide that carries meaning, store the asset in the raw layer and embed a preview or direct link from the source page
- avoid source pages that only point to themselves via frontmatter identifiers; preserve human-navigable links between raw and curated layers
- do not trust copied link patterns from older notes; a wrong relative path can replicate across many source pages unchanged
- after editing relations, click-test or otherwise verify that the source->raw link does not resolve back into wiki/sources by mistake
- when the repo uses a stable raw/wiki split, add a deterministic pre-commit or audit check for suspicious path shapes rather than relying on the model to remember them

- do not rely on a frontmatter id or link text that looks correct if the markdown target path is wrong
- for assets stored under raw/assets/, a source page in wiki/sources/ will usually embed them via ../../raw/assets/<file>
- add a backlink from the raw note to both the source page and the stored asset when the asset itself carries information

6. Prefer integration over duplication.
If a concept already exists, enrich or cross-link it rather than creating near-duplicate pages.

7. Verify retrieval value.
Confirm that a future query could recover:
- the main thesis
- image-only details
- why this source matters
- where it connects into the graph

Pitfalls

- Dropping image-only examples because the text looks complete
- Treating an infographic as decoration instead of content
- Creating many tiny concept pages when the source is better kept as a source-centric taxonomy
- Copying a taxonomy without stating how it should be used in the target PKM
- Failing to distinguish quoted source content from your framing of its relevance

For PKM-style projects

- Keep raw plus curated/wiki layers distinct
- If the source is most valuable as a compact taxonomy, preserve it as taxonomy first and ontology second
- Use existing anchor concepts as bridges so the ingest strengthens the graph instead of fragmenting it
- If attached images add missing examples, store them explicitly as image-only additions
- Keep PKM-specific operational helpers with the owning skill, not as standalone project-local scripts with no context
- Put reusable validators, fixers, and ingest helpers under the skill's scripts/ directory and document purpose, trigger conditions, inputs, outputs, and limits in SKILL.md
- Treat the PKM repo primarily as state plus curated knowledge artifacts; treat procedural automation and rationale as skill assets unless the project itself is explicitly the system-of-record for that automation

Automation placement

When an ingest workflow needs a deterministic checker or repair tool:
- prefer adding it to the relevant Hermes skill under scripts/
- add a one-line pointer in SKILL.md so future agents know it exists
- keep project-local wrappers only if there is a deliberate repository-level integration point
- avoid leaving a script in the PKM repo "just because it was created during the task"; without the skill context, future reuse becomes guesswork

Verification checklist

- Raw note contains both text and image-derived content
- Source page explains why the source is useful
- Image-only material is explicitly marked or otherwise recoverable
- New concepts are only created when they are stable and reusable
- Existing concept pages gained links where appropriate
- If the active vault/repo uses raw/source linking, run `skills/multimodal-source-ingest/scripts/check_raw_source_links.py <vault_or_repo_root>` before closing the task

Support files

- references/pkm-social-post-pattern.md — concise pattern from a real session ingesting a social post plus infographic into a PKM repo
- scripts/check_raw_source_links.py — deterministic checker/fixer for raw↔source relative links in either the canonical vault layout (`sources/`, `raw/`, `assets/raw/`) or the legacy repo split (`wiki/sources/`, `raw/`, `raw/assets/`)
