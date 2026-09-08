# Session Handoff — Digital Mind / PKM System

Last updated: 2026-09-08
Status: active

## Active Work

Design the connection between project work and Digital Mind before changing the ontology or agent contracts.

The discussion currently has two coupled questions:

1. whether active projects should become first-class `Project` entities in the knowledge graph, rather than remaining inside the broad `Implementation` type
2. how project workflows should identify reusable knowledge at completion and hand an approved concept package to the persistent PKM specialist

This is a design discussion. No ontology, PKM requirement, MAS contract, agent mission, or KnowledgeVault change has been approved yet.

Related backlog context: `PKM-003` and `PKM-010` in `BACKLOG.md`. The current discussion does not change their status by itself.

## Current Working Direction

- Project repositories and the MAS project catalog remain authoritative for project identity, paths, lifecycle, requirements, active work, and operational state.
- A PKM project page, if adopted, is a semantic projection: why the project exists and which concepts, goals, constraints, processes, patterns, and artifacts it relates to.
- PKM must not become a second project tracker or backlog.
- Project completion should include a knowledge-yield check, not an unconditional ingest task. A PKM handoff is created only when the work produced reusable concepts, relations, decisions, patterns, or source-backed knowledge.
- For course authoring, a completed section or module may produce an instructor-approved concept package containing stable concepts, definitions, relationships, evidence paths, and unresolved proposals. The course agent must not write directly to the canonical vault.
- The PKM specialist reconciles the package against the existing ontology, reuses existing entities, applies only supported relations, validates the vault, and returns created, updated, reused, rejected, and deferred items.

## Last Verified State

- `Requirements/05-knowledge-graph-schema.md` currently treats a project as part of the broad `Implementation` entity type; no separate `Project` type exists.
- `Requirements/01-vision-and-scope.md` and `Requirements/04-domain-model.md` already require the knowledge field to represent projects and provide structured context to agents.
- `BACKLOG.md` item `PKM-010` already covers agent-context ontology, including roles, goals, constraints, processes, artifacts, and evaluation criteria.
- The persistent TEAM agent `swc-hermes-pkm-curator` currently accepts only `pkm-concept-ingest`, `pkm-concept-ingest-fixture`, and `pkm-ingest-result-return`.
- Its current router and `SOUL.md` require a valid MAS STATE task and explicitly block architecture or scope decisions.
- Sending text to Telegram topic `5733` with `hermes send` produced an outbound bot message for Maxim; it did not constitute an agent-addressed handoff. After Maxim explicitly asked the curator to read it, the curator correctly returned `blocked` and made no changes.
- A new Hermes Desktop project named `Digital Mind / PKM` now anchors this conversation to `/home/maxim/dev/projects/agents-projects/pkm-system`.
- The checkout is a standalone Git repository with remote `git@github.com:sobol-mo/pkm-system.git`. The MAS project catalog still identifies it as part of `sobol-mo/agents-projects`; that registry discrepancy should be reconciled separately and does not block this design discussion.

## Open Decisions

1. Promote `Project` to a canonical entity type with a `projects/` folder, or keep projects as a subtype of `Implementation`.
2. Define the minimal project page fields and typed relations without duplicating mutable project state.
3. Decide where the project-to-PKM responsibility belongs. Current recommendation: a reusable PKM knowledge-yield procedure plus an explicit project-router or completion-gate reference; not a large duplicated rule in every global `SOUL.md`.
4. Decide whether `swc-hermes-pkm-curator` should gain a bounded advisory task such as `pkm-architecture-consultation`, or whether ontology design should remain with a separate project-level design authority.
5. Define a generic knowledge-handoff contract and determine how course-specific `pkm-concept-ingest` requests specialize it.
6. Select the first pilot. The strongest candidates are the AI Systems Design course, Multi-Agent System, and Personal Data Management System.

## Exact Next Action

Discuss the six open decisions with Maxim in this project-scoped session and select the smallest coherent design.

After approval, update only the owning artifacts:

- ontology meaning and entity/relation rules in `Requirements/04-domain-model.md` and `Requirements/05-knowledge-graph-schema.md`
- actionable implementation work in `BACKLOG.md`
- reusable PKM maintenance procedure in the project-owned `skills/` tree
- deployed TEAM identity, routing, and task-class changes in the Multi-Agent System project
- course-specific completion rules in the AI Systems Design project only when that project becomes the pilot

Do not implement all layers merely because they are listed here. The approved design must define the minimal first slice.

## Blocking Decision

Maxim must choose the initial authority and scope boundaries before implementation begins. In particular, adding consultation authority to the existing curator must not be inferred from its ability to ingest concepts.

## Repository State

Repository and Git root: `/home/maxim/dev/projects/agents-projects/pkm-system`

Remote: `git@github.com:sobol-mo/pkm-system.git`

Branch at handoff creation: `main`

## Governing Artifacts

- `AGENTS.md`
- `BACKLOG.md`
- `Requirements/01-vision-and-scope.md`
- `Requirements/04-domain-model.md`
- `Requirements/05-knowledge-graph-schema.md`
- `/home/maxim/dev/projects/multi-agent-system/CONTROL/TEAM/swc-hermes-pkm-curator/AGENTS.md`
- `/home/maxim/dev/projects/multi-agent-system/CONTROL/TEAM-KNOWLEDGE/SOP/request-pkm-concept-ingest.md`
