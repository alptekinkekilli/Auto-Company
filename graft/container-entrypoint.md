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
    relation: uses
    description: Launches scripts/core/auto-loop.sh as a background process.
  - to: cockpit-server
    relation: uses
    description: Launches dashboard/server.py as a background process.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

PID-1 bootstrap: drops privileges via gosu, stamps boot-epoch for the MCP-config freshness gate, applies operator overrides from runtime.env (parsed literally to avoid shell-special-char corruption), launches dashboard and auto-loop as background processes, waiting on either to exit so the container restarts. Persists state across redeploys via symlinks and volume relocations; seeds Codex auth only on first boot to avoid token-rotation 401s. set +e guard around wait -n so a non-zero child exit still names the dead process.

## Related

- uses [[autonomous-loop]] — Launches scripts/core/auto-loop.sh as a background process.
- uses [[cockpit-server]] — Launches dashboard/server.py as a background process.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
