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
      Writes auto-loop.log and state files that the dashboard reads via
      /api/status.
  - to: directive-writer
    relation: uses
    description: >-
      Restores/guards human-directive.md via directive_writer.py during analyst
      runs.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The 24/7 autonomous driver running continuous work cycles via Claude/Codex/jcode CLIs, with consensus.md as the cross-cycle relay baton and PROMPT.md as standing law. Enforces a four-gate budget model, a circuit breaker on consecutive errors, usage-limit detection, and a jcode tool denylist that doubles as a context-budget lever. Persists state to logs and idempotent spend ledgers; an ERR trap with set -E records silent set -e deaths.

## Related

- produces [[cockpit-dashboard]] — Writes auto-loop.log and state files that the dashboard reads via /api/status.
- uses [[directive-writer]] — Restores/guards human-directive.md via directive_writer.py during analyst runs.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
