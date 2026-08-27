---
name: Auto-loop core engine
slug: auto-loop-core-engine
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: b8f8a3989fee29f5a561d7f4d4eb8f558086586d603c5217caf20288b84d27ec
sources_digest: 9acc0249ddcf7d53dc97c65117d01ec63059f34e1003f3864d7b48ce6de9355a
links:
  - to: budget-spend-accounting
    relation: uses
  - to: cycle-metadata-cost-attribution
    relation: produces
  - to: mcp-configuration-probe
    relation: uses
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The central orchestration loop (scripts/core/auto-loop.sh) that drives autonomous cycles: cycle counter, budget gates, engine selection (claude→jcode vs codex→cli), escalation, idle-skip, and metadata extraction. Fail-closed on any unmeasurable state; caps bind on messages not firms; degraded reads never lower a prior observation.

## Related

- uses [[budget-spend-accounting]]
- produces [[cycle-metadata-cost-attribution]]
- uses [[mcp-configuration-probe]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
