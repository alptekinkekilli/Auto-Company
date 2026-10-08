---
name: State Snapshot & Delta
slug: state-snapshot-delta
type: concept
sources:
  - path: scripts/ops/state-snapshot.py
    hash: 3112f4632b64a6b531b215ea81ba82b2ceb6436942511f816de94ced3171bfe8
  - path: scripts/ops/work-window.py
    hash: 7b39b958c05be0d7242887ae4957cf7e6034f20990d587dbab31471a3365c92a
sources_digest: 5bd3576abebe22c135de576af436f030bf1dc7985bd34ea211e06706664eb2d0
links:
  - to: auto-company-ops-scripts
    relation: part_of
    description: state-snapshot.py is one of the advisory ops scripts.
  - to: fail-closed-operational-brakes
    relation: produces
    description: >-
      work-window.py consumes the DELTA line to decide whether a tracked surface
      changed and a work-window should open.
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
  - symbol: _app_dir
    kind: function
    at: 'scripts/ops/work-window.py:L44-L48'
  - symbol: _env_int
    kind: function
    at: 'scripts/ops/work-window.py:L51-L58'
  - symbol: _parse_delta
    kind: function
    at: 'scripts/ops/work-window.py:L61-L70'
  - symbol: _read_state
    kind: function
    at: 'scripts/ops/work-window.py:L73-L80'
  - symbol: _write_state
    kind: function
    at: 'scripts/ops/work-window.py:L83-L87'
  - symbol: _line
    kind: function
    at: 'scripts/ops/work-window.py:L90-L100'
  - symbol: main
    kind: function
    at: 'scripts/ops/work-window.py:L103-L160'
---
<!-- context:generated:start -->
## Summary

A one-call probe (state-snapshot.py) that collapses per-cycle state checks into a single turn, hashing five watched surfaces (directives, OPREQ ledger, Wowcar sources, decisions) and computing a DELTA against the previous snapshot. The DELTA semantics explicitly state that 'none' does not mean 'nothing to do' — standing orders still apply. It always exits 0 so a probe failure never kills the cycle, and implements OPREQ-INFRA-ANALYST-ROUTING-001 Option B by making the auditor report hash delta-visible.

## Related

- part of [[auto-company-ops-scripts]] — state-snapshot.py is one of the advisory ops scripts.
- produces [[fail-closed-operational-brakes]] — work-window.py consumes the DELTA line to decide whether a tracked surface changed and a work-window should open.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
