#!/usr/bin/env bash
# Check vault-sync health and optionally send desktop notification on failure.
# Exits 0 when healthy, 1 when unhealthy.
set -euo pipefail

STATE_DIR="${HOME}/.local/share/vault-sync"
STATE_FILE="${STATE_DIR}/state.json"
MAX_STALE_SECONDS=7200   # 2 hours
MAX_CONSECUTIVE_FAILURES=6

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

NOTIFY=false
[[ "${1:-}" == "--notify" ]] && NOTIFY=true

healthy=true
messages=()

# Check state file exists
if [[ ! -f "${STATE_FILE}" ]]; then
  messages+=("State file missing: ${STATE_FILE}")
  healthy=false
else
  # Parse state with python3 (more robust than jq for optional fields)
  read -r last_status completion peers_connected peers_configured consecutive_failures last_success_at pairing_required syncthing_running vault_exists <<< \
    "$(python3 -c "
import json, sys
s = json.load(open('${STATE_FILE}'))
print(
    s.get('last_status', 'unknown'),
    s.get('completion', 'N/A'),
    s.get('peers_connected', 'N/A'),
    s.get('peers_configured', 'N/A'),
    s.get('consecutive_failures', 0),
    s.get('last_success_at', 'never'),
    s.get('pairing_required', False),
    s.get('syncthing_running', False),
    s.get('vault_exists', False),
)
" 2>/dev/null || echo "parse_error N/A N/A N/A 0 never false false false")"

  if [[ "${last_status}" == "parse_error" ]]; then
    messages+=("Cannot parse state file")
    healthy=false
  fi

  # Check Syncthing is running
  if [[ "${syncthing_running}" != "True" ]]; then
    messages+=("Syncthing is not running")
    healthy=false
  fi

  # Check vault path exists
  if [[ "${vault_exists}" != "True" ]]; then
    messages+=("Vault path does not exist")
    healthy=false
  fi

  # Check pairing
  if [[ "${pairing_required}" == "True" ]]; then
    messages+=("Pairing required — no peers configured")
    healthy=false
  fi

  # Check consecutive failures
  if [[ "${consecutive_failures}" -ge "${MAX_CONSECUTIVE_FAILURES}" ]]; then
    messages+=("${consecutive_failures} consecutive failures")
    healthy=false
  fi

  # Check last success freshness
  if [[ "${last_success_at}" != "never" && "${last_success_at}" != "None" ]]; then
    last_success_epoch="$(date -d "${last_success_at}" +%s 2>/dev/null || echo 0)"
    now_epoch="$(date +%s)"
    age=$(( now_epoch - last_success_epoch ))
    if [[ ${age} -gt ${MAX_STALE_SECONDS} ]]; then
      messages+=("Last success is ${age}s old (max ${MAX_STALE_SECONDS}s)")
      healthy=false
    fi
  fi
fi

# Output result
if ${healthy}; then
  printf "${GREEN}  OK${NC}  vault-sync healthy | completion=${completion:-N/A}% peers=${peers_connected:-N/A}/${peers_configured:-N/A}\n"
  exit 0
else
  printf "${RED}FAIL${NC} vault-sync unhealthy\n"
  for msg in "${messages[@]}"; do
    printf "      %s\n" "${msg}"
  done
  if ${NOTIFY} && command -v notify-send &>/dev/null; then
    notify-send -u critical "Vault Sync" "Sync is unhealthy: ${messages[*]::3}"
  fi
  exit 1
fi
