---
name: Sentry heartbeat & container status
slug: sentry-heartbeat-container-status
type: system
sources:
  - path: scripts/core/sentry-heartbeat.sh
    hash: 874eccbdbde7e82f3b3f97f023c1503321380b2c7a28754386d1fb7b366ac12f
  - path: scripts/linux/noop-action.sh
    hash: 0f0aaa7c6c79e6c7844c7528a253084811b9a9b7277f557a1a60a8011347f4d9
  - path: scripts/linux/status-linux.sh
    hash: 1dc4a455fe8ffdd5e1696608d50d02311afd701906d80ee26d5708374d3947d8
sources_digest: 7d54067efde1833ca1ad85a8ef62a01b08a1b6a11a78245975ed7ffaa96e0225
links:
  - to: auto-loop-orchestration
    relation: uses
    description: >-
      sentry-heartbeat.sh verifies the loop PID file liveness and is started by
      docker-entrypoint.sh.
  - to: dashboard-server
    relation: produces
    description: >-
      status-linux.sh output is parsed by parse_macos_status_output in
      dashboard/server.py.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Container-adapted health reporting: sentry-heartbeat.sh proves the process tree is alive independently of the dashboard/loop cycle (catches crash-loops APP-250 that app-level error reporting misses), reporting ok only if both dashboard /api/status and loop PID are alive to avoid false positives during restart storms (APP-240). status-linux.sh emits the same === Section === Key=Value format parse_macos_status_output expects, marking sleep guard not_applicable and assuming Coolify restart policy. noop-action.sh is a placeholder for Start/Stop controls in container mode so the dashboard never attempts macOS/launchd actions.

## Related

- uses [[auto-loop-orchestration]] — sentry-heartbeat.sh verifies the loop PID file liveness and is started by docker-entrypoint.sh.
- produces [[dashboard-server]] — status-linux.sh output is parsed by parse_macos_status_output in dashboard/server.py.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
