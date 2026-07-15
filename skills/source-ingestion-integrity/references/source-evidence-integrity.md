# Source evidence integrity failure pattern

## Trigger

A source ingest claims that a full transcript, article, or raw evidence capture was saved, but the raw file contains only a summary or derived extraction.

This is a severe PKM integrity failure because raw is the evidence layer. Curated pages can be wrong or incomplete, but raw should let a future agent re-check the source.

## Diagnostic signs

- Raw filename includes transcript, article text, or source capture, but body is only bullet summary.
- Log says full transcript ingested while raw has no continuous transcript text.
- Source page contains detailed derived claims without a complete evidence layer.
- Entity extraction was performed but original wording cannot be audited.
- User notices a missed entity/link that should have been found from full text.

## Corrective action

1. Do not pretend the raw is complete.
2. Mark the raw page clearly as INCOMPLETE RAW CAPTURE.
3. Correct log/source wording that overclaimed full capture.
4. Preserve the derived summary as derived content, not evidence.
5. Attempt to recapture the source from the original URL or preserved asset.
6. If access fails, record the blocker explicitly and ask for the missing transcript/source text.
7. Run an entity reconciliation pass against the existing vault for anything already extracted.
8. Link obvious existing entities immediately.

## Entity reconciliation audit

For each source, check these classes against the vault:

- named people
- quoted authors
- quoted phrases
- frameworks and named laws
- techniques and methods
- books, articles, videos, papers, and source references
- tools, products, systems, and implementations
- concepts already present under another name

Search strategies:

- exact title/name
- lowercase/kebab-case slug
- surname-only for well-known people
- distinctive quote fragment
- acronym and expanded form
- translated term and original-language term

## Important distinction

Conservative semantic cross-linking protects the graph from weak conceptual edges.
It must not block identity links.

Example:
- Weak semantic edge: Brandolini's Law related to every communication concept — require judgment.
- Identity link: source mentions Mark Twain and `people/mark-twain.md` exists — link immediately.

## Final report requirement

The final user-facing report must separate:

- captured evidence
- derived summary
- created/updated graph pages
- existing entities linked
- unresolved candidates
- blockers preventing full verification

Do not say done if raw evidence is incomplete unless the incompleteness is the stated result.
