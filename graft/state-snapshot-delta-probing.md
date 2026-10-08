---
name: State snapshot & delta probing
slug: state-snapshot-delta-probing
type: system
sources:
  - path: scripts/ops/state-snapshot.py
    hash: 3112f4632b64a6b531b215ea81ba82b2ceb6436942511f816de94ced3171bfe8
sources_digest: b49055f6ad2667278243a5d453a6f3a32f13b362f453588327ababae654d5019
links:
  - to: turn-economics-auditing
    relation: uses
    description: The snapshot's directive hashes feed the per-cycle audit surfaces.
  - to: work-window-bloat-brakes
    relation: produces
    description: >-
      Emits the DELTA line that work-window.py consumes to open/close its
      window.
generator:
  version: 1
covers:
  - symbol: file_sha16
    kind: function
    at: 'scripts/ops/state-snapshot.py:L54-L61'
  - symbol: directive_state
    kind: function
    at: 'scripts/ops/state-snapshot.py:L64-L72'
  - symbol: opreq_open
    kind: function
    at: 'scripts/ops/state-snapshot.py:L75-L87'
  - symbol: wowcar_sources
    kind: function
    at: 'scripts/ops/state-snapshot.py:L90-L104'
  - symbol: main
    kind: function
    at: 'scripts/ops/state-snapshot.py:L107-L166'
---
<!-- context:generated:start -->
## Summary

state-snapshot.py collapses per-cycle state checks into one grep-friendly probe of five surfaces (directive status, open OPREQ blocks, auditor report hash, Wowcar source tree hash, operator decisions), computing a DELTA against the previous snapshot so an unchanged world can be dismissed. Always exits 0 so a probe failure never kills the cycle; errored fields print ERROR and are excluded from delta comparison. Implements OPREQ-INFRA-ANALYST-ROUTING-001 Option B by making the auditor report hash delta-visible.

## Related

- uses [[turn-economics-auditing]] — The snapshot's directive hashes feed the per-cycle audit surfaces.
- produces [[work-window-bloat-brakes]] — Emits the DELTA line that work-window.py consumes to open/close its window.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
