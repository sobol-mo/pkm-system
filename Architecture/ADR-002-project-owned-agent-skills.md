# ADR-002: Project-Owned Agent Skills

**Date:** 2026-05-28
**Status:** Accepted

## Context

Digital Mind wiki maintenance is performed by AI agents through repeatable skills: ingest, query, lint, multimodal ingest, and related workflows.

Initially, these skills lived in the VPS production agent environment because the main operational use case was a VPS-based agent interacting with Maxim through Telegram.

The project now has an additional requirement: localhost agents working with the local project clone must be able to use, inspect, and modify the same skills. Otherwise, important project behavior lives outside the project itself and becomes environment-specific hidden state.

This creates a new system/state boundary question:

- Are PKM skills part of the VPS agent runtime?
- Or are PKM skills part of the Digital Mind project system layer and deployed into runtimes as needed?

## Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **A: Keep skills only on VPS** | Simple for current Telegram production agent | Localhost agents cannot reproduce behavior; skills become hidden runtime state; difficult to review and version with project |
| **B: Keep skills in a separate global skills repo** | Reusable across multiple projects | Weak project cohesion; changes may affect unrelated projects; still not visible from the PKM project tree |
| **C: Store PKM-specific skills with the Digital Mind system layer** | Skills are versioned, reviewable, local-first, and project-specific; both VPS and localhost can share the same source | Requires deployment/sync mechanism into runtime-specific skill paths |

## Decision

PKM-specific skills are project system assets.

They must live with the Digital Mind project system files, not only inside the VPS production agent runtime.

The project-owned skill source location is:

```text
skills/
  pkm/
  pkm-ingest/
  pkm-query/
  pkm-lint/
  multimodal-source-ingest/
```

Runtime environments may load these skills directly if supported, or receive deployed/synced copies into their own skill directories.

The VPS runtime path and localhost runtime path are deployment targets, not the source of truth.

## Relationship To ADR-001

ADR-001 separates the project into:

- system
- canonical vault
- derived runtime

This ADR clarifies that agent skills belong to the **system** layer.

They define how agents operate on the vault and should be versioned like requirements, ADRs, schemas, templates, scripts, and automation.

They are not vault content and not runtime state.

## Consequences

### Positive

- Localhost agents can use the same PKM workflows as VPS agents.
- Skill behavior becomes inspectable and reviewable in the project repository.
- Skill changes can be discussed, diffed, and committed with related architecture or requirement changes.
- Production behavior no longer depends on undocumented files in the VPS agent environment.

### Neutral

- A deployment or sync step is needed so the VPS agent runtime can consume project-owned skills.
- Existing VPS skills need to be copied or migrated into the project tree.

### Negative

- Project repository contains more operational implementation detail.
- If skills are shared incorrectly across projects, project-specific assumptions may leak into global agent behavior.

## Implementation Notes

- Do not copy VPS skills blindly without review; treat the first import as migration of operational source code.
- Keep PKM-specific assumptions inside `skills/` for this project.
- Extract truly generic note-taking skills only if there is a clear reuse need.
- Runtime-specific configuration should point to project-owned skills or deploy them from the project tree.

## Decision Log

| Date | Decision | Context |
|------|----------|---------|
| 2026-05-28 | PKM-specific skills are project-owned system assets | Localhost and VPS agents must use and modify the same wiki-maintenance workflows |
