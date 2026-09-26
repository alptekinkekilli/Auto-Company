---
name: auto-loop core engine
slug: auto-loop-core-engine
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: b3850b8050b576a46bfa19953ae0492889b603967275721a09344b9589552d56
sources_digest: 09399485c2e8e9c57d25cea9e3e3d4e9c22b720c86c8238a7c7a4b25e1fc5140
links:
  - to: escalation-one-shot-semantics
    relation: implements
  - to: idle-skip-mechanism
    relation: implements
  - to: mcp-config-sync-invariant
    relation: depends_on
  - to: mixed-harness-attribution
    relation: implements
  - to: prompt-transport-contract
    relation: implements
  - to: set-e-shape-lint
    relation: validates
  - to: tier-ladder-daily-budget
    relation: implements
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The central orchestration loop that drives per-cycle engine selection (claude/jcode/codex/cli), prompt assembly, escalation, tier ladder, idle skip, budget gates, and ledger writes. It is the highest-risk file in the repo: several tests extract its function bodies verbatim via awk to drive the shipping code, and it is the target of the APP-240 set -e incident and the prompt-assembly quote outage.

## Related

- implements [[escalation-one-shot-semantics]]
- implements [[idle-skip-mechanism]]
- depends on [[mcp-config-sync-invariant]]
- implements [[mixed-harness-attribution]]
- implements [[prompt-transport-contract]]
- validates [[set-e-shape-lint]]
- implements [[tier-ladder-daily-budget]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
