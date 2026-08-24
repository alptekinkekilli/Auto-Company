---
name: Autonomous loop
slug: autonomous-loop
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: b7375f132f3e571151b83d045a7716b07dc7f6fa9ea37d0788c49606d992f842
sources_digest: 4c6c77833f44a2de7965557f13f6803d56cd1b8d4453d991d55e0c715e787f33
links:
  - to: directive-writer
    relation: uses
    description: Writes/restores human-directive.md through the fail-closed writer.
  - to: opportunity-analyst-pipeline
    relation: uses
    description: Runs the analyst passes as part of the loop cycles.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

24/7 orchestration loop launching fresh Claude/Codex/jcode sessions with consensus.md as cross-cycle relay. Enforces four-gate budget model with idempotent spend ledgers, quota-aware engine router, circuit breaker, and JCODE_TOOLS_DENY denylist.

## Related

- uses [[directive-writer]] — Writes/restores human-directive.md through the fail-closed writer.
- uses [[opportunity-analyst-pipeline]] — Runs the analyst passes as part of the loop cycles.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
