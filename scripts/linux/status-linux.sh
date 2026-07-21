#!/usr/bin/env bash
# ============================================================
# Auto Company — Linux / container Status Report for Dashboard
# ============================================================
# Emits the same "=== Section ===" + Key=Value format the dashboard
# parser expects (see parse_macos_status_output in dashboard/server.py),
# adapted for a container where the loop is the main process and there is
# no launchd/caffeinate.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_DIR="$PROJECT_DIR/logs"
STATE_FILE="$PROJECT_DIR/.auto-loop-state"
PID_FILE="$PROJECT_DIR/.auto-loop.pid"
CONSENSUS_FILE="$PROJECT_DIR/memories/consensus.md"

loop_pid=""
if [ -f "$PID_FILE" ]; then
    loop_pid="$(cat "$PID_FILE" 2>/dev/null || true)"
fi

loop_running=false
if [ -n "$loop_pid" ] && kill -0 "$loop_pid" 2>/dev/null; then
    loop_running=true
fi

echo "=== Guardian ==="
# No sleep guard needed in a container (the host is always awake).
echo "State=not_applicable"
echo "Raw=Container runtime — no sleep guard needed"

echo ""
echo "=== Daemon ==="
# In a container the loop IS the always-on process (managed by the runtime).
if [ "$loop_running" = true ]; then
    echo "State=active"
    echo "MainPID=$loop_pid"
    echo "Raw=Container process (auto-loop)"
else
    echo "State=inactive"
    echo "Raw=Loop process not running"
fi

echo ""
echo "=== Autostart ==="
echo "State=configured"
echo "Raw=Container restart policy (Coolify)"

echo ""
echo "=== Loop ==="
if [ "$loop_running" = true ]; then
    echo "State=running"
    echo "Pid=$loop_pid"
    echo "Raw=Loop running"
elif [ -n "$loop_pid" ]; then
    echo "State=stopped"
    echo "Raw=Loop stopped (stale PID $loop_pid)"
else
    echo "State=stopped"
    echo "Raw=Loop not running"
fi

echo ""
echo "=== State File ==="
if [ -f "$STATE_FILE" ]; then
    cat "$STATE_FILE"
fi

echo ""
echo "=== Latest Consensus ==="
if [ -f "$CONSENSUS_FILE" ]; then
    head -30 "$CONSENSUS_FILE"
else
    echo "(no consensus file)"
fi

echo ""
echo "=== Recent Log ==="
if [ -f "$LOG_DIR/auto-loop.log" ]; then
    tail -20 "$LOG_DIR/auto-loop.log"
else
    echo "(no log file)"
fi
