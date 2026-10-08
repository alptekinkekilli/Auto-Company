---
name: Session-leak scanner (bridge_leak_scan)
slug: session-leak-scanner-bridge-leak-scan
type: file
sources:
  - path: scripts/core/bridge_leak_scan.py
    hash: e5b7b7ecf614217b79e93037d780bdd0314f4953d8e6308939a49fe5b5b92bcf
sources_digest: b640af07b633d17a562a8a5f854a19c94a33c6169c66e46291f8978bc47e1945
links:
  - to: trust-gating-canary-pattern
    relation: implements
    description: >-
      Selftest exit-3 gate mirrors the same trust-gating pattern as
      directive-rule-sweep's canary.
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

Value-sensitive regex scanner that flags only key-plus-value session adjacencies (Set-Cookie, Authorization with scheme/token, named credential keys, populated localStorage) while passing assurance sentences and public evidence fields. Has a self-test canary gate (exit 3) that refuses to report CLEAN if any fixture fails, mirroring directive-rule-sweep's trust-gating pattern. Deliberately hardened 2026-07-29 to avoid the original word-presence false positive by requiring a known scheme or credential-length opaque token after 'authorization'.

## Related

- implements [[trust-gating-canary-pattern]] — Selftest exit-3 gate mirrors the same trust-gating pattern as directive-rule-sweep's canary.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
