# Fixture Format

Each fixture represents one workflow scenario for KnowledgeVault automation.

## Directory layout

Each fixture lives under:

`fixtures/<fixture-name>/`

Required files:
- `input.json` — normalized input payload
- `preconditions.md` — initial vault assumptions and special setup notes

Optional later:
- `seed-vault/` — minimal input vault snapshot for isolated execution
- `notes.md` — human comments about ambiguity, semantics, or review expectations

## input.json contract

Required top-level fields:
- `fixture_name` — stable fixture identifier
- `workflow_class` — one of `thought`, `source`, `quote`, `link_request`, `enrichment`, `analysis`, `implementation`
- `automation_mode` — expected behavior mode, for example `capture_only`, `capture_and_curate`, `link_only`
- `user_request` — raw user instruction
- `input_payload` — the actual content to process
- `expected_risk_level` — `low`, `medium`, or `high`
- `allowed_uncertainty` — explicit list of fields that may remain unresolved

Recommended fields:
- `channel` — telegram, local, etc.
- `attachments` — list of attachment references
- `evidence_urls` — list of external URLs if any
- `review_required` — boolean
- `invariants_under_test` — list of workflow invariants this fixture exists to protect

## Example workflow interpretation

- `thought` + `capture_only`
  - preserve the thought as raw/user-originated material first
  - do not invent external sources
  - do not auto-create curated concept pages unless explicitly requested

- `source` + `capture_and_curate`
  - create raw evidence layer and curated source layer
  - update vault surfaces if the workflow requires it

- `link_request` + `link_only`
  - modify relations only
  - do not trigger full ingest for unrelated entities

## preconditions.md contract

Describe:
- whether the fixture assumes an empty temp vault or a seeded vault
- which files must already exist
- which files must not exist
- any specific prior entities that must be reused
- whether `PKM-idea.md` is the expected raw destination

## Fixture design rules

- keep fixtures minimal
- isolate one workflow ambiguity per fixture where possible
- name the invariant being protected
- prefer conservative expected outcomes for ambiguous inputs
- every production bug should become a new fixture
