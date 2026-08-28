---
name: decision_text_hash
slug: decision-text-hash
type: file
sources:
  - path: scripts/core/decision_text_hash.py
    hash: 790b22fa08940d8d4c5418ec441c98f9d119b33eb718b7cfde81c01c71d94922
sources_digest: 837c6e521378bcf965cbfcc5891b481682400ecc60b202a8af12f5fc90600758
links:
  - to: kik-decision-read
    relation: produces
    description: >-
      kik-decision-read dynamically imports this module to compute the canonical
      hash for comparability with the bridge.
generator:
  version: 1
covers:
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
---
<!-- context:generated:start -->
## Summary

Canonical content-hash for KİK decision pages. Normalization pipeline is load-bearing: decode UTF-8 with replacement, drop script/style, replace tags with single space, unescape entities after tag removal, NBSP→space, collapse whitespace. digest returns first 16 hex of SHA-256 of normalized text + char count. fetch uses urllib with curl fallback (TLS handshake fails on some builds). Single source of truth — any other hash is not comparable and must not be written to the bridge (2026-07-29 incident).

## Related

- produces [[kik-decision-read]] — kik-decision-read dynamically imports this module to compute the canonical hash for comparability with the bridge.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
