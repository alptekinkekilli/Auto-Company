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
    relation: uses
    description: Scans evidence whose hashes come from the canonical hash implementation.
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

Value-sensitive session-leak scanner for EKAP Bridge records, flagging only key-plus-value adjacencies (Set-Cookie: name=value, Authorization: Bearer <token>, named credential keys, populated localStorage dumps) while passing assurance sentences and public evidence fields. Five compiled regex rules; selftest with 2 negative + 6 positive fixtures exits 3 on any misbehavior (canary gate preventing trust after regression). Hardened 2026-07-29: auth headers matched only when followed by known scheme or opaque token, never bare prose.

## Related

- uses [[content-hash-provenance]] — Scans evidence whose hashes come from the canonical hash implementation.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
