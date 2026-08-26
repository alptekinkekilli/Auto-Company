---
name: Bridge Leak Scanner
slug: bridge-leak-scanner
type: file
sources:
  - path: scripts/core/bridge_leak_scan.py
    hash: e5b7b7ecf614217b79e93037d780bdd0314f4953d8e6308939a49fe5b5b92bcf
sources_digest: b640af07b633d17a562a8a5f854a19c94a33c6169c66e46291f8978bc47e1945
links:
  - to: content-hash-provenance
    relation: validates
    description: Scans bridge records including content_hash evidence fields.
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

Value-sensitive session-leak scanner for EKAP Bridge records, flagging only key-plus-value adjacencies (Set-Cookie: name=value, Authorization: Bearer <token>, named credential keys, populated localStorage dumps) while passing assurance sentences and public evidence fields. Has a selftest with two negative and six positive fixtures that exits 3 on any misbehavior — a canary gate preventing the scanner from being trusted after a regression. Authorization headers are matched only when followed by a known scheme or opaque token of credential length, never by bare prose, to avoid recreating a word-presence false positive.

## Related

- validates [[content-hash-provenance]] — Scans bridge records including content_hash evidence fields.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
