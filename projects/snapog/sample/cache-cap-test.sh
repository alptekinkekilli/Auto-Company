#!/usr/bin/env bash
# SnapOG — R2 cache-key cap smoke test (G8 fix #2).
# Fires MONTHLY_CACHE_KEY_CAP + a few distinct requests against a running
# dev server and verifies that early requests return X-Cache: MISS while
# requests past the cap return X-Cache: BYPASSED (still 200, still PNG).
#
# Requires:
#   BASE_URL — running SnapOG dev server (default http://localhost:8891)
#   API_KEY  — a valid free-tier key issued via POST /register
#
# NOTE: your test key must have monthly_limit high enough to absorb all
# requests. We temporarily bump usage_count == 0 and monthly_limit == 9999
# via a direct sqlite UPDATE before running this in CI, or use a fresh key.
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8891}"
KEY="${API_KEY:?API_KEY env var is required}"
CAP="${CAP:-30}"                 # must match src/types.ts MONTHLY_CACHE_KEY_CAP
EXTRA="${EXTRA:-3}"              # how many requests to fire past the cap
TOTAL=$((CAP + EXTRA))

echo "=== SnapOG cache-key cap test ==="
echo "Base URL: $BASE_URL"
echo "Firing $TOTAL requests with distinct titles (cap=$CAP)"
echo ""

miss=0
bypassed=0
other=0
first_bypass_at=""

for i in $(seq 1 "$TOTAL"); do
  # Distinct title per request → distinct cacheKey per request.
  UNIQUE="cap-test-$(date +%s%N)-$i"
  HDR=$(mktemp /tmp/snapog-hdr-XXXX)
  BODY=$(mktemp /tmp/snapog-body-XXXX.png)
  HTTP_CODE=$(curl -sf -D "$HDR" -o "$BODY" -w '%{http_code}' \
    "$BASE_URL/og?title=$UNIQUE&key=$KEY")
  if [ "$HTTP_CODE" != "200" ]; then
    echo "  request #$i → HTTP $HTTP_CODE (unexpected). Headers:"
    cat "$HDR"
    exit 1
  fi
  XCACHE=$(grep -i '^x-cache:' "$HDR" | awk '{print $2}' | tr -d '\r\n')
  SIZE=$(wc -c < "$BODY" | tr -d ' ')
  if [ "$SIZE" -lt 1000 ]; then
    echo "  request #$i returned suspiciously small PNG ($SIZE bytes)"
    exit 1
  fi
  case "$XCACHE" in
    MISS)     miss=$((miss + 1)) ;;
    BYPASSED)
      bypassed=$((bypassed + 1))
      if [ -z "$first_bypass_at" ]; then first_bypass_at="$i"; fi
      ;;
    *)        other=$((other + 1)); echo "  request #$i unexpected X-Cache: $XCACHE" ;;
  esac
  rm -f "$HDR" "$BODY"
done

echo ""
echo "Summary:"
echo "  MISS     : $miss"
echo "  BYPASSED : $bypassed"
echo "  first BYPASSED at request #$first_bypass_at"
[ "$other" -eq 0 ] || { echo "unexpected X-Cache values: $other"; exit 1; }

# Expected shape:
#   The FIRST $CAP requests should be MISS (or a few could already be BYPASSED
#   if this key had prior traffic this billing month — tolerated).
#   The requests after the cap must include at least $EXTRA BYPASSED.
if [ "$bypassed" -lt "$EXTRA" ]; then
  echo "FAIL: expected at least $EXTRA BYPASSED responses, got $bypassed"
  exit 1
fi
if [ "$miss" -gt "$CAP" ]; then
  echo "FAIL: got $miss MISS responses but cap is $CAP"
  exit 1
fi

echo ""
echo "PASS ✓ per-key distinct-cache-key cap is enforced"
