#!/bin/bash
# Tests for scripts/ops/tool-usage-audit.py — categorization from a realistic jcode
# event stream (tool_start + fragmented tool_input deltas) and ledger idempotence.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TUA="$HERE/../scripts/ops/tool-usage-audit.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); echo "  PASS: $1"; }
bad() { FAIL=$((FAIL+1)); echo "  FAIL: $1"; }

mkdir -p "$TMP/logs/cycle-ndjson"
python3 - "$TMP/logs/cycle-ndjson/cycle-0001.ndjson" <<'PY'
import json, sys
ev = []
def tool(name, command=None):
    ev.append({"type": "tool_start", "name": name})
    if command is not None:
        # jcode streams the input as fragments — split mid-token on purpose
        raw = json.dumps({"command": command})
        ev.append({"type": "tool_input", "delta": raw[:9]})
        ev.append({"type": "tool_input", "delta": raw[9:]})
    ev.append({"type": "tool_exec", "name": name})
tool("bash", "cd /app && npx ctx7@latest docs /websites/sqlite_docs 'fts5' > /tmp/ctx7.txt")
tool("bash", "python3 scripts/ops/airtable-read.py --table tblX --fields A")
tool("bash", "python3 scripts/ops/airtable-read.py --table tblX --record recY")
tool("bash", "python3 scripts/ops/airtable-write.py --apply --table tblX")
tool("mcp__airtable__update_records_for_table")
tool("mcp__airtable__get_table_schema")
tool("bash", "python3 scripts/ops/linear-track.py --comment APP-269")
tool("bash", "python3 scripts/ops/site-contact-evidence.py example.com")
tool("bash", "grep -n foo /app/PROMPT.md")
tool("read")
ev.append({"type": "done", "model": "claude-sonnet-5"})
open(sys.argv[1], "w").write("\n".join(json.dumps(e) for e in ev) + "\n")
PY

echo "[1] categorization from fragmented tool_input stream"
python3 "$TUA" --app "$TMP"
LINE=$(head -1 "$TMP/logs/tool-usage-history.ndjson")
check() { # desc, jq-ish key, expected
    got=$(python3 -c "import json,sys;print(json.loads(sys.argv[1])[sys.argv[2]])" "$LINE" "$2")
    [ "$got" = "$3" ] && ok "$1" || bad "$1 — expected $3, got $got"
}
check "total calls counted"   calls      10
check "ctx7 counted"          ctx7        1
check "airtable reads (script+mcp)" airtable_r 3
check "airtable writes (script+mcp)" airtable_w 2
check "linear counted"        linear      1
check "browser counted"       browser     1

echo "[2] idempotence: second run appends nothing"
python3 "$TUA" --app "$TMP"
N=$(wc -l < "$TMP/logs/tool-usage-history.ndjson" | tr -d ' ')
[ "$N" = 1 ] && ok "ledger still one line" || bad "ledger grew to $N lines"

echo "[3] new file is picked up (backfill)"
cp "$TMP/logs/cycle-ndjson/cycle-0001.ndjson" "$TMP/logs/cycle-ndjson/cycle-0002.ndjson"
python3 "$TUA" --app "$TMP"
N=$(wc -l < "$TMP/logs/tool-usage-history.ndjson" | tr -d ' ')
[ "$N" = 2 ] && ok "second cycle appended" || bad "expected 2 lines, got $N"

echo "[4] --report prints the ledger, exit 0 without ndjson dir"
OUT=$(python3 "$TUA" --app "$TMP" --report)
printf '%s' "$OUT" | grep -q '"ctx7":1' && ok "report shows counts" || bad "report missing counts"
rm -rf "$TMP/logs/cycle-ndjson"
python3 "$TUA" --app "$TMP" && ok "exit 0 with missing dir" || bad "nonzero exit on missing dir"

echo
echo "tool-usage-audit: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
