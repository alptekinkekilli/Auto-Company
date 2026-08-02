#!/usr/bin/env bash
# Regression tests for the outreach outcome watcher (scripts/ops/reply-watch.py).
#
#   bash tests/test_reply_watch.sh
#
# The judgement this pins is the one nobody re-checks by eye: a message that did not arrive
# must never be counted as silence, and silence must never harden into a verdict. Five real
# firms are waiting on this classification, and the send order depends on it.
#
#   1. a reply           -> reported once, and NOT reported again on the next run
#   2. a bounce          -> DELIVERY FAILURE, and that row is not also called silent
#   3. fresh send        -> nothing (below the silence threshold)
#   4. old, no reply     -> SILENCE, stated with its age, once
#   5. replied AND old   -> reply only; a row that answered is never "silent"
#   6. wording           -> the silence alert says it is an observation, not a verdict
set -uo pipefail
SCRIPT="${1:-scripts/ops/reply-watch.py}"
fail=0
contains() { case "$2" in *"$3"*) echo "  PASS $1" ;; *) echo "  FAIL $1: '$3' not in output"; fail=1 ;; esac; }
absent()   { case "$2" in *"$3"*) echo "  FAIL $1: unexpected '$3'"; fail=1 ;; *) echo "  PASS $1" ;; esac; }

WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT
mkdir -p "$WORK/logs"
NOW=$(python3 -c "import datetime;print(datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z'))")
OLD=$(python3 -c "import datetime;print((datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(hours=100)).strftime('%Y-%m-%dT%H:%M:%S.000Z'))")

python3 - "$WORK/rows.json" "$NOW" "$OLD" <<'PY'
import json, sys
out, now, old = sys.argv[1], sys.argv[2], sys.argv[3]
rows = [
 {"id": "recREPLY", "fields": {"Business": "Cevap Veren A.Ş.", "Replied": True,
  "Email log": "[%s] Sent: Sent (1/15 today)" % old,
  "Reply log": "[%s] iletisim@cevapveren.com: İKN 2026/123456 ile ilgileniyoruz" % now}},
 {"id": "recBOUNCE", "fields": {"Business": "Ulasilamayan Ltd.",
  "Email log": "[%s] Failed: Error: 5.1.1 recipient rejected" % now}},
 {"id": "recFRESH", "fields": {"Business": "Yeni Gonderim Ltd.",
  "Email log": "[%s] Sent: Sent (2/15 today)" % now}},
 {"id": "recSILENT", "fields": {"Business": "Sessiz Kalan Ltd.",
  "Email log": "[%s] Sent: Sent (3/15 today)" % old}},
]
open(out, "w", encoding="utf-8").write(json.dumps(rows, ensure_ascii=False))
PY

run() { python3 "$SCRIPT" --app "$WORK" --fixture "$WORK/rows.json" --silence-hours 72 "$@" 2>&1; }

echo "1-5. first pass over a mixed fixture"
OUT=$(run)
contains "counts"          "$OUT" "sent_rows=4 new_replies=1 new_failures=1 newly_silent=1"
contains "reply reported"  "$OUT" "Cevap Veren"
contains "reply content"   "$OUT" "İKN 2026/123456"
contains "stage-2 warning" "$OUT" "Stage 2"
contains "bounce reported" "$OUT" "Ulasilamayan"
contains "bounce wording"  "$OUT" "SESSİZLİK DEĞİLDİR"
contains "silence"         "$OUT" "Sessiz Kalan"
absent   "fresh row quiet" "$OUT" "Yeni Gonderim"
# The replied row is 100h old: it must NOT also be listed as silent.
absent   "replied != silent" "$OUT" "Cevap Veren A.Ş. (100"

echo "6. the silence alert stays an observation"
contains "no verdict"      "$OUT" "hüküm değil"

echo "7. state suppresses a second alert for the same outcomes"
OUT2=$(run)
contains "nothing new"     "$OUT2" "new_replies=0 new_failures=0 newly_silent=0"
contains "silent run"      "$OUT2" "no new outcomes"

echo "8. --dry-run leaves no state behind"
rm -f "$WORK/logs/reply-watch-state.json"
run --dry-run >/dev/null
if [ -f "$WORK/logs/reply-watch-state.json" ]; then
    echo "  FAIL dry-run wrote state"; fail=1
else
    echo "  PASS dry-run wrote no state"
fi

if [ "$fail" -eq 0 ]; then echo "ALL PASS"; else echo "FAILURES"; fi
exit "$fail"
