#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"

mkdir -p "$REPO_ROOT/admin_panel/logs"

dispatch_script="$SCRIPT_DIR/trigger_dispatch.sh"
if [[ ! -f "$dispatch_script" ]]; then
    echo "Error: expected dispatch script at $dispatch_script." >&2
    exit 1
fi
chmod +x "$dispatch_script"

echo "Admin panel support directories and dispatch script are ready."
