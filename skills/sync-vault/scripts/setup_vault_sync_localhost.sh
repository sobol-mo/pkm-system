#!/usr/bin/env bash
# Deploy Knowledge Vault sync on a localhost machine using Syncthing.
# Idempotent: safe to re-run on an already-configured host.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
STATE_DIR="${HOME}/.local/share/vault-sync"
SYSTEMD_USER_DIR="${HOME}/.config/systemd/user"
SYNCTHING_CONFIG="${HOME}/.config/syncthing/config.xml"
FOLDER_ID="pkm-vault"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

say()  { printf '%b\n' "$*"; }
ok()   { printf "${GREEN}  OK${NC}  %s\n" "$*"; }
warn() { printf "${YELLOW} WARN${NC} %s\n" "$*"; }
fail() { printf "${RED}FAIL${NC} %s\n" "$*" >&2; exit 1; }

# ---------------------------------------------------------------------------
# Step 0 — detect OS
# ---------------------------------------------------------------------------
say "==> Detecting OS..."
OS="$(uname -s)"
case "${OS}" in
  Linux)  say "  Linux detected" ;;
  Darwin) say "  macOS detected" ;;
  *)      fail "Unsupported OS: ${OS}. This script supports Linux and macOS." ;;
esac

# ---------------------------------------------------------------------------
# Step 1 — resolve canonical vault path
# ---------------------------------------------------------------------------
say "==> Resolving vault path..."

if [[ -n "${PKM_VAULT_PATH:-}" ]]; then
  VAULT_PATH="${PKM_VAULT_PATH}"
  ok "Using PKM_VAULT_PATH: ${VAULT_PATH}"
elif [[ -n "${OBSIDIAN_VAULT_PATH:-}" ]]; then
  VAULT_PATH="${OBSIDIAN_VAULT_PATH}"
  ok "Using OBSIDIAN_VAULT_PATH: ${VAULT_PATH}"
else
  VAULT_PATH="${HOME}/KnowledgeVault"
  ok "Using default: ${VAULT_PATH}"
fi

# ---------------------------------------------------------------------------
# Step 2 — install Syncthing
# ---------------------------------------------------------------------------
say "==> Installing Syncthing..."

need_install=false
if command -v syncthing &>/dev/null; then
  syncthing_version="$(syncthing --version 2>/dev/null | head -1 || echo "unknown")"
  ok "Syncthing already installed: ${syncthing_version}"
else
  need_install=true
fi

if ${need_install}; then
  if [[ "${OS}" == "Linux" ]]; then
    if command -v apt-get &>/dev/null; then
      say "  Installing via apt..."
      sudo apt-get update -qq && sudo apt-get install -y -qq syncthing
    elif command -v dnf &>/dev/null; then
      say "  Installing via dnf..."
      sudo dnf install -y syncthing
    elif command -v pacman &>/dev/null; then
      say "  Installing via pacman..."
      sudo pacman -S --noconfirm syncthing
    else
      fail "No supported package manager found. Install Syncthing manually: https://syncthing.net/downloads/"
    fi
  elif [[ "${OS}" == "Darwin" ]]; then
    if command -v brew &>/dev/null; then
      say "  Installing via Homebrew..."
      brew install syncthing
    else
      fail "Homebrew not found. Install it first or install Syncthing manually: https://syncthing.net/downloads/"
    fi
  fi
  ok "Syncthing installed"
fi

# ---------------------------------------------------------------------------
# Step 3 — enable and start Syncthing user service
# ---------------------------------------------------------------------------
say "==> Starting Syncthing service..."

if [[ "${OS}" == "Linux" ]]; then
  systemctl --user enable --now syncthing 2>/dev/null || {
    warn "Could not enable syncthing via systemd. Starting directly..."
    nohup syncthing serve --no-browser >/dev/null 2>&1 &
    sleep 2
  }
elif [[ "${OS}" == "Darwin" ]]; then
  # macOS: use launchd via brew services or manual start
  if brew services list 2>/dev/null | grep -q syncthing; then
    brew services restart syncthing
  else
    brew services start syncthing 2>/dev/null || {
      warn "brew services failed. Starting directly..."
      nohup syncthing serve --no-browser >/dev/null 2>&1 &
      sleep 2
    }
  fi
fi

ok "Syncthing service started"

# ---------------------------------------------------------------------------
# Step 4 — wait for Syncthing to generate config
# ---------------------------------------------------------------------------
say "==> Waiting for Syncthing config..."

max_wait=30
waited=0
while [[ ! -f "${SYNCTHING_CONFIG}" ]]; do
  if [[ ${waited} -ge ${max_wait} ]]; then
    fail "Syncthing config not found after ${max_wait}s. Check: systemctl --user status syncthing"
  fi
  sleep 1
  waited=$((waited + 1))
done
ok "Config ready after ${waited}s"

# ---------------------------------------------------------------------------
# Step 5 — extract API key
# ---------------------------------------------------------------------------
API_KEY="$(grep -oP '(?<=<apikey>).*?(?=</apikey>)' "${SYNCTHING_CONFIG}" 2>/dev/null || true)"
if [[ -z "${API_KEY}" ]]; then
  fail "Could not extract API key from ${SYNCTHING_CONFIG}"
fi
ok "API key extracted"

# ---------------------------------------------------------------------------
# Step 6 — create vault directory
# ---------------------------------------------------------------------------
say "==> Creating vault directory..."
mkdir -p "${VAULT_PATH}"
ok "Vault directory: ${VAULT_PATH}"

# ---------------------------------------------------------------------------
# Step 7 — configure Syncthing folder via REST API
# ---------------------------------------------------------------------------
say "==> Configuring Syncthing folder..."

# Check if folder already exists
existing_folder="$(curl -s -H "X-API-Key: ${API_KEY}" \
  "http://127.0.0.1:8384/rest/config/folders" 2>/dev/null | \
  python3 -c "import sys,json; folders={f['id']:f for f in json.load(sys.stdin)}; print(folders.get('${FOLDER_ID}',{}).get('id',''))" 2>/dev/null || true)"

if [[ "${existing_folder}" == "${FOLDER_ID}" ]]; then
  ok "Folder '${FOLDER_ID}' already configured"
else
  # Create folder via REST API
  folder_config="{\"id\":\"${FOLDER_ID}\",\"label\":\"Knowledge Vault\",\"path\":\"${VAULT_PATH}\",\"type\":\"sendreceive\",\"rescanIntervalS\":3600,\"fsWatcherEnabled\":true,\"fsWatcherDelayS\":10,\"ignorePerms\":false,\"autoNormalize\":true,\"versioning\":{\"type\":\"simple\",\"params\":{\"keep\":\"5\"}}}"

  curl -s -X POST -H "X-API-Key: ${API_KEY}" \
    -H "Content-Type: application/json" \
    -d "${folder_config}" \
    "http://127.0.0.1:8384/rest/config/folders" >/dev/null 2>&1 || {
    warn "Folder creation via API failed. The folder may be pre-configured or Syncthing API not yet ready."
    say "  You can add the folder manually via WebUI: http://127.0.0.1:8384"
    say "  Folder ID: ${FOLDER_ID}"
    say "  Folder path: ${VAULT_PATH}"
  }
  ok "Folder '${FOLDER_ID}' configured at ${VAULT_PATH}"
fi

# ---------------------------------------------------------------------------
# Step 8 — create .stignore if missing
# ---------------------------------------------------------------------------
say "==> Checking .stignore..."
STIGNORE="${VAULT_PATH}/.stignore"
if [[ ! -f "${STIGNORE}" ]]; then
  cat > "${STIGNORE}" <<'STIGNORE_EOF'
# Syncthing ignore patterns for Knowledge Vault
# This file is synced - changes propagate to all peers

# Obsidian workspace state (session-specific)
.obsidian/workspace.json
.obsidian/workspace-mobile.json

# OS files
.DS_Store
Thumbs.db
*.tmp
*~

# Syncthing metadata
.syncthing*
.stfolder
STIGNORE_EOF
  ok "Created default .stignore"
else
  ok ".stignore already exists"
fi

# ---------------------------------------------------------------------------
# Step 9 — install monitoring scripts
# ---------------------------------------------------------------------------
say "==> Installing monitoring scripts..."
mkdir -p "${BIN_DIR}" "${STATE_DIR}"

cp "${SKILL_ROOT}/scripts/vault-sync-runner.py" "${BIN_DIR}/vault-sync-runner"
cp "${SKILL_ROOT}/scripts/vault-sync-healthcheck.sh" "${BIN_DIR}/vault-sync-healthcheck"
chmod +x "${BIN_DIR}/vault-sync-runner" "${BIN_DIR}/vault-sync-healthcheck"
ok "Monitoring scripts installed"

# ---------------------------------------------------------------------------
# Step 10 — install systemd user units (Linux only)
# ---------------------------------------------------------------------------
if [[ "${OS}" == "Linux" ]]; then
  say "==> Installing systemd user units..."
  mkdir -p "${SYSTEMD_USER_DIR}"

  cat > "${SYSTEMD_USER_DIR}/vault-sync.service" <<SVCUNIT
[Unit]
Description=Check Knowledge Vault sync health via Syncthing API
After=network-online.target

[Service]
Type=oneshot
ExecStart=${BIN_DIR}/vault-sync-runner
TimeoutSec=30
SVCUNIT
  ok "Service unit installed"

  cat > "${SYSTEMD_USER_DIR}/vault-sync.timer" <<TMRUNIT
[Unit]
Description=Periodic Knowledge Vault sync health check

[Timer]
OnCalendar=hourly
Persistent=true

[Install]
WantedBy=timers.target
TMRUNIT
  ok "Timer unit installed"

  systemctl --user daemon-reload
  systemctl --user enable --now vault-sync.timer 2>/dev/null || {
    warn "Could not enable vault-sync.timer via systemd. Run manually: systemctl --user enable --now vault-sync.timer"
  }
  ok "Timer enabled and started"
fi

# ---------------------------------------------------------------------------
# Step 11 — run first sync check
# ---------------------------------------------------------------------------
say "==> Running first sync check..."
if "${BIN_DIR}/vault-sync-runner" 2>/dev/null; then
  ok "First sync check completed"
else
  warn "First sync check had issues (expected if no peers paired yet)"
fi

if [[ -f "${STATE_DIR}/state.json" ]]; then
  say "  State:"
  python3 -m json.tool "${STATE_DIR}/state.json" 2>/dev/null || cat "${STATE_DIR}/state.json"
fi

# ---------------------------------------------------------------------------
# Step 12 — get device ID and show pairing instructions
# ---------------------------------------------------------------------------
DEVICE_ID="$(curl -s -H "X-API-Key: ${API_KEY}" \
  "http://127.0.0.1:8384/rest/system/status" 2>/dev/null | \
  python3 -c "import sys,json; print(json.load(sys.stdin)['myID'])" 2>/dev/null || echo "unknown")"

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
say ""
say "  ================================================================="
say "  Knowledge Vault sync deployed."
say ""
say "  Vault path:    ${VAULT_PATH}"
say "  Folder ID:     ${FOLDER_ID}"
say "  WebUI:         http://127.0.0.1:8384"
say "  State file:    ${STATE_DIR}/state.json"
say "  Sync check:    every hour (systemd user timer)"
say ""
say "  THIS DEVICE ID:  ${DEVICE_ID}"
say ""
say "  ==== NEXT STEP: Device Pairing ===="
say ""
say "  On each existing peer (Prod VPS, other laptops), run:"
say ""
say "    syncthing cli config devices add --device-id ${DEVICE_ID} --name $(hostname)-vault"
say "    syncthing cli config folders ${FOLDER_ID} devices add --device-id ${DEVICE_ID}"
say ""
say "  On this device, add each existing peer:"
say ""
say "    syncthing cli config devices add --device-id <PEER_ID> --name <peer-name>-vault"
say "    syncthing cli config folders ${FOLDER_ID} devices add --device-id <PEER_ID>"
say ""
say "  After pairing, verify:"
say ""
say "    curl -s -H 'X-API-Key: ${API_KEY}' 'http://127.0.0.1:8384/rest/db/status?folder=${FOLDER_ID}' | python3 -c \"import sys,json; d=json.load(sys.stdin); print(f'State: {d.get(\\\"state\\\")}, Errors: {d.get(\\\"errors\\\")}')\""
say ""
say "  Commands:"
say "    ~/.local/bin/vault-sync-healthcheck           # manual health check"
say "    systemctl --user status vault-sync.timer       # timer status"
say "    systemctl --user start vault-sync.service      # manual sync check"
say "    cat ~/.local/share/vault-sync/state.json       # view state"
say "  ================================================================="
