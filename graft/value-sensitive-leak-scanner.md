---
name: Value-Sensitive Leak Scanner
slug: value-sensitive-leak-scanner
type: file
sources:
  - path: scripts/core/bridge_leak_scan.py
    hash: e5b7b7ecf614217b79e93037d780bdd0314f4953d8e6308939a49fe5b5b92bcf
sources_digest: b640af07b633d17a562a8a5f854a19c94a33c6169c66e46291f8978bc47e1945
links:
  - to: opportunity-analyst
    relation: uses
    description: >-
      Scans analyst session output for leaked credentials before they are
      persisted.
generator:
  version: 1
covers:
  - symbol: scan
    kind: function
    at: 'scripts/core/bridge_leak_scan.py:L63-L69'
  - symbol: selftest
    kind: function
    at: 'scripts/core/bridge_leak_scan.py:L98-L111'
  - symbol: main
    kind: function
    at: 'scripts/core/bridge_leak_scan.py:L114-L127'
---
<!-- context:generated:start -->
## Summary

A session-leak scanner for EKAP Bridge records that flags only key-plus-value adjacencies (Set-Cookie, Authorization Bearer, named credential keys, populated localStorage dumps) while passing assurance sentences and public evidence fields. Has a selftest gate that exits 3 if any fixture misbehaves, refusing to be trusted after a regression — the same trust-gating pattern as directive-rule-sweep.

## Related

- uses [[opportunity-analyst]] — Scans analyst session output for leaked credentials before they are persisted.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
