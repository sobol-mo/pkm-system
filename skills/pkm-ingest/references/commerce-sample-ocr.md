Commerce/book preview ingest via sample-image OCR

Use when a source page is commercially hosted, bot-guarded, or only exposes meaningful structure through preview/sample pages.

When to apply
- Product page fetch returns captcha, placeholder HTML, or thin marketing text.
- Mobile/product HTML exposes a sample/preview reader link.
- The preview reader renders pages as images, but those images contain the table of contents, chapter list, diagrams, or topic map.

Minimal workflow
1. Save the clean canonical product URL in the curated note.
2. Record any alternate verification path in raw notes: text proxy, mobile page, preview reader URL pattern, OCR method.
3. Extract preview/sample page URLs.
4. If preview content is image-based, OCR the relevant pages.
5. Store the raw evidence as an explicit section such as sample-derived contents evidence.
6. In the curated source page, summarize only what the preview actually proves.
7. Add a limitations note stating that the result is partial if the full work was not accessible.

What to preserve
- Canonical product URL
- Access path used for verification
- Whether the evidence came from text extraction, image OCR, or both
- The exact scope proven by the preview: chapter list, visible subtopics, diagrams, etc.

What not to overclaim
- Do not call preview-derived data the full contents unless every section was actually visible.
- Do not imply the direct canonical fetch succeeded if verification really came from a proxy/mirror/preview path.
- Do not collapse OCR guesses into authoritative claims without marking uncertainty.

Good note language
- Verified sample-derived contents
- Visible subtopics from preview pages
- Limitations: derived from preview/sample pages only; full text unavailable without purchase/access

Typical value
- Recover table of contents from book previews
- Capture diagram-only topic lists from screenshots/pages
- Preserve provenance for later re-check when full access becomes available
