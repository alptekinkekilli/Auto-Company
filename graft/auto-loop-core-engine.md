---
name: Auto-loop core engine
slug: auto-loop-core-engine
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 30cc1c943819800a5516778d7d841255d14720019a6bce081cc5b2d730631e64
sources_digest: b464e67c211c1ff1554e0643aab744e36fe30b6a947596c4b5e9785a9170c824
links:
  - to: budget-spend-accounting
    relation: uses
    description: >-
      auto-loop.sh calls evaluate_budget_gates, record_total_spend,
      _codex_spend_since, and codex_ledger_spend_since to gate and record spend.
  - to: cycle-metadata-extraction
    relation: uses
    description: >-
      extract_cycle_metadata() parses engine output into
      CYCLE_TYPE/SUBTYPE/RESULT_TEXT.
  - to: prod-mechanism-guard
    relation: validates
    description: >-
      auto-loop.sh is a protected path that prod-mechanism-guard.py blocks edits
      to without an approval marker.
  - to: prompt-transport-assembly
    relation: uses
    description: auto-loop.sh assembles FULL_PROMPT and passes it to engine CLIs via STDIN.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The central orchestration loop that drives autonomous cycles: selects an engine (claude/jcode, codex/cli), applies budget gates, idle-skip, escalation, and prompt assembly, then runs the cycle and records spend/metadata. It is the single most protected surface in the repo and the target of most regression tests.

## Related

- uses [[budget-spend-accounting]] — auto-loop.sh calls evaluate_budget_gates, record_total_spend, _codex_spend_since, and codex_ledger_spend_since to gate and record spend.
- uses [[cycle-metadata-extraction]] — extract_cycle_metadata() parses engine output into CYCLE_TYPE/SUBTYPE/RESULT_TEXT.
- validates [[prod-mechanism-guard]] — auto-loop.sh is a protected path that prod-mechanism-guard.py blocks edits to without an approval marker.
- uses [[prompt-transport-assembly]] — auto-loop.sh assembles FULL_PROMPT and passes it to engine CLIs via STDIN.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
