---
name: auto-loop core loop
slug: auto-loop-core-loop
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 19f2148376589dba4de398b1ec4040b9419c62ea0a03089842cc8978b006f8b0
sources_digest: 0b7277763f7379a71ac05648532b143d79d145d71b19ad3b17f02fff588efdc0
links:
  - to: budget-spend-accounting
    relation: uses
    description: >-
      auto-loop calls evaluate_budget_gates, apply_tier_ladder,
      record_total_spend, _codex_spend_since, codex_ledger_spend_since to gate
      and record spend.
  - to: cycle-metadata-extraction
    relation: uses
    description: >-
      extract_cycle_metadata() and _cycle_ran_on_codex() parse engine output
      into CYCLE_TYPE/CYCLE_SUBTYPE/RESULT_TEXT.
  - to: escalation-operator-requests
    relation: uses
    description: >-
      apply_cycle_escalation() consumes one-shot operator escalations;
      _offhours_logged and idle-skip interact with operator_request_notify.
  - to: ops-scripts
    relation: uses
    description: >-
      auto-loop invokes state-snapshot, idle-skip-note, operator_request_notify,
      and other ops scripts during each cycle.
  - to: prompt-assembly-transport
    relation: uses
    description: >-
      auto-loop assembles FULL_PROMPT and passes it to engine CLIs via
      run_claude_cycle_cli/run_codex_cycle_cli/run_jcode_cycle.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The central orchestration loop (scripts/core/auto-loop.sh) that drives autonomous cycles: selects an engine (claude/jcode vs codex/cli), applies budget gates and tier ladders, assembles the prompt, transports it to the engine CLI, records spend and cycle metadata, and handles idle-skip, escalation, and off-hours polling. It is the single most safety-critical file in the repo; many tests extract its functions verbatim via awk to drive the shipping code rather than a copy.

## Related

- uses [[budget-spend-accounting]] — auto-loop calls evaluate_budget_gates, apply_tier_ladder, record_total_spend, _codex_spend_since, codex_ledger_spend_since to gate and record spend.
- uses [[cycle-metadata-extraction]] — extract_cycle_metadata() and _cycle_ran_on_codex() parse engine output into CYCLE_TYPE/CYCLE_SUBTYPE/RESULT_TEXT.
- uses [[escalation-operator-requests]] — apply_cycle_escalation() consumes one-shot operator escalations; _offhours_logged and idle-skip interact with operator_request_notify.
- uses [[ops-scripts]] — auto-loop invokes state-snapshot, idle-skip-note, operator_request_notify, and other ops scripts during each cycle.
- uses [[prompt-assembly-transport]] — auto-loop assembles FULL_PROMPT and passes it to engine CLIs via run_claude_cycle_cli/run_codex_cycle_cli/run_jcode_cycle.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
