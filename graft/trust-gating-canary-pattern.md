---
name: Trust-gating canary pattern
slug: trust-gating-canary-pattern
type: concept
sources:
  - path: scripts/core/bridge_leak_scan.py
    hash: e5b7b7ecf614217b79e93037d780bdd0314f4953d8e6308939a49fe5b5b92bcf
  - path: scripts/ops/directive-rule-sweep.py
    hash: 7284bd834ff1cf86bcc5f6d104cf23388bf9258dcc827b681f578e6ce7172c57
sources_digest: 9ca63a05e5c3fda207c6f119dc29bde9354e17c28f66d2dcc90d67c3dc0938b1
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
  - symbol: key_phrases
    kind: function
    at: 'scripts/ops/directive-rule-sweep.py:L49-L52'
  - symbol: covered
    kind: function
    at: 'scripts/ops/directive-rule-sweep.py:L55-L68'
---
<!-- context:generated:start -->
## Summary

A cross-cutting invariant: any tool whose correctness is load-bearing must prove itself before being trusted, via an embedded canary fixture that fails the run (exit 3) if the heuristic regresses. Seen in bridge_leak_scan.py's selftest (six positive/two negative fixtures, refuses to report CLEAN on any failure) and directive-rule-sweep.py's zibberflux canary (exits 3 and reports UNKNOWN if not flagged). The pattern prevents a silently-broken checker from being trusted after a regression.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
