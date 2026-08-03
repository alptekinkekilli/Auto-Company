#!/bin/bash
# Offline tests for scripts/ops/state-snapshot.py (--skip-network path + DELTA logic).
# Network fields (bridges/sends/replies) are covered by the live loop itself; what must
# never regress silently is the local parsing (directive status/sha, OPREQ OPEN blocks)
# and the DELTA semantics (first-run, none, named-change, error-exclusion).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SNAP="$HERE/../scripts/ops/state-snapshot.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

PASS=0
FAIL=0
ok()   { PASS=$((PASS+1)); echo "  PASS: $1"; }
bad()  { FAIL=$((FAIL+1)); echo "  FAIL: $1"; }
expect_contains() { # desc, haystack, needle
    if printf '%s' "$2" | grep -qF -- "$3"; then ok "$1"; else bad "$1 — missing [$3] in: $2"; fi
}

mkdir -p "$TMP/memories" "$TMP/logs"
printf '# Human Directive\n\n## Status\nPENDING\n\n## Updated\n2026-08-03T09:00:00Z\n\n## Directive\nbody here\n' > "$TMP/memories/human-directive.md"
printf '## OPREQ-TEST-OPEN-001\n\n- Status: OPEN\n- Type: credential\n\n## OPREQ-TEST-DONE-001\n\n- Status: RESOLVED\n' > "$TMP/memories/operator-requests.md"

echo "[1] first snapshot: parses directive + OPREQ, DELTA is first-run"
OUT=$(python3 "$SNAP" --app "$TMP" --skip-network)
expect_contains "status parsed" "$OUT" "status=PENDING"
SHA=$(python3 -c "import hashlib;print(hashlib.sha256(open('$TMP/memories/human-directive.md','rb').read()).hexdigest()[:16])")
expect_contains "sha16 matches file" "$OUT" "sha16=$SHA"
expect_contains "only OPEN block counted" "$OUT" "opreq: open=1 ids=OPREQ-TEST-OPEN-001"
expect_contains "first-run delta" "$OUT" "DELTA: first snapshot"
expect_contains "network fields skipped" "$OUT" "registry_pending=SKIPPED"

echo "[2] unchanged world: DELTA none"
OUT=$(python3 "$SNAP" --app "$TMP" --skip-network)
expect_contains "delta none" "$OUT" "DELTA: none"

echo "[3] directive edit: DELTA names directive fields only"
printf '# Human Directive\n\n## Status\nDONE\n\n## Updated\n2026-08-03T10:00:00Z\n\n## Directive\nbody here\n' > "$TMP/memories/human-directive.md"
OUT=$(python3 "$SNAP" --app "$TMP" --skip-network)
expect_contains "status change seen" "$OUT" "status=DONE"
expect_contains "delta names directive" "$OUT" "changed=directive_status,directive_sha16"

echo "[4] OPREQ flip to RESOLVED: DELTA names opreq_open"
printf '## OPREQ-TEST-OPEN-001\n\n- Status: RESOLVED\n- Type: credential\n\n## OPREQ-TEST-DONE-001\n\n- Status: RESOLVED\n' > "$TMP/memories/operator-requests.md"
OUT=$(python3 "$SNAP" --app "$TMP" --skip-network)
expect_contains "zero open" "$OUT" "opreq: open=0"
expect_contains "delta names opreq" "$OUT" "changed=opreq_open"

echo "[5] missing ledger: visible ERROR, exit still 0, and no phantom DELTA next run"
rm "$TMP/memories/operator-requests.md"
set +e; OUT=$(python3 "$SNAP" --app "$TMP" --skip-network); RC=$?; set -e
[ "$RC" -eq 0 ] && ok "exit 0 on missing ledger" || bad "exit $RC on missing ledger"
expect_contains "error printed" "$OUT" "opreq: ERROR ledger unreadable"
OUT=$(python3 "$SNAP" --app "$TMP" --skip-network)
expect_contains "errored field excluded from delta" "$OUT" "DELTA: none"

echo
echo "state-snapshot: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
