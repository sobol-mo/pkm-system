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

### Canonical Peer Registry

This skill is the canonical operator registry for the PKM Syncthing cluster. When a new host is paired successfully, update this section immediately with its device ID and its explicit reachable address.

Current known peers:

| Host | Role | Device ID | Canonical vault path | Address strategy | Current explicit address |
|------|------|-----------|----------------------|------------------|--------------------------|
| `Prod` | Always-on anchor VPS | `SAAYF4I-2EH3ZWM-4C6JDQC-NDORP2I-FE6KNZ2-XTHJJ2C-57ANVE6-ARTDOAY` | `/home/hermes/KnowledgeVault` | explicit TCP | `tcp://46.225.7.241:22000` |
| `MWC2` | operator laptop | `XCSSCQ5-Z6F6WVT-HYTK4CS-OL7363W-VYE4JU4-ZOC5B6N-27TOYQ6-TUKMIQG` | `/home/maxim/KnowledgeVault` | explicit TCP | `tcp://193.106.63.15:22000` |
| `maxim-dev` | existing operator host | `UQHQC53-SG5UDHE-PLJNCI4-ZWRITPA-TTLPMVW-7IYCOFV-4MKKSU7-5JVJCAY` | operator-managed | explicit TCP on Prod | `tcp://193.106.63.15:22000` |
| `MWC3` | existing operator host | `7WCXEC3-HMLB7OC-HG6JK3C-CODNTZV-GPBRQ6E-GV22S4W-G3R7DFN-SICLIQ5` | operator-managed | explicit TCP on Prod | `tcp://193.106.63.15:22000` |

Registry rules:
- do not leave a newly paired host documented only as `<NEW_DEVICE_ID>` in shell history or chat
- after successful pairing, add the host name, device ID, canonical vault path, and explicit address here
- if a host changes public address strategy, update this registry before treating the rollout as complete
- treat this table as the first place to look up peer IDs during future pairing work

### Canonical Addressing Strategy

The current real deployment uses explicit peer TCP addresses for the Prod anchor model.

Canonical rule for this cluster:
- keep `Prod` as the always-on anchor
- pair every new operator host with `Prod`
- add device membership on both sides for `pkm-vault`
- set explicit `tcp://<reachable-ip>:22000` addresses on both sides when the host has a stable reachable address
- do not rely on `dynamic` alone unless global discovery and relays are intentionally part of the declared topology

Observed operational lesson:
- adding a host with device membership but leaving it as `dynamic` only can produce a formally paired configuration that never syncs on the real network topology
- in this deployment family, the safe default is explicit addresses first

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

**Then set explicit addresses on both sides** when the deployment follows the current canonical Prod-anchor topology:

```bash
# On Prod, point the new host device at its reachable TCP address
syncthing cli config devices <NEW_DEVICE_ID> addresses set tcp://<NEW_HOST_REACHABLE_IP>:22000

# On the new host, point Prod at the VPS TCP address
syncthing cli config devices <PROD_DEVICE_ID> addresses set tcp://46.225.7.241:22000
```

If `syncthing cli ... addresses set` is unavailable in the installed Syncthing build, edit the device `addresses` array through the REST `/rest/config` endpoint or the WebUI, then restart Syncthing.

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
- `/rest/config/devices` shows the intended explicit `tcp://...:22000` addresses for topologies that use explicit addressing
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
3. Look up existing peer IDs in the canonical peer registry in this skill
4. Add the new device to each relevant existing peer's device registry
5. Add the new device to the `pkm-vault` folder membership on each relevant existing peer
6. Add each existing peer to the new host's device registry
7. Add each existing peer to the new host's `pkm-vault` folder membership
8. Set explicit TCP addresses on both sides when the host has a stable reachable address
9. Verify completion and real files on disk
10. Update the canonical peer registry in this skill with the new host's ID and address

The critical pitfalls are step 5, step 7, or step 8 being skipped.

Observed failure mode:

- Syncthing connection is visible in WebUI
- healthcheck looks healthy or mostly healthy
- `KnowledgeVault` files on disk remain stale

Root cause:

- device registration existed, but folder membership for `pkm-vault` was incomplete

Second observed failure mode:

- device registration and folder membership existed
- the new host was left on `dynamic` only
- the real deployment topology required explicit addresses

Second root cause:

- the operator used generic Syncthing pairing steps, but the actual cluster relied on explicit `tcp://...:22000` addresses for reachability

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

For the current live family, the practical address pattern is:

```text
Prod -> explicit device addresses for operator hosts
MWC2 -> Prod at tcp://46.225.7.241:22000
MWC3 -> explicit address on Prod
maxim-dev -> explicit address on Prod
```

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
