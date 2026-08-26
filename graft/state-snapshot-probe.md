---
name: State snapshot probe
slug: state-snapshot-probe
type: file
sources:
  - path: scripts/ops/state-snapshot.py
    hash: 3112f4632b64a6b531b215ea81ba82b2ceb6436942511f816de94ced3171bfe8
sources_digest: b49055f6ad2667278243a5d453a6f3a32f13b362f453588327ababae654d5019
links:
  - to: auto-loop-core-engine
    relation: produces
    description: 'The snapshot''s DELTA: none line drives idle detection in auto-loop.sh.'
  - to: operator-request-ledger
    relation: uses
    description: Parses open OPREQ-* blocks from memories/operator-requests.md.
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

A one-call read-only probe that collapses per-cycle state checks into a single grep-friendly report of five watched surfaces (directive status, open OPREQ blocks, auditor report hash, Wowcar source hash, operator-decisions hash) plus a DELTA line against the previous snapshot. Always exits 0 so a probe failure never kills the calling cycle; errored fields print as ERROR and are excluded from DELTA on both sides.

## Related

- produces [[auto-loop-core-engine]] — The snapshot's DELTA: none line drives idle detection in auto-loop.sh.
- uses [[operator-request-ledger]] — Parses open OPREQ-* blocks from memories/operator-requests.md.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
