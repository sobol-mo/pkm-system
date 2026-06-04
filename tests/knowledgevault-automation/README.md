# KnowledgeVault Automation Tests

Purpose: deterministic acceptance and regression tests for future KnowledgeVault automation.

This directory tests workflow invariants, not only file creation.

Structure:
- `fixture-format.md` — contract for fixture inputs
- `manifest-schema.json` — machine-readable schema for expected outcomes
- `fixtures/` — input cases and preconditions
- `manifests/` — expected outcomes for each fixture
- `expected/` — optional golden diffs or text snapshots later

Initial MVP:
- `thought-simple`

MVP principle:
- test a Maxim-originated thought first
- verify raw-first handling before any aggressive curation
- keep semantics conservative

Out of scope for this first commit:
- executable runner
- real vault mutation engine
- judge-model semantic review

Those come after the fixture and manifest contract stabilizes.
