#!/usr/bin/env bash
# Regression tests for scripts/ops/registry-queue-watch.py (APP-277).
#
#   bash tests/test_registry_queue_watch.sh
#
# The watcher tells the operator when a MERSİS session is worth their time. Two failure
# modes it must never have:
#   1. Crying wolf — firing below the threshold, or repeating inside the cooldown, trains
#      the operator to ignore it.
#   2. Misattributing the bottleneck — an empty bridge queue with many attribution-Held
#      firms is a COMPANY gap ("we never asked"), not an operator gap ("you owe us
#      CAPTCHAs"). The 2026-08-01 dry run produced exactly that message with a "0 bekleyen
#      sorgu var" headline; these cases pin the corrected wording.
#
# Airtable is stubbed by intercepting urllib at import time, so the tests are offline and
# deterministic.
set -uo pipefail
WATCHER="${1:-scripts/ops/registry-queue-watch.py}"
fail=0
contains() { case "$2" in *"$3"*) echo "  PASS $1" ;; *) echo "  FAIL $1: '$3' not in '${2:0:400}'"; fail=1 ;; esac; }
not_contains() { case "$2" in *"$3"*) echo "  FAIL $1: unexpected '$3'"; fail=1 ;; *) echo "  PASS $1" ;; esac; }

WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
mkdir -p "$WORK/logs" "$WORK/scripts/core"
printf 'AIRTABLE_API_KEY=stub-key\n' > "$WORK/logs/runtime.env"

# $1 = registry-pending, $2 = attribution-held, $3 = ekap-pending, $4.. = extra args
run_watch() {
    local pend="$1" held="$2" ekap="${3:-0}"; shift 3 2>/dev/null || shift 2
    PEND_N="$pend" HELD_N="$held" EKAP_N="$ekap" APP_DIR="$WORK" WATCHER_PATH="$WATCHER" \
    python3 - "$@" <<'PY'
import io, json, os, sys, types, urllib.request

pend_n, held_n = int(os.environ["PEND_N"]), int(os.environ["HELD_N"])
ekap_n = int(os.environ.get("EKAP_N", "0"))
app = os.environ["APP_DIR"]

def rec(fields):
    return {"id": "rec" + str(abs(hash(str(fields))))[:10], "fields": fields}

pending = [rec({"request_id": f"REGBR-T-{i}", "firm": f"Pendfirm{i} A.Ş.",
                "query_key": f"PENDFIRM{i}", "status": "PENDING"}) for i in range(pend_n)]
held = [rec({"Business": f"Heldfirm{i} Ltd. Şti.", "Status": "Held - Evidence insufficient",
             "Notes": "G4 attribution fails under Rule 9"}) for i in range(held_n)]
ekap = [rec({"request_id": f"EKAPBR-T-{i}", "KararNo": f"2026/UM.IV-{1600+i}",
             "status": "PENDING"}) for i in range(ekap_n)]

def fake_urlopen(req, timeout=None):
    url = req.full_url if hasattr(req, "full_url") else str(req)
    if "tblrQfg4nS3htetcE" in url:
        body = {"records": ekap}
    elif "tblREW6MtTMTP5h5N" in url:
        body = {"records": pending}
    else:
        body = {"records": held}
    return io.BytesIO(json.dumps(body).encode())

class _Ctx(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *a): return False

def wrapped(req, timeout=None):
    return _Ctx(fake_urlopen(req, timeout).getvalue())

urllib.request.urlopen = wrapped
sys.argv = ["watch", "--app", app] + sys.argv[1:]
exec(compile(open(os.environ["WATCHER_PATH"]).read(), "watcher", "exec"), {"__name__": "__main__"})
PY
}

echo "--- 1: below threshold — silent ---"
out=$(run_watch 1 0 0 --dry-run 2>&1)
contains "counts reported" "$out" "registry_pending=1"
contains "stays silent"    "$out" "below threshold"
not_contains "no message"  "$out" "would notify"

echo "--- 2: pending at threshold — operator-actionable message ---"
out=$(run_watch 3 0 0 --dry-run 2>&1)
contains "fires"              "$out" "would notify"
contains "bridge headline"   "$out" "Operatör oturumu zamanı"
contains "lists a request"    "$out" "REGBR-T-0"
contains "names the ask"      "$out" "köprü turu yapalım"

echo "--- 3: empty queue + many attribution holds — COMPANY gap, not operator gap ---"
out=$(run_watch 0 6 0 --dry-run 2>&1)
contains "fires"                    "$out" "would notify"
contains "correct headline"         "$out" "kuyruğu BOŞ"
contains "attributes correctly"     "$out" "operatör darboğazı DEĞİL"
not_contains "no misleading count"  "$out" "0 bekleyen sorgu var"
not_contains "does not demand captchas" "$out" "köprü turu yapalım"

echo "--- 3b: EKAP-only queue fires (the v1 blind spot) ---"
out=$(run_watch 0 0 3 --dry-run 2>&1)
contains "ekap counted"      "$out" "ekap_pending=3"
contains "fires"             "$out" "would notify"
contains "names EKAP queue"  "$out" "KararId köprüsü"
contains "lists a KararNo"   "$out" "2026/UM.IV-1600"

echo "--- 4: cooldown — a second call inside repeat-hours stays silent ---"
rm -f "$WORK/logs/.registry-queue-state.json"
out=$(run_watch 3 0 0 2>&1)                    # real run: writes state (notify is a no-op, no telegram-notify.sh)
contains "first call notifies" "$out" "notified"
out=$(run_watch 3 0 0 2>&1)
contains "second call silent"  "$out" "notified" # prints "notified Xh ago — silent"
contains "cooldown honoured"   "$out" "silent"

echo "--- 5: queue drains — state cleared so the NEXT backlog alerts immediately ---"
out=$(run_watch 0 0 0 2>&1)
contains "silent when clear" "$out" "below threshold"
if [ -f "$WORK/logs/.registry-queue-state.json" ]; then echo "  FAIL state not cleared"; fail=1; else echo "  PASS state cleared"; fi
out=$(run_watch 3 0 0 2>&1)
contains "alerts again right away" "$out" "notified"

echo
if [ "$fail" = "0" ]; then echo "ALL PASS"; else echo "FAILURES"; exit 1; fi
