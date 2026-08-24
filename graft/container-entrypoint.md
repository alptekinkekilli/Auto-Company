---
name: Container Entrypoint
slug: container-entrypoint
type: system
sources:
  - path: docker-entrypoint.sh
    hash: fbc2010d8d1d9dda2bc7ebd72fba1d674136624f968ff2f453bf7bbb894de017
sources_digest: 4859f8b1dfb24f857df1d999107a7d92d7c4d14a2c247976ae81cbb021029d23
links:
  - to: autonomous-loop
    relation: produces
    description: Launches scripts/core/auto-loop.sh as a background process.
  - to: cockpit-dashboard
    relation: produces
    description: Launches dashboard/server.py as a background process.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

PID-1 bootstrap for the Auto-Company container: drops privileges to the app user via gosu, stamps a boot-epoch file for the loop's MCP-config freshness gate, applies operator overrides from runtime.env (parsed literally to avoid shell-special corruption), and launches the dashboard and auto-loop as background processes, restarting the container if either exits. Persists state across redeploys via symlinks into the memories/logs volumes, seeds Codex auth only on first boot, and provisions jcode's MCP config when the harness is jcode.

## Related

- produces [[autonomous-loop]] — Launches scripts/core/auto-loop.sh as a background process.
- produces [[cockpit-dashboard]] — Launches dashboard/server.py as a background process.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
