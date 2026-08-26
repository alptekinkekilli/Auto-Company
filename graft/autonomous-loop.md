---
name: Autonomous Loop
slug: autonomous-loop
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 8047ae1ceb7eac76beba89e0584912e2500baee4f68bb2f372c872739a2c7193
sources_digest: 09490ff62dd4b45d3340d0b71341695ef1b4205f1305a986d18cf8036c7ab394
links:
  - to: container-entrypoint
    relation: depends_on
    description: >-
      Launched and supervised by docker-entrypoint.sh; consumes the boot-epoch
      stamp and runtime.env overrides.
  - to: directive-writer
    relation: uses
    description: >-
      The loop's directive promotion/restore paths route through
      directive_writer.py.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The core loop: a Bash script that continuously runs a CLI coding agent (Claude/Codex/jcode) in fresh sessions, using consensus.md as the cross-cycle relay and PROMPT.md as the standing instruction set. Enforces a four-gate budget model (per-engine 5h, daily, weekly) backed by an idempotent spend ledger, a tier ladder for cost spreading, strict guardrail verification of the source PROMPT.md, a jcode tool denylist, and a circuit breaker that disables Codex on permanent auth failures while distinguishing them from transient limits.

## Related

- depends on [[container-entrypoint]] — Launched and supervised by docker-entrypoint.sh; consumes the boot-epoch stamp and runtime.env overrides.
- uses [[directive-writer]] — The loop's directive promotion/restore paths route through directive_writer.py.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
