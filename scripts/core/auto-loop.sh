#!/bin/bash
# ============================================================
# Auto Company — 24/7 Autonomous Loop
# ============================================================
# Keeps selected CLI engine (Claude/Codex) running continuously.
# Uses fresh sessions with consensus.md as the relay baton.
#
# Usage:
#   ./auto-loop.sh              # Run in foreground
#   ./auto-loop.sh --daemon     # Run via launchd (macOS only)
#
# Stop:
#   ./stop-loop.sh              # Graceful stop
#   kill $(cat .auto-loop.pid)  # Force stop
#
# Config (env vars):
#   ENGINE=claude               # Engine selection: claude|codex (default: claude)
#   MODEL=...                   # Optional model override (empty = engine default)
#   CLAUDE_BIN=...              # Optional Claude executable override
#   CLAUDE_PERMISSION_MODE=bypassPermissions
#                               # Claude permission mode (default: bypassPermissions)
#   CODEX_BIN=...               # Optional Codex executable override
#   CODEX_SANDBOX_MODE=danger-full-access
#                               # Codex sandbox mode (only for ENGINE=codex)
#   LOOP_INTERVAL=30            # Seconds between cycles (default: 30)
#   CYCLE_TIMEOUT_SECONDS=1800  # Max seconds per cycle before force-kill
#   MAX_CONSECUTIVE_ERRORS=5    # Circuit breaker threshold
#   COOLDOWN_SECONDS=300        # Cooldown after circuit break
#   LIMIT_WAIT_SECONDS=3600     # Wait on usage limit
#   MAX_LOGS=200                # Max cycle logs to keep
#   AUTO_LOOP_PROTECT_GITIGNORE=1
#                               # Restore .gitignore if a cycle mutates it
# ============================================================

set -euo pipefail

# === Resolve project root (always relative to this script) ===
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

LOG_DIR="$PROJECT_DIR/logs"
CONSENSUS_FILE="$PROJECT_DIR/memories/consensus.md"
PROMPT_FILE="$PROJECT_DIR/PROMPT.md"
PID_FILE="$PROJECT_DIR/.auto-loop.pid"
STATE_FILE="$PROJECT_DIR/.auto-loop-state"

# Loop settings (all overridable via env vars)
ENGINE="${ENGINE:-claude}"
ENGINE="$(echo "$ENGINE" | tr '[:upper:]' '[:lower:]')"
MODEL="${MODEL:-}"
MODEL_LABEL="${MODEL:-config-default}"
CLAUDE_BIN="${CLAUDE_BIN:-}"
CLAUDE_EFFORT="${CLAUDE_EFFORT:-}"
CLAUDE_PERMISSION_MODE="${CLAUDE_PERMISSION_MODE:-bypassPermissions}"
CODEX_BIN="${CODEX_BIN:-}"
CODEX_SANDBOX_MODE="${CODEX_SANDBOX_MODE:-danger-full-access}"
FALLBACK_ENGINE="$(echo "${FALLBACK_ENGINE:-}" | tr '[:upper:]' '[:lower:]')"
CODEX_MODEL="${CODEX_MODEL:-}"
# Codex reasoning effort (low/medium/high). Empty = use the codex config.toml default.
# "medium" is the standard tier — heavier, more thorough (used for audits).
CODEX_EFFORT="${CODEX_EFFORT:-}"
# Tier ladder (APP-193): round-robin the model/effort within a MIN..MAX range each
# cycle to spread token burn across cheap/expensive tiers. Opt-in. Ladders are
# comma-separated, cheapest first. When ROUTER_TIER_LADDER=1, per cycle the Claude
# MODEL and the Codex effort each advance round-robin through their ladder.
ROUTER_TIER_LADDER="${ROUTER_TIER_LADDER:-0}"
CLAUDE_TIER_LADDER="${CLAUDE_TIER_LADDER:-claude-haiku-4-5-20251001,claude-sonnet-5}"
CODEX_TIER_LADDER="${CODEX_TIER_LADDER:-low,medium}"
BASE_MODEL="$MODEL"
BASE_CODEX_EFFORT="$CODEX_EFFORT"
RESOLVED_CODEX_BIN=""
FALLBACK_USED=0
CYCLE_ENGINE_OVERRIDE=""
# Set to 1 when a Codex run reports a PERMANENT auth failure (rotated/consumed
# refresh token). Codex is then treated as unavailable for the rest of this
# process so alternation/fallback don't burn every other cycle on a dead engine.
CODEX_DISABLED=0
# Rolling-window spend cap: pause the loop when spend in the last WINDOW_SECONDS
# reaches WINDOW_BUDGET_USD (empty = disabled). Reserves quota for the operator.
WINDOW_BUDGET_USD="${WINDOW_BUDGET_USD:-}"
WINDOW_SECONDS="${WINDOW_SECONDS:-18000}"
BUDGET_PAUSE_SECONDS="${BUDGET_PAUSE_SECONDS:-1800}"
SPEND_LEDGER="$LOG_DIR/spend-window.log"
# Codex quota ledger (APP-189 Phase 1). Codex `exec` returns no USD cost, and the
# ChatGPT/Codex quota is message/window-based rather than dollar-based — so Codex
# consumption is metered as CYCLE COUNT within the same rolling WINDOW_SECONDS.
# This is only a meter: the quota-aware router (Phase 2) will consult it to decide
# alternation/headroom; nothing reads it yet, so engine selection is unchanged.
CODEX_SPEND_LEDGER="$LOG_DIR/codex-window.log"
CODEX_WINDOW_LIMIT="${CODEX_WINDOW_LIMIT:-}"   # max Codex cycles per window (empty = unmetered)
# Weights for the unpriced Codex load index (no published gpt-5.6-sol $/credit rate
# to convert tokens to money). Relative only: output tokens ~4x input, cached ~0.1x.
CODEX_CACHE_WEIGHT="${CODEX_CACHE_WEIGHT:-0.1}"
CODEX_OUTPUT_WEIGHT="${CODEX_OUTPUT_WEIGHT:-4}"
# Quota-aware router (APP-189 Phase 2). ROUTER_ALTERNATE=1 spreads load across both
# quotas: when Claude AND Codex both have window headroom, cycles alternate between
# them (~2x daily throughput, neither exhausts early). Default 0 = prior behavior
# (Claude primary; Codex only on budget-cap or usage-limit). The last engine chosen
# is persisted so fresh per-cycle processes actually alternate.
ROUTER_ALTERNATE="${ROUTER_ALTERNATE:-0}"
ROUTER_STATE_FILE="$LOG_DIR/router-state"
TIER_STATE_FILE="$LOG_DIR/tier-state"
LOOP_INTERVAL="${LOOP_INTERVAL:-30}"
CYCLE_TIMEOUT_SECONDS="${CYCLE_TIMEOUT_SECONDS:-1800}"
MAX_CONSECUTIVE_ERRORS="${MAX_CONSECUTIVE_ERRORS:-5}"
COOLDOWN_SECONDS="${COOLDOWN_SECONDS:-300}"
LIMIT_WAIT_SECONDS="${LIMIT_WAIT_SECONDS:-3600}"
MAX_LOGS="${MAX_LOGS:-200}"
AUTO_LOOP_PROTECT_GITIGNORE="${AUTO_LOOP_PROTECT_GITIGNORE:-1}"
RESOLVED_ENGINE_BIN=""

if [ "$ENGINE" != "claude" ] && [ "$ENGINE" != "codex" ]; then
    echo "Error: ENGINE must be 'claude' or 'codex' (received: '$ENGINE')."
    exit 1
fi

# Keep Agent Teams compatibility for legacy prompts/config.
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# === Functions ===

log() {
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local msg="[$timestamp] $1"
    echo "$msg" >> "$LOG_DIR/auto-loop.log"
    if [ -t 1 ]; then
        echo "$msg"
    fi
}

log_cycle() {
    local cycle_num=$1
    local status=$2
    local msg=$3
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] Cycle #$cycle_num [$status] $msg" >> "$LOG_DIR/auto-loop.log"
    if [ -t 1 ]; then
        echo "[$timestamp] Cycle #$cycle_num [$status] $msg"
    fi
}

check_usage_limit() {
    local output="$1"
    if echo "$output" | grep -qi "usage limit\|rate limit\|too many requests\|resource_exhausted\|overloaded\|quota\|429\|billing\|insufficient credits"; then
        return 0
    fi
    return 1
}

# PERMANENT Codex auth failure (rotated/consumed/revoked refresh token, or a
# missing bearer). Distinct from a transient usage limit — retrying will not fix
# it; the operator must re-login and reseed. Used to disable Codex for the run.
codex_auth_failed() {
    local output="$1"
    echo "$output" | grep -qiE "refresh token was already used|token_invalidated|invalid_grant|missing bearer|401 unauthorized|not logged in"
}

# Append a cycle's cost to the rolling-window ledger (skips 0 / N/A).
record_spend() {
    local cost="$1"
    case "$cost" in ''|N/A|0|0.0) return 0 ;; esac
    printf '%s %s\n' "$(date +%s)" "$cost" >> "$SPEND_LEDGER" 2>/dev/null || true
}

# Sum spend within the last WINDOW_SECONDS, pruning older entries. Echoes USD.
window_spend() {
    [ -f "$SPEND_LEDGER" ] || { echo "0"; return; }
    local now cutoff
    now=$(date +%s)
    cutoff=$((now - WINDOW_SECONDS))
    awk -v c="$cutoff" '$1 >= c' "$SPEND_LEDGER" > "$SPEND_LEDGER.tmp" 2>/dev/null \
        && mv "$SPEND_LEDGER.tmp" "$SPEND_LEDGER" 2>/dev/null || true
    awk '{s += $2} END {printf "%.4f", s + 0}' "$SPEND_LEDGER" 2>/dev/null || echo "0"
}

# Record one completed Codex cycle's real token usage (APP-189). `codex exec --json`
# emits a `turn.completed.usage` event; ChatGPT-auth runs carry no USD cost, so we
# meter TOKENS. Row: `epoch load input cached output reasoning exit`, where `load`
# is an unpriced relative index:
#   load = non_cached_input + cached*CODEX_CACHE_WEIGHT + (output+reasoning)*CODEX_OUTPUT_WEIGHT
# Falls back to a count row (load=1) when usage can't be parsed, so windowing and
# cycle-count stay correct on older CLIs or truncated output. $1 = codex JSONL stdout.
record_codex_usage() {
    local jsonl="$1" epoch usage in cached out reasoning load
    epoch="$(date +%s)"
    usage=""
    if command -v jq >/dev/null 2>&1; then
        usage="$(printf '%s' "$jsonl" | jq -sc '
            [.[] | select(.type == "turn.completed" and .usage != null)] | last | .usage // empty
        ' 2>/dev/null || true)"
    fi
    if [ -z "$usage" ] || [ "$usage" = "null" ]; then
        printf '%s 1 0 0 0 0 %s\n' "$epoch" "${EXIT_CODE:-0}" >> "$CODEX_SPEND_LEDGER" 2>/dev/null || true
        return
    fi
    in="$(printf '%s' "$usage"        | jq -r '.input_tokens // 0'            2>/dev/null || echo 0)"
    cached="$(printf '%s' "$usage"    | jq -r '.cached_input_tokens // 0'     2>/dev/null || echo 0)"
    out="$(printf '%s' "$usage"       | jq -r '.output_tokens // 0'          2>/dev/null || echo 0)"
    reasoning="$(printf '%s' "$usage" | jq -r '.reasoning_output_tokens // 0' 2>/dev/null || echo 0)"
    load="$(awk -v i="$in" -v c="$cached" -v o="$out" -v r="$reasoning" \
        -v cw="$CODEX_CACHE_WEIGHT" -v ow="$CODEX_OUTPUT_WEIGHT" \
        'BEGIN { nc = i - c; if (nc < 0) nc = 0; printf "%.0f", nc + c*cw + (o + r)*ow }')"
    printf '%s %s %s %s %s %s %s\n' "$epoch" "$load" "$in" "$cached" "$out" "$reasoning" "${EXIT_CODE:-0}" \
        >> "$CODEX_SPEND_LEDGER" 2>/dev/null || true
}

# Prune the Codex ledger to the last WINDOW_SECONDS (idempotent helper).
_codex_prune() {
    [ -f "$CODEX_SPEND_LEDGER" ] || return 0
    local now cutoff
    now=$(date +%s); cutoff=$((now - WINDOW_SECONDS))
    awk -v c="$cutoff" '$1 >= c' "$CODEX_SPEND_LEDGER" > "$CODEX_SPEND_LEDGER.tmp" 2>/dev/null \
        && mv "$CODEX_SPEND_LEDGER.tmp" "$CODEX_SPEND_LEDGER" 2>/dev/null || true
}

# Count Codex cycles within the window (row count). Used against CODEX_WINDOW_LIMIT.
codex_window_count() {
    [ -f "$CODEX_SPEND_LEDGER" ] || { echo "0"; return; }
    _codex_prune
    awk 'END {print NR + 0}' "$CODEX_SPEND_LEDGER" 2>/dev/null || echo "0"
}

# Sum the weighted token load across the window (telemetry / future token budgeting).
codex_window_load() {
    [ -f "$CODEX_SPEND_LEDGER" ] || { echo "0"; return; }
    _codex_prune
    awk '{s += $2} END {printf "%d", s + 0}' "$CODEX_SPEND_LEDGER" 2>/dev/null || echo "0"
}

# Persist the engine chosen this cycle so the next (fresh) cycle process can alternate.
_router_persist() {
    printf '%s\n' "$1" > "$ROUTER_STATE_FILE" 2>/dev/null || true
}

# Tier ladder (APP-193): round-robin the Claude MODEL + Codex effort within their
# MIN..MAX ladders each cycle, to spread token burn across cheap/expensive tiers.
# Advances a persisted counter. When off, restores the base config. Called each
# cycle before the engine runs; the chosen engine reads MODEL (Claude) / CODEX_EFFORT.
apply_tier_ladder() {
    if [ "$ROUTER_TIER_LADDER" != "1" ]; then
        MODEL="$BASE_MODEL"
        CODEX_EFFORT="$BASE_CODEX_EFFORT"
        MODEL_LABEL="${MODEL:-config-default}"
        return 0
    fi
    local idx=0
    [ -f "$TIER_STATE_FILE" ] && idx="$(cat "$TIER_STATE_FILE" 2>/dev/null || echo 0)"
    case "$idx" in ''|*[!0-9]*) idx=0 ;; esac

    local _CL _CO n_cl n_co
    IFS=',' read -ra _CL <<< "$CLAUDE_TIER_LADDER"
    IFS=',' read -ra _CO <<< "$CODEX_TIER_LADDER"
    n_cl=${#_CL[@]}; n_co=${#_CO[@]}
    if [ "$n_cl" -gt 0 ]; then
        MODEL="$(printf '%s' "${_CL[$((idx % n_cl))]}" | tr -d '[:space:]')"
        MODEL_LABEL="${MODEL:-config-default}"
    fi
    if [ "$n_co" -gt 0 ]; then
        CODEX_EFFORT="$(printf '%s' "${_CO[$((idx % n_co))]}" | tr -d '[:space:]')"
    fi
    printf '%s\n' "$(( (idx + 1) % 1000000 ))" > "$TIER_STATE_FILE" 2>/dev/null || true
    log "[TIER] round-robin idx=$idx → Claude=$MODEL, Codex effort=$CODEX_EFFORT"
}

# APP-189 Phase 2 — decide which engine runs THIS cycle from remaining quota headroom
# in both ledgers, with optional per-cycle alternation. Sets globals:
#   CYCLE_ENGINE_OVERRIDE : "" (use primary ENGINE / Claude) or "codex"
#   CYCLE_ROUTER_ACTION   : "run" | "pause"
#   CYCLE_ROUTER_MSG      : human-readable reason for the caller to log
# With ROUTER_ALTERNATE=0 this reproduces the prior budget gate exactly: under
# budget -> primary; over budget -> Codex if available, else pause.
select_cycle_engine() {
    CYCLE_ENGINE_OVERRIDE=""
    CYCLE_ROUTER_ACTION="run"
    CYCLE_ROUTER_MSG=""

    # Is Codex usable as an alternate this cycle?
    local codex_avail=0
    if [ "$FALLBACK_ENGINE" = "codex" ] && [ "$CODEX_DISABLED" != "1" ]; then
        [ -z "$RESOLVED_CODEX_BIN" ] && RESOLVED_CODEX_BIN="$(resolve_codex_bin 2>/dev/null || true)"
        [ -n "$RESOLVED_CODEX_BIN" ] && codex_avail=1
    fi

    # Claude window headroom (USD ledger vs budget cap)
    local claude_full=0 window_now="0"
    if [ -n "$WINDOW_BUDGET_USD" ]; then
        window_now="$(window_spend)"
        if awk -v s="$window_now" -v b="$WINDOW_BUDGET_USD" 'BEGIN { exit !(s + 0 >= b + 0) }'; then
            claude_full=1
        fi
    fi

    # Codex window headroom (count ledger vs cycle limit)
    local codex_full=0 codex_now
    codex_now="$(codex_window_count)"
    if [ -n "$CODEX_WINDOW_LIMIT" ] && [ "$codex_now" -ge "$CODEX_WINDOW_LIMIT" ] 2>/dev/null; then
        codex_full=1
    fi

    # Over the Claude budget: offload to Codex if it has headroom, else pause.
    if [ "$claude_full" -eq 1 ]; then
        if [ "$codex_avail" -eq 1 ] && [ "$codex_full" -eq 0 ]; then
            CYCLE_ENGINE_OVERRIDE="codex"
            CYCLE_ROUTER_MSG="[ROUTER] Claude window \$$window_now >= cap \$$WINDOW_BUDGET_USD — offloading to Codex (codex $codex_now/${CODEX_WINDOW_LIMIT:-∞})"
        else
            CYCLE_ROUTER_ACTION="pause"
            CYCLE_ROUTER_MSG="[ROUTER] Claude window \$$window_now >= cap \$$WINDOW_BUDGET_USD; Codex unavailable/full — pausing ${BUDGET_PAUSE_SECONDS}s"
        fi
        _router_persist "${CYCLE_ENGINE_OVERRIDE:-claude}"
        return 0
    fi

    # Claude has headroom. Optional alternation to spread load across both quotas.
    if [ "$ROUTER_ALTERNATE" = "1" ] && [ "$codex_avail" -eq 1 ] && [ "$codex_full" -eq 0 ]; then
        local last
        last="$(cat "$ROUTER_STATE_FILE" 2>/dev/null || echo claude)"
        if [ "$last" = "claude" ]; then
            CYCLE_ENGINE_OVERRIDE="codex"
            CYCLE_ROUTER_MSG="[ROUTER] Alternate → Codex (both have headroom; claude \$$window_now/${WINDOW_BUDGET_USD:-∞}, codex $codex_now/${CODEX_WINDOW_LIMIT:-∞})"
        else
            CYCLE_ROUTER_MSG="[ROUTER] Alternate → Claude (both have headroom; claude \$$window_now/${WINDOW_BUDGET_USD:-∞}, codex $codex_now/${CODEX_WINDOW_LIMIT:-∞})"
        fi
        _router_persist "${CYCLE_ENGINE_OVERRIDE:-claude}"
        return 0
    fi

    # Default: primary Claude.
    _router_persist "claude"
    return 0
}

check_stop_requested() {
    if [ -f "$PROJECT_DIR/.auto-loop-stop" ]; then
        rm -f "$PROJECT_DIR/.auto-loop-stop"
        return 0
    fi
    return 1
}

save_state() {
    cat > "$STATE_FILE" << EOF
LOOP_COUNT=$loop_count
ERROR_COUNT=$error_count
LAST_RUN=$(date '+%Y-%m-%d %H:%M:%S')
STATUS=$1
MODEL=$MODEL_LABEL
ENGINE=$ENGINE
EOF
}

cleanup() {
    log "=== Auto Loop Shutting Down (PID $$) ==="
    rm -f "$PID_FILE"
    save_state "stopped"
    exit 0
}

snapshot_gitignore() {
    if [ "$AUTO_LOOP_PROTECT_GITIGNORE" = "0" ]; then
        echo ""
        return
    fi

    local gitignore_file="$PROJECT_DIR/.gitignore"
    local snapshot_file=""
    if [ -f "$gitignore_file" ]; then
        snapshot_file=$(mktemp)
        cp "$gitignore_file" "$snapshot_file"
    fi
    echo "$snapshot_file"
}

restore_gitignore_if_changed() {
    local snapshot_file="$1"
    if [ "$AUTO_LOOP_PROTECT_GITIGNORE" = "0" ]; then
        [ -n "$snapshot_file" ] && rm -f "$snapshot_file"
        return
    fi

    local gitignore_file="$PROJECT_DIR/.gitignore"
    local changed=0

    if [ -f "$gitignore_file" ]; then
        if [ -z "$snapshot_file" ] || [ ! -f "$snapshot_file" ]; then
            changed=1
        elif ! cmp -s "$gitignore_file" "$snapshot_file"; then
            changed=1
        fi
    else
        if [ -n "$snapshot_file" ] && [ -f "$snapshot_file" ]; then
            changed=1
        fi
    fi

    if [ "$changed" -eq 1 ]; then
        if [ -n "$snapshot_file" ] && [ -f "$snapshot_file" ]; then
            cp "$snapshot_file" "$gitignore_file"
            log_cycle "$loop_count" "GUARD" "Blocked cycle mutation of .gitignore and restored baseline"
        else
            rm -f "$gitignore_file"
            log_cycle "$loop_count" "GUARD" "Blocked cycle-created .gitignore and removed it"
        fi
    fi

    [ -n "$snapshot_file" ] && rm -f "$snapshot_file"
}

get_file_size_bytes() {
    local target_file="$1"
    if [ ! -f "$target_file" ]; then
        echo 0
        return
    fi

    if stat -c%s "$target_file" >/dev/null 2>&1; then
        stat -c%s "$target_file"
        return
    fi

    if stat -f%z "$target_file" >/dev/null 2>&1; then
        stat -f%z "$target_file"
        return
    fi

    wc -c < "$target_file" | tr -d ' '
}

rotate_logs() {
    # Keep only the latest N cycle logs
    local count
    count=$(find "$LOG_DIR" -name "cycle-*.log" -type f 2>/dev/null | wc -l | tr -d ' ')
    if [ "$count" -gt "$MAX_LOGS" ]; then
        local to_delete=$((count - MAX_LOGS))
        find "$LOG_DIR" -name "cycle-*.log" -type f | sort | head -n "$to_delete" | xargs rm -f 2>/dev/null || true
        log "Log rotation: removed $to_delete old cycle logs"
    fi

    # Rotate main log if over 10MB
    local log_size
    log_size=$(get_file_size_bytes "$LOG_DIR/auto-loop.log")
    if [ "$log_size" -gt 10485760 ]; then
        mv "$LOG_DIR/auto-loop.log" "$LOG_DIR/auto-loop.log.old"
        log "Main log rotated (was ${log_size} bytes)"
    fi
}

cleanup_accidental_root_artifacts() {
    local removed=0
    local removed_names=""
    local f base

    # Known accidental artifacts caused by malformed shell redirections in generated commands.
    for f in "$PROJECT_DIR"/=* "$PROJECT_DIR"/口径说明*; do
        [ -f "$f" ] || continue
        if [ ! -s "$f" ]; then
            rm -f "$f"
            removed=$((removed + 1))
            base=$(basename "$f")
            if [ -z "$removed_names" ]; then
                removed_names="$base"
            else
                removed_names="$removed_names, $base"
            fi
        fi
    done

    if [ "$removed" -gt 0 ]; then
        log_cycle "$loop_count" "GUARD" "Removed accidental root zero-byte artifact(s): $removed_names"
    fi
}

backup_consensus() {
    if [ -f "$CONSENSUS_FILE" ]; then
        cp "$CONSENSUS_FILE" "$CONSENSUS_FILE.bak"
    fi
}

restore_consensus() {
    if [ -f "$CONSENSUS_FILE.bak" ]; then
        cp "$CONSENSUS_FILE.bak" "$CONSENSUS_FILE"
        log "Consensus restored from backup after failed cycle"
    fi
}

validate_consensus() {
    if [ ! -s "$CONSENSUS_FILE" ]; then
        return 1
    fi
    if ! grep -q "^# Auto Company Consensus" "$CONSENSUS_FILE"; then
        return 1
    fi
    if ! grep -q "^## Next Action" "$CONSENSUS_FILE"; then
        return 1
    fi
    if ! grep -q "^## Company State" "$CONSENSUS_FILE"; then
        return 1
    fi
    return 0
}

consensus_changed_since_backup() {
    if [ ! -f "$CONSENSUS_FILE" ]; then
        return 1
    fi

    if [ ! -f "$CONSENSUS_FILE.bak" ]; then
        return 0
    fi

    if cmp -s "$CONSENSUS_FILE" "$CONSENSUS_FILE.bak"; then
        return 1
    fi

    return 0
}

resolve_codex_bin() {
    if [ -n "$CODEX_BIN" ]; then
        if [ -x "$CODEX_BIN" ]; then
            echo "$CODEX_BIN"
            return 0
        fi
        if command -v "$CODEX_BIN" >/dev/null 2>&1; then
            command -v "$CODEX_BIN"
            return 0
        fi
    fi

    # Prefer WSL-local Codex installed via nvm.
    local nvm_candidate=""
    for candidate in "$HOME"/.nvm/versions/node/*/bin/codex; do
        if [ -x "$candidate" ]; then
            nvm_candidate="$candidate"
        fi
    done
    if [ -n "$nvm_candidate" ]; then
        echo "$nvm_candidate"
        return 0
    fi

    # Fallback: ask an interactive bash shell (loads user profile).
    local interactive_candidate
    interactive_candidate=$(bash -ic 'command -v codex' 2>/dev/null | tail -n1 | tr -d '\r' || true)
    if [ -n "$interactive_candidate" ] && [ -x "$interactive_candidate" ]; then
        echo "$interactive_candidate"
        return 0
    fi

    # Last fallback: current shell PATH.
    if command -v codex >/dev/null 2>&1; then
        command -v codex
        return 0
    fi

    return 1
}

resolve_claude_bin() {
    if [ -n "$CLAUDE_BIN" ]; then
        if [ -x "$CLAUDE_BIN" ]; then
            echo "$CLAUDE_BIN"
            return 0
        fi
        if command -v "$CLAUDE_BIN" >/dev/null 2>&1; then
            command -v "$CLAUDE_BIN"
            return 0
        fi
    fi

    # Prefer WSL-local Claude CLI installed via nvm.
    local nvm_candidate=""
    for candidate in "$HOME"/.nvm/versions/node/*/bin/claude; do
        if [ -x "$candidate" ]; then
            nvm_candidate="$candidate"
        fi
    done
    if [ -n "$nvm_candidate" ]; then
        echo "$nvm_candidate"
        return 0
    fi

    # Fallback: ask an interactive bash shell (loads user profile).
    local interactive_candidate
    interactive_candidate=$(bash -ic 'command -v claude' 2>/dev/null | tail -n1 | tr -d '\r' || true)
    if [ -n "$interactive_candidate" ] && [ -x "$interactive_candidate" ]; then
        echo "$interactive_candidate"
        return 0
    fi

    # Last fallback: current shell PATH.
    if command -v claude >/dev/null 2>&1; then
        command -v claude
        return 0
    fi

    return 1
}

resolve_engine_bin() {
    case "$ENGINE" in
        claude)
            resolve_claude_bin
            ;;
        codex)
            resolve_codex_bin
            ;;
        *)
            return 1
            ;;
    esac
}

run_codex_cycle() {
    local prompt="$1"
    local output_file timeout_flag message_file

    output_file=$(mktemp)
    timeout_flag=$(mktemp)
    message_file=$(mktemp)

    set +e
    (
        cd "$PROJECT_DIR" || exit 1
        # --skip-git-repo-check: the container workspace /app is not a git repo, and
        # codex exec otherwise refuses to run ("Not inside a trusted directory").
        # Without this, every Claude→Codex fallback fails with exit 1 (observed in
        # container cycles #3/#4/#9).
        # --json makes stdout a JSONL event stream carrying `turn.completed.usage`
        # (per-run token counts) — metered into the Codex ledger. `-o` still writes
        # the clean final message to $message_file, so the cycle SUMMARY is unaffected.
        local codex_cmd=("$RESOLVED_ENGINE_BIN" "exec" "--skip-git-repo-check" "--json" "-c" "sandbox_mode=\"${CODEX_SANDBOX_MODE}\"" "-o" "$message_file")
        if [ -n "$MODEL" ]; then
            codex_cmd+=("-m" "$MODEL")
        fi
        if [ -n "$CODEX_EFFORT" ]; then
            codex_cmd+=("-c" "model_reasoning_effort=\"${CODEX_EFFORT}\"")
        fi
        codex_cmd+=("$prompt")
        "${codex_cmd[@]}"
    ) > "$output_file" 2>&1 &
    local codex_pid=$!

    (
        sleep "$CYCLE_TIMEOUT_SECONDS"
        if kill -0 "$codex_pid" 2>/dev/null; then
            echo "1" > "$timeout_flag"
            kill -TERM "$codex_pid" 2>/dev/null || true
            sleep 5
            kill -KILL "$codex_pid" 2>/dev/null || true
        fi
    ) &
    local watchdog_pid=$!

    wait "$codex_pid"
    EXIT_CODE=$?

    kill "$watchdog_pid" 2>/dev/null || true
    wait "$watchdog_pid" 2>/dev/null || true
    set -e

    OUTPUT=$(cat "$output_file")
    RESULT_MESSAGE=$(cat "$message_file" 2>/dev/null || true)
    rm -f "$output_file" "$message_file"

    if [ -s "$timeout_flag" ]; then
        CYCLE_TIMED_OUT=1
        EXIT_CODE=124
    else
        CYCLE_TIMED_OUT=0
    fi
    rm -f "$timeout_flag"
}

run_claude_cycle() {
    local prompt="$1"
    local output_file timeout_flag

    output_file=$(mktemp)
    timeout_flag=$(mktemp)

    set +e
    (
        cd "$PROJECT_DIR" || exit 1
        local claude_cmd=("$RESOLVED_ENGINE_BIN" "-p" "$prompt" "--output-format" "json")
        if [ -n "$MODEL" ]; then
            claude_cmd+=("--model" "$MODEL")
        fi
        if [ -n "$CLAUDE_EFFORT" ]; then
            claude_cmd+=("--effort" "$CLAUDE_EFFORT")
        fi
        if [ -n "$CLAUDE_PERMISSION_MODE" ]; then
            claude_cmd+=("--permission-mode" "$CLAUDE_PERMISSION_MODE")
        fi
        "${claude_cmd[@]}"
    ) > "$output_file" 2>&1 &
    local claude_pid=$!

    (
        sleep "$CYCLE_TIMEOUT_SECONDS"
        if kill -0 "$claude_pid" 2>/dev/null; then
            echo "1" > "$timeout_flag"
            kill -TERM "$claude_pid" 2>/dev/null || true
            sleep 5
            kill -KILL "$claude_pid" 2>/dev/null || true
        fi
    ) &
    local watchdog_pid=$!

    wait "$claude_pid"
    EXIT_CODE=$?

    kill "$watchdog_pid" 2>/dev/null || true
    wait "$watchdog_pid" 2>/dev/null || true
    set -e

    OUTPUT=$(cat "$output_file")
    RESULT_MESSAGE="$OUTPUT"
    rm -f "$output_file"

    if [ -s "$timeout_flag" ]; then
        CYCLE_TIMED_OUT=1
        EXIT_CODE=124
    else
        CYCLE_TIMED_OUT=0
    fi
    rm -f "$timeout_flag"
}

run_engine_cycle() {
    local prompt="$1"
    FALLBACK_USED=0
    # Budget-forced Codex override: at the Claude window cap, run this cycle on
    # Codex (a separate quota) instead of Claude so the company keeps working.
    if [ "$CYCLE_ENGINE_OVERRIDE" = "codex" ] && [ -n "$RESOLVED_CODEX_BIN" ]; then
        local _bo="$RESOLVED_ENGINE_BIN" _mo="$MODEL"
        RESOLVED_ENGINE_BIN="$RESOLVED_CODEX_BIN"
        MODEL="$CODEX_MODEL"
        run_codex_cycle "$prompt"
        RESOLVED_ENGINE_BIN="$_bo"
        MODEL="$_mo"
        return
    fi
    case "$ENGINE" in
        claude)
            run_claude_cycle "$prompt"
            # Codex fallback: if Claude is usage-limited and a codex fallback is
            # configured, re-run the SAME cycle on Codex so the company keeps
            # working. run_codex_cycle overwrites OUTPUT/EXIT_CODE/etc., so the
            # rest of the loop evaluates the Codex result transparently.
            if [ "$FALLBACK_ENGINE" = "codex" ] && check_usage_limit "$OUTPUT"; then
                if [ -z "$RESOLVED_CODEX_BIN" ]; then
                    RESOLVED_CODEX_BIN="$(resolve_codex_bin 2>/dev/null || true)"
                fi
                if [ -n "$RESOLVED_CODEX_BIN" ]; then
                    log "Cycle #$loop_count [FALLBACK] Claude usage-limited — retrying on Codex"
                    local _saved_bin="$RESOLVED_ENGINE_BIN" _saved_model="$MODEL"
                    RESOLVED_ENGINE_BIN="$RESOLVED_CODEX_BIN"
                    MODEL="$CODEX_MODEL"   # empty -> codex config.toml default (gpt-5.6-sol)
                    run_codex_cycle "$prompt"
                    RESOLVED_ENGINE_BIN="$_saved_bin"
                    MODEL="$_saved_model"
                    FALLBACK_USED=1
                else
                    log "Cycle #$loop_count [FALLBACK] requested but codex binary not found"
                fi
            fi
            ;;
        codex)
            # Primary Codex engine: MODEL holds the CLAUDE model (e.g. haiku) for
            # Claude cycles; it must NOT be passed to codex. Swap to CODEX_MODEL
            # (empty -> codex config.toml default gpt-5.6-sol) for this run.
            local _mo="$MODEL"
            MODEL="$CODEX_MODEL"
            run_codex_cycle "$prompt"
            MODEL="$_mo"
            ;;
        *)
            echo "Error: Unsupported ENGINE '$ENGINE'" >&2
            return 1
            ;;
    esac
}

extract_cycle_metadata() {
    RESULT_TEXT=""
    CYCLE_COST="N/A"
    CYCLE_SUBTYPE="unknown"
    CYCLE_TYPE="${ENGINE}_exec"

    if [ "$ENGINE" = "claude" ]; then
        if command -v jq >/dev/null 2>&1; then
            RESULT_TEXT=$(echo "$RESULT_MESSAGE" | jq -r '.result // .message // .output_text // empty' 2>/dev/null | head -c 2000 || true)
            if [ -z "$RESULT_TEXT" ]; then
                RESULT_TEXT=$(echo "$RESULT_MESSAGE" | jq -r '.. | .text? // empty' 2>/dev/null | head -c 2000 || true)
            fi

            parsed_cost=$(echo "$RESULT_MESSAGE" | jq -r '.total_cost_usd // .cost_usd // empty' 2>/dev/null || true)
            if [ -n "$parsed_cost" ]; then
                CYCLE_COST="$parsed_cost"
            fi

            parsed_subtype=$(echo "$RESULT_MESSAGE" | jq -r '.subtype // empty' 2>/dev/null || true)
            if [ -n "$parsed_subtype" ]; then
                CYCLE_SUBTYPE="$parsed_subtype"
            fi

            parsed_type=$(echo "$RESULT_MESSAGE" | jq -r '.type // empty' 2>/dev/null || true)
            if [ -n "$parsed_type" ]; then
                CYCLE_TYPE="$parsed_type"
            fi
        fi

        if [ -z "$RESULT_TEXT" ]; then
            RESULT_TEXT=$(echo "$OUTPUT" | head -c 2000 || true)
        fi

        if [ "$CYCLE_SUBTYPE" = "unknown" ]; then
            if [ "$EXIT_CODE" -eq 0 ]; then
                CYCLE_SUBTYPE="success"
            else
                CYCLE_SUBTYPE="error"
            fi
        fi
        return
    fi

    RESULT_TEXT=$(echo "$RESULT_MESSAGE" | head -c 2000 || true)
    if [ -z "$RESULT_TEXT" ]; then
        RESULT_TEXT=$(echo "$OUTPUT" | head -c 2000 || true)
    fi

    if [ "$EXIT_CODE" -eq 0 ]; then
        CYCLE_SUBTYPE="success"
    else
        CYCLE_SUBTYPE="error"
    fi
}

# === Setup ===

mkdir -p "$LOG_DIR" "$PROJECT_DIR/memories"

# Clean up stale stop file from previous run
rm -f "$PROJECT_DIR/.auto-loop-stop"

# Check for existing instance
if [ -f "$PID_FILE" ]; then
    existing_pid=$(cat "$PID_FILE")
    if kill -0 "$existing_pid" 2>/dev/null; then
        echo "Auto loop already running (PID $existing_pid). Stop it first with ./stop-loop.sh"
        exit 1
    fi
fi

# Check dependencies
if ! RESOLVED_ENGINE_BIN="$(resolve_engine_bin)"; then
    if [ "$ENGINE" = "claude" ]; then
        echo "Error: Claude CLI not found. Install Claude Code in WSL and verify with 'claude --version'."
    else
        echo "Error: Codex CLI not found. Install Codex in WSL and verify with 'codex --version'."
    fi
    exit 1
fi

if [ ! -f "$PROMPT_FILE" ]; then
    echo "Error: PROMPT.md not found at $PROMPT_FILE"
    exit 1
fi

# Write PID file
echo $$ > "$PID_FILE"

# Trap signals for graceful shutdown
trap cleanup SIGTERM SIGINT SIGHUP

# Initialize counters
loop_count=0
error_count=0

log "=== Auto Company Loop Started (PID $$) ==="
log "Project: $PROJECT_DIR"
if [ "$ENGINE" = "codex" ]; then
    log "Engine: codex | Model: $MODEL_LABEL | Sandbox: $CODEX_SANDBOX_MODE"
else
    log "Engine: claude | Model: $MODEL_LABEL | PermissionMode: $CLAUDE_PERMISSION_MODE"
fi
log "Engine bin: $RESOLVED_ENGINE_BIN"
engine_version=$("$RESOLVED_ENGINE_BIN" --version 2>/dev/null | head -n1 || true)
case "$RESOLVED_ENGINE_BIN" in
    /mnt/c/*)
        if [ "$ENGINE" = "codex" ]; then
            log "Warning: Codex binary resolves to Windows-mounted path. Prefer WSL-local install for stability."
        else
            log "Warning: Claude binary resolves to Windows-mounted path. Prefer WSL-local install for stability."
        fi
        ;;
esac
if [ -n "$engine_version" ]; then
    if [ "$ENGINE" = "codex" ]; then
        log "Codex version: $engine_version"
    else
        log "Claude version: $engine_version"
    fi
fi
log "Interval: ${LOOP_INTERVAL}s | Timeout: ${CYCLE_TIMEOUT_SECONDS}s | Breaker: ${MAX_CONSECUTIVE_ERRORS} errors"
if [ -n "$FALLBACK_ENGINE" ]; then
    log "Fallback engine: $FALLBACK_ENGINE (on Claude usage limit)"
fi
if [ -n "$WINDOW_BUDGET_USD" ]; then
    log "Window budget: \$$WINDOW_BUDGET_USD per ${WINDOW_SECONDS}s (pause ${BUDGET_PAUSE_SECONDS}s when reached)"
fi
if [ "$ROUTER_ALTERNATE" = "1" ]; then
    log "Router: quota-aware alternation ON (Claude↔Codex when both have headroom; Codex limit ${CODEX_WINDOW_LIMIT:-∞}/window)"
else
    log "Router: single-engine (alternation OFF; Codex only on budget-cap/usage-limit)"
fi
if [ "$ROUTER_TIER_LADDER" = "1" ]; then
    log "Tier ladder: ON (round-robin) | Claude [$CLAUDE_TIER_LADDER] | Codex effort [$CODEX_TIER_LADDER]"
else
    log "Tier ladder: OFF (fixed Model: ${BASE_MODEL:-config-default}, Codex effort: ${BASE_CODEX_EFFORT:-default})"
fi

# === Main Loop ===

while true; do
    # Check for stop request
    if check_stop_requested; then
        log "Stop requested. Shutting down gracefully."
        cleanup
    fi

    # Quota-aware router: pick this cycle's engine from headroom in both ledgers
    # (Claude USD window + Codex count window), with optional alternation. Reserves
    # Claude-window headroom for the operator and keeps working on Codex when Claude
    # is capped, instead of pausing.
    select_cycle_engine
    [ -n "$CYCLE_ROUTER_MSG" ] && log "$CYCLE_ROUTER_MSG"
    if [ "$CYCLE_ROUTER_ACTION" = "pause" ]; then
        save_state "budget_paused"
        sleep "$BUDGET_PAUSE_SECONDS"
        continue
    fi

    # Tier ladder: pick this cycle's model/effort within the configured MIN..MAX range.
    apply_tier_ladder

    loop_count=$((loop_count + 1))
    cycle_log="$LOG_DIR/cycle-$(printf '%04d' "$loop_count")-$(date '+%Y%m%d-%H%M%S').log"

    log_cycle "$loop_count" "START" "Beginning work cycle"
    save_state "running"

    # Log rotation
    rotate_logs

    # Backup consensus before cycle
    backup_consensus
    gitignore_snapshot=$(snapshot_gitignore)

    # Build prompt with consensus pre-injected
    PROMPT=$(cat "$PROMPT_FILE")
    CONSENSUS=$(cat "$CONSENSUS_FILE" 2>/dev/null || echo "No consensus file found. This is the very first cycle.")
    FULL_PROMPT="$PROMPT

---

## Runtime Guardrails (must follow)

1. Early in the cycle, create or update \`memories/consensus.md\` with the required section skeleton.
2. If work scope is large, persist partial decisions to \`memories/consensus.md\` before deep dives.
3. Prefer shipping one completed milestone over broad parallel exploration.
4. Never write files via shell heredoc (\`cat <<EOF\`). Use \`apply_patch\` for file creates/edits.
5. Never execute shell lines that begin with \`>\` or \`>=\`; treat them as text and keep them inside markdown/files.

---

## Current Consensus (pre-loaded, do NOT re-read this file)

$CONSENSUS

---

This is Cycle #$loop_count. Act decisively."

    # Run selected engine in headless mode with per-cycle timeout
    run_engine_cycle "$FULL_PROMPT"

    # If this cycle ran on Codex and it hit a PERMANENT auth failure, disable Codex
    # for the rest of the process — otherwise alternation/fallback keep sending every
    # other cycle to a dead engine. Recovery needs a re-login + reseed (see APP-200).
    if { [ "$FALLBACK_USED" -eq 1 ] || [ "$CYCLE_ENGINE_OVERRIDE" = "codex" ] || [ "$ENGINE" = "codex" ]; } \
        && [ "$CODEX_DISABLED" != "1" ] && codex_auth_failed "$OUTPUT"; then
        CODEX_DISABLED=1
        log "[CODEX-AUTH-FAIL] Codex auth permanently rejected (rotated/consumed token) — disabling Codex for this run; re-login + reseed required"
    fi

    # Save full output to cycle log
    echo "$OUTPUT" > "$cycle_log"

    # Clean up known malformed-redirection artifacts created by bad generated shell commands.
    cleanup_accidental_root_artifacts
    restore_gitignore_if_changed "$gitignore_snapshot"

    # Extract result fields for status classification
    extract_cycle_metadata

    # Record spend into the rolling-window ledger — Claude cycles only. The budget
    # guards the operator's Claude quota; Codex (fallback or budget-offload) runs
    # on a separate quota, so as Claude entries age out the window frees and the
    # loop returns to Claude automatically.
    if [ "$FALLBACK_USED" -eq 1 ] || [ "$CYCLE_ENGINE_OVERRIDE" = "codex" ] || [ "$ENGINE" = "codex" ]; then
        # This cycle actually ran on Codex (fallback, budget-offload, or primary
        # engine) — meter its real token usage from the JSONL stream. Codex runs on a
        # separate quota, so it is intentionally NOT written to the Claude USD ledger.
        record_codex_usage "$OUTPUT"
    else
        record_spend "$CYCLE_COST"
    fi

    cycle_failed_reason=""
    cycle_soft_timeout=0
    if [ "$CYCLE_TIMED_OUT" -eq 1 ]; then
        if validate_consensus && consensus_changed_since_backup; then
            cycle_soft_timeout=1
        else
            cycle_failed_reason="Timed out after ${CYCLE_TIMEOUT_SECONDS}s"
        fi
    elif [ "$EXIT_CODE" -ne 0 ]; then
        cycle_failed_reason="Exit code $EXIT_CODE"
    elif ! validate_consensus; then
        cycle_failed_reason="consensus.md validation failed after cycle"
    fi

    if [ "$cycle_soft_timeout" -eq 1 ]; then
        log_cycle "$loop_count" "OK" "Timed out after ${CYCLE_TIMEOUT_SECONDS}s but consensus was updated; keeping progress (cost: ${CYCLE_COST}, subtype: ${CYCLE_SUBTYPE})"
        if [ -n "$RESULT_TEXT" ]; then
            log_cycle "$loop_count" "SUMMARY" "$(echo "$RESULT_TEXT" | head -c 300)"
        fi
        error_count=0
    elif [ -z "$cycle_failed_reason" ]; then
        log_cycle "$loop_count" "OK" "Completed (cost: ${CYCLE_COST}, subtype: ${CYCLE_SUBTYPE})"
        if [ -n "$RESULT_TEXT" ]; then
            log_cycle "$loop_count" "SUMMARY" "$(echo "$RESULT_TEXT" | head -c 300)"
        fi
        error_count=0
    else
        error_count=$((error_count + 1))
        log_cycle "$loop_count" "FAIL" "$cycle_failed_reason (cost: ${CYCLE_COST}, subtype: ${CYCLE_SUBTYPE}, errors: $error_count/$MAX_CONSECUTIVE_ERRORS)"

        # Restore consensus on hard failure
        restore_consensus

        # Check for usage limit
        if check_usage_limit "$OUTPUT"; then
            log_cycle "$loop_count" "LIMIT" "API usage limit detected. Waiting ${LIMIT_WAIT_SECONDS}s..."
            save_state "waiting_limit"
            sleep "$LIMIT_WAIT_SECONDS"
            error_count=0
            continue
        fi

        # Circuit breaker
        if [ "$error_count" -ge "$MAX_CONSECUTIVE_ERRORS" ]; then
            log_cycle "$loop_count" "BREAKER" "Circuit breaker tripped! Cooling down ${COOLDOWN_SECONDS}s..."
            save_state "circuit_break"
            sleep "$COOLDOWN_SECONDS"
            error_count=0
            log "Circuit breaker reset. Resuming..."
        fi
    fi

    save_state "idle"
    log_cycle "$loop_count" "WAIT" "Sleeping ${LOOP_INTERVAL}s before next cycle..."
    sleep "$LOOP_INTERVAL"
done
