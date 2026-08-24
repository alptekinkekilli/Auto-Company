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
tool("bash", "python3 scripts/ops/browse-extract.py https://x.test --grep kvkk")
tool("mcp__browseros__navigate")
tool("mcp__browseros__grep")
tool("bash", "grep -n foo /app/PROMPT.md")
tool("read")
tool("bash", "grep -n send_gate graft/INDEX.md graft/scripts/ops/send-gate.md")
tool("bash", "bash .graft-kit/bin/graft-build.sh")
tool("bash", "echo engrafting is a word but not a card path")
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
check "total calls counted"   calls      16
check "ctx7 counted"          ctx7        1
check "airtable reads (script+mcp)" airtable_r 3
check "airtable writes (script+mcp)" airtable_w 2
check "linear counted"        linear      1
# browser = site-contact-evidence + browse-extract harness + 2 raw MCP steps; the harness
# must be COUNTED, otherwise moving work into it would fake a drop in the A/B.
check "browser counts harness AND mcp" browser 4
check "browser_mcp counts only raw MCP steps" browser_mcp 2
check "graft card reads + kit wrapper counted" graft 2

echo "[2] idempotence: second run appends nothing"
python3 "$TUA" --app "$TMP"
N=$(wc -l < "$TMP/logs/tool-usage-history.ndjson" | tr -d ' ')
[ "$N" = 1 ] && ok "ledger still one line" || bad "ledger grew to $N lines"

echo "[3] new file is picked up (backfill)"
cp "$TMP/logs/cycle-ndjson/cycle-0001.ndjson" "$TMP/logs/cycle-ndjson/cycle-0002.ndjson"
python3 "$TUA" --app "$TMP"
N=$(wc -l < "$TMP/logs/tool-usage-history.ndjson" | tr -d ' ')
[ "$N" = 2 ] && ok "second cycle appended" || bad "expected 2 lines, got $N"

echo "[3b] a REWRITTEN filename is audited again (cycle counter resets on restart)"
# The loop numbers cycles from 1 after every container restart, so cycle-0001.ndjson is
# rewritten by a brand-new cycle. Dedup by filename alone silently dropped those cycles.
sleep 1                                     # ensure a distinct mtime
cat "$TMP/logs/cycle-ndjson/cycle-0001.ndjson" "$TMP/logs/cycle-ndjson/cycle-0001.ndjson" \
    > "$TMP/logs/cycle-ndjson/cycle-0002.ndjson"
python3 "$TUA" --app "$TMP"
N=$(wc -l < "$TMP/logs/tool-usage-history.ndjson" | tr -d ' ')
[ "$N" = 3 ] && ok "rewritten file re-audited" || bad "expected 3 lines, got $N"
LAST=$(tail -1 "$TMP/logs/tool-usage-history.ndjson")
python3 -c "import json,sys; d=json.loads(sys.argv[1]); sys.exit(0 if d['calls']==32 else 1)" "$LAST" \
  && ok "re-audit counted the NEW content" || bad "re-audit used stale counts"
python3 "$TUA" --app "$TMP"
N=$(wc -l < "$TMP/logs/tool-usage-history.ndjson" | tr -d ' ')
[ "$N" = 3 ] && ok "still idempotent when unchanged" || bad "grew to $N on unchanged rerun"

echo "[3c] per-MCP-tool-name counts (the input a denylist trim needs)"
FIRST=$(head -1 "$TMP/logs/tool-usage-history.ndjson")
namecount() { python3 -c "
import json,sys
n=json.loads(sys.argv[1]).get('names',{})
print(n.get(sys.argv[2], 0))" "$FIRST" "$1"; }
[ "$(namecount mcp__airtable__update_records_for_table)" = 1 ] \
  && ok "mcp tool name recorded" || bad "airtable write tool name missing"
[ "$(namecount mcp__browseros__navigate)" = 1 ] \
  && ok "browseros tool name recorded" || bad "browseros tool name missing"
# bash dominates every cycle and is not denylist material — recording it would bloat the
# ledger for no decision it could inform.
[ "$(namecount bash)" = 0 ] && ok "non-MCP tools are not name-recorded" || bad "bash leaked into names"
NKEYS=$(python3 -c "
import json,sys; print(len(json.loads(sys.argv[1]).get('names',{})))" "$FIRST")
[ "$NKEYS" = 4 ] && ok "exactly the 4 distinct MCP tools" || bad "expected 4 name keys, got $NKEYS"

OUT=$(python3 "$TUA" --app "$TMP" --names)
printf '%s' "$OUT" | grep -q "LEDGER (durable)" && ok "--names reports the ledger" || bad "no ledger section"
printf '%s' "$OUT" | grep -q "TRANSCRIPTS ON DISK" \
  && ok "--names keeps transcripts separate from the ledger" || bad "no transcript section"
printf '%s' "$OUT" | grep -q "mcp__airtable__update_records_for_table" \
  && ok "--names lists tool names" || bad "tool names missing from report"
printf '%s' "$OUT" | grep -qi "were denied" \
  && ok "--names warns that absence is not evidence of disuse" || bad "missing denylist caveat"
BEFORE=$(wc -l < "$TMP/logs/tool-usage-history.ndjson" | tr -d ' ')
python3 "$TUA" --app "$TMP" --names >/dev/null
AFTER=$(wc -l < "$TMP/logs/tool-usage-history.ndjson" | tr -d ' ')
[ "$BEFORE" = "$AFTER" ] && ok "--names writes nothing" || bad "--names mutated the ledger"

echo "[4] --report prints the ledger, exit 0 without ndjson dir"
OUT=$(python3 "$TUA" --app "$TMP" --report)
printf '%s' "$OUT" | grep -q '"ctx7":1' && ok "report shows counts" || bad "report missing counts"
rm -rf "$TMP/logs/cycle-ndjson"
python3 "$TUA" --app "$TMP" && ok "exit 0 with missing dir" || bad "nonzero exit on missing dir"

echo
echo "tool-usage-audit: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
