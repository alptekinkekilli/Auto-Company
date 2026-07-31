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

# `airtable-call-ok` is deliberately in the required set: a server can be VISIBLE and
# still fail every call — measured 2026-07-31, when the airtable bridge appeared in the
# model's server list and then answered "Failed to connect to MCP server 'airtable'" on
# each attempt (a corrupt npx dependency cache). Visibility is not capability, so the
# probe now proves one real read.
REQUIRED="${1:-${JCODE_MCP_REQUIRED:-airtable,linear,context7,browseros,airtable-call-ok}}"
JCODE_BIN="${JCODE_BIN:-$(command -v jcode 2>/dev/null || echo /usr/local/bin/jcode)}"
PROVIDER="${JCODE_PROBE_PROVIDER:-claude}"
MODEL="${JCODE_PROBE_MODEL:-claude-haiku-4-5}"
TIMEOUT="${JCODE_PROBE_TIMEOUT:-180}"
WORKDIR="${JCODE_PROBE_CWD:-${PROJECT_DIR:-/app}}"

[ -x "$JCODE_BIN" ] || { echo "MCP_PROBE_FAILED: jcode not executable at $JCODE_BIN" >&2; exit 2; }

# The loop deliberately keeps the RAW sk-ant-oat token in its own environment (so the
# CLI rollback path keeps working) and wraps it only inside each jcode subprocess. This
# probe is its own process, so it must do the same wrap — without it jcode gets a token
# shape it cannot use, answers nothing, and the probe reports "unreachable" for servers
# that are perfectly fine. (Exactly what happened on the first canary run.)
case "${CLAUDE_CODE_OAUTH_TOKEN:-}" in
    sk-ant-oat*)
        _exp=$(( ($(date +%s) + 86400*300) * 1000 ))
        _wrapped=$(python3 -c 'import json,os,sys; print(json.dumps({"claudeAiOauth":{"accessToken":os.environ["CLAUDE_CODE_OAUTH_TOKEN"],"refreshToken":"","expiresAt":int(sys.argv[1]),"scopes":["user:inference"],"subscriptionType":"max"}}))' "$_exp" 2>/dev/null || true)
        [ -n "$_wrapped" ] && export CLAUDE_CODE_OAUTH_TOKEN="$_wrapped"
        unset _wrapped _exp
        ;;
esac

ev="$(mktemp)"; trap 'rm -f "$ev"' EXIT

# Deliberately the cheapest model and a read-only question: this runs on every boot.
# --tools is NOT restricted here; the probe must see what the harness will see, and the
# cycle-time allowlist is applied separately by auto-loop.sh.
timeout "$TIMEOUT" "$JCODE_BIN" -p "$PROVIDER" -m "$MODEL" -C "$WORKDIR" \
    run 'Call the airtable MCP tool that lists bases. Then reply with ONE line: the comma-separated lowercase names of every MCP server you can see. Nothing else.' \
    --quiet --no-update --no-selfdev --ndjson > "$ev" 2>/dev/null
rc=$?

# DETERMINISTIC verdict from the event stream, not from the model's prose. The stream
# carries `tool_start`/`tool_done` events with the real tool name, an `error` field and
# the raw `output` — facts. An earlier version graded the model's sentence, which is
# both fuzzy and gameable by narration ("I'll call the airtable tool…" contains the
# server name whether or not anything was called).
vf="$(mktemp)"; trap 'rm -f "$ev" "$vf"' EXIT
python3 - "$ev" "$REQUIRED" > "$vf" 2>/dev/null <<'PY'
import json, sys
ev_path, required = sys.argv[1], sys.argv[2]
called_ok = set()      # servers with at least one SUCCESSFUL tool_done
seen = set()           # servers that appear at all (start or done)
text = []
with open(ev_path, encoding="utf-8", errors="replace") as fh:
    for line in fh:
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        t = e.get("type")
        if t == "text_delta":
            text.append(str(e.get("text") or ""))
        name = str(e.get("name") or "")
        if name.startswith("mcp__"):
            parts = name.split("__")
            if len(parts) >= 2:
                seen.add(parts[1])
                if t == "tool_done":
                    err = e.get("error")
                    out = str(e.get("output") or "")
                    bad = err not in (None, "None", "") or not out
                    if not bad:
                        called_ok.add(parts[1])
# Server visibility still comes from the model's line (jcode exposes no list command),
# but a CALL is judged only by events.
listed = "".join(text).lower()
missing = []
for r in required.split(","):
    r = r.strip()
    if not r:
        continue
    if r == "airtable-call-ok":
        if "airtable" not in called_ok:
            missing.append("airtable-call-ok(no successful mcp__airtable__* tool_done)")
    elif r not in listed and r not in seen:
        missing.append(r)
print("MISSING:" + ",".join(missing) if missing else "OK")
print("called_ok=" + ",".join(sorted(called_ok)) + " seen=" + ",".join(sorted(seen)))
PY
verdict="$(cat "$vf" 2>/dev/null || true)"

if [ -z "$verdict" ]; then
    echo "MCP_PROBE_FAILED: could not evaluate the event stream (rc=$rc)" >&2
    exit 2
fi
case "$verdict" in
    MISSING:*)
        echo "MCP_PROBE_MISSING: $(printf '%s' "$verdict" | head -1 | cut -d: -f2-)" >&2
        printf '%s\n' "$verdict" | tail -1 >&2
        exit 1
        ;;
esac

echo "MCP_PROBE_OK: $(printf '%s' "$verdict" | tail -1)"
exit 0
