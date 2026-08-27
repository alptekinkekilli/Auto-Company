---
name: State snapshot & directive hashing
slug: state-snapshot-directive-hashing
type: system
sources:
  - path: scripts/ops/state-snapshot.py
    hash: 3112f4632b64a6b531b215ea81ba82b2ceb6436942511f816de94ced3171bfe8
  - path: tests/test_idle_skip.sh
    hash: 13ce9f0b8801b94a1bc896bd2db53f2fc68c2984b45db8372050ca760e1edb53
sources_digest: 862c4befc1b02d528aa7f80eeb41264ef3d2b8c908e73a9b65b879fd8307f1ed
links:
  - to: auto-loop-core-engine
    relation: uses
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

state-snapshot.py hashes watched surfaces (directives, OPREQ ledger, Wowcar sources) into a compact report with a DELTA line; the auditor report hash is delta-visible per OPREQ-INFRA-ANALYST-ROUTING-001 Option B. Advisory and read-only toward the world, always exits 0.

## Related

- uses [[auto-loop-core-engine]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
