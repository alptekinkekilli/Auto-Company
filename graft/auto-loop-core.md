---
name: auto-loop core
slug: auto-loop-core
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: b8f8a3989fee29f5a561d7f4d4eb8f558086586d603c5217caf20288b84d27ec
sources_digest: 9acc0249ddcf7d53dc97c65117d01ec63059f34e1003f3864d7b48ce6de9355a
links:
  - to: budget-spend-accounting
    relation: part_of
    description: >-
      Budget gates, spend ledger, ccusage fail-closed logic, and cycle counter
      all live inside auto-loop.sh.
  - to: mcp-config-probe
    relation: configures
    description: >-
      auto-loop.sh holds the JCODE_MCP_CONFIG_REQUIRED preflight list and
      OPREQ-A invariant that airtable/linear are absent from loop config.
  - to: ops-probe-audit-scripts
    relation: produces
    description: >-
      Writes logs/cycle-ndjson, logs/.jcode, memories/*, and runtime.env that
      the probes parse.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The central orchestration script that runs each cycle: seeds the monotonic cycle counter, selects the engine (claude→jcode vs codex→cli), applies budget gates and spend accounting, handles idle-skip, escalation, and operator-request notification, and writes cycle metadata. It is the protected production surface that many tests extract functions from verbatim via awk.

## Related

- part of [[budget-spend-accounting]] — Budget gates, spend ledger, ccusage fail-closed logic, and cycle counter all live inside auto-loop.sh.
- configures [[mcp-config-probe]] — auto-loop.sh holds the JCODE_MCP_CONFIG_REQUIRED preflight list and OPREQ-A invariant that airtable/linear are absent from loop config.
- produces [[ops-probe-audit-scripts]] — Writes logs/cycle-ndjson, logs/.jcode, memories/*, and runtime.env that the probes parse.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
