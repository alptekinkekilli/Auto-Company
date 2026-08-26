---
name: Auto-loop core engine
slug: auto-loop-core-engine
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: bc00d41b28222e0836508c4e1674f4e8146364f9a8d8e3a35fcf4c4a3e67f1f6
sources_digest: 2a434563773d52689cea1c99c376307922ef71ecfe3b855098543da135bccbda
links:
  - to: budget-spend-accounting
    relation: uses
    description: >-
      evaluate_budget_gates, record_total_spend, and ccusage reads gate each
      cycle
  - to: prompt-transport-contract
    relation: implements
    description: >-
      run_claude_cycle_cli/run_codex_cycle_cli pass prompts via STDIN;
      run_jcode_cycle refuses oversized prompts
  - to: state-snapshot-probe
    relation: uses
    description: reads the DELTA line from state-snapshot.py to decide idle-skip
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The central orchestration loop that runs each cycle: selects an engine (claude/jcode/codex), assembles the prompt, enforces budget gates, handles idle-skip, escalation, and metadata extraction. Most other scripts are probes or hooks that feed or guard this loop.

## Related

- uses [[budget-spend-accounting]] — evaluate_budget_gates, record_total_spend, and ccusage reads gate each cycle
- implements [[prompt-transport-contract]] — run_claude_cycle_cli/run_codex_cycle_cli pass prompts via STDIN; run_jcode_cycle refuses oversized prompts
- uses [[state-snapshot-probe]] — reads the DELTA line from state-snapshot.py to decide idle-skip
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
