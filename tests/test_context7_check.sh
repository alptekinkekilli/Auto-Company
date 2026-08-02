#!/usr/bin/env bash
# Regression tests for the Context7 consultation check (scripts/ops/context7-check.py).
#
#   bash tests/test_context7_check.sh
#
# The whole value of this check is that it does NOT fire on our own ops scripts, which import
# urllib/json/subprocess and need no documentation lookup. If it cried wolf there it would be
# scrolled past within a day, like the 41%-false-alarm turn audit before it. So the tests are
# mostly about what must stay silent.
#
#   1. stdlib-only Python write            -> OK (this is most of what we write)
#   2. external Python import, no Context7 -> NO-CHECK, and it names the module
#   3. external import WITH a Context7 call -> OK
#   4. relative and node: imports           -> OK (a local file is not a library)
#   5. scoped npm package                   -> named as @scope/pkg, not "@scope"
#   6. a docs-only cycle                    -> OK even with zero Context7 calls
#   7. content with escaped quotes/newlines -> still parsed (regex over a code payload is why
#                                              this is JSON-parsed, not pattern-matched)
set -uo pipefail
SCRIPT="${1:-scripts/ops/context7-check.py}"
fail=0
TMP=$(mktemp -d)
contains() { case "$2" in *"$3"*) echo "  PASS $1" ;; *) echo "  FAIL $1: '$3' not in '$2'"; fail=1 ;; esac; }

# Build a one-line ndjson cycle record. $1=file path, $2=content, $3=extra json lines
cycle() {  # cycle <outfile> <written-path> <content-python-literal> [extra_line]
    python3 - "$1" "$2" "$3" "${4:-}" <<'PY'
import json, sys
out, path, content, extra = sys.argv[1:5]
rec = {"type": "assistant", "message": {"content": [
    {"type": "tool_use", "name": "write", "input": {"file_path": path, "content": content}}]}}
with open(out, "w") as fh:
    fh.write(json.dumps(rec) + "\n")
    if extra:
        fh.write(extra + "\n")
PY
}
C7CALL='{"type":"assistant","message":{"content":[{"type":"tool_use","name":"mcp__context7__query-docs","input":{}}]}}'

run() { python3 "$SCRIPT" --cycle "$1" --report; }

echo "1. stdlib-only python stays silent"
cycle "$TMP/a.ndjson" "/app/scripts/ops/foo.py" "import os
import json
from urllib.request import urlopen"
contains "OK" "$(run "$TMP/a.ndjson")" "CONTEXT7 OK"

echo "2. external import with no Context7 call is flagged"
cycle "$TMP/b.ndjson" "/app/scripts/ops/pay.py" "import os
import stripe
from requests import get"
OUT=$(run "$TMP/b.ndjson")
contains "flagged" "$OUT" "CONTEXT7 NO-CHECK"
contains "names the module" "$OUT" "stripe"
contains "names the file" "$OUT" "pay.py"

echo "3. the same write with a Context7 call is fine"
cycle "$TMP/c.ndjson" "/app/scripts/ops/pay.py" "import stripe" "$C7CALL"
contains "OK" "$(run "$TMP/c.ndjson")" "CONTEXT7 OK"

echo "4. relative and node: imports are not libraries"
cycle "$TMP/d.ndjson" "/app/scripts/send.js" "const a = require('./local');
import fs from 'node:fs';
const p = require('path');"
contains "OK" "$(run "$TMP/d.ndjson")" "CONTEXT7 OK"

echo "5. a scoped package keeps its scope"
cycle "$TMP/e.ndjson" "/app/scripts/send.js" "import x from '@aws-sdk/client-s3';"
contains "scope kept" "$(run "$TMP/e.ndjson")" "@aws-sdk/client-s3"

echo "6. a docs-only cycle is silent"
cycle "$TMP/f.ndjson" "/app/memories/consensus.md" "import stripe (this is prose, not code)"
contains "OK" "$(run "$TMP/f.ndjson")" "none importing an external library"

echo "7. a payload full of quotes and newlines is still parsed"
cycle "$TMP/g.ndjson" "/app/scripts/x.py" 'import boto3
s = "he said \"hi\"\nand left"
t = """triple
quoted"""'
contains "still flagged" "$(run "$TMP/g.ndjson")" "boto3"

rm -rf "$TMP"
if [ "$fail" -eq 0 ]; then echo "ALL PASS"; else echo "FAILURES"; fi
exit "$fail"
