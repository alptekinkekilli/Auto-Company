#!/usr/bin/env bash
# Regression tests for the single-record Airtable writer (scripts/ops/airtable-write.py).
#
#   bash tests/test_airtable_write.sh
#
# Only the guard is testable offline — every other path in that script needs a live GET.
# That is precisely why the guard was pulled out of main(): the refusals are the part that
# has to hold, and a guard that can only be exercised against production is not exercised.
#
#   1. an ordinary edit of an existing field passes
#   2. a field absent from the row is refused, and --force lifts it
#   3. blanking a field that currently has a value is refused, and --allow-clear lifts it
#   4. blanking an ALREADY-empty field is not "clearing" and needs no flag
#   5. a refusal names the flag that fixes it (a refusal without a remedy gets worked around)
set -uo pipefail
SCRIPT="${1:-scripts/ops/airtable-write.py}"
fail=0
check() { if [ "$2" = "$3" ]; then echo "  PASS $1"; else echo "  FAIL $1: got '$2' want '$3'"; fail=1; fi; }
contains() { case "$2" in *"$3"*) echo "  PASS $1" ;; *) echo "  FAIL $1: '$3' not in '$2'"; fail=1 ;; esac; }

g() {  # g <before-json> <new-json> <allow_clear 0|1> <force 0|1> -> refusal text, "" if allowed
    python3 - "$SCRIPT" "$1" "$2" "$3" "$4" <<'PY'
import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("aw", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
out = m.guard(json.loads(sys.argv[2]), json.loads(sys.argv[3]),
              sys.argv[4] == "1", sys.argv[5] == "1")
print(" | ".join(out).replace("\n", " "))
PY
}

echo "1. an ordinary edit is allowed"
check "no refusal" "$(g '{"Ref":"old","Other":"x"}' '{"Ref":"new"}' 0 0)" ""

echo "2. an unknown field is refused unless forced"
OUT=$(g '{"Ref":"old"}' '{"Reff":"new"}' 0 0)
contains "names the field" "$OUT" "Reff"
contains "names the flag" "$OUT" "--force"
check "forced" "$(g '{"Ref":"old"}' '{"Reff":"new"}' 0 1)" ""

echo "3. clearing a non-empty field is refused unless allowed"
OUT=$(g '{"Ref":"old"}' '{"Ref":""}' 0 0)
contains "names the field" "$OUT" "Ref"
contains "names the flag" "$OUT" "--allow-clear"
check "allowed" "$(g '{"Ref":"old"}' '{"Ref":""}' 1 1)" ""

echo "4. an already-empty field is not a clear"
# Airtable omits empty fields from reads, so 'absent' and 'empty' are the same state; writing
# "" over either one erases nothing and must not demand a flag. --force covers the absence.
check "empty -> empty" "$(g '{"Ref":""}' '{"Ref":""}' 0 0)" ""

echo "5. both problems are reported together, not one at a time"
OUT=$(g '{"Ref":"old"}' '{"Ref":"","Nope":"x"}' 0 0)
contains "clear reported" "$OUT" "--allow-clear"
contains "missing reported" "$OUT" "--force"

if [ "$fail" -eq 0 ]; then echo "ALL PASS"; else echo "FAILURES"; fi
exit "$fail"
