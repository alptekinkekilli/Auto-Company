#!/usr/bin/env bash
# Tests for scripts/ops/browse-extract.py — run against a FAKE MCP gateway so they are
# offline and deterministic. The fake logs every tools/call name+args to CALLS so the
# tests can assert the tab is ALWAYS closed (the invariant that protects the single-tab
# gateway from leaking tabs on error paths).
set -u
cd "$(dirname "$0")/.."
SCRIPT=scripts/ops/browse-extract.py
TMP=$(mktemp -d)
trap 'kill $SRV_PID 2>/dev/null; rm -rf "$TMP"' EXIT
PASS=0; FAIL=0
ok()   { PASS=$((PASS+1)); echo "  ok  - $1"; }
bad()  { FAIL=$((FAIL+1)); echo "  FAIL - $1"; }
check(){ if [ "$1" = "0" ]; then ok "$2"; else bad "$2"; fi; }

cat > "$TMP/fake_gateway.py" <<'PY'
import json, os, sys
from http.server import BaseHTTPRequestHandler, HTTPServer

CALLS = os.environ["CALLS"]
MODE = os.environ.get("MODE", "ok")   # ok | grep-error

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        method = body.get("method", "")
        rid = body.get("id")
        if method == "initialize":
            out = {"jsonrpc": "2.0", "id": rid, "result": {"protocolVersion": "2024-11-05",
                   "capabilities": {}, "serverInfo": {"name": "fake", "version": "0"}}}
        elif method == "tools/call":
            name = body["params"]["name"]
            args = body["params"]["arguments"]
            with open(CALLS, "a") as f:
                f.write(json.dumps({"name": name, "args": args}) + "\n")
            text, is_err = self.dispatch(name, args)
            out = {"jsonrpc": "2.0", "id": rid, "result": {
                "content": [{"type": "text", "text": text}], "isError": is_err}}
        else:
            out = {"jsonrpc": "2.0", "id": rid, "result": {}}
        data = json.dumps(out).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def dispatch(self, name, args):
        if name == "tabs" and args.get("action") == "new":
            return "Opened page 31 in background", False
        if name == "tabs" and args.get("action") == "close":
            return "closed", False
        if name == "navigate":
            return "navigated", False
        if name == "wait":
            return "waited", False
        if name == "grep":
            if MODE == "grep-error":
                return "boom: renderer crashed", True
            return "12: info@firma.com.tr found here\n40: kvkk aydinlatma metni", False
        if name == "read":
            return "X" * 10000, False
        return "?", True

HTTPServer(("127.0.0.1", int(sys.argv[1])), H).serve_forever()
PY

PORT=8931
export CALLS="$TMP/calls.ndjson"
MODE=ok CALLS="$CALLS" python3 "$TMP/fake_gateway.py" $PORT & SRV_PID=$!
sleep 0.6
MCP="http://127.0.0.1:$PORT/mcp"

echo "1) usage: no URL -> rc 2"
python3 $SCRIPT >/dev/null 2>&1
[ $? = 2 ] && ok "argparse rejects empty" || bad "argparse rejects empty"

echo "2) happy path grep"
: > "$CALLS"
OUT=$(python3 $SCRIPT https://x.test --grep "kvkk" --mcp "$MCP" --wait-ms 10 2>&1); RC=$?
check $RC "rc 0"
echo "$OUT" | grep -q "GREP 'kvkk': 2 line" && ok "grep lines counted" || bad "grep lines counted"
echo "$OUT" | grep -q "info@firma.com.tr" && ok "match text surfaced" || bad "match text surfaced"
grep -q '"action": "close"' "$CALLS" && ok "tab closed" || bad "tab closed"
echo "$OUT" | grep -q "READ" && bad "no read when grep given" || ok "no read when grep given"

echo "3) read truncation cap"
OUT=$(python3 $SCRIPT https://x.test --mcp "$MCP" --wait-ms 10 --max-bytes 4000 2>&1)
echo "$OUT" | grep -q "READ text: 4000B of 10000B \[truncated\]" && ok "cap + true size named" || bad "cap + true size named"

echo "4) multi-URL: one tab, navigate for the rest"
: > "$CALLS"
OUT=$(python3 $SCRIPT https://a.test https://b.test --grep "x" --mcp "$MCP" --wait-ms 10 2>&1); RC=$?
check $RC "rc 0"
NAVS=$(grep -c '"name": "navigate"' "$CALLS")
[ "$NAVS" = "1" ] && ok "exactly 1 navigate for 2nd url" || bad "exactly 1 navigate for 2nd url (got $NAVS)"
NEWS=$(grep -c '"action": "new"' "$CALLS")
[ "$NEWS" = "1" ] && ok "exactly 1 tab opened" || bad "exactly 1 tab opened (got $NEWS)"
[ "$(echo "$OUT" | grep -c '^== ')" = "2" ] && ok "2 url blocks" || bad "2 url blocks"

echo "5) --json parses and has grep key"
python3 $SCRIPT https://x.test --grep k --mcp "$MCP" --wait-ms 10 --json 2>/dev/null \
  | python3 -c "import json,sys; d=json.load(sys.stdin); assert d[0]['grep']" \
  && ok "json shape" || bad "json shape"

echo "6) --keep-tab: no close, page id printed"
: > "$CALLS"
OUT=$(python3 $SCRIPT https://x.test --grep k --keep-tab --mcp "$MCP" --wait-ms 10 2>&1)
echo "$OUT" | grep -q "KEPT TAB: page 31" && ok "page id printed" || bad "page id printed"
grep -q '"action": "close"' "$CALLS" && bad "close skipped" || ok "close skipped"

echo "7) tool error mid-flow: rc 4, tab STILL closed"
kill $SRV_PID 2>/dev/null; wait $SRV_PID 2>/dev/null
MODE=grep-error CALLS="$CALLS" python3 "$TMP/fake_gateway.py" $PORT & SRV_PID=$!
sleep 0.6
: > "$CALLS"
OUT=$(python3 $SCRIPT https://x.test --grep "kvkk" --mcp "$MCP" --wait-ms 10 2>&1); RC=$?
[ $RC = 4 ] && ok "rc 4 on tool error" || bad "rc 4 on tool error (got $RC)"
echo "$OUT" | grep -q "ERROR:" && ok "error surfaced" || bad "error surfaced"
grep -q '"action": "close"' "$CALLS" && ok "tab closed on error path" || bad "tab closed on error path"

echo "8) gateway unreachable: rc 3"
python3 $SCRIPT https://x.test --mcp "http://127.0.0.1:1/mcp" >/dev/null 2>&1
[ $? = 3 ] && ok "rc 3 unreachable" || bad "rc 3 unreachable"

echo
echo "browse-extract: $PASS passed, $FAIL failed"
[ $FAIL = 0 ]
