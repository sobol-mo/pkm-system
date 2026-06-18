YouTube/long-form media ingest notes

When the source is a YouTube video and automated transcript extraction is unavailable or unreliable, treat a user-provided transcript/text file as the canonical content layer for PKM ingest. Do not block source creation on missing yt-dlp or transcript APIs.

Recommended evidence order for metadata and participant verification:
1. YouTube oEmbed for title/channel baseline.
2. Video page JSON / structured data for description fragments.
3. Official channel/about pages for role framing.
4. Authoritative external pages for participant bios when needed.
5. User-provided transcript/text for claims, concepts, and quote extraction.

PKM modeling lessons from this ingest:
- Create new concept pages when the source introduces a distinct angle not cleanly covered by an existing concept, even if there is thematic overlap.
- Keep implementation/project entities separate from people/concepts when a concrete product or company is mentioned repeatedly.
- In frontmatter source arrays, keep bare source IDs without a $ prefix; reserve $-prefixed forms for inline knowledge-link syntax only, if the vault uses that convention.
- After bulk creation, run a consistency pass specifically for broken source references and updated dates in log/index artifacts.

Useful for future ingests:
- Debate/interview sources often require separate handling for host vs guests vs referenced third parties.
- If external tooling is partial, combine lightweight public metadata with transcript-driven concept extraction instead of delaying the ingest.

## Metadata-only ingest (no transcript available)

When ALL retrieval paths fail (IP block, expired cookies, no user-provided transcript) but the user wants the video in the vault:

1. Create a minimal raw capture with oEmbed-verified metadata (title, channel, canonical URL).
2. Include an explicit "Retrieval status" section noting which methods failed and why.
3. Use `publication_date: unverified` in raw frontmatter, `date: unverified` in source frontmatter.
4. The raw body should contain: verified metadata block, retrieval status block, and context block (why the user asked to add it).
5. Link to existing related sources, implementations, and people rather than treating the video as isolated.
6. Run the health checker post-ingest — it accepts `date: unverified` without flagging.
