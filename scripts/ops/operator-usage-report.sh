#!/usr/bin/env bash
# Runs on the OPERATOR's machine (not the server, not the container).
#
# The loop and the operator share one Claude plan, but the container can only see
# the loop's own spend — so a fixed budget is wrong whenever the operator is
# working. This pushes the operator's current 5h block spend (from ccusage) into
# the container, where refresh_dynamic_budget() sizes the loop's cap around it:
#
#   loop_cap = PLAN_CEILING_USD - max(operator_spend, reserve% x ceiling)
#
# Safe to run on a schedule. Every failure path is a no-op: if ccusage is missing,
# the Mac is offline, or the container is down, nothing is written and the loop
# falls back to treating the operator as idle (the reserve-only cap).
set -uo pipefail

HOST="${AC_SSH_HOST:-powerupp-ts}"
CCUSAGE="${CCUSAGE_BIN:-ccusage}"

command -v "$CCUSAGE" >/dev/null 2>&1 || exit 0

raw=$("$CCUSAGE" blocks --active --json 2>/dev/null) || exit 0
[ -n "$raw" ] || exit 0

payload=$(printf '%s' "$raw" | python3 -c '
import json, sys, time
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)
blocks = d.get("blocks") or ([d] if isinstance(d, dict) and "costUSD" in d else [])
active = next((b for b in blocks if b.get("isActive")), None)
if not active:
    sys.exit(0)          # no active block = operator idle; write nothing, let it go stale
print(json.dumps({
    "costUSD":    round(float(active.get("costUSD") or 0), 4),
    "blockStart": active.get("startTime"),
    "blockEnd":   active.get("endTime"),
    "capturedAt": int(time.time()),
    "source":     "ccusage blocks --active",
}))
') || exit 0
[ -n "$payload" ] || exit 0

# Write it inside the container. The file's mtime is what the loop uses to decide
# freshness, so a stopped reporter degrades to "operator idle" on its own.
printf '%s' "$payload" | ssh -o BatchMode=yes -o ConnectTimeout=10 "$HOST" '
  C=$(docker ps --format "{{.Names}}" | grep "^z12a992" | head -1)
  [ -n "$C" ] || exit 0
  docker exec -i -u app "$C" bash -c "cat > /app/logs/operator-usage.json"
' 2>/dev/null || exit 0

[ "${1:-}" = "-v" ] && echo "pushed: $payload"
exit 0
