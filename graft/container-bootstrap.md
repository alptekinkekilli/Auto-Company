---
name: Container Bootstrap
slug: container-bootstrap
type: system
sources:
  - path: docker-entrypoint.sh
    hash: fbc2010d8d1d9dda2bc7ebd72fba1d674136624f968ff2f453bf7bbb894de017
sources_digest: 4859f8b1dfb24f857df1d999107a7d92d7c4d14a2c247976ae81cbb021029d23
links:
  - to: autonomous-loop-orchestrator
    relation: produces
    description: Launches scripts/core/auto-loop.sh as a background process.
  - to: cockpit-dashboard
    relation: produces
    description: Launches dashboard/server.py as a background process.
  - to: sentry-reporter
    relation: uses
    description: Depends on sentry-heartbeat.sh for external liveness.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The PID-1 entrypoint that drops privileges to the app user, stamps a boot-epoch file for the loop's MCP-config freshness gate, applies operator overrides from runtime.env (parsed literally to avoid shell-special corruption), and launches the dashboard and auto-loop as background processes, restarting the container if either exits. Persists state across redeploys via symlinks and volume relocations, and seeds Codex auth only on first boot to avoid token-rotation 401s.

## Related

- produces [[autonomous-loop-orchestrator]] — Launches scripts/core/auto-loop.sh as a background process.
- produces [[cockpit-dashboard]] — Launches dashboard/server.py as a background process.
- uses [[sentry-reporter]] — Depends on sentry-heartbeat.sh for external liveness.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
