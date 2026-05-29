#!/usr/bin/env python3
"""Query Syncthing REST API and write vault sync health state.

Reads API key from ~/.config/syncthing/config.xml.
Writes state JSON to ~/.local/share/vault-sync/state.json.
Logs to ~/.local/share/vault-sync/log.

Exit 0 on success, non-zero on failure.
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API_BASE = "http://127.0.0.1:8384/rest"
FOLDER_ID = "pkm-vault"

STATE_DIR = Path.home() / ".local" / "share" / "vault-sync"
STATE_FILE = STATE_DIR / "state.json"
LOG_FILE = STATE_DIR / "log"

SYNCTHING_CONFIG = Path.home() / ".config" / "syncthing" / "config.xml"
VAULT_PATH = os.environ.get("PKM_VAULT_PATH") or os.environ.get("OBSIDIAN_VAULT_PATH") or os.path.join(str(Path.home()), "KnowledgeVault")

COMPLETION_THRESHOLD = 99.9


def _read_api_key() -> str:
    if not SYNCTHING_CONFIG.exists():
        raise FileNotFoundError(f"Syncthing config not found: {SYNCTHING_CONFIG}")
    content = SYNCTHING_CONFIG.read_text()
    m = re.search(r"<apikey>(.*?)</apikey>", content)
    if not m:
        raise ValueError("API key not found in Syncthing config")
    return m.group(1)


def _api_get(path: str, api_key: str) -> dict:
    url = f"{API_BASE}{path}"
    req = urllib.request.Request(url, headers={"X-API-Key": api_key})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        raise ConnectionError(f"Syncthing API unreachable at {API_BASE}: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from Syncthing API: {e}")


def _check_vault_exists() -> bool:
    return Path(VAULT_PATH).is_dir()


def _check_syncthing_running() -> bool:
    try:
        urllib.request.urlopen(f"{API_BASE}/system/status", timeout=5)
        return True
    except Exception:
        return False


def _collect_state(api_key: str) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    state = {
        "checked_at": now,
        "vault_path": VAULT_PATH,
        "vault_exists": _check_vault_exists(),
        "syncthing_running": _check_syncthing_running(),
        "pairing_required": False,
        "completion": None,
        "peers_connected": 0,
        "peers_configured": 0,
        "folder_errors": 0,
        "folder_state": None,
        "last_status": "failed",
    }

    if not state["syncthing_running"]:
        state["error"] = "Syncthing is not running or API is unreachable"
        return state

    # Check folder status
    try:
        folder_status = _api_get(f"/db/status?folder={FOLDER_ID}", api_key)
        state["folder_state"] = folder_status.get("state", "unknown")
        state["folder_errors"] = folder_status.get("errors", 0)
    except Exception as e:
        state["folder_state_error"] = str(e)

    # Check completion
    try:
        completion = _api_get(f"/db/completion?folder={FOLDER_ID}", api_key)
        state["completion"] = completion.get("completion", 0)
    except Exception as e:
        state["completion_error"] = str(e)

    # Check connections
    try:
        connections = _api_get("/system/connections", api_key)
        conn_map = connections.get("connections", {})
        state["peers_connected"] = len(conn_map)
    except Exception as e:
        state["connections_error"] = str(e)

    # Check configured devices for this folder
    try:
        config = _api_get("/config/folders", api_key)
        for folder in config:
            if folder.get("id") == FOLDER_ID:
                devices = folder.get("devices", [])
                state["peers_configured"] = len(devices)
                break
    except Exception as e:
        state["config_error"] = str(e)

    if state["peers_configured"] == 0:
        state["pairing_required"] = True

    # Determine success
    if state["pairing_required"]:
        state["last_status"] = "failed"
        state["error"] = "No peers configured. Run device pairing."
    elif state["folder_state"] == "error" or state["folder_errors"] > 0:
        state["last_status"] = "failed"
        state["error"] = f"Folder state={state['folder_state']}, errors={state['folder_errors']}"
    elif state["completion"] is not None and state["completion"] >= COMPLETION_THRESHOLD:
        state["last_status"] = "success"
    elif not state["vault_exists"]:
        state["last_status"] = "failed"
        state["error"] = f"Vault path does not exist: {VAULT_PATH}"
    else:
        state["last_status"] = "failed"
        state["error"] = f"Completion below threshold: {state['completion']:.1f}%"

    return state


def _update_consecutive_failures(state: dict) -> None:
    prev = {}
    if STATE_FILE.exists():
        try:
            prev = json.loads(STATE_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            pass

    prev_failures = prev.get("consecutive_failures", 0)
    prev_status = prev.get("last_status")

    if state["last_status"] == "success":
        state["consecutive_failures"] = 0
        state["last_success_at"] = state["checked_at"]
    else:
        state["consecutive_failures"] = prev_failures + 1
        state["last_success_at"] = prev.get("last_success_at")

    if prev_status is None:
        state["previous_status"] = "initial"


def _write_state(state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = STATE_FILE.with_suffix(STATE_FILE.suffix + ".tmp")
    tmp.write_text(json.dumps(state, indent=2) + "\n")
    tmp.rename(STATE_FILE)


def _log(state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    line = (
        f"{state['checked_at']} "
        f"status={state['last_status']} "
        f"completion={state.get('completion', 'N/A')}% "
        f"peers={state.get('peers_connected', 0)}/{state.get('peers_configured', 0)} "
        f"folder_state={state.get('folder_state', 'N/A')} "
        f"errors={state.get('folder_errors', 0)} "
        f"consecutive_failures={state.get('consecutive_failures', 0)}\n"
    )
    with open(LOG_FILE, "a") as f:
        f.write(line)


def main() -> int:
    api_key = _read_api_key()
    state = _collect_state(api_key)
    _update_consecutive_failures(state)
    _write_state(state)
    _log(state)

    if state["last_status"] == "success":
        print(f"OK: completion={state.get('completion', 'N/A')}%, peers={state.get('peers_connected', 0)}/{state.get('peers_configured', 0)}")
        return 0
    else:
        error = state.get("error", "unknown")
        print(f"FAIL: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
