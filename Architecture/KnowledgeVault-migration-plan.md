# KnowledgeVault Migration Plan

Status: Draft for execution
Last updated: 2026-05-28

## Purpose

This document defines the canonical migration plan for moving PKM content from the current mixed repo layout into the accepted target model from `ADR-001` and `ADR-003`:

- system repo
- canonical synced vault
- derived runtime

This is a migration plan, not a replacement for those ADRs.

## Scope

In scope:

- move canonical PKM content from `/home/maxim/dev/projects/agents-projects/pkm-system/raw/` and `/home/maxim/dev/projects/agents-projects/pkm-system/wiki/` into `/home/maxim/KnowledgeVault/`
- preserve folder semantics and file identity where possible
- define the cutover sequence for `Dev` first, then `Prod`
- define rollback and verification rules

Out of scope:

- sync transport implementation details on `Prod`
- derived runtime implementation details
- ontology/schema redesign during migration
- content rewriting beyond path and location normalization

## Source And Target

Source content roots in the current repo:

- `/home/maxim/dev/projects/agents-projects/pkm-system/raw/`
- `/home/maxim/dev/projects/agents-projects/pkm-system/wiki/`

Target canonical vault root on `Dev`:

- `/home/maxim/KnowledgeVault/`

Target canonical vault root on `Prod`:

- `/home/hermes/KnowledgeVault/`

Target derived runtime root on `Prod`:

- `/home/hermes/.knowledge-runtime/`

System repo remains at:

- `/home/maxim/dev/projects/agents-projects/pkm-system/`

## Migration Principle

Migration is a **content relocation**, not a content reinterpretation.

Rules:

- preserve markdown files as canonical records
- preserve filenames unless there is a concrete collision or invalid target placement
- preserve raw-vs-curated separation
- move content first, then update tooling and references
- do not mix migration with ontology/entity-type redesign

## Current-To-Target Mapping

### Raw Layer

| Current | Target | Notes |
|---------|--------|-------|
| `/home/maxim/dev/projects/agents-projects/pkm-system/raw/*.md` | `/home/maxim/KnowledgeVault/raw/*.md` | Raw source captures move without semantic rewrite |
| `/home/maxim/dev/projects/agents-projects/pkm-system/raw/assets/**` | `/home/maxim/KnowledgeVault/assets/raw/**` | Raw-media attachments stay separate from curated note assets |

### Curated Wiki Root Files

| Current | Target | Notes |
|---------|--------|-------|
| `/home/maxim/dev/projects/agents-projects/pkm-system/wiki/index.md` | `/home/maxim/KnowledgeVault/index.md` | Root vault entry point |
| `/home/maxim/dev/projects/agents-projects/pkm-system/wiki/overview.md` | `/home/maxim/KnowledgeVault/overview.md` | Project-level vault overview |
| `/home/maxim/dev/projects/agents-projects/pkm-system/wiki/glossary.md` | `/home/maxim/KnowledgeVault/glossary.md` | Root glossary |
| `/home/maxim/dev/projects/agents-projects/pkm-system/wiki/connection-map.md` | `/home/maxim/KnowledgeVault/connection-map.md` | Root relation map |
| `/home/maxim/dev/projects/agents-projects/pkm-system/wiki/log.md` | `/home/maxim/KnowledgeVault/log.md` | Chronological ingest log |

### Curated Wiki Entity Folders

| Current | Target | Notes |
|---------|--------|-------|
| `/home/maxim/dev/projects/agents-projects/pkm-system/wiki/concepts/**` | `/home/maxim/KnowledgeVault/concepts/**` | Direct move |
| `/home/maxim/dev/projects/agents-projects/pkm-system/wiki/people/**` | `/home/maxim/KnowledgeVault/people/**` | Direct move |
| `/home/maxim/dev/projects/agents-projects/pkm-system/wiki/quotes/**` | `/home/maxim/KnowledgeVault/quotes/**` | Direct move if/when present |
| `/home/maxim/dev/projects/agents-projects/pkm-system/wiki/thoughts/**` | `/home/maxim/KnowledgeVault/thoughts/**` | Direct move |
| `/home/maxim/dev/projects/agents-projects/pkm-system/wiki/sources/**` | `/home/maxim/KnowledgeVault/sources/**` | Direct move |
| `/home/maxim/dev/projects/agents-projects/pkm-system/wiki/analyses/**` | `/home/maxim/KnowledgeVault/analyses/**` | Direct move |
| `/home/maxim/dev/projects/agents-projects/pkm-system/wiki/implementations/**` | `/home/maxim/KnowledgeVault/implementations/**` | Direct move if/when present |
| `/home/maxim/dev/projects/agents-projects/pkm-system/wiki/mocs/**` | `/home/maxim/KnowledgeVault/mocs/**` | Reserved, move if created later |

### Not Moved Into The Vault

These stay in the system repo:

- `/home/maxim/dev/projects/agents-projects/pkm-system/AGENTS.md`
- `/home/maxim/dev/projects/agents-projects/pkm-system/BACKLOG.md`
- `/home/maxim/dev/projects/agents-projects/pkm-system/Architecture/`
- `/home/maxim/dev/projects/agents-projects/pkm-system/Requirements/`
- `/home/maxim/dev/projects/agents-projects/pkm-system/Requirements/05-knowledge-graph-schema.md`
- `/home/maxim/dev/projects/agents-projects/pkm-system/skills/`
- `/home/maxim/dev/projects/agents-projects/pkm-system/PKM-idea.md`

`PKM-idea.md` remains a system-side raw capture scratchpad until there is an explicit later decision to move or replace it.

## Migration Phases

### Phase 0: Preconditions

Before moving content:

- `ADR-001` and `ADR-003` remain the accepted architecture baseline
- `Dev` vault path exists: `/home/maxim/KnowledgeVault/`
- `Prod` Layer 1 vault path exists or is being provisioned separately: `/home/hermes/KnowledgeVault/`
- no concurrent bulk refactor of filenames or ontology structure is in progress

### Phase 1: Create Target Vault Skeleton On Dev

Create the target structure on `Dev`:

```text
/home/maxim/KnowledgeVault/
  inbox/
  raw/
  concepts/
  people/
  quotes/
  thoughts/
  sources/
  analyses/
  implementations/
  daily/
  mocs/
  assets/
```

Also create root files if missing:

- `/home/maxim/KnowledgeVault/index.md`
- `/home/maxim/KnowledgeVault/overview.md`
- `/home/maxim/KnowledgeVault/glossary.md`
- `/home/maxim/KnowledgeVault/connection-map.md`
- `/home/maxim/KnowledgeVault/log.md`

### Phase 2: Copy, Then Verify On Dev

Migration execution order:

1. copy raw files into `/home/maxim/KnowledgeVault/raw/`
2. copy raw assets into `/home/maxim/KnowledgeVault/assets/raw/`
3. copy curated wiki root files into the vault root
4. copy curated entity folders into their target vault folders
5. verify counts, spot-check links, and confirm that no target files are obviously missing

This phase is copy-first, not delete-first.

The repo remains the working fallback until verification completes.

### Phase 3: Update Path Consumers

After content exists in `/home/maxim/KnowledgeVault/`:

- update PKM skills and tooling to resolve the vault through `PKM_VAULT_PATH`
- stop treating `/home/maxim/dev/projects/agents-projects/pkm-system/wiki/` as the live canonical curated location
- stop treating `/home/maxim/dev/projects/agents-projects/pkm-system/raw/` as the live canonical raw location

During transition, repo-local `wiki/` and `raw/` are legacy mirrors/reference state, not the long-term canonical home.

### Phase 4: Freeze Repo-Local Vault Content

Once Dev verification succeeds and path consumers are updated:

- declare repo-local `raw/` and `wiki/` frozen
- do not continue normal ingest into repo-local content roots
- all new canonical vault changes land in `/home/maxim/KnowledgeVault/`

At this point, `PKM` repo becomes system-only for ongoing work.

### Phase 5: Enable Prod Replication

After `Dev` is the canonical source:

- sync `/home/maxim/KnowledgeVault/` to `/home/hermes/KnowledgeVault/` using the chosen sync transport
- verify `Prod` sees the same folder structure and content set
- only then allow runtime rebuild/index workflows to depend on the new `Prod` vault

If Syncthing is the chosen transport, multi-host rollout is not complete when the new device merely appears in the remote device list.

For every host added after the first Prod bootstrap:

- register the new host as a Syncthing device on the relevant peers
- add the new host to the `pkm-vault` folder membership on the relevant peers
- add the relevant peers to the new host's own `pkm-vault` folder membership
- verify real files on disk, not just transport health

Known operational pitfall:

- a host can show as connected in Syncthing WebUI while `KnowledgeVault` remains stale on disk
- root cause is incomplete folder membership for `pkm-vault`, not lack of network connectivity

### Phase 6: Cut Over Rebuild Targets

After `Prod` vault replication is verified:

- rebuild runtime artifacts from `/home/hermes/KnowledgeVault/`
- keep runtime output in `/home/hermes/.knowledge-runtime/`
- do not rebuild from repo-local `wiki/` paths anymore

## Verification Checklist

Minimum migration verification on `Dev`:

- target root exists at `/home/maxim/KnowledgeVault/`
- raw file count in target is not lower than the current repo source count
- curated note count in target is not lower than the current repo source count
- root files exist: `index.md`, `overview.md`, `glossary.md`, `connection-map.md`, `log.md`
- a sample of internal links still resolves under the new root structure
- a sample of raw sources referenced from curated pages still exists in target raw/assets locations

Minimum cutover verification on `Prod`:

- target root exists at `/home/hermes/KnowledgeVault/`
- sync transport reports healthy replication
- `pkm-vault` folder membership includes all intended hosts for this rollout wave
- a sample of expected vault files exists on `Prod`
- derived runtime rebuild reads from `/home/hermes/KnowledgeVault/`, not from repo-local paths

Minimum verification for each additional host after Prod is already live:

- target root exists at the resolved canonical vault path for that host
- Syncthing peer connection exists to `Prod`
- `pkm-vault` folder membership includes both `Prod` and the host itself, plus any additional intended peers
- root files such as `index.md`, `log.md`, and `connection-map.md` match expected timestamps or sizes after convergence
- transport reports `completion=100%` and `needFiles=0`

## Rollback Strategy

Rollback trigger examples:

- major missing-file discrepancy
- broken root navigation files
- path consumers still writing to old repo-local paths after cutover
- sync replication to `Prod` proves unreliable during first cutover window

Rollback actions:

1. stop cutover and treat `/home/maxim/dev/projects/agents-projects/pkm-system/raw/` and `/home/maxim/dev/projects/agents-projects/pkm-system/wiki/` as the active source again
2. revert path-consumer configuration to repo-local paths if already switched
3. do not delete repo-local content until a later verified retry window
4. preserve `/home/maxim/KnowledgeVault/` as a failed migration candidate for inspection, not as the active source

Rollback rule:

- repo-local source content is not removed until the new Dev vault and Prod replication are both verified

## Cutover Completion Criteria

PKM-008 can be considered complete when:

- the canonical Dev vault exists at `/home/maxim/KnowledgeVault/`
- repo-local `raw/` and `wiki/` are no longer treated as the live canonical content roots
- path consumers use `PKM_VAULT_PATH`
- `Prod` receives the vault through the approved sync transport
- runtime rebuild targets the Prod vault path
- rollback is no longer needed for routine operation

## Non-Goals During Migration

- do not rename concepts just to make migration cleaner
- do not redesign frontmatter structure mid-migration
- do not merge raw evidence into curated notes
- do not move system docs into the vault
- do not treat derived runtime state as part of the migration source set

## References

- `/home/maxim/dev/projects/agents-projects/pkm-system/Architecture/ADR-001-folder-organization-and-system-state-separation.md`
- `/home/maxim/dev/projects/agents-projects/pkm-system/Architecture/ADR-003-cross-environment-vault-deployment-and-sync.md`
- `/home/maxim/dev/projects/agents-projects/pkm-system/BACKLOG.md`
