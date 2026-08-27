---
name: Value-Sensitive Leak Scanner
slug: value-sensitive-leak-scanner
type: concept
sources:
  - path: scripts/core/bridge_leak_scan.py
    hash: e5b7b7ecf614217b79e93037d780bdd0314f4953d8e6308939a49fe5b5b92bcf
sources_digest: b640af07b633d17a562a8a5f854a19c94a33c6169c66e46291f8978bc47e1945
links:
  - to: loop-driver
    relation: uses
    description: Used to scan EKAP Bridge records for session leaks during loop cycles.
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

A family of regex-based scanners that flag only key-plus-value adjacencies (Set-Cookie, Authorization Bearer, named credential keys, populated localStorage) while passing assurance sentences and public evidence fields. Each ships an embedded selftest that exits non-zero on any fixture regression, gating trust in the scanner itself — the same trust-gating pattern as directive-rule-sweep.

## Related

- uses [[loop-driver]] — Used to scan EKAP Bridge records for session leaks during loop cycles.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
