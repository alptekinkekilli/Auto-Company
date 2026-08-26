---
name: Auto-loop core engine
slug: auto-loop-core-engine
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 376e5c5d4935009b140ead228b3ca323f3084a991e38f8961a9a9b045cf54ddb
sources_digest: 7454b13d037f0452d6e70bc9cfe60936ccc83ecee56b7661a84c43c98821179c
links:
  - to: budget-spend-accounting
    relation: uses
    description: >-
      evaluate_budget_gates, record_total_spend, _codex_spend_since,
      codex_ledger_spend_since are extracted and tested by the budget suites.
  - to: cycle-metadata-extraction
    relation: uses
    description: >-
      extract_cycle_metadata() and codex-final-text.py parse engine output into
      CYCLE_TYPE/SUBTYPE/RESULT_TEXT.
  - to: prod-mechanism-guard
    relation: part_of
    description: auto-loop.sh is a protected surface blocked by the PreToolUse hook.
  - to: state-snapshot-probe
    relation: uses
    description: >-
      Idle detection reads the snapshot's DELTA: none line to decide whether to
      skip a cycle.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The central orchestration loop (scripts/core/auto-loop.sh) that drives per-cycle engine selection, budget gates, cycle counter, idle-skip, escalation, prompt assembly/transport, and metadata extraction. It is the single most protected surface in the repo; many tests extract its functions verbatim via awk to drive the shipping code rather than copies.

## Related

- uses [[budget-spend-accounting]] — evaluate_budget_gates, record_total_spend, _codex_spend_since, codex_ledger_spend_since are extracted and tested by the budget suites.
- uses [[cycle-metadata-extraction]] — extract_cycle_metadata() and codex-final-text.py parse engine output into CYCLE_TYPE/SUBTYPE/RESULT_TEXT.
- part of [[prod-mechanism-guard]] — auto-loop.sh is a protected surface blocked by the PreToolUse hook.
- uses [[state-snapshot-probe]] — Idle detection reads the snapshot's DELTA: none line to decide whether to skip a cycle.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
