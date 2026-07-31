#!/usr/bin/env bash
# Auto-Company container entrypoint: runs the dashboard + the autonomous loop
# together, wired so the container exits (and Coolify restarts) if either dies.
set -euo pipefail
cd /app

# --- privilege drop ---------------------------------------------------------
# tini launches us as root (PID 1). claude refuses --dangerously-skip-permissions
# as root, so we fix the mounted-volume ownership here (needs root) then re-exec
# this same script as the non-root `app` user.
if [ "$(id -u)" = "0" ]; then
    mkdir -p memories projects logs
    chown -R app:app memories projects logs 2>/dev/null || true
    exec gosu app "$0" "$@"
fi

# --- from here on we run as `app` (non-root) ---
export HOME=/home/app
cd /app

# Boot-epoch stamp (REVISE-2 gate B11): the loop's MCP-config freshness gate
# compares the generator's mcp.json.meta timestamp against THIS value, so a stale
# config left on the persistent volume by a previous boot can never pass for a
# generation that actually failed this boot. Written before anything else runs.
mkdir -p logs 2>/dev/null || true
date +%s > logs/.container-boot-epoch 2>/dev/null \
    || echo "[entrypoint] WARNING: cannot stamp logs/.container-boot-epoch — a jcode boot will fail its config-freshness gate" >&2

# --- operator runtime overrides (SSH-editable; no Coolify env UI needed) --------
# A KEY=value file on a persistent volume lets config be tuned by editing it over
# SSH or the cockpit Settings panel + redeploying, instead of the Coolify env UI.
# Values here OVERRIDE the container env (last write wins).
#
# There are exactly TWO config stores, and each key should have ONE owner:
#   * Coolify env UI  — image/identity values fixed at build/boot: auth tokens the
#     container cannot function without, git identity, DASHBOARD_PORT.
#   * this file       — every operator-tunable knob, plus the API keys the loop
#     acquires over its life. It is on a persistent volume and is the only store
#     the cockpit can write.
# A key set in BOTH is not an error, but it IS invisible: this file wins and the
# Coolify UI keeps displaying a value that has no effect (found 2026-07-28 with a
# stale MODEL=claude-haiku-4-5-20251001 and a LOOP_INTERVAL that disagreed with
# the live one). The override report below makes that shadowing visible at boot
# instead of leaving it to be discovered from behaviour. See docs/devops/env-ownership.md.
RUNTIME_ENV_FILE="${RUNTIME_ENV_FILE:-/app/logs/runtime.env}"
if [ -f "$RUNTIME_ENV_FILE" ]; then
    echo "[entrypoint] applying runtime overrides from $RUNTIME_ENV_FILE"
    _shadowed=""
    # Parse KEY=value literally (NOT `. file`) so values with shell-special chars
    # — e.g. a Coolify token like `1|abcdef` whose `|` would otherwise be read as a
    # pipe — are exported verbatim. Handles `=` in the value and optional quotes.
    while IFS= read -r _line || [ -n "$_line" ]; do
        case "$_line" in ''|\#*) continue ;; esac
        _k=${_line%%=*}
        _v=${_line#*=}
        _k=$(printf '%s' "$_k" | tr -d '[:space:]')
        case "$_v" in
            \"*\") _v=${_v#\"}; _v=${_v%\"} ;;
            \'*\') _v=${_v#\'}; _v=${_v%\'} ;;
        esac
        # An explicit `if`, not `[ -n "$_k" ] && export ...`. Measured 2026-07-28:
        # in THIS position the AND-list is safe, because the loop is fed by a
        # redirect (`done < FILE`) and `set -e` exempts the left operand of an
        # AND-OR list. The same shape as the last command of a loop fed by a PIPE
        # is fatal — the pipeline inherits status 1 and `set -e` fires. Since the
        # difference is invisible at the call site, the shape is simply not used
        # here; a blank line or a line starting with `=` now skips quietly.
        if [ -n "$_k" ]; then
            # Shadowing check before the export, while the container-env value is
            # still readable. Only a DIFFERENT value is worth reporting; a key set
            # identically in both places is redundant, not confusing.
            if [ -n "${!_k+set}" ] && [ "${!_k}" != "$_v" ]; then
                _shadowed="$_shadowed $_k"
            fi
            export "$_k=$_v"
        fi
    done < "$RUNTIME_ENV_FILE"

    if [ -n "$_shadowed" ]; then
        echo "[entrypoint] runtime.env OVERRIDES the container env for:$_shadowed"
        echo "[entrypoint]   (the Coolify UI still shows its own value for these; it has no effect)"
    fi
    unset _line _k _v _shadowed
fi

# --- required auth (from `claude setup-token`, injected as a Coolify secret) ---
if [ -z "${CLAUDE_CODE_OAUTH_TOKEN:-}" ]; then
    echo "FATAL: CLAUDE_CODE_OAUTH_TOKEN is not set." >&2
    echo "Generate it with 'claude setup-token' and set it as a Coolify secret." >&2
    exit 1
fi

# --- runtime dirs (also mounted as persistent volumes) ---
mkdir -p memories projects logs

# --- persist docs/ across redeploys ---------------------------------------------
# Agents write deliverables to docs/<role>/ (per CLAUDE.md), but docs/ is NOT a
# mounted volume, so cycle docs (decision rationale, research, build logs) are
# wiped on every redeploy. Back docs/ with the persistent memories volume via a
# symlink. The image ships an (essentially empty, docs/* is gitignored) docs/ dir;
# migrate it into the store without clobbering persisted files, then symlink.
#
# The handful of TRACKED docs files (.gitignore's docs/* whitelist) are an
# exception: they are code, not agent output, and must always reflect the
# current deploy. Found 2026-07-25: the no-clobber copy below (correct for
# agent-written content) was also freezing these few files at whatever the
# FIRST deploy after this feature shipped happened to contain — a code change
# to app-230-mcp-wiring.md landed in git and was deployed, but production kept
# serving the Jul 22-24 version through several later redeploys. Always
# overwrite the tracked set before the no-clobber bulk copy runs.
DOCS_STORE="${DOCS_STORE:-/app/memories/_docs}"
mkdir -p "$DOCS_STORE"
TRACKED_DOCS_FILES="windows-setup.md devops/phase-6-runbook.md devops/app-230-mcp-wiring.md devops/app-250-crash-alarm.md handoff.html"
if [ ! -L /app/docs ]; then
    if [ -d /app/docs ]; then
        for f in $TRACKED_DOCS_FILES; do
            if [ -f "/app/docs/$f" ]; then
                mkdir -p "$DOCS_STORE/$(dirname "$f")"
                cp -a "/app/docs/$f" "$DOCS_STORE/$f"
            fi
        done
        cp -a -n /app/docs/. "$DOCS_STORE/" 2>/dev/null || true
        rm -rf /app/docs
    fi
    ln -s "$DOCS_STORE" /app/docs
    echo "[entrypoint] docs/ -> $DOCS_STORE (persistent, tracked files refreshed)"
fi

# --- persist .claude/skills/ so company-authored skills survive redeploys --------
# The company can author new skills via skill-creator, but .claude/skills/ ships in
# the image (not a volume) so they'd be wiped on redeploy. Back it with the memories
# volume: seed the image's base skills into the store without clobbering persisted
# ones, then symlink. The symlink must exist BEFORE the loop starts so Claude Code
# discovers the full set. (APP-204)
SKILLS_STORE="${SKILLS_STORE:-/app/memories/_skills}"
mkdir -p "$SKILLS_STORE"
if [ ! -L /app/.claude/skills ]; then
    if [ -d /app/.claude/skills ]; then
        # clobber (no -n): base skills stay repo-authoritative (image updates win),
        # while company-authored skills (unique names, not in the image) are left
        # untouched in the store and thus persist.
        cp -a /app/.claude/skills/. "$SKILLS_STORE/" 2>/dev/null || true
        rm -rf /app/.claude/skills
    fi
    ln -s "$SKILLS_STORE" /app/.claude/skills
    echo "[entrypoint] .claude/skills/ -> $SKILLS_STORE (persistent)"
fi

# --- the company's own git identity for its commits/deploys (optional) ---
[ -n "${COMPANY_GIT_NAME:-}" ]  && git config --global user.name  "$COMPANY_GIT_NAME"
[ -n "${COMPANY_GIT_EMAIL:-}" ] && git config --global user.email "$COMPANY_GIT_EMAIL"
git config --global --add safe.directory /app || true

# --- GitHub auth for the company's own pushes / repo creation ---
# gh CLI reads GH_TOKEN automatically; wire git push (HTTPS) to the same token.
if [ -n "${GH_TOKEN:-}" ]; then
    printf 'https://x-access-token:%s@github.com\n' "$GH_TOKEN" > "$HOME/.git-credentials"
    chmod 600 "$HOME/.git-credentials"
    git config --global credential.helper store
fi

# --- persist Claude's config + session transcripts on a volume ---
# Claude Code stores per-session transcripts under $CLAUDE_CONFIG_DIR (default ~/.claude,
# which is EPHEMERAL here and reset on every redeploy). Relocate it onto the persistent
# logs volume so usage history survives restarts and ccusage (Cost panel) can price the
# Claude side. Both Claude Code and ccusage honor CLAUDE_CONFIG_DIR; auth still comes from
# CLAUDE_CODE_OAUTH_TOKEN, so relocating the dir does not affect login.
export CLAUDE_CONFIG_DIR="${CLAUDE_CONFIG_DIR:-/app/logs/.claude}"
mkdir -p "$CLAUDE_CONFIG_DIR" && chmod 700 "$CLAUDE_CONFIG_DIR"
echo "[entrypoint] CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR (persistent)"

# Relocating the config dir loses the workspace trust record, and untrusted /app makes
# `claude -p` print an "Ignoring N permissions.allow entries" warning ABOVE its JSON
# result — which broke cost parsing (and therefore the Claude budget ledger). Mark /app
# trusted so stdout stays clean. Non-interactive runs cannot answer a trust dialog.
_cc_json="$CLAUDE_CONFIG_DIR/.claude.json"
[ -s "$_cc_json" ] || echo '{}' > "$_cc_json"
if command -v jq >/dev/null 2>&1; then
    if jq '.projects["/app"].hasTrustDialogAccepted = true' "$_cc_json" > "$_cc_json.tmp" 2>/dev/null; then
        mv "$_cc_json.tmp" "$_cc_json"
        echo "[entrypoint] marked /app as a trusted Claude workspace"
    else
        rm -f "$_cc_json.tmp"
    fi
fi

# --- Codex fallback auth (optional) ---
# Codex (0.144.x) owns the ChatGPT OAuth session: during `codex exec` it refreshes
# and ROTATES the tokens, writing the new refresh/access tokens back to auth.json.
# So CODEX_HOME must live on a PERSISTENT volume and CODEX_AUTH_B64 must only SEED
# it on first boot — re-writing the original secret every restart resurrects an
# already-used refresh token and 401s ("refresh token was already used"). We put
# CODEX_HOME inside the persistent logs volume (no extra Coolify mount needed) and
# force the file credential store (no keyring in a container).
export CODEX_HOME="${CODEX_HOME:-/app/logs/.codex}"
mkdir -p "$CODEX_HOME" && chmod 700 "$CODEX_HOME"
if [ ! -f "$CODEX_HOME/config.toml" ]; then
    # 2026-07-25: write-capable MCP parity with the Claude engine (Context7,
    # Linear, Airtable via their official HTTP MCP endpoints, sharing the same
    # LINEAR_API_KEY/AIRTABLE_API_KEY/CONTEXT7_API_KEY the loop already exports).
    # CLAUDE.md is set as the project-doc fallback since Codex looks for
    # AGENTS.md by default and this repo has none. Kept in sync with the live
    # /app/logs/.codex/config.toml — if you edit one, edit both.
    cat > "$CODEX_HOME/config.toml" <<'EOF'
model = "gpt-5.6-sol"
model_reasoning_effort = "low"
approval_policy = "never"
cli_auth_credentials_store = "file"

project_doc_fallback_filenames = ["CLAUDE.md"]
project_doc_max_bytes = 32768
project_root_markers = [".git", "CLAUDE.md"]

[projects."/app"]
trust_level = "trusted"

[mcp_servers.openaiDeveloperDocs]
url = "https://developers.openai.com/mcp"

[mcp_servers.context7]
url = "https://mcp.context7.com/mcp"
env_http_headers = { "CONTEXT7_API_KEY" = "CONTEXT7_API_KEY" }
enabled = true
required = false
startup_timeout_sec = 20
tool_timeout_sec = 60
enabled_tools = ["resolve-library-id", "query-docs"]

[mcp_servers.linear]
url = "https://mcp.linear.app/mcp"
bearer_token_env_var = "LINEAR_API_KEY"
enabled = true
required = false
startup_timeout_sec = 20
tool_timeout_sec = 60
enabled_tools = [
  "get_issue", "list_issues", "save_issue",
  "list_issue_statuses", "get_issue_status", "list_issue_labels",
  "list_comments", "save_comment",
  "list_projects", "get_project", "list_project_labels", "save_project",
  "get_status_updates", "save_status_update",
  "list_teams", "get_team",
]

[mcp_servers.airtable]
url = "https://mcp.airtable.com/mcp"
bearer_token_env_var = "AIRTABLE_API_KEY"
enabled = true
required = false
startup_timeout_sec = 20
tool_timeout_sec = 60
enabled_tools = [
  "ping", "list_bases", "search_bases", "list_tables_for_base",
  "get_table_schema", "list_records_for_table", "search_records",
  "list_record_comments",
  "create_records_for_table", "update_records_for_table",
  "create_record_comment",
  "create_table", "create_field", "update_table", "update_field",
]

# Browser, reached through the host-side gateway on the docker bridge — the container has
# no route to the tailnet itself. The gateway also holds the single-flight lock (the VM
# fits one active task) and alerts the operator on connector activity. Deliberately no
# enabled_tools allowlist: the operator chose to watch the connector surface rather than
# restrict it (2026-07-28). Rules for using this live in PROMPT.md "BROWSER".
[mcp_servers.browseros]
url = "http://172.17.0.1:9245/mcp"
enabled = true
required = false
startup_timeout_sec = 30
tool_timeout_sec = 180
EOF
fi
if [ -s "$CODEX_HOME/auth.json" ]; then
    # Persisted (possibly rotated) auth already present — never overwrite it.
    chmod 600 "$CODEX_HOME/auth.json" 2>/dev/null || true
    export FALLBACK_ENGINE="${FALLBACK_ENGINE:-codex}"
    echo "[entrypoint] Codex auth: using persisted $CODEX_HOME/auth.json"
elif [ -n "${CODEX_AUTH_B64:-}" ]; then
    # First boot only: seed auth.json from the bootstrap secret.
    if echo "$CODEX_AUTH_B64" | base64 -d > "$CODEX_HOME/auth.json" 2>/dev/null; then
        chmod 600 "$CODEX_HOME/auth.json"
        export FALLBACK_ENGINE="${FALLBACK_ENGINE:-codex}"
        echo "[entrypoint] Codex auth: seeded from CODEX_AUTH_B64 (first boot)"
    else
        echo "[entrypoint] warning: CODEX_AUTH_B64 failed to decode; Codex disabled" >&2
    fi
else
    echo "[entrypoint] Codex auth: none present; Codex fallback disabled"
fi

DASHBOARD_PORT="${DASHBOARD_PORT:-8787}"

DASH_PID=""
LOOP_PID=""
HEARTBEAT_PID=""
term() {
    echo "[entrypoint] shutting down..."
    [ -n "$LOOP_PID" ] && kill -TERM "$LOOP_PID" 2>/dev/null || true
    [ -n "$DASH_PID" ] && kill -TERM "$DASH_PID" 2>/dev/null || true
    [ -n "$HEARTBEAT_PID" ] && kill -TERM "$HEARTBEAT_PID" 2>/dev/null || true
}
trap term TERM INT

# --- Sentry Crons heartbeat (background, best-effort, APP-250) — NOT part of
# the dashboard/loop supervision below: its own death must never tear down the
# container, it only proves to an external watcher that the container is alive.
./scripts/core/sentry-heartbeat.sh &
HEARTBEAT_PID=$!

# --- dashboard (background), bound to all interfaces for Traefik/Cloudflare ---
echo "[entrypoint] starting dashboard on 0.0.0.0:${DASHBOARD_PORT}"
python3 dashboard/server.py --host 0.0.0.0 --port "$DASHBOARD_PORT" &
DASH_PID=$!

# --- jcode harness provisioning (only when the loop will actually use it) ---------
# Three things jcode needs that the CLIs do not, each one a SILENT capability loss if
# missing rather than an error:
#   1. MCP config. jcode reads only its own global ~/.jcode/mcp.json (it does not read
#      the repo's .mcp.json in v0.64.2) and speaks stdio only. Without this the cycles
#      still run — with no Airtable, Linear, Context7 or browser tools at all.
#   2. Claude credentials in jcode's shape: the sk-ant-oat token wrapped in the
#      claudeAiOauth JSON blob, plus the one-time consent that lets jcode use Claude
#      Code's native credentials.
#   3. features off. jcode's local embedding/memory subsystem costs ~270MB of peak RSS
#      and carries context between runs; the loop's only cross-cycle memory must stay
#      consensus.md.
if [ "${LOOP_HARNESS:-cli}" = "jcode" ] || [ "${LOOP_HARNESS_CODEX:-cli}" = "jcode" ]; then
    export JCODE_NO_TELEMETRY=1
    # Default to the PERSISTENT logs volume, not $HOME: the container filesystem is
    # replaced on every redeploy, and jcode's OpenAI credential is a FILE
    # (~/.jcode/openai-auth.json — there is no env-var equivalent the way there is for
    # Claude). On an ephemeral home, every redeploy would silently kill the openai
    # provider: the usage-limit fallback and the budget-offload path both go dead while
    # the loop keeps reporting healthy Claude cycles.
    JHOME="${JCODE_HOME:-/app/logs/.jcode}"
    export JCODE_HOME="$JHOME"
    # Guarded: under `set -e` an unguarded failure here exits the entrypoint, and the
    # entrypoint IS the container — one bad line becomes a restart loop (APP-235/240).
    mkdir -p "$JHOME" 2>/dev/null || echo "[entrypoint] WARNING: cannot create $JHOME" >&2
    chmod 700 "$JHOME" 2>/dev/null || true

    if python3 /app/scripts/core/jcode-mcp-config.py --src /app/.mcp.json --dest "$JHOME/mcp.json"; then
        echo "[entrypoint] jcode MCP config written"
    else
        echo "[entrypoint] WARNING: jcode MCP config generation FAILED — the loop's config-freshness gate will refuse this boot (a stale mcp.json cannot stand in; REVISE-2 gate B11)" >&2
    fi

    # NOTE: the loop no longer wraps the token here. The claudeAiOauth blob is built
    # inside each jcode subprocess (run_jcode_cycle) so the loop's own environment keeps
    # the RAW sk-ant-oat value. That is what makes the LOOP_HARNESS=cli rollback work
    # without a redeploy: the CLI needs the raw token, and a globally-wrapped blob would
    # have turned the rollback path into per-cycle 401s.

    # Idempotent: only append what is absent, never rewrite a config the operator or a
    # login flow has already shaped.
    grep -q claude_code_native_credentials "$JHOME/config.toml" 2>/dev/null || \
        printf '[auth]\ntrusted_external_sources = ["claude_code_native_credentials"]\n' >> "$JHOME/config.toml" 2>/dev/null || \
        echo "[entrypoint] WARNING: could not write $JHOME/config.toml (auth consent)" >&2
    grep -q '^\[features\]' "$JHOME/config.toml" 2>/dev/null || \
        printf '\n[features]\nmemory = false\nswarm = false\nmermaid = false\n\n[agents]\nmemory_sidecar_enabled = false\n' >> "$JHOME/config.toml" 2>/dev/null || \
        echo "[entrypoint] WARNING: could not write $JHOME/config.toml (features off)" >&2
fi

# --- autonomous loop (background so we can wait on both) ---
echo "[entrypoint] starting auto-loop (engine=${ENGINE:-claude} harness=${LOOP_HARNESS:-cli})"
export ENGINE="${ENGINE:-claude}"
export CLAUDE_PERMISSION_MODE="${CLAUDE_PERMISSION_MODE:-bypassPermissions}"
./scripts/core/auto-loop.sh &
LOOP_PID=$!

# --- if either process exits, tear the container down so the runtime restarts it ---
# `set -euo pipefail` (line 4) applies here, and `wait -n` is a simple command in
# non-conditional position: a NON-ZERO child exit kills this script instantly,
# before `_rc=$?` and before the naming block below -- and a `set -e` exit is
# silent, so nothing reaches `docker logs` either. That is why APP-240 could not
# name the culprit for three days: the diagnostic added in `a71afc6` only ever ran
# for a CLEAN (rc=0) child exit, which is not the failing case. Verified in the
# container's own bash 5.2.15: child rc=1 -> no diagnostic, script exits 1;
# child rc=0 -> diagnostic runs. Disarm set -e for exactly this one call.
set +e
wait -n "$DASH_PID" "$LOOP_PID"
_rc=$?
set -e
# Name the process that died. "a managed process exited" told us nothing, and the
# container has restarted 64 times today without us being able to say which side
# fell over (APP-240). Whichever pid is still alive is the survivor.
if kill -0 "$LOOP_PID" 2>/dev/null; then
    _dead="dashboard (python3 dashboard/server.py, pid $DASH_PID)"
elif kill -0 "$DASH_PID" 2>/dev/null; then
    _dead="auto-loop (scripts/core/auto-loop.sh, pid $LOOP_PID)"
else
    _dead="both processes"
fi
echo "[entrypoint] $_dead exited with rc=$_rc; stopping container"
# The loop logs to a file, not to stdout, so `docker logs` has never carried any
# context about what it was doing when it died. Echo its tail into the container
# log, which survives the restart and is what forensics actually reach for.
echo "[entrypoint] --- last 20 lines of logs/auto-loop.log ---"
tail -n 20 /app/logs/auto-loop.log 2>/dev/null | sed 's/^/[entrypoint]   /' || true
echo "[entrypoint] --- end of loop log tail ---"
term
wait || true
exit 1
