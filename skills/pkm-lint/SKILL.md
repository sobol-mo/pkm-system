---
name: pkm-lint
description: Use when auditing a PKM wiki for contradictions, stale claims, missing links, or structural drift before applying fixes.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [pkm, lint, audit, consistency, wiki]
    related_skills: [pkm, pkm-ingest, pkm-query, multimodal-source-ingest, obsidian]
---

# PKM Lint

## Overview

Audit the wiki before repairing it.
This skill is for health checks, consistency review, and controlled cleanup of a PKM graph.

## When to Use

Use this skill when:
- the user asks to check the wiki, audit it, lint it, or verify relations
- you suspect drift after several ingests
- you need a structured report before deciding what to fix

## Audit Categories

Check for:
- contradictions between pages
- stale claims or superseded assertions
- orphan pages with no meaningful inbound graph links
- concepts mentioned repeatedly but missing their own page when they deserve one
- missing cross-references
- inconsistent terminology or naming
- broken raw/source or asset links
- frontmatter drift when the project depends on it

## Workflow

1. Inspect the relevant wiki surface.
2. Group findings by severity.
3. Report issues before applying fixes.
4. Ask which fixes to apply when the edits are non-trivial.
5. Apply approved fixes.
6. Re-read modified pages.
7. Commit and push if the project workflow expects it.

## Reporting Shape

Report by buckets such as:
- critical contradictions
- navigation or link breakage
- orphan or underlinked pages
- taxonomy or terminology drift
- metadata/frontmatter issues

If there are too many issues, start with high-severity buckets instead of dumping a giant flat list.

## Fix Rules

- Never silently resolve contradictions.
- Never delete pages without explicit confirmation.
- When a deterministic checker exists, run it before or after manual repairs.
- Use project commit helpers when they exist and commit scope is appropriate.

## Common Pitfalls

1. Fixing first and reporting later.
2. Treating every unlinked page as a bug without checking whether it is intentionally isolated.
3. Applying broad terminology rewrites without understanding local context.
4. Forgetting to verify the repair after editing.

## Verification Checklist

- [ ] Findings grouped by severity
- [ ] Report delivered before non-trivial fixes
- [ ] Deterministic checks run where available
- [ ] Modified pages re-read after edits
- [ ] Commit helper used if fixes were committed
