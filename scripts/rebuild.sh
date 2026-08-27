#!/usr/bin/env bash
# Rebuild the site and restart the local `jekyll serve`.
# Usage: scripts/rebuild.sh
set -euo pipefail
cd "$(dirname "$0")/.."

PORT=4000
PIDFILE=.jekyll-serve.pid
LOG=.jekyll-serve.log
BASEURL="$(sed -n 's/^baseurl: *//p' _config.yml | head -1 | tr -d '"' | cut -d' ' -f1)"

# 1. Stop any running server: pidfile first, then a sweep.
#    The pattern uses the [s] trick so pkill never matches this script's own cmdline.
if [[ -f "$PIDFILE" ]]; then
  kill "$(cat "$PIDFILE")" 2>/dev/null || true
  rm -f "$PIDFILE"
fi
pkill -f 'jekyll[s]erve' 2>/dev/null || true
sleep 1

# 2. Clean rebuild.
rm -rf _site .jekyll-cache
bundle exec jekyll build

# 3. Start detached (own session, so it survives this shell exiting).
setsid nohup bundle exec jekyll serve --port "$PORT" > "$LOG" 2>&1 < /dev/null &

# 4. Wait for it, then record the real listener pid and verify the page.
UP=""
for _ in $(seq 1 30); do
  if curl -sf "http://127.0.0.1:$PORT$BASEURL/" -o /dev/null; then UP=1; break; fi
  sleep 1
done
[[ -n "$UP" ]] || { echo "server did not come up; see $LOG" >&2; exit 1; }

PID="$(ss -tlnp 2>/dev/null | grep ":$PORT " | grep -oP 'pid=\K[0-9]+' | head -1 || true)"
[[ -n "$PID" ]] && echo "$PID" > "$PIDFILE"

echo "serving: http://127.0.0.1:$PORT$BASEURL/  (pid ${PID:-?}, log $LOG)"
