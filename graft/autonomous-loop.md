---
name: Autonomous Loop
slug: autonomous-loop
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: bc00d41b28222e0836508c4e1674f4e8146364f9a8d8e3a35fcf4c4a3e67f1f6
sources_digest: 2a434563773d52689cea1c99c376307922ef71ecfe3b855098543da135bccbda
links:
  - to: directive-writer
    relation: uses
    description: >-
      Fail-closed tripwire on human-directive.md changes; directive_writer.py is
      the sole writer of that file.
  - to: opportunity-analyst
    relation: uses
    description: >-
      The analyst runs inside the loop's container as user app with CODEX_HOME
      on a persistent volume.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The 24/7 operator loop that repeatedly launches fresh Claude/Codex/jcode sessions with consensus.md as the cross-cycle relay, enforcing a four-gate budget model (per-engine 5h, daily, weekly) backed by an idempotent TOTAL_SPEND_LEDGER keyed on run_id. Quota-aware router alternates engines, tier ladder for model/effort selection, circuit-breaking on consecutive errors, watchdog timeout per cycle. ERR trap with set -E diagnoses silent set -e deaths; jcode tool denylist serves both safety and context-budget (each denied tool saves ~540 prompt tokens per turn); fail-closed tripwire on human-directive.md changes.

## Related

- uses [[directive-writer]] — Fail-closed tripwire on human-directive.md changes; directive_writer.py is the sole writer of that file.
- uses [[opportunity-analyst]] — The analyst runs inside the loop's container as user app with CODEX_HOME on a persistent volume.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
