# ADR-003: Cross-Environment Vault Deployment and Sync

**Date:** 2026-05-28
**Status:** Accepted

## Context

ADR-001 established a three-way split:

- system
- canonical vault
- derived runtime

ADR-002 established that PKM-specific skills belong to the project system layer and must be usable from both localhost and VPS environments.

The next unresolved question is how the canonical vault should exist across environments in practice.

Current reality:

- the PKM system lives in a git-backed project repo
- the canonical vault must sync across at least two environments: localhost development and VPS production
- the VPS already runs an Infrastructure as Code model for host provisioning and monitoring
- the VPS agent runtime (`/home/hermes/.hermes`) is a framework-specific workspace/runtime boundary and is not an appropriate location for the canonical PKM vault

Two operational needs must both be satisfied:

1. The PKM system layer must be delivered from development into production in a controlled, reviewable way
2. The canonical vault must replicate across devices/environments as human-facing synced state, not as framework runtime data and not as a git deployment artifact

## Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **A: Keep system repo and canonical vault in one git deployment flow** | Simple mental model | Conflates code/config delivery with knowledge-state replication; pollutes history; poor fit for sync-first vault state |
| **B: Keep vault only on VPS and treat localhost as a temporary editor** | Simple production story | Breaks cross-device symmetry; localhost becomes second-class; weak offline/dev experience |
| **C: Put the canonical vault inside Hermes runtime paths** (`/home/hermes/.hermes/...`) | Easy for one agent runtime to see | Couples PKM lifecycle to one framework; violates system/vault/runtime separation; harms portability |
| **D: Separate system deploy, vault sync, and derived runtime rebuild** | Clean boundaries; compatible with IaC; portable across tools and runtimes | Requires explicit sync and monitoring design |

## Decision

Option D is accepted.

### 1. Three distinct cross-environment flows

The PKM operating model across environments is:

```text
Dev system repo -> GitHub -> controlled deploy/update to Prod
Dev KnowledgeVault <-> sync transport <-> Prod KnowledgeVault
Prod derived runtime <- rebuild from Prod KnowledgeVault
```

These are different contracts and must not be collapsed into one delivery mechanism.

### 2. System repo delivery uses git-based controlled deployment

The PKM **system layer** includes:

- `AGENTS.md`
- `Requirements/`
- `Architecture/`
- `BACKLOG.md`
- `skills/`
- `scripts/`
- `schema/`
- `templates/`

This layer is delivered from development to production through a controlled git-based path:

- development changes are committed and pushed to GitHub
- production receives updates through an explicit deploy/update workflow
- current Hermes production implementation uses a host-managed `systemd` sync timer that fast-forwards the production repo from GitHub
- production must not depend on manual copying into ad hoc server paths

The production copy of the PKM system is a deployed system artifact, not the canonical knowledge state.

### 3. Canonical vault uses sync transport, not git deployment

The PKM **canonical vault** is a synced human-facing markdown corpus.

It must not be treated as:

- a subdirectory of the system repo
- a git deployment target
- a Hermes runtime subdirectory
- generic server-only user-data

The canonical vault is replicated through a sync-oriented transport suitable for cross-device use.

This ADR fixes the boundary and responsibility model first. The current reference implementation uses Syncthing, but the architectural rule is broader than one product:

- sync is a first-class infrastructure concern
- sync is not the same thing as backup
- sync health must be visible from the host maintenance plane

For Syncthing-based implementations, one operational rule is non-negotiable:

- device-level connectivity and folder-level membership are different things
- seeing a peer as `connected` does not prove that the canonical folder is actually shared with that peer
- verification must check both the peer connection and the `pkm-vault` folder device list

### 4. Canonical path contract: logical name + environment binding

The canonical vault identity is the external folder named `KnowledgeVault`.

Default path convention:

- `Dev`: `/home/maxim/KnowledgeVault`
- `Prod`: `/home/hermes/KnowledgeVault`

Canonical path resolution contract:

1. `PKM_VAULT_PATH`
2. `OBSIDIAN_VAULT_PATH` when an Obsidian-specific workflow is being used
3. fallback default: `$HOME/KnowledgeVault`

Architecture defines the vault identity and default convention.
Environment configuration defines the concrete absolute path.

### 5. Production vault path is Layer 1 infrastructure

On production, the vault path and sync mechanism belong to the Layer 1 infrastructure contract.

Layer 1 on production must own:

- creation of the vault directory path
- ownership and permissions
- environment/config exposure of `PKM_VAULT_PATH`
- sync service/timer installation
- sync healthcheck state output
- host-visible monitoring and alerting for sync freshness/failure
- backup/retention policy for the vault as a separate concern from sync

This path must be provisioned through Infrastructure as Code, not by manual SSH setup.

### 6. Production monitoring rule for vault sync

The canonical vault sync on production is part of the host maintenance plane.

It must follow the same operational philosophy as other production maintenance workflows:

- host-managed service/timer, not agent-chat maintenance
- host-visible state file for workflow health
- watchdog/availability integration
- explicit failure surfacing when sync is stale, failing, or blocked

At minimum, monitoring must be able to surface:

- whether the vault path exists
- whether the last successful sync is recent enough
- whether the sync command exited successfully
- whether lock/conflict/stuck states exist
- whether the configured remote/peer is reachable enough for the expected operating mode

Monitoring alone is not sufficient to prove correct multi-device replication.

For Syncthing, host-visible health can still look green when:

- the Syncthing daemon is running
- at least one peer device is connected
- the local folder is `idle`

but the intended target host is missing from the `pkm-vault` folder membership.

Therefore the operator verification contract for new hosts must include:

- device exists in Syncthing peer list
- device is explicitly present in the `pkm-vault` folder device membership
- folder completion is 100 percent after initial convergence
- spot-check of real files on disk confirms that current content reached the host

### 7. Derived runtime remains rebuildable and downstream

Production runtime artifacts such as vector indexes, graph stores, caches, and exports remain derived state.

They are rebuilt from `Prod KnowledgeVault`, not synchronized independently as primary state.

The production derived runtime must stay separate from both:

- the system repo
- the canonical vault

Suggested default path class:

- `Prod`: `/home/hermes/.knowledge-runtime`

The exact runtime implementation may evolve, but the dependency direction is fixed:

```text
KnowledgeVault -> rebuild -> runtime
```

## Rationale

- The system repo and the vault have different lifecycles and different failure modes
- Git is appropriate for reviewed system artifacts, but not as the canonical replication mechanism for live PKM state
- The vault must remain portable across agent frameworks, note tools, and runtime technologies
- The Hermes runtime home (`/home/hermes/.hermes`) is already a framework-specific workspace/runtime boundary and should not become the canonical home of Digital Mind itself
- Production path creation, sync scheduling, and health visibility are infrastructure responsibilities and should be expressed through IaC rather than remembered shell actions
- Rebuildable runtime artifacts preserve the rule that files are canonical and databases/indexes are compiled

## Consequences

### Positive

- Clean separation between system deployment and knowledge-state replication
- Production path creation and sync behavior become reviewable infrastructure
- Localhost and VPS follow the same logical model with different environment bindings
- PKM remains portable beyond Hermes or any single runtime
- Monitoring and availability discipline extends naturally to vault sync

### Neutral

- A separate sync mechanism must be selected and implemented later
- Production now has one more Layer 1 managed workflow to monitor

### Negative

- More moving parts than a naive "just git push everything" model
- Sync conflicts and stale-peer cases must be explicitly handled by the future sync implementation
- System deploy and vault sync now require separate operational documentation and validation

## Implementation Notes

- Update ADR-001 language so `~/KnowledgeVault` is treated as a default convention, not as a hard-coded universal path truth
- Add production infrastructure variables for vault path, sync workflow, and sync-health state paths in the Hermes infrastructure project
- Keep the production PKM vault outside `/home/hermes/.hermes`
- Treat sync and backup as separate workflows with separate health semantics
- Document the scaling/bootstrap procedure for every additional Syncthing host

### Current Syncthing implementation note

The current operational model is:

```text
Prod <-> SWC
Prod <-> MWC3
Prod <-> future MWC2
optional laptop-to-laptop links when convenient
```

Scaling rule:

- adding a new host is not complete when the device is merely registered
- the new device must also be added to the `pkm-vault` folder membership on the relevant existing peers
- the new device must reciprocally share `pkm-vault` back to those peers

Failure mode observed in practice:

- WebUI and API can show an active Syncthing connection while `KnowledgeVault` files stay stale on disk
- root cause: the host was connected as a device, but was not included in the `pkm-vault` folder membership on the peer

Operational takeaway:

- for multi-host scaling, treat `connected peer` and `folder participant` as separate checks

## Decision Log

| Date | Decision | Context |
|------|----------|---------|
| 2026-05-28 | System repo delivery and canonical vault replication are separate flows | Needed clean boundary between git-managed project assets and sync-managed knowledge state |
| 2026-05-28 | Canonical vault identity is `KnowledgeVault`; path is environment-bound | Needed one logical vault model for Dev and Prod without hard-coding one absolute path |
| 2026-05-28 | Production vault path/sync/monitoring are Layer 1 concerns | Production setup must be reproducible through IaC and visible through host monitoring |
| 2026-05-28 | Derived runtime rebuilds from `Prod KnowledgeVault` | Preserves files-as-canonical, runtime-as-compiled rule |

## References

- `Architecture/ADR-001-folder-organization-and-system-state-separation.md`
- `Architecture/ADR-002-project-owned-agent-skills.md`
- `Requirements/03-system-requirements.md`
- `Requirements/04-domain-model.md`
- `skills/pkm-system-boundaries/references/pkm-vault-vs-userdata-vs-derived-state.md`
- `/home/maxim/dev/projects/My_AI_Assistant/10_Implementation/openclaw/hermes-infra-project/INFRASTRUCTURE-RUNBOOK.md`
