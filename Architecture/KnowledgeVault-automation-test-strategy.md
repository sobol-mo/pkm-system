# KnowledgeVault Automation Test Strategy

Status: Draft
Last updated: 2026-06-04

## Purpose

This document defines how we will verify that future KnowledgeVault automation actually preserves the intended PKM workflow instead of merely producing plausible markdown files.

The test strategy is designed before implementation on purpose.
The goal is to make the automation prove that it respects the system's core ideas:

- raw evidence stays distinct from curated knowledge
- type-based entity routing stays intact
- links and global vault surfaces stay consistent
- deterministic mechanics are automated
- semantic judgments remain explicit and reviewable

This document is a test strategy, not an implementation plan.

## Why the test comes first

The main failure mode is not "the script crashes".
The real failure mode is "the script silently produces a vault that looks fine but violates the ontology and workflow contract".

So the test must check not only success of execution, but preservation of invariants.

## What is being tested

Target automation scope:

- capture of incoming material into the correct raw layer
- routing into the correct entity workflow: thought, source, quote, person, concept enrichment, implementation, analysis
- deterministic file creation from templates
- deterministic frontmatter completion when evidence exists
- deterministic update of `index.md`, `connection-map.md`, and `log.md`
- deterministic link creation and link validation
- deterministic structural checks after mutation of the vault

Not fully delegated to automation:

- whether an interpretation is semantically correct
- whether a concept should be created or an existing one should be enriched
- whether a claim is strong enough to be stated as fact
- whether ambiguous material should stay raw pending Maxim review

## Core testing principle

Test the automation against workflow invariants, not against one source type.

A good test harness should work for:

- a thought from Maxim
- a quote
- a book URL
- a video URL with transcript evidence
- a forwarded note
- an update to an existing source
- a relation-only link request

If the same harness cannot evaluate all of them, the harness is too narrow.

## Acceptance model

The automation passes only if all three layers pass.

### Layer A — Mechanical correctness

These are deterministic and must be checked by scripts.

Required checks:

- expected files were created
- no unexpected files were created
- required frontmatter fields exist for curated pages
- folder/type mapping is valid
- `## Relations` exists where required
- raw-to-curated and curated-to-raw links resolve correctly
- `index.md`, `connection-map.md`, and `log.md` were updated when required
- no broken relative links were introduced
- filenames and titles are stable and consistent

This layer should be 100 percent script-verified.

### Layer B — Workflow-contract correctness

These checks are still mostly deterministic, but depend on the workflow design.

Required checks:

- raw evidence is preserved and not rewritten into interpretation
- the automation does not skip raw capture when the workflow requires raw first
- a thought is not incorrectly treated as a source
- a source is not incorrectly stored as a thought
- existing pages are preferred over duplicate creation when an exact target already exists
- uncertainty is marked explicitly when verification is incomplete
- the automation does not invent publication dates, authors, or relations without evidence

These checks should be a mix of script assertions plus fixture-specific expectations.

### Layer C — Semantic adequacy

These checks cannot be fully deterministic.
They exist to ensure the automation does not optimize for structure while losing meaning.

Required review questions:

- did the automation choose the correct workflow class
- did it extract the right reusable entities
- did it over-create concepts
- did it use wording that overstates certainty
- did it preserve the actual meaning of the input

This layer should be reviewed by an LLM judge or by Maxim on a small curated fixture set.

## Test architecture

The test system should have four parts.

### 1. Fixture inputs

A folder of canonical test cases, each with:

- `input.json` or `input.md`
- declared workflow intent
- initial vault preconditions
- expected outputs
- allowed uncertainty

Suggested fixture classes:

1. `thought-simple`
   - Maxim sends a short original thought
   - Expected: append to `PKM-idea.md` or create a `thoughts/` page, depending on the chosen workflow mode

2. `quote-with-author`
   - Quote text plus known author
   - Expected: raw capture, quote page, person page or reuse, concept/value links if explicitly endorsed

3. `source-book-url`
   - Commercial book URL with limited preview
   - Expected: raw source note, curated source page, explicit limitations

4. `source-video-with-transcript`
   - Video URL plus transcript fixture
   - Expected: source page, raw evidence note, extracted entities only where evidence supports them

5. `forwarded-note-ambiguous`
   - Text that may be either thought, source fragment, or scratch note
   - Expected: conservative handling, not aggressive ontology expansion

6. `existing-page-enrichment`
   - Input that should update an existing page instead of creating a new duplicate
   - Expected: mutation of existing page plus log/index updates as needed

7. `link-only-request`
   - User asks to connect two already-known entities
   - Expected: no unnecessary new pages, only relation updates and surface maintenance

### 2. Expected result manifest

Each fixture should declare an explicit oracle.

Oracle fields:

- expected created files
- expected modified files
- expected untouched files
- required frontmatter fields by file
- expected relation targets
- expected log entry pattern
- expected index entry pattern
- expected connection-map entry pattern
- prohibited outcomes

Examples of prohibited outcomes:

- creating a `source` page for a pure personal thought
- writing curated interpretation into raw capture
- creating placeholder notes only to satisfy validation
- inventing a date when the source date is unknown

### 3. Structural checker

This should be a deterministic script layer.

It should run:

- vault health checker
- frontmatter validator
- link resolver
- folder/type validator
- expected-file diff checker
- surface update checker for `index.md`, `connection-map.md`, `log.md`

This layer should return machine-readable JSON.

### 4. Semantic review harness

A smaller review layer runs only on a curated subset of fixtures.

Its job is to answer:

- was the workflow class correct
- were the extracted relations defensible
- was uncertainty stated correctly
- did the output remain faithful to the input

This layer may be manual first.
Later it may use a judge model, but only as a review aid, not as the source of truth.

## The first MVP test

The first test should be thought ingestion.

Reason:

- it is universal
- it is closer to Maxim's real daily workflow than book or video ingest
- it exposes the most important routing boundary: raw scratch capture versus curated thought page
- if we cannot preserve the meaning of a simple thought, more complex source automation is not trustworthy

### MVP fixture: `thought-simple`

Input example:

- one short original thought from Maxim
- no external URL
- no attached evidence

The test must verify:

- the input is not treated as an external source
- raw capture behavior follows the chosen workflow contract exactly
- if a curated thought page is created, it uses correct type and naming
- no fake sources are invented
- any extracted concept links are clearly attributed as interpretation, not raw evidence
- `log.md` reflects the action if the workflow says it should
- no unrelated pages change

## Negative tests

The automation must also prove that it refuses the wrong thing.

Required negative cases:

- missing metadata must not be hallucinated
- ambiguous input must not be over-promoted into curated truth
- a relation request must not trigger full ingest of unrelated pages
- broken evidence must block strong claims rather than degrade silently
- duplicate page names must trigger reuse or explicit conflict handling

A good automation should fail conservatively.

## Regression tests

Every bug found in production must become a fixture.

Examples relevant to this vault:

- wrong relative link between `sources/` and `raw/`
- accidental creation of duplicate asset trees
- missing `## Relations`
- index updated but connection map forgotten
- connection map updated but log forgotten
- raw note rewritten after initial capture
- source date guessed instead of marked unverified

The rule is simple:

bug once -> fixture forever

## Pass/fail gates

A run passes only if:

- zero critical structural violations
- zero prohibited outcomes
- expected file diff matches manifest
- expected links resolve
- surface files changed exactly when required
- semantic review for MVP fixtures is accepted

A run fails if:

- it creates ontological drift while keeping markdown valid
- it invents evidence
- it mutates raw evidence incorrectly
- it bypasses uncertainty handling
- it introduces hidden side effects outside the manifest

## Suggested repository layout for tests

Recommended system-layer location:

- `tests/knowledgevault-automation/fixtures/`
- `tests/knowledgevault-automation/manifests/`
- `tests/knowledgevault-automation/expected/`
- `tests/knowledgevault-automation/run_fixture.py`
- `tests/knowledgevault-automation/check_results.py`

These artifacts belong in the PKM system repo, not inside the live vault.

## Suggested execution modes

### Mode 1: Fixture-on-temp-vault

- copy a minimal vault snapshot into a temp directory
- run the automation against the temp vault
- compare resulting diff against manifest
- run structural checker

This should be the default test mode.

### Mode 2: Regression-on-real-vault-clone

- clone or copy the real vault into an isolated temp directory
- replay a known workflow
- verify no unintended surface drift

Use this before major refactors.

### Mode 3: Golden-diff review

- produce a human-readable diff for a few curated fixtures
- inspect semantic adequacy manually

Use this for thought and quote workflows first.

## Mapping to system requirements

This test strategy directly protects:

- FR-01 raw input remains raw first
- FR-07 thought ingestion as first-class workflow
- FR-08 source ingestion with raw plus curated layers
- FR-10 lint and schema consistency
- NFR-04 raw evidence separated from curated interpretation
- NFR-06 deterministic startup around canonical files
- DR-02 frontmatter consistency
- DR-03 traceability of claims
- DR-05 raw captures remain immutable

## Decision for implementation phase

The implementation should start only after these artifacts exist:

1. one MVP fixture for `thought-simple`
2. one manifest/oracle format
3. one deterministic checker command that returns pass/fail plus JSON
4. one regression policy: every future workflow bug becomes a fixture

That is the minimum proof scaffold.

## Recommended next step

Implement the test harness before implementing the general automation engine.

Order:

1. build the fixture format
2. build the result manifest checker
3. build the MVP thought-ingestion fixture
4. run the harness against a fake/no-op implementation first
5. only then build the actual automation
