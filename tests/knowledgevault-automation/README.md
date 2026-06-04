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

Current MVP scripts:
- `run_fixture.py` — runs a deterministic stub implementation against an isolated temp vault
- `check_results.py` — validates diff and workflow-contract expectations against the manifest

Still out of scope:
- real vault mutation engine beyond the deterministic stub
- judge-model semantic review
