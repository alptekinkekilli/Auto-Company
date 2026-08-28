---
name: Container Entrypoint
slug: container-entrypoint
type: system
sources:
  - path: docker-entrypoint.sh
    hash: fbc2010d8d1d9dda2bc7ebd72fba1d674136624f968ff2f453bf7bbb894de017
sources_digest: 4859f8b1dfb24f857df1d999107a7d92d7c4d14a2c247976ae81cbb021029d23
links:
  - to: auto-loop
    relation: produces
    description: Launches scripts/core/auto-loop.sh as a background process.
  - to: auto-loop
    relation: configures
    description: >-
      Applies runtime.env overrides and stamps boot-epoch for the MCP-config
      freshness gate.
  - to: cockpit-dashboard
    relation: produces
    description: Launches dashboard/server.py as a background process.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

PID-1 bootstrap that drops privileges via gosu, stamps the boot-epoch file for the MCP freshness gate, applies operator overrides from runtime.env (parsed literally to avoid shell-special-char corruption), and launches the dashboard and auto-loop as background processes, restarting the container if either exits. Persists state across redeploys via symlinks and volume relocations, and seeds Codex auth only on first boot to avoid token-rotation 401s.

## Related

- produces [[auto-loop]] — Launches scripts/core/auto-loop.sh as a background process.
- configures [[auto-loop]] — Applies runtime.env overrides and stamps boot-epoch for the MCP-config freshness gate.
- produces [[cockpit-dashboard]] — Launches dashboard/server.py as a background process.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
