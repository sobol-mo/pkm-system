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
- `../../scripts/knowledgevault_automation.py` — real automation entrypoint
- `run_fixture.py` — runs fixture inputs against the real automation entrypoint on an isolated temp vault
- `check_results.py` — validates diff and workflow-contract expectations against the manifest

Still out of scope:
- source/quote/link/enrichment workflows beyond thought capture
- judge-model semantic review
