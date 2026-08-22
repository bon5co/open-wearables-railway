#!/bin/sh
# Rewrites the build-time API URL placeholder in the served bundle to this
# deployment's backend URL, then starts the Nitro server.
set -e

: "${OW_BACKEND_URL:?FATAL: OW_BACKEND_URL is not set. Refusing to boot.}"

BACKEND_URL="${OW_BACKEND_URL%/}"
case "$BACKEND_URL" in
    http://*|https://*) ;;
    *) BACKEND_URL="https://${BACKEND_URL}" ;;
esac

rm -rf /app/.output
cp -a /app/.output.pristine /app/.output

grep -rl '__OW_BACKEND_URL__' /app/.output \
    | while read -r f; do
        sed -i "s|https://__OW_BACKEND_URL__|${BACKEND_URL}|g; s|__OW_BACKEND_URL__|${BACKEND_URL}|g" "$f"
    done

if grep -rq '__OW_BACKEND_URL__' /app/.output; then
    echo "FATAL: API URL placeholder survived the rewrite. Refusing to boot." >&2
    exit 1
fi

echo "[railway] frontend API URL set to ${BACKEND_URL}"
exec "$@"
