#!/usr/bin/env bash
# OPREQ-GOV-DIRECTIVE-BODY-001 (operator-authorized 2026-08-11): directive_writer.py's
# undefined_section_refs() must catch a body that references "§N" without ever defining
# a matching "## §N" header — exactly the shape that froze directive revision 11 (it
# referenced absent §6/§7, making its Completion clause unsatisfiable). Pure-function
# test: no file I/O, no live directive state, calls the function directly.
#
#   bash tests/test_directive_section_refs.sh scripts/core/directive_writer.py
set -uo pipefail
SRC="${1:-scripts/core/directive_writer.py}"
fail=0
check() { if [ "$2" = "$3" ]; then echo "  PASS $1"; else echo "  FAIL $1: expected '$3' got '$2'"; fail=1; fi; }

run_py() {
  # $1 = body (heredoc via stdin), prints undefined_section_refs() as comma-joined
  python3 -c "
import importlib.util
spec = importlib.util.spec_from_file_location('dw', '$SRC')
dw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dw)
import sys
body = sys.stdin.read()
print(','.join(dw.undefined_section_refs(body)))
"
}

echo "== test_directive_section_refs =="

# 1. Clean body: every referenced section is defined.
out="$(run_py <<'EOF'
status: ACTIVE

## §1 -- Scope

See §1 for the current scope.

## §2 -- Standing mode

Refer back to §1 when in doubt.
EOF
)"
check "clean body: no missing refs" "$out" ""

# 2. Body with zero section markers at all (most directives): must not false-positive.
out="$(run_py <<'EOF'
status: ACTIVE

Plain prose directive with no section markers anywhere.
EOF
)"
check "no §-markers at all: no missing refs" "$out" ""

# 3. Revision-11 shape: references §6 (twice) and §7 (three times), neither defined.
out="$(run_py <<'EOF'
status: ACTIVE

## §1 -- Scope

## Completion

Mark DONE only when §6 confirms and §7 confirms, per §6 and §7 above, and §7 once more.
EOF
)"
check "revision-11 shape: §6 and §7 both flagged" "$out" "6,7"

# 4. A single undefined ref among otherwise-defined sections.
out="$(run_py <<'EOF'
status: ACTIVE

## §1 -- Scope
## §2 -- Mode

Refer to §1, §2, and §3 (the last one is never defined).
EOF
)"
check "single undefined ref among defined ones" "$out" "3"

# 5. Header defined but never referenced in prose: fine, not an error either way
#    (an unreferenced section is not the failure mode this check targets).
out="$(run_py <<'EOF'
status: ACTIVE

## §1 -- Scope
## §9 -- Never mentioned again
EOF
)"
check "defined-but-unreferenced section: no missing refs" "$out" ""

# 6. Empty body: no refs, no crash.
out="$(run_py <<'EOF'
EOF
)"
check "empty body: no missing refs, no crash" "$out" ""

echo
if [ "$fail" = "0" ]; then
  echo "ALL PASS"
else
  echo "SOME FAILED"
fi
exit "$fail"
