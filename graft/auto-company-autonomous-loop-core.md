---
name: Auto Company autonomous loop core
slug: auto-company-autonomous-loop-core
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 19f2148376589dba4de398b1ec4040b9419c62ea0a03089842cc8978b006f8b0
sources_digest: 0b7277763f7379a71ac05648532b143d79d145d71b19ad3b17f02fff588efdc0
links:
  - to: directive-writer-and-promotion-gate
    relation: uses
    description: >-
      The loop's guardrail checks and directive handling rely on
      directive_writer.py's fail-closed write/status/restore semantics.
  - to: engine-usage-cost-adapter
    relation: uses
    description: >-
      Budget/ledger helpers price jcode token output via engine-usage-cost.py to
      enforce spend gates.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The 24/7 autonomous loop that repeatedly invokes the Claude/Codex/jcode CLI in fresh sessions, using memories/consensus.md as the relay baton and PROMPT.md as the standing directive. Enforces a four-gate budget model (per-engine 5h, daily, weekly) with idempotent spend ledgers, a tool denylist, guardrail verification, circuit breaker/cooldown, and an ERR trap for silent set -e failures.

## Related

- uses [[directive-writer-and-promotion-gate]] — The loop's guardrail checks and directive handling rely on directive_writer.py's fail-closed write/status/restore semantics.
- uses [[engine-usage-cost-adapter]] — Budget/ledger helpers price jcode token output via engine-usage-cost.py to enforce spend gates.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
