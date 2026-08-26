---
name: Auto Loop
slug: auto-loop
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 30cc1c943819800a5516778d7d841255d14720019a6bce081cc5b2d730631e64
sources_digest: b464e67c211c1ff1554e0643aab744e36fe30b6a947596c4b5e9785a9170c824
links:
  - to: directive-writer
    relation: depends_on
    description: >-
      Tripwire fails closed if human-directive.md changes without going through
      directive_writer.py.
  - to: opportunity-analyst
    relation: uses
    description: >-
      Invokes the analyst's report and promotion passes as part of the loop's
      decision flow.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The 24/7 orchestration loop that repeatedly invokes a CLI coding engine (Claude or Codex, via cli or jcode harness) in fresh sessions, using consensus.md as the cross-cycle relay and PROMPT.md as the standing instruction set. Implements budget gates (per-engine 5h, daily, weekly hard caps), a quota-aware router, tier ladder, circuit-breaker cooldowns, per-cycle timeouts, and a persistent spend ledger with idempotent run IDs. Fails closed if human-directive.md changes without the writer; its own fail-closed mechanisms are explicitly not security boundaries.

## Related

- depends on [[directive-writer]] — Tripwire fails closed if human-directive.md changes without going through directive_writer.py.
- uses [[opportunity-analyst]] — Invokes the analyst's report and promotion passes as part of the loop's decision flow.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
