---
name: Autonomous Loop Orchestrator
slug: autonomous-loop-orchestrator
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 429ad6c9ab94694e7399685cf7b7f63d5d8c387141baef14d1adb065cdca6292
sources_digest: 903c7dcb6c440915b2bed1d5c8d80f286a371c253704e4713d742468a8760e27
links:
  - to: cockpit-dashboard
    relation: configures
    description: >-
      The dashboard's hold and directive controls feed the loop's state each
      cycle.
  - to: opportunity-analyst
    relation: uses
    description: >-
      The loop's analyst trigger uses a file-based ANALYST_RUN_REQUEST because
      the cockpit runs inside the app container and cannot start host-side cron
      containers.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The 24/7 loop that runs AI coding agents (Claude/Codex/jcode) in fresh sessions with memories/consensus.md as the relay baton. Implements a four-gate budget model (per-engine 5h, daily, weekly) with idempotent spend tracking, prompt guardrail verification, provider rate-limit detection, circuit breakers, and a tool denylist. Supports legacy cli and jcode harnesses with tier ladders and ROUTER_ALTERNATE quota-aware engine alternation.

## Related

- configures [[cockpit-dashboard]] — The dashboard's hold and directive controls feed the loop's state each cycle.
- uses [[opportunity-analyst]] — The loop's analyst trigger uses a file-based ANALYST_RUN_REQUEST because the cockpit runs inside the app container and cannot start host-side cron containers.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
