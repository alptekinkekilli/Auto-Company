---
name: Content-Hash Provenance
slug: content-hash-provenance
type: concept
sources:
  - path: scripts/core/decision_text_hash.py
    hash: 790b22fa08940d8d4c5418ec441c98f9d119b33eb718b7cfde81c01c71d94922
sources_digest: 837c6e521378bcf965cbfcc5891b481682400ecc60b202a8af12f5fc90600758
links:
  - to: bridge-leak-scanner
    relation: uses
    description: >-
      The leak scanner's public evidence fields like content_hash are validated
      against this canonical hash.
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

The canonical content-hash implementation for KİK decision pages (decision_text_hash.py). Exists because raw HTML from the ASP.NET endpoint varies by client (User-Agent, __VIEWSTATE), making raw-byte hashes unreliable. The normalization pipeline order is load-bearing (drop script/style, replace tags with a single space, unescape entities after tag removal, collapse whitespace). This file is the single source of truth — a hash produced any other way is not comparable and must not be written to the bridge.

## Related

- uses [[bridge-leak-scanner]] — The leak scanner's public evidence fields like content_hash are validated against this canonical hash.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
