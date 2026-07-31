#!/usr/bin/env bash
# RUNTIME proof that jcode can actually reach the required MCP servers.
#
#   jcode-mcp-probe.sh [required_csv]   (default: airtable,linear,context7,browseros)
#
# Why a runtime probe and not a config check: a config listing four servers proves
# nothing about four servers being reachable, and jcode reports NO ERROR for a server
# that fails to launch — the model just silently has fewer tools. Measured 2026-07-31:
# the community `airtable-mcp-server` package died on its own broken dependency
# (`Cannot find module 'hono/ws'`) and every check that read the config file passed
# while Airtable — this company's most-used write surface — was simply absent from the
# cycle. A boot check that cannot see that is decoration.
#
# So this asks jcode itself, once, and greps its answer.
#
# Exit: 0 all required servers present · 1 one or more missing · 2 the probe could not
# run (which is also a failure — an unprovable capability is not a capability).
set -uo pipefail

REQUIRED="${1:-${JCODE_MCP_REQUIRED:-airtable,linear,context7,browseros}}"
JCODE_BIN="${JCODE_BIN:-$(command -v jcode 2>/dev/null || echo /usr/local/bin/jcode)}"
PROVIDER="${JCODE_PROBE_PROVIDER:-claude}"
MODEL="${JCODE_PROBE_MODEL:-claude-haiku-4-5}"
TIMEOUT="${JCODE_PROBE_TIMEOUT:-180}"
WORKDIR="${JCODE_PROBE_CWD:-${PROJECT_DIR:-/app}}"

[ -x "$JCODE_BIN" ] || { echo "MCP_PROBE_FAILED: jcode not executable at $JCODE_BIN" >&2; exit 2; }

ev="$(mktemp)"; trap 'rm -f "$ev"' EXIT

# Deliberately the cheapest model and a read-only question: this runs on every boot.
# --tools is NOT restricted here; the probe must see what the harness will see, and the
# cycle-time allowlist is applied separately by auto-loop.sh.
timeout "$TIMEOUT" "$JCODE_BIN" -p "$PROVIDER" -m "$MODEL" -C "$WORKDIR" \
    run 'List the names of every MCP server you can currently see, comma separated, lowercase, nothing else. If you can see none, reply exactly NONE.' \
    --quiet --no-update --no-selfdev --ndjson > "$ev" 2>/dev/null
rc=$?

answer=""
if [ -s "$ev" ] && [ -x "$(dirname "$0")/jcode-final-text.py" ]; then
    answer="$(python3 "$(dirname "$0")/jcode-final-text.py" "$ev" 2>/dev/null | tr '[:upper:]' '[:lower:]')"
fi

if [ -z "$answer" ]; then
    echo "MCP_PROBE_FAILED: no answer from jcode (rc=$rc) — cannot prove MCP reachability" >&2
    exit 2
fi

missing=""
for r in $(printf '%s' "$REQUIRED" | tr ',' ' '); do
    case "$answer" in *"$r"*) ;; *) missing="$missing $r" ;; esac
done

if [ -n "$missing" ]; then
    echo "MCP_PROBE_MISSING:$missing" >&2
    echo "  jcode answered: $(printf '%s' "$answer" | head -c 200)" >&2
    exit 1
fi

echo "MCP_PROBE_OK: $(printf '%s' "$answer" | head -c 200)"
exit 0
