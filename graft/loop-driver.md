---
name: Loop Driver
slug: loop-driver
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: b8f8a3989fee29f5a561d7f4d4eb8f558086586d603c5217caf20288b84d27ec
sources_digest: 9acc0249ddcf7d53dc97c65117d01ec63059f34e1003f3864d7b48ce6de9355a
links:
  - to: cockpit-dashboard
    relation: produces
    description: >-
      Writes auto-loop.log and state files that the dashboard's /api/status
      reads.
  - to: opportunity-analyst
    relation: uses
    description: >-
      The analyst runner and loop share the directive/consensus state files and
      the directive_writer guardrail.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The 24/7 autonomous driver that runs continuous work cycles via the Claude CLI, Codex CLI, or the unified jcode harness, with each cycle starting a fresh session that reads consensus.md as the cross-cycle relay baton and PROMPT.md as standing law. Enforces a four-gate budget model (per-engine 5h, daily, weekly hard gates), a circuit breaker on consecutive errors, usage-limit detection, and a jcode tool denylist that doubles as a context-budget lever. Persists state to auto-loop.log, idempotent spend ledgers, and PID/state files.

## Related

- produces [[cockpit-dashboard]] — Writes auto-loop.log and state files that the dashboard's /api/status reads.
- uses [[opportunity-analyst]] — The analyst runner and loop share the directive/consensus state files and the directive_writer guardrail.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
