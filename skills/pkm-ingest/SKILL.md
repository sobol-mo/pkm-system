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

### Partial publication-date rule

Some sources expose only partial date granularity, especially local PDFs or slide decks whose title page shows only a month and year such as `May 2026`.
In that case:
- preserve the visible date evidence exactly as seen in the body text
- do not invent a day value in frontmatter
- use the coarsest truthful machine-readable value available on the curated page (for example `date: 2026` when month-only precision does not fit the current field contract cleanly)
- state explicitly that the exact day is unverified
- in the raw note, mention where the date came from, for example `document date shown in PDF: May 2026`

The rule is conservative truthfulness over fake precision.

### Local PDF extraction fallback

When the user sends a local PDF and no text is inlined, first preserve the original file under `raw/files/` and treat it as the canonical evidence artifact.
If the session Python lacks PDF libraries, prefer an ephemeral extraction path over mutating the environment:

```bash
uv run --with pypdf python3 - <<'PY'
from pypdf import PdfReader
reader = PdfReader('document.pdf')
for page in reader.pages:
    print(page.extract_text() or '')
PY
```

Use this to inspect the document, recover title/authors/table of contents/key sections, and verify whether the visible publication date is exact or only partial.
This is especially useful for one-off source ingest where installing a permanent PDF stack would be unnecessary.

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
asset: raw/files/document-slug.pdf  # optional — local copy of the source file
tags: [raw, topic1, topic2]
---
```

Rules:
- `curated_page` is REQUIRED — it creates the bidirectional raw↔source link that the vault's link contract depends on
- `asset` is OPTIONAL — local copy of the source file (PDF, image, data file) stored in `raw/files/`
- `source_kind` describes the type of source (not `source_type`, which conflicts with `type` in the schema)
- `tags` includes `raw` as the first tag plus topic tags
- **Obsidian clickability rule:** YAML frontmatter values are NOT clickable in Obsidian. Both `curated_page` and `asset` MUST also appear as clickable markdown links in the body of the raw file, immediately after the title/metadata block. Frontmatter = machine-readable contract. Body link = human navigation.
- After creating a raw file, run `check_vault_health.py` to verify links resolve

**Body link template** (place after the title and metadata lines):
```
**Curated page:** [source-slug](../sources/source-slug.md)  
**Local PDF:** [document-slug.pdf](files/document-slug.pdf) (X.X MB)
```


## Curated Page Frontmatter Convention

Canonical relation types, entity types, temporal conventions, page format, and link policy live in `Requirements/05-knowledge-graph-schema.md`.
This skill is not a second ontology document.
This section is only an operational summary for ingest execution.

Source-of-truth contract:
- `Requirements/05-knowledge-graph-schema.md` = canonical meaning contract
- `skills/pkm-ingest/SKILL.md` = execution workflow for applying that contract during ingest
- `skills/pkm-ingest/references/*` = optional examples and edge-case aids only, never normative sources of ontology truth

If this skill, a reference file, and the schema appear to disagree, follow the schema and patch the skill/reference.

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

### Source page frontmatter — additional fields

The operational schema (`schema-driven-vault-maintenance/references/operational-schema.json`) requires additional fields for `type: source` pages beyond the canonical template:

```yaml
---
title: "..."
type: source
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: "Author Name(s)"
url: https://...
date: YYYY  # or YYYY-MM-DD
tags: [source, ...]
sources: []  # still valid alongside author/url/date
asset: raw/files/document-slug.pdf  # optional — local copy of the source file
---
```

Required for source pages: `title`, `type`, `created`, `updated`, `author`, `url`, `date`, `tags`.
The canonical schema (`05-knowledge-graph-schema.md`) uses `sources:` as the generic field; the operational schema adds source-specific metadata fields that the health checker enforces.
If `author`, `url`, or `date` are missing, the health checker flags `curated_missing_required_fields`.
Do not omit `sources: []` even when adding `author/url/date` — both sets of fields coexist.

## Curated Layer Rules

Update existing pages before creating new ones.
Create new concept pages only for stable reusable concepts, not every phrase in a source.
When the source mainly adds evidence or nuance to an existing page, enrich the existing page instead of spawning a duplicate node.
Do not default to writing new canonical curated pages into repo-local `PKM/wiki/` after vault cutover.

Think in terms of graph-worthy entities, not only concepts.
The unit of preservation is not just an interesting idea but any reusable entity that should live independently in the graph.

Allowed graph-worthy entity classes include:
- concept
- framework node
- taxonomy or collection node
- technique node
- relation hub

Do not force every graph node to masquerade as a concept.
Some nodes exist mainly to organize or connect other nodes.

Minimum operational rule:
Every ingest must extract at least a small graph-useful set of entities and relations.
If the source is saved only as raw text plus a source summary, the knowledge remains trapped inside the source and has not yet been integrated into the graph.

## Ingest Depth Modes

Choose the depth of extraction intentionally.
Do not treat every source as requiring the same amount of ontology work.

### Level 1 — source capture

Use when the goal is to preserve the source quickly without deep decomposition yet.
Still extract a minimal graph-useful set:
- raw capture
- source page
- 2 to 5 important graph-worthy entities
- the most important explicit relations needed for later retrieval

### Level 2 — structured extraction

Use when the source contains several reusable ideas and a meaningful internal structure.
Extract:
- main concepts
- major frameworks, techniques, or taxonomy nodes
- the key relations between them, keeping hierarchy cleaner than prose when the branch is meant for graph-first or teaching-first use

### Level 3 — ontology expansion

Use when the source is itself highly structured, strategically important, or clearly intended as a conceptual map.
Here the agent should perform ontology extraction plus normalization:
- recover the source's conceptual architecture
- separate concepts from organizing nodes
- preserve contrasts, taxonomies, frameworks, and relation hubs as first-class graph entities where justified
- avoid flattening a mind map into a single summary page

Heuristics for choosing Level 3:
- the author presents an explicit map, framework, taxonomy, or staged model
- the value of the source lies in distinctions between neighboring concepts
- Maxim explicitly signals that the source is important for graph-building, ontology, or structured reuse
- later retrieval would be degraded if the structure stayed buried inside prose

### Structural-link policy for Level 3 ingests

Follow the canonical link policy in `Requirements/05-knowledge-graph-schema.md`.

Operational ingest reminder:
- preserve layered traversal for structurally rich sources
- keep taxonomy, framework, technique, and obstacle/distortion roles separate
- do not create parent -> all descendants links by default
- do not create source -> branch plus source -> all branch leaves by default; let the source point to the first-layer organizing node and let the branch node carry the descendants
- avoid direct leaf -> root links when a valid middle-layer organizing node exists
- inside one taxonomy level, do not default to sibling -> sibling links; keep siblings attached to the shared parent unless a cross-link is semantically necessary
- when a branch is becoming pedagogical or graph-heavy, introduce an intermediate organizing node (for example taxonomy bucket, techniques bucket, obstacles bucket) so traversal stays general -> intermediate -> specific
- use tags as facets and typed links as semantic structure
- add cross-links only when they materially improve retrieval

When prose needs to explain how siblings differ, prefer putting the contrast into the page body rather than encoding every contrast as a graph edge.

Co-listing pages in a retrieval surface is not evidence that those pages should point to each other directly.
Treat those files as navigation aids, not as graph-expansion prompts.

### Cross-linking to existing vault — conservatism rule

When a Level 3 ingest produces new concept pages, do NOT rush to cross-link them with existing vault pages.
The only cross-links that should be created are those where BOTH conditions hold:
1. a clear semantic relationship exists (the new page IS a subclass, instance, enabler, or narrower/broader variant of the existing page)
2. a clear hierarchical relationship exists (the link follows general→specific, parent→child, or abstract→concrete direction)

When either condition is uncertain, ask Maxim in dialog mode rather than forcing the link.
A new page that stands alone in the graph is better than a forced edge that muddies traversal.
The test: if you have to justify the link in a sentence longer than the relation name itself, it's not clear enough — ask.

### Selecting a validation target for hierarchy cleanup

When the user wants to test or demonstrate the hierarchy rules on an existing part of the vault, do not pick a branch that was already cleaned up and now behaves well.
Choose a branch that still shows the failure mode you are trying to detect or fix:
- source -> branch plus source -> many leaves fan-out
- same-level nodes densely cross-linked without retrieval need
- a broad hub whose leaves also link heavily sideways, flattening the graph into a mesh

The goal of the test branch is to stress the rule, not to re-verify an already-normalized example.
A good candidate is slightly messy but still small enough to inspect end-to-end.

If you need a compact worked example, see `references/layered-link-policy.md`.
That reference is illustrative only and must not override the canonical schema.

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
- if asset files are stored in `raw/files/`, source pages and raw captures link there explicitly with clickable body links

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

These files are optional operational aids.
They are not canonical schema documents and must not introduce competing ontology rules.

- references/layered-link-policy.md — compact examples for layered traversal and sparse cross-linking in Level 3 ingests.
- references/commerce-sample-ocr.md — fallback pattern for bot-guarded commercial/book pages where useful content is only visible in preview images.
- references/thought-only-ingest-pattern.md — condensed workflow for thought-only ingests where no external source exists: skip raw/ and sources/, create concept + thought with bidirectional `--about-->` links.

## Common Pitfalls

1. Creating too many tiny concept pages from one source.
2. Forgetting to update index/log/glossary after page changes.
3. Treating curated interpretation as if it were raw capture.
4. Using broken relative links between raw and source pages.
5. **Confusing entity type with topic.** If you find yourself thinking "this concept is about AI, so it should go in an AI folder" — stop. It goes in `concepts/` because it IS a concept. The topic emerges from links, not folder hierarchy. The type-based system prevents the multiple-belonging problem that plagues topic-based trees.
6. **Reducing ingest to summary.** A clean summary is not enough for this vault when the source contains reusable structure. If concepts, frameworks, techniques, contrasts, or taxonomy-like groupings remain buried inside prose, the ingest is incomplete from a graph-construction perspective.
7. **Forcing every node to be a concept.** Some first-class graph entities are organizational rather than conceptual: framework nodes, taxonomy nodes, technique buckets, or relation hubs.
8. **Creating pages without checking existing conventions.** Before writing any new vault page, the deterministic health checker must be consulted — either by running `check_vault_health.py` on the existing vault to see the expected frontmatter shape in action (via sample issues), or by inspecting a recent page of the same type. Creating pages blind leads to frontmatter drift, language violations, missing `## Relations` sections, and non-clickable `relations:` fields that duplicate the link section. The checker catches these automatically, so the fix is to run it pre-ingest for orientation and post-ingest for validation.
9. **Using `## Related` instead of `## Relations`.** The vault convention and health checker both expect `## Relations`. Using `## Related` causes the page to be flagged as missing its Relations section.
10. **Flattening a layered branch from the source node.** If a source links to an organizing node and also to that branch's leaves, the graph loses depth and the teaching hierarchy becomes visually noisy. Prefer `source -> branch entry node`, then `branch node -> direct members`.
11. **Omitting source-page metadata fields.** Source pages (`type: source`) require `author`, `url`, and `date` in frontmatter per the operational schema, in addition to the canonical `title/type/created/updated/tags` fields. The health checker flags missing `author/url/date` as `curated_missing_required_fields`. Always include these three fields when creating or updating a source page.
12. **Taxonomy nodes without a parent taxonomy link.** When creating specialized taxonomy nodes (e.g. `rag-kg-paradigm-taxonomy`, `word-embedding-taxonomy`), link them to the general `taxonomy` concept page as their broader parent with `--narrower_than-->` `[taxonomy](taxonomy.md)`. If the general taxonomy page already exists in the vault, also update it with `--broader_than-->` links back to the new nodes. This keeps the general→specific hierarchy intact and prevents orphan taxonomy nodes.
13. **Patching connection-map.md without enough context.** `connection-map.md` lists the same concept names across multiple sections (Concept→Concept, Source→Concept, Hub Nodes, Clusters), so a `patch` with a short `old_string` like `taxonomy → personal-ontology` will match in 2+ places and fail with "Found N matches". Always include surrounding unique lines (adjacent concept entries, section headers) in the `old_string` to disambiguate which occurrence to replace.
14. **Adding rows to index.md with wrong table prefix.** The `index.md` Concepts table has inconsistent row prefixes — some rows use `|` (single pipe) and others `||` (double pipe). When adding new rows, match the prefix of the immediately adjacent rows. More importantly: always `read_file` the target area before patching — do not patch index.md blind from memory of its format.
15. **Omitting clickable body links for curated_page and asset.** YAML frontmatter values are not clickable in Obsidian. If `curated_page` and `asset` exist only in frontmatter, the human cannot navigate from raw → source or raw → local file. Always duplicate these as clickable markdown links in the body of every raw capture, immediately after the title/metadata block. Use the body link template from the Raw File Frontmatter Convention section.

## Verification Checklist

- [ ] Raw capture saved with enough fidelity to re-check the source later
- [ ] Curated page explains why the source matters
- [ ] Existing pages were preferred over duplicates
- [ ] The ingest produced graph-useful entities and explicit relations, not only a summary
- [ ] For structurally rich sources, concepts were separated from framework/taxonomy/technique nodes where justified
- [ ] Global retrieval surfaces updated where needed
- [ ] Raw/source links verified (bidirectional `curated_page` ↔ relative link)
- [ ] `check_vault_health.py` run post-ingest — no new issues from this ingest
- [ ] Clickable body links present for `curated_page` and `asset` (if asset exists) — not just frontmatter
- [ ] Commit helper used when commit was required

For curated thoughts, also verify:
- [ ] The real file exists at `thoughts/YYYY-MM-DD-slug.md` in the canonical vault
- [ ] The note preserves the user-provided thought unless rewriting was requested
- [ ] `index.md`, `connection-map.md`, and `log.md` were updated when expected
- [ ] The user-facing report includes exact created and updated paths
