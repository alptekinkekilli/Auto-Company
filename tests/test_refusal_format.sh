#!/usr/bin/env bash
# The cockpit writes a refusal; operator_request_notify.py must still close the request.
#
# Why this test exists: the REFUSE line is matched by a LINE-ANCHORED regex, so the panel
# used to flatten the operator's whole reason onto it — which turned a numbered, paragraphed
# refusal into one 2,000-character run-on in the ledger (observed 2026-08-06). The fix puts
# a short head on the REFUSE line and the verbatim text below it. That is exactly the kind
# of format change that silently breaks the parser, so: assert BOTH that the multi-line
# shape survives AND that the request still ends up REFUSED.
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
NOTIFY="$ROOT/scripts/core/operator_request_notify.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); echo "  PASS: $1"; }
bad() { FAIL=$((FAIL+1)); echo "  FAIL: $1"; }

mkdir -p "$TMP/memories" "$TMP/logs"

{
  printf '# Operator Requests\n\n'
  printf '## OPREQ-FORMAT-TEST-001\n\n'
  printf -- '- Status: OPEN\n'
  printf -- '- Type: external-action-authorization\n'
  printf -- '- Blocked scope: none, format regression test\n'
  printf -- '- Required input: Authorize or refuse the trim.\n'
  printf -- '- Acceptable response format: REFUSE OPREQ-FORMAT-TEST-001 at the start of its own line.\n'
  printf -- '- Created: 2026-08-06T09:00:00Z\n'
} > "$TMP/memories/operator-requests.md"

# Exactly the shape dashboard/server.py now writes: one-line head, verbatim block below.
{
  printf '# Operator Decisions\n\n'
  printf '## OPREQ-FORMAT-TEST-001 — refused 2026-08-06T09:21:27+00:00\n\n'
  printf 'Resolves: OPREQ-FORMAT-TEST-001\n'
  printf 'Decided via: cockpit operator-decision panel\n'
  printf 'REFUSE OPREQ-FORMAT-TEST-001 — Refused on evidence quality, not on the goal.\n'
  printf '\nFull reasoning as written by the operator:\n\n'
  printf 'Refused on evidence quality, not on the goal.\n\n'
  printf '1. The evidence is circular: the ledger begins after the tools were denied.\n'
  printf '2. The original reason was different from the one now recorded.\n\n'
  printf 'Re-file after 2026-08-13 with seven days of per-tool-name data.\n'
} > "$TMP/memories/operator-decisions.md"

echo "[1] the written shape is genuinely multi-line"
LINES=$(wc -l < "$TMP/memories/operator-decisions.md" | tr -d ' ')
[ "$LINES" -ge 12 ] && ok "reasoning kept its line structure ($LINES lines)" \
                    || bad "collapsed to $LINES lines"
grep -qE '^REFUSE OPREQ-FORMAT-TEST-001 — .{1,200}$' "$TMP/memories/operator-decisions.md" \
  && ok "REFUSE head is a single bounded line" || bad "REFUSE line missing or oversized"
grep -q '^2\. The original reason' "$TMP/memories/operator-decisions.md" \
  && ok "numbered points survive as their own lines" || bad "numbering flattened"

echo "[2] the parser still closes the request"
python3 "$NOTIFY" "$TMP" >/dev/null 2>&1
STATUS=$(grep -A2 '^## OPREQ-FORMAT-TEST-001' "$TMP/memories/operator-requests.md" \
         | grep -m1 'Status:' | sed 's/.*Status:[[:space:]]*//')
[ "$STATUS" = "REFUSED" ] && ok "request marked REFUSED" || bad "status is '$STATUS', expected REFUSED"

if [ -f "$TMP/memories/operator-requests-audit.log" ]; then
  grep -q 'REFUSED OPREQ-FORMAT-TEST-001' "$TMP/memories/operator-requests-audit.log" \
    && ok "audit log records the refusal" || bad "audit log has no REFUSED entry"
  # The audit line is one line: the head, not the whole essay.
  LONGEST=$(awk '{ print length }' "$TMP/memories/operator-requests-audit.log" | sort -rn | head -1)
  [ "$LONGEST" -lt 600 ] && ok "audit line stays readable ($LONGEST chars)" \
                         || bad "audit line is $LONGEST chars — the essay leaked into it"
else
  bad "no audit log written"
fi

echo "[3] rerun is idempotent"
python3 "$NOTIFY" "$TMP" >/dev/null 2>&1
N=$(grep -c 'REFUSED OPREQ-FORMAT-TEST-001' "$TMP/memories/operator-requests-audit.log" 2>/dev/null || echo 0)
[ "$N" = 1 ] && ok "no duplicate refusal entry" || bad "audit grew to $N entries"

echo
echo "refusal-format: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
