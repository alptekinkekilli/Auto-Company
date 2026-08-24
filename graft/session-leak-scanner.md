---
name: Session-leak scanner
slug: session-leak-scanner
type: file
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

Value-sensitive session-leak scanner for EKAP Bridge records, flagging only key-plus-value adjacencies while passing assurance sentences and public evidence fields. Selftest with embedded fixtures exits 3 on any regression (canary gate) so the scanner is never trusted after a regression.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
