#!/usr/bin/env bash
# The .mcp.json key fallback must work on macOS AND stay a no-op in the container.
#
#   bash tests/test_mcp_key_fallback.sh
#
# Background. `.mcp.json` used to say "AIRTABLE_API_KEY": "${AIRTABLE_API_KEY}" and nothing
# else. When the variable is absent from the process that spawns the MCP server, Claude Code
# passes the placeholder through VERBATIM — the server then receives the 19-character string
# "${AIRTABLE_API_KEY}", which is why Airtable's error read "API key seems too short (19
# characters)". On macOS the variable is absent whenever Claude Code was not started from a
# shell that had sourced ~/.zshrc, which is most of the time.
#
# The fix wraps the server in `sh -c` and falls back to the Keychain. The container reads the
# SAME file and has no `security` binary, so the fallback must never fire there. That is what
# these tests pin: the branch is chosen by the SHAPE of the key that arrives.
#
#   1. macOS, placeholder arrives   -> Keychain is consulted
#   2. macOS, variable unset        -> Keychain is consulted
#   3. container, real key present  -> passed through untouched, `security` never runs
#   4. the command actually embedded in .mcp.json is the one tested (not a copy that drifts)
set -uo pipefail
CFG="${1:-.mcp.json}"
fail=0
check() { if [ "$2" = "$3" ]; then echo "  PASS $1"; else echo "  FAIL $1: got '$2' want '$3'"; fail=1; fi; }

STUB=$(mktemp -d)
# A stand-in for macOS `security` so this suite is hermetic and runs on Linux too. It records
# that it was called, which is how test 3 proves the container path never reaches it.
printf '#!/bin/sh\necho called >> "%s/called"\nprintf %%s FROM-KEYCHAIN.value\n' "$STUB" > "$STUB/security"
chmod +x "$STUB/security"

# Pull the real command out of the config: everything before `exec`, then report the result.
snippet() {  # snippet <server> <varname>
    python3 -c "
import json,sys
srv=json.load(open('$CFG'))['mcpServers']['$1']
cmd=srv['args'][1]
print(cmd.split('exec ')[0] + 'printf %s \"\$$2\"')
"
}
run() {  # run <snippet> <env assignment...>
    env PATH="$STUB:$PATH" "${@:2}" sh -c "$1"
}

for pair in "airtable AIRTABLE_API_KEY pat-real.value" "linear LINEAR_API_KEY lin_api_realvalue"; do
    set -- $pair
    srv=$1; var=$2; real=$3
    echo "$srv"
    S=$(snippet "$srv" "$var")
    case "$S" in *security*) echo "  PASS fallback present in $CFG" ;;
                 *) echo "  FAIL no Keychain fallback in $CFG for $srv"; fail=1 ;; esac

    rm -f "$STUB/called"
    check "placeholder -> keychain" "$(run "$S" "$var=\${$var}")" "FROM-KEYCHAIN.value"

    rm -f "$STUB/called"
    check "unset -> keychain" "$(env -u "$var" PATH="$STUB:$PATH" sh -c "$S")" "FROM-KEYCHAIN.value"

    rm -f "$STUB/called"
    check "real key passes through" "$(run "$S" "$var=$real")" "$real"
    if [ -f "$STUB/called" ]; then
        echo "  FAIL container path invoked security — it does not exist there"; fail=1
    else
        echo "  PASS security not invoked when the key is already valid"
    fi
done

rm -rf "$STUB"
if [ "$fail" -eq 0 ]; then echo "ALL PASS"; else echo "FAILURES"; fi
exit "$fail"
