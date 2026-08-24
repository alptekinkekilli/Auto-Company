---
name: Autonomous Loop
slug: autonomous-loop
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 19f2148376589dba4de398b1ec4040b9419c62ea0a03089842cc8978b006f8b0
sources_digest: 0b7277763f7379a71ac05648532b143d79d145d71b19ad3b17f02fff588efdc0
links:
  - to: cockpit-dashboard
    relation: configures
    description: >-
      The dashboard's hold/release and settings control this loop's state files
      and runtime.env.
  - to: opportunity-analyst
    relation: uses
    description: >-
      The loop's analyst trigger uses a file-based request because the cockpit
      runs inside the app container and cannot start host containers directly.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The 24/7 loop that continuously invokes the Claude/Codex/jcode CLI in fresh sessions, using memories/consensus.md as the relay baton and PROMPT.md as the standing directive. Implements a four-gate budget model (per-engine 5h, daily, weekly) with idempotent spend ledgers, an optional tier ladder for round-robin model selection, a tool denylist, guardrail verification of required prompt sections, a circuit breaker/cooldown, and an ERR trap for diagnosing silent set -e failures.

## Related

- configures [[cockpit-dashboard]] — The dashboard's hold/release and settings control this loop's state files and runtime.env.
- uses [[opportunity-analyst]] — The loop's analyst trigger uses a file-based request because the cockpit runs inside the app container and cannot start host containers directly.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
