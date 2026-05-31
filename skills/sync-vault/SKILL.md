---
name: sync-vault
description: Set up Knowledge Vault synchronization on any host using Syncthing. Deploy peer-to-peer sync for the canonical PKM vault across laptops, desktops, and servers.
version: 1.0.0
author: Kilo Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [pkm, sync, syncthing, vault, deployment, cross-device]
    related_skills: [pkm, pkm-system-boundaries, obsidian]
---

# Sync Vault

## Purpose

Deploy Knowledge Vault synchronization on any host where the PKM system repository is cloned. This skill installs and configures Syncthing for peer-to-peer vault replication across all your devices.

## When to Use

Use this skill when:
- Setting up a new laptop or desktop as a PKM working environment
- The Knowledge Vault needs to sync bidirectionally with other devices (laptops, VPS)
- A fresh host needs to join the existing Syncthing cluster
- Verifying sync health after deployment

Do not use this skill when:
- The task is about the system repo (that uses git, not Syncthing)
- The vault path conflict is about Obsidian configuration only

## Architecture

The skill follows ADR-003's cross-environment model:

```text
Dev KnowledgeVault <--Syncthing--> Prod KnowledgeVault
Dev KnowledgeVault <--Syncthing--> Other Dev KnowledgeVault
```

Each device is a Syncthing peer. Peers discover each other and sync the `pkm-vault` folder bidirectionally over encrypted connections. No central server required.

Important distinction:

- a Syncthing device can be connected at the transport level without actually participating in the `pkm-vault` folder
- `KnowledgeVault` content moves only when the peer is both registered as a device and included in the `pkm-vault` folder device membership
- a green WebUI connection or healthy timer alone does not prove the right folder is shared to the right host

### Canonical Path Resolution

1. `PKM_VAULT_PATH` environment variable
2. `OBSIDIAN_VAULT_PATH` (for Obsidian-specific workflows)
3. Fallback: `$HOME/KnowledgeVault`

The vault directory is created automatically if it does not exist.

### What Gets Synced

| Included | Excluded |
|----------|----------|
| All markdown files in the vault | `.syncthing` metadata folders |
| Attachments and images | `.obsidian/workspace.json` (Obsidian session state) |
| Folder structure | OS-specific temp files |

The `.stignore` file in the vault root controls exclusions and is itself synced across peers.

## Deployment

### Quick Setup

Run the localhost setup script:

```bash
skills/sync-vault/scripts/setup_vault_sync_localhost.sh
```

The script:
1. Installs Syncthing via the system package manager
2. Resolves the canonical vault path
3. Enables and starts the Syncthing user service
4. Configures the `pkm-vault` folder in Syncthing via REST API
5. Creates a `.stignore` file if missing
6. Installs the vault-sync healthcheck runner
7. Creates a systemd user timer for periodic sync monitoring
8. Outputs device pairing instructions

### Device Pairing

After deployment on a new device, you must pair it with existing peers. This is a one-time manual step because Syncthing device IDs are generated at runtime and must be exchanged out-of-band.

**On the new device:**

```bash
# Get this device's ID
curl -s -H "X-API-Key: $(grep -oP '(?<=<apikey>).*?(?=</apikey>)' ~/.config/syncthing/config.xml)" \
  http://127.0.0.1:8384/rest/system/status | python3 -c "import sys,json; print(json.load(sys.stdin)['myID'])"
```

**On each existing peer** (Prod VPS, other laptops):

```bash
# Add the new device
syncthing cli config devices add --device-id <NEW_DEVICE_ID> --name <HOSTNAME>-vault
syncthing cli config folders pkm-vault devices add --device-id <NEW_DEVICE_ID>

# On the new device, add each existing peer:
syncthing cli config devices add --device-id <EXISTING_PEER_ID> --name <HOSTNAME>-vault
syncthing cli config folders pkm-vault devices add --device-id <EXISTING_PEER_ID>
```

**Verify pairing:**

```bash
# Check connections from both sides
curl -s -H "X-API-Key: <key>" http://127.0.0.1:8384/rest/system/connections | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Connected peers: {len(d.get(\"connections\",{}))}')"

# Check folder state
curl -s -H "X-API-Key: <key>" 'http://127.0.0.1:8384/rest/db/status?folder=pkm-vault' | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'State: {d.get(\"state\")}, Errors: {d.get(\"errors\")}')"
```

What must be true after pairing:
- `/rest/system/connections` shows the peer devices
- `/rest/config/folders` for `pkm-vault` includes the intended device IDs
- `/rest/db/status?folder=pkm-vault` shows `state` != `error`, `errors` == 0
- Completion converges to 100% on both sides

Recommended extra verification for real hosts:

```bash
# Verify the folder membership, not just the live connection
curl -s -H "X-API-Key: <key>" http://127.0.0.1:8384/rest/config/folders \
  | jq '.[] | select(.id=="pkm-vault") | {id, path, devices}'

# Spot-check a real file on disk
stat "$HOME/KnowledgeVault/index.md" "$HOME/KnowledgeVault/log.md"
```

If file timestamps or sizes differ between peers after Syncthing reports `completion=100%`, suspect wrong folder membership before suspecting filesystem issues.

### Scaling To Additional Hosts

Canonical pattern for multiple operator machines:

- `Prod` stays the always-on anchor
- each new host such as `SWC`, `MWC3`, or future `MWC2` must be paired with `Prod`
- optional host-to-host links are allowed, but `Prod` remains the minimum common peer

For every newly added host, complete all of these steps:

1. Install and bootstrap Syncthing on the new host with `setup_vault_sync_localhost.sh`
2. Obtain the new device ID
3. Add the new device to each relevant existing peer's device registry
4. Add the new device to the `pkm-vault` folder membership on each relevant existing peer
5. Add each existing peer to the new host's device registry
6. Add each existing peer to the new host's `pkm-vault` folder membership
7. Verify completion and real files on disk

The critical pitfall is step 4 or step 6 being skipped.

Observed failure mode:

- Syncthing connection is visible in WebUI
- healthcheck looks healthy or mostly healthy
- `KnowledgeVault` files on disk remain stale

Root cause:

- device registration existed, but folder membership for `pkm-vault` was incomplete

### Syncthing WebUI

WebUI is available at `http://127.0.0.1:8384` on each device.

Use the WebUI for:
- One-time device pairing and folder sharing
- Visual confirmation of sync state
- Inspecting out-of-sync items or errors

Use the WebUI carefully for multi-host scale-out:

- check that each intended host appears inside the `pkm-vault` folder share list
- do not assume that a device shown under `Remote Devices` is already a participant in `pkm-vault`

Do not change casually in the WebUI:
- Folder path or folder ID
- GUI bind address
- Transport defaults

## Steady-State Observability

After deployment, the healthcheck runner monitors sync health:

| Artifact | Path |
|----------|------|
| Runner script | `~/.local/bin/vault-sync-runner` |
| Healthcheck script | `~/.local/bin/vault-sync-healthcheck` |
| Systemd service | `vault-sync.service` (user) |
| Systemd timer | `vault-sync.timer` (user, every hour) |
| State file | `~/.local/share/vault-sync/state.json` |
| Log | `~/.local/share/vault-sync/log` |

The runner queries Syncthing REST API and writes state with:
- `last_status`: `success` or `failed`
- `completion`: local folder completion percentage
- `peers_connected`: count of connected peers
- `pairing_required`: true when no peers are configured
- `consecutive_failures`: counter for escalation
- `last_success_at`: timestamp of last successful check

Operational caveat:

- the runner is a health observer, not the sync transport itself
- it confirms Syncthing API state, not semantic correctness of your intended multi-host folder membership
- after adding a new host, always perform one explicit folder-membership check and one real-file spot-check

### Operator Commands

```bash
# Check sync timer status
systemctl --user status vault-sync.timer

# Trigger a manual sync check
systemctl --user start vault-sync.service

# View sync state
cat ~/.local/share/vault-sync/state.json | python3 -m json.tool

# Run healthcheck manually (exits 0=ok, 1=fail)
~/.local/bin/vault-sync-healthcheck

# View recent sync logs
journalctl --user -u vault-sync.service -n 20 --no-pager

# Stop sync monitoring
systemctl --user stop vault-sync.timer
```

## Shared Peer Topology

The recommended topology for multiple devices:

```text
Laptop-1  <-->  Laptop-2
   |               |
   +---- VPS ------+
```

All devices share the same `pkm-vault` folder ID. Syncthing handles conflict resolution automatically (renames conflicting files with a timestamp suffix).

For N devices, each device should connect to at least the VPS (which is always online) and ideally to one other laptop for direct LAN sync when available.

For the current real deployment family, the intended scale path is:

```text
SWC  <---->
            Prod
MWC3 <---->
MWC2 <---->   (future)
```

This means `Prod` must keep `pkm-vault` shared to all intended operator hosts, not just to one currently connected laptop.

## Troubleshooting

### Sync stuck or slow

```bash
# Check folder errors
curl -s -H "X-API-Key: <key>" 'http://127.0.0.1:8384/rest/db/status?folder=pkm-vault' | python3 -m json.tool

# Check peer connectivity
curl -s -H "X-API-Key: <key>" http://127.0.0.1:8384/rest/system/connections | python3 -m json.tool

# Restart Syncthing
systemctl --user restart syncthing
```

### Pairing required after deploy

State file shows `pairing_required: true`. This is expected until you complete the one-time device pairing with at least one peer. Follow the pairing procedure above.

### WebUI says connected, but local files are stale

Check in this order:

1. `rest/system/connections` - is the intended peer connected
2. `rest/config/folders` - is the intended peer included in `pkm-vault.devices`
3. `rest/db/status?folder=pkm-vault` - is the folder healthy and idle
4. `stat` or `ls -la` on real files such as `index.md` and `log.md`

If step 1 is green but step 2 is wrong, Syncthing can look healthy while `KnowledgeVault` content does not update on disk.

### Conflicts

Syncthing renames conflicting files automatically (e.g., `page.md` -> `page.sync-conflict-20260529-120000.md`). Review conflicts manually and remove the unwanted version.

## References

- `Architecture/ADR-003-cross-environment-vault-deployment-and-sync.md` — cross-environment sync model
- `Architecture/ADR-001-folder-organization-and-system-state-separation.md` — system/vault/runtime separation
- `skills/pkm-system-boundaries/references/pkm-vault-vs-userdata-vs-derived-state.md` — vault boundary guide
- `10_Implementation/openclaw/hermes-infra-project/INFRASTRUCTURE-RUNBOOK.md` — Prod Syncthing deployment reference
