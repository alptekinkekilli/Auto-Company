---
name: Autonomous Loop
slug: autonomous-loop
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: b8f8a3989fee29f5a561d7f4d4eb8f558086586d603c5217caf20288b84d27ec
sources_digest: 9acc0249ddcf7d53dc97c65117d01ec63059f34e1003f3864d7b48ce6de9355a
links:
  - to: cockpit-server
    relation: produces
    description: >-
      Writes auto-loop.log, spend ledgers, and PID/state files that server.py
      reads via its 256KB tail window.
  - to: container-entrypoint
    relation: part_of
    description: Launched as a background process by docker-entrypoint.sh.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

24/7 autonomous driver running continuous work cycles by invoking Claude CLI, Codex CLI, or the unified jcode Rust harness. Each cycle starts a fresh session reading memories/consensus.md as the cross-cycle relay baton and PROMPT.md as standing law. Enforces a four-gate budget model (per-engine 5h, daily, weekly hard gates over notional usage per APP-263), a circuit breaker on consecutive errors, usage-limit detection, and a jcode tool denylist that doubles as a context-budget lever (each advertised tool costs ~540 prompt tokens per turn). ERR trap with set -E records silent set -e deaths (APP-240); guardrail verification checks PROMPT.md itself rather than only the assembled prompt because consensus.md is model-rewritten and could mask a deleted section; Codex auth failure requires both non-zero exit and an auth phrase to avoid false positives from transcript prose.

## Related

- produces [[cockpit-server]] — Writes auto-loop.log, spend ledgers, and PID/state files that server.py reads via its 256KB tail window.
- part of [[container-entrypoint]] — Launched as a background process by docker-entrypoint.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
