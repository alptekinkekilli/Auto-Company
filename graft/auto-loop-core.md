---
name: auto-loop core
slug: auto-loop-core
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: f3e965e3aed59b32903f95d8be2954d7b966aa422c82a10fa581359fd906bb0b
sources_digest: 37ab20fc08031b66afd3689d1156671eff37d4ad8b4d6b223063c5bb09234e8f
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
