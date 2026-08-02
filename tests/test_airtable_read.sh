#!/usr/bin/env bash
# Regression tests for the scoped Airtable reader (scripts/ops/airtable-read.py).
#
#   bash tests/test_airtable_read.sh
#
# Why this exists: whole-table reads were the largest single context cost in the system
# (28,717 bytes/call average, $2.41 in re-reads over 7 cycles — more than every external
# web fetch combined). The wrapper is only worth denying the raw MCP tool for if its
# refusals cannot be bypassed by accident and its queries are shaped the way Airtable
# documents. Every test below runs OFFLINE via --print-query, so the suite needs no API
# key and touches no base.
#
#   1. no scope                    -> REFUSED (this is the whole point)
#   2. scope but no columns        -> REFUSED
#   3. --all-fields over the cap   -> REFUSED, and --force lifts it
#   4. --max-records over the cap  -> REFUSED
#   5. scoped + columns            -> query carries fields/maxRecords/pageSize
#   6. --record ids                -> RECORD_ID() OR-formula, combined with --formula via AND
#   7. pageSize never exceeds Airtable's documented 100 ceiling
#   8. --describe                  -> exempt from scoping (it reads exactly one row)
set -uo pipefail
SCRIPT="${1:-scripts/ops/airtable-read.py}"
fail=0
contains() { case "$2" in *"$3"*) echo "  PASS $1" ;; *) echo "  FAIL $1: '$3' not in '$2'"; fail=1 ;; esac; }
not_contains() { case "$2" in *"$3"*) echo "  FAIL $1: unexpected '$3'"; fail=1 ;; *) echo "  PASS $1" ;; esac; }
rc_is() { if [ "$2" = "$3" ]; then echo "  PASS $1"; else echo "  FAIL $1: rc=$2 expected $3"; fail=1; fi; }

run() { python3 "$SCRIPT" --print-query "$@" 2>&1; }

echo "1. unscoped read is refused"
OUT=$(run --table tblX --fields Name); RC=$?
rc_is "rc" "$RC" 2
contains "names the fix" "$OUT" "--formula"
contains "offers count-only" "$OUT" "--count-only"

echo "2. scoped but column-less read is refused"
OUT=$(run --table tblX --formula "{Status}='PENDING'"); RC=$?
rc_is "rc" "$RC" 2
contains "names --fields" "$OUT" "--fields"

echo "3. --all-fields is capped, --force lifts it"
OUT=$(run --table tblX --view V --all-fields --max-records 50); RC=$?
rc_is "refused" "$RC" 2
OUT=$(run --table tblX --view V --all-fields --max-records 50 --force); RC=$?
rc_is "forced" "$RC" 0

echo "4. --max-records ceiling holds"
OUT=$(run --table tblX --view V --fields Name --max-records 500); RC=$?
rc_is "refused" "$RC" 2
contains "names the ceiling" "$OUT" "200"

echo "5. a proper scoped query is emitted"
OUT=$(run --table tblRegistry --view "Ready to send" --fields Name --fields Status --max-records 7)
contains "fields" "$OUT" '"fields": ["Name", "Status"]'
contains "view" "$OUT" '"view": "Ready to send"'
contains "maxRecords" "$OUT" '"maxRecords": 7'

echo "6. record ids become a RECORD_ID() formula"
OUT=$(run --table tblX --record recAAA --record recBBB --fields Name)
contains "OR of ids" "$OUT" "OR(RECORD_ID()='recAAA',RECORD_ID()='recBBB')"
OUT=$(run --table tblX --record recAAA --formula "{Status}='X'" --fields Name)
contains "AND with formula" "$OUT" "AND(OR(RECORD_ID()='recAAA'),{Status}='X')"

echo "7. pageSize respects Airtable's 100 ceiling"
OUT=$(run --table tblX --view V --fields Name --max-records 150 --force)
contains "pageSize capped" "$OUT" '"pageSize": 100'
OUT=$(run --table tblX --view V --fields Name --max-records 3)
contains "pageSize follows small asks" "$OUT" '"pageSize": 3'

echo "8. --fields accepts the comma form as well as the repeated one"
# The company guessed comma-joined twice in two cycles and burned a turn each time. Both
# spellings must produce the identical query.
A=$(run --table tblX --view V --fields "Name,Status" --fields Email)
B=$(run --table tblX --view V --fields Name --fields Status --fields Email)
if [ "$A" = "$B" ]; then echo "  PASS comma form == repeated form"; else
    echo "  FAIL comma form differs"; echo "   A=$A"; echo "   B=$B"; fail=1; fi
contains "fields expanded" "$A" '"fields": ["Name", "Status", "Email"]'

echo "9. --describe needs no scope"
# --print-query so this stays offline even on a machine that HAS a key: --describe would
# otherwise reach the API, and a suite that hits the network on some machines is not a suite.
OUT=$(run --table tblX --describe --base appX); RC=$?
rc_is "rc" "$RC" 0
not_contains "not refused for scope" "$OUT" "unscoped read refused"

if [ "$fail" -eq 0 ]; then echo "ALL PASS"; else echo "FAILURES"; fi
exit "$fail"
