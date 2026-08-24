---
name: Value-sensitive leak scanning
slug: value-sensitive-leak-scanning
type: system
sources:
  - path: scripts/core/bridge_leak_scan.py
    hash: e5b7b7ecf614217b79e93037d780bdd0314f4953d8e6308939a49fe5b5b92bcf
sources_digest: b640af07b633d17a562a8a5f854a19c94a33c6169c66e46291f8978bc47e1945
links: []
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

A scanner that flags only key-plus-value adjacencies (Set-Cookie, Authorization Bearer, named credential keys, populated localStorage dumps) in EKAP Bridge records while passing assurance sentences and public evidence fields. Includes an embedded selftest that exits 3 if any fixture misbehaves, gating trust in the scanner after a regression. Deliberately hardened to avoid the original word-presence false positive by matching auth headers only when followed by a known scheme or opaque token.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
