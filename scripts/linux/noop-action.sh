#!/usr/bin/env bash
# In container mode the loop is the container's main process — start/stop are
# managed by the container runtime (Coolify), not by the dashboard. This script
# is a safe no-op so the dashboard Start/Stop buttons report a message instead
# of trying to run macOS/launchd actions.
echo "Container mode: the loop is managed by the runtime."
echo "Use Coolify to stop / restart / redeploy this application."
exit 0
