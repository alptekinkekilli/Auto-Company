---
name: Session-leak scanning & evidence integrity
slug: session-leak-scanning-evidence-integrity
type: concept
sources:
  - path: scripts/core/bridge_leak_scan.py
    hash: e5b7b7ecf614217b79e93037d780bdd0314f4953d8e6308939a49fe5b5b92bcf
  - path: scripts/core/decision_text_hash.py
    hash: 790b22fa08940d8d4c5418ec441c98f9d119b33eb718b7cfde81c01c71d94922
  - path: scripts/ops/directive-rule-sweep.py
    hash: 7284bd834ff1cf86bcc5f6d104cf23388bf9258dcc827b681f578e6ce7172c57
sources_digest: 73060411436fbe180ce2b7cdfa7e9a860c4cbf430b10ffde948f115f5ff3dbf0
links:
  - to: ki-k-decision-evidence-pipeline
    relation: part_of
    description: >-
      decision_text_hash is the canonical hash used by kik-decision-read and
      written to the bridge; any other hash is not comparable.
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
  - symbol: normalize
    kind: function
    at: 'scripts/core/decision_text_hash.py:L54-L60'
  - symbol: digest
    kind: function
    at: 'scripts/core/decision_text_hash.py:L63-L65'
  - symbol: fetch
    kind: function
    at: 'scripts/core/decision_text_hash.py:L68-L96'
  - symbol: main
    kind: function
    at: 'scripts/core/decision_text_hash.py:L99-L112'
  - symbol: key_phrases
    kind: function
    at: 'scripts/ops/directive-rule-sweep.py:L49-L52'
  - symbol: covered
    kind: function
    at: 'scripts/ops/directive-rule-sweep.py:L55-L68'
---
<!-- context:generated:start -->
## Summary

A cross-cutting trust-gating pattern: value-sensitive scanners (bridge_leak_scan) and content-hash pipelines (decision_text_hash) exist because raw evidence varies by client or contains false-positive-prone prose. Both encode deliberate hardening (authorization matched only with credential-length tokens; normalization order load-bearing) and refuse to report CLEAN/trusted output if a canary fixture fails, so a regression can never silently re-enable a false positive.

## Related

- part of [[ki-k-decision-evidence-pipeline]] — decision_text_hash is the canonical hash used by kik-decision-read and written to the bridge; any other hash is not comparable.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
