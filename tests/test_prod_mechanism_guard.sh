#!/usr/bin/env bash
# Prod-mekanizma tripwire testleri (scripts/prod-mechanism-guard.py):
# PreToolUse stdin JSON'u sentetik üretilir, korunan yüzey / marker / container
# / fail-open davranışları exit koduyla doğrulanır. Canlı hook devreye bir
# SONRAKİ oturum başlangıcında girer; bu test script'i doğrudan çağırır.
#
#   bash tests/test_prod_mechanism_guard.sh scripts/prod-mechanism-guard.py
set -uo pipefail
SRC="${1:-scripts/prod-mechanism-guard.py}"
fail=0
check() { if [ "$2" = "$3" ]; then echo "  PASS $1"; else echo "  FAIL $1: expected exit $3 got $2"; fail=1; fi; }

SB="$(mktemp -d)"; trap 'rm -rf "$SB"' EXIT
mkdir -p "$SB/.claude"

run() { # $1=json  $2=CLAUDE_PROJECT_DIR
  printf '%s' "$1" | CLAUDE_PROJECT_DIR="$2" python3 "$SRC" >/dev/null 2>&1; echo $?
}
payload() { printf '{"tool_name":"%s","tool_input":{"file_path":"%s"}}' "$1" "$2"; }

echo "== test_prod_mechanism_guard =="

r=$(run "$(payload Edit "$SB/scripts/core/auto-loop.sh")" "$SB")
check "1 korunan Edit bloklanir" "$r" 2

r=$(run "$(payload Edit "$SB/scripts/ops/cost-audit.py")" "$SB")
check "2 korunmayan Edit gecer" "$r" 0

r=$(run "$(payload Write "$SB/scripts/ops/send-gate.py")" "$SB")
check "3 send-gate Write bloklanir" "$r" 2

r=$(run "$(payload Edit "$SB/deploy/runtime.env")" "$SB")
check "4 runtime.env bloklanir" "$r" 2

r=$(run "$(payload Edit "$SB/deploy/runtime.env.example")" "$SB")
check "5 runtime.env.example gecer" "$r" 0

touch "$SB/.claude/.prod-change-approved"
r=$(run "$(payload Edit "$SB/scripts/core/auto-loop.sh")" "$SB")
check "6 taze marker izin verir" "$r" 0

python3 - "$SB/.claude/.prod-change-approved" <<'PY'
import os, sys, time
os.utime(sys.argv[1], (time.time() - 10800,) * 2)
PY
r=$(run "$(payload Edit "$SB/scripts/core/auto-loop.sh")" "$SB")
check "7 bayat marker (3h) bloklar" "$r" 2
rm -f "$SB/.claude/.prod-change-approved"

r=$(printf 'not-json' | CLAUDE_PROJECT_DIR="$SB" python3 "$SRC" >/dev/null 2>&1; echo $?)
check "8 bozuk JSON fail-open" "$r" 0

r=$(run "$(payload Edit "/app/scripts/core/auto-loop.sh")" "/app")
check "9 container no-op" "$r" 0

r=$(run "$(payload Bash "$SB/scripts/core/auto-loop.sh")" "$SB")
check "10 Edit-disi tool'a dokunmaz" "$r" 0

echo
if [ "$fail" = "0" ]; then
  echo "ALL PASS"
else
  echo "SOME FAILED"
fi
exit "$fail"
