---
name: Container Entrypoint
slug: container-entrypoint
type: file
sources:
  - path: docker-entrypoint.sh
    hash: fbc2010d8d1d9dda2bc7ebd72fba1d674136624f968ff2f453bf7bbb894de017
sources_digest: 4859f8b1dfb24f857df1d999107a7d92d7c4d14a2c247976ae81cbb021029d23
links:
  - to: autonomous-loop
    relation: part_of
    description: Launches auto-loop.sh as a background process.
  - to: dashboard-server
    relation: part_of
    description: Launches dashboard/server.py as a background process.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

PID-1 bootstrap: drops privileges to app user via gosu, stamps boot-epoch for MCP-config freshness gate, applies operator overrides from runtime.env (parsed literally to avoid shell-special-char corruption), launches dashboard and auto-loop as background processes, waits on either to exit so container restarts. Persists state across redeploys via symlinks into memories volume; relocates CLAUDE_CONFIG_DIR/CODEX_HOME onto logs volume; seeds Codex auth only on first boot to avoid token-rotation 401s. set +e guard around wait -n; trap forwards TERM/INT to children.

## Related

- part of [[autonomous-loop]] — Launches auto-loop.sh as a background process.
- part of [[dashboard-server]] — Launches dashboard/server.py as a background process.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
