Pattern: X post with inaccessible native article, accessible mirror available

When to use

Use when an X post exposes only teaser text or a card title, while the linked x.com/i/article, thread expansion, or video/transcript is not directly retrievable in-session.

Minimal preservation contract

- capture the X post URL, author, timestamp, visible teaser text, and card title
- record the failed native endpoint explicitly if one was attempted
- add exactly one accessible mirror or secondary summary page for enrichment
- mark which details are mirror-derived rather than primary-source verified

Good raw-note shape

- Source metadata
- Verbatim visible preview from X
- Verification path:
  - primary X URL
  - inaccessible endpoint
  - accessible mirror URL
- Mirror-derived operational details
- Limits and confidence

Good curated-page shape

- focus on durable patterns, not every tool mention
- say clearly that richer detail came from a mirror
- avoid adopting vendor/tool specifics unless they matter architecturally

Worked example from session

Primary source:
- X post by Ben Holmes, 2026-07-07

Observed failure:
- direct x.com/i/article/... endpoint not retrievable

Accessible enrichment path:
- daily.dev mirror summary of the linked material

Durable extracted pattern:
- low-friction capture
- auto-enrichment/backlinks
- markdown wiki compilation
- visualization layer
- scheduled cloud refresh

Conservative lesson

When the primary platform is only partially accessible, the ingest should still preserve the source, but the provenance boundary matters as much as the content.
