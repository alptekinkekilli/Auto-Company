---
name: Autonomous Loop
slug: autonomous-loop
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 19f2148376589dba4de398b1ec4040b9419c62ea0a03089842cc8978b006f8b0
sources_digest: 0b7277763f7379a71ac05648532b143d79d145d71b19ad3b17f02fff588efdc0
links:
  - to: directive-writer
    relation: uses
    description: Consumes the standing directive written by directive_writer.py.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The 24/7 loop invoking Claude/Codex/jcode in fresh sessions, using consensus.md as relay baton and PROMPT.md as standing directive. Four-gate budget model (per-engine 5h, daily, weekly) with idempotent spend ledgers, optional tier ladder, tool denylist, guardrail verification, circuit breaker/cooldown/usage-limit wait, and an ERR trap for diagnosing silent set -e failures.

## Related

- uses [[directive-writer]] — Consumes the standing directive written by directive_writer.py.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
