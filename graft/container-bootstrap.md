---
name: Container Bootstrap
slug: container-bootstrap
type: system
sources:
  - path: docker-entrypoint.sh
    hash: fbc2010d8d1d9dda2bc7ebd72fba1d674136624f968ff2f453bf7bbb894de017
sources_digest: 4859f8b1dfb24f857df1d999107a7d92d7c4d14a2c247976ae81cbb021029d23
links:
  - to: cockpit-dashboard
    relation: produces
    description: Launches dashboard/server.py as a background process.
  - to: loop-driver
    relation: produces
    description: Launches scripts/core/auto-loop.sh as a background process.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

PID-1 entrypoint that drops privileges via gosu, stamps a boot-epoch file for the MCP freshness gate, applies operator overrides from runtime.env (parsed literally to avoid shell-special-char corruption), and launches the dashboard and loop as background children, restarting the container if either exits. Persists state across redeploys via symlinks and volume relocation, seeds Codex auth only on first boot, and forwards TERM/INT to all children.

## Related

- produces [[cockpit-dashboard]] — Launches dashboard/server.py as a background process.
- produces [[loop-driver]] — Launches scripts/core/auto-loop.sh as a background process.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
