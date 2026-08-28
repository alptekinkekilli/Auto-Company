---
name: Auto Loop
slug: auto-loop
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 332728052d5c8e3d8dbb64ca1d391062fc22c656cdb0a87d5e258b4f688d6103
sources_digest: e83a8e8032c2bc43a843b2b950aa2034327797a2081555c358b8a4ed9f508ec7
links:
  - to: cockpit-dashboard
    relation: produces
    description: Writes the state files and ledgers the dashboard reads via /api/status.
  - to: container-entrypoint
    relation: depends_on
    description: >-
      Launched by the entrypoint; its boot-epoch stamp gates the MCP-config
      freshness check.
  - to: directive-writer
    relation: uses
    description: Restores/snapshots human-directive.md through directive_writer.py.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The 24/7 autonomous loop that keeps a CLI engine (Claude/Codex/jcode) running in fresh sessions, using memories/consensus.md as the relay baton between cycles. Enforces a four-gate budget model, alternate routing and tier ladders, and a JCODE_TOOLS_DENY denylist that trims context and blocks destructive MCP tools while keeping read tools.

## Related

- produces [[cockpit-dashboard]] — Writes the state files and ledgers the dashboard reads via /api/status.
- depends on [[container-entrypoint]] — Launched by the entrypoint; its boot-epoch stamp gates the MCP-config freshness check.
- uses [[directive-writer]] — Restores/snapshots human-directive.md through directive_writer.py.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
