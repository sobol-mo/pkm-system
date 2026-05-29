# PKM Architecture Decisions

This directory contains accepted architecture decisions.

Project definition and requirements are canonical in `../Requirements/`.
Architecture decisions should explain how requirements are implemented or constrained; they should not become a replacement for product definition.

## ADR Index

| ADR | Status | Date | Decision |
|-----|--------|------|----------|
| [ADR-001: Folder Organization and System/State Separation](ADR-001-folder-organization-and-system-state-separation.md) | Accepted | 2026-05-27 | Type-based folders; system/vault/runtime separation; markdown canonical, databases compiled |
| [ADR-002: Project-Owned Agent Skills](ADR-002-project-owned-agent-skills.md) | Accepted | 2026-05-28 | PKM-specific skills belong to the project system layer and are deployed/synced to agent runtimes |
| [ADR-003: Cross-Environment Vault Deployment and Sync](ADR-003-cross-environment-vault-deployment-and-sync.md) | Accepted | 2026-05-28 | Separate system deploy from vault sync; make prod vault path/sync/monitoring Layer 1 concerns; rebuild runtime from Prod vault |
