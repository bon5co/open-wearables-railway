#!/bin/bash
# Railway entrypoint for the Open Wearables backend image.
#
# Usage: railway-entrypoint.sh <role-script>   e.g. scripts/start/app.sh
#
# Railway injects PORT into every service and its HTTP healthcheck dials that
# injected port, so the API has to listen on it; upstream reads API_PORT.
set -e

export API_PORT="${PORT:-${API_PORT:-8000}}"

ROLE_SCRIPT="$1"
if [ -z "$ROLE_SCRIPT" ]; then
    echo "FATAL: no role script given to railway-entrypoint.sh" >&2
    exit 1
fi

echo "[railway] role=${ROLE_SCRIPT} API_PORT=${API_PORT}"
exec bash "$ROLE_SCRIPT"
