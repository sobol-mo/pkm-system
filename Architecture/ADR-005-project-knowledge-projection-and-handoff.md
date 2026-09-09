# ADR-005: Project Knowledge Projection and Handoff

Last updated: 2026-09-09
Status: Accepted
Date: 2026-09-09
Decision owner: Maxim Sobol

## Context

Digital Mind must represent which projects exist, why they exist, and how they relate to reusable concepts, goals, constraints, processes, patterns, and artifacts. Project repositories and the MAS project catalog already own project identity, lifecycle, paths, requirements, backlog, and operational state. Copying those mutable facts into the vault would create a competing project tracker.

Project work can also produce reusable knowledge. The project performing the work can identify that yield, but it must not bypass PKM authority and write directly into the canonical vault. The PKM system owns ontology meaning, reconciliation, validation, and canonical knowledge writes.

The existing AI Systems Design course already demonstrates the intended producer/curator split, but its course-specific request and the MAS ingest SOP do not yet share one generic handoff contract.

## Decision

### Project is a first-class entity

`Project` is a canonical entity type stored under `projects/`.

A project page is a semantic projection. It records why a project exists and its durable relations to knowledge objects. It is not authoritative for mutable project-management or runtime state.

`Implementation` remains the type for a concrete tool, system, product, or reference implementation. A project may produce or operate implementations, but the endeavor and its realized systems are not the same entity.

### Minimal project-page contract

Project pages use the standard curated-page fields plus:

- `project_id`: stable project identity
- `authority_refs`: stable references to the authoritative project catalog, repository, or project package

The page body contains a short purpose, a durable semantic boundary, and typed relations. It must not copy current status, milestone, backlog, next actions, branch, checkout paths, runtime state, or mutable team assignments.

The initial project-specific relation set is:

- `pursues_goal`
- `constrained_by`
- `uses_process`
- `produces_artifact`

Existing relations such as `uses_pattern`, `enables`, `solves`, and `related_concept` remain available and should be preferred where their established meaning fits.

### Knowledge-yield responsibility

Projects connected to Digital Mind perform a knowledge-yield check as a project-local extension of `session-close-bundle` when a logical work block closes. The project decides whether the completed work produced stable, reusable, source-backed concepts, relations, decisions, patterns, or other knowledge.

No PKM task is created when there is no reusable yield. When reusable knowledge exists, the producing project prepares an immutable handoff package but does not write to the vault.

The PKM project owns the reusable knowledge-yield procedure, the generic package contract, reconciliation, ingest rules, and validation. Each participating project keeps only a short completion-workflow reference to that project-owned procedure. MAS may transport and route a package but does not own its semantic meaning.

### Read-only ontology consultation

The persistent `swc-hermes-pkm-curator` may accept a separate `pkm-ontology-consultation` task class.

This task is read-only. It may report existing entities, likely reuse, conflicts, supported mappings, unsupported relations, and questions requiring Maxim's decision. It may not modify the vault, requirements, schema, architecture, or project artifacts, and it may not approve new ontology types or relation meanings.

Ontology decisions remain with Maxim in the Digital Mind project design context. Consultation does not satisfy the separate approval required for a canonical write.

### Generic handoff envelope

The generic contract is `pkm-knowledge-handoff.v1`. It is an immutable envelope containing:

- handoff identity and producer project identity
- completed work-block reference
- knowledge-yield categories and reuse rationale
- payload profile
- immutable payload references with repository identity, commit, path, and digest
- explicit included identifiers or another bounded selection
- requested mode: consultation, proposal, or canonical ingest
- required result shape
- unresolved questions

The envelope points to authoritative producer artifacts and does not duplicate their semantic content. Its exact-file digest is stored in the external task and handoff records rather than inside the file being hashed. Approval for a canonical write binds Maxim's decision to that exact digest.

The AI Systems Design specialization is `course-concepts.v1`. It adds module identity, the approved concept artifact, terminology registry, included concept identifiers, and the requirement to preserve instructor-approved meaning.

The generic result reports reused, created, updated, rejected, and deferred entities; added, rejected, and deferred relations; conflicts; validation outcomes; exact read-back paths; and the originating envelope identity and digest.

### Pilot order

The AI Systems Design course is the first pilot because it already has approved producer artifacts and a proven curator boundary. The next approved course concept package will exercise the generic envelope and the `course-concepts.v1` profile.

The Multi-Agent System is the second pilot. It will test whether the envelope generalizes beyond course concepts after the relevant role, process, artifact, goal, constraint, and evaluation decisions in `PKM-010` are sufficiently resolved.

## Rejected Alternatives

- Keep projects tagged as `Implementation`: rejected because it conflates an endeavor with a concrete system or tool and weakens agent retrieval.
- Copy project status and backlog into the vault: rejected because repositories and project registries already own mutable state.
- Make the knowledge-yield gate globally mandatory in MAS: rejected because projects may operate outside MAS and PKM owns knowledge semantics.
- Let the curator scan projects autonomously: rejected because the producing project owns completion context and selection of candidate knowledge.
- Duplicate a full rule in every global `SOUL.md`: rejected because copies would drift.
- Give the curator ontology decision authority: rejected because read access and ingest capability do not imply product or schema authority.
- Use one flat handoff schema with every domain field: rejected because project-specific payload meaning belongs to the producing project.

## Consequences

- The schema and operational validator must support `type: project` and `projects/`.
- Existing project-like implementation pages are not migrated automatically. Migration requires explicit reconciliation so implementation and project identities are not collapsed incorrectly.
- A reusable PKM-owned knowledge-yield procedure and machine-readable envelope/profile contracts must be implemented before the first pilot.
- MAS routing changes are limited to transport and the bounded read-only consultation task; they do not move schema authority into MAS.
- The course pilot must preserve its current instructor approval and exact-digest canonical-write gate.
- The MAS second pilot remains downstream of the relevant `PKM-010` ontology decisions.
