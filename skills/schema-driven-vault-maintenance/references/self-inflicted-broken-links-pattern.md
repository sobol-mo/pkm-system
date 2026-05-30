# Self-Inflicted Broken Links Pattern

When recovering missing target pages from source evidence, newly created pages often link to other non-existent targets in their Relations section. This creates a second wave of broken links that only appears after the creation pass.

## Real example (2026-05-30 vault gap analysis)

26 pages created from source evidence.
After creation pass, checker reported 10 new broken links. The new pages introduced links to:
- marketing-management, linus-torvalds, open-source-development
- deterministic-workflow, knowledge-vault (implementations/), operating-systems-design
- microkernel-architecture, maxim-sobol, transparent-ai

## Why it happens

When reconstructing a page from source evidence, it feels natural to add rich Relations linking to related concepts. But those concepts likely don't exist either — they were never created, same as the page we're now creating.

## Fix

1. Expect this. Plan for a second pass.
2. After creating all pages, re-run the checker to see what new links are broken.
3. Fix each by either:
   - Removing the link (if the concept doesn't warrant a page yet)
   - Creating the linked page too (if there's evidence)
   - Pointing to an existing canonical page instead
4. Re-run checker to confirm zero.
