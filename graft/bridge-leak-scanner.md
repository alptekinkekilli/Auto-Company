---
name: Bridge leak scanner
slug: bridge-leak-scanner
type: system
sources:
  - path: scripts/core/bridge_leak_scan.py
    hash: e5b7b7ecf614217b79e93037d780bdd0314f4953d8e6308939a49fe5b5b92bcf
sources_digest: b640af07b633d17a562a8a5f854a19c94a33c6169c66e46291f8978bc47e1945
links:
  - to: content-hash-provenance
    relation: uses
    description: >-
      Passes content_hash fields as public evidence rather than flagging them as
      leaks.
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

Value-sensitive session-leak scanner for EKAP Bridge records that flags only key-plus-value adjacencies (Set-Cookie, Authorization Bearer, named credential keys, localStorage dumps) while passing assurance sentences and public evidence fields. Embeds a selftest canary gate (exit 3 on fixture failure) so the scanner is never trusted after a regression, and deliberately avoids the original word-presence false positive by requiring a known scheme or credential-length opaque token after 'authorization'.

## Related

- uses [[content-hash-provenance]] — Passes content_hash fields as public evidence rather than flagging them as leaks.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
