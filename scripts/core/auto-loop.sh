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

# --- Locate silent `set -e` deaths (APP-240) --------------------------------
# The entrypoint's teardown now names THIS script as the child that exits rc=1
# during Codex-routed cycles, but a `set -e` exit prints nothing at all, so the
# failing command is still invisible. This trap records it. `set -E` is required
# for the ERR trap to be inherited into functions and subshells -- the failure is
# somewhere inside one, and without errtrace the trap would never fire there.
# Deliberately writes with printf rather than log(): log() is not defined yet at
# this point in the file, and a diagnostic that depends on later setup is exactly
# the kind of thing that fails when you need it.
# NOTE the wording: an ERR trap fires on ANY non-zero command under errtrace,
# including ones `set -e` tolerates (conditionals, subshells, guarded calls). It
# cannot know whether the shell is about to exit, so it must not claim it is.
# The first version said "exiting rc=..." and was immediately misleading on a
# harmless SIGPIPE. A diagnostic that lies is worse than no diagnostic — the
# whole point of APP-240 was that we could not trust what the logs told us.
set -E
trap '_erc=$?; printf "[%s] [ERR] rc=%s at line %s: %s\n" \
    "$(date "+%Y-%m-%d %H:%M:%S")" "$_erc" "$LINENO" "$BASH_COMMAND" \
    >> "$LOG_DIR/auto-loop.log" 2>/dev/null || true' ERR

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
BASE_CLAUDE_EFFORT="$CLAUDE_EFFORT"
BASE_CODEX_EFFORT="$CODEX_EFFORT"
RESOLVED_CODEX_BIN=""
FALLBACK_USED=0
CYCLE_ENGINE_OVERRIDE=""
# Set to 1 when a Codex run reports a PERMANENT auth failure (rotated/consumed
# refresh token). Codex is then treated as unavailable for the rest of this
# process so alternation/fallback don't burn every other cycle on a dead engine.
CODEX_DISABLED=0
# DEPRECATED (APP-263, 2026-07-30): WINDOW_BUDGET_USD and the APP-237 dynamic
# reserve cap (PLAN_CEILING_USD / OPERATOR_RESERVE_PCT / WINDOW_BUDGET_FLOOR_USD)
# are parsed ONLY to emit startup warnings — no gate reads them and they cannot
# override the four explicit APP-263 limits. The Claude gate is
# CLAUDE_5H_BUDGET_USD; operator interactive capacity is preserved by the
# Alternate routing policy and measured in the 14-day calibration report.
# Remove these variables from runtime.env after the migration period.
WINDOW_BUDGET_USD="${WINDOW_BUDGET_USD:-}"
PLAN_CEILING_USD="${PLAN_CEILING_USD:-}"
OPERATOR_RESERVE_PCT="${OPERATOR_RESERVE_PCT:-}"
WINDOW_BUDGET_FLOOR_USD="${WINDOW_BUDGET_FLOOR_USD:-}"
# operator-usage.json remains load-bearing: _window_anchor_epoch reads its
# blockStart to align both 5h gates to the real plan window.
OPERATOR_USAGE_FILE="${OPERATOR_USAGE_FILE:-$LOG_DIR/operator-usage.json}"
OPERATOR_USAGE_STALE_SECS="${OPERATOR_USAGE_STALE_SECS:-900}"
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
# Default cut 1800 -> 900 on 2026-07-28 (APP-238). Cache-read cost is SUPERLINEAR in
# cycle length -- every turn re-reads the whole (growing) context -- so a cycle that runs
# to the wall is the single biggest cost driver. The one cycle that actually reached the
# old 1800s wall did 145 turns / 19.2M cache-read tokens and cost $32.22, 88% of a whole
# $40 5h window; normal cycles finish in ~4 min, so 900s still leaves 3-4x headroom.
# DEPRECATED (APP-263, 2026-07-30): parsed ONLY to emit a startup warning; never
# read by any gate. Replaced by the four explicit gates below.
TOTAL_BUDGET_USD="${TOTAL_BUDGET_USD:-}"

# ── Four-gate budget model (APP-263 operator decision, 2026-07-30) ──────────────
# All four are HARD gates over API-equivalent/NOTIONAL usage (both engines are
# flat subscriptions; ccusage prices what the tokens would have cost — nothing
# here is billed cash). Empty = that gate disabled.
#  - per-engine 5h gates use each engine's existing plan-window anchor semantics
#    (_window_anchor_epoch — Claude's blockStart, shared, as before)
#  - DAILY is the UTC calendar day; WEEKLY is a rolling 7×24h period (no
#    calendar-week reset); a 5h rollover never resets either TOTAL
#  - one engine's rollover never alters the other engine's counter
CLAUDE_5H_BUDGET_USD="${CLAUDE_5H_BUDGET_USD:-}"
CODEX_5H_BUDGET_USD="${CODEX_5H_BUDGET_USD:-}"
TOTAL_DAILY_BUDGET_USD="${TOTAL_DAILY_BUDGET_USD:-}"
TOTAL_WEEKLY_BUDGET_USD="${TOTAL_WEEKLY_BUDGET_USD:-}"
# Cumulative ledger feeding DAILY/WEEKLY for Claude: `epoch engine run_id usd`,
# idempotent on run_id (a retry or crash-replay cannot charge a cycle twice),
# NEVER window-pruned — only 90-day retention. Codex DAILY/WEEKLY come from
# ccusage period totals instead (see _codex_spend_since), so codex rows are not
# appended here.
TOTAL_SPEND_LEDGER="$LOG_DIR/spend-total.log"
TOTAL_LEDGER_RETENTION_DAYS="${TOTAL_LEDGER_RETENTION_DAYS:-90}"
# Verified Opportunity-Analyst codex thread ids (`epoch thread_id` rows, deduped,
# persisted): excluded from company Codex 5h/DAILY/WEEKLY figures. Absent or
# unparseable ids are simply not excluded — fail closed in the budget-TIGHTENING
# direction (analyst counts toward the company when in doubt).
ANALYST_SESSIONS_FILE="$LOG_DIR/analyst-codex-sessions.log"
# Stable per-boot component of Claude run_ids (loop_count restarts at 1 on every
# container boot; this keeps run_ids unique across boots while staying identical
# across retries within one cycle).
LOOP_BOOT_ID="$(date +%s)-$$"
# Test hook: lets the gate tests pin "now" without faketime. NEVER set in prod.
BUDGET_NOW_OVERRIDE="${BUDGET_NOW_OVERRIDE:-}"
CYCLE_TIMEOUT_SECONDS="${CYCLE_TIMEOUT_SECONDS:-900}"
# An operator-escalated cycle (see apply_cycle_escalation) is deliberately allowed the
# old, longer wall: it is a human-approved, one-shot, expensive-on-purpose run.
ESCALATED_CYCLE_TIMEOUT_SECONDS="${ESCALATED_CYCLE_TIMEOUT_SECONDS:-1800}"
# Per-cycle effective wall, reset every cycle by apply_cycle_escalation.
CYCLE_TIMEOUT_ACTIVE="$CYCLE_TIMEOUT_SECONDS"
MAX_CONSECUTIVE_ERRORS="${MAX_CONSECUTIVE_ERRORS:-5}"
COOLDOWN_SECONDS="${COOLDOWN_SECONDS:-300}"
LIMIT_WAIT_SECONDS="${LIMIT_WAIT_SECONDS:-3600}"
MAX_LOGS="${MAX_LOGS:-200}"
AUTO_LOOP_PROTECT_GITIGNORE="${AUTO_LOOP_PROTECT_GITIGNORE:-1}"
RESOLVED_ENGINE_BIN=""

# --- Harness selection (jcode migration) ------------------------------------
# `cli`   = the historical path: `claude -p --output-format json` / `codex exec --json`.
# `jcode` = one Rust binary for BOTH providers: `jcode -p <provider> run --ndjson`.
# ENGINE still names the PROVIDER (claude|codex); this names the HARNESS that runs it,
# so the router, tier ladder, budget gates and fallback logic keep working unchanged.
# Rolling back is one variable — set LOOP_HARNESS=cli and restart; the CLIs stay in
# the image on purpose until jcode has a clean observation window.
LOOP_HARNESS="${LOOP_HARNESS:-cli}"
JCODE_BIN="${JCODE_BIN:-$(command -v jcode 2>/dev/null || echo /usr/local/bin/jcode)}"
# jcode's provider names differ from this loop's ENGINE names.
jcode_provider_for() { case "$1" in codex) echo openai ;; *) echo claude ;; esac; }
if [ "$LOOP_HARNESS" != "cli" ] && [ "$LOOP_HARNESS" != "jcode" ]; then
    echo "Error: LOOP_HARNESS must be 'cli' or 'jcode' (received: '$LOOP_HARNESS')."
    exit 1
fi

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
    # Match ONLY provider error signatures. The previous pattern matched bare
    # "billing", "quota", "429", "overloaded" and "rate limit" anywhere in the
    # cycle output — including the model's OWN prose. This company researches SaaS
    # pricing, so those words appear in normal successful cycles ("output quota",
    # "rate limits, webhooks", "native metering/billing substitute"), and every
    # such cycle was misread as usage-limited: needless Codex offloads and bogus
    # ceiling events. Keep these anchored to how the CLIs/API actually report it.
    if echo "$output" | grep -qiE 'usage limit reached|claude ai usage limit|rate_limit_error|resource_exhausted|429 too many requests|"status" *: *429|quota exceeded|exceeded your quota|insufficient credits|overloaded_error|upgrade to increase your usage limit'; then
        return 0
    fi
    return 1
}

# PERMANENT Codex auth failure (rotated/consumed/revoked refresh token, or a
# missing bearer). Distinct from a transient usage limit — retrying will not fix
# it; the operator must re-login and reseed. Used to disable Codex for the run.
# A PERMANENT codex auth rejection. BOTH conditions are required:
#   1. the engine actually failed (EXIT_CODE != 0), and
#   2. an auth-rejection phrase appears in its output.
# Condition 1 is not belt-and-braces, it is the whole correctness argument: $OUTPUT is
# the full JSONL transcript, which embeds every file the agent read or wrote. On
# 2026-07-29 a SUCCESSFUL Codex cycle (it rotated the Twilio SEND_SECRET, exit 0) was
# disabled for the rest of the run because a devops doc it authored quoted a Worker
# returning `401 unauthorized`. A cycle that completed its work did not have its
# credentials rejected — never decide this from transcript prose alone.
# Sets CODEX_AUTH_EVIDENCE to the matched fragment so the log says WHY.
codex_auth_failed() {
    local output="$1"
    CODEX_AUTH_EVIDENCE=""
    [ "${EXIT_CODE:-0}" -ne 0 ] || return 1
    # 124 is the watchdog timeout. A cycle killed at the wall clock says nothing
    # about credentials, and its transcript is long — i.e. maximally likely to
    # contain an unrelated "401 unauthorized" somewhere in a file it read.
    [ "${EXIT_CODE}" -ne 124 ] || return 1
    CODEX_AUTH_EVIDENCE=$(echo "$output" \
        | grep -oiE ".{0,60}(refresh token was already used|token_invalidated|invalid_grant|missing bearer|401 unauthorized|not logged in).{0,60}" \
        | head -1 || true)
    [ -n "$CODEX_AUTH_EVIDENCE" ]
}

# The brakes that must be present in every assembled prompt. Each is a section
# heading the company is required to obey, chosen because losing one is silent:
# the prompt still assembles, the cycle still runs, and the only symptom is the
# company doing something it should have been stopped from doing.
#
# Match on the HEADING TEXT, not on a whole line — headings get reworded. If a
# rename is deliberate, update this list in the same commit; that is the point,
# it forces the edit to be conscious.
REQUIRED_PROMPT_GUARDRAILS=(
    "HARD STOP — no build before willingness-to-pay evidence"
    "OPERATOR ESCALATION — deterministic request ledger (OPREQ)"
    "EXTERNAL ADJUDICATION — when the company must not rule on itself"
    "EXTERNAL-SYSTEM WRITE AUTHORITY"
    # The tender-track gates. These spent weeks living only in the single-slot
    # human-directive.md, surviving each rewrite only because whoever wrote the next
    # directive remembered to retype them; a 2026-07-29 check found seven of them in
    # no standing file at all. Anchored here so their disappearance is loud.
    "TENDER TRACK STANDING RULES"
    # The rule that stops a directive from becoming the only home of a rule.
    "DIRECTIVE AUTHORITY AND PERSISTENCE"
)

# Gates that were MOVED OUT of the every-cycle prompt (2026-07-29) and now live in
# PROJECT_EVALUATION_FRAMEWORK.md. Moving them saved prefix tokens and cost the
# invariant its view of them — the assembled prompt only carries a pointer now. So
# the check follows them: the file must exist and still contain both anchors. A
# pointer to a section someone deleted, emptied or renamed is worse than no pointer,
# because it reads as a live rule and enforces nothing.
REQUIRED_FRAMEWORK_ANCHORS=(
    "SEARCH REGIME"
    "Fırsat kaydı ve tarama dedup"
)

# True when every required guardrail survived into the assembled prompt AND the
# gates delegated to the framework file are still really there.
# Sets MISSING_GUARDRAILS to whatever did not.
prompt_guardrails_intact() {
    local assembled="$1" g fw pf
    MISSING_GUARDRAILS=""
    pf="$PROJECT_DIR/PROMPT.md"
    for g in "${REQUIRED_PROMPT_GUARDRAILS[@]}"; do
        # TWO checks, and the first is the one that matters. $assembled embeds
        # $CONSENSUS verbatim, and memories/consensus.md is rewritten by the model
        # every cycle — so a cycle that happened to write "TENDER TRACK STANDING
        # RULES" into its own consensus would satisfy an assembled-text-only check
        # even with the section deleted from PROMPT.md. The law has to be checked
        # where the law lives. (Caught by an independent adjudicator on 2026-07-29,
        # hours after the assembled-only version shipped; it was latent, not live.)
        if [ ! -s "$pf" ] || ! grep -qF -- "$g" "$pf"; then
            MISSING_GUARDRAILS="${MISSING_GUARDRAILS:+$MISSING_GUARDRAILS; }PROMPT.md: $g"
            continue
        fi
        # Still verify assembly did not drop it on the way into the prompt.
        case "$assembled" in
            *"$g"*) ;;
            *) MISSING_GUARDRAILS="${MISSING_GUARDRAILS:+$MISSING_GUARDRAILS; }assembly dropped: $g" ;;
        esac
    done
    fw="$PROJECT_DIR/PROJECT_EVALUATION_FRAMEWORK.md"
    if [ ! -s "$fw" ]; then
        MISSING_GUARDRAILS="${MISSING_GUARDRAILS:+$MISSING_GUARDRAILS; }PROJECT_EVALUATION_FRAMEWORK.md missing or empty"
    else
        for g in "${REQUIRED_FRAMEWORK_ANCHORS[@]}"; do
            grep -qF -- "$g" "$fw" || \
                MISSING_GUARDRAILS="${MISSING_GUARDRAILS:+$MISSING_GUARDRAILS; }framework anchor: $g"
        done
    fi
    [ -z "$MISSING_GUARDRAILS" ]
}

# Did human-directive.md change without the writer? Fail closed if so.
#
# NAMING RULE (operator-mandated, 2026-07-29): this is an ACCIDENTAL/DIRECT-WRITE
# TRIPWIRE, never a "fail-closed security boundary". The loop, the dashboard and
# the writer all run as `app` and the file, this ledger and this very script are
# `app`-writable, so the autonomous model can bypass or forge all of it — measured,
# and it succeeded. A Telegram notification is not a privilege separation. The real
# fix is ownership (separate UID / narrow socket with no override operation) and it
# is NOT built. What this tripwire does do: catch accidental or unaudited direct
# writes and refuse to run a cycle on top of them until a human looks.
#
# Mandated semantics, all fail-closed with NO self-repair:
#   - audit ledger absent/empty  -> BLOCKED. Never seed a baseline from live
#     content: an agent (or an accident) that deletes the ledger must not be able
#     to bless whatever the file happens to contain. Baseline creation is
#     operator-only, via the HOST-side channel (autocompany-deploy/scripts/
#     directive-baseline.sh), against a previously known trusted hash.
#   - live file absent/unreadable -> BLOCKED (a vanished directive is an
#     unaudited change, not a pass).
#   - live hash != the LAST writer-recorded resulting hash -> BLOCKED. Matching
#     against *any* historical entry would let a silent rollback to an old
#     audited content pass; only the most recent resulting state counts.
#     Refused actions log after_sha=- and are skipped when finding that state.
directive_unaudited() {
    local f="$PROJECT_DIR/memories/human-directive.md"
    local audit="$PROJECT_DIR/memories/directive-audit.log"
    DIRECTIVE_AUDIT_DETAIL=""
    if [ ! -s "$audit" ]; then
        DIRECTIVE_AUDIT_DETAIL="audit ledger absent or empty — operator must baseline via the host-side channel (directive-baseline.sh); the loop never seeds one"
        return 0
    fi
    if [ ! -f "$f" ]; then
        DIRECTIVE_AUDIT_DETAIL="human-directive.md is MISSING while the audit ledger exists — a vanished directive is an unaudited change"
        return 0
    fi
    local live last
    live=$(sha256sum "$f" 2>/dev/null | cut -c1-16)
    if [ -z "$live" ]; then
        DIRECTIVE_AUDIT_DETAIL="could not hash human-directive.md — refusing on an unreadable state"
        return 0
    fi
    last=$(grep -o 'after_sha=[0-9a-f]\{16\}' "$audit" | tail -1 | cut -d= -f2)
    if [ -z "$last" ]; then
        DIRECTIVE_AUDIT_DETAIL="audit ledger holds no resulting-state entry — operator baseline required"
        return 0
    fi
    [ "$live" = "$last" ] && return 1
    DIRECTIVE_AUDIT_DETAIL="live=$live != last writer-recorded state $last in directive-audit.log"
    return 0
}

_budget_now() { echo "${BUDGET_NOW_OVERRIDE:-$(date +%s)}"; }

# Start of the current UTC calendar day (DAILY gate anchor).
_utc_day_start() {
    local now
    now="$(_budget_now)"
    echo $(( now - (now % 86400) ))
}

_fmt_utc() {
    date -u -d "@$1" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null \
        || date -u -r "$1" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null \
        || echo "epoch $1"
}

# Append a cycle's cost to the rolling-window ledger (skips 0 / N/A) AND to the
# cumulative TOTAL ledger, idempotently.
record_spend() {
    local cost="$1"
    case "$cost" in ''|N/A|0|0.0) return 0 ;; esac
    printf '%s %s\n' "$(date +%s)" "$cost" >> "$SPEND_LEDGER" 2>/dev/null || true
    record_total_spend "claude" "${LOOP_BOOT_ID}-c${loop_count:-0}" "$cost"
}

# `epoch engine run_id usd` — refuses a duplicate run_id, so a retry, crash
# recovery or repeated record_spend() call charges each cycle exactly once
# across every period the ledger feeds (DAILY and WEEKLY alike).
record_total_spend() {
    local engine="$1" run_id="$2" usd="$3"
    if [ -f "$TOTAL_SPEND_LEDGER" ] \
       && awk -v r="$run_id" '$3 == r { found=1; exit } END { exit !found }' "$TOTAL_SPEND_LEDGER" 2>/dev/null; then
        return 0
    fi
    printf '%s %s %s %s\n' "$(_budget_now)" "$engine" "$run_id" "$usd" >> "$TOTAL_SPEND_LEDGER" 2>/dev/null || true
    # Retention prune (90d default) — enough history for the rolling 7-day gate
    # and for auditing previous periods, per APP-263.
    local cutoff
    cutoff=$(( $(_budget_now) - TOTAL_LEDGER_RETENTION_DAYS * 86400 ))
    awk -v c="$cutoff" '$1 >= c' "$TOTAL_SPEND_LEDGER" > "$TOTAL_SPEND_LEDGER.tmp" 2>/dev/null \
        && mv "$TOTAL_SPEND_LEDGER.tmp" "$TOTAL_SPEND_LEDGER" 2>/dev/null || true
}

# Codex notional spend since an epoch, from the cumulative ledger. Only the jcode
# harness writes codex rows here; on the CLI path this is legitimately 0 and the
# ccusage figure is the real one. Callers take the MAX of the two so a mixed window
# (some CLI cycles, some jcode cycles) can never read lower than either source alone —
# a budget reader that under-counts is not a brake.
codex_ledger_spend_since() {
    [ -f "$TOTAL_SPEND_LEDGER" ] || { echo "0.0000"; return; }
    awk -v c="$1" '$1 >= c && $2 == "codex" { s += $4 } END { printf "%.4f", s + 0 }' \
        "$TOTAL_SPEND_LEDGER" 2>/dev/null || echo "0.0000"
}

_max_usd() { awk -v a="$1" -v b="$2" 'BEGIN { printf "%.4f", (a+0 > b+0 ? a+0 : b+0) }'; }

# Claude notional spend since an epoch, from the cumulative ledger.
claude_spend_since() {
    [ -f "$TOTAL_SPEND_LEDGER" ] || { echo "0.0000"; return; }
    awk -v c="$1" '$1 >= c && $2 == "claude" { s += $4 } END { printf "%.4f", s + 0 }' \
        "$TOTAL_SPEND_LEDGER" 2>/dev/null || echo "0.0000"
}

# Sum spend within the last WINDOW_SECONDS, pruning older entries. Echoes USD.
# The instant the current plan window starts. Extracted so the Claude cap and the
# combined TOTAL cap can never disagree about where the window begins — two
# independent copies of this logic drifting apart is exactly the kind of bug that
# makes a budget guard silently wrong.
_window_anchor_epoch() {
    local now cutoff anchor
    now=$(_budget_now)
    cutoff=$((now - WINDOW_SECONDS))
    if [ -f "$OPERATOR_USAGE_FILE" ] \
       && [ $(( now - $(stat -c %Y "$OPERATOR_USAGE_FILE" 2>/dev/null || echo 0) )) -le "$OPERATOR_USAGE_STALE_SECS" ]; then
        anchor=$(jq -r '.blockStart // empty' "$OPERATOR_USAGE_FILE" 2>/dev/null || true)
        if [ -n "$anchor" ]; then
            anchor=$(date -u -d "$anchor" +%s 2>/dev/null || echo "")
            if [ -n "$anchor" ] && [ "$anchor" -gt "$cutoff" ] 2>/dev/null; then
                cutoff="$anchor"
            fi
        fi
    fi
    echo "$cutoff"
}

# Codex USD inside the CURRENT plan window, priced by ccusage — the same tool that
# already prices Claude, so the two figures are in the same currency and can be
# added. Codex bills against a ChatGPT subscription rather than per token, so this
# is API-equivalent/NOTIONAL cost — the currency every APP-263 gate speaks.
# ~380ms over 794 sessions, i.e. cheap enough for once per cycle.
# Prints TWO fields: "<usd> <stale 0|1>". Deliberately not a global flag --
# callers use this inside $( ), which is a subshell, so a global set in here would
# never reach the caller and the STALE warning would silently never fire. Caught
# by tests/test_total_budget.sh before it shipped.
CODEX_SPEND_CACHE="$LOG_DIR/.codex-spend-cache"

# Codex notional USD since an anchor epoch, from ccusage period totals (never
# per-cycle appended estimates — APP-263). Analyst sessions whose VERIFIED
# thread_id (from ANALYST_SESSIONS_FILE) appears in the ccusage sessionFile are
# excluded; a session with missing/ambiguous metadata is INCLUDED — the
# exclusion fails closed in the budget-tightening direction.
#
# $2 is a per-gate cache key (5h|daily|weekly): a STALE/failed refresh falls
# back to that gate's LAST SUCCESSFUL measurement, so a failure can never
# reduce an already-observed total. (A fresh SUCCESSFUL read may legitimately
# be lower — a 5h window roll, or weekly spend aging out — that is a real
# period change, not a stale reduction.)
# Prints "<usd> <stale 0|1>". Subshell-safe, same as before.
_codex_spend_since() {
    local anchor="$1" key="${2:-5h}" out cache
    cache="$CODEX_SPEND_CACHE-$key"
    out="$(CODEX_HOME="${CODEX_HOME:-$LOG_DIR/.codex}" ccusage codex session --json 2>/dev/null \
        | python3 -c '
import json, sys, datetime, os, re
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(1)
anchor = int(sys.argv[1])
excl = set()
try:
    with open(sys.argv[2], encoding="utf-8") as fh:
        for line in fh:
            parts = line.split()
            if len(parts) >= 2 and re.fullmatch(r"[0-9a-fA-F-]{36}", parts[1]):
                excl.add(parts[1].lower())
except Exception:
    excl = set()  # unreadable exclusion file -> exclude nothing (tightening)
total = 0.0
for s in d.get("sessions", []):
    la = s.get("lastActivity")
    if not la:
        continue
    try:
        e = int(datetime.datetime.fromisoformat(la.replace("Z", "+00:00")).timestamp())
    except Exception:
        continue
    # lastActivity is the sessions END, so a session straddling the anchor is
    # counted in full. That over-counts, which is the safe direction for a cap.
    if e < anchor:
        continue
    sf = (s.get("sessionFile") or "").lower()
    if sf and any(t in sf for t in excl):
        continue  # verified analyst session
    total += float(s.get("costUSD") or 0)
print("%.4f" % total)
' "$anchor" "$ANALYST_SESSIONS_FILE" 2>/dev/null || true)"
    if [ -n "$out" ]; then
        printf '%s' "$out" > "$cache" 2>/dev/null || true
        printf '%s 0' "$out"
        return 0
    fi
    # Measurement failed. Fall back to this gate's last known value rather than
    # printing 0 — reporting zero would quietly switch the gate off, which is
    # the one failure mode a budget guard must never have.
    printf '%s 1' "$(cat "$cache" 2>/dev/null || echo "0")"
    return 0
}

# Per-session "epoch usd" pairs since an anchor (analyst-excluded) — used to
# compute the WEEKLY gate's exact spend-expiry resume time. Prints nothing on
# ccusage failure (callers then fall back to a conservative estimate).
_codex_spend_entries_since() {
    local anchor="$1"
    CODEX_HOME="${CODEX_HOME:-$LOG_DIR/.codex}" ccusage codex session --json 2>/dev/null \
        | python3 -c '
import json, sys, datetime, re
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(1)
anchor = int(sys.argv[1])
excl = set()
try:
    with open(sys.argv[2], encoding="utf-8") as fh:
        for line in fh:
            parts = line.split()
            if len(parts) >= 2 and re.fullmatch(r"[0-9a-fA-F-]{36}", parts[1]):
                excl.add(parts[1].lower())
except Exception:
    excl = set()
for s in d.get("sessions", []):
    la = s.get("lastActivity")
    if not la:
        continue
    try:
        e = int(datetime.datetime.fromisoformat(la.replace("Z", "+00:00")).timestamp())
    except Exception:
        continue
    if e < anchor:
        continue
    sf = (s.get("sessionFile") or "").lower()
    if sf and any(t in sf for t in excl):
        continue
    print("%d %.6f" % (e, float(s.get("costUSD") or 0)))
' "$anchor" "$ANALYST_SESSIONS_FILE" 2>/dev/null || true
}

# Earliest UTC epoch at which the rolling 7-day total drops below the WEEKLY
# limit: walk contributing entries (Claude ledger rows + Codex sessions) oldest
# first; each expires 7×24h after its own timestamp — entry-by-entry, never at a
# calendar-week boundary.
_weekly_resume_epoch() {
    local week_anchor="$1" limit="$2"
    {
        [ -f "$TOTAL_SPEND_LEDGER" ] \
            && awk -v c="$week_anchor" '$1 >= c && $2 == "claude" { print $1, $4 }' "$TOTAL_SPEND_LEDGER" 2>/dev/null
        _codex_spend_entries_since "$week_anchor"
    } | sort -n | awk -v limit="$limit" '
        { epoch[NR] = $1; cost[NR] = $2; total += $2 }
        END {
            if (NR == 0 || total < limit) { print 0; exit }
            for (i = 1; i <= NR; i++) {
                total -= cost[i]
                if (total < limit) { print epoch[i] + 604800; exit }
            }
            print epoch[NR] + 604800
        }'
}

window_spend() {
    [ -f "$SPEND_LEDGER" ] || { echo "0"; return; }
    local now cutoff
    now=$(date +%s)
    cutoff=$((now - WINDOW_SECONDS))
    # Prune on the rolling cutoff (this ledger's own retention)...
    awk -v c="$cutoff" '$1 >= c' "$SPEND_LEDGER" > "$SPEND_LEDGER.tmp" 2>/dev/null \
        && mv "$SPEND_LEDGER.tmp" "$SPEND_LEDGER" 2>/dev/null || true

    # ...but SUM from the operator's plan-window anchor when we know it. The plan's
    # quota resets at a fixed instant while this ledger rolls, so right after a reset
    # the rolling window still carries pre-reset spend: the loop would read itself as
    # a third full against a plan that is actually empty, and downgrade the model for
    # no reason. blockStart comes from `ccusage blocks --active` via the reporter.
    # Shared with codex_window_spend() via _window_anchor_epoch() so the Claude cap
    # and the TOTAL cap can never disagree about where the window starts.
    cutoff="$(_window_anchor_epoch)"

    awk -v c="$cutoff" '$1 >= c {s += $2} END {printf "%.4f", s + 0}' "$SPEND_LEDGER" 2>/dev/null || echo "0"
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

# Tier ladder (APP-193, FILL-WEIGHTED): pick the Claude MODEL + Codex effort from their
# CHEAPEST-FIRST ladders by how full each rolling window is — the most-capable tier while
# the window is fresh, downgrading toward the cheapest tier as it fills (this is the
# quota-weighted design; it replaces the earlier plain round-robin). Claude fill = 5h USD
# spend / CLAUDE_5H_BUDGET_USD; Codex fill = window count / CODEX_WINDOW_LIMIT. When a provider
# has NO cap set, there is no fill signal → stay at the cheapest tier (conservative). When
# the ladder is off, restore the base config. The chosen engine reads MODEL / CODEX_EFFORT.
apply_tier_ladder() {
    if [ "$ROUTER_TIER_LADDER" != "1" ]; then
        MODEL="$BASE_MODEL"
        CLAUDE_EFFORT="$BASE_CLAUDE_EFFORT"
        CODEX_EFFORT="$BASE_CODEX_EFFORT"
        MODEL_LABEL="${MODEL:-config-default}"
        # This always computes the CLAUDE pick, even on a Codex cycle — see the
        # matching note below. Cockpit MODEL must reflect what actually ran.
        if [ "${CYCLE_ENGINE_OVERRIDE:-$ENGINE}" = "codex" ]; then
            MODEL_LABEL="${CODEX_MODEL:-codex-default}:${CODEX_EFFORT}"
        fi
        return 0
    fi

    # _tier_pick <fill_num> <fill_den> <csv, cheapest-first> → echoes the chosen tier.
    # index = (n-1) - floor(fill*n), clamped; fill = num/den. den<=0 → cheapest (index 0).
    _tier_pick() {
        local num="$1" den="$2" csv="$3" arr n idx
        IFS=',' read -ra arr <<< "$csv"
        n=${#arr[@]}
        [ "$n" -eq 0 ] && { printf ''; return; }
        idx="$(awk -v x="$num" -v d="$den" -v n="$n" 'BEGIN{
            if (d+0 <= 0) { print 0; exit }
            s = int((x / d) * n); if (s < 0) s = 0; if (s > n-1) s = n-1;
            print (n-1) - s
        }')"
        printf '%s' "$(printf '%s' "${arr[$idx]}" | tr -d '[:space:]')"
    }

    local c_num c_den x_num x_den m e
    c_num="$(window_spend)";       c_den="${CLAUDE_5H_BUDGET_USD:-0}"
    x_num="$(codex_window_count)"; x_den="${CODEX_WINDOW_LIMIT:-0}"
    # A ladder rung may carry its own reasoning effort as `model:effort` (APP-241).
    # Without it the ladder only ever moved the MODEL while CLAUDE_EFFORT stayed
    # pinned to whatever the environment set — in practice `low`, so opus never
    # actually thought. One combined quality ladder keeps model and effort coherent:
    # a full window can't land on haiku-at-high, and an empty one runs opus properly.
    m="$(_tier_pick "$c_num" "$c_den" "$CLAUDE_TIER_LADDER")"
    e="$(_tier_pick "$x_num" "$x_den" "$CODEX_TIER_LADDER")"
    if [ -n "$m" ]; then
        case "$m" in
            *:*)
                CLAUDE_EFFORT="${m##*:}"
                MODEL="${m%%:*}"
                ;;
            *)  MODEL="$m"
                # No effort on this rung: restore the configured baseline rather than
                # inheriting whatever a previous rung set, or the ladder would leak a
                # high effort downward into a cheap model.
                CLAUDE_EFFORT="$BASE_CLAUDE_EFFORT"
                ;;
        esac
        MODEL_LABEL="${MODEL:-config-default}"
    fi
    [ -n "$e" ] && CODEX_EFFORT="$e"
    log "[TIER] fill-weighted → Claude=$MODEL effort=${CLAUDE_EFFORT:-default} [claude \$$c_num/${CLAUDE_5H_BUDGET_USD:-∞}], Codex effort=$CODEX_EFFORT [codex $x_num/${CODEX_WINDOW_LIMIT:-∞}]"
    # The block above always computes the CLAUDE-ladder pick, even when this cycle
    # will actually run on Codex — MODEL_LABEL otherwise shows e.g. "claude-opus-4-8"
    # in the cockpit/state file for a cycle that never touched Claude at all
    # (found 2026-07-25: operator read ENGINE=codex + MODEL=claude-opus-4-8 in
    # /api/status and reasonably concluded the engine switch hadn't taken effect).
    if [ "${CYCLE_ENGINE_OVERRIDE:-$ENGINE}" = "codex" ]; then
        MODEL_LABEL="${CODEX_MODEL:-codex-default}:${CODEX_EFFORT}"
    fi
}

# --- One-shot operator escalation (APP-238, 2026-07-28) ----------------------------
# The company runs on the cheap ladder by default. When the operator wants a single
# cycle done by the expensive model (e.g. approving a GO), they arm
# `ESCALATE_NEXT_CYCLE=claude-opus-5:high` in the cockpit Settings panel; the next
# eligible cycle uses it, and the loop CONSUMES it so it can never fire twice.
#
# Read straight from runtime.env rather than the environment: the loop's env is fixed
# at container boot, so an env-only read would need a restart to see the operator's
# edit -- which defeats the point of a one-shot approval.
_read_runtime_env_key() {
    local f="$LOG_DIR/runtime.env" k="$1"
    [ -f "$f" ] || return 0
    sed -n "s/^${k}=//p" "$f" 2>/dev/null | tail -1 | tr -d '\r'
}

# Remove the key from runtime.env. Line-oriented on purpose: the file is a flat
# KEY=value list (docker-entrypoint.sh parses it literally, never sources it), and
# dropping a key is exactly how dashboard/server.py represents "blank = default".
_consume_escalation() {
    local f="$LOG_DIR/runtime.env" tmp
    [ -f "$f" ] || return 0
    tmp="$(mktemp)" || return 0
    if grep -v '^ESCALATE_NEXT_CYCLE=' "$f" > "$tmp" 2>/dev/null; then
        cat "$tmp" > "$f" 2>/dev/null || true   # preserve inode/ownership
    fi
    rm -f "$tmp" 2>/dev/null || true
}

# Sets MODEL / CLAUDE_EFFORT / CYCLE_TIMEOUT_ACTIVE for THIS cycle only. Must run
# AFTER apply_tier_ladder (it deliberately overrides the ladder's pick) and AFTER
# select_cycle_engine (it refuses to burn an escalation on a Codex cycle).
ESCALATION_USED=""
apply_cycle_escalation() {
    CYCLE_TIMEOUT_ACTIVE="$CYCLE_TIMEOUT_SECONDS"
    ESCALATION_USED=""
    local esc
    esc="$(_read_runtime_env_key ESCALATE_NEXT_CYCLE)"
    [ -n "$esc" ] || return 0

    # Two refusals, both LEAVE THE ESCALATION ARMED rather than silently burning it:
    # an approval the operator paid attention to should not be spent on a cycle they
    # did not mean. Both are logged every cycle so an armed escalation is never invisible.
    if [ "${CYCLE_ENGINE_OVERRIDE:-$ENGINE}" = "codex" ]; then
        log "[ESCALATE] armed ($esc) but this cycle routed to Codex — left armed, not consumed"
        return 0
    fi
    if ! _directive_is_pending; then
        log "[ESCALATE] armed ($esc) but human-directive.md is not PENDING — left armed, not consumed"
        return 0
    fi

    case "$esc" in
        *:*) MODEL="${esc%%:*}"; CLAUDE_EFFORT="${esc##*:}" ;;
        *)   MODEL="$esc" ;;
    esac
    MODEL_LABEL="${MODEL:-config-default}"
    CYCLE_TIMEOUT_ACTIVE="$ESCALATED_CYCLE_TIMEOUT_SECONDS"
    ESCALATION_USED="$esc"
    _consume_escalation
    log "[ESCALATE] one-shot '$esc' CONSUMED — model=$MODEL effort=${CLAUDE_EFFORT:-default} timeout=${CYCLE_TIMEOUT_ACTIVE}s"
    # Notify unconditionally: nothing else in the system is model-proof (the cycle runs
    # with a full shell), so the operator seeing every escalation that fires is the real
    # control, exactly as with the OPREQ ledger's notify-on-escalation rule.
    if [ -n "${TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${TELEGRAM_CHAT_ID:-}" ]; then
        bash "$SCRIPT_DIR/telegram-notify.sh" "⬆️ Escalated cycle: $esc (one-shot, consumed).
Timeout ${CYCLE_TIMEOUT_ACTIVE}s. If you did not arm this, the escalation was set from inside the container." \
            >/dev/null 2>&1 || true
    fi
}

# APP-189 Phase 2 — decide which engine runs THIS cycle from remaining quota headroom
# in both ledgers, with optional per-cycle alternation. Sets globals:
#   CYCLE_ENGINE_OVERRIDE : "" (use primary ENGINE / Claude) or "codex"
#   CYCLE_ROUTER_ACTION   : "run" | "pause"
#   CYCLE_ROUTER_MSG      : human-readable reason for the caller to log
# With ROUTER_ALTERNATE=0 this reproduces the prior budget gate exactly: under
# budget -> primary; over budget -> Codex if available, else pause.
# --- stall detection (APP-242) -------------------------------------------------
# On 2026-07-25 cycles 147-157 ran for two hours and left NOTHING behind: no research
# artifact, no registry change. They re-verified a blocked candidate and stopped there,
# burning ~$5. A new human directive at 08:53 restored output on the very next cycle.
#
# The reliable signal is not what a cycle SAYS but whether it left anything behind, so
# the check is a fingerprint over the research artifacts + the candidate registry. It
# only WARNS: writing directives stays with the operator (the Codex second-brain's own
# scope says it never applies one). A stall episode notifies once, not every cycle.
STALL_THRESHOLD_CYCLES="${STALL_THRESHOLD_CYCLES:-3}"
STALL_STATE_FILE="$LOG_DIR/stall-state"
RESEARCH_DIR="$PROJECT_DIR/docs/research"
CANDIDATE_REGISTRY="$PROJECT_DIR/memories/candidate-registry.md"
STALL_DRAFT_FILE="$PROJECT_DIR/memories/stall-directive-draft.md"

# POSIX only, deliberately: an earlier version used `ls --time-style` and `stat -c`,
# which silently produce nothing where those GNU flags are absent. The fingerprint
# then never changes and EVERY cycle looks stalled — a detector that cries wolf is
# worse than none. Echoes nothing when it cannot measure, and the caller skips.
_work_fingerprint() {
    [ -d "$RESEARCH_DIR" ] || return 0
    local files newest registry
    files=$(ls -1 "$RESEARCH_DIR" 2>/dev/null | wc -l | tr -d ' ')
    # `head -1` closes the pipe after one line, so `ls` takes SIGPIPE and pipefail
    # surfaces 141 every cycle. Harmless, but it fired the ERR trap on each pass.
    newest=$(ls -1t "$RESEARCH_DIR" 2>/dev/null | head -1 || true)
    registry=$(wc -c < "$CANDIDATE_REGISTRY" 2>/dev/null | tr -d ' ')
    printf '%s|%s|%s' "${files:-0}" "${newest:-none}" "${registry:-0}"
}

# A PENDING directive means the operator just gave the company something to do, so a
# quiet cycle is expected rather than a stall.
_directive_is_pending() {
    grep -A2 '^## Status' "$PROJECT_DIR/memories/human-directive.md" 2>/dev/null \
        | grep -qi 'PENDING'
}

check_stall() {
    local fp prev count notified
    fp="$(_work_fingerprint)"
    # Cannot measure ⇒ say nothing. Never infer a stall from a failed measurement.
    [ -n "$fp" ] || return 0
    prev=""; count=0; notified=0
    if [ -f "$STALL_STATE_FILE" ]; then
        prev=$(sed -n '1p' "$STALL_STATE_FILE" 2>/dev/null)
        count=$(sed -n '2p' "$STALL_STATE_FILE" 2>/dev/null)
        notified=$(sed -n '3p' "$STALL_STATE_FILE" 2>/dev/null)
    fi
    case "$count" in ''|*[!0-9]*) count=0 ;; esac
    case "$notified" in ''|*[!0-9]*) notified=0 ;; esac

    if [ "$fp" != "$prev" ]; then
        printf '%s\n0\n0\n' "$fp" > "$STALL_STATE_FILE" 2>/dev/null || true
        return 0
    fi

    count=$((count + 1))
    if [ "$count" -ge "$STALL_THRESHOLD_CYCLES" ] && [ "$notified" -eq 0 ] && ! _directive_is_pending; then
        log "[STALL] $count consecutive cycles produced no research artifact and no registry change — notifying the operator"
        _write_stall_draft "$count"
        bash "$SCRIPT_DIR/telegram-notify.sh" "⚠️ Auto-Company stalled: $count cycles in a row produced no new research artifact and no candidate-registry change.

The standing directive is marked DONE, so the company is re-verifying a blocked state instead of opening new ground. This is what burned ~\$5 over cycles 147-157 today.

A ready-to-apply directive draft is waiting in memories/stall-directive-draft.md — review it and apply via the cockpit if you agree. Nothing was changed automatically." >/dev/null 2>&1 || true
        notified=1
    fi
    printf '%s\n%s\n%s\n' "$fp" "$count" "$notified" > "$STALL_STATE_FILE" 2>/dev/null || true
}

# A draft for the OPERATOR to review — never applied automatically.
_write_stall_draft() {
    {
        echo "# Stall — directive draft (NOT applied)"
        echo
        echo "Generated $(date -u +%Y-%m-%dT%H:%M:%SZ) after $1 consecutive cycles with no"
        echo "research artifact and no candidate-registry change."
        echo
        echo "## What the company has been doing"
        grep -h 'SUMMARY' "$LOG_DIR/auto-loop.log" 2>/dev/null | tail -3 | cut -c1-220
        echo
        echo "## Current blocker (from consensus)"
        grep -A6 -i '^## Next Action' "$PROJECT_DIR/memories/consensus.md" 2>/dev/null | head -8
        echo
        echo "## Suggested directive — edit before applying"
        echo '```'
        echo "## Status"
        echo "PENDING"
        echo
        echo "## Directive"
        echo "The current hold is blocked on something only the operator can unblock, and"
        echo "re-verifying it every cycle produces nothing. Keep the hold, but stop spending"
        echo "cycles on it: check it at most once every 10 cycles."
        echo
        echo "Primary activity until the blocker clears: open genuinely NEW ground per"
        echo "PROMPT.md -> SEARCH REGIME. Each cycle must leave an artifact under"
        echo "docs/research/ or change memories/candidate-registry.md; a cycle that finds"
        echo "nothing must still record WHAT was searched and WHY it was killed, so the"
        echo "next cycle does not repeat it."
        echo '```'
    } > "$STALL_DRAFT_FILE" 2>/dev/null || true
}

# refresh_dynamic_budget (APP-237 reserve-% cap) was removed by APP-263: the four
# explicit gates replace it, and Alternate routing is the operator-capacity
# mechanism. See git history for the formula.

# Fire a gate-block Telegram once per (gate, period), not once per paused cycle.
# Keyed on the gate name + a period identity, so the next period notifies again.
_notify_gate_block_once() {
    local gate="$1" period_key="$2" message="$3" marker
    marker="$LOG_DIR/.gate-notified-$gate-$period_key"
    if [ -f "$marker" ]; then
        return 0
    fi
    : > "$marker" 2>/dev/null || true
    find "$LOG_DIR" -maxdepth 1 -name ".gate-notified-$gate-*" ! -name "*-$period_key" -delete 2>/dev/null || true
    if [ -n "${TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${TELEGRAM_CHAT_ID:-}" ]; then
        bash "$SCRIPT_DIR/telegram-notify.sh" "$message" >/dev/null 2>&1 || true
    fi
}

# ── Four-gate evaluation (APP-263) ─────────────────────────────────────────────
# Sets globals; emits the single unambiguous [BUDGET] status line. All figures
# are API-equivalent/NOTIONAL usage, never billed cash.
#   BG_CLAUDE5 BG_CODEX5 BG_DAILY BG_WEEKLY    — current notional spend
#   BG_CLAUDE_OK BG_CODEX_OK                   — per-engine 5h eligibility (1/0)
#   BG_TOTAL_GATE ("" | DAILY_TOTAL | WEEKLY_TOTAL)
#   BG_TOTAL_RESUME_EPOCH BG_5H_RESUME_EPOCH
evaluate_budget_gates() {
    local now anchor day_start week_start x5_raw xd_raw xw_raw x5_stale
    now="$(_budget_now)"
    anchor="$(_window_anchor_epoch)"
    day_start="$(_utc_day_start)"
    week_start=$(( now - 604800 ))

    BG_CLAUDE5="$(window_spend)"
    x5_raw="$(_codex_spend_since "$anchor" 5h)"
    BG_CODEX5="${x5_raw%% *}"; x5_stale="${x5_raw##* }"
    xd_raw="$(_codex_spend_since "$day_start" daily)"
    xw_raw="$(_codex_spend_since "$week_start" weekly)"
    # Take the higher of ccusage (CLI cycles) and the ledger (jcode cycles) for every
    # codex figure. Neither source sees the other's cycles, and a window can legally
    # contain both across a cutover or a rollback.
    local xd_usd xw_usd
    BG_CODEX5="$(_max_usd "$BG_CODEX5" "$(codex_ledger_spend_since "$anchor")")"
    xd_usd="$(_max_usd "${xd_raw%% *}" "$(codex_ledger_spend_since "$day_start")")"
    xw_usd="$(_max_usd "${xw_raw%% *}" "$(codex_ledger_spend_since "$week_start")")"
    BG_DAILY="$(awk -v a="$(claude_spend_since "$day_start")" -v b="$xd_usd" 'BEGIN { printf "%.4f", a + b }')"
    BG_WEEKLY="$(awk -v a="$(claude_spend_since "$week_start")" -v b="$xw_usd" 'BEGIN { printf "%.4f", a + b }')"

    local stale_note=""
    [ "$x5_stale" = "1" ] && stale_note=" (codex figures STALE — ccusage failed, last known values reused; a stale read never lowers an observed total)"
    log "[BUDGET] Claude 5h \$$BG_CLAUDE5/\$${CLAUDE_5H_BUDGET_USD:-∞} | Codex 5h \$$BG_CODEX5/\$${CODEX_5H_BUDGET_USD:-∞} | Daily TOTAL \$$BG_DAILY/\$${TOTAL_DAILY_BUDGET_USD:-∞} | Weekly TOTAL \$$BG_WEEKLY/\$${TOTAL_WEEKLY_BUDGET_USD:-∞}$stale_note"

    _budget_ge() { awk -v s="$1" -v b="$2" 'BEGIN { exit !(s + 0 >= b + 0) }'; }

    BG_TOTAL_GATE=""; BG_TOTAL_RESUME_EPOCH=0
    if [ -n "$TOTAL_DAILY_BUDGET_USD" ] && _budget_ge "$BG_DAILY" "$TOTAL_DAILY_BUDGET_USD"; then
        BG_TOTAL_GATE="DAILY_TOTAL"
        BG_TOTAL_RESUME_EPOCH=$(( day_start + 86400 ))
    elif [ -n "$TOTAL_WEEKLY_BUDGET_USD" ] && _budget_ge "$BG_WEEKLY" "$TOTAL_WEEKLY_BUDGET_USD"; then
        BG_TOTAL_GATE="WEEKLY_TOTAL"
        BG_TOTAL_RESUME_EPOCH="$(_weekly_resume_epoch "$week_start" "$TOTAL_WEEKLY_BUDGET_USD")"
        # ccusage failure during the walk yields a Claude-only estimate; never
        # report an epoch in the past for a gate that is currently closed.
        [ "$BG_TOTAL_RESUME_EPOCH" -le "$now" ] 2>/dev/null && BG_TOTAL_RESUME_EPOCH=$(( now + BUDGET_PAUSE_SECONDS ))
    fi

    BG_CLAUDE_OK=1; BG_CODEX_OK=1
    if [ -n "$CLAUDE_5H_BUDGET_USD" ] && _budget_ge "$BG_CLAUDE5" "$CLAUDE_5H_BUDGET_USD"; then
        BG_CLAUDE_OK=0
    fi
    if [ -n "$CODEX_5H_BUDGET_USD" ] && _budget_ge "$BG_CODEX5" "$CODEX_5H_BUDGET_USD"; then
        BG_CODEX_OK=0
    fi
    # Both 5h gates share the plan-window anchor today, so both reopen at the
    # same instant; computed per-engine anyway so a future per-engine anchor
    # cannot silently break the resume arithmetic.
    BG_5H_RESUME_EPOCH=$(( anchor + WINDOW_SECONDS ))
    return 0
}

select_cycle_engine() {
    CYCLE_ENGINE_OVERRIDE=""
    CYCLE_ROUTER_ACTION="run"
    CYCLE_ROUTER_MSG=""

    evaluate_budget_gates

    # ── TOTAL gates take precedence over routing: both engines pause. ──────────
    if [ -n "$BG_TOTAL_GATE" ]; then
        local resume spent limit period_key reason
        resume="$(_fmt_utc "$BG_TOTAL_RESUME_EPOCH")"
        if [ "$BG_TOTAL_GATE" = "DAILY_TOTAL" ]; then
            spent="$BG_DAILY"; limit="$TOTAL_DAILY_BUDGET_USD"
            period_key="$(_utc_day_start)"
            reason="next UTC midnight"
        else
            spent="$BG_WEEKLY"; limit="$TOTAL_WEEKLY_BUDGET_USD"
            period_key="$BG_TOTAL_RESUME_EPOCH"
            reason="earliest spend-expiry returning the rolling 7×24h total below the limit"
        fi
        CYCLE_ROUTER_ACTION="pause"
        CYCLE_ROUTER_MSG="[GATE] $BG_TOTAL_GATE — notional \$$spent >= limit \$$limit; affected: BOTH engines. Resume: $resume ($reason). Values are API-equivalent/notional usage, not billed cash."
        _notify_gate_block_once "$BG_TOTAL_GATE" "$period_key" \
            "💸 $BG_TOTAL_GATE gate closed — company paused (both engines).
Notional \$$spent of \$$limit. Resume: $resume ($reason).
API-equivalent/notional usage, not billed cash."
        _router_persist "${ENGINE}"
        return 0
    fi

    # ── Per-engine availability (binary/auth) on top of the 5h gates. ──────────
    local codex_avail=0
    if [ "$CODEX_DISABLED" != "1" ]; then
        [ -z "$RESOLVED_CODEX_BIN" ] && RESOLVED_CODEX_BIN="$(resolve_codex_bin 2>/dev/null || true)"
        [ -n "$RESOLVED_CODEX_BIN" ] && codex_avail=1
    fi
    local codex_count_full=0 codex_now
    codex_now="$(codex_window_count)"
    if [ -n "$CODEX_WINDOW_LIMIT" ] && [ "$codex_now" -ge "$CODEX_WINDOW_LIMIT" ] 2>/dev/null; then
        codex_count_full=1
    fi
    local claude_eligible codex_eligible
    claude_eligible="$BG_CLAUDE_OK"
    codex_eligible=0
    [ "$BG_CODEX_OK" = "1" ] && [ "$codex_avail" = "1" ] && [ "$codex_count_full" = "0" ] && codex_eligible=1

    local resume5
    resume5="$(_fmt_utc "$BG_5H_RESUME_EPOCH")"

    # ── Both engines individually blocked → pause until the earliest reopen. ───
    if [ "$claude_eligible" = "0" ] && [ "$codex_eligible" = "0" ]; then
        CYCLE_ROUTER_ACTION="pause"
        if [ "$BG_CLAUDE_OK" = "0" ] && [ "$BG_CODEX_OK" = "0" ]; then
            CYCLE_ROUTER_MSG="[GATE] CLAUDE_5H + CODEX_5H — claude notional \$$BG_CLAUDE5 >= \$$CLAUDE_5H_BUDGET_USD and codex notional \$$BG_CODEX5 >= \$$CODEX_5H_BUDGET_USD; affected: BOTH engines. Resume: $resume5 (earliest eligible 5h window end). Values are API-equivalent/notional usage, not billed cash."
            _notify_gate_block_once "BOTH_5H" "$(_window_anchor_epoch)" \
                "⏸️ Both 5h gates closed — company paused. Claude \$$BG_CLAUDE5/\$$CLAUDE_5H_BUDGET_USD, Codex \$$BG_CODEX5/\$$CODEX_5H_BUDGET_USD. Resume: $resume5. Notional usage, not billed cash."
        elif [ "$BG_CLAUDE_OK" = "0" ]; then
            CYCLE_ROUTER_MSG="[GATE] CLAUDE_5H — notional \$$BG_CLAUDE5 >= limit \$$CLAUDE_5H_BUDGET_USD; affected: claude (codex unavailable: avail=$codex_avail count_full=$codex_count_full). Resume: $resume5 (5h window end). Values are API-equivalent/notional usage, not billed cash."
        else
            CYCLE_ROUTER_MSG="[GATE] CODEX_5H — notional \$$BG_CODEX5 >= limit \$$CODEX_5H_BUDGET_USD; affected: codex (claude ineligible/unavailable). Resume: $resume5 (5h window end). Values are API-equivalent/notional usage, not billed cash."
        fi
        _router_persist "${ENGINE}"
        return 0
    fi

    # ── Exactly one engine eligible → run it; report the closed gate if any. ───
    if [ "$claude_eligible" = "1" ] && [ "$codex_eligible" = "0" ]; then
        [ "$ENGINE" != "claude" ] && CYCLE_ENGINE_OVERRIDE="claude"
        if [ "$BG_CODEX_OK" = "0" ]; then
            CYCLE_ROUTER_MSG="[GATE] CODEX_5H — notional \$$BG_CODEX5 >= limit \$$CODEX_5H_BUDGET_USD; affected: codex only. Claude continues. Codex resume: $resume5 (5h window end). Values are API-equivalent/notional, not billed cash."
        else
            CYCLE_ROUTER_MSG="[ROUTER] Codex unavailable (avail=$codex_avail, count $codex_now/${CODEX_WINDOW_LIMIT:-∞}) — running Claude"
        fi
        _router_persist "claude"
        return 0
    fi
    if [ "$claude_eligible" = "0" ] && [ "$codex_eligible" = "1" ]; then
        [ "$ENGINE" != "codex" ] && CYCLE_ENGINE_OVERRIDE="codex"
        CYCLE_ROUTER_MSG="[GATE] CLAUDE_5H — notional \$$BG_CLAUDE5 >= limit \$$CLAUDE_5H_BUDGET_USD; affected: claude only. Codex continues. Claude resume: $resume5 (5h window end). Values are API-equivalent/notional, not billed cash."
        _router_persist "codex"
        return 0
    fi

    # ── Both eligible → Alternate (intentional policy: distributes plan load and
    # preserves the operator's interactive capacity across both plans; NOT a
    # temporary fallback). Deterministic: the state file holds the last engine
    # run; a previously-blocked engine simply rejoins the toggle when eligible.
    if [ "$ROUTER_ALTERNATE" = "1" ]; then
        local last
        last="$(cat "$ROUTER_STATE_FILE" 2>/dev/null || echo claude)"
        if [ "$last" = "claude" ]; then
            [ "$ENGINE" != "codex" ] && CYCLE_ENGINE_OVERRIDE="codex"
            CYCLE_ROUTER_MSG="[ROUTER] Alternate → Codex (both eligible; claude 5h \$$BG_CLAUDE5/\$${CLAUDE_5H_BUDGET_USD:-∞}, codex 5h \$$BG_CODEX5/\$${CODEX_5H_BUDGET_USD:-∞})"
            _router_persist "codex"
        else
            [ "$ENGINE" != "claude" ] && CYCLE_ENGINE_OVERRIDE="claude"
            CYCLE_ROUTER_MSG="[ROUTER] Alternate → Claude (both eligible; claude 5h \$$BG_CLAUDE5/\$${CLAUDE_5H_BUDGET_USD:-∞}, codex 5h \$$BG_CODEX5/\$${CODEX_5H_BUDGET_USD:-∞})"
            _router_persist "claude"
        fi
        return 0
    fi

    # No alternation configured: run the configured primary.
    CYCLE_ROUTER_MSG="[ROUTER] Engine=$ENGINE primary, both gates open (claude 5h \$$BG_CLAUDE5/\$${CLAUDE_5H_BUDGET_USD:-∞}, codex 5h \$$BG_CODEX5/\$${CODEX_5H_BUDGET_USD:-∞})"
    _router_persist "$ENGINE"
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
        # NOT `[ -n "$x" ] && rm ...` followed by a bare `return`: when the test is
        # false the list returns 1, the bare `return` inherits it, and `set -e` kills
        # the CALLER. And with protection off snapshot_gitignore() always returns "",
        # so this path was guaranteed to fire — setting AUTO_LOOP_PROTECT_GITIGNORE=0
        # (a documented flag) would have bricked every cycle. Same family as APP-240.
        if [ -n "$snapshot_file" ]; then
            rm -f "$snapshot_file"
        fi
        return 0
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

    # Explicit `if` + `return 0`: as a function's LAST command, a false test would
    # make the function return 1 and `set -e` would kill the caller. That is exactly
    # how the container was dying for three days (APP-240) — different function, same
    # shape. This one fires whenever .gitignore is absent at cycle start.
    if [ -n "$snapshot_file" ]; then
        rm -f "$snapshot_file"
    fi
    return 0
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

# Kill a timed-out engine and EVERYTHING IT SPAWNED (APP-272, observed in production
# 2026-07-31). The old pattern killed only the direct child; on cycle #16 the timeout
# fired, `wait` returned rc=143, the loop declared FAIL and moved on — while the engine
# kept running in the background, finished its work 20 minutes later, and wrote
# consensus.md and Airtable AT THE SAME TIME as the next cycle's engine. Two writers,
# no lock. It resolved cleanly by luck of task ordering, not by design.
# Job control (`set -m`) puts the background subshell in its own process group, so a
# negative-pid signal reaches the whole tree. TERM first, then KILL for whatever
# ignores it.
_kill_engine_group() {
    local pid="$1"
    kill -TERM -"$pid" 2>/dev/null || kill -TERM "$pid" 2>/dev/null || true
    sleep 5
    kill -KILL -"$pid" 2>/dev/null || kill -KILL "$pid" 2>/dev/null || true
}

# jcode path for BOTH providers. Differences from the CLI path, each measured:
#   * no `total_cost_usd` — cost comes from scripts/core/engine-usage-cost.py over the
#     ndjson (which SUMS every `tokens` event: `done.usage` is the LAST request only,
#     so trusting it would undercount a multi-tool cycle and slacken the budget gates).
#   * no `--effort` flag — effort is an env var, per provider.
#   * no `-o message_file` — the final text is the `done` event's message.
#   * an unknown `-m` is NOT an error: jcode silently runs its default model. The model
#     preflight at boot is what keeps a typo from quietly becoming an opus-5 bill.
# $2 is the PROVIDER and is passed explicitly, never derived from $ENGINE or from
# _cycle_ran_on_codex: on the usage-limit fallback path `FALLBACK_USED=1` is assigned
# AFTER the engine call returns, so deriving it here would route the fallback cycle
# back to the provider that just hit its limit.
run_jcode_cycle() {
    local prompt="$1"
    local provider="${2:-claude}"
    local output_file timeout_flag events_file effort
    output_file=$(mktemp); timeout_flag=$(mktemp); events_file=$(mktemp)
    if [ "$provider" = "openai" ]; then
        effort="$CODEX_EFFORT"
        # Empty MODEL means "the codex config.toml default" on the CLI path; jcode has
        # no such file, and an empty -m would silently run ITS default model instead.
        [ -z "$MODEL" ] && MODEL="${JCODE_OPENAI_MODEL:-gpt-5.6-sol}"
    else
        effort="$CLAUDE_EFFORT"
    fi

    set +e
    set -m
    (
        cd "$PROJECT_DIR" || exit 1
        [ -n "$effort" ] && case "$provider" in
            openai) export JCODE_OPENAI_REASONING_EFFORT="$effort" ;;
            *)      export JCODE_ANTHROPIC_REASONING_EFFORT="$effort" ;;
        esac
        local cmd=("$JCODE_BIN" "-p" "$provider" "-C" "$PROJECT_DIR")
        [ -n "$MODEL" ] && cmd+=("-m" "$MODEL")
        cmd+=("run" "$prompt" "--quiet" "--no-update" "--no-selfdev" "--ndjson")
        "${cmd[@]}"
    ) > "$events_file" 2> "$output_file" &
    local engine_pid=$!
    set +m

    (
        sleep "$CYCLE_TIMEOUT_ACTIVE"
        if kill -0 "$engine_pid" 2>/dev/null; then
            echo "1" > "$timeout_flag"
            _kill_engine_group "$engine_pid"
        fi
    ) &
    local watchdog_pid=$!

    wait "$engine_pid"
    EXIT_CODE=$?
    kill "$watchdog_pid" 2>/dev/null || true
    wait "$watchdog_pid" 2>/dev/null || true
    set -e

    # OUTPUT feeds check_usage_limit / codex_auth_failed / the fallback trigger. On the
    # CLI path it was the full merged stdout+stderr; jcode splits them, and its API
    # errors (rate_limit_error, auth failures) arrive as ndjson EVENTS on stdout, not on
    # stderr. Taking stderr alone would make a rate-limited cycle look like a plain
    # error: no Codex fallback, no [LIMIT] ceiling row, and a 300s cooldown retry
    # against a closed window instead of the 3600s limit wait. Concatenate both, with
    # the error events first so a long stack trace cannot push them out of the tail.
    OUTPUT=$( { grep -h '"type":"error"' "$events_file" 2>/dev/null | tail -c 2000; \
                tail -c 4000 "$output_file" 2>/dev/null; } || true)

    # Final assistant text. NOT `done.text` alone — that is the last text BLOCK, not the
    # answer (measured: a two-line reply came back as its second line only). The shared
    # extractor keeps the longer of done.text and the concatenated deltas.
    RESULT_MESSAGE=""
    if [ -x "$PROJECT_DIR/scripts/core/jcode-final-text.py" ]; then
        RESULT_MESSAGE=$(python3 "$PROJECT_DIR/scripts/core/jcode-final-text.py" "$events_file" 2>/dev/null || true)
    fi

    # Cost: never silently zero. The adapter prices unknown models conservatively and
    # flags them; a missing number here would loosen four budget gates at once.
    JCODE_COST_JSON=""
    if [ -s "$events_file" ] && [ -x "$PROJECT_DIR/scripts/core/engine-usage-cost.py" ]; then
        JCODE_COST_JSON=$(python3 "$PROJECT_DIR/scripts/core/engine-usage-cost.py" \
            --ndjson-file "$events_file" 2>/dev/null || true)
    fi

    # Keep the raw stream for cost audits / price calibration (last 20 cycles).
    if [ -s "$events_file" ]; then
        mkdir -p "$LOG_DIR/cycle-ndjson" 2>/dev/null || true
        cp "$events_file" "$LOG_DIR/cycle-ndjson/cycle-$(printf '%04d' "${loop_count:-0}").ndjson" 2>/dev/null || true
        ls -t "$LOG_DIR/cycle-ndjson"/*.ndjson 2>/dev/null | tail -n +21 | xargs -r rm -f 2>/dev/null || true
    fi

    rm -f "$output_file" "$events_file"
    if [ -s "$timeout_flag" ]; then CYCLE_TIMED_OUT=1; EXIT_CODE=124; else CYCLE_TIMED_OUT=0; fi
    rm -f "$timeout_flag"
}

run_codex_cycle_cli() {
    local prompt="$1"
    local output_file timeout_flag message_file

    output_file=$(mktemp)
    timeout_flag=$(mktemp)
    message_file=$(mktemp)

    set +e
    set -m
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
    set +m

    (
        sleep "$CYCLE_TIMEOUT_ACTIVE"
        if kill -0 "$codex_pid" 2>/dev/null; then
            echo "1" > "$timeout_flag"
            _kill_engine_group "$codex_pid"
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

run_claude_cycle_cli() {
    local prompt="$1"
    local output_file timeout_flag

    output_file=$(mktemp)
    timeout_flag=$(mktemp)

    set +e
    set -m
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
    set +m

    (
        sleep "$CYCLE_TIMEOUT_ACTIVE"
        if kill -0 "$claude_pid" 2>/dev/null; then
            echo "1" > "$timeout_flag"
            _kill_engine_group "$claude_pid"
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

# Harness dispatch. Call sites below (router alternation, budget override, usage-limit
# fallback) are unchanged and keep calling these two names; only the harness underneath
# swaps. The provider is passed explicitly — see the note on run_jcode_cycle.
run_codex_cycle() {
    if [ "$LOOP_HARNESS" = "jcode" ]; then run_jcode_cycle "$1" openai
    else run_codex_cycle_cli "$1"; fi
}

run_claude_cycle() {
    if [ "$LOOP_HARNESS" = "jcode" ]; then run_jcode_cycle "$1" claude
    else run_claude_cycle_cli "$1"; fi
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
                    # Record WHERE the plan's real 5h ceiling sits. The configured
                    # CLAUDE_5H_BUDGET_USD is self-imposed; the plan's actual limit
                    # may bind first (it did: $12.28 of a $25 cap on 2026-07-24).
                    # Stamp the window spend at the exact moment the limit hits —
                    # the 14-day calibration report reads these rows.
                    log "[LIMIT] Claude 5h plan limit hit at window \$$(window_spend)/${CLAUDE_5H_BUDGET_USD:-∞} (model=${MODEL:-?})"
                    printf '%s limit %s %s\n' "$(date +%s)" "$(window_spend)" "${CLAUDE_5H_BUDGET_USD:-inf}" \
                        >> "$LOG_DIR/ceiling-events.log" 2>/dev/null || true
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

# Did THIS cycle actually run on Codex? `$ENGINE` alone is the wrong question:
# with router alternation (or a usage-limit fallback) the configured engine stays
# `claude` while the cycle is routed to Codex. Three other sites below already
# spell this test out inline; this is the same predicate, named.
_cycle_ran_on_codex() {
    [ "$FALLBACK_USED" -eq 1 ] || [ "$CYCLE_ENGINE_OVERRIDE" = "codex" ] || [ "$ENGINE" = "codex" ]
}

extract_cycle_metadata() {
    RESULT_TEXT=""
    CYCLE_COST="N/A"
    CYCLE_SUBTYPE="unknown"
    if _cycle_ran_on_codex; then
        CYCLE_TYPE="codex_exec"
    else
        CYCLE_TYPE="${ENGINE}_exec"
    fi

    # APP-240 root cause: this branch used to be gated on `[ "$ENGINE" = "claude" ]`,
    # which is TRUE on an alternation-routed Codex cycle — so Codex's plain-prose
    # final message was fed to the Claude JSON parser below. `grep` then matched
    # nothing and exited 1, `set -o pipefail` propagated it, and `set -e` killed the
    # loop SILENTLY mid-cycle, taking the container down with it (the entrypoint
    # supervises this process). That is the whole "container restarts every 5-10
    # minutes" mystery: 6 of 6 Codex-routed cycles died here, 6 of 6 Claude-routed
    # cycles survived because Claude's --output-format json always has a `{` line.
    # It also explains why `ENGINE=codex` as PRIMARY was never affected: the branch
    # was skipped entirely. Located by the ERR trap at the top of this file:
    #   [FATAL] auto-loop exiting rc=1 at line 1153: RESULT_JSON=$(printf ... | tail -1)
    # jcode carries no result JSON at all: the text came from the `done` event and the
    # cost from the token adapter, both already set by run_jcode_cycle. Feeding this
    # through the Claude JSON parser would set CYCLE_COST to empty and silently stop
    # record_spend — the same class of failure as APP-240, where a mis-routed parser
    # took the whole loop down.
    if [ "$LOOP_HARNESS" = "jcode" ]; then
        RESULT_TEXT=$(printf '%s' "$RESULT_MESSAGE" | head -c 2000 || true)
        [ -z "$RESULT_TEXT" ] && RESULT_TEXT=$(printf '%s' "$OUTPUT" | head -c 2000 || true)
        if [ -n "$JCODE_COST_JSON" ] && command -v jq >/dev/null 2>&1; then
            local _c _est
            _c=$(printf '%s' "$JCODE_COST_JSON" | jq -r '.cost_usd // empty' 2>/dev/null || true)
            _est=$(printf '%s' "$JCODE_COST_JSON" | jq -r '.estimated // false' 2>/dev/null || true)
            if [ -n "$_c" ]; then
                CYCLE_COST="$_c"
                [ "$_est" = "true" ] && log "[COST] estimated (uncalibrated model) — $(printf '%s' "$JCODE_COST_JSON" | head -c 200)"
            else
                log "[COST] adapter produced no number — budget gates would under-read; failing the cycle"
                CYCLE_SUBTYPE="error"
                [ "$EXIT_CODE" -eq 0 ] && EXIT_CODE=1
            fi
        else
            # No number at all (adapter missing/crashed, empty stream, jq absent).
            # This used to log and move on, which is precisely the silent-zero the
            # whole adapter exists to prevent: a systemic cause (a lost +x bit, a
            # future image without jq) would under-read all four gates forever while
            # every cycle logged healthy. Fail the cycle instead — five consecutive
            # failures trip the existing circuit breaker, which IS the brake.
            log "[COST] NO COST NUMBER for this cycle — failing it rather than letting the budget gates under-read"
            CYCLE_SUBTYPE="error"
            [ "$EXIT_CODE" -eq 0 ] && EXIT_CODE=1
        fi
        CYCLE_TYPE="jcode_${ENGINE}"
        if [ "$CYCLE_SUBTYPE" = "unknown" ]; then
            if [ "$EXIT_CODE" -eq 0 ]; then CYCLE_SUBTYPE="success"; else CYCLE_SUBTYPE="error"; fi
        fi
        return
    fi

    if ! _cycle_ran_on_codex; then
        # `claude -p --output-format json` writes its result JSON as ONE line, but the
        # CLI may prepend warnings on stdout/stderr (e.g. the untrusted-workspace
        # "Ignoring N permissions.allow entries" notice). Feeding the whole blob to jq
        # then fails, silently zeroing CYCLE_COST — which also stops record_spend, so
        # the Claude budget window undercounts and the cap never binds. Parse the LAST
        # JSON-looking line instead of the raw output.
        # `|| true` is load-bearing under `set -o pipefail`: "no JSON-looking line"
        # is a normal outcome, not an error, but grep signals it with exit 1 and
        # pipefail turns that into a failed assignment. Keep it even now that the
        # branch is Claude-only — a warning-only run would hit the same edge.
        RESULT_JSON=$(printf '%s\n' "$RESULT_MESSAGE" | grep -E '^[[:space:]]*\{' | tail -1 || true)
        [ -z "$RESULT_JSON" ] && RESULT_JSON="$RESULT_MESSAGE"
        if command -v jq >/dev/null 2>&1; then
            RESULT_TEXT=$(echo "$RESULT_JSON" | jq -r '.result // .message // .output_text // empty' 2>/dev/null | head -c 2000 || true)
            if [ -z "$RESULT_TEXT" ]; then
                RESULT_TEXT=$(echo "$RESULT_JSON" | jq -r '.. | .text? // empty' 2>/dev/null | head -c 2000 || true)
            fi

            parsed_cost=$(echo "$RESULT_JSON" | jq -r '.total_cost_usd // .cost_usd // empty' 2>/dev/null || true)
            if [ -n "$parsed_cost" ]; then
                CYCLE_COST="$parsed_cost"
            fi

            parsed_subtype=$(echo "$RESULT_JSON" | jq -r '.subtype // empty' 2>/dev/null || true)
            if [ -n "$parsed_subtype" ]; then
                CYCLE_SUBTYPE="$parsed_subtype"
            fi

            parsed_type=$(echo "$RESULT_JSON" | jq -r '.type // empty' 2>/dev/null || true)
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

# Check for existing instance.
# `kill -0 $pid` only proves SOME process holds that pid — not that it is this loop.
# On a container restart the pid file survives in the image layer while pids are
# handed out afresh, so the recorded pid is routinely reused by an unrelated process
# (the dashboard). The guard then refuses to start, the entrypoint exits, Docker
# restarts the container, and it loops forever — this caused two multi-hour outages
# (APP-235). Verify the process is actually an auto-loop before believing the file.
if [ -f "$PID_FILE" ]; then
    existing_pid=$(cat "$PID_FILE" 2>/dev/null || true)
    existing_cmd=""
    if [ -n "$existing_pid" ] && kill -0 "$existing_pid" 2>/dev/null; then
        if [ -r "/proc/$existing_pid/cmdline" ]; then
            existing_cmd=$(tr '\0' ' ' < "/proc/$existing_pid/cmdline" 2>/dev/null || true)
        else
            existing_cmd=$(ps -p "$existing_pid" -o args= 2>/dev/null || true)
        fi
    fi
    case "$existing_cmd" in
        *auto-loop.sh*)
            echo "Auto loop already running (PID $existing_pid). Stop it first with ./stop-loop.sh"
            exit 1
            ;;
        *)
            if [ -n "$existing_pid" ]; then
                echo "[startup] clearing stale PID file (pid $existing_pid is not an auto-loop)"
            fi
            rm -f "$PID_FILE"
            ;;
    esac
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
    # $MODEL_LABEL at this point is still the raw Claude $MODEL default (apply_tier_ladder
    # hasn't run for a cycle yet) — showing it here next to "Engine: codex" is misleading
    # (found 2026-07-27: boot log read "Engine: codex | Model: claude-haiku-4-5-...").
    log "Engine: codex | Model: ${CODEX_MODEL:-codex-default}:${CODEX_EFFORT:-config-default} | Sandbox: $CODEX_SANDBOX_MODE"
else
    log "Engine: claude | Model: $MODEL_LABEL | PermissionMode: $CLAUDE_PERMISSION_MODE"
fi
log "Engine bin: $RESOLVED_ENGINE_BIN"

# --- jcode harness preflight ------------------------------------------------
# jcode does NOT error on an unknown `-m`: it silently runs its own default model
# (measured 2026-07-31 — a dated `claude-haiku-4-5-20251001` ran as opus-5, which is
# both the wrong tier and roughly an order of magnitude more expensive per cycle).
# The tier ladder feeds MODEL from CLAUDE_TIER_LADDER, so a name jcode's catalog does
# not carry would silently un-do the entire cost-control ladder. Refuse to start.
if [ "$LOOP_HARNESS" = "jcode" ]; then
    if [ ! -x "$JCODE_BIN" ]; then
        echo "Error: LOOP_HARNESS=jcode but jcode not found at '$JCODE_BIN'." >&2
        exit 1
    fi
    log "Harness: jcode ($("$JCODE_BIN" --version 2>/dev/null | head -n1 || echo unknown))"
    _jcode_catalog() { "$JCODE_BIN" --quiet --no-update model list -p "$1" 2>/dev/null || true; }
    _claude_catalog="$(_jcode_catalog claude)"
    _openai_catalog="$(_jcode_catalog openai)"
    # An EMPTY catalog is an UNKNOWN, never a proof of absence. Reading it as
    # "every model is missing" would exit 1 on every boot, and the entrypoint
    # supervises this process — that is a container crash loop, the APP-235/240
    # shape. (Measured 2026-07-31: the catalog is static, answering with no auth
    # and with --network none. This guard is for the day that stops being true.)
    if [ -z "$_claude_catalog" ] || [ -z "$_openai_catalog" ]; then
        log "WARNING: jcode model catalog unavailable — cannot verify model names."
        log "         Falling back to LOOP_HARNESS=cli for this boot rather than"
        log "         running unverified (an unknown -m silently becomes jcode's default model)."
        LOOP_HARNESS="cli"
    else
    _bad=""
    # Ladder rungs may legally carry a `model:effort` suffix (APP-241); the catalog
    # holds bare model names, so compare only the part before the colon.
    for _m in $(printf '%s' "$CLAUDE_TIER_LADDER" | tr ',' ' ') "$MODEL"; do
        [ -z "$_m" ] && continue
        _m="${_m%%:*}"
        printf '%s\n' "$_claude_catalog" | grep -qx -- "$_m" || _bad="$_bad claude:$_m"
    done
    _om="${CODEX_MODEL:-${JCODE_OPENAI_MODEL:-gpt-5.6-sol}}"
    _om="${_om%%:*}"
    printf '%s\n' "$_openai_catalog" | grep -qx -- "$_om" || _bad="$_bad openai:$_om"
    if [ -n "$_bad" ]; then
        echo "Error: model name(s) not in jcode's catalog:$_bad" >&2
        echo "       jcode would SILENTLY run its default model instead of failing." >&2
        echo "       Fix CLAUDE_TIER_LADDER / MODEL / CODEX_MODEL, or set LOOP_HARNESS=cli." >&2
        exit 1
    fi
    log "Harness preflight: all ladder models present in jcode catalog"
    fi
    # MCP is not optional for this company: cycles read and write Airtable and Linear.
    # jcode reads only the global ~/.jcode/mcp.json, so a missing file is a silent
    # capability loss, not an error — check it here where it is still loud.
    if [ ! -s "${JCODE_HOME:-$HOME/.jcode}/mcp.json" ]; then
        log "WARNING: ${JCODE_HOME:-$HOME/.jcode}/mcp.json missing — cycles will run WITHOUT Airtable/Linear/Context7/browser tools"
    else
        log "Harness MCP: $(python3 -c 'import json,sys;print(",".join(json.load(open(sys.argv[1]))["mcpServers"]))' "${JCODE_HOME:-$HOME/.jcode}/mcp.json" 2>/dev/null || echo unreadable)"
    fi
fi
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
log "Interval: ${LOOP_INTERVAL}s | Timeout: ${CYCLE_TIMEOUT_SECONDS}s (escalated ${ESCALATED_CYCLE_TIMEOUT_SECONDS}s) | Breaker: ${MAX_CONSECUTIVE_ERRORS} errors"
# Fallback/alternation only mean anything when Claude is primary — when $ENGINE is
# already codex there's no "Claude usage limit" to fall back from, so logging this
# unconditionally (old behavior) was actively misleading on a codex-primary config.
if [ "$ENGINE" = "claude" ] && [ -n "$FALLBACK_ENGINE" ]; then
    log "Fallback engine: $FALLBACK_ENGINE (on Claude usage limit)"
fi
# ── Four-gate budget summary + deprecation warnings (APP-263) ──────────────────
log "Budget gates (all notional/API-equivalent, none billed cash): Claude 5h \$${CLAUDE_5H_BUDGET_USD:-∞} | Codex 5h \$${CODEX_5H_BUDGET_USD:-∞} | Daily TOTAL \$${TOTAL_DAILY_BUDGET_USD:-∞} (UTC day) | Weekly TOTAL \$${TOTAL_WEEKLY_BUDGET_USD:-∞} (rolling 7×24h)"
if [ -z "$CLAUDE_5H_BUDGET_USD" ] && [ -z "$CODEX_5H_BUDGET_USD" ] \
   && [ -z "$TOTAL_DAILY_BUDGET_USD" ] && [ -z "$TOTAL_WEEKLY_BUDGET_USD" ]; then
    log "WARNING: NO budget gate is configured — engine spend is UNBOUNDED. Set the four APP-263 variables."
fi
if [ -n "$WINDOW_BUDGET_USD" ]; then
    log "[DEPRECATED] WINDOW_BUDGET_USD=\$$WINDOW_BUDGET_USD is set but IGNORED — replaced by CLAUDE_5H_BUDGET_USD (APP-263). It cannot override the new gates; remove it from runtime.env."
fi
if [ -n "$TOTAL_BUDGET_USD" ]; then
    log "[DEPRECATED] TOTAL_BUDGET_USD=\$$TOTAL_BUDGET_USD is set but IGNORED — replaced by TOTAL_DAILY_BUDGET_USD/TOTAL_WEEKLY_BUDGET_USD (APP-263). It cannot override the new gates; remove it from runtime.env."
fi
if [ -n "$PLAN_CEILING_USD" ] || [ -n "$OPERATOR_RESERVE_PCT" ] || [ -n "$WINDOW_BUDGET_FLOOR_USD" ]; then
    log "[DEPRECATED] PLAN_CEILING_USD/OPERATOR_RESERVE_PCT/WINDOW_BUDGET_FLOOR_USD are set but IGNORED — the APP-237 dynamic reserve cap was retired by APP-263; Alternate routing is the operator-capacity mechanism."
fi
if [ "$ENGINE" != "claude" ]; then
    log "Router: \$ENGINE=$ENGINE is the configured primary; APP-263 gates apply to every engine"
elif [ "$ROUTER_ALTERNATE" = "1" ]; then
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
    # One-shot operator escalation overrides the ladder's pick for this cycle only.
    apply_cycle_escalation

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
    # Opportunity Discovery on/off (cockpit Settings -> DISCOVERY_ENABLED, logs/runtime.env).
    # Default OFF when unset (operator decision, 2026-07-27) -- unlike the other settings
    # knobs, which default to their prior standing behavior when blank. See PROMPT.md's
    # "TENDER TRACK" section for what the loop should do instead while this is off.
    if [ "${DISCOVERY_ENABLED:-0}" = "1" ]; then
        _discovery_line="6. Opportunity Discovery is ENABLED (cockpit setting) — normal new-axis discovery may run per PROMPT.md's own rules."
    else
        # No candidate ID is hardcoded here, deliberately. This line used to name
        # `176-R`, and it kept naming it after the operator terminated and archived
        # that candidate — so every cycle, by default, the loop's own authoritative
        # instruction told the company to develop something that no longer existed.
        # A shell script must not carry an identifier a registry can retire underneath
        # it; ask the registry instead.
        _discovery_line="6. Opportunity Discovery is DISABLED (cockpit setting, default) — do NOT scan/rank/propose brand-new candidate axes this cycle. Follow PROMPT.md's \`### TENDER TRACK\` section instead: pursue tender candidates, and/or continue whatever candidate \`memories/candidate-registry.md\` currently records as the Active Validation — read it, do not assume one from memory, and if Selected is empty then there is no such candidate and the Tender Track is the whole job. This does not pause an in-flight tender feasibility packet, or Human Directive / OPREQ handling."
    fi
    FULL_PROMPT="$PROMPT

---

## Runtime Guardrails (must follow)

1. Early in the cycle, create or update \`memories/consensus.md\` with the required section skeleton.
2. If work scope is large, persist partial decisions to \`memories/consensus.md\` before deep dives.
3. Prefer shipping one completed milestone over broad parallel exploration.
4. Never write files via shell heredoc (\`cat <<EOF\`). Use \`apply_patch\` for file creates/edits.
5. Never execute shell lines that begin with \`>\` or \`>=\`; treat them as text and keep them inside markdown/files.
$_discovery_line

---

## Current Consensus (pre-loaded, do NOT re-read this file)

$CONSENSUS

---

This is Cycle #$loop_count. Act decisively."

    # The company's own brakes must be IN the prompt that is actually sent. Assert on
    # the assembled text, never on the source files — every silent failure this loop
    # has shipped was source-level logic that looked right and was never checked
    # against what actually came out the other end.
    #
    # Concretely: a 2026-07-29 proposal to make the selection section conditional on
    # DISCOVERY_ENABLED was measured with a parser that ignored fenced code blocks. It
    # drew the section boundary at 16,857 bytes when the real section is 32,720
    # (PROMPT.md:24-507) and CONTAINS the WTP hard stop, the OPREQ escalation ledger
    # and the external-adjudication rule — the three things PROMPT.md:787-788 says
    # continue "regardless of this toggle". Shipped, it would have removed all three
    # BY DEFAULT, since DISCOVERY_ENABLED defaults to 0, and nothing would have
    # errored. This check is what makes that class of edit fail loudly instead.
    if directive_unaudited; then
        log "[DIRECTIVE-UNAUDITED] Refusing to run Cycle #$loop_count — directive tripwire fired ($DIRECTIVE_AUDIT_DETAIL)"
        log "[DIRECTIVE-UNAUDITED] This is the accidental/direct-write tripwire, not a security boundary. Reconciliation and baselining are OPERATOR-ONLY via the host-side channel (autocompany-deploy/scripts/directive-baseline.sh) — the loop and the model never self-repair this state."
        if [ -n "${TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${TELEGRAM_CHAT_ID:-}" ]; then
            bash "$SCRIPT_DIR/telegram-notify.sh" \
                "🛑 Cycle #${loop_count} BLOCKED — directive tripwire: ${DIRECTIVE_AUDIT_DETAIL}. No cycle ran. Reconcile via host-side directive-baseline.sh only." \
                >/dev/null 2>&1 || true
        fi
        save_state "idle"
        log_cycle "$loop_count" "WAIT" "Sleeping ${LOOP_INTERVAL}s before next cycle..."
        sleep "$LOOP_INTERVAL" || true
        continue
    fi

    if ! prompt_guardrails_intact "$FULL_PROMPT"; then
        log "[GUARDRAIL-MISSING] Refusing to run Cycle #$loop_count — the assembled prompt is missing: $MISSING_GUARDRAILS"
        log "[GUARDRAIL-MISSING] Not a crash: the loop stays up and will retry next interval. Fix PROMPT.md or the assembly, do NOT bypass this."
        if [ -n "${TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${TELEGRAM_CHAT_ID:-}" ]; then
            bash "$SCRIPT_DIR/telegram-notify.sh" \
                "🛑 Cycle #${loop_count} BLOCKED — assembled prompt lost a guardrail: ${MISSING_GUARDRAILS}. No cycle ran." \
                >/dev/null 2>&1 || true
        fi
        save_state "idle"
        log_cycle "$loop_count" "WAIT" "Sleeping ${LOOP_INTERVAL}s before next cycle..."
        sleep "$LOOP_INTERVAL" || true
        continue
    fi

    # Run selected engine in headless mode with per-cycle timeout
    run_engine_cycle "$FULL_PROMPT"

    # If this cycle ran on Codex and it hit a PERMANENT auth failure, disable Codex
    # for the rest of the process — otherwise alternation/fallback keep sending every
    # other cycle to a dead engine. Recovery needs a re-login + reseed (see APP-200).
    if { [ "$FALLBACK_USED" -eq 1 ] || [ "$CYCLE_ENGINE_OVERRIDE" = "codex" ] || [ "$ENGINE" = "codex" ]; } \
        && [ "$CODEX_DISABLED" != "1" ] && codex_auth_failed "$OUTPUT"; then
        CODEX_DISABLED=1
        log "[CODEX-AUTH-FAIL] Codex auth permanently rejected (rotated/consumed token) — disabling Codex for this run; re-login + reseed required (exit=$EXIT_CODE, evidence: ${CODEX_AUTH_EVIDENCE:-none})"
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
        # …but the USD still has to reach the DAILY/WEEKLY totals and the Codex 5h
        # gate. On the CLI path those read `ccusage codex session`, which parses
        # CODEX_HOME session files. **jcode never writes CODEX_HOME**, so without this
        # line an openai cycle under LOOP_HARNESS=jcode is invisible to three of the
        # four APP-263 gates while the adapter's correct figure is dropped on the
        # floor: unbounded gpt-5.6-sol spend behind a [BUDGET] line reading $0.0000.
        # Found by the pre-deploy audit, not by testing — every cycle "worked".
        if [ "$LOOP_HARNESS" = "jcode" ]; then
            record_total_spend "codex" "${LOOP_BOOT_ID}-c${loop_count:-0}" "$CYCLE_COST"
        fi
    else
        record_spend "$CYCLE_COST"
    fi

    # --- per-cycle telemetry ledger (opus experiment + reserve-% cap controller) ---
    # One line per completed cycle: epoch engine model effort cost claude_window_usd.
    _tele_eng="claude"; _tele_model="${MODEL:-config-default}"; _tele_eff="${CLAUDE_EFFORT:--}"
    if [ "$FALLBACK_USED" -eq 1 ] || [ "$CYCLE_ENGINE_OVERRIDE" = "codex" ] || [ "$ENGINE" = "codex" ]; then
        _tele_eng="codex"; _tele_model="${CODEX_MODEL:-gpt-5.6-sol}"; _tele_eff="${CODEX_EFFORT:--}"
    fi
    _tele_fill="$(window_spend)"
    printf '%s %s %s %s %s %s\n' "$(date +%s)" "$_tele_eng" "$_tele_model" "$_tele_eff" "${CYCLE_COST:-N/A}" "$_tele_fill" >> "$LOG_DIR/engine-telemetry.log" 2>/dev/null || true
    log "[TELEMETRY] engine=$_tele_eng model=$_tele_model effort=$_tele_eff cost=${CYCLE_COST:-N/A} claude_window=\$$_tele_fill/${CLAUDE_5H_BUDGET_USD:-∞}"

    # Did this cycle actually leave anything behind? (APP-242)
    check_stall

    cycle_failed_reason=""
    cycle_soft_timeout=0
    if [ "$CYCLE_TIMED_OUT" -eq 1 ]; then
        if validate_consensus && consensus_changed_since_backup; then
            cycle_soft_timeout=1
        else
            cycle_failed_reason="Timed out after ${CYCLE_TIMEOUT_ACTIVE}s"
        fi
    elif [ "$EXIT_CODE" -ne 0 ]; then
        cycle_failed_reason="Exit code $EXIT_CODE"
    elif ! validate_consensus; then
        cycle_failed_reason="consensus.md validation failed after cycle"
    fi

    if [ "$cycle_soft_timeout" -eq 1 ]; then
        log_cycle "$loop_count" "OK" "Timed out after ${CYCLE_TIMEOUT_ACTIVE}s but consensus was updated; keeping progress (cost: ${CYCLE_COST}, subtype: ${CYCLE_SUBTYPE})"
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
            # Second usage-limit path (no Codex fallback available) — stamp the
            # ceiling here too, otherwise limits hit on this branch are invisible
            # to the reserve-% controller. See the fallback branch above.
            log_cycle "$loop_count" "LIMIT" "API usage limit detected at window \$$(window_spend)/${CLAUDE_5H_BUDGET_USD:-∞}. Waiting ${LIMIT_WAIT_SECONDS}s..."
            printf '%s limit %s %s\n' "$(date +%s)" "$(window_spend)" "${CLAUDE_5H_BUDGET_USD:-inf}" \
                >> "$LOG_DIR/ceiling-events.log" 2>/dev/null || true
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

    # Operator-request ledger (OPREQ): process any new/changed escalation-worthy
    # request the cycle just wrote to memories/operator-requests.md — dedup on
    # content hash, notify Telegram only on genuine API success, check for
    # resolutions, regenerate consensus.md's "Awaiting Operator" projection.
    # Deterministic, never fails the loop (script always exits 0).
    python3 "$SCRIPT_DIR/operator_request_notify.py" "$PROJECT_DIR" \
        >> "$LOG_DIR/operator-requests.log" 2>&1 || true

    # Telegram: ping the operator with this cycle's summary (no-op if TELEGRAM_* unset; never fails the loop).
    if [ -n "${TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${TELEGRAM_CHAT_ID:-}" ]; then
        _tg_head="OK"; [ -n "${cycle_failed_reason:-}" ] && _tg_head="FAIL: ${cycle_failed_reason}"
        bash "$SCRIPT_DIR/telegram-notify.sh" "🔄 Cycle #${loop_count} — ${_tg_head} (cost ${CYCLE_COST})
$(printf '%s' "${RESULT_TEXT:-}" | head -c 600)" >/dev/null 2>&1 || true
    fi

    save_state "idle"
    log_cycle "$loop_count" "WAIT" "Sleeping ${LOOP_INTERVAL}s before next cycle..."
    # `|| true` is load-bearing twice over. Under `set -e` a killed sleep exits
    # non-zero and would take the whole loop down with it — the same failure
    # shape as the 2026-07-26 crash-loop. With the guard, killing this sleep
    # becomes a deliberate "run the next cycle now" primitive:
    #   docker exec <container> pkill -f "sleep ${LOOP_INTERVAL}"
    # which starts the next cycle immediately without a rebuild, without
    # resetting loop_count, and without shortening LOOP_INTERVAL (shortening it
    # multiplies spend against the Claude window; waking on demand does not).
    sleep "$LOOP_INTERVAL" || true
done
