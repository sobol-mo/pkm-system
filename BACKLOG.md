# PKM Project Backlog

This file tracks actionable work only.

Canonical project meaning lives in `Requirements/`.
Accepted architecture decisions live in `Architecture/`.
Raw ideas live in `PKM-idea.md` and `raw/`.

Statuses: `Backlog` | `In Progress` | `Review (Maxim)` | `Done`

## In Progress

No active implementation task recorded.

## Review (Maxim)

No items awaiting review.

## Backlog

### PKM-003 — Define initial ontology

Status: Backlog
Type: Design
Owner: Maxim + Calen

Goal: define the first useful set of node/entity types, relation types, review states, and bilingual naming conventions.

Canonical context:

- `Requirements/04-domain-model.md`
- `wiki/schema.md`

Acceptance criteria:

- minimal relation set is defined for the first working version
- worldview relations are separated from structural and attribution relations
- review/endorsement states are defined or explicitly deferred
- language policy is decided or documented as an open decision

### PKM-004 — Agent workflow for PKM operations

Status: Backlog
Type: Implementation Design
Owner: Calen

Goal: define Orchestrator/Executor/Critic or equivalent workflow for ingest, query, lint, and review.

Canonical context:

- `Requirements/03-system-requirements.md`
- `Requirements/04-domain-model.md`
- `wiki/schema.md`

Acceptance criteria:

- workflow separates raw capture, AI extraction, Maxim review, and curated update
- decision points requiring Maxim approval are explicit
- unresolved work is externalized into durable artifacts

### PKM-005 — LightRAG deployment on VPS

Status: Backlog
Type: Implementation
Owner: Calen

Goal: deploy LightRAG as a derived runtime/index, not as canonical storage.

Canonical context:

- `Architecture/ADR-001-folder-organization-and-system-state-separation.md`
- `Requirements/03-system-requirements.md`

Acceptance criteria:

- LightRAG reads from canonical markdown/vault files
- runtime data is rebuildable
- connectivity from OpenClaw is tested

### PKM-006 — Prototype first file extraction

Status: Backlog
Type: Implementation
Owner: Calen

Goal: take one raw file and validate extraction quality into concepts, relations, and source summary.

Depends on: PKM-003, PKM-005

Acceptance criteria:

- raw input remains preserved
- extracted entities are reviewable
- curated output follows `wiki/schema.md`
- relation quality is manually assessed

### PKM-007 — Telegram interface for ontology ingestion

Status: Backlog
Type: Implementation
Owner: Calen

Goal: support natural-language command such as "process file X" or forwarded content ingestion through Telegram/OpenClaw.

Depends on: PKM-004, PKM-006

Acceptance criteria:

- Telegram capture creates raw evidence first
- agent proposes curated changes instead of silently rewriting truth
- Maxim approval path is explicit for worldview claims

### PKM-008 — Vault migration planning

Status: Review (Maxim)
Type: Architecture / Migration
Owner: Maxim + Calen

Goal: plan migration from current `PKM/raw` + `PKM/wiki` layout to the ADR-001 target split: system repo, canonical vault, derived runtime.

Canonical context:

- `Architecture/ADR-001-folder-organization-and-system-state-separation.md`
- `Architecture/ADR-003-cross-environment-vault-deployment-and-sync.md`
- `Architecture/KnowledgeVault-migration-plan.md`

Acceptance criteria:

- migration steps are documented
- source and target paths are explicit
- rollback strategy is defined
- no canonical content is lost

### PKM-009 — Migrate PKM skills into project system layer

Status: Backlog
Type: Migration / Implementation
Owner: Maxim + Calen

Goal: move the current VPS-hosted PKM skills into the project-owned `skills/` directory so both VPS and localhost agents use the same workflow source.

Canonical context:

- `Architecture/ADR-002-project-owned-agent-skills.md`
- `Requirements/03-system-requirements.md`
- `skills/README.md`

Acceptance criteria:

- current VPS skill directories are identified
- PKM-specific skills are copied into `skills/` for review
- environment-specific assumptions are documented or removed
- localhost agent can inspect and use project-owned skills
- VPS runtime can consume the same skills through direct loading, symlink, deployment, or sync

### PKM-010 — Define agent-context ontology

Status: Backlog
Type: Design
Owner: Maxim + Calen

Goal: define how Digital Mind represents agent roles, onboarding context, goals, constraints, processes, artifacts, and evaluation criteria.

Canonical context:

- `Requirements/01-vision-and-scope.md`
- `Requirements/03-system-requirements.md`
- `Requirements/04-domain-model.md`
- `wiki/thoughts/2026-05-17-pkm-as-unified-knowledge-field.md`

Acceptance criteria:

- decide whether agent-management objects remain tagged concepts or become separate entity types
- define minimal relation types for agent onboarding and evaluation
- define how an agent receives role-specific context from the vault
- document how goal-oriented agent work differs from prompt-only task execution

## Done

Done items contain historical summaries and traceability notes. They are not canonical product definition; canonicalized outcomes are listed under each item.

### PKM-001 — Define project name and scope

Completed: 2026-03-18

Outcome:

- user-facing name: Digital Mind
- technical name: Personal Ontology
- scope strategy: Scope B by design, Scope A first
- technology-agnostic direction accepted
- quotes recognized as first-class personality nodes

Canonicalized into:

- `Requirements/01-vision-and-scope.md`
- `Requirements/02-business-requirements.md`
- `Requirements/04-domain-model.md`

Historical source:

- `raw/PKM-001-naming-scope.md`

### PKM-002 — Storage technology research

Completed: 2026-04-04

Outcome:

- LightRAG selected as a runtime/index candidate
- local/free CPU embeddings preferred
- MiniMax API was current LLM provider at the time of decision
- later refined by ADR-001: markdown files are canonical, databases are compiled artifacts

Canonicalized into:

- `Architecture/ADR-001-folder-organization-and-system-state-separation.md`
- `Requirements/03-system-requirements.md`
- `Requirements/04-domain-model.md`

Historical source:

- `raw/LightRAG-architecture.md`

## Notes

- Telegram topic for this project: 2882.
- All review items should be surfaced to Maxim in topic 2882.
- `PKM-idea.md` is a raw idea dump, not canonical project definition.
